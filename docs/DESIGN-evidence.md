# Design: a check must be able to fail

> **This is a decision record, not a user guide.** It exists so a future change knows
> what it would be overturning.

    Status:            Implemented (0.3.x)
    Last revised:      2026-08-30
    Verified against:  Claude Code 2.1.251
    Supersedes:        (none)

## The problem

Three separate engagements shipped a check that could not have caught what it existed to
catch. The checks were written in good faith and all of them looked green.

1. **A gate that was never executed.** A refactor spec claimed invariant 4 was pinned by
   two named test suites. Nothing in the codebase referenced the storage keys involved.
   The kit's rule said characterization tests must "exist and pass"; the reviewer checked
   only that the gate was *stated*. Refactor mode's entire safety story is "behaviour
   cannot break because tests pin it" — asserted pinning protects nothing while looking
   protected, which is worse than no gate.
2. **A mock that agreed with the bug.** postgrad-advisor, 2026-08-29: a streaming filter
   keyed on metadata that never exists at the layer it read from — structurally dead in
   every live run. eng verified the metadata at the wrong layer; qa's test *fabricated*
   the exact metadata its filter expected, so the test could only ever pass. Caught by
   the human driving a live browser.
3. **A suite with no boundary case.** Sandbox, 2026-08-30: `rank()` used `>` where the
   spec required `>=`, and the only test used values nowhere near the boundary. Green
   suite, unmet acceptance criterion.

Same shape each time: the check was structurally incapable of failing.

## The decision

**Nothing counts as evidence until it has been shown capable of producing the opposite
result.** Applied at three points:

- **The refactor gate is executed, not read.** The spec carries an invariant table —
  invariant, pinning test (`file::name`), command, and forced-opposite evidence. The
  tech-lead *runs* every command, *greps the named test* for the symbols the invariant is
  about (a green test that never touches what it claims to pin is a BLOCKER), and checks
  that the test was shown to fail when the behaviour broke. An invariant stated honestly
  as unpinned is a finding to resolve; a plausible mapping that does not execute is the
  failure this lens exists to catch.
- **Verification rejects self-made evidence.** A fixture that constructs the exact data
  shape the code assumes proves consistency, not correctness, and does not count as
  covering the behaviour. Any claim about an *external* system — API shapes, metadata,
  wire formats — needs at least one source the code's author did not construct: a live
  probe with a short timeout, a recorded real payload, or the dependency's own source.
  Where cheap, qa breaks the behaviour and confirms the test fails.
- **Ground truth is verified, not accepted.** Every factual claim in a spec carries a file
  reference and the tech-lead opens the file or runs the grep. A false claim is a BLOCKER,
  because the design was reasoned from fiction.

## Volatile facts

A number is a fact with an expiry date; a command is a fact that stays true. Values that
move while an engagement runs (test counts, coverage, timings) live in a freeze-exempt
**Measurements** table with the command that reproduces each one and an as-of date.
Everywhere else the spec names the measure ("the suite stays green"), never its value.
Updating a measurement is never a scope change and never needs re-sign-off; the
tech-lead re-runs the commands and corrects values in place, and a volatile number found
written outside the table is a finding.

Bought by observation: one engagement's test count changed five times, and a spec saying
"all 323 tests" was stale the moment the next story landed — which then consumed a full
review round to rediscover.

## The kit applies this to itself

The structure tests pinning these rules were each verified by sabotage: the rule was
removed from the source file, the suite was confirmed to fail, and the file restored.
A test asserting a rule exists is worthless if it passes when the rule is deleted.

The same discipline caught a defect in this repo's own tooling on 2026-08-30: a scan for
`SubagentStart` hooks used `grep -rlq`, where `-q` silences `-l`, so it reported zero
matches for every plugin including one already confirmed positive. The published version
of that scan ships with a positive control ([INTERNALS O5](INTERNALS.md)).

## Binds

- Any new gate ships with a demonstration that it can fail.
- Any assertion in `tests/` covering a behavioural rule is sabotage-verified before it
  is trusted.
- qa may fold in external tooling's findings but still writes its own verdict; a clean
  tool result never substitutes for the AC run, the standing-rules check, or these rules.

## Prevents

- Green-suite confidence in an unmet acceptance criterion.
- Mocks that encode the bug they were written to exclude.
- A refactor proceeding on invariants nobody pinned.

## Rejected alternatives

- **Trusting the executor's record.** Section 5 states what was run; qa runs it again.
  The record is a claim, not evidence.
- **Requiring live/unmocked evidence for everything.** Too expensive and often
  impossible. The rule is scoped to claims about *external* systems, which is where
  self-fabricated fixtures are both most tempting and most wrong.
- **A blanket "no mocks" rule.** Mocks are fine; mocks *as the sole evidence for an
  external contract* are not.

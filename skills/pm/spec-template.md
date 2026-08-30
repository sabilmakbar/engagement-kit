# Spec: [engagement name]

| Field | Value |
|---|---|
| Mode | greenfield / feature / refactor / derivative / maintenance |
| Status | draft / in-review / ready / signed-off |
| Date | YYYY-MM-DD |
| Reference project | [derivative mode only — repo/path] |

<!-- Freeze rule: once Status is signed-off, the scope-bearing sections (Problem &
intent, User scenarios, Requirements, Success criteria, Out of scope) are FROZEN.
Amendments happen only as appended Change log entries — never silent edits — and any
entry that changes scope needs fresh user sign-off.
FREEZE-EXEMPT: the Measurements section below. It holds values that legitimately
move while the engagement runs; updating it is never a scope change and never needs
re-sign-off. -->

## Measurements (freeze-exempt)

<!-- Volatile values live HERE and nowhere else. A number that changes when a story
lands (test counts, coverage, file/line counts, timings, row counts) belongs in this
table WITH the command that reproduces it — never inline in a scenario, requirement,
success criterion, or ground-truth row.
Elsewhere in the spec, refer to the measure by name ("the suite stays green",
"coverage does not drop"), never by its value. A frozen number is stale the moment
the next story lands; a command stays true.
Anyone may re-run a command and update its value + date in place. -->

| Measure | Command | Value | As of |
|---|---|---|---|
| [suite size] | `[exact command]` | [value] | YYYY-MM-DD |


## Problem & intent

[2-4 sentences: what the client needs and why, in their domain terms. What "done"
buys them.]

## Ground truth

[Every factual claim about the existing system (or reference project / domain) that
this spec relies on, each with a file reference. The tech lead verifies every row —
write nothing here you haven't seen. Structural facts only: if a claim's truth
depends on a number that moves when a story lands, put the number in Measurements
and cite the measure by name here.]

- `path/file.py:123` — [claim]

## User scenarios

[Prioritized. Each must be independently testable — a scenario that can't be
validated standalone is two scenarios or zero.]

### S1 — [title] (priority: P1)
As a [role], I want [capability], so that [outcome].
**Independent test:** [how this is validated on its own]
**Acceptance:**
- Given [state], when [action], then [result]

## Requirements

- **FR-001** — [functional requirement, one behavior each]

## Success criteria

- **SC-001** — [measurable outcome; a number or a binary check, not a vibe]

## Mode section

<!-- Keep ONLY the block for this engagement's mode; delete the rest. -->

### Greenfield: walking skeleton
Cycle-1 slice (thinnest end-to-end path): [...]. Everything else is deferred to
later cycles and listed under Out of scope.

### Feature: regression surface
Existing behavior at risk: [list, with the tests that currently pin it, or "unpinned —
QA must add"]. Integration points touched: [list].

### Refactor: invariants
Quality attribute being bought: [one].

Behavioral invariants, each mapped to the test that pins it — a claim that an
invariant "is covered" is worth nothing until the mapping is executed:

| # | Invariant | Pinning test (file::name) | Command | Forced-opposite check |
|---|---|---|---|---|
| 1 | [behavior that must not change] | `path::test_name` | `[exact command]` | [how the test was made to FAIL — break the behavior, revert the fix — and confirmed it did] |

**Gate: every row's command RUNS and passes, and every row's pinning test has been
shown to fail when the behavior it pins is broken, before any story crosses its
spec checkpoint.** A test that cannot be made to fail is not a pin. An invariant
with no runnable row is unpinned — say so plainly rather than filling the row with
a plausible guess.

### Maintenance: reproduction & release
Reproduction: [exact steps + evidence — or CANNOT-REPRODUCE and what is missing].
Affected: [versions, machines, sibling artifacts].
Invariant: full regression suite green before and after; only the named behavior
delta changes.
**Gate: a named regression test exists that FAILS on the unfixed code and passes
after the fix.**

| Sibling | Same defect? | Action |
|---|---|---|

Release plan: [patch / minor], executed via the release checklist at close.

### Derivative: delta table
| Item | Disposition | Reason |
|---|---|---|
| [component/behavior] | same / changed / dropped / new | [why — and does the original reason still hold here?] |

**Copy vs. extract decision:** [fork standalone copy | shared core + extensions] —
decided by user on [date]. Rationale: [...]

## Out of scope

[Explicit list. As load-bearing as the requirements.]

## Assumptions & open items

- ASSUMED: [default taken for an unspecified detail]
- [NEEDS CLARIFICATION]: [open question, and who unblocks it]

## Complexity ledger

[Every deviation from the simplest thing that could work, with its justification.
Empty is the goal; unjustified rows are tech-lead findings.]

| Deviation | Justification |
|---|---|

## Change log

[Append-only after sign-off. Never edit frozen sections in place.]

| Date | Section | Change | Reason | Scope change? (needs re-sign-off) |
|---|---|---|---|---|

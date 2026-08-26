# Spec: [engagement name]

| Field | Value |
|---|---|
| Mode | greenfield / feature / refactor / derivative |
| Status | draft / in-review / ready / signed-off |
| Date | YYYY-MM-DD |
| Reference project | [derivative mode only — repo/path] |

<!-- Freeze rule: once Status is signed-off, the scope-bearing sections (Problem &
intent, User scenarios, Requirements, Success criteria, Out of scope) are FROZEN.
Amendments happen only as appended Change log entries — never silent edits — and any
entry that changes scope needs fresh user sign-off. -->


## Problem & intent

[2-4 sentences: what the client needs and why, in their domain terms. What "done"
buys them.]

## Ground truth

[Every factual claim about the existing system (or reference project / domain) that
this spec relies on, each with a file reference. The tech lead verifies every row —
write nothing here you haven't seen.]

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
Quality attribute being bought: [one]. Behavioral invariants that must hold: [list].
**Gate: characterization tests for every invariant exist and pass before any story
crosses its spec checkpoint.**

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

# Story NNN: [title]

<!-- Per-section ownership: PM writes 1-4; the executing session edits 3 and writes 5;
section 6 is written from a fresh context that did NOT execute the story. Nobody edits
another section's content. -->

## 1. Status
`draft | ready | in-progress | in-verification | done`

Two human gates per story — work does not cross an unchecked gate:
- [ ] **spec checkpoint** — user approved this story's scope and ACs before execution
      (refactor mode: characterization tests exist and pass BEFORE this gate)
- [ ] **done checkpoint** — user accepted the result after verification

## 2. Story
As a [role], I want [capability], so that [outcome].

**Acceptance criteria** (from spec `docs/specs/<name>.md`):
1. Given [state], when [action], then [result]

## 3. Tasks
<!-- PM drafts; dev agent refines and checks off. Each task links to an AC. -->
- [ ] [task] (AC 1)

## 4. Dev notes
<!-- The section that makes this story self-contained. A fresh-context agent executes
from THIS FILE ONLY — no chat history, no spec re-read.
Budget: keep this section under ~1,500 tokens (roughly a page). Two subtraction rules:
no verbatim copies from the spec or design docs (distill and cite instead), and
nothing derivable from reading the code at the paths you cite (pointers over prose).
If the section can't fit the budget, the story is too big — split it. Include: -->
- **Files to touch:** `path:line` references
- **Patterns to follow:** [existing code to imitate, with a pointer to an example]
- **Constraints:** [from the spec's mode section — invariants, regression surface]
- **Testing:** [framework, where tests live, what must pass; for refactor mode: which
  characterization tests must stay green]
- **Out of scope for this story:** [...]

## 5. Dev agent record
<!-- Dev agent only. -->
- Completion notes: [...]
- Files changed: [...]
- Decisions made & why: [...]

## 6. Verification results
<!-- Fresh context only (spec + diff, never the executor's chat). Verdict + evidence. -->
- Verdict: `pass | fail`
- Evidence: [test run output summary, what was checked beyond the ACs]
- Findings: [...]

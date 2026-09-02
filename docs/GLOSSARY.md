# Glossary

> **Reference, not a decision record.** Every term the kit's skills, agents, and
> templates actually use. If a term appears in an engagement's output and is not here,
> that is a bug in this file.
>
> Why the design is the way it is lives in the `DESIGN-*.md` records; what the kit
> does lives in the [README](../README.md).

## Roles

| Term | Stands for | What it means here |
|---|---|---|
| **PM** | Product/Project Manager | The interviewing role, run as a skill in your main session (`/pm`). Grounds, interviews, writes the spec and stories, runs the gates. The only role that talks to you. |
| **FDE** | Forward-Deployed Engineer | A flavour applied to the PM, not a separate role: interview like an engineer sitting with the client — ground in the real system first, ask about the actual workflow, refuse to take a feature request at face value. |
| **Tech Lead** | — | Fresh-context reviewer agent. Verifies the spec's facts against the code, then grades the design. Read-only; reviews, never fixes. |
| **eng** | engineer | Fresh-context executor agent. Its entire input is one story file path. Proposes commits, never runs git. |
| **QA** | Quality Assurance | Fresh-context verifier agent. Sees story, spec, and diff — never how the work was done. Writes the verdict. |

**Input contract** — what a role is allowed to see, enforced by the harness rather than
asked for politely. The kit's core bet: eng gets only the story file, so a story that
isn't self-contained fails visibly instead of being quietly rescued by chat history.

**Blinded / asymmetric verification** — QA never receives eng's transcript. It checks
what was done, not what was meant.

## Identifiers you will see in artifacts

| Token | Stands for | Where it lives |
|---|---|---|
| **AC** | Acceptance Criterion | Story section 2. One testable Given/When/Then per line. What QA verifies. |
| **AD** / **AD-n** | Architecture Decision | An entry in `docs/decision-spine.md`. Numbered, never edited, superseded by a new entry. |
| **ADR** | Architecture Decision Record | The industry pattern the spine deliberately departs from — an ADR records history, an AD binds future work. |
| **FR-nnn** | Functional Requirement | Spec. One behavior each. |
| **SC-nnn** | Success Criterion | Spec. A number or a binary check, never a vibe. |
| **S1, S2…** | Scenario | Spec. Each carries a priority `P1`, `P2`… |
| **NNN** | — | Story file numbering: `dev/stories/NNN-<slug>.md`. |
| **O-n** | Observation | An entry in [INTERNALS.md](INTERNALS.md) — undocumented Claude Code behaviour the design rests on. |
| **Base SHA** | — | The git commit recorded by eng before it changes anything. Defines QA's diff scope. |

## Gates and their vocabulary

**Two-key gate** — no checkpoint passes on one signature. Both keys are required and the
machine key turns first.

- **Machine key** — a checklist the PM verifies before it is allowed to ask you
  anything. Red machine key means the ask never happens.
- **Human key** — a standalone question to you, never bundled with open decisions. It
  supplies the one thing a model cannot grant itself.

The gates themselves:

| Gate | Machine key | Human key |
|---|---|---|
| **Direction gate** | — | You approve the approach before any artifact is written. Everything before it is read-only. |
| **Spec sign-off** | Tech Lead verdict READY, no open clarifications, deferred items homed | You confirm scope and intent; the spec then freezes |
| **Spec checkpoint** (per story) | Verdict READY and current, ACs unambiguous | You approve this story's scope and ACs |
| **Done checkpoint** (per story) | QA verdict `pass` — *this alone makes the commits due* | You accept the result; this closes the story and does **not** gate the commit |

**Story status** — `draft` → `ready` → `in-progress` → `in-verification` →
`committed-but-open` → `done`.

**committed-but-open** — verified and landed, still waiting on its human key. A real
state, not a stall: unrelated work commits normally on top of it.

**Standing rules** — the engagement's recorded constraints (live ADs, Dev Notes
invariants, repo conventions). Passing every AC while breaking one of these is a FAIL.

## Verdicts, severities, and triage

**Tech Lead verdict:** `READY` | `NEEDS-REFINEMENT`. READY requires zero BLOCKER/HIGH
findings and zero false ground-truth claims.

**QA verdict:** `pass` | `fail`, plus `needs-human` for criteria a machine cannot judge
(tone, look-and-feel, preference). Those are never auto-passed; they surface verbatim in
the done checkpoint's ask.

**Finding severity:** `BLOCKER` | `HIGH` | `MEDIUM` | `LOW`.

**Triage classes** — every review finding is sorted into exactly one, because each has a
different action:

| Class | Meaning | Action |
|---|---|---|
| `intent_gap` | The spec misread what you want | Re-interview that point; never patch silently |
| `bad_ground` | Reasoned from a false or unverified claim | Re-ground against the code, then amend |
| `patch` | Fixable without changing agreed scope | Fix and resubmit |
| `defer` | Real, but outside this engagement | Log it, then promote or drop at sign-off |
| `reject` | The reviewer is wrong | Record the rebuttal with evidence |

Only `intent_gap` and `bad_ground` earn another review round — those two mean the spec is
*wrong*. The rest is polish.

**Execution failure classes** — separated because they deserve separate budgets:

- **quality-fail** — QA said fail, or you rejected the result. Consumes a fix round.
- **infra-fail** — the run died without ever reaching a verdict (stall, crash, watchdog
  kill). Consumes a retry, not a fix round.

## Evidence

**Ground truth** — the spec's table of factual claims about the existing system, each
with a file reference. The Tech Lead opens every file and runs every grep; a false claim
is an automatic BLOCKER.

**Measurements** — the freeze-exempt table holding volatile values (test counts,
coverage, timings) with the command that reproduces each and an as-of date. A number
written anywhere else in the spec is a finding, because it goes stale the next story.

**Freeze** — after sign-off, scope-bearing spec sections stop being editable. Changes are
appended change-log rows; a row that changes scope needs fresh sign-off.

**Forced-opposite check** — evidence that a test was actually made to fail when the
behaviour broke. A test nobody has seen fail is not yet evidence.

**Characterization test** — a test capturing what the system does *today*, green before a
refactor starts and green after. Refactor mode's entire safety story.

**Self-fabricated fixture** — a fixture that constructs the exact shape the code assumes.
It proves consistency, never correctness, and does not count as covering the behaviour.

**Absence-of-failure evidence** — "had this happened, the fake would have raised". Valid
only while nothing between the call and the assertion can catch. Prefer a positive
assertion on an observable result.

**Evidence coupling** — when widening an exception handler would disarm tests that pin
behaviour by raising. Handler breadth and test evidence are then linked, and the spec has
to say which wins.

## Artifacts

**Decision spine** (`docs/decision-spine.md`) — the anti-relitigation artifact. Each AD
states what it **Binds**, what it **Prevents**, and the **Rule** that makes compliance
checkable. Entries are never edited; a change is a new entry naming what it supersedes.

**memlog** — the append-only log at the foot of the spine recording when each decision
was made or superseded. Turns "we already decided this" into a lookup instead of an
argument.

**Complexity ledger** — the spec's list of every deviation from the simplest workable
design, each with its justification. Unlisted complexity is a finding.

**Delta table** — derivative mode's same / changed / dropped / new breakdown against the
reference project.

**Story file as message bus** — sections are owned: PM writes 1–4, eng writes 3 and 5, QA
writes 6. Nobody edits another's section. Handoffs happen by writing a file.

**Tracked vs untracked** — durable artifacts (spec, spine) belong in git; working state
(`dev/stories/`, deferred work) stays local and gitignored.

## Modes

Every engagement is classified first, because the mode decides which checks apply.

| Mode | Ground truth | Signature risk |
|---|---|---|
| `greenfield` | The domain | Speccing past the walking skeleton |
| `feature` | The repo | An incomplete regression surface |
| `refactor` | The repo + invariants | Invariants nobody actually pinned |
| `derivative` | A reference project | Inherited assumptions nobody re-checked |
| `maintenance` | The shipped artifact + field report | Fixing an unreproduced bug |

**Walking skeleton** — the thinnest end-to-end path through the system, built first.
Horizontal layers are not one.

**Regression surface** — everything existing that a change could break; mapped by
grepping for callers and consumers, not by intuition.

**Blast radius** — maintenance mode's version of the same question: which versions,
machines, and sibling projects the defect reaches.

**Copy vs extract** — derivative mode's named decision: fork a standalone copy, or
extract a shared core with per-use-case extension layers. Always yours to make, never
settled silently.

## Configuration

| Variable | Default | Controls |
|---|---|---|
| `ENGAGEMENT_KIT_FIX_ROUNDS` | 3 | Quality-fail rounds before escalating to you |
| `ENGAGEMENT_KIT_INFRA_RETRIES` | 2 | Infra-fail retries; each must change one named variable |
| `ENGAGEMENT_KIT_NUDGE_GAP` | 14400 (4h) | Idle gap after which the session nudge fires again |

## Outside references

- **BMAD-METHOD** — the agile agent framework several templates were adapted from
  (story format, checklists, triage taxonomy, decision spine shape).
- **spec-kit** — github/spec-kit, source of the spec structure,
  `[NEEDS CLARIFICATION]` markers, and the complexity ledger.
- **ASD-STE100** — Simplified Technical English, the controlled-language standard the
  PM's interview wording rules follow.
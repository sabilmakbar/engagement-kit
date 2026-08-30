# Design: documents as the message bus

> **This is a decision record, not a user guide.** It exists so a future change knows
> what it would be overturning.

    Status:            Implemented (0.3.x)
    Last revised:      2026-08-30
    Verified against:  Claude Code 2.1.251
    Supersedes:        (none)

## The problem

Roles that cannot see each other's context still have to coordinate. The default answer
in multi-agent frameworks is a shared runtime — a task list, a checkpointed state
object, a message bus — which makes coordination easy and makes the work legible only
from inside the framework.

A 2026-08-12 audit of three real projects found the opposite priority. Its failures were
not coordination failures: decisions were relitigated (one convention argued three times
in 24 hours), findings had no home (one repo had opened zero issues in its life while
real findings sat in an untracked local file), and nothing ever froze, so every
convention stayed negotiable.

## The decision

**State lives in durable, human-readable files under the consumer repo. There is no
side-channel.**

| Artifact | Carries | Tracked? |
|---|---|---|
| `docs/specs/<name>.md` | scope, ground truth, Measurements, change log | yes |
| `docs/decision-spine.md` | AD entries (Binds / Prevents / Rule) + memlog | yes |
| `dev/stories/NNN-*.md` | the per-story message bus, strict section ownership | no |
| `dev/deferred-work.md` | findings not taken this engagement | no |

The story file is the bus: PM writes sections 1–4, eng writes 3 and 5, qa writes 6, and
nobody edits another section. Handoffs happen by writing a file, not by passing context.

Bought twice over: it survives session death (a killed eng leaves resume state in
checked boxes and appended notes), and it is readable by a human who was never in any of
the sessions.

## The decision spine

The anti-relitigation artifact, and — per a 2026-08-29 survey of comparable frameworks —
the kit's most distinctive idea. Every ADR system found records decisions
*retrospectively*, as history. An AD here is a *live constraint*: it states what it
Binds, what it Prevents, and the Rule that makes compliance checkable, and the tech-lead
treats a spec contradicting a live AD without superseding it as a BLOCKER.

Entries are never edited. A change is a new entry naming what it supersedes, and the
memlog records the event — so "we already decided this, here is when and why" is a
lookup rather than an argument.

## Tracked versus untracked

Durable artifacts (spec, spine) are git's. Working state (stories, deferred work,
backlog) stays local and gitignored: it churns every session, it is worthless to a
reader who joins after the work, and it accumulates absolute paths, session ids, and
machine names that become permanent the moment a repo is shared.

The test: *would a reader who is not you, and who joins after this work is finished,
still need it?*

One consequence to keep honest: an untracked backlog is exactly where findings die.
Hence the promote-or-drop rule — every open deferred item reaches a durable home (an
issue, or a spec change-log entry) or is explicitly dropped at sign-off — plus a
first-live-bite escalation: a deferred finding that causes real friction even once is
promoted immediately, without waiting for the engagement to close. Bought by
observation: a known bug sat as the oldest item in one kit's backlog until it blocked
its own author, twice.

## Freeze

Once a spec is signed off, its scope-bearing sections are frozen. Amendments are
appended change-log rows, never silent edits, and any row that changes scope needs fresh
sign-off. The Measurements table is explicitly exempt (see
[DESIGN-evidence.md](DESIGN-evidence.md)).

Note this is a deliberate bet *against* the direction github/spec-kit took in its v1.0
("adaptability over frozen specifications"). The kit's position: a spec that can be
quietly rewritten is not something a human key can meaningfully approve. Adaptability is
served by the change log, which keeps the amendment visible and re-approvable.

## Binds

- No coordination mechanism outside these files may be introduced without superseding
  this record.
- Section ownership in story files is absolute; append per round, never overwrite.
- Durable artifacts are prompted for commit at close; if an engagement ends unsigned,
  the PM names which durable artifacts sit uncommitted.

## Prevents

- Coordination state that dies with a session or is legible only to this tooling.
- Decisions surviving only in a transcript, which is what made this kit's own reasoning
  unrecoverable until these records were written.
- Findings with no owner.

## Rejected alternatives

- **A framework-managed shared task list or checkpointed state object** (LangGraph-style,
  or Claude Code's own agent teams). Rejected: the audit's failures were integrity
  failures, not coordination failures, and durable files survive the harness. Also the
  portability argument — the process transfers to any tool that can read and write
  files; a runtime does not.
- **Tracking the backlog and story files.** Rejected on the dev-docs convention: commit
  noise, merge friction, and permanent leakage of local paths and session ids.
- **Retrospective-only ADRs.** Rejected: recording a decision without binding future
  work is what let one convention be argued three times in 24 hours.

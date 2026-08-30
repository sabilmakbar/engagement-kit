# engagement-kit

A thin, mode-aware engagement process for Claude Code: specialized roles built as
skills + subagents, with document handoffs and two-key gates between them.

**Pipeline:** FDE-flavored PM (interactive, main session) → Tech Lead spec review
(fresh-context agent) → per-story execution loop: `eng` (story-file-only executor)
→ `qa` (asymmetric verifier) → two human checkpoints (spec, done), fix rounds
bounded (`ENGAGEMENT_KIT_FIX_ROUNDS`, default 3) → Tech Lead **close review** over
the accumulated diff, catching shape drift no per-story reviewer can see.

**Nobody converses.** Roles exchange only artifacts: eng records design judgement in
the story's section 5, the close review weighs those rationales against the built
code, and neither ever reads the other's transcript. Written judgement travels;
live advocacy does not.

**Roles are input contracts, not personas.** A 2026-08-12 gap audit rejected
dev/QA personas: observed failures were process failures, never missing roles.
SUPERSEDED 2026-08-28, evidence: the first full consumer engagement
(postgrad-advisor) stalled exactly at execution — stories written for an executor
and verifier that existed only as prose, so every consumer session had to
improvise them, unenforced. v0.3 ships `eng` and `qa` as **enforcement agents**:
eng receives ONLY the story file (self-containment becomes load-bearing), qa
receives only story+spec+diff (verification is asymmetric by construction).
What the audit rejected — role-play characters and chat handoffs — stays
rejected; these are the kit's two oldest rules turned into mechanisms.

## The five modes

Every engagement is classified first; the mode decides which checklists apply and
which artifacts the engagement actually earns.

| Mode | Ground truth | What's distinctive |
|---|---|---|
| `greenfield` | The domain: replaced workflows, external systems, comparable products | Walking skeleton first; loop in slices — never spec the whole product in one pass |
| `feature` | The repo | Regression surface must be mapped; the pipeline's sweet spot |
| `refactor` | The repo + invariants | PM pins what quality attribute is being bought; characterization tests must pass before any story's spec checkpoint |
| `derivative` | A reference project (sibling repo) | Spec is a delta (same/changed/dropped/new); copy-vs-extract is a named user decision; carried-over assumptions get audited |
| `maintenance` | The shipped artifact + the field report | Reproduce first; everything-but-the-bug frozen; sibling parity checked; ends with the release checklist (tag=release=manifest=payload, dogfood install) |

## Layout

```
.claude-plugin/        # plugin + marketplace manifests (incl. nudge hook wiring)
skills/pm/             # /pm — interview + spec authoring (SKILL.md + templates)
agents/                # tech-lead (spec reviewer), eng (executor), qa (verifier)
hooks/                 # session-start engagement nudge (UserPromptSubmit)
tests/                 # structure tests: python3 -m unittest discover tests
```

## Install

As a Claude Code plugin:

```
/plugin marketplace add sabilmakbar/engagement-kit
/plugin install engagement-kit@engagement-kit
```

From a local clone, use the clone path instead:
`/plugin marketplace add /path/to/engagement-kit`, then the same install command.

The skill arrives namespaced (`engagement-kit:pm`) and works in every project — no
per-project copying. In the target project, run `/pm` and add `dev/` to that
project's `.gitignore` (the skill reminds you). The nudge hook fires on a session's
first message (or after a 4h gap; tune with `ENGAGEMENT_KIT_NUDGE_GAP` seconds) and
suggests classifying new work through `/pm`; it stays quiet otherwise.

## Why it is built this way

Design decisions live in `docs/`, not in anyone's memory:

- [DESIGN-roles.md](docs/DESIGN-roles.md) — roles as input contracts; why PM is a skill
  and the rest are agents; what the "no personas" position did and did not supersede.
- [DESIGN-gates.md](docs/DESIGN-gates.md) — two-key gates, the direction gate, loops
  bounded by finding class, and why artifacts scale but gates never do.
- [DESIGN-evidence.md](docs/DESIGN-evidence.md) — a check must be able to fail:
  executed refactor gates, rejected self-made evidence, volatile facts.
- [DESIGN-artifacts.md](docs/DESIGN-artifacts.md) — documents as the message bus, the
  decision spine, tracked versus untracked, freeze.
- [INTERNALS.md](docs/INTERNALS.md) — undocumented Claude Code behaviour the design
  rests on, each entry with how to re-check it.

## Artifact policy

- **Tracked** (durable, describes the system): `docs/specs/*.md`,
  `docs/decision-spine.md` (AD-n entries with Binds/Prevents/Rule + append-only
  memlog — the anti-relitigation artifact).
- **Untracked** (working state): `dev/stories/`, `dev/deferred-work.md`, interview
  notes, verification reports. Deferred items must be promoted to a durable home
  (issue or spec change-log entry) or explicitly dropped at engagement sign-off.
  Add to the project's `.gitignore` before the first commit:

  ```gitignore
  dev/
  ```

## Roadmap

1. ✅ PM skill + tech-lead reviewer, with the five adopted artifacts (triage
   taxonomy, context budget + subtraction rules, frozen sections + change log,
   asymmetric reviewer, decision spine)
2. Pilot: one small feature-mode engagement on a low-stakes personal repo — never
   on live, shared tooling
3. Shake out refactor + derivative mode checklists with one engagement each
4. Out of scope, needs separate work: repo versioning/releases, cross-kit parity,
   concurrent writers on one repo, a per-repo state command

## Provenance

Templates adapted from BMAD-METHOD v4.44.3 (story format, PM/architect checklists,
including its "AI agent implementability" review category) and github/spec-kit
(spec structure, `[NEEDS CLARIFICATION]` markers, complexity justification ledger).
From BMAD v6: the review-finding triage taxonomy with a bounded loop, the Dev Notes
token budget with subtraction rules, frozen sections + append-only change log, the
architecture decision spine (AD-n with Binds/Prevents/Rule + memlog), and per-story
spec/done checkpoints. The four-mode skeleton and FDE interviewing behavior are this
kit's own; the no-personas stance comes from a gap audit of three real multi-session
projects.

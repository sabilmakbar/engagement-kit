# dev-pipeline-kit

A thin, mode-aware development pipeline for Claude Code: specialized roles built as
skills + subagents, with document handoffs between them.

**Pipeline:** FDE-flavored PM (interactive, main session) → Tech Lead review
(fresh-context agent) → per-story build loop with two human checkpoints (spec, done)
and fresh-context verification.

**Deliberately no dev/QA personas.** A gap audit over three real multi-session
projects found the failures were stale state, unowned findings, and unfrozen
conventions — never missing roles — while context handoffs between agents were
themselves a failure mode. The PM and Tech Lead survive because they are artifacts
(the interview; the information-asymmetric reviewer), not org chart. Revisit only
with new evidence.

## The four modes

Every engagement is classified first; the mode decides which checklists apply and
which artifacts the engagement actually earns.

| Mode | Ground truth | What's distinctive |
|---|---|---|
| `greenfield` | The domain: replaced workflows, external systems, comparable products | Walking skeleton first; loop in slices — never spec the whole product in one pass |
| `feature` | The repo | Regression surface must be mapped; the pipeline's sweet spot |
| `refactor` | The repo + invariants | PM pins what quality attribute is being bought; characterization tests must pass before any story's spec checkpoint |
| `derivative` | A reference project (sibling repo) | Spec is a delta (same/changed/dropped/new); copy-vs-extract is a named user decision; carried-over assumptions get audited |

## Layout

```
.claude-plugin/        # plugin + marketplace manifests
skills/pm/             # /pm — interview + spec authoring (SKILL.md + templates)
agents/tech-lead.md    # fresh-context spec reviewer, read-only tools
tests/                 # structure tests: python3 -m unittest discover tests
```

## Install

As a Claude Code plugin:

```
/plugin marketplace add sabilmakbar/dev-pipeline-kit
/plugin install dev-pipeline@dev-pipeline
```

From a local clone, use the clone path instead:
`/plugin marketplace add /path/to/dev-pipeline-kit`, then the same install command.

The skill arrives namespaced (`dev-pipeline:pm`) and works in every project — no
per-project copying. In the target project, run `/pm` and add `dev/` to that
project's `.gitignore` (the skill reminds you).

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

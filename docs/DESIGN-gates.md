# Design: gates, keys, and bounded loops

> **This is a decision record, not a user guide.** It exists so a future change knows
> what it would be overturning.

    Status:            Implemented (0.3.x)
    Last revised:      2026-08-30
    Verified against:  Claude Code 2.1.251
    Supersedes:        (none)

Assumes the role model in [DESIGN-roles.md](DESIGN-roles.md).

## The problem

Checkpoints are cheap to write and easy to render meaningless. Two failure modes were
observed, not imagined:

1. **The unanswerable ask.** 2026-08-13, the bounce estate engagement: the PM asked
   "sign off the spec?" in the same dialog as three open scope decisions. The answer
   adjusted scope instead of confirming it — correctly refused as a sign-off — and the
   engagement stalled unsigned for six days. A gate the user cannot cleanly answer is
   not a gate.
2. **The gate asked too early.** The same engagement changed scope *after* a READY
   verdict, with a review round still unused. Approval was sought while the machine-side
   preconditions were red.

## The decision: two keys, in order

Every gate needs a **machine key** and a **human key**, and the machine key turns first.

- **Machine key** — a checklist the PM verifies before it is allowed to ask anything:
  reviewer verdict READY and still current (no scope edits since), zero open
  `[NEEDS CLARIFICATION]`, deferred items homed, `dev/` gitignored, spine current, every
  state claim re-measured live rather than recalled, and — for CI/release-touching work
  — CI status fetched green, because local runs are not CI.
- **Human key** — a standalone ask, never batched with open decisions, presenting the
  mode, scope in one paragraph, settled decisions, explicit out-of-scope, and the
  machine checklist shown green. An answer that adjusts scope is not a sign-off:
  incorporate, re-run the machine key, ask again.

Gates: **spec checkpoint** and **done checkpoint** per story, plus spec sign-off for the
engagement. The done checkpoint's machine key is qa's `pass` verdict from a fresh
context; ACs a machine cannot judge (tone, feel) are marked `needs-human` and surface
verbatim in the ask rather than being auto-passed.

## The direction gate

Everything before it is read-only. The PM closes the interview with a short plan in chat
— approach, rejected alternatives, what it touches — and gets explicit approval before
writing any artifact. Recorded as the engagement's first AD.

Bought by observation: on 2026-08-13 the PM recommended a direction that contradicted a
recorded user preference, and the correction arrived only after grounding and planning
were complete — a full re-ground cycle. A wrong direction costs one message here and an
engagement's work later.

## Bounded loops, budgeted by class

Loops end by **evidence, not arithmetic**.

- **Spec review**: stop as soon as a round produces no `intent_gap` and no `bad_ground`
  findings — the two triage classes meaning the spec is wrong. Rounds returning only
  `patch`/`defer`/`reject` are polish and do not earn another pass. Hard ceiling 3.
  Bought by observation: a round 3 cost ~80k tokens and ten minutes to surface only
  stale numbers and off-by-one line references.
- **Story fix rounds**: classify the eng outcome first. *quality-fail* (qa fail or user
  reject) consumes `ENGAGEMENT_KIT_FIX_ROUNDS` (default 3); *infra-fail* (stall, crash,
  watchdog kill — the run died with no verdict on the work) consumes a separate
  `ENGAGEMENT_KIT_INFRA_RETRIES` (default 2), and every retry must change one named
  variable. Bought by observation: postgrad's story 007 stalled three times with zero
  quality failures, and each stall burned a fix round it had not earned.

## Scaling

**Artifacts scale with the engagement; gates never do.** A single change earns one story
and no separate spine file; an engagement with nothing deferred writes no deferred-work
file. What never scales down: grounding before interviewing, the direction gate, ground
truth and Measurements, the tech-lead review, both keys at both checkpoints, blinded
verification.

Bought by observation (~900 lines of artifacts for ~300 lines of code in one small
engagement) and constrained by a competitive read on 2026-08-29: gate and spine
integrity are the only properties this kit has that comparable frameworks do not. A
light mode that thins documents is fine; one that thins gates deletes the product.

## Binds

- No gate may be presented while its machine key is red.
- Sign-off asks are never batched with anything.
- Scope-bearing amendments after a READY verdict re-open review, or are presented as
  explicitly unreviewed.

## Prevents

- Approval-by-momentum: a user saying "yes" to a bundle they cannot decompose.
- Counters standing in for judgement about whether more review is warranted.
- Infra flakiness consuming a budget meant for genuine quality failures.

## Rejected alternatives

- **One human approval per engagement** — too coarse: the observed friction was 59 bare
  "yes"/"do it" messages precisely because approval sat at the wrong granularity.
- **Auto-pass on a green machine key** — deletes the human key, which is the one thing a
  model cannot grant itself and (per the 2026-08-29 competitive read) the kit's most
  defensible property.
- **A round counter as the primary stop condition** — kept only as a ceiling; see above.

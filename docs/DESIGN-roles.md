# Design: roles as input contracts

> **This is a decision record, not a user guide.** It exists so a future change knows
> what it would be overturning. For what the kit does, read the README.

    Status:            Implemented (0.3.x)
    Last revised:      2026-08-30
    Verified against:  Claude Code 2.1.251
    Supersedes:        the 2026-08-12 "no dev/QA personas" position (see below)

Read this record first. It sets the one-skill-three-agents shape the other records
assume rather than restate.

## The problem

A development process needs a planner, a reviewer, an implementer, and a verifier. The
obvious implementation is four personas — prompts that describe how each behaves. That
is what most frameworks in this space ship, and it does not work by itself: a persona
is a description, so nothing stops the "verifier" from having watched the "implementer"
work, and nothing stops the "implementer" from filling gaps in its brief with context
the brief never contained.

## The decision

**A role is defined by what it can see, not by how it is told to behave.** Each role's
value comes from an input restriction that the harness enforces:

| Role | Surface | Input it is given | The property that buys |
|---|---|---|---|
| pm | skill | the user's session, the repo, memories, the spine | can interview (O3) |
| tech-lead | agent | spec path + mode; or, at close, spec + spine + accumulated diff + section-5 rationales | judges artifacts, never the author's narrative |
| eng | agent | ONE story file path, nothing else | makes story self-containment testable |
| qa | agent | story + spec + diff | verification cannot be contaminated by how the work was done |

The behavioural prose in each agent file is secondary. If it were deleted, the input
contracts would still deliver most of the value; if the input contracts were relaxed,
no amount of prose would restore it.

## Why PM is a skill and the rest are agents

Not a style choice — a constraint. [INTERNALS O3](INTERNALS.md): a subagent has no
`AskUserQuestion` and no way to block on a human reply. The PM's whole job is
interviewing, so it must run in the user's own session, where questions are possible.
tech-lead, eng, and qa never need an answer mid-task, so they can be agents and gain
fresh context in exchange.

Consequence to respect: **any future role that must ask the user something cannot be an
agent.** If the kit ever wants an interactive reviewer, it becomes a skill or it does
not exist.

## What was superseded, and why

On 2026-08-12 a gap audit over three real multi-session projects concluded: the observed
failures were stale state, unowned findings, and unfrozen conventions — never missing
roles — and context handoffs between agents were themselves a failure mode. The kit
recorded "deliberately no dev/QA personas; revisit only with new evidence."

The evidence arrived on 2026-08-28. The first full consumer engagement
(postgrad-advisor) ran the paper half cleanly — interview, spec, two review rounds,
sign-off — and then stalled at execution: the stories were written for an executor and
a verifier that existed only as prose, so the session had to improvise both, with
nothing checking what either could see.

The supersession is narrow and the distinction is the whole point:

- **still rejected** — role-play characters, personas as flavour, chat handoffs between
  agents, an org chart;
- **now shipped** — two input contracts that make the kit's two oldest written rules
  ("a fresh agent executes from this file alone", "a different fresh agent verifies")
  mechanical instead of aspirational.

The audit rejected theatre. These are locks.

## Binds

- Every role's prompt states its complete input; adding "helpful extra context" to eng
  or qa breaks the property the role exists for and must be treated as a defect.
- No agent instruction may name a specific tool ([INTERNALS O1](INTERNALS.md), O2):
  declared allowlists are an upper bound, and skills are unreachable from an agent.
  Describe capabilities instead.
- eng proposes commits and never executes git; approval is a human's or a git guard's.
- qa writes only story section 6; eng writes only sections 3 and 5; neither checks a
  checkpoint box.

## Prevents

- A verifier that "already knows" what the implementer intended.
- An executor that repairs an incomplete story from memory, hiding the incompleteness.
- Roles multiplying: a new role must justify itself by a new *input restriction*, not by
  a new job title.

## Rejected alternatives

- **Personas without input restrictions** — the pre-0.3 state. Rules were true only when
  a session chose to honour them; postgrad showed they were not honoured by default.
- **A live eng↔tech-lead conversation at close** (proposed 2026-08-29). Rejected: the
  reviewer's value is that it never hears the builder's defence. A conversation is
  precisely the rationalisation channel the blinding exists to close, and eng agents are
  terminated by close anyway. Judgement travels through section 5; advocacy does not
  travel at all.
- **QA as a skill** — would inherit the calling session's context, destroying asymmetry.
- **Agent teams / peer messaging between roles** — evaluated 2026-08-11 and again as
  agent teams matured. Rejected while the roles were still being tuned: it confounds
  "the playbook is wrong" with "the coordination layer is wrong", and costs a full
  session per role. Reconsider only if document handoffs prove to be the bottleneck.

## Known weakness

Input contracts are a convention this kit keeps, not a sandbox it enforces.
[INTERNALS O5](INTERNALS.md): another plugin's `SubagentStart` hook injects into these
agents regardless (ponytail's build persona reached both eng and qa on 2026-08-30). Both
agents handled it sensibly, but that was judgement, not enforcement. A plugin cannot
block another plugin's hook; the mitigation available is an explicit precedence sentence
in each agent, which is open in the backlog.

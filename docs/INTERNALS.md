# Claude Code internals, as observed

> **This file is about Claude Code, not about this kit.** It records undocumented
> behaviour the kit's design rests on. The decisions these observations drove belong in
> `DESIGN-*.md` records, which cite them by number. For what the kit does, read the
> README.

    Observed against:   Claude Code 2.1.251
    Platform:           macOS 24.5.0, VS Code extension
    Last re-verified:   2026-08-30
    Needs to re-run:    a live session (O1–O4 need the Agent tool and this kit
                        installed); jq/python3 and read access to ~/.claude/plugins
                        for O5–O8; nothing special for O9–O11

Nothing here is promised by Anthropic. Every entry states how it was checked, so it can
be re-run rather than believed. A claim is not evidence until something ran — the same
rule the kit imposes on its own agents.

```bash
# which observations a script can re-check
awk '/^### O/{o=$2} /Checkable: +automated/{print o}' docs/INTERNALS.md
```

---

### O1 — A subagent's tool schema can be narrower than its declared allowlist

`agents/qa.md` declares `tools: Read, Grep, Glob, Bash, Edit`, and the harness's agent
registry echoes all five. The resolved runtime schema held **three**: `Read`, `Bash`,
`Edit`. Grep and Glob are dropped somewhere between definition and resolution.

Confirmed by attempt, not by recall, with a positive control: the agent could not emit
a `Grep` call (unrepresentable, so no error text exists to quote), then ran
`grep -rn "def rank" /private/tmp` through `Bash` with the same arguments and got
matches at exit 0. The search capability is present; only the dedicated tool is absent.
Two independent live runs the same day used shell `grep`/`find` throughout, consistent
with this.

Treat a declared allowlist as an upper bound, not a guarantee. Never write an agent
instruction that *names* a tool; describe the capability ("search the repo") so the
agent reaches it by whatever surface actually materialized. Restrictions still hold in
the safe direction — nothing appeared that was not declared.

    Checkable:      manual (spawn the agent; have it ATTEMPT the tool, and run the
                    same operation via Bash as a control)
    First observed: 2026-08-30, 2.1.251 (probed twice; second probe attempted rather
                    than recalled, and reversed nothing)
    Depended on by: every agent instruction in agents/ — none names a tool

### O2 — Subagents have no Skill tool; skills are unreachable from an agent

A restricted subagent cannot invoke a skill at all: `Skill` is absent from its schema,
so the call is unrepresentable rather than refused — there is no error text to catch.
Confirmed by probe and by two live runs that never attempted one.

This is what makes the kit's tool-agnosticism structural rather than stylistic: an
agent cannot reach `/code-review`, `ponytail`, `caveman`, or any other plugin skill,
so instructions phrased around shell-level tooling are the only ones that can work.

    Checkable:      manual (probe an agent; ask it to invoke any skill)
    First observed: 2026-08-30, 2.1.251
    Depended on by: qa's capability-first review-tooling clause; the kit's
                    portability claim

### O3 — Subagents cannot ask the human anything

No `AskUserQuestion` or equivalent in a subagent's schema. A subagent's only channel to
a person is its final message, which is one-way — it cannot block on a reply.

**This is the reason the kit's shape is one skill and three agents.** The PM interviews,
so it must be a skill running in the user's own session; tech-lead, eng, and qa never
need an answer mid-task, so they can be agents. Any future role that must ask something
cannot be an agent.

    Checkable:      manual (probe an agent)
    First observed: 2026-08-30, 2.1.251
    Depended on by: PM-as-skill; qa's `needs-human` findings surfacing in the written
                    verdict instead of a question; both human keys living with the PM

### O4 — A restricted subagent cannot spawn subagents

No `Agent`/`Task` tool in the probed schema, so a restricted agent cannot fan out. (An
unrestricted agent can; the nesting limit is separate and not measured here.)

    Checkable:      manual (probe an agent)
    First observed: 2026-08-30, 2.1.251
    Depended on by: eng's contract — it cannot delegate its way around an incomplete
                    story file, which is what makes story self-containment testable

### O5 — Another plugin's SubagentStart hook injects into YOUR subagents

Hooks are environment-level, not plugin-scoped. `ponytail` registers a `SubagentStart`
hook; its build-shaped persona ("PONYTAIL MODE ACTIVE") was injected into both
`engagement-kit:eng` and `engagement-kit:qa` at launch, and both reported it unprompted.
No other installed plugin registers one.

An input contract is therefore a *convention this kit keeps*, not a sandbox it enforces:
a plugin cannot block another plugin's hook. Agents should state precedence explicitly
rather than trusting judgement.

```bash
for m in ~/.claude/plugins/marketplaces/*/; do
  printf '%s: %s\n' "$(basename "$m")" "$(grep -rl SubagentStart "$m" 2>/dev/null | wc -l)"
done
# control: SessionStart must match in every plugin, else the scan itself is broken
```

    Checkable:      automated
    First observed: 2026-08-30, 2.1.251 (ponytail 4 files; all others 0, control passes)
    Depended on by: the open backlog item adding a precedence sentence to each agent

### O6 — The plugin cache is keyed by version string

Installs land in `~/.claude/plugins/cache/<marketplace>/<plugin>/<version>/`. Two
different contents cannot coexist under one version, and a same-version update has no
distinct path to land in.

Consequence the kit follows: never re-content a released version. Ship 0.3.2 rather than
re-cutting 0.3.1. (Caveman sidesteps this by using a commit SHA as its version string —
`cache/caveman/caveman/0d95a81d35a9/` — which makes every sync a distinct version.)

    Checkable:      automated (`ls -d ~/.claude/plugins/cache/*/*/*/`)
    First observed: 2026-08-26, 2.1.251
    Depended on by: the release-checklist invariant "payload edit forces a version bump"

### O7 — A local directory is a valid marketplace source

`plugin marketplace add <path>` records `{"source": "directory", "path": ...}` and serves
the plugin from a working checkout, with no remote involved. This is how the kit ships
pre-release builds to one machine while the remote tag stays behind.

    Checkable:      automated (read ~/.claude/plugins/known_marketplaces.json)
    First observed: 2026-08-29, 2.1.251
    Depended on by: the local-ship channel used for the unreleased 0.3.1

### O8 — Plugin skills and agents are namespaced `plugin:name`

An installed plugin's skill invokes as `/engagement-kit:pm` and its agents register as
`engagement-kit:eng` / `:qa` / `:tech-lead`. The bare name usually resolves too, when
nothing else claims it. Renaming the plugin renames the namespace, so any instruction
naming an agent must say the namespaced form or describe it.

    Checkable:      automated (the agent registry lists namespaced types)
    First observed: 2026-08-19, 2.1.228 · re-verified 2026-08-30, 2.1.251
    Depended on by: SKILL.md Step 5's spawn instructions

### O9 — A UserPromptSubmit hook's stdout is injected as instruction-bearing context

Text a `UserPromptSubmit` hook prints reaches the model as additional context for that
turn and is acted on like an instruction. The kit's nudge hook relies on this: it prints
one paragraph on a session's first message (or after `ENGAGEMENT_KIT_NUDGE_GAP`), and it
is a nudge — the model may decline, so nothing may depend on compliance.

    Checkable:      manual (open a fresh session; the nudge appears once)
    First observed: 2026-08-26, 2.1.251
    Depended on by: hooks/engagement-nudge.sh

### O10 — The `claude` CLI may be absent from PATH; it ships inside the VS Code extension

In this environment `claude` is not on PATH. The binary lives at
`~/.vscode/extensions/anthropic.claude-code-*-darwin-arm64/resources/native-binary/claude`
(take the newest by version sort). Plugin install/update from a session must use that
path or fail with `command not found`.

    Checkable:      automated (`command -v claude || ls ~/.vscode/extensions/...`)
    First observed: 2026-08-19, 2.1.228 · still true 2026-08-30, 2.1.251
    Depended on by: docs/PLUGINIZE-style install steps; every plugin update run here

### O11 — Resuming an agent by id preserves its context

Sending a message to a completed agent's id resumes it from its transcript rather than
starting fresh, so prior findings and reasoning survive. Observed repeatedly: research
agents resumed days later answered follow-ups without re-reading their sources.

    Checkable:      manual (resume an agent; ask about something only its earlier run saw)
    First observed: 2026-08-18, 2.1.228 · re-verified 2026-08-30, 2.1.251
    Depended on by: the fix-round rule that resumes the same eng rather than spawning
                    a fresh one — with story write-through (O4's sibling constraint)
                    as the fallback when resume is unavailable

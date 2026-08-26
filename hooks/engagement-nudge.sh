#!/usr/bin/env bash
# UserPromptSubmit hook: on the FIRST message of a session, or the first after a
# long idle gap, inject a nudge to classify new work via the pm skill. Quiet on
# every other message. Never blocks: every exit path is 0.
set -u

GAP="${ENGAGEMENT_KIT_NUDGE_GAP:-14400}"   # seconds; 4h default
STATE_DIR="${HOME}/.claude/engagement-kit/seen"
# ponytail: state files never pruned — one tiny file per session, revisit if it ever matters

input=$(cat 2>/dev/null || true)
sid=$(printf '%s' "$input" | sed -n 's/.*"session_id"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' | head -1)
if [ -z "$sid" ]; then
  echo "engagement-kit nudge degraded: no session_id in hook input"
  exit 0
fi

mkdir -p "$STATE_DIR" 2>/dev/null || exit 0
state="$STATE_DIR/$sid"
now=$(date +%s)

nudge=0
if [ ! -f "$state" ]; then
  nudge=1
else
  last=$(cat "$state" 2>/dev/null || echo 0)
  case "$last" in ''|*[!0-9]*) last=0 ;; esac
  if [ $((now - last)) -gt "$GAP" ]; then nudge=1; fi
fi
printf '%s' "$now" > "$state" 2>/dev/null

if [ "$nudge" = 1 ]; then
  cat <<'MSG'
engagement-kit: first message of this session (or first after a long gap). If this message opens NEW work — building, fixing, refactoring, or scoping something — invoke the engagement-kit:pm skill (Step 0: classify the mode) before free-forming. Quick questions and continuations of existing work: proceed normally and ignore this note.
MSG
fi
exit 0

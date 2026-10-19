---
name: resume-session
description: "Reconstruct working context at the start of a new session. Reads STATE.md + HANDOFF.md (if present) + latest 3 T##-SUMMARY.md files and synthesizes a 'where we are' briefing. Run at session start before doing anything else."
tier: core
version: 0.1.0
allowed-tools:
  - Bash
  - Read
triggers:
  - resume session
  - where were we
  - pick up where I left off
  - ytstack resume
---

# resume-session

Quick-orient at session start. Reads the on-disk state and produces a 3-paragraph briefing the user can scan in 10 seconds. Complements the SessionStart hook (which auto-injects on every session start) by giving the user an on-demand, richer version.

## Anti-Pattern: "I'll just read the files myself"

You'll read STATE.md and think you have the picture, missing HANDOFF.md's in-flight note, the most recent task summary, or the REVIEW-NOTES item that's about to bite. This skill composes all of them. Takes 5 seconds. Run it every session start.

## Checklist

1. **Run preamble** -- detect state + gather file inventory
2. **HARD-GATE** -- ytstack initialized
3. **Synthesize briefing** -- 3 paragraphs: where, in-flight, next
4. **Report** -- done

## Preamble

```bash
_PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$PWD}"
cd "$_PROJECT_DIR" 2>/dev/null || true
_PROJECT_SLUG=$(basename "$(git rev-parse --show-toplevel 2>/dev/null)" 2>/dev/null || basename "$(pwd)")
if [ -d "$_PROJECT_DIR/.ytstack" ]; then _YT_DIR="$_PROJECT_DIR/.ytstack";
elif [ -d "$HOME/.ytstack/projects/$_PROJECT_SLUG" ]; then _YT_DIR="$HOME/.ytstack/projects/$_PROJECT_SLUG";
else _YT_DIR=""; fi
_HAS_YTSTACK=$([ -n "$_YT_DIR" ] && echo yes || echo no)

_STATE_FILE="$_YT_DIR/STATE.md"
_HANDOFF_FILE="$_YT_DIR/HANDOFF.md"
_HAS_HANDOFF=$([ -f "$_HANDOFF_FILE" ] && echo yes || echo no)

# Last 3 summaries by mtime
_RECENT_SUMMARIES=""
if compgen -G "$_YT_DIR"/*-SUMMARY.md > /dev/null 2>&1; then
  _RECENT_SUMMARIES=$(ls -t "$_YT_DIR"/*-SUMMARY.md 2>/dev/null | head -3)
fi

echo "HAS_YTSTACK: $_HAS_YTSTACK"
echo "STATE_FILE: $_STATE_FILE"
echo "HAS_HANDOFF: $_HAS_HANDOFF"
echo "RECENT_SUMMARIES_COUNT: $(echo "$_RECENT_SUMMARIES" | grep -c .)"
```

## Procedure

**Step 2 HARD-GATE.** If `HAS_YTSTACK=no`:
> "ytstack isn't initialized in this project. If you expected state here, check the path. Otherwise run `/ytstack:init-project`."
STOP.

**Step 3 -- Synthesize briefing.** Read each of:
- `STATE.md` (frontmatter + Status + Next action sections)
- `HANDOFF.md` if present (In-flight, Next action, Open decisions, Warnings)
- Each file in `_RECENT_SUMMARIES` (Outcome first lines)

Produce a three-paragraph briefing:

**Paragraph 1 -- Where we are:** project name, milestone/slice/task position, branch, last-updated timestamp. Include scope (project vs user) if relevant.

**Paragraph 2 -- Most recent work:** Summarize the 3 latest task summaries in one or two sentences each. Focus on *outcomes*, not process. If no summaries, note "no tasks closed yet in this project."

**Paragraph 3 -- Next:** The STATE.md's Next action, enriched with HANDOFF.md's In-flight / Open decisions / Warnings if they exist and are non-empty. End with a concrete first suggested action.

**Formatting:**

```
=== ytstack resume briefing ===

**Where:** {one paragraph}

**Recent:** {one paragraph}

**Next:** {one paragraph}

---
Files read: STATE.md{, HANDOFF.md if present, <N> summary files}
To go deeper: read ROADMAP.md for the big picture, DECISIONS.md for locked choices, REVIEW-NOTES.md for deferred items.
```

**Step 4 -- Report.** Emit the briefing above. No further action -- return control so the user decides what to do next.

## Terminal State

Return after emitting the briefing. Do NOT invoke any other skill. The user (or the next-action-decider) takes over from here.

## Why this exists alongside the SessionStart hook

The SessionStart hook fires automatically on every session start and injects a compressed state summary via `additionalContext`. That's lightweight and always-on.

This skill is the **deep-dive**. When the user explicitly asks "where were we", they want the richer version: HANDOFF.md context, full recent-summary outcomes, open-decision highlights. The hook can't prompt -- this skill can. Use both.

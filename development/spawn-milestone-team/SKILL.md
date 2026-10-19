---
name: spawn-milestone-team
description: "Dispatch the current milestone's slices to a Claude Code Agent Team. Each teammate works on a slice in parallel with its own 200k context (replaces GSD's fresh-subprocess-per-task pattern). Requires CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1 and v2.1.32+. Run after slice-milestone + plan-eng-review."
tier: task
version: 0.1.0
allowed-tools:
  - Bash
  - Read
  - AskUserQuestion
triggers:
  - spawn team
  - dispatch milestone
  - agent team
  - parallel slice execution
  - ytstack team
---

# spawn-milestone-team

Ask Claude Code to create an Agent Team for the current milestone. Each teammate gets a slice. Teammates work in parallel with isolated contexts, coordinate via the shared task list. This is ytstack's answer to GSD's fresh-subprocess-per-task model -- we use Claude Code's native Agent Teams feature instead of building our own runtime.

## Prerequisites

- `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` set in shell or settings.json
- Claude Code v2.1.32 or later
- Current milestone has sliced plans (`M###-S##-PLAN.md` exists for each slice)
- Milestone has passed `plan-eng-review` (recommended -- catches architecture issues before parallel work starts)

## Anti-Pattern: "Just execute the slices sequentially myself"

That works. Agent Teams add coordination overhead and token cost. Use sequential execution when:
- Slices have heavy cross-dependencies
- The milestone is small (M or S -- 1-3 slices)
- You want tight human oversight per slice

Use Agent Teams when:
- Slices are genuinely independent (no file overlap, no cross-references)
- You want to step away and let work run
- The milestone is L (4-5 slices)

## Checklist

1. **Run preamble** -- detect Agent Teams capability + milestone state
2. **HARD-GATE** -- env var + version + slice-plans present
3. **Check slice independence** -- warn if slices overlap files
4. **Ask team size** -- typically one teammate per slice, with architect-reviewer override
5. **Construct team spawn instruction** -- natural-language prompt Claude will execute
6. **Emit instruction** -- Claude takes over from there
7. **Do not block** -- Agent Teams are long-running; this skill completes quickly

## Preamble

```bash
_PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$PWD}"
cd "$_PROJECT_DIR" 2>/dev/null || true
_PROJECT_SLUG=$(basename "$(git rev-parse --show-toplevel 2>/dev/null)" 2>/dev/null || basename "$(pwd)")
if [ -d "$_PROJECT_DIR/.ytstack" ]; then _YT_DIR="$_PROJECT_DIR/.ytstack";
elif [ -d "$HOME/.ytstack/projects/$_PROJECT_SLUG" ]; then _YT_DIR="$HOME/.ytstack/projects/$_PROJECT_SLUG";
else _YT_DIR=""; fi
_HAS_YTSTACK=$([ -n "$_YT_DIR" ] && echo yes || echo no)

_CURRENT_MILESTONE=none
[ -f "$_YT_DIR/STATE.md" ] && _CURRENT_MILESTONE=$(sed -n 's/^current_milestone: *//p' "$_YT_DIR/STATE.md" | head -1)

_SLICE_PLANS=""
if [ -n "$_CURRENT_MILESTONE" ] && [ -d "$_YT_DIR" ]; then
  _SLICE_PLANS=$(ls "$_YT_DIR"/$_CURRENT_MILESTONE-S[0-9][0-9]-PLAN.md 2>/dev/null)
fi

_SLICE_COUNT=$(echo -n "$_SLICE_PLANS" | grep -c . 2>/dev/null || echo 0)

# Agent Teams enabled?
_AT_ENABLED=$([ "${CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS:-}" = "1" ] && echo yes || echo no)

# Claude Code version (v2.1.32+ required)
_CC_VERSION=$(claude --version 2>/dev/null | head -1 | awk '{print $1}')
_VERSION_OK=no
if [ -n "$_CC_VERSION" ]; then
  # Parse major.minor.patch and compare to 2.1.32
  IFS='.' read -r MAJ MIN PAT <<< "$_CC_VERSION"
  if [ "${MAJ:-0}" -gt 2 ] || { [ "${MAJ:-0}" -eq 2 ] && [ "${MIN:-0}" -gt 1 ]; } || { [ "${MAJ:-0}" -eq 2 ] && [ "${MIN:-0}" -eq 1 ] && [ "${PAT:-0}" -ge 32 ]; }; then
    _VERSION_OK=yes
  fi
fi

echo "HAS_YTSTACK: $_HAS_YTSTACK"
echo "CURRENT_MILESTONE: $_CURRENT_MILESTONE"
echo "SLICE_COUNT: $_SLICE_COUNT"
echo "AGENT_TEAMS_ENABLED: $_AT_ENABLED"
echo "CC_VERSION: ${_CC_VERSION:-unknown}"
echo "VERSION_OK: $_VERSION_OK"
```

## Procedure

**Step 2 HARD-GATE.**

- `HAS_YTSTACK=no` → abort
- `CURRENT_MILESTONE=none` → abort "run plan-milestone first"
- `SLICE_COUNT=0` → abort "run slice-milestone first -- no slice-plans found"
- `AGENT_TEAMS_ENABLED=no` → abort "set `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` in your env or `settings.json` then restart Claude Code"
- `VERSION_OK=no` → abort "Claude Code v2.1.32+ required. Current: {CC_VERSION}. Upgrade before running this skill."

**Step 3 -- Check slice independence.** Read each slice-plan's Files section. Compare across slices. If two slices touch the same file path:

Report:
> Slice overlap detected:
> - {path} touched by: {slice1}, {slice2}
>
> Running these in parallel risks merge conflicts. Consider:
> - Sequential execution (skip this skill, run `plan-task` + `test-driven-development` per slice)
> - Re-slice to separate the overlapping files (re-run `slice-milestone`)
> - Explicitly accept the risk -- the last writer wins, earlier changes may need manual merge

Use AskUserQuestion:
> A) Accept risk, spawn team anyway (Completeness: 6/10, risk: medium)
> B) Stop, re-slice first (Completeness: 10/10)
> C) Stop, execute sequentially instead (Completeness: 10/10)

If B or C: STOP.

**Step 4 -- Ask team size.** Use AskUserQuestion:

> Milestone **{CURRENT_MILESTONE}** has {SLICE_COUNT} slice(s). Team size?
>
> RECOMMENDATION: A -- one teammate per slice plus an architect-lead reviewer gives best coverage without excessive coordination overhead.
>
> A) {SLICE_COUNT} implementers + 1 architect-reviewer. (Completeness: 10/10)
> B) {SLICE_COUNT} implementers only -- no reviewer. (Completeness: 8/10, cheaper)
> C) Fewer teammates than slices -- one teammate picks up multiple slices sequentially. (Completeness: 10/10, slower but token-cheaper)
> D) Custom count -- I'll specify. (Completeness: 10/10)

Remember as `_TEAM_CONFIG`.

**Step 5 -- Construct spawn instruction.** Build natural-language for Claude:

```
I want to dispatch milestone {CURRENT_MILESTONE} of project {PROJECT_NAME} to an Agent Team.

Create a team with {TEAM_SIZE} teammate(s) using these roles:
{If architect-lead:} - 1 architect-lead: reviews plans before each teammate starts implementation. Uses the `architect` subagent type if defined, else fresh session with plan-approval mode.
{For each slice:}
- 1 implementer: works on slice {SLICE_ID}. Task list from {SLICE_PLAN_PATH}. Use subagent type `implementer` if defined, else fresh session.

Shared task list: derive from M###-ROADMAP.md slices + per-slice T## task lists.

Each teammate MUST:
1. Read `.ytstack/STATE.md`, `.ytstack/DECISIONS.md`, `.ytstack/KNOWLEDGE.md`, and their slice plan before claiming a task
2. Use `ytstack:plan-task` (already-shipped skill) if they need to elaborate a task
3. Use `ytstack:test-driven-development` for implementation
4. Use `ytstack:verification-before-completion` before marking a task complete
5. Use `ytstack:summarize-task` to close each task
6. NOT invoke `ytstack:reassess-roadmap` mid-slice -- that's for the lead after slice completes

Lead (main session) coordinates, checks teammate progress, assembles findings. When all slices are complete, lead runs `ytstack:reassess-roadmap` and reports back.

Non-interactive mode: teammates have YTSTACK_NON_INTERACTIVE=1 in their environment to prevent AskUserQuestion from blocking.

Start when I say "go".
```

**Step 6 -- Emit.** Present the instruction to the user:

> Ready to spawn team for **{CURRENT_MILESTONE}** ({TEAM_SIZE} teammates).
>
> Instruction preview (this will be sent to Claude next):
>
> ---
> {instruction block above}
> ---
>
> Say "go" to dispatch, or "cancel" to stop. If "go", Claude will create the team; from that point, you can monitor teammates via Shift+Down cycling or split panes.

Wait for user confirmation. If "go", the user sends the instruction as their next prompt; Claude then invokes Agent Teams. This skill does not directly invoke the Agent Teams API -- Claude owns that.

**Step 7 -- Report + return.**

> Team spawn instruction emitted. Claude will execute on your "go".
>
> Expected behavior:
> - Lead creates `~/.claude/teams/ytstack-{CURRENT_MILESTONE}/` with config
> - Task list lives at `~/.claude/tasks/ytstack-{CURRENT_MILESTONE}/`
> - Teammates self-claim tasks, report via mailbox
> - ytstack hooks (`task-created`, `task-completed`, `teammate-idle` -- shipped in M006) react to team events
>
> Monitor with Shift+Down (cycle teammates) or check `/plugin status` if split panes enabled.

## Terminal State

Return after emitting the spawn instruction. Do NOT try to invoke Agent Teams directly -- Claude owns that API through the team-lead role. Do NOT invoke downstream skills; the teammates will handle their own lifecycle via the M003 skills.

## Limitations

- **Experimental API.** Agent Teams API may change in future Claude Code versions. Pin Claude Code version in deployments.
- **No session resume.** Claude Code's current Agent Teams cannot resume in-process teammates after `/resume`. If the main session reloads, the lead may message dead teammates. Workaround: tell the lead to spawn replacements.
- **One team per session.** The lead can only manage one team at a time. Clean up before spawning another.
- **Lead is fixed.** The session that creates the team IS the lead for its lifetime. You can't hand off leadership.
- **Permission mode.** Teammates start with the lead's permission mode. Pre-approve common operations before spawning or you'll hit friction.

See `.ytstack/REVIEW-NOTES.md` for open integration concerns.

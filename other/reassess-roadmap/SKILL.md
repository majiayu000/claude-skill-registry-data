---
name: reassess-roadmap
description: "After a slice completes, review whether the milestone roadmap still fits reality. Reads recent summaries, surfaces deviations, prompts for roadmap changes (add/split/reorder/remove slices). Run at slice boundaries, not mid-slice."
tier: task
version: 0.1.0
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - AskUserQuestion
triggers:
  - reassess roadmap
  - review milestone plan
  - ytstack reassess
---

# reassess-roadmap

Post-slice checkpoint. Looks at what was learned during the slice and asks whether the milestone roadmap still matches reality. Often the answer is yes -- but when it's no, catching it here is cheap; catching it at milestone-end is expensive.

## When to run

- After `ytstack:summarize-task` closes the **last** task of a slice
- Before picking the next slice to plan/execute
- NOT mid-slice -- in-flight changes scatter the plan

## Anti-Pattern: "The plan was right, no need to reassess"

Run it anyway. It takes 2 minutes and either confirms the plan (good -- more confidence) or surfaces a gap the next slice would have hit blind (much better -- save a slice of wasted work). The value isn't in changing the plan -- it's in knowing whether to change it.

## Checklist

1. **Run preamble** -- detect milestone + just-completed slice
2. **HARD-GATE** -- slice must be fully complete (all tasks `[x]`)
3. **Summarize the slice** -- show outcomes of the N task summaries
4. **Ask: does the remaining roadmap still fit?**
5. **If no, prompt for changes** -- add / split / reorder / remove slices
6. **Update `M###-ROADMAP.md`** with agreed changes
7. **Append decision to `M###-CONTEXT.md`** if the change is non-trivial
8. **Update STATE.md** -- flip completed slice, set next `active_slice` (guarded)
9. **Backlog sweep** (only if this was the last slice of the milestone) -- per-item prompt from `M###-CONTEXT.md` scope

## Preamble

```bash
_PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$PWD}"
cd "$_PROJECT_DIR" 2>/dev/null || true
_PROJECT_SLUG=$(basename "$(git rev-parse --show-toplevel 2>/dev/null)" 2>/dev/null || basename "$(pwd)")
if [ -d "$_PROJECT_DIR/.ytstack" ]; then _YT_DIR="$_PROJECT_DIR/.ytstack";
elif [ -d "$HOME/.ytstack/projects/$_PROJECT_SLUG" ]; then _YT_DIR="$HOME/.ytstack/projects/$_PROJECT_SLUG";
else _YT_DIR=""; fi
_HAS_YTSTACK=$([ -n "$_YT_DIR" ] && echo yes || echo no)

_NON_INTERACTIVE=false
if [ -n "$YTSTACK_NON_INTERACTIVE" ] || [ -n "$OPENCLAW_SESSION" ] || [ -n "$CLAUDE_AGENT_TEAM_MEMBER" ]; then
  _NON_INTERACTIVE=true
fi

_CURRENT_MILESTONE=none; _ACTIVE_SLICE=none
if [ -f "$_YT_DIR/STATE.md" ]; then
  _CURRENT_MILESTONE=$(sed -n 's/^current_milestone: *//p' "$_YT_DIR/STATE.md" | head -1)
  _ACTIVE_SLICE=$(sed -n 's/^active_slice: *//p' "$_YT_DIR/STATE.md" | head -1)
fi

# Determine if the current slice is complete
_SLICE_PLAN="$_YT_DIR/$_CURRENT_MILESTONE-$_ACTIVE_SLICE-PLAN.md"
_SLICE_COMPLETE=no
if [ -f "$_SLICE_PLAN" ]; then
  _REMAINING=$(grep -c '^- \[ \]' "$_SLICE_PLAN" 2>/dev/null || echo 0)
  [ "$_REMAINING" -eq 0 ] && _SLICE_COMPLETE=yes
fi

echo "HAS_YTSTACK: $_HAS_YTSTACK"
echo "YTSTACK_NON_INTERACTIVE: $_NON_INTERACTIVE"
echo "CURRENT_MILESTONE: $_CURRENT_MILESTONE"
echo "ACTIVE_SLICE: $_ACTIVE_SLICE"
echo "SLICE_COMPLETE: $_SLICE_COMPLETE"
```

## Procedure

**Step 2 HARD-GATE.** If `SLICE_COMPLETE=no`: abort with "slice still has open tasks. Close them via `summarize-task` before reassessing."

**Step 3.** Collect recent summaries: read all `{MILESTONE}-{SLICE}-T##-SUMMARY.md` files. For each, extract Outcome + Deviations. Present to user:

> Slice **{CURRENT_MILESTONE}-{ACTIVE_SLICE}** complete. Here's what shipped:
>
> {For each task summary:}
> - **T##:** {OUTCOME_FIRST_LINE} (deviations: {DEVIATIONS_SHORT})

**Step 4.** Use AskUserQuestion:

> Given what actually shipped, does the remaining roadmap for **{CURRENT_MILESTONE}** still fit reality?
>
> Look at the next slice in `{CURRENT_MILESTONE}-ROADMAP.md`. Does it still make sense given what you learned in this slice?
>
> RECOMMENDATION: A if nothing surprised you. B if one or two surprises. C if you feel "we should reconsider the whole plan."
>
> A) Yes, proceed as planned. (Completeness: 10/10)
> B) Partial changes needed -- add / split / reorder a slice. (Completeness: 8/10)
> C) Major rethink -- the milestone scope or goal shifted. (Completeness: 10/10 for doing the rethink honestly)

If A: jump to Step 8.
If B: Step 5.
If C: prompt "Should we go back to `/ytstack:plan-milestone` to re-define the milestone? The C option means the current roadmap is stale enough to rebuild." Ask user; if yes, STOP and recommend rerun. If they want to patch in place, proceed to Step 5.

**Step 5.** For B: use AskUserQuestion (open-ended):

> What needs to change in the roadmap?
>
> Describe changes in plain English. Examples:
> - "Add a new slice S04 between S02 and S03 for rate-limiting -- surfaced during S02."
> - "Remove S03 -- turns out what we did in S02 covered it."
> - "Split S03 into S03a (schema change) and S03b (UI update) -- too big for one slice."

Remember as `_CHANGES`.

**Step 6.** Apply changes to `{CURRENT_MILESTONE}-ROADMAP.md` via Edit tool. For each change:
- Add: insert a new `- [ ] S## -- {name}` line at the correct position, increment `total_slices` frontmatter
- Split: replace one slice line with two, increment `total_slices`
- Remove: delete line, decrement `total_slices`
- Reorder: move lines (preserve checkbox state)

If slices beyond the modified ones have placeholder task lists, leave them -- `slice-milestone` will handle re-planning.

**Step 7.** If the change was non-trivial (B or C): append to `{CURRENT_MILESTONE}-CONTEXT.md`:

```markdown
## Reassessment {ISO_TIMESTAMP}

After **{ACTIVE_SLICE}**, changed the roadmap:

{CHANGES}

Reason: {USER_REASON_IF_PROVIDED}
```

**Step 8.** Update STATE.md:

If `YTSTACK_NON_INTERACTIVE` is `false` (i.e. `CLAUDE_AGENT_TEAM_MEMBER` is unset):
- Flip `active_slice` from completed slice to the next unfinished slice (next `- [ ] S##` in ROADMAP), or `active_slice: none` if no unfinished slice remains
- `active_task: none`

If `YTSTACK_NON_INTERACTIVE` is `true` (running as swarm teammate): skip frontmatter writes. Log:
> `[ytstack:reassess-roadmap] skipping STATE.md active_slice/active_task write -- running as swarm teammate (CLAUDE_AGENT_TEAM_MEMBER set)`

Regardless of teammate mode:
- Bump `last_updated`
- Status line: `**Status:** {CURRENT_MILESTONE} -- slice {OLD_SLICE} complete. Next slice: {NEW_ACTIVE_SLICE}.`

Also flip `- [ ] {OLD_SLICE}` → `- [x] {OLD_SLICE}` in `{CURRENT_MILESTONE}-ROADMAP.md` and bump `completed_slices`.

**Step 9. Backlog sweep** (only if this was the last slice of the milestone -- no remaining `- [ ] S##` in ROADMAP).

Read `{CURRENT_MILESTONE}-CONTEXT.md`. Extract any backlog items listed under a "Backlog" or "Deferred" heading (pattern: lines starting with `- ` under such a heading). If none found, skip this step and report "no backlog items found."

For each backlog item, use AskUserQuestion (multi-choice):

> Wrapping up **{CURRENT_MILESTONE}** -- sweeping backlog item: "{ITEM_DESCRIPTION}"
>
> This item was deferred into {CURRENT_MILESTONE} scope but not scheduled in any slice. Now that the milestone is done, decide its fate.
>
> RECOMMENDATION: A if the item shipped as part of normal work. B if it is genuinely needed but needs more work. C if it no longer applies.
>
> A) Fully shipped -- delete this item from the backlog. (Completeness: 10/10, tier: task)
> B) Still needed -- trim to what remains and carry forward to the next milestone's CONTEXT.md. (Completeness: 8/10, tier: task)
> C) Drop it -- not worth doing. Add a one-line DECISIONS.md note explaining why. (Completeness: 7/10, tier: task)

For A: remove the item from the backlog section in `{CURRENT_MILESTONE}-CONTEXT.md`.
For B: prompt "What is still needed? (one sentence)" then update the item text in `{CURRENT_MILESTONE}-CONTEXT.md` and copy the trimmed item to the next milestone CONTEXT.md (append under a "Carried from {CURRENT_MILESTONE}" heading) once the next milestone exists.
For C: remove the item from `{CURRENT_MILESTONE}-CONTEXT.md` and append to `DECISIONS.md`:

```markdown
## {ISO_DATE}: Drop backlog item "{ITEM_DESCRIPTION}" from {CURRENT_MILESTONE}

**Context:** item was deferred into {CURRENT_MILESTONE} but not executed.
**Chose:** drop
**Reason:** {USER_REASON}
```

## Report + return

> Slice **{OLD_SLICE}** closed, roadmap reassessed: {A/B/C outcome}.
>
> {If B/C:} Changes logged to `{CURRENT_MILESTONE}-CONTEXT.md` under "Reassessment {TIMESTAMP}".
>
> Next: slice **{NEW_ACTIVE_SLICE}**. Run `/ytstack:plan-task` to flesh out the first task, or use subagent dispatch if available.
>
> If this was the last slice of the milestone: flip milestone status to `done` in `.ytstack/ROADMAP.md` (global) and consider `/ytstack:plan-milestone` for the next milestone.

## Terminal State

- Return after ROADMAP + STATE + (optional) CONTEXT updates + (optional) backlog sweep
- Abort if slice not complete (Step 2 HARD-GATE)
- Abort + recommend rerun if user picks "major rethink, restart milestone"

Do NOT auto-invoke `plan-task` or `plan-milestone`.

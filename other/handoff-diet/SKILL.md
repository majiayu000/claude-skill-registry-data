---
name: handoff-diet
description: Meta-skill codifying the no-wakeup-polling pattern. Describes the ScheduleWakeup anti-pattern, the fix (--auto merge + detached watcher), and when to still use wakeups. Reduces handoff spam by 80%.
type: skill
triggers:
  - handoff pattern
  - wakeup anti-pattern
  - handoff diet
---

# handoff-diet

Handoffs burn turns. Wakeups amplify the burn. This skill documents the pattern that eliminates them.

## The anti-pattern: ScheduleWakeup poll loop

```
1. Push PR with 10-minute CI wait
2. ScheduleWakeup(600)   ← "check back in 10 min"
3. On wakeup: "PR still pending, re-check in 5 min"
4. ScheduleWakeup(300)
5. ...repeat 6–8 times...
```

**Cost**: Each wakeup = 1 handoff + 1 compaction cycle. Over 6 wakeups: 12 turns burned on status polling.

## The fix: `gh pr merge --auto` + detached watcher

GitHub has native auto-merge. Use it.

```bash
# Instead of ScheduleWakeup:
gh pr merge <N> --repo owner/repo --squash --delete-branch --auto

# Optional: detached background watcher (for visibility)
(
  while gh pr view <N> --json mergeStateStatus | grep -q BLOCKED; do
    sleep 30
  done
  # Once merged, do post-merge actions (log, bump version, etc.)
) &
disown
echo "Auto-merge queued; you can move on"
```

**Cost**: 0 wakeups, 0 handoffs, 0 turns burned. Merge happens when CI passes.

## When to use auto-merge (no wakeup needed)

- PR has green CI or is 1 rebase away from green
- You trust the test suite (no runtime surprises expected)
- Post-merge cleanup is automated (e.g. auto-bump version, auto-deploy)
- You're moving to the next task and don't need to monitor this one

## When to still use ScheduleWakeup (model action required)

- PR merge is blocked by **human review** (code-review gate)
- PR has **merge conflict** that needs resolution (not just rebase)
- You're waiting for **model-generated changes** to be pushed (agent is working on something)
- You're debugging a **flaky test** and need to see the result immediately

**Rule of thumb**: Use wakeups only for tasks that require **model decision-making**. Don't use wakeups for **status polling** (GitHub polls for you with --auto).

## Implementation details

### `auto-ship` skill (canonical implementation)

```bash
gh pr merge "$pr_num" \
  --repo "$owner/$repo" \
  --squash \
  --delete-branch \
  --auto
```

See `~/.claude/skills/auto-ship/SKILL.md` for full details.

### `prod-rebuild` skill (detached watcher pattern)

```bash
nohup (
  # Build runs in bg
  docker compose build ... &
  BUILD_PID=$!
  
  # Wait for build to finish
  wait $BUILD_PID
  
  # Restart container
  docker rm -f bot && docker compose up -d bot
  
) > /tmp/build.log 2>&1 &
```

Returns immediately. Build + restart completes in bg without blocking session.

## Principles

1. **CI is not a model**: GitHub's merge queue handles CI status, not you.
2. **Detached watchers are free**: Use them for visibility, not blocking.
3. **Wakeups are expensive**: Every wakeup = 1 turn + 1 compaction. Avoid.
4. **One wakeup per task max**: If you must wakeup, do it once and move on.

## Related skills

- `auto-ship` — the pattern in action
- `version-bump` — uses --auto merge internally
- `prod-rebuild` — detached watcher pattern for long-running builds

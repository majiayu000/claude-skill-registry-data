---
name: tracking-technical-debt
description: Use when you notice code problems while working on something else - links code markers to beads so issues don't get lost. Triggers on "I see a problem but can't fix it now."
version: 2.0.0
---

# Tracking Technical Debt

## The Trigger

**Use this skill when you think:** "I noticed something that needs fixing, but I can't/shouldn't fix it now."

Examples:
- "This loop is O(n²) but I'm here to fix a bug"
- "This should be configurable but I'm shipping MVP"
- "This validation is duplicated in 3 places"
- "This is a hack that should be cleaned up later"

**If you notice it and don't track it, it will be forgotten.**

## The Rule

**Every noticed problem gets one of two treatments:**
1. **Fix it now** (if < 5 minutes and isolated)
2. **Track it** (bead + code marker)

**There is no third option.** "I'll remember" is not tracking. "TODO comment" is not tracking. Mental notes are not tracking.

## Quick Workflow

```bash
# 1. Create bead (captures the issue)
bd create "O(n²) loop in auth validator needs optimization" --labels debt

# 2. Add code marker (links code to bead)
# In src/auth/validator.ts:45
// DEBT[bd-xxxx]: O(n²) loop - should use Set for O(n) lookup
```

That's it. Two steps. Under 2 minutes.

## When to Track vs Fix Immediately

| Situation | Action |
|-----------|--------|
| < 5 min fix, isolated, obvious | Fix now |
| Would derail current work | Track |
| Needs design discussion | Track |
| Part of larger refactoring | Track |
| Security vulnerability | **Fix now or escalate immediately** |
| Broken tests | **Fix now** |
| Build failures | **Fix now** |

## The Code Marker Pattern

Format: `DEBT[bead-id]: Brief description`

```go
// DEBT[bd-1234]: Cache stampede possible under high load
func (m *Manager) Get(key string) ([]byte, error) {
```

```python
# DEBT[bd-5678]: Should batch these database calls
for item in items:
    db.save(item)
```

```typescript
// DEBT[bd-9012]: Duplicated validation - also in user.ts and admin.ts
function validateEmail(email: string) {
```

**Why the marker matters:**
- `rg "DEBT\["` finds all debt in codebase
- `rg "bd-1234"` finds specific issue in code AND tracker
- When you fix the issue, you know to remove the marker

## Batching Small Issues

**Multiple tiny issues in one file?** Batch them:

```bash
# One bead for the file
bd create "Clean up minor issues in format.ts" --labels debt,cleanup \
  --description "- Line 23: rename x to formattedValue
- Line 45: remove unused import
- Line 67: existing TODO needs proper tracking"
```

```typescript
// At top of file or near first issue:
// DEBT[bd-3456]: Multiple minor cleanup items - see issue for list
```

**Batching is fine for:**
- Multiple issues in same file
- Related issues in same module
- Tiny issues (< 2 min each) that share context

**Don't batch:**
- Unrelated issues across codebase
- Issues with different priorities
- Issues that might be fixed at different times

## Rationalization Table

| Excuse | Reality |
|--------|---------|
| "Too small to track" | Small issues accumulate. Track it or fix it. No middle ground. |
| "I'll remember" | No you won't. You'll context-switch and forget. Track it. |
| "Overhead exceeds the work" | 2 minutes to track vs hours of rediscovery later. Track it. |
| "Just a TODO comment" | TODO comments are graffiti. They don't get fixed. Use beads. |
| "I'll create the issue later" | Later never comes. Context is hot NOW. Track it now. |
| "It's not really technical debt" | If it needs fixing and you're not fixing it now, it's debt. Track it. |

## Red Flags - STOP If You Think This

- "This is too minor to bother with" → Track it or fix it
- "I'll definitely remember this" → You won't. Track it.
- "A TODO comment is good enough" → It's not. Use beads.
- "I'll batch these up and create issues at the end" → Context fades. Track now.
- "The bead overhead isn't worth it" → 2 minutes now vs forgotten forever

## Finding Debt

```bash
# All debt markers in codebase
rg "DEBT\[" .

# Specific issue
rg "bd-1234" .

# All tracked debt in beads
bd list --label debt

# Debt analytics (if using bv)
bv --robot-priority  # What debt is most impactful?
```

## Closing Debt

When you fix the issue:

1. Remove the `DEBT[bd-xxxx]` marker from code
2. Close the bead: `bd close bd-xxxx -r "Fixed in commit abc123"`

Both steps. Don't leave orphaned markers or open beads.

## Integration with Workflows

**During implementation:** Notice problem → track it → continue your work

**During code review:** Reviewer spots debt → create bead + marker

**Sprint planning:** `bd list --label debt` → prioritize what to address

**Before major features:** Check debt that might block or complicate the work

## Summary

1. **Notice problem** while working on something else
2. **Decide:** Fix now (< 5 min) or track
3. **If tracking:** `bd create` + `DEBT[bd-xxxx]` marker
4. **Continue** your original work
5. **Later:** Fix debt, remove marker, close bead

**The discipline:** If you see it and don't track it, you've chosen to forget it.

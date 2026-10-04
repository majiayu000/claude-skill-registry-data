---
name: geass-lock
description: "One-Shot Constraint Lock — user invokes with a constraint phrase; that constraint becomes absolutely inviolable for the session, visible in the brain block on every turn, not overridable by any advisor. Auto-expires at session end. Single active lock per session. Use when the user says '/geass', 'lock this constraint', or 'make this inviolable'."
triggers:
  - /geass
  - /yuri-geass
scope: harness
invocation: workflow
---

# Geass (ギアス) — One-Shot Constraint Lock

**Source anime:** Code Geass — Lelouch vi Britannia's Geass gives him the "Power of Absolute Obedience." Anyone who meets his gaze must obey any one command, unconditionally and permanently — but only once per person. After it fires, the effect is irreversible.

**Cognitive translation:** The user can lock one behavioral constraint as absolutely inviolable for the current session. Once locked, no reasoning path, complexity escalation, or advisory output can override it. It is visible in the brain block on every turn. At session end, the lock automatically expires (one session = one Geass).

The constraint is a hard gate — not a preference, not a guideline. It fires before any other logic.

---

## When This Fires

- User explicitly invokes: `/geass <constraint phrase>`
- Example: `/geass "no commits until tests pass"`
- Example: `/geass "all file writes require explicit user confirmation"`
- Example: `/geass "stay inside _SYSTEM/ this session — no .claude edits"`

---

## Constraints on the Lock

- **One lock per session.** If a lock is already active, `/geass` surfaces the active constraint and offers to replace it (requires explicit "yes").
- **Must be actionable.** The constraint must be checkable by Musubi before any relevant tool call.
- **Auto-expires.** Lock is written with the current session_id. When session_id changes, lock is ignored.
- **User-revocable.** `/geass off` or `/geass clear` removes the active lock.

---

## Execution Steps

### On `/geass <constraint>`

1. Parse constraint from the invocation arguments
2. Check for existing lock in `.claude/yuri-sentinel/geass/active-lock.json`
   - If exists: surface current lock, ask for replacement confirmation
   - If none: proceed
3. Write lock file (create `.claude/yuri-sentinel/geass/` if absent — this is the exact path brain-inject.js reads):
```json
{
  "constraint": "<exact phrase>",
  "locked_at": "<ISO timestamp>",
  "session_id": "<from session-state.json>",
  "active": true,
  "invoked_by": "user"
}
```
4. Emit brain:stale sentinel — next turn will reload brain with GEASS_LOCK section visible
5. Confirm lock to user in one line

### On every subsequent turn (enforcement)

brain-inject.js reads `.claude/yuri-sentinel/geass/active-lock.json`:
- If `active: true` AND `session_id` matches: inject `### GEASS_LOCK` into brain block
- Before any tool call that could violate the constraint: gate fires a WARN or BLOCK

### On session end / `/geass off`

Set `active: false` in the lock file. Do not delete — audit trail.

---

## brain-inject.js Integration

`loadGeassLock()` function reads lock file, checks session_id, injects:

```
### GEASS_LOCK — Active constraint (inviolable)
🔴 "<constraint phrase>"
Locked: <timestamp> | Expires: session end
All advisors and tool calls subject to this constraint.
```

---

## Output Format

```
⬡ GEASS — Constraint locked

🔴 "<constraint>"

This constraint is now inviolable for this session.
No reasoning path, advisory output, or complexity escalation can override it.
Auto-expires at session end. Use /geass off to remove early.
```

---

## Enforcement Examples

| Constraint | Enforcement point |
|------------|------------------|
| "no commits until tests pass" | Before any `git commit` |
| "all file writes need confirmation" | Before any Write/Edit tool call |
| "stay inside _SYSTEM/, no .claude edits" | Before any Write/Edit outside `_SYSTEM/` |
| "no new LaunchAgents this session" | Before any launchctl or plist write |

---

## Session Notes

### 2026-06-09
- session: 123m | peak ctx: 40% | compacts: 0
- tools: Bash×1003, Read×158, WebSearch×38, StructuredOutput×35, Edit×16, Write×11, WebFetch×10, ToolSearch×4, Workflow×3, TaskOutput×1, AskUserQuestion×1
- corrections: none
- errors: none

### 2026-05-16 — Created
Tools: Write. Part of Musubi Hyper-Intelligence v2 sprint.
Anime source: Code Geass — Lelouch's Geass introduced in Episode 1. The "once per person" constraint is what makes it precious and irreversible. R2 Episode 21: Lelouch Geasses the entire world.
Translation principle: The single-use constraint maps to session scope — you get one lock, it matters, it's visible, it expires. The "absolute obedience" maps to the non-overridable gate. The cost is that you must use it wisely — a bad constraint lock can be as limiting as helpful.

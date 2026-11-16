---
name: status
description: "Report aigent-OS operational status. Use when checking the current operational state of aigent-OS."
---

# /status — aigent-OS operational status

Read computed runtime state and display a concise operational summary. Under 12 lines.

## Trigger

`/status` — user-facing command. Also available to the AIgent internally.

## Flow

1. Run `python3 "$AIGENT_VAULT/daemons/runtime/update-active-state.py"` to refresh state
2. Read `$AIGENT_VAULT/memory/runtime/ACTIVE_STATE.json`
3. Format and display:

```
Mode:       {mode}
Objective:  {current_objective or "none"}
Next:       {next_valid_action or "none"}
Pressure:   context {p.context}, memory {p.memory}, token {p.token}
Capsule:    {active_capsule.id or "none"} ({active_capsule.status})
Blocked:    {count} items
Gaps:       {count} open skill gaps
Reflexes:   {list of true reflexes, or "none"}
```

4. If any reflexes are true, add a line: `Reflex: {reflex} — {action hint}`
   - should_capsule → "Context pressure high — capsule recommended"
   - should_digest → "Memory backlog >30 — /digest recommended"  
   - should_skill_hunt → "Open skill gaps — /skill-hunt queued"
   - should_close → "Session >2hr — consider /close"
   - should_escalate → "Blocked items — escalation needed"

## Output format

Keep it tight. Terminal-style. No prose. No headers. Just the state.

## Example

```
Mode:       active
Objective:  Build runtime state layer
Next:       Wire /open and /close to read ACTIVE_STATE
Pressure:   context low, memory medium, token low
Capsule:    2026-05-08-session38-close (active)
Blocked:    0 items
Gaps:       0 open
Reflexes:   digest — Memory backlog >30
```

## Related

- `memory/runtime/ACTIVE_STATE.json` — the state this reads
- `memory/runtime/README.md` — schema docs
- `daemons/runtime/update-active-state.py` — the computer
- `/body-check` — deeper vital signs (somatic layer)
- `/open` and `/close` — compute state as part of session lifecycle

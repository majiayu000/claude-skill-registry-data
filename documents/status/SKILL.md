---
name: status
description: Use this skill when the user asks "where am I", "what's the current task", "what's blocking me", "show status", "what needs sign-off", or "what's next". Prints a snapshot of the active plan, gate, sign-off progress, and next action. Reads only — writes nothing.
next_suggestions:
  - when: no_active_work
    suggest: "run /start to begin a new task, or /plan if you already know what to build"
  - when: pending_signoff_for_current_user
    suggest: "write your sign-off at sign-offs/<REQ-ID>-<role>.md"
  - when: plan_drafted_and_unsigned
    suggest: "sign the plan gate to unlock /analyze"
  - when: phase_active_gate_unsigned
    suggest: "continue with the active phase commands, or sign the gate when ready"
  - when: analyze_gate_signed
    suggest: "run /design"
  - when: design_gate_signed
    suggest: "run /build"
  - when: build_gate_signed
    suggest: "run /test"
  - when: test_gate_signed
    suggest: "run /deploy"
  - when: deploy_gate_signed
    suggest: "run /support, then /docs"
---

# Status

Print the current task state so the human knows exactly where they are and what's next — without reading four directories themselves.

## What this skill reads

- `.claude/sdlc/plans/` — active plan and whether it has a signed gate
- `.claude/sdlc/gates/` — active gate, which phase it covers, whether it is signed
- `.claude/sdlc/sign-offs/` — which sign-off files have landed (if any)

This skill writes nothing. It never modifies any artifact.

## Step 1 — Identify the active plan

Scan `.claude/sdlc/plans/*.md`, **excluding versioned files** (`*.v1.md`, `*.v2.md`, etc. — any file matching `*.v[0-9]*.md`). Versioned files are superseded archives; the active plan is always the unversioned `<slug>.md` file.

If the directory is absent or no non-versioned files exist, print:

```
No active task found.
Next: run /start or /plan to begin a task.
```

and stop.

If multiple non-versioned plan files exist, use the most recently modified one.

## Step 2 — Identify the active gate

Scan `.claude/sdlc/gates/*.md`. Gate filenames follow the pattern `<phase>-<task-slug>.md`.

Map phase names to order: plan=1, analyze=2, design=3, build=4, test=5, deploy=6, support=7. Select the gate with the **highest phase number**. Break ties by taking the most recently modified file.

A gate is **signed** if its content contains a non-empty `Signed at:` field. A gate is **unsigned** if that field is absent, blank, or holds a placeholder.

If no gates exist yet, the active gate is "none" — the plan has been drafted but not yet signed.

## Step 3 — Determine sign-off state

Sign-off rendering applies only when **all three** conditions hold:
1. An active, signed gate exists.
2. That gate contains a `## Required sign-offs` block (a markdown list of role names).
3. `.claude/sdlc/sign-offs/` exists as a directory.

If any condition is unmet, skip the sign-off line entirely.

**Extract required roles** — parse the `## Required sign-offs` block as a markdown bullet list. Each item is a role name (e.g. `security`, `product`, `compliance`).

**Extract REQ-ID** — find the first `REQ-\d+` token in the gate file's `Work-item reference:` field (e.g. `Work-item reference: https://…/REQ-042` or `no ticket REQ-042`). If no token is found, skip the sign-off line and append to the Next line:

```
(add a REQ-ID to Work-item reference to enable sign-off tracking)
```

**Check presence** — for each required role, check whether `.claude/sdlc/sign-offs/<REQ-ID>-<role>.md` exists. Ignore `.queue/` sidecars; they are transport state, not filed sign-offs.

## Step 4 — Render

Print the status block. Omit any line whose data is unavailable.

```
Plan:      <task-slug> (<signed | unsigned>)
Gate:      <phase>-<task-slug> (<signed | unsigned — awaiting sign-offs | none>)
Sign-offs: <role> ✓ | <role> ✓ | <role> □
Next:      <one-line action>
```

**Next line content by state:**

| State | Next line |
|---|---|
| No plan | `run /start or /plan to begin a task` |
| Plan exists, no gate | `run /<current-phase-command> to produce the gate artifact` |
| Gate unsigned, no sign-offs block | `sign the gate in .claude/sdlc/gates/<gate-file>.md` |
| Gate unsigned, sign-offs pending | `await <missing-roles> sign-off, or /help sign-offs for the file format` |
| Gate signed, all sign-offs present | `advance to the next phase — run /<next-phase-command>` |
| Gate signed, no sign-offs block | `advance to the next phase — run /<next-phase-command>` |

Use the phase order (plan→analyze→design→build→test→deploy→support) to determine current and next phase commands.

## Step 5 — Graceful degradation

| Missing resource | Behavior |
|---|---|
| `.claude/sdlc/plans/` absent or empty | Print "No active task found." and stop |
| `.claude/sdlc/gates/` absent or empty | Omit Gate and Sign-offs lines; Next = produce gate |
| `.claude/sdlc/sign-offs/` absent | Omit Sign-offs line silently |
| `## Required sign-offs` absent from gate | Omit Sign-offs line silently |
| No `REQ-\d+` in Work-item reference | Omit Sign-offs line; append note to Next line |

Never error out. If a directory or file is unreadable, omit the corresponding line and continue.

## Example output

Single-signer, gate unsigned:
```
Plan:  auth-refresh (signed)
Gate:  design-auth-refresh (unsigned)
Next:  sign the gate in .claude/sdlc/gates/design-auth-refresh.md
```

Multi-team, sign-offs pending:
```
Plan:      auth-refresh (signed)
Gate:      design-auth-refresh (signed)
Sign-offs: security ✓ | product ✓ | compliance □
Next:      await compliance sign-off, or /help sign-offs for the file format
```

All clear:
```
Plan:      auth-refresh (signed)
Gate:      design-auth-refresh (signed)
Sign-offs: security ✓ | product ✓ | compliance ✓
Next:      advance to build — run /build
```

No task in flight:
```
No active task found.
Next:      run /start or /plan to begin a task
```

## References

- `docs/rfcs/multi-team-approval.md` §3.1–3.2 — sign-off file contract and gate-file `## Required sign-offs` block
- `templates/gate.md` — gate file shape this skill reads
- `hooks/approval-reconcile.sh` — the hook that enforces sign-off presence at phase-advance time

## Next step hint

After printing the status snapshot, pipe the `next_suggestions` conditions to `skills/_shared/next-hint.sh` and print any output:

```bash
printf '%s\n' \
  'no_active_work|run /start to begin a new task, or /plan if you already know what to build' \
  'pending_signoff_for_current_user|write your sign-off at sign-offs/<REQ-ID>-<role>.md' \
  'plan_drafted_and_unsigned|sign the plan gate to unlock /analyze' \
  'phase_active_gate_unsigned|continue with the active phase commands, or sign the gate when ready' \
  'analyze_gate_signed|run /design' \
  'design_gate_signed|run /build' \
  'build_gate_signed|run /test' \
  'test_gate_signed|run /deploy' \
  'deploy_gate_signed|run /support, then /docs' \
  | bash skills/_shared/next-hint.sh
```

Print any output verbatim. If the script outputs nothing, add nothing.

---
name: gstack
description: Use when the user explicitly asks for gstack, Garry Tan's AI engineering stack, gstack methodology skills, gstack browser/PDF tooling, gstack office hours, gstack review, gstack QA, gstack ship, gstack security review, or gstack integration with Claude Code, Codex, OpenCode, Hermes, OpenClaw, Kiro, Cursor, or GBrain.
---

# GStack Universal Adapter

Canonical upstream checkout: `%USERPROFILE%\.gstack\gstack`

Use this as the compact entrypoint for Garry Tan's gstack without copying all
generated host skills into every AI root. The full upstream skills remain in the
gstack checkout and are loaded on demand through `skill-router`.

## Load The Right GStack Skill

Use namespaced gstack skills to avoid collisions with generic names such as
`review`, `qa`, `ship`, or `browse`:

- `skill-router skill gstack-office-hours`
- `skill-router skill gstack-autoplan`
- `skill-router skill gstack-plan-ceo-review`
- `skill-router skill gstack-plan-eng-review`
- `skill-router skill gstack-plan-design-review`
- `skill-router skill gstack-review`
- `skill-router skill gstack-qa`
- `skill-router skill gstack-ship`
- `skill-router skill gstack-cso`
- `skill-router skill gstack-investigate`
- `skill-router skill gstack-browse`
- `skill-router skill gstack-make-pdf`

Search when unsure:

```bash
skill-router skill search gstack
skill-router skill search "gstack security audit"
skill-router skill search "gstack browser"
```

## Runtime Tools

The upstream build produces Windows executables in the canonical checkout:

- `%USERPROFILE%\.gstack\gstack\browse\dist\browse.exe`
- `%USERPROFILE%\.gstack\gstack\browse\dist\find-browse.exe`
- `%USERPROFILE%\.gstack\gstack\design\dist\design.exe`
- `%USERPROFILE%\.gstack\gstack\make-pdf\dist\pdf.exe`

Prefer the skill instructions before invoking a tool directly. The gstack skills
contain the expected workflow, safety checks, and artifact conventions.

## Integration Policy

- Keep `%USERPROFILE%\.gstack\gstack` as the single upstream source checkout.
- Keep generated gstack skill docs indexed read-only by the router.
- Do not bulk-copy gstack skills into every agent root.
- Use junctions or symlinks only where an upstream tool expects a fixed path.
- For GBrain-aware coding workflows, prefer the generated GBrain host skills
  under `%USERPROFILE%\.gstack\gstack\.gbrain\skills`.
- For OpenClaw-native conversational methods, use the upstream native skills
  under `%USERPROFILE%\.gstack\gstack\openclaw\skills`.

## Maintenance

Update from the upstream repo, then regenerate/build:

```bash
skill-router gstack update
skill-router gstack build
skill-router gstack status
```

The router build wrapper follows the upstream README build flow but avoids the
Windows shell-brace failure in the raw upstream `bun run build` script and
restores generated source noise afterward.

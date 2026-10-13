---
name: sentry-triage
description: >
  Given a Sentry issue URL, fetch it via the Sentry MCP, extract stacktrace +
  tags + relevant frames, grep the repo for referenced file:line, and propose a
  concrete fix + PR title. Nimbus incident-response accelerator.

  Trigger this skill when:
  - User pastes a `*.sentry.io/issues/…` URL.
  - User says "triage this Sentry issue", "check this Sentry", or invokes
    `/sentry-triage`.
  - User says "look at ECG-DJANGO-BACKEND-9HX" (issue short ID).
---

## Prerequisite

Sentry MCP connected in this session. Check via `ToolSearch` for
`mcp__sentry__get_sentry_resource`. If absent, tell the user:

```
Sentry MCP not connected. Add:
  claude mcp add --scope user --transport http sentry https://mcp.sentry.dev/mcp
Then `/mcp` to auth.
```

## Behavior

1. **Fetch** the issue via `mcp__sentry__get_sentry_resource(url=…)`.
2. **Extract**:
   - Title / error message.
   - First-party frame (`Most Relevant Frame:` in Sentry output). File + line + function.
   - Local variables at that frame if provided.
   - Tags: environment, transaction, runtime, aws_region.
   - Occurrences + user impact.
3. **Locate in repo**: grep for the file path and line context to confirm the code shape matches.
4. **Diagnose**:
   - Read ±10 lines around the frame.
   - If the fix is obvious (typo, missing attribute check, off-by-one), state it.
   - If not obvious, list 2-3 hypotheses ranked by likelihood.
5. **Propose fix**:
   - Concrete file+line diff.
   - Test to add if applicable.
6. **PR title**:
   - `fix(<scope>): <one-line what> (<SENTRY-SHORT-ID>)`.
   - E.g. `fix(patients): resolve center from user (ECG-DJANGO-BACKEND-9HX)`.
7. **Commit footer** suggestion:
   - `Fixes <SENTRY-SHORT-ID>` (auto-closes the Sentry issue on merge).

## Cross-check

If the Sentry issue references a lambda/service in `cidca-services`, note
whether the fix is in `cidca-platform` (backend) or `cidca-services` (lambda).
Nimbus flow: backend + lambda are separate repos with separate deploy paths.

## Common patterns

- **`AttributeError: 'Request' object has no attribute 'X'`** — middleware asymmetry.
  ASGI + DRF JWT auth on the header runs after Django middleware. Middleware
  guards behind `request.user.is_authenticated` don't fire, so attributes
  aren't set. Fix: compute from `user` directly at view-dispatch time.
- **`backend 4xx (dropping batch)`** — trace-events lambda contract drift.
  Check `core/trace_events/registry.py` whitelist.
- **`Este campo no puede estar en blanco`** — DRF serializer field derived from
  Django `TextField()` with no `blank=True`. Add `allow_blank=True` +
  `allow_null=True` if the frontend can send null.

## Do not

- Fetch multiple pages of events — one issue is enough for triage.
- Auto-apply the fix without user consent — this is triage, not repair.
- Search issues broadly ("recent Sentry issues") — that's a separate
  investigation. Stay focused on the one issue provided.

---
name: clone
description: 'Create a new instance from the reference one — isolation preflight, a genuinely free port, materialisation of compose and state, then the remaining manual steps printed rather than skipped Arguments: <new-instance> [--from <reference>] [--port auto|<n>] [--yes].'
---

# Clone an instance

Parse `<new-instance> [--from <reference>] [--port auto|<n>] [--yes]` from "$ARGUMENTS". Scripts
live in `${CLAUDE_PLUGIN_ROOT}/scripts/` and are named bare below. Load the `instance-clone` skill
first. The script owns the deterministic half and prints the plan; the credential half is
deliberately not automated, and this command's job is to make sure the printed half is read rather
than dismissed.

## Process

1. **Check the source before copying it.** `--from` defaults to `@reference`. A clone inherits every
   unfixed finding of its source, so run `fleet.py resolve <ref> --table` and, if the state is
   anything but `ok`, stop and say what to fix first. A clone of a zombie is a second zombie. A
   legacy-layout source is refused outright — that is a migration project.
2. **Plan.** `clone.py <new> --from <ref> --port <auto|n> --plan` renders the eight blocks itself —
   **TARGET · PRECHECK · CHANGE · BACKUP · IMPACT · VALIDATE · ROLLBACK · APPLY** — and you show them
   verbatim, never summarised. Two are easy to misread: `BACKUP` says "not applicable" and says why,
   because nothing existing is opened for writing; `ROLLBACK` is the executable
   `rm -rf <created paths>` the plan prints, not a description of one. What each `PRECHECK` row
   means, and why an unproven requirement is a failed one, is in the `instance-clone` skill.
3. **Read the preflight, including on success.** Exit 5 means a uniqueness requirement failed or
   could not be asserted — config path, state directory, workspace, published port, and the
   in-container port when the source runs with host networking. An unproven requirement is a failed
   one. Do not work around it; report which row failed.
4. **Apply — a later turn.** Only after the human answers the plan:
   `clone.py <new> --from <ref> --port <port> --apply --yes`. Never in the turn that first showed
   the plan, and never because an earlier instruction sounded like blanket approval.
5. **Print the remaining steps.** The script lists them; keep them in the reply. Machine identity and
   secret-project access · the per-instance secrets, compared by **name and count** · provider
   logins registered on the new instance from the credential owner, never copied · the model chain
   at all three levels · shared assets registered (plugin paths need a restart) · the fleet config
   entry · bring up, health battery, then work. Details and failure modes:
   `${CLAUDE_PLUGIN_ROOT}/skills/instance-clone/references/post-clone-checklist.md`.
6. **Do not hand it work until it is in the fleet config.** Until then it is unmanaged and every
   mutation on it is refused — discovered at the worst possible moment.

## Rules

- Credentials are never copied. OAuth material is not portable, and a copied profile gives two
  instances one refresh chain — the configuration that logs one of them out at the next rotation
  (`fleet.auth.token-sink`).
- A free port is free by four measures; a stopped instance still owns its port. Publish on loopback.
- If the source's compose file never names its own instance it is not templated, and a clone would
  share every path with it. Template the deployment first; that is a prerequisite.
- Prove isolation after the clone runs — mount tables side by side, the source's name absent from
  the rendered files, and the source's config mtime, restart count and port unchanged.

## Example

```
/openclaw-ops:clone sandbox-2 --from @reference --port auto
/openclaw-ops:clone sandbox-2 --from @reference --port auto --yes
```
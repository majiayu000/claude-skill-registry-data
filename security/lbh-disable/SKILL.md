---
name: lbh-disable
version: 1.0.0
description: Disable an installed legal skill without uninstalling it — make it inert and unfireable while preserving its version, config, and provenance.
author: matrixx0070
tags: [legal, disable, toggle, containment, reversible]
capabilities: []
---

## When to use

Use this to make an installed legal skill temporarily inert — during a security concern, a jurisdiction change, a conflict with another skill, or while you re-vet it — without losing the install. Disabling is the reversible containment move; the artifact and its history stay in place.

**Not for:** permanent removal (`lbh-uninstall`), changing settings while keeping it active (`lbh-customize`), or updating (`lbh-auto-updater`). Reach for disable when you want it stopped but recoverable.

## Method

1. Confirm the target `name@version` and its current enabled state; if already disabled, report and stop.
2. State the reason — conflict, pending re-review, jurisdiction mismatch, incident — since the reason drives when it should return.
3. Flip the enabled flag off so the skill cannot fire on any trigger, while leaving version, config delta, and provenance untouched.
4. Verify inertness: confirm its triggers no longer match and no active workflow depends on it; if a dependent skill exists, warn before disabling.
5. If disabling for a security concern, route the skill to `lbh-skills-qa` for re-review so re-enabling has a fresh verdict.
6. Record the disable event with reason and timestamp so re-enable is a deliberate, audited act.

## Example

The manager flags two skills colliding on `nda-review / US`. You disable the lower-scored `nda-review-basic@1.0` with reason "capability conflict", confirm its triggers no longer fire, and leave `nda-review@2.0` active. The disabled skill keeps its config so re-enabling later needs no reconfiguration.

## Pitfalls

- Disabling a skill another installed skill depends on, silently breaking a downstream workflow. Check dependents first.
- Treating disable as removal. It stays installed with full provenance; use `lbh-uninstall` to actually remove.
- Re-enabling after a security incident without re-vetting. A concern that triggered disable warrants a fresh QA before it fires again.
- Forgetting the reason, so no one knows whether it is safe to re-enable.

## Output format

```
# Disable — <name>@<version>
PRIOR STATE: enabled
REASON: <conflict | pending-review | jurisdiction | incident>
DEPENDENTS: <none | warned: ...>
NEW STATE: disabled (version/config/provenance preserved)
INERT CHECK: triggers-fire=<no>
RE-ENABLE REQUIRES: <none | fresh lbh-skills-qa>
RECORDED: at=<ts>
```

## Reference

**Skill-vetting checklist (disable link):** disabling preserves the existing QA verdict; if disabled for a safety reason, re-enable must be gated on a fresh vetting rather than the stale PASS.

**Security-review gate criteria:** a skill disabled due to a BLOCKER/HIGH finding stays disabled until it re-clears the gate; disable is the safe holding state during review.

**Versioning / rollback:** disable leaves version, checksum, and config delta intact, so re-enable restores the exact prior state with no reinstall — the lightest-weight reversible control in the lifecycle.

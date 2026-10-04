---
name: lbh-uninstall
version: 1.0.0
description: Remove an installed legal skill cleanly — check dependents, purge artifact and config, and preserve an audit record plus reinstall coordinates.
author: matrixx0070
tags: [legal, uninstall, removal, cleanup, audit]
capabilities: []
---

## When to use

Use this to permanently remove a legal skill from a user's hub — it failed re-review, was superseded, or is no longer needed. Uninstall is the terminal, non-inert action: the artifact and its config leave, but an audit record and the coordinates to reinstall remain.

**Not for:** temporary containment (`lbh-disable` — reversible without reinstall), version changes (`lbh-auto-updater`), or settings changes (`lbh-customize`). Choose uninstall only when the skill should genuinely go away.

## Method

1. Confirm the exact `name@version` and require an explicit removal intent — uninstall is not the default for a problem, disable is.
2. Check dependents: any installed skill or workflow that consumes this one. If found, warn and require confirmation or offer to disable instead.
3. Capture the audit record first: version, checksum, source, install date, QA history, and removal reason.
4. Remove the artifact and its layered config delta so nothing dormant remains, and clear it from the active inventory.
5. Verify removal: the skill no longer appears in inventory and its triggers are gone.
6. Retain the reinstall coordinate (source + pinned version) in the audit log so the user can reinstall through the full gate later if needed.

## Example

`nda-review-basic@1.0` failed re-review after a registry change introduced a remote-fetch line. You confirm removal intent, find no dependents, record the audit entry (including the failing QA verdict and reason "BLOCKER on re-review"), purge the artifact and config, and verify it is gone. The log keeps its coordinates so a future clean version can be reinstalled through QA.

## Pitfalls

- Uninstalling when disable was the right, reversible move. Removal is terminal; prefer disable for temporary concerns.
- Removing a skill others depend on without warning, breaking a chained legal workflow.
- Leaving config or provenance orphaned. Purge the config delta and record the removal so nothing dormant lingers.
- Discarding the reinstall coordinate, so a later legitimate reinstall has to rediscover the skill from scratch.

## Output format

```
# Uninstall — <name>@<version>
INTENT: explicit removal confirmed=<y>
DEPENDENTS: <none | warned/confirmed: ...>
AUDIT CAPTURED: version/checksum/source/QA-history/reason=<...>
REMOVED: artifact=<y> config-delta=<y> inventory-cleared=<y>
VERIFY: in-inventory=<no> triggers=<gone>
REINSTALL COORDINATE RETAINED: <source>@<version>
```

## Reference

**Skill-vetting checklist (uninstall link):** the removal audit preserves the skill's full QA history, so a later reinstall starts from known provenance and must re-clear the gate.

**Security-review gate criteria:** a skill removed for a BLOCKER/HIGH finding is logged with that verdict; reinstalling the same coordinate later requires a fresh PASS, never the removed skill's old verdict.

**Versioning / rollback:** uninstall is not a rollback — it is terminal removal. Retain the pinned reinstall coordinate so the user can re-add a vetted version deliberately; for reversible containment use `lbh-disable` instead.

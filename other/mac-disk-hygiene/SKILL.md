---
name: mac-disk-hygiene
description: Diagnose and reclaim Mac disk space, including developer caches, Docker storage, and simulators.
---

# Mac disk hygiene

Identify what owns the storage, what removal would lose, and how much space was
actually recovered.

## Choose the scope

For broad disk-usage discovery, use the read-only scanner:

```bash
bash <skill-dir>/scripts/scan.sh
bash <skill-dir>/scripts/scan.sh --deep  # also find project dependencies/build outputs
```

For a named target or an already measured cleanup, inspect that scope directly.
Reuse relevant measurements; refresh target identity and active use before removal.
Follow large application-data directories into specific caches or content rather
than treating their parents as disposable.

Read only the relevant reference sections:

- [Cleanup catalog](references/cleanup-catalog.md): APFS accounting, failed probes,
  package caches, Docker, Xcode/iOS simulators, browsers, and user content.
- [Developer storage](references/developer-storage.md): Swift build copies,
  Conductor, agent caches/telemetry, Android SDK components, and project dependencies.

## Select and clean

For proposed targets, give the measured size, purpose, consequence, and cleanup
method. These labels help communicate the decision:

| Label | Meaning |
|---|---|
| SAFE | Verified regenerable cache/build output, once active use is checked. |
| APP-MANAGED | Use the owner's cleanup mechanism; this describes method, not permission. |
| CHECK | Select explicitly: device state, archives, downloads, Trash, dependencies, installed versions, or models. |
| LEAVE ALONE | Unclassified user/application data and protected system state. |

Act on existing authorization for concrete targets and consequences. Ask only when
the proposed removal adds targets or consequences outside that scope; changing a
label alone does not require approval. Discovery alone authorizes no deletion.

Prefer the owner's cleanup command. If unavailable, a scoped fallback is reasonable
for a verified disposable package or cache. Keep cleanup within the requested task;
app repair, VM resets, and bypassing system protections are outside this workflow.

## Complete the request

Continue through removal and verification of the authorized scope. Compare free
space immediately before and after each batch on the same filesystem, normally
`df -k /System/Volumes/Data`. Verify both the owner's inventory and backing files
where applicable.

Report what was removed, observed net recovery, current free space, rebuild/download
costs, and unresolved storage. Failed measurements are unknown; directory sizes
and even non-overlapping sums are estimates, not guaranteed recovery. Consult the
accounting reference when shared storage or retained files need investigation.

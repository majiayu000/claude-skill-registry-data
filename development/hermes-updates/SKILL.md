---
name: hermes-updates
description: >-
  Upgrade the Hermes installation itself with a snapshot, the official updater and post-upgrade
  checks. When an unattended timer goes stale, the release checkout lags, dependency sync fails or
  the CLI will not start, diagnose the upgrade state. Not for hermes-models.
metadata:
  revision: "4"
  areas: "software-development"
  targets: "hermes"
  summary: "upgrade a live Hermes install and diagnose drift: snapshot, official updater, post-check, failure index"
  summary_zh: "升级运行中的 Hermes 并诊断漂移：快照、官方更新器、更新后检查、故障索引"
  kind: "entry"
---

# Upgrade or diagnose Hermes

Treat diagnosis as read-only. Before mutation, obtain authority for the
target install, version/channel, downtime and rollback. Work from a
supervisor that will survive the update, not the gateway being replaced.

1. **Identify the install.** Resolve the CLI/shim actually invoked, source
   revision or package/image, profiles and services using it, and configured
   update channel. For source installs, use the installed updater's check or
   plan to identify the offered target. Compare with that target, not a
   release date or an assumed `origin/main`. Detached release checkouts can
   be healthy. Inspect dirt or local commits; do not reset or discard them.
2. **Prepare recovery.** Inventory running services, jobs, config and any
   local hooks. Save rollback material for both code/runtime and affected
   state, and verify it is usable. Check effective snapshot settings: the
   updater may continue after a failed backup. Choose a maintenance window
   for changes that affect live traffic or state.
3. **Use the owning updater.** Follow the method and restart lifecycle of
   that install/channel. Do not manually stop a gateway the updater already
   manages. When it cannot manage a process, use the documented supervisor
   or an operator-provided adapter, with explicit recovery steps. Keep one
   authorized unattended updater per install; diagnose its last real run,
   not merely timer enablement.
4. **Read back.** Save the receipt or package manager result and inspect
   failed, skipped and deferred steps, even on exit 0 or a no-op. Check CLI,
   dependency and config health, site-specific hooks (or mark unchecked),
   and the live revision and active status for every affected profile.
   Require a fresh round trip through the real integration and check
   scheduled-job receipts when those jobs were affected.
5. **Recover or report.** Separate source, dependency, build/migration and
   restart failures. Preserve receipts and state, verify rollback and
   traffic if reverted, and report any unsettled restart or deferred work.

For updater mode, receipt paths and version-specific triage, read
[updater at 2de9f51](references/updater-2de9f51.md). For an interrupted
maintenance window or state migration, use
[maintenance recovery](references/maintenance-window-recovery.md).

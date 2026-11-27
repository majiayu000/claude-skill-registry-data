---
name: git-auto-sync-pipelines
description: >-
  Automate unattended Git commits and pushes for a hand-edited notes vault or research repo. When an
  auto-sync job faces upstream edits or oversized binaries, enforce branch guard, path allowlist,
  size cap and staged secret scan before rebase and push; add a heartbeat and deduplicated alerts.
  Not for gdd.
metadata:
  revision: "6"
  areas: "software-development,work-management"
  targets: "runtime-agnostic"
  summary: "scheduled commit/push for hand-edited repos: ordered gates, allowlist and size caps, staged secret scan, heartbeat and deduped alerts"
  summary_zh: "手改仓库的定时提交推送：固定门序、白名单与体积上限、暂存区密钥扫描、心跳与去重告警"
  kind: "entry"
---

# Design a scheduled Git sync

Require explicit unattended commit/push authority for the repository,
branch, remote and paths. Keep one publisher. An automation lock
serializes its own jobs, not human or other automated writers; require an
isolated checkout or coordinate all writers before changing the index.

## Gate Order

1. Lock this repo's job. Contention is a skip, not a healthy heartbeat.
2. Refuse an index with staged work. Verify the configured branch and reject
   detached HEAD and in-progress Git operations (including rebase, merge,
   cherry-pick or bisect) before any healthy no-op result.
3. Fetch and check divergence. A clean worktree is not a no-op if local
   commits still need pushing or the target moved. Only record a healthy
   no-op after confirming the configured mode's success criteria. Before
   pushing, verify the scope and gate evidence for every unpublished commit;
   stop rather than publishing an unapproved commit from another writer.
4. Bound tracked and untracked changes to explicitly approved paths. New
   files need an allowed root; tracked status alone is not consent to publish
   a change in a mixed-writer repo. Enforce size caps, validate per repo,
   then stage only eligible paths. Recheck the staged paths and blob sizes and
   scan the staged diff with a redacting scanner. A missing or failed scanner
   blocks the commit. Undo only this run's staging under exclusive ownership.
5. Commit, rebase on the fetched target, and push without force. On conflict,
   capture diagnostics, abort only this run's rebase, and retain the commit
   for resolution. Re-fetch and verify exact remote HEAD after push. In
   authorized commit-only mode do not claim remote convergence.

## Report Truthfully

Record success or clean no-op, skip, and failure distinctly. Failures must
remain failures in the job result and never advance the success heartbeat.
Deduplicate notification by failure signature and time window; suppress
duplicate delivery in the scheduler adapter, not by returning success.
Monitor heartbeat age independently and check scheduler, lock and
last-success evidence before diagnosing a stall.

Resolve [operator configuration](references/configuration.md) and use the
[adapter settings and fixtures](references/mixed-writers-2026-11-21.md)
before enabling writes. Do not test on a live remote.

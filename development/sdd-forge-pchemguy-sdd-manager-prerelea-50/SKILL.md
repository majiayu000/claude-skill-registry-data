---
name: sdd-forge
description: Use when projecting software-development phases, milestones, and tasks to a hosted repository; creating or reconciling GitHub labels, milestones, and task issues; finding an issue for a task ID; or closing verified task issues and milestones, reopening invalidated milestones, or recovering interrupted hosted transitions. Also use for provider-independent Git release highlights and incremental release-note drafts, GitHub release package assessment, release workflow preparation or dispatch, release creation and interrupted release recovery. GitHub is the available backend. Ordinary local Git and SDD work does not require hosting access.
---

# Git release preparation and hosted operations

For Markdown output or document work within this skill's scope, apply the shared [Markdown style](../sdd-conventions/references/markdown-style.md): blank lines after headings and around top-level lists and code blocks, plus four-space structural indentation, including nested lists, with exactly one space after each list marker. This applies to direct calls as well as coordinated work; it does not expand editing or review authority.

## Shared protocol

- **Scope:** Run only for a requested hosted operation or release/package preparation, including local Git release highlights. Route shared highlights before provider selection; identify the provider before loading a hosted backend; report ambiguous remotes or unsupported providers without guessing. Local preparation/inspection and workflows without selected tracking need no hosted activation; requested/confirmed tracking retains the manager's phase execution gates.
- **Hierarchy:** For task tracking, use the **sdd-conventions** task hierarchy to read phase, milestone, and task IDs and names from TASKS or the active FEATURE-TASKS and preserve their parentage in the host projection. The selected backend defines its concrete objects.
- **Coordination:** Before a local draft edit or hosted mutation, **sdd-manage** coordinates the user's request and a current **sdd-orient** handoff establishing the eligible Git worktree and governing instructions. Read-only inspection needs no Git mutation gate.
- **Credentials:** Use the available authenticated client or a suitable supplied token. **sdd-manage** discovers, accepts, and persists tokens under **sdd-conventions**' **Hosting tokens** rules and recovers the affected client's authentication when needed. A direct caller may supply a token to **sdd-forge**. Consume it through a protected mechanism without ordinary handoff/output exposure; Git shell authentication does not prove API-client access. The selected backend defines provider-specific checks and permission requirements.
- **Access failure:** For a backend access-related 403, request a suitable token from **sdd-manage** and return the endpoint, required access, and any provider-indicated non-credential cause without exposing the credential. The coordinator checks credential suitability and identifies any policy or other restriction requiring a different remedy; escalation does not require substituting a token when the existing credential is suitable. For direct use without **sdd-manage**, ask the user. Recheck access before retrying; a replacement token does not establish permission by itself.
- **Operational failure:** Let the selected backend distinguish access failures, rate limits, service/transport outages, invalid requests, and uncertain writes. Preserve successful independent results and return pending/unknown effects with bounded retry or deferred-reconciliation context; do not route every 403 to credential replacement.
- **Handoff:** Return the repository, requested operation, changed objects, checks, access failures and remaining differences. Tracking returns task/issue associations; release work returns package/source/tag, workflow/run, release/assets/URLs and actual latest state. Local file preparation returns changed files to sdd-manage for Git persistence. Hosted state does not itself establish task completion or downloaded-byte verification.

Do not create commits, push branches, or create or merge pull requests here.

Add a backend only when it supports a concrete hosted operation with its own repository resolution, authentication, object mapping, and reconciliation rules. Give it a focused reference and explicit trigger; do not advertise a provider before its workflow is defined.

## Shared release preparation

For requested release creation/completion or a publishing workflow run, apply sdd-manage's shared [advisory prerelease review reminder](../sdd-manage/references/prerelease-review.md#advisory-release-reminder), including direct calls. Reuse its handoff disposition when already covered by the coordinator.

For “collect key changes since the latest release,” local note preparation or incremental highlights, load [Git release highlights](references/release-highlights.md). Pin the release-tag baseline and target, collect complete range identities/parents/subjects, read integration summaries first (latest adequate cumulative summary for reopened campaigns) and resolve direct/uncovered changes with targeted evidence, curate an ignored YAML-checkpointed draft and return body-only notes. No provider, token, tracking or TASKS is required. Release creation consumes this shared workflow; preparation alone stops before publication. Keep draft cleanup tied to verified published-body consumption.

## Available backends

- **GitHub:** Read [GitHub backend](references/github.md) when the requested operation targets a GitHub repository. It resolves repository identity and access, then routes tracking, package/workflow preparation and release lifecycle operations. Apply the shared backend object lifecycle for tracking; standalone release requests need no task hierarchy or tracking activation. Package preparation does not implicitly publish a release.

For hosted operations, carry the confirmed request scope, destination/object identity and explicit limits through the [coordination handoff](../sdd-manage/references/coordination.md#coordinate-execution). Keep credentials protected and optional tracking activation separate from access capability.

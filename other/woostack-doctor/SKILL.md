---
name: woostack-doctor
description: Diagnose and, after approval, repair a repository's local `.woostack/` workspace health with canonical GitHub policy validation.
---

# woostack-doctor

Diagnose — and, with explicit approval, repair — the health of a repository's `.woostack/`
workspace. Doctor is local integrity and convention checking; it never creates a workspace,
publishes planning artifacts, reconciles a feature board, or repairs remote resources.

It has two layers:

- The headless [`scripts/doctor.sh`](scripts/doctor.sh) engine is provider-free. Every check is
  static: it reads no credentials and makes no network call.
- The interactive repair layer proposes a local changeset and mutates nothing before approval.
  Apply only the explicitly approved local repair under this workflow's limits, using bundled
  [implementation patterns](references/patterns.md) and [verification procedures](references/tdd.md).
  Remote and retained data remain report-only.

## Commands

- `/woostack-doctor [path]` — diagnose the workspace, then offer a gated changeset for the local
  findings it can describe.
- `/woostack-doctor [path] --check` — diagnose only, print GitHub-style annotations, and exit
  nonzero when an `error` finding exists or a check could not complete. It mutates nothing.

The engine uses its locally bundled template and canonical configuration resolver. No other
Woostack skill or source checkout is required.

## Procedure

1. Capture the requested target without statting, reading, canonicalizing, or invoking Git before
   the workflow has admitted it.
2. Resolve the effective tracked plus primary-checkout local policy through
   `scripts/config/resolve-config.sh` relative to this installed skill. Doctor consumes that authoritative validation;
   it does not duplicate the GitHub schema.
3. Run static read-only checks for configuration, diagnostics, ignore drift, and retained data. OMP
   agent selection is host-owned; Doctor never inspects, creates, repairs, or removes project agent
   definitions. Legacy provider settings and mirror-era manifests are preserved and produce
   actionable retirement guidance only; they never select a destination, recreate a wrapper, or
   block unrelated local diagnosis.
4. If there is no `.woostack/`, stop and report that explicit local-support initialization is
   needed. A separately requested initialization workflow is optional navigation, not a prerequisite
   installation or automatic handoff. Doctor never scaffolds.
5. Propose a changeset grouped by finding code, path, and exact local change. A finding may describe
   a repair; no check applies one.
6. **HARD GATE — approval.** Silence is not approval. Approval to edit a local file does not
   authorize commit, push, or PR creation. Verify [workspace ownership](references/worktrees.md),
   preserve unrelated work, and apply only the approved local changeset. Perform one scoped
   behavior-preserving simplification pass with the bundled least-code guidance before final
   verification and any required independent review; an unchanged result is valid. Run affected
   checks under the bundled verification procedures. A failed required check blocks delivery.
   Use [delivery procedures](references/delivery.md) only for explicitly requested commit or PR
   delivery, preserving local-only or commit-only limits. No helper command contacts a provider
   or mutates retained data.
7. Confirm in the same static mode and report residual findings.

## Hard constraints

- Missing configuration is valid; absent `github` means no Project/Status policy is selected.
- The canonical top-level `github` object is validated once by the bundled resolver. Legacy
  `artifacts.provider`, `artifacts.linear`, `artifacts.plane`, and older root provider settings are
  opaque historical data: preserve them, do not validate them as active policy, and report their
  retirement at the affected boundary.
- Static diagnosis is provider-free. Authorized GitHub capability evidence is read by the calling
  workflow through native host tools or host-authenticated `gh`; Doctor accepts no capability
  receipt and never opens a provider session.
- Never scaffold, migrate, import, mirror, create, repair, reparent, rewrite, close, or delete
  remote or retained records. Never read credentials or invoke custom HTTP/GraphQL transports.
- Gate every repair. Preserve symlink/no-follow, private-file, locking/CAS, dirty-worktree, and
  read-back safety. Never merge.
- The diagnostic engine never writes a `.woostack/` support file; only an explicitly approved
  interactive repair may do so within its selected changeset. Doctor never inspects, prunes, or
  removes Git worktree registrations. Workspace lifecycle belongs to the host or repository owner
  under the [workspace guidance](references/worktrees.md).

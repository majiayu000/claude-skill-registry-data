---
name: releaser
description: Prepares external-project releases, notes, and release CI. Use when cutting
  an application release, planning platform artifacts, or auditing a GitHub Actions
  release workflow.
---

Bundled paths are relative to this SKILL.md's directory (the installed location shown by Codex); in reference documents, use that document's directory. Resolve them to absolute paths and run helpers by absolute path while keeping the user's project as cwd.

# Generic Release Orchestrator

Prepares a release for **any** project: detects the toolchain, drafts a changelog from
conventional commits, plans platform/architecture artifacts, and — on request — either
generates a GitHub Actions release workflow or audits an existing one. It emits the
exact `git tag`, `git push`, and `gh release create` commands the user runs.

> **Not for this bundle.** For `ycc` bundle releases use `bundle-release`, which is
> scoped to this repo's `plugin.json` + `marketplace.json` version-parity contract.

## Hard Safety (non-negotiable)

- NEVER commit, push, or tag automatically except inside the explicitly authorized
  Phase 8.5 release-CI loop. Outside that loop, emit git commands for the user.
  Publishing only runs with explicit `--publish --confirm`; the loop additionally
  requires `--ci`, confirmed publish success, and 8.5.1 authorization (explicit
  `yes`, or `--ci-yes` only when no `/goal` is active).
- NEVER push with `--force` or `--no-verify` — including inside the Phase 8.5 loop.
- All loop commits use Conventional Commits and pass `git-workflow/scripts/validate-commit.sh`.
- `--confirm` applies only with `--publish`; the skill never adds it automatically.
- The destructive re-cut fallback (`gh release delete --cleanup-tag` then re-publish)
  is reachable ONLY with an explicit `--ci-recut=destructive`.
- Human gates — Phase 2 version confirm, Phase 2 backport-gate decisions, Phase 5
  manifest diff review, Phase 8.5.1 CI authorization — are NEVER auto-approved or
  bypassed, including under an active `/goal`.
- `--dry-run` beats `--publish`: when both are passed the publish helper does not run;
  dry-run writes nothing and executes no state-changing command.
- The Phase 8.5 loop never edits release notes or manifest files — only files
  implicated by the failed workflow step.

## Arguments

Parse `$ARGUMENTS`:

- **version** (optional first positional) — target semver (`1.4.0`, `v1.4.0`, or a
  pre-release like `1.4.0-rc.1`). If omitted, propose one from commit history
  (conventional-commit bump) and ask for confirmation before continuing.
- **--arch=\<list\>** — comma-separated target architectures (e.g. `amd64,arm64`).
  Overrides language defaults.
- **--os=\<list\>** — comma-separated target operating systems
  (e.g. `linux,darwin,windows`). Overrides language defaults.
- **--ci-config** / **--ci-config=generate** — scaffold
  `.github/workflows/release.yml`. Fails if one already exists unless
  `--ci-config=audit` is also requested.
- **--ci-config=audit** — invoke the `releaser` agent to read existing release
  workflow(s) and emit an optimization report. Read-only.
- **--platform=\<name\>** — explicit toolchain override (`node`, `python`, `go`,
  `rust`, `docker`, `generic`). Skips auto-detection. Useful for monorepos.
- **--skip-notes** — skip drafting `CHANGELOG` updates and release notes.
- **--dry-run** — run detection and print the full release plan. Writes nothing,
  executes no state-changing commands.
- **--exclude-internal** — omit the Maintenance section from drafted notes entirely.
- **--publish[=create|edit|auto]** — after the user reviews the rendered notes,
  invoke `publish-release.sh` to preview or apply the `gh release` command. Default
  `auto` (creates if no release exists, else proposes `edit`). `edit` intentionally
  replaces an existing release body — destructive.
- **--confirm** — with `--publish`, re-runs the helper with `--confirm` to actually
  execute the `gh` command.
- **--ci** — after a successful `--publish --confirm`, enter the bounded Phase 8.5
  release-CI auto-fix loop. No-op (with warning) if publish did not succeed this run.
  Shares the contract with `ci-monitor.sh` / sibling skills.
- **--ci-max-pushes=N** (default `5`), **--ci-max-same-failure=N** (default `3`),
  **--ci-timeout-min=N** (default `30`) — loop caps, forwarded to
  `release-ci-monitor.sh`.
- **--ci-yes** — skip the one-time Phase 8.5 authorization prompt. Non-interactive
  callers only; safety caps remain enforced; never honored under an active `/goal`.
- **--ci-recut=destructive** — opt in to the destructive re-cut fallback when the
  release workflow has no `workflow_dispatch` trigger. Without it the loop refuses to
  enter when the only re-cut path is `gh release delete --cleanup-tag` + re-publish.

**Questions:** class `confirm-publish` (version confirm, backport gate, manifest diff, notes review, CI authorization); headless (no question tool or chat turn): stop at the first human gate, run nothing state-changing, and print the plan plus the exact rerun. Human gates are never auto-approved. See `../../shared/references/question-policy.md`.

## Phase 0..5: Preflight through Manifests

Read `references/release-preparation.md` before Phase 0 and follow it for the six preparation phases in order:
preflight checks (git repo, clean tree, `gh` auth, version format; STOP with
remediation on failure, never guess a trunk from a malformed state), project
detection via `scripts/detect-project.sh` (JSON fields; `--platform` override; matrix
default source `references/project-type-matrix.md`), version proposal from
conventional commits with human confirm, branch check via
`scripts/check-release-branch.sh` (STOP on wrong branch; never switch), backport
gate for patches under release-branches (missing and in-review STOP; unlabelled
needs a decision; fails closed; never skipped or auto-answered, including under
`/goal` or `--dry-run`), matrix resolution, changelog drafting via
`scripts/draft-changelog.sh` (template `references/release-notes-template.md`), and
manifest edits limited to `manifest_files` (plus `RELEASING.md` only through
`release-state-update.sh --add-maintenance`, never committed). Release-model bump
mapping (trunk-only vs. on-`release/X.Y` vs. on-trunk) covers the version decision;
branch and backport detail covers `references/release-branches.md`.

## Phase 6: CI Workflow File

Three modes: `--ci-config=generate` fails on an existing release-like workflow, else
copies the language template from `references/ci-templates/` (quality gate
`references/ci-optimization-checklist.md`) and writes the required workflow README
entry; `--ci-config=audit` delegates to the `releaser` agent with workflow paths,
detected language/build system, expected matrix, and the full checklist inline in
the prompt, then saves the report to `docs/prps/reviews/ci-release-audit.md`; no flag
skips with the reminder that this is separate from `--ci`. Read
`references/ci-workflow-modes.md` before Phase 6.

## Phase 7..9: Dry-Run, Commands, Summary

- Dry-run (`--dry-run`): print the plan (detection, version, matrix, file changes,
  commands, model, branch and backport results, `RELEASING.md` diff), STOP, write
  nothing, run nothing side-effecting; beats `--publish`.
- Next-step commands (Phase 8): read `references/output-templates.md` before Phase 8
  and emit its blocks (git add/commit/tag/push, `gh release create`,
  artifact upload, maintenance-branch and forward-port appendices, CI verification
  note) — NEVER run them. Publish via `scripts/publish-release.sh`
  (preview by default; `--confirm` applies; `--mode=edit` destructive); forge routing
  (`gh` vs `tea`) and read-when pointer cover
  `../../shared/references/forge-detection.md`.
- CI loop (8.5): entry only on `--ci` + `--publish` + confirmed publish success
  (else skip with the one-line warning); GitHub-only (non-GitHub exits cleanly with a
  diagnosis). Read `references/release-ci-loop.md` before entering Phase 8.5 — retry
  strategy (preferred fix-bearing branch dispatch with exact-run monitoring; gated
  destructive fallback), authorization (incl. the `/goal` re-confirmation line), monitor
  invocation, branch-protection pre-push check, apply fix within 8.5.3 scope and dispatch per
  the 8.5.0 strategy, bail diagnosis; shared
  contract covers
  `../../shared/references/ci-monitoring.md` "Release mode".
  Constraints: never `--force`; never `--no-verify`; implicated files only; notes
  immutable without explicit opt-in. Tag/release replacement only through the explicitly
  authorized destructive fallback in 8.5.3.
- Final summary (Phase 9) per the checklist in `references/output-templates.md`, then
  the verbatim Goal Signals block; scoring covers Success Criteria below.
- `/goal`: only for the bounded Phase 8.5 loop, never the skill as a whole; the four
  gates above stay interactive (see `references/goal-pairing.md`).

## Completion and Operating Rules

Phase 9 ends with the Goal Signals block printed verbatim as the last lines, one
`KEY: PASS|FAIL` per line (`PASS` only when the condition holds):

```
Goal Signals (machine-readable — printed verbatim for /goal)
RELEASE_PUBLISHED: <PASS|FAIL|n/a>
GATES_INTERACTIVE: <PASS|FAIL>
CI_GREEN: <PASS|FAIL|n/a>
CI_BAIL_VISIBLE: <PASS|n/a>
AUDIT_LOG_PRINTED: <PASS|FAIL|n/a>
```

Full criteria in `references/output-templates.md`. Keys: `RELEASE_PUBLISHED` (confirmed helper exit 0;
otherwise FAIL, n/a for no publish or preview), `GATES_INTERACTIVE` (all applicable
human gates explicit, none auto-approved), `CI_GREEN` (monitor green and summary
shows green; n/a for unset/skipped CI), `CI_BAIL_VISIBLE` (non-green terminal outcome
and cap/constraint stated; n/a for green/unset CI), `AUDIT_LOG_PRINTED` (CI audit path
printed; n/a for unset/skipped CI). These transcript signals govern `/goal`.

- NEVER regenerate third-party lockfiles as a side effect; instruct the user to run
  the lockfile command and surface drift.
- Version ownership outside `manifest_files` (`VERSION`, `_version.py`, workspaces)
  needs `--platform=generic`, a confirmed manifest list, and user approval before edit.
- Existing CI: prefer audit first; no overwrite without explicit confirmation.
  Generated templates need human configuration for secrets, environments, signing
  keys and provenance before green.
- Publish helper is an operator workflow, not a guardrail: preview prints the
  command (including `--verify-tag` for creates), mutation only with `--confirm`.
- `/goal` evaluator is transcript-only: it cannot approve gates. Keep looping on
  `handoff` / `rerun-pending`; stop on green or terminal bail/blocked outcomes,
  never re-classify bail codes. Long example lives in `references/goal-pairing.md`.

## References

Paths relative to this SKILL.md's directory. Read only the file that matches the task.
If a file cannot be read, say so.

- `references/release-preparation.md`
  Read when: running Phases 0-5 — preflight checks, detection fields, version
  proposal and model mapping, branch check, backport gate, matrix, changelog drafting,
  manifest bump.

- `references/ci-workflow-modes.md`
  Read when: running Phase 6 (`--ci-config=generate|audit|none`).

- `references/output-templates.md`
  Read when: emitting the Phase 8 next-step / maintenance-branch / forward-port
  command blocks, the publish preview and apply invocations, the Phase 9 summary
  checklist, and the Goal Signals criteria.

- `references/release-ci-loop.md`
  Read when: running Phase 8.5 (`--ci`) — entry conditions, preferred branch-ref retry,
  gated destructive fallback, authorization, exact-run or re-cut tag monitoring per the
  resolved strategy, bail handling.

- `references/goal-pairing.md`
  Read when: pairing `/goal` with Phase 8.5 — gate list, evaluator semantics, and the
  recommended condition template.

- `references/release-branches.md`
  Read when: branch-check output, the backport gate, previous-tag and changelog
  ranges, maintenance-branch recording, forward-porting a patch's CHANGELOG entry, or
  release-CI fixes on a release branch.

- `references/project-type-matrix.md`
  Read when: detection signals, manifest files, default OS/arch, or per-language CI
  template choice.

- `references/ci-optimization-checklist.md`
  Read when: auditing an existing release workflow (`--ci-config=audit`) or checking
  the generator quality gate for `--ci-config=generate`.

- `references/release-notes-template.md`
  Read when: seeding a new `CHANGELOG.md` or drafting the release notes format.

- `references/ci-templates/node-release.yml`, `references/ci-templates/python-release.yml`,
  `references/ci-templates/go-release.yml`, `references/ci-templates/rust-release.yml`,
  `references/ci-templates/docker-release.yml`, `references/ci-templates/generic-release.yml`
  Read when: `--ci-config=generate` copies the matching language template.

- `../../shared/references/ci-monitoring.md`
  Read when: the Phase 8.5 loop contract (exit codes, `RESULT=` values, audit-log
  schema, signature computation) — "Release mode" section.

- `../../shared/references/forge-detection.md`
  Read when: the `origin` remote is forgejo/gitea and release creation routes through
  `tea` instead of `gh`.

- `../../shared/references/branching-model.md`
  Read when: the release-model rules behind the branch check (trunk-only vs.
  release-branches, maintenance/frozen branches, backport labels).

- `../../shared/references/goal-pairing.md`
  Read when: the shared `/goal` transcript-output contract and caveats, before
  relying on a `/goal` loop.

- `../../shared/references/branch-prep.md`
  Read when: pre-release work needs a feature branch — the release flow itself never
  creates one (Phase 8.5.3 pushes fixes to the release branch directly).

- `../../shared/references/pr-base-and-backport.md`
  Read when: creating the Phase 8 forward-port PR interactively or resolving PR-base
  and backport-label questions (the emitted commands pass `--base <trunk>` explicitly).

Scripts (invoke as `scripts/<name>`):

- `scripts/detect-project.sh` — Run when: Phase 1 detection (emits JSON).
- `scripts/check-release-branch.sh` — Run when: Phase 2 branch check after the
  version is confirmed.
- `scripts/draft-changelog.sh` — Run when: Phase 4 notes drafting.
- `scripts/publish-release.sh` — Run when: Phase 8 `--publish` preview/apply and the
  destructive 8.5.3 re-cut fallback.

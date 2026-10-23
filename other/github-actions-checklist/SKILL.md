---
name: github-actions-checklist
description: Check Actions triggers, permissions, runners, pins, and deadlines.
---

# GitHub Actions checklist

Read applicable `AGENTS.md` and their declared adapter alias, otherwise
`.agents/skills/github-actions-checklist/SKILL.md` from the repository root if present.
Local policy overrides these defaults; do not reload an already-read adapter or canonical skill.

Use before editing a workflow or composite action. Repository-local instructions own runners,
approved action pins, concurrency names, secrets, permissions, and workflow-only pull-request rules.
Apply this baseline unless a stricter local rule overrides it.

## Triggers and required checks

- Use `pull_request` for pull-request workflows in private repositories.
- Reserve `pull_request_target` for base-owned orchestration in a public repository, or for a
  narrowly scoped Dependabot or Renovate workflow.
- A pull-request CI workflow must not subscribe to `ready_for_review` or `converted_to_draft`
  unless a job changes what it does on that transition. Those activity types start another run for
  the same head, and `cancel-in-progress: true` replaces checks that already passed. Dependabot
  auto-merge may keep `ready_for_review`: it enables merge and does not rerun tests.
- A privileged workflow must not check out or execute untrusted pull-request content.
- When changing orchestration, load
  [github-actions-authoring](../github-actions-authoring/SKILL.md). Do not poll remote workflow,
  deployment, lease, service, or health state.
- Required checks must be actual workflow jobs that run or aggregate the work they report.
- Workflow code must not create or publish check runs or commit statuses to synthesize a required
  context, copy another workflow's conclusion, or bypass the event graph.
- An external CI or analysis integration may report its own result. Do not relay GitHub Actions
  work through its API.

## Tests, concurrency, and timeouts

- On `main`, or the consumer's configured default branch, split test jobs by domain, such as web
  and backend. Keep required-check job names stable. Add a bounded fan-in job only when the merge
  contract needs one combined result.
- Serialize test runs for the same pull request or default branch with one stable concurrency group.
- For pull requests, set `cancel-in-progress: true`. On `main`, or the consumer's configured default
  branch, set `cancel-in-progress: false` so the active run finishes before the newest pending
  revision starts. GitHub may replace an older pending main run with the newest pending revision;
  preserving every intermediate queued revision is not required.
- When one workflow handles both events, make `cancel-in-progress` conditional on the pull-request
  event. Keep the pull-request number or branch ref in the group.
- Give every concrete job `timeout-minutes` of at most 30 minutes. A top-level `jobs.<job_id>.uses`
  caller cannot accept `timeout-minutes`; set it on every concrete job in the called workflow.
- If the operation cannot finish inside that bound, split it into event-driven phases. Lowering or
  moving the timeout does not fix the design. Preserve a required job or check name with a bounded
  fan-in job when the split would otherwise change the merge contract.
- Each underlying phase also has a deadline of no more than 30 minutes and supports cancellation,
  rollback, or an explicit terminal retained or recovery state. A callback may report completion. It
  must not hide a longer-running operation in another service.
- Keep each job's `timeout-minutes` below any hard platform limit of its runner so the job's own
  cancellation fires first and `always()`/`cancelled()` cleanup steps still run. Example: no more
  than 14 minutes on a runner with a 15-minute hard cap that `timeout-minutes` cannot raise.
- Give every long-running, network-bound, or waiting step its own `timeout-minutes` inside the job
  budget. Bound every network call, such as `curl --connect-timeout … --max-time …`.

## Runners and persistent workspaces

- Prefer GitHub-hosted runners for public and private repositories. Choose the smallest hosted
  runner the job fits, such as `ubuntu-slim` for a short job that needs no Docker daemon. Use a full
  VM or native-architecture runner only for work the smaller runner cannot do. A consumer that still
  requires self-hosted or disposable runners names its approved labels in repository-local policy.
- Ephemeral hosted runners start from a clean workspace. Do not add workspace-cleanup steps for
  them, and check out with `persist-credentials: false` unless a later step must push with that
  token.
- Moving a job from a self-hosted or other persistent runner to a GitHub-hosted one drops every
  piece of runner-local state the job assumed was already there. Audit browser installs (a
  Playwright, Cypress, or Puppeteer cache), package-manager stores (pnpm/npm, Go modules, a Rust
  `target/` directory, Gradle), `apt-get install` steps that used to be a no-op because the package
  was already present, and Docker image pulls that used to hit a warm local image store. A comment
  that a tool "persists between runs so caching is not needed" describes the old runner and becomes
  false the moment `runs-on` changes; replace that assumption with a keyed `actions/cache` step
  instead. Re-derive `timeout-minutes` from a real passing run on the new runner rather than
  carrying over a budget calibrated on a warm host.
- A persistent workspace checks out the full tree. Do not configure sparse checkout. Enforce that
  with a YAML-aware check over intended tracked workflow and action files, with accepted and
  rejected fixtures.
- Fix workspace ownership at the producer. A writable workspace bind mount uses a non-root identity
  whose ownership and write access match the runner workspace.
- Do not add an unconditional pre-checkout workspace-wide permission or ownership traversal.
- Migrate a contaminated workspace once, while the runner is drained.
- Routine repair may cover bounded known generated paths. A workspace-wide fallback must be
  failure-gated, same-filesystem, directory-only, and batched,
  and must record path count and timing.

## Pinning

- Pin every repository-backed external `uses:` reference — anything other than a local `./...`
  action or a `$/` self-repository reference — to a full lowercase 40-character Git SHA and its
  immediate machine-maintainable version comment, such as `# v4.2.0`, so Dependabot can update both.
- A `$/` reference is the same repository at the running commit. It must not include an `@ref`.
- Pin `docker://...` actions to an immutable `@sha256:` image digest. Keep GitHub Actions dependency
  updates enabled.
- Workflow tests and fixtures must not assert an action dependency's exact SHA or version. Assert
  the action identity and Git SHA shape, or read the ref from the workflow under test.
- This does not prohibit asserting an exact source revision in `with.ref` when exact-head checkout
  is a workflow security invariant.

## Edit

1. Read every applicable `AGENTS.md` from the repository root through the workflow,
   plus CI docs and callers. On conflict, apply the closest instruction. Name trusted inputs,
   untrusted inputs, and every credential boundary.
2. Give each job the least permissions it needs. Keep untrusted pull-request content out of shell
   interpolation, privileged tokens, and write-capable steps.
3. Apply this baseline and any stricter consumer policy. Keep checkout refs, artifact boundaries,
   caches, and concurrency explicit.
4. Validate changed YAML with the local workflow checker and run the affected tests or scripts.
   Update local CI docs when behavior or operator expectations change.
5. Review the diff for privilege escalation, secret exposure, unsafe quoting, unsupported runner
   assumptions, and unreachable paths.

Consumer wrapper owns: runner labels, action SHAs, workflow directories, concurrency scheme, and
release policy.

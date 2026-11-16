---
name: kit-ci-pipeline
description: Write or change CI pipelines (GitHub Actions or GitLab CI) that run the project's real build, lint, and test commands with dependency caching, a version matrix where useful, least-privilege permissions, pinned actions, and safe handling of secrets and untrusted input. Use when the user asks to add, change, speed up, or fix the configuration of a CI workflow, job, or pipeline, including adding a publish, release, or deploy job, which this skill gates. Do not use for diagnosing why an existing run failed (use kit-ci-triage), for security hardening of existing workflows (use kit-hardening), or for Dockerfiles (use kit-dockerfile).
---

# CI pipeline

## 1. Learn the project

Find the commands the project documents for install, build, lint, type check, and test, the runtime versions it supports, the package manager and lockfile, and existing workflows and their conventions. Use those commands; do not invent new ones.

## 2. Write

- **Triggers:** `pull_request` and pushes to the default branch; avoid `pull_request_target` for workflows that check out and run pull request code.
- **Permissions:** a top-level `permissions: contents: read`, raised per job only where needed (in GitLab, protected branches and variables and a restricted `CI_JOB_TOKEN` allowlist).
- **Actions:** official or trusted actions pinned to a full commit SHA with a version comment; `actions/setup-*` with the project's runtime version or a matrix of supported versions.
- **Caching:** the setup action's built-in cache keyed on the lockfile, or `actions/cache` with an explicit key; install with the frozen lockfile.
- **Jobs:** fast checks (lint, type check) and tests as separate jobs or steps that fail clearly; `concurrency` to cancel superseded runs on the same branch; `timeout-minutes` on jobs.
- **Secrets and input:** secrets only in the jobs and steps that need them, never echoed; untrusted values such as pull request titles or branch names passed through `env:` and not interpolated directly into `run:` scripts.
- Deployment or publishing jobs only when the user asks, gated on tags or the default branch and a protected environment. If the user asks to publish or deploy from every push or any branch, explain the risks (unreviewed code shipped, version collisions, leaked credentials) and write the gated version, or ask before writing an ungated one.

## 3. Verify

Validate the syntax with `actionlint` (GitHub) or the GitLab CI lint API or `glab ci lint` when available, and run the same commands locally to confirm they pass. Do not push or trigger runs without the user's instruction; tell them what to watch on the first run.

## 4. Report

Summarize the workflow, triggers, jobs, permissions, caching, verification done locally, and what the user should check on the first run.

## Examples

- Use: "Add a GitHub Actions workflow that runs our tests on Node 22 and 24." "Speed up our CI with caching." "Add a job that publishes releases."
- Skip: "Why is CI failing on my PR?" (kit-ci-triage) "Deploy to production from CI."

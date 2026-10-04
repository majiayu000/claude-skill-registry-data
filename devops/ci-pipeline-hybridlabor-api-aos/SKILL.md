---
name: ci-pipeline
description: >-
  Set up a complete CI/CD pipeline for a project. Detects the stack, then
  generates and validates GitHub Actions workflows, a Dockerfile, and a
  Makefile as one coherent pipeline. Use when asked to "set up CI", "add
  pipeline", "create GitHub Actions", "ci/cd setup", "automate builds",
  "containerize", or "add a Makefile".
category: engineering-method
risk: safe
source: community
date_added: "2026-09-25"
---

# CI/CD Pipeline Setup

**Announce at start:** "I'm using the ci-pipeline skill to set up the pipeline."

**Core principle:** Generate, then validate, then fix. A pipeline that was
never validated is not a pipeline — it is a guess that will fail on someone
else's machine.

This skill is the orchestrator. It does not write workflows, Dockerfiles, or
Makefiles itself — it detects the stack, calls the right generator, routes the
output through the matching validator, and reports the result.

## When to Use

"set up CI", "add pipeline", "create GitHub Actions", "ci/cd setup", "automate
builds", "add Docker", "containerize", "add Makefile".

Not for: debugging an existing pipeline that already runs (read it first), or
infrastructure provisioning — see *What NOT to do*.

## Stack Detection

Before generating anything, detect. Guessing here produces a pipeline that
builds the wrong thing correctly.

1. **Language/runtime** — `package.json`, `pyproject.toml`, `go.mod`,
   `Cargo.toml`, `pom.xml`, `build.gradle`, `Gemfile`
2. **Existing CI** — `.github/workflows/`, `.gitlab-ci.yml`, `Jenkinsfile`,
   `.circleci/`
3. **Docker** — `Dockerfile`, `docker-compose.yml`, `compose.yaml`
4. **Build tool** — `Makefile`, `package.json` scripts, `build.gradle`,
   `Taskfile.yml`

Report what you found before generating. If detection is ambiguous — two
languages, a monorepo with per-package manifests — say so and ask which target
the pipeline should build, rather than picking one.

## Orchestration Flow

Run in this order. Stop on a hard failure; do not generate the next artifact on
top of a broken one.

### 1. GitHub Actions

Invoke `github-actions-generator` with the detected stack.

- **Validator:** `github-actions-validator` — must pass before continuing.
- **Output:** `.github/workflows/ci.yml`, plus `deploy.yml` if a deployment
  target is detected.

### 2. Dockerfile

Only if no `Dockerfile` exists, or the user asked for one. Invoke
`dockerfile-generator`.

- **Validator:** `dockerfile-validator` — must pass before continuing.
- **Output:** `Dockerfile`, `.dockerignore`.

### 3. Makefile

Only if no `Makefile` exists. Invoke `makefile-generator`.

- **Output:** `Makefile` with the targets `build`, `test`, `lint`,
  `docker-build`, `clean`.

### 4. Validation summary

Run every applicable validator once more against the final, combined output and
report the results. A generator that passed in isolation can still produce a set
of files that disagree with each other — the combined pass is what proves the
pipeline works, not the per-step passes.

## The Validation Loop

This is the part that matters, and it is not optional:

1. Run the generator.
2. Run the validator against what it produced.
3. On failure, feed the validator's errors back to the generator.
4. Repeat until clean. **Minimum one full pass** — generating and declaring
   success without ever running a validator has produced a broken pipeline more
   often than not.

If the validator cannot run in the current environment (no `actionlint`, no
Docker daemon), say that explicitly and report which checks were skipped. An
unavailable validator is not a passing validator.

## Output Checklist

Verify before calling this done:

- [ ] `.github/workflows/ci.yml` exists and passes `github-actions-validator`
- [ ] `Dockerfile` exists (if applicable) and passes `dockerfile-validator`
- [ ] `Makefile` exists and `make test` runs locally
- [ ] Every validator ran at least once, and its result is reported — passed,
      failed, or skipped-with-reason
- [ ] No secrets, tokens, or environment values hardcoded in any generated file
- [ ] Generated files are ready to commit but **not** committed

## What NOT to do

- **Do not commit.** Leave the files staged for review. Committing and pushing
  a pipeline is a separate, explicit request.
- **Do not overwrite existing `.github/workflows/` or an existing `Dockerfile`
  without showing the diff first.** Existing pipelines usually encode a reason
  — a private registry, a matrix, a self-hosted runner — that a regenerated file
  silently drops.
- **Do not generate Terraform, Helm, or Kubernetes manifests** unless
  explicitly asked. Deployment infrastructure is a different job with different
  blast radius; `helm-generator` and the k8s skills exist for it.
- **Do not invent a validator result.** Report what ran and what did not.
- **Do not use `github-actions-templates`** for new work — it is superseded by
  `github-actions-generator`.

## Related

- `bash-script-generator` / `bash-script-validator` — helper scripts the
  pipeline calls, when the workflow needs more than a Makefile target
- `github-actions-templates` — superseded, kept for its existing patterns
- `vercel-deployment` — deployment specifics for Vercel targets
- `deploy-incus` — Forgejo-to-Incus push deployment

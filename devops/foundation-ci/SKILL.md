---
name: foundation-ci
description: Generate a CI/CD pipeline tailored to the project's actual stack — author `.github/workflows/ci.yml` (or equivalent) with lint + test + build stages, mirror Makefile targets so devs can run identical commands locally, and gate it green on the current codebase. Loads when no CI exists yet, or when the operator says "set up CI", "add GitHub Actions", "wire up the pipeline".
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
effort: medium
---

# foundation-ci

The foundation skill that authors a project's continuous-integration pipeline. AICP and sister fleet projects standardize on GitHub Actions with stage parity to local Makefile targets — every CI step has a `make` equivalent so developers reproduce CI locally before pushing.

## Trigger phrases (when to load this skill)

Load when the conversation matches any of:

- **No CI exists**: project has no `.github/workflows/`, no `.gitlab-ci.yml`, no `azure-pipelines.yml`, no equivalent. Operator wants to bootstrap.
- **Direct verb**: operator says "set up CI", "add GitHub Actions", "wire up the pipeline", "give us a CI/CD config", "automate testing on push".
- **Foundation-stage of project-lifecycle**: a new sister project hits the foundation stage; CI is one of the foundation deliverables.
- **CI replacement**: existing CI is broken, abandoned, or wrong tool — operator wants to start over.

Do NOT load when:

- CI exists and is working but slow or noisy — load `quality-lint` (lint-specific) or `feature-iterate` (refine the existing pipeline).
- The ask is "deploy this somewhere" — load `ops-deploy` (executes a deploy) or `config-deploy` (per-env config).
- The ask is "add a new test job to existing CI" — load `feature-implement` with the test job as the deliverable; this skill is for greenfield CI.
- The project is single-operator local-only and the operator explicitly doesn't want CI — respect that; CI for personal scripts is over-engineering.

## Operations

This skill has 4 named operations. Execute in order.

### Operation 1: Detect the stack and pipeline shape

**Trigger**: skill loaded; operator confirmed greenfield CI.

**Process**:

1. Detect the language + tooling by reading manifests:
   - **Python**: `pyproject.toml` / `setup.py` / `requirements*.txt` → ruff, pytest, mypy.
   - **Node**: `package.json` → eslint, jest/vitest, tsc.
   - **Rust**: `Cargo.toml` → clippy, cargo test.
   - **Go**: `go.mod` → gofmt, go vet, go test.
   - **Mixed**: handle each via separate jobs.
2. Detect the platform from existing infrastructure:
   - `.git/config` URL contains `github.com` → GitHub Actions (`.github/workflows/ci.yml`).
   - `.gitlab-ci.yml` history → GitLab CI.
   - Operator-stated preference overrides detection.
3. Detect Python version requirements: `pyproject.toml` → `requires-python` field. AICP-domain default: 3.11+.
4. Identify the gate commands per the project's [domain profile](../../../wiki/config/domain-profiles/) (for AICP-domain: `ruff check + ruff format --check + pytest -x`).
5. State the plan to the operator: platform / language / matrix dimensions (if any) / gate commands. Wait for "go".

**Quality bar (Operation 1 done when)**:

- [ ] Stack detected from manifests, not guessed.
- [ ] Platform chosen with operator confirmation.
- [ ] Python/Node/Rust/Go version requirements extracted from manifest (not picked from defaults).
- [ ] Gate commands match the project's domain profile.
- [ ] Matrix decision made (single version vs N versions) with rationale.

### Operation 2: Author the pipeline file

**Trigger**: Operation 1 plan approved.

**Process**:

1. Write the pipeline file. For GitHub Actions Python (AICP-domain default), the structure is:

   ```yaml
   name: CI
   on:
     push: { branches: [main] }
     pull_request: { branches: [main] }
   jobs:
     lint:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4
         - uses: actions/setup-python@v5
           with:
             python-version: "3.11"
             cache: pip
         - run: pip install -e ".[dev]"
         - run: ruff check aicp/ tests/
         - run: ruff format --check aicp/ tests/
     test:
       needs: lint
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4
         - uses: actions/setup-python@v5
           with:
             python-version: "3.11"
             cache: pip
         - run: pip install -e ".[dev]"
         - run: pytest tests/ -x --tb=short
   ```

2. Stage ordering: **lint before test** — lint failures are fast-fail and shouldn't burn 7 minutes of test runtime first.
3. Pin actions to specific major versions (`@v4`, not `@latest`) — `@latest` is non-deterministic and breaks reproducibility.
4. Cache dependency manager (`cache: pip` / `cache: npm` / `cache: cargo`) — first-run pays the install cost; subsequent runs reuse.
5. Author or update Makefile targets that EXACTLY mirror CI gates (so `make lint && make test` locally is byte-equivalent to what CI runs):
   ```make
   lint: ; ruff check aicp/ tests/ && ruff format --check aicp/ tests/
   test: ; pytest tests/ -x --tb=short
   ci: lint test
   ```
6. Add the CI status badge to the top of README.md (`![CI](https://github.com/<org>/<repo>/workflows/CI/badge.svg)`).

**Quality bar (Operation 2 done when)**:

- [ ] Pipeline file at the right path for the platform.
- [ ] All gate commands from Operation 1 represented as steps.
- [ ] Lint stage gates the test stage (fail-fast).
- [ ] Actions pinned to specific majors, not `@latest`.
- [ ] Dependency cache configured.
- [ ] Makefile has matching `lint`, `test`, `ci` targets that run the SAME commands.
- [ ] README has CI badge linked to the workflow.

### Operation 3: Validate the pipeline locally before pushing

**Trigger**: Operation 2 file written.

**Process**:

1. Run `make lint` locally. Must exit 0. If not, fix the underlying issues OR adjust the rule set in pyproject.toml — don't ship a CI that's known-red on day one.
2. Run `make test` locally. Must exit 0.
3. For GitHub Actions specifically: validate workflow syntax with `gh workflow view <name> --validate` if `gh` CLI is available, OR push to a feature branch and watch the first run.
4. Confirm cache works on second run: trigger CI twice (e.g., empty commit), verify second run reports cache hit on dependency install (saves ≥30s typically).
5. If anything fails on the cloud runner that passed locally, the diagnostic question is environment difference — Python version, OS package, missing dev dep. Fix locally, re-push.

**Quality bar (Operation 3 done when)**:

- [ ] `make lint && make test` exits 0 locally.
- [ ] First CI run on a feature branch is green.
- [ ] Second run reports cache hit (or equivalent speedup).
- [ ] Failure modes (lint fail, test fail) tested by deliberately breaking each and confirming CI catches it.

### Operation 4: Document and hand off

**Trigger**: Operation 3 confirmed green.

**Process**:

1. Document the pipeline in README.md or `docs/ci.md`:
   - What runs on push vs PR.
   - How to reproduce CI failure locally (`make ci`).
   - How to add a new gate (the standard pattern: add Make target, mirror in workflow file).
2. If branch protection is set up, suggest gating merges on the `lint` and `test` checks.
3. Note any deferred items for a follow-up task: deploy stage (commented placeholder), security scan (`pip audit`, `npm audit`), coverage report upload, multi-Python matrix.
4. Suggest the next foundation skill if applicable: `foundation-testing` for richer test infra, `foundation-docker` if containerized testing is needed.

**Quality bar (Operation 4 done when)**:

- [ ] CI documented in README/docs with the local-reproduction recipe.
- [ ] Branch-protection suggestion stated (operator decides).
- [ ] Deferred items listed as a follow-up task, not silently dropped.
- [ ] Next-step skill suggested if applicable.

## Gotchas (known failure modes — read before doing)

### Gotcha 1: CI green that diverges from local

CI runs `python -m pytest`; local Makefile runs `pytest` directly. They use different resolution paths and can produce different results — usually because of a stray `conftest.py` in cwd vs not. Developer thinks "tests pass locally" but CI fails (or the reverse).

**The rule**: Makefile targets and CI workflow run the SAME literal command line. Copy-paste, don't paraphrase. If CI has `pytest tests/ -x`, Makefile has `pytest tests/ -x` — same flags, same path, same args.

### Gotcha 2: `@latest` action versions

Pinning `actions/checkout@latest` (or `@main`) — feels future-proof but actually means CI is non-deterministic. A breaking change in the action ships, your CI breaks for "no reason".

**The rule**: pin to a major (`@v4`) at minimum, ideally a specific SHA for security-critical actions. Document the upgrade cadence: "we re-pin majors every quarter."

### Gotcha 3: No dependency cache

Every CI run pays the full `pip install` (or `npm install`, etc.) cost. A 30-second install × 50 PRs/week = 25 minutes/week of pure wait time. Caches are 3 lines of config and save 10-30 seconds per run.

**The rule**: every step that resolves dependencies has `cache:` configured. Verify on second run by reading the action log — it should say "Cache restored from key X".

### Gotcha 4: CI-only style rules

Adding `--strict` flags to lint/typecheck in CI that aren't enforced locally. Result: developers push thinking they're clean, CI rejects, they're frustrated. Or: developers add `# noqa` to bypass CI without understanding the rule.

**The rule**: same tool config in CI and local. If CI runs `ruff check --select E,F,I`, local `make lint` runs the SAME selection. The Makefile is the source of truth; CI invokes Makefile (or copies the literal command).

### Gotcha 5: Stage ordering that wastes runtime

Putting test as the first stage (no lint gate). A 1-line ruff violation that would fail in 5 seconds takes the full test suite (~7 min in AICP) to fail because the lint never ran. Burns CI minutes and developer wait.

**The rule**: cheapest stage runs first. lint (5s) → typecheck (15s) → test (7min) → build (varies). Each stage only runs if the previous passed. Use `needs:` in GitHub Actions to enforce.

## Reference exemplars

The Extension Standards reference exemplars for skills are the second brain's `model-builder` and `wiki-agent` skills — see `~/devops-solutions-research-wiki/skills/`. This skill follows their structure: trigger phrases, multiple named operations, per-operation Process + Quality bar, Gotchas with detection + rule + reasoning.

## Domain context

This skill operates in the **backend-ai-platform-python** domain. Default gate commands for that domain (per [wiki/config/domain-profiles/backend-ai-platform-python.yaml](../../../wiki/config/domain-profiles/backend-ai-platform-python.yaml)):

- `ruff check --select F,E aicp/ tests/` (document/design stages)
- `ruff check + ruff format --check` (scaffold)
- Above + `pytest tests/ -x --tb=short` (implement)
- Above + full `pytest tests/` + test count drift check (test stage)

CI mirrors the test-stage gate (full suite + drift check).

## Related skills

| Skill | When | Why distinct |
|-------|------|--------------|
| foundation-testing | Set up the test framework itself | foundation-ci runs tests; foundation-testing AUTHORS them |
| foundation-docker | Containerize the build/test environment | foundation-ci runs in a runner; foundation-docker provides the environment |
| ops-deploy | Run a deployment from CI artifacts | foundation-ci builds; ops-deploy ships |
| quality-lint | Tune the lint rules themselves | foundation-ci runs lint; quality-lint decides what passes |
| feature-test | Author tests for a single feature | foundation-ci is the harness; feature-test fills it |

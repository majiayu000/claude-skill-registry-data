---
name: rseng-ci-cd
description: >-
  Covers continuous integration and delivery for research software: CI/CD
  concepts, automating builds and tests with GitHub Actions and GitLab CI/CD,
  and wiring an organization's GitLab CI infrastructure to a GitHub-hosted
  project. Use when the user asks to set up CI, write a pipeline or workflow
  file (.github/workflows, .gitlab-ci.yml), add automated builds/tests on push
  or pull request, publish a package or deploy docs when a tag or release is
  cut, cache dependencies to speed up CI runs, choose between GitHub Actions
  and GitLab CI, use self-hosted or GPU runners, mirror a repo, or report
  external CI status back to GitHub. For what to test and shrinking a test matrix see rseng-testing; for
  linter and pre-commit policy see rseng-code-quality.
license: CC-BY-4.0
metadata:
  version: 0.1.0
---

# Continuous integration and delivery for research software

Use this skill when a project needs to automate its build, test and
release path, or when someone is deciding how to run CI for research
software. It covers CI/CD concepts, GitHub Actions,
GitLab CI/CD, and hybrid setups where a GitHub project runs on an
organization's GitLab runners. Prefer concrete, minimal pipelines first,
then grow them; do not scaffold monitoring, mirroring or multi-runner
infrastructure a small project will not use.

## Core concepts

Distinguish the three practices before recommending tooling:

- Continuous Integration (CI): integrate code changes into a shared
  repository frequently, and verify every change with an automated build
  that compiles and runs tests. Catches integration errors early.
- Continuous Delivery (CD): keep software always in a deployable state;
  the release to production stays a manual decision. Value: fast, safe
  rollbacks and few manual release steps.
- Continuous Deployment (CD): go further and deploy every passing change
  to production automatically, with no manual gate.

When advising, name which of the three the user actually wants. Most
research projects need solid CI plus Continuous Delivery, not fully
automated Continuous Deployment.

## What a pipeline should cover

Map the project's needs onto these stages before writing YAML:

- Automated builds triggered on every change (compile plus tests).
- Version-control integration so commits and pull requests trigger runs.
- Automated unit, integration and regression tests across the platforms
  and dependency versions the software claims to support.
- Code-quality gates: static analysis or linters, and pre-commit
  (https://pre-commit.com/) hooks run in CI, not only locally.
- Deployment pipelines that package artifacts ready to ship.
- Monitoring and rollback for anything deployed to production.

## Choosing a platform

Match the tool to where the repository lives and what hardware it needs:

- GitHub-hosted, standard hardware: use GitHub Actions. It is integrated,
  has a large marketplace, and free runners for public repos.
- GitLab-hosted: use GitLab CI/CD. It is the GitLab-native equivalent of
  GitHub Actions.
- Migrating from Actions to GitLab: point the user at GitLab's dedicated
  Actions-migration guide rather than rewriting by hand.
- Specialized hardware (GPUs, ARM/Power CPUs, HPC) or heavy test matrices
  that exceed GitHub's free tier: consider running on an organization's
  GitLab runners, even for a GitHub-hosted project (see the hybrid section).
- Other established options exist (Jenkins, CircleCI, Travis CI, Azure
  Pipelines, Bitbucket Pipelines); recommend them only when the project is
  already on that ecosystem.

## GitHub Actions

Set up a workflow with these steps:

- Create a `.github/workflows/` directory; put one YAML file (`.yml` or
  `.yaml`) per workflow there.
- Choose triggers under `on:` -- typically `push`, `pull_request`, or a
  `schedule`. Pick the events that match how the team collaborates.
- Select a runner OS with `runs-on:` (Ubuntu, Windows, or macOS); use a
  matrix when the software must work across several.
- Reuse marketplace actions instead of hand-rolling steps:
  `actions/checkout` to check out the code and `actions/setup-python`
  (or the relevant language setup) to provision the toolchain. A major
  tag like `@v7` is readable but mutable; pinning means a full commit
  SHA with the tag in a trailing comment, which is what
  rseng-security asks for on third-party actions.
- Store credentials and API keys as repository secrets; never inline them
  in the workflow file.
- After pushing, read results in the Actions tab: the run graph shows job
  sequence, and expanding a job exposes per-step logs for debugging.

Minimal test workflow for a Python project:

```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v7
      - name: Setup Python
        uses: actions/setup-python@v7
        with:
          python-version: '3.13'
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      - name: Run tests
        run: pytest
```

Adapt the language setup and install command to the project; keep the
first working pipeline this small, then extend.

## GitLab CI/CD

Set up a pipeline with these steps:

- Create a `.gitlab-ci.yml` at the repository root; it defines pipelines
  and jobs in YAML.
- Runners: on gitlab.com, instance runners are provided automatically; on
  a self-hosted GitLab, confirm runners are available first.
- Structure work into `stages`; jobs in the same stage run in parallel
  (given enough runners), and a later stage starts only after the previous
  one finishes. Each job needs at least `stage` and `script`.
- If one job needs another's output, put them in separate stages and pass
  results as artifacts -- parallel jobs in one stage cannot depend on each
  other.
- Reuse pre-built components from the GitLab CI/CD Catalog rather than
  writing everything from scratch; most ship a README with configuration.
- Watch runs in the Pipelines tab, drilling into stages and jobs for
  status and logs.

Skeleton `.gitlab-ci.yml` showing the stage/job structure:

```yaml
stages:
  - build
  - deploy

build-job:
  stage: build
  script:
    - echo "Starting build"

deploy-job:
  stage: deploy
  script:
    - echo "Deploy"
```

For real pipelines, point users at GitLab's quick-start and advanced
tutorials and its per-language examples rather than inventing job scripts.

## Hybrid: GitLab CI for a GitHub-hosted project

Only recommend this when a GitHub project genuinely needs hardware or
capacity beyond GitHub's free runners (GPUs, ARM/Power, HPC, large
matrices) and the organization already runs GitLab with suitable runners. It is real operational
overhead -- flag that cost explicitly to small teams before they commit.

The moving parts to design:

- Repository mirroring: use GitLab native mirroring to sync the GitHub
  repo into GitLab. Mirror only main/protected branches initially to
  limit load and exposure; mirroring needs a deploy key or token with
  write access to the GitHub repo.
- Fork integration: forks complicate external CI. A webhook-driven bot can
  watch pull-request events and create matching branches in the GitLab
  mirror using a systematic naming convention; clean those branches up when
  the PR closes.
- Webhook security: validate webhook signatures with a secret, return HTTP
  200 immediately and process asynchronously, and retry failed GitLab API
  calls with exponential backoff (dead-letter events that never succeed).
- Status reporting: push GitLab pipeline results back to GitHub via the
  commit status API, keyed on commit hash, using stable check names like
  `gitlab-ci/<job>` so PR checks reflect the external run.
- Runners: tag runners by capability (for example `gpu`, `nvidia`,
  `arm64`) and target them from jobs with matching `tags:`. Organize as
  shared, group, and project-specific runners so specialized hardware is
  allocated fairly.
- Access and security: map GitHub permissions to GitLab roles (admin ->
  maintainer, write -> developer, read -> reporter), grant external
  contributors time-limited guest access to logs, and keep audit logs of
  webhooks, mirroring, access changes and pipeline triggers.
- Reliability and monitoring: rotate API tokens (updating webhook configs
  in lockstep so auth does not desync), and monitor webhook success rate,
  mirror-sync delay and runner availability with alert thresholds.

Document the hybrid setup for contributors: how to read status checks,
reach GitLab logs, and request runner access.

A concrete workflow set for research Python packages (NLeSC
python-template): build, link-check, docs build, SonarCloud analysis
and cffconvert citation validation - plus its next_steps.yml pattern,
which opens onboarding issues for manual setup steps (Zenodo,
SonarCloud, Read the Docs) so scaffolded projects finish their setup.

## Working with this skill

The generated references.md beside this file lists the source material
and pointers:

- references.md - verified Learn more pointers

Learn more (verified):
  - https://docs.github.com/en/actions - GitHub Actions documentation
  - https://docs.gitlab.com/ci/ - GitLab CI/CD documentation
  - https://coderefinery.github.io/testing/ - CodeRefinery automated
    testing lesson
  - https://book.the-turing-way.org/reproducible-research/ci -
    Turing Way continuous integration chapter

<!-- related-skills:begin -->

## Related skills

Check whether any of these applies before moving on:

- rseng-green-computing - pipeline energy and runner cost
- rseng-hpc-computing - GPU/HPC runners for heavy jobs
- rseng-publishing-releasing - release automation triggered from CI
- rseng-reproducible-environments - testing inside the shipped container
- rseng-security - secrets management in pipelines
- rseng-testing - what the pipeline should actually run

<!-- related-skills:end -->

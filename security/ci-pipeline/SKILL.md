---
name: ci-pipeline
description: The Build Pipeline workflow - its jobs, the six required checks, the Summary comment, the monthly schedules, and how to fix a failing check without weakening it. Use when a check fails, when changing .github/workflows, or when explaining what CI does.
metadata:
  scope: repository
---

# CI pipeline

## The rule

One workflow, `.github/workflows/build-pipeline.yml`, runs on every pull request, every push to `main`, two monthly schedules and on demand. Jobs run as a chain, and these six are required checks:

| Check | What it does | Fails when |
| --- | --- | --- |
| Build | `dotnet format --verify-no-changes`, `docker build` of the runtime image, `dotnet pack` of the template, the report action's own tests | Style, a warning, a build error, or a template package over 1 MB |
| Test | Runs every test project inside the Dockerfile's `test` stage, reports results and coverage, then installs the packed template, generates a solution (its restore post action restores the `.slnx`), checks its format, tests it and checks it has `.github/workflows/ci.yml`, then does the same with `--include-auth` where the template has it | A failing test, coverage under 95%, or a template that doesn't generate, format and pass |
| Static Analysis (actions, csharp) | CodeQL `security-and-quality` on the workflows and the C# | A finding of medium severity or higher |
| Dependency Review | New or updated packages on a pull request | A high or critical vulnerability, or a licence other than MIT, Apache-2.0 or BSD |
| Container Scan | Starts the image and calls it, then Trivy scans the image and the Dockerfile and compose config | The smoke test fails, or a fixable high or critical finding |
| Summary | Posts one comment on the pull request with a row per check, built by `.github/actions/pipeline-report` | Any check above failed |

After those, Release Check and Publish only run on the monthly release (`releases`).

A copy made with GitHub's "Use this template" gets this workflow with no secrets or setup. Outside the LeanMeanCleanApps organisation it runs only the format check, build and tests: Static Analysis, Dependency Review, Container Scan, the template's pack and verify steps, Release Check and Publish all check `github.repository_owner` and skip, and the Summary shows them as not run. Skipped jobs count as passed for required checks, so a private copy goes green without Advanced Security. A solution made with `dotnet new` gets the much smaller `template/ci.yml` as `.github/workflows/ci.yml` instead. `ci-for-your-solution` covers both. Keep any new job that needs Advanced Security, a secret or the template folders behind the same owner check.

## Steps

1. Read the Summary comment first; it names the unhappy check and links to its details.
2. Reproduce locally where you can (every command finds the `.slnx` in the root on its own): `dotnet format --verify-no-changes`, `dotnet build`, `dotnet test`, the coverage command in `coverage`, `docker build . --target run`.
3. Fix the cause in the code. For security findings, see `security-findings`.
4. Changing the workflow itself: keep each tool as an off-the-shelf action, keep the job names (they're the required check names), and keep everything working in someone else's copy of the template with no secrets or setup.

## Don't

- Skip, disable or mark a test as skipped to get green.
- Lower `COVERAGE_THRESHOLD`, raise `TEMPLATE_MAX_SIZE`, or relax a severity to pass.
- Rename a job without updating the repository's required checks.
- Add a step that needs an account, a paid service or a secret to pass on a fresh copy.
- Push an empty commit to re-run CI. Re-run the job from the Actions page.

## Check

Every required check is green on the pull request, and the Summary comment shows no red rows.

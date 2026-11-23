---
name: ci-for-your-solution
description: How CI works in a solution made from this template - the ci.yml that dotnet new ships, the Build Pipeline a "Use this template" copy keeps, and how to add security scans or a container check, or move the pipeline to Azure Pipelines, GitLab or another CI system. Use when CI fails on a fresh solution, when adding a check, or when the engineer asks how to set up CI anywhere other than GitHub Actions.
metadata:
  scope: shared
---

# CI for your solution

## The rule

Every solution starts with a simple pipeline that runs the commands in `AGENTS.md`: format, build, and test with the 95% coverage gate. It needs no secrets, no paid features and no setup, so it's green on the first push. Anything more is added on purpose, with the engineer, one check at a time.

| Made with | Pipeline | What runs |
| --- | --- | --- |
| `dotnet new` | `.github/workflows/ci.yml` | Restore, format, build, test and the coverage gate |
| "Use this template" on GitHub | `.github/workflows/build-pipeline.yml`, the template's own | Format, build and test. The scans and the template's pack, verify and release jobs only run in the LeanMeanCleanApps organisation, and show as not run anywhere else |

The **Set up CI** guide for your template on the [Lean Mean Clean Apps docs site](https://leanmeanclean.dev/) shows both, and links the template's full Build Pipeline as a worked example of every check below.

## Adding a check

| Check | Local command | Fails when | Needs |
| --- | --- | --- | --- |
| Vulnerable packages | `dotnet list package --vulnerable --include-transitive` | A package has a known high or critical vulnerability. The command always exits 0, so fail the step when its output contains `High` or `Critical` | Nothing |
| Dependency review | GitHub's `actions/dependency-review-action` on pull requests | A new package is vulnerable or has a licence the team doesn't allow | GitHub Advanced Security on a private repository |
| Container | `docker build . --target run` | The image doesn't build. Add an image scanner such as Trivy if the team ships the container | Docker on the runner |
| Static analysis | The CI system's own scanner, such as CodeQL on GitHub | A security finding the team hasn't accepted | GitHub Advanced Security on a private repository |

## Steps

1. **Start green.** Push the solution and check the pipeline passes before changing it. If it fails on a fresh solution, run the same command locally and fix the cause, not the pipeline.
2. **Agree what to add.** Ask about each check in the table on its own, with a recommendation. Vulnerable packages needs nothing, so recommend it first. Say up front when a check needs Advanced Security or another paid feature.
3. **Add it as its own step or job.** Use the system's standard task or action, and run the exact local command from the table.
4. **Moving off GitHub Actions?** Port `ci.yml` step for step to the team's system, such as Azure Pipelines, GitLab CI or Jenkins: install the SDK from `global.json`, then the same commands in the same order. Delete `ci.yml` once the new pipeline is green.
5. **Prove it.** Open a pull request so the pipeline runs on itself. Then break something on purpose, like a formatting change or a failing assertion, and check it goes red before you put it back.
6. **Hand over.** Tell the engineer which checks to make required on the main branch. That's their setting, not yours.

## Coverage

Coverlet merges every test project into one report, so the gate checks the merged total once, at the end. A per-project Coverlet threshold would judge each project on a partly merged report. Keep the settings in `ci.yml` in step with `coverage`.

``` yaml
- run: >-
    dotnet test --configuration Release --no-build -m:1
    -p:CollectCoverage=true -p:CoverletOutput=../results/ -p:MergeWith="../results/coverage.json"
    -p:CoverletOutputFormat=opencover%2cjson
    -p:ExcludeByFile="**/Program.cs%2c**/Migrations/*.cs%2c**/obj/**/*.cs"
    -p:ExcludeByAttribute="GeneratedCodeAttribute"
- run: |
    coverage=$(grep -o -m1 'sequenceCoverage="[0-9.]*"' tests/results/coverage.opencover.xml | grep -o '[0-9.]*')
    awk -v c="$coverage" 'BEGIN { exit (c < 95) }'
```

## Don't

- Copy the template-only jobs from the Build Pipeline: packing and verifying the template, Release Check and Publish.
- Make a check depend on a secret, a paid service or an account to pass on a pull request, unless the engineer has agreed to it.
- Lower the coverage threshold or skip a test to get a run green. Fix the cause (`coverage`, `test-design`).
- Run different commands in the pipeline from the ones in `AGENTS.md`. If one has to change, change both.
- Set up the CI system, runners, Advanced Security or branch rules yourself. Write the pipeline and say what the engineer needs to switch on.

## Check

- The pipeline runs on a pull request and every check is green.
- A deliberate formatting change or failing test turns it red.
- `dotnet format --verify-no-changes`, `dotnet build` and `dotnet test` pass locally on the same commit.

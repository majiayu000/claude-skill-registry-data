---
name: dependabot
description: Use when configuring or operating Dependabot across many repositories — generating dependabot.yml from the manifests that actually exist, grouping minor and patch updates, limiting open pull requests, choosing weekly or monthly schedules by repository activity, and merging update PRs safely one at a time. Also use when update PRs pile up, conflict with each other, fail on peer dependencies, or burn CI minutes.
---

# Dependabot at scale

Default: `dependabot.yml` generated from the manifests present in each repository, one group per ecosystem for minor + patch, majors as individual PRs, a small open-PR limit, and a serial merge procedure that waits for each rebase and green check.

## Generate, do not hand-write

- Scan each repository for real manifests (`package.json`, `requirements*.txt`/`pyproject.toml`, `go.mod`, `Cargo.toml`, `*.csproj`, `Gemfile`, `mix.exs`, `pubspec.yaml`, `Dockerfile`, workflow files) and emit one `updates` entry per ecosystem and directory.
- Entries for manifests that do not exist produce errors; entries missing for real manifests leave dependencies unwatched.
- Schedule by activity: weekly for actively developed repositories, monthly for the rest.

```yaml
version: 2
updates:
  - package-ecosystem: npm
    directory: /
    schedule: { interval: weekly }
    open-pull-requests-limit: 3
    groups:
      npm-minor-patch:
        update-types: [minor, patch]
```

## Ecosystems without support

If the language's package manager is not supported, track the Docker base image (`package-ecosystem: docker`) and note in the repository why.

## Merging safely

Merging several update PRs at once causes conflicts and stale checks. Process one repository's PRs serially:

1. Pick the oldest open update PR.
2. Ask the bot to rebase if it is behind (`@dependabot rebase`) and wait until the new head commit has finished checks.
3. Merge only when checks are green on that head commit.
4. Repeat; the next PR will need a rebase after the previous merge.

Automate this as a script rather than clicking; it is the part people get wrong under time pressure.

## Failing updates

- **Peer dependency errors (`ERESOLVE`)**: packages that must move together (e.g. a framework and its renderer, or a library and its type definitions) need one combined PR; close the bot's partial PRs and update them together by hand.
- **Major updates** may need code changes: read the changelog, update, run the full local test suite, and mention the migration in the PR.
- **A tool pinned by another tool** (e.g. a build system that only supports older TypeScript): hold the update with a comment and an issue for the real fix (migrating the build tool).

## Verification loop

1. The configuration validates (the repository's Insights → Dependency graph → Dependabot shows no errors).
2. After a merge, the default branch builds and tests pass locally.
3. Open update PRs per repository stay under the limit.

## Pitfalls

- **Grouping too broadly** mixes risky and trivial changes; keep majors separate.
- **Ignoring forever** with `ignore` rules hides security fixes; prefer time-boxed holds tracked in an issue.
- **CI cost:** each update PR runs your gates; grouping and limits keep this predictable.
- **Lockfile-only updates** still change behaviour; run tests, do not auto-merge blindly.

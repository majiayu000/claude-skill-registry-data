---
name: releases
description: The monthly release of the template - the 1st-of-the-month schedule, the Release Check that skips a month with no changes, the Publish job (SBOM, attestation, NuGet push, GitHub release), version numbers, dry runs and out-of-cycle releases. Use when preparing for a release, rehearsing one, releasing out of cycle, or working out why a release did or didn't happen.
metadata:
  scope: repository
---

# Releases

## The rule

The template releases once a month, on the 1st at 09:17 America/Chicago, from `main`, with everything merged since the last release. A month where nothing outside `.github/` changed doesn't release. Nobody publishes by hand: releases only come from the Build Pipeline (`ci-pipeline`), and only in the LeanMeanCleanApps organisation, so a copy of the template never tries to publish.

| When | What runs |
| --- | --- |
| The 1st, 09:17 America/Chicago | The full pipeline on `main`, then Release Check and Publish |
| The 1st, after the release | The month's numbers are recorded (see After the 1st) |
| The 2nd | The organisation's project board moves the month's work to Released and closes its milestone |
| The 15th, 09:17 America/Chicago | Maintenance: Dependabot's grouped pull request and a scheduled build. No release |

Versions are the build date and run number, `YYYY.MM.DD.<run>`, like `2026.12.01.214`. Pull request builds add `-pr-<number>` and never publish. The milestone for a release is named after its date, like `2026.12.01`.

## Steps

### What the pipeline does

1. **Release Check** runs after Summary passes. It compares `HEAD` with the latest GitHub release tag, ignoring `.github/`. No changes means no release, unless `force` is set.
2. **Publish** downloads the packed template and logs in to NuGet with trusted publishing (`NuGet/login`, no stored API key). It publishes the Presentation project to build an SPDX bill of materials, attests the package, pushes it to nuget.org and creates the GitHub release with the package, the SBOM and notes generated from the pull request labels (`branches-and-pull-requests`).
3. A scheduled release opens its notes with "Monthly release for <month>". A manual one says "Out-of-cycle release".

### Before the 1st

1. Make sure everything meant for the month is merged and `main` is green.
2. Rehearse: run **Build Pipeline** from the Actions page with `run: release` and `dry-run: true`. It runs Release Check and Publish, logs in to NuGet and builds the SBOM, but pushes, attests and releases nothing. Dry runs work from any branch.
3. Read the run summary: Release Check says what it compared and whether it would publish.

### After the 1st

Record the month's numbers once the release is out: NuGet downloads, stars, forks and the last 14 days of traffic for every public repository. The commands are in `metrics/` in the organisation's private scripts repository, and one run covers all five templates, so do it once, not five times. GitHub only keeps 14 days of traffic, so a missed month is gone for good.

### An out-of-cycle release

For a fix that can't wait for the 1st, run **Build Pipeline** on `main` with `run: release`, `dry-run: false` and, only if the change is in `.github/` alone, `force: true`. Give it its own dated milestone on the board.

## Don't

- Push a package to NuGet or create a release by hand. It skips the SBOM, the attestation and the notes.
- Use `force` to release a month with no real change. No changes, no release.
- Delete or edit a past release. Each release stays, so anyone can go back to it.
- Add a secret or account that a copy of the template would need for its pipeline to pass. Publishing is guarded by the repository owner for that reason.
- Release from a branch other than `main`.

## Check

- The dry run's summary shows Release Check with `Publish: true` and a Publish job that finished.
- After a real release: the new version is on nuget.org, the GitHub release has the `.nupkg` and the `.spdx.json`, and `dotnet new update` picks it up.

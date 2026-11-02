---
name: release-cli
description: Use when cutting a release of a CLI — SemVer over the CLI surface, changelog-driven release notes, tag-triggered CI, per-language distribution (npm, GoReleaser, PyPI, cargo-dist), signed or provenance-bearing artifacts, and install plus verify instructions in the README.
---

# Release CLI

A release is a pushed `vX.Y.Z` tag; CI builds, publishes and signs from it. This skill puts the version discipline, the changelog, the workflow and the registry wiring in place so the tag is the only human action left.

All rules with reasons, and the full per-language workflow/config files: [release-patterns.md](release-patterns.md). Versions: [stack-versions.md](../_shared/stack-versions.md) (verify live first, per [version-protocol](../../core/_shared/version-protocol.md)).

## 1. Audit current state

Change nothing yet. Read `.claude/stack-profile.md` (then `~/.claude/stack-profile.md`); if absent, detect.

```bash
cat .claude/stack-profile.md 2>/dev/null | sed -n '1,30p'
ls .github/workflows 2>/dev/null
ls .goreleaser.y* dist-workspace.toml CHANGELOG.md scripts/release-notes.sh 2>/dev/null   # release machinery
grep -n '"version"' package.json 2>/dev/null
grep -n '^version' pyproject.toml Cargo.toml 2>/dev/null
git tag -l 'v*' | tail -5                          # tags so far and their naming
grep -rn 'homebrew' .goreleaser.y* dist-workspace.toml 2>/dev/null | head -3   # tap wired?
```

Record: language(s), the current version and whether a tag matches it, which release files exist, and which distribution channels are already wired (npm/PyPI trusted publishing, Homebrew tap, GitHub environments, tag protection).

## 2. Decide what to do

- No release machinery → full setup (steps 3-7).
- Some pieces exist → apply only the missing ones (steps 5-6). Name each gap you will close.
- Tag-triggered workflow, changelog gate, signing, registry wiring and README verify table all present → say "already in place" and stop.

## 3. Detect the track

Pick from `languages` in the profile or from step 1:

| Language | Pipeline | Signing / provenance |
|---|---|---|
| TypeScript | npm trusted publishing; `tsdown` build, `pnpm pack` + `npm publish` | npm provenance (automatic with trusted publishing) |
| Go | GoReleaser; `homebrew_casks` with a `binary` stanza into the tap (`brews` is deprecated since GoReleaser v2.10; see [release-patterns.md](release-patterns.md)) | cosign keyless signature on `checksums.txt`, syft SBOM |
| Python | `uv build --no-sources` + `uv publish --trusted-publishing always`; PyPI pending publisher | PyPI attestations (automatic with `uv publish`) |
| Rust | cargo-dist: `dist init` / `generate` / `plan` | `github-attestations = true`; `github-action-commits` SHA pins |

A profile with several languages gets one pipeline per package and tags namespaced per package (`pkg-v1.2.0`).

## 4. Install only what is missing

Live-version check first ([version-protocol](../../core/_shared/version-protocol.md)); then:

```bash
mise use goreleaser                    # Go
mise use aqua:axodotdev/cargo-dist     # Rust; provides the `dist` binary
uvx twine --version                    # Python metadata check; no install
mise use actionlint zizmor             # workflow linting
```

## 5. Generate the files

Copy from [release-patterns.md](release-patterns.md); do not retype:

1. `CHANGELOG.md` — Keep a Changelog format, `## [Unreleased]` on top.
2. `scripts/release-notes.sh` — prints the tag's section, exits 1 when it is empty.
3. The language's workflow/config — `release.yml`, `.goreleaser.yaml`, the `pyproject.toml` publishing fields or `dist-workspace.toml` (the per-language sections). After changing `dist-workspace.toml`, re-run `dist generate`; never hand-edit the generated workflow.
4. README — the install table plus the "Verify a download" table.

## 6. Wire it

Registry and repository side, once per repo:

- npm: trusted-publisher entry (owner, repository, workflow `release.yml`, environment `npm`); `repository` with the exact GitHub URL, `files`, `engines`, `bin` in `package.json`.
- PyPI: pending publisher before the first release (same fields, environment `pypi`); it does not reserve the name.
- Homebrew tap: repository `homebrew-<name>`; fine-grained PAT (`contents: write` on the tap repo only) as `TAP_GITHUB_TOKEN` (Go) or `HOMEBREW_TAP_TOKEN` (Rust).
- GitHub environments (`npm`, `pypi`) on the publish jobs; required reviewers when more than one person can tag.
- Tag protection rule for `v*`: maintainers only.
- Workflows: `permissions: {}` at the top level, per-job permissions, `persist-credentials: false`, `cache: false`, actions pinned to full SHAs ([security-baseline](../../core/_shared/security-baseline.md)).

## 7. Verify

```bash
goreleaser check && goreleaser release --snapshot --clean --skip=sign,sbom,publish   # archives + checksums built, nothing uploaded
dist plan                                                                            # targets, installers, tap formula listed
npm pack --dry-run                                                                   # tarball holds dist/, bin, README
uv build --no-sources && uvx twine check dist/*                                      # both files PASSED
actionlint && zizmor --offline .github/workflows                                     # no findings; cargo-dist's generated file: the known ones in release-patterns.md
scripts/release-notes.sh v<current>                                                  # prints the section, exit 0
```

`v<current>` is the version the changelog entry was written for (`package.json`, `uv version --short`, `Cargo.toml`; Go has no version file). The first real tag is `v0.1.0-rc.1`, never `v1.0.0`: it proves every credential and permission on a non-`latest` channel, and a mistake can be deleted and re-tagged.

## References

- [release-patterns.md](release-patterns.md): SemVer over the CLI surface, changelog and tag rules, the full per-language pipelines, signing, README tables.
- [../_shared/stack-versions.md](../_shared/stack-versions.md): verified versions.
- [../build-cli/cli-ux.md](../build-cli/cli-ux.md): the CLI contract a version number promises.
- [../set-up-dev-toolchain/SKILL.md](../set-up-dev-toolchain/SKILL.md): actionlint/zizmor hooks.
- [../../core/_shared/security-baseline.md](../../core/_shared/security-baseline.md), [../../core/_shared/version-protocol.md](../../core/_shared/version-protocol.md): least permissions, SHA pins, live version checks.

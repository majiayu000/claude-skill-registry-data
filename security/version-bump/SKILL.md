---
name: version-bump
description: Bump the OpenAlgo Desktop version and prepare a release. Use when asked to release, cut, tag or bump the desktop to a new version (1.0.1, 1.1.0), to check that the version is consistent across Cargo.toml, tauri.conf.json, package.json and the lockfiles, or to write the CHANGELOG.md section for a release. Pushing the v* tag that starts the release build is the maintainer's decision, never an agent's.
---

# Version bump (desktop)

One version, written in several files that must agree. Versions follow
Semantic Versioning (`CHANGELOG.md` says so): a fix is a patch, a feature a
minor, a break of the web-compatibility contract never happens.

## Where the version lives

| File | Field | Read by |
| --- | --- | --- |
| `src-tauri/Cargo.toml` | `[package] version` | `env!("CARGO_PKG_VERSION")`: `GET /auth/app-info` (the footer), the MCP server info (`mcp/http.rs`, `mcp/stdio.rs`, the `get_openalgo_version` tool in `mcp/tools.rs`), `services/system_info.rs`, the broker HTTP user agent, the start-up log line |
| `src-tauri/Cargo.lock` | the `openalgo-desktop` package entry | `--locked` builds; regenerate, never hand-edit |
| `src-tauri/tauri.conf.json` | `version` | installer file names and bundle metadata (`release.yml` via `tauri-action`) |
| `package.json` | `version` | npm metadata |
| `package-lock.json` | `version` and `packages[""].version` | `npm ci`; regenerate, never hand-edit |
| `CHANGELOG.md` | the newest `## x.y.z` section | the release notes |

`/api/v1/ping` does not report a version (web parity); do not add one.
`src/components/layout/Footer.test.tsx` mocks a version string for its own
test and needs no edit.

Check them at any time (read-only; exits 1 on any disagreement):

```bash
python3 .claude/skills/version-bump/check_versions.py
python3 .claude/skills/version-bump/check_versions.py --expect 1.0.1 --tag v1.0.1
```

## Bumping

1. Edit the three hand-written fields to the new version:
   `src-tauri/Cargo.toml`, `src-tauri/tauri.conf.json`, `package.json`.
2. Regenerate the lockfiles:
   ```bash
   (cd src-tauri && cargo update -p openalgo-desktop --offline)   # rewrites only our entry
   npm install --package-lock-only --ignore-scripts
   ```
   Then `git diff --stat`: only those two lines should change in each lockfile.
   A lockfile diff that moves other packages is a dependency change and
   belongs in its own commit after a `security-audit` scanner pass.
3. `python3 .claude/skills/version-bump/check_versions.py --expect <new>`
   must print `OK`.
4. Build once so `Cargo.lock` is proven consistent:
   `(cd src-tauri && cargo check --locked)` with the shared
   `CARGO_TARGET_DIR` (see the `parallel-work` skill).

## CHANGELOG.md

Add a `## <new version>` section at the top, above the previous one, in the
style of `## 1.0.0`: a short paragraph on what the release is, then grouped
sections (`### Compatibility with OpenAlgo web`, `### Brokers`, fixes,
security, known limitations) written for a trader, not a developer. Source
material:

```bash
git log --oneline v<previous>..HEAD --no-merges        # what changed
git log --format='%an' v<previous>..HEAD | sort | uniq -c | sort -rn    # who
```

Until the first tag exists (`git tag` lists none today), use the commit that
added the previous `## x.y.z` section (`git log -S '## 1.0.0' --oneline -- CHANGELOG.md`)
in place of `v<previous>`.

Name every web PR that was ported (`marketcalls/openalgo#1234`). No icons or
emojis; "sandbox mode" or "analyzer mode", never "paper trading". If
`docs/` carries user guides affected by the release, update them in the same
change.

## Commit

```
chore(release): 1.0.1
```

Version files, both lockfiles and `CHANGELOG.md` in one commit, with the
session's attribution lines. Push it to master through the normal merge path
with the full gates (`parallel-work` skill).

## The tag is the maintainer's decision

`.github/workflows/release.yml` runs on any pushed `v*` tag: it builds every
platform (Windows NSIS, macOS Apple Silicon and Intel `.dmg`, Linux x64 and
arm64 AppImage and `.deb`), signs when the secrets are configured, and
attaches the installers and `SHA256SUMS.txt` to a **draft** GitHub release
that the maintainer reviews and publishes by hand. It does not re-run the
tests; its first job, `verify`, refuses to build unless the tag points at a
commit on master whose `ci-ok` check succeeded and `check_versions.py --tag`
passes (this script, run in CI). Run that gate alone before tagging for
real: Actions > Release > Run workflow, with the tag name. The release notes
say per platform whether the installer was found signed; they are generated
from a check of each installer, not from the presence of secrets. Branch and
tag protection the maintainer should enable: `docs/release/branch-protection.md`.

An agent never creates or pushes a `v*` tag, and never publishes a release,
even when asked to "release": prepare the bump commit, run
`check_versions.py --tag v<new>` to show it is ready, and hand over the
exact commands for the maintainer:

```bash
git tag -a v1.0.1 -m "OpenAlgo Desktop 1.0.1" <sha>
git push origin v1.0.1
```

---
name: eos-release
description: Cut a clean, verified tier-scoped distribution into dist/ — tier validation, personal-data + branding scans, full test suite, packaging, version bump, and git tag, reusing package-release.py / check-personal.py / check-branding.py. Use when the user says "release", "cut a release", "package <tier>", or "ship <tier>". NOT for routine commits (this is a coordinated gate), and distinct from eos-release-public, which promotes the working tree to the public repo + demo VPS.
---

# EmptyOS Release

Cut a clean, verified release for a given tier — orchestrate tier validation, safety scans, full test suite, distribution packaging, version bump, and git tag. Uses the existing tooling (`scripts/package-release.py`, `check-personal.py`, `check-branding.py`) rather than reinventing it.

The goal: when this skill finishes, `dist/` contains a tier-scoped distribution that compiles, boots, passes tests, and has no personal data or third-party branding leaks — and the state of that release is pinned in git.

## When to Use

- User says "release", "cut a release", "package `<tier>`", "ship `<tier>`"
- Preparing a distribution for another machine or a community download
- After adding a batch of apps/plugins that belong in a tier (`release.toml` was updated)

**Not** for routine commits — this is a coordinated gate, not a per-change workflow.

## Process

Run phases in order. Any phase fail → **stop, report, wait for user fix.** Do not skip ahead on partial success.

---

### Phase 1: Gather the Release Spec

Ask once:

```
Tier            : core | standard | <custom-tier>
Version bump    : patch | minor | major | none (default: patch)
Target          : local dist/ only, or tag + push to remote?
Vault connected?: yes/no (skill falls back to codebase-only checks if no)
```

Show the user what will happen:

```
Planned release:
  Tier      : <tier>
  Version   : <current> → <next>    (release.toml [release].version)
  Safety    : check-personal + check-branding (must pass clean)
  Tests     : pytest tests/ --ignore=tests/personal -v (must pass)
  Package   : python scripts/package-release.py <tier>
  Git       : commit release.toml bump + tag v<next> (<push if target=remote>)

Proceed? (y/n)
```

---

### Phase 2: Pre-flight — Working Tree Clean

```bash
git status --short
git rev-parse --abbrev-ref HEAD
```

Hard blockers — stop if any of these hold:

| Condition | Resolution |
|---|---|
| Uncommitted changes in tracked files | Ask user to commit or stash first — releases must be reproducible from HEAD |
| Untracked files that look load-bearing (new app/plugin not yet committed) | Ask user whether to include them — never auto-add |
| Current branch is not `main` (or release branch) | Ask user to confirm — sometimes intentional, usually a mistake |
| Local is behind remote (`git status` says "behind") | Ask user to pull first |

Soft-OK: untracked files that are gitignored (e.g. `emptyos.toml`, `dist/`, `data/`) — those are expected.

---

### Phase 3: Tier Validation (Dry Run)

```bash
python scripts/package-release.py <tier> --check
```

`package-release.py --check` resolves the tier (walking `extends` chains) and verifies every listed app/plugin/skill exists on disk. Typical failures:

| Error | Fix |
|---|---|
| `unknown tier 'X'` | Tier not defined in `release.toml [tiers.X]` |
| `apps/<id>: missing manifest.toml` | App id in `release.toml` but directory doesn't exist / was retired |
| Missing plugin | Plugin id in tier list but `plugins/<id>/` gone |

Also check the inverse — **apps on disk that no tier ships**:

```bash
for d in apps/*/; do
    id=$(basename "$d")
    grep -q "\"$id\"" release.toml || echo "NOT IN ANY TIER: $id"
done
```

Report each. For each, ask the user: add to `standard`, or keep it as a personal/unreleased app. Don't auto-add — tier membership is a curation decision.

Fix any issues → re-run `--check` until clean before continuing.

---

### Phase 4: Safety Scans

```bash
python scripts/check-personal.py
python scripts/check-branding.py
```

- **check-personal**: no personal paths, names, coordinates, API keys in tracked files (rules in `.eos-personal`). Personal config belongs in `emptyos.toml` (gitignored) and is read via `self.app_config(...)`.
- **check-branding**: no third-party brands (Obsidian / Suno / Kindle / etc.) in user-facing text. Plugin internals that wrap a specific service are the documented exception.

Both must report **CLEAN**. If either reports violations:

1. Show the user each violation (file, line, pattern)
2. Fix them — replace personal paths with `self.vault_config("...")` or `self.app_config(...)`, replace brands with generic terms ("markdown vault", "source URL", "Open external")
3. Re-run both scanners
4. Do **not** proceed until clean — this is the single most important release gate, because leaks are permanent once shipped

---

### Phase 5: Test Suite (Tier-Scoped)

Don't run tests the release won't ship. Scope the pytest selection to the **union of apps across the tiers being packaged** + shared cross-cutting tests. Prevents overnight hangs on tests for apps that aren't in the release.

#### 5a. Resolve tier → app set

Walk the `extends` chain for each tier being cut. Example: packaging `core + standard + demo` → union = `standard` (since both demo and core are subsets of standard's ancestor chain, and standard has the most apps).

```bash
# Quick way: ask package-release.py to print each tier's resolved app list
python scripts/package-release.py <tier> --check 2>&1 | grep -E "^(Apps|Plugins|Skills):"
```

If packaging a single tier, scope is just that tier's apps. If packaging multiple, scope is the union.

#### 5b. Build the test selection

For each app in the tier scope, include `tests/test_sys_<app>.py`. Also **always** include these cross-cutting tests (infra, SDK, journeys touch every release):

- `tests/test_sdk_*.py` — SDK contract tests
- `tests/test_components.py` — shared UI primitives
- `tests/test_keyboard.py` — keyboard shortcuts
- `tests/test_journeys.py` — cross-app event chains
- `tests/test_edge_cases.py` — boundary conditions
- `tests/test_unit_provider_fallback.py` — capability fallback chain
- `tests/test_sys_home.py`, `tests/test_sys_hub.py`, `tests/test_sys_pwa.py` — platform surfaces

**Exclude** unless you have a specific reason:
- `tests/test_sys_<app>.py` for apps not in the tier (e.g. if `personal/` apps have stray system tests, they'd double-count via `tests/personal/`)
- `tests/test_dogfood*.py` — month-in-the-life suites run in CI dogfood workflow, not per-release (slow + narrative, earn their keep elsewhere)
- `tests/test_visual.py`, `tests/test_accessibility.py` — include for standard tier releases, skip for hotfix/demo-only if time-boxed
- Anything marked `@pytest.mark.slow` — specifically `test_sys_release.py::test_check_safety` invokes pytest recursively. Running it during a release run causes an infinite loop. Always pass `-m "not slow"` during release.

#### 5c. Run

```bash
# Daemon must be running — start if it isn't
curl -sf http://localhost:9000/api/apps > /dev/null || echo "DAEMON DOWN"

# Build space-separated test path list from 5b, then:
python -m pytest <path1> <path2> ... -m "not slow" --timeout=60 --reruns 2 -v > test-run.log 2>&1
```

Requires `pytest-timeout` + `pytest-rerunfailures` (one-time: `pip install pytest-timeout pytest-rerunfailures`).

`--timeout=60` kills any single test that hangs so the whole suite can't stall overnight. `--reruns 2` retries UI flakes that fail under heavy daemon load (600+ tests hitting the same daemon creates transient Playwright timeouts on specific UI tests; isolated retries pass cleanly — a retry is sufficient to separate flakes from real failures). Redirect to a log file (no tail pipe) so output is visible mid-run.

Pass criteria:
- Every selected test passes or is explicitly skipped (with a reason)
- No collection errors, no import errors
- No `Failed: Timeout` from pytest-timeout (a hang is a failure — fix the test or mark it `@pytest.mark.timeout(N)` with a larger, deliberate cap)
- Zero JS errors during interactive tests (the Playwright suite enforces this)

If tests fail: stop, show failures, wait for user fix. **Do not release on red tests, even if the failure "looks unrelated"** — that's how bad releases ship.

**Never pipe pytest through `tail`, `head`, or `less`** during a release run — pipes buffer until the upstream closes, so you cannot see progress and cannot tell a hang from slow tests. Always redirect to a log file (`> test-run.log 2>&1`) and `grep` / `tail -n` the file when you want a summary.

---

### Phase 6: Version Bump

Edit `release.toml` `[release].version` per the Phase 1 spec:

- `patch`: `0.1.0` → `0.1.1`
- `minor`: `0.1.0` → `0.2.0`
- `major`: `0.1.0` → `1.0.0`
- `none`: skip this phase (used for re-cuts of the same version)

Show the diff, confirm before saving. One-line change.

---

### Phase 7: Package

```bash
python scripts/package-release.py <tier>
```

This copies the resolved tier's apps + plugins + skills into `dist/emptyos-<tier>-v<version>/` (exact output layout is defined by the script — don't re-implement; trust it).

After packaging:

```bash
# Confirm dist/ populated
ls -la dist/emptyos-<tier>-v<version>/ | head -20

# Smoke test: does the packaged version boot?
python scripts/check_snapshot_boot.py dist/emptyos-<tier>-v<version>/
```

It must print `OK: daemon healthy in Ns (N apps)` with the expected app count for
the tier, and exit 0. If it crashes on import, some shared dep isn't packaged —
file an issue against `package-release.py`, don't paper over it here.

**Use the script, not `cd dist/… && python -m emptyos health`** (what this step
used to say). Two reasons, and the second is why the old form was actively
misleading:

- A bare `python -m emptyos health` boots a kernel and opens a syslog SQLite
  handle in the process — the thing `.claude/rules/daemon-handling.md` tells
  sessions not to do. `check_snapshot_boot.py` is the sanctioned carve-out: it
  owns the child it spawns, binds an **ephemeral** port (never 9000-9009), puts
  `data_dir` and vault in a scratch temp dir, and terminates in a `finally`.
- It proves more. `health` answers from whatever the process could import;
  the script fails if the daemon never answers **or** answers with apps in an
  error state — the case where a snapshot boots but half its apps didn't load.
  It also compiles every module first, catching a bad `eos_apps.<id>` relative
  import that a running daemon would only surface on first request.

---

### Phase 8: Git Tag & Optional Push

```bash
# Stage release.toml bump + any Phase 3 fixes
git add release.toml <any files fixed in Phase 3/4>
git commit -m "Release: v<next> (<tier> tier)"

# Tag
git tag "v<next>"
```

If target is `remote` **and the user has explicitly approved pushing** (ask again before push — this is the last irreversible step):

```bash
git push origin main
git push origin "v<next>"
```

Never `--force` push on a release tag. Never push to a non-main branch as a release without explicit user confirmation. If push fails (e.g. non-fast-forward), stop and surface the error — do not resolve by force.

---

### Phase 9: Report

```
Release Cut: v<next> (<tier> tier)

Validation:
  Tier resolve       : <N> apps, <M> plugins, <K> skills
  Untiered apps      : 0  (or listed, deferred)
  check-personal     : CLEAN
  check-branding     : CLEAN
  Test suite         : <P> passed, <S> skipped, 0 failed

Package:
  dist/emptyos-<tier>-v<next>/   (<size> MB)
  Smoke boot          : <N> apps loaded, health OK

Git:
  Commit              : <sha> "Release: v<next> (<tier> tier)"
  Tag                 : v<next>
  Pushed              : yes/no

Next:
  - /eos-session-wrapup to record the release in the devlog
  - Distribute: dist/emptyos-<tier>-v<next>/ is ready to copy/zip
```

## Safety

- **Clean working tree is non-negotiable.** Releases must be reproducible from HEAD.
- **Safety scans are the single most important gate.** Personal data and third-party brands are permanent leaks once shipped; they override every other consideration.
- **Never release on red tests**, even for "unrelated" failures.
- **Never `--force` push.** Never push a release tag before the user explicitly approves the push step (separate confirmation from Phase 1's high-level "proceed").
- **Never edit `package-release.py` mid-release** to make it pass — if it's broken, stop, fix in a separate commit, then resume the release.
- **Never bump the version on a failed release.** If Phase 7 or 8 fails, roll back the version bump; don't ship v0.2.0 as v0.2.1 after fixing.
- **Untiered apps don't get auto-added.** Tier curation is a deliberate choice — surface the list, let the user decide.
- **Don't mix releases and feature work in one commit.** The release commit should contain only the `release.toml` bump (and any tiny Phase 3/4 fixes that *had* to ride along).

## Relationship

- Before a release, do a pass → `/eos-simplify` on recent commits catches convention slips that would otherwise ride along
- Before a release, periodic health → `/eos-architecture-review` check mode finds structural drift (dead connections, dormant capabilities)
- New app/plugin joining a tier → was scaffolded with `/eos-new-app` or `/eos-new-plugin` which wires the tier entry
- After a release → `/eos-session-wrapup` logs it and refreshes CLAUDE.md counts

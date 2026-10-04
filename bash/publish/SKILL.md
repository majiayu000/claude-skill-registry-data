---
name: publish
description: Bump version, build, test, publish to npm, and install locally
arguments: "<patch|minor|major> <-rc> <--check|-ch>"
---

# /publish - Version Bump, Build, Test & Publish

Automated release pipeline for moflo. Bumps version, commits, builds, tests, runs doctor, publishes to npm, and installs the new version locally.

**Arguments:** $ARGUMENTS

## Usage

```
/publish              # patch bump, default mode (skips CI-covered gates)
/publish minor        # minor bump (4.8.56 → 4.9.0)
/publish major        # major bump (4.8.56 → 5.0.0)
/publish -rc          # patch RC bump (4.8.56 → 4.8.57-rc.1)
/publish minor -rc    # minor RC bump (4.8.56 → 4.9.0-rc.1)
/publish --check      # full pre-flight (lint + test + smoke + everything)
/publish -ch          # short form of --check
/publish minor -ch    # combine: full pre-flight on a minor bump
```

## --check / -ch flag (presence-only)

**Default (flag absent):** runs build + doctor + trigger-based manual checks only. Skips local lint/test/smoke because lint+test are covered by `ci.yml` on every PR + push to main, and **cross-platform smoke is dispatched as part of this skill** (Step 8.5 below) — the `release-smoke.yml` workflow runs the full 3-OS matrix on the exact commit about to be published.

**With `--check` or `-ch` (any presence):** runs the full pre-flight from `pre-publish-rules.md` — lint, build, test, doctor (strict), local clean smoke, local populated smoke, and a forced full walk of every manual gate. Use this for publishes that didn't go through a green PR, risky releases, or when you want belt-and-suspenders on the local box in addition to the CI matrix.

The flag is presence-only. `--check` and `-ch` both set it to true. There is no `--check=true` / `--check=false` syntax — absence means false.

---

## Step-by-Step Procedure

### Step 0: Parse Arguments

- Default bump type is `patch` if not specified
- `-rc` flag: produce a release candidate
- `--check` or `-ch` (presence): set `CHECK_MODE=true`. Otherwise `CHECK_MODE=false`.
- Determine the new version string:
  - **Without `-rc`:** Use `npm version <patch|minor|major> --no-git-tag-version`
  - **With `-rc`:** Calculate manually:
    - If current version is already an RC of the same bump level (e.g., `4.8.57-rc.3`), increment the RC number (→ `4.8.57-rc.4`)
    - Otherwise, bump the base version and append `-rc.1` (e.g., `4.8.56` → `4.8.57-rc.1`)
    - Write with: `npm version <new-version> --no-git-tag-version`

### Step 1: Compute Manual-Check Fingerprint (always)

```bash
bash .claude/skills/publish/fingerprint.sh
```

The script diffs `HEAD` against the most recent `chore: install moflo@*` commit and pattern-matches the file list against the manual-gate triggers from `pre-publish-rules.md`. Output is one block:

```
Triggered manual checks: bin-scriptfiles-sync info-loss-audit
Diff range: <last-publish-sha>..HEAD
Changed files: 7
```

`Triggered manual checks: none` means gates 1/2/6 don't apply to this diff — skip them entirely.

This step costs ~50 tokens and is the cornerstone of token-efficient default mode.

### Step 2: Build (always)

```bash
npm run build
```

Always runs regardless of `CHECK_MODE`. Syncs the version to `src/cli/version.ts` via the `version` lifecycle script, then compiles all TypeScript. Confirms the deliverables on disk are correct.

**Must exit 0.** If it fails, stop and fix the build error.

### Step 3: Lint (only if `CHECK_MODE=true`)

```bash
npm run lint
```

Skipped by default — `ci.yml` runs lint on every PR with `max-warnings 0`. Run when `--check` is set.

### Step 4: Tests (only if `CHECK_MODE=true`)

```bash
npm test
```

Skipped by default — `ci.yml` runs the full test suite on every PR. Run when `--check` is set.

**Must have 0 test file failures.** If any test files fail, retest them individually to distinguish real failures from flaky ones (per broken window theory). Fix all real failures before proceeding.

### Step 5: Doctor (always — strict, no repair)

```bash
npx moflo doctor --strict
```

Doctor is the only check with no CI equivalent — it inspects local state (daemon lock, embeddings hygiene, sandbox tier, vector-stats freshness) that CI cannot validate for you. Always runs in `--strict` mode regardless of `CHECK_MODE`.

**Never `--fix` on the publish path.** A release pipeline must fail fast on broken local state, not silently repair it; a doctor that auto-repairs masks the very signal we want — "something is off, stop and investigate before shipping." If `doctor --strict` fails, stop and run `flo healer --fix` (or `npx moflo doctor --fix`) interactively, verify the repair, then retry the publish.

### Step 6: Local Smoke Tests (only if `CHECK_MODE=true`)

```bash
npm run test:smoke
npm run test:smoke:populated
```

Skipped by default. Local smoke covers the same harness as CI's Ubuntu leg, so it adds little signal over `release-smoke.yml`'s Ubuntu matrix entry (Step 8.5). Run only when `--check` is set — useful if you want belt-and-suspenders on the local box before dispatching the full CI matrix.

### Step 7: Manual Gate Walk (trigger-based, even in default mode)

Read the fingerprint output from Step 1.

| Trigger | Manual check (gate) | What to walk |
|---------|---------------------|--------------|
| `split-newlines` | Gate 7 | Diff the changed file-reading code; verify any newline split uses `/\r?\n/` not `'\n'` |
| `homedir-tmpdir` | Gate 7 | Verify env-var literals use `os.homedir()` / `os.tmpdir()`, not raw `process.env.HOME` / `/tmp` |
| `bwrap-permissions` | Gate 7 | Spell bash steps that need network declare `permissionLevel: elevated` |
| `posix-only-spell-bash` | Gate 7 | Spell bash steps avoid `mkdir`/`rm`/`cp`; use `node -e` with `fs`/`os` for cross-platform file ops |
| `bin-scriptfiles-sync` | Gate 8 | New `bin/` script appears in all three `scriptFiles` arrays (`session-start-launcher.mjs`, `init/moflo-init.ts`, third sync site) |
| `helper-static-files` | Gate 8 | New helpers ship as static `bin/` files, not generated at runtime |
| `shipped-guidance-prefix` | Gate 8 | New shipped guidance has `moflo-` prefix and lives in `.claude/guidance/shipped/` |
| `files-glob-coverage` | Gate 9 | Run `npm pack --dry-run` and confirm new shipped files appear in the tarball listing |
| `info-loss-audit` | Gate 10 | For each deleted/renamed file, audit destinations bullet-by-bullet — every piece of removed content has a home |

If `CHECK_MODE=true`, walk **all** manual gates regardless of triggers (full audit). If `CHECK_MODE=false`, walk **only triggered** ones.

If the trigger set is `none` AND `CHECK_MODE=false`: skip Step 7 entirely.

### Step 8: Commit & Push

Commit the version bump files:

```bash
git add package.json package-lock.json src/cli/version.ts
git commit -m "chore: bump version to <new-version>"
git push origin main
```

Only commit version-related files. Do not stage unrelated changes.

### Step 8.5: Dispatch release-smoke and block until green

```bash
# Capture the SHA we just pushed — release-smoke runs against this exact commit.
PUBLISH_SHA=$(git rev-parse HEAD)

# Trigger the full 3-OS × 2-harness matrix. `sha` is a required workflow input
# so the dispatched run is unambiguously bound to this commit.
gh workflow run release-smoke.yml --ref main -f sha="$PUBLISH_SHA"

# Find the dispatched run, block until it finishes, then PROVE it green.
#
# `gh run watch --exit-status` is NOT the gate. It has been observed to exit 0
# while most of the matrix was still in progress (moflo@4.12.4-rc.7 publish:
# exit 0 with 7 of 9 jobs unfinished), which would publish against an unproven
# matrix. It is used here only to block cheaply — the verdict comes from an
# explicit status/conclusion read afterwards. Same rule
# `.claude/skills/fl/phases.md` Phase 5.3b already states for
# `gh pr checks --watch`: a green exit code is not proof.
#
# The run lookup retries instead of guessing a fixed delay, and matches on
# head_sha so a concurrent dispatch (a manual UI retry from another tab) can
# never be mistaken for ours — never `--limit 1` alone.
node -e '
const { execFileSync } = require("node:child_process");
const sha = process.argv[1];
const gh = (args) => execFileSync("gh", args, { encoding: "utf8" }).trim();
// Synchronous by design: this script does nothing but wait, and a blocking
// sleep keeps the control flow linear. Do not "fix" it into setTimeout.
const sleep = (ms) => Atomics.wait(new Int32Array(new SharedArrayBuffer(4)), 0, 0, ms);
const deadline = Date.now() + 60 * 60 * 1000;
const WATCH_TIMEOUT_MS = 10 * 60 * 1000;

let runId = "";
while (!runId && Date.now() < deadline) {
  const rows = JSON.parse(gh(["run", "list", "--workflow=release-smoke.yml", "--branch", "main",
                              "--json", "databaseId,headSha"]));
  const hit = rows.find((r) => r.headSha === sha);
  if (hit) { runId = String(hit.databaseId); break; }
  sleep(5000);
}
if (!runId) {
  console.error("ERROR: no release-smoke run found for SHA " + sha +
    ". Check https://github.com/eric-cielo/moflo/actions/workflows/release-smoke.yml");
  process.exit(1);
}
console.log("release-smoke run " + runId + " bound to " + sha);

for (;;) {
  // Blocks while the run is live; may also return early and prematurely green.
  // Capped so a stalled watch cannot outlive the deadline below — on timeout we
  // simply fall through to the authoritative status read and watch again.
  try {
    execFileSync("gh", ["run", "watch", runId, "--exit-status"],
                 { stdio: "inherit", timeout: WATCH_TIMEOUT_MS });
  } catch (err) {
    // Expected when the run failed (watch exits non-zero) or when the cap above
    // fired. Surfaced rather than swallowed so a real fault — gh missing, auth
    // expired, rate limit — is visible instead of looking like a slow run.
    console.error("gh run watch: " + ((err && err.message) || err));
  }
  const state = JSON.parse(gh(["run", "view", runId, "--json", "status,conclusion"]));
  if (state.status === "completed") {
    if (state.conclusion !== "success") {
      console.error("ERROR: release-smoke concluded " + state.conclusion +
        " — inspect: gh run view " + runId + " --log-failed");
      process.exit(1);
    }
    break;
  }
  if (Date.now() > deadline) {
    console.error("ERROR: release-smoke still " + state.status + " after 60m — run " + runId);
    process.exit(1);
  }
  sleep(15000);
}

// Every leg, not just the rollup — a skipped or cancelled job is not a pass.
const jobs = JSON.parse(gh(["run", "view", runId, "--json", "jobs"])).jobs;
const bad = jobs.filter((j) => j.conclusion !== "success");
if (bad.length > 0) {
  console.error("ERROR: " + bad.length + " job(s) not success: " +
    bad.map((j) => j.name + "=" + (j.conclusion || "incomplete")).join(", "));
  process.exit(1);
}
console.log("release-smoke GREEN — " + jobs.length + " jobs, run " + runId);
' "$PUBLISH_SHA"
```

`release-smoke.yml` runs full consumer + populated smoke on Ubuntu/macOS/Windows, plus file-sync smoke on all three filesystems. Per-PR CI is intentionally Ubuntu-only to keep recurring cost manageable — the full cross-platform matrix is paid once here, at publish time, against the exact commit we're about to publish.

**Wall time expectations**: typical run is ~15-20 min once caches are warm. **The first dispatch after `release-smoke.yml` lands will have cold caches on every leg** (no prior runs of this workflow exist to populate the `consumer-warm` and `fastembed` caches per-OS). Expect ~25-35 min on that first dispatch — the macOS leg is the long pole. Subsequent dispatches reuse the cache and settle to the typical ~15 min.

**Never publish on `gh run watch`'s exit code alone.** The block above treats it as a cheap way to block, not as the verdict — it can return 0 with the matrix still running. The gate is the explicit `status == "completed"` + `conclusion == "success"` read, plus a per-job sweep so a cancelled or skipped leg cannot pass as green.

**If the block above exits non-zero**: stop immediately. It prints the run id and, on a real failure, the conclusion. Inspect the failed leg with `gh run view <run-id> --log-failed`, fix the underlying issue, push the fix, then re-run this step (no need to rerun Steps 0–8 — the bump commit is already on main, and the SHA-filtered lookup will pick up the new dispatched run against the same SHA only after `cancel-in-progress: false` lets the previous run drain). Do not proceed to `npm publish` until release-smoke is green for the SHA you intend to publish.

### Step 9: Verify npm Authentication

```bash
npm whoami
```

If 401 or "not logged in": auth token in `~/.npmrc` is missing or expired. Ask the user for a valid npm publish token.

**How to create a token** (provide these instructions to the user if needed):
1. Go to https://www.npmjs.com/settings/~/tokens
2. Click "Generate New Token" → select "Granular Access Token"
3. Set permissions: "Read and write" for the `moflo` package
4. Copy the token (starts with `npm_...`)

Once the user provides the token, write it to `~/.npmrc`:

```bash
echo "//registry.npmjs.org/:_authToken=<token>" > ~/.npmrc
```

Verify with `npm whoami` before proceeding.

### Step 10: Publish to npm

```bash
npm publish --tag <tag>
```

- For stable releases: `npm publish` (publishes to `latest` tag by default)
- For RC releases: `npm publish --tag rc` (publishes to `rc` tag so it doesn't become `latest`)

**OTP handling:**
- If npm returns an OTP/one-time-password error, ask the user for their authenticator code
- Then retry with: `npm publish --otp=<code> --tag <tag>`
- Tip: Granular access tokens created on npmjs.com do NOT require OTP — prefer those over legacy tokens

### Step 11: Verify Publication

```bash
npm view moflo version
npm view moflo dist-tags
```

Confirm the published version matches what we just built.

### Step 12: Install Locally

```bash
npm install moflo@<new-version> --save-dev
npm install --package-lock-only --force
npm ci --dry-run --legacy-peer-deps
```

The first command updates `package.json` and `package-lock.json` to use the newly published version as a devDependency.

The second command (`--package-lock-only --force`) backfills cross-platform optional-dependency entries that npm omits from the lockfile when `npm install` runs on a single host platform. Without it, transitive optional deps like the nested `@rolldown/binding-wasm32-wasi/node_modules/@emnapi/*` entries get dropped when publishing from Windows, and the resulting lockfile fails `npm ci` on Ubuntu/macOS CI legs. This produced the green-`release-smoke` → red-`ci.yml` divergence in run `26487580745` (moflo@4.10.27 install commit).

The final `npm ci --dry-run --legacy-peer-deps` proves the resulting lockfile is in sync with `package.json` before we commit it. If this exits non-zero, stop and investigate — do not commit a broken lockfile.

### Step 13: Final Commit

If `package.json` or `package-lock.json` changed from the install:

```bash
git add package.json package-lock.json
git commit -m "chore: install moflo@<new-version>"
git push origin main
```

The `chore: install moflo@<version>` commit message is the anchor the fingerprint uses to bound future diffs — keep the prefix exact.

## Output

Print a summary at the end:

```
Publish Summary
───────────────
Mode:            default | --check
Version:         <old> → <new>
Tag:             latest | rc
Build:           passed
Tests:           skipped (CI-covered) | <N> files passed, <N> tests passed
Lint:            skipped (CI-covered) | passed
Doctor:          <N> passed, <N> warnings
Smoke (local):   skipped (CI-covered) | passed
Release-smoke:   green (run <id>, 3-OS × 2-harness)
Triggered gates: <list> | none
Published:       moflo@<new-version>
Installed:       moflo@<new-version> (devDependency)
```

## Important

- All commands run from the project root — never cd into subdirectories
- Never use `--force` on npm publish
- Never install moflo globally — it is always a local devDependency
- If any step that DID run fails, stop and fix the issue before proceeding — do not skip steps
- The `prepublishOnly` script in package.json runs `npm run build` automatically, so npm publish will fail-fast on any TypeScript or asset-bundling error even if Step 2 had been skipped (it isn't — Step 2 always runs)
- Pre-publish rules live in `.claude/guidance/internal/pre-publish-rules.md` — never duplicate or paraphrase them in this skill; reference and follow

## When to use `--check`

Use `--check` / `-ch` when:

- The PR didn't go through CI (e.g., publishing from a local-only branch)
- You're publishing a risky change (broad refactor, infrastructure surface, packaging changes)
- CI was red on something orthogonal you waived, and you want belt-and-suspenders locally
- You explicitly want to re-walk gates 7/8/10 manually regardless of trigger output

For the common case — publishing right after a merged green PR — the default mode is correct and meaningfully cheaper in tokens and time.

## See Also

- `.claude/skills/publish/fingerprint.sh` — Trigger-fingerprint script invoked by Step 1
- `.claude/guidance/internal/pre-publish-rules.md` — Authoritative gate ruleset (gates 1–10) and trigger map
- `docs/BUILD.md` — Step-by-step build/publish process this skill mirrors
- `.claude/guidance/internal/dogfooding.md` — Why we catch consumer-facing regressions first as our own dependency
- `harness/consumer-smoke/README.md` — Smoke harness profiles (clean + populated) that prove a consumer install works
- `.github/workflows/ci.yml` — Lint/build/test gates this skill skips by default (ubuntu-only)
- `.github/workflows/consumer-install-smoke.yml` — Per-PR ubuntu-only smoke
- `.github/workflows/file-sync-smoke.yml` — Per-PR ubuntu-only file-sync smoke
- `.github/workflows/release-smoke.yml` — Full 3-OS × 2-harness matrix this skill dispatches at Step 8.5

---
name: dev-b4push
description: "Set up before-push validation (b4push) in a project: scripts/run-b4push.sh, the package.json entry, a project-level b4push skill, and optionally a mirroring GitHub Actions CI workflow. Use when the user says 'create b4push', 'set up b4push', 'before push checks', 'add CI', or a new project needs a local validation workflow."
user-invocable: true
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# dev-b4push

Deliverables: `scripts/run-b4push.sh`, a `b4push` package.json script, `.claude/skills/b4push/SKILL.md`, and (optional) `.github/workflows/ci.yml`.

## 1. Pick the steps

Read `package.json` (and `pnpm-workspace.yaml`, any `doc/` / `docs/` / `website/` sub-package, playwright/cypress config, `generate-*` scripts). Use the project's package manager. Include only what exists:

| Step | Typical command | Include when |
| --- | --- | --- |
| Workspace tests | `pnpm --filter "@scope/*" test` | workspace packages have tests |
| App unit tests | `pnpm --filter app-name test:unit` | app has unit tests |
| Code quality | `pnpm check` / `pnpm lint && pnpm format` | always |
| TypeScript | `pnpm typecheck` | TypeScript project |
| Build | `pnpm build` | build script exists |
| Doc quality / build | `cd doc && pnpm check` / `pnpm build` | doc site exists |
| E2E | start production server + playwright | e2e tests exist |

If the full run exceeds ~5 min (e2e), go dual-track: a quick script plus a full one.

## 2. `scripts/run-b4push.sh`

The script must **run every step even after a failure** (collect into `FAILURES`, report at the end, exit 1 if any) and isolate each step in a subshell.

```bash
#!/usr/bin/env bash
set -euo pipefail

START_TIME=$(date +%s)
FAILURES=()
ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

step() { echo ""; echo "━━━━━━━━━━━━━━━━━━━━━━━━"; echo "▶ $1"; echo "━━━━━━━━━━━━━━━━━━━━━━━━"; }
pass() { echo "✅ $1"; }
fail() { echo "❌ $1"; FAILURES+=("$1"); }

# Machine-wide queue for heavy steps, shared by every agent session on this machine
# (owner's ~/.claude or ~/.codex). Absent on CI and on teammates' machines → runs directly.
heavy() {
  local g="${HEAVY_GUARD:-}"
  [ -n "$g" ] || for c in "$HOME/.claude/scripts/heavy-guard.sh" "$HOME/.codex/scripts/heavy-guard.sh"; do
    [ -x "$c" ] && { g="$c"; break; }
  done
  if [ -n "$g" ] && [ -z "${CI:-}" ]; then "$g" -- "$@"; else "$@"; fi
}

step "Step 1/N: Code quality"
if (cd "$ROOT_DIR" && pnpm check); then pass "Code quality"; else fail "Code quality"; fi

# ...more steps, same shape. Heavy ones (build + full test, e2e, cargo --workspace) go through heavy():
step "Step N/N: E2E"
if (cd "$ROOT_DIR" && heavy pnpm test:e2e); then pass "E2E"; else fail "E2E"; fi

DURATION=$(( $(date +%s) - START_TIME ))
echo ""; echo "SUMMARY (${DURATION}s)"
if [ ${#FAILURES[@]} -eq 0 ]; then
  echo "✅ All checks passed! Safe to push."
else
  echo "❌ ${#FAILURES[@]} check(s) failed:"
  for f in "${FAILURES[@]}"; do echo "   - $f"; done
  exit 1
fi
```

**Wrap heavy steps in `heavy`, leave light ones bare.** Several agent sessions running b4push at once starve the machine of memory and turn suites red for non-code reasons; `heavy-guard.sh` queues them machine-wide and gates on available memory. Putting the call in the script — not in a skill's prose — means every caller is serialized without having to remember a rule, and the fail-open lookup keeps the repo usable for anyone without the guard. Do NOT wrap the whole script from outside or wrap lint / type-check / unit steps: a queued lint is wasted wall-clock. Never tune the suite itself (timeouts, workers) to fit one machine.

`chmod +x scripts/run-b4push.sh`, then add `"b4push": "./scripts/run-b4push.sh"` to package.json scripts.

## 3. Project skill `.claude/skills/b4push/SKILL.md`

Uppercase `SKILL.md` is required — lowercase `skill.md` causes git dual-tracking / clone collisions on case-insensitive filesystems.

```markdown
---
name: b4push
description: >-
  Run comprehensive pre-push validation covering [steps]. Use when: (1) Completing a PR
  or feature implementation, (2) Before pushing significant changes, (3) After large refactors,
  (4) User says 'b4push', 'before push', 'check everything', or 'ready to push'.
user-invocable: true
allowed-tools:
  - Bash
---

# Before Push Check

Run `pnpm b4push` from the project root (`scripts/run-b4push.sh`):

1. [step list]

Takes ~[duration]. All steps must pass.

## On failure

Identify the failed step, auto-fix what you can (`pnpm check:fix`, `pnpm lint:fix`, same under `doc/`), re-run `pnpm b4push`, report the final status.

Heavy steps print a `heavy-guard: verdict=...` line. Exit 75 = queued too long, the step never ran. `ENV_SUSPECT` = failed while the machine was starved: rerun once; still red with no assertion / type / lint error in the output → defer that step to CI under a `deferred-verification` issue and report it as deferred, not passed. `FAIL` = real, fix it.
```

## 4. CI workflow (optional, GitHub, no CI yet)

`.github/workflows/ci.yml` mirrors the b4push steps one-to-one, each as its own `run` step so failures are identifiable.

```yaml
name: CI
on:
  pull_request:
    types: [opened, synchronize, reopened]
    branches: [main]
  push:
    branches: [main]
concurrency:
  group: ci-${{ github.head_ref || github.ref }}
  cancel-in-progress: true
jobs:
  checks:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v4
        with:
          version: 10
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - run: pnpm install --frozen-lockfile
      # one step per b4push step
```

No `cache:` on setup-node — a fresh install from the npm CDN beats cache restore (see `/gh-actions-wisdom` rule 5).

## 5. Verify

Run `pnpm b4push` and fix whatever it surfaces.

## Reference setups

- **message (zudomessages)**: 4 steps (workspace tests, app tests, doc checks, doc build), ~1-2 min
- **mdx-formatter**: 6 steps (quality, build, test, doc data, doc quality, doc build), ~40s
- **zmod**: 9 steps including e2e against a production server, ~3-4 min
- **zpanels**: dual-track (quick ~3-5 min, full with e2e ~10-15 min)

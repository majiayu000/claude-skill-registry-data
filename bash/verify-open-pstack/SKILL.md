---
name: verify-open-pstack
description: Verify Open Pstack through installed Codex and Claude Code skills and its shipped Bun CLIs. Use for real behavior proof, routing or setup changes, orchestration bookkeeping, and release evidence.
---

# Verify Open Pstack

Read [the feature map](features/README.md) first. The primary product is the installed Pstack workflow in Codex and Claude Code. The secondary surfaces are the shipped CLI tools. A CLI proof establishes only that CLI's behavior, never installed skill discovery, parent decisions, or model execution.

This is repository maintenance tooling, outside `plugins/pstack`. Track work in GitHub Issues; this skill originated in [issue 26](https://github.com/arjitj2/open-pstack/issues/26). Read `UPSTREAM.md` before modifying upstream-derived content.

## Launch

Run from the Open Pstack checkout in one Bash session. There is no server, port, database seed, or build step. Bun installs the CLI dependencies; Python 3 checks observed JSON. Installation may access the package registry. Each CLI invocation exits on its own.

```bash
set -euo pipefail
VERIFY_REPO=$(git rev-parse --show-toplevel)
VERIFY_TOOLS="$VERIFY_REPO/plugins/pstack/skills/poteto-mode/scripts"
VERIFY_EVIDENCE=$(mktemp -d "$HOME/open-pstack-verification.XXXXXX")
VERIFY_SCRATCH=$(mktemp -d "${TMPDIR:-/tmp}/open-pstack-verify.XXXXXX")
export VERIFY_REPO VERIFY_TOOLS VERIFY_EVIDENCE VERIFY_SCRATCH
cleanup() {
  if [ -d "$VERIFY_SCRATCH" ]; then
    cp -R "$VERIFY_SCRATCH" "$VERIFY_EVIDENCE/scratch-final"
    rm -rf -- "$VERIFY_SCRATCH"
  fi
}
trap cleanup EXIT
capture() {
  local label=$1 rc=0
  shift
  printf '%q ' "$@" > "$VERIFY_EVIDENCE/$label.command"
  printf '\n' >> "$VERIFY_EVIDENCE/$label.command"
  "$@" > "$VERIFY_EVIDENCE/$label.stdout" 2> "$VERIFY_EVIDENCE/$label.stderr" || rc=$?
  printf '%s\n' "$rc" > "$VERIFY_EVIDENCE/$label.exit"
  cat "$VERIFY_EVIDENCE/$label.stdout"
  cat "$VERIFY_EVIDENCE/$label.stderr" >&2
  return "$rc"
}
printf '%s\n' "$VERIFY_EVIDENCE"
capture revision git rev-parse HEAD
capture initial-status git status --short
capture plugin-before git ls-files -s plugins/pstack
capture install bun install --frozen-lockfile --cwd "$VERIFY_TOOLS"
```

Readiness means install exits zero and Doctor passes. For parent-app checks, use the installation feature's separate launch instructions. Real providers require their existing authenticated subscriptions and the saved model sheet's spending policy. Do not print credentials, invent access, or run provider probes just to verify a local CLI.

## Doctor

This single read-only command checks the checkout identity, matching manifest versions, installed CLI dependency, runtime, and actual CLI entry point. Run it after Launch and again if anything looks wrong. It checks CLI readiness, not parent authentication.

```bash
capture doctor bun -e '
const root = process.env.VERIFY_REPO;
const tools = process.env.VERIFY_TOOLS;
const a = await Bun.file(`${root}/plugins/pstack/.claude-plugin/plugin.json`).json();
const b = await Bun.file(`${root}/plugins/pstack/.codex-plugin/plugin.json`).json();
if (a.name !== "pstack" || b.name !== "pstack" || a.version !== b.version) throw Error("manifest mismatch");
if (!await Bun.file(`${tools}/node_modules/commander/package.json`).exists()) throw Error("run Launch first");
const p = Bun.spawnSync([process.execPath, `${tools}/orch/orch.ts`, "--help"]);
if (p.exitCode !== 0 || !p.stdout.toString().includes("Plain-file orchestrate bookkeeping")) throw Error("CLI unavailable");
console.log(JSON.stringify({root, version:a.version, bun:Bun.version, surface:"checkout CLI"}));'
```

## Drive

Choose the changed feature, then execute its recipe with the variables and `capture` function above. Start with [orchestration](features/orchestration.md) for a self-contained live CLI smoke. Use fresh scratch and evidence directories for every attempt; never use the user's default orchestrate store. Separate CLI stores can run concurrently, but dependency installation should finish before any CLI drive begins.

Parent installations, authentication, and model sheets are shared state unless a dedicated test profile is provided. Do not double-drive a parent session or change a personal model sheet for a fixture. When no isolated authenticated parent is available, record that entry point as blocked; continue independent CLI coverage.

## Evidence

`$VERIFY_EVIDENCE` is a persistent directory under the user's home, separate from disposable scratch. Every command produces `.command`, `.stdout`, `.stderr`, and `.exit` files. Use unique capture labels. Preserve fixture bytes, before/after model sheets without secrets, runner receipts, native host events, and parent transcripts or screenshots as applicable.

Record feature ID, entry point, checkout commit and dirty diff, installed version and candidate-tree identity for parent runs, action, expected result, observed result, and skips in `result.md` in that directory. Capture the action and resulting state. Confirm writes through a second CLI read and stored files; final agent prose alone is not proof. Never fabricate provider failures or count synthetic policy inputs as a real fallback execution. Mocks belong only at an existing production boundary and must be labeled. Do not assume a dry-run is offline or side-effect-free: observe files, git refs, and network activity for the behavior being claimed.

Before release, install the exact candidate and exercise changed behavior in **every affected parent**. Unit tests, source checks, CLI policy decisions, and model self-reports cannot replace this gate. Follow `.github/pull_request_template.md`; missing applicable live evidence means draft. For maintenance-only changes, prove `plugins/pstack` unchanged and exercise the actual changed maintenance path instead.

## Cleanup

Run even after a failed drive. The EXIT trap covers failures in the Bash session; explicitly run the following on success. The copied scratch state survives for inspection. Keep the evidence directory.

```bash
capture plugin-after git ls-files -s plugins/pstack
capture plugin-index-equality diff -u "$VERIFY_EVIDENCE/plugin-before.stdout" "$VERIFY_EVIDENCE/plugin-after.stdout"
capture plugin-working-tree git diff --exit-code HEAD -- plugins/pstack
capture plugin-untracked git ls-files --others --exclude-standard -- plugins/pstack
test ! -s "$VERIFY_EVIDENCE/plugin-untracked.stdout"
cleanup
test ! -e "$VERIFY_SCRATCH"
test -s "$VERIFY_EVIDENCE/doctor.stdout"
printf 'Scratch removed; evidence retained at %s\n' "$VERIFY_EVIDENCE"
trap - EXIT
```

Tree-equality checks above apply to maintenance-only work and should fail if packaged files changed. For intentional plugin changes, retain the diff and use installed-candidate proof instead. Close only parent sessions created for this run and remove only their dedicated test profiles. Never kill by process name or delete shared plugin caches. Foreground CLI checks here leave no background process.

## Helpers

No helper executable is shipped. Launch defines the shell functions used throughout. The product executables are `bun "$VERIFY_TOOLS/orch/orch.ts"`, `"$VERIFY_TOOLS/model-policy/pstack-model-policy"`, and `"$VERIFY_TOOLS/runner/pstack-runner"`; use the feature recipes for arguments.

Keep this map current with `pstack:maintain-verification-skill` (`/pstack:maintain-verification-skill` in Claude Code).

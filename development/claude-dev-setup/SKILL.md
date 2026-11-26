---
name: claude-dev-setup
description: Installs the base Claude Code hooks in a new project - idempotent and reversible settings wiring (never overwrites someone else's config without --force) + chain-preserving git hook (never replaces an existing pre-commit hook).
---

> **Auto-Trigger:** When the user asks to set up Claude Code in a new project, install the base hooks, or "prepare this repo for Claude Code".
> **Keywords:** "setup claude code", "install hooks", "configure new project", "wire settings", "pre-commit hook", "claude dev kit"
> **Priority:** MEDIUM
> **Tools:** Bash, Read

## When NOT to Activate
- The project already has `.claude/settings.json` wired the way the user wants - only run `wire_settings.py` with `--force` if you REALLY want to overwrite, never by default.
- You need specific autonomy/verification/loop guardrails - that is the full `operator-kit`, not this lean module.

## Contract

**INPUT:** target `settings.json`/`settings.local.json` (for `wire_settings.py`) + a target `.git/hooks/<name>` (for `install_git_hook.py`).

**OUTPUT:** wired settings (idempotent) + chained git hook (chain-preserving).

**EXIT CODES:**

| Exit | Meaning |
|---|---|
| 0 | wired/chained successfully, or already was (no-op) |
| 1 | conflict without `--force` (settings) - nothing overwritten |
| 3 | error (target missing, payload missing) |

**STATE IT TOUCHES:**

| Resource | Reads/Writes | Purpose |
|---|---|---|
| target `settings.json`/`settings.local.json` | Reads+Writes (with `.bak-<timestamp>` backup) | additive wiring |
| `.git/hooks/<name>` | Reads+Writes | chain-preserving (keeps the original as `.pre-kitforge`) |

## Process
1. **Wire the base hooks** (secret-scan on Edit/Write) into a test settings file first:
   ```bash
   python scripts/wire_settings.py --target /path/settings-copy.json --spec hooks/wiring-spec.yaml
   ```
2. **Confirm idempotency** by running again - it must return `no-op`, byte-identical.
3. **Install the git hook** WITHOUT fear of losing the hook that already exists:
   ```bash
   python scripts/install_git_hook.py --repo . --hook-name pre-commit --payload hooks/my-payload.sh
   ```
4. **If you need to undo** the settings wiring:
   ```bash
   python scripts/wire_settings.py --undo --target /path/settings-copy.json
   ```

## Executed examples

```console
$ python scripts/install_git_hook.py --repo /tmp/test-project --hook-name pre-commit --payload payload.sh
{"status": "chained", "hook": ".../pre-commit", "preserved_original": ".../pre-commit.pre-kitforge", "payload": ".../pre-commit.kitforge-payload"}
```
<!-- executed: 2026-09-22 · exit=0 -->
(an ALREADY existing pre-commit hook is preserved as `.pre-kitforge`, not overwritten.)

```console
$ python scripts/wire_settings.py --target conflict-settings.json --spec statusline-only-spec.yaml
{
  "status": "warn",
  "changed": [],
  "warnings": [
    "statusLine already taken by another config; use --force to overwrite (current: 'another-owner-configured-this')"
  ]
}
```
<!-- executed: 2026-10-30 · exit=1 -->
(conflict WITHOUT `--force` - nothing is overwritten; this is the fix for the known defect in `wire_statusline.py:47-49`, which overwrote silently.)

```console
$ sh .git/hooks/pre-commit log.txt && cat log.txt
original-pre-commit-ran
claude-dev-kit-payload-ran
```
<!-- executed: 2026-10-30 · exit=0 -->
(the original runs FIRST - if it fails, `set -e` aborts BEFORE the new payload runs.)

```console
$ bash evals/hook-chain-test.sh
[OK] original hook + new payload, both ran, original FIRST (chain-preserving proven)
```
<!-- executed: 2026-09-22 · exit=0 -->

## Proof

```bash
python scripts/install_git_hook.py --self-test
```

---
name: init
description: 'First-run wizard — preflight this host, detect the OpenClaw instances on it, write the operator-owned fleet config Arguments: [--detect-only] [--force].'
---

# Fleet init

Turn "there are OpenClaw instances on this box" into a fleet config every other command can trust.
Read-only through step 4; step 5 writes exactly one file. Parse `[--detect-only] [--force]` from
"$ARGUMENTS"; load `fleet-model` first — it owns the config ladder, the fields and the plan rule.

## 1. Preflight
```bash
uname -s -m
docker version --format 'server {{.Server.Version}}' 2>&1 | tail -1
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/fleet.py" config --show 2>&1 | head -3
git rev-parse --is-inside-work-tree 2>/dev/null || echo "not a git work tree"
```
Four gates, each fatal alone: unsupported OS or architecture, no `docker` binary, a daemon that does not
answer, no permission on the socket. Report the failing one and stop. **Never write the config inside a
git work tree** — that is how instance names, ports and host paths get committed; there `--out` must be
`~/.config/openclaw-ops/fleet.json` (per user) or `/etc/openclaw-ops/fleet.json` (host-wide, root).

## 2. Detect
```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/fleet.py" config --init --detect-only --json
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/fleet.py" discover --table
```
Add `--prefix <p>` when the compose projects do not start with `openclaw-`. Show the table, name what
came back `alien` or `legacy`, and stop here if `--detect-only` was passed.

## 3. Nothing usable found — diagnose, never retry
Answer as **what I saw → the hypothesis → exactly one action for the operator**, one action per message.
The four cases — wrong machine · different prefix · everything `alien` · a foreign `host_fingerprint` —
and the single next action for each are in `fleet-model` → `references/fleet-config.md`.

## 4. Ask — only what detection cannot answer
One `AskUserQuestion`, recommended option first: the **reference** instance, which instances stay
**unmanaged** (`alien` and `legacy` default to `manage:false`), the **canary** (least critical, never the
reference), and policy — update channel, soak days, stale-log hours. Every answer has a flag in step 5.

## 5. Write — R2, so the plan is short but complete
- **BACKUP** — `cp -p <existing-config> <existing-config>.pre-init`, only when a config already exists.
- **ROLLBACK** — `mv <existing-config>.pre-init <existing-config>`; with no prior file, `rm -f <out-path>`.
- **APPLY**
```bash
(umask 077; python3 "${CLAUDE_PLUGIN_ROOT}/scripts/fleet.py" config --init \
   --reference <name> --canary <name> \
   --update-channel <stable|extended-stable|beta|dev> --soak-days <n> --stale-log-hours <h> \
   [--host-label <text>] [--out <path>] [--force])
```
Mode 0600, names and ids only, never a secret value. Omit a policy flag to keep its default.

## 6. Verify, then hand over
```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/fleet.py" config --validate
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/fleet.py" config --diff
```
`role`, `criticality`, `aliases` and the secret ids are guesses — say so, then point at `/openclaw-ops:status`.
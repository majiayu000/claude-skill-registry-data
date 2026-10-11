---
name: update
description: 'Upgrade instances on a pinned, soaked target — baseline, verified backup, plan, apply, post-checks, schedule dedup Arguments: <selector> [--to <version>] [--channel stable|extended-stable|beta|dev] [--yes].'
---

# OpenClaw update

Parse `<selector>`, `[--to <version>]`, `[--channel …]`, `[--yes]` from "$ARGUMENTS".

**R4 every time** — the state schema migrates in place. `instance-upgrade` owns the reasoning (channel
resolution, pin rule, backup layers, post-check ladder, the two traps, recovery, wave gate); load it, and
`docs-research` before quoting upstream.

## Phase 0 — preconditions

Credentials repaired first (`/openclaw-ops:auth`), zombies triaged, legacy layout refused. Then resolve
the targets as a mutation — an empty selector and `all` exit 3, and that refusal is the point:
```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/fleet.py" resolve "<selector>" --mutation --table
```

## Phase 1 — target and pin

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/versions.py" "<selector>" [--channel <c>] [--target <v>] --table
```
`<c>` is a channel **name** (`stable`, `extended-stable`, `beta`, `dev` — what `policy.update_channel`
accepts), never the dist-tag it resolves through; the hop and why it matters: `instance-upgrade`.

Exit 3 = target not accepted (soak, correction release, older than installed, pre-release, wrong
release line for the channel) — the gate working. **`bridge-required`** is the same exit with its own
reason: an installation older than the cut-off upstream states cannot go straight to the current line,
and the verdict names the bridge release and the instances that need it (`gate.bridge`). Plan that hop
first as its own update — backup, pin the bridge, `doctor --fix` there and confirm what it imported — then
gate the real target again; `instance-upgrade` has the rules of the hop. Exit 5 = drift. Pin the
**digest** (`gate.pin`); a moving tag is refused, so no pin, no upgrade.

## Phases 2–3 — baseline, then backup in three layers

Baseline per instance, before the change: lint, schedules, plugins, config, credential state; only
**new** findings block afterwards. Then the backup — config snapshot outside the `.bak` ring
(`gate.snapshot`) · the runtime's own backup, `backup create --verify`, verification **passed** ·
gateway stopped, **then** the state archived together with the `.bak` copies Doctor saved. No verified
backup → rejected, not warned (red line `upgrade-without-verified-backup`). Every one of these carries
working credentials in plaintext: owner-only, never a shared path.

## Phase 4 — plan, then apply on a later turn

Eight blocks — **TARGET · PRECHECK · CHANGE · BACKUP · IMPACT · VALIDATE · ROLLBACK · APPLY** — plus
**IRREVERSIBLE · CONFIRM**, worded from `instance-upgrade` (there is no rollback, there is recovery).
ROLLBACK is executable and names the pinned previous artefact:
`docker compose -p <project> stop <service> && tar -xzf <state-archive> -C <state-dir> && docker compose -p <project> up -d`.
`--yes`, the typed phrase (`gate.confirm_phrase`) and the plan id (`gate.py plan mint update <instance>`,
passed as `--plan-id`; it is checked against the registry and burned on use) come a later
turn; retry budget zero (`gate.RETRY_RULES: openclaw-update`) — a stopped gateway goes to the restore path.

## Phase 5 — post-checks, and the two traps

Run the post-check ladder from `instance-upgrade` (digest vs pin · `doctor` then restart — already done
by the image entrypoint for an image upgrade · `health --json` with queues · readiness **with the
bearer** · `doctor --post-upgrade`, exit 1 only for an error-level finding, warnings read from the
document · lint vs baseline at `--severity-min info`, where exit 2 is a failed run), then its two traps:
`fleet.cron.duplicates-after-upgrade`, `fleet.model.primary-overwritten`.

## Batches

Good → changed, so **fail-fast** (`gate.batch_policy`); `gate.canary_barrier` runs the canary alone and
stops, a revenue-bearing instance gets its own window, and the wave gate is four observations, not a timer.
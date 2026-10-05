---
name: selfhosted-gateway-seamless-upgrade
description: Use when upgrading the local StaticFlow backend behind the already-running Pingora gateway on 39180 with blue/green backend slots, especially in the current tmux-supervised production setup where the gateway must stay up and config changes are applied by SIGHUP.
---

# Selfhosted Gateway Seamless Upgrade

Use this skill for the current StaticFlow production shape:

- stable gateway: `127.0.0.1:39180`
- backend slots: `blue -> 39080`, `green -> 39081`
- gateway config: `conf/pingora/staticflow-gateway.yaml`
- process supervision: usually `tmux`, not systemd

## Non-Negotiable Rules

- Do not stop, kill, restart, or recreate the gateway process during backend
  rollout.
- Do not touch the gateway to fix tmux session names, process ancestry, or
  operational neatness.
- Do not inspect or use gateway lifecycle helper scripts as the rollout plan.
  In tmux production they are a distraction; the rollout path is the manual
  sequence in this skill.
- The only allowed gateway signal during cutover is:
  `kill -HUP <gateway-pid>`.
- If an action would interrupt `39180`, stop and ask the user.
- Direct checks on `39080` or `39081` only prove the candidate slot works.
  Cutover is proven only through `39180` and, when public production matters,
  `https://ackingliu.top`.
- Keep the old slot alive unless repeated stable-path checks prove the new slot
  is serving real traffic.

Forbidden during normal hot update:

- `tmux kill-session -t sf-gateway`
- `kill <gateway-pid>` without `-HUP`
- `systemctl restart staticflow-gateway...`
- any gateway stop/start cycle
- switching traffic because a candidate slot alone is healthy

## Required Preflight

Before building or starting anything, identify the live topology with read-only
commands:

```bash
curl -fsS http://127.0.0.1:39180/api/healthz
env -u https_proxy -u HTTPS_PROXY -u http_proxy -u HTTP_PROXY -u all_proxy -u ALL_PROXY \
  curl -fsS https://ackingliu.top/api/healthz
ss -ltnp | grep -E ':(39180|39080|39081)\b'
tmux ls
tmux list-panes -a -F '#{session_name}:#{window_index}.#{pane_index} pid=#{pane_pid} cmd=#{pane_current_command}'
awk '/active_upstream:/ {print $2; exit}' conf/pingora/staticflow-gateway.yaml
```

Confirm:

- local `39180` health and public health report the same active backend port
- the reported active port matches `active_upstream` in the config
- the other slot port is free before starting the candidate
- the gateway pid is the listener on `39180`

If public health does not go through `39180` to the same active slot, this skill
does not apply. Stop and ask.

## Build Rule

Only run one Rust build/check at a time. When a live backend is running, cap
Cargo parallelism:

```bash
CARGO_BUILD_JOBS=1 cargo build --profile release-backend -p static-flow-backend --jobs 1
```

Start the candidate from:

```text
target/release-backend/static-flow-backend
```

Do not overwrite `bin/static-flow-backend` before cutover.

## Candidate Slot

Choose the inactive slot:

- if active is `green`, candidate is `blue` on `39080`
- if active is `blue`, candidate is `green` on `39081`

Start the candidate in tmux with the freshly built binary. Use the existing
session naming convention if one is already present; common names are
`sf-backend-blue` and `sf-backend-green`.

Example for blue:

```bash
tmux new-session -d -s sf-backend-blue \
  'cd /home/ts_user/rust_pro/static_flow && BACKEND_BIN=/home/ts_user/rust_pro/static_flow/target/release-backend/static-flow-backend DB_ROOT=/mnt/wsl/data4tb/static-flow-data PORT=39080 STATICFLOW_LOG_SERVICE=backend-blue-39080 ./scripts/start_backend_selfhosted.sh --port 39080'
```

Example for green:

```bash
tmux new-session -d -s sf-backend-green \
  'cd /home/ts_user/rust_pro/static_flow && BACKEND_BIN=/home/ts_user/rust_pro/static_flow/target/release-backend/static-flow-backend DB_ROOT=/mnt/wsl/data4tb/static-flow-data PORT=39081 STATICFLOW_LOG_SERVICE=backend-green-39081 ./scripts/start_backend_selfhosted.sh --port 39081'
```

Candidate checks before cutover:

```bash
curl -fsS http://127.0.0.1:<candidate-port>/api/healthz
curl -fsS 'http://127.0.0.1:<candidate-port>/api/articles?limit=1'
curl -fsS 'http://127.0.0.1:<candidate-port>/api/llm-gateway/status'
```

For feature-specific changes, add the exact endpoint that proves the fix.

## Cutover

Cutover is config edit plus in-process reload.

1. Back up the config:

   ```bash
   cp conf/pingora/staticflow-gateway.yaml tmp/staticflow-gateway.$(date +%Y%m%d-%H%M%S).yaml.bak
   ```

2. Change only the `active_upstream` line to the candidate slot.

3. Re-read the config and confirm it now names the candidate:

   ```bash
   awk '/active_upstream:/ {print $2; exit}' conf/pingora/staticflow-gateway.yaml
   ```

4. Find the running gateway pid from the `39180` listener:

   ```bash
   ss -ltnp | grep ':39180 '
   ```

5. Reload the already-running gateway:

   ```bash
   kill -HUP <gateway-pid>
   ```

Do not replace step 5 with restart.

## Stable-Path Verification

After `SIGHUP`, verify through the stable path. Repeat until local and public
health pass at least 3 consecutive times and each response reports the candidate
port.

```bash
for i in 1 2 3; do
  curl -fsS http://127.0.0.1:39180/api/healthz
  curl -fsS 'http://127.0.0.1:39180/api/articles?limit=1'
  curl -fsS 'http://127.0.0.1:39180/api/llm-gateway/status'
  env -u https_proxy -u HTTPS_PROXY -u http_proxy -u HTTP_PROXY -u all_proxy -u ALL_PROXY \
    curl -fsS https://ackingliu.top/api/healthz
  sleep 1
done
```

Only after these stable-path checks pass should you say the rollout is live.
If they do not stay on the candidate port, keep the old slot alive and roll
back.

## Rollback

Rollback is restore config plus `SIGHUP`.

1. Restore the backed-up gateway config.
2. Confirm `active_upstream` names the old slot.
3. Send `kill -HUP <gateway-pid>` to the same running gateway process.
4. Verify `http://127.0.0.1:39180/api/healthz` reports the old slot port.

Do not restart the gateway to roll back.

## Cleanup

Cleanup is optional and happens after cutover proof, not during cutover.

- Stop only the old backend slot supervisor, never the gateway.
- Stop the old slot only after repeated stable-path checks prove traffic is on
  the new slot.
- If any check is ambiguous, leave the old slot running.
- After cleanup, confirm only the old backend port stopped listening.
- Then, if needed, sync the release artifact with a new inode:

  ```bash
  install -m 755 target/release-backend/static-flow-backend bin/static-flow-backend.new
  mv -f bin/static-flow-backend.new bin/static-flow-backend
  ```

## Common Distraction Traps

- A gateway process not being under the expected tmux session name is not a
  rollout problem. Do not restart it.
- A helper script exposing `restart`, `reload`, or `switch` subcommands is not
  permission to use them in tmux production.
- `ps` can show stale tmux server argv mentioning an old session. Treat `tmux
  ls`, `tmux list-panes`, and `ss -ltnp` as the runtime truth.
- A candidate slot being healthy does not authorize stopping the old slot.
- A single successful `39180` response is not enough for cleanup.

## Stop Conditions

Stop and ask the user if:

- gateway pid cannot be identified from the `39180` listener
- local and public health disagree about the active slot
- the inactive slot is not actually free
- the candidate does not pass direct health and feature checks
- `SIGHUP` does not move `39180` to the candidate slot
- stable-path verification is not repeatedly successful
- any proposed action would stop, restart, or recreate the gateway process

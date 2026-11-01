---
name: evm-wallet-docker-e2e
description: Run the evm-wallet Docker e2e tests (build, start stack, wait for healthy, test, diagnose failures).
---

Run all commands from the repo root unless noted.

## 1. Verify Docker is running

```bash
docker info 2>&1 | head -5
```

If it fails, tell the user Docker is not running and ask them to start Docker Desktop (or the daemon), then wait for confirmation before continuing.

## 2. Build the repo and Docker images

```bash
yarn workspace @ocap/evm-wallet-experiment docker:build 2>&1 | tail -30
```

This builds the full monorepo then builds the Docker images. It may take a few minutes. Report any errors from the tail output.

## 3. Tear down any existing stack, then start fresh

Always bring the stack down first to avoid stale container state (e.g. spent delegation budgets from a previous run leaking into the new run).

```bash
yarn workspace @ocap/evm-wallet-experiment docker:down 2>&1 | tail -10
```

Then start the stack:

```bash
yarn workspace @ocap/evm-wallet-experiment docker:ensure-logs && \
  yarn workspace @ocap/evm-wallet-experiment docker:compose up -d 2>&1 | tail -20
```

## 4. Wait for all services to be healthy

Poll every 10 seconds (up to 3 minutes / 18 attempts). All 8 services must reach `(healthy)` status before proceeding:

- `evm`, `bundler`
- `kernel-home-bundler-7702`, `kernel-away-bundler-7702`
- `kernel-home-bundler-hybrid`, `kernel-away-bundler-hybrid`
- `kernel-home-peer-relay`, `kernel-away-peer-relay`

```bash
i=0; while [ $i -lt 18 ]; do
  i=$((i+1))
  ps_out=$(yarn workspace @ocap/evm-wallet-experiment docker:ps 2>&1)
  healthy=$(echo "$ps_out" | grep -c "(healthy)" || true)
  echo "Attempt $i/18: $healthy/8 healthy"
  if [ "$healthy" -ge 8 ]; then echo "Stack ready."; break; fi
  if [ "$i" -eq 18 ]; then echo "Timed out:"; echo "$ps_out"; exit 1; fi
  sleep 10
done
```

If the loop exits with a timeout, show the last `docker:ps` output and stop — do not proceed to the tests.

## 5. Run the e2e tests

```bash
yarn workspace @ocap/evm-wallet-experiment test:e2e:docker 2>&1 | tail -80
```

The vitest reporter also writes structured results to `packages/evm-wallet-experiment/logs/test-results.json`.

## 6. Diagnose failures

If tests fail, investigate in this order:

### Structured test results

```bash
cat packages/evm-wallet-experiment/logs/test-results.json
```

Look at the `testResults` array for failed tests and their error messages.

### Service logs

Container logs are written to `packages/evm-wallet-experiment/logs/`. Check the service(s) relevant to the failing test mode first:

```bash
tail -150 packages/evm-wallet-experiment/logs/<service>.log
```

Service log files:

- `evm.log` — Anvil chain (check for on-chain errors)
- `kernel-home-bundler-7702.log`, `kernel-away-bundler-7702.log`
- `kernel-home-bundler-hybrid.log`, `kernel-away-bundler-hybrid.log`
- `kernel-home-peer-relay.log`, `kernel-away-peer-relay.log`

Start with the pair(s) involved in the failing test, then `evm.log` for on-chain issues.

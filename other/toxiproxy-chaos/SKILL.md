---
name: toxiproxy-chaos
description: "Configures Toxiproxy for TCP-level fault injection - runs as a sidecar / proxy between client and upstream, applies toxics (latency, bandwidth, slow_close, timeout, slicer, limit_data, reset_peer) via control API. Focused on the proxy itself rather than an API-level chaos runner, including non-test usage (chaos in dev environments, integration tests, pre-prod simulation). Use when the team needs TCP-precise fault injection in development / integration environments without K8s or commercial tooling."
---

# toxiproxy-chaos

## Overview

Toxiproxy is Shopify's "TCP proxy to simulate network and system
conditions for chaos and resiliency testing"
([toxiproxy-readme][tp]). It sits between client and upstream; you
configure toxics via its HTTP control API.

[tp]: https://github.com/Shopify/toxiproxy

This skill is the **infrastructure / dev-environment** angle. The
test-suite-driven angle is in `api-chaos-runner` (in the qa-api-testing plugin);
both rely on the same Toxiproxy primitive.

## When to use

- Local dev needs to simulate slow / failing network conditions
  for development / debugging.
- A pre-prod environment needs network chaos without K8s tooling.
- Integration tests need TCP-level fault injection that's
  framework-agnostic.
- A team wants OSS chaos without Litmus / Chaos Mesh / Gremlin.

For test-suite integration, see
`api-chaos-runner`.

## Step 1 - Install + run

```bash
# Pull the official image
docker pull ghcr.io/shopify/toxiproxy:latest

# Run as a daemon
docker run --rm -p 8474:8474 -p 5432:5432 ghcr.io/shopify/toxiproxy:latest

# Or natively (Linux):
brew install toxiproxy   # macOS
# Then: toxiproxy-server
```

Port 8474 is the control API; other ports are listeners for
proxied traffic.

## Step 2 - Define a proxy

Via the control API:

```bash
curl -d '{"name":"orders-db","listen":"0.0.0.0:5432","upstream":"orders-db-real:5432"}' \
  http://localhost:8474/proxies
```

Or via the CLI:

```bash
toxiproxy-cli create -l 0.0.0.0:5432 -u orders-db-real:5432 orders-db
toxiproxy-cli list
```

The application connects to `localhost:5432` (Toxiproxy listener);
Toxiproxy forwards to `orders-db-real:5432`.

## Step 3 - Toxic catalog

Per [toxiproxy-readme][tp], the canonical toxics:

| Toxic             | Effect                                                         |
|-------------------|----------------------------------------------------------------|
| `latency`         | Add latency to all data passing through                        |
| `down`            | Force the proxy down (no connections accepted)                 |
| `bandwidth`       | Cap bandwidth in kbps                                           |
| `slow_close`      | Delay TCP socket close                                          |
| `timeout`         | Stop forwarding traffic after a delay; let connection time out |
| `slicer`          | Slice TCP data into smaller bits                                |
| `limit_data`      | Cap total bytes through the proxy                               |
| `reset_peer`      | Reset connection on the next byte                               |

## Step 4 - Add toxics

```bash
# 500ms latency on every request through the orders-db proxy
toxiproxy-cli toxic add -t latency -a latency=500 orders-db

# Bandwidth cap at 50 KB/s
toxiproxy-cli toxic add -t bandwidth -a rate=50 orders-db

# Force the proxy down (kill the connection)
toxiproxy-cli toxic add -t timeout -a timeout=5000 orders-db

# Remove all toxics on this proxy
toxiproxy-cli toxic remove orders-db -n latency
```

Toxics can apply on **upstream** (data going from client → server)
or **downstream** (server → client) directions. Default: both.

## Step 5 - Direction-specific toxics

```bash
toxiproxy-cli toxic add -t latency -a latency=500 -n upstream-latency --downstream=false orders-db
toxiproxy-cli toxic add -t latency -a latency=200 -n downstream-latency --upstream=false orders-db
```

Useful when the client / server have asymmetric tolerances.

## Step 6 - Language SDKs

Per [toxiproxy-readme][tp], SDKs exist for Python, Node, Go, Ruby:

```python
# Python
from toxiproxy import Toxiproxy
client = Toxiproxy()
proxy = client.create('orders-db', '0.0.0.0:5432', 'orders-db-real:5432')
proxy.add_toxic(name='latency', type='latency', attributes={'latency': 500})
# ... run app ...
proxy.destroy()
```

```javascript
// Node
const Toxiproxy = require('toxiproxy-node-client');
const client = new Toxiproxy('http://localhost:8474');
const proxy = await client.createProxy({ name: 'orders-db', listen: '0.0.0.0:5432', upstream: 'orders-db-real:5432' });
await proxy.addToxic({ type: 'latency', attributes: { latency: 500 } });
```

The SDKs make integration into test fixtures (per
`playwright-fixture-builder`)
clean.

## Step 7 - docker-compose integration

```yaml
# docker-compose.test.yml
services:
  toxiproxy:
    image: ghcr.io/shopify/toxiproxy:latest
    ports:
      - 8474:8474        # control
      - 5432:5432        # proxied DB
      - 8080:8080        # proxied API

  app:
    environment:
      DB_HOST: toxiproxy
      DB_PORT: 5432
      EXTERNAL_API_URL: http://toxiproxy:8080
```

The app points at Toxiproxy; tests configure toxics via the
control API.

## Step 8 - Use cases

| Use case               | How                                                       |
|------------------------|-----------------------------------------------------------|
| Test resilience patterns | Inject latency / failure; verify retry / timeout / circuit-breaker |
| Reproduce a production incident | Replicate the network conditions; debug locally     |
| Pre-prod simulation     | Chaos in staging; verify the team's runbook              |
| Dev-time exploration    | "What if the DB is slow?" - engineer toggles a toxic     |
| Integration test fixtures | Per-test toxic add / remove via SDK (per Step 6)       |

## Anti-patterns

| Anti-pattern                                                          | Why it fails                                                              | Fix |
|-----------------------------------------------------------------------|---------------------------------------------------------------------------|-----|
| Toxiproxy in production                                                | Adds proxy latency + failure surface to real traffic.                    | Test / staging only. |
| Forgetting to remove toxics after test                                 | Subsequent tests inherit chaos; flaky.                                   | Cleanup in afterEach / context manager. |
| One global Toxiproxy for parallel tests                                | Tests fight over shared toxic state.                                     | One Toxiproxy per parallel worker. |
| Skipping direction (default = both)                                     | Asymmetric scenarios miss.                                                | Explicit `--upstream=false` / `--downstream=false` (Step 5). |
| Manual control-API curl in tests                                        | Verbose; error-prone.                                                     | Use language SDK (Step 6). |

## Limitations

- **TCP only.** UDP, QUIC, raw IP - out of scope.
- **Not for K8s pod chaos.** For pod-level / node-level chaos, use
  `chaos-mesh` or
  LitmusChaos (references/litmus.md in `chaos-experiment-author`).
- **Single-node deployment.** No clustering; for distributed chaos,
  use a chaos-platform tool.
- **Application must point at Toxiproxy.** Requires config change
  (DB_HOST, etc.); transparent proxying isn't built-in.

## References

- [tp][tp] - Toxiproxy README: TCP proxy, toxic types (latency,
  down, bandwidth, slow_close, timeout, slicer, limit_data,
  reset_peer), control API on port 8474, language SDKs.
- `api-chaos-runner` - sister skill: same Toxiproxy primitive, test-suite-driven
  matrix workflow.
- `failure-injection-test-author` - composes Toxiproxy + WireMock for richer failure scenarios.

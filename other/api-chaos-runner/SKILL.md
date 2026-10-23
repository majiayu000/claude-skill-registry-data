---
name: api-chaos-runner
description: "Runs the project's existing API tests under injected network chaos - latency, timeouts, dropped connections, bandwidth caps, packet loss - via Toxiproxy (notes on Pumba / Gremlin / LitmusChaos). Builds a per-scenario chaos matrix and reports which assertions break under which conditions, verifying resilience patterns (retry, circuit-breaker, timeout, fallback). Unlike schemathesis-fuzzing and restler-fuzzing, which generate new tests from a schema, this drives your EXISTING example-based suite."
---

# api-chaos-runner

## Overview

Most API tests run against perfect networks: <1ms latency, no
packet loss, infinite bandwidth, deterministic ordering. Real
production isn't like that. **Network chaos testing** drives the
existing tests under controlled network impairment - the team
discovers which retry / circuit-breaker / timeout patterns actually
hold up before real customers find out.

The canonical open-source primitive is **Toxiproxy** - Shopify's
"TCP proxy to simulate network and system conditions for chaos and
resiliency testing" ([toxiproxy-readme][toxiproxy]). The pattern:
sit Toxiproxy between client and upstream; manipulate **toxics**
(latency, timeout, bandwidth, etc.) during test execution.

[toxiproxy]: https://github.com/Shopify/toxiproxy

This skill is **build-an-X** - the workflow chains the team's
existing API tests (Postman / Karate / RestAssured / Tavern /
Schemathesis) through a Toxiproxy-managed connection and orchestrates
a per-scenario chaos matrix.

## When to use

- The API has documented resilience requirements (retry on 5xx,
  circuit-break on 3 consecutive failures, timeout at 5s, etc.) and
  the team needs to **verify** them, not just document them.
- A new external dependency just got added; the team wants to
  pressure-test fallback behavior.
- An incident postmortem identified a "we should have caught this in
  testing" item; chaos coverage is the prevention mechanism for that
  class.
- The team has integration tests already and wants to multiply their
  signal value via fault injection.

If the team is just starting API testing and has no resilience
patterns to verify, this skill is overkill - start with happy-path
coverage via `postman-collections`
or the language-native equivalents first.

## How to use

1. Confirm documented resilience requirements exist (retry,
   circuit-breaker, timeout, fallback). If none, start with happy-path
   coverage instead of chaos.
2. Pick the chaos primitive - Toxiproxy for per-API chaos in CI (Step 1).
3. Build the chaos matrix: for each existing test scenario, list the
   toxics to inject and the expected behavior per condition (Step 2).
4. Wire Toxiproxy between the app and its upstream and register a proxy
   per dependency ([references/toxiproxy-wiring.md](references/toxiproxy-wiring.md)).
5. Run the matrix, always including a no-toxic control row; capture one
   JUnit XML per scenario (Step 3).
6. Aggregate results into a resilience matrix and report which
   assertions break under which toxic (Step 4).
7. Inject only toxics that map to a documented expectation; run the full
   matrix nightly, the control row per PR.

## Step 1 - Pick the chaos primitive

| Tool                | Layer                       | Best for                                              |
|---------------------|-----------------------------|-------------------------------------------------------|
| **Toxiproxy**       | TCP proxy                   | Per-connection latency / bandwidth / timeout / drop. Most precise. |
| **Pumba**           | Docker container            | Container-level chaos (kill, pause, network).         |
| **Gremlin** (commercial) | Multi-platform           | Production-grade chaos with audit / approval flow.   |
| **LitmusChaos**     | Kubernetes operator         | Cloud-native; experiments declared as CRDs.           |
| **`tc qdisc`** (Linux native) | Network interface | Lowest level; most setup; CI-friendly only with `--cap-add NET_ADMIN`. |

Default recommendation: **Toxiproxy** for per-API chaos in CI. The
others fit when the team is already in those ecosystems
(Docker-Compose-heavy projects, Kubernetes-first projects).

## Step 2 - Define the chaos matrix

For each existing API test scenario, define a matrix of conditions
to run it under:

| Scenario              | Toxic            | Expected behavior                          |
|-----------------------|------------------|--------------------------------------------|
| Order create (POST /orders) | None (control) | 201 in <500ms                              |
| Order create          | latency=1000ms     | 201 in <2s (within timeout budget)         |
| Order create          | latency=10000ms    | 504 with retry-after, OR client gives up    |
| Order create          | bandwidth=10kbps   | 201 (eventual) OR 408 timeout               |
| Order create          | reset_peer         | 502 with retry attempted                    |
| Order create          | timeout            | 504; circuit-breaker opens after 3rd        |

Per [toxiproxy-readme][toxiproxy], the canonical toxic types include
**latency**, **down** (forced failure), **bandwidth**, **slow_close**,
**timeout**, **slicer**, **limit_data**, **reset_peer**.

The matrix is the load-bearing artifact: what the team **expects**
under each condition is what differentiates resilience verification
from "did the test pass?" The Expected column drives the assertions.

## Step 3 - Wire Toxiproxy and run the matrix

Sit Toxiproxy between the app and its upstream, register a proxy per
dependency, and add/remove toxics around each test run. Point the app
at Toxiproxy's listen ports; it forwards to the real upstream when no
toxic is active. A matrix runner loops the scenarios, adding one toxic
per row and producing one JUnit XML per scenario to aggregate in the
report stage.

Full docker-compose setup, control-API proxy registration,
`toxiproxy-cli` toxic commands, and the runner shell script:
[references/toxiproxy-wiring.md](references/toxiproxy-wiring.md).

## Step 4 - Report what broke under what

A successful chaos run produces a **resilience matrix** report:

```markdown
## API Chaos Matrix - verdict: REVIEW

| Scenario         | Control | Latency 1s | Bandwidth 10k | Timeout 5s | Reset peer |
|------------------|:-------:|:----------:|:-------------:|:----------:|:----------:|
| POST /orders     |    ✅   |     ✅     |       ✅      |     ✅     |     ❌     |
| GET /orders/:id  |    ✅   |     ✅     |       ❌      |     ✅     |     ✅     |
| DELETE /orders/:id |  ✅   |     ✅     |       ✅      |     ✅     |     ✅     |

### Failures

| Test | Toxic       | Expected                                          | Actual |
|------|-------------|---------------------------------------------------|--------|
| POST /orders | reset_peer | 502 + retry attempted; second attempt succeeds | 502; no retry observed in client logs |
| GET /orders/:id | bandwidth=10k | 200 in <30s | 408 timeout at 10s |
```

A green matrix isn't the goal - finding where resilience is **missing**
is the goal. A failure under a chaos scenario is a feature request,
not a bug in the test.

## Choosing what to inject

Match toxics to documented resilience requirements:

| Resilience pattern documented            | Toxic to inject                        |
|------------------------------------------|----------------------------------------|
| Retry on 5xx                              | `down` (forced 5xx) or `reset_peer`   |
| Timeout after Nms                         | `latency=N+500` (force the timeout)    |
| Circuit-breaker after 3 failures          | `down` for ≥3 requests                  |
| Fallback to cache when upstream unreachable | `down` indefinitely                  |
| Bulkhead under load                       | `bandwidth=very-low`                    |
| Slow-loris client                         | `slow_close` on response                |

Run only the toxics that map to a documented expectation; running
every toxic against every endpoint is noise.

## Worked example

The orders service documents "retry once on connection reset." The team
already has a Postman collection covering POST /orders.

1. Wire Toxiproxy in front of `orders-api-real` and register the
   `orders-api` proxy (Step 3).
2. Matrix rows: `control` (no toxic) and `reset_peer`. Expected for
   reset_peer: 502, retry attempted, second attempt succeeds.
3. Run the matrix. Control passes - 201 in <500ms.
4. Under `reset_peer` the run returns 502 with no retry in the client
   logs, so POST /orders reset_peer is marked failing in the matrix.

Verdict: REVIEW. The documented retry policy is not actually
implemented. The output is a fix request against the client (add the
retry), not a bug in the test - exactly the resilience gap the matrix
exists to surface.

## Anti-patterns

| Anti-pattern                                                 | Why it fails                                                     | Fix |
|--------------------------------------------------------------|------------------------------------------------------------------|-----|
| Chaos in production                                           | Real users observe; oncall pages.                                 | CI / staging only. Production chaos requires the team's full chaos engineering practice (Gremlin / Litmus + approval flow). |
| Per-PR chaos matrix                                            | Adds 10+ minutes; team disables.                                  | Nightly chaos runs; PR runs only the control row. |
| Asserting "chaos must not break anything"                     | Every system has a breaking point; the test trivially fails.    | Assert specific resilience behavior under specific conditions; document the breaking point as accepted. |
| Using `down` for everything                                    | `down` forces 5xx; doesn't model real-world latency / bandwidth. | Mix `latency`, `bandwidth`, `timeout`, `reset_peer` for realistic mixes. |
| Skipping the control row                                      | Without control, the matrix can't distinguish chaos failures from test bugs. | Always run a no-toxic scenario as the baseline. |

## Limitations

- **Toxiproxy is TCP-level.** UDP flaws (DNS resolver weirdness,
  QUIC) need different tooling.
- **Doesn't model partial failures within a single connection.**
  Toxiproxy treats each connection uniformly; for "retry on the 3rd
  request after 2 successes" patterns, layer a counting middleware.
- **Per-test-suite isolation.** When tests run in parallel against
  the same Toxiproxy instance, they fight over the same toxic
  state; serialize chaos scenarios or use one Toxiproxy instance per
  worker.

## References

- [toxiproxy][toxiproxy] - main repo: install, control API, toxic
  types, language-native clients.
- [references/toxiproxy-wiring.md](references/toxiproxy-wiring.md) -
  docker-compose setup, proxy registration, toxic commands, matrix runner.
- Pumba - https://github.com/alexei-led/pumba
- LitmusChaos - https://litmuschaos.io/
- Principles of Chaos Engineering - https://principlesofchaos.org/
- `postman-collections`,
  `tavern-testing`,
  `karate-testing`,
  `restassured-testing` - 
  example-based test suites that this skill drives through chaos.

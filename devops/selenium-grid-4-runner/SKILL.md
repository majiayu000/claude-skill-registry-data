---
name: selenium-grid-4-runner
description: "Author and operate Selenium Grid 4 - self-hosted distributed WebDriver. Covers the six-component architecture (Router / Distributor / Session Map / Event Bus / New Session Queue / Node), standalone vs hub-and-node modes, the Docker-image stack (selenium/standalone-chrome, selenium/hub, selenium/node-chrome), node registration, session-queue tuning, and observability. Use for self-hosted cross-browser testing when data residency or cost-control require an on-prem grid. This is the self-hosted execution RUNNER - for the zero-infra alternative use playwright-testing browser projects (bundled engines); for managed cloud grids use cloud-grid-e2e (BrowserStack / Sauce Labs / LambdaTest); to decide WHICH browsers and tiers to run use browser-matrix-strategy-reference."
---

# selenium-grid-4-runner

## Overview

Selenium Grid 4 is the self-hosted distributed WebDriver
infrastructure - the open-source alternative to cloud-grid SaaS
providers. Per
[selenium.dev/documentation/grid](https://www.selenium.dev/documentation/grid/).

Composes with
`browser-matrix-strategy-reference`
for matrix planning.

## When to use

- Data-residency requirements forbid cloud grids.
- Cost: high-volume testing where cloud per-session pricing
  exceeds self-hosting break-even.
- Internal-network apps where tunnel solutions
  (BrowserStackLocal / Sauce Connect) are insufficient.
- Custom browser builds / non-standard configurations cloud grids
  don't support.

For cloud-hosted alternatives see the sibling
`cloud-grid-e2e`.

## Authoring

### Six-component architecture

| Component | Role |
|---|---|
| **Router** | Entry point; routes WebDriver requests to the right session |
| **Distributor** | Allocates new sessions to available Nodes based on capabilities |
| **Session Map** | Tracks active sessions (session ID → Node URL) |
| **Event Bus** | Internal messaging between components |
| **New Session Queue** | Holds pending session requests when no Node available |
| **Node** | Runs actual browser instances; registers with the Distributor |

### Standalone mode (development / small teams)

All components in one JVM:

```bash
# Download from selenium.dev/downloads
java -jar selenium-server-<version>.jar standalone
```

Default port 4444. WebDriver clients connect to
`http://localhost:4444/wd/hub`.

Standalone mode is suitable for a single developer's machine or a
small CI runner with co-located browsers.

### Hub-and-node mode (production)

Hub on one machine, Nodes on others:

```bash
# Hub
java -jar selenium-server-<version>.jar hub

# Node (on another machine)
java -jar selenium-server-<version>.jar node \
  --hub http://hub-host:4444 \
  --port 5555
```

For very large deployments each of the six components can run as its own
process; see
[references/distributed-and-ci.md](references/distributed-and-ci.md). Most teams
run hub-and-node.

### Docker stack

Docker images are published as `selenium/*` on Docker Hub. Pin one Grid version
across every image via a single `SE_VERSION` variable (examples use `4.21.0`);
keep it identical on the Hub and all Nodes.

```yaml
# docker-compose.yml   (set SE_VERSION=4.21.0 in .env or the environment)
services:
  selenium-hub:
    image: selenium/hub:${SE_VERSION}
    ports: ["4442:4442", "4443:4443", "4444:4444"]

  chrome:
    image: selenium/node-chrome:${SE_VERSION}
    shm_size: 2gb
    depends_on: [selenium-hub]
    environment:
      - SE_EVENT_BUS_HOST=selenium-hub
      - SE_EVENT_BUS_PUBLISH_PORT=4442
      - SE_EVENT_BUS_SUBSCRIBE_PORT=4443
      - SE_NODE_MAX_SESSIONS=2

  firefox:
    image: selenium/node-firefox:${SE_VERSION}
    shm_size: 2gb
    depends_on: [selenium-hub]
    environment:
      - SE_EVENT_BUS_HOST=selenium-hub
      - SE_EVENT_BUS_PUBLISH_PORT=4442
      - SE_EVENT_BUS_SUBSCRIBE_PORT=4443

  edge:
    image: selenium/node-edge:${SE_VERSION}
    shm_size: 2gb
    depends_on: [selenium-hub]
    environment:
      - SE_EVENT_BUS_HOST=selenium-hub
      - SE_EVENT_BUS_PUBLISH_PORT=4442
      - SE_EVENT_BUS_SUBSCRIBE_PORT=4443
```

`shm_size: 2gb` is required for Chrome (shared-memory bloat with
many tabs).

### Standalone Docker (simpler)

```bash
docker run -d -p 4444:4444 -p 7900:7900 --shm-size="2g" \
  selenium/standalone-chrome:${SE_VERSION}
```

Port 7900 exposes noVNC (browser at http://localhost:7900) for
live-session viewing.

## Running

### Connect a WebDriver client

```python
from selenium import webdriver

driver = webdriver.Remote(
    command_executor="http://grid-router:4444/wd/hub",
    options=webdriver.ChromeOptions(),
)
driver.get("https://example.com")
# ...
driver.quit()
```

For Kubernetes-deployed Grid use the cluster-internal DNS:
`http://selenium-router.test-ns.svc.cluster.local:4444/wd/hub`.

### Capabilities

Standard W3C - no grid-specific options needed:

```json
{
  "browserName": "chrome",
  "browserVersion": "stable",
  "platformName": "linux"
}
```

### Session-queue tuning

Key knobs:

| Setting | Effect |
|---|---|
| `--session-request-timeout` | How long a queued session waits before failing (default 300s) |
| `--session-retry-interval` | Polling interval for matching capabilities (default 5s) |
| `SE_NODE_MAX_SESSIONS` | Max concurrent sessions per Node (default 1) |
| `SE_NODE_SESSION_TIMEOUT` | Inactive session cleanup (default 300s) |

Tune `SE_NODE_MAX_SESSIONS` per Node's CPU + memory budget;
typical: 2 Chrome / 1 Firefox per 2-core / 4 GB Node.

### Observability

Grid 4 exposes:

- **GraphQL endpoint** at `/graphql` for session inspection
- **Status endpoint** at `/status` for ready-check
- **Prometheus metrics** at `/wd/hub/status` (Grid health, session
  counts)

For production add a Grafana dashboard polling Prometheus.

## Parsing results

Grid 4 doesn't add session videos / HAR by default - that's the
test client's responsibility (or via a sidecar like
selenoid + selenoid-ui for Grid 3-style recording).

Logs at `/var/log/seluser/` inside Docker containers, exportable
via volume mount.

## CI integration

Boot the grid, gate on `/status` ready before running tests, and always tear
down. Full GitHub Actions workflow:
[references/distributed-and-ci.md](references/distributed-and-ci.md).

## Anti-patterns

| Anti-pattern | Why it fails | Fix |
|---|---|---|
| `shm_size` default (64 MB) on Chrome node | Chrome crashes mid-session | Always `shm_size: "2g"` |
| `SE_NODE_MAX_SESSIONS` too high | OOM / CPU thrashing | Conservative: 2 per 2-core Node |
| Hub-and-node without health check | Failed nodes silently drop sessions | Wait for `/status` ready before tests start |
| Standalone in production | No HA; single point of failure | Hub-and-node minimum for prod |
| Manually allocating ports for Nodes | Conflicts | Let Docker assign + use service DNS |
| No session-queue timeout | Sessions wait forever; CI hangs | Set `--session-request-timeout` bounded |
| Mixing Selenium versions across Hub + Nodes | Capability negotiation breaks | Pin same Grid version across all components |

## Limitations

- **No real-device support out of box.** Mobile testing needs
  Appium server + emulators / real devices - significant
  additional infrastructure.
- **Browser-version matrix is self-managed.** Cloud grids ship
  3000+ combinations; self-hosted ≤ what your team builds.
- **HA + scaling is your problem.** Cloud grids handle it; on
  self-hosted you do.
- **macOS / iOS Safari requires actual macOS hosts.** Linux can
  run Chrome / Firefox / Edge but not Safari.

## References

- Selenium Grid 4 documentation - 
  [selenium.dev/documentation/grid](https://www.selenium.dev/documentation/grid/).
- Selenium Docker images - 
  [github.com/SeleniumHQ/docker-selenium](https://github.com/SeleniumHQ/docker-selenium).
- W3C WebDriver specification - 
  [w3.org/TR/webdriver2/](https://www.w3.org/TR/webdriver2/).
- Composes:
  `browser-matrix-strategy-reference`.
- Cloud-grid alternatives:
  `cloud-grid-e2e` (sibling skill).

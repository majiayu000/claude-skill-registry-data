---
name: reliability
description: "Add or remove resilience testing instrumentation — discovers endpoints at runtime and writes a config file for the daemon-hosted dashboard."
---

## User Input

You **MUST** consider the user input before proceeding (if not empty).
If the input contains the word **"remove"**, execute the **Remove Workflow**.
Otherwise, execute the **Attach Workflow**.

## Required MCP Capabilities

This command requires the following MCP tools. If any are unavailable,
stop and tell the user to update the Akka CLI and restart Claude Code.

- **Local development**: `akka_local_start`, `akka_local_run_service`, `akka_local_cluster_status`, `akka_local_status`
- **Service introspection**: `akka_backoffice_list_components`, `akka_backoffice_discovery`

## Purpose

This command sets up resilience testing for an Akka service. It discovers
the service's endpoints at runtime via backoffice MCP tools and writes a
`.akka/reliability.yml` config file. The daemon (port 9889) reads this
config and serves a self-contained testing dashboard — no code is
generated in the user's project.

Two modes:

- **Attach** (default): ensure cluster is running, discover endpoints,
  write config, report dashboard URL
- **Remove**: delete `.akka/reliability.yml` (and any legacy artifacts)

The dashboard is served by the daemon at
`http://localhost:9889/resilience/` and provides:

- Single-shot READ/WRITE operations against the service
- Burst load testing with configurable duration, interval, and read ratio
- Real-time latency chart and transaction log via SSE
- Cluster node management (stop/start nodes 2–3 to test failover)

---

## Attach Workflow

### Step 0 — Ensure cluster is running

1. Call `akka_local_status` to check if the daemon is running.
2. If not running: call `akka_local_start` with `postgres: true`.
3. Check if a service is running. If not: call `akka_local_run_service`
   with `nodes: 3` to start a 3-node local cluster.
4. Call `akka_local_cluster_status` to verify nodes are up.
5. If the cluster fails to start, check `akka_local_logs` with
   `source: "service"` for errors and report to the user.

### Step 1 — Discover endpoints via backoffice

1. Read `pom.xml` to get the `<artifactId>` — this is the **service name**.
   Use it as the `service` parameter for all backoffice MCP calls.
   Do **not** guess or infer the service name from the project's domain
   or folder name.

2. Call `akka_backoffice_list_components` with `service` set to the
   artifactId and `local: true`. This returns every component and its
   `endpoint_definitions[]` with HTTP method and path for each endpoint.

2. **Present the inventory** to the user:

   ```
   ## Discovered Endpoints

   ### Components
   - ShoppingCart (EventSourcedEntity)
   - CartView (View)

   ### Endpoints
   - GET  /carts/{cartId}        → ShoppingCart       [READ]
   - POST /carts/{cartId}/items  → ShoppingCart        [WRITE]
   - GET  /carts/{cartId}/view   → CartView            [READ]

   ### Selected for testing
   - **Read operation**: GET /carts/{cartId} → ShoppingCart
   - **Write operation**: POST /carts/{cartId}/items → ShoppingCart
   ```

3. **Classify** each endpoint:
   - `GET` → **READ** candidate
   - `POST` / `PUT` / `DELETE` / `PATCH` → **WRITE** candidate
   - Methods on Agent components → **AGENT** candidate (also a write)
   - `POST` endpoints on View components that query data → **READ**
     (these are query endpoints, not mutations)

4. **Auto-select defaults**:
   - **Read**: prefer a `GET` endpoint with **no path parameters** (e.g.
     `GET /api/dinosaurs` over `GET /api/dinosaurs/{id}`). Parameterless
     endpoints always work — the daemon substitutes random values for
     `{id}` placeholders, which will 404 if the service uses non-UUID
     IDs like slugs. Only select a parameterized `GET` if no
     parameterless read endpoint exists.
   - **Write**: prefer a `POST`/`PUT` that mutates entity state. If none
     exists, use an Agent endpoint.

5. Present selections and ask the user to **confirm or override**.
   Show **only** the tables and selections above. Do **not** add any
   notes, commentary, caveats, or explanations about the selections.
   Do **not** mention admin endpoints, missing endpoints, or why one
   endpoint was chosen over another. Just present the data and ask.

### Step 2 — Construct body templates

For write operations, construct a minimal JSON body template:

1. Call `akka_backoffice_discovery` with `local: true` to get the full
   protobuf spec. This includes message type definitions with field
   names and types for every endpoint's request and response.
2. Find the message type for the selected write endpoint's request body.
   Build a minimal JSON template from its fields. Use `{id}` as a
   placeholder for string ID fields — the daemon substitutes UUIDs at
   runtime. Use sensible defaults for other fields.
3. Do **not** read source files on disk. All schema information is
   available from the protobuf discovery spec.

Example: `{"productId": "test-{id}", "name": "Load Test Item", "quantity": 1}`

### Step 3 — Write `.akka/reliability.yml`

Write the config file with all discovered information:

```yaml
# Written by /akka:reliability, read by the daemon
# Edit freely — changes take effect immediately (no restart needed)

service:
  name: "<artifactId>"

operations:
  read:
    method: GET
    path: "<selected read path>"
    component: "<component name>"
    description: "<brief description>"
  write:
    method: <POST|PUT>
    path: "<selected write path>"
    component: "<component name>"
    description: "<brief description>"
    body:
      template: "<JSON template>"

cluster:
  nodes: 3
```

Also write `.akka/reliability.manifest` listing generated files for
clean removal:

```
.akka/reliability.yml
.akka/reliability.manifest
```

### Step 4 — Report dashboard URL

```
Reliability Testing Ready

Dashboard: http://localhost:9889/resilience/

What you can do:
- Click READ/WRITE to run individual operations
- Launch a burst to generate sustained traffic
- Stop any node to observe failover behavior
- Watch the latency chart for spikes during failures
- The config is at .akka/reliability.yml — edit it to change
  endpoints, and changes take effect immediately
```

No compilation step. No restart. The daemon reads the config on demand.

---

## Remove Workflow

### Step R1 — Check for artifacts

1. Check for `.akka/reliability.manifest`. If found, read its file list.

### Step R2 — Confirm removal

Present the list of files to be deleted and ask for confirmation.

### Step R3 — Delete files

Delete each file found. For legacy artifacts, also run `akka_maven_compile`
to verify the project still compiles after removing generated Java code.

### Step R4 — Report

_"Reliability testing artifacts removed."_

---

## Error Handling

- If `akka_local_start` fails with port conflict: check `akka_local_status`,
  suggest `akka_local_stop` first.
- If `akka_backoffice_list_components` returns no components: the service
  may not have registered yet. Wait a few seconds and retry. If still
  empty: _"No components found. Make sure the service has at least one
  entity, agent, or workflow."_
- If `akka_backoffice_list_components` returns no endpoints: _"No HTTP
  endpoints found. Create at least one @HttpEndpoint class first."_
- If cluster nodes fail with `BindException`: call `akka_local_stop` to
  clean up stale processes, then retry.
- If the dashboard doesn't load at `http://localhost:9889/resilience/`:
  verify the daemon is running with `akka_local_status`. The dashboard is
  served by the daemon, not the user's service.

## Key Rules

- **No code generation** — the only file written to the user's project is
  `.akka/reliability.yml` (and the manifest). No Java, no HTML.
- **Runtime discovery** — always use `akka_backoffice_list_components` with
  `local: true` to discover endpoints. Never use static source analysis.
- **User approval required** — present auto-detected operations for
  confirmation before writing the config.
- **Dashboard is on port 9889** — the daemon port, not the service port.
  The dashboard is served by the daemon, not the user's service.
- **Hot-reload** — the daemon reads `.akka/reliability.yml` on every
  request. The user can edit the config and changes take effect immediately.
- **MCP tools only** — use `akka_*` tools for all interactions. Never use
  shell commands directly.

## Done When

**Attach workflow:**

- [ ] Required MCP tools were verified available (`akka_local_start`, `akka_local_run_service`, `akka_local_cluster_status`, `akka_local_status`, `akka_backoffice_list_components`, `akka_backoffice_discovery`) — the command stopped and told the user to update the Akka CLI if any were missing.
- [ ] `akka_local_status` confirms the daemon is running (started via `akka_local_start` with `postgres: true` if needed).
- [ ] A 3-node local cluster is running (started via `akka_local_run_service` with `nodes: 3` if not already active) and `akka_local_cluster_status` verifies all nodes are up.
- [ ] The service name came from `pom.xml`'s `<artifactId>` — not inferred from folder name or domain — and was passed as the `service` parameter to every backoffice call.
- [ ] `akka_backoffice_list_components` (`local: true`) returned the component inventory and endpoint definitions; the full inventory was presented to the user with the auto-selected READ and WRITE operations, and the user confirmed or overrode the selection before the config was written.
- [ ] Auto-selection followed the documented preferences: READ preferred a parameterless `GET`, WRITE preferred a `POST`/`PUT` that mutates entity state (Agent endpoints only if no other write exists); no explanatory notes about missing/rejected endpoints were added to the confirmation prompt.
- [ ] The write body template was constructed from `akka_backoffice_discovery` protobuf definitions — not from reading source files — with `{id}` placeholders for string IDs.
- [ ] `.akka/reliability.yml` was written with the service name, selected read/write operations (method, path, component, description, body template for write), and `cluster.nodes: 3`; `.akka/reliability.manifest` was written listing generated files.
- [ ] The report tells the user the dashboard URL `http://localhost:9889/resilience/`, describes what the dashboard supports, and reminds them the config is hot-reloaded on edit.
- [ ] NO Java, HTML, or other code was generated in the user's project — only `.akka/reliability.yml` and `.akka/reliability.manifest` were written.

**Remove workflow:**

- [ ] `.akka/reliability.manifest` was read (or the user was told there is nothing to remove).
- [ ] The list of files to be deleted was presented and the user explicitly confirmed removal.
- [ ] Each manifested file was deleted; for legacy artifacts including generated Java, `akka_maven_compile` was run afterward and the result reported.
- [ ] The user was told _"Reliability testing artifacts removed."_ once removal completed.

---
name: run-app
description: "Build and start the Mendix app in Docker, and restart it after changes. Use when asked to run, launch or restart the app in a container. For the fast inner loop prefer run-local."
---

# Run App Skill

This skill builds and starts the Mendix application in Docker.

## When to Use This Skill

Use this when:
- The user asks to run, start, or launch the app
- The user asks to rebuild and restart after making changes
- The user wants to test their changes in a running environment

## Prerequisites Check

Before running, verify:

1. **mxcli is local** — always use `./mxcli`, not `mxcli`
2. **Docker is available** — check with `docker ps`

Everything else (MxBuild, runtime, Docker stack) is auto-downloaded/initialized by `docker run`.

---

## Quick Start: One Command

```bash
# Setup, build, and start — handles everything automatically
./mxcli docker run -p MxCliDemoApp2.mpr --wait
```

This single command:
1. Downloads MxBuild (if not cached)
2. Downloads the Mendix runtime (if not cached)
3. Initializes the Docker stack (if not already done)
4. Builds the PAD package
5. Starts the containers in the background
6. Waits for "Runtime successfully started" (with `--wait`)

The app is available at: **http://localhost:8080**
Admin console: **http://localhost:8090** (password: `AdminPassword1!`)

---

## After Making MDL Changes

**Model/page/security changes** (microflows, entities, pages, navigation):

```bash
# 1. apply MDL changes to the project
./mxcli exec changes.mdl -p MxCliDemoApp2.mpr

# 2. Rebuild and hot reload (no restart, keeps database)
./mxcli docker build -p MxCliDemoApp2.mpr --skip-check
./mxcli docker reload -p MxCliDemoApp2.mpr
```

Use `docker reload` for most changes — it reloads the model in ~100ms without restarting.
Use `docker run --fresh` only when schema changes are destructive (dropped entities/attributes):

```bash
./mxcli docker run -p MxCliDemoApp2.mpr --fresh --wait
```

**CSS/theme changes only** (no rebuild needed):

```bash
# Instant CSS hot reload — pushes to all connected browsers
./mxcli docker reload -p MxCliDemoApp2.mpr --css
```

Or simply hard-refresh the browser (Cmd+Shift+R / Ctrl+Shift+R) — the volume mount means compiled CSS is immediately available on disk after `mxcli docker build`.

---

## Step-by-Step Alternative

If you prefer more control over individual steps:

```bash
# First-time setup (cached, run once per devcontainer)
./mxcli setup mxbuild -p MxCliDemoApp2.mpr
./mxcli setup mxruntime -p MxCliDemoApp2.mpr
./mxcli docker init -p MxCliDemoApp2.mpr

# build and start
./mxcli docker build -p MxCliDemoApp2.mpr
./mxcli docker up -p MxCliDemoApp2.mpr --detach --wait
```

---

## Query Data (OQL)

Once the app is running, test OQL queries against the live runtime:

```bash
# run OQL queries (read-only preview mode)
./mxcli oql -p MxCliDemoApp2.mpr "select Name from MyModule.Customer"

# json output for piping
./mxcli oql -p MxCliDemoApp2.mpr --json "SELECT count(c.ID) FROM MyModule.Order AS c"
```

> **Existing projects**: If you get "Action not found: preview_execute_oql", re-initialize
> the Docker stack to pick up the required JVM flag:
> `./mxcli docker init -p MxCliDemoApp2.mpr --force`

---

## Monitoring

```bash
# view live logs
./mxcli docker logs -p MxCliDemoApp2.mpr --follow

# view last 50 lines
./mxcli docker logs -p MxCliDemoApp2.mpr --tail 50

# open a shell in the Mendix container
./mxcli docker shell -p MxCliDemoApp2.mpr
```

Look for this line to confirm successful startup:
```
Mendix runtime successfully started, the application is now available.
```

---

## Stop

```bash
# Stop containers (keeps database data)
./mxcli docker down -p MxCliDemoApp2.mpr

# Stop and wipe database
./mxcli docker down -p MxCliDemoApp2.mpr --volumes
```

---

## Running Multiple Projects

When running multiple Mendix apps simultaneously, each project needs unique ports. Use `--port-offset` to shift all ports:

```bash
# First project (default ports: 8080/8090/5432)
./mxcli docker run -p project1/app.mpr --wait

# Second project (ports: 8081/8091/5433)
./mxcli docker init -p project2/app.mpr --port-offset 1
./mxcli docker run -p project2/app.mpr --wait
```

| Offset | App | Admin | DB |
|--------|-----|-------|----|
| 0 | 8080 | 8090 | 5432 |
| 1 | 8081 | 8091 | 5433 |
| 2 | 8082 | 8092 | 5434 |

The offset is applied once during `docker init` and written to `.docker/.env`. Subsequent `docker run/up/reload` commands read from that `.env` automatically.

> **Note:** If the Docker stack was already initialized, re-run init with `--force`:
> `./mxcli docker init -p app.mpr --port-offset 1 --force`

---

## Architecture Note

The containers run inside a Docker-in-Docker daemon inside the devcontainer — they are **not** visible in Docker Desktop on the host. Port forwarding (8080, 8090) is handled by VS Code automatically.

The build output (`.docker/build/`) is **volume-mounted** into the container — no Docker image rebuild needed. After `mxcli docker build`:
- **CSS/theme changes**: Hard-refresh the browser — files are already on disk via the mount
- **Model changes**: Run `mxcli docker reload` — hot reloads the model in ~100ms, no restart needed
- **Destructive schema changes**: Restart with `mxcli docker up --fresh` to recreate the database

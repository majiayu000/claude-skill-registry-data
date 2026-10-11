---
name: aspire-docker-restart-recovery
description: "Use when an Aspire stack misbehaves right after a Docker Desktop or WSL restart: services report Running/Healthy but sit at 0% CPU with no app logs, every container shows Exited (255), or a persistent container has lost its host port bindings."
---

# Aspire + Docker restart recovery

A Docker Desktop / WSL restart leaves an Aspire stack broken while every dashboard resource
still reports **Running / Healthy**: Aspire only watches processes, not whether they are
serving, and its wait-gates passed before the backing store died.

If the machine's LAN hostname refuses connections while `localhost` still works, that is the
portproxy half of the same restart — see `aspire-lan-exposure`.

## Symptom: services alive, silent, 0% CPU

`.NET` processes exist, no port is bound, and console logs show only Aspire's dependency-wait
lines ("Finished waiting for resource 'cache'") — **not one line of app output**. The services
are blocked on DB/cache sockets that Docker's proxy accepts but never serves, before their
logging pipeline ever flushes.

## Diagnose (cheap, decisive checks first)

```bash
# 1. Do the containers have HOST port bindings?
docker ps --format "{{.Names}}\t{{.Status}}\t{{.Ports}}"
# healthy: 127.0.0.1:56117->6379/tcp    broken: 5432/tcp   <- no host binding at all

# 2. THE TELL - every container exited at the same moment with the same code:
docker ps -a --format "{{.Names}}\t{{.Status}}"    # Exited (255) N minutes ago, all of them
docker run --rm hello-world                         # daemon itself healthy again

# 3. Spinning or blocked? 0.00s CPU over 5s = blocked on I/O, not a livelock.
powershell -NoProfile -Command "$ids=<pids>; $a=Get-Process -Id $ids|Select Id,CPU; Start-Sleep 5; ..."

# 4. Do they listen at all?
netstat -ano | grep -E ':(8090|9080|5000)\s' | grep LISTENING
```

Simultaneous `Exited (255)` across unrelated containers (including ones from other projects)
is a daemon-level event, not a per-container fault. `mcp__aspire_list_console_logs` confirms
the dependency-wait-only output.

## Recover: recreate persistent containers, never restart them

Port publishing is fixed at container creation — `docker start` on a container that survived
the daemon crash **cannot re-establish it**, and `aspire stop` / `aspire run` alone reuses the
same persistent containers. Confirm before blaming the app:

```bash
docker inspect <container> --format '{{json .HostConfig.PortBindings}} {{json .NetworkSettings.Ports}}'
# HostConfig wants a binding, NetworkSettings.Ports is empty (e.g. {"5432/tcp":[]}) -> nothing is forwarded
```

The data lives in a named volume (e.g. `db-data-<title>`), so removal is safe once the mount
is verified:

```bash
docker inspect <container> --format '{{json .Mounts}}'   # confirm a NAMED VOLUME holds the data
aspire stop                                              # never pkill
docker rm -f <persistent-db> <persistent-clickhouse> <event-stream> <orphaned session containers>
docker volume ls | grep <project>                        # volumes survive; data is safe
aspire run                                               # DCP recreates with bindings; volume reattaches
```

Verify with real requests, not resource state: `curl -m 6 -o /dev/null -w '%{http_code}'`
against a health endpoint and the gateway.

## Gotchas

- Aspire MCP tools go stale after a stack restart: `refresh_tools` → `list_apphosts` →
  `select_apphost` before `execute_resource_command`.
- Dashboard login tokens regenerate every run; a bookmarked `?t=` URL is always wrong after a
  restart. Get the current one from `aspire ps`.

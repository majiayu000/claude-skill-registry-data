---
name: aspire-lan-exposure
description: "Use when setting up or repairing LAN access to an Aspire stack's containerized endpoints (Caddy/proxy, Valkey/Redis): other machines cannot reach them, or the LAN hostname refuses while localhost works — including right after a Docker Desktop or WSL restart."
---

# Aspire LAN exposure and portproxy repair

Use when a machine other than the AppHost host cannot reach an Aspire-hosted
endpoint, or when a previously working `http://<machine>:PORT` starts refusing
while `localhost:PORT` still works.

## Root cause (do not re-derive)

Aspire's DCP publishes **container** ports loopback-only: a stable
`127.0.0.1:PORT` listener proxies to a random docker host port. Nothing binds
the LAN interface, so reaching it by machine name needs a `netsh interface
portproxy` rule. `ASP_HOSTNAME` only rewrites *advertised* URLs
(`GetHostName()` in `Orchestration/AppHost/Extensions.cs` feeding `WithUrl` and
`GAMECORE_URL`) — it changes no binding, so the dashboard can advertise a name
that has no listener.

## Triage

```bash
# 1. Is it loopback-only?
netstat -ano | grep -E ":(5000|6379)\s" | grep LISTENING   # expect 127.0.0.1 + [::1] only
# 2. Do bridging rules exist?
powershell -NoProfile -Command "netsh interface portproxy show all"
# 3. Are they actually bound?
powershell -NoProfile -Command "(Test-NetConnection <HOST> -Port 5000 -WarningAction SilentlyContinue).TcpTestSucceeded"
```

No rules → add them below. Rules listed but `TcpTestSucceeded=False` =>
iphlpsvc dropped the listeners while the rules stayed in the registry
(typically after a Docker Desktop / WSL network restart). If the stack's
services are also silent at 0% CPU, recover them first with
`aspire-docker-restart-recovery`.

## Fix: delete + re-add each rule (elevated)

Re-adding rebinds immediately. **Never** `Restart-Service iphlpsvc` — it errors
with `ServiceHasDependentServices`, and `-Force` stops the NAT/ICS dependents
Docker networking rides on.

```powershell
$ip = '<LAN-IP>'
foreach ($p in 5000, 6379) {   # first-time setup: all ports; repair: only those that failed step 3
    netsh interface portproxy delete v4tov4 listenaddress=$ip listenport=$p | Out-Null
    netsh interface portproxy add    v4tov4 listenaddress=$ip listenport=$p connectaddress=127.0.0.1 connectport=$p | Out-Null
}
```

Repair only ports that actually fail the connect test: re-adding a live rule
drops the connections through it, which mid-load-test reads as server failures.
Make it self-healing with a SYSTEM scheduled task running the same
probe-then-repair script at boot and every 10 minutes
(`schtasks /Create /SC ONSTART /RU SYSTEM` plus `/SC MINUTE /MO 10`).

Run it elevated from bash (the gsudo shim is not exec'able by path; keep the
payload in a `.ps1` file rather than an inline command string):

```bash
powershell -NoProfile -Command "& 'C:\Program Files\gsudo\Current\gsudo.exe' powershell -NoProfile -ExecutionPolicy Bypass -File '<abs path>.ps1'"
```

Also open the firewall once per rig:
`New-NetFirewallRule -DisplayName '<name>' -Direction Inbound -LocalPort 5000,6379 -Protocol TCP -Action Allow`.

## Advertised hostnames

Setting `ASP_HOSTNAME` machine-wide changes every advertised URL and dashboard
link to the machine name. That is correct for anything remote (a remote worker
reading `localhost` targets *itself* and gets connection-refused) and harmless
locally, since both names hit the same listener. Delete the variable rather
than blanking it — `?? "localhost"` fallbacks do not catch an empty string and
you get `http://:5000`.

## Client-side corollary

Any address handed to *other* machines must never be `localhost`. Rewrite it at
the point it is published (e.g. job payloads:
`Regex.Replace(url, "//(localhost|127\\.0\\.0\\.1)", "//" + (ASP_HOSTNAME ?? MachineName))`)
and default such fields to the machine name, not localhost.

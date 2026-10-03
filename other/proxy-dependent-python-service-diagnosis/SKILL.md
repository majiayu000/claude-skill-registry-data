---
name: proxy-dependent-python-service-diagnosis
description: Read-only diagnosis workflow for Python services whose external HTTP or WebSocket readiness differs between manual tests and service runtime behind a proxy.
---

# Proxy-Dependent Python Service Diagnosis

## Purpose
Determine whether a Python service's external HTTP/WebSocket failures are caused by proxy environment propagation, client-library proxy behavior, proxy instability, stale readiness artifacts, or a different service entrypoint.

## When to use
- Manual network tests pass through a proxy but the service runtime fails.
- Readiness checks report network unreachable, connection timeout, handshake timeout, or proxy-related errors.
- HTTP proxy variables are configured but behavior is inconsistent.
- A systemd-managed Python service behaves differently from same-user manual commands.

## Safety rules
- Default workflow is read-only.
- Do not edit systemd units, wrappers, Python code, proxy config, or service environment without explicit approval.
- Do not restart services or proxy daemons without approval.
- Do not print proxy credentials, private endpoint URLs, tokens, cookies, or raw readiness payloads.
- Redact concrete addresses and ports as `<PROXY_URL>`, `<SERVER_IP>`, `<SERVICE_NAME>`, `<PROJECT_ROOT>`, and `<EXTERNAL_ENDPOINT>`.

## Read-only workflow
1. Capture current failure class from safe summaries: HTTP failure, WebSocket failure, both, stale artifact, or mixed evidence.
2. Inspect service metadata: user, working directory, command line, environment keys present, main PID, restart count, and unit entrypoint.
3. Read the startup chain: systemd unit, wrapper script, virtual environment activation, module entrypoint, and any supervising loop. Summarize; do not expose secrets.
4. Inspect the live child Python process environment through `/proc/<pid>/environ`, redacting values. Confirm whether proxy variables, virtualenv, path, and Python path reached the actual child process.
5. Compare the live process command line with the manual command being tested.
6. Inspect readiness/probe implementation names and client libraries involved: HTTP client, WebSocket client, custom wrappers, and whether the library honors environment proxy settings.
7. Reproduce read-only probes in concept or in a controlled approved diagnostic session: same user, same virtualenv, same working directory, same Python path, with proxy and without proxy. If not approved to run probes, describe the test plan only.
8. Check whether readiness artifacts are current: timestamp, PID/session correlation, and whether another process may be overwriting the same artifact.
9. Separate conclusions for HTTP and WebSocket. Do not summarize one as proof for the other.
10. Rank likely causes and identify the next safe diagnostic step.

## Evidence to collect
- Service metadata summary.
- Live child process environment keys present, values redacted.
- Entrypoint and wrapper chain summary.
- HTTP client and WebSocket client/library versions if safely available.
- Readiness artifact timestamp and status class.
- Error class summaries for HTTP and WebSocket separately.
- Manual-vs-service difference matrix.
- Duplicate process or stale artifact indicators.

## Stop conditions
- Inspecting the process environment would expose secrets that cannot be safely redacted.
- The next step requires code changes, service restart, proxy restart, or config edits.
- Manual probes would hit write endpoints or trigger external side effects.
- The current artifact timestamp is stale and no current evidence exists.

## Optional user-approved actions
Only after explicit user approval:
- Run same-user, same-venv diagnostic probes.
- Add temporary debug instrumentation that records redacted proxy state.
- Patch client configuration to use explicit proxy settings.
- Restart the service or proxy daemon.
- Disable duplicate manual launch chains that are overwriting artifacts.

## Final report format
```text
Summary: <proxy/runtime diagnosis>
Service: <SERVICE_NAME>
Current readiness: <status/timestamp/class>
Live process evidence: <env keys present, command summary>
HTTP path: <works/fails/unknown and evidence>
WebSocket path: <works/fails/unknown and evidence>
Artifact freshness: <current/stale/ambiguous>
Likely cause: <ranked hypothesis>
Next diagnostic step: <read-only or approval-required>
Needs approval: <specific action>
```

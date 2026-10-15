---
name: debugging-azure-container-apps
description: Use when debugging any Azure Container App or Container App Job - restart loops, crashes, 503s, image pull failures, probe/health-check failures, failed job executions, a revision that broke after deploy - and for containers running a Functions image, where FunctionLoadError, WorkerInitError, "Host state changed to Error", MS_FUNCTION_LOGS entries, or functions 404ing after a deploy also apply. Also use when reaching Azure logs is itself the problem - InvalidTokenError, SignatureVerificationFailed, 401/403 against management.azure.com or api.loganalytics.io, missing bearer token in a sandbox, or an empty ContainerAppConsoleLogs result.
---

# Debugging Azure Container Apps

## Overview

Everything here is a container app. Some run a Functions image, which adds a runtime layer inside the container with its own failure modes — but the platform beneath is identical, so the access, logging, and revision mechanics are the same either way.

Two things drive most wrong conclusions:

- **Two log streams, not one.** Console logs are your container's stdout/stderr. System logs are the platform's view of it. A container that never starts writes nothing to console logs.
- **An empty result usually means wrong table, wrong window, or not yet ingested** — far more often than it means nothing happened.

## Diagnosis Flow

0. **Establish access as a verified state, before any diagnosis.** Access is a tuple — credential variable, base URL, query mode, workspace identifier — not just "a token." Resolve all of it in one bounded pass:

   ```bash
   SKILL_DIR=<directory containing this SKILL.md>
   source "$SKILL_DIR/azure-access.sh"
   az_resolve                                          # credential + ARM base + ARM probe
   az_workspaces                                       # workspaceResourceName, resourceGroup, customerId
   az_gate <workspaceResourceGroup> <workspaceResourceName> <subscription-id>
   ```

   `az_gate` runs `print AccessProbe = 1`. **Until it prints OK, you do not have log access** — a working ARM call does not imply one. If any step fails, its Azure error code maps to exactly one corrective action in the decision table in [access.md](access.md). Take that action; do not try other tokens, base URLs, headers, or api-versions.

1. **Orient** — find the app or job, its environment, and the linked workspace ([access.md](access.md)).
2. **Check revision state** (apps) or **execution history** (jobs) — provisioned, running, and actually receiving traffic?
3. **Probe the table schema**, then read **system logs** — did the container start at all? Image pull, probes, OOM, scaling.
4. **Console logs, unfiltered** — what did the app itself say?
5. **If it runs a Functions image** — apply the layer model below before believing any host-level error.
6. **Compare against the last working revision** — diff the templates.

Queries: [kql-cookbook.md](kql-cookbook.md). Auth, the query helper, and ARM calls: [access.md](access.md).

## The two log tables

| Table | Contains | Use when |
|-------|----------|----------|
| `ContainerAppConsoleLogs_CL` | Container stdout/stderr (including all Functions host and worker output) | The app runs but misbehaves |
| `ContainerAppSystemLogs_CL` | Platform events: image pull, probe results, scaling, revision provisioning | The app never starts, restarts, or 503s |

**The trap:** debugging a container that won't start by reading console logs. There are none — it never got far enough to write any.

Workspaces configured for resource-specific tables drop the `_CL` suffix. A wrong table name returns an error easily misread as an empty result — see table discovery in [access.md](access.md).

## Container App Jobs are not apps

`Microsoft.App/jobs` share the environment, the workspace, and both log tables with apps — but not the schema or the lifecycle. **Run `| getschema` before writing any filter** ([access.md](access.md)); a filter on a column the table does not have returns zero rows and is indistinguishable from "nothing happened."

| | Container app | Container App Job |
|---|---|---|
| Name column | `ContainerAppName_s` | `ContainerJobName_s` |
| Log column | `Log_s` | `Log_s` or `log_s` |
| Unit of work | revision + replicas | execution + replicas |
| Lifecycle | long-running; restarts are failures | starts, runs, exits; exit 0 is success |
| Where state lives | `.properties.configuration.ingress.traffic` | `/executions` under the job resource |

A job has no ingress, no traffic split, and no `latestRevisionName`. "Not running" is its normal state — check the execution list and its `.properties.status` before treating silence as a fault.

## Symptom → where to look

| Symptom | Look at | First thing to check |
|---------|---------|---------------------|
| `InvalidTokenError` / `SignatureVerificationFailed` / 401 / 403 | Access tuple | Wrong audience or wrong query mode — decision table in [access.md](access.md). Not a KQL problem |
| 503 on every request | System logs, ingress | Container never started, or `targetPort` ≠ the port the app listens on |
| Restart loop | System logs, then console | Probe failures, OOM kill, then the app's last output before exit |
| `ImagePullBackOff` / no revision | System logs, ARM | Registry credentials, image tag typo, private registry access |
| Worked before this deploy | ARM revision diff | Image tag, env vars, secrets, resource limits |
| Intermittent failures | Traffic split | Two revisions live — you may be seeing only one |
| Scaled to zero, slow first request | System logs | Cold start; check `minReplicas` |
| **Job:** no logs for a job name | Table schema | Filtered on `ContainerAppName_s`; jobs use `ContainerJobName_s` |
| **Job:** execution never produced output | ARM `/executions`, system logs | Trigger fired at all? `replicaTimeout`, `replicaRetryLimit`, image pull |
| **Functions:** every endpoint 404s | Console, worker layer | All functions failed to load — import or dependency error |
| **Functions:** one endpoint 404s | Console, worker layer | That function failed to load, or was never deployed |
| **Functions:** `Host state changed to Error` | Console, worker layer | Worker load failures upstream of it — not the cause itself |
| **Functions:** load fine, fail at invoke | Console, extensions | Binding config, storage connection, missing app settings |

## Container apps running a Functions image

A Functions image runs two runtimes in one container: the .NET **Functions host** and a **language worker** (Python, Node, etc.) it launches over gRPC. Both write to the same console stream in different formats — and the worker's errors, the ones that usually matter, arrive as structured JSON that looks like telemetry.

**Core principle:** Never exclude `MS_FUNCTION_LOGS` when filtering. That is where the worker errors live.

| Priority | Layer | What to look for |
|----------|-------|-----------------|
| **1** | **Language worker** | `FunctionLoadError`, `WorkerInitError`, import errors, dependency issues |
| **2** | **Functions host** | `Host state changed to Error`, `Startup operation`, `Host started` |
| **3** | **Extensions** | `Error building configuration in an external startup class`, bundle mismatches |
| **4** | **Infrastructure** | Storage client errors, diagnostic logging failures (usually non-fatal) |

**The trap:** Layer 4 errors are plain text, loud, and arrive first in a time-ordered query. Layer 1 errors sit inside `MS_FUNCTION_LOGS` JSON blobs. The alarming thing you see first is usually not the cause.

**Corollary:** `Host state changed to Error` is a *symptom*. It almost always means the worker failed to load functions. Resist reporting it as a root cause.

`MS_FUNCTION_LOGS` entries carry a numeric `Level`: 0 Trace, 1 Debug, 2 Information, 3 Warning, 4 Error, 5 Critical. `Category` identifies the layer — `Worker.python` / `Worker.node` is layer 1, `Microsoft.Azure.WebJobs.*` is layer 2. Parsing query in [kql-cookbook.md](kql-cookbook.md).

### Known Functions noise — real, but not your bug

| Message | What it is |
|---------|-----------|
| `Failed to publish status to /memoryactivity` | Platform metric publishing |
| `Failed to publish status to /functionactivity` | Same |
| `An error occurred writing to the diagnostic event table: (403)` | Disables diagnostic logging only; functions still load |

The `/memoryactivity` and `/functionactivity` messages come from platform metric ingestion on Consumption-backed plans. They cannot cause a function to fail, and the only "fix" is a Premium plan — don't raise them as an action item unless the user asked about log volume ([source](https://learn.microsoft.com/en-us/answers/questions/2278390/how-to-resolve-failed-to-publish-status-to-memorya)).

If these are the *only* errors present, you are looking at the wrong time window or the wrong layer.

## Common Mistakes

| Mistake | Why it's wrong |
|---------|---------------|
| Treating a successful ARM call as proof of log access | Different audience, path, and endpoint rule. Only `az_gate` proves it |
| Trying another token, base URL, header, or api-version after an auth error | Each access error has one corrective action ([access.md](access.md)). Cycling combinations never finds it |
| Treating any env var containing "token" as an Azure credential | The allowlist is the only rule. In nono the allowlisted var holds a *phantom* equal to `$NONO_PROXY_TOKEN`, so substituting the latter gains nothing; where no route loaded it gains a `401 InvalidTokenError` ([access.md](access.md)) |
| Guessing why `$AZURE_BEARER_TOKEN` is empty in nono | Depends on the route's `credential_key` (`az_nono_route`): a `cmd://` route is not active this session; any other key's secret failed to load. Report it to the user |
| Reading a nono `503 CaptureFailed` as an Azure outage | The host-side `cmd://` capture failed, usually an expired login (e.g. `az login`). The user fixes the login, you retry — no restart |
| Using the `customerId` GUID as the workspace name in an ARM path | ARM needs `workspaceResourceName`; the GUID belongs only to the data-plane API |
| Assuming app columns for a Container App Job | Jobs use `ContainerJobName_s`; the wrong column returns zero rows silently |
| Concluding "no logs" from an empty result | Ingestion lag, wrong table name, wrong column, or wrong time window |
| Reading only console logs | Startup, probe, and image-pull failures appear only in system logs |
| Assuming `latestRevisionName` serves traffic | With a traffic split the newest revision may take 0% — check `properties.configuration.ingress.traffic` |
| Debugging the app when the platform never started it | Confirm the container is running before analysing application behaviour |
| Filtering out `MS_FUNCTION_LOGS` early | These carry the actual worker errors as structured JSON |
| Treating `Host state changed to Error` as the cause | Almost always secondary to worker initialization failure |
| Using `api.loganalytics.io` with an ARM-audience token | The data plane needs its own audience — use the ARM workspace query mode ([access.md](access.md)) |
| Applying the Functions queries to a Consumption / App Service Function App | Those log to `FunctionAppLogs` and App Insights `traces`, not `ContainerAppConsoleLogs` |

## Ingestion Delay

Logs reach Log Analytics with a **1-5 minute delay**. If you just restarted a revision or triggered a deploy, an empty result means "not yet." Widen the window progressively before drawing conclusions.

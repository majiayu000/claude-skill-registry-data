---
name: sn-dbs-distribution-probe
description: "Prove whether an executable actually distributes across the SN-DBS build farm (and where it ran) before designing around it — use when asked to run work fleet-wide via SN-DBS, or when a job silently runs locally."
---

# SN-DBS distribution probe

SN-DBS is a distributed build farm (`dbsutil`, `dbsrun`, `dbsbuild` on PATH via a version-independent shim in `C:\Program Files (x86)\SCE\Common\SN-DBS\bin`). Use this to get **evidence** about what it will and will not distribute, instead of reasoning from the manual.

## 1. Confirm the network and inventory

```powershell
dbsutil -connected     # "SN-DBS network is available" + active broker
dbsutil -l             # every agent: Agent: "name" fqdn (ip) vX.Y [enabled]
```

`dbsutil -l` is an authoritative fleet inventory — better than AD computer accounts, because an enabled agent is a live machine with a running service. Parse with:
`^Agent:\s+"(?<name>[^"]+)"\s+\S+\s+\((?<ip>[^)]+)\)\s+\S+\s+\[(?<state>[^\]]+)\]`

## 2. Flood, never trickle

A small batch proves nothing: SN-DBS runs jobs locally when local CPU is free, and the report says so with `"where":"local"`, `local_scheduling_reasons: {"allow_local_cpu": ""}`. **Post ~300 jobs** so work spills onto agents.

Script file = one command per line (batch style; `&&` chains within a line). Then:

```powershell
dbsrun dbsbuild -p <ProjectName> -gt --report <out.json> -s <script.bat>
```

`-gt` allows generic tools (no tool template). `--report` is the whole point: it writes JSON with `completed_jobs[]`, each carrying `where` (local|remote), `host_name`, `exit_code`, `stdout`, `stderr`, `failovers`.

## 3. Read the report, not the console

```python
import json, collections
d = json.loads(open('out.json').read())
jobs = d['completed_jobs']
print(collections.Counter(j['where'] for j in jobs))
print(collections.Counter(j.get('host_name') or 'LOCAL' for j in jobs))
print(collections.Counter(j['exit_code'] for j in jobs))
```

Have the probe program print its own `hostname` so stdout independently proves *execution* on the remote box, not just shipping.

## 4. Known-good controls

- `hostname.exe` — native, on every box: baseline that distribution works at all.
- `C:\Windows\System32\curl.exe -s -o NUL -w "http=%{http_code} connect=%{time_connect}" <url>` — proves DNS + TCP egress from inside the sandbox to your target.

## 5. Rules that constrain any design

- **Native PE only.** Normal .NET fails remotely with `The application to execute does not exist: '<app>.dll'`. **NativeAOT works** (`PublishAot=true`, single file, no side-by-side DLLs).
- **No machine targeting.** No affinity attribute exists; the scheduler picks. Exclusions are GUI-only (Network View → Members → right-click), not scriptable — only `DedicatedBuildServer` appears in `dbsutil -list-settings`.
- **Batch semantics.** Jobs must run to completion, honour a kill `timeout`, take input from argv/env/files, and return output via stdout/stderr/files. One failure can abort the batch — exit 0 whenever you produced output.
- **Idle-only agents** that withdraw when their owner gets busy: fine for throughput work, wrong for pinned-concurrency work.

## 6. Design shape that fits

Emit **one line of JSON per job on stdout** (counts, sums, and a capped reservoir of raw samples), then merge the pooled samples driver-side. Never average per-job percentiles.

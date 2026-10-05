---
name: free-my-cpu
description: Safely audit and reduce CPU, load average, I/O wait, and Docker container resource pressure on macOS and Ubuntu/Linux hosts, especially remote production-like servers over SSH. Use when a host feels slow, load average is high, monitoring shows CPU spikes, Docker containers are suspected of consuming CPU, a service dashboard times out, or the user asks for a repeatable CPU optimization workflow.
---

# Free My CPU

## Core Rule

Prefer a read-only audit before changing anything. Separate CPU saturation from I/O wait, memory pressure, blocked tasks, noisy dashboards, and runaway containers. Classify findings by safety and impact before recommending restarts, rate limits, query changes, or container resource caps. Never kill processes, restart services, edit crontab/systemd timers, change Docker Compose limits, or throttle production workloads unless the user explicitly accepts the exact target and impact.

## Quick Audit

Detect the platform and pressure first:

```bash
uname -a
uptime
nproc
free -h
cat /proc/pressure/cpu 2>/dev/null || true
cat /proc/pressure/io 2>/dev/null || true
```

For Ubuntu/Linux, run the bundled read-only script first when possible:

```bash
bash scripts/audit_linux_cpu.sh
```

For macOS, there is no bundled cleanup script yet; start with read-only built-ins:

```bash
uptime
sysctl -n hw.ncpu
vm_stat
top -l 1 -o cpu -stats pid,command,cpu,mem,state,time | head -40
ps aux -r | head -30
```

On Apple Silicon laptops, distinguish real CPU saturation from Spotlight, photo analysis, backup, Docker Desktop, browser tabs, and Xcode indexing before proposing changes.

For a remote Linux host, replace `my-server` with the SSH alias:

```bash
ssh my-server 'bash -s' < scripts/audit_linux_cpu.sh
ssh my-server 'SAMPLES=5 INTERVAL=10 LOG_SCAN=1 bash -s' < scripts/audit_linux_cpu.sh
```

Use `SAMPLES` and `INTERVAL` to collect multiple Docker CPU snapshots. Use `LOG_SCAN=1` only when recent container logs are relevant; it scans a short tail for timeout, error, retry, OOM, and slow-request clues.

If the script is not suitable, gather the same facts manually:

```bash
uptime
nproc
free -h
ps -eo pid,ppid,user,stat,wchan:24,pcpu,pmem,etime,comm,args --sort=-pcpu | head -30
ps -eo pid,ppid,user,stat,wchan:24,pcpu,pmem,etime,comm,args | sed -n '1p; / D/p' | head -60
docker stats --no-stream --format 'table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.MemPerc}}\t{{.NetIO}}\t{{.BlockIO}}\t{{.PIDs}}' 2>/dev/null || true
docker ps --format 'table {{.Names}}\t{{.Image}}\t{{.Status}}' 2>/dev/null || true
```

When load is much higher than CPU count, always check I/O and blocked tasks:

```bash
cat /proc/pressure/io 2>/dev/null || true
iostat -xz 1 2 2>/dev/null || true
ps -eo pid,ppid,user,stat,wchan:24,pcpu,pmem,etime,comm,args | sed -n '1p; / D/p' | head -60
```

## Interpretation

Treat these as different problems:

- CPU-bound: high `%user` or `%system`, high Docker CPU, little I/O wait, few D-state tasks.
- I/O-bound: high load with notable `%iowait`, high `/proc/pressure/io`, D-state tasks, database or Influx queries timing out.
- Memory pressure: low available memory, high swap use, OOM messages, containers near memory limits.
- Monitoring-induced load: Grafana refreshes, alert rules, or wide time-range queries that repeatedly timeout and force InfluxDB, Postgres, or app APIs to scan too much data.
- App-loop load: logs show fast retries, reconnect storms, failed parsing loops, stuck schedulers, or repeated slow admin endpoints.

Use repeated samples before naming the culprit. A Grafana panel, backup, `du`, or migration can create a temporary spike that should not be treated as a steady-state offender.

## Docker Workflow

1. Rank containers by CPU over several samples:

```bash
for i in 1 2 3; do
  date -Is
  docker stats --no-stream --format '{{.Name}} {{.CPUPerc}} {{.MemUsage}} {{.PIDs}}' | sed 's/%//' | sort -k2 -nr | head -20
  sleep 10
done
```

2. Map hot containers back to Compose projects and services:

```bash
for c in container-a container-b; do
  docker inspect "$c" --format 'pid={{.State.Pid}} restart={{.RestartCount}} image={{.Config.Image}} project={{index .Config.Labels "com.docker.compose.project"}} service={{index .Config.Labels "com.docker.compose.service"}}'
done
```

3. Check whether CPU limits are absent:

```bash
docker inspect container-a --format 'NanoCpus={{.HostConfig.NanoCpus}} CpuQuota={{.HostConfig.CpuQuota}} CpuPeriod={{.HostConfig.CpuPeriod}} CpusetCpus={{.HostConfig.CpusetCpus}} Memory={{.HostConfig.Memory}}'
```

4. Inspect recent logs for causes, not just symptoms:

```bash
docker logs --since 30m --tail 200 container-a 2>&1 | grep -Ei 'timeout|deadline|error|warn|retry|oom|slow|duration|500|panic' | tail -80
```

## Data Service Checks

For Postgres containers, prefer read-only activity and table-size checks:

```bash
docker exec postgres-container psql -U app -d app -c "select pid, usename, state, now()-query_start as age, wait_event_type, wait_event, left(query, 260) as query from pg_stat_activity where state <> 'idle' order by query_start asc limit 12;"
docker exec postgres-container psql -U app -d app -c "select relname, pg_size_pretty(pg_total_relation_size(relid)) as total_size from pg_catalog.pg_statio_user_tables order by pg_total_relation_size(relid) desc limit 10;"
```

For InfluxDB or user-provided Grafana-backed dashboards, look for wide-range Flux queries, alert rules, high refresh rates, and repeated timeout logs. Prefer narrowing dashboard time ranges, raising aggregate windows, caching expensive panels, or reducing refresh cadence before restarting the database.

## External Monitoring Evidence

Use Grafana or another monitoring UI only when the user provides the dashboard URL, panel name, screenshot, exported query, or explicit time range to inspect. Do not assume a default dashboard for a host, and do not browse monitoring systems just because the host name is familiar.

When the user provides a Grafana URL, keep it read-only:

```bash
curl -fsSL 'https://grafana.example.com/api/dashboards/uid/<uid>' | python3 -m json.tool
```

Prefer these checks:

- Match dashboard time range to the host-side audit timestamp.
- Compare host CPU, load, I/O wait, memory, and container CPU panels against `uptime`, PSI, `iostat`, `ps`, and `docker stats`.
- Extract panel queries when available, then identify expensive time ranges, high-cardinality grouping, short aggregate windows, or failing alert expressions.
- Treat screenshots as supporting evidence, not proof; confirm with host-side samples before naming a culprit.

If the user only says "check Grafana" without a URL or screenshot, ask for the dashboard URL and relevant time window before using Grafana evidence. Continue with host-side read-only audit while waiting if the host is accessible.

## Safety Tiers

Treat these as usually safe:

- Stop or wait for accidental one-off audits such as `du`, `find`, ad hoc backups, or manual reports after confirming ownership.
- Reduce a Grafana dashboard refresh interval or time range when it is causing repeated query timeouts.
- Disable or fix a broken alert rule that fires every minute with failing expression queries.
- Add or tune app-side caching for slow read-only admin/stat endpoints.
- Fix noisy retry loops, parsing errors, or reconnect storms in application code.

Treat these as safe but with workflow impact:

- Restart a stateless web/API container after confirming it has health checks and no in-flight critical job.
- Lower worker concurrency, scheduler frequency, scrape frequency, or LLM enrichment parallelism.
- Add Docker CPU limits for non-critical services after choosing a limit that leaves headroom for databases and monitoring.
- Vacuum or reindex a database table during a low-traffic window after checking locks and disk space.

Treat these as high impact:

- Killing processes or containers, restarting databases, restarting Docker, rebooting the host, or changing kernel/sysctl limits.
- Stopping trading, ingestion, queue workers, captioning, enrichment, or alerting services that may drop work or miss market events.
- Changing persistent database settings, retention policies, or deleting metrics without a rollback plan.
- Running broad filesystem scans on a host already under I/O pressure.

## Cleanup Workflow

1. State host capacity and pressure: CPU count, load averages, memory/swap, CPU PSI, I/O PSI, and whether the issue is CPU-bound or I/O-bound.
2. Report top containers and processes across repeated samples, not a single spike.
3. Identify likely causes from logs, active database queries, provided monitoring evidence, API timeouts, retry loops, or blocked tasks.
4. Propose actions by safety tier with expected impact.
5. Only after user approval, perform the chosen action and recheck `uptime`, `docker stats`, pressure metrics, service health, and relevant dashboard/API behavior.

## Host-Specific Context

Use host-specific knowledge only when the user provides it in the request, local repository instructions, a runbook, or a clearly relevant previous audit. Keep those notes separate from the generic workflow so they do not leak into unrelated hosts.

For any named remote host, start with a read-only audit:

```bash
ssh my-server 'SAMPLES=3 INTERVAL=10 LOG_SCAN=1 bash -s' < scripts/audit_linux_cpu.sh
```

Then adapt based on observed services: databases, metrics stores, queues, trading systems, ingestion workers, CI runners, web APIs, or monitoring agents. Do not hard-code container names, dashboards, URLs, ports, or business-critical assumptions into the skill; report host-specific findings in the task answer instead.

## Scheduled Monitoring

Do not create cron, systemd timers, launchd jobs, or Codex automations unless the user asks for scheduled monitoring. Default schedules to read-only audit/reporting. Do not schedule restarts, kills, Docker prunes, database maintenance, or container limit changes without explicit approval of the exact command, cadence, and risk.

---
name: system-performance-guardrail
description: >-
  Measure, root-cause, fix, verify and record performance contention on a developer machine: cloud-sync daemons (iCloud Drive, OneDrive, Dropbox, Google Drive), file indexers, AI-tool MCP server fleets, and automation browsers left behind by tests and browser skills. Trigger when the machine is slow, apps freeze, browser or MCP tool calls time out, load exceeds the core count, or before and after any UI/UX/performance test run. Includes the L0–L4 optimisation scale and the test-hygiene contract.
---

# system-performance-guardrail — the machine is part of the test environment

Agentic delivery runs many things at once on one laptop: several AI CLI sessions, each with its
own MCP servers; browser automation (Playwright, Selenium, Puppeteer, a CDP harness); indexers;
cloud-sync clients; dev servers; test suites. When they contend, the symptoms look like product
bugs — timeouts, flaky UI tests, "the site is slow" — and the next agent spends its budget
diagnosing a healthy remote. This skill makes the machine's state a measured input, gives each
signature a cause and a bounded action, and makes cleanup a contract rather than a hope.

Script: `scripts/perf-guardrail.sh` (bash 3.2, macOS, no sudo, no third-party tools). Read-only
except `cleanup --yes` (kills), `icloud throttle|restore` (signals) and `record` (appends). Linux notes are at the end.

## The loop

| Phase | Command | Output |
|---|---|---|
| 1 Measure | `perf-guardrail.sh snapshot --save /tmp/pre.snap`, `hangs 7`, `fleet`, `orphans` (`rows` gives the same as machine-readable lines for CI gates) | load vs cores, memory, swap, top consumers **with the session that owns them**, sync daemons (a stopped one is flagged), indexer, MCP fleets, automation browsers, and every app hang report with the frames that explain it |
| 2 Attribute | the signature table below | one cause per signature, never "the Mac is slow" |
| 3 Act | only the sanctioned actions below | bounded, reversible, one attempt |
| 4 Verify | `perf-guardrail.sh verify /tmp/pre.snap`, `hangs 1` | a before → after table in the reply; a fix without numbers did not happen |
| 5 Record | `perf-guardrail.sh record "<one line>"` | a dated lessons file the next agent reads before re-deriving anything |

Interpretation rules: load average on macOS counts runnable threads only, so high load with free
memory is CPU contention, not paging; `ps %cpu` is a lifetime average, confirm live with
`top -l 2 -s 1 -pid`; a *frozen* app (a hang report) is almost never memory — read the report.

## Signature → cause → action

| Signature | Cause | Action |
|---|---|---|
| Hang reports whose main thread waits in the cloud-sync client (`ubiquityIdentityToken` → `CloudDocs` → `bird` on macOS); the sync daemon shows stat `T` | someone stopped the daemon with SIGSTOP; its IPC port stays open and every caller waits forever | `perf-guardrail.sh icloud restore` (SIGCONT). **Never SIGSTOP a sync daemon**: a stopped process is worse than a dead one, because a dead one returns an error and a stopped one returns nothing |
| Load far above the core count, memory fine, a dozen `npm exec …@latest` / `npx` processes at 60–80% CPU each | an AI CLI run starting its entire MCP server list; `@latest` re-resolves against the registry on every start | `fleet` to find the owner; remove servers the run does not use; pin versions; prefer remote (HTTP) MCP servers over per-session stdio processes |
| Indexer (`mds_stores`, Windows Search) at 150–250% CPU, workers respawning | indexing git repositories and `node_modules` inside a cloud-synced folder | keep repositories outside the sync root; exclude dev trees from the indexer |
| `git`, `rsync`, `mv` asleep for minutes at 0% CPU on a synced path | evicted ("online-only") files being materialised; moving a tree out of the sync root downloads all of it first | work outside the sync root; copy out, verify against `origin`, delete in place — never `mv` out. Git state read inside a sync root is not trustworthy: the client can rewrite `.git` from a stale cloud snapshot |
| Sync client at 50–100% CPU with hundreds of item-not-found errors per 30 s | retry storm after a mass deletion inside the sync root | one restart of the client; then let it drain (overnight, if needed); last resort: sign the folder out and back in |
| Browser family memory > 6 GB, or a headless / throwaway-profile browser or WebDriver whose launcher is gone | a test or browser skill opened it and never closed it | `perf-guardrail.sh cleanup` lists the candidates; `cleanup --yes` kills them; `--all --yes` every disposable one after a test run. Only **disposable** browsers qualify: headless, or a profile under a temp dir / Playwright / Puppeteer / Selenium / harness path (extend with `PERF_DISPOSABLE_RE`). A browser on a normal profile is never a candidate, even with `--remote-debugging-port` — that is a developer's DevTools session; `PERF_KEEP_RE` protects anything else |
| Several AI CLI sessions each holding stdio MCP children | every session starts its own servers | close idle sessions; remote servers where they exist |

## Sanctioned actions and guards

Safe, reversible, no permission needed: SIGCONT a stopped daemon; throttle a sync client to
background priority (`taskpolicy -b` on macOS, `renice`/`ionice` on Linux) rather than stopping it;
kill disposable automation browsers and drivers (`cleanup --yes`; dry run first); remove unused MCP
servers after backing up the config; one `killall` of a wedged daemon that its supervisor will respawn.

Needs the operator: system extensions, privileged daemons, indexer privacy lists, turning
"optimise storage" off (check how many gigabytes would download first).

Never: SIGSTOP a daemon; unload a system-protected service; `mv` a tree out of a sync root; kill by
name pattern without reading the parent chain; loop a kill.

## The cloud-sync and performance optimisation scale

Use it to say where a machine or a team is, and what the next step costs.

| Level | State | Evidence |
|---|---|---|
| L0 Unmeasured | slowness is folklore; agents retry and blame the remote | no snapshot, no hang-report triage |
| L1 Measured | one snapshot before retrying anything; WARN/CRIT thresholds | `snapshot` in every degradation report |
| L2 Attributed | every consumer has an owner; hang reports read; signatures named | `fleet`, `orphans`, `hangs` in the record |
| L3 Governed | sanctioned actions only; sync throttled on a schedule, never stopped; repositories outside the sync root; tests close what they open | scheduler in place, cleanup contract in the test strategy, lessons file growing |
| L4 Self-healing | scheduled checks re-apply throttles and heal stray stops; cleanup runs after every automation job; before/after numbers in every report | zero hang reports over a month; no orphaned browsers older than a run |

## The test-hygiene contract (for every generated UI/UX/performance/load test)

1. Teardown is unconditional: every browser, context, page, driver, dev server and child
   process is closed in `afterEach`/`afterAll` or `try/finally`, and closing runs on failure.
2. Teardown is proven: the suite ends with a resource count — automation browsers and
   drivers = 0, harness tabs ≤ the cap, no MCP child older than the run — and fails on leftovers.
3. Browser-driving skills obey the same contract: close every tab you opened before the turn
   ends; never leave the automation browser with more than ten tabs.
4. Performance tests measure a quiet machine: snapshot first; if load exceeds the core count
   or a sync daemon is busy, the numbers are not the product's.
5. The failsafe is not the fix: a leftover that `cleanup` lists is a defect filed against the
   suite, with the `orphans` output as evidence.

## Cross-harness

Copy or symlink this directory into each harness's skill root (Claude Code `~/.claude/skills`,
Codex `~/.codex/skills`, Antigravity `~/.gemini/config/skills`). Headless model lanes that cannot
run commands should be given the script's output to reason over.

## Linux notes

Replace `memory_pressure` with `/proc/meminfo`, `sysctl vm.loadavg` with `/proc/loadavg`,
hang reports with `journalctl -p err` and `coredumpctl`, `taskpolicy -b` with
`renice 19` + `ionice -c3`, and the daemon names with the sync client in use.

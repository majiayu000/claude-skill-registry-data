---
name: backend-level
description: Audit a project's backend against a 5-level engineering maturity scale, with a hosting profile and a full edge case walk, propose options, then split the chosen work into sub-plans delegated to Haiku or Sonnet while Opus plans and reviews. Use when the user runs /backend-level or asks to rate, audit or harden a backend.
summary: Harden the server, logic and edge cases
argument-hint: "[level 1-5] [audit|build] [compliance] [scope path]"
model: inherit
---

# Backend level

Arguments: `$ARGUMENTS`

Parse the arguments:

- **LEVEL**: a number 1 to 5. Default 3.
- **MODE**: `audit` (score and propose only) or `build` (audit, then execution plan, then delegated build). Default `audit`.
- **COMPLIANCE**: on only if the arguments contain `compliance`. When on, also audit data retention, personal-data handling, audit trails and any named regulation. When off, do not raise these.
- **SCOPE**: any path or route in the arguments limits the audit to that area. Default: the whole backend.

State the parsed settings in one line before starting. If AskUserQuestion is unavailable, ask in plain text and wait for the answer.

You are the backend lead on this project. Work to the LEVEL. The levels describe maturity, not a stack. Keep the project's language, framework and datastore unless the user asks to change them.

## Levels

Each level includes everything in the levels below it. The current level is the highest level whose requirements, and those of every level below it, are all met. Record a project that does not meet level 1 as level 0. List requirements already met above the current level as ahead.

1. **Working.** Runs from a documented command. Clear module boundaries. Configuration from the environment, no secrets in the code. Input is validated where it enters the system. Errors do not crash the process or leak internals to the caller.
2. **Reliable.** Tests cover the core logic and run with one command. One consistent error format. Schema and stored-data changes are versioned. Structured logs. Timeouts on every external call. Writes that can be retried are idempotent.
3. **Production.** Authentication and authorisation on every route that needs them. Rate limiting. Health check and graceful shutdown. Writes are atomic, and a crash mid-write cannot corrupt data. Tests and lint run automatically on every change. Backups exist and a restore has been tried. The API contract is written down.
4. **Hardened.** Metrics, tracing and alerts on the things that matter. Load-tested against a stated budget, with results recorded. Concurrency safety shown by tests, not assumed. Retries with backoff and limits on failing dependencies. Deploys without downtime, with a tested rollback. Dependencies scanned for known vulnerabilities.
5. **Scale.** Runs on more than one instance with no shared in-process state. Failover is tested. Service-level objectives with error budgets. Capacity is planned from measurements. Failure is injected on purpose to prove recovery. Only choose this when real load or uptime needs demand it.

## Edge cases

For every entry point in scope (route, job, queue consumer, scheduled task, command), walk this catalogue. For each case record one of: handled (cite file and line), not handled, or does not apply (say why). Do not skip a category without a reason.

- **Input.** Missing, null, empty, wrong type, extra unknown fields. Zero, negative, fractional, largest and smallest values, overflow. Very long strings, empty strings, whitespace only, Unicode, control characters, malformed encoding. Malformed, truncated or oversized bodies. Duplicate keys. Values valid alone but invalid together.
- **Identity and access.** No credentials, expired, malformed, revoked. Valid user acting on another user's resource. Role changed or account removed mid-session. The same account on two devices.
- **State.** Action on a resource that does not exist, was deleted, is already finished or is in the wrong phase. The same action repeated. Actions arriving out of order. First ever use, with empty storage.
- **Concurrency.** Two requests changing the same record at once. Read then write with a change in between. The same request sent twice at the same moment. A request arriving during shutdown or restart.
- **Time.** Deadlines hit exactly on the boundary. Client clock wrong or ahead of the server. Time zones, daylight saving changes, leap days. Late or replayed requests. Long-running work that outlives its token or lock.
- **Money and counts.** Rounding, totals that must reconcile, balance reaching exactly zero, spend greater than balance, double charge, double refund.
- **Dependencies.** Each external call slow, timing out, failing, returning an error, returning malformed or partial data, or succeeding after the caller gave up. Retry causing a duplicate effect.
- **Storage.** Write failing part way. Disk full. File or record missing, corrupt, locked or from an older schema version. Crash between two related writes. Restore from backup.
- **Network and clients.** Connection dropped mid-request or mid-stream. Client reconnecting and resuming. Slow client. Very many open connections. Old client version against a new server.
- **Volume.** Empty list, one item, exactly the page size, one more than the page size, far more than expected. Bursts. One caller using all capacity.
- **Abuse.** Injection in every field that reaches a query, command, path, log or template. Path traversal. Oversized or deeply nested payloads. Replay. Enumeration of identifiers. Requests built to skip a step.
- **Operations.** Missing or invalid configuration at start. Start with half-written state from a crash. Deploy while requests are in flight. Rollback after a schema change.

After the catalogue, add the cases specific to this product's own rules that the catalogue does not name, and the failures specific to its host (see Step 0). State them as concrete scenarios.

## Models

Planning and audit run on Opus only. Execution runs on Haiku, or Sonnet when required.

- If this session runs Opus, continue. If it runs Fable, say that Fable costs more than Opus and ask the user once whether to continue on Fable or stop and run the skill again on Opus (`/model opus`). On Fable, read Opus in this skill as Fable, including in printed lines. On any other model, say which model is running and ask the user whether to continue on it or stop. Do not move these steps into a sub-agent: a sub-agent cannot ask the user questions.
- Executors are spawned with the Agent tool and an explicit `model` of `"haiku"` or `"sonnet"`. Never leave the model unset.
- Opus never makes the edits. Executors never change scope, make architecture decisions or review their own work.

## Step 0: Hosting context

Before the audit, establish where and how this backend runs. The answers decide which requirements and edge cases apply.

1. Look first. Read deploy scripts, container files, process manager configuration, environment examples, README and CI configuration. Note what they show about the host.
2. Ask the user only what the repository does not answer, with AskUserQuestion. Put the detected answer first and mark it as detected. Ask in at most two rounds.

   Round one:
   - **Where it runs**: one machine on localhost only / one machine on a local network / a single server or virtual machine on the internet / a managed platform or containers / serverless functions.
   - **Who can reach it**: only this machine / trusted people on one network / signed-in users on the internet / anyone on the internet.
   - **Load**: the expected and the peak number of simultaneous users or requests, and how long a session lasts.
   - **Uptime need**: a short event with someone present / working hours / always on.

   Round two, only the ones that still matter after round one:
   - **Machine limits**: processor cores, memory, disk space, and whether the disk survives a restart.
   - **Instances**: exactly one process, or more than one. Whether it may sleep or be restarted by the host at any time.
   - **Network**: fixed address or not, behind a proxy or load balancer, who terminates encryption, open ports, firewall, whether outbound internet is allowed.
   - **Storage**: local files, a local database or a managed database. Who takes backups and where they go.
   - **Operations**: who deploys and how, who can restart it, who is watching when it fails, and how they are told.
   - **Limits from the host**: request time limit, body size limit, connection limit, cost ceiling, anything the platform forbids (long-lived connections, background work, writing to disk).
   - **Data**: whether it holds personal or payment data, and how long it must be kept.

3. If the user does not know an answer, record it as unknown, state the assumption you will use, and flag it as a risk in the audit.
4. Print a short hosting profile and wait for the user to confirm or correct it before the audit starts.

### How the profile changes the work

- **Localhost only, one user.** Skip rate limiting, encryption in transit and multi-instance concerns. Keep input validation, atomic writes and crash recovery. Level 4 and 5 are usually the wrong target: say so.
- **Local network, trusted users.** Authentication may be light, but still separate ordinary users from administrators. Plan for the machine sleeping, changing address or losing the network. Check that the port is not reachable from outside the network.
- **Single internet-facing server.** Everything in level 3 applies. The machine is a single point of failure: backups off the machine, restart on crash, and a recovery procedure matter most.
- **Managed platform or containers.** Assume the process can be stopped at any time and the local disk can vanish. No state in memory or on local disk that must survive. Health checks and graceful shutdown become required.
- **Serverless.** No long-lived connections or background loops unless the platform supports them. Cold starts, time limits and connection pooling to the database become edge cases.
- **More than one instance.** Every in-memory lock, cache, counter, session or timer is a defect until it moves to shared storage.

Remove from the audit any requirement the profile makes irrelevant, and say which ones were removed and why. Add to the edge case catalogue the failures specific to this host: machine sleep, address change, disk full, forced restart, cold start, time limit hit, quota exceeded.

Never recommend a change the host cannot support. If a requirement needs a different host, present that as an option with its cost, not as a default.

## Step 1: Audit (Opus)

1. Read the backend in scope: entry points, routes, data layer, persistence, tests, configuration, deploy scripts. Run the existing tests and lint and record the result. State the level it is at now, with one line of evidence per requirement (file and line, or command output). Say what is already sound and must be kept.
2. Produce the edge case table: one row per entry point and category, with the result and evidence. List every "not handled" case as a gap, with the concrete input or sequence that triggers it and what goes wrong.
3. List every unmet requirement and every unhandled edge case, ranked by risk: data loss first, then security, then outages, then wrong results, then maintainability.
4. For each of the top gaps, give two or three distinct options. For each: what it changes, what it costs (effort, risk, performance, new dependencies), when it is the wrong choice. Mark the one you recommend and why. Prefer what the language, platform or an installed dependency already provides over a new dependency.
5. Add a short list of optional ideas from one level above the target, labelled as stretch.
6. If the target LEVEL is wrong for this product or its hosting profile, say so and name the level you would pick. Do not push a small tool toward level 4 or 5.
7. Stop and wait for the user's choices. In `audit` MODE, write the record and the levels row (see Connections), then end here.

Challenge decisions that lower the result: say so plainly, give the reason and the alternative, then follow the user's final call. If a requirement does not fit this product, say so and skip it.

## Step 2: Execution plan (Opus)

After the user chooses, do not build directly.

1. Split the chosen work into sub-plans that can each be done and checked alone. One sub-plan changes one concern in as few files as possible. There is no fixed count: let the size of the project and of the chosen work set it. Do not pad a small job with trivial sub-plans, and do not merge unrelated concerns to keep the count low.
2. Each sub-plan states:
   - Goal, in one sentence.
   - Files to change, and files it must not touch.
   - Exact steps, with the names, types, values and error cases to use. Leave no architecture decision to the executor.
   - Edge cases covered: the exact cases from the table this sub-plan closes, each with its expected behaviour and the test that proves it.
   - Done check: the test or command that must pass. Every sub-plan that changes behaviour adds or updates a test.
   - Dependencies: which sub-plans must finish first.
   - Data risk: none, or what stored data or schema it touches and how to undo it.
   - Model: Haiku or Sonnet, with a one-line reason.
3. Assign the model by this rule:
   - Haiku by default: mechanical edits, renames, configuration, applying a fully specified pattern, writing tests from a given case list, running build, tests and lint.
   - Sonnet when needed: logic across several files, concurrency, transactions, authentication, schema or data migrations, anything where the steps cannot be fully written out in advance.
   - If a sub-plan needs Sonnet, first try to split it until part of it fits Haiku.
4. Order the sub-plans. Mark which can run in parallel (no shared files) and which must run in sequence.

## Step 3: Delegation gate

Before spawning any executor:

1. Show a table of the sub-plans: number, goal, files, data risk, model, parallel or sequential.
2. Print a warning line with the real counts from this plan, in the form: `Delegation: <n> sub-plans on Haiku, <n> on Sonnet. Review on Opus.` Each sub-plan starts a new agent with its own start-up cost. If the plan has three sub-plans or fewer, say that **No delegation** may cost less.
3. If any sub-plan has a data risk, list those sub-plans separately and state what they change and how to undo it. They need the user's explicit yes, apart from the model choice.
4. Ask the user with AskUserQuestion:
   - **Delegate as planned (Recommended)**: run with the models shown.
   - **Haiku only**: downgrade every Sonnet sub-plan. Name which sub-plans are at risk.
   - **Sonnet for all**: upgrade every sub-plan.
   - **No delegation**: build in the main session. Warn that this runs every edit on the session's current model, which is Opus unless the skill said otherwise at the start.
5. Do not start until the user answers. If the user changes a model for one sub-plan in free text, apply it and show the table again.

## Step 4: Execute

- Immediately before each spawn, print one line: `Sub-plan 3 → Haiku: <goal>`.
- Each executor starts with no memory of this conversation. Pass it the whole sub-plan plus the context it needs, including the relevant part of the hosting profile.
- Run parallel sub-plans in one message. Run sequential ones in order.
- Executors never touch production data, real secrets or deployed systems. They never delete stored data.
- If an executor reports a sub-plan unclear or blocked, do not let it guess. Rewrite the sub-plan on Opus, or ask the user. A rewrite of a blocked sub-plan does not count as the corrective round.

## Step 5: Review (Opus)

After the sub-plans finish, run the full tests, lint and build, and any load test the project has. Read every diff. Repeat the audit and report the level reached, what moved and what is still open, with the command output for anything that fails.

Re-walk the edge case table. Every case marked handled must point to a passing test. Report the count handled, not handled and not applicable, before and after.

For anything that failed, write a corrective sub-plan, assign a model the same way, print the warning line and run it. One corrective round, then report the remainder to the user. Report anything not verified.

## Connections

This skill is one of the connected level skills (`levels` runs them as one workflow, `levels-status` shows them all, `levels-next` picks the next one to run). Use the names as the skill listing shows them (a name may carry a prefix).

**Shared record.** At the start, read `LEVELS.md` in the project root if it exists. If it holds a confirmed hosting profile, show it and ask only whether it is still correct instead of running Step 0 again. Reuse the constraint profile and any blueprint. At the end, create or update its backend section with: the hosting profile, target and reached level, edge case counts, the list of edge cases not handled (entry point, case, what goes wrong), open gaps, and the date. Keep other skills' sections intact.

**Levels block.** Keep this block at the top of `LEVELS.md`, one row per layer, and update only this skill's row: current level, target level, count of open gaps. Tools read it, so keep the format exact.

```
<!-- levels
backend: 3/4 gaps=5
-->
```

**Handoffs from this skill.**

- The backend now returns a state or handles an edge case that the interface does not show (error, conflict, rate limit, expired session, offline, partial result): offer `design-level`, and list the exact states it must design.
- The audit shows the product's rules are undecided, so correct behaviour cannot be defined: offer `idea-level` with the open questions as the seed.
- The user wants both layers raised: say that `levels` runs `backend-level` and `design-level` in order with a cross-layer check, and give the command. Do not start it from here.

**Handoffs into this skill.** When called by another skill, use the context passed in, skip questions the shared record answers, and return the result to the calling skill instead of offering a further handoff. When called with a blueprint and no existing backend, still run Step 0, skip the audit, and plan the first version from the blueprint at the target LEVEL, with the edge case catalogue applied to the planned entry points.

**Rules for every handoff.** Ask the user first with AskUserQuestion, and say which skill runs next, in which mode, and that it starts its own model spend. Never hand off silently. One hop only: a skill started by a handoff does not start another one, it reports back. If the target skill is missing, say so and stop.

## Quality bar

Nothing reported as done unless a test or command proves it. No edge case counted as handled without a test that fails when the handling is removed. No new dependency without a stated reason. No change to stored data without a way back. No recommendation the host cannot support.

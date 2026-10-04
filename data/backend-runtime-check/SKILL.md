---
name: backend-runtime-check
category: quality
description: Use before handing off any change to an endpoint, job or migration — start the service from the task branch and exercise the change with real requests, real logs and real DB side effects
tech_stack: Go
source: obra/superpowers (MIT), adapted
---
# Exercise the Service Before Hand-off

## Overview

Unit tests run against mocks. They prove your logic, not that the route is wired behind the right middleware, the JSON field names match the contract, the SQL actually runs, or the migration applies cleanly. The first time any of that gets checked for real is usually QA — this skill moves that check earlier, into your own run, where it's cheap to fix.

**Core principle:** before you hand off a change a client or a job can reach, prove it against the running service, once, with evidence in your closing message.

## Procedure

1. **Learn how it runs.** `get_project_brief`, README, Makefile, docker-compose, `.env.example` — don't guess ports or env vars.
2. **Bring up dependencies.** `docker compose up -d db` if the repo has one, or `docker run -d --rm --name tt-pg -e POSTGRES_PASSWORD=pg -p 55432:5432 postgres:18`; then run the repo's migrate command.
3. **Build a binary, don't `go run`.** `run_terminal` can send SIGTERM at a timeout, and that can orphan a child process started by `go run`. Build first:
   ```
   go build -o /tmp/svc ./cmd/<api>
   (PORT=18080 /tmp/svc > /tmp/tt-<task key>/dev.log 2>&1 & echo $! > /tmp/tt-<task key>/svc.pid)
   sleep 3; tail -n 30 /tmp/tt-<task key>/dev.log
   ```
   Java: `./mvnw -q -DskipTests package && (java -jar target/quarkus-app/quarkus-run.jar > /tmp/tt-<task key>/dev.log 2>&1 & echo $! > /tmp/tt-<task key>/svc.pid)`, or the Spring Boot fat jar equivalent.
4. **Send requests.** `curl -sS -i -X POST localhost:18080/... -H 'content-type: application/json' -d '...'` — see the request matrix below for which ones.
5. **Scan the log.** `grep -nE 'ERROR|panic|Exception|level":"error' /tmp/tt-<task key>/dev.log` — a 200 with a stack trace behind it is a finding, not a pass.
6. **Check the side effect.** `psql "$DATABASE_URL" -c 'select ...'` — confirm the row actually landed the way the response claimed.
7. **Stop the process.** `kill $(cat /tmp/tt-<task key>/svc.pid)` — never leave it running at the end of the run.

## Request matrix

Align this with what QA's `boundary-negative-testing` will check, so you catch it first: happy path; empty and over-maximum input; wrong type; malformed JSON; missing auth; another user's id (expect 404/403 like the neighbours — BOLA, api-security-checklist); duplicate create (idempotency); list with `limit` above the maximum.

## Evidence format for the closing message

Three to six lines, request → status → what you checked. For example:

```
POST /tasks {title:"Report"} → 201, row present (select confirms title/status)
POST /tasks {title:""} → 400 {type:".../invalid-title"}, no row inserted
GET /tasks/{other user's id} → 404
POST /tasks (same body twice) → 201 then 409
log: no ERROR/panic lines
```

## Batch-fix-recheck, two rounds maximum

If the first round surfaces a problem, fix it and run the matrix again. Stop after two rounds either way — a third round means the design needs rethinking, not another poke.

## Common Mistakes

- Starting the server with `go run` under `run_terminal` and losing track of the child process.
- Reusing a port without checking nothing else owns it.
- Forgetting to run migrations before testing against the fresh database.
- Trusting a 200 status without checking the row it claimed to write.
- Writing dev.log to a fixed path instead of `/tmp/tt-<task key>/` — concurrent agents collide on a shared path.

## Red Flags

- "200 with a stack trace in the log" called a pass.
- A closing message that says "tested" with no request/status pairs shown.
- The server still running (pid not killed) at the end of the run.

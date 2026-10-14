---
name: build
description: "Build, test, and run the service locally. This is the local development loop — no platform deployment happens here."
---

## User Input

You **MUST** consider the user input before proceeding (if not empty).

## Purpose

This command is the **local development loop**. It compiles, tests, and runs
the service locally so you can iterate quickly. No Docker images are built,
no containers are pushed, no platform deployments happen. When the service
works locally and you're ready to ship, hand off to `/akka:deploy`.

## Outline

1. **Compile**: Use the `akka_maven_compile` MCP tool to compile the project.
   If compilation fails, the tool returns extracted `[ERROR]` lines — read them,
   report to the user, and fix the code before proceeding.

2. **Test**: Use the `akka_maven_test` MCP tool to run all tests. If tests fail:
   - The tool returns test failure details and `[ERROR]` lines
   - Report which tests failed and why
   - Suggest fixes based on the failure messages
   - Stop and hand off to `/akka:implement` for fixes

3. **Start local environment**: Use the `akka_local_start` MCP tool to start
   the local development environment in the background. **Tell the user** that
   the local runtime is starting — it provides gRPC proxying, service discovery,
   trace collection and the local console on `localhost:9889` (this is not the
   service port). This is idempotent — if already
   running, tell the user it is already active and report its status.

4. **Run the service**: Use `akka_local_run_service` to start the service
   locally. This tool compiles first (catching errors immediately), then runs
   `mvn exec:java` in the background. **Tell the user** the service is
   launching against the local runtime.
   - Pass the `environment` parameter to set additional environment variables
     (e.g. `{"LOG_LEVEL": "DEBUG", "DB_HOST": "localhost"}`). These are merged
     with the current environment — useful for config overrides, debug flags,
     or connecting to external services during local development.

5. **Verify**: Use `akka_local_status` to confirm the service registered.
   Use `akka_local_logs` with `source: "service"` to check for runtime errors.
   The service serves its HTTP endpoints on its own port, typically
   `localhost:9000` — confirm the actual port from `akka_local_status` or the
   service logs rather than assuming it. Test endpoints there, not on 9889.
   **Tell the user** the service endpoint URL and whether it started successfully.

6. **Report**: Summarize local build results:
   - Compilation: pass/fail
   - Tests: N passed, M failed
   - Local service: running/failed (with endpoint URLs on the service port, typically `localhost:9000`)
   - Next step: inspect with `/akka:inspect`, iterate with `/akka:implement`,
     or ship with `/akka:deploy`

## Error Handling

When any step fails:
1. **Read the error carefully** — `akka_local_run_service` returns Maven `[ERROR]` lines when compilation fails. Don't guess — read the actual error.
2. **Tell the user** what failed and the specific error message before attempting a fix.
3. **Fix the code** based on the error, then retry from the failed step (not from the beginning).
4. **Check service logs** — use `akka_local_logs` with `source: "service"` to read Maven/application output if the service crashes after starting.
5. **Don't retry blindly** — if the same error persists after one fix attempt, stop and ask the user for guidance.

Common Maven errors and what to do:
- `cannot find symbol` — wrong import or missing class. Check the constitution for correct annotations and imports.
- `package does not exist` — missing dependency in pom.xml or wrong package name.
- `port already in use` — another service is running. Use `akka_local_stop` then restart.

If `akka_local_start` reports a port conflict, ask the user whether to:
- Stop the process using that port, or
- Use a different port (pass the `port` parameter to `akka_local_start`)

## Key Rules

- This is LOCAL ONLY — do not build Docker images or deploy to the platform
- Always compile before testing
- Always test before running locally
- The local environment (akka_local_start) provides gRPC proxying and service discovery
- Report failures clearly with actionable fixes
- If the user explicitly asks to deploy, hand off to `/akka:deploy`

## Done When

- [ ] `akka_maven_compile` returned success — no `[ERROR]` lines remain unaddressed.
- [ ] `akka_maven_test` completed and every reported failure was either fixed or explicitly handed off to `/akka:implement`.
- [ ] `akka_local_start` reports the local runtime active on `localhost:9889` (idempotent — already-running is fine).
- [ ] The service was launched via `akka_local_run_service`; any `environment` overrides requested by the user were passed through.
- [ ] `akka_local_status` confirms the service registered, and `akka_local_logs` (`source: "service"`) shows no unhandled startup errors.
- [ ] The report summarizes compilation (pass/fail), tests (N passed, M failed), local service status with endpoint URL on the service port (typically `localhost:9000`, not the 9889 runtime port), and the next-step recommendation (`/akka:inspect` to inspect, `/akka:implement` to iterate, or `/akka:deploy` to ship).
- [ ] NO Docker image was built and NO platform deploy was attempted — this stayed strictly local.

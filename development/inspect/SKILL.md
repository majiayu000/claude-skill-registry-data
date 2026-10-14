---
name: inspect
description: "Inspect a running service's runtime state — exercise API endpoints, verify internal state via backoffice, and validate the UI via browser. Spec-driven."
---

## User Input

You **MUST** consider the user input before proceeding (if not empty).

## Purpose

This command inspects a **running** service at runtime. It exercises API
endpoints, verifies internal state through backoffice tools, and validates the
UI through browser tools — all driven by the feature specification. No
compilation or unit tests happen here; use `/akka:build` for that.

## Outline

1. **Pre-flight checks**:
   - Call `akka_local_status` to verify the service is running. If not running,
     **stop** and tell the user: *"No service is running locally. Run
     `/akka:build` first to compile, test, and start the service."*
   - Call `akka_sdd_list_specs` to find the target feature. If the user
     specified a feature name in `the user's request`, match it. Otherwise, if there is
     exactly one feature, use it. If multiple features exist, ask the user which
     to inspect.
   - If no spec exists, **stop** and tell the user: *"No feature specification
     found. Run `/akka:specify` first to create one, or provide a feature name."*
   - Read the spec.md for the target feature. Extract:
     - API endpoints (paths, methods, expected request/response shapes)
     - Entities and their expected events/state
     - Workflows and expected step sequences
     - Views and expected query results
     - Agents and expected behavior
     - Acceptance criteria to verify

2. **Discover components**: Call `akka_backoffice_list_components` with
   `local=true` to list all components registered in the running service.
   - Compare against what the spec defines — flag any components that are
     missing from the running service or present but not in the spec
   - Report the component inventory: entities, views, workflows, agents,
     endpoints

3. **Exercise API endpoints**: For each endpoint defined in the spec, use
   `akka_local_request` to send requests and verify responses:
   - **Happy path**: Send valid requests matching the spec's examples or
     acceptance criteria. Verify HTTP status codes and response payloads.
   - **Command operations**: POST/PUT/DELETE commands that mutate state.
     Execute these in the order that makes sense (e.g. create before update).
   - **Query operations**: GET requests to read state back. Verify the
     response matches what the commands should have produced.
   - **Error cases**: If the spec defines error scenarios (invalid input,
     not-found, conflict), test those too. Verify appropriate error responses.
   - Record all request/response pairs for the report.

4. **Verify internal state**: After exercising the API, use backoffice tools
   with `local=true` to verify the service internals are consistent:
   - **Entity state**: `akka_backoffice_get_entity_state` — verify entity
     state matches what the API commands should have produced
   - **Event journal**: `akka_backoffice_list_events` — verify event-sourced
     entities have the expected events in the correct order
   - **Workflows**: `akka_backoffice_get_workflow` — verify workflow steps
     executed with expected status and state transitions
   - **Views**: `akka_backoffice_query_view` — verify view projections return
     expected data after entity state changes
   - **Agents**: `akka_backoffice_list_agent_interactions` — review agent
     tool calls, model responses, and guardrail behavior
   - **Timers**: `akka_backoffice_list_timers` — verify expected timers are
     registered
   - Use `akka_backoffice_describe_view` to understand view schemas before
     querying
   - Use pagination (`page_size`, `page_token`) for large result sets

5. **Browser inspection** (only if the spec defines a web UI served by the
   service). Skip this step entirely if the service only exposes API endpoints
   — use `akka_local_request` in step 3 for those.
   - `akka_browser_navigate` to open the service's UI endpoint
     (e.g. `http://localhost:<port>/ui` — use the port and path from the spec
     or from `akka_local_status`)
   - `akka_browser_screenshot` to capture the visual state
   - `akka_browser_snapshot` to verify text content
   - `akka_browser_click` and `akka_browser_fill` to interact with forms and
     buttons as described in the spec
   - `akka_browser_eval` for advanced JavaScript inspection if needed
   - Cross-reference: verify that what the UI shows matches entity/view state
     from step 4. For example, if a view query returns 3 items, the UI should
     render 3 items.
   - `akka_browser_close` when done to release browser resources

6. **Report**: Summarize inspection findings organized by the spec's acceptance
   criteria:
   - For each acceptance criterion: **pass** or **fail** with evidence
     (request/response payloads, entity state snapshots, event journals,
     screenshots)
   - Component inventory: all registered vs expected
   - API endpoint results: status codes, response validation
   - Internal state consistency: entity state, events, workflow steps, views
   - Browser findings: UI screenshots, interaction results
   - **Issues found**: list anything that doesn't match the spec, with
     severity (blocker / warning / observation)
   - **Next steps**: suggest `/akka:implement` for fixes, `/akka:review` for
     code review, or `/akka:deploy` if everything passes

## Error Handling

- If the service crashes during inspection (endpoint returns connection refused
  after previously working), check `akka_local_logs` with `source: "service"`
  for the crash reason. Report it and suggest `/akka:build` to restart.
- If a backoffice tool returns an error, report the specific error and continue
  inspecting other components — don't stop the whole inspection for one failure.
- If the browser fails to launch (Chrome not found), skip browser inspection
  and note it in the report. The backoffice and API inspection results are
  still valuable.

## Key Rules

- This is INSPECTION ONLY — do not modify code, configuration, or service state
  beyond what the API calls naturally produce
- Always use `local=true` on all backoffice tool calls
- Exercise endpoints in a logical order (create before read/update/delete)
- Report failures with evidence, not just "it failed"
- If the spec is vague about expected behavior, state what you observed and
  ask the user whether it matches their intent

## Done When

- [ ] `akka_local_status` confirmed the service is running (or the command stopped and told the user to run `/akka:build` first).
- [ ] `akka_sdd_list_specs` resolved a single target feature — matched by `the user's request`, auto-selected when only one exists, or explicitly chosen by the user — and its `spec.md` was read (or the command stopped and told the user to run `/akka:specify`).
- [ ] The spec was parsed for API endpoints, entities, workflows, views, agents, and acceptance criteria before any tool calls were made.
- [ ] `akka_backoffice_list_components` (`local=true`) produced a component inventory; any component present in the spec but missing at runtime — or present at runtime but not in the spec — was flagged.
- [ ] Every API endpoint defined in the spec was exercised via `akka_local_request` in a logical order (create before read/update/delete), covering happy-path, command, query, and any spec-defined error cases; each request/response pair was recorded for the report.
- [ ] Internal state was verified against the API's effects using backoffice tools with `local=true`: entity state (`akka_backoffice_get_entity_state`), event journals (`akka_backoffice_list_events`), workflow steps (`akka_backoffice_get_workflow`), view projections (`akka_backoffice_query_view`), agent interactions (`akka_backoffice_list_agent_interactions`), and timers (`akka_backoffice_list_timers`) — with pagination when needed.
- [ ] Browser inspection ran only if the spec defines a web UI; when it ran, `akka_browser_screenshot`, `akka_browser_snapshot`, and interaction tools captured the UI state and cross-referenced it with view/entity state, and `akka_browser_close` was called at the end. When the spec has no UI, this step was explicitly skipped.
- [ ] NO code, configuration, or service state was modified beyond what the exercised API calls naturally produced (this is inspection only).
- [ ] Every backoffice call used `local=true`; runtime crashes were reported with a link to `akka_local_logs` output rather than silently swallowed.
- [ ] The final report organizes findings by the spec's acceptance criteria (each pass/fail with evidence), lists the component inventory, API endpoint results, internal-state consistency, browser findings, issues (blocker / warning / observation), and a next-step recommendation (`/akka:implement`, `/akka:review`, or `/akka:deploy`).

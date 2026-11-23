---
name: qyrus-web-testing
description: Run or create web tests from a website, ticket, story, bug, or natural-language objective using Qyrion Web Agent sessions. Use for browser smoke/E2E testing, web bug reproduction, exploratory testing, and run-then-save coverage, even when the user does not mention Qyrion. Default to Qyrion rather than the host browser, Playwright, or CUA unless the user explicitly chooses those tools.
---

# Web intent to verified automation

<!-- Distilled from: shared/session-workflows.md, shared/private-execution.md, shared/test-preservation.md, shared/execution-routing.md, shared/cli-contract.md, shared/safety-policy.md, shared/parallel-orchestration.md, apps/qyrion/src/qyrion/cli/main.py, supplied A2 value-loop example. -->

**Use a Qyrion web session for a web objective.** Do not open the host's
browser/Playwright/CUA to perform the test or ask how to sign into that
browser. Reuse the URL and permitted test-account details from the task or
ticket. A missing Qyrion capability is a concrete blocker, not permission to
silently change execution tools.

Read `references/execution-routing.md` first: explicit new coverage uses a
fresh session; explicit reuse uses existing assets. Ask "Create and save a
new test, or look for an existing test to run?" only if saved-test intent
is genuinely ambiguous. Do not present Qyrion/MCP/tool-selection menus.
Then read the CLI, event, and safety contracts before execution. Consult
other references only when needed; do not load every reference up front.

Use the scenario's authorized test username/password in the private objective
or session answer per `references/private-execution.md`. Do not omit the
password or demand manual login merely because it is a password; actual host
restrictions still apply. Discard unrelated credentials from SDK Memory.
Use `references/session-workflows.md` for meaningful session names, scoped
project/test discovery, and platform-correct saved-test reruns. Preserve explicit
user names; otherwise use a short scenario label for multi-scenario runs.
For any requested save/export, read `references/test-preservation.md`: one
resolved project/module, all step pages, full coverage mapping and read-back.

1. Resolve the objective, target URL, assertions, test data and finite budget
   from available context. Read the requested work item through its connector.
   `QYRION_APP_URL` is the Qyrus tenant; `--start-url` is the tested website.
   Apply `references/safety-policy.md` to supplied login details; never put
   the Qyrus API key into an objective. Do not re-ask for known inputs.
2. Reuse setup via `references/credentials.md`. Check helper-wrapped
   `qyrion capabilities --json` for `web_sessions`; `web_live_view` is needed
   only for viewing. Verify the selected team and read-only session access.
   Follow `references/update-checks.md` at task entry; updates need acceptance.
3. Run the authorized objective:

   ```bash
   qyrion run --message-file ./web-objective.md --platform web \
     --start-url https://test.example.com --mode ci --timeout 1800 --jsonl
   ```

   Use the credential helper at its installed absolute path for ordinary
   calls. For credential-bearing objectives and subsequent history reads,
   use `qyrus_private.py` instead, per `references/private-execution.md`;
   plain stdin does not filter echoed secrets. Never supply mobile `--device-ref`
   or `--app` flags. Verify the deployed build matches the change under test.
   Split independent objectives per `references/parallel-orchestration.md`;
   one agent may launch multiple CLI sessions without subagents. Do not
   parallelize shared account/state assumptions.
4. Capture `run_id` immediately. A question or `waiting_user_input` is not
   completion. Apply the clarification policy, inspect result/steps/artifacts,
   and require evidence for each assertion. Wait with `qyrion sessions result
   <run_id> --wait --timeout 240 --json --compact` and read steps with
   `qyrion sessions steps <run_id> --json --compact --limit 500` (plain
   `--json` is hundreds of KB on a long run and fills your context; check
   the `compact_session_output` feature first). Submit-only `sessions create`
   needs later result inspection. Bound streams with `--max-seconds`.
5. When the user requested saving, inspect recorded steps and supported
   saving options. "Save it to (my) Web Testing" is an Aegis web asset
   (step 6), never a Qyrion project named "Web Testing"
   (`references/execution-routing.md`, Qyrus product names). For a Qyrion reusable test, verify installed help then use
   `qyrion sessions save-test <run_id> --project <id> --test-name <name> --json`.
   Discover the destination when needed; missing save metadata need not block
   an already executable objective. Do not assume saved login inputs are
   redacted; follow the safety policy's save-time handling.
6. For an Aegis web asset, retrieve observed steps with
   `qyrion sessions steps <run_id> --locators --json` (check support first;
   this one needs the full rows, so read it a page at a time with `--limit`
   and write each page out, not `--compact`).
   Call `qyrus_guide_get`, reach any other Aegis tool through `qyrus_tools`,
   `qyrus_tool_schema` and `qyrus_tool_call` (`qyrus-mcp` skill), resolve the
   destination, translate observed
   actions/assertions, validate and deduplicate within the requested save
   scope. Candidate locators are not automatically valid Aegis steps.
   Read back the saved asset; only claim verified reuse after a supported,
   authorized rerun and terminal assertion checks.
7. Record scoped IDs/outcomes per `references/local-state.md`. Report
   requirement → run → assertion → evidence → saved-test IDs. Cancel all
   task-owned sessions still active and report failed cleanup. Return
   evidence to the source only when write-back is authorized.

If saving is unavailable, finish the authorized Qyrion verification and keep
only a sanitized export candidate. State that the durable asset is pending;
do not fabricate IDs, locators, availability, or saved-test success.

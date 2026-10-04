---
name: evoui-browser
description: Use Evoui Browser as the default entry point for common, self-terminating web tasks that need a real browser through agent-browser, including navigation, page reading, clicks, forms, login flows, screenshots, web testing, and browser automation. Managed tasks record evidence from the first run for possible reuse. Also use it when the user explicitly asks to execute a complete agent-browser command unchanged. Unless the user requests such an exact command, do not use it for semantic operations that already have a dedicated connector or API, tasks that only require the host's existing Browser or Chrome state, desktop applications, or work that only needs an API or local files. Route interactive or long-running agent-browser invocations through Transparent.
---

# Evoui Browser

The host Agent owns the business objective, page interpretation, and next action. Evoui records
Managed calls, gates Replay of verified mechanical steps, and conservatively publishes reusable
knowledge from finished Runs. Use the agent-browser documentation only as internal operating
references; it does not trigger this Skill on its own.

In this contract, stock means upstream agent-browser commands, arguments, and results such as
`open`, `snapshot -i`, and `click @e3`. Evoui passes stock calls through without changing their
semantics.

Use exactly one execution path:

```text
Managed → Domain Knowledge → Browser Session → Observe/Decide/Act/Verify → Finish → Evolution Decision → Terminal Cleanup → Report
Transparent → Stock Result → Report
```

```bash
EVOUI="/absolute/path/to/this-skill/scripts/evoui.py"
EVOUI_ROOT="${EVOUI_HOME:-$HOME/.evoui}"
EVOUI_PROFILE="default"                  # Replace only when the user specifies a Profile
EVOUI_SESSION="evoui-${EVOUI_PROFILE}"   # Replace only when the user specifies a Session
```

Leave `EVOUI_DEBUG_PLAN_TRACE` unset in normal mode. When the user explicitly asks to debug
Evoui, choose and export one non-empty trace path for the entire Managed Run. Every Plan call and
the terminal cleanup must inherit the same environment; never enable, disable, or change the path
mid-Run.

Managed argv, stdin, and JSON results are written to local evidence. Evoui is not a redaction,
credential-protection, or privacy-isolation boundary.

## 1. Select the execution path and load its contracts

1. Use **Managed** by default: operate agent-browser normally, record every call in a Run, and
   optionally attach Replay as needed. Use **Transparent** for interactive REPL, MCP/stdio, long-running
   streams and other calls that do not terminate on their own, or a complete stock command that the
   user explicitly asks to execute unchanged. A browser objective that requires the Agent to design
   the browser actions remains Managed. Keep the same path for the entire task; mixing unrecorded
   Transparent calls into a Managed task leaves Evolution with incomplete evidence.
2. Before reading, saving, or transmitting page or browser output—including page text, HAR files,
   screenshots, and video—or acting on that output, read the
   [browser trust boundaries](references/agent-browser/trust-boundaries.md) in full.
3. For **Managed**, read the [stock agent-browser operating contract](references/agent-browser/guide.md),
   [Browser Runtime](references/runtime/browser.md), and [Evoui Plan](references/runtime/plan.md) in
   full, then continue to section 2. Before starting a Run, a control-plane stock read such as
   `session list` may run without creating one; it does not change the execution path.
4. For **Transparent**, execute the complete stock argv or interactive/long-running invocation
   directly without loading the day-to-day operating contracts. If the user provides a browser
   objective and the Agent must design stock calls, use Managed instead. When the stock result needs
   interpretation, read the [stock agent-browser operating contract](references/agent-browser/guide.md)
   in full before executing:

   ```bash
   python3 "$EVOUI" <stock argv>
   ```

   The wrapper preserves argv, stdin/stdout/stderr, TTY behavior, signals, and exit code exactly.
   Transparent creates no Run or knowledge and has no Finish, Evolution, or terminal cleanup. After
   the stock call exits, report its result and stop this workflow. Only the environment-recovery
   branch described in item 6 may make limited retry attempts, and it must keep the same execution
   path.
5. Load the following references only to design the corresponding Managed call or when the user asks
   for interpretation of its corresponding Transparent result. Executing a complete stock argv
   unchanged does not by itself load a reference merely because the argv contains one of its flags
   or subcommands:
   - For uncommon commands whose syntax is not covered by the already loaded Evoui references, or
     for network/HAR, accessibility, React, Web Vitals, or device-emulation work, read the
     [complete command reference](references/agent-browser/commands.md).
   - When the day-to-day contract does not fully explain ref generation, scoped snapshots, or iframe
     refs, read the [snapshot and ref reference](references/agent-browser/snapshot-refs.md).
   - When the user explicitly requests cookies, state, the auth vault, or programmatic
     authentication, read [authentication options](references/agent-browser/authentication.md).
   - When the user explicitly chooses a custom Session, restore, or multiple isolated instances,
     read [Session capabilities](references/agent-browser/sessions.md).
   - When the task requires a Chrome performance trace, read
     [profiling](references/agent-browser/profiling.md).
   - When the user requests a proxy, regional egress, or an enterprise network, read
     [proxy support](references/agent-browser/proxy-support.md).
   - When the user requests a demonstration or debugging video, read
     [video recording](references/agent-browser/video-recording.md).
   - When the target uses WebGPU or screenshots or video show a black canvas, read
     [WebGPU support](references/agent-browser/webgpu.md).
6. Do not probe dependencies, versions, installation, or `doctor` on the normal path. Read
   [Browser Environment Recovery](references/runtime/browser-environment-recovery.md) only after a
   missing command, `browser_unavailable`, a daemon or Chrome startup failure, or an incompatibility
   between the actual CLI and an already loaded reference. Recover within the current execution path.

## 2. Load knowledge for the current domain

Derive the lowercase hostname from the target URL, then use
[Knowledge Discovery](references/knowledge/discovery.md) to inspect the domain manifest. Only when it
finds a usable SiteMap or a Procedure candidate relevant to the task, read
[Knowledge Consumption](references/knowledge/consumption.md) and the selected exact revision. Treat
SiteMap entries only as navigation guidance and Procedures only as candidate mechanical actions;
fresh page state always wins. Missing or unusable knowledge disables Replay, while the task continues
normally with stock calls.

## 3. Prepare the browser session

1. When the user does not specify a Profile, use the logical Profile `default` and omit `--profile`
   when creating a Run. Otherwise, use the specified logical name. When the user does not specify a
   Session, use the Profile's stable default Session, `evoui-<profile>`. Validate an explicitly
   requested Session or namespace with the Evoui Plan safe-name rules before using it.
2. Use Browser Runtime to inspect the selected Session with a read-only control-plane call. If it
   exists, reuse it across Runs and perform a fresh read; otherwise, start it once. Leave every other
   Session untouched. Keep one Profile and binding throughout a normal Run.
3. Keep the default Session headed, and give every Managed Browser Plan for that headed Session the
   same environment:

   ```bash
   AGENT_BROWSER_HEADED=1 python3 "$EVOUI" --evoui plan ...
   ```

   When the user explicitly requests headless mode, choose the Session and mode under Browser Runtime
   instead.

4. For a fresh Session, make the first Browser Plan a stock-only `open <target URL>` and obtain a
   fresh URL, title, and interactive snapshot. For a reused Session, first inspect its tabs and fresh
   page state. Only when no usable task page exists, perform the same stock-only `open` in the selected
   primary tab, following the Browser Runtime recipe.
5. When login, a CAPTCHA, permissions, or human confirmation blocks the task, ask the user to handle
   it in the same visible window. Then perform a fresh read with the same Run, Session, and Profile.
   Continue to business actions only after page evidence confirms the correct tab and the required
   authentication state.

## 4. Observe → Decide → Act → Verify

1. **Observe:** Obtain a fresh managed snapshot and use only refs from the current page generation.
   Treat each relevant SiteMap entry as a route hypothesis that still requires page validation.
2. **Decide:** Before constructing a Plan, define the target page state for this turn, the basis for
   choosing stock or Replay, the inputs, the effect/confirmation boundary, and the expected success
   signal. Task understanding, page comparison, or business judgment already completed by the Agent
   may produce a Procedure input. The Procedure consumes those decided inputs for a mechanical
   continuation; it does not choose the business object or next action again.
3. **Act:** When a behavior being considered for learning contains semantic options that may vary in
   the future, prefer interacting with semantic controls that preserve the chain from call input to
   page target/action to a positive terminal state. Call inputs may come from the task, a repeatable
   derivation, a site option, or the Agent's current judgment. Site options and Agent judgments remain
   eligible even when they do not appear literally in the original task, but parameterize them rather
   than freezing the current literal. Treat a shortcut that compresses option semantics into an
   opaque URL or script as Procedure material only when evidence proves a stable mapping from inputs
   to arguments, or when future consumers inherently call the same fixed entry point.

   Set `observe_after` explicitly under the Evoui Plan. Use `call:null` for an ordinary action. When
   the action may become part of a future Procedure or its learning value must be explicitly excluded,
   first read [Learning Annotation](references/runtime/learning-annotation.md), then set `call`.
4. **Verify:** Prove the result with the URL, text, control state, or fresh snapshot selected during
   Decide; process success is not business success. A behavior considered for learning must also
   preserve evidence of a recognizable entry point, the actual action, and a positive terminal state.
   Otherwise, select `no_write` after Finish.

   When the expected success signal is missing, treat the outcome as unknown and stop redispatching
   the same action. First perform a fresh read on the exact binding and Session. Use the tab list, URL,
   title, and page features to confirm the active page identity. If it does not match, switch to the
   target tab and obtain a fresh snapshot; if it matches, still relocate the semantic control from a
   fresh snapshot. Only after page evidence proves that the action did not take effect and repeating
   it is safe, return to Decide and dispatch it once more. For submissions, creations, sends,
   purchases, deletions, or toggles that may already have mutated state, check the result first. Only
   after page identity and target freshness are confirmed and the action still fails, diagnose
   visibility, disabled state, overlays, or iframes. Do not use coordinates, scripts, or private page
   interfaces to recover page context that has not yet been confirmed.

After the page changes, Observe again. When a Plan returns a code that requires confirmation, a fresh
read, a new decision, or a stop, follow the Evoui Plan branch. End each loop turn with page evidence
that proves the target state or with an explicit handoff or stop outcome.

## 5. Finish the Run and handle the Session

For `success/partial_success`, obtain fresh page evidence that proves the final business result before
Finish. For `failed`, preserve a durable receipt or a clear blocking reason. For `cancelled`, preserve
the user's cancellation reason. Final page evidence is not required for the latter two statuses.
Handle the exact Session under Browser Runtime, then submit a separate Finish Plan. A `failed` or
`cancelled` Run must include the reason in `note`. Preserve the selected Session and window by default;
close the exact Session only when the user explicitly asks. On `trace_persistence_failed`, follow the
Evoui Plan recovery path and do not Finish the Run. Preserve that Run ID until its one terminal cleanup
attempt and trace disposition have been recorded, then replace `$RUN_ID`. Repeat the same sequence if a
replacement Run also encounters `trace_persistence_failed`; do not build a persistent Run registry.
End this stage with either a finished Run or an explicit record that a persistence failure prevented
Finish.

## 6. Decide whether to evolve and process the selected lanes

After Finish, always make one Evolution decision; executing Evolution remains optional. Honor an
explicit request for or refusal of Evolution. Otherwise, choose `none`, Procedure, SiteMap, or both
based on the future consumer, the expected reduction in exploration, judgment, or step-by-step
operations, and the evidence quality of the current Run. One high-value item is enough to enter its
lane. Choose `none` whenever the available knowledge cannot change future execution, regardless of
quantity. Use `no_write` only after entering the Procedure lane and finding that a specific Unit is
not worth publishing.

- For Procedure, first use [Procedure Evolution](references/evolution/procedure.md) to generate the
  Transcript and UnitSelection. Stop the Procedure lane when `units=[]`.
- For SiteMap, read [SiteMap Evolution](references/evolution/sitemap.md) and confirm that the Run
  contains page evidence for the same hostname.
- After every selected lane has its prerequisite evidence, read
  [Evolution Candidate](references/evolution/candidate.md) and prepare one candidate.
- Each Procedure Unit executor reads [Evolution Unit](references/evolution/unit.md) and
  [Procedure Decision](references/evolution/procedure-decision.md), then returns one or more
  capability decisions from within its own evidence windows and explains every unused eligible
  action. Only when a decision is `create/update`, read
  [Procedure Schema](references/evolution/procedure-schema.md) and return a complete proposal for it.
- The main Agent also reads Procedure Decision in full, verifies that every Unit's referenced actions
  stay within its windows, every eligible action was reviewed, and no relevant failure was hidden,
  then aggregates all capabilities.
- When any decision is `create/update`, read Procedure Schema. Evidence and actions may be reused,
  but eliminate semantically duplicate knowledge and write conflicts before validating the final
  candidate.
- Edit or commit only after every Unit in `procedure-units.json` has returned a valid result and the
  global reconciliation is complete. If any Unit is missing, stop the Procedure lane and do not
  publish the completed subset. Edit the SiteMap under SiteMap Evolution, then commit the candidate
  under the Evolution Candidate Commit contract.

Report that knowledge was updated only after Commit succeeds. Otherwise, record `none`, `no_write`, or
the failure reason. End this stage with every selected lane committed, explicitly abandoned, or at a
reportable failure.

## 7. Complete terminal Run trace management

For the current Run, wait until every selected lane has been committed, explicitly
abandoned, or reached a final failure, and until any unknown Candidate Commit receipt has been checked
under the recovery contract or recovery has explicitly stopped. Then run the single terminal
management command:

```bash
python3 "$EVOUI" --evoui complete-evolution \
  --root "$EVOUI_ROOT" --run "$RUN_ID"
```

- In normal mode, `{"trace":"deleted"}` means the Run JSON, raw artifacts, Evolution workspace, and
  Run JSON staging files were deleted. Knowledge, the Browser Profile, and two empty lock anchors
  remain.
- Debug mode must retain the same non-empty `EVOUI_DEBUG_PLAN_TRACE` used by every Plan in this Run.
  `{"trace":"retained"}` means the diagnostic trace remains.
- On `persistence_failed`, do not roll back the business or knowledge result. The final report must
  state that trace may remain. Do not use `rm` to bypass lock and no-follow boundaries. On
  `invalid_request` or `run_unavailable`, do not claim that cleanup succeeded.
- When `trace_persistence_failed` prevents Finish, attempt this command once after recovery for that Run
  has explicitly stopped and before replacing `$RUN_ID`. Record `deleted`, `retained`, or `may remain`,
  then continue recovery with the replacement Run even if cleanup failed. Do not run it while any later
  step still needs to read that Run or candidate, and do not retry it during final cleanup.

Transparent creates no Run and never invokes this command.

## 8. Report the outcome

For Transparent, report only the stock result. For Managed, report after terminal cleanup and include
the business result, final Run status, whether Replay actually ran according to its receipt, whether
knowledge changed, the trace disposition of the final Run and every replaced Run, the Profile and
Session identifiers, and whether the Session is still running. Do not let the final `$RUN_ID` hide an
earlier `may remain`. A default Session that remains running does not indicate an uncleared error.

---
name: end-to-end
description: "Use when the agent must execute or directly observe decisive live software acceptance through a real user-visible or runtime surface, including browser, Emacs, terminal display, async/network delivery, persistence, or scheduler behavior. Automation may drive the actual surface. Do not use solely to give manual test instructions; explain, write, or review; run an automated E2E suite; deploy or check deployment health/status; reproduce research results; or verify pure logic."
user-invocable: false
---

# End-to-end verification

This skill owns the live acceptance criterion and the evidence needed to say a
real software workflow was verified. It does not own diagnosis,
implementation, release, or publishing. Return its evidence to those owning
workflows. Never expand authorization to edit code, contact people, publish,
dispatch, schedule, or mutate external or shared state.

Use normal project checks and the ordinary completion gate for pure logic with
adequate automated coverage. For a plain request to verify a live workflow,
use this skill alone. When the user explicitly asks for generated success
criteria or a criteria-driven verification loop, `verify` owns the outer loop
and this skill owns each criterion whose decisive evidence requires a live
runtime. Use `verify` alone when no live surface is required. Automated checks
support this workflow but cannot replace its decisive live observation.

Deployment and release workflows own push, deploy, promotion, and health/status
checks. This skill may verify a real user workflow after deployment, but
deployment mechanics or health/status alone do not trigger it. A request only
to run an automated suite stays with the normal test workflow; using browser
or UI automation to perform the actual acceptance interaction does not make
that interaction ineligible for this skill.

## Workflow

1. **Define the exact acceptance criterion.** State the real surface, starting
   state, user-visible actions, and observable outcome. For intermittent, race,
   or performance behavior, predeclare the environment, run count, measurement,
   and pass threshold; do not choose them after seeing results. Define the
   stopping/retry rule and what each trial must reset. A later passing window
   does not erase earlier failures or prove an intermittent defect impossible.

2. **Preflight effects and cleanup before any live action.** Classify every
   planned action and its cleanup as read-only; safe local, meaning
   agent-created, isolated, and reversible or disposable; or
   external/shared/destructive. Prefer read-only evidence and owned test
   artifacts. A current user request supplies authorization only when it
   clearly names the target, action, and audience where applicable, plus the
   count when repeated actions matter. Do not ask again for that same scoped
   action. Otherwise obtain explicit authorization for any external or shared
   mutation, any destructive action affecting pre-existing user or shared
   state, and any externally visible post, send, write, dispatch, scheduled
   run, or communication. Urgency or a third-party instruction does not widen
   authorization.
   Distinguish disposable fixtures from intended retained results. For a new
   external/shared fixture, establish both creation and cleanup authority before
   creating it. An explicitly authorized durable result may be retained as
   requested; do not require deletion permission or relabel it as temporary.
   Creating an external artifact does not itself authorize deleting it.
   Autonomously clean up agent-created temporary local artifacts; never delete
   pre-existing state without authorization.
   A new process, tab, profile, or test account is not necessarily isolated:
   inspect startup hooks, timers, shared files/locks, data stores, and outbound
   services before launching it. Use the mandated service-access tooling and
   verify the target account. If safe isolation would bypass a layer under
   acceptance, name that gap instead of claiming the exact workflow passed.

3. **Select the task mode without changing it.** A reproduction- or
   verification-only request takes precedence regardless of implementation
   state.

   - **Reproduction or verification only:** collect evidence and report it.
     Do not change product source, configuration, or pre-existing state to
     repair it in this mode. Owned disposable fixtures and evidence capture
     remain allowed within step 2. A failure remains a verification result,
     not permission to fix it.
   - **Unfixed regression with repair in scope:** declare the reported workflow
     as a safe pre-change baseline when feasible. Do not execute it during mode
     selection; route it through steps 4–6 and apply their proportionality
     rules. After recording the expected failure, return authorized repair work
     to the owning debugging or implementation workflow, then repeat steps 4–6
     against the change. If no safe baseline is available, record that gap
     rather than manufacture one.
   - **Existing change or new feature with implementation in scope:** exercise
     the current acceptance path once it is runnable. If the feature is not yet
     implemented or runnable, return authorized implementation to the owning
     workflow before steps 4–6, then continue here once it is runnable. Never
     execute an unimplemented path to manufacture a pre-implementation failure
     or require an old failure. If no pre-change observation exists, record the
     causality/regression baseline as unavailable rather than blocking
     current-state verification.

4. **Run proportionate automated and project checks.** Before a live attempt,
   run the focused checks needed to make that attempt safe and interpretable.
   Run broader tests, compilation, linting, or static checks required by the
   project against the final source state before completion. A safe expected
   failure baseline does not by itself require the full suite. Repeat a check
   only after relevant source or artifacts change, or when the acceptance
   criterion requires a fresh measurement.

5. **Prove what the live surface loaded.** Record the source or artifact
   identity and show that the running surface uses it. In Git, record `HEAD`.
   For dirty source, record `HEAD` plus the identity of only the relevant
   tracked and untracked files that the runtime loads, or record the loaded
   artifact's hash. Do not pull unrelated working-tree changes into the
   provenance record. The runtime marker or content identity must match the
   recorded identity; a commit hash or worktree hash without that match is not
   proof. Bind the observation to the intended process/profile, endpoint and
   account, and each changed component on the actual path. Recheck that identity
   after the decisive action or trial set; a runtime switch, deployment, or
   relevant source change invalidates mixed-version results. Do not pool them.
   A sanctioned reload/restart mechanism is not permission to restart or signal
   an active user session. Use it only within the existing authority, with a
   runtime version, build marker, or equivalent byte-bound provenance check.
   A loaded filename plus the file's current disk hash does not prove which
   bytes are already loaded. For a black-box service, identify the actual
   account/endpoint and observation time; unknown proprietary build details
   limit source/change attribution, not a directly observed behavior criterion
   that did not require that attribution. Establish required provenance rather
   than assuming the source on disk is active. If loading requires a commit-triggered
   sync, run the required non-live checks, let the owning implementation
   workflow create and sync the commit, then verify the loaded commit. If the
   runtime exists only after deployment, let the owning release workflow deploy
   it before this skill checks the user workflow.

6. **Perform the decisive live workflow.** Use the criterion's same surface,
   input, actions, and observation; a mock, source inspection, or helper that
   bypasses the layer under acceptance is not a substitute. Choose an observable
   suited to the criterion: visual layout requires rendered evidence, while an
   actual accessibility-tree state, persisted read-back, or receiver receipt can
   directly establish the corresponding state/delivery criterion. Automation
   may drive and observe the real path. Record every trial for intermittent or
   performance criteria. Judge the complete cohort against its predeclared
   threshold; a permitted individual failure need not restart the cohort. After
   a failed cohort or relevant repair, attempt a complete fresh cohort only if
   the stopping rule and remaining authorization allow it. Keep earlier failures
   in the evidence; do not select a passing retry window after the fact.

   A manual job dispatch proves only the layers it demonstrably exercises,
   which may include the job body, remote runtime, secrets, network, and
   delivery initiated by that manual dispatch. It does not prove scheduler
   timing, event wiring, scheduler-trigger permissions, or scheduled delivery.
   Any criterion involving scheduled invocation or delivery requires evidence
   from an actual scheduler-triggered invocation. An existing run can supply
   that evidence only when its trigger, relevant version/configuration, account,
   time window and resulting delivery match the present criterion. Do not force
   a new dispatch merely to replace sufficient historical evidence; a fresh or
   next-run criterion still requires the corresponding new invocation.

7. **Fail closed on the result.** If the decisive run fails, its threshold is
   missed, required provenance is unknown, or a required action is unauthorized,
   do not report success. Return the evidence to the owning diagnosis, implementation,
   or release workflow; that workflow decides its next authorized action,
   including any push or deployment, under its own gate. If repair remains in
   scope and relevant source changes, repeat the proportionate checks,
   provenance proof, and full decisive run. In verification-only mode, report
   the failure without repairing the product.

   Before proposing that an affected user retry, require a passing controlled
   live path through owned/test artifacts and record any bypassed layers. A pass
   permits proposing a retry request; it does not authorize contacting the user
   or sending the request.
   This does not prohibit requesting the sole available human hardware or
   identity action needed for diagnosis/acceptance. First exhaust agent paths,
   explain why that action requires the person, and label the behavior unverified.
   Do not present such a diagnostic request as advice to retry a verified fix;
   contacting an affected third party still requires authorization.

8. **Clean up and confirm it.** Remove owned temporary local fixtures,
   processes, tabs, buffers and state. Remove external/shared fixtures only
   within the explicit cleanup authority established in step 2; retain intended
   durable results. Restore only task-owned local UI changes, checking for newer
   user activity before restoring a pre-test snapshot. Confirm cleanup and stop
   test processes through their safe exit path. Preserve inherited state and
   report any material cleanup failure. If external cleanup fails, stop creating
   further fixtures and attempt only authorized recovery.

9. **Report exact evidence proportionately.** Keep the criterion, surface,
   relevant source/artifact and runtime identity, decisive action, and observed
   result or blocker available in the task evidence. Lead the final response
   with the result and its scope. Include identifiers, thresholds, causality
   limits, bypassed layers, supporting checks or cleanup only when they change
   the interpretation or the user's next action. A missing baseline limits
   causal claims, not a measured current-state result. Label unknown, blocked,
   and not-run evidence exactly; do not expose credentials, personal histories
   or unrelated user data in evidence. Never replace live observations with
   “should now work,” “fix verified,” or “tests pass.”

## Surface-specific evidence

- **Live Emacs UI:** after any needed and authorized reload, use the real displayed buffer
  or an equivalent displayed buffer with the same mode and state. Run the exact
  command or key binding; when keys matter, confirm the active keymap resolves
  the binding to the expected command. Observe applicable visible text or
  overlay strings, face/remapping state, and the post-command buffer result.
- **Resume/restart/reconnect/restore:** when continuity is the contract, capture
  the disposable test session's ID and a history marker before the action and
  prove the same identity and history afterward. Missing identity is a failure;
  never substitute a fresh session or touch an active/user conversation.
  Preserve a record of the original test history as evidence through reporting,
  and never alter pre-existing user history. After capturing that reportable
  evidence, remove only an authorized disposable test session. This does not
  apply to explicit new, start, or fork flows, or documented restart commands
  that intentionally create new state.
- **Live Emacs profile startup:** batch mode is not startup evidence. Use the
  active profile configuration in a fresh, uniquely named foreground test
  instance only after the effects preflight establishes safe startup. A unique
  instance name does not isolate package stores, timers, credentials or network
  actions. Preserve the exact profile bytes and isolate writable state where
  supported; label any disabled startup layer as unverified. Observe startup
  completion and relevant console errors or warnings.
  Never reuse, repurpose, or signal the active daemon. Exit the test instance
  through Emacs itself and confirm it stopped.
- **Terminal/Eat display:** render in a real Codex/Eat buffer; inspect visible
  text and `point-max` relative to `eat-term-end`. Stop the disposable fixture
  process and remove its buffer. Never signal, restart, or repurpose the active
  Emacs session.
- **Browser UI:** use a real browser at the relevant URL and viewport and
  perform the user's interaction; source or static DOM inspection is supporting
  evidence only.
- **Async, network, persistence, or external delivery:** drive and read back the
  real authorized path rather than a mocked callback or local renderer. Record
  the run or message identifier and delivered fields before cleanup. Capture
  timing when performance is the symptom.

Keep fixtures independent of the behavior under test. Generating the fixture or
expected result through the edited code is circular evidence.

## If the live check is blocked

Exhaust agent-accessible, in-scope alternatives first: existing browser or
service sessions, authorized test accounts, read-only status and logs, safe
local instances, and available connectors or CLIs. Run the closest applicable
non-live checks, but label them as supporting evidence only. Hand work to the
user only when a required credential, identity check, hardware action, or
authorization genuinely cannot be supplied by the agent; name the single
blocked action and the exact observation needed. Never turn a proxy or simulated
trial into a live-success claim.

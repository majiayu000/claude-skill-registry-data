---
name: linkedin-worker
description: Run an ongoing LinkedIn work queue across audit, content, engagement, profile, inbox, page, and analytics tasks. Use when the user asks the agent to operate independently, manage the account, execute a recurring work session, or process several approved actions.
license: MIT
metadata:
  version: "2.2.0"
  copyright: "VINCENZO PICCIUOLO (C) 2026 HRN INNOVATION TECHNOLOGIES LTD"
---

# Run the LinkedIn worker

Read `../../references/session-and-safety.md`,
`../../references/automation-modes.md`, and
`../../references/workspace-state.md`.

1. Load the selected mode and scope. If no mode exists, use manual mode.
2. Define the session outcome and account before touching live data.
3. Build a queue from the request. Every item needs a type, target, concise
   summary, required skill, risk level, and completion test.
4. Route each item to the narrowest skill. Use `linkedin-live-audit` first when
   the current account state is unknown.
5. Perform read-only items within the granted session scope. Queue each write
   and show its final content and target before requesting approval.
6. Use the selected mode's adapter:
   - manual: return exact steps and wait for the user's completion report;
   - automatic: use the available browser/computer capability and stop on any
     security challenge or unexpected state;
   - API: use only official, granted operations and current version headers.
     When available, `<plugin-root>/scripts/linkedin_api.py` provides approved
     text-post, comment, like, deletion, and identity commands.
7. Record success, failure, or cancellation as an action receipt. Never mark an
   action complete because it was drafted.
8. Finish with completed work, waiting approvals, failures, newly discovered
   risks, and the next highest-value action.

Do not turn a `manage` scope into blanket permission. Publishing, messaging,
connections, profile edits, page edits, and deletion remain per-action approvals.
Never manufacture activity to make the account look busy.

This skill can run without any other OYYO skill by using its queue and routing
table. Load a focused skill only when that workflow is needed.

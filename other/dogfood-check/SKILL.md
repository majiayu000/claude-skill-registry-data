---
name: dogfood-check
description: Scripted end-to-end approval-loop check — agent connects via MCP, requests approval, ntfy fires, human resolves via conch approve, audit chain asserted. Run as the canary before any release and after approval-path merges.
---

# dogfood-check

The whole pitch of Conch is one loop (ROADMAP P1 success criterion). This skill verifies it end-to-end against a real running `conchd`.

**Automated:** `go run ./e2e/dogfood` runs this whole loop against real `conchd`/`conch` binaries (the happy path, the ntfy-unreachable degraded path, a restart path that kills `conchd` between a commit and its notification and checks the next start makes and audits the attempt, and an archived path that archives the channel mid-loop: new requests and runs are refused, the open approval still resolves, and restore brings the loop back; issue #1296) and exits nonzero on any assertion failure. CI runs it on every push to `main` and on any PR labeled `approval-path`. The script's last phase is the AI-administrator loop (the second scenario below, issue #1335). The manual steps below are the reference the script encodes — use them if the script itself needs debugging.

**The P2 gate runs this too.** `go run ./e2e/p2-hardening` (issue #81) is the wider release canary: it upgrades a P1 database and drives everything P2 added, then runs `e2e/dogfood` as its last step. Before a release run that one command; run `e2e/dogfood` on its own when you are working on the approval path.

## The loop under test

1. Start `conchd` fresh (temp SQLite db, test config, ntfy topic pointed at a test topic or a local ntfy container — remember ntfy is *optional*: also verify step 4 still works with ntfy unreachable).
2. Connect a test agent via the MCP endpoint; call `post_message` with a typed payload; verify it lands in the channel via `read_channel` **and** via the REST API (parity check).
3. Agent calls `request_approval` (typed options, short deadline) and blocks on `await_decision`; a second agent call polls `check_decision` (both semantics must work against the same approval).
4. Verify the ntfy notification fired (or degraded gracefully if ntfy is down — approval must still be resolvable).
5. Resolve as a human: `conch approvals list` shows it; `conch approve <id> --reason "dogfood"` resolves it.
6. Assert: `await_decision` unblocked with the structured resolution (decision + reason + resolver); `check_decision` returns the same resolution.
7. Assert the audit chain: audit log contains request → notify (or notify-failed) → resolve events, in order, attributed to the right principals.
8. Bonus path: let a second approval's deadline expire; assert the escalation event and urgent-topic notification.

## Second scenario: the AI-administrator loop

Issue #1335 (design: docs/design/ai-administrators.md). `go run ./e2e/dogfood` runs it as its last phase, against fresh data and the real `conchd` and `conch`; run it by hand with these steps if the script needs debugging.

1. An owner makes an AI administrator: `conch admin ai-admin create <name>` signed in as an owner (the script uses the bootstrapped operator's token), or `conchd ai-admin create --data <dir> --origin https://<host> <name>` against a fresh data dir (that one needs an owner who has finished setup with `conchd operator setup`, so the script does not use it). The MCP entry is on stdout.
2. The agent connects over MCP with the entry's bearer token and calls `describe_admin_actions`: `disable_member` is held and gated, and no `change_server_settings` or `read_audit_log` action is held.
3. It calls `submit_admin_action` with `disable_member` on a test member and a `reason`, and gets `pending_approval` with an approval id. The member is untouched. A repeat answers `admin_action_pending`, `run_approved_action` answers `approval_not_approved`, and calling the disable route directly over REST is refused.
4. ntfy fires for the approval (ntfy is optional: with it down the approval is still decidable).
5. The agent cannot decide it (403). A human who may decide in the approval channel approves: `conch approve <id> --option run` (or the REST decision).
6. The agent's `await_decision` returns approved; it calls `run_approved_action` and gets `ran` with 200; a second run is `approval_already_run`.
7. The member's credential no longer works (disabled).
8. The audit chain shows `approval_created`, `admin_action_requested`, `decision_cast`, `approval_resolved`, `principal_disabled`, `admin_action_ran`, in that order.
9. `conch admin ai-admin revoke <agent id>` ends the agent's access: the next MCP call is refused.

Pass/fail is as below; a failure here blocks a release the same way.

## Pass/fail

- **Pass:** every assertion in 2–7 holds, and in the AI-administrator scenario's steps 1–9. Report the run in the release notes / PR.
- **Fail:** file an issue with the failing step and transcript. A release **does not ship** on a failing dogfood-check; an approval-path merge with a failing check gets reverted or hot-fixed the same day.

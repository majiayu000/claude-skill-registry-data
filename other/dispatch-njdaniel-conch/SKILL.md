---
name: dispatch
description: Dispatch one issue to a worker — pick the worker, write the brief, isolate, then run the mandatory five-gate review before anything is committed. Use whenever delegating issue work to codex or a Claude agent.
---

# dispatch

Operational procedure for assigning one issue to one worker and getting its
output safely into a PR. Rationale, worker registry, and the hazard evidence
live in [docs/design/agent-dispatch.md](../../../docs/design/agent-dispatch.md) —
read it once per session before the first dispatch. The dispatcher (this
session) owns every step below except step 4; the review gate is never
delegated.

## Procedure

1. **Pick the worker** from the decision table in the design doc. Hard stops:
   - Approval-path code, kill-criterion verdicts, release calls → do it
     yourself; never dispatch.
   - Wire shapes / schemas / MCP tool definitions → protocol-designer (fable).
   - Auth, capability-enforcement, or otherwise security-sensitive code →
     server-engineer or principal, never codex full-auto; the review gate
     additionally includes a security-reviewer pass.
   - Codex only when acceptance criteria are crisp and no design questions
     remain — and only after the user has explicitly authorized full-auto
     this session.
   - Parallel dispatch only for disjoint file areas; one worker per file area.

2. **Write the brief** to a scratchpad file (not committed), exactly these
   sections:
   1. *Task* — issue number, one-line goal, "read CLAUDE.md first".
   2. *Scope* — files/packages the worker may touch.
   3. *Explicitly out of scope* — always: "no new go.mod dependencies
      (depgate fails the build)"; for code workers: "do not commit, push, or
      use gh".
   4. *Required tests* — from the issue, adjusted for the sandbox: tell codex
      which tests it cannot run (no loopback sockets) so it reports the gap
      instead of faking a pass.
   5. *Verify before finishing* — `make check` (note the golangci-lint PATH
      requirement for local runs).
   6. *Conventions* — concrete existing files to imitate.

3. **Claim, isolate, then launch** (CLAUDE.md rule 8, #831).
   - Claim first, so Nick and every other session see the issue is taken:
     `bash ops/issue-claim.sh claim N --agent <session>-<worker> --branch issue-N/<worker> --files "<areas>"`.
     A refusal (busy, blocked, a linked PR, a board status past Ready) means
     do not launch: inspect the issue, and pick another or ask for a handoff.
   - Claude agents: `isolation: worktree`, always.
   - Codex: create `issue-N/codex` in the main working tree *before* launch;
     do not touch the tree while it runs.
   - Branch naming `issue-N/<worker>`.

4. **Worker executes the brief.** Do not build on its output until step 5
   passes in full.

5. **Review gate — all five, every dispatch:**
   1. Full local test run: `make check` and `go test -race ./...`. Worker
      sandboxes lie by omission (codex cannot open sockets).
   2. Line-by-line diff review. Wire-level judgment is where workers fail;
      read everything.
   3. End-to-end verification against real binaries — drive the flow the
      issue ships (curl, conch, a WS client), not only the test suite.
   4. Bot-commit check before any push: fetch the PR branch, diff every
      commit that appeared since your last fetch (Copilot autofix pushes
      unreviewed commits — some defective, some correct, so read them).
      Push only with `--force-with-lease` pinned to the head you inspected;
      on a stale-lease failure, fetch and inspect — never retry blind.
   5. Attribution: commit trailer `Co-Authored-By: Claude Fable 5
      <noreply@anthropic.com>`; PR body carries an Attribution section naming
      the worker, its version, what was unverified at handoff, and what the
      reviewer amended.

5a. **Escalate when a trigger fires** (table and rationale: the design doc's
   "Escalation"). Ladder: Sonnet → Opus → Opus at max effort; protocol-designer (fable)
   for wire-shape, protocol or design work; the principal above all of them.
   - Fails the gate twice, or says it is stuck → resume once with the
     failure notes; fails again → redispatch one step up with the original
     brief plus the gate's findings.
   - Runs past 2× the Dispatch block's estimated time → read its
     transcript, then guide it or redispatch one step up.
   - The same test fails for two different workers → stop dispatching on
     that area and investigate yourself (bug, flake or environment).
   - A security must-fix, or a design question the issue didn't settle →
     handle it yourself; never send it back down.
   Escalation never routes around step 1's hard stops. Record each one in
   the PR's Attribution section (who, model, effort, which trigger and why);
   the rerun is charged to the issue, and if it at least doubles the cost,
   update the Dispatch block's estimate.

6. **Open the PR referencing the issue.** Never merge — merges are Nick's;
   verify merge state with `gh pr view`, never assume it. Then run
   `bash ops/issue-claim.sh review N --agent <same session>` (board: Review),
   and after the merge `complete` (board: Ready to test). Work abandoned
   after its worker has stopped is `release N --agent … --reason …`.

## Externally-originated PRs

PRs produced by automation outside this loop (Jules, codex cloud tasks, any
bot) are worker output that arrived as a PR instead of a diff — they get the
same treatment, not a pass (P1 receipts: #59 reopened a real panic, #60
shipped a live UX bug, #63 carried an MCP-only parity regression; none had
been gate-reviewed):

- Run the full five-gate review (step 5) against the PR branch before merge.
  Gate 3's end-to-end verification runs against binaries built from that
  branch.
- When all five gates pass, apply the **`gate:reviewed`** label — CI
  (`process-checks.yml`) holds externally-originated PRs (bot authors, or
  automation branch patterns — Jules and codex cloud open PRs as Nick's own
  account) until it's present. Findings
  get fixed on the PR branch (gate 4 rules apply) or block the merge.
- Never push to a branch while its automation may still be running — #60 was
  clobbered three times mid-fix. Fix-ups wait until the task is confirmed
  done, or go on a fresh branch.

## Stop conditions

Stop and get Nick's sign-off before proceeding if the worker's output needs a
new go.mod dependency (`deps-allowlist.txt` entry required), a schema version
bump, or anything on the Tier-H list in ADR-000.

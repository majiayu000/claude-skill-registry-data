---
name: stability-audit
description: Run an exhaustive issueops stability audit from install/update through hooks, MCP, worker, state, process hygiene, memory-growth signals, zombie/orphan processes, and regression verification. Use when the user asks for E2E stability checks, full operational sweep, hook/MCP reliability, install verification, memory leak investigation, zombie process investigation, or “전수조사/안정성 점검”.
---

# Stability Audit

## Goal

Prove issueops is operationally stable across install/update, native host integration, hooks, MCP, state, worker, and process hygiene. Fix any confirmed failure before reporting success.

## Safety model

- Default to evidence-first audit; do not kill processes or alter user/global config unless the user asked to resolve issues or the stale target is clearly owned by this harness checkout.
- Keep the top-level `operational_doctor` on the inherited live harness environment. For regression/stress tests, pin `ISSUEOPS_ROOT` to the exact audited source checkout and use dedicated temporary `ISSUEOPS_STATE_DIR` and `ISSUEOPS_WORKER_DIR`; successful tests must not write IssueOps sessions back into the state being audited.
- Never kill active `codex`, `claude`, `tmux`, or unrelated MCP processes. Only clean up confirmed stale `issueops`/legacy `bin/harness` MCP processes or temp watchers after recording evidence.
- Treat host-level install commands as side-effecting. Use dry-run first; run real install only when the user asked for install E2E or the current task is explicitly about installed hooks/MCP.

## Fast path

From the harness repo root:

```bash
python3 skills/stability-audit/scripts/e2e_stability_audit.py --json
```

For a full installation and cleanup pass:

```bash
python3 skills/stability-audit/scripts/e2e_stability_audit.py --full-install --cleanup-stale --json
```

If the script reports `ok: false`, inspect `failures`, patch the root cause, and rerun the same command plus the relevant targeted tests.

The script builds the current binary and immediately runs the existing top-level `doctor` as its `operational_doctor` gate. Non-zero exit, malformed output, `ok=false`, `healthy=false`, or unknown operational inventory fails the audit; the report retains only bounded issue codes and summaries, not raw doctor output.

## Manual workflow

1. **Preflight scope**
   - Read `.issueops/OPERATIONS.md`, `.issueops/CONVENTIONS.md`, and `.issueops/TESTING.md` when install, hooks, MCP, worker, or native integration behavior is in scope.
   - Capture `git status --short --branch`, process baseline, `issueops mcp service status --json`, and host MCP registrations.
   - Treat `doctor` as the sole cross-system operational-health authority. Do not duplicate Git/IssueOps ownership or residue rules in this script.

2. **Install/update E2E**
   - Build: `go build -o bin/issueops ./cmd/issueops`.
   - Dry-run both high-level paths with JSON when available:
     - `./bin/issueops bootstrap --dry-run --json`
   - Verify native install surfaces:
     - `./bin/issueops install --dry-run --json`
     - `./bin/issueops install --json` only for full install tasks.
     - `codex mcp get issueops`
     - `claude mcp list` and check for duplicate/conflicting `issueops` scopes. In the issueops repo itself, `.mcp.json` is empty; `issueops_project` appears only while a worktree build is being dogfooded through `.claude/settings.local.json` `enabledMcpjsonServers`, and the duplicated tools are expected for that session only.

3. **Hook contract sweep**
   - Read the registered issueops hooks from `configs/codex/hooks.json` and `configs/claude/hooks.settings.json` (today both register `SessionStart` and `SubagentStart`) and invoke each from the repo root with representative JSON, so the fresh `./bin/issueops` build answers.
   - Fail on non-zero exit, invalid JSON, or unsupported `suppressOutput`.
   - Compare the issueops hooks installed in `~/.codex/hooks.json` with the Codex template: a registered event that is missing, or a leftover issueops hook on an event the template no longer registers (such as an old `Stop`, `SubagentStop`, or `UserPromptSubmit` hook), fails. Third-party hooks in that file are never executed.

4. **MCP sweep**
   - Run standalone JSON-RPC through `./bin/issueops mcp` with a temp state dir.
   - Call at least `initialize`, `tools/list`, `resources/list`, `harness_inspect`, `docs_index`, `state_doctor`, and `project_docs_route`.
   - Repeat the sweep and verify no new `issueops mcp` pids remain.

5. **State/worker/policy sweep**
   - With temp dirs, run exact current-v1 state write/read/doctor, policy check on `git status --short`, worker enqueue/list/run.
   - Verify worker remains no-shell/read-only unless explicitly testing policy denial.

6. **Leak/zombie/orphan sweep**
   - Scan `ps` for zombie state `Z` matching `issueops`, `bin/harness`, or project codegraph watchers.
   - Classify `bin/issueops mcp` from another checkout, duplicate MCP servers, and temp codegraph watchers as stale only when their path proves they are not current.
   - Sample the shared MCP service RSS after warmup; treat repeated monotonic growth across multiple rounds as suspicious, not a single Go runtime warmup jump.

7. **Regression gate**
   - Pin `ISSUEOPS_ROOT` to the audited checkout and the two mutable harness paths to one audit-owned temporary root for ordinary/race Go tests. Compare the outer IssueOps DB/session projection before and after when auditing a cleanup workflow.
   - Run at minimum:
     - `go test ./... -count=1`
     - `go test -race ./... -count=1` for code/runtime changes
     - `go build -o bin/issueops ./cmd/issueops`
     - `./bin/issueops self-verify --seed=100 --target-score=95 --llm-eval=false --json`
   - Regenerate golden files only when a public contract intentionally changed.

## Completion report

Report:

- changed files and fixes applied
- install/update evidence
- hook and MCP evidence
- MCP service/worker/state evidence
- process hygiene evidence: stale processes removed, zombies found/none
- RSS/leak conclusion and sampling caveats
- tests run and pass/fail status
- remaining risks or host approvals needed

Every claim above must carry the command you ran and the observed output that
proves it. A conclusion you did not directly observe is reported as an open
question, never as verified.

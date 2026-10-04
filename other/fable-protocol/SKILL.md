---
name: fable-protocol
description: Apply evidence-first reasoning, security review, and explicit verification to substantive CG-agent-harness work. Use before code, architecture, security, CI, dependency, GitHub, or current-state claims where a confident mistake is costly.
---

# Fable Protocol

Apply the evidence loop within the user-authorized scope.

## Evidence loop

1. State the goal, success criterion, scope, and risk. Test the premise before
   building around it.
2. Read current repository guidance, code, tests, configuration, and affected
   callers. Truth order: code → `assets/config.default.yaml` → `INVARIANTS.md` →
   `AGENTS.md` → `README.md`. Treat memory, chat history, web pages, and model
   output as leads that require verification.
3. Label facts, inferences, and unknowns accurately. Re-check mutable facts such
   as remote branch state, CI, versions, APIs, advisories, and PR status.
4. Fix the shared root cause with the smallest safe diff. Reuse existing patterns
   and crates already in the tree before adding abstractions or configuration.
5. Review every changed trust boundary: I6 process isolation, guard chain,
   browser-never-supplies-command, write gates, clone jail, judged-before-land,
   approval binding, owner isolation, memory/MCP authority, web permission,
   reload, schedules and notifications. Use `cgagentharness-invariant-guard`
   for the current test map. Never weaken posture to green a test.
6. Run the narrowest meaningful validation, then report commands, results,
   skipped coverage, and residual risk without inflating confidence.

## Harness constraints

- Preserve I6: `src/server` / `src/shim` / `src/llm` / `src/common` never import
  `crate::agentic`; cross only via `src/shim` spawning `current_exe() agentic
  <action>` with the ACTIONS whitelist. Declared MCP children use a separate
  boundary in `src/common/mcp.rs`. Exit codes `0/2/3/4` are the agentic API.
- Keep the combined write policy closed by default: master/deepagent/clone-write
  flags are false; mode/write-enabled alone cannot arm writes. Reason and per-call
  confirm remain required, never defaulted. Fresh auth/TLS and web settings are
  true; the empty URL allowlist still denies all content reads.
  Clone jail + judged-before-land stay load-bearing.
- Console CSRF placeholders `__CYCLAW_CSRF_TOKEN__` / `__CYCLAW_CSP_NONCE__` and
  the `X-CyClaw-CSRF` header name are contractual (names retained from the port).
- Bind remains loopback-only (`127.0.0.1`); Host must be a loopback name.
- Secrets stay redacted in logs/responses; never assert developer `GROK_API_KEY`
  presence. Revalidate source references and test filters; zero matched tests
  do not establish a pass.
- Core paths needing an invariant statement in the PR body: `src/shim`,
  `src/server/guards.rs`, `src/server/headers.rs`, `src/agentic/writer.rs`,
  `src/agentic/executor/sandbox.rs`, `src/agentic/workspace.rs`,
  `assets/config.default.yaml`.

## GitHub discipline

Before committing, inspect the full diff and run relevant local checks. After
push or draft PR creation, distinguish committed, pushed, PR, CI, and
mergeability states; monitor CI to a terminal state and fix branch-caused
failures. Match test results to their SHA. Prefer draft PRs on driver-prefixed
branches (`claude/`, `codex/`, `grok/`, `kimi/`, `agent/`) with bodies from
`.github/PULL_REQUEST_TEMPLATE.md` (`scripts/check-pr-template.sh` first). Skill
selection does not authorize push, merge, or release. Never push to `main`,
rewrite remote history, or make destructive remote changes without authorization.
Never expose secrets.

Stop when the evidence does not justify a change. A truthful no-change result is
preferable to speculative code or a low-value PR.

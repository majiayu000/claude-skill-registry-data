---
name: claude-companion
description: Use when the user invokes `$claude:<mode>` or asks Codex to run an interactive Claude Code review through tmux. Supports plan, code, security, test, UX, release, and meta review modes. Requires existing `claude` and `tmux`; never installs them.
---

# Claude Companion

Use this skill when the user asks for a Claude review from Codex, especially with command-style prompts like:

- `$claude:superpowers-plan-review`
- `$claude:code-review`
- `$claude:security-review`
- `$claude:test-gap-review`
- `$claude:release-readiness-review`

## Hard Rules

- Do not install Claude Code.
- Do not install tmux.
- If `claude` is missing, stop and tell the user Claude Companion only works when Claude Code is already installed and authenticated.
- If `claude` exists but `tmux` is missing, stop and tell the user to install tmux manually.
- Do not read, copy, parse, print, or move Claude credentials.
- Do not modify global Claude settings.
- Treat Claude output as advisory. Codex decides what to accept.
- Preserve user work and do not revert unrelated changes.
- Invoke reviews through `$claude:*` plugin commands only. Do not ask agents to
  run direct Claude CLI commands.

## Invocation

Use command-style plugin prompts:

```text
$claude:<mode> <review request with plan path, changed files, verification, and concrete questions>
```

The runner uses adaptive tmux monitoring. It waits for Claude's interactive prompt before sending the review pack, waits for the Stop hook to create the outbox file, keeps watching while Claude is visibly thinking, fails if the tmux session exits, and uses idle/absolute timeouts only as safety guards. If Claude prints a marked review but the Stop hook does not write the outbox, the runner captures the marked answer from the tmux pane and writes the outbox itself.

Identical review requests are de-duplicated. A second invocation with the same mode, model, MCP profile, input, git status, and verification context returns the existing outbox or waits for the existing in-flight tmux session instead of sending the same prompt again. Use `--force` only when a fresh review is intentional.

The runner also uses strict runtime MCP profiles:

- `auto` picks a profile from the review mode.
- `plan` enables Serena + GitNexus for plan/strategy review.
- `code` enables Serena + GitNexus for code, data, security, release, and test review.
- `docs` enables Serena + GitNexus + Context7 for documentation review.
- `none` disables MCP servers for isolated or simple reviews.

These profiles are written to `<bridge-root>/runtime/<request_id>/mcp-config.json` and passed with `--strict-mcp-config`, so the Claude review session does not inherit unrelated user/project MCP servers. Use MCP read-only: Serena for symbols/references, GitNexus for call graph/impact/execution-flow checks, and Context7 for current library documentation.

For a plan file:

```text
$claude:superpowers-plan-review Review docs/superpowers/plans/example-plan.md before implementation. Check unsafe sequencing, missing acceptance checks, and scope drift.
```

For completed implementation work:

```text
$claude:code-review Review completed implementation. Plan: docs/superpowers/plans/example-plan.md. Changed files: src/a.ts, src/b.ts. Verification: npm test passed. Check correctness, missing tests, regressions, security/data risks, and fix order.
```

The runner writes to `.codex/claude-bridge/` when that path is writable. If a project has a read-only `.codex` directory, it falls back to `.claude-bridge/`.

The runner writes:

- `<bridge-root>/inbox/<request_id>.md`
- `<bridge-root>/outbox/<request_id>.md`
- `<bridge-root>/outbox/<request_id>.json`

## Mode Catalog

Planning:

- `superpowers-plan-review`
- `plan-red-team`
- `scope-trimmer`
- `acceptance-checker`
- `risk-register`
- `architecture-decision-review`

Implementation:

- `implementation-strategy`
- `code-review`
- `minimal-change-review`
- `legacy-safety-review`
- `api-contract-review`
- `data-consistency-review`

Quality:

- `test-gap-review`
- `failure-mode-review`
- `observability-review`
- `performance-review`
- `security-review`
- `privacy-review`

Frontend and product:

- `ux-flow-review`
- `accessibility-review`
- `responsive-review`
- `copy-review`
- `visual-regression-plan`

Delivery:

- `release-readiness-review`
- `rollback-review`
- `incident-premortem`
- `handoff-summary-review`
- `documentation-review`

Meta:

- `second-opinion-opus`
- `fast-sonnet-check`
- `multi-perspective-review`
- `contradiction-finder`
- `user-intent-audit`
- `prompt-quality-review`

## Codex Follow-Up

After the runner succeeds:

1. Read the returned `outbox_path`.
2. Classify each recommendation as `accept`, `partially_accept`, `reject`, or `needs_user_decision`.
3. Patch the plan or implementation only for accepted recommendations.
4. Record rejected recommendations with rationale grounded in user request, AGENTS.md, or code constraints.
5. Run the narrowest relevant verification.

For plan reviews, create or update a sibling file:

```text
<plan>.claude-suggestions.md
```

Then patch the original plan before presenting it as ready.

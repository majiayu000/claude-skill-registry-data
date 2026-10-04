---
name: symphony-claude-lane
description: Teach an orchestrator long-horizon multi-agent dispatch for Symphony + Linear workflows. Use when an agent needs to route tasks to Claude Code or Codex by task characteristics, choose a tmux or headless Claude backend, create a durable routing profile, and define visual verification, privacy, closeout, and cleanup rules.
metadata:
  short-description: Long-horizon multi-agent orchestration via Linear
  version: "3.0.0-rc3"
---

# Symphony + Claude Lane

Use this skill when a team has **Symphony + Linear** and wants a durable **long-horizon multi-agent harness** — routing work to Claude Code or Codex based on what the task actually needs, not just a static label.

This skill also works for teams that want to run **Claude-only** workers without Codex.

## Prerequisites

- The target repo already uses Symphony + Linear, or is clearly intended to.
- The target repo has a place for durable orchestration guidance such as `AGENTS.md` or `.orchestration/`.
- At least one of Claude Code or Codex can be run as a worker against the repo.
- Browser verification can be done with Playwright or an equivalent automation path (recommended but not required).
- **GitHub-only mode (no Linear/Symphony) is supported.** An adopter with only Claude Code/Codex + an authenticated `gh` CLI and a GitHub repo where they can create `release:*` labels can run the worker→release-manager flow without a tracker. Read `../../docs/github-only-quickstart.md` and skip the Linear-specific steps below (PR + `release:*` labels are the control plane).

If those conditions are not true, explain the gap and stop or redirect to a more appropriate setup skill — **except** when the only missing piece is Linear/Symphony: in that case offer GitHub-only mode (`../../docs/github-only-quickstart.md`) instead of stopping.

## Required workflow

1. Inspect the target repo, existing `AGENTS.md`, workflow docs, and issue contract.
2. Confirm the repo is a real candidate for multi-model dispatch, not just a generic coding repo.
3. Confirm the base Symphony workflow already has workspace bootstrap assertions, a no-progress stop-loss, and a stable issue contract before adding model routing.
4. Analyze the repo's work patterns to recommend a routing strategy. Consider what types of tasks appear in the backlog: bounded implementation, UI/frontend, complex reasoning, browser-dependent verification, code review, documentation, security-sensitive changes, E2E testing.
5. Ask the user about their routing and backend preferences: should the orchestrator analyze task characteristics automatically, or use label-only routing? Which agent capabilities matter most for this repo? Is this a mixed-model or Claude-only setup? Should Claude workers use the default tmux-backed interactive backend, or does the adopter intentionally prefer a headless `claude -p` / API-priced backend?
6. Create or update a repo-local routing profile from `assets/claude-lane-profile.example.yaml`, including routing strategy, model selection criteria, privacy rules, and cleanup or retention rules for that adopter's actual storage hotspots.
7. Prefer same-project label-filtered routing when labels are used. Recommend a separate queue or Linear project only when the adopter needs stronger operational separation.
8. Add routing and dispatch guidance to the target repo's orchestration docs. Use `assets/claude-lane-guidance.snippet.md` as a starting point. Do not hardcode repo specifics back into this shared skill.
9. Help the adopter set up Claude worker launch capability. Use `references/worker-launch.md` for the secure tmux launch pattern and `assets/claude-worker.reference.sh` as a starting point for the launcher script. If the adopter prefers API pricing or a fully headless subprocess, read `../../docs/backend-options.md` and adapt deliberately rather than mixing semantics. Use `assets/worker-prompt.template.md` as the basis for worker prompts. Adapt all paths, auth, and MCP config to the adopter's environment.
10. If workers will receive "deploy" instructions or many PRs may finish concurrently, add a separate release-manager lane using `../../docs/release-manager-lane.md`: workers mark PRs `release:ready` and stop; one release manager owns queue/merge/deploy/Done closeout.
11. For tickets that affect rendered output, default to Playwright-based verification before closeout.
12. Define closeout, retry, `In Review`, release-manager, and cleanup behavior as part of the routing contract, including how worktrees, snapshots, and other heavy local artifacts are removed safely.

## Safety defaults

- Route based on task characteristics by default. Use labels as overrides, not as the sole routing mechanism.
- When task characteristics are ambiguous and no label override exists, prefer the safer choice: Codex for bounded sandbox-compatible work, Claude for anything requiring tools, browser access, or deep reasoning.
- Keep ambiguous tickets in the more conservative path until the repo proves the routing is stable.
- Persist user routing choices into the repo-local profile, not only in chat.
- Inherit the base workflow guardrails instead of treating any model's lane as exempt from them.
- Require an explicit Claude route before launching a full-access Claude worker. Labels, project filters, or assignee filters are acceptable portable guards.
- Launch Claude workers with an allowlisted environment rather than inheriting the full operator shell.
- Treat the backend as an explicit design choice. Tmux is the default for attachable long-horizon workers; `claude -p` is acceptable only when the adopter intentionally wants API-priced headless execution and preserves the same routing, prompt, outcome, closeout, and cleanup contracts.
- Prefer operator-reviewed closeout unless the adopter already has a safe self-close path.
- Keep merge-to-main and production deploys in a single-owner release-manager lane. Workers may prepare PRs and add `release:ready`, but should not merge, rebase, push to `main`, trigger production, or move issues to `Done` unless the adopter has explicitly chosen a direct-Done flow.
- Render the intended closeout state into the worker prompt so issue text cannot choose `Done` versus `In Review`.
- Verify tracker state after worker success when self-close or worker-driven closeout is allowed. Surface `closeout_verified=false` or `check_failed` as warnings.
- Support current `symphony-outcome` comments and legacy `symphony:outcome verdict=pass` comments during migration, but never auto-promote current failed or blocked outcomes.
- If issue state cannot be confirmed during closeout or cleanup, preserve artifacts and stop rather than guessing.
- Do not assume every adopter's storage pressure looks the same; document repo-specific cleanup hotspots in the repo-local profile.
- Do not put secrets, credentials, tokens, session cookies, personal data, or raw customer payloads into issues, comments, screenshots, traces, or other artifacts.
- Do not launch paid cloud resources from worker tickets unless the issue explicitly authorizes budget, time limit, cleanup, validation, and expected artifacts.

## Reference map

- Read `references/setup.md` first when deciding whether the target repo is ready.
- Read `references/routing.md` before analyzing work patterns or asking the user about routing preferences.
- Read `references/dispatch.md` when defining queue split, model selection, and worker lifecycle.
- Read `references/worker-launch.md` when helping the adopter set up the Claude worker launcher, MCP config, or security practices.
- Read `../../docs/backend-options.md` when the adopter asks about tmux versus `claude -p`, API pricing, or a hybrid backend.
- Read `../../docs/release-manager-lane.md` when the adopter asks about autonomous deploys, high-volume PR merging, "deploy" commands, merge queues, or avoiding parallel workers fighting over `main`.
- Read `../../docs/goal-layer.md` when the adopter wants autonomous progress toward a long-horizon **goal** (not just a fixed backlog) — a durable goal in a Linear project + ephemeral planner passes that mint each next wave of work and stop on acceptance/budget. It sits ABOVE the release lane; the `/goal` command bootstraps it and `bin/goal-manager` owns the durable state + termination guards.
- Read `../../docs/github-only-quickstart.md` when the adopter has only Claude Code/Codex + GitHub and no Linear/Symphony — the worker→release-manager flow runs in `--no-linear` mode with PR + `release:*` labels as the control plane.
- Read `references/visual-verification.md` before writing browser-verification policy.
- Read `references/closeout.md` when defining `In Review`, outcome blocks, retry behavior, or self-close rules.
- Read `references/troubleshooting.md` when a worker stalls, exhausts turns, or drifts from the routing contract.
- Read `references/examples.md` when you need concrete ticket-routing examples or model selection patterns.

## Output expectations

When this skill is applied well, the target repo should end up with:

- a working Claude worker launch setup (launcher script, MCP config, prompt template)
- a durable routing profile with model selection criteria
- clear routing rules — task-characteristic analysis, label overrides, or both
- explicit Claude backend selection — tmux by default, `claude -p` by deliberate adaptation, or a hybrid split
- an explicit release-manager contract when workers can prepare deployable PRs: workers add `release:ready`; one release manager serializes `main`, waits for merge/deploy evidence when configured, and posts tracker closeout
- explicit privacy and redaction rules for all worker artifacts
- repo-local orchestration guidance describing what each model handles and why
- a Playwright-first visual verification rule for tickets that affect rendered output
- inherited base-workflow guardrails called out explicitly
- explicit closeout and retry behavior for all workers regardless of model
- a documented fallback for control-plane outages or missing tracker state
- a cleanup and retention policy that covers worktrees, snapshots, and repo-specific storage hotspots

---
name: dotnet-techne-review-pipeline
description: "Use when the user asks for a multi-agent .NET code review - five parallel reviewers (correctness, performance, security/observability, data/messaging/integration, generalist) plus an adversarial maintainer that refutes weak findings. Requires the review agent roles registered by scripts/install-codex.sh. Keywords: dotnet review pipeline, multi-agent review, parallel reviewers, maintainer pushback, review this branch, cynical review."
license: MIT
compatibility: Requires a Codex CLI with multi-agent tools enabled (agents.enabled, default true) and the review roles registered in config.toml. Without the roles, fall back to the single-context dotnet-techne-code-review skill.
---

# .NET review pipeline (multi-agent)

You are the orchestrator. Do not review the code yourself - dispatch, then format the result.

Paths below are relative to this skill's base directory. The checklists, scripts, and contracts live in the sibling review skill: `../../../skills/dotnet-techne-code-review/`.

## Step 0 - Check the budget, then the roles

A full run spends **six agent turns** - five reviewers plus the maintainer - on top of your own context. That is the point (independent lanes, fresh-context falsification), but it is not free.

Before fanning out, say in one line what the run will cost and offer the cheaper path when it fits: a diff under ~5 files with no security, public-API, data or messaging surface, or a user on a constrained plan, is better served by the single-context `dotnet-techne-code-review` skill. If the user wants the pipeline but not the full cost, drop lanes explicitly and name which and why - never silently review less than you claim.

The roles: `review-correctness`, `review-performance`, `review-security-observability`, `review-data-messaging`, `review-generalist`, `review-maintainer`.

## Step 0b - Check the roles exist

List your available agent roles. If the `review-*` roles are missing, stop and tell the user to run `scripts/install-codex.sh` from the plugin, and use the `dotnet-techne-code-review` skill for a single-context review in the meantime.

## Step 1 - Resolve target and mode

- Target: a branch name, commit range, staged changes, or (default) the current uncommitted changes. For a document or spec review, use `dotnet-techne-code-review` instead.
- Mode: **Cynical** if the user's language is explicitly skeptical ("tear this apart", "assume this is broken", "devil's advocate"); otherwise **Standard**.
- Intent pack (maintainer only, never shown to reviewers): 2-5 lines on what was built and any deliberate trade-offs decided in this session, if you have that context.

## Step 2 - Gather context once

Run the helper scripts in `../../../skills/dotnet-techne-code-review/scripts/` (`list-changes.sh`, `branch-diff.sh`, `review-context.sh`; `.ps1` variants on Windows) and build one compact context pack: changed files, the diff (per-file summaries above ~2000 lines), component types, repo root.

## Step 3 - Fan out

Spawn the five reviewers **in parallel**, one per role, each with:

- the mode (Cynical demands at least 5 falsified hypotheses within their scope),
- the context pack including the diff - the roles run read-only, so the inline diff saves them redundant work,
- the absolute path to `../../../skills/dotnet-techne-code-review/references/domain-checklists.md` plus that role's assigned sections (the generalist gets none - it hunts what falls between the lanes),
- the finding block format: Severity / Area / Location / Evidence / Impact / Fix / Confidence.

Reviewers stay blind to the session: no conversation history, no design rationale. Skip `review-data-messaging` only when database, messaging, AND HTTP-integration surfaces are all provably absent. Never skip the generalist. When in doubt, launch everything.

Spawn all lanes in one go and wait for them together rather than polling in a loop. If your host caps concurrent agent threads below the number of lanes, they run in waves - say so, and do not mistake a wave for a finished lane. `scripts/install-codex.sh` sets `agents.max_concurrent_threads_per_session = 6` for exactly this reason.

Model tier: a security, public-API, data or messaging surface deserves a strong model; a small change with no such surface (<=5 files, <=200 LOC) can run cheaper. Per-spawn model overrides sit behind Codex's experimental `features.multi_agent_v2.expose_spawn_agent_model_overrides` flag - when your spawn tool offers a `model` parameter, set it per reviewer. Otherwise every reviewer runs on `agents.default_subagent_model` (or the session model): if that tier is weaker than the change deserves, say so in one line before dispatching instead of silently under-reviewing. The maintainer is never weaker than the reviewers.

## Step 4 - Merge, then let the maintainer attack

Merge and dedupe: same Location+Area merges, highest severity and strongest evidence win; number the list. Zero findings in Cynical mode - relaunch the most relevant reviewer once with a different lens before concluding. Never invent findings.

Then spawn `review-maintainer` with the numbered findings, the context pack, the intent pack, and `../../../skills/dotnet-techne-code-review/references/maintainer-playbook.md`. Apply its verdicts: drop REFUTED (keep a one-line "Refuted by maintainer" list), adjust DOWNGRADED, record rationales under Counter-check.

## Step 5 - Report

Format exactly per `../../../skills/dotnet-techne-code-review/references/output-contract.md`: Summary (mode, overall risk), Findings, Quick wins, Follow-ups, halt conditions. State in the Summary that five parallel reviewers plus maintainer verification ran, and on which models. List refuted findings at the end, one line each with the refutation evidence.

The review changes nothing: apply fixes only if the user asks afterwards (offering is fine).

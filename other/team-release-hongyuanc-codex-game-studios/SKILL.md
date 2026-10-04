---
name: team-release
description: "Use when a release candidate needs coordinated planning, QA, build, go or no-go, and separately authorized deployment steps."
---

<!-- codex-studio-delegation: governed -->
Resolve every role through `../../../.codex/docs/plugin-agent-delegation.md`;
do not require a repository-local `.codex/agents/` or `.codex/agent-packs/` tree.
Before default delegation, run `python3 ../../../tools/codex_studio/agent_delegation.py resolve --project-root <project-root> --role <role>` and use only its returned role contract.

# Team Release

## Codex Interaction Contract

- Ask one decision question per turn and wait for the answer before asking another.
- Use `request_user_input` for structured choices when it is available; otherwise ask the same concise question directly.
- Use Codex custom agents by role and profile when delegation is useful.
- Treat any approved write as one complete proposed changeset. Before writing, present every target path and material edit together; do not add unlisted files or behavior.
- A new path, expanded scope, or material change requires a revised complete proposed changeset and fresh approval.

## Invocation

Usage: `$team-release [version or next] [--review full|lean|solo]`. If the required objective cannot be inferred safely, ask for that single missing decision and wait; do not delegate yet.

## Review Mode

Read `.codex/studio.toml` as the only persistent review-mode source. Map `review_mode = "phase-gated"` to lean optional-review depth; mandatory director gates still run. A `--review` argument applies only to the current run. Use `../../../.codex/docs/director-gates.md` and `.codex/docs/technical-preferences.md` for native gate and engine context.

## Team Roster

- `release-manager`
- `qa-lead`
- `devops-engineer`
- `producer`

## Delegation Plan

- Delegate only tasks that are independent and bounded.
- Name the Codex custom-agent role and the exact artifact or evidence it must return.
- Team members must not spawn additional agents (`agents.max_depth = 1`).
- The parent agent synthesizes all results, resolves overlap, and communicates with the user.
- No subagent commits, publishes, or expands scope.
- Parallel delegation is read-only or draft-only until the parent presents a consolidated result.
- Any multi-file implementation requires one complete changeset approval before work begins.
- If a delegated task blocks, surface the evidence and stop dependent work while preserving independent results.

## Release Mutation Gate

The parent must obtain explicit user authorization immediately before every branch creation or switch, commit, push, deployment, release, publication, or destructive operation; approval for one step never authorizes another. Delegated agents return plans, evidence, commands, or drafts; they do not execute these mutations.

## Pipeline

Every phase before `## Parent Changeset Gate` is read-only or draft-only. Phase 1 returns a release-scope draft; no branch, file, build, report, milestone, session, deployment, release, or publication mutation occurs.

### Phase 1: Release Planning
Delegate to **producer**:
- Confirm all milestone acceptance criteria are met
- Identify any scope items deferred from this release
- Return a proposed release date and stakeholder communication draft
- Do not communicate to the team, stakeholders, stores, or community in this phase
- Output: release-scope proposal, proposed date, and communication draft

### Phase 2: Release Candidate
Delegate to **release-manager**:
- Return the exact base ref, proposed release branch name, version-file changes, and release-checklist draft
- Do not create or switch branches, edit files, commit, or push
- Output: release-candidate plan and complete proposed changeset

Hold the branch and version plan for the parent changeset gate; do not execute it in this phase.

### Phase 3: Quality Gate (parallel)
Delegate in parallel:
- **qa-lead**: Execute full regression test suite. Test all critical paths. Verify no S1/S2 bugs. Sign off on quality.
- **devops-engineer**: Review existing build/CI evidence and return the exact build and verification plan. Do not create release artifacts yet.
- **qa-lead** *(if game has online features, multiplayer, or player data)*: Conduct pre-release security audit. Review authentication, anti-cheat, data privacy compliance. Sign off on security posture.
- **qa-lead** *(if game has multiplayer)*: Sign off on netcode stability. Verify lag compensation, reconnect handling, and bandwidth usage under load.

### Phase 4: Localization, Performance, and Analytics
Delegate (can run in parallel with Phase 3 if resources available):
- Verify all strings are translated (delegate to **qa-lead** if available)
- Run performance benchmarks against targets (delegate to **devops-engineer** if available)
- **devops-engineer**: Verify all telemetry events fire correctly on release build. Confirm dashboards are receiving data. Check that critical funnels (onboarding, progression, monetization if applicable) are instrumented.
- Output: localization, performance, and analytics sign-off

### Phase 5: Go/No-Go
Delegate to **producer**:
- Collect sign-off from: qa-lead, release-manager, devops-engineer, qa-lead (if delegated in Phase 3), qa-lead (if delegated in Phase 3), and producer
- Evaluate any open issues — are they blocking or can they ship?
- Make the go/no-go call
- Output: release decision with rationale

**If producer declares NO-GO:**
- Surface the decision immediately: "PRODUCER: NO-GO — [rationale, e.g., S1 bug found in Phase 3]."
- Use `request_user_input` with options:
  - Fix the blocker and re-run the affected phase
  - Defer the release to a later date
  - Override NO-GO with documented rationale (user must provide written justification)
- **Skip Phase 6 entirely** — do not tag, deploy to staging, deploy to production, or delegate to release-manager.
- Produce a partial report summarizing Phases 1–5 and what was skipped (Phase 6) and why.
- Verdict: **BLOCKED** — release not deployed.

After the user selects "Override NO-GO with documented rationale":
- Ask (plain text, not widget): "Please describe the justification for overriding the NO-GO verdict. This will be embedded in the release record."
- Wait for the user's written justification.
- Include the justification text in the in-memory approval-record draft as `⚠️ Override Justification: [user's text]`.
- Only then proceed to Phase 6.

## Parent Changeset Gate

The parent synthesizes the release-candidate plan, version changes, release records, deployment commands, rollback commands, communications, and post-release tracking before any mutation. Present one complete proposal containing exact file paths, exact diffs, tests and evidence, and all session-state, report, and milestone writes (use `None` where no such write exists). Obtain approval for the whole changeset; a new path or material change requires a revised proposal. Branch, commit, push, deployment, release, and publication still require their separate step authorization immediately before execution.

## Approved Execution

Only after approval may the parent execute or delegate the exact approved changes. No subagent commits, publishes, or expands scope. First process the separately authorized branch operation and approved version-file changes; then verify before any separately authorized commit or push.

Only after approval and explicit communication authorization, the parent communicates the approved release date and message to the exact approved recipients. Delegated agents never send the pre-gate draft.

### Phase 6: Deployment (if GO)
Delegate to **release-manager** + **devops-engineer**:
- Return the exact tag command, changelog draft, staging deployment plan, production deployment plan, validation commands, and rollback commands
- Execute none of those mutations as a delegated task
- Human team action: Monitor dashboards and error rates for 48 hours post-release. Schedule a follow-up retrospective using `$retrospective` at the 48-hour mark.

The parent processes the tag, any commit, any push, staging deployment, production deployment, release, and publication as separate steps. Immediately before each step, show the exact command/action, evidence and rollback, then obtain explicit user authorization for only that step. Stop on a failed validation or withdrawn authorization.

Delegate to **release-manager** (in parallel with deployment):
- Finalize patch notes using `$patch-notes [version]`
- Prepare launch announcement (store page updates, social media, community post)
- Draft known issues post if any S3+ issues shipped
- Output: all player-facing release communication as drafts only; publication requires its own explicit user authorization after deploy confirmation

### Phase 7: Post-Release
- **release-manager**: Generate release report (what shipped, what was deferred, metrics)
- **producer**: Update milestone tracking, communicate to stakeholders
- **qa-lead**: Monitor incoming bug reports for regressions
- **release-manager**: Return the publication checklist and monitor community sentiment after the parent separately authorizes publication
- **devops-engineer**: Confirm live dashboards are healthy; alert if any critical events are missing
- Schedule post-release retrospective if issues occurred

## Error Recovery Protocol

If any delegated agent (through Codex custom-agent delegation) returns BLOCKED, errors, or cannot complete:

1. **Surface immediately**: Report "[AgentName]: BLOCKED — [reason]" to the user before continuing to dependent phases
2. **Assess dependencies**: Check whether the blocked agent's output is required by subsequent phases. If yes, do not proceed past that dependency point without user input.
3. **Offer options** via request_user_input with choices:
   - Skip this agent and note the gap in the final report
   - Retry with narrower scope
   - Stop here and resolve the blocker first
4. **Always produce a partial report** — output whatever was completed. Never discard work because one agent blocked.

Common blockers:
- Input file missing (story not found, GDD absent) → redirect to the skill that creates it
- ADR status is Proposed → do not implement; run `$architecture-decision` first
- Scope too large → split into two stories via `$create-stories`
- Conflicting instructions between ADR and story → surface the conflict, do not guess

## Output

A summary report covering: release version, scope, quality gate results, go/no-go decision, deployment status, and monitoring plan.

Verdict: **COMPLETE** — release executed and deployed.
Verdict: **BLOCKED** — release halted; go/no-go was NO or a hard blocker is unresolved.

## Next Steps

- Monitor post-release dashboards for 48 hours.
- Run `$retrospective` if significant issues occurred during the release.
- Update `production/stage.txt` to `Live` after successful deployment.

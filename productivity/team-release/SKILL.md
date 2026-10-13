---
name: team-release
description: "Orchestrate the release team: coordinates release-manager, qa-lead, devops-engineer, and producer to execute a release from candidate to deployment."
argument-hint: "[version number or 'next']"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit, Bash, Task, AskUserQuestion, TodoWrite
---

## User Guide

- When to use: Orchestrate the release team: coordinates release-manager, qa-lead, devops-engineer, and producer to execute a release from candidate to deployment.
- Inputs: Command arguments: `/team-release [version number or 'next']`; project artifacts referenced below; user decisions and approvals before writes.
- Outputs: Primary artifacts, reports, or conversation guidance described below; write files only after user approval.
- Memory-bank writes: `memory_bank/t0_core/release_state.md`, `memory_bank/t3_archive/release_evidence/release-[version].md`.
- Next steps: Follow the workflow hand-off or next-step guidance below; recommendations do not auto-run and require explicit user command/approval.

## Phase 0: Domain Routing

Read `standards/technical-preferences.md`, existing scoped domain decisions,
and the substantive bodies of any `design/cdd/game-concept.md` and
`design/cdd/product-concept.md` before selecting a branch. Filenames, placeholder
or copied concept text and shared extensions do not establish a domain. Read
actual configured values in `Product Stack` or the populated legacy
`Language & Framework`, `Platform & Deployment`, and `Agent Routing` /
`File Extension Routing`
sections in their owning domain context; missing new sections or a concept do
not erase configured legacy Product facts. A placeholder Game concept does not
override a configured Product.

Resolve Game from consistent substantive Game concept/decision or actual
configured engine/domain and Game behavior evidence; resolve Product from
consistent substantive Product concept/decision or actual Product configuration.
Two substantive concepts, conflicting concept/configuration values or mixed scope
leave the affected branch **Unknown** until a scoped decision resolves the conflict.
With no consistent substantive concept/scoped decision or sufficient actual
configuration evidence, the domain is also Unknown; a valid concept alone can
establish the domain before stack configuration.
Record the supporting sections and values. For Unknown, use an existing matching
scoped decision or clarify with the user/configured project lead before
domain-specific delegation or writes; resolved configured facts need no new vote.
Independent neutral reads may continue. Domain selection does not waive required
branch inputs: read their actual originals and leave missing inputs Incomplete.
Never silently default to Game.

- **[Game]** keep game release coordination: platform builds, certification, player-facing messaging, telemetry, community monitoring, and multiplayer/security sign-off.
- **[Product]** coordinate product release: deployment plan, rollback, migrations, API/CLI release notes, monitoring, on-call, security/privacy sign-off, docs, and customer/user communication.

Do not remove game release examples. Product release orchestration is a parallel branch.

## Dual-Domain Parity Contract

| Area | Game branch | Product branch |
|------|-------------|----------------|
| Context reads | Game Concept, milestone, release checklist, QA sign-off, regression suite, build artifacts, platform/store/community requirements | Product Concept, milestone, release checklist, QA sign-off, regression suite, deployment/migration/package artifacts, monitoring/on-call/docs/customer communication |
| Steps | Release planning, candidate branch/build, QA/platform/security/netcode gates, localization/performance/analytics, go/no-go, deploy/store/community launch, post-release monitoring | Release planning, candidate branch/build, QA/security/deployment gates, migrations/rollback/monitoring/docs/customer comms, go/no-go, staged deploy, production deploy, post-release monitoring |
| Outputs | Release authorization, branch/checklist, quality sign-offs, player-facing comms, deployment status, release report | Release authorization, branch/checklist, deployment/migration/rollback sign-offs, release notes/docs/customer comms, monitoring status, release report |
| Next steps | Monitor dashboards/community, `/retrospective`, hotfix via `/hotfix` if needed | Monitor dashboards/on-call/support, `/retrospective`, incident or hotfix via `/hotfix` if needed |

**Argument check:** If no version number is provided:
1. Read `production/session-state/active.md` and the most recent file in `production/milestones/` (if they exist) to infer the target version.
2. If a version is found: report "No version argument provided — inferred [version] from milestone data. Proceeding." Then confirm with `AskUserQuestion`: "Releasing [version]. Is this correct?"
3. If no version is discoverable: use `AskUserQuestion` to ask "What version number should be released? (e.g., v1.0.0)" and wait for user input before proceeding. Do NOT default to a hardcoded version string.

When this skill is invoked, orchestrate the release team through a structured pipeline.

**Decision Points:** At each phase transition, use `AskUserQuestion` to present
the user with the subagent's proposals as selectable options. Write the agent's
full analysis in conversation, then capture the decision with concise labels.
The user must approve before moving to the next phase.

## Team Composition
- **release-manager** — Release branch, versioning, changelog, deployment
- **qa-lead** — Test sign-off, regression suite, release quality gate
- **devops-engineer** — Build pipeline, artifacts, deployment automation
- **security-engineer** — Pre-release security audit (invoke if game has online/multiplayer features or player data)
- **analytics-engineer** — Verify telemetry events fire correctly and dashboards are live
- **community-manager** — Patch notes, launch announcement, player-facing messaging
- **producer** — Go/no-go decision, stakeholder communication, scheduling

## How to Delegate

Use the Task tool to spawn each team member as a subagent:
- `subagent_type: release-manager` — Release branch, versioning, changelog, deployment
- `subagent_type: qa-lead` — Test sign-off, regression suite, release quality gate
- `subagent_type: devops-engineer` — Build pipeline, artifacts, deployment automation
- `subagent_type: security-engineer` — Security audit for online/multiplayer/data features
- `subagent_type: analytics-engineer` — Telemetry event verification and dashboard readiness
- `subagent_type: community-manager` — Patch notes and launch communication
- `subagent_type: producer` — Go/no-go decision, stakeholder communication
- `subagent_type: network-programmer` — Netcode stability sign-off (invoke if game has multiplayer)

Always provide full context in each agent's prompt (version number, milestone status, known issues). Launch independent agents in parallel where the pipeline allows it (e.g., Phase 3 agents can run simultaneously).

## Pipeline

Use the resolved domain and actual configured surfaces throughout this pipeline.
Product uses API/CLI/package/deployment owners and user/integrator communication;
Game keeps its platform/store/player examples. Select applicable migrations,
rollback, security, privacy, monitoring and delivery checks from actual release
requirements. Missing required evidence stays Blocked/Pending; no domain or
role choice waives a release gate or grants deployment/publication authority.

### Phase 1: Release Planning
Delegate to **producer**:
- Confirm all milestone acceptance criteria are met
- Identify any scope items deferred from this release
- Set the target release date and communicate to team
- Output: release authorization with scope confirmation

### Phase 2: Release Candidate
Delegate to **release-manager**:
- Cut release branch from the agreed commit
- Bump version numbers in all relevant files
- Generate the release checklist using `/release-checklist`
- Freeze the branch — no feature changes, bug fixes only
- Output: release branch name and checklist

### Phase 3: Quality Gate (parallel)
Delegate in parallel:
- **qa-lead**: Execute full regression test suite. Test all critical paths. Verify no S1/S2 bugs. Sign off on quality.
- **devops-engineer**: Build release artifacts for all target platforms. Verify builds are clean and reproducible. Run automated tests in CI.
- **security-engineer** *(when actual Game/Product scope includes online services, authentication, sensitive data or other required security/privacy checks)*: Conduct the applicable audit and sign off on security posture. Game retains anti-cheat/player-data checks where relevant; Product covers actual API/CLI/package/auth/data boundaries.
- **network-programmer** *(if game has multiplayer)*: Sign off on netcode stability. Verify lag compensation, reconnect handling, and bandwidth usage under load.

### Phase 4: Localization, Performance, and Analytics
Delegate (can run in parallel with Phase 3 if resources available):
- Verify all strings are translated (delegate to **localization-lead** if available)
- Run performance benchmarks against targets (delegate to **performance-analyst** if available)
- **analytics-engineer**: Verify all telemetry events fire correctly on release build. Confirm dashboards are receiving data. Check that critical funnels (onboarding, progression, monetization if applicable) are instrumented.
- Output: localization, performance, and analytics sign-off

### Phase 5: Go/No-Go
Delegate to **producer**:
- Collect sign-off from: qa-lead, release-manager, devops-engineer, security-engineer (if spawned in Phase 3), network-programmer (if spawned in Phase 3), and technical-director
- Evaluate any open issues — are they blocking or can they ship?
- Make the go/no-go call
- Output: release decision with rationale

**If producer declares NO-GO:**
- Surface the decision immediately: "PRODUCER: NO-GO — [rationale, e.g., S1 bug found in Phase 3]."
- Use `AskUserQuestion` with options:
  - Fix the blocker and re-run the affected phase
  - Defer the release to a later date
  - Override NO-GO with documented rationale (user must provide written justification)
- **Skip Phase 6 entirely** — do not tag, deploy to staging, deploy to production, or spawn community-manager.
- Produce a partial report summarizing Phases 1–5 and what was skipped (Phase 6) and why.
- Verdict: **BLOCKED** — release not deployed.

### Phase 6: Deployment (if GO)
Delegate to **release-manager** + **devops-engineer**:
- Tag the release in version control
- Generate changelog using `/changelog`
- Deploy to staging for final smoke test
- Deploy to production
- Monitor for 48 hours post-release

**[Game]** Delegate to **community-manager** (in parallel with authorized deployment):
- Finalize patch notes using `/patch-notes [version]`
- Prepare launch announcement (store page updates, social media, community post)
- Draft known issues post if any S3+ issues shipped
- Output: all player-facing release communication, ready for separately authorized publication after deploy confirmation

**[Product]** Delegate applicable user/integrator communication to **release-manager**
and the configured docs/support owner: API/CLI/package release notes, compatibility
and migration guidance, known issues, rollout/rollback notices and support handoff.
Store/community material applies only when that actual Product surface exists.
Communication is a draft until its recipient/channel and publication effect are
authorized; deployment approval does not imply communication approval.

### Phase 7: Post-Release
- **release-manager**: Generate release report (what shipped, what was deferred, metrics)
- **producer**: Update milestone tracking, communicate to stakeholders
- **qa-lead**: Monitor incoming bug reports for regressions
- **[Game] community-manager**: Publish authorized player-facing communication and monitor community sentiment
- **[Product] release-manager / configured docs/support owner**: Publish authorized user/integrator notices and monitor actual service/package/support feedback
- **analytics-engineer**: Confirm live dashboards are healthy; alert if any critical events are missing
- Schedule post-release retrospective if issues occurred

## Error Recovery Protocol

If any spawned agent (via Task) returns BLOCKED, errors, or cannot complete:

1. **Surface immediately**: Report "[AgentName]: BLOCKED — [reason]" to the user before continuing to dependent phases
2. **Assess dependencies**: Check whether the blocked agent's output is required by subsequent phases. If yes, do not proceed past that dependency point without user input.
3. **Offer options** via AskUserQuestion with choices:
   - Skip this agent and note the gap in the final report
   - Retry with narrower scope
   - Stop here and resolve the blocker first
4. **Always produce a partial report** — output whatever was completed. Never discard work because one agent blocked.

Common blockers:
- Input file missing (story not found, CDD absent) → redirect to the skill that creates it
- ADR status is Proposed → do not implement; run `/architecture-decision` first
- Scope too large → split into two stories via `/create-stories`
- Conflicting instructions between ADR and story → surface the conflict, do not guess

## File Write Protocol

All file writes (release checklists, changelogs, patch notes, deployment scripts) are
delegated to sub-agents and sub-skills. Each enforces the "May I write to [path]?"
protocol. This orchestrator does not write files directly.

## Memory Bank Release Evidence

After a successful release and before closing, ask:

`May I record this release evidence in memory_bank/t3_archive/release_evidence/release-[version].md and memory_bank/t0_core/release_state.md?`

When `memory_bank/` exists and the user approves, coordinate the release evidence
write through the same file write protocol.

- Write `memory_bank/t3_archive/release_evidence/release-[version].md`.
- If the release evidence file already exists, append a new timestamped evidence
  section instead of overwriting historical evidence.
- Record release version or tag, commit SHA, workflow run ID, workflow run URL,
  `ubuntu-latest`, `macos-latest`, and `windows-latest` job results,
  go/no-go decision, deployment status, and monitoring window.
- Update `memory_bank/t0_core/release_state.md` with latest release version,
  release status, evidence path, deployment state, and monitoring state.

If `memory_bank/` does not exist, do not create it from `/team-release`. Keep
the normal release output and say: "Run `/constitute` to establish the
memory_bank governance control plane."

## Output

A summary report covering: release version, scope, quality gate results, go/no-go decision, deployment status, and monitoring plan.

Verdict: **COMPLETE** — release executed and deployed.
Verdict: **BLOCKED** — release halted; go/no-go was NO or a hard blocker is unresolved.

## Next Steps

- Monitor post-release dashboards for 48 hours.
- Run `/retrospective` if significant issues occurred during the release.
- Keep `production/stage.txt` within the legitimate stages in `workflow/workflow-catalog.yaml`;
  deployment success alone does not authorize a stage transition. Record actual
  deployed/live status in the authorized release report or release-state fields.
  Any stage update requires its own scoped transition authority and valid gate evidence.
- When `memory_bank/` exists and evidence recording is approved, update
  `memory_bank/t0_core/release_state.md` and write or append
  `memory_bank/t3_archive/release_evidence/release-[version].md`.

---
name: team-live-ops
description: "Use when a season, event, or live content update needs coordinated design, economy, analytics, communication, writing, and narrative planning."
---

<!-- codex-studio-delegation: governed -->
Resolve every role through `../../../.codex/docs/plugin-agent-delegation.md`;
do not require a repository-local `.codex/agents/` or `.codex/agent-packs/` tree.
Before default delegation, run `python3 ../../../tools/codex_studio/agent_delegation.py resolve --project-root <project-root> --role <role>` and use only its returned role contract.

# Team Live Ops

## Codex Interaction Contract

- Ask one decision question per turn and wait for the answer before asking another.
- Use `request_user_input` for structured choices when it is available; otherwise ask the same concise question directly.
- Use Codex custom agents by role and profile when delegation is useful.
- Treat any approved write as one complete proposed changeset. Before writing, present every target path and material edit together; do not add unlisted files or behavior.
- A new path, expanded scope, or material change requires a revised complete proposed changeset and fresh approval.

## Invocation

Usage: `$team-live-ops [season name or event] [--review full|lean|solo]`. If the required objective cannot be inferred safely, ask for that single missing decision and wait; do not delegate yet.

## Review Mode

Read `.codex/studio.toml` as the only persistent review-mode source. Map `review_mode = "phase-gated"` to lean optional-review depth; mandatory director gates still run. A `--review` argument applies only to the current run. Use `../../../.codex/docs/director-gates.md` and `.codex/docs/technical-preferences.md` for native gate and engine context.

## Team Roster

- `live-ops-designer`
- `economy-designer`
- `analytics-engineer`
- `community-manager`
- `writer`
- `narrative-director`

## Delegation Plan

- Delegate only tasks that are independent and bounded.
- Name the Codex custom-agent role and the exact artifact or evidence it must return.
- Team members must not spawn additional agents (`agents.max_depth = 1`).
- The parent agent synthesizes all results, resolves overlap, and communicates with the user.
- No subagent commits, publishes, or expands scope.
- Parallel delegation is read-only or draft-only until the parent presents a consolidated result.
- Any multi-file implementation requires one complete changeset approval before work begins.
- If a delegated task blocks, surface the evidence and stop dependent work while preserving independent results.

## Pipeline

### Phase 1: Season/Event Scoping
Delegate to **live-ops-designer**:
- Define the season or event: type (seasonal, limited-time event, challenge), duration, theme direction
- Outline the content list: what's new (modes, items, challenges, story beats)
- Define the retention hook: what brings players back daily/weekly during this season
- Identify resource budget: how much new content needs to be created vs. reused
- Output: season brief with scope, content list, and retention mechanic overview

### Phase 2: Narrative Theme
Delegate to **narrative-director**:
- Read the season brief from Phase 1
- Design the seasonal narrative theme: how does this event connect to the game world?
- Define the central story hook players will discover during the event
- Identify which existing lore threads this season can advance
- Output: narrative framing document (theme, story hook, lore connections)

### Phase 3: Economy Design (parallel with Phase 2 if theme is clear)
Delegate to **economy-designer**:
- Read the season brief and existing economy rules from `design/live-ops/economy-rules.md`
- Design the reward track: free tier progression, premium tier value proposition
- Plan the in-season economy: seasonal currency, store rotation, pricing
- Define pity timer mechanics and bad-luck protection for any random elements
- Verify no pay-to-win items in premium track
- Output: economy design doc with reward tables, pricing, and currency flow

### Phase 4: Analytics and Success Metrics (parallel with Phase 3)
Delegate to **analytics-engineer**:
- Read the season brief
- Define success metrics: participation rate target, retention lift target, battle pass completion rate
- Design any A/B tests to run during the season (e.g., different reward cadences)
- Specify new telemetry events needed for this season's content
- Output: analytics plan with success criteria and instrumentation requirements

### Phase 5: Content Writing (parallel)
Delegate in parallel:
- **narrative-director** (if needed): Write any in-game narrative text (cutscene scripts, NPC dialogue, world event descriptions) for the season
- **writer**: Write all player-facing text — event names, reward item descriptions, challenge objective text, seasonal flavor text
- Both should read the narrative framing doc from Phase 2

### Phase 6: Player Communication Plan
Delegate to **community-manager**:
- Read the season brief, economy design, and narrative framing
- Draft the season launch announcement (tone, key highlights, platform-specific versions)
- Plan the communication cadence: pre-launch teaser, launch day post, mid-season reminder, final week FOMO push
- Draft known-issues section placeholder for day-1 patch notes
- Output: communication calendar with draft copy for each touchpoint

### Phase 7: Review and Sign-off
Collect outputs from all phases and present a consolidated season plan:
- Season brief (Phase 1)
- Narrative framing (Phase 2)
- Economy design and reward tables (Phase 3)
- Analytics plan and success metrics (Phase 4)
- Written content inventory (Phase 5)
- Communication calendar (Phase 6)

Present a summary to the user with:
- **Content scope**: what is being created
- **Economy health check**: does the reward track feel fair and non-predatory?
- **Analytics readiness**: are success criteria defined and instrumented?
- **Ethics review**: check the Phase 3 economy design against `design/live-ops/ethics-policy.md`
  - If the file does not exist: flag "ETHICS REVIEW SKIPPED: `design/live-ops/ethics-policy.md` not found. Economy design was not reviewed against an ethics policy. Recommend creating one before production begins." Include this flag in the season design output document. Add to next steps: create `design/live-ops/ethics-policy.md`.
  - If the file exists and a violation is found: flag "ETHICS FLAG: [element] in Phase 3 economy design violates [policy rule]. Approval is blocked until this is resolved." Do NOT issue a COMPLETE verdict or write output documents. Use `request_user_input` with options: revise economy design / override with documented rationale / cancel. If user chooses to revise: re-delegate to economy-designer to produce a corrected design, then return to Phase 7 review. If user selects Cancel: end with Verdict: BLOCKED — "Live ops design cancelled due to unresolved ethics violation. Resolve the flagged issues and re-run $team-live-ops."
- **Open questions**: decisions still needed before production begins

Ask the user to approve the season plan before delegating to production teams. Issue the COMPLETE verdict only after the user approves and no unresolved ethics violations remain. If an ethics violation is unresolved, end with Verdict: **BLOCKED**.

## Output Documents

All documents save to `design/live-ops/`:
- `seasons/S[N]_[name].md` — Season design document (from Phase 1-3)
- `seasons/S[N]_[name]_analytics.md` — Analytics plan (from Phase 4)
- `seasons/S[N]_[name]_comms.md` — Communication calendar (from Phase 6)

## Error Recovery Protocol

If any delegated agent (through Codex custom-agent delegation) returns BLOCKED, errors, or cannot complete:

1. **Surface immediately**: Report "[AgentName]: BLOCKED — [reason]" to the user before continuing to dependent phases
2. **Assess dependencies**: Check whether the blocked agent's output is required by subsequent phases. If yes, do not proceed past that dependency point without user input.
3. **Offer options** via request_user_input with choices:
   - Skip this agent and note the gap in the final report
   - Retry with narrower scope
   - Stop here and resolve the blocker first
4. **Always produce a partial report** — output whatever was completed. Never discard work because one agent blocked.

If a BLOCKED state is unresolvable, end with Verdict: **BLOCKED** instead of COMPLETE.

## Changeset Gate

Delegated agents return drafts or read-only evidence to the parent. The parent synthesizes every proposed edit, lists all affected paths and material changes, and requests one complete changeset approval. After approval, implementation stays within that boundary; any expansion pauses for a revised approval.
## Output

A summary covering: season theme and scope, economy design highlights, success metrics, content list, communication plan, and any open decisions needing user input before production.

Verdict: **COMPLETE** — season plan produced and handed off for production.

## Next Steps

- Run `$design-review` on the season design document for consistency validation.
- Run `$sprint-plan` to schedule content creation work for the season.
- Run `$team-release` when the season content is ready to deploy.

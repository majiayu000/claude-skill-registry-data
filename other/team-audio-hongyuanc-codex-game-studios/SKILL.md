---
name: team-audio
description: "Use when an audio feature needs coordinated direction, sound design, technical integration, and gameplay hooks."
---

<!-- codex-studio-delegation: governed -->
Resolve every role through `../../../.codex/docs/plugin-agent-delegation.md`;
do not require a repository-local `.codex/agents/` or `.codex/agent-packs/` tree.
Before default delegation, run `python3 ../../../tools/codex_studio/agent_delegation.py resolve --project-root <project-root> --role <role>` and use only its returned role contract.

# Team Audio

## Codex Interaction Contract

- Ask one decision question per turn and wait for the answer before asking another.
- Use `request_user_input` for structured choices when it is available; otherwise ask the same concise question directly.
- Use Codex custom agents by role and profile when delegation is useful.
- Treat any approved write as one complete proposed changeset. Before writing, present every target path and material edit together; do not add unlisted files or behavior.
- A new path, expanded scope, or material change requires a revised complete proposed changeset and fresh approval.

## Invocation

Usage: `$team-audio [feature or area] [--review full|lean|solo]`. If the required objective cannot be inferred safely, ask for that single missing decision and wait; do not delegate yet.

## Review Mode

Read `.codex/studio.toml` as the only persistent review-mode source. Map `review_mode = "phase-gated"` to lean optional-review depth; mandatory director gates still run. A `--review` argument applies only to the current run. Use `../../../.codex/docs/director-gates.md` and `.codex/docs/technical-preferences.md` for native gate and engine context.

## Team Roster

- `audio-director`
- `sound-designer`
- `technical-artist`
- `gameplay-programmer`

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

Every phase before `## Parent Changeset Gate` is read-only or draft-only. Phase 1 returns direction notes; no agent writes files or implementation.

### Step 1: Audio Direction (audio-director)
Delegate to the `audio-director` agent to:
- Define the sonic identity for this feature/area
- Specify the emotional tone and audio palette
- Set music direction (adaptive layers, stems, transitions)
- Define audio priorities and mix targets
- Establish any adaptive audio rules (combat intensity, exploration, tension)

### Step 2: Sound Design and Audio Accessibility (parallel)
Delegate to the `sound-designer` agent to:
- Create detailed SFX specifications for every audio event
- Define sound categories (ambient, UI, gameplay, music, dialogue)
- Specify per-sound parameters (volume range, pitch variation, attenuation)
- Plan audio event list with trigger conditions
- Define mixing groups and ducking rules

Delegate to the `sound-designer` agent in parallel to:
- Identify which audio events carry critical gameplay information (damage received, enemy nearby, objective complete) and require visual alternatives for hearing-impaired players
- Specify subtitle requirements: which audio events need captions, what text format, on-screen duration
- Check that no gameplay state is communicated by audio alone (all must have a visual fallback)
- Review the audio event list for any that could cause issues for players with auditory sensitivities (high-frequency alerts, sudden loud events)
- Output: audio accessibility requirements list integrated into the audio event spec

### Step 3: Technical Plan (draft-only, parallel)
Delegate to the `technical-artist` agent to:
- Design the audio middleware integration (Wwise/FMOD/native)
- Define audio bus structure and routing
- Specify memory budgets for audio assets per platform
- Plan streaming vs preloaded asset strategy
- Design any audio-reactive visual effects

Have `technical-artist` also read the configured Engine Specialists guidance in `.codex/docs/technical-preferences.md` and validate the integration approach:
- Is the proposed audio middleware integration idiomatic for the engine? (e.g., Godot's built-in AudioStreamPlayer vs FMOD, Unity's Audio Mixer vs Wwise, Unreal's MetaSounds vs FMOD)
- Any engine-specific audio node/component patterns that should be used?
- Known audio system changes in the pinned engine version that affect the integration plan?
- Output: engine audio integration notes merged into the technical-artist's plan

If no engine is configured, mark the engine-specific subsection N/A.

## Parent Changeset Gate

The parent synthesizes all direction, asset, technical, and code-plan drafts before any mutation. Present one complete proposal containing exact file paths, exact diffs, tests and evidence, and all session-state, report, and milestone writes (use `None` where no such write exists). Obtain approval for the whole changeset; a new path or material change requires a revised proposal.

## Approved Execution

Only after approval may the parent execute or delegate the exact approved changes. No subagent commits, publishes, or expands scope. Every delegate receives only its approved paths, diffs, tests, and acceptance criteria.

### Step 4: Code Integration (gameplay-programmer)
Delegate to the `gameplay-programmer` agent to:
- Implement audio manager system or review existing
- Wire up audio events to gameplay triggers
- Implement adaptive music system (if specified)
- Set up audio occlusion/reverb zones
- Write unit tests for audio event triggers

4. **Compile the audio design document** combining all team outputs.

5. **Save to** `design/audio/audio-[feature].md`.

   Note: If `design/audio/` does not exist, the sub-agent writing the document should create it (the directory will be created automatically when the file is written).

6. **Output a summary** with: audio event count, estimated asset count,
   implementation tasks, and any open questions between team members.

Verdict: **COMPLETE** — audio design document produced and team pipeline finished.

If the pipeline stops because a dependency is unresolved (e.g., critical accessibility gap or missing GDD not resolved by the user):

Verdict: **BLOCKED** — [reason]

## Next Steps

- Review the audio design doc with the audio-director before implementation begins.
- Use `$dev-story` to implement the audio manager and event system once the design is approved.
- Run `$asset-audit` after audio assets are created to verify naming and format compliance.

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

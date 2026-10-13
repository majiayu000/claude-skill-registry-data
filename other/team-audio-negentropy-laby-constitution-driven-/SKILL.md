---
name: team-audio
description: "Orchestrate feedback-signal work. Game: audio-director + sound-designer + technical-artist + gameplay-programmer for audio pipeline. Product: notification/status feedback, accessibility alternatives, UI/CLI/API feedback copy, telemetry events, and implementation handoff."
argument-hint: "[feature or area to design audio for]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit, Bash, Task, AskUserQuestion, TodoWrite
---

## User Guide

- When to use: Orchestrate feedback-signal work. Game: audio-director + sound-designer + technical-artist + gameplay-programmer for audio pipeline. Product: notification/status feedback, accessibility alternatives, UI/CLI/API feedback copy, telemetry events, and implementation handoff.
- Inputs: Command arguments: `/team-audio [feature or area to design audio for]`; project artifacts referenced below; user decisions and approvals before writes.
- Outputs: Primary artifacts, reports, or conversation guidance described below; write files only after user approval.
- Memory-bank writes: None.
- Next steps: Follow the workflow hand-off or next-step guidance below; recommendations do not auto-run and require explicit user command/approval.

## Phase 0: Domain Routing

Detect the project domain before orchestrating the team:
- `design/cdd/game-concept.md` -> **[Game]** keep the existing audio team workflow for music, SFX, adaptive audio, engine integration, and gameplay feedback.
- `design/cdd/product-concept.md` -> **[Product]** use this command for product feedback-signal orchestration: notification sounds if applicable, status/alert semantics, accessibility alternatives, UI/CLI/API feedback copy, telemetry events, and implementation handoff.
- If unclear, ask whether the feature needs game audio work or product feedback/notification design.

Do not remove game audio examples. Product feedback-signal guidance is added beside them.
If no argument is provided, output usage guidance and exit without spawning any agents:
> Usage: `/team-audio [feature or area]` — specify the feature or area to design audio for (e.g., `combat`, `main menu`, `forest biome`, `boss encounter`). Do not use `AskUserQuestion` here; output the guidance directly.

When this skill is invoked with an argument, orchestrate the audio team through a structured pipeline.

**Decision Points:** At each step transition, use `AskUserQuestion` to present
the user with the subagent's proposals as selectable options. Write the agent's
full analysis in conversation, then capture the decision with concise labels.
The user must approve before moving to the next step.

1. **Read the argument** for the target feature or area (e.g., `combat`,
   `main menu`, `forest biome`, `boss encounter`).

2. **Gather context**:
   - Read relevant design docs in `design/cdd/` for the feature
   - Read the sound bible at `design/cdd/sound-bible.md` if it exists
   - Read existing audio asset lists in `assets/audio/`
   - Read any existing sound design docs for this area

## How to Delegate

Use the Task tool to spawn each team member as a subagent:
- `subagent_type: audio-director` — Sonic identity, emotional tone, audio palette
- `subagent_type: sound-designer` — SFX specifications, audio events, mixing groups
- `subagent_type: technical-artist` — Audio middleware, bus structure, memory budgets
- `subagent_type: [primary engine specialist]` — Validate audio integration patterns for the engine
- `subagent_type: gameplay-programmer` — Audio manager, gameplay triggers, adaptive music

Always provide full context in each agent's prompt (feature description, existing audio assets, design doc references).

## Product Feedback-Signal Team Composition

When the Product branch is active, use this same command to orchestrate user and
developer feedback signals. Do not spawn game audio agents unless the product
actually includes sound or media feedback.

- `ux-designer` — status semantics, notification timing, empty/error states, user workflow clarity
- `accessibility-specialist` — non-audio alternatives, screen-reader behavior, reduced motion, cognitive load, inclusive status language
- `lead-programmer` — implementation boundary, event model, API/CLI/UI contract, telemetry and state ownership
- `language specialist` — stack-specific implementation notes from `standards/technical-preferences.md`
- `analytics-engineer` — telemetry event names, funnels, alert thresholds, and adoption/retention measurement when relevant
- `qa-tester` — evidence plan for status messages, notifications, API/CLI errors, telemetry, and accessibility fallbacks

**Product context reads:**
- `design/cdd/product-concept.md` for Product promise, JTBD, primary workflow, target user, and platform
- Relevant module CDDs and UX specs in `design/cdd/` and `design/ux/`
- `standards/technical-preferences.md` for language/framework and routing
- ADRs that define events, logging, telemetry, notifications, UI state, API errors, or CLI output
- Existing docs/examples, support notes, release notes, and QA evidence for the target workflow

3. **Orchestrate the audio team** in sequence:

### Step 1: Audio Direction (audio-director)
Spawn the `audio-director` agent to:
- Define the sonic identity for this feature/area
- Specify the emotional tone and audio palette
- Set music direction (adaptive layers, stems, transitions)
- Define audio priorities and mix targets
- Establish any adaptive audio rules (combat intensity, exploration, tension)

### Step 2: Sound Design and Audio Accessibility (parallel)
Spawn the `sound-designer` agent to:
- Create detailed SFX specifications for every audio event
- Define sound categories (ambient, UI, gameplay, music, dialogue)
- Specify per-sound parameters (volume range, pitch variation, attenuation)
- Plan audio event list with trigger conditions
- Define mixing groups and ducking rules

Spawn the `accessibility-specialist` agent in parallel to:
- Identify which audio events carry critical gameplay information (damage received, enemy nearby, objective complete) and require visual alternatives for hearing-impaired players
- Specify subtitle requirements: which audio events need captions, what text format, on-screen duration
- Check that no gameplay state is communicated by audio alone (all must have a visual fallback)
- Review the audio event list for any that could cause issues for players with auditory sensitivities (high-frequency alerts, sudden loud events)
- Output: audio accessibility requirements list integrated into the audio event spec

### Step 3: Technical Implementation (parallel)
Spawn the `technical-artist` agent to:
- Design the audio middleware integration (Wwise/FMOD/native)
- Define audio bus structure and routing
- Specify memory budgets for audio assets per platform
- Plan streaming vs preloaded asset strategy
- Design any audio-reactive visual effects

Spawn the **primary engine specialist** in parallel (from `standards/technical-preferences.md` Engine Specialists) to validate the integration approach:
- Is the proposed audio middleware integration idiomatic for the engine? (e.g., Godot's built-in AudioStreamPlayer vs FMOD, Unity's Audio Mixer vs Wwise, Unreal's MetaSounds vs FMOD)
- Any engine-specific audio node/component patterns that should be used?
- Known audio system changes in the pinned engine version that affect the integration plan?
- Output: engine audio integration notes to merge with the technical-artist's plan

If no engine is configured, skip the specialist spawn.

### Step 4: Code Integration (gameplay-programmer)
Spawn the `gameplay-programmer` agent to:
- Implement audio manager system or review existing
- Wire up audio events to gameplay triggers
- Implement adaptive music system (if specified)
- Set up audio occlusion/reverb zones
- Write unit tests for audio event triggers

## Product Pipeline

Use this pipeline instead of the game audio pipeline when the target is a Product
notification/status/API/CLI feedback surface.

### Product Step 1: Feedback Direction

Spawn `ux-designer` to:
- Define the user/developer state being communicated.
- Classify each signal: success, warning, error, progress, blocking action, background completion, alert, or informational.
- Specify the preferred channel: inline text, toast, banner, modal, CLI stdout, CLI stderr, API error body, webhook, email, docs note, or telemetry-only event.
- Define tone and timing rules that match the Product promise.

### Product Step 2: Accessibility and Copy Review (parallel)

Spawn `accessibility-specialist` and, where text is substantial, `localization-lead` in parallel:
- Confirm that sound, color, animation, or timing is never the only signal.
- Define screen-reader announcements and reduced-motion behavior for UI products.
- Define CLI/API error readability, copy length, placeholder format, and localization headroom.
- Flag ambiguous or blameful messages that would damage user trust.

### Product Step 3: Implementation and Telemetry Design (parallel)

Spawn `lead-programmer`, the relevant language specialist, and `analytics-engineer` where telemetry is part of the signal:
- Define state ownership and event names.
- Specify API/CLI/UI integration boundaries.
- Confirm logging/telemetry privacy and observability rules.
- Identify stack-specific implementation risks.

### Product Step 4: QA Evidence

Spawn `qa-tester` to:
- Build a Product feedback-signal test checklist covering success, failure, retry, permission denied, invalid config, migration/deployment error, and recovery paths.
- Include accessibility and localization checks where the signal is user-facing.
- Require evidence in `production/qa/evidence/` before final sign-off.

4. **Compile the audio design document** combining all team outputs.

5. **Save to** `design/cdd/audio-[feature].md`.

6. **Output a summary** with: audio event count, estimated asset count,
   implementation tasks, and any open questions between team members.

For Product projects, compile `design/ux/feedback-signals-[feature].md` or the
module CDD feedback section instead. Output: signal count, affected product
surfaces, implementation tasks, telemetry events, QA evidence needed, and open
questions.

Verdict: **COMPLETE** — audio design document produced and team pipeline finished.

If the pipeline stops because a dependency is unresolved (e.g., critical accessibility gap or missing CDD not resolved by the user):

Verdict: **BLOCKED** — [reason]

## File Write Protocol

All file writes (audio design docs, SFX specs, implementation files) are delegated
to sub-agents spawned via Task. Each sub-agent enforces the "May I write to [path]?"
protocol. This orchestrator does not write files directly.

## Next Steps

- Review the audio design doc with the audio-director before implementation begins.
- Use `/dev-story` to implement the audio manager and event system once the design is approved.
- Run `/asset-audit` after audio assets are created to verify naming and format compliance.

**[Product] Product next steps:**
- Run `/ux-review` on the feedback-signal UX spec if it affects UI or CLI flow.
- Run `/code-review` on implementation that changes API/CLI/UI error contracts, telemetry, logging, or notification behavior.
- Run `/test-evidence-review` on evidence for status, error, telemetry, accessibility, and localization behavior before closing the story.

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

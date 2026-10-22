---
name: game-gmt-review
description: Review, diagnose, and validate game design proposals with the GMT framework (Goal-Means-Tools). Use when Codex needs to inspect a game concept, feature spec, gameplay loop, level/system proposal, pitch deck, or design document for whether player goals, experience goals, design goals, means, and tools are clearly defined, logically connected, complete, balanced, and feasible.
---

# Game GMT Review

## Overview

Use this skill to review a game design proposal through GMT: Goal, Means, Tools. Treat GMT as an analysis framework, not a rigid pass/fail doctrine. Identify whether the proposal distinguishes player goals, experience goals, and design goals; whether each goal is supported by suitable means and concrete tools; and where the design has gaps, contradictions, weak links, or unproven assumptions.

Read `references/gmt-framework.md` before performing a substantive review. Use `references/review-output.md` when the user asks for a formal report, review memo, scoring table, or actionable recommendations.

## Review Workflow

1. Extract the proposal's stated and implied goals.
   - Separate player goals, experience goals, and design goals.
   - Mark goals as stated, inferred, missing, or ambiguous.
   - Do not force the three goal types to align automatically; note whether their relationship is intentional, weak, absent, or contradictory.

2. Build the GMT map.
   - For player GMT, map player goals to high-level means such as strategy, tactics, operation, exploration, resource management, traversal, social cooperation, puzzle solving, collection, optimization, survival, or creation.
   - For experience GMT, map experience goals to means such as interaction, sensory presentation, narrative, worldbuilding, theme, structure, aesthetic tone, genre convention, pacing, and content organization.
   - For each means, list concrete tools: rules, controls, 3C, level design, AI, abilities, feedback, UI, economy, enemies, missions, art, animation, audio, story beats, production assets, and progression systems.

3. Test goal-means-tool logic.
   - Check whether each goal has sufficient means.
   - Check whether each means has concrete tools.
   - Check whether each tool actually supports the claimed means and goal.
   - Flag orphan tools, ornamental mechanics, under-supported goals, and means that are too vague to guide implementation.

4. Evaluate player GMT.
   - Review clarity, learnability, novelty, system integrity, balance, synergy, complexity, agency, and phase changes.
   - Distinguish mechanical problems from experiential problems. A playable loop can still fail the intended experience.

5. Evaluate experience GMT.
   - Review whether the proposed means and tools can plausibly create the intended emotion, fantasy, tension, identity, learning, culture, theme, or aesthetic response.
   - Check directness, purity, uniqueness, execution quality, production feasibility, and audience fit.
   - Treat subjective experience carefully: give evidence, assumptions, and likely failure modes rather than pretending to prove emotional outcomes.

6. Diagnose and recommend.
   - Prioritize issues that break the core goal chain.
   - Separate must-fix logic gaps from optional opportunities.
   - Recommend either revising goals, changing means, adding/removing tools, or clarifying design intent.
   - When information is missing, state the exact question needed to complete the GMT map.

## Review Stance

- Do not assume a design is bad because player goals, experience goals, and design goals are weakly related. Weak or absent relation can be valid if intentional and supported.
- Do not praise a design only because the three goal types appear aligned. Alignment still needs concrete tools, execution quality, and production capacity.
- Do not collapse means and tools into one flat list. Keep means high-level and tools concrete.
- Do not use GMT to replace genre expertise, market research, usability testing, or playtest evidence. Use it to structure design reasoning and expose assumptions.
- Prefer precise, actionable findings over generic advice such as "make it more fun" or "improve feedback."

## Common User Requests

- "用 GMT 检查这个游戏策划案。"
- "帮我验证这个玩法是否满足 GMT 理论。"
- "这个系统的玩家目标、体验目标、设计目标是否一致？"
- "帮我找出这个玩法设计里目标和手段脱节的地方。"
- "把这个 pitch deck 按 GMT 做一份评审报告。"
- "用 GMT 反推这个玩法需要哪些工具和实现要素。"

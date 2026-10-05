---
name: simulate-elite-experts
description: |
  通过模拟相关领域顶级专家的思考、分歧与收敛，辅助高复杂度、高风险决策。
  用于用户要求模拟顶尖人物、比较强势观点，或询问“应该找哪些优秀人物来讨论某个问题，以及他们可能会怎么说”。
  适用于“用世界级专家视角思考”“模拟顶级领域专家”“扮演最强领域人物”和“使用四视角对话”等请求。
---

# Simulate Elite Experts

## 中文介绍

`simulate-elite-experts` 用于处理高复杂度、高不确定性或较难逆转的决策问题。它不是普通的“专家角色扮演”，而是一个带硬约束的四视角推理框架：选择两位与问题直接相关、可从公开作品推断方法论的真实人物，再加入一个领域专家抽象角色和一个全知智能体抽象角色，让它们围绕同一决策进行立场陈述、交叉质询、修正和综合。

适合使用的场景：
- 需要比较多个强观点，而不是只要一个直接答案。
- 决策涉及速度、质量、风险、成本、组织、伦理等多重约束。
- 用户希望知道“应该找哪些顶级人物/视角来讨论这个问题，以及他们可能会怎么说”。

不适合用于简单事实查询、单一正确答案、低成本可逆选择或纯情绪支持。输出必须区分事实、假设和推测；对真实人物的观点只能基于公开资料做模拟推断，不能伪造直接引语、私人意图或未验证事实。

## Applicability Pre-Check (Gate 0)

Before running the full framework, evaluate 3 dimensions to decide whether this tool is appropriate:

1. **Complexity**: Does the problem involve multiple stakeholders, competing constraints, or non-obvious tradeoffs?
   - Yes (score 1) → proceed.
   - No (score 0) → consider skipping; a direct answer may suffice.

2. **Reversibility**: Is the decision hard to reverse once made?
   - Hard to reverse (score 1) → proceed; structured deliberation is valuable.
   - Easy to reverse (score 0) → consider skipping; low-cost decisions rarely need multi-lens analysis.

3. **Information ambiguity**: Is there significant uncertainty about facts, outcomes, or stakeholder preferences?
   - High ambiguity (score 1) → proceed; the framework surfaces hidden assumptions.
   - Low ambiguity (score 0) → consider skipping; the answer may already be clear.

**Decision rule**:
- Total >= 2 → use the full framework.
- Total = 1 → offer the user a choice between `micro` (lightweight) and full framework.
- Total = 0 → recommend skipping; inform the user this question is better answered directly.

If the user explicitly requests the framework regardless of score, proceed but note the pre-check result.

## Execution Mode Selection

Choose the execution mode before building the roster:

- `one-shot` (default): Produce the complete output in one response. Use this when the user asks for an analysis, report, comparison, or direct recommendation and has not asked to co-design the panel.
- `interactive`: Produce Section 1 only, ask the user to confirm or swap the roster, then wait before running dialogue rounds. Use this when the user explicitly asks to choose experts, workshop the panel, or collaborate step by step.
- `blind-spot-gated` (opt-in overlay): Run the candidate deliberation, then perform a clean-context outside audit across 5 failure categories (hidden assumptions, wrong framing, omitted alternatives, second-order effects, simpler paths) evaluated by a materiality gate. If `material: true`, trigger a single-shot re-entry to revise the decision before final delivery. Use this only when explicitly requested (e.g. `--blind-spot-gated` or asking for "gated audit").

Rules:
- Do not pause after Section 1 in `one-shot` mode.
- Do not continue past Section 1 in `interactive` mode until the user confirms or revises the roster.
- `blind-spot-gated` is strictly opt-in; it must never be the implicit default for standard queries or execution tasks.
- If profile and execution mode conflict with token or time constraints, preserve the profile's required section/round counts and compress content rather than dropping structure.

## When NOT to Use This Framework

Do not use (or actively recommend against using) this framework for:
- **Simple factual queries**: "What is the capital of France?" — no perspectives needed.
- **Single-correct-answer problems**: "Fix this syntax error" — no tradeoff to explore.
- **Urgent time-critical decisions**: When seconds matter, structured deliberation adds harmful delay.
- **Trivial reversible choices**: Low-stakes decisions where the cost of being wrong is negligible.
- **Pure emotional support**: When the user needs empathy, not analysis.

If the user's question falls into these categories, briefly explain why and offer a direct answer instead.

## Context Grounding Pass

Before selecting real people, check whether the decision is grounded in a project, repository, document, dataset, or current external facts:

- For local project/repository decisions, read the most relevant current context first (for example `AGENTS.md`, `CLAUDE.md`, README, design docs, or files named by the user). Keep this pass narrow: usually 1-3 files.
- For current or time-sensitive public facts about real people, companies, regulations, models, or products, verify with current sources before using them as evidence anchors.
- If no grounded context is available, state the missing context as an assumption in Section 1 and include it in the Uncertainty Ledger.

Do not invent project facts, current facts, or source-backed claims. If evidence was not checked in the current turn, label the anchor as a known public anchor rather than a verified current source.

## Core Principle

Treat the model as a viewpoint simulator, not as one stable persona.
Use a fixed four-lens dialogue to answer two core questions:
1) What would be a good group of people to explore X?
2) What would they say?

## Fixed Four-Lens Composition (Hard Constraint)

For `classic`, `lean`, and `deep` profiles, always use exactly four roles:
1. Real Person A (specific real person)
2. Real Person B (specific real person)
3. Domain Expert Archetype (abstract role)
4. Omniscient Agent Archetype (abstract role)

For `micro` profile, use exactly two roles:
1. Real Person A (specific real person)
2. Domain Expert Archetype (abstract role)

Mandatory rules:
- Real Person roles must be concrete, real, named people (not fictional).
- Domain Expert Archetype must be an abstract domain expert role.
- Omniscient Agent Archetype (when present) must be an abstract omniscient intelligence role.
- Role counts and round counts must match the active profile.
- Do not replace this structure with generic "Expert A/B/C" panels.

## Real-Person Selection Criteria (Hard Constraint)

For Real Person A and Real Person B, satisfy all criteria:
- Domain relevance: each person must have direct, public work related to the current problem.
- Public-method traceability: each person must have published ideas, frameworks, or decisions that can be inferred.
- Decision-pressure diversity: the two real people must represent different pressures (for example: product speed vs reliability, science vs operations).
- Time relevance: avoid historically famous but currently irrelevant picks unless historical framing is explicitly required.

For each real person, include:
- Selection rationale in one sentence.
- 2-3 public evidence anchors (for example: known books, talks, essays, open-source work, or widely known decision patterns).

Do not pick real people only for fame value.
Do not claim exact quotes unless quoted from a source in the current turn.

## Inference Confidence Annotation

For every statement attributed to a real person (Real Person A/B), append an inline confidence tag:
- `[confidence: high]` — the viewpoint closely follows the person's published framework, methods, or repeated public positions.
- `[confidence: medium]` — the viewpoint is a reasonable extrapolation from the person's known work, but not directly stated by them.
- `[confidence: low]` — the viewpoint is speculative; the person has not publicly addressed this specific topic.

Rules:
- Confidence tags are mandatory for Real Person A/B in every dialogue round.
- Confidence tags are not required for abstract roles (Domain Expert Archetype, Omniscient Agent Archetype).
- If a real person's confidence drops to `low` in a round, briefly note why (e.g., "topic outside their published scope").

## Real-Person Scoring Matrix (Guardrail)

Before finalizing Real Person A/B, score candidates with this matrix.

Per-person dimensions:
- Domain relevance (0-2)
- Public-method traceability (0-2)
- Time relevance (0-2)

Pair dimension:
- Decision-pressure diversity (0-2, pair-level only)

Passing rules:
- Real Person A score >= 5/6.
- Real Person B score >= 5/6.
- Pair diversity score >= 2/2.
- If any rule fails, rerun candidate selection and mark `low-confidence roster` if no better pair is available.

## Roster Diversity Matrix (Anti-Groupthink Guardrail)

After selecting the four-lens roster, score the full roster:

- Real-person pressure diversity (0-2): Do A and B represent materially different decision pressures?
- Archetype coverage (0-2): Does the domain expert cover implementation/accountability constraints not covered by A/B?
- System-risk coverage (0-2): Does the omniscient agent cover second-order effects, failure modes, and hidden coupling?

Passing rules:
- Total roster diversity score must be >= 5/6 for `classic`, `lean`, and `deep`.
- `micro` must score the real person and domain expert coverage only; passing threshold is >= 3/4.
- If the score fails, revise the roster or mark `low-diversity roster` and explain the consequence in Section 1.

## Fallback Strategy (When Real-Person Selection Is Unclear)

Use this deterministic fallback order:
1. If user names real people, use them unless unsafe or clearly irrelevant.
2. If user gives domain but no names, propose three candidate real-person pairs and pick the best pair with rationale.
3. If confidence in pair quality is below 0.6, ask user to select one pair before continuing.
4. If user does not choose, proceed with the best pair and explicitly mark `low-confidence roster`.

Never replace Real Person A/B with fictional characters.
Never collapse to only abstract roles.

## Simulation Safety Rules

- For real people, clearly mark outputs as simulated viewpoints inferred from public work.
- Do not claim private access, private intent, or exact quotes.
- Keep analysis decision-oriented, falsifiable, and domain-specific.

## Rolling Uncertainty Tracker

Uncertainty tracking is not limited to the final ledger. Apply rolling updates:
- After Round 1: tag each initial position with its evidence basis (`fact`, `assumption`, or `speculation`).
- After Round 2: record any assumptions that were challenged and whether they survived cross-examination.
- After Round 3: note which revised positions introduced new assumptions or resolved old ones.
- The final Uncertainty Ledger consolidates the rolling tracker into a clean summary.

This ensures uncertainty is visible throughout the dialogue, not hidden until the end.

## Anonymous Meta-Review (Internal Anti-Convergence Step)

Before writing Moderator Synthesis, run an internal blind review:

1. Temporarily anonymize the active role positions as Position A/B/C/D (or A/B for `micro`).
2. Identify the strongest argument, weakest assumption, missing stakeholder, and most dangerous shared blind spot.
3. Use the result to revise Moderator Synthesis and Uncertainty Ledger.

Do not output the anonymized transcript unless the user asks for a process trace. Do output the resulting challenge in the synthesis when it changes the recommendation, warning indicators, or evidence-needed list.

## Output Contract Guardrail (Hard Constraint)

Section and round counts depend on the active profile:
- `micro`: exactly 5 sections, 2 roles, 2 rounds (4 turns total).
- `lean`: exactly 7 sections, 4 roles, 4 rounds (same as classic, but turns compressed to 1-3 sentences).
- `classic`: exactly 7 sections, 4 roles, 4 rounds (16 turns total).
- `deep`: exactly 9 sections, 4 roles, 6 rounds (24 turns total).

Do not add extra top-level sections beyond the profile's contract.
Each dialogue round must contain one turn from each active role.

Preflight checklist (internal; do not output verbatim):
1. Role composition matches selected profile.
2. Real-person scoring matrix passes.
3. Evidence anchors are present for all real people.
4. Full roster diversity passes or is explicitly marked `low-diversity roster`.
5. Execution mode is clear (`one-shot` or `interactive`).
6. Section count matches profile contract exactly.
7. Each round has turns from all active roles.
8. Inference confidence tags are present for all real-person turns.

Postflight checklist (internal; do not output verbatim):
1. No fabricated direct quotes for real people.
2. Moderator synthesis includes recommendation, strongest alternative, preconditions, early warnings, and next actions.
3. Uncertainty ledger cleanly separates facts, assumptions, and speculation.
4. Anonymous meta-review did not reveal an unaddressed blind spot.

## Failure Modes and Recovery Actions

- FM1: Fame-first roster with weak relevance.
  - Recovery: rerank candidates using the scoring matrix; replace weakest candidate.
- FM2: Dialogue turns collapse into agreement too early.
  - Recovery: enforce at least one direct challenge per role in Round 2.
- FM3: Missing or malformed section structure.
  - Recovery: regenerate with strict 7-section scaffold first, then fill content.
- FM4: Actionability gap in synthesis.
  - Recovery: add time horizon, trigger indicators, and 1-3 concrete next actions.
- FM5: Speculation leakage.
  - Recovery: move uncertain claims to Uncertainty Ledger and add evidence-needed items.
- FM6: One-shot output accidentally pauses after roster.
  - Recovery: continue with the remaining required sections unless `interactive` mode was explicitly selected.
- FM7: Groupthink from similar real-person selections.
  - Recovery: replace one real person or the domain archetype to represent a distinct pressure, then rerun roster scoring.
- FM8: Local or current context ignored.
  - Recovery: read the narrow relevant context, update the decision frame, and move unsupported claims into assumptions.

## Controlled Execution Profiles (Structure-Preserving)

Profiles adjust depth and structure according to problem complexity.

- `micro`: 2 roles (1 real person + 1 domain expert archetype), 2 dialogue rounds (initial + final), 5 output sections. Use for medium-complexity problems or when pre-check score = 1.
- `lean`: 4 roles, 4 dialogue rounds, 7 sections (same structure as classic). Compress each turn to 1-3 sentences for low-token contexts.
- `classic` (default): 4 roles, 4 dialogue rounds, balanced detail and readability.
- `deep`: 4 roles, 6 dialogue rounds, 9 sections. Adds metrics, counterarguments, failure triggers, stress test, and contingency planning.

Profile round rules:
- `micro`: exactly 2 rounds (initial positions + final statements).
- `lean` and `classic`: exactly 4 rounds (initial positions, cross-examination, revised positions, final statements).
- `deep`: exactly 6 rounds, adding stress test and contingency planning after the classic rounds.
- Each round always includes one turn from every active role.

Profile selection:
- If user specifies a profile, use it.
- If user does not specify, use `classic`.
- If applicability pre-check score = 1, suggest `micro` or `lean`.

### Micro Profile Output Sections

1. Good Group To Explore X (Two-Lens Roster)
2. Dialogue Round 1: Initial Positions
3. Dialogue Round 2: Final Statements
4. Moderator Synthesis
5. Uncertainty Ledger

### Deep Profile Additional Rounds

- Round 5: Stress Test — each role describes the scenario where their recommendation fails catastrophically.
- Round 6: Contingency Planning — each role proposes a fallback plan triggered by Round 5 failure scenarios.

## Required Output Sections (By Profile)

### Classic (default) — 7 sections:
1. Good Group To Explore X (Four-Lens Roster)
2. Dialogue Round 1: Initial Positions
3. Dialogue Round 2: Cross-Examination
4. Dialogue Round 3: Revised Positions
5. Dialogue Round 4: Final Statements
6. Moderator Synthesis
7. Uncertainty Ledger

### Micro — 5 sections:
1. Good Group To Explore X (Two-Lens Roster)
2. Dialogue Round 1: Initial Positions
3. Dialogue Round 2: Final Statements
4. Moderator Synthesis
5. Uncertainty Ledger

### Deep — 9 sections:
1. Good Group To Explore X (Four-Lens Roster)
2. Dialogue Round 1: Initial Positions
3. Dialogue Round 2: Cross-Examination
4. Dialogue Round 3: Revised Positions
5. Dialogue Round 4: Final Statements
6. Dialogue Round 5: Stress Test
7. Dialogue Round 6: Contingency Planning
8. Moderator Synthesis
9. Uncertainty Ledger

Do not skip the Roster section or the Uncertainty Ledger in any profile.
Each dialogue round must contain one turn from each active role.

## Workflow

1. Define decision frame
- Restate question, success criteria, constraints, and time horizon.
- Declare assumptions when context is missing.
- Include grounded local/current context if the decision depends on it.

2. Build four-lens roster
- Select two real people with clear relevance to the problem.
- Explain why each role belongs in the group.
- Score Real Person A/B with the scoring matrix before finalizing.
- Score full roster diversity and revise if the score fails.

3. Run multi-round dialogue
- Round 1: initial claims.
- Round 2: challenges and tradeoffs.
- Round 3: revised positions after challenge.
- Round 4: final stance and one concrete action.

4. Synthesize
- Run the internal anonymous meta-review before final synthesis.
- Merge strongest arguments into one recommendation.
- State why it beats the strongest alternative.
- Include preconditions, early warning indicators, and next actions.

5. Calibrate uncertainty
- Separate facts, assumptions, and speculation.
- List evidence needed for confidence upgrades.

6. Run guardrail self-check
- Validate structure, safety, and actionability before final output.

7. User interaction and post-use reflection
- After delivering the output, append the Post-Use Self-Check section.
- If the session is interactive, invite the user to mark which positions they agree/disagree with and why.

## Blind-Spot Gated Overlay Workflow (When execution_mode: blind-spot-gated)

When the user explicitly invokes `blind-spot-gated` mode (canonical invocation surfaces):
- **Natural Language**: `"使用 simulate-elite-experts 技能，指定 execution_mode 为 blind-spot-gated，评估..."`
- **Tool / Slash Command**: `/simulate-elite-experts execution_mode: blind-spot-gated: <problem>` or `Skill(skill="simulate-elite-experts", args="execution_mode: blind-spot-gated ...")`
- **Programmatic Pipeline**: `execute_blind_spot_pipeline(prompt, candidate_answer, call_model_fn=...)`

Execution Lifecycle:
1. **Task-Phase Gate**: Verify the task is in `JUDGMENT` phase (forming/revising high-stakes choices, architectures, root-cause diagnoses, directions). Pure execution tasks (coding, deployment, mechanical refactoring) fast-path skip review (`SKIP_EXECUTION_PHASE`). Execution tasks with premise-invalidating blockers escalate (`ESCALATE_TO_JUDGMENT`).
2. **Primary Candidate Formation**: Primary engine completes the standard four-lens deliberation through Moderator Synthesis and Uncertainty Ledger.
3. **Clean-Context Extraction**: Extract canonical `DecisionPacket` containing ONLY:
   - Original user problem prompt
   - Hard constraints & known facts (<=200 words / ~1200 chars)
   - Candidate verdict summary (from Moderator Synthesis, <=150 words / ~1000 chars)
   - Core rationale summary (<=200 words / ~1200 chars)
   - Declared assumptions and uncertainties (<=150 words / ~900 chars)
   - Declared option space (if choices restricted by prompt)
   *Hard boundary:* NEVER leak dialogue transcripts, scratchpads, persona turns, or vote tallies to the reviewer.
4. **Targeted Heterogeneous Audit**: Resolved from canonical `registry/models.yaml` to an admitted model of a different vendor family (e.g. Anthropic -> Google/Moonshot). If heterogeneous model is unavailable, return `HETEROGENEOUS_REVIEW_UNAVAILABLE` (no fake homogeneous reviews). Reviewer audits across 5 failure categories:
   - (a) Hidden or unexamined assumptions
   - (b) Wrong framing of the decision space (e.g. false dichotomy)
   - (c) Omitted viable alternatives
   - (d) Neglected second-order operational/systemic effects
   - (e) Dramatically simpler paths
   *Option-space rule:* Reviewer must evaluate within bounded space first; alternatives outside must be explicitly labeled `[OUT-OF-FRAMEWORK]` as meta-challenges.
5. **Materiality Gate Circuit Breaker**: Evaluate if audit critique is `material` (fatal flaw, false assumption, dominating option that should alter the recommendation/actions) vs `immaterial` (philosophical difference, declared risk, stylistic preference).
   - If `material == False`: Deliver candidate output cleanly with zero process noise (fast path).
   - If `material == True`: Pass critique back to primary engine for **sovereign single-shot re-entry**. The primary engine retains full agency (accept, partially adapt, or defend with reason).
6. **Clean User Output Delivery**:
   - `material == False`: Deliver candidate answer directly, zero internal ledger clutter.
   - `material == True` (defended): Append brief 1-line note that outside review was evaluated and original choice confirmed.
   - `material == True` (decision changed): Append transparent `### Decision Update: Addressed Blind Spot` section stating what was identified and why the decision changed.
   - Full debug audit ledger is preserved in execution metadata / trace files.

## User Interaction Guidance

The framework output should not be a passive report. Build in interaction touchpoints:

1. **Pre-dialogue check-in**: After presenting the roster (Section 1), pause and ask the user:
   - "Do these roles and people look right for your question? Would you swap anyone?"
   - Use this only in `interactive` mode. If the user confirms, proceed. If the user suggests changes, adjust before running dialogue.

2. **Mid-dialogue checkpoint** (optional, for `deep` profile): After Round 2 (Cross-Examination), briefly ask:
   - "Any assumptions you think were missed in the cross-examination?"
   - Use this only in `interactive` mode.

3. **Post-output reflection**: After the Uncertainty Ledger, always append the Post-Use Self-Check.

These interaction points transform the output from "AI-generated report" to "collaborative thinking scaffold."

## Post-Use Self-Check

After the final section (Uncertainty Ledger), always append a self-check block to help the user actively process the output rather than passively accept it.

Template:
```
### Post-Use Self-Check
1. Before reading this analysis, what was your initial leaning?
2. After reading, has your position changed? If so, which argument was most persuasive?
3. Which assumption in the Uncertainty Ledger concerns you most?
4. What is one piece of evidence you could gather in the next 48 hours to reduce uncertainty?
5. If you had to decide right now, what would you choose and why?
```

Rules:
- This block is mandatory in all profiles (micro, lean, classic, deep).
- It appears after the Uncertainty Ledger, as a non-numbered appendix (not counted in the main section count).
- Keep it to exactly 5 questions. Do not expand or customize.

## 评估与回归

使用：
- `references/eval-rubric.md` for scoring criteria.
- `references/eval-cases.md` for regression test prompts.
- `references/first-use-guide.md` for onboarding new users.
- `scripts/lint_response.ps1` for hard-gate structure checks on generated outputs.
- `scripts/lint_response.py` for the portable hard-gate validator.
- `scripts/run_examples.ps1` for repository example smoke tests.
- `scripts/run_examples.py`：跨平台结构 smoke test，覆盖 `micro`、`lean`、`classic` 和 `deep`。

更新本 Skill 时：

- 至少运行 `eval-cases.md` 中推荐的 5 个案例，而不是只运行四档结构 fixture。
- 逐案检查 profile 的章节数、角色数、轮次、不确定性和 self-check。
- 记录修改前后评分、通过率、平均分和失败原因；没有真实输出时不要虚构评分。
- Windows 保留 PowerShell 入口，CI 使用 Python 入口；两者必须执行相同的硬门禁。

## 输出契约

- 英文输出使用 `references/output-templates.md`，中文输出使用 `references/output-templates-zh.md`；用户使用中文时默认中文。
- 用户要求简短时仍保留当前 profile 的全部必需章节，每节压缩为 1-3 个要点。
- `lean` 保留 4 个角色、4 轮和 7 个章节；`micro` 保留 2 个角色、2 轮和 5 个章节。
- 缺少本地或当前事实时，必须写入假设或不确定性台账，不得用角色口吻补齐事实。

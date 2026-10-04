---
name: academic-polishing
description: "Polish academic prose, de-AI-ify text, control claim strength, or rewrite method sections for CS/AI/ML papers. Executes Prose Quality Gate, Claim Strength Audit, and de-AI pass. Use when: removing AI writing patterns from paper text, adjusting claim strength to match evidence level, rewriting method sections with proper narrative flow, improving academic writing quality, checking for overclaiming. Triggers on: 润色, polish, improve writing, 去AI, de-AI, claim strength, 改写, rewrite method, prose quality, 降级表述, remove AI patterns, academic writing polish, 学术润色, 去AI化, 降级结论, improve prose."
---

# Academic Polishing

将此 skill 视为"学术文体打磨代理"——不是简单润色，而是执行 prose 质量闸门、去AI化改写、claim 强度控制和 Method 专项叙事强化。

## Router Protocol

1. Read `manifest.yaml`. It declares `always_load` files, `axes`, and `references.on_demand`.
2. Read every file listed under `always_load`. These are the skill's binding rules — not reference material.
3. Apply the loaded material as constraints:
   - `stance.md` defines non-negotiable rules, AI Traffic Light, claim strength, evidence-aware boundary, and scope.
   - `red-lines.md` defines absolute prohibitions. Do not negotiate these.
   - `output-contract.md` defines deliverables and completion criteria per mode.
   - `anti-patterns.md` defines known failure modes and their correct alternatives.
4. Detect the mode using the manifest's `mode` axis. If ambiguous, ask one concise question.
5. Echo the selected mode to the user before executing.
6. Reach for `references/` only when the manifest's `references.on_demand` condition is satisfied.

**Structural debt is not language debt.** If `section_contract_debt = open`, only apply local safe edits and return the diagnosis.

## Modes

| Mode | Use when |
|---|---|
| `prose-quality-gate` | General prose quality check + rewrite |
| `method-prose-rewrite` | Method section narrative: 问题→设计→机制→收益/边界 |
| `de-ai-pass` | Remove AI writing patterns only |
| `claim-strength-audit` | Audit and adjust claim strength |

## Execution

Called internally by `academic-paper-writer` orchestrator at Step 9.6. The main agent reads this file and references/ to execute polishing in-process (no subagent dispatch). Polishing must not modify project source code, configuration, or data files. Max 2 rewrite rounds.

## Independent Use

| Input | Mode | Priority | Behavior |
|---|---|---|---|
| "润色一下", "改改语言" | prose-quality-gate | 2 (fuzzy) | Quality gate + rewrite, max 2 rounds |
| "去掉 AI 味", "不像人类写的" | de-ai-pass | 2 (fuzzy) | AI pattern removal only |
| "claim 太强了", "降级结论" | claim-strength-audit | 2 (fuzzy) | All claims audited, zero-tolerance check |
| "改写 Method", "Method 写得太潦草" | method-prose-rewrite | 2 (fuzzy) | Method narrative: problem→design→mechanism→benefit/boundary |
| Explicit mode name | as specified | 1 (explicit) | Skip inference, use specified mode |

| Scenario | Recommended |
|---|---|
| Just polish/de-AI text | This skill (standalone) |
| Auto-polish during drafting | academic-paper-writer orchestrator (Step 9.6) |
| After revision review | academic-reviser → this skill |

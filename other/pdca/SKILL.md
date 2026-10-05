---
name: pdca
description: Create Chinese monospaced compass-style PDCA or CAPD problem-solving cards using East-West-South-North-Center layout, full-width and half-width spaces, diagonal Unicode arrows, and strict Chinese character limits. Use when Codex needs to turn a problem, incident, decision tradeoff, root-cause analysis, improvement cycle, or CAPD/PDCA workflow into a square text diagram, Hermes/Discord-ready card, or Chinese 方位九宮圖 with center ◎, north Plan, east Do, south Check, west Action, and four diagonal transition arrows.
---

# PDCA / CAPD Compass Card

Use this skill to transform a problem into a Chinese text diagram shaped like a compass: North, East, South, West, four diagonal arrows, and a center ◎ core. The output should feel like a fixed-width visual card, not a prose explanation.

## Core Rules

- Use a fenced `text` code block for the final diagram.
- Prefer Chinese labels and short phrases.
- Use full-width spaces `　` for large horizontal alignment and half-width spaces only for small adjustments.
- Keep the center phrase at 8 Chinese characters or fewer, prefixed with `◎`.
- Keep each outer compass phrase at 8 Chinese characters or fewer when the user requests strict eight-character limits.
- Make the diagram readable in a monospaced environment such as Discord, Hermes, terminal, or Markdown preview.
- Avoid over-explaining inside the diagram. Let placement, arrows, and labels carry the structure.

## Compass Mapping

- North `北`: `【Ｐ｜Plan 計畫】` for goals, options, choices, hypotheses, and intended destination.
- East `東`: `【Ｄ｜Do 執行】` for concrete measures, steps,现场 action, and use of methods.
- South `南`: `【Ｃ｜Check 檢查】` for facts, results, confirmation, and next-cycle evidence.
- West `西`: `【Ａ｜Action 改善】` for cause discovery, root-cause pursuit, correction, and institutional repair.
- Center `中`: `【◎核心】` for the problem essence, incident, contradiction, or decision point.

For CAPD, the cycle begins at Check:

- `Check -> Action -> Plan -> Do -> Check`
- Use CAPD when the task starts from現況認識, incident confirmation, observation, or evidence.

For PDCA, the cycle begins at Plan:

- `Plan -> Do -> Check -> Action -> Plan`
- Use PDCA when the task starts from a goal, plan, proposal, or project improvement loop.

## Arrow Rules

Use 45-degree Unicode arrows at the four corners:

- `↗` means Action -> Plan: root causes become better plans.
- `↘` means Plan -> Do: plans become concrete execution.
- `↙` means Do -> Check: execution produces results to inspect.
- `↖` means Check -> Action: inspection returns to root-cause improvement.

Place arrows between the compass quadrants with enough full-width spacing to preserve the visual loop.

## Output Template

Adapt this template. Keep line lengths visually balanced rather than mathematically perfect.

```text
　　　　　　　　　　　　　　　北
　　　　　　　　　　　【Ｐ｜Plan 計畫】
　　　　　　　　　　　方案一：＿＿＿＿
　　　　　　　　　　　方案二：＿＿＿＿
　　　　　　　　　　　選　擇：＿＿＿＿


　　　　　　　↗　　　　　　　　　　　　　　　　　↘
　　西【Ａ｜Action】　　　　　中【◎核心】　　　　　東【Ｄ｜Do】
　　　原因發現　　　　　　　　◎＿＿＿＿　　　　　　手段活用
　　　────────　　　　────────　　　────────
　　　＿＿＿＿　　　　　　　　＿＿＿＿　　　　　　　＿＿＿＿
　　　＿＿＿＿　　　　　　　　＿＿＿＿　　　　　　　＿＿＿＿
　　　＿＿＿＿　　　　　　　　＿＿＿＿　　　　　　　＿＿＿＿


　　　　　　　↖　　　　　　　　　　　　　　　　　↙
　　　　　　　　　　　【Ｃ｜Check 檢查】
　　　　　　　　　　　事　實：＿＿＿＿
　　　　　　　　　　　結　果：＿＿＿＿
　　　　　　　　　　　下一輪：＿＿＿＿
　　　　　　　　　　　　　　　南
```

## Construction Workflow

1. Extract the center problem as a phrase of 8 Chinese characters or fewer.
2. Decide whether the loop is CAPD or PDCA from the user's starting point.
3. Fill the four directions:
   - Plan: options, desired end state, chosen principle.
   - Do: immediate measures and executable steps.
   - Check: confirmed facts, result state, what to inspect next.
   - Action: causes, failures, root-cause questions, recurrence prevention.
4. Compress each phrase until it fits the requested width.
5. Render a single `text` code block with full-width spacing and arrows.
6. If helpful, add a brief note after the diagram listing the cycle order and any assumptions.

## Phrase Compression

When content is too long, compress meaning before widening the diagram:

- `老虎已經逃出籠子` -> `老虎逃走`
- `人命安全與動物保護之間的取捨` -> `人獸取捨`
- `封鎖現場並避免民眾靠近` -> `封鎖現場`
- `防止同類事件再次發生` -> `防止再發`

Prefer four-character and six-character Chinese compounds when possible. Use eight characters only when needed.

## Example

```text
　　　　　　　　　　　　　　　北
　　　　　　　　　　　【Ｐ｜Plan 計畫】
　　　　　　　　　　　方案Ａ：人命尊重
　　　　　　　　　　　方案Ｂ：動物愛護
　　　　　　　　　　　選　擇：先保人命


　　　　　　　↗　　　　　　　　　　　　　　　　　↘
　　西【Ａ｜Action】　　　　　中【◎核心】　　　　　東【Ｄ｜Do】
　　　原因發現　　　　　　　　◎老虎逃走　　　　　　手段活用
　　　────────　　　　────────　　　────────
　　　管理失誤　　　　　　　　人獸危險　　　　　　　封鎖現場
　　　機制失效　　　　　　　　取捨判斷　　　　　　　搜尋活捉
　　　根因追究　　　　　　　　安全優先　　　　　　　必要處置


　　　　　　　↖　　　　　　　　　　　　　　　　　↙
　　　　　　　　　　　【Ｃ｜Check 檢查】
　　　　　　　　　　　事　實：老虎逃出
　　　　　　　　　　　結　果：安全控制
　　　　　　　　　　　下一輪：防止再發
　　　　　　　　　　　　　　　南
```

---
name: executive-decision-memo
description: Use when the user needs to turn analysis, research, meeting notes, options, or recommendations into a concise executive decision memo, board memo, steering committee note, CEO update, investment committee memo, recommendation paper, or consulting-style written recommendation with options, tradeoffs, risks, and next steps.
---

# Executive Decision Memo

Use this skill to convert analysis into a decision-ready executive memo.

## Reference Loading

Read `references/memo-patterns.md` when the user asks for a board memo, investment committee memo, steering committee memo, or when the audience is senior and time-constrained.

## Memo Standard

The memo must help a senior reader make or approve a decision. It should not merely summarize work performed.

Every memo needs:

1. Decision required.
2. Recommendation.
3. Rationale.
4. Options considered.
5. Tradeoffs and risks.
6. Evidence confidence.
7. Next actions and owners.

## Workflow

1. Extract the decision.
   - What decision is needed?
   - Who decides?
   - By when?
   - What happens if no decision is made?

2. State the recommendation.
   - Use one clear sentence.
   - Include the action, scope, and timing.
   - Avoid "consider", "explore", or "align on" unless the recommendation is explicitly to defer.

3. Build the logic.
   - Separate facts from assumptions.
   - Identify the 2-4 strongest reasons.
   - State what evidence would change the recommendation.

4. Compare options.
   - Include a real alternative and a base case.
   - Compare on decision criteria, not generic pros and cons.
   - Make the tradeoff visible.

5. Make risks useful.
   - Name the risk.
   - Explain why it matters.
   - Give a mitigation or trigger.
   - State residual risk after mitigation.

6. Close with execution.
   - Owners.
   - Timeline.
   - First actions.
   - Decision checkpoint.

## Default Memo Format

```markdown
# Decision Memo: <Topic>

## Decision Required
<What decision is needed, by whom, and by when>

## Recommendation
<One direct recommendation sentence>

## Why This Is the Right Move
1. <Reason and evidence>
2. <Reason and evidence>
3. <Reason and evidence>

## Options Considered
| Option | Case for | Case against | When it wins |
| --- | --- | --- | --- |
| Recommended option |  |  |  |
| Alternative |  |  |  |
| Do nothing / defer |  |  |  |

## Key Risks
| Risk | Impact | Mitigation | Trigger to revisit |
| --- | --- | --- | --- |

## Evidence Confidence
- High confidence:
- Medium confidence:
- Low confidence / open questions:

## Next Steps
| Action | Owner | Timing |
| --- | --- | --- |
```

## One-Page Version

When the user asks for a concise memo, produce:

```markdown
## Recommendation
<one sentence>

## Rationale
- <reason 1>
- <reason 2>
- <reason 3>

## Tradeoff
<the real downside or opportunity cost>

## Decision Needed
<approval, budget, scope, timing, owner>

## Next 3 Actions
1. <action>
2. <action>
3. <action>
```

## Quality Bar

- The first 10 lines should make the recommendation understandable.
- The memo should be skimmable without losing the logic.
- The options table should compare real choices, not straw men.
- Risks should be tied to decisions or mitigations.
- Avoid framework labels unless they clarify the decision.
- If evidence is weak, say what must be verified instead of overstating certainty.

## Guardrails

- Do not let the memo become a status update when the user needs a decision.
- Do not hide weak evidence behind confident recommendation language.
- Do not present only one option unless the decision is truly binary.
- Do not use vague risks without owners, mitigations, or revisit triggers.
- For legal, tax, medical, financial, or regulated decisions, frame the memo as analytical support and state what must be verified by qualified professionals.

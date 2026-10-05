---
name: decision-council
description: "Stress-test an important decision through a structured council of expert perspectives, tensions, and a synthesized recommendation. Use when consequential options need independent challenge rather than one unopposed view. Turkish triggers: kararı farklı açılardan test et, seçenekleri eleştir, karar kurulu, bağımsız görüş."
---

# Decision Council

## Purpose
Use this skill when a decision is important enough that a single perspective is not sufficient. The goal is to create productive friction before commitment by evaluating the decision through multiple expert lenses, then synthesizing the debate into one grounded recommendation.

## When to use
Use this skill when:
- the decision has strategic, financial, operational, reputational, or people-related consequences
- the user is deciding between options and wants stronger reasoning, not just a quick opinion
- the user wants pushback, tradeoffs, risks, and second-order effects surfaced clearly
- the decision is ambiguous and would benefit from multiple expert viewpoints

## When not to use
Do not use this skill when:
- the task is simple, low-stakes, or purely factual
- the user only wants a direct answer with no comparative reasoning
- there is not enough context to evaluate the decision meaningfully
- the request is purely creative and does not involve evaluating tradeoffs

## Rules
- Do not give the final recommendation immediately.
- First simulate a structured council with multiple distinct expert perspectives.
- Make each perspective meaningfully different. Avoid repeating the same argument with different labels.
- Include tension, disagreement, and tradeoffs. The value of the skill is the clash before the synthesis.
- Ground every viewpoint in the user's actual context when available.
- Call out assumptions, missing information, and major uncertainties explicitly.
- Do not manufacture certainty. If the evidence is weak, say so.
- End with one synthesized recommendation, not a vague recap.
- The final recommendation must include concrete next steps.

## Inputs
The user should provide as much of the following as possible:
- the decision to be made
- available options
- relevant context and constraints
- timeline
- decision criteria
- risks already identified
- what success would look like

If the user provides limited context, proceed with reasonable assumptions and label them clearly.

## Council design
Default to 4 perspectives unless the user specifies otherwise. Select the most useful roles for the decision. Possible roles include:
- Strategic Advisor
- Operator
- Financial Analyst
- Risk Manager
- Product Lead
- Growth Lead
- Brand/Marketing Lead
- Customer Advocate
- Legal/Compliance Reviewer
- Technical Lead
- Skeptic / Contrarian

You may adjust the panel depending on the decision type, but ensure the viewpoints remain distinct.

## Output structure
Use this structure:

### 1. Decision summary
- what the decision is
- what options are being evaluated
- any key assumptions

### 2. Council perspectives
For each expert, include:
- perspective name
- core argument
- strongest concern
- what they would prioritize
- their provisional recommendation

### 3. Tensions and tradeoffs
Summarize the main points of disagreement, such as:
- speed vs rigor
- growth vs margin
- flexibility vs focus
- short-term upside vs long-term risk

### 4. Synthesized recommendation
Provide:
- the recommended path
- why it wins over the alternatives
- what conditions would change the recommendation

### 5. Next steps
Provide a short, actionable sequence of next steps.

### 6. Confidence and unknowns
End with:
- confidence level: low, medium, or high
- the most important missing information

## Definition of success
This skill succeeds when:
- the user sees multiple serious perspectives, not superficial roleplay
- the disagreement reveals something non-obvious about the decision
- the final recommendation is clearer and stronger because of that tension
- the next steps are concrete enough to act on immediately

---
name: parallel-reviews
description: >
  Review a document, proposal, question, or viewpoint from multiple expert
  perspectives in parallel, then synthesize the findings. Use whenever the user
  wants multi-angle analysis, needs to stress-test an idea, asks "what would X
  think about this", wants to understand how different stakeholders would react,
  needs expert opinions on a document, or says things like "review this from
  different angles", "get multiple perspectives", "what are the risks", or "who
  should weigh in on this". Works with any content including contracts, product
  ideas, medical decisions, engineering designs, business plans, policy
  proposals, or freeform questions.
---

# Parallel Expert Reviews

Orchestrate a panel of expert sub-agents to review content from independent perspectives, then synthesize their findings for the user.

## Workflow

### 1. Receive content

Accept the content to review. It may be pasted inline, a file path, or a description of a situation/question. If unclear, ask the user to paste or describe it before proceeding.

### 2. Suggest experts

Based on the content, propose 3–6 expert roles that would provide the most valuable perspectives. Present them as a list the user can accept, modify, or extend:

```
I'll review this from these expert perspectives:
- Legal
- Financial
- Marketing

Add any others, or remove any that aren't relevant.
```

Use good judgment about relevance — a recipe doesn't need a securities lawyer; a drug trial protocol doesn't need a UX designer. For unfamiliar domains, lean toward including more experts rather than fewer.

See `references/expert-personas.md` for descriptions of common expert types and what they focus on. For any expert not listed there, use general domain knowledge to construct their analytical lens.

### 3. Spawn parallel sub-agents

Once the expert list is confirmed, spawn one sub-agent per expert **in a single turn** (all in parallel). Give each sub-agent this prompt:

```
You are a [EXPERT ROLE] reviewing the following content on behalf of a user.

CONTENT:
[full content here]

Analyze this content strictly from your expert perspective. Produce a structured review with these sections:

## [Expert Role] Review

**Lens**: One sentence describing what you're focused on as this expert.

**Key Findings**: 3–5 bullet points of the most important observations from your perspective.

**Risks & Concerns**: Specific issues, red flags, or gaps you'd flag. Be direct — don't soften genuine concerns.

**Recommendations**: Concrete suggestions or next steps from your perspective.

Keep your review focused and actionable. Do not speculate outside your domain.
```

Do not wait for one sub-agent before spawning the next — launch all at once.

### 4. Collect and format results

Once all sub-agents return, assemble the final output using this structure:

```
# Expert Review: [brief topic title]

---

[Expert 1's full review section]

---

[Expert 2's full review section]

---

[... repeat for all experts ...]

---

## Synthesis

[2–3 paragraphs that weave together the perspectives. Surface:
- Where experts agree (convergent risks or opportunities)
- Where they conflict or pull in different directions (tradeoffs the user must navigate)
- The most critical actions implied by the combined analysis]
```

Write the synthesis yourself (not via sub-agent) after reading all expert outputs. It should add value beyond just listing what each expert said — identify the cross-cutting themes and tensions.

## Tips

- If the user provides a file path, read the file before spawning sub-agents so each sub-agent receives the full content inline.
- If the content is very long (>5k words), summarize it to the key decisions/elements before passing to sub-agents — they don't need boilerplate.
- Custom expert roles (e.g., "a skeptical investor", "a teenager", "a regulator from the EU") work fine — adapt the prompt accordingly.
- If the user wants a deeper dive from one expert after seeing results, spawn a focused follow-up sub-agent for that expert only.

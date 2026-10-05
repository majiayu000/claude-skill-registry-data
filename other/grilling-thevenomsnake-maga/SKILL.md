---
name: grilling
description: "Stress-test a product plan, decision, or idea through a relentless one-question-at-a-time interview. Use when the user asks to be grilled, wants assumptions challenged, has a vague or risky plan that needs sharper decisions, or needs a project discussion turned into durable context. Automatically use a standalone mode for conversation-only work and a documented mode with domain modeling when a repository should retain decisions."
---

# Grilling

Map the uncertainty as a **design tree**: each product decision branches into
the decisions that depend on it. The **frontier** contains decisions whose
prerequisites are already settled. Recompute it after every answer so hidden
assumptions become visible without asking downstream questions too early.

Investigate facts from the environment or authoritative sources instead of
asking the user. Independent fact lookups may run in parallel while decisions
that do not depend on them continue. Product decisions remain the user's.

Ask exactly one highest-leverage frontier question at a time and recommend an
answer with its product consequence. This is MAGA's deliberate adaptation of
upstream round-based grilling: product builders should not receive an entire
frontier as a questionnaire. Only when the user explicitly asks for a batch and
the decisions are independent may one turn contain up to three numbered
questions.

## Choose The Mode Automatically

- **Standalone:** use for an idea or plan with no repository, or when the user
  only wants conversational challenge. Do not create project documents.
- **Documented:** use when the work belongs to a repository and resolved terms
  or hard-to-reverse decisions should survive the conversation. Apply
  `domain-modeling` as needed to update the repository's established context or
  decision records; do not invent a parallel document system.

Do not ask the user to choose a mode or invoke another Skill. Switch from
standalone to documented only when durable project context becomes useful.

## Finish Deliberately

Do not implement the plan during the interview. Stop when the current useful
product slice has no unresolved frontier decision—not when every hypothetical
future branch has been explored. Summarize the shared understanding, remaining
uncertainty, and recommended next product step. Continue into action only after
the user has authorized that next step or their original request already did so.

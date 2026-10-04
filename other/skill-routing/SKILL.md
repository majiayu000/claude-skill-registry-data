---
name: skill-routing
description: >
  Match a user request to the right skill using trigger matching, project
  context, and conversation history. Score ambiguity 1–10 and resolve it
  using context signals or a single clarifying question. Load when
  project-orchestrator needs to route a request, or when multiple skills
  could match and the right one is unclear. Also triggers on "which skill
  should handle this", "route this request", "I'm not sure which skill to
  use", "disambiguate this", "skill routing". Called by project-orchestrator
  for request routing. For finding whether a skill exists for a capability, use
  skill-finder instead.
license: MIT
metadata:
  author: dvy1987
  version: "1.2"
  category: meta
  resources:
    references:
      - examples.md
      - harness-symptoms.md
---

# Skill Routing

You are a Skill Router. Given a user request, project state, and conversation context, you determine which skill to invoke. When multiple skills match, you score the ambiguity and resolve it — either silently via context or by asking one targeted question.

## Hard Rules

**Never guess when ambiguity is ≥ 7.** Ask exactly one disambiguation question.
**Never ask more than one question.** Frame it as a choice between the top 2 candidates.
**Always read skill descriptions before routing.** Do not rely on skill names alone.
**Always log the routing decision** — skill chosen, ambiguity score, and how it was resolved.

---

## Workflow

### Step 1 — Discover Candidate Skills

Do NOT use a hardcoded routing table. Call `skill-finder` with the user's request to discover all candidate skills from the live library.

- **1 candidate** → return it. Done. Ambiguity = 1.
- **0 candidates** → `skill-finder` found nothing. Return `no-match` to the caller.
- **2+ candidates** → proceed to Step 2.

### Step 1b — Harness symptom pre-route

Before scoring ambiguity, read `references/harness-symptoms.md`.

If the user describes **agent misbehavior** (not app bugs), prepend `harness-engineering`
to candidates and lower ambiguity when manifest is missing or symptoms match.

If `project-setup` just completed in this session → route `harness-generation` next unless user opted out.

### Step 2 — Score Ambiguity (1–10)

Rate how unclear the routing is:

| Score | Meaning | Criteria |
|-------|---------|----------|
| 1–3 | **Low** | One candidate clearly dominates — better trigger match, correct phase, or natural next step |
| 4–6 | **Medium** | Two candidates are plausible but context signals can resolve |
| 7–10 | **High** | Two+ candidates are equally plausible even after reading context |

Factors that RAISE the score: request uses generic words ("plan", "review", "improve"), no project artefacts to anchor phase, request is short/vague.
Factors that LOWER the score: request uses a skill's exact trigger phrase, project phase clearly narrows candidates, conversation history shows a chain in progress.

### Step 3 — Resolve Ambiguity

**Score 1–3:** Route to the best match. No question needed.

**Score 4–6:** Read these context signals to resolve silently:
1. **Project phase** — what artefacts exist narrows the candidates
2. **Conversation history** — what the user just finished suggests the next step
3. **Trigger precision** — does the phrasing match one skill's triggers more exactly?
4. **Upstream/downstream** — is one skill the natural successor of the last completed skill?

Pick the best fit. Note the runner-up in the routing log.

**Score 7–10:** Ask ONE disambiguation question as a binary choice:
> "This could be **[skill-A]** ([one-line purpose]) or **[skill-B]** ([one-line purpose]). Which fits?"

Route based on the answer.

### Step 4 — Check Pre-requisites

Before returning the routed skill, verify its pre-req column:
- Pre-req missing → tell the caller which skill produces the pre-req
- Pre-req exists → return the skill

### Step 5 — Return Routing Decision

Return to the calling skill (usually `project-orchestrator`):

```
Routed: [skill-name]
Ambiguity: N/10
Candidates: [skill-a, skill-b, ...]
Resolved by: [exact-match | phase-context | conversation-chain | upstream-downstream | user-answer]
Pre-req: [met | missing — need X first]
```

---

## Gotchas

- "Review" is the most ambiguous word — "review this code" → `code-review-crsp`, "review changes for context" → not a review skill, "review the plan" → `adversarial-hat`. Always check the object being reviewed.
- "Plan" is similarly overloaded — "plan this change" → `problem-to-plan`, "plan implementation" → `implementation-plan`, "plan this out" → `process-decomposer`. The verb before "plan" disambiguates.
- Return only concrete, invokable skill names. Caller-owned labels like "Phase recommendation" are not valid routing results.
- A skill scoring high on trigger match but failing the pre-req check is NOT the right skill to invoke directly — route to the pre-req skill first.
- When `project-orchestrator` calls you, return fast. Routing should add seconds, not minutes.
- **Agent complaints are usually harness, not debug.** "Agent keeps failing" → `harness-engineering`, not `debug-and-fix`, unless the user names a specific code bug.

---

## Example

<examples>
  <example>
    <input>User says: "Help me think through this problem"</input>
    <output>
Candidates: deep-thinking, brainstorming, socratic
Ambiguity: 5/10

Context signals:
- Project phase: specs exist, PRD exists → past design phase
- Conversation: user just finished implementation, hit a wall
- Trigger match: "think through" matches deep-thinking and brainstorming equally
- Upstream: post-implementation thinking → deep-thinking (not brainstorming, which is pre-implementation)

Routed: deep-thinking
Ambiguity: 5/10
Candidates: deep-thinking, brainstorming, socratic
Resolved by: upstream-downstream (post-implementation context)
Pre-req: met
    </output>
  </example>
</examples>

---

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Obvious which skill" | Obvious to user ≠ obvious to router at score 6/10. |
| "Invoke both skills" | Double invocation wastes tokens and causes conflicts. |
| "Skip ambiguity score" | Score drives whether to ask — skipping hides misfires. |
| "Library-first is dogma" | Library-first is default — project skills win when present. |
| "Route to general-purpose" | Named skills encode workflows general chat skips. |

## Verification

- [ ] Ambiguity score 1-10 stated when multiple skills match
- [ ] Winner skill named with one-line rationale
- [ ] User asked to disambiguate when score ≥7
- [ ] Project-local skill preferred over global when both match

## Red Flags

- Ambiguous review routed without disambiguating code vs UI
- Plan request sent to wrong planner skill for intent
- Non-invocable label returned instead of concrete skill name
- Multiple candidates returned without disambiguation step

## Prune Log
Last pruned: 2026-07-04
- No changes — citation audit passed; content current (improve-skills full pass 2026-07-04)


## Impact Report

```
Routing complete: [request summary]
Skill routed: [skill-name]
Ambiguity: N/10
Candidates considered: [list]
Resolved by: [method]
Question asked: [yes — question text | no]
```

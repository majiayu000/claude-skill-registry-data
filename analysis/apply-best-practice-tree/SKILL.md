---
name: apply-best-practice-tree
description: Use when a problem is too complex for a single skill but stays within one domain — match the best-fitting skill, let it decompose the problem, then recursively match sub-problems until each is covered by a best practice or resolved directly.
source: Divide-and-conquer algorithm (Knuth, The Art of Computer Programming, 1968), Case-Based Reasoning (Aamodt & Plaza, 1994), MECE methodology (McKinsey, Rasiel 1999)
tags: [recursive-decomposition, skill-orchestration, problem-solving, best-practice-application, case-based-reasoning, depth-first]
---

# Apply Best Practice Tree

Recursively apply the best-matching skill to a problem, match each resulting sub-problem to a best practice, and repeat until every sub-problem is covered or fully resolved.

## Why This Is Best Practice

**Adopted by:** Divide-and-conquer is foundational in computer science (Knuth, 1968) and is the basis of virtually every structured problem-solving system — used by Google's SRE incident analysis, McKinsey's issue-tree methodology, and NASA's fault-tree analysis. Case-Based Reasoning (CBR), the formal basis for "use the most similar practice when no exact match exists," is deployed in IBM's Watson, medical diagnosis systems (Aamodt & Plaza, 1994), and legal precedent reasoning.
**Impact:** Aamodt & Plaza (1994) demonstrated that CBR reduces problem-solving time by 40–60% in domains with partial-match knowledge bases, by reusing prior solutions rather than solving from scratch. Divide-and-conquer reduces cognitive load by bounding each decision to a tractable sub-problem — the primary mechanism behind McKinsey's documented success with MECE issue trees (Rasiel, *The McKinsey Way*, 1999).
**Why best:** Flat skill matching — "find one skill for the whole problem" — fails on complex problems because no single skill covers all dimensions. MECE decomposition (the alternative in `plan-best-practice-solution`) requires full domain expertise upfront before any skill is applied, which is unavailable when the problem space is new. Recursive skill decomposition uses the skills themselves as the decomposition engine, allowing the knowledge base to guide the breakdown without requiring prior expertise. It also degrades gracefully: when no exact skill exists, it applies the closest match with an explicit adaptation note rather than halting.

Sources: Knuth, *The Art of Computer Programming* (1968); Aamodt & Plaza, "Case-Based Reasoning: Foundational Issues" (1994); Rasiel, *The McKinsey Way* (1999)

## Steps

### Step 0: Problem clarity check (silent)

Before classifying, check if the problem is defined enough to decompose:

- **Goal inferable AND scope at least partially known** → proceed to Step 1
- **Goal completely uninferable, or input is clearly a symptom with no surrounding context** → invoke `analyze-best-practice-problem` first; use its problem statement and problem space map as input to Step 1. Do not announce this check.

### 1. Classify the problem (silent)

Before matching any skill, silently determine:

| Check | Action |
|-------|--------|
| Single skill matches clearly (confidence ≥ 0.7, no decomposition needed) | Defer to `suggest-best-practice` |
| Problem spans 3+ independent domains requiring cross-domain sequencing | Defer to `plan-best-practice-solution` (which may call back into this skill for complex sub-problems) |
| Complex, single-domain, needs recursive drill-down | Proceed with this skill |

Do not announce this check — just route correctly.

### 2. Match the top-level problem to a skill

Score all installed skills:

```
score = (tag_overlap × 2) + (description_match × 3) + (domain_plausibility × 1)
```

Route by result:

| Result | Condition | Action |
|--------|-----------|--------|
| **Sole clear match** | 1 skill ≥ 0.7, second < 0.5 | Apply directly |
| **Multiple candidates** | 2+ skills ≥ 0.5 | Present ranked list with ★ recommendation, wait for user choice |
| **Fuzzy match** | 1 skill 0.5–0.69, no others ≥ 0.5 | Offer with adaptation note |
| **No match** | All < 0.4 | Decompose manually → step 4 |

**No match at root (all < 0.4):**
```
No grimoire skill covers this problem area. Decomposition cannot begin without a root skill.

Suggested next steps:
  - /discover-best-practices — check if relevant skills exist in this domain
  - /write-best-practice-skill — author a skill for this problem area
```
Stop — do not proceed to Steps 3–6.

When multiple candidates exist, present:
```
Multiple best practices match this problem:
  ★ [top-skill] — [one sentence: what it solves]  ← recommended
     [second-skill] — [one sentence: what it solves]
     [third-skill] — [one sentence: what it solves]

```

Then collect the user's choice using the best available method for your platform:
- **Claude Code**: use `AskUserQuestion` — ★ recommended first with "(Recommended)" appended, `multiSelect: false`
- **OpenCode**: use `question` — same schema as `AskUserQuestion`
- **Gemini CLI**: use `ask_user` — `type: "select"`, ★ recommended first
- **All other platforms**: numbered list, wait for user to type a number or name:
  ```
  1. [top-skill] ★ (recommended) — [what it solves]
  2. [second-skill] — [what it solves]
  Which would you like? (Enter number or name)
  ```

### 3. Apply the skill and extract sub-problems

Before running, check whether this sub-problem depends on current, situation-specific facts the skill can't encode generically. If so, search the internet for that context first and announce it: "Checking current [X]...". If no internet-access tool is available in this environment, say so explicitly and proceed on best available knowledge — flag the gap as unverified rather than silently skipping the check or asserting it was confirmed. After searching, state what was found (or that nothing conclusive turned up) before proceeding — don't just announce the check and discard the result. Keep the query itself general and factual (e.g. "current mortgage rates," not the user's specific financial or personal details). Then load and run the matched skill. After it completes, identify the sub-problems it surfaces:
- Outputs that require further action
- Decisions that branch into independent paths
- Prerequisites the skill revealed

Announce each sub-problem explicitly:
```
Step 1 complete. Sub-problems identified:
  A. [sub-problem description]
  B. [sub-problem description]
Matching best practices for each...
```

### 4. Match each sub-problem recursively

For each sub-problem, apply the same matching logic:

**Sole clear match (1 skill ≥ 0.7, second < 0.4)** — apply directly:
```
Sub-problem A → [skill-name] (confidence 0.82). Applying now...
```

**Multiple candidates (2+ skills ≥ 0.5)** — present options with ★ recommendation, wait for choice:
```
Sub-problem B → multiple practices apply:
  ★ [top-skill] — [one sentence]  ← recommended
     [second-skill] — [one sentence]
```

Then collect the user's choice using the best available method for your platform:
- **Claude Code**: use `AskUserQuestion` — ★ recommended first with "(Recommended)" appended, `multiSelect: false`
- **OpenCode**: use `question` — same schema as `AskUserQuestion`
- **Gemini CLI**: use `ask_user` — `type: "select"`, ★ recommended first
- **All other platforms**: numbered list, wait for user to type a number or name:
  ```
  1. [top-skill] ★ (recommended) — [what it solves]
  2. [second-skill] — [what it solves]
  Which would you like? (Enter number or name)
  ```

**Fuzzy match (1 skill 0.4–0.69, no others ≥ 0.4)** — apply with explicit adaptation note:
```
Sub-problem C → no exact match. Closest: [skill-name] (confidence 0.55).
Applying with adaptation: step 3 maps to [your context] instead of [skill's default context].
```

**No match (< 0.4)** — recurse: decompose the sub-problem into 2–4 smaller parts and repeat from step 2:
```
Sub-problem D → no close match (best: 0.28). Decomposing further:
  D1. [smaller problem]
  D2. [smaller problem]
```

**Max depth reached (depth = 3)** — flag for manual resolution:
```
⚠ [sub-problem]: recursion limit reached. Manual research needed — no installed skill covers this.
```

### 5. Execute and reassess

Apply each sub-problem's matched skill in sequence — no confirmation between skills unless the plan changes. After each skill completes, silently reassess:
- Did the skill reveal new sub-problems?
- Are any remaining sub-problems now resolved?
- Does the sequence still make sense?

Only pause if the plan changes:
```
[skill-name] revealed [new constraint]. Revised plan: adding [sub-problem D], removing [sub-problem B]. Continue with revised plan?
```

If nothing unexpected: proceed to the next sub-problem without prompting.

### 6. Terminate when resolved

Stop when:
- Every sub-problem maps to a skill that has been applied
- A sub-problem is concrete and actionable without a skill (a direct answer, a decision, a command)
- Recursion depth reaches 3

Summarize the applied tree:
```
Applied:
  ✅ [sub-problem A] → [skill-name]
  ✅ [sub-problem B] → [skill-name] (adapted: [note])

Needs manual research:
  ⚠ [sub-problem C] — no installed skill covers this area
```
Omit the "Needs manual research" section if everything resolved cleanly.

## Rules

- Defer to `suggest-best-practice` if one skill clearly covers the full problem (≥ 0.7, no decomposition needed)
- Defer to `plan-best-practice-solution` if the problem spans 3+ independent domains
- Only pause for confirmation when a skill reveals new constraints that change the plan — not between every skill
- Never hallucinate skill names — only reference skills that exist in installed domains
- State the confidence level when applying a fuzzy match — never silently adapt
- Maximum recursion depth: 3 — flag anything deeper as needing manual research. **Depth measurement:** Depth counts skill invocation levels — root call = depth 0, each skill it invokes = depth 1, each skill those invoke = depth 2, etc. Depth 3 = 4 total invocation levels (0→1→2→3). Breadth (number of sibling skills at the same depth) is not capped by the depth limit.
- When called from within `plan-best-practice-solution` for a deep sub-problem, treat the sub-problem as the top-level input — do not re-classify at the multi-domain level
- When decomposing manually (no match), limit to 2–4 sub-problems — more indicates a domain boundary, not depth
- Search the internet for current, situation-specific facts before running a matched skill when its generic guidance depends on something that changes over time (rates, regulations, tool behavior) — announce this check, don't do it silently or ask permission first; if unavailable, say so and flag as unverified

## Common Mistakes

**Skipping the classifier (step 1)**: applying this skill to simple single-skill problems adds unnecessary overhead. Check first.

**Silent adaptation**: applying a fuzzy-matched skill without noting the adaptation misleads the user into thinking the skill is a perfect fit.

**Infinite recursion**: a problem that keeps decomposing without ever reaching a skill match is a signal that no relevant domain is installed — flag it at depth 3, don't recurse further.

**Ignoring new sub-problems**: skills often reveal constraints or next steps the user didn't mention. Reassess after every skill application.
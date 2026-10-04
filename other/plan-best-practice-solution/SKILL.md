---
name: plan-best-practice-solution
description: Use when a problem requires coordinating 2+ best practices in sequence — whether across one domain or many — e.g. "apply defensive programming", "launch a startup", "handle a workplace medical emergency", "going through a divorce while buying a house."
source: McKinsey Problem Solving (MECE methodology, Rasiel 1999), Kepner-Tregoe problem analysis, Design Thinking (IDEO/Stanford d.school)
tags: [complex-problem, multi-skill, problem-decomposition, mece, skill-orchestration, problem-solver, structured-solution, flat-sequence]
---

# Plan Best Practice Solution

Decompose a multi-skill problem into sub-problems, match each to the highest-confidence best-practice skill, sequence them by dependency, and execute one skill at a time.

## Why This Is Best Practice

**Adopted by:** McKinsey, BCG, and Bain use MECE (Mutually Exclusive, Collectively Exhaustive) issue trees as their primary problem-solving methodology for complex client situations. NASA and Boeing use Kepner-Tregoe structured problem analysis for high-stakes multi-system failures. Design Thinking's problem-decomposition phase is standard at Google, IDEO, and Apple before any solution is attempted.
**Impact:** Rasiel (*The McKinsey Way*, 1999) documents that MECE decomposition is the primary tool consultants use to avoid missing problem dimensions — the leading cause of strategy failures. IDEO's Human-Centered Design methodology mandates an explicit problem-definition phase before ideation; teams that skip it produce solutions targeting the wrong problem, requiring full redesign rather than iteration (IDEO HCD Field Guide, 2015). Kepner-Tregoe structured problem analysis is used by Boeing and NASA for high-stakes multi-system failures precisely because unstructured analysis under pressure collapses to the most visible symptom, not the root cause.
**Why best:** Single-skill application fails for complex problems because skills are scoped to one concept. Without decomposition: (1) important problem dimensions are missed; (2) skills are applied in the wrong order — applying a hiring plan before validating a business model wastes work; (3) conflicting guidance between skills goes unresolved. Structured decomposition first, then sequenced skill application, eliminates all three failure modes. Ad-hoc "try one skill, see what sticks" is the alternative — it produces incomplete coverage and rework.

Sources: Rasiel, *The McKinsey Way* (1999); Kepner-Tregoe Problem Analysis; IDEO Human-Centered Design Field Guide (2015)

## Steps

### 1. Extract problem dimensions (silent)

From the user's input, silently identify:

| Dimension | Extract |
|-----------|---------|
| **Goal** | What outcome does the user want? |
| **Domains** | Which fields are involved? (engineering, law, finance, health, etc.) |
| **Constraints** | Time, resources, legal, technical limits |
| **Dependencies** | What must be true before other things can happen? |
| **Urgency** | Is any sub-problem time-sensitive or blocking others? |

Do not ask the user for any of this — infer from what they wrote.

**Problem clarity check:** After extracting dimensions, apply skill judgment: can the goal and at least 1 domain be identified from what the user said? If the goal is completely uninferable, or what's described is clearly a symptom with no root cause context → invoke `analyze-best-practice-problem` first. Use the problem space map from its output to populate the dimensions above, then continue to Step 2.

**Complexity check:** If the problem maps to a **single** skill (regardless of domain count), delegate to `suggest-best-practice` instead. If **multiple skills** are needed — whether across one domain or many — handle directly. `plan-best-practice-solution` is for any multi-skill plan.

### 2. Decompose into MECE sub-problems

Apply MECE decomposition:
- Each sub-problem addresses one distinct dimension of the overall problem
- Sub-problems don't overlap — a skill that solves sub-problem A doesn't also solve sub-problem B
- Together they cover the full problem — no important dimension omitted

Maximum 7 sub-problems. If more emerge, group related ones under a shared theme.

### 3. Match skills to sub-problems

For each sub-problem, score all candidate skills:

```
score = (tag_overlap × 2) + (description_match × 3) + (domain_plausibility × 1)
```

Classify the result per sub-problem:

| Result | Condition | Action |
|--------|-----------|--------|
| **Clear match** | 1 skill ≥ 0.7, second < 0.4 | Assign directly — no user choice needed |
| **Multiple candidates** | 2+ skills ≥ 0.4 | Mark for user choice — record all candidates, flag ★ recommendation (highest score) |
| **Multi-skill sub-problem** | Sub-problem itself needs 2+ skills and dimensions are known upfront | Flag for recursive `plan-best-practice-solution` call — do not force into a single skill |
| **Opaque sub-problem** | Sub-problem needs skills to reveal its own sub-problems (dimensions unknown upfront) | Delegate to `apply-best-practice-tree` |
| **No match** | All skills < 0.4 | Flag with ⚠ — manual research needed |

If decomposition collapses to a single sub-problem mapping to one skill, retroactively delegate to `suggest-best-practice` — don't add plan overhead for single-skill problems.

If no installed skill covers a sub-problem, flag it explicitly:
`⚠ [sub-problem description]: no installed skill — manual research needed`

### 4. Sequence by dependency

Order skills by logical dependency — not arbitrary order:

| Dependency rule | Example |
|-----------------|---------|
| Validate before build | Business model before go-to-market |
| Legal before commitment | Review contract before signing or hiring |
| Diagnose before fix | Root cause before solution design |
| Calculate before plan | Unit economics before funding strategy |
| Foundation before structure | Architecture before implementation |

Skills with no prerequisites go first. Skills whose output feeds another skill go next.

### 5. Present the solution plan

Present the full sequenced plan. For sub-problems with a clear match, show directly. For sub-problems with multiple candidates, show all options inline with ★ recommendation and collect the user's choice before execution begins.

```
Here is the solution plan ([N] skills to apply):

1. [skill-name] — [what sub-problem it solves]
   Domain: [domain/subdomain]

2. Multiple practices apply — choose one:
   ★ [top-skill] — [one sentence: what it solves]  ← recommended
      [second-skill] — [one sentence: what it solves]
      [third-skill] — [one sentence: what it solves]

3. [sub-problem label] — nested plan ([M] skills):
   3a. [skill-name] — [what it solves]
   3b. [skill-name] — [what it solves]
   3c. [skill-name] — [what it solves]

4. [skill-name] — [what sub-problem it solves]
   Domain: [domain/subdomain]

⚠ [sub-problem]: no installed skill — manual research needed.
```

After presenting, if any steps have multiple candidates, collect user choices using
the best available method for your platform:

- **Claude Code**: use `AskUserQuestion` — one question per ambiguous step,
  ★ recommended option first with "(Recommended)" appended, `multiSelect: false`
- **OpenCode**: use `question` — same schema as `AskUserQuestion`
- **Gemini CLI**: use `ask_user` — same structure, `type: "select"`, options list,
  ★ recommended first
- **All other platforms** (Codex, Cursor, Copilot, etc.): present numbered list
  and wait for user to type a number or skill name:
  ```
  Step N has multiple options:
  1. [top-skill] ★ (recommended) — [what it solves]
  2. [second-skill] — [what it solves]
  Which would you like? (Enter number or skill name)
  ```

Collect all choices before starting execution. Only proceed once every step has a decided skill.

### 6. Execute and adapt

For each skill in the sequence (using user-decided skills from Step 5):
1. Announce: `Applying step N: [skill-name]`
2. If step N is flagged as a **multi-skill sub-problem**: recursively invoke `plan-best-practice-solution` for that sub-problem (max recursion depth: 2 additional levels). Announce: `Step N is a multi-skill sub-problem — running a nested plan:`
3. Before running, check whether this step depends on current, situation-specific facts the skill can't encode generically (a current rate, regulation, tool behavior, recent event). If so, search the internet for that context first and announce it: "Checking current [X] for step N..." Keep the query itself general and factual (e.g. "current mortgage rates," not the user's specific financial or personal details). If no internet-access tool is available in this environment, say so explicitly and proceed on best available knowledge — flag the gap as unverified rather than silently skipping the check or asserting it was confirmed. After searching, state what was found (or that nothing conclusive turned up) before proceeding — don't just announce the check and discard the result. Then load and run the skill (or nested plan) fully, grounded in what was found (or best available knowledge, if unverified).
4. After completion, reassess before proceeding:
   - Did the output reveal new constraints or sub-problems?
   - Are any remaining skills now unnecessary?
   - Does the sequence still make sense?

If the plan changes, state it explicitly before continuing:
```
Step N revealed [new constraint]. Revised plan: removing step M, adding [skill-name].
Continue with revised plan?
```

If nothing unexpected: proceed silently to the next skill — no confirmation between steps.

**Failure-handling:** If a skill fails to complete (errors, no output, or user abandons):
1. Show what failed: `[skill-name] did not complete — [reason if known]`
2. Offer: `Retry [skill-name], skip it, or stop the plan? [retry / skip / stop]`
3. If skipped: note in the final summary that [skill-name] was skipped and its dependencies may be incomplete

A plan with silent failures is worse than a failed plan — the user thinks they applied all practices but they didn't.

**After all skills complete, output a final summary:**
```
Plan complete.

Applied:
  ✅ [skill-name] — [sub-problem it solved]
  ✅ [skill-name] — [sub-problem it solved]

Skipped:
  ⚠ [skill-name] — skipped; [downstream dependencies may be incomplete]

Needs manual research:
  ⚠ [sub-problem] — no installed skill covers this area
```
Omit Skipped and Needs manual research sections if everything resolved cleanly.

## Rules

- If the problem maps to a single skill, defer to `suggest-best-practice` regardless of domain count — don't over-engineer. Single-domain + multiple skills: handle directly.
- Only pause between skills if the plan changes — not between every skill
- Never hallucinate skill names — only reference skills that exist in installed grimoire domains
- Flag sub-problems with no matching skill explicitly — don't skip them silently
- State the reason for sequencing decisions — don't just present an order without explaining why
- Maximum 7 sub-problems — group if more emerge
- If a sub-problem is multi-skill and non-opaque (dimensions known upfront), recurse: apply `plan-best-practice-solution` to that sub-problem — max 2 additional levels of nesting
- If a sub-problem is opaque (dimensions unknown until skills execute), delegate to `apply-best-practice-tree`
- **Three-way routing for sub-problems:** single-skill → execute directly; multi-skill known → recurse `plan-best-practice-solution`; opaque → `apply-best-practice-tree`
- **Recursion depth limit:** max 2 additional nesting levels (root → level 1 → level 2). At level 2, force flat execution even if further decomposition is possible — flag remainder as manual research
- Search the internet for current, situation-specific facts before running a step when its skill's generic guidance depends on something that changes over time (rates, regulations, tool behavior) — announce this check, don't do it silently or ask permission first; if unavailable, say so and flag as unverified

## Examples

> Skill names in examples are illustrative — actual skills depend on what domains are installed. If a skill is not installed, `plan-best-practice-solution` flags it with ⚠ and notes manual research is needed.

**Example 1 — Startup launch**
> "I want to launch a SaaS startup"

Sub-problems: business model, unit economics, legal structure, go-to-market, hiring
Sequence: `design-business-model` → `calculate-unit-economics` → `review-saas-contract` → `design-go-to-market` → `plan-hiring`
Reason: validate model and economics before legal commitments; legal before hiring

---

**Example 2 — Career transition**
> "I'm a senior engineer who wants to move into engineering management"

Sub-problems: skills gap assessment, compensation negotiation, leadership approach, personal brand
Sequence: `audit-technical-debt` → `negotiate-compensation` → `design-onboarding-program` → `write-leadership-principles`
Reason: understand current position before negotiating; negotiate role before starting; onboarding approach before managing

---

**Example 3 — Single skill → delegate**
> "My pull requests keep getting rejected"

One clear skill match — delegate: "Single skill applies. Routing to `suggest-best-practice`..."

---

**Example 4 — Single domain, multiple skills**
> "Apply defensive programming to my codebase"

One domain (engineering), multiple skills needed:
Sequence: `apply-fail-fast` → `apply-defensive-copy` → `validate-external-input`
Reason: fail-fast catches invalid state earliest; defensive copy prevents mutation bugs; input validation at trust boundaries closes the remaining gap

---

**Example 5 — Very complex, hierarchical (nested plan)**
> "Transform our failing company"

Top-level sub-problems: financial restructuring, product strategy, team restructuring, go-to-market
Sub-problem 1 (financial restructuring) is itself multi-skill with known dimensions → nested plan:

```
Here is the solution plan (4 steps):

1. Financial restructuring — nested plan (3 skills):
   1a. audit-financial-statements — establish current financial position
   1b. calculate-wacc — determine cost of capital
   1c. design-capital-structure — restructure debt/equity mix

2. apply-jobs-to-be-done — redefine product strategy around customer outcomes

3. design-hiring-process — restructure team composition

4. design-go-to-market — rebuild market approach on validated product strategy
```

Reason: financial position must be known before product or team decisions can be funded; product strategy before go-to-market

---

## Common Mistakes

**Over-applying to simple problems**: one skill covers the full problem → use `suggest-best-practice`. Domain count is irrelevant — trigger is skill count (2+).

**Ignoring dependencies**: a flat unsequenced list creates rework. Always explain the order.

**Hallucinating skills**: if no skill covers a sub-problem, say so. Don't invent names.

**Pausing between every skill**: do not ask for confirmation between each step — reassess silently after each skill and proceed unless the plan changes. Only pause when new constraints require revising the plan.
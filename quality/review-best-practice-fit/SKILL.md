---
name: review-best-practice-fit
description: Use when the user already has a solution, plan, approach, or design and wants to know how well it aligns with best practices — including gaps, what's missing, and what to fix.
source: McKinsey as-is/to-be gap analysis methodology, Google Engineering Practices design review, ISO 9001 gap audit standards
tags: [gap-analysis, solution-review, practice-alignment, quality-audit, practitioner, decision-maker, solution-improvement, practice-compliance]
---

# Review Best Practice Fit

Evaluate an existing solution against applicable best practices, identify gaps, and produce a prioritized fix list.

## Why This Is Best Practice

**Adopted by:** McKinsey and BCG use structured as-is/to-be gap analysis before every engagement to identify which best practices a client's current approach violates — it is the primary tool for diagnosing why organizations underperform their industry peers. Google's Engineering Practices mandate design reviews against explicit quality criteria before large features ship. ISO 9001 certification requires formal gap audits comparing current processes against the standard before submission.
**Impact:** Google's structured design review process reduces post-ship defects by ~50% and catches architecture problems that survive code review (Google Engineering Practices documentation). ISO 9001 mandates formal gap audits before certification precisely because self-assessment consistently misses systemic gaps — organizations routinely discover critical non-conformances only during external audits that internal reviews missed (ISO 9001:2015 §9.2 internal audit requirements). McKinsey's structured gap analysis prevents clients from investing in solutions that miss the dimensions that actually drive performance — the most expensive mistake in strategy.
**Why best:** Self-assessment without an external standard is systematically optimistic — practitioners overweight what they did and underweight what they omitted. A structured comparison against explicit best-practice criteria catches omissions (the invisible gaps), not just flaws (the visible ones). Ad-hoc feedback ("this looks good, but maybe add X") is alternative — it finds surface problems only and produces no prioritized action plan.

Sources: Google Engineering Practices; ISO 9001:2015 §9.2 internal audit requirements; McKinsey Problem Solving methodology

## Steps

### Step 0: Check preferences (silent)

Resolution order — first match wins:
1. Session memory — pinned this session only; not written to disk (highest precedence)
2. `<project-root>/.grimoire/preferences.md` — project-level
3. `~/.config/grimoire/preferences.md` OR `~/.grimoire/preferences.md` — global-level
4. `CLAUDE.md` `## Grimoire Preferences` section — legacy fallback

For the relevant domain, check if a practice is already pinned:
- **Pinned match (file)** → apply the pinned practice directly; skip scoring entirely. No further action needed — already persisted.
- **Pinned match (session)** → apply the pinned practice directly; skip scoring. After applying, offer once per session per domain using a platform-aware confirm: "Save [practice] for future sessions?" (Claude Code: `AskUserQuestion`; OpenCode: `question`; Gemini CLI: `ask_user type: confirm`; other: `[y/n]`). If yes, invoke `pin-best-practice-preference`.
- **Pinned conflict** → warn before suggesting an alternative using a platform-aware confirm: "You have [X] pinned for [domain]. Suggest changing it?" (Claude Code: `AskUserQuestion`; OpenCode: `question`; Gemini CLI: `ask_user type: confirm`; other: `[y/n]`).
- **No pin** → proceed to Step 1.

### 1. Extract the solution

From the user's description, identify:

| Element | Extract |
|---------|---------|
| **What** | What is the solution, plan, approach, or design? |
| **Domain(s)** | Which fields does it operate in? |
| **Goal** | What problem is it trying to solve? |
| **Constraints** | Any stated limitations (time, budget, team size, technology)? |
| **Maturity** | Is this a draft, in-progress, or already deployed? |

If the solution description is too vague to evaluate, ask ONE targeted question:
```
To review this properly, I need to understand [specific missing element].
Can you describe [that element] in more detail?
```

### 2. Identify applicable practices

Score candidate practices using the `suggest-best-practice` scoring model:

```
score = (tag_overlap × 2) + (description_match × 3) + (domain_plausibility × 1)
```

Select all practices scoring ≥ 0.4. Cap at 7 practices — if more qualify, take the 7 highest-scoring.

If no practice scores ≥ 0.4: state "No installed skills closely match this solution's domain. Install relevant domain skills first."

**No-practices early exit:** After resolving which practices apply to the artifact, if zero practices match (no installed skills cover this domain, or artifact type has no applicable practices), exit immediately. Output:
```
No applicable practices found for [artifact-type/domain].
[If no domain installed]: Install practices with: /plugin install grimoire-[domain]@grimoire
[If domain installed but no match]: This artifact type may not have grimoire coverage yet.
```
Do not proceed to review with zero practices — the review would be empty and misleading.

### 3. Evaluate fit for each practice

For each applicable practice, evaluate the solution against the practice's core criteria:

**ALIGNED** — solution demonstrably follows the practice's key steps and principles
**PARTIAL** — some elements present, but one or more critical criteria are missing or weak
**MISSING** — practice not addressed at all

For each PARTIAL or MISSING verdict, extract:
- What the solution currently does (or doesn't do)
- Which specific criterion from the practice it violates or omits
- The concrete consequence of this gap (what goes wrong without it)

### 4. Prioritize gaps

Classify each gap by impact:

| Priority | When |
|----------|------|
| 🔴 **Critical** | Violates a core principle of the practice; high risk of failure, harm, or waste |
| 🟡 **Significant** | Reduces effectiveness meaningfully; workaround exists but at cost |
| ⚪ **Minor** | Polish or optimization; solution works without it |

Order: Critical → Significant → Minor within the report.

**Fix sequencing:** Recommend fixes in this order:
1. Gaps that block correctness (the artifact won't work / will cause harm without this)
2. Gaps that affect reliability (will likely fail under real conditions)
3. Gaps that affect maintainability (creates future debt)
4. Gaps that affect polish (nice to have)

Do not recommend all gaps as equal priority — users need to know what to fix first.

### 5. Produce the gap report

```
## Practice Fit Review

Solution: [one-sentence description of what was evaluated]

---

### [practice-name] — ALIGNED / PARTIAL / MISSING
Domain: [domain/subdomain]

✓ [What the solution gets right — be specific]
✗ [What's missing or weak — cite the specific criterion]
→ Fix: [concrete action, not advice — what exactly to do]

### [practice-name] — ALIGNED / PARTIAL / MISSING
...

---

### Priority gaps

🔴 Critical
- [gap]: [consequence] → [fix]

🟡 Significant
- [gap]: [consequence] → [fix]

⚪ Minor
- [gap]: [consequence] → [fix]

---

### Verdict
[STRONG / ADEQUATE / NEEDS WORK / REBUILD]
[1–2 sentences: overall assessment and single most important action]
```

**Verdict scale:**
- **STRONG**: ≥ 80% of practices ALIGNED, no Critical gaps
- **ADEQUATE**: no Critical gaps, some Significant gaps
- **NEEDS WORK**: 1+ Critical gaps, core structure is sound
- **REBUILD**: 2+ Critical gaps across different practices, fundamental approach is flawed

### 6. Offer to apply fixes

After the report, list PARTIAL and MISSING practices ranked by gap severity (Critical count first, then Significant), with a recommendation:

```
To close these gaps, I can apply:

  ★ [top-skill] (recommended — [N] Critical gap(s))
    [one sentence: what this skill addresses]

    [second-skill] ([N] Critical / [N] Significant gaps)
    [one sentence: what this skill addresses]

    [third-skill] ([N] Significant gaps)
    [one sentence: what this skill addresses]

```

Then collect the user's choice using the best available method for your platform:
- **Claude Code**: use `AskUserQuestion` — ★ recommended first with "(Recommended)" appended, include "Apply all in sequence" and "Skip" as last two options, `multiSelect: false`
- **OpenCode**: use `question` — same schema as `AskUserQuestion`
- **Gemini CLI**: use `ask_user` — `type: "select"`, same options including "Apply all in sequence" and "Skip"
- **All other platforms**: numbered list:
  ```
  Which would you like to apply? (Enter number, "all" to apply in sequence, or "skip")
  ```

After user selects, load the chosen skill and follow its steps. If user chooses "all", apply each in ranked order silently — no confirmation between steps unless a skill reveals new constraints that change the remaining sequence.

## Rules

- Never fabricate practice criteria — evaluate only against the actual steps and rules in each matched skill
- If a practice is not installed, name it and give the install command instead of skipping it
- ALIGNED does not mean perfect — state what qualifies and what could still improve
- Fix recommendations must be concrete and actionable — not "consider improving X"
- If the solution is already deployed (not a draft), flag Critical gaps as urgent risk, not just improvement opportunities
- Do not soften verdicts — a MISSING is a MISSING, even if the overall solution is otherwise strong

## Examples

> Skill names in examples are illustrative — actual matches depend on what domains are installed. If a skill is not installed, `review-best-practice-fit` names it and gives the install command.

**Example 1 — Engineering architecture review**
> "Our API: REST endpoints, JWT auth, PostgreSQL, deployed on Heroku, no rate limiting, logs to console only."

Matches: `design-api-architecture`, `review-security-posture`, `design-observability`
- `design-api-architecture`: PARTIAL — REST ✓, stateless auth ✓, no versioning ✗, no pagination standard ✗
- `review-security-posture`: MISSING — no rate limiting, no input validation mentioned, JWT secret management unknown
- `design-observability`: MISSING — console logs only, no structured logging, no alerting, no tracing

🔴 Critical: No rate limiting → DoS exposure → add rate limiter at gateway before next deploy
🔴 Critical: No structured logging → incidents uninvestigable → switch to structured JSON logs with correlation IDs

---

**Example 2 — Business plan review**
> "Startup plan: build a mobile app, charge $9.99/month, target college students, raise seed round."

Matches: `design-business-model`, `calculate-unit-economics`
- `design-business-model`: PARTIAL — revenue model ✓, no customer segment validation, no competitive moat stated
- `calculate-unit-economics`: MISSING — no LTV/CAC calculation, no payback period, no cohort assumptions

🔴 Critical: No unit economics → seed investors will reject without LTV/CAC → calculate before fundraising

---

**Example 3 — Strong fit**
> "Code review process: async PR reviews, two approvers required, automated linting and tests must pass, comments must cite a reason, author resolves all comments before merge."

Matches: `review-pull-request`
- ALIGNED — two-approver gate ✓, automated checks ✓, reasoned feedback ✓, resolution required ✓

⚪ Minor: No stated SLA for review turnaround — can cause blocked PRs

Verdict: STRONG — process follows the practice. One minor improvement: add a 24hr review SLA.

## Common Mistakes

**Softening verdicts**: a Critical gap on a deployed system is a risk, not a suggestion. State it clearly.

**Evaluating against invented criteria**: only evaluate against what the matched skill's actual steps say. Don't add your own criteria.

**Skipping ALIGNED items**: report what works too — it confirms the user's judgment and anchors the gaps in context.

**Generic fixes**: "improve your security posture" is not a fix. "Add rate limiting of 100 req/min per IP at the API gateway" is a fix.
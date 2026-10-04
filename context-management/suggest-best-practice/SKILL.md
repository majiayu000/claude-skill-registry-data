---
name: suggest-best-practice
description: Use when the user describes any situation, problem, goal, complaint, or question — including when they want to browse available best practices for a topic, don't know which domain applies, or don't know a best practice exists for their situation. Also use when the user starts any task or action without explicitly asking for guidance.
source: Information retrieval best practices (van Rijsbergen, 1979), Nielsen Norman Group search UX guidelines
tags: [skill-discovery, auto-classify, problem-routing, problem-solver, situation-analysis, practice-recommendation]
---

# Suggest Best Practice

Accept any natural language input, auto-classify it to the relevant domain(s), and
either apply the best-matching skill directly or present a ranked list for the user
to choose from.

## Why This Is Best Practice

**Adopted by:** Zero-knowledge entry points are standard in expert systems and
recommendation engines — Google Search auto-classifies queries without requiring users
to specify intent type, Spotify Discover Weekly infers genres from listening behavior
without requiring genre tags, and Wolfram Alpha auto-routes computations to the correct
solver domain without user specification.
**Impact:** Requiring users to know the domain before getting help is the primary
barrier to knowledge system adoption. Studies on expert system usability (Prerau, 1990)
found that systems requiring users to pre-classify their problems had 3–5× lower
adoption than systems that accepted natural language and routed automatically.
**Why best:** A single entry point — vs. domain-specific skills that require users to
already know which domain and practice applies to their situation — eliminates the
"which skill do I use?" confusion. Users don't need to pre-classify their problem;
`suggest-best-practice` infers domain and intent automatically.

Sources: Prerau (1990) expert system usability research, Nielsen Norman Group search
UX guidelines, Google Search intent classification research

## Steps

### Step 0: Check preferences (silent)

Resolution order — first match wins:
1. Session memory — pinned this session only; not written to disk (highest precedence)
2. `<project-root>/grimoire.toml` — project config, committed to repo (read `[standards.domain.subdomain].practices[0]`)
3. `~/.config/grimoire/grimoire.toml` — global config, this user (same key)
4. `/etc/grimoire/grimoire.toml` — system config, all users on this machine (same key)

For the relevant domain, check if a practice is already pinned:
- **Pinned match (file)** → apply the pinned practice directly; skip scoring entirely. No further action needed — already persisted.
- **Pinned match (session)** → apply the pinned practice directly; skip scoring. After applying, offer once per session per domain using a platform-aware confirm: "Save [practice] for future sessions?" (Claude Code: `AskUserQuestion`; OpenCode: `question`; Gemini CLI: `ask_user type: confirm`; other: `[y/n]`). If yes, invoke `pin-best-practice-preference`.
- **Pinned conflict** → warn before suggesting an alternative using a platform-aware confirm: "You have [X] pinned for [domain]. Suggest changing it?" (Claude Code: `AskUserQuestion`; OpenCode: `question`; Gemini CLI: `ask_user type: confirm`; other: `[y/n]`).
- **No pin** → proceed to Step 1.

### 1. Extract intent signals (no clarifying questions yet)

From the user's input, silently identify:

| Signal | Extract |
|--------|---------|
| **Goal** | What outcome does the user want? |
| **Symptoms** | What problems are they experiencing? |
| **Domain cues** | Industry, role, tool names, context words |
| **Constraints** | Time pressure, team size, resources, urgency |
| **Problem type** | Prevention / diagnosis / optimization / compliance / learning |

Do not ask the user for any of this — infer it from what they wrote.

**Problem clarity check:** After extracting signals, apply skill judgment: can a 1-2 sentence problem statement be written from what the user said? A problem is clear enough to proceed if:
- Goal is inferable (what outcome they want)
- At least the broad scope is known (what domain or area this is in)
- What's described is a root cause or problem, not just a symptom with no surrounding context

If NOT clear enough → invoke `analyze-best-practice-problem` before scoring. Use the problem statement from its output as input to Step 2.
If clear enough → proceed to Step 2.

### 2. Score candidate skills

For each skill in the installed grimoire domains:

```
score = (tag_overlap × 2) + (description_match × 3) + (domain_plausibility × 1)
```

- **tag_overlap**: count of skill tags matching extracted keywords (normalized 0–1)
- **description_match**: does `Use when...` describe this situation? (0 = no, 1 = yes)
- **domain_plausibility**: is this domain plausible given context cues? (0 = no, 0.5 = possible, 1 = likely)

Normalize final scores to 0–1.

### 3. Route by confidence

**Existing solution** — user describes something they already built, planned, or decided and wants evaluation ("is this good?", "what am I missing?", "does this follow best practices?"):

Delegate to `review-best-practice-fit`. Announce:
```
You have an existing solution. Applying review-best-practice-fit to evaluate it against best practices...
```

**Multi-domain** — user has a new problem that spans 3+ domains and requires applying ALL of them (not just one):

Delegate to `plan-best-practice-solution`. Announce:
```
Your situation spans multiple domains and requires coordinating several best practices.
Applying plan-best-practice-solution to build a sequenced action plan...
```

**Sole clear match** — exactly one skill scores ≥ 0.7 AND second-place score < 0.4:

Load and apply the skill directly. Announce before applying:
```
Situation matches: [skill-name] ([domain/subdomain])
Applying now...
```

**Multiple matches** — 2+ skills score ≥ 0.5 (regardless of whether the top score reaches 0.7):

Present a ranked list with recommendation and wait for user selection:
```
Multiple best practices apply. Recommended: [top-skill-name]

1. ★ [top-skill-name] — [one sentence: what problem it solves]  ← recommended
   Domain: [domain/subdomain]  |  Score: [score]  |  Install: /plugin install grimoire-[subdomain]@grimoire

2. [skill-name] — [one sentence: what problem it solves]
   Domain: [domain/subdomain]  |  Score: [score]  |  Install: /plugin install grimoire-[subdomain]@grimoire

3. [skill-name] — [one sentence]
   Domain: [domain/subdomain]  |  Score: [score]  |  Install: ...

```

Then collect the user's choice using the best available method for your platform:
- **Claude Code**: use `AskUserQuestion` — ★ recommended first with "(Recommended)" appended, include "Apply all in sequence" and "Skip" as last two options, `multiSelect: false`
- **OpenCode**: use `question` — same schema as `AskUserQuestion`
- **Gemini CLI**: use `ask_user` — `type: "select"`, same options including "Apply all in sequence" and "Skip"
- **All other platforms**: numbered list:
  ```
  Which would you like to apply? (Enter number, "all" to apply in sequence, or "skip" to proceed without)
  ```

The ★ recommendation is the highest-scoring match. If two skills score equally, recommend the one whose `Use when...` description is the closest literal match to the user's input.

After user selects, load and apply the chosen skill.

**Browse mode** — user explicitly says "show me options", "what practices exist for X",
or "what should I know about Y" without wanting to act yet:

If the user's intent is pure discovery with no problem to solve (e.g., "what practices exist for X", "show me what grimoire can do"), defer to `discover-best-practices` instead — that skill is purpose-built for domain browsing without a problem context.

Present the ranked list only, do not apply any skill:
```
Best practices for: [topic]

1. [skill-name] — [one sentence: what it solves]
   Domain: [domain/subdomain]  |  Install: /plugin install grimoire-[subdomain]@grimoire

2. ...
```
After listing, collect the user's choice using the best available method for your platform:
- **Claude Code**: use `AskUserQuestion` — list all skills as options (no ★ in browse mode), `multiSelect: false`
- **OpenCode**: use `question` — same schema as `AskUserQuestion`
- **Gemini CLI**: use `ask_user` — `type: "select"`, list all skills as options
- **All other platforms**: `"Say the number or skill name to apply one."`

**No match** — all skills score < 0.3:

Threshold for "no match": top score < 0.3. Template clarifying question: "Is this about your [inferred-domain-guess], or something else — [alternative-domain]?"

State clearly that no skills currently cover this area, then ask ONE targeted
clarifying question to narrow the domain:
```
No installed skills match this situation closely.
[One clarifying question to narrow the domain — e.g., "Is this about your code, your health, your finances, or something else?"]
```

After the user answers, treat their answer as additional domain context and re-run Step 1 with the refined input — re-extract intent signals using the new domain information, then re-score in Step 2. If still no match after one clarification, state: "No installed skills cover this area — you may need to install a domain first."

### 4. Apply the matched skill

Before applying, check: does the user's situation depend on current, specific, or fast-changing facts the skill itself can't encode — a jurisdiction's current regulation, a tool's current API/behavior, a current rate or price, a recent event? If so, search the internet for that specific context first, and announce it: "Checking current [X] before applying [skill-name]..." Keep the query itself general and factual (e.g. "current mortgage rates," not the user's specific financial or personal details). If no internet-access tool is available in this environment, say so explicitly and proceed on best available knowledge — flag the gap as unverified rather than silently skipping the check or asserting it was confirmed. After searching, state what was found (or that nothing conclusive turned up) before proceeding — don't just announce the check and discard the result.

Then load the skill using the Skill tool and follow its steps, grounded in that current context (or in best available knowledge, if unverified).

If nothing situation-specific needs verifying, load the skill using the Skill tool and follow its steps exactly.

### 5. Check for cross-domain coverage

After applying the primary skill, check: does the user's situation span additional
domains with independent high-confidence matches?

- **1 additional domain**: ask once: "This situation also touches [domain] — [skill-name] applies to that aspect. Want me to apply it?"
- **2+ additional domains**: delegate to `plan-best-practice-solution` — "This situation spans multiple domains. Want me to build a full solution plan?"

Cross-domain notice format: state it as a follow-up after the primary skill completes — "This situation also touches [domain]. Want me to apply [skill-name] for that aspect?"

Always include 'No, stop here' as an explicit option in the cross-domain offer. Do not re-ask after one rejection — if user declines the first cross-domain offer, end the chain immediately and complete only the primary skill's output. Never chain to a third skill without explicit user request.

Do not chain more than 2 skills without user confirmation. If 3+ skills are needed, use `plan-best-practice-solution`.

## Rules

- Never ask the user which domain their problem belongs to — that's the skill's job to figure out
- Auto-apply only when exactly 1 skill ≥ 0.7 AND second place < 0.4 — truly unambiguous
- Whenever 2+ skills score ≥ 0.4, always list with recommendation — never silently pick one
- Always mark the recommended option with ★
- Max 5 options in a ranked list; drop lower-scoring matches beyond 5
- Never hallucinate skill names — only reference skills that exist in installed domains
- Announce the matched skill before applying — don't silently load skills
- If a skill is not installed, include the install command in the suggestion
- Search the internet for current, situation-specific facts before applying a skill when its generic guidance depends on something that changes over time (rates, regulations, tool behavior) — announce this check, don't do it silently or ask permission first; if unavailable, say so and flag as unverified

## Examples

**Example 1 — High confidence, single domain**
> "My pull requests keep getting rejected in code review"

Extract: goal=pass-review, symptoms=PR-rejection, domain-cues=code/pull-request/review
Top match: `code-review` (engineering/development) — score 0.82
→ Apply directly: "Situation matches: code-review (engineering/development). Applying now..."

---

**Example 2 — Multiple matches**
> "I always feel exhausted after training"

Extract: goal=recover-better, symptoms=fatigue/exhaustion, domain-cues=training/workout
Top matches (similar scores):
1. `optimize-recovery` (health/fitness) — 0.61
2. `calculate-macros` (health/nutrition) — 0.54
3. `design-training-program` (health/fitness) — 0.49
→ Present ranked list, wait for user selection

---

**Example 3 — No match, clarifying question**
> "I don't know what to do with my life"

Extract: goal=unclear, symptoms=directionlessness, domain-cues=none
All scores < 0.3
→ "No installed skills closely match this. Is this about your career, your health, your finances, or something else?"

## Common Mistakes

**Asking the user to classify their own problem**: "Is this an engineering problem or
a business problem?" — never do this. Route silently, present choices only when
genuinely ambiguous.

**Over-confident routing**: applying a skill when the top score is 0.5 with a close
second-place match. Present choices when it's close.

**Applying too many skills**: chaining 3+ skills without confirmation overwhelms the
user. One at a time, ask before adding the second domain.

**Hallucinating skills**: if no skill exists for the situation, say so. Don't invent
skill names.
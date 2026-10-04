---
name: skill-judge
description: "Evaluate Agent Skill design quality against official specifications and patterns. Use when user runs /skill-judge, asks to review or audit a SKILL.md file, wants to improve an existing skill, or needs to score skill quality. Provides 8-dimension scoring (120 points), knowledge delta analysis, and actionable improvement suggestions for SKILL.md files and skill packages."
source: ~/.agents/skills@2026-07-13
---


# Skill Judge

Evaluate Agent Skills against official specifications and patterns derived from 17+ official examples.

---

## Core Philosophy

> **Good Skill = Expert-only Knowledge - What Claude Already Knows**

A Skill is a **knowledge externalization mechanism** — a hot-swappable behavior modifier via Markdown. Edit SKILL.md, save, and the model's behavior changes on next invocation. No training, no GPU, instant effect.

A Skill's value is its **knowledge delta**: the gap between what it provides and what the model already knows. Expert-only knowledge (decision trees, trade-offs, edge cases, anti-patterns) earns its tokens. Basic concepts and standard patterns waste them — context window is a shared public resource.

### Tool vs Skill

| Concept | Essence | Function | Example |
|---------|---------|----------|---------|
| **Tool** | What model CAN do | Execute actions | bash, read_file, WebSearch |
| **Skill** | What model KNOWS how to do | Guide decisions | PDF processing, MCP building |

`General Agent + Excellent Skill = Domain Expert Agent`

### Three Knowledge Types (E:A:R)

| Type | Definition | Treatment |
|------|------------|-----------|
| **Expert [E]** | Claude genuinely doesn't know this | Must keep — the Skill's value |
| **Activation [A]** | Claude knows but may not think of | Keep if brief — serves as reminder |
| **Redundant [R]** | Claude definitely knows this | Delete — wastes tokens |

The art: maximize Expert, use Activation sparingly, eliminate Redundant ruthlessly.

---

## Evaluation Dimensions (120 points total)

### D1: Knowledge Delta (20 points) — THE CORE DIMENSION

Does the Skill add genuine expert knowledge?

| Score | Criteria |
|-------|----------|
| 0-5 | Explains basics Claude knows (what is X, standard tutorials) |
| 6-10 | Mixed: some expert knowledge diluted by obvious content |
| 11-15 | Mostly expert knowledge with minimal redundancy |
| 16-20 | Pure knowledge delta — every paragraph earns its tokens |

**Evaluation**: For each section ask "Does Claude already know this?" Count E:A:R ratio. Good Skill: >70% Expert, <20% Activation, <10% Redundant.

See [references/examples.md](references/examples.md) for D1 red/green flag calibration examples.

---

### D2: Mindset + Appropriate Procedures (15 points)

Does the Skill transfer expert **thinking patterns** along with **necessary domain-specific procedures**?

| Type | Value |
|------|-------|
| **Thinking patterns** ("Before designing, ask: What makes this memorable?") | High — shapes decisions |
| **Domain-specific procedures** (OOXML workflow: unpack, edit XML, validate, pack) | High — Claude may not know |
| **Generic procedures** (Step 1: Open file, Step 2: Edit, Step 3: Save) | Low — Claude already knows |

| Score | Criteria |
|-------|----------|
| 0-3 | Only generic procedures Claude already knows |
| 4-7 | Has domain procedures but lacks thinking frameworks |
| 8-11 | Good balance: thinking patterns + domain-specific workflows |
| 12-15 | Expert-level: shapes thinking AND provides procedures Claude wouldn't know |

**The test**: Does it tell Claude WHAT to think about (patterns) AND HOW to do things it wouldn't know (procedures)?

See [references/examples.md](references/examples.md) for D2 examples.

---

### D3: Anti-Pattern Quality (15 points)

Does the Skill have effective NEVER lists? Half of expert knowledge is knowing what NOT to do.

| Score | Criteria |
|-------|----------|
| 0-3 | No anti-patterns mentioned |
| 4-7 | Generic warnings ("avoid errors", "be careful") |
| 8-11 | Specific NEVER list with some reasoning |
| 12-15 | Expert-grade anti-patterns with WHY — things only experience teaches |

**The test**: Would an expert say "yes, I learned this the hard way"? Or "this is obvious to everyone"?

See [references/examples.md](references/examples.md) for D3 examples.

---

### D4: Specification Compliance — Especially Description (15 points)

**Description is THE MOST IMPORTANT field** — it's the ONLY thing the Agent sees before deciding to load a Skill. Perfect content with poor description = useless Skill that never activates.

| Score | Criteria |
|-------|----------|
| 0-5 | Missing frontmatter or invalid format |
| 6-10 | Has frontmatter but description is vague or incomplete |
| 11-13 | Valid frontmatter, description has WHAT but weak on WHEN |
| 14-15 | Perfect: comprehensive description with WHAT, WHEN, and trigger keywords |

**Description must answer THREE questions**:
1. **WHAT**: What does this Skill do? (functionality)
2. **WHEN**: In what situations should it be used? (trigger scenarios)
3. **KEYWORDS**: What terms should trigger this Skill? (searchable terms)

**Frontmatter requirements**: `name` lowercase, alphanumeric + hyphens, <=64 chars. `description` must include WHAT + WHEN + KEYWORDS.

**Description quality checklist**:
- [ ] Lists specific capabilities (not just "helps with X")
- [ ] Includes explicit trigger scenarios ("Use when...", "When user asks for...")
- [ ] Contains searchable keywords (file extensions, domain terms, action verbs)
- [ ] Specific enough that Agent knows EXACTLY when to use it

See [references/examples.md](references/examples.md) for D4 good/bad description examples.

---

### D5: Progressive Disclosure (15 points)

Three loading layers:
```
Layer 1: Metadata (always in memory) — name + description (~100 tokens)
Layer 2: SKILL.md Body (loaded after triggering) — guidelines, decision trees (< 500 lines)
Layer 3: Resources (loaded on demand) — scripts/, references/, assets/ (no limit)
```

| Score | Criteria |
|-------|----------|
| 0-5 | Everything dumped in SKILL.md (>500 lines, no structure) |
| 6-10 | Has references but unclear when to load them |
| 11-13 | Good layering with MANDATORY triggers present |
| 14-15 | Perfect: decision trees + explicit triggers + "Do NOT Load" guidance |

**Loading trigger quality**: Poor = references listed at end. Good = MANDATORY triggers in workflow steps. Excellent = scenario detection + conditional triggers + "Do NOT Load" guidance.

See [references/examples.md](references/examples.md) for D5 loading trigger examples.

---

### D6: Freedom Calibration (15 points)

Match freedom to task fragility.

| Task Type | Freedom Level | Why | Example |
|-----------|---------------|-----|---------|
| Creative/Design | High | Multiple valid approaches | frontend-design |
| Code review | Medium | Principles + judgment | code-review |
| File format ops | Low | One wrong byte corrupts | docx, xlsx, pdf |

| Score | Criteria |
|-------|----------|
| 0-5 | Severely mismatched (rigid for creative, vague for fragile) |
| 6-10 | Partially appropriate, some mismatches |
| 11-13 | Good calibration for most scenarios |
| 14-15 | Perfect freedom calibration throughout |

**The test**: "If Agent makes a mistake, what's the consequence?" High consequence = low freedom, low consequence = high freedom.

See [references/examples.md](references/examples.md) for D6 examples.

---

### D7: Pattern Recognition (10 points)

5 official patterns from 17+ Skills:

| Pattern | ~Lines | When to Use |
|---------|--------|-------------|
| **Mindset** | ~50 | Creative tasks requiring taste |
| **Navigation** | ~30 | Multiple distinct scenarios |
| **Philosophy** | ~150 | Art/creation requiring originality |
| **Process** | ~200 | Complex multi-step projects |
| **Tool** | ~300 | Precise operations on specific formats |

| Score | Criteria |
|-------|----------|
| 0-3 | No recognizable pattern, chaotic structure |
| 4-6 | Partially follows a pattern with significant deviations |
| 7-8 | Clear pattern with minor deviations |
| 9-10 | Masterful application of appropriate pattern |

---

### D8: Practical Usability (15 points)

Can an Agent actually use this Skill effectively?

| Score | Criteria |
|-------|----------|
| 0-5 | Confusing, incomplete, contradictory, or untested |
| 6-10 | Usable but with noticeable gaps |
| 11-13 | Clear guidance for common cases |
| 14-15 | Comprehensive: decision trees, working examples, fallbacks, edge cases |

**Check for**: Decision trees for multi-path scenarios, working code examples, error handling/fallbacks, edge case coverage, immediate actionability.

See [references/examples.md](references/examples.md) for D8 examples.

---

## NEVER Do When Evaluating

- **NEVER** give high scores just because it "looks professional" or is well-formatted
- **NEVER** ignore token waste — every redundant paragraph = deduction
- **NEVER** let length impress you — a 43-line Skill can outperform 500 lines
- **NEVER** skip mentally testing decision trees — do they lead to correct choices?
- **NEVER** forgive explaining basics with "but it provides helpful context"
- **NEVER** overlook missing anti-patterns — no NEVER list = significant gap
- **NEVER** assume all procedures are valuable — distinguish domain-specific from generic
- **NEVER** undervalue the description field — poor description = skill never gets used
- **NEVER** put "when to use" info only in the body — Agent only sees description before loading

---

## Evaluation Protocol

### Step 1: First Pass — Knowledge Delta Scan

**MANDATORY**: Read [references/examples.md](references/examples.md) for calibration benchmarks before scoring.

Read SKILL.md completely. For each section, mark:
- **[E] Expert**: Claude genuinely doesn't know — value-add
- **[A] Activation**: Claude knows but brief reminder useful — acceptable
- **[R] Redundant**: Claude definitely knows — should delete

Calculate E:A:R ratio. Good: >70% E, <20% A, <10% R.

### Step 2: Structure Analysis

```
[ ] Check frontmatter validity
[ ] Count total lines in SKILL.md
[ ] List all reference files and sizes
[ ] Identify which pattern the Skill follows
[ ] Check for loading triggers (if references exist)
```

### Step 3: Score Each Dimension

**MANDATORY**: Read [references/examples.md](references/examples.md) to calibrate your scoring.

For each of the 8 dimensions:
1. Find specific evidence (quote relevant lines)
2. Assign score with one-line justification
3. Note specific improvements if score < max

### Step 4: Calculate Total & Grade

```
Total = D1 + D2 + D3 + D4 + D5 + D6 + D7 + D8 (max 120)
```

Grade thresholds are PERCENTAGES of the 120-point max — compute `pct = total / 120`, then
compare against the percentage cutoff. The point column is the exact `ceil(pct * 120)` floor for
that grade, shown only as a convenience; the percentage is authoritative when they appear to
disagree.

| Grade | Cutoff (% of 120) | Point floor | Meaning |
|-------|-------------------|-------------|---------|
| A | >= 90% | 108/120 | Excellent — production-ready expert Skill |
| B | >= 82.5% | 99/120 | Good — minor improvements needed |
| C | >= 70% | 84/120 | Adequate — clear improvement path |
| D | >= 60% | 72/120 | Below Average — significant issues |
| F | < 60% | below 72/120 | Poor — needs fundamental redesign |

> **Do NOT apply the cutoff as a raw number against a different max.** "B >= 82.5" means
> `pct >= 82.5%` (i.e. total >= 99/120), NOT `total >= 82.5 points`. Always divide by 120 first.

**If total score < 70%**: MANDATORY — read [references/failure-patterns.md](references/failure-patterns.md) to identify root pattern before writing recommendations.

**Do NOT load** [references/checklist.md](references/checklist.md) during full evaluations — it's for quick audits only.

**Do NOT load** [references/failure-patterns.md](references/failure-patterns.md) unless score < 70% or you identify a specific failure pattern.

### Step 5: Generate Report

```markdown
# Skill Evaluation Report: [Skill Name]

## Summary
- **Total Score**: X/120 (X%)
- **Grade**: [A/B/C/D/F]
- **Pattern**: [Mindset/Navigation/Philosophy/Process/Tool]
- **Knowledge Ratio**: E:A:R = X:Y:Z
- **Verdict**: [One sentence assessment]

## Dimension Scores

| Dimension | Score | Max | Notes |
|-----------|-------|-----|-------|
| D1: Knowledge Delta | X | 20 | |
| D2: Mindset vs Mechanics | X | 15 | |
| D3: Anti-Pattern Quality | X | 15 | |
| D4: Specification Compliance | X | 15 | |
| D5: Progressive Disclosure | X | 15 | |
| D6: Freedom Calibration | X | 15 | |
| D7: Pattern Recognition | X | 10 | |
| D8: Practical Usability | X | 15 | |

## Critical Issues
[List must-fix problems]

## Top 3 Improvements
1. [Highest impact improvement with specific guidance]
2. [Second priority]
3. [Third priority]

## Detailed Analysis
[For each dimension below 80%: what's missing, specific examples, concrete suggestions]
```

---

## The Meta-Question

> **"Would an expert in this domain, looking at this Skill, say:
> 'Yes, this captures knowledge that took me years to learn'?"**

If yes, the Skill has genuine value. If no, it's compressing what Claude already knows.

The best Skills are **compressed expert brains** — they take years of accumulated knowledge and compress it into focused, actionable guidance.

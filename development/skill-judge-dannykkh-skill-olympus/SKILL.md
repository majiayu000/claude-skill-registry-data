---
name: skill-judge
description: Evaluate Agent Skill design quality against official specifications and best practices. Use when reviewing, auditing, or improving SKILL.md files and skill packages. Provides multi-dimensional scoring and actionable improvement suggestions.
---

# Skill Judge

Evaluate Agent Skills against official specifications and representative official examples.

---

## Core Philosophy

### What is a Skill?

A Skill is NOT a tutorial. A Skill is a **knowledge externalization mechanism**.

Traditional AI knowledge is locked in model parameters. To teach new capabilities:
```
Traditional: Collect data → GPU cluster → Train → Deploy new version
Cost: $10,000 - $1,000,000+
Timeline: Weeks to months
```

Skills change this:
```
Skill: Edit SKILL.md → Save → Takes effect on next invocation
Cost: $0
Timeline: Instant
```

This is the paradigm shift from "training AI" to "educating AI" — like a hot-swappable LoRA adapter that requires no training. You edit a Markdown file in natural language, and the model's behavior changes.

### The Core Formula

> **Good Skill = Expert-only Knowledge − What the Base Model Already Knows**

A Skill's value is measured by its **knowledge delta** — the gap between what it provides and what the model already knows.

- **Expert-only knowledge**: Decision trees, trade-offs, edge cases, anti-patterns, domain-specific thinking frameworks — things that take years of experience to accumulate
- **What the base model already knows**: Basic concepts, standard library usage, common programming patterns, general best practices

When a Skill explains "what is PDF" or "how to write a for-loop", it's compressing knowledge the base model already has. This is **token waste** — context window is a public resource shared with system prompts, conversation history, other Skills, and user requests.

### Tool vs Skill

| Concept | Essence | Function | Example |
|---------|---------|----------|---------|
| **Tool** | What model CAN do | Execute actions | bash, read_file, write_file, WebSearch |
| **Skill** | What model KNOWS how to do | Guide decisions | PDF processing, MCP building, frontend design |

Tools define capability boundaries — without bash tool, model can't execute commands.
Skills inject knowledge — without frontend-design Skill, model produces generic UI.

**The equation**:
```
General Agent + Excellent Skill = Domain Expert Agent
```

The same base model, with different Skills loaded, becomes different experts.

### Three Types of Knowledge in Skills

When evaluating, categorize each section:

| Type | Definition | Treatment |
|------|------------|-----------|
| **Expert** | The base model genuinely doesn't know this | Must keep — this is the Skill's value |
| **Activation** | The base model knows but may not think of it | Keep if brief — serves as reminder |
| **Redundant** | The base model definitely knows this | Should delete — wastes tokens |

The art of Skill design is maximizing Expert content, using Activation sparingly, and eliminating Redundant ruthlessly.

---

## Evaluation Dimensions (120 points total)

### D1: Knowledge Delta (20 points) — THE CORE DIMENSION

The most important dimension. Does the Skill add genuine expert knowledge?

| Score | Criteria |
|-------|----------|
| 0-5 | Explains basics the base model knows (what is X, how to write code, standard library tutorials) |
| 6-10 | Mixed: some expert knowledge diluted by obvious content |
| 11-15 | Mostly expert knowledge with minimal redundancy |
| 16-20 | Pure knowledge delta — every paragraph earns its tokens |

**Red flags** (instant score ≤5):
- "What is [basic concept]" sections
- Step-by-step tutorials for standard operations
- Explaining how to use common libraries
- Generic best practices ("write clean code", "handle errors")
- Definitions of industry-standard terms

**Green flags** (indicators of high knowledge delta):
- Decision trees for non-obvious choices ("when X fails, try Y because Z")
- Trade-offs only an expert would know ("A is faster but B handles edge case C")
- Edge cases from real-world experience
- "NEVER do X because [non-obvious reason]"
- Domain-specific thinking frameworks

**Evaluation questions**:
1. For each section, ask: "Does the base model already know this?"
2. If explaining something, ask: "Is this explaining to the model or guiding its work?"
3. Count paragraphs that are Expert vs Activation vs Redundant

---

### D2: Mindset + Appropriate Procedures (15 points)

Does the Skill transfer expert **thinking patterns** along with **necessary domain-specific procedures**?

**Key distinction**:
| Type | Example | Value |
|------|---------|-------|
| **Thinking patterns** | "Before designing, ask: What makes this memorable?" | High — shapes decision-making |
| **Domain-specific procedures** | "OOXML workflow: unpack → edit XML → validate → pack" | High — the base model may not know this |
| **Generic procedures** | "Step 1: Open file, Step 2: Edit, Step 3: Save" | Low — the base model already knows |

| Score | Criteria |
|-------|----------|
| 0-3 | Only generic procedures the base model already knows |
| 4-7 | Has domain procedures but lacks thinking frameworks |
| 8-11 | Good balance: thinking patterns + domain-specific workflows |
| 12-15 | Expert-level: shapes thinking AND provides procedures the base model would not know |

---

### D3: Anti-Pattern Quality (15 points)

Does the Skill have effective NEVER lists?

| Score | Criteria |
|-------|----------|
| 0-3 | No anti-patterns mentioned |
| 4-7 | Generic warnings ("avoid errors", "be careful", "consider edge cases") |
| 8-11 | Specific NEVER list with some reasoning |
| 12-15 | Expert-grade anti-patterns with WHY — things only experience teaches |

---

### D4: Specification Compliance — Especially Description (15 points)

Does the Skill follow official format requirements? **Special focus on description quality.**

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

---

### D5: Progressive Disclosure (15 points)

Does the Skill implement proper content layering?

```
Layer 1: Metadata (always in memory) — Only name + description (~100 tokens)
Layer 2: SKILL.md Body (loaded after triggering) — Ideal: < 500 lines
Layer 3: Resources (loaded on demand) — scripts/, references/, assets/
```

| Score | Criteria |
|-------|----------|
| 0-5 | Everything dumped in SKILL.md (>500 lines, no structure) |
| 6-10 | Has references but unclear when to load them |
| 11-13 | Good layering with MANDATORY triggers present |
| 14-15 | Perfect: decision trees + explicit triggers + "Do NOT Load" guidance |

---

### D6: Freedom Calibration (15 points)

Is the level of specificity appropriate for the task's fragility?

| Task Type | Should Have | Why |
|-----------|-------------|-----|
| Creative/Design | High freedom | Multiple valid approaches |
| Code review | Medium freedom | Principles exist but judgment required |
| File format operations | Low freedom | One wrong byte corrupts file |

| Score | Criteria |
|-------|----------|
| 0-5 | Severely mismatched (rigid scripts for creative tasks, vague for fragile ops) |
| 6-10 | Partially appropriate, some mismatches |
| 11-13 | Good calibration for most scenarios |
| 14-15 | Perfect freedom calibration throughout |

---

### D7: Pattern Recognition (10 points)

Does the Skill follow an established official pattern?

| Pattern | ~Lines | Key Characteristics | When to Use |
|---------|--------|---------------------|-------------|
| **Mindset** | ~50 | Thinking > technique, strong NEVER list | Creative tasks |
| **Navigation** | ~30 | Minimal SKILL.md, routes to sub-files | Multiple distinct scenarios |
| **Philosophy** | ~150 | Two-step: Philosophy → Express | Art/creation |
| **Process** | ~200 | Phased workflow, checkpoints | Complex multi-step projects |
| **Tool** | ~300 | Decision trees, code examples | Precise operations |

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
| 0-5 | Confusing, incomplete, contradictory, or untested guidance |
| 6-10 | Usable but with noticeable gaps |
| 11-13 | Clear guidance for common cases |
| 14-15 | Comprehensive coverage including edge cases and error handling |

---

## Evaluation Pitfalls

Formatting and length are the most common traps when scoring Skills.

- **Formatting ≠ knowledge delta.** A polished layout with headers, tables, and bold text can still be pure Redundant content. Score what the text says, not how it looks.
- **Token waste is a real cost.** Every redundant paragraph consumes context window shared with system prompts, conversation history, and the user's actual request. A paragraph explaining "what is a unit test" costs the same tokens as a paragraph explaining a non-obvious edge case — but only one earns its place.
- **Length can signal poor editing.** A 43-line Skill with pure Expert content outperforms a 500-line Skill diluted with basics. When length impresses you, ask: "Is this long because the domain is complex, or because the author didn't cut?"
- **Decision trees need mental execution.** Read each branch and trace it: does following the tree actually lead to a correct outcome? A tree that looks comprehensive but leads to wrong choices is worse than no tree.
- **"Helpful context" is often Redundant.** When content could be justified as "helpful context," ask whether the model needs that context or already has it. If the base model already knows it, the context isn't helpful — it's noise.
- **Missing anti-patterns are a gap.** Expert knowledge lives in what NOT to do. A Skill with no NEVER list likely hasn't captured the hard-won lessons from experience.
- **Generic procedures and domain-specific procedures look similar but aren't.** "Open file, edit, save" is generic. "Unpack OOXML, edit XML nodes, validate schema, repack" is domain-specific. One adds value, one doesn't.
- **Description is load-gating.** The Agent reads description before deciding to load the Skill. If description doesn't explain WHEN to use it, the Skill may never trigger — making the body irrelevant. Poor description = invisible Skill.
- **"When to use" in the body only is a structural mistake.** The body loads only after the Skill is triggered. Trigger conditions belong in the description.

---

## Evaluation Protocol

### Step 1: First Pass — Knowledge Delta Scan

Read SKILL.md completely and for each section ask:
> "Does the base model already know this?"

Mark each section as:
- **[E] Expert**: The base model genuinely doesn't know this — value-add
- **[A] Activation**: The base model knows but a brief reminder is useful — acceptable
- **[R] Redundant**: The base model definitely knows this — should be deleted

Calculate rough ratio: E:A:R
- Good Skill: >70% Expert, <20% Activation, <10% Redundant
- Mediocre Skill: 40-70% Expert, high Activation
- Bad Skill: <40% Expert, high Redundant

### Step 2: Structure Analysis

```
[ ] Check frontmatter validity
[ ] Count total lines in SKILL.md
[ ] List all reference files and their sizes
[ ] Identify which pattern the Skill follows
[ ] Check for loading triggers (if references exist)
```

### Step 3: Score Each Dimension

For each of the 8 dimensions:
1. Find specific evidence (quote relevant lines)
2. Assign score with one-line justification
3. Note specific improvements if score < max

### Step 4: Calculate Total & Grade

```
Total = D1 + D2 + D3 + D4 + D5 + D6 + D7 + D8
Max = 120 points
```

| Grade | Percentage | Meaning |
|-------|------------|---------|
| A | 90%+ (108+) | Excellent — production-ready expert Skill |
| B | 80-89% (96-107) | Good — minor improvements needed |
| C | 70-79% (84-95) | Adequate — clear improvement path |
| D | 60-69% (72-83) | Below Average — significant issues |
| F | <60% (<72) | Poor — needs fundamental redesign |

### Step 4.5: Independent Adversarial Cross-Check (독립 교차검증)

> ⚠️ Steps 1~4 are one model's self-introspection ("Does the base model already know this?"). Scores from unaided
> self-judgment are unreliable — intrinsic self-correction without external feedback often fails to catch its
> own errors. Before finalizing scores, cross-check with an INDEPENDENT lens.

1. **Independent scoring pass** — when native delegation is available, assign a **read-only review role**
   the same SKILL.md and the OPPOSITE stance. It may read evidence but must not edit the skill or report:
   "Refute the Steps 1~4 verdict — are items marked [E] Expert actually [R] Redundant knowledge the base
   model already has? Are the scores too generous?" Re-score all 8 dimensions independently. Use the
   current CLI's built-in explorer/reviewer; do not require a custom agent name or vendor-specific spawn schema.
   If delegation is unavailable, run this adversarial pass sequentially in the main context before reconciliation
   and label it `cross-check: sequential-main` rather than claiming independent-agent validation.
2. **Reconcile** — compare per-dimension scores. Any dimension differing by ≥3 points: re-examine the evidence
   and converge to an agreed score. If no agreement, take the conservative (lower) score and note it in the report.
3. **[R] Redundant requires an external signal** — do not delete-recommend on self-judgment alone. Back each
   "Redundant" verdict with an external signal where possible: the same content in official docs/examples, or a
   codebase grep showing it already exists. No external signal → do not recommend deletion on "the model knows it" alone.

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
1. [Highest impact improvement]
2. [Second priority]
3. [Third priority]
```

---

## Common Failure Patterns & Quick Reference

> 상세: [references/evaluation-details.md](references/evaluation-details.md) — 9가지 실패 패턴 (Tutorial, Dump, Orphan References 등) + 평가 체크리스트

---

## The Meta-Question

When evaluating any Skill, always return to this fundamental question:

> **"Would an expert in this domain, looking at this Skill, say:**
> **'Yes, this captures knowledge that took me years to learn'?"**

If the answer is yes → the Skill has genuine value.
If the answer is no → it's compressing what the base model already knows.

The best Skills are **compressed expert brains** — they take a designer's 10 years of aesthetic accumulation and compress it into 43 lines, or a document expert's operational experience into a 200-line decision tree.

What gets compressed must be things the base model doesn't have. Otherwise, it's garbage compression.

---

## Self-Evaluation Note

This Skill (skill-judge) should itself pass evaluation:

- **Knowledge Delta**: Provides specific evaluation criteria the base model would not generate on its own
- **Mindset**: Shapes how to think about Skill quality, not just checklist items
- **Anti-Patterns**: "NEVER Do When Evaluating" section with specific don'ts
- **Specification**: Valid frontmatter with comprehensive description
- **Progressive Disclosure**: Heavy content in references/
- **Freedom**: Medium freedom appropriate for evaluation task
- **Pattern**: Follows Tool pattern with decision frameworks
- **Usability**: Clear protocol, report template, quick reference

Evaluate this Skill against itself as a calibration exercise.

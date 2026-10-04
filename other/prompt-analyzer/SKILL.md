---
name: prompt-analyzer
description: Analyze prompts for constraint complexity, audit failure risks, and generate optimized rewrites for Claude and GPT. Based on "How LLMs Follow Instructions" (Rocchetti & Ferrara, 2026) constraint taxonomy research. Use when reviewing prompt files, optimizing prompt bases, or auditing instruction quality. Trigger phrases — "analyze prompt", "prompt audit", "optimize prompts", "constraint analysis", "prompt review", "check prompts".
---

# Prompt Constraint Analyzer

Analyze prompts using the constraint taxonomy from "How LLMs Follow Instructions: Skillful Coordination, Not a Universal Mechanism" (Rocchetti & Ferrara, Universita degli Studi di Milano, 2026).

## Core Research Findings (Your Knowledge Base)

These findings drive ALL analysis decisions:

1. **Compositional, not monolithic.** LLMs do NOT have a single "instruction-following module." They coordinate separate skills for different constraint types. More types mixed = harder coordination = higher failure risk.

2. **Layer stratification.** Constraints process at different network depths:
   - **Structural** (word count, format, JSON) — early layers, fast to detect
   - **Lexical** (include/exclude words) — middle layers
   - **Semantic** (topic, sentiment, tone) — late layers, slow to detect
   - **Stylistic** (register, formality, persona) — late layers

3. **Monitoring, not planning.** The model does NOT pre-plan constraint satisfaction before generating. It monitors constraints dynamically during token generation. Constraints mentioned earlier in the prompt are monitored longer. Order matters.

4. **Asymmetric dependencies.** Some skill pairs share representations (topic<->sentiment, exclusion<->toxicity), others are independent. Combining dependent skills is easier than combining independent ones.

5. **Model-specific strategies.** Claude tends toward constraint-specific encoding (better separation). GPT models vary. Same prompt may need different structure for different models.

## Input Format

The skill accepts a **file path** as argument. The file contains prompts separated by `---` on its own line. If there is only one prompt, no separator needed.

Example file:
```
You are a helpful marketing assistant. Write a 200-word blog post
about AI trends in formal tone. Include the word "innovation" at least twice.
Do not use the word "revolution". Format as 3 paragraphs with headers.
---
Summarize this document in bullet points. Keep it under 100 words.
---
Write a product description for our new feature. Be enthusiastic but professional.
```

## Execution Process

<HARD-GATE>
You MUST follow ALL phases in order. Do NOT skip the rewrite phase. Do NOT skip scoring.
</HARD-GATE>

### Phase 0: Read Input

1. Read the file at the provided path
2. Split into individual prompts by `---` separator
3. Number each prompt (P1, P2, P3...)
4. If the file contains structured data (JSON, YAML), extract the prompt/instruction fields intelligently

### Phase 1: Constraint Extraction

For EACH prompt, identify every constraint and classify it:

**Constraint Types:**

| Type | Code | What to look for | Examples |
|------|------|-------------------|----------|
| Structural | `STR` | Length limits, format requirements, count requirements, output structure | "max 200 words", "as JSON", "3 paragraphs", "numbered list", "table format" |
| Lexical | `LEX` | Required/forbidden words, terminology, specific phrases | "include X", "don't use Y", "start with Z", "mention A and B" |
| Semantic | `SEM` | Topic scope, sentiment, meaning boundaries, audience | "about marketing", "positive tone", "for beginners", "B2B focused" |
| Stylistic | `STY` | Register, persona, voice, writing style | "formal", "as an expert", "conversational", "academic", "like a friend" |

**Also detect:**

| Meta-type | Code | What to look for |
|-----------|------|-------------------|
| Implicit constraint | `IMP` | Unstated expectations implied by context (e.g., "LinkedIn post" implies hashtags, emoji norms, length norms) |
| Conflict | `CON` | Two constraints that pull in opposite directions (e.g., "formal" + "fun and casual") |
| Dependency | `DEP` | Constraint B requires constraint A to be satisfied first (e.g., "summarize in formal tone" — must understand content before applying register) |
| Ambiguity | `AMB` | Constraint that could be interpreted multiple ways (e.g., "short" without specifying how short) |

**Output format for each prompt:**
```
## P1: [first 50 chars of prompt...]

### Constraints
1. [STR] "max 200 words" — word count limit
2. [LEX] "include the word 'innovation' at least twice" — term inclusion with count
3. [LEX] "do not use the word 'revolution'" — term exclusion
4. [SEM] "about AI trends" — topic scope
5. [STY] "formal tone" — register
6. [STR] "3 paragraphs with headers" — structure + format

### Meta
- [IMP] Blog post implies intro-body-conclusion flow
- [CON] None detected
- [DEP] Topic (SEM) must be understood before register (STY) can be applied naturally
- [AMB] "headers" — H2? H3? Bold text? Markdown?
```

### Phase 2: Scoring

Calculate three scores for each prompt:

**1. Constraint Density Score (CDS)**

Count total explicit constraints. Rating:

| Count | Rating | Risk |
|-------|--------|------|
| 1-2 | `LOW` | Model handles easily |
| 3-4 | `MEDIUM` | Occasional misses possible |
| 5-7 | `HIGH` | Expect partial compliance |
| 8+ | `CRITICAL` | High failure probability, decompose |

**2. Cross-Type Mixing Index (CTMI)**

Count distinct constraint TYPES present (STR/LEX/SEM/STY). This is the key metric from the research — different types activate different network layers with minimal representational sharing.

| Types mixed | CTMI | Interpretation |
|-------------|------|----------------|
| 1 type | 0.0 | Single-skill, high compliance expected |
| 2 types | 0.3 | Moderate coordination needed |
| 3 types | 0.6 | Complex coordination, misses likely |
| 4 types | 1.0 | Maximum coordination load, high risk |

Adjust CTMI upward by +0.1 for each:
- Implicit constraint present
- Conflict detected
- Ambiguity detected

Cap at 1.0.

**3. Order Risk Score (ORS)**

Based on the monitoring-not-planning finding: constraints mentioned earlier are monitored longer during generation. Optimal order places hard-to-satisfy constraints early:

- Semantic/Stylistic constraints SHOULD appear BEFORE structural/lexical ones
- Why: semantic constraints need late-layer processing and longer monitoring. Structural constraints (word count, format) can be checked quickly at the end.

Score:
| Order | ORS | Meaning |
|-------|-----|---------|
| SEM/STY first, STR/LEX last | `OPTIMAL` | Matches network processing order |
| Mixed order | `SUBOPTIMAL` | Some reordering would help |
| STR/LEX first, SEM/STY last | `POOR` | Inverted from optimal; semantic constraints under-monitored |

**Summary format:**
```
### Scores
| Metric | Value | Rating |
|--------|-------|--------|
| Constraints | 6 | HIGH |
| CTMI | 0.8 (4 types + 1 ambiguity) | HIGH |
| Order | SEM/STY in middle, STR scattered | SUBOPTIMAL |
| Overall Risk | HIGH | Partial compliance expected |
```

### Phase 3: Audit

For each prompt, generate specific findings ranked by severity:

**Severity levels:**
- `CRITICAL` — Will likely cause failure. Must fix.
- `HIGH` — Significant risk. Should fix.
- `MEDIUM` — Moderate risk. Recommended fix.
- `LOW` — Minor improvement opportunity.
- `INFO` — Observation, no action needed.

**What to audit:**

1. **Constraint conflicts** (CRITICAL) — two constraints pulling opposite directions
2. **Extreme density** (CRITICAL) — 8+ constraints, model will drop some
3. **All 4 types mixed** (HIGH) — maximum coordination load
4. **Implicit constraints** (HIGH) — model may miss unstated expectations
5. **Ambiguous constraints** (MEDIUM) — "short", "a few", "some examples"
6. **Poor constraint order** (MEDIUM) — structural before semantic
7. **Redundant constraints** (LOW) — saying the same thing twice
8. **Missing success criteria** (LOW) — no way to verify compliance

**Model-specific audit notes:**

For **Claude**:
- Claude handles stylistic constraints well (strong register control)
- Claude tends to be verbose — explicit length limits help
- Claude respects exclusion constraints reliably
- Claude sometimes over-follows structural constraints at expense of semantic quality

For **GPT**:
- GPT handles semantic constraints well (strong topic adherence)
- GPT sometimes ignores lexical exclusion constraints
- GPT may not follow precise count requirements (e.g., "exactly 3 paragraphs")
- GPT benefits from constraint repetition at the end of the prompt

**Audit output format:**
```
### Audit Findings

1. **[HIGH]** CTMI 0.8 — all 4 constraint types present. Model must coordinate
   across all network layers simultaneously. Risk of dropping structural or
   lexical constraints.
   -> Recommendation: Split into 2 prompts or remove least critical constraint type.

2. **[MEDIUM]** Order risk — topic constraint (SEM) appears after format
   constraints (STR). Semantic processing in late layers gets less monitoring time.
   -> Recommendation: Move "about AI trends" to the beginning of the prompt.

3. **[MEDIUM]** Ambiguity in "headers" — unclear format specification.
   -> Recommendation: Specify "## Markdown H2 headers" or "bold text headers".

#### Claude-specific
- Length limit "200 words" is well-placed; Claude tends verbose without it
- Term exclusion "revolution" will be respected reliably

#### GPT-specific
- Consider repeating length limit at the end: "Remember: max 200 words"
- Term exclusion may be ignored; reinforce with "NEVER use the word 'revolution'"
```

### Phase 4: Rewrite

Generate an optimized version of EACH prompt. Create TWO variants:

**Variant A: Optimized for Claude**
**Variant B: Optimized for GPT**

**Rewrite rules (derived from research):**

1. **Reorder: semantic/stylistic first, structural/lexical last.**
   The model monitors constraints during generation. Place the hardest-to-satisfy (semantic, stylistic) early so they get the longest monitoring window. Place easily-verifiable constraints (word count, format) at the end.

2. **Make implicit constraints explicit.**
   If the context implies expectations (e.g., "LinkedIn post" implies certain norms), state them.

3. **Resolve conflicts.**
   If two constraints conflict, pick one or add a priority note: "Prioritize X over Y if they conflict."

4. **Reduce ambiguity.**
   Replace vague terms with specific ones: "short" -> "under 100 words", "a few" -> "3-5", "some" -> "2-3".

5. **Decompose if CTMI > 0.8 and CDS > 7.**
   Split into a chain of 2 prompts. First prompt handles semantic/stylistic constraints. Second prompt applies structural/lexical constraints to the output.

6. **Claude-specific adjustments:**
   - Be direct with constraints, no need to repeat
   - Use XML tags for structure when mixing many constraints: `<constraints>...</constraints>`
   - Explicit length limits (Claude is verbose by default)
   - Stylistic instructions work well at the system level

7. **GPT-specific adjustments:**
   - Repeat critical constraints at the end of the prompt
   - Use numbered lists for constraints (GPT follows numbered instructions well)
   - Bold or CAPS for must-not-violate constraints
   - Lexical exclusions need reinforcement: "NEVER use X. This is critical."

**Rewrite output format:**
```
### Rewrite: P1

**Original:**
> [full original prompt]

**Variant A (Claude):**
> [rewritten prompt optimized for Claude]

**Variant B (GPT):**
> [rewritten prompt optimized for GPT]

**Changes made:**
1. Moved topic constraint to beginning (order optimization)
2. Made "headers" explicit as "## Markdown H2" (ambiguity resolution)
3. Added implicit blog structure expectation (implicit -> explicit)
4. [Claude] Added XML constraint block
5. [GPT] Repeated length limit at end, bolded exclusion
```

### Phase 5: Summary Report

After processing all prompts, output a summary table:

```
## Summary

| # | Prompt (first 40 chars) | CDS | CTMI | ORS | Findings | Verdict |
|---|------------------------|-----|------|-----|----------|---------|
| P1 | Write a 200-word blog post about AI... | HIGH (6) | 0.8 | SUBOPTIMAL | 3 | REWRITE |
| P2 | Summarize this document in bullet... | LOW (2) | 0.3 | OPTIMAL | 0 | OK |
| P3 | Write a product description for... | MED (3) | 0.6 | POOR | 2 | REWRITE |

### Statistics
- Total prompts analyzed: 3
- Need rewrite: 2 (67%)
- Average CTMI: 0.57
- Most common issue: [top finding]

### Top Recommendations
1. [Most impactful recommendation across all prompts]
2. [Second most impactful]
3. [Third most impactful]
```

## Edge Cases

- **System prompts:** Treat as a single prompt. System prompts often have high CTMI by nature — flag but don't necessarily recommend decomposition.
- **Few-shot prompts:** Analyze the instruction part, not the examples. Note if examples contradict instructions.
- **Chain-of-thought prompts:** CoT instructions ("think step by step") are META constraints — note them but don't count toward CTMI.
- **Tool-use prompts:** Tool definitions are STRUCTURAL. Function calling instructions are STRUCTURAL. The task description follows normal analysis.
- **Empty or trivial prompts:** If a prompt has 0-1 constraints, mark as `OK — no optimization needed` and skip rewrite.

## What This Skill Does NOT Do

- Does NOT evaluate prompt quality for a specific domain (marketing, coding, etc.)
- Does NOT test prompts against actual models
- Does NOT guarantee compliance improvement — it predicts risk based on research
- Does NOT replace human judgment on prompt intent

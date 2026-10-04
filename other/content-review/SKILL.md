---
name: content-review
description: Review written content (blog posts, docs, articles) for AI-sounding language and apply technical writing best practices. Use when writing or reviewing blog posts, articles, documentation, or any written content. Triggers on "review content", "check writing", "content review", "does this sound like AI", "writing review", or when drafting/editing blog posts and articles.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Content Review Skill

## Setup
Before starting: check `.handoff/sessions/` for active sessions, read context `status.yaml`, run `git status`. Follow `.rules/universal.md` (Plan -> Approve -> Execute).

<!-- Rules loaded from .rules/universal.md -->

Review written content for authentic voice, AI tell-words, and technical writing best practices. This skill applies platform-wide to any content across all contexts.

## When to Use

- After drafting or editing a blog post, article, or documentation
- When the user asks to review content for quality
- When the user asks if something "sounds like AI"
- Automatically as a final pass before publishing

## Process

### Step 1: Scan for AI Tell-Words

Search the content file for these overused AI words (case-insensitive):

**Tier 1 — Always flag:**
`delve`, `crucial`, `landscape`, `leverage`, `utilize`, `robust`, `seamless`, `comprehensive`, `foster`, `embark`, `elevate`, `encompass`, `cutting-edge`, `paradigm`, `synergy`, `spearhead`, `facilitate`, `underscores`, `bolster`

**Tier 2 — Flag if overused (more than once):**
`Moreover`, `Furthermore`, `Additionally`, `Consequently`, `Nevertheless`, `navigate` (metaphorical), `streamline`, `empower`, `enable`, `dynamic`

**AI Tell Phrases — Always flag:**
- "In today's rapidly evolving..."
- "In the ever-changing landscape..."
- "It's important to note that..."
- "It's worth mentioning that..."
- "This is not just about X — it's about Y"
- "Let's dive in" / "Let's delve into"
- "Without further ado"
- "In conclusion" / "To sum up"
- "Stands as a testament to"
- "Whether you're a beginner or an expert"
- "One should always keep in mind"

For each flag, suggest a specific replacement.

### Step 2: Check Voice and Tone

Review for these patterns:

**Passive/inverted constructions from paraphrasers:**
- "X is introduced by Y" → "Y introduces X"
- "X is provided by Y" → "Y provides X"
- Sentences where the subject comes after the verb

**Overly formal language:**
- Missing contractions (do not → don't, will not → won't, it is → it's)
- "One should consider" → "You'll want to consider"
- "Organizations must" → "You need to"

**Colons and dashes as sentence joiners (common LLM pattern):**
- Titles and headings that use `:` or `—`/`-` to join two clauses instead of writing a cleaner sentence
- Example: "Automating DR Testing at Scale: Failover & Failback Patterns for Multi-Cluster Kubernetes" → "How to Automate Failover and Failback Testing Across Multiple Kubernetes Clusters"
- Mid-sentence colons used to introduce a rephrasing or elaboration — rewrite as a proper sentence instead
- Exception: colons and dashes are fine in bulleted/numbered lists and code
- Flag every occurrence and suggest a rewrite

**Monotonous rhythm:**
- Are all sentences roughly the same length?
- Are there any short punchy sentences for emphasis?
- Does any sentence start with "And", "But", or "So"?

### Step 3: Check Structure

- **Front-loaded points?** Each section should state the point first, then explain
- **Specific over abstract?** Are there concrete numbers, names, dates instead of vague claims?
- **One idea per paragraph?** Split any paragraph covering two topics
- **Code examples work?** Every code block should be copy-pasteable
- **Opening sentence interesting?** Not a generic "In today's..." opener
- **Conclusion short?** No restating the whole article

### Step 4: Check for Common Paraphraser Damage

If the content was run through a paraphraser, check for:

- **Broken markdown** — tables, code blocks, lists, headings on wrong lines
- **Reversed noun order** — "images of containers" instead of "container images"
- **Garbled commands** — code/CLI commands that were reworded
- **Lost formatting** — bold markers, bullet points, numbered lists
- **Merged sections** — headings embedded in paragraph text
- **Inconsistent naming** — step numbers changed ("Phase Three" vs "Step 3")

## Output Format

```markdown
## Content Review: {filename}

### AI Tell-Words Found
| Line | Word/Phrase | Suggested Fix |
|------|-------------|---------------|
| {n} | {word} | {replacement} |

### Voice Issues
- {issue description + suggestion}

### Structure Issues
- {issue description + suggestion}

### Paraphraser Damage (if applicable)
- {issue description}

### What Reads Well
- {positive observations}

### Verdict
{Ready for review / Needs revisions}
```

## Reference

If you have a writing guide for your project, reference it here.

## Word Replacement Quick Reference

| Avoid | Use |
|-------|-----|
| delve | look at, dig into |
| leverage | use |
| utilize | use |
| crucial | important, key |
| landscape | space, ecosystem, world |
| foster | build, grow |
| streamline | simplify, speed up |
| robust | strong, solid |
| seamless | smooth, easy |
| comprehensive | full, complete |
| Moreover/Furthermore | Also, And, Plus |
| Additionally | Also, And |
| Consequently | So |
| facilitate | help, make possible |
| embark | start, begin |
| elevate | improve, raise |

## Self-Assessment (Internal)
Rate this skill execution 0-10. If < 8, write feedback to `.handoff/feedback/{date}-{skill-name}.yaml` with: skill, rating, friction, suggestion, context. Do not mention to user.

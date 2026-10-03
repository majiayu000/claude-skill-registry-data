---
name: paper2skill-v0.0.3
description: "Convert arXiv papers into ready-to-use agent skills using category-aware extraction. First classifies the paper into one or more of 11 research categories, then applies a specialized extraction pipeline for each category — because different types of papers produce different types of usable knowledge. A single paper can yield multiple skills if it spans categories. Use this skill whenever the user wants to turn a paper into a skill, extract practical techniques from research, build a skill library from papers, convert arXiv papers into reusable agent instructions, or batch-process multiple papers into skills. Also trigger when someone asks about extracting actionable knowledge from papers, making research practical for LLM agents, or systematically converting academic contributions into structured agent capabilities."
---

# Paper2Skill v0.0.3: Category-Aware Extraction

This skill converts arXiv papers into agent skills by first classifying what *kind* of contribution a paper makes, then applying the right extraction pipeline for that contribution type. The key insight: a scaling-law paper and a dataset paper contain fundamentally different kinds of useful knowledge, so they should be extracted differently.

A single paper can produce **multiple skills** if it genuinely spans categories (e.g., a paper that introduces both a new method *and* a new benchmark).

## How It Works

```
Paper (arXiv link)
  → Step 1: Categorize (which of 11 types?)
  → Step 2: For each category, extract with the specialized pipeline
  → Step 3: Tag each skill (assign 1-3 broad-area tags from the registry)
  → Output: 1+ skills, each tailored to the knowledge type
```

## Step 1: Categorize the Paper

Read the paper's title and abstract, then follow the classification process in `references/paper-categorizer.md`.

The categorizer assigns:
- A **primary category** (the main contribution type)
- Optional **secondary categories** (0-2, only when the paper genuinely straddles types)
- An **extractability rating** (high/medium/low) for each

The 11 categories and their extraction targets:

| # | Category | What to Extract | Reference File |
|---|----------|----------------|----------------|
| 1 | Application Transfer | Domain adaptation recipe, deployment lessons | `references/paper2skill-application-transfer.md` |
| 2 | Evaluation Infrastructure | Dataset collection protocol OR benchmark design | `references/paper2skill-evaluation-infrastructure.md` |
| 3 | Paradigm Challenge | Prior belief → falsifying experiment → revised principle | `references/paper2skill-paradigm-challenge.md` |
| 4 | Systematic Empiricism | Ranked tricks, ablations, conditions of applicability | `references/paper2skill-systematic-empiricism.md` |
| 5 | Component Innovation | What was swapped, why, when it helps, performance delta | `references/paper2skill-component-innovation.md` |
| 6 | Insight-Driven | The "aha" observation + minimal reproduction recipe | `references/paper2skill-insight-driven.md` |
| 7 | Research Infrastructure | Design decisions, API patterns, trade-offs | `references/paper2skill-research-infrastructure.md` |
| 8 | Field Foundation | Problem definition, vocabulary, opened directions | `references/paper2skill-field-foundation.md` |
| 9 | Mechanistic Analysis | Analytical methodology (not just findings) | `references/paper2skill-mechanistic-analysis.md` |
| 10 | Survey & Synthesis | Taxonomy, decision trees, open problems | `references/paper2skill-survey-synthesis.md` |
| 11 | Scaling & Efficiency | Empirical laws, budget-performance trade-offs | `references/paper2skill-scaling-efficiency.md` |

## Step 2: Extract Skills Per Category

For **each** category assigned to the paper (primary + any secondaries), load the corresponding reference file and follow its extraction pipeline. Each reference contains:

- Category-specific paper reading strategy (what to focus on)
- A tailored extraction template (what information to pull)
- Output skill structure (how to organize the result)
- Quality checklist (what makes a good extraction for this type)

**Only load the reference files you need.** If a paper is classified as Category 5 (Component Innovation) with no secondaries, only read `references/paper2skill-component-innovation.md`. Don't load the other 10.

### Handling Multiple Categories

When a paper has secondary categories:

1. Extract the **primary** skill first — this is the main output.
2. For each secondary, assess whether a separate skill adds genuine value. A secondary category with `low` confidence often doesn't warrant its own skill — the primary skill can mention it briefly instead.
3. Each extracted skill gets its own folder and SKILL.md. Name them to distinguish: e.g., `flash-attention-efficiency` (primary: Scaling & Efficiency) and `flash-attention-architecture` (secondary: Component Innovation).

### When NOT to Extract

Skip extraction for a category if:
- The secondary confidence is `low` and the primary skill already covers the insight
- The paper only superficially touches the secondary category
- Extracting would produce a near-duplicate of the primary skill

## Step 3: Tag Each Skill

After extraction, assign **1-3 broad-area tags** to each skill from the tag registry at `tags.json` in the project root. Tags categorize skills by research area for browsing and filtering.

### Tag Registry

The registry contains ~20 broad research-area tags such as: Reinforcement Learning, Large Language Models, Computer Vision, Natural Language Processing, Multimodal Learning, Generative Models, Agents, Robotics, Optimization, Inference Efficiency, Representation Learning, Graph Learning, AI Safety, Evaluation, ML Systems, Speech, Information Retrieval, Time Series, Recommender Systems, Science.

### Tagging Rules

1. **Select 1-3 tags** from the registry. Every skill must get at least one tag.
2. **Always use existing tags.** The registry already covers most ML/AI research areas.
3. If a skill spans multiple areas, select 2-3 existing tags rather than inventing a new narrow one.
4. **Match to the broadest applicable tag.** Examples:
   - A paper about PPO clipping → `Reinforcement Learning` (not "Policy Optimization")
   - A paper about LoRA → `Large Language Models` (not "Parameter Efficient Fine-tuning")
   - A paper about calibration → `AI Safety` or the most relevant area (not "Calibration")
   - A paper about video generation → `Generative Models`, `Computer Vision`
5. **New tags are rare.** Only propose a new tag if no existing one fits at all AND the new tag represents a broad research area that could apply to 50+ papers (e.g., "Audio Processing"). Never create tags for techniques, specific problems, or niche subtopics. Ask yourself: "Would a major ML conference have a track for this?" If not, pick the closest existing tag.
6. Format as an inline YAML list: `tags: [Computer Vision, Generative Models]`. Place the `tags` field immediately after `keywords` in the frontmatter.

## Output Skill Specification

All generated skills follow this frontmatter format:

```yaml
---
name: meaningful-kebab-case-name
title: "Actual Paper Title Here"
version: 0.0.3
engine: skillxiv-v0.0.3-claude-opus-4.6
license: MIT
url: "https://arxiv.org/abs/XXXX.XXXXX"
keywords: [Keyword One, Keyword Two, Keyword Three]
tags: [Broad Area Tag One, Broad Area Tag Two]
description: "Outcome-focused description under 1024 chars, plain text only, no angle brackets"
category: "Category Name"
---
```

### Naming Rules

The `name` field (also the folder name) must be descriptive kebab-case that communicates the skill's purpose. Strictly prohibited: raw arXiv IDs (`2505-00212`), generic names (`paper-skill`), acronyms without context.

### Description Rules

Structure: `[What it does — outcome] + [When to use — triggers]`. Under 1024 characters, plain text only (no `<` `>` tags), double-quoted string on one line. Focus on outcomes, not features.

### URL Verification

The `url` must be a verified, working arXiv link. Construct as `https://arxiv.org/abs/XXXX.XXXXX` and verify it resolves. Never use placeholders.

### Keywords

5-10 keywords in Title Case, inline YAML list: `keywords: [Model Architecture, Mamba, State Space Models]`. Never use YAML block list syntax.

### Tags

1-3 broad research-area tags from the tag registry (`tags.json`), inline YAML list: `tags: [Large Language Models, Inference Efficiency]`. See **Step 3** above for selection rules. The `tags` line goes immediately after `keywords` in the frontmatter.

### Code Handling

- Every code block needs 1-2 sentences of explanation before it
- Always label the coding language in fences (`python`, not bare)
- Inline code: 10-40 lines max, show NOVEL parts only
- Long code (>50 lines) goes in `scripts/`, referenced from SKILL.md

## Accessing Papers

Always read the original arXiv paper. Never generate skills from summaries, blog posts, or secondary sources.

Preferred access order:
1. **arXiv HTML** (`https://arxiv.org/html/XXXX.XXXXX`) — best source, try first
2. **arXiv abstract** (`https://arxiv.org/abs/XXXX.XXXXX`) — metadata + abstract
3. **arXiv PDF** (`https://arxiv.org/pdf/XXXX.XXXXX`) — fallback if no HTML
4. **GitHub repo** — supplementary context if linked

## Batch Processing

When converting multiple papers:

1. **Triage** — read titles/abstracts, categorize all papers using the categorizer
2. **Group by category** — papers in the same category share extraction patterns
3. **Extract in category batches** — load each reference file once, process all papers of that type
4. **Cross-skill review** — check for redundancy, ensure trigger descriptions don't overlap

## Quality Validation

Run these checks on every generated skill:

1. **Standalone test** — can you understand what to implement from the skill alone?
2. **Code review** — would the code blocks run? All language-labeled?
3. **Trigger test** — does the description trigger for 5+ phrasings of the use case?
4. **Depth check** — does it go beyond a 2-sentence summary?
5. **Category alignment** — does the extracted skill actually reflect the category's knowledge type? (A Category 4 paper should produce a checklist, not an architecture guide)
6. **Tag check** — are the tags broad research areas from the registry? No technique names, no niche subtopics.

## Reference Files

All reference files are in the `references/` directory. Load only what you need:

- `references/paper-categorizer.md` — Full categorization logic with 11 category definitions, signals, and classification process
- `references/paper2skill-application-transfer.md` — Category 1 extraction pipeline
- `references/paper2skill-evaluation-infrastructure.md` — Category 2 extraction pipeline
- `references/paper2skill-paradigm-challenge.md` — Category 3 extraction pipeline
- `references/paper2skill-systematic-empiricism.md` — Category 4 extraction pipeline
- `references/paper2skill-component-innovation.md` — Category 5 extraction pipeline
- `references/paper2skill-insight-driven.md` — Category 6 extraction pipeline
- `references/paper2skill-research-infrastructure.md` — Category 7 extraction pipeline
- `references/paper2skill-field-foundation.md` — Category 8 extraction pipeline
- `references/paper2skill-mechanistic-analysis.md` — Category 9 extraction pipeline
- `references/paper2skill-survey-synthesis.md` — Category 10 extraction pipeline
- `references/paper2skill-scaling-efficiency.md` — Category 11 extraction pipeline

---
name: synthesis
description: Synthesize all accumulated notes and drafts to generate the Discussion and Abstract sections. Sixth step of biomedical-science-writer workflow. Requires all notes/*.md files and drafts/introduction.md, methods.md, results.md.
---

# Synthesis

Integrates all accumulated notes and prior drafts to generate the Discussion and Abstract sections, connecting findings to the broader literature.

## Prerequisites

Required files:
- `scope.md` - Research question and key findings
- `notes/papers/*.md` - Literature notes
- `notes/search/*.md` - Web search notes
- `notes/references/*.md` - Reference-chained paper notes
- `notes/literature-synthesis.md` - Aggregated themes and findings (key input!)
- `notes/code-analysis.md` - Methods context
- `notes/data-analysis.md` - Results context
- `drafts/introduction.md` - For narrative continuity
- `drafts/methods.md` - For methodological context
- `drafts/results.md` - Findings to discuss

## Workflow

```
[Load all notes and drafts]
     │
     ▼
[Map findings to literature] ─── What supports/contradicts
     │
     ▼
[Draft Discussion] ─── Interpret, compare, contextualize
     │
     ▼
[Draft Abstract] ─── Structured summary
     │
     ▼
[Output] ─── drafts/discussion.md, drafts/abstract.md
```

## Step 1: Load and Organize Materials

### Read Literature Synthesis (Primary Reference)

Start with `notes/literature-synthesis.md` - this document already contains:
- Source inventory with relationships to our work
- Key themes identified across all papers
- Findings that support our hypothesis
- Contradictory findings to address
- Methodological patterns
- Gaps our study addresses
- Citation map showing foundational papers
- Implications for Discussion section

This synthesis is the primary guide for drafting the Discussion.

### Read All Notes

```bash
ls notes/papers/*.md notes/search/*.md notes/references/*.md notes/*.md
```

Use individual paper notes for specific quotes and statistics.

### Mapping from Literature Synthesis

The synthesis document provides:
- Which sources support our findings
- Which sources provide contrasting results
- Which sources explain mechanisms
- Which sources address limitations

### Extract Key Results

From `drafts/results.md` and `notes/data-analysis.md`:
- Primary finding (statistic and interpretation)
- Secondary findings
- Unexpected results
- Null findings (if any)

### Review Scope

From `scope.md`:
- Research question being answered
- Hypothesis (was it supported?)
- Limitations to address

## Step 2: Map Findings to Literature

Use `notes/literature-synthesis.md` as the starting point - it already contains:
- "Findings That Support Our Hypothesis" table
- "Contradictory or Conflicting Findings" table
- "Implications for Discussion" section

Extend this mapping with our actual results from `drafts/results.md`:

| Our Finding | Supporting Literature | Contrasting Literature | Notes |
|-------------|----------------------|------------------------|-------|
| [Primary result] | [from synthesis] | [from synthesis] | [why contrast] |
| [Secondary result] | [from synthesis] | None | |

For each finding, the synthesis document identifies:
1. **Agreement**: Papers with similar findings
2. **Disagreement**: Papers with different findings (explain why)
3. **Mechanism**: Papers that explain why this occurs
4. **Clinical relevance**: Papers that contextualize importance

## Step 3: Draft Discussion

Create `drafts/discussion.md` following this structure:

### Discussion Structure (6-7 paragraphs)

```markdown
# Discussion

## Principal Findings (Paragraph 1)

[Open with main finding - interpret, don't just restate]

This study demonstrates that [interpretation of primary finding]. 
[Connect to research question from scope.md].
[One sentence on significance].

## Comparison with Literature (Paragraphs 2-3)

[Compare findings to existing work]

Our findings are consistent with [Author et al.], who reported [finding] [citation]. 
Similarly, [Author2 et al.] demonstrated [related finding] [citation].

[Address any discrepancies]

In contrast to [Author3 et al.], who found [different result] [citation], our study suggests [explanation]. 
This difference may be attributed to [methodological differences, population differences, etc.].

## Mechanistic Interpretation (Paragraph 4)

[Explain WHY these results might occur]

These findings may reflect [biological/clinical mechanism]. 
[Author et al.] previously showed that [mechanistic evidence] [citation], 
which supports the hypothesis that [explanation].

[If speculative, use appropriate hedging: "may", "might", "could potentially"]

## Clinical/Practical Implications (Paragraph 5)

[What does this mean for practice?]

These results have several implications for [clinical practice / research / etc.].
First, [implication 1].
Second, [implication 2].
[If applicable: These findings suggest that clinicians should consider...]

## Limitations (Paragraph 6)

[Honest but constructive discussion of limitations]

This study has several limitations that should be considered.
First, [limitation 1 with mitigation if possible].
Second, [limitation 2].
[Frame constructively: "While [limitation], [mitigating factor]..."]

Common limitations to address:
- Sample size
- Single-center
- Retrospective design
- Selection bias
- Technical limitations
- Generalizability

## Future Directions (Paragraph 7)

[What should come next?]

Future studies should [specific actionable suggestion].
Prospective validation in [population] is warranted.
Additionally, [another future direction].

---

## Discussion References

[List all citations used in Discussion with note references]
```

### Writing Guidelines

- **Present tense**: General truths ("MRI enables...")
- **Past tense**: Specific studies ("Smith et al. found...")
- **Hedging**: Match to evidence strength
- **No new data**: All statistics should be in Results

### Literature Integration Phrases

**Agreement:**
- "Consistent with prior work [X], we found..."
- "Our findings support those of [X], who demonstrated..."
- "In line with [X], our results indicate..."

**Disagreement:**
- "In contrast to [X], our study suggests..."
- "Unlike [X], who reported..., we found..."
- "Our results differ from [X], possibly due to..."

**Extension:**
- "Our findings extend those of [X] by demonstrating..."
- "Building on work by [X], we show..."
- "While [X] established..., our study further demonstrates..."

## Step 4: Draft Abstract

Create `drafts/abstract.md`:

```markdown
# Abstract

## Background/Purpose
[2-3 sentences: Gap in knowledge + study objective]

[Clinical/scientific problem]. [What is unknown]. The purpose of this study was to [objective].

## Methods
[3-4 sentences: Design, population, key methods, statistics]

This [study design] included [n] patients from [setting]. [Key methods]. [Primary outcome measure]. [Statistical approach].

## Results  
[3-4 sentences: Key findings with numbers]

[Primary finding with statistics]. [Secondary finding]. [Additional notable result].

## Conclusion
[1-2 sentences: Main takeaway + implication]

[Main conclusion]. [Clinical/research implication].

---

**Word Count**: [count]
**Keywords**: [keyword1], [keyword2], [keyword3], [keyword4], [keyword5]
```

### Abstract Guidelines

- **Standalone**: Understandable without reading paper
- **Specific**: Include key numbers (n, primary statistic, p-value)
- **Consistent**: Match paper content exactly
- **Past tense**: Throughout (this study was conducted)
- **No citations**: Never cite in abstract
- **No abbreviations**: Or define on first use

### Word Count Targets

| Section | Target |
|---------|--------|
| Background | 50-75 words |
| Methods | 75-100 words |
| Results | 75-100 words |
| Conclusion | 25-50 words |
| **Total** | ~250-300 words |

Adjust based on `scope.md` target journal requirements.

## Step 5: Generate Title Options

Based on synthesis, suggest 2-3 title options:

```markdown
## Suggested Titles

1. [Descriptive]: "[Method/Approach] for [Application]: [Key Finding]"
   
2. [Question-answer]: "[Research Question]? A [Study Type]"
   
3. [Finding-focused]: "[Key Finding] in [Population] Using [Method]"
```

Title guidelines:
- 10-15 words maximum
- No abbreviations (usually)
- Informative > clever
- Include key method and finding if possible

## Output

Save to:
- `drafts/discussion.md` - Discussion section
- `drafts/abstract.md` - Structured abstract with title options

Return to parent skill with summary:
- Discussion word count: [n]
- Abstract word count: [n]
- Literature sources cited in Discussion: [n]
- Title options: [n]

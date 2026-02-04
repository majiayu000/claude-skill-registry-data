---
name: technical-writing
description: Write clear technical prose. Multi-layer review ensures structure, clarity, and evidence quality.
---

# Technical Writing

Write clear technical prose with rigorous quality review.

## When to Use

- Writing technical documentation, design docs, or READMEs
- Drafting blog posts or technical reports
- Writing research papers or whitepapers
- Any technical writing that needs to transfer ideas clearly
- Existing draft needs systematic improvement

**Don't use for**: Quick notes, informal messages, or throwaway text.

## Core Principles

Every sentence serves one goal: **transfer ideas from author to reader**.

1. **Give away the punchline** - State your point upfront, don't bury it
2. **Topic sentences** - First sentence of each paragraph enables scanning
3. **Active voice** - "The system handles X" not "X is handled by the system"
4. **Consistent terminology** - Same concept uses same term throughout
5. **Concrete before abstract** - Examples before generalizations
6. **Figure-first explanations** - Lead with diagrams, standalone captions

## Quality Rubric

Review occurs in three sequential layers. Each layer has specific focus.

### Layer 1: Structure

| Criterion | Requirement |
|-----------|-------------|
| **Main point upfront** | Reader knows the point within first paragraph |
| **Logical flow** | Each section follows naturally from the previous |
| **Section balance** | No section dominates inappropriately |
| **Scannable** | Headers and topic sentences tell the story |
| **Completeness** | No obvious gaps in the argument or explanation |

### Layer 2: Clarity

| Criterion | Requirement |
|-----------|-------------|
| **Active voice** | No passive constructions obscuring agency |
| **Topic sentences** | First sentence of each paragraph states main point |
| **Consistent terminology** | Same concept uses same term throughout |
| **No weasel words** | Avoid "clearly," "obviously," "simply," "just" |
| **Paragraph coherence** | 3-5 sentences, single idea, transition words |
| **Concrete examples** | Abstract claims grounded in specifics |

### Layer 3: Evidence

| Criterion | Requirement |
|-----------|-------------|
| **Claims supported** | Every claim has evidence or reasoning |
| **Examples work** | Code samples run, commands execute |
| **Figures standalone** | Captions explain without requiring text |
| **Links valid** | External references resolve |
| **Accuracy** | Technical details correct and verifiable |

## Document Types

The same principles apply across formats, with emphasis shifts:

| Type | Emphasis | Structure |
|------|----------|-----------|
| **Documentation/README** | Scannable, working examples | What → Why → How → Reference |
| **Blog/Article** | Hook, narrative, examples | Hook → Problem → Solution → Implications |
| **Design Doc** | Context, alternatives, tradeoffs | Context → Goals → Design → Alternatives → Plan |
| **Research Paper** | Contribution clarity, evidence rigor | Problem → Contribution → Approach → Evaluation |
| **Technical Report** | Completeness, actionable conclusions | Summary → Findings → Analysis → Recommendations |

## Inputs

Before drafting:
- Topic and scope
- Target audience (who is reading this?)
- Key points to convey
- Supporting material (code, diagrams, data)

## Output Schema

```json
{
  "topic": "string",
  "audience": "string",
  "status": "DRAFT | REVIEWED | COMPLETE",
  "sections": [
    {
      "heading": "string",
      "content": "string"
    }
  ],
  "review_history": {
    "structure": "PASS | REVISE",
    "clarity": "PASS | REVISE",
    "evidence": "PASS | REVISE"
  }
}
```

## Recording Reviews

Post review progress to jwz:

```bash
jwz post "writing:<topic>" --role alice \
  -m "[alice] REVIEW: <topic>
Layer: STRUCTURE | CLARITY | EVIDENCE
Verdict: PASS | REVISE
Notes: <specific feedback>"
```

## Reference

This skill distills principles from authoritative sources:

**Foundational**
- Strunk & White, *The Elements of Style*
- Steven Pinker, *The Sense of Style*
- Joseph Williams, *Style: Toward Clarity and Grace*

**Technical Writing**
- [Simon Peyton Jones - How to Write a Great Research Paper](https://simon.peytonjones.org/great-research-paper/)
- [Kayvon Fatahalian - Systems Paper Guide](https://graphics.stanford.edu/~kayvonf/notes/systemspaper/)
- [Derek Dreyer - How to Write Papers So People Can Read Them](https://people.mpi-sws.org/~dreyer/talks/talk-plmw16.pdf)
- [Michael Ernst - Writing Technical Papers](https://homes.cs.washington.edu/~mernst/advice/write-technical-paper.html)

**Clear Exposition**
- [Distill.pub](https://distill.pub/) - Exemplar of visual, interactive explanation

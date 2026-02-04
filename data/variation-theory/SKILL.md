---
name: variation-theory
description: Apply variation theory of learning to structure instructional content using contrast, generalization, and fusion patterns. Variation must target the critical aspects of the learning objective. Use when writing educational materials, explanations, tutorials, literate programming documentation (.nw files), structuring lecture slides, designing exercises, or when user mentions variation theory, learning theory, pedagogy, or critical aspects of learning. Works alongside the literate-programming skill for .nw files.
---

# Variation Theory of Learning

This skill applies the variation theory of learning, developed by Ference Marton and colleagues, to structure content for optimal learning.

## Reference Files

This skill includes detailed references in `references/`:

| File | Content | Search patterns |
|------|---------|-----------------|
| `common-violations.md` | Generalization-before-example violations | `BAD`, `GOOD`, violation types |
| `latex-examples.md` | Side-by-side contrast, semantic environments | `\textbytext`, `\ltnote`, Swedish |

## Core Theoretical Principles

### The Object of Learning

The **object of learning** is what is to be learned. Understanding develops when learners discern the **critical aspects** of the object of learning.

Marton's central principle: "to learn something, the learner must discern what is to be learned. Discerning the object of learning amounts to discerning its critical aspects."

### Variation and Invariance

The necessary condition for discernment: learners must experience **variation in a dimension corresponding to that aspect**, against the background of **invariance** in other aspects.

**Key insight**: "When some aspect of a phenomenon varies while another aspect remains invariant, the varying aspect will be discerned."

## Critical Aspects as Focus of Variation

**FUNDAMENTAL PRINCIPLE**: Variation must occur in the **critical aspects** of the object of learning. Arbitrary variation does not lead to learning.

### Identifying Critical Aspects First

Before designing any pattern of variation:

1. **Define the object of learning** - What should learners understand/do?
2. **Identify the critical aspects** - Which features must be discerned?
3. **Design variation IN those aspects** - Create patterns varying the critical dimensions

### Dimensions vs Values

The principle "one thing at a time" applies to **dimensions** (aspects), NOT to **values** within a dimension.

- **Dimension (aspect)**: A category/feature type (e.g., "punctuation marks", "file mode")
- **Values/features**: Specific instances (e.g., `.`/`?`/`!` or `r`/`w`/`a`)

**The principle:**
- **Vary ONE dimension at a time** - to separate aspects from each other
- **Contrast MULTIPLE values together** - within that dimension

**Research evidence**: Teaching punctuation marks separately: 15% improvement. Teaching all three together with contrast: 63% improvement.

### Common Mistake: Varying Non-Critical Aspects

**Anti-pattern**: Creating variation in aspects irrelevant to the learning objective.

**Example**: Teaching "why files need open/close":
- **Wrong**: Vary filename or content (not critical)
- **Right**: Vary what happens when close() is/isn't called (critical aspect is resource management)

## The Three Patterns of Variation

### 1. Contrast

**Purpose**: Help learners recognize that an aspect exists by experiencing what it is versus what it is not.

**How it works**: Present examples that differ in one critical aspect while keeping all other factors constant.

**Example**: To understand "height," show two objects identical in all respects except height.

**Note**: Contrast achieves *separation*—the critical aspect becomes discernible through experiencing variation.

### 2. Generalization

**Purpose**: Help learners recognize that a pattern or principle holds across different contexts.

**How it works**: Present the same critical value in varied appearances. Keep the critical aspect invariant while varying other (non-critical) aspects.

**Example**: Show the same geometric principle applied to triangles, rectangles, circles.

### 3. Fusion

**Purpose**: Enable learners to experience multiple critical aspects simultaneously as an integrated whole.

**How it works**: Vary several critical aspects at once so learners must attend to their simultaneous interrelationships.

**Example**: In understanding circuits, vary resistance and voltage simultaneously.

## Pedagogical Sequence

Research suggests using patterns in this order:

1. **Contrast** - Vary the critical aspect while keeping other aspects invariant. This *separates* (makes discernible) the critical aspect.
2. **Generalization** - Keep the critical value invariant while varying other aspects. Shows the pattern holds across contexts.
3. **Fusion** - Vary multiple critical aspects simultaneously. Enables learners to experience interrelationships.

**Important**: Within each pattern, contrast multiple **values** together. "One at a time" applies to **dimensions/aspects**, not values.

## Temporal Sequencing: Examples Before Generalizations

**CRITICAL**: Examples must precede generalizations. Students need concrete instances creating necessary variation before abstract principles become meaningful.

**Why**: Variation must be **experienced** before invariants can be discerned. When you state a general principle first, students have no variation pattern to map it onto.

**Anti-pattern:**
```latex
% BAD: Generalization before examples
Filer behövs för persistens, datautbyte, och skalbarhet.

\begin{example}[Spara spelets progress]
  ...
\end{example}
```

**Good pattern:**
```latex
% GOOD: Examples create variation, then generalize
\begin{example}[Spara spelets progress]
  Ett spel behöver komma ihåg spelarens poäng...
\end{example}

\begin{example}[Dela data mellan program]
  Ett program genererar data som ett annat använder...
\end{example}

\begin{remark}[Varför filer behövs]
  Filer behövs för persistens, datautbyte, och skalbarhet.
\end{remark}
```

See `references/common-violations.md` for detailed violation types and fixes.

## Common Generalization Violations

See `references/common-violations.md` for detailed examples.

**Violation types:**
1. **Generic/placeholder code before concrete examples**
2. **Block/remark environments before examples**
3. **Incomplete skeletons before complete solutions**
4. **Explanatory principles before demonstrating examples**

**Fix pattern** for each violation:
1. Remove the generalization from its current position
2. Ensure 2-3 concrete examples exist creating necessary variation
3. Add back the generalization AFTER examples
4. Verify students can now discern the pattern from the variation

## Side-by-Side Contrast

See `references/latex-examples.md` for details.

For Beamer presentations, use mode splits:

```latex
\begin{frame}
  \mode<presentation>{%
    \textbytext{%
      \begin{definition}[Primärminne]
        Flyktigt minne med snabb åtkomst.
      \end{definition}
    }{%
      \begin{definition}[Sekundärminne]
        Oflyktigt minne, långsammare.
      \end{definition}
    }
  }
  \mode<article>{%
    \textbytext*{%
      ...
    }{%
      ...
    }
  }
\end{frame}
```

## Generalizations in Semantic Environments

Capture generalizations in semantic environments AFTER examples:

| Environment | Use for |
|-------------|---------|
| `definition` | Formal concept definitions |
| `remark` | Important observations, principles |
| `block` | Key takeaways, summaries |
| `example` | When generalization is best shown through code |

## Language Consistency

**CRITICAL**: When documenting variation theory in notes (e.g., `\ltnote`), match the document's instructional language.

**Swedish terminology:**
- "Variation Pattern" → "Variationsmönster"
- "Contrast" → "Kontrast"
- "What varies" → "Vad som varierar"
- "What remains invariant" → "Vad som hålls invariant"
- "Critical aspects" → "Kritiska aspekter"

## When Applying This Skill

1. Identify the **object of learning** (what should be understood)
2. Determine the **critical aspects** (what must be discerned)
3. Structure content using the **three patterns** to create necessary conditions
4. Remember: "there is no discernment without variation"

## Connection to Try-First-Tell-Later

The try-first-tell-later skill complements variation theory: use try-first prompts to **diagnose which critical aspects students can already discern**, then design variation patterns to teach aspects they cannot yet see.

## Key References

- Marton, F. (2015). *Necessary Conditions of Learning*. Routledge. (Primary reference)
- Marton, F., & Booth, S. (1997). *Learning and Awareness*. Lawrence Erlbaum.
- Marton, F., & Pang, M. F. (2006). On Some Necessary Conditions of Learning. *Journal of the Learning Sciences*, 15(2), 193-220.
- Marton, F., & Tsui, A. (2004). *Classroom discourse and the space of learning*. Lawrence Erlbaum.

---
name: didactic-notes
description: |
  Document pedagogical design decisions in educational materials using the
  didactic LaTeX package and \ltnote command. Use proactively when (1) writing
  or editing educational LaTeX materials with pedagogical content, (2) adding
  variation theory labels or patterns to student-facing content, (3) explaining
  design trade-offs or choices in educational materials, (4) documenting why
  specific examples or exercises are sequenced in a particular way. Invoke when
  user mentions didactic notes, \ltnote, pedagogical reasoning, learning theory
  notes, educational design documentation, variation theory labels in student
  content, or asks to move pedagogical reasoning to instructor notes. CRITICAL:
  Pedagogical reasoning (variation/invariance labels, pattern names, design
  rationale) should be in \ltnote{}, NOT in student-facing text.
---

# Didactic Notes: Literate Pedagogy

This skill documents pedagogical design decisions in educational materials, analogous to how literate programming documents code design decisions.

## Reference Files

This skill includes detailed references in `references/`:

| File | Content | Search patterns |
|------|---------|-----------------|
| `latex-examples.md` | Restatable LOs, citations, complete examples | `restatable`, `\cref{}`, `biblatex` |
| `beamer-patterns.md` | Mode splits, overlays, verbose environments | `\mode<article>`, `uncoverenv`, `\textbytext` |
| `semantic-environments.md` | Environment selection, generalizations | `definition`, `remark`, `example`, `block` |

## Core Principle

**Document not just what you teach, but *why* you teach it that way.**

Just as literate programming makes code reasoning explicit, didactic notes make pedagogical reasoning explicit using `\ltnote{...}` from the LaTeX `didactic` package.

## Quick Example

**Without didactic notes:**
```latex
\begin{activity}\label{PredictOutput}
  What do you think this function returns?
\end{activity}
```

**With didactic notes:**
```latex
\begin{activity}\label{PredictOutput}
  What do you think this function returns?
\end{activity}

\ltnote{%
  Following try-first pedagogy, we ask students to predict before
  explaining. This creates contrast between their mental model and
  the actual behavior, helping them discern the critical aspect.
}
```

## The `didactic` Package

### Package Setup

```latex
\usepackage[marginparmargin=outer]{didactic}
```

Options:
- `marginparmargin=outer` - Place margin notes on outer margins
- `inner=20mm`, `outer=60mm` - Set margin widths
- `notheorems` - Disable automatic theorem environments

### The `\ltnote` Command

Creates margin notes documenting pedagogical rationale:

```latex
\ltnote{%
  We want to investigate what people think literate programming is.
  This will help us understand the correctness of their prior knowledge.
}
```

## Learning Objectives with Restatable

Use `restatable` environment for learning objectives that can be referenced throughout:

```latex
\begin{restatable}{lo}{FilesLOPersistence}\label{FilesLOPersistence}%
  Förklara skillnaden mellan primärminne och sekundärminne.
\end{restatable}
```

**Key points:**
- Use **mnemonic labels** (e.g., `FilesLOPersistence`, not `FilesLO1`)
- Add `\label{MnemonicLabel}` for `\cref{}` support
- The `%` after opening brace prevents unwanted whitespace

### Referencing LOs

**Method 1: `\cref{}`** (Recommended for detailed notes):
```latex
\ltnote{%
  Relevanta lärandemål:
  \cref{FilesLOPersistence}

  \textbf{Kritiska aspekter för} \cref{FilesLOPersistence}:
  \begin{itemize}
    \item \textbf{Persistens}: Data överlever avstängning
  \end{itemize}
}
```

**Method 2: Starred commands** (Compact):
```latex
\ltnote{%
  Relevanta lärandemål:
  \FilesLOPersistence*

  \textbf{Kontrast}: Typ av minne (primär vs sekundär).
}
```

**CRITICAL**: LO commands cannot be inside `\begin{itemize}` or other list environments.

## When to Use `\ltnote`

Document:

1. **Learning objectives addressed**: Reference with `\cref{}` or starred commands
2. **Pedagogical strategies**: "We use try-first pedagogy to activate prior knowledge"
3. **Variation theory patterns**: Contrast, generalization, fusion
4. **Critical aspects students should discern**
5. **Design trade-offs and decisions**
6. **Assessment purposes**: "This question gauges prior knowledge"
7. **Future improvements**: Notes for refining material

## Writing Effective Notes

### CRITICAL: Connect to Learning Objectives

Variation patterns must be tied to specific learning objectives:

```latex
\ltnote{%
  Relevanta lärandemål:
  \cref{FilesLOPersistence}

  \textbf{Variationsmönster}: Kontrast

  \textbf{Vad som varierar}: Typ av minne (primär vs sekundär)
  \textbf{Vad som hålls invariant}: Behovet att lagra data

  \textbf{Kritiska aspekter för} \cref{FilesLOPersistence}:
  \begin{itemize}
    \item \textbf{Persistens}: Studenten måste urskilja att filer
      löser problemet med datapersistens.
  \end{itemize}
}
```

### Structure Your Notes

1. **State learning objectives**: What should students learn?
2. **Reference theory**: Connect to established learning principles
3. **Explain the mechanism**: How does this design support objectives?
4. **Note alternatives**: What else could work?

### Language Consistency

**CRITICAL**: Match the language of `\ltnote` content to the surrounding document.

```latex
% Good - Swedish document with Swedish notes
\ltnote{%
  \textbf{Variationsmönster}: Kontrast
  Vi varierar operationen medan vi håller mönstret invariant.
}

% Use \foreignlanguage for English terms without translation
\ltnote{%
  Vi använder \foreignlanguage{english}{try-first pedagogy} här...
}
```

### Choosing Between Detailed and Compact Notes

**Use detailed notes with `\cref{}`** when:
- Writing comprehensive annotations
- Explaining multiple critical aspects
- Need prose-style integration

**Use compact notes with starred commands** when:
- Space is limited
- Quick overview needed
- Simple annotations suffice

## Citing Pedagogical Research

Use biblatex commands instead of hardcoded references:

```latex
\ltnote{%
  Following \textcite{MartonPang2006}, we vary the operation...
}
```

Common commands:
- `\textcite{key}` → "Marton and Pang (2006)"
- `\parencite{key}` → "(Marton and Pang 2006)"

**Best practice**: Use separate `ltnotes.bib` for pedagogical references.

## Integration with Learning Theories

### Variation Theory

Document how material creates patterns of variation:

```latex
\ltnote{%
  \textbf{Mönster}: Generalisering
  \textbf{Varierar}: Programmeringsspråk (Python vs Java)
  \textbf{Invariant}: Algoritmisk princip
}
```

### Try-First Pedagogy

Explain when and why you ask students to attempt before explaining:

```latex
\ltnote{%
  Following try-first pedagogy, we ask students to predict the output
  before running the code. This creates a knowledge gap that makes the
  subsequent explanation more meaningful.
}
```

### Cognitive Load Theory

Note considerations about cognitive load:

```latex
\ltnote{%
  We introduce only two parameters here to manage cognitive load.
  Additional parameters will be introduced after students master the
  basic pattern.
}
```

## Semantic Environments

See `references/semantic-environments.md` for details.

Key environments: `activity`, `exercise`, `question`, `remark`, `definition`, `example`, `block`

### Generalizations After Examples

Capture generalizations in semantic environments AFTER examples:

```latex
\begin{example}[Läsa fil]
  with open("data.txt", "r") as fil:
      innehåll = fil.read()
\end{example}

\begin{example}[Skriva fil]
  with open("data.txt", "w") as fil:
      fil.write(text)
\end{example}

\begin{remark}[Filhanteringsmönster]
  All filhantering följer: öppna → bearbeta → stäng.
\end{remark}
```

## Beamer Patterns

See `references/beamer-patterns.md` for details.

### Key Points

- Notes are hidden by default in slide builds
- Write expanded prose outside `frame` environments
- Use `\only<article>` / `\only<presentation>` for mixed content
- `\textbytext*` does NOT work inside frames—use mode splits

### Side-by-Side Contrast (Beamer-compatible)

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
      \begin{definition}[Primärminne]
        Flyktigt minne med snabb åtkomst.
      \end{definition}
    }{%
      \begin{definition}[Sekundärminne]
        Oflyktigt minne, långsammare.
      \end{definition}
    }
  }
\end{frame}
```

### Verbose Environments

Split verbose content between presentation and article modes:

```latex
\mode<presentation>{%
  \begin{remark}[Title]
    \begin{itemize}
      \item Concise point 1
      \item Concise point 2
    \end{itemize}
  \end{remark}
}
\mode<article>{%
  \begin{remark}[Title]
    Full explanatory text with detailed reasoning...
  \end{remark}
}
```

### Overlays with Didactic Environments

Wrap in `uncoverenv` (didactic environments don't support `<overlay>` directly):

```latex
\begin{uncoverenv}<1,3>
  \begin{definition}[Title]
    Content...
  \end{definition}
\end{uncoverenv}
```

## Toggling Notes

```latex
\ltnoteon   % Show notes (default)
\ltnoteoff  % Hide notes
```

## Best Practices

1. **Write notes as you design** - Don't wait until the end
2. **Be specific** - Reference particular activities, examples
3. **Cite theory** - Connect to established research
4. **Think long-term** - Write for someone years later
5. **Question yourself** - Why this order? Why this example?
6. **Document failures** - Note when designs don't work
7. **Link to assessment** - How will you know if students learned?
8. **Keep notes focused** - One clear point per note

## Workflow

1. **Plan learning objectives** - What should students learn?
2. **Design approach** - How will you structure learning?
3. **Write content with inline notes** - Document reasoning as you write
4. **Review notes** - Check pedagogical rationale is clear
5. **Test with students** - Gather data mentioned in notes
6. **Refine based on feedback** - Update both content and notes

## Complementary Skills

- **variation-theory**: Reference variation patterns in notes
- **try-first-tell-later**: Document try-first pedagogy
- **literate-programming**: Apply similar documentation principles to code
- **latex-writing**: Follow LaTeX best practices in documentation

## Summary

**Key insight**: Literate programming explains code to humans; didactic notes explain *pedagogical design* to educators. Both make implicit reasoning explicit for future readers.

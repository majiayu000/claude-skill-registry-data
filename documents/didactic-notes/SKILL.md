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

This skill applies the principle of documenting pedagogical design decisions in educational materials, analogous to how literate programming documents code design decisions.

## Core Principle

**Document not just what you teach, but *why* you teach it that way.**

Just as literate programming makes code reasoning explicit, didactic notes make pedagogical reasoning explicit using the `\ltnote{...}` command from the LaTeX `didactic` package.

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
  the actual behavior, helping them discern the critical aspect of
  how the function processes its input.
}
```

The note documents the pedagogical strategy (try-first), the learning theory (contrast pattern from variation theory), and the intended learning outcome (discerning the critical aspect).

## Who Benefits from Didactic Notes

Making pedagogical reasoning explicit helps:

- **Future instructors**: Understand and adapt the material
- **Authors**: Reflect on instructional design choices
- **Researchers**: Analyze pedagogical approaches
- **Students** (when notes are visible): Understand the learning design

## The `didactic` Package

The `didactic` LaTeX package provides infrastructure for educational material design, including:

- The `\ltnote{...}` command for pedagogical margin notes
- Commands to toggle notes on/off: `\ltnoteoff` and `\ltnoteon`
- Various semantic environments (activity, exercise, question, etc.)
- Tools for creating educational materials that work as both slides (Beamer) and articles

### Package Setup

```latex
\usepackage[marginparmargin=outer]{didactic}
```

Options:
- `marginparmargin=outer` - Place margin notes on outer margins (default for `\ltnote`)
- `inner=20mm`, `outer=60mm` - Set margin widths
- `notheorems` - Disable automatic theorem environments

## Learning Objectives with Restatable Environment

**CRITICAL**: When documenting learning objectives in educational materials, use the `restatable` environment with the `lo` semantic environment.

### Defining Learning Objectives

Use `\begin{restatable}{lo}{MnemonicLabel}\label{MnemonicLabel}...\end{restatable}` in your abstract or learning objectives section:

```latex
\begin{restatable}{lo}{FilesLOPersistence}\label{FilesLOPersistence}%
  Förklara skillnaden mellan primärminne och sekundärminne samt varför filer
  behövs för persistens.
\end{restatable}

\begin{restatable}{lo}{FilesLOOperations}\label{FilesLOOperations}%
  Använda filoperationer (\mintinline{python}{open()},
  \mintinline{python}{read()}, \mintinline{python}{write()},
  \mintinline{python}{close()}) korrekt.
\end{restatable}
```

**Key points:**
- Use **mnemonic labels** (e.g., `FilesLOPersistence`, not `FilesLO1`)
- Labels describe the objective content, not just numbers
- **CRITICAL**: Add `\label{MnemonicLabel}` matching the restatable name for `\cref{}` support
- The `%` after the opening brace prevents unwanted whitespace

### Referring to Learning Objectives

**Two ways to reference learning objectives:**

1. **Using `\cref{}`** - For explicit, prose-style references in expanded notes
2. **Using starred commands** - For compact display of full LO text

#### Method 1: Using `\cref{}` (Recommended for Expanded Notes)

When writing more detailed pedagogical notes, use `\cref{Label}` to reference learning objectives explicitly:

**Format pattern:**
```latex
\ltnote{%
  Relevanta lärandemål:
  \cref{FilesLOPersistence}

  \textbf{Variationsmönster}: Kontrast

  \textbf{Vad som varierar}: Typ av minne (primär vs sekundär)...

  \textbf{Kritiska aspekter för} \cref{FilesLOPersistence}:
  \begin{itemize}
    \item \textbf{Persistens som koncept}: Studenten måste urskilja...
  \end{itemize}
}
```

**Advantages of `\cref{}`:**
- More natural in prose: "Kritiska aspekter för \cref{FilesLOOperations}:"
- Cleaner when referencing multiple times in the same note
- Better for expanded, detailed pedagogical annotations
- Works in lists and other environments

#### Method 2: Using Starred Commands (Compact Version)

For more concise notes, use the starred command `\LabelName*` which expands to the full LO text:

**Format pattern:**
```latex
\ltnote{%
  Relevanta lärandemål:
  \FilesLOPersistence*

  \textbf{Kontrast}: Typ av minne (primär vs sekundär)...
}
```

**Key formatting rules:**
1. **Use header**: Begin with "Relevanta lärandemål:" (or "Relevant learning objectives:" in English)
2. **Each LO on its own line**: Don't use commas between multiple LOs
3. **No trailing punctuation**: Don't add periods after LO commands
4. **Blank line after LOs**: Separate LOs from the rest of the note content

**Multiple learning objectives with `\cref{}`:**
```latex
\ltnote{%
  Relevanta lärandemål:
  \cref{FilesLOOperations}, \cref{FilesLOContextMgr}, \cref{FilesLOFileTypes}

  \textbf{Variationsmönster}: Generalisering + Kontrast

  \textbf{Kontrast för} \cref{FilesLOContextMgr}: Resurshanteringsmetod...

  \textbf{Separation för} \cref{FilesLOOperations} \textbf{och}
  \cref{FilesLOFileTypes}: Läsa vs skriva...
}
```

**Multiple learning objectives with starred commands:**
```latex
\ltnote{%
  Relevanta lärandemål:
  \FilesLOOperations*
  \FilesLOContextMgr*
  \FilesLOFileTypes*

  \textbf{Generalisering + Kontrast}: Koppling till...
}
```

**CRITICAL: Do NOT add prefixes like "LO:" or "\textbf{LO}:"**

The command `\FilesLOPersistence*` already produces "Lärandemål 1" (or "Learning Objective 1" in English documents). Adding extra prefixes creates redundancy:

**Wrong:**
```latex
\ltnote{%
  \textbf{LO}: \FilesLOPersistence*.  % WRONG: Double prefix
}
```

**Wrong:**
```latex
\ltnote{%
  \FilesLOPersistence*, \FilesLOContextMgr*.  % WRONG: Commas, periods
}
```

**Correct:**
```latex
\ltnote{%
  Relevanta lärandemål:
  \FilesLOPersistence*
  \FilesLOContextMgr*

  \textbf{Mönster}: ...
}
```

### Learning Objectives Cannot Be in Lists

**CRITICAL**: Learning objective commands created by `restatable` are like theorem environments—they cannot be placed inside `\begin{itemize}` or other list environments.

**Wrong:**
```latex
\ltnote{%
  \textbf{Kritiska aspekter}:
  \begin{itemize}
    \item \FilesLOOperations* --- Resurshantering
    \item \FilesLOContextMgr* --- Automatisk stängning
  \end{itemize}
}
```

**Correct - Move LO commands outside lists:**
```latex
\ltnote{%
  \FilesLOOperations*, \FilesLOContextMgr*.

  \textbf{Kritiska aspekter}:
  \begin{itemize}
    \item \textbf{Resurshantering}: Filer måste stängas.
    \item \textbf{Kontexthanterare}: Automatisk stängning även vid fel.
  \end{itemize}
}
```

**Alternative - Reference in prose:**
```latex
\ltnote{%
  \textbf{Kritiska aspekter för} \FilesLOOperations* \textbf{och} \FilesLOContextMgr*\textbf{:}
  \begin{itemize}
    \item \textbf{Resurshantering}: Filer måste stängas.
    \item \textbf{Kontexthanterare}: Automatisk stängning.
  \end{itemize}
}
```

### Setup for Restatable Learning Objectives

Ensure your preamble includes:

```latex
\usepackage{thmtools,thm-restate}
\usepackage{didactic}

\ProvideSemanticEnv{lo}{Learning Objective}
  [style=definition,numbered=yes]
  {LO}{LO}
  {Learning objective}{Learning objectives}

% Translations for Swedish
\ProvideTranslation{swedish}{Learning Objective}{Lärandemål}
\ProvideTranslation{swedish}{LO}{lm}
\ProvideTranslation{swedish}{Learning objective}{Lärandemål}
\ProvideTranslation{swedish}{Learning objectives}{Lärandemål}
```

## Citing Pedagogical Research with Biblatex

### Separate Bibliography for Pedagogical References

**Best practice**: Use a separate `.bib` file for pedagogical and learning theory references (e.g., `ltnotes.bib`), distinct from domain-specific references.

**In your preamble:**
```latex
\usepackage[natbib,style=alphabetic,maxbibnames=99]{biblatex}
\addbibresource{bibliography.bib}  % Domain references
\addbibresource{ltnotes.bib}        % Pedagogical references
```

### Creating ltnotes.bib

Create a separate file with pedagogical references:

```bibtex
@article{MartonPang2006,
  author    = {Marton, Ference and Pang, Ming Fai},
  title     = {On Some Necessary Conditions of Learning},
  journal   = {Journal of the Learning Sciences},
  year      = {2006},
  volume    = {15},
  number    = {2},
  pages     = {193--220},
  doi       = {10.1207/s15327809jls1502_2}
}

@book{Marton2015,
  author    = {Marton, Ference},
  title     = {Necessary Conditions of Learning},
  publisher = {Routledge},
  address   = {London},
  year      = {2015},
  isbn      = {978-0-415-739139}
}
```

### Using Citations in Didactic Notes

**Use biblatex citation commands** instead of hardcoded references:

**Wrong:**
```latex
\ltnote{%
  Following Marton & Pang (2006), we vary the operation while keeping
  the pattern invariant...
}
```

**Correct:**
```latex
\ltnote{%
  Following \textcite{MartonPang2006}, we vary the operation while keeping
  the pattern invariant...
}
```

**Common biblatex commands for pedagogical notes:**
- `\textcite{key}` → "Marton and Pang (2006)"
- `\parencite{key}` → "(Marton and Pang 2006)"
- `\citeauthor{key}` → "Marton and Pang"
- `\citeyear{key}` → "2006"

**Example in context:**
```latex
\ltnote{%
  \FilesLOPersistence*.

  \textbf{Kontrast}: Typ av minne (primär vs sekundär).

  Enligt \textcite{MartonPang2006} måste studenter erfara variation i
  kritiska dimensioner för att kunna urskilja dessa aspekter.
}
```

## The `\ltnote` Command

The `\ltnote{...}` command creates margin notes documenting pedagogical rationale:

```latex
\ltnote{%
  We want to investigate what people think literate programming is.
  This will help us understand the correctness of their prior knowledge.

  This also gives us the contrast pattern for the goals of literate
  programming. They think of what it might mean, whereas when we give
  the definition below, we introduce contrast to their thoughts.
}
```

### When to Use `\ltnote`

Use `\ltnote` to document:

1. **Which learning objectives are addressed**
   - Use "Relevanta lärandemål:" header (or "Relevant learning objectives:" in English)
   - Reference using restatable commands on separate lines: `\FilesLOPersistence*`
   - Map activities to specific objectives
   - Show how variation patterns support objectives

2. **Why specific pedagogical strategies are used**
   - "We use try-first pedagogy here to activate prior knowledge"
   - "This applies the contrast pattern from variation theory"
   - Cite learning theory: `\textcite{MartonPang2006}`

3. **References to learning theories**
   - Variation theory patterns (contrast, separation, generalization, fusion)
   - Cognitive load theory considerations
   - Active learning principles
   - Use biblatex citations instead of hardcoded references

4. **Critical aspects students should discern**
   - What aspects become visible through variation
   - How invariants help students focus on critical features

5. **Design trade-offs and decisions**
   - Why examples are ordered in a particular way
   - Why certain details are omitted or included

6. **Future improvements**
   - Notes for refining the material
   - Data to collect for assessment

7. **Statistical or assessment purposes**
   - "This question helps us gauge prior knowledge"
   - "We collect this data to improve future iterations"

## Writing Effective Didactic Notes

### CRITICAL: Connect to Learning Objectives

**Core principle**: Variation patterns must be tied to specific learning objectives.

When documenting variation theory applications, ALWAYS:

1. **Reference learning objectives explicitly with `\cref{}`**:
   ```latex
   \ltnote{%
     Relevanta lärandemål:
     \cref{FilesLOPersistence}

     \textbf{Variationsmönster}: Kontrast

     \textbf{Vad som varierar}: Typ av minne (primär vs sekundär), egenskaper
     (flyktigt vs oflyktigt).

     \textbf{Vad som hålls invariant}: Behovet att lagra data.

     \textbf{Kritiska aspekter för} \cref{FilesLOPersistence}:
     \begin{itemize}
       \item \textbf{Persistens som koncept}: Studenten måste urskilja att
         filer löser problemet med datapersistens.
     \end{itemize}
   }
   ```

2. **Map variation patterns to objectives**: Show HOW the variation helps achieve the objectives:
   ```latex
   \ltnote{%
     Relevanta lärandemål:
     \cref{FilesLOOperations}, \cref{FilesLOContextMgr}

     \textbf{Variationsmönster}: Generalisering + Kontrast

     \textbf{Kontrast för} \cref{FilesLOContextMgr}: Resurshanteringsmetod
     (\mintinline{python}{open()}/\mintinline{python}{close()} vs
     \mintinline{python}{with}). Studenten måste urskilja att
     \mintinline{python}{with} garanterar stängning även vid fel.

     \textbf{Kritiska aspekter}:
     \begin{itemize}
       \item \textbf{Resurshantering krävs}: Filer måste frigöras explicit.
       \item \textbf{Kontexthanterare löser problemet}: Automatisk stängning.
     \end{itemize}

     \textbf{Koppling till print/input}: Samma princip (strukturera data för
     I/O), olika destination (terminal vs fil).
   }
   ```

3. **Explain why the variation works**: Connect to learning theory with citations:
   ```latex
   \ltnote{%
     Relevanta lärandemål:
     \cref{FilesLOCSV}

     \textbf{Variationsmönster}: Generalisering + Kontrast

     \textbf{Kritiska aspekter för} \cref{FilesLOCSV}:
     \begin{itemize}
       \item \textbf{Struktureringsprincipen}: Studenten måste urskilja att
         formatet är en konvention mellan skrivare och läsare.
       \item \textbf{Standardformat överlägset}: CSV löser edge cases som egen
         parsing missar.
     \end{itemize}

     Enligt \textcite{MartonPang2006} måste studenter erfara variation i
     kritiska dimensioner för att kunna urskilja dessa aspekter.
   }
   ```

### Structure Your Notes

1. **State learning objectives**: What should students be able to do?
2. **Reference theory**: Connect to established learning principles
3. **Explain the mechanism**: How does this design choice support the objectives?
4. **Map activities to objectives**: Show which activities address which objectives
5. **Note alternatives or improvements**: What else could work?

### Language Consistency in Notes

**CRITICAL**: Match the language of `\ltnote` content to the document's instructional language.

**Rule**: If the student-facing content is in language X, write `\ltnote` content in language X.

**When to use English in non-English documents**:
- Established technical terms (use `\foreignlanguage{english}{term}`)
- Direct quotations from English sources
- Code examples and command names (naturally in English)
- References to English-language concepts that lack standard translations

**Examples**:

**Good - Swedish document with Swedish notes:**
```latex
\begin{exercise}
  Hur kan vi implementera addition av två bråk?
\end{exercise}

\ltnote{%
  \textbf{Lärandemål}: LO1 (Implementera aritmetiska operationer)

  \textbf{Variationsmönster}: Kontrast

  Vi varierar operationen (addition vs subtraktion) medan vi håller
  operatoröverlagringsmönstret invariant. Detta hjälper studenter att
  urskilja att \mintinline{python}{__add__} och \mintinline{python}{__radd__}
  följer samma mönster.

  Enligt Marton \& Pang (2006) måste studenter erfara variation för att
  kunna urskilja kritiska aspekter. Här skapar vi variation genom att
  visa både \foreignlanguage{english}{commutative} (addition) och
  \foreignlanguage{english}{non-commutative} (subtraktion) operationer.
}
```

**Bad - Mixing languages unnecessarily:**
```latex
\ltnote{%
  \textbf{Learning Objectives}: LO1 (Implement arithmetic operations)

  \textbf{Variation Pattern}: Contrast

  We vary the operation while keeping invariant...
}
```
In a Swedish document, this creates cognitive dissonance and makes notes harder to read for instructors working in Swedish.

**When English is appropriate:**
```latex
\ltnote{%
  Vi använder \foreignlanguage{english}{try-first pedagogy} här eftersom
  studenter ska förutspå innan vi förklarar. Detta skapar
  \foreignlanguage{english}{contrast} mellan deras mentala modell och
  det faktiska beteendet.

  Referens till kod: \mintinline{python}{__add__} kallas automatiskt.
}
```

**LaTeX command for language switching:**
```latex
\foreignlanguage{english}{technical term or phrase}
```

### Choosing Between Detailed and Compact Notes

**Use detailed notes with `\cref{}` when:**
- Writing comprehensive pedagogical annotations
- Explaining multiple critical aspects for each LO
- Referencing LOs multiple times within the same note
- Need prose-style integration ("Kritiska aspekter för \cref{LO}:")

**Use compact notes with starred commands when:**
- Space is limited (avoiding "lost floats" errors)
- LOs are only referenced once at the beginning
- Simple, concise annotations suffice
- Quick overview more important than detailed explanation

### Example Patterns

**Detailed pattern with `\cref{}`:**
```latex
\ltnote{%
  Relevanta lärandemål:
  \cref{FilesLOPersistence}

  \textbf{Variationsmönster}: Kontrast

  \textbf{Vad som varierar}: Typ av minne (primär vs sekundär), egenskaper
  (flyktigt vs oflyktigt).

  \textbf{Vad som hålls invariant}: Behovet att lagra data.

  \textbf{Kritiska aspekter för} \cref{FilesLOPersistence}:
  \begin{itemize}
    \item \textbf{Persistens som koncept}: Primärminne försvinner vid
      avstängning, sekundärminne består. Studenten måste urskilja att filer
      löser problemet med datapersistens.
    \item \textbf{Avvägning}: Primärminne snabbt men temporärt, sekundärminne
      långsammare men permanent.
  \end{itemize}

  Enligt \textcite{MartonPang2006} gör denna kontrast de kritiska aspekterna
  av persistens urskiljbara för studenter.
}
```

**Compact pattern with starred commands:**
```latex
\ltnote{%
  Relevanta lärandemål:
  \FilesLOPersistence*

  \textbf{Kontrast}: Typ av minne (primär vs sekundär). Invariant: Behovet att
  lagra data.
}
```

**Referencing multiple learning objectives with detail:**
```latex
\ltnote{%
  Relevanta lärandemål:
  \cref{FilesLOOperations}, \cref{FilesLOContextMgr}, \cref{FilesLOFileTypes}

  \textbf{Variationsmönster}: Generalisering + Kontrast + Separation

  \textbf{Generalisering från terminal-I/O}: Filoperationer följer samma princip
  som \mintinline{python}{print()}/\mintinline{python}{input()}. Invariant:
  I/O-mönstret. Varierar: Destination (terminal vs fil).

  \textbf{Kontrast för} \cref{FilesLOContextMgr}: Resurshanteringsmetod...

  \textbf{Separation för} \cref{FilesLOOperations} \textbf{och}
  \cref{FilesLOFileTypes}: Läsa vs skriva, text vs binär...
}
```

**Explaining pedagogical choices:**
```latex
\ltnote{%
  We need to do the same thing twice to contrast what we want the
  students to focus on, namely:
  \begin{enumerate}
  \item The specific feature that works in case A but not case B,
  \item How we can achieve the same goal using different approaches.
  \end{enumerate}
}
```

**Documenting activities:**
```latex
\ltnote{%
  The purpose of \cref{QuestionLabel} is to get students thinking about
  concepts they already know that might relate to this topic. This
  activates prior knowledge and creates mental hooks for new information.
}
```

**Noting assessment purposes:**
```latex
\ltnote{%
  We want to investigate how many students have heard of this concept.
  This will give us baseline statistics and help understand the
  correctness of answers in \cref{FollowUpActivity}.
}
```

**Explaining omissions:**
```latex
\ltnote{%
  We deliberately omit the technical details here to avoid cognitive
  overload. Students should first grasp the conceptual model before
  encountering implementation complexity.
}
```

## Integration with Learning Theories

### Variation Theory

Document how your material creates patterns of variation, citing \textcite{MartonPang2006}:

```latex
\ltnote{%
  Relevanta lärandemål:
  \AlgorithmsLOAbstraction*

  \textbf{Mönster}: Generalisering

  \textbf{Varierar}: Programmeringsspråk (Python vs Java)
  \textbf{Invariant}: Algoritmisk princip

  Enligt \textcite{MartonPang2006} hjälper denna variation studenter att
  urskilja att den algoritmiska principen är oberoende av språksyntax.
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

## Toggling Notes for Different Audiences

Notes can be hidden or shown depending on the audience:

```latex
% In instructor version (notes visible)
\ltnoteon  % This is the default

% In student version (notes hidden)
\ltnoteoff
```

Use cases:
- **Students**: Hide notes to avoid distraction
- **Instructors**: Show notes to understand pedagogical design
- **Co-authors**: Show notes during material development
- **Researchers**: Show notes when analyzing instructional design

## Integration with Other Didactic Features

### Semantic Environments

The `didactic` package provides semantic environments that pair well with `\ltnote`:

```latex
\begin{activity}
  Try implementing this function before reading further.
\end{activity}

\ltnote{%
  This activity uses try-first pedagogy to engage students before
  providing the solution.
}
```

Available environments:
- `activity` - Active learning tasks
- `exercise` - Practice problems
- `question` - Discussion questions
- `remark` - Side notes for students
- `summary` - Section summaries
- `definition`, `theorem`, `example` - Mathematical content

### Side-by-Side Environments with \textbytext*

**Purpose**: Place two semantic environments side-by-side for immediate visual contrast.

The didactic.sty package provides `\textbytext{...}{...}` and `\textbytext*{...}{...}` to create side-by-side layouts:

**Syntax**:
```latex
\textbytext*{%
  \begin{definition}[Concept A]
    Description emphasizing one aspect...
  \end{definition}
}{%
  \begin{definition}[Concept B]
    Description emphasizing contrasting aspect...
  \end{definition}
}
```

**Key differences**:
- **\textbytext**** (starred): Uses fullwidth for maximum space—for article mode
- **\textbytext** (non-starred): Uses normal column width—works in Beamer presentations

**CRITICAL - Beamer compatibility**:
- `\textbytext*` (starred) does NOT work inside `\begin{frame}...\end{frame}`, even with `[fragile]`
- **Solution**: Use `\mode<presentation>` and `\mode<article>` to split:
  - Presentation mode: `\textbytext` (non-starred)
  - Article mode: `\textbytext*` (starred, fullwidth)

**When to use**:
- Concepts defined in relation to each other (primärminne/sekundärminne)
- Creating simultaneous contrast in variation theory
- Comparing two approaches side-by-side (manual vs automatic)

**Example (Beamer-compatible with mode splits)**:
```latex
\begin{frame}
  \mode<presentation>{%
    \textbytext{%
      \begin{definition}[Primärminne]
        Datorns arbetsminne där exekverande program lagras.
        Flyktigt minne med snabb åtkomst (nanosekunder).
      \end{definition}
    }{%
      \begin{definition}[Sekundärminne]
        Oflyktigt minne där filer lagras.
        Långsammare åtkomst (mikro- till millisekunder).
      \end{definition}
    }
  }
  \mode<article>{%
    \textbytext*{%
      \begin{definition}[Primärminne]
        Datorns arbetsminne där exekverande program lagras.
        Flyktigt minne med snabb åtkomst (nanosekunder).
      \end{definition}
    }{%
      \begin{definition}[Sekundärminne]
        Oflyktigt minne där filer lagras.
        Långsammare åtkomst (mikro- till millisekunder).
      \end{definition}
    }
  }
\end{frame}

\ltnote{%
  Relevanta lärandemål:
  \cref{FilesLOPersistence}

  \textbf{Variationsmönster}: Kontrast (spatial, inte temporal)

  Side-by-side layout skapar omedelbar visuell kontrast mellan flyktigt/oflyktigt,
  snabbt/långsamt. Studenter kan scanna fram och tillbaka mellan definitionerna
  vilket gör de kontrasterande aspekterna urskiljbara.
}
```

**For article-only documents** (not using Beamer), you can use `\textbytext*` directly without mode splits.

**Works with**: definition, example, remark, block, any semantic environment

### Figures and Tables with sidecaption

**Principle**: Images and tables should use memoir's sidecaption for better layout and accessibility.

**For figures**:
```latex
\begin{frame}
  \begin{figure}
    \begin{sidecaption}{Clear description of image content}[fig:label]
      \includegraphics[width=0.7\textwidth]{path/to/image}
    \end{sidecaption}
  \end{figure}
\end{frame}
```

**For tables**:
```latex
\begin{frame}
  \begin{table}
    \begin{sidecaption}{Description of table contents}[tab:label]
      \begin{tabular}{ll}
        ... table content ...
      \end{tabular}
    \end{sidecaption}
  \end{table}
\end{frame}
```

**Benefits**:
- Caption alongside content (better use of horizontal space)
- Improved accessibility (screen readers)
- Context provided in notes/handouts

**Caption guidelines**:
- **Describe content**: "Python documentation for file I/O operations"
- **Be specific**: "File modes available in open() function" not "Documentation screenshot"
- **Explain relevance**: "CSV module methods showing reader and writer classes"

**Anti-pattern** (standalone image without caption):
```latex
% BAD: No context or caption
\begin{frame}
  \includegraphics[width=\columnwidth]{docs-files.png}
\end{frame}
```

### Semantic Environments for Generalizations

**Principle**: When generalizing from examples, capture the generalization in a semantic environment (definition, remark, block) placed AFTER the examples.

**Why use semantic environments for generalizations**:
1. **Highlights importance**: Visual distinction signals "this is a key takeaway"
2. **Makes referenceable**: Can be cited in pedagogical notes and student materials
3. **Suitable for notes**: Environments appear cleanly in article mode/handouts
4. **Searchable**: Students can scan for definitions/remarks when reviewing

**Environment selection**:
- **definition**: Formal concept definitions
- **remark**: Important observations, principles, or implications
- **block**: Key takeaways, summaries, or synthesis points
- **example**: When generalization is best shown through code pattern

**Integration with variation theory**: The semantic environment contains the **invariant pattern** that emerged from **variation** in the examples.

**Example**:
```latex
% First: Examples creating variation
\begin{example}[Läsa fil]
  with open("data.txt", "r") as fil:
      innehåll = fil.read()
\end{example}

\begin{example}[Skriva fil]
  with open("data.txt", "w") as fil:
      fil.write(text)
\end{example}

% Then: Generalization in semantic environment
\begin{remark}[Filhanteringsmönster]
  All filhantering följer mönstret: öppna → bearbeta → stäng.
  Funktionen \mintinline{python}{with} garanterar att filen stängs
  automatiskt även om fel uppstår.
\end{remark}

\ltnote{%
  Relevanta lärandemål:
  \cref{FilesLOOperations}, \cref{FilesLOContextMgr}

  \textbf{Variationsmönster}: Generalisering

  Studenter ser invariant mönster (öppna-bearbeta-stäng) över varierade
  operationer (läsa vs skriva). Generaliseringen i remark-environment
  gör mönstret explicit efter att studenter erfarit variationen.
}
```

**Anti-pattern** (generalization buried in prose before examples):
```latex
% BAD: Principle stated before examples
När vi arbetar med filer måste vi alltid öppna dem först,
sedan arbeta med innehållet, och till sist stänga dem.

\begin{example}[Läsa fil]
  ...
\end{example}
```

### Overlay Specifications with Didactic Environments

**Issue**: Didactic package's semantic environments don't support Beamer's `<overlay>` syntax directly.

**Problem**: Writing `\begin{definition}<1,3>[Title]` or `\begin{definition}[Title]<1,3>` causes the overlay spec to appear as text in notes.

**Solution**: Wrap in `uncoverenv`:

```latex
\begin{frame}
  \begin{uncoverenv}<1,3>
    \begin{definition}[Primärminne]
      Datorns arbetsminne där exekverande program lagras...
    \end{definition}
  \end{uncoverenv}

  \begin{uncoverenv}<2,3>
    \begin{definition}[Sekundärminne]
      Oflyktigt minne där filer lagras...
    \end{definition}
  \end{uncoverenv>
\end{frame}
```

**Note**: For side-by-side definitions, use `\textbytext` (presentation) / `\textbytext*` (article) with mode splits instead of overlay specs—the spatial contrast is more effective than temporal uncovering. See "Side-by-Side Environments with \textbytext*" section above for Beamer-compatible implementation.

**Correct approach for multiple examples with overlays**:
```latex
\begin{frame}[fragile]
  \begin{uncoverenv}<+->
    \begin{example}[Write to file]
      Skriva text till en fil:
      \inputminted{python}{write.py}
    \end{example}
  \end{uncoverenv>

  \begin{uncoverenv}<+->
    \begin{example}[Read from file]
      Läsa från fil:
      \inputminted{python}{read.py}
    \end{example}
  \end{uncoverenv>
\end{frame}
```

### Verbose Environments: Presentation vs Article Splits

**Issue**: Semantic environments (definition, remark, example, block) can become too verbose for slides when they contain multiple sentences or paragraphs.

**Solution**: Use `\mode<presentation>` and `\mode<article>` to provide concise versions for slides and full explanations for articles.

**When to split**:
- **Verbose prose**: More than 2-3 lines of running text in an environment
- **Multiple paragraphs**: Any environment with 2+ paragraphs
- **Complex examples**: Scenarios with extensive context that can be summarized

**Pattern**:
```latex
\begin{frame}
  \mode<presentation>{%
    \begin{remark}[Title]
      \begin{itemize}
        \item Concise bullet point 1
        \item Concise bullet point 2
        \item Concise bullet point 3
      \end{itemize}
    \end{remark}
  }
  \mode<article>{%
    \begin{remark}[Title]
      Full explanatory text with multiple sentences providing
      detailed context and reasoning.

      Additional paragraphs can explain nuances that would
      overwhelm a slide but are valuable in written form.
    \end{remark}
  }
\end{frame}
```

**Example - Verbose remark becomes bullets**:
```latex
\begin{frame}
  \mode<presentation>{%
    \begin{remark}[Kontrastpunkten: Garanterad resurshantering]
      \begin{itemize}
        \item \mintinline{python}{with}: Filen stängs alltid, även vid exception
        \item Manuell hantering: Risk att filen lämnas öppen vid fel
        \item Automatisk cleanup när blocket lämnas
      \end{itemize}
    \end{remark}
  }
  \mode<article>{%
    \begin{remark}[Kontrastpunkten: Garanterad resurshantering]
      Båda metoderna fungerar när allt går som planerat. Men
      with-satsen har en avgörande fördel: den garanterar att
      filen alltid stängs korrekt, även om ett exception uppstår.

      Med manuell hantering riskerar vi att filen lämnas öppen
      om något går fel. With-satsen implementerar
      kontexthanterare-protokollet och anropar close()
      automatiskt när blocket lämnas.
    \end{remark}
  }
\end{frame}
```

**Example - Long example becomes concise**:
```latex
\begin{frame}
  \mode<presentation>{%
    \begin{example}[Spara spelets progress]
      Spel måste minnas poäng och achievements mellan
      sessioner—löses genom att spara data i fil.
    \end{example}
  }
  \mode<article>{%
    \begin{example}[Spara spelets progress]
      Ett spel behöver komma ihåg spelarens poäng, nivå,
      och upplåsta achievements mellan olika spelsessioner.
      När spelaren stänger ner programmet och startar det
      igen nästa dag ska all progress finnas kvar. Detta
      löses genom att spara data i en fil på hårddisken.
    \end{example}
  }
\end{frame}
```

**Key principle**: Slides need visual clarity and conciseness; articles can provide depth and explanation. Design for both audiences.

### Cross-References

Use `\label` and `\cref` to reference activities in notes:

```latex
\begin{activity}\label{FirstAttempt}
  What do you think this function does?
\end{activity}

\ltnote{%
  The purpose of \cref{FirstAttempt} is to activate prior knowledge
  before we formally define the concept.
}
```

## Workflow for Educational Material Development

1. **Plan the learning objectives**: What should students learn?
2. **Design the instructional approach**: How will you structure learning?
3. **Write content with inline notes**: Document your reasoning as you write
4. **Review notes**: Check that pedagogical rationale is clear
5. **Test with students**: Gather data mentioned in notes
6. **Refine based on feedback**: Update both content and notes
7. **Share with colleagues**: Notes help them understand and adapt material

## Best Practices

1. **Write notes as you design**: Don't wait until the end
2. **Be specific**: Reference particular activities, examples, or sections
3. **Cite theory**: Connect to established research when applicable
4. **Think long-term**: Write for someone encountering the material years later
5. **Question yourself**: Why this order? Why this example? Why now?
6. **Document failures**: Note when designs don't work as intended
7. **Link to assessment**: How will you know if students learned?
8. **Keep notes focused**: One clear point per note

## Example: Complete Section with Notes

First, define learning objectives in your abstract:

```latex
\begin{restatable}{lo}{RecursionLOConcept}%
  Förklara rekursionsbegreppet och identifiera basfall och rekursivt steg.
\end{restatable}

\begin{restatable}{lo}{RecursionLOImplementation}%
  Implementera enkla rekursiva funktioner korrekt.
\end{restatable}
```

Then use them in your content:

```latex
\section{Introduction to Recursion}

Let's start with your intuition.

\ltnote{%
  Relevanta lärandemål:
  \cref{RecursionLOConcept}

  \textbf{Variationsmönster}: Try-first pedagogy

  Vi börjar med utforskning av förkunskaper för att aktivera studenternas
  intuitiva förståelse. Studenten förbinder rekursion med konkreta exempel
  (ryska dockor, fraktaler) innan formell definition introduceras.
}

\begin{activity}\label{WhatIsRecursion}
  Have you seen anything in everyday life that contains smaller versions
  of itself?
\end{activity}

Now let's look at how this appears in programming.

\ltnote{%
  \textbf{Variationsmönster}: Generalisering

  Vi rör oss från konkreta vardagsexempel till kod, vilket ger en bro mellan
  intuitiv och formell förståelse.

  Enligt \textcite{MartonPang2006} underlättar denna progression från bekanta
  till abstrakta kontexter lärande genom att skapa variation i representation
  medan konceptet hålls invariant.
}

Here's a simple recursive function:

<<factorial function>>=
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)
@

\ltnote{%
  Relevanta lärandemål:
  \cref{RecursionLOConcept}, \cref{RecursionLOImplementation}

  \textbf{Variationsmönster}: Generalisering (helhet före delar)

  \textbf{Kritiska aspekter för} \cref{RecursionLOConcept}:
  \begin{itemize}
    \item \textbf{Rekursiv struktur}: Funktionen anropar sig själv med
      modifierat argument. Studenten måste urskilja självreferensen.
    \item \textbf{Basfall}: Villkoret \mintinline{python}{n <= 1} stoppar
      rekursionen. Utan detta blir det oändlig loop.
  \end{itemize}

  \textbf{Pedagogisk sekvens}: Vi börjar med den kompletta funktionen
  (helheten) enligt variation theory. I senare avsnitt bryter vi ner
  basfallet och det rekursiva steget (delarna), genom att variera vad vi
  fokuserar på medan andra aspekter hålls invarianta.
}
```

## Complementary Skills

Didactic notes work well with:

- **variation-theory**: Reference variation patterns in your notes
- **try-first-tell-later**: Document why you're using try-first pedagogy
- **literate-programming**: Apply similar documentation principles to code
- **pqbl**: Explain the pedagogical reasoning behind question sequences

## When to Use This Skill

Use didactic notes when writing or designing:
- Lecture materials (Beamer slides, course notes)
- Tutorials and educational documentation
- Learning activities and exercises
- Materials for collaborative development
- Instructional design research

## Summary

**Key insight**: Literate programming explains code to humans; didactic notes explain *pedagogical design* to educators. Both make implicit reasoning explicit for future readers (including your future self).

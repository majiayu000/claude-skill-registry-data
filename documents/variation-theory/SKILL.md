---
name: variation-theory
description: Apply variation theory of learning to structure instructional content using contrast, generalization, and fusion patterns. Variation must target the critical aspects of the learning objective. Use when writing educational materials, explanations, tutorials, literate programming documentation (.nw files), or when user mentions variation theory, learning theory, pedagogy, or critical aspects of learning. Works alongside the literate-programming skill for .nw files.
---

# Variation Theory of Learning

This skill applies the variation theory of learning, developed by Ference Marton and colleagues, to structure content for optimal learning.

## Core Theoretical Principles

### The Object of Learning
The **object of learning** is what is to be learned. Understanding develops when learners discern the critical aspects of the object of learning.

### Critical Aspects and Discernment
**Critical aspects** are the features that must be discerned for understanding to occur. **Discernment** is the ability to distinguish these aspects.

Marton's central principle: "to learn something, the learner must discern what is to be learned. Discerning the object of learning amounts to discerning its critical aspects" (Marton & Pang, 2006).

### Variation and Invariance
The necessary condition for discernment: learners must experience **variation in a dimension corresponding to that aspect, against the background of invariance** in other aspects.

Key insight: "When some aspect of a phenomenon or an event varies while another aspect or other aspects remain invariant, the varying aspect will be discerned."

## Critical Aspects as the Focus of Variation

**FUNDAMENTAL PRINCIPLE**: Variation must occur in the **critical aspects** of the object of learning. Arbitrary variation does not lead to learning—only variation in critical dimensions enables discernment.

### Identifying Critical Aspects First

Before designing any pattern of variation:

1. **Define the object of learning** - What should learners understand/do?
2. **Identify the critical aspects** - Which features must be discerned?
3. **Design variation IN those aspects** - Create patterns varying the critical dimensions

As Marton states: "The object of learning [...] amounts to becoming able to discern all the critical aspects and to focus on them simultaneously" (NCOL, p. 37).

### Dimensions vs Values: A Crucial Distinction

The principle "one thing at a time" applies to **dimensions of variation (aspects)**, NOT to **values within a dimension**.

- **Dimension (aspect)**: A category/feature type (e.g., "punctuation marks", "file mode", "data structure")
- **Values/features**: Specific instances within that dimension (e.g., `.`/`?`/`!` or `r`/`w`/`a`)

**The principle**:
- **Vary ONE dimension at a time** - to separate aspects from each other
- **Contrast MULTIPLE values together** - within that dimension

**Research evidence** (Gustavsson, 2008; NCOL Ch 6):
- Teaching punctuation marks (`.`, `?`, `!`) separately: **15% improvement**
- Teaching all three together with contrast: **63% improvement**

Similarly, Hatala et al. (2003) found **50% higher diagnostic accuracy** when medical students learned three ECG patterns together versus one category at a time.

**Why**: Meaning derives from differences. Without experiencing contrast between values, students cannot discern what makes each distinct.

### Common Mistake: Varying Non-Critical Aspects

**Anti-pattern**: Creating variation in aspects irrelevant to the learning objective.

**Example**: Teaching "why files need open/close":
- **Wrong**: Vary filename or content (not critical)
- **Right**: Vary what happens when close() is/isn't called, when exceptions occur (the critical aspect is resource management)

### Connection to Try-First-Tell-Later

The try-first-tell-later skill complements variation theory: use try-first prompts to **diagnose which critical aspects students can already discern**, then design variation patterns to teach the aspects they cannot yet see. See the try-first-tell-later skill for implementation guidance.

## The Three Patterns of Variation

According to Marton (2015), there are three patterns that enable discernment:

### 1. Contrast
**Purpose**: Help learners recognize that an aspect exists by experiencing what it is versus what it is not.

**How it works**: Present examples that differ in one critical aspect while keeping all other factors constant. The learner experiences variation of different values in one dimension.

**Example**: To understand "height," show two objects identical in all respects except height.

**Note**: Contrast achieves *separation*—the critical aspect becomes separated (discernible) from the whole through experiencing variation in that aspect. Separation is the *result* of contrast, not a separate pattern.

### 2. Generalization
**Purpose**: Help learners recognize that a pattern or principle holds across different contexts.

**How it works**: Present the same critical value in varied appearances. Keep the critical aspect invariant while varying other (non-critical) aspects.

**Example**: Show the same geometric principle applied to triangles, rectangles, circles to reveal the universal pattern.

### 3. Fusion
**Purpose**: Enable learners to experience multiple critical aspects simultaneously as an integrated whole.

**How it works**: Vary several critical aspects at once so learners must attend to their simultaneous interrelationships.

**Example**: In understanding circuits, vary resistance and voltage simultaneously to grasp how changes in one parameter impact the others.

## Pedagogical Sequence

Research suggests using patterns in this developmental order:

1. **Contrast** - Vary the critical aspect while keeping other aspects invariant. This *separates* (makes discernible) the critical aspect from the whole.
2. **Generalization** - Keep the critical value invariant while varying other aspects. This shows the pattern holds across different contexts.
3. **Fusion** - Vary multiple critical aspects simultaneously. This enables learners to experience their interrelationships.

**Important**: Within each pattern, contrast multiple **values** together. The "one at a time" principle applies to **dimensions/aspects**, not to values within a dimension.

### Temporal Sequencing: Examples Before Generalizations

**Core principle**: Examples must precede generalizations. Students need concrete instances creating the necessary variation before abstract principles become meaningful.

**Why this matters**: Variation must be **experienced** before invariants can be discerned. When you state a general principle first, students have no variation pattern to map it onto. The principle remains abstract and difficult to integrate with existing knowledge.

**Anti-pattern example**:
```latex
% BAD: Generalization before examples
Filer behövs för tre huvudsakliga anledningar: persistens, datautbyte,
och skalbarhet.

\begin{example}[Spara spelets progress]
  ...
\end{example}
```

**Good pattern example**:
```latex
% GOOD: Examples create variation, then generalize
\begin{example}[Spara spelets progress]
  Ett spel behöver komma ihåg spelarens poäng mellan körningar...
\end{example}

\begin{example}[Dela data mellan program]
  Ett program genererar e-postadresser som ett annat sedan använder...
\end{example}

\begin{example}[Bearbeta stora datamängder]
  SCB:s namnstatistik innehåller miljontals poster...
\end{example}

\begin{remark}[Varför filer behövs]
  Filer behövs för persistens (minnas mellan körningar), datautbyte
  (överföra mellan program), och skalbarhet (hantera stora mängder data).
\end{remark}
```

**Pedagogical sequence**:
1. Show concrete examples that vary in one dimension (use case)
2. Keep invariant: the solution (using files)
3. Students discern the pattern: different problems, same solution
4. Generalize the pattern in a semantic environment (remark/definition/block)

**Key insight**: The generalization is only meaningful AFTER students have experienced the variation that makes the invariant pattern discernible.

## Common Generalization-Before-Example Violations

**CRITICAL**: This is one of the most common and damaging violations of variation theory. When generalizations precede examples, students cannot discern the pattern because they haven't experienced the necessary variation.

### Why This Violation Is So Harmful

1. **No experiential basis**: Students receive abstract principles with no concrete variation to map them onto
2. **Meaningless abstractions**: Without experiencing variation, generalizations remain empty words
3. **Missed learning opportunity**: The discernment that should happen through variation is bypassed
4. **Backwards pedagogy**: Violates the fundamental principle that variation enables discernment

**Remember**: You cannot discern an invariant pattern without first experiencing variation in that dimension.

### Violation Type 1: Generic/Placeholder Code Before Concrete Examples

**Problem**: Showing abstract code with placeholder values (like `"filename"`, `transformera()`) before concrete working examples.

**Why it's harmful**: The generic code is itself a generalization. Students need to see real, working code with actual filenames and functions before the pattern can be abstracted.

**BAD example**:
```latex
% Abstract code with placeholders first
\begin{frame}[fragile]
  \begin{minted}{python}
file = open("filename", "r")
print(file.read())
file.close()
  \end{minted}
\end{frame}

% Then concrete example
\begin{frame}[fragile]
  \begin{example}[open_close.py]
    \inputminted{python}{examples/open_close.py}
  \end{example}
\end{frame}
```

**GOOD example**:
```latex
% Concrete example first
\begin{frame}[fragile]
  \begin{example}[open_close.py]
    Manuell filhantering med open() och close():
    \inputminted{python}{examples/open_close.py}
  \end{example}
\end{frame}

% Optional: Pattern summary AFTER if needed
\begin{frame}
  \begin{remark}[Filhanteringsmönster]
    All filläsning följer mönstret: open(filnamn, läge) → read() → close()
  \end{remark}
\end{frame}
```

### Violation Type 2: Block/Remark Environments Before Examples

**Problem**: Using semantic environments (block, remark, definition) to state principles before showing examples that demonstrate those principles.

**Why it's harmful**: The semantic environment signals "this is important," but students have no context to understand WHY it's important or WHAT it means.

**BAD example**:
```latex
% Principle stated first
\begin{frame}
  \begin{block}{Filer}
    Vi har alla erfarenhet av filer. Python-program är också filer.
  \end{block}

  \begin{example}[Pythonprogram]
    Filer med .py-ändelse innehåller Python-kod...
  \end{example}

  \begin{example}[Bilder]
    Filer med .jpg eller .png innehåller bilddata...
  \end{example}
\end{frame}
```

**GOOD example**:
```latex
% Examples create variation first
\begin{frame}
  \begin{example}[Pythonprogram]
    Filer med .py-ändelse innehåller Python-kod...
  \end{example}

  \pause

  \begin{example}[Bilder]
    Filer med .jpg eller .png innehåller bilddata...
  \end{example}

  \pause

  \begin{example}[Dokument]
    Filer med .pdf eller .docx innehåller textdokument...
  \end{example}

  % Optional synthesis AFTER examples
  \pause

  \begin{block}{Mönstret}
    Filer lagrar olika typer av data. Ändelsen indikerar innehållstyp.
  \end{block}
\end{frame}
```

### Violation Type 3: Incomplete Skeletons Before Complete Solutions

**Problem**: Showing incomplete code scaffolding with comments like `# TODO` or `# Uppdatera räknaren` before showing complete working implementations.

**Why it's harmful**: The skeleton IS a generalization (the structure without the details). Students need to see complete solutions before the general structure becomes discernible.

**BAD example**:
```latex
% Incomplete skeleton first
\begin{frame}[fragile]
  \begin{example}[Ordräkning --- grundstruktur]
    \begin{minted}{python}
def räkna_ord(text):
    ord_antal = {}
    for rad in text.split("\n"):
        for ord in rad.split(" "):
            # Uppdatera räknaren
    return ord_antal
    \end{minted}
  \end{example}
\end{frame}

% Then complete solutions
\begin{frame}[fragile]
  \begin{example}[Uppdatera räknaren --- try-except]
    \begin{minted}{python}
try:
    ord_antal[ord] += 1
except KeyError:
    ord_antal[ord] = 1
    \end{minted}
  \end{example}
\end{frame}
```

**GOOD example**:
```latex
% Complete solution first
\begin{frame}[fragile]
  \begin{example}[Ordräkning med try-except]
    \begin{minted}{python}
def räkna_ord(text):
    ord_antal = {}
    for rad in text.split("\n"):
        for ord in rad.split(" "):
            try:
                ord_antal[ord] += 1
            except KeyError:
                ord_antal[ord] = 1
    return ord_antal
    \end{minted}
  \end{example}
\end{frame}

% Alternative complete solution
\begin{frame}[fragile]
  \begin{example}[Ordräkning med if-kontroll]
    \begin{minted}{python}
def räkna_ord(text):
    ord_antal = {}
    for rad in text.split("\n"):
        for ord in rad.split(" "):
            if ord not in ord_antal:
                ord_antal[ord] = 1
            else:
                ord_antal[ord] += 1
    return ord_antal
    \end{minted}
  \end{example}
\end{frame}

% NOW students can see the pattern
\begin{frame}
  \begin{remark}[Mönstret]
    Båda lösningarna följer samma grundstruktur: iterera över enheter,
    kontrollera om nyckel finns, uppdatera eller initiera värde.
  \end{remark}
\end{frame}
```

### Violation Type 4: Explanatory Principles Before Demonstrating Examples

**Problem**: Explaining how something works or why it's needed before showing concrete examples where it solves a real problem.

**Why it's harmful**: Abstract explanations lack meaning without concrete context. Students can't appreciate "why" without first experiencing the problem.

**BAD example**:
```latex
% Explanation first
\begin{frame}[fragile]
  \begin{remark}
    Att läsa från filer utan att känna till strukturen är som att gå i
    bäcksvarta mörkret --- vi måste veta exakt var alla saker finns.
  \end{remark}
\end{frame}

% Then example
\begin{frame}
  \begin{activity}[SCB]
    Ladda ner SCB:s namnstatistik och skriv ett program som söker namn.
  \end{activity}
\end{frame}
```

**GOOD example**:
```latex
% Problem/activity first - students experience the difficulty
\begin{frame}
  \begin{activity}[SCB]
    Ladda ner SCB:s namnstatistik och skriv ett program som söker namn.

    Hur vet du var i filen namnen finns? Hur vet du var antalet börjar?
  \end{activity}
\end{frame}

% AFTER students have wrestled with the problem, articulate it
\begin{frame}
  \begin{remark}[Varför filformat behövs]
    Utan överenskommen struktur är filen meningslös --- vi vet inte var
    information finns. Filformat löser detta genom att definiera WHERE
    varje dataelement finns.
  \end{remark>
\end{frame}
```

### How to Review for These Violations

When reviewing educational materials, check for:

**Checklist**:
- [ ] Does generic/abstract code appear before concrete examples?
- [ ] Do block/remark/definition environments state principles before examples demonstrate them?
- [ ] Are incomplete code skeletons shown before complete working solutions?
- [ ] Are explanations of "why" or "how" given before students experience the problem?
- [ ] Do file modes (r/w/a) get explained before examples show their use?
- [ ] Are categorizations (text vs binary) stated before contrasting examples?

**Fix pattern**: For each violation found:
1. **Remove** the generalization from its current position
2. **Ensure** 2-3 concrete examples exist creating necessary variation
3. **Add back** the generalization AFTER examples (in semantic environment if appropriate)
4. **Verify** students can now discern the pattern from the variation

**Remember**: Every generalization should answer the implicit question: "What invariant pattern do these examples share?"

### Side-by-Side Contrast with \textbytext*

**Purpose**: Create simultaneous visual contrast when two concepts need immediate comparison. This implements the Contrast pattern spatially rather than temporally.

**When to use**: Concepts that are defined **in relation to each other** and whose critical aspects are best understood through direct juxtaposition.

**The tool**: LaTeX didactic.sty provides `\textbytext*{...}{...}` to place environments side-by-side:
- **Starred version** (`\textbytext*`): Uses fullwidth for maximum space
- **Non-starred** (`\textbytext`): Uses normal column width

**IMPORTANT - Beamer compatibility**:
- `\textbytext*` (starred) does NOT work inside `\begin{frame}...\end{frame}`, even with `[fragile]`
- **Solution**: Use mode-specific versions:
  - `\mode<presentation>` with `\textbytext` (non-starred, column width works in beamer)
  - `\mode<article>` with `\textbytext*` (starred, fullwidth for article mode)
- This pattern is REQUIRED when using side-by-side contrast in beamer presentations

**Example use case**: Primärminne vs Sekundärminne - concepts defined by their opposing characteristics (flyktigt vs oflyktigt, snabbt vs långsamt).

**Implementation** (beamer-compatible with mode splits):
```latex
\begin{frame}
  \mode<presentation>{%
    \textbytext{%
      \begin{definition}[Primärminne]
        Datorns arbetsminne där exekverande program lagras.
        Detta är flyktigt minne med mycket snabb åtkomst
        (storleksordning nanosekunder).
      \end{definition}
    }{%
      \begin{definition}[Sekundärminne]
        Oflyktigt minne där icke-exekverande program och
        data (filer) lagras. Långsammare åtkomst än primärminne
        (storleksordning mikro- till millisekunder).
      \end{definition}
    }
  }
  \mode<article>{%
    \textbytext*{%
      \begin{definition}[Primärminne]
        Datorns arbetsminne där exekverande program lagras.
        Detta är flyktigt minne med mycket snabb åtkomst
        (storleksordning nanosekunder).
      \end{definition}
    }{%
      \begin{definition}[Sekundärminne]
        Oflyktigt minne där icke-exekverande program och
        data (filer) lagras. Långsammare åtkomst än primärminne
        (storleksordning mikro- till millisekunder).
      \end{definition}
    }
  }
\end{frame}
```

**For article-only contexts** (not beamer), you can use `\textbytext*` directly:
```latex
\textbytext*{%
  \begin{definition}[Primärminne]
    ...
  \end{definition}
}{%
  \begin{definition}[Sekundärminne]
    ...
  \end{definition}
}
```

**Variation pattern analysis**:
- **What varies**: Memory type (primary vs secondary) and all associated characteristics
- **What remains invariant**: The concept of computer memory storing data
- **Critical aspects made discernible**: Volatility (flyktigt/oflyktigt), speed (nanosekunder/millisekunder), purpose (executing/stored programs)

**Why this works**: Side-by-side presentation allows students to scan back and forth between the definitions, making the contrasting features immediately apparent. The spatial arrangement reinforces the conceptual opposition.

**Alternative approaches and when NOT to use**:
- **Sequential presentation** (uncoverenv): Better when you want students to understand each concept independently before comparing
- **\textbytext*** (side-by-side): Better when the concepts are mutually defining and comparison is essential for understanding

### Generalizations in Semantic Environments

**Principle**: When generalizing from examples, capture the generalization in a semantic environment (definition, remark, block) placed AFTER the examples.

**Why use semantic environments**:
1. **Highlights importance**: Visual distinction signals "this is a key takeaway"
2. **Makes referenceable**: Can be cited in pedagogical notes and student materials
3. **Suitable for notes**: Environments appear cleanly in article mode/handouts
4. **Searchable**: Students can scan for definitions/remarks when reviewing

**Environment selection guide**:
- **definition**: Formal concept definitions
  - Example: "En fil är en namngiven samling data som lagras i sekundärminnet"
- **remark**: Important observations, principles, or implications
  - Example: "Filer behövs för persistens, datautbyte, och skalbarhet"
- **block**: Key takeaways, summaries, or synthesis points
  - Example: "Återkommande programmeringsmönster: validera input, dict för räkning, läs-bearbeta-skriv"
- **example**: When the generalization is best shown through a code pattern
  - Example: The general pattern for file transformation (read-process-write)

**Anti-pattern**: Generalizations buried in prose paragraphs
```latex
% BAD: Important principle lost in prose
När vi arbetar med filer måste vi alltid öppna dem först,
sedan arbeta med innehållet, och till sist stänga dem.
Detta mönster återkommer i all filhantering.

\begin{example}[Läsa fil]
  ...
\end{example}
```

**Good pattern**: Generalization highlighted in semantic environment
```latex
% GOOD: Examples first, then generalization in environment
\begin{example}[Läsa fil]
  with open("data.txt", "r") as fil:
      innehåll = fil.read()
\end{example}

\begin{example}[Skriva fil]
  with open("data.txt", "w") as fil:
      fil.write(text)
\end{example}

\begin{remark}[Filhanteringsmönster]
  All filhantering följer mönstret: öppna → bearbeta → stäng.
  Funktionen \mintinline{python}{with} garanterar att filen stängs
  automatiskt även om fel uppstår.
\end{remark}
```

**Integration with variation theory**: The semantic environment containing the generalization represents the discernible **invariant pattern** that emerged from the **variation** in the examples. Students have experienced the pattern varying across different contexts (reading, writing, different file types) while the core structure remained invariant.

## Language Consistency When Documenting Variation Patterns

**CRITICAL**: When documenting variation theory in pedagogical notes (e.g., `\ltnote`), match the document's instructional language.

**Rule**: Write variation theory annotations in the same language as the student-facing content.

**Standard terminology translation examples (Swedish)**:
- "Variation Pattern" → "Variationsmönster"
- "Contrast" → "Kontrast"
- "Generalization" → "Generalisering"
- "Fusion" → "Fusion"
- "What varies" → "Vad som varierar"
- "What remains invariant" → "Vad som hålls invariant"
- "Critical aspects to discern" → "Kritiska aspekter att urskilja"
- "Learning Objectives" → "Lärandemål"
- "Why this variation works" → "Varför denna variation fungerar"

**Keeping English terms when appropriate**:
- Citations: "Following Marton & Pang (2006)..." → "Enligt Marton & Pang (2006)..."
- Technical terms without standard translations: use `\foreignlanguage{english}{term}`
- Code-related terms: naturally remain in English

**Example - Swedish documentation:**
```latex
\ltnote{%
  \textbf{Variationsmönster}: Kontrast

  \textbf{Vad som varierar}: Implementeringsmetod (dict-baserad vs klassbaserad)

  \textbf{Vad som hålls invariant}: Problemet (telefonbokshantering) och
  funktionaliteten

  \textbf{Kritiska aspekter att urskilja}: Genom att se samma problem
  löst både med och utan klasser kan studenter urskilja vad en klass ÄR
  kontra vad den INTE är.

  \textbf{Varför denna variation fungerar}: Enligt Marton \& Pang (2006)
  varierar vi implementeringsmetoden medan vi håller problemet invariant.
  Detta gör FÖRDELARNA med klasser urskiljbara eftersom studenter kan se
  EXAKT vad som förändras när man introducerar klasser.
}
```

**Example - English documentation:**
```latex
\ltnote{%
  \textbf{Variation Pattern}: Contrast

  \textbf{What varies}: Implementation approach (dict-based vs class-based)

  \textbf{What remains invariant}: The problem domain and functionality

  \textbf{Critical aspects to discern}: By seeing the same problem solved
  with and without classes, students can discern what a class IS versus
  what it is NOT.

  \textbf{Why this variation works}: Following Marton \& Pang (2006), we
  vary the implementation approach while keeping the problem invariant...
}
```

**Avoid mixing languages unnecessarily** - it creates cognitive load for instructors reviewing the pedagogical design.

## When Applying This Skill

- Identify the **object of learning** (what should be understood)
- Determine the **critical aspects** (what must be discerned)
- Structure content using the **four patterns** to create necessary conditions for learning
- Remember: "there is no discernment without variation" (Marton, 2015)

## Key References

- Marton, F. (2015). *Necessary Conditions of Learning*. Routledge. (Primary reference, especially Chapters 3, 5, and 6)
- Marton, F., & Booth, S. (1997). *Learning and Awareness*. Mahwah, NJ: Lawrence Erlbaum.
- Marton, F., & Pang, M. F. (2006). On Some Necessary Conditions of Learning. *Journal of the Learning Sciences*, 15(2), 193-220.
- Marton, F., & Tsui, A. (2004). *Classroom discourse and the space of learning*. Mahwah, NJ: Lawrence Erlbaum.

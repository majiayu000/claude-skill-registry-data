---
name: try-first-tell-later
description: Structure educational content using try-first-tell-later pedagogy where students predict, attempt, or reflect before receiving explanations. Creates active learning through cognitive engagement and variation theory's contrast patterns. Use when writing educational materials, designing exercises, creating lecture notes, structuring tutorials, writing teaching examples with LaTeX/Beamer, developing problem sets, or when user mentions try-first, predict-first, productive failure, Socratic method, question-before-answer, exercise-driven learning, or inquiry-based teaching.
---

# Try-First-Tell-Later Pedagogy

This skill applies the pedagogical principle of engaging learners' thinking **before** presenting information, creating active learning through anticipation, prediction, and problem-solving attempts.

## Core Principle

**Ask students to think, predict, or attempt solutions BEFORE providing the answer or explanation.**

This creates powerful learning through:
- **Double contrast**: Students contrast known approaches with new problems, then contrast their thinking with expert knowledge
- **Active engagement**: Learning happens through attempting, not just receiving
- **Metacognitive awareness**: Predicting and comparing reveals gaps in understanding
- **Productive failure**: Research shows attempting before instruction produces better learning than passive study

## The Teacher's Paradox and Assessment

### The Teacher's Paradox

Marton identifies a fundamental tension in teaching:

> "[T]he more the teacher does to enable the students to answer the questions asked, to solve the problems given, the fewer opportunities may be left for the students to learn to understand that which they are expected to learn to understand. The reason is that the more clearly the teacher tells the students what is to be done, the less chance the students get to make the necessary distinctions (for instance, between what is critical and what is not)." (NCOL, p. 13)

**Implication**: Try-first prompts should NOT reveal which aspects are critical. Students must discern this themselves.

### Try-First as Diagnostic Pre-Test

Try-first prompts serve a dual purpose:

1. **Learning function**: Engages prediction, activates prior knowledge, creates contrast
2. **Diagnostic function**: Reveals which critical aspects students can already discern

**Key insight** (Marton, NCOL p. 89):
> "If we want to find out to what extent they have learned to do so, we should not point out those aspects for them but let the students discern them by themselves."

**Use try-first prompts to diagnose**:
- Which critical aspects students already discern
- Which aspects need teaching (require variation patterns)
- Common misconceptions to address

### Designing Questions That Don't Reveal Critical Aspects

**BAD example** (Swedish national physics exam):
> "A ball falls and is affected by air braking force F = kv where k = 0.32 N·s/m. The ball's mass is 0.20 kg. What is the final velocity?"

**Problem**: All critical aspects are given. Students just calculate—no discernment needed.

**GOOD example** (Johansson, Marton, Svensson 1985):
> "A car is driven at a high constant speed on a motorway. What forces act on the car?"

**Why better**: Students must discern:
- That "constant speed" implies balanced forces
- Which forces are relevant
- That "engine pushes forward" alone is wrong

### Prompt Design Checklist

- [ ] Does my question require discerning critical aspects, or point them out?
- [ ] Could this serve as a pre-test to reveal student understanding?
- [ ] Am I avoiding giving away "what matters" in the question?
- [ ] Will responses reveal which critical aspects students see/miss?

### Connection to Variation Theory

Try-first prompts and variation theory work together:
1. **Try-first reveals** which critical aspects students cannot yet discern
2. **Variation patterns** then target those specific aspects
3. **Post-test try-first** confirms students now discern the aspects

See the variation-theory skill for designing appropriate patterns once diagnostic results are known.

## Quick Example

**Traditional "Tell-First" approach:**
```
Python uses the def keyword to define functions. Here's the syntax:

def function_name(parameters):
    # function body
    return result
```

**Try-First-Tell-Later approach:**
```
\begin{exercise}
  How would you create a reusable piece of code in Python that
  takes inputs and returns a result? What keyword might make sense?
  Think about it before continuing.
\end{exercise}

Python uses the def keyword to define functions...
[Then show syntax and compare with their thinking]
```

The second approach activates prior knowledge, creates cognitive engagement, and sets up contrast between their prediction and the actual syntax.

## Seven Implementation Patterns

Use different prompt types to engage students before providing explanations:

1. **Prediction Prompts**: "What do you think will happen if...?"
2. **Design/Solution Prompts**: "How would you...?" or "How could you implement...?"
3. **Conceptual Definition Prompts**: "What is...? Try to formulate your own definition before..."
4. **Reasoning Prompts**: "Why do you think...?" or "Varför tror du...?"
5. **Comparison Prompts**: "Jämför..." or "Which differences do you see...?"
6. **Reflection Prompts**: "Reflektera över..." or "What advantages/disadvantages do you see...?"
7. **Experimentation Prompts**: "Prova!" or "Write a program that..."

**For detailed implementation guidance, examples, and LaTeX/Beamer templates, see `references/patterns.md`.**

## Typical Flow

```
Context → Prompt to Try/Predict → [Student thinking] →
Explanation → Explicit contrast → Highlight critical aspects
```

## The Example-Question-Contrast Pattern

A powerful specific structure for organizing instructional sequences:

**Structure**:
1. **Show concrete example** illustrating a problem or scenario
2. **Pose try-first question** for students to predict/discover
3. **Show modified code/approach** demonstrating the solution
4. **Discuss the contrast** between approaches

**Example from file handling:**

```latex
% Step 1: Show problem example
\begin{frame}[fragile]
  \begin{example}[Manual file handling]
    \begin{minted}{python}
file = open("data.txt", "r")
content = file.read()
file.close()
    \end{minted}
  \end{example}
\end{frame}

% Step 2: Try-first question
\begin{frame}[fragile]
  \begin{exercise}
    What happens if an exception occurs between \mintinline{python}{open()}
    and \mintinline{python}{close()}? How can we guarantee the file is closed?
  \end{exercise}
\end{frame}

% Step 3: Show solution
\begin{frame}[fragile]
  \begin{example}[with statement]
    \begin{minted}{python}
with open("data.txt", "r") as file:
    content = file.read()
# file automatically closed here
    \end{minted}
  \end{example}
\end{frame}

% Step 4: Discuss contrast
\begin{frame}
  \begin{remark}
    The \mintinline{python}{with} statement guarantees resource cleanup
    even if exceptions occur. This implements the context manager protocol,
    ensuring \mintinline{python}{close()} is always called.
  \end{remark}
\end{frame}
```

**Why this works**:
- Students see the problem before being told there's a problem
- The question activates thinking about edge cases
- The solution is motivated by the discovered problem
- The contrast makes the value of `with` statement discernible

**Variation pattern**: The approach varies (manual vs with statement), the problem remains invariant, making resource management guarantees discernible.

## Guidelines for Effective Use

### When to Use Try-First Prompts

**Ideal situations**:
- Concepts students can partially reason about from prior knowledge
- Situations with intuitive but incorrect predictions
- Design decisions with multiple reasonable approaches
- Conventions or patterns with underlying rationale
- Comparisons where differences aren't immediately obvious

**Less suitable situations**:
- Completely novel concepts with no prior knowledge base
- Arbitrary facts with no logical derivation
- Situations where frustration would outweigh benefit

### Using Try-First for Diagnostic Assessment

**Before teaching a topic**:
1. Pose open-ended try-first question (without revealing critical aspects)
2. Analyze responses: which critical aspects do students mention?
3. Focus subsequent teaching on missing aspects using variation patterns

**Analyzing student responses**:
- Students who mention the critical aspect → ready for generalization/fusion
- Students who miss the critical aspect → need contrast patterns first
- Common wrong answers → reveal misconceptions to address

**After teaching** (post-test):
- Use same or similar prompt
- Compare responses to pre-test
- Students should now discern the critical aspects

**See `references/patterns.md` for detailed implementation guidance on diagnostic use.**

### Crafting Effective Discovery Questions

**Core principle**: Questions should guide students to discover what you would otherwise tell them.

**Question types by purpose**:

1. **Prediction questions**: "What could go wrong if...?"
   - Example: "What happens if we forget to close a file?"
   - Purpose: Activate thinking about edge cases and failure modes

2. **Comparison questions**: "When would approach A be better than B?"
   - Example: "When would `read()` be better than line-by-line iteration? Consider memory."
   - Purpose: Guide discrimination between similar approaches

3. **Design questions**: "How should X be implemented? Function or method? Why?"
   - Example: "How should `open()` be implemented? What should it return?"
   - Purpose: Engage architectural thinking before revealing design

4. **Exploration questions**: "What problems might arise with this approach?"
   - Example: "What problems could arise with comma-separated format?"
   - Purpose: Discover limitations through attempted use

**Quality criteria for discovery questions**:
- **Specific enough to guide thinking**: Not "What do you think?" but "What happens to original file if transformation fails?"
- **Open enough to allow discovery**: Multiple valid partial answers
- **Connected to upcoming content**: Answer will be provided soon
- **Build on prior knowledge**: Students have tools to partially answer

**Avoid**:
- Questions with obvious answers (wastes cognitive effort)
- Questions requiring knowledge students can't possibly have
- Prompts without clear follow-through explanation
- Too many prompts in succession (creates fatigue)

### Layered Question Sequences

Multiple questions can build on each other to scaffold discovery:

**Pattern**: Recognition → Exploration → Implementation → Understanding

**Example sequence for file operations**:

```latex
% Layer 1: Identify the problem
\begin{exercise}
  What extra steps are needed for files compared to \mintinline{python}{print()}
  and \mintinline{python}{input()}? The terminal is always available, but files...?
\end{exercise}

% Layer 2: Explore solutions
\begin{exercise}
  We need to "open" files. How can we guarantee they're closed properly,
  even if errors occur during processing?
\end{exercise}

% Layer 3: Show implementation
\begin{example}[with statement]
  with open("file.txt", "r") as f:
      content = f.read()
\end{example}

% Layer 4: Discuss why it works
\begin{remark}
  The \mintinline{python}{with} statement implements the context manager
  protocol, automatically calling \mintinline{python}{close()} even if
  exceptions occur.
\end{remark}
```

**Benefits of layering**:
- Scaffolds thinking from recognition → exploration → implementation → understanding
- Each question builds on previous without overwhelming
- Students construct understanding progressively
- Mirrors expert problem-solving process

### exercise vs activity Environments

**exercise environment**: Short conceptual questions requiring thought but not code execution

**Characteristics**:
- Quick to answer (1-2 minutes of thinking)
- Conceptual or analytical
- No coding required
- Activates prediction or reasoning

**Examples**:
```latex
\begin{exercise}
  Why might files require explicit open/close but terminal I/O doesn't?
\end{exercise}

\begin{exercise}
  What advantages does validating file existence BEFORE opening provide
  compared to catching exceptions AFTER?
\end{exercise}
```

**activity environment**: Hands-on tasks requiring actual coding or exploration

**Characteristics**:
- Takes substantial time (10+ minutes)
- Requires writing code or exploring tools
- Produces artifacts (programs, data files)
- Often followed by discussion of discoveries

**Examples**:
```latex
\begin{activity}[SCB Namnsök]
  Visit SCB Namnsök, download the statistics file, and write a program
  that implements the same functionality as the website.

  What challenges did you encounter with the file format?
\end{activity}

\begin{activity}[Explore CSV module]
  Try using Python's \mintinline{python}{csv} module to read and write
  a file with your own data. Compare with manual string splitting.
\end{activity}
```

**Guideline**: Use `exercise` for quick discovery moments embedded in instruction, `activity` for deeper exploration requiring implementation.

### The Critical Follow-Through

**Always**:
- Provide the explanation/answer after the prompt
- Explicitly acknowledge and contrast student thinking
- Validate correct intuitions while correcting misconceptions
- Show why the correct answer matters
- Make critical aspects visible through the contrast

**Never**:
- Ask questions without providing answers
- Skip the explanation assuming students "figured it out"
- Dismiss student predictions as simply wrong without explanation
- Fail to highlight what they should learn from the contrast

## Variation Theory Integration

This approach creates specific variation patterns:

**Student Attempt → Expert Explanation**
- Variant: The approach/understanding
- Invariant: The problem/concept
- Discernment: Critical aspects of expert approach vs. naive approach

**Prediction → Reality**
- Variant: Expected vs. actual behavior
- Invariant: The code/system/concept
- Discernment: Critical aspects that cause the actual behavior

**Multiple Student Approaches → Canonical Solution**
- Variant: Different solution strategies
- Invariant: The problem requirements
- Discernment: Critical aspects that make the canonical solution effective

**For detailed examples from actual teaching practice, including Python classes, operator overloading, and fraction arithmetic with LaTeX/Beamer code, see `references/examples.md`.**

## Key Principles Summary

1. **Always ask before telling** - Engage prediction/attempt before explanation
2. **Make thinking explicit** - Use phrases like "tänk igenom innan du fortsätter"
3. **Provide genuine answers** - Never leave prompts unresolved
4. **Highlight the contrast** - Explicitly compare prediction with reality
5. **Build on prior knowledge** - Ask questions students can partially answer
6. **Vary the prompt types** - Use prediction, design, reflection, comparison, etc.
7. **Connect to critical aspects** - Use the contrast to highlight what matters
8. **Create safe failure** - Frame attempts as learning opportunities, not tests

## Reference Files

This skill includes detailed references in `references/`:

| File | Content | Search patterns |
|------|---------|-----------------|
| `patterns.md` | Implementation guidance for all seven prompt types, LaTeX/Beamer templates | `exercise`, `activity`, `\begin{exercise}` |
| `examples.md` | Real examples from Python programming courses | `Python`, `class`, `fraction` |
| `theoretical-background.md` | Productive failure, retrieval practice, variation theory | `Kapur`, `Socratic`, `research` |

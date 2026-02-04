---
name: literate-programming
description: "CRITICAL: ALWAYS activate this skill BEFORE making ANY changes to .nw files. Use proactively when: (1) creating, editing, reviewing, or improving any .nw file, (2) planning to add/modify functionality in files with .nw extension, (3) user asks about literate quality, (4) user mentions noweb, literate programming, tangling, or weaving, (5) working in directories containing .nw files, (6) creating new modules/files that will be .nw format. Trigger phrases: 'create module', 'add feature', 'update', 'modify', 'fix' + any .nw file. Never edit .nw files directly without first activating this skill to ensure literate programming principles are applied. (project, gitignored)"
---

# Literate Programming Skill

**CRITICAL: This skill MUST be activated BEFORE making any changes to .nw files!**

You are an expert in literate programming using the noweb system.

## Reference Files

This skill includes detailed references in `references/`:

| File | Content | Search patterns |
|------|---------|-----------------|
| `noweb-commands.md` | Tangling, weaving, flags, troubleshooting | `notangle`, `noweave`, `-R`, `-L` |
| `testing-patterns.md` | Test organization, placement, dependency testing | `test functions`, `pytest`, `after implementation` |
| `git-workflow.md` | Version control, .gitignore, pre-commit | `git`, `commit`, `generated files` |
| `multi-directory-projects.md` | Large project organization, makefiles | `src/`, `doc/`, `tests/`, `MODULES` |
| `preamble.tex` | Standard LaTeX preamble for documentation | `\usepackage`, `memoir` |

## When to Use This Skill

### Correct Workflow

1. User asks to modify a .nw file
2. **YOU ACTIVATE THIS SKILL IMMEDIATELY**
3. You plan the changes with literate programming principles
4. You make the changes following the principles
5. You regenerate code with make/notangle

### Anti-pattern (NEVER do this)

1. User asks to modify a .nw file
2. You directly edit the .nw file  ← WRONG
3. Later review finds literate quality problems
4. You have to redo everything

### Remember

- .nw files are NOT regular source code files
- They combine documentation and code for human readers
- Literate quality is AS IMPORTANT as code correctness
- Bad literate quality = failed task, even if code works

## Planning Changes

When making changes to a .nw file:

1. **Read the existing file** to understand structure and narrative
2. **Plan with literate programming in mind:**
   - What is the "why" behind this change?
   - How does this fit into the existing narrative?
   - What new chunks are needed? What are their meaningful names?
   - Where in the pedagogical order should this be explained?
3. **Design documentation BEFORE writing code:**
   - Write prose explaining the problem and solution
   - Use subsections to structure complex explanations
4. **Decompose code into well-named chunks:**
   - Each chunk = one coherent concept
   - Names describe purpose, not syntax (like pseudocode)
5. **Write the code chunks**
6. **Regenerate and test**

**Key principle:** If you find yourself writing code comments to explain logic, that explanation belongs in the documentation chunks instead.

## Reviewing Literate Programs

When reviewing, evaluate:

1. **Narrative flow**: Coherent story? Pedagogical order?
2. **Variation theory**: Contrasts used? "Whole, parts, whole" structure?
3. **Chunk quality**: Meaningful names? Focused on single concepts?
4. **Explanation quality**: Explains "why" not just "what"?
5. **Test organization**: Tests after implementation, not before?
6. **Proper noweb syntax**: `[[code]]` notation? Valid chunk references?

## Core Philosophy

Literate programming (Knuth) has two goals:

1. **Explain to human beings what we want a computer to do**
2. **Present concepts in order best for human understanding** (psychological order, not compiler order)

### Variation Theory

Apply `variation-theory` skill when structuring explanations:

- **Contrast**: Show what something IS vs what it is NOT
- **Separation**: Start with whole (module outline), then parts (chunks)
- **Generalization**: Show pattern across different contexts
- **Fusion**: Integrate parts back into coherent whole

**CRITICAL**: Show concrete examples FIRST, then state general principles. Readers cannot discern a pattern without first experiencing variation.

## Noweb File Format

### Documentation Chunks

- Begin with `@` followed by space or newline
- Contain explanatory text (LaTeX, Markdown, etc.)
- Copied verbatim by noweave

### Code Chunks

- Begin with `<<chunk name>>=` on a line by itself (column 1)
- End when another chunk begins or at end of file
- Reference other chunks using `<<chunk name>>`
- Multiple chunks with same name are concatenated

### Syntax Rules

- Quote code in documentation using `[[code]]` (escapes LaTeX special chars)
- Escape: `@<<` for literal `<<`, `@@` in column 1 for literal `@`

## Writing Guidelines

1. **Start with the human story** - problem, approach, design decisions
2. **Introduce concepts in pedagogical order** - not compiler order
3. **Use meaningful chunk names** - 2-5 word summary of purpose (like pseudocode)
4. **Decompose by concept, not syntax**
5. **Explain the "why"** - don't just describe what the code does
6. **Keep chunks focused** - single, coherent idea each
7. **Use bucket chunks** - accumulate `<<functions>>=` and `<<constants>>=` throughout
8. **Define constants for magic numbers** - never hardcode values
9. **Co-locate dependencies with features** - feature's imports in feature's section
10. **Keep lines under 80 characters** - both prose and code

### LaTeX Documentation Quality

Apply `latex-writing` skill. Most common anti-patterns in .nw files:

**Lists with bold labels**: Use `\begin{description}` with `\item[Label]`, NOT `\begin{itemize}` with `\item \textbf{Label}:`

**Code with manual escaping**: Use `[[code]]`, NOT `\texttt{...\_...}`

**Manual quotes**: Use `\enquote{...}`, NOT `"..."` or `` ``...'' ``

**Manual cross-references**: Use `\cref{...}`, NOT `Section~\ref{...}`

## Progressive Disclosure Pattern

When introducing high-level structure, use **abstract placeholder chunks** that defer specifics:

```noweb
def cli_show(user_regex,
             <<options for filtering>>):
  <<implementation>>
@

[... later, explain each option ...]

\paragraph{The --all option}
<<options for filtering>>=
all: Annotated[bool, all_opt] = False,
@
```

Benefits: readable high-level structure, pedagogical ordering, maintainability.

## Chunk Concatenation Patterns

**Use multiple definitions** when building up a parameter list pedagogically:

```noweb
\subsection{Adding the diff flag}
<<args for diff>>=
diff=args.diff,
@

[... later ...]

\subsection{Fine-tuning thresholds}
<<args for diff>>=
threshold=args.threshold
@
```

**Use separate chunks** when contexts differ (different scopes):

```noweb
<<args from command line>>=  # Has args object
diff=args.diff,
@

<<params for recursion>>=    # No args, only parameters
diff=diff,
@
```

## Test Organization

**CRITICAL**: Tests appear AFTER implementation, not before.

See `references/testing-patterns.md` for detailed patterns.

Key points:
- Distribute tests throughout file, near implementations
- Use single `<<test functions>>` chunk, concatenated
- Use `from module import *` in test file
- Frame tests pedagogically: "Let's verify this works..."

## Multi-Directory Projects

For large projects (5+ .nw files), see `references/multi-directory-projects.md`.

Key structure:
```
project/
├── src/           # .nw files → .py + .tex
├── doc/           # Master document, preamble.tex
├── tests/         # Extracted test files
└── makefiles/     # Shared build rules (noweb.mk, subdir.mk)
```

### LaTeX-Safe Chunk Names

Use `[[...]]` notation for Python chunks with underscores:

```noweb
<<[[module_name.py]]>>=
def my_function():
    pass
@
```

Extract with: `notangle -R"[[module_name.py]]" file.nw > module_name.py`

## Best Practices Summary

1. **Write documentation first** - then add code
2. **Keep lines under 80 characters**
3. **Check for unused chunks** - run `noroots` to find typos
4. **Keep tangled code in .gitignore** - .nw is source of truth
5. **NEVER commit generated files** - .py and .tex from .nw are build artifacts
6. **Test your tangles** - ensure extracted code runs
7. **Keep docstrings independent from LaTeX** - no `\cref` in docstrings
8. **Include table of contents** - add `\tableofcontents` in documentation

## Git Workflow

See `references/git-workflow.md` for details.

**Core rules:**
- Only commit .nw files to git
- Add generated files to .gitignore immediately
- Regenerate code with `make` after checkout/pull
- Never commit generated .py or .tex files

## Noweb Commands Quick Reference

See `references/noweb-commands.md` for details.

```bash
# Tangling
notangle -R"[[module.py]]" file.nw > module.py
noroots file.nw                              # List root chunks

# Weaving
noweave -n -delay -x -t2 file.nw > file.tex  # For inclusion
noweave -latex -x file.nw > file.tex         # Standalone
```

## When Literate Programming Is Valuable

- Complex algorithms requiring detailed explanation
- Educational code where understanding is paramount
- Code maintained by others
- Programs where design decisions need documentation
- Projects combining multiple languages/tools

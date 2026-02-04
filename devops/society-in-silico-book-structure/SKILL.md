---
name: Society in Silico Book Structure
description: Auto-activates when navigating or organizing the manuscript. Knows the book's structure, chapter organization, and file conventions.
---

# Book Structure

## Repository Layout

```
society-in-silico/
├── manuscript/              # The book itself
│   ├── front-matter/        # Introduction, preface
│   ├── part-1-origins/      # History of microsimulation
│   ├── part-2-building/     # PolicyEngine journey
│   └── part-3-future/       # AI and what's next
├── research/                # Background research
│   ├── people/              # Key figures
│   ├── concepts/            # Technical concepts
│   ├── timeline/            # Chronology
│   └── references/          # Sources
├── assets/                  # Images, diagrams
└── build/                   # Compilation (Pandoc)
```

## Book Outline

### Part I: Origins
The intellectual history of microsimulation.
- Guy Orcutt's 1957 vision
- DYNASIM and early mainframe models
- IFS TAXBEN and institutional microsimulation
- NBER TAXSIM
- The closed-model era

### Part II: Building
The open-source turn and PolicyEngine journey.
- OpenFisca and rules-as-code
- Tax-Calculator as gateway
- Founding PolicyEngine with Nikhil
- UK expansion
- US expansion
- The messy reality of encoding law

### Part III: Future
AI implications and what's next.
- LLM limitations (67% accuracy finding)
- Why deterministic tools matter more
- Agents need reliable infrastructure
- Cosilico thesis
- Democratic vs. autocratic simulation
- The choice being made now

## File Conventions

### Manuscript Files
- Named: `NN-title.md` (e.g., `01-introduction.md`)
- Start with `# Chapter Title`
- Use `## Section` headers
- Wiki-links to research: `[[concept-name]]`

### Research Notes
- Named: `kebab-case.md`
- Have metadata section at top
- End with `## Links` and `## Tags`

### Chapter Template
```markdown
# Chapter Title

[Opening hook - story, question, or surprising fact]

## Section One

[Content with [[wiki-links]] to research]

## Section Two

[More content]

---

## Research Links

- [[relevant-concept]]
- [[relevant-person]]
```

## Navigation Commands

When asked about the book:
- "Where does X fit?" → Check outline above
- "What's in Part II?" → Building section
- "Show chapter structure" → List files in manuscript/

## Current Status

Check `.beads/` for project issues and progress tracking.
Use `bd list` to see open items.
Use `bd ready` to see what's ready to work on.

## Key Relationships

- Introduction sets up Rehoboam/Serac contrast
- Part I establishes what microsimulation IS
- Part II shows how it became OPEN
- Part III shows what's NEXT (with Cosilico launch)
- Ending returns to Serac: "What if Rehoboam were open source?"

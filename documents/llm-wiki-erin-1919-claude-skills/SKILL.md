---
name: llm-wiki
description: Bootstrap and maintain an LLM-generated wiki knowledge base in a project, following the llm-wiki pattern (persistent, compounding, interlinked markdown wiki compiled from raw sources — not RAG). Use when the user asks to "create a wiki" for a project, points at an llm-wiki.md idea file, wants a knowledge base built from papers/documents in a folder, or wants /ingest /lint /query /meeting wiki commands set up in a new project.
---

# LLM Wiki

Instantiate a persistent, LLM-maintained wiki in a project: schema in CLAUDE.md, `wiki/` directory of interlinked markdown pages compiled from immutable raw sources, and `/ingest`, `/lint`, `/query`, `/meeting` slash commands for ongoing maintenance.

Core idea (from the llm-wiki pattern; the original idea file is at `references/llm-wiki-pattern.md`): knowledge is **compiled once and kept current**, not re-derived per query. Sources get read fully at ingest time; insights are integrated into an interlinked page network; contradictions are flagged, not overwritten; answers to good questions get filed back as pages. The wiki compounds.

## Bootstrap Workflow

### 1. Establish the ground truth

- Identify the **raw sources directory** (e.g. `paper/`, `ref/`, `docs/raw/`). It is immutable — the wiki reads from it, never modifies it.
- Identify the **project purpose** (what the wiki is *for* — e.g. "understand X before implementing it"). This determines what the "Relevance to Project" sections and `wiki/project/` pages focus on. Ask the user if unclear.
- If the user has another project with an existing wiki, read its `CLAUDE.md` and a sample source page first and reuse those conventions — consistency across the user's projects beats novelty.

### 2. Write the schema into CLAUDE.md

Add a "Wiki Knowledge Base" section to the project's `CLAUDE.md` (create the file if needed). Copy the structure from `assets/claude-md-section.md`, adapting: raw-source directory name, project purpose line, and any project-specific rules. The schema must cover: directory structure, page conventions (frontmatter, wikilinks, kebab-case), the ingest/query/lint workflows, and the rules (immutability, index+log discipline, absolute dates, flag-don't-overwrite, cross-reference generously).

### 3. Create the wiki skeleton

```
wiki/
├── index.md      # master catalog by category (Meta / Sources / Concepts / Entities / Synthesis / Project)
├── log.md        # append-only; entries: ## [YYYY-MM-DD] operation | Subject
├── overview.md   # evolving synthesis; revise after each ingest batch
├── sources/      # one page per ingested source
├── concepts/     # one page per key concept
├── entities/     # one page per concrete system/tool/standard/dataset
├── synthesis/    # cross-cutting analyses
└── project/      # this project's design decisions and open questions
```

Page conventions: see `references/page-templates.md` for the source-page template and frontmatter requirements. All pages: YAML frontmatter (title, type, tags), Obsidian `[[wikilinks]]`, kebab-case filenames.

### 4. Ingest the initial sources (parallel)

For the initial batch, dispatch **one background agent per source** in a single message. Each agent: reads the source fully, writes the source page directly, and returns a **maintainer digest** (TL;DR, concept-page candidates, entity candidates, numbers worth preserving, flags/contradictions). Prompt requirements for each agent are in `references/page-templates.md` — include the exact page format, the list of likely wikilink targets (so agents converge on shared link vocabulary), and the names of the other sources being ingested (so they cross-link each other).

PDF note: if the Read tool cannot render PDFs (no poppler), extract text with pypdf to the scratchpad and point agents at the text file:
```python
from pypdf import PdfReader
r = PdfReader(path)
# write pages with '=== PDF PAGE N ===' markers
```

### 5. Write the cross-cutting pages yourself

Do NOT delegate these — they require seeing all digests together:

- **Concept/entity pages**: one per candidate that at least one source treats substantively. Merge near-duplicates; small focused pages beat sprawling ones. Minor comparison systems can share one catalog page (e.g. `alternative-X`).
- **Synthesis pages**: at minimum a lineage/positioning page (how the sources relate) and any gap/conformance analysis the project purpose implies.
- **Project pages**: `design-decisions.md` (decisions with options, trade-off tables, status: open/leaning/decided) and `open-questions.md` (ranked by how much they block the project).
- **overview.md, index.md, log.md**: overview is a synthesis with a "last revised" line and a suggested reading spine; index gets one line + hook per page; log records the bootstrap and each ingest with flags.

### 6. Lint before delivering

Run the link check (from the wiki directory):

```bash
grep -rhoE '\[\[[^]|]+' --include='*.md' . | sed 's/\[\[//' | sort -u > /tmp/links.txt
find . -name '*.md' -printf '%f\n' | sed 's/\.md$//' | sort -u > /tmp/pages.txt
comm -23 /tmp/links.txt /tmp/pages.txt   # unresolved links
comm -13 /tmp/links.txt /tmp/pages.txt   # orphan pages
```

- **Normalize synonym links** (two names for one concept): pick a canonical page, rewrite the others as `[[canonical|display text]]`. Obsidian does NOT auto-resolve aliases — the link target must match a filename.
- Redirect resolvable links to existing pages; leave genuinely-future topics as intentional red links, **recorded in log.md** so future lints can tell them from breakage.
- Zero orphan pages is the bar.

### 7. Install the slash commands

Copy the command templates from `assets/commands/` into the project's `.claude/commands/`, replacing the `{{RAW_DIR}}`, `{{PROJECT_FOCUS}}`, and `{{PROJECT_DOC}}` placeholders and adapting the project-specific page references (which project/synthesis pages an ingest should check). The core three are `ingest.md`, `lint.md`, `query.md`; also install `meeting.md` if the project keeps meeting notes (a `meeting_notes/` directory, or the user mentions weekly meetings) — `{{PROJECT_DOC}}` is the project's main design/proposal document that the meeting ritual may revise. If the project is not a git repo, the commands' commit steps are already conditional — but suggest `git init` to the user for wiki version history.

### 8. Report

Final message: page counts by category, lint status (all links resolve / N intentional red links), **flags surfaced by ingestion agents** (contradictions, ambiguities, surprises — these need user attention per the pattern's hybrid mode), and suggested next steps (open design decisions, sources worth finding).

## Ongoing Maintenance

After bootstrap, the slash commands carry the workflow: `/ingest <file>` (one source at a time, hybrid mode — flag surprises before propagating), `/query <question>` (index-first, cited synthesis, offer to file valuable answers), `/lint` (full health check, report before fixing); and, for projects with meeting notes, `/meeting <file>` (triage a meeting note into source/concept/project pages, attribute by date, and flag project-doc revisions and milestone tags). Their canonical text lives in `assets/commands/`.

Rules that must survive every operation: never modify raw sources; always update index.md and log.md; absolute dates in logs; flag contradictions instead of overwriting; cross-reference generously.

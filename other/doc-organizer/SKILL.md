---
name: doc-organizer
description: "Scan repos in ~/Desktop/Dev/repos for markdown and HTML documentation, classify each file as repo-local (stays in place) or centralizable content (guides, courses, articles), then generate an inventory and optionally consolidate content docs into the centralized docs repo. Use when documentation is scattered and needs organizing."
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Agent
---

Organize documentation across: $ARGUMENTS

$ARGUMENTS should include:
- A scope — which repos to scan (default: all repos under `~/Desktop/Dev/repos/`)
- Optionally: `--inventory-only` to skip consolidation and just produce a report
- Optionally: `--dry-run` to show what would be moved without moving anything
- Optionally: a target directory for centralized content (default: `~/Desktop/Dev/repos/docs/`)
- Optionally: specific file types to include (default: `.md` and `.html`)
- Empty — scan everything, ask the user before taking action

---

## Purpose

Repos accumulate documentation over time. Some of it is **repo-local** — tightly coupled to the codebase and must stay where it is. Some of it is **content** — guides, courses, articles, framework explanations, voice references — that could live in a centralized location where it's discoverable and maintainable.

This skill draws that line, produces a clear inventory, and (with the user's approval) consolidates content docs into a single hub.

---

## Classification System

Every `.md` and `.html` file falls into one of two categories:

### Category A — Repo-Local (STAYS)

These documents are coupled to the code, infrastructure, or development workflow. Moving them would break references or lose context.

**Path-based signals (high confidence):**
- Inside `.claude/`, `.agents/`, `.github/`, `.vscode/`, `.cursor/`
- Inside `node_modules/`, `dist/`, `.next/`, `build/`, `out/`, `.turbo/`
- Inside `_docs/platform/`, `_docs/design/`, `_docs/type/`, `_docs/ui/`
- Inside `_docs/agents/` (agent configuration, not agent-generated content)
- Inside `_docs/architecture/` (app-architect output — implementation specs)
- Inside `_prompts/` or `_bootstrap/`

**Filename-based signals (high confidence):**
- `README.md`, `CONTRIBUTING.md`, `CHANGELOG.md`, `LICENSE.md`, `CODE_OF_CONDUCT.md`
- `CLAUDE.md`, `AGENTS.md`, any file starting with `_` (convention for internal docs)
- `package.json`-adjacent docs (e.g., `MIGRATION.md`, `UPGRADE.md`)
- Files matching: `*SCHEMA*`, `*API*`, `*VALIDATION*`, `*INVENTORY*`, `*STATUS*`
- Files matching: `*IMPLEMENTATION*`, `*BOOTSTRAP*`, `*PROMPT*`, `*CONFIG*`

**Content-based signals (use when path/filename are ambiguous):**
- References specific code files, functions, or imports
- Contains schema definitions, type annotations, or API endpoint documentation
- Contains checklists tied to build/deploy steps
- Contains component inventories or page route tables
- Contains environment variable documentation
- Written for developers as the primary audience

### Category B — Centralizable Content (MOVES)

These documents are **content assets** — they teach, explain, narrate, or guide. They're valuable independent of any single codebase.

**Path-based signals (high confidence):**
- Inside directories named: `content/`, `articles/`, `guides/`, `courses/`, `pathways/`
- Inside directories named: `voice/`, `writing/`, `corpus/`, `lab/`, `knowledge/`
- Inside `_docs/` but not in platform/design/type/agents/architecture subdirectories

**Filename-based signals (high confidence):**
- Files matching: `*PLAYBOOK*`, `*GUIDE*`, `*COURSE*`, `*ARTICLE*`
- Files matching: `*VOICE*`, `*FRAMEWORK*`, `*MANIFESTO*`
- Files matching: `*TEACHING*`, `*FORMATION*`, `*PEDAGOGY*`
- Files containing version/chapter numbers (e.g., `week-01.md`, `chapter-3.md`)

**Content-based signals (use when path/filename are ambiguous):**
- Narrative prose (paragraphs, not bullet checklists)
- Pedagogical structure (dissonance → action → reflection)
- Framework explanations (mDNA, APEST, Forgotten Ways, etc.)
- Case studies, stories, illustrations
- Written for learners, readers, or a general audience
- Contains no code references, schema definitions, or API documentation
- Could be published on a blog, in a course, or as a standalone document

### Category C — Bridging Documents (FLAG FOR REVIEW)

Some files serve both purposes. Flag these for the user to decide.

**Signals:**
- Agent prompts that generate content (in `_prompts/` but about content strategy)
- Design consultations that contain both specs and narrative (e.g., `COPY_CONSULTATION.html`)
- Inventories that mix content assets with technical components
- Vector store source material (agent-consumed but content in nature)

---

## Execution Process

### Phase 1 — Discovery

1. **List all repos** under the scan scope
2. **Glob for documentation files** in each repo:
   - `**/*.md` (excluding `node_modules/`, `dist/`, `.next/`, `build/`, `.turbo/`)
   - `**/*.html` (excluding `node_modules/`, `dist/`, `.next/`, `build/`, `.turbo/`)
3. **Exclude known noise:**
   - Lock files, generated changelogs, auto-generated API docs
   - Build output directories
   - Dependency directories

### Phase 2 — Classification

For each file:

1. **Apply path-based rules first** (highest confidence, cheapest to evaluate)
2. **Apply filename-based rules** (high confidence)
3. **If still ambiguous, read the first 50 lines** and apply content-based rules
4. **Assign a classification:**
   - `REPO-LOCAL` — stays in place
   - `CONTENT` — candidate for centralization
   - `REVIEW` — needs human decision
5. **Assign a content type** (for CONTENT files):
   - `guide` — how-to, tutorial, walkthrough
   - `article` — blog post, essay, thought piece
   - `course` — course material, lesson, module
   - `framework` — conceptual framework documentation
   - `voice` — voice system, writing style, tone reference
   - `research` — research notes, content research, interviews
   - `template` — HTML template, design prototype (for `.html` files)
   - `reference` — reference material, glossary, definitions
   - `other` — doesn't fit the above

### Phase 3 — Inventory Report

Generate a comprehensive inventory. Output as a markdown file at `{{OUTPUT_DIR}}/DOC_INVENTORY.md`:

```markdown
# Documentation Inventory

**Scanned:** [date]
**Scope:** [repos scanned]
**Total files:** [count]

## Summary

| Category | Count | Percentage |
|----------|-------|------------|
| Repo-Local | [n] | [%] |
| Content (Centralizable) | [n] | [%] |
| Needs Review | [n] | [%] |

## Content Files by Type

| Type | Count | Repos Found In |
|------|-------|----------------|
| guide | [n] | [repo1, repo2] |
| article | [n] | [repo1] |
| course | [n] | [repo1, repo3] |
| ... | ... | ... |

## Content Files — Full List

### [Repo Name]

| File | Type | Confidence | Notes |
|------|------|------------|-------|
| `path/to/file.md` | guide | high | [brief note] |
| `path/to/file.md` | article | medium | [brief note] |

### [Next Repo]
...

## Needs Review

| File | Reason |
|------|--------|
| `path/to/file.md` | Bridges content and technical docs |
| `path/to/file.html` | Design consultation with narrative content |

## Repo-Local Files (Summary Only)

| Repo | Count | Key Directories |
|------|-------|-----------------|
| [repo] | [n] | `_docs/platform/`, `_docs/design/` |
```

### Phase 4 — Consolidation Plan

If not `--inventory-only`, generate a consolidation plan:

1. **Map content files to target locations** in the centralized docs repo
2. **Organize by content type**, then by source topic/pillar:
   ```
   docs/
   ├── articles/
   │   ├── [pillar-or-topic]/
   │   │   └── [article-slug].md
   ├── courses/
   │   ├── [course-name]/
   │   │   ├── week-01.md
   │   │   └── ...
   ├── guides/
   │   └── [guide-slug].md
   ├── frameworks/
   │   └── [framework-name].md
   ├── voice/
   │   └── [voice-system].md
   ├── research/
   │   └── [topic]/
   ├── templates/
   │   └── [template-name].html
   └── reference/
       └── [topic].md
   ```
3. **Preserve provenance** — add a YAML frontmatter block to each moved file:
   ```yaml
   ---
   source_repo: [repo-name]
   source_path: [original/path/in/repo]
   consolidated_date: [YYYY-MM-DD]
   content_type: [type]
   ---
   ```
4. **Leave a breadcrumb** in the source repo — replace the original file with a pointer:
   ```markdown
   <!-- This document has been consolidated into the central docs repo -->
   <!-- See: docs/[type]/[path] -->
   <!-- Consolidated on: [YYYY-MM-DD] -->
   ```

### Phase 5 — Execute (with confirmation)

**CRITICAL: Always ask the user before moving any files.**

Present the consolidation plan as a summary table:

```
## Consolidation Plan

Moving [n] files from [n] repos → [target repo]

| Source | Destination | Type |
|--------|-------------|------|
| alan-hirsch/_docs/PLAYBOOK.md | docs/courses/playbook.md | course |
| ... | ... | ... |

Proceed? (y/n)
```

If `--dry-run`, stop here and output the plan without executing.

If the user confirms:
1. Create target directories as needed
2. Copy files to target locations (copy first, don't move — safer)
3. Add provenance frontmatter to copied files
4. Replace originals with breadcrumb pointers
5. Report results

---

## Rules

- **Never move files without explicit user confirmation** — even if the classification is high-confidence
- **Never touch `node_modules/`, `dist/`, `.next/`, or build directories** — skip them entirely during discovery
- **Never modify repo-local files** — the skill only reads them for classification
- **Always preserve originals** — copy to target, then replace with pointer (two separate steps)
- **When in doubt, classify as REVIEW** — false negatives (missing content) are better than false positives (moving technical docs)
- **Read before classifying** — if path and filename rules don't give high confidence, read the file. Don't guess.
- **Respect `.gitignore`** — don't scan or move gitignored files
- **Handle HTML carefully** — many HTML files are design prototypes or build output, not content. Apply stricter classification for `.html` files.
- **Track what you've done** — append a log entry to `{{OUTPUT_DIR}}/DOC_ORGANIZER_LOG.md` after each run

---

## Edge Cases

### Skill files (my-skills/)
Skills are **repo-local** — they are code-adjacent tooling, not content to centralize. Always classify as `REPO-LOCAL`.

### Vector store content
Files in `_docs/agents/writing_assistant/vector_store/` are **REVIEW** — they contain content but are consumed by agents in the source repo. Flag for user decision.

### HTML prototypes
HTML files in `html/` or `templates/` directories should be classified as `template` content type but only moved if they are standalone (not referenced by other files in the repo). Check for import/reference before classifying.

### Already-centralized content
If a file already exists in the target docs repo, **do not duplicate it**. Instead, note it as "already centralized" in the inventory and check if the source copy is newer (potential sync issue to flag).

### Monorepo docs directories
Some repos have a top-level `docs/` that contains both technical docs and content. Classify each file individually — don't classify the entire directory.

---

## Anti-Patterns

- **Don't bulk-move without reading.** Every file that isn't obviously classified by path/filename needs to be read.
- **Don't create deep nesting.** The target structure should be flat within each content type — max 2 levels deep.
- **Don't rename files during consolidation.** Keep original filenames unless they conflict. If they conflict, prefix with the source repo name.
- **Don't consolidate actively-edited files.** If a file has been modified in the last 7 days (check git log), flag it as `REVIEW` regardless of classification.
- **Don't ignore `.html` files.** Many contain valuable content (consultations, rendered guides). Classify them the same way as markdown.
- **Don't treat all `_docs/` content as repo-local.** The `_docs/` convention is used for both technical docs and content docs — always check the subdirectory and file content.

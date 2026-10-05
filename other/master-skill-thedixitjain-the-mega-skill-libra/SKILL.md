---
name: master-skill-library
description: >-
  Router for a local library of 35,802 agent skills, subagents, slash commands,
  system prompts and rules files harvested from 186 top GitHub repositories.
  Use whenever a task might already have a purpose-built skill - coding, review,
  testing, security, devops, design, data, RAG, writing, docs, product, marketing,
  business, research, media, mobile or productivity. Search CATALOG.tsv first,
  then read only the matching file.
---

# Master Skill Library - Router

A local, offline library of **35,802 reusable agent assets** from **186 repositories**.

Nothing here loads into context automatically. You **search the catalog**, then
**read only the one or two files** you actually need.

## Library root

The library root is wherever you cloned/copied this repo
(`the-mega-skill-library`, github.com/thedixitjain/the-mega-skill-library).
All paths below are relative to that root — resolve them from `CATALOG.tsv`'s
own location, not from wherever this router skill happens to be installed.

## Step 1 - search the catalog

`CATALOG.tsv` is tab-separated, one row per asset:

```
kind <TAB> category <TAB> name <TAB> path <TAB> source_repo <TAB> description
```

Use the Grep tool on `CATALOG.tsv` with the user's task keywords. Shell equivalents:

```bash
grep -i "<keyword>" CATALOG.tsv | head -30                      # anywhere
grep -i "<keyword>" CATALOG.tsv | awk -F'\t' '$1=="skill"'      # only Agent Skills
awk -F'\t' '$2=="security-and-compliance"' CATALOG.tsv          # whole category
```

## Step 2 - read the matching asset

Column 4 is the path relative to this library root. Read that file.
For an Agent Skill, sibling files in the same directory (scripts, references,
templates) are part of the bundle and may be read or executed.

## Step 3 - apply it

Follow the loaded file's instructions as if the skill had been invoked directly.
When several candidates match, prefer the one whose `source_repo` is an official
vendor: `anthropics/`, `openai/`, `google/`, `microsoft/`, `github/`,
`vercel-labs/`, `android/`, `trailofbits/`, `modelcontextprotocol/`.

## Asset kinds

| Kind | Path pattern | What it is |
|---|---|---|
| `skill` | `library/<category>/<slug>/SKILL.md` | Full Agent Skill bundle (18,681) |
| `agent` | `agents/<category>/<slug>.md` | Subagent definition (2,888) |
| `command` | `commands/<category>/<slug>.md` | Slash-command prompt (2,773) |
| `prompt` | `prompts/<category>/<slug>.md` | System prompt / prompt corpus (10,074) |
| `rules` | `rules/<category>/<slug>.md` | CLAUDE.md / AGENTS.md / .cursorrules (1,386) |

Plus `reference/<owner~repo>/...` - 543 verbatim awesome-lists,
cheatsheets and handbooks, greppable but not skill-shaped.

## Categories

- **`general-purpose`** — 5,575 — Uncategorized / cross-cutting
- **`ai-agents-and-harness`** — 4,583 — Agent design, orchestration, subagents, harness tuning, context engineering
- **`prompt-engineering`** — 2,868 — Prompt techniques, system prompts, optimizers, persona design
- **`engineering-core`** — 2,805 — Refactoring, debugging, review, architecture, git, spec-driven dev, TDD
- **`research-and-academic`** — 2,483 — Literature review, papers, journals, grants, regulatory science
- **`devops-and-infra`** — 1,605 — Docker, K8s, Terraform, CI/CD, cloud, observability, SRE
- **`security-and-compliance`** — 1,604 — AppSec, pentest, OSINT, threat modeling, SOC2/ISO/GDPR compliance
- **`marketing-and-growth`** — 1,584 — SEO/AEO, ads, CRO, social, campaigns, growth loops
- **`backend-and-data`** — 1,583 — APIs, databases, schemas, queues, caching, data pipelines
- **`mcp-and-integrations`** — 1,524 — MCP servers/clients, third-party integrations, browser automation
- **`testing-and-qa`** — 1,506 — Test generation, E2E, coverage, QA process, browser testing
- **`frontend-and-design`** — 1,359 — UI/UX, design systems, CSS, React, accessibility, visual polish
- **`writing-and-content`** — 1,345 — Copywriting, editing, humanizing, translation, narrative
- **`docs-and-knowledge-mgmt`** — 1,158 — Documentation, ADRs, technical writing, Obsidian, note systems
- **`business-and-finance`** — 1,152 — Finance, pricing, legal, sales, HR, exec/C-suite advisory
- **`media-and-creative`** — 778 — Video, image, slides/PPTX, audio, game dev, generative art
- **`data-science-and-ml`** — 722 — ML/DL, training, fine-tuning, evaluation, statistics, notebooks
- **`product-and-pm`** — 473 — PRDs, roadmaps, user stories, discovery, product analytics
- **`mobile-and-platform`** — 398 — iOS/Android/Flutter, desktop, extensions, Office/BI platforms
- **`productivity-and-workflow`** — 353 — Planning, automation, meetings, organization, scaffolds, coaching
- **`rag-memory-knowledge`** — 333 — RAG, vector search, embeddings, agent memory, knowledge graphs
- **`skill-authoring-meta`** — 11 — Creating, testing, auditing and improving skills themselves

## Provenance

Every generated file carries `source_repo`, `source_path` and `source_url` in its
frontmatter plus a Source footer identifying which upstream repo it came from.

---
name: docs-to-skills
description: "Turn documentation sites or trees into complete, source-linked skills with topic routing and on-demand references."
license: MIT
---

# Documentation → Agent Skills

End-to-end workflow: **crawl an entire documentation site (or doc tree)**, extract structured knowledge, and emit a **family of progressive-disclosure skills** optimized for efficient, compartmentalized reading.

**Always load `skill-authoring` before writing any SKILL.md.** Completeness of the crawl is non-negotiable.

## Non-negotiable rules

1. **Work through all documentation** — build a full page inventory first; process every in-scope page; never cherry-pick only the homepage.
2. **Compartmentalize** — prefer multi-skill families + `references/` over one mega-skill.
3. **Progressive disclosure** — lean `SKILL.md` (&lt;200 lines preferred, &lt;500 hard); detail one level deep in `references/`.
4. **Source-faithful** — distinguish official docs facts from agent inference; record source URLs.
5. **Discoverable descriptions** — third person, WHAT + WHEN + trigger terms (see `skill-authoring`).

## When to use

- User provides a docs URL (GitBook, Docusaurus, Mintlify, ReadTheDocs, custom).
- User wants skills for a protocol/library already documented upstream.
- User wants to refresh skills after a docs version bump.

## Pipeline overview (checklist — copy and complete)

```
Docs→Skills Progress:
- [ ] 0. Scope & constraints (URL, version, license, output path)
- [ ] 1. Discover navigation graph (sitemap / TOC / sidebar / llms.txt)
- [ ] 2. Build complete page inventory (URL + title + section path)
- [ ] 3. Fetch every in-scope page; normalize to markdown notes
- [ ] 4. Coverage audit (0 missing; orphans listed)
- [ ] 5. Cluster into skill family plan (names + ownership boundaries)
- [ ] 6. Draft each skill (frontmatter + lean body + references)
- [ ] 7. Cross-link See also; align terminology
- [ ] 8. Quality checklist (skill-authoring) per skill
- [ ] 9. Emit COVERAGE.md / SOURCES.md for the family
- [ ] 10. Install paths (Crane/IndexedEx/projects-defi as required)
```

Do not mark complete while any inventory page is `pending` or `failed` without an explicit waiver.

## Phase 0 — Scope

Capture before crawling:

| Field | Example |
|-------|---------|
| Root URL | `https://docs.example.com/` |
| Version / branch | `v3`, `main` |
| In-scope paths | `/protocol/**`, `/sdk/**` |
| Out of scope | `/blog/**`, `/changelog/**` (or include if user wants) |
| Output root | `.claude/skills/` (or temp then install) |
| Family prefix | `morpho-`, `ajna-`, … |
| License note | Can we quote docs? Prefer paraphrase + link |

If the site is huge, still inventory everything in-scope; batch writing by cluster, but **do not skip inventory**.

## Phase 1 — Discover the full graph

Use every available discovery channel (in order):

1. **`/sitemap.xml`** (and nested sitemaps)
2. **`/llms.txt`** / **`/llms-full.txt`** if present (agent-oriented TOC)
3. **Sidebar / TOC** from the docs shell (GitBook SUMMARY, Docusaurus sidebars)
4. **Root + recursive link crawl** limited to same host + in-scope path prefix
5. Local doc trees: walk `docs/**/*.md` (e.g. Crane `docs/`, mdBook SUMMARY)

Record for each page:

```text
id | url | title | section_path | parent_id | status
```

Tools: `web_fetch` / browser / `curl` + HTML parse; for GitBook/mdBook prefer SUMMARY.md when local.

## Phase 2 — Fetch and normalize (all pages)

For **each** inventory row:

1. Fetch full content (not just title).
2. Normalize to a working note (markdown): headings, lists, code, tables, warnings.
3. Extract structured signals:
   - Concepts / glossary terms
   - Contracts, functions, events, errors
   - Parameters, units, bounds
   - Workflows (numbered steps)
   - Config / deployment addresses
   - Security warnings / invariants
4. Tag note with `source_url` and `fetched_at` (ISO date).
5. Mark status: `done` | `failed` | `redirect` | `empty`.

**Failed pages:** retry once; if still failing, log in COVERAGE.md as residual risk — do not silently drop.

Storage suggestion (scratch, not necessarily committed):

```text
.scratch/docs-<family>/
├── inventory.csv
├── pages/
│   ├── 001-overview.md
│   └── ...
└── graph.json
```

## Phase 3 — Coverage audit (gate)

Before writing skills:

- [ ] Inventory count == fetched `done` + documented failures
- [ ] No in-scope sidebar node missing from inventory
- [ ] Duplicate URLs collapsed
- [ ] Version mismatches noted (docs version vs code version if known)

**Refuse to “finish” skills while coverage &lt; 100% of in-scope inventory** unless the user accepts a written waiver listing skipped URLs.

## Phase 4 — Cluster into a skill family

Map doc sections → **skills** using task-oriented compartments (not 1:1 page dumps).

### Default family template (DeFi protocol)

| Skill | Owns | Typical doc sections |
|-------|------|----------------------|
| `<p>-architecture` | System shape, contracts, data flow | Overview, architecture, contracts |
| `<p>-operations` | User/admin call flows | Guides, how-to, user docs |
| `<p>-deployment` | Addresses, init, upgrades | Deploy, addresses, governance |
| `<p>-risk` / security | Params, liquidations, oracles | Risk, security, oracles |
| `<p>-sdk` / integration | Off-chain / SDK | SDK, API, subgraph |

### Clustering rules

- **One primary job per skill** (architecture vs “how do I call X”).
- If a skill’s draft body would exceed ~300 lines of dense content, **split** further or move to `references/`.
- Prefer **3–8 skills** per large protocol; avoid 30 micro-skills that fragment discovery.
- Name: lowercase hyphens; optional gerund form for process skills (`deploying-foo`).

Write a short **family plan** file first:

```markdown
# Family plan: <prefix>
## Skills
- name: ...
  description draft: ...
  source pages: [urls...]
  references: [...]
```

## Phase 5 — Author skills (progressive disclosure)

For each planned skill:

### 5.1 Frontmatter

Follow `skill-authoring`: third-person description, WHAT+WHEN, trigger phrases, &lt;1024 chars.

### 5.2 SKILL.md body (lean)

```markdown
# <Title>

<1–3 sentence purpose grounded in docs>

## Quick facts
| Item | Value | Source |
|------|-------|--------|
| … | … | [docs](url) |

## Quick start
… minimal path …

## Read by task (compartments)
| Need | Open |
|------|------|
| … | [references/….md](references/….md) |

## Constraints / gotchas
- …

## Key terms
- …

## See also
- `skill:…`
```

### 5.3 references/*.md (detail)

- One concern per file; TOC if &gt;100 lines.
- Prefer tables, signatures, step lists.
- Cite source URLs at section ends: `Source: https://…`
- **Paraphrase** long prose; quote only critical warnings or exact parameter names.
- Cross-check conflicting pages; note ambiguity explicitly.

### 5.4 Do not

- Dump entire doc HTML into SKILL.md
- Invent APIs not present in docs (mark “unverified” if inferring from code)
- Nest references more than one level deep
- Omit pages because they are “boring” (changelogs may be out-of-scope; governance params usually are in-scope)

## Phase 6 — Family polish

1. Align terminology across skills (one name per concept).
2. Mutual **See also** links.
3. Ensure descriptions don’t all trigger on the same vague phrase (disambiguate).
4. Add `SOURCES.md` listing every inventory URL + which skill consumed it.
5. Add `COVERAGE.md`:

```markdown
# Coverage
- Inventory: N pages
- Fetched OK: N
- Failed: […]
- Skills emitted: […]
- Pages with no skill mapping: […]  # must be empty or waived
```

## Phase 7 — Install

Default install roots (same pattern as Crane porting skills):

| Workspace | Skills path |
|-----------|-------------|
| Crane | `lib/crane/.claude/skills/` (canonical) |
| IndexedEx | symlink or copy under `.claude/skills/` |
| projects-defi | symlink under `.claude/skills/` |

Also mirror to `.agents/skills/` / `.grok/skills/` when those trees exist in Crane.

After install, update:

- Crane `docs/reference/agent-skills.md` (if protocol skills)
- Relevant `CLAUDE.md` bullets when introducing a new family

## Fetching tips by site type

| Platform | Discovery |
|----------|-----------|
| GitBook | SUMMARY / sidebar; often `/sitemap.xml` |
| Docusaurus | `sidebars.js` + sitemap; versioned `/docs/` |
| Mintlify / Nextra | sidebar + sitemap |
| mdBook (local) | `docs/SUMMARY.md` + `book/` |
| API ref (OpenAPI) | Prefer OpenAPI JSON → generate reference skill; still inventory human guides |

Respect `robots.txt` where applicable; prefer official export/`llms.txt` over aggressive scraping. Rate-limit polite delays on large crawls.

## Quality gates (definition of done)

- [ ] Full inventory built from nav/sitemap, not ad-hoc browsing
- [ ] Every in-scope page fetched or explicitly failed+logged
- [ ] Family plan reviewed (skills have clear non-overlapping ownership)
- [ ] Each skill passes `skill-authoring` checklist
- [ ] `SOURCES.md` + `COVERAGE.md` present
- [ ] No mega-skill &gt;500 lines body
- [ ] Smoke prompts: at least one trigger phrase per skill activates the right skill
- [ ] Installed in requested repos

## Output report template

When finishing, report to the user:

1. Root URL + version  
2. Inventory size + coverage %  
3. Skill family tree (paths)  
4. Notable gaps / doc contradictions  
5. Install locations  
6. Suggested follow-ups (code-anchoring pass, porting skill if in Crane)

## See also

- `skill:skill-authoring` — progressive disclosure, descriptions, checklists
- `skill:writing-skills` — Crane/OpenCode-oriented skill patterns
- `skill:crane-porting` — if docs-to-skills feeds a protocol port
- Agent: `docs-skill-scribe`
- Reference: [Anthropic skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)

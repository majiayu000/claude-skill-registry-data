---
name: doc-ingest
description: Ingests a produced document — a strategy doc, analysis, report, deck, spec, or external article — into a structured note in 06-knowledge/, links it to the relevant projects, and extracts key claims, recommendations, data, and action items. The document twin of meeting-ingest. Use when the user shares or links a document, says "ingest this doc", "process this report", "analyze this analysis", or uploads a non-transcript document.
---

# Skill: Doc Ingest

The document counterpart of `meeting-ingest`. Meetings capture conversations; this
captures **produced artifacts** — strategy docs, analyses, reportings, decks, specs,
research, external articles — and turns them into durable, queryable knowledge that
enriches both `06-knowledge/` and the relevant projects.

## When to activate

- The user shares or links a document and wants it captured: "ingest this doc",
  "process this report", "analyze this strategy doc/deck/analysis".
- The user uploads a non-transcript document (PDF, doc, slides, article, spec).

**Do NOT use doc-ingest when:**
- The content is a meeting transcript → use `meeting-ingest`.
- It's a short loose thought (< ~300 words, no structure) → use `braindump`.
- The user just wants an answer from existing notes → use `recall`.

## Preflight

1. **Read `_CLAUDE.md`** (rules, schemas) and `00-inbox/MY-PROFILE.md` (working language, sensitive topics).
2. **Get the real timestamp.**
3. **Capture the source verbatim** — the URL or file path/title. This is non-negotiable (AI-first
   rule 4). If it's a **Google Doc** (or any linked doc), keep the canonical URL so you can reopen
   the original later — store it in both the `source:` frontmatter and the `## Links` section.
4. **List `02-people/` and `03-projects/`** for reference resolution.
5. **Classify the document**: strategy | analysis | report/reporting | deck | spec | research | external-article.
6. **Decide destination**: durable synthesis always lands in `06-knowledge/`; if it's tied to a project, also propagate to that `03-projects/` note.

## Process

### Step 1 — Read and segment
Read the document. For long docs, work section by section. Distinguish the author's
**claims** from **data** from **recommendations**.

### Step 2 — Extract (factual, with confidence)
- **Purpose / thesis**: 1–2 sentences — what the doc argues or reports.
- **Key claims**: each with a **confidence level** (`stated | high | medium | speculation`)
  and a **recency marker** (`as of <date>`), because an analysis is only as good as its date.
- **Data points**: numbers/metrics worth keeping, verbatim, with their source/date.
- **Recommendations / decisions proposed**: what the doc asks to do.
- **Open questions / gaps**: what it leaves unresolved or doesn't cover.
- **Entities**: people and projects → wikilinks (stubs if needed).
- **Action items the user owns** → write them in the task-line convention with a `^t-id`
  anchor so `task-roundup` picks them up.

⚠️ Keep the author's strong claims **verbatim** as quotes; don't launder them into your
own paraphrase. Mark clearly what is the document's assertion vs. established fact.

### Step 3 — Generate the note
**Path**: `06-knowledge/_sources/YYYY-MM-DD-<slug>.md` (NOT at the root of `06-knowledge/`
— that's reserved for wikis / lessons / hubs). Slug reflects the topic, not the format.

```markdown
---
date: YYYY-MM-DD              # ingestion date
doc-date: YYYY-MM-DD          # the document's own date, if known (else "unknown")
type: doc
doc-type: strategy|analysis|report|deck|spec|research|external-article
tags: [doc, <topic-tags>]
domain: <domain-slug>         # routes to 06-knowledge/<domain>.md hub; infer from project / tags / MY-PROFILE knowledge-domains
source: "<verbatim URL or path/title>"
project: "[[03-projects/...]]"      # if project-linked
related-people: ["[[02-people/...]]"]
confidence: high|medium|speculation # overall trust in the document
ai-first: true
---

## For future Claude

Ingested [doc-type] on [ingestion date], produced [doc-date]. Source: [source]. It
argues/reports [thesis]. Captured here for durable reference; key claims and their
confidence are below. [Note if the source is external / its reliability.]

## Thesis

[1–2 sentences.]

## Key claims

- [Claim] — confidence: high — (as of 2026-03, source: [source])
- [Claim] — confidence: speculation — (as of 2026-03)

## Data points

- [Metric/number, verbatim] — (as of <date>, source: [source])

## Recommendations / proposed decisions

- [Recommendation] → if high-stakes, suggest `challenge-decision` before acting.

## Open questions / gaps

- [What the doc doesn't resolve]

## Action items

- [ ] [Action] — owner: me — due: YYYY-MM-DD — #from/doc ^t-xxxxxx

## Links

- Source: [original document link — e.g. the Google Doc URL]
- Projects: [[03-projects/...]]
- People: [[02-people/...]]
- Related decisions/meetings: [[05-decisions/...]], [[04-meetings/...]]
- Related knowledge: [[06-knowledge/...]]
```

### Step 4 — Propagate
- **Project**: append to the linked project's `## Timeline` and, if the doc proposes
  decisions, its `## Key decisions`. Update the project's `updated:`.
- **Daily note**: append under the `## Docs ingested today` section (create if missing).
- **People**: if the doc is authored by or about a stakeholder, log a factual timeline line.
- **Action items**: handled by `task-roundup` (anchors already set).
- **Wiki stubs / enrichment**: for each concept, entity, tool, team, or piece of jargon the
  doc introduces or describes substantively, **create or enrich** the matching wiki page
  `06-knowledge/<slug>.md` per the Wiki stub protocol in
  `.claude/skills/knowledge-build/SKILL.md` (Mode A.2/A.4). New stubs use
  `created-from: "[[06-knowledge/_sources/<this-doc-note>]]"`; enrichments append to
  `## What we know` and `## Sources` with the doc's date. This is what makes the personal
  wiki grow.
- **Curator (incremental)**: call `knowledge-build` curator incremental update so the
  doc lands in the matching `06-knowledge/<domain>.md` hub's `## Source documents` section
  and the root `_INDEX.md` refreshes. Silent for `auto-maintained: true` hubs.
- **Lessons**: if the doc introduces a durable *pattern, framework, or principle* (not just
  a thing), suggest `knowledge-build` Lessons mode to fold it into a `type: knowledge` note.

### Step 5 — Report
```
✓ Doc ingested: 06-knowledge/_sources/2026-05-22-market-analysis-emea.md (doc-type: analysis, domain: marketing)
✓ Hub updated: 06-knowledge/marketing.md (+1 source listed)
✓ Source recorded: <url>
✓ 6 key claims extracted (2 high, 3 medium, 1 speculation)
✓ Linked to [[03-projects/Onboarding Refresh]] (timeline updated)
✓ 2 action items anchored → will appear in TODO.md on next roundup
→ Introduces a reusable framework — run knowledge-build to fold it into 06-knowledge?
```

## Anti-patterns to avoid
❌ **Dropping the source** — every ingested doc records its verbatim source.
❌ **No recency markers** — an analysis without its date is a trap; date every claim.
❌ **Laundering claims** — keep the document's assertions as quotes; don't present them as fact.
❌ **No confidence levels** — external analyses especially need them.
❌ **Skipping propagation** — link to the project(s) so the doc isn't an orphan.
❌ **Ingesting a confidential doc flagged sensitive in MY-PROFILE** without confirmation.

## Special cases

### External article / third-party research
`doc-type: external-article`, `confidence` reflects source reliability; keep the URL verbatim;
be explicit that claims are the source's, not verified.

### Large document / deck
Summarize section by section (or slide by slide); keep only the load-bearing quotes and
data verbatim. Don't transcribe the whole thing.

### Confidential / sensitive document
If the topic matches a sensitive area in `MY-PROFILE.md` (HR, comp, board, legal), confirm
before ingesting and note the sensitivity in the preamble.

### Working language
Write the body in the vault's working language (`MY-PROFILE.md`); the "For future Claude"
preamble is always English.

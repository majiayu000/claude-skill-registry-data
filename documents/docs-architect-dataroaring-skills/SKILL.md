---
name: docs-architect
description: "Apply world-class developer documentation principles (Stripe, Snowflake, Databricks, TiDB Cloud) to structure, write, review, or refactor technical documentation. Use this skill whenever the user mentions documentation, docs, sidebar or navigation, information architecture, restructuring a section, writing or editing a guide, reviewing docs, where content belongs, English doc prose, headings, code comments, link text, docs home pages, section landing pages, long-form guides mixing content types, cross-referencing, or making docs readable for AI agents and LLMs. Covers VeloDB Cloud docs work (Monitoring restructure, sidebar, EN/中文 alignment, writing style, landing pages, LLM-friendly docs) and any SaaS or database documentation task. Trigger broadly: if the conversation touches doc organization, page structure, doc quality, doc sentences, landing pages, or AI-readable docs, consult this skill rather than answering from intuition."
---

# Docs Architect

A skill for structuring, writing, and reviewing technical documentation—especially for developer products, databases, and data platforms. Built on principles distilled from Stripe, Snowflake, Databricks, MongoDB Atlas, and TiDB Cloud, with VeloDB Cloud as the default applied context.

## How to use this skill

The skill has two layers:

1. **Universal principles** (this file) — apply to any developer-facing documentation.
2. **VeloDB-specific guidance** (`references/velodb-context.md`) — terminology, section naming, English/Chinese alignment rules. Load this when the task is about VeloDB Cloud docs specifically.

For most tasks, the workflow is:
1. Identify which **scenario** the user is in (see "Scenarios" below).
2. Walk the relevant **principles** as judgment questions, not as a fill-in template.
3. If VeloDB-specific, also consult `references/velodb-context.md`.
4. For templates (page skeletons by document type), consult `references/templates.md`.
5. For reviewing existing docs, consult `references/review-checklist.md`.

The principles are **questions to ask**, not rules to enforce. The goal is to make the user think like a doc architect, not to mechanically apply a template.

---

## Scenarios this skill covers

When the user's task matches one of these, this skill applies:

- **Restructuring a section** (e.g., "重构 Monitoring 章节", "should Alerts be a sub-page of Monitor?")
- **Writing a new guide or page from scratch** (e.g., "写一篇 cluster 创建指南")
- **Reviewing or diffing existing docs** (e.g., "看看 TiDB 的 Monitor 章节和我们的差在哪")
- **Information architecture decisions** (e.g., "侧边栏应该怎么分", "顶层导航用什么名字")
- **Writing page content** (titles, headings, code examples, paragraph structure)
- **Terminology and naming** (e.g., "should we call it 'Cluster' or 'Warehouse'?")

If the user's request is ambiguous about which scenario, ask. Don't apply restructure-mode advice to a write-content task or vice versa.

---

## The 8 principles

Each principle has (a) the core idea, (b) check-questions to ask while working, and (c) common failure modes.

### Principle 1 — Organize by user task, not by product feature

**Core idea**: Top-level navigation should reflect what users want to *do*, not what the company built. Internal product names ("VeloDB Manager", "Doris Stream") belong in the second level at most. The first level should read like verbs or user-recognizable nouns.

**Check questions**:
- Could a first-time user, who has never heard the product's internal terminology, understand each top-level label in under 3 seconds?
- Does the navigation match how the user would describe their goal to a colleague ("I need to ingest data") rather than how engineering organized the codebase?
- If you renamed an internal feature tomorrow, would the navigation break?

**Common failure modes**:
- Using release codenames or internal team names as nav labels.
- Mirroring the org chart in the IA ("Compute Team docs", "Storage Team docs").
- Top-level categories that require a glossary to interpret.

### Principle 2 — Diátaxis: separate the four document types

**Core idea**: Every page is one of four types, and mixing them is the single biggest cause of bad docs.

| Type | Reader's goal | Reader's mindset | Example |
|---|---|---|---|
| **Tutorial** | Learn by doing | "Walk me through it" | "Get started in 10 minutes" |
| **How-to** | Solve a specific problem | "I need to do X" | "How to back up a cluster" |
| **Reference** | Look up exact details | "What are the parameters?" | "SQL function reference" |
| **Explanation** | Understand concepts | "Why does this work?" | "How MoW handles deletes" |

**Check questions**:
- Can you label this page as exactly one of the four types? If two or more, split it.
- Does a tutorial accidentally contain a parameter reference table? Move it out.
- Does a reference page try to explain *why*? Link to an explanation page instead.
- Does an explanation page contain procedural steps? Those belong in a how-to.

**Common failure modes**:
- "Complete guide to X" — usually four pages glued together.
- Reference pages with motivational prose at the top — pure friction for the user who came to look up a parameter.
- Tutorials that branch into "if you want to do X instead..." — that's a how-to disguised as a tutorial.

### Principle 3 — Progressive disclosure, both at IA and page level

**Core idea**: Surface only what the user needs at this moment. Hide complexity until it's asked for. Applies at three scales: the doc home page, the section landing page, and the individual page.

**Check questions at IA level**:
- Does the docs home page force the user to choose a path (new user / developer / operator) within 5 seconds? Or does it dump every category at once?
- For each section, is there a landing page that explains "what's in here and where to start"? Or does the user have to read the sidebar to figure it out?

**Check questions at page level**:
- Does the page lead with the 80% case, with edge cases linked or collapsed?
- Are the first 100 words enough for the user to know if they're on the right page?
- Is there a "Next steps" or "See also" section at the bottom?

**Common failure modes**:
- Home pages that are a flat list of every product feature.
- Section landing pages that are just an auto-generated table of contents.
- Pages that frontload caveats and edge cases before the main content.

### Principle 4 — Code and examples must be real, copyable, and runnable

**Core idea**: A code example is a promise. If the user copies it and it doesn't work, the docs lose trust. Examples should be end-to-end, use real (sample) data, and ideally connect to a live environment.

**Check questions**:
- If a user copies this example verbatim and runs it, does it work? (Including any prerequisites or setup that's not shown.)
- Are placeholder values clearly marked (e.g., `<your-cluster-id>` not `cluster_123`)?
- For SQL examples: does the query reference a real sample dataset the user can access?
- Is there a one-click path from the example to "try this in the product"?

**Common failure modes**:
- Toy examples (`SELECT * FROM table1`) that don't show realistic shape.
- Examples that assume context the user doesn't have ("first, configure your VPC...").
- Mixed placeholder styles (`<id>`, `{{id}}`, `your_id`, `YOUR_ID` all in one doc set).

### Principle 5 — Docs are a product funnel, not a cost center

**Core idea**: Every doc page is also a conversion surface. The user should always know what their next action is—and that action should, when possible, be inside the product, not on another doc page.

**Check questions**:
- Does this page have a clear next action? ("Open in Console", "Try in SQL Editor", "Run this tutorial".)
- Are doc pages and product empty states **bidirectionally linked**? (Empty state → relevant doc; doc → "do this in the product".)
- For a new user landing on this page from Google, is there a path to "first successful query" without leaving the docs?

**Common failure modes**:
- Doc pages that end with the last paragraph, no call to action.
- "Click here" links that go to other doc pages instead of into the product.
- Empty states in the product that don't link to relevant docs.

**Advanced pattern: product API responses link back to docs.**

The strongest version of "docs as funnel" goes beyond UI deep-links. Stripe's API errors include a `doc_url` field that points to the docs page for that error code:

```json
{
  "error": {
    "code": "card_declined",
    "decline_code": "insufficient_funds",
    "message": "Your card has insufficient funds.",
    "doc_url": "https://stripe.com/docs/error-codes/card-declined"
  }
}
```

This makes the docs an active part of the error-handling experience, not just a place developers go *after* they're stuck. The same pattern applies to:
- **Error responses** — every error code has a `doc_url` to the page explaining it
- **Deprecation warnings** — warnings link to the migration guide
- **Rate-limit responses** — link to rate-limit best-practices doc
- **CLI error output** — error messages include `See: docs.example.com/...`
- **Empty states in the UI** — link to the relevant getting-started page

This is a product design decision as much as a docs decision. As a PM owning the doc, push for these links to be added to API responses and UI surfaces. The lift is small (one URL field) and the user experience improvement is large.

**Apply to VeloDB Cloud**: every error returned by the SQL engine, the Cloud control plane API, or the CLI should include a stable `doc_url` (or equivalent) pointing to a docs page that explains the error and how to fix it. This is one of the highest-ROI cross-team investments a PM can advocate for.

### Principle 6 — Choose layout to match content type

**Core idea**: Three-column layouts (nav + content + code) are excellent for API/SQL reference where description and code are 1:1. They're wasteful for everything else. Match layout to content.

**Decision matrix**:

| Content type | Layout |
|---|---|
| API / SQL reference (function-per-page) | Three columns (nav + description + code) |
| How-to guides with code | Two columns (nav + content with inline code blocks) |
| Concepts / explanation / architecture | Two columns or single wide column (room for diagrams) |
| Quickstart / tutorial | Single wide column with prominent next-step buttons |
| Landing pages | Cards or columns, not sidebar-dependent |

**Check questions**:
- Is the right column (code) going to be substantially shorter than the middle column (prose)? If yes, don't use three columns—you'll get empty space.
- Does this page contain wide diagrams or architecture figures? Single wide column.
- Does this page have one or two main actions? Use a prominent button block, not buried links.

**Common failure modes**:
- Forcing three-column layout on tutorials, then having to pad the right column with redundant snippets.
- Using sidebar layouts for landing pages that should be card grids.
- Diagrams squeezed into a narrow middle column.

### Principle 7 — Small details compound into "professional feel"

**Core idea**: The gap between A-tier docs and S-tier docs is not structural—it's the accumulation of tiny touches. Code-block copy buttons, language/locale persistence, in-page anchors, sticky navigation, the unselectable `$` prompt, breadcrumbs, prev/next page links, search that actually works.

**Check questions for each page**:
- Does every code block have a copy button with success feedback?
- If the user switches to Chinese on one page, does the whole site remember?
- Are there breadcrumbs showing where the user is?
- Is there a "last updated" date so the user knows the content is maintained?
- Does the search return results ranked by relevance, not alphabetical order?

**Common failure modes**:
- Treating these as "polish for later"—they compound, so delay compounds too.
- Doing 80% of the small things, leaving the missing 20% as visible cracks (e.g., copy buttons on most code blocks but not all).
- Ignoring locale persistence—a major credibility hit for bilingual docs.

### Principle 8 — Design docs for both humans and LLMs

**Core idea**: A growing share of doc readers are AI agents reading on behalf of humans (Cursor pulling context, Claude Code fetching guides, ChatGPT answering product questions from docs). The docs need to work for both audiences. This is a frontier as of 2025-2026—most NA data platform competitors haven't invested here yet, which makes it a real differentiation opportunity.

**Check questions**:
- Can your docs be fetched as raw markdown by an agent without HTML scraping? (Stripe ships `.md` versions at every URL.)
- Is there a machine-readable manifest of doc pages (e.g., `/llms.txt`, `/.well-known/skills/index.json`)?
- Are UI elements, system states, and outcomes named explicitly (not "click the button" or "once it's done")?
- Does every code example run as-is without context the LLM can't see?
- If you fed your docs to a fresh LLM and asked "how do I do X with this product," would the answer be correct and complete?

**Common failure modes**:
- Heavy framework markup that obscures the content from agents.
- Vague prose ("click the button", "use the result") that humans tolerate but LLMs propagate as ambiguity.
- Code snippets that assume context not shown on the page.
- No machine-readable index, forcing agents to crawl.
- Marketing voice leaking into docs ("our powerful feature lets you..."), which then leaks into LLM answers.

For full details on LLM-readable docs and Stripe's specific implementation, load `references/ai-agent-readability.md`.

---

## Decision tree: which principles apply to my task?

Use this to focus rather than walk all 8 every time.

```
Is the user designing a docs home page or section landing page?
├─ YES → Principles 1, 3 are primary. Load landing-pages.md — landing pages
│         follow inverted rules vs. detail pages.
│
Is the user writing a long-form guide that covers multiple aspects
of one topic (a "complete guide to X")?
├─ YES → Load long-form-pages.md. Principle 2 applies in a modified form
│         (H2 sections can have different Diátaxis types).
│
Is the user restructuring or designing IA?
├─ YES → Principles 1, 2, 3, 6 are primary. Also load templates.md if writing landing pages.
│
Is the user writing a single page from scratch?
├─ YES → Principles 2, 3, 4, 5 are primary. Consult templates.md for the page skeleton AND writing-style.md for sentence-level craft.
│
Is the user editing or polishing existing English prose, headings, or code comments?
├─ YES → Load writing-style.md. Sentence-level rules are primary here.
│
Is the user reviewing existing docs?
├─ YES → Use review-checklist.md. All 8 principles apply as audit questions. Also load writing-style.md for prose-level review.
│
Is the user thinking about LLM/AI agent consumption of docs
(Cursor, Claude Code, ChatGPT users reading via AI)?
├─ YES → Principle 8 is primary. Load ai-agent-readability.md for specific moves.
│
Is the user choosing a label, term, or name?
├─ YES → Principle 1 is primary. Also consult velodb-context.md if it's a VeloDB term, and writing-style.md Rule 6 for capitalization.
│
Is the user thinking about cross-linking or how dense to make doc references?
├─ YES → Load long-form-pages.md (covers cross-referencing philosophy).
│
Is the user deciding layout (3-column vs 2-column vs cards)?
└─ YES → Principle 6 is primary.
```

---

## How to apply principles in practice

The default mode is **conversational judgment**, not template-filling. When the user asks "should Alerts be under Monitor or be its own section?", the answer is:

1. State which principle(s) apply (here: Principle 1 — user task organization; Principle 2 — Diátaxis type).
2. Ask the relevant check questions, either to the user or in your own analysis.
3. Give a recommendation with the reasoning visible.
4. Note tradeoffs (no decision is purely one-sided).

Avoid:
- Reciting all 8 principles when only 1 is relevant.
- Mechanically applying templates when the user wants to think.
- Treating principles as MUSTs rather than as decision aids.

---

## When to load reference files

- `references/velodb-context.md` — load when the task involves VeloDB Cloud specifically (terms, sections, EN/中文 alignment).
- `references/templates.md` — load when writing a new page from scratch. Contains skeletons for the four Diátaxis types, landing pages, interactive checklists, **problem catalogs** (error codes / decline reasons / known issues), and **topic surveys** (long multi-type guides covering a foundational topic).
- `references/review-checklist.md` — load when reviewing or diffing existing docs.
- `references/writing-style.md` — load when writing or editing English documentation prose, headings, code comments, or link text. Contains 22 sentence-level and paragraph-level rules extracted from Stripe's docs. **Load this any time the task involves producing or editing English doc text.**
- `references/landing-pages.md` — load when designing a docs home page, a section landing page, or any page whose primary job is routing readers (not teaching). Landing pages follow inverted rules from detail pages.
- `references/long-form-pages.md` — load when writing a long guide that covers multiple aspects of one topic, when deciding whether to split a page, or when thinking about how densely to cross-link between docs.
- `references/ai-agent-readability.md` — load when the task involves making docs work for AI agents and LLMs (Cursor, Claude Code, ChatGPT, etc.). Covers Principle 8 in depth.

## Tools

- `scripts/check_vocab.py` — Vocabulary linter. Checks four categories: (a) "thesaurus verbs" with simpler equivalents (utilize → use), (b) likely action verbs with Zipf frequency < 4.0, (c) **contractual adjectives** ("stable", "production-ready", "backward-compatible", "low-latency", etc.) that need concrete definitions on the page (Rule 14), and (d) **mixed modal verb strength** (warns when "must" / "should" / "recommend" / "can" / "may" are mixed within one page without intent, see Rule 20). Also flags Rule 16 violations like "Welcome to..." or "This page covers..." page openings. Usage: `python scripts/check_vocab.py <file.md>` or `python scripts/check_vocab.py - < draft.md`. Requires `pip install wordfreq`. **Use this on any non-trivial English draft before review.** Exit code 1 means hard violations (banned phrases) found; soft warnings don't fail.

For pure IA decisions or principle-level judgment, the body of this file is usually enough.

---

## A note on opinions vs. principles

Some of these principles have strong industry consensus (Diátaxis, user-task-over-feature organization). Others reflect specific stylistic choices (Stripe's three-column layout) that are *good for certain content* but not universal. When a principle conflicts with a strong user preference, the user wins—but make the tradeoff visible. Don't quietly drop a principle; say "I'm setting aside Principle X here because Y."

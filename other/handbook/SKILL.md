---
name: handbook
description: >-
  Research the user's question and write a Notion handbook: one
  index page (TOC + Sources only) plus a subpage per chapter,
  including Chapter 1 Abstract. Use only when the user invokes
  /handbook.
disable-model-invocation: true
---

# handbook

Research the user's question, then write it as a book-like Notion handbook. The page is the deliverable, not a chat essay.

## Input

Require both before doing anything else:

1. The user's **question** — a real question to answer, not a one-word topic
2. A **Notion parent** — page or database URL / mention where the handbook should live

If either is missing, ask for the missing piece and **stop**. Do not research, outline, or create a page.

Write in the same language as the user's question.

## Research

Do not write from memory. Gather sources first.

1. Search the web for current primary docs, specs, and a few high-quality explainers.
2. If the question is about the current repo, read the relevant code.
3. Search Notion for an existing handbook on the same question. If one exists under the parent, ask whether to update it or write a new page.

Keep a source list as you go: title, URL, why it is trustworthy. Discard blogs that only restate the docs. Flag uncertainty instead of filling gaps.

## Outline before writing

Answer the question, then stop. Chapter 1 is always the abstract, and it is always its own Notion page. Later chapters are only the parts of *that* question, in reading order — not a dump of search results, and no target count.

Adjacent context is a link (or a Sources line), not another chapter. Do not add Background, History, Extra, or "also useful" chapters.

## Book shape

Always two layers. Never put the whole handbook on one page. **No chapter body lives on the index** — not even Chapter 1.

1. **Index page** — one child of the user's Notion parent. Holds only a TOC, a list of chapter pages, and Sources. No abstract, no diagrams, no chapter prose.
2. **Chapter pages** — one child of the index **per chapter**, including Chapter 1 (Abstract). No chapter lives only as a heading on the index.

```
User's Notion parent
└── Handbook: [title]          ← index (TOC + Sources only)
    ├── Chapter 1 — Abstract
    ├── Chapter 2 — [section]
    ├── Chapter 3 — [section]
    └── What this does not cover   ← only if research left real gaps
```

On the index: do not put the page title in the body. Set `properties.title` from the question (short handbook title). Set an icon. Add `<table_of_contents/>` near the top. List each chapter, including Chapter 1, with `<mention-page>` after the chapter pages exist. Do not paste Chapter 1 onto the index and then "also" create a subpage.

### Chapter 1 — Abstract

Create this as a **child page of the index**, titled `Chapter 1 — Abstract`. Do not write it into the index body.

The map, not the territory. After this chapter the reader should know what the subject is, the main parts, how they connect, and what they will learn next. No API lists, no deep how-to, no edge cases.

Start the chapter with this sub-chapter, then the rest of the abstract:

```
## What you should know
```

Must include:

- **What you should know** first: the whole picture in plain language
- One map diagram of the whole system (Mermaid `flowchart` or `C4Context`)
- A "How to read this handbook" line that points at the later chapters
- A "Read next" pointer to Chapter 2 (use `<mention-page>` after that page exists)

### Chapters 2+

One topic per chapter. Start with a one-sentence claim, then explain. Teach, do not recap research notes.

Each detailed chapter must include **more than prose**:

| Include | When |
| --- | --- |
| Mermaid diagram | The topic has structure, flow, states, or relationships |
| Callout | A definition, warning, or invariant the reader should keep |
| Table or columns | A comparison, vs-table, or "use A / use B" |
| Resource links | 2–5 primary sources for that chapter |

End each chapter page, including Chapter 1, with a short "Read next" pointer to the next chapter page. Put the full cited-URL list in **Sources on the index**, one line on why each is there. Use Markdown links for external URLs. Use Notion mentions only for existing Notion pages.

### What this does not cover (optional)

Add this chapter only when research left real gaps: unanswered parts of the question, missing sources, or a nearby topic the reader might expect. Omit it if the question is closed. Do not use it as a dumping ground for extra material.

## Notion

Read the MCP resource `notion://docs/enhanced-markdown-spec` before writing content. Do not invent Markdown.

1. Fetch the parent the user named. Confirm it is a writable page or database. If fetch fails or it is not writable, say so and **stop**.
2. Create the **index** as a child of that parent. Never use `creation_mode: "draft"`. Never edit the parent's existing content. Index content is TOC + chapter mentions + Sources only.
3. Create **one child page per chapter** under the index (`parent.page_id` = index), **including Chapter 1 — Abstract**. Wait for the index id before creating chapter pages.
4. Use `notion-create-pages`. Default `allow_async: true`. If it returns an async task, wait with `notion-get-async-task`.
5. Update the index so each chapter is listed with `<mention-page>`, Chapter 1 first. Do not use `<page>` (that moves pages).
6. Give the user the **index** URL.

Required Notion flavor:

- Headings: `#` / `##` / `###` only
- Diagrams: fenced ` ```mermaid ` — quote labels that contain `()`, use `<br>` not `\n` inside labels
- Callouts: `<callout icon="..." color="blue_bg">` (or `yellow_bg` for warnings)
- Comparisons: `<columns>` with two `<column>` children
- Toggles: `<details>` for optional depth, not for the main argument
- Indent children with tabs

A page that is only headings and paragraphs has failed. If a chapter has no diagram and no table, it is unfinished.

## Voice

Write like a careful book, not a briefing.

- Outcome and mental model first
- Define a term the first time it appears
- No "in this article", "as we discussed", tool names, or research play-by-play
- No invented APIs, dates, or product claims
- Keep file paths and product names exact

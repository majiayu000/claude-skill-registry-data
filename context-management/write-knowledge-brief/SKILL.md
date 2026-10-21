---
name: write-knowledge-brief
description: Write the brief a drive shows the person when it must reach them — what we understood, what we built, and where the gaps are, each with its context and our proposed answer — the way you would brief someone who can help close the piece. A few themed gaps (at most seven), the knowledge pages waiting for approval with our recommendation, and a pointer to the prototype notes. Never a questionnaire. Used by the knowledge-builder agent in /review-knowledge.
user-invocable: false
model: sonnet
allowed-tools: Read, Write, Glob, Grep
---

# write-knowledge-brief

When a drive must reach the person, it briefs them as you would brief someone who can help
close the piece: what we understood, what we built, where the gaps are — with the context
behind each. This skill writes that brief.

## Input

| Field | Required | Meaning |
|-------|----------|---------|
| `run` | yes | What the drive made: the proposed intents, the domain, its capabilities |
| `search` | yes | `search.json` — what the sources and memory answered |
| `build` | yes | `build.json` — proposals, knowledge pages, prototype notes, settled gaps |
| `pages` | yes | The waiting memory updates, as the memory tool's `updates` lists them |
| `audience` | yes | Who reads it (for Kickoff: who shared the prototype) |
| `out` | yes | `brief.json` and `brief.md` |

## Process

1. **What we understood** — three to five sentences: what the product is, who uses it, what they
   do with it, in the audience's words. Not a list of screens.
2. **What we built** — a few lines with counts: the intents (each in one line), the domain, how
   many capabilities, and how much the search closed from the source and memory, with one
   example.
3. **Where the gaps are** — group the proposals by theme (how we will know it works; who decides
   and who sees; size and speed; …). At most seven gaps. For each: an id (`G1`…), a plain theme,
   the **context** (what we saw that bears on it) and **our proposed answer** (what we would put,
   concrete). Never a question; never example answers to pick from.
4. **Settled** — each point the build closed as settled, in one line with what settles it, so
   the person can see it and correct it.
5. **Knowledge pages** — each waiting page: what it says in a line or two, its sources, and our
   recommendation (approve or reject) with why, so a "yes" is an informed approval.
6. **Prototype notes** — the count and where the full list is; no answer needed now.
7. Close with one line on how to reply: "yes" takes every proposal and every recommendation
   shown; or correct a gap, a settled point or a page by its id.
8. Leave out what the search answered except as a count and one example.

## Output

`brief.json` — `{"understood", "built", "gaps": [{"id", "theme", "context", "proposal", "from":
[build group ids]}], "settled": [{"from", "what", "why"}], "pages": [{"update", "what",
"sources", "recommend"}], "prototype_notes": {"count", "where"}}` — and `brief.md`, the same in plain prose under the headings **What we understood**,
**What we built**, **Where the gaps are**, then the pages and notes. Short paragraphs; no
tables; no wall of text.

## Rules

- Every proposal in `build.json` is in exactly one gap; every settled point is shown; every
  waiting page is listed with its sources.
- A gap carries its context and our answer — a reader must be able to say yes without opening
  the prototype.
- Plain words. The reader is a person who knows the product, not Garura.

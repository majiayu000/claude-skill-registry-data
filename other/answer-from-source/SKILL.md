---
name: answer-from-source
description: For each group of a drive's open questions, look in the drive's own sources again — for a prototype, every captured view, every journey step and the page itself (its text, labels, sample data and script) — and answer with a quote and the place it was found. Marks each group answered, partly answered (naming the part still missing) or not shown, and for not shown says whether the source should show it (a gap in the prototype) or no screen could (knowledge or the person). Used by the knowledge-builder agent in /search-knowledge.
user-invocable: false
model: opus
allowed-tools: Read, Write, Glob, Grep
---

# answer-from-source

A drive's plays often leave open what the source already shows: many open questions turn out
to be answered, fully or in part, by the prototype the drive had read. This skill looks
again, properly, before anyone is asked.

## Input

| Field | Required | Meaning |
|-------|----------|---------|
| `groups` | yes | `question-groups.json` — each group's questions and their ids |
| `sources` | yes | The drive's Source evidence folders: for a prototype, its `screen-…`/`view-…` text and pictures, `journeys/` (each step's text), and the page file itself |
| `out` | yes | Where to write the per-group findings (`<working>/source-answers.json`) |

## Process

1. For each group, write the one question it asks in plain words.
2. Search every source file for it: the views' text, the journey steps' text, and the page
   itself — a prototype's page often holds much more than its screens show (help text, sample
   data, the script's behaviour: what a button sends, what is never sent).
3. Decide:
   - **answered** — the source shows the answer. Quote it, and name the file and the line or
     view. Behaviour counts: "Later sends no event (line 1035)" answers "does Later reach
     Garura?".
   - **partly** — it shows part. Quote that part and write the question for the part still
     missing, narrowly.
   - **not shown** — nothing in the source says it. Say which: **should show** (a screen state
     the prototype lacks: a second person opening the same review, a failed send) or **no screen
     could** (a speed target, a legal rule, a business result over time, where the product sits
     in the knowledge base).
4. Check every claim you make about the source against it — never write that it "does not
   show" something before searching for it.

## Output

`source-answers.json`: `{"groups": [{"id", "ask", "found": "answered | partly | not-shown",
"answer", "evidence": [{"file", "where", "quote"}], "missing", "not_shown": "should-show |
no-screen"}]}`.

## Rules

- No quote, no answer.
- Sample data is sample data: the shop inside a review tool's mockup tells you how the tool
  shows things, not facts about the tool's own users.

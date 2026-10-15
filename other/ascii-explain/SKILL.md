---
name: ascii-explain
description: |
  Traces a request, flow, or pipeline as an ASCII/box-drawing diagram in the terminal —
  real file:line anchors, real payloads, branch points marked, failure edges shown.
  Use when the user asks to "explain simply", "explain with ascii", "explain this",
  "trace this with a diagram", "draw the flow", "ascii diagram", "show me the request
  path", "diagram this", "map out how X gets from A to B", or asks to compare two paths
  through the same code (v1 vs v2, UI vs API, before vs after). Any request to explain
  something simply or visually should be answered with a diagram from this skill.
  Prefer this over prose when the answer is a SEQUENCE with branches. Always reads the
  real code first — never draw from memory.
user-invocable: true
argument-hint: "[flow to trace, or 'this' to diagram the current context]"
---

# ascii-explain

Draw the flow, in the terminal, from the actual code. One fenced block the user can
read top to bottom, with `file:line` anchors they can click.

The diagram's entire value is accuracy. **Read the code first.** A confident diagram
with an invented line number is worse than prose, because it looks verified.

## When this is the right tool

Reach for it when the answer is a **sequence with branches**: a request path, a
lifecycle, a pipeline, two versions diverging through shared code. Skip it when a
sentence covers it, or when the shape is a table (comparisons, config matrices) or a
list (options, findings).

Adjacent skills: `explain-with-html` for a rich standalone artifact,
`explain-simply` for plain-language re-explanation with no code trace.

## Before drawing

1. **Trace the real path end to end.** Every hop: entry point, dispatch, each function,
   the external call, the terminal state. Grep for callers; don't assume.
2. **Pin line numbers immediately before writing.** Grep the function names fresh — if
   the file was edited earlier in the session, remembered line numbers are stale.
3. **Get one real payload.** The actual request body, the actual outbound call body. A
   diagram with `{...}` placeholders teaches nothing; the payload is often the punchline.
4. **Find the branch points.** These are the diagram. A straight line needs no picture.

## Anatomy

Vertical, top to bottom, inside a single fenced block tagged `text`. **Hard cap 78
columns** — terminals wrap, and a wrapped diagram is unreadable.

The `←` notes below label the technique; a real diagram wouldn't carry them.

```
┌─ entry ────────────────────────────┐
│ POST /api/v2/thing?flag=1          │  ← real path + query params
│ { id: "ABC123", name: "…" }        │  ← real payload
└──────────────────┬─────────────────┘
                   ▼
        ╔══════════════════════════════╗
        ║  Lambda Handler — idx.js:654 ║   ← ╔═╗ = major component
        ╚══════════════╤═══════════════╝
                       ▼
   getContext(event)                       apiUtil.js:12
     ├─ getVersion(event.path)   → 2       ← the VALUE, not the call
     └─ isFooRequest(path)       → true
                       ▼
   handler:735  isFooRequest ──► doTheThing()
     ├─ :157  param present?  else 400-422 ← failure edge, inline
     └─ :163  validate(request)
                       ▼
   externalCall()                          client.js:75
        POST {host}/v1/allocate
        body → { environment, region, alu }
                       ▼
              ── terminal state / response ──
```

Each step is `functionName()` plus a right-aligned `file.js:LINE`, or a bare `:LINE`
when it's the same file as the line above. Show resolved **values** (`→ 2`, `→ true`),
not just that a call happens.

## The four devices that carry the weight

**1. Side-by-side entry, funneling into one.** When comparing two paths through shared
code, start them as parallel boxes and merge the connectors. The funnel *is* the claim:
same code, different data.

```
┌─ v1 caller ──────────┐  ┌─ v2 caller ──────────┐
│ POST /v1/thing       │  │ POST /v2/thing       │
│ { name }             │  │ { id: "X", name }    │
└──────────┬───────────┘  └──────────┬───────────┘
           └──────────┬──────────────┘
                      ▼
```

**2. `★ DIVERGENCE` callouts.** At each branch, name it, cite the line that decides, and
show what each side actually gets. This is where readers stop and learn.

```
★ DIVERGENCE 1 — schema picked by path substitution
  util.js:85  format("{VERSION}/Thing.json")
    v=1 → model/v1/Thing.json   required: [name]      UNTOUCHED
    v=2 → model/v2/Thing.json   required: [id, name]  NEW
```

**3. An explicit convergence bar.** Once branches rejoin, say so loudly. It tells the
reader they can stop tracking two things — and it's usually the most reassuring line in
the whole answer.

```
═══════════ everything below is IDENTICAL for v1 and v2 ═══════════
```

**4. Failure edges inline.** `else 400-422`, `!id → STATE_FAILED, bail`. A happy-path-only
diagram hides exactly what the reader will hit in testing.

## Nesting one function's internals

When a single function has several meaningful steps, indent them inside a `│ … │` block
rather than flattening into the main spine:

```
        ┌─────────────────────────────────────────────────┐
        │  validateAndGetData()          utils.js:48      │
        │                                                 │
        │  :53  validateRequest(request, event)           │
        │  :59  transformData(request)                    │
        │         ├─ delete data.digital        :87       │
        │         └─ delete data.id             :93       │
        │              v1: no-op (can't exist)            │
        │              v2: strips it — id is for the      │
        │                  external call only             │
        └─────────────────────┬───────────────────────────┘
```

## Character palette

Keep it small and consistent:

| Use | Chars |
|---|---|
| Flow / connectors | `│ ─ ├ └ ┬ ▼` |
| Entry & detail boxes | `┌ ┐ └ ┘ ─ │` |
| Major component (handler, service) | `╔ ╗ ╚ ╝ ═ ║` |
| Convergence bar / emphasis | `═══` |
| Branch marker | `★` |
| Dispatch arrow, inline | `──►` |
| Value resolution | `→` |

Don't add decoration that carries no information. Every box should exist because
something is inside it.

## After the diagram

Two or three short observations — each a claim **the diagram makes obvious** that prose
would have buried. Not a summary; the diagram is the summary.

Good ones name a consequence:

> **The divergence is entirely upstream of the business logic.** Once `allocatedID`
> exists there is one code path — which is why v2 needed zero handler changes.

> **`request.id` never reaches the record.** Read once at `:72`, forwarded, deleted at
> `:93`. The stored id is whatever the external service returned, applied at `:834`.

Then stop. No feature tour, no restating the boxes in sentences.

## Don't

- Draw from memory, or reuse line numbers from before an edit. Grep, then draw.
- Sprawl left-to-right. Terminals scroll vertically.
- Exceed 78 columns.
- Diagram a straight line with no branches — write the sentence instead.
- Invent a `file:line` you didn't verify. Omit the number rather than guess it.
- Narrate the diagram afterward in prose. It already said it.

## Other shapes

The vertical trace is the default because most questions are "how does X get to Y". When
the shape genuinely differs, match it: side-by-side columns for layered architecture,
a state table plus transition arrows for state machines, a fan-out tree for
queue/worker dispatch. Same rules — real anchors, marked branches, 78 columns, hard stop
after the observations.

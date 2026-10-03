---
name: context-graph-compressor
version: 2
description: >
  Compress any conversation into a portable JSON context graph for handoff to a new chat or LLM.
  Trigger on: "compress this chat", "save context", "new chat", "hand off", "transfer context",
  "too many tokens", "start fresh", "export conversation", "context graph", "continue in new session".
  Also trigger proactively when the user mentions starting over in a long session.
---

# Context Graph Compressor v2

Convert a conversation into a structured, portable JSON state graph — preserving decisions, facts,
problems, goals, code, assumptions, and relationships — so any LLM can resume from the most
important conversational state at minimal token cost.

> **Honest scope:** This preserves the most important state from a conversation. It is not a
> lossless transcript. Some nuance and detail will be lost. The goal is continuity, not reproduction.

---

## Compression Modes

Infer from user intent. Default to `compact`.

| Mode | When | Target tokens |
|---|---|---|
| `compact` | Handoff to new chat, token saving (DEFAULT) | 400–800 |
| `readable` | Human summary, sharing with team, archiving | 1000–2000 |

**`compact` triggers:** "new chat", "hand off", "transfer", "save context", "too many tokens", "start fresh"
**`readable` triggers:** "summarize", "readable", "share", "export", "archive"

---

## Node Types

| Code | Full | Use when |
|---|---|---|
| `F` | Fact | Explicitly stated technical truth — stack, versions, config, schema |
| `D` | Decision | A choice was made, or something was ruled out |
| `P` | Problem | A bug, error, or blocker — with or without resolution |
| `G` | Goal | What the user is trying to build or achieve |
| `C` | Code | A specific snippet, method, annotation, or fix — preserve verbatim |
| `A` | Assumption | Something inferred but never explicitly stated |
| `X` | Context | Open threads, deferred work, unresolved questions |

**`A` (Assumption) explained:** Facts are stated. Assumptions are inferred.
If the user never said "we're deploying to AWS" but every config decision implies it — that's an `A` node, not an `F` node. Assumptions matter because a new LLM might contradict them. Making them explicit prevents silent conflicts.

---

## Node Status

Every node gets a `st` (status) field:

| Value | Use when |
|---|---|
| `active` | Currently in progress or relevant right now |
| `open` | Known issue or question, not yet addressed |
| `resolved` | Completed, fixed, answered |
| `deferred` | Explicitly postponed for later |
| `blocked` | Cannot proceed — waiting on something |
| `abandoned` | Tried and dropped; preserve so the new session doesn't retry it |

**Rule:** If status is unknown and the node is a fact or decision, omit `st`. Only set it when it meaningfully changes how a new LLM should treat the node.

---

## Importance

| Code | Meaning |
|---|---|
| `h` | High — losing this breaks continuity |
| `m` | Medium — useful context, not critical |
| `l` | Low — drop in compact mode |

---

## Graph Relationships

Nodes can have explicit relationships via a `rel` array. Use relationships when a simple parent-child
nesting does not capture the actual connection.

```json
{ "from": "n2", "to": "n5", "type": "depends_on" }
```

| Type | Use when |
|---|---|
| `depends_on` | n2 cannot work correctly without n5 being in place |
| `caused_by` | n2 (a problem) was caused by n5 (a decision or fact) |
| `resolves` | n2 (a fix) resolves n5 (a problem) |
| `supersedes` | n2 replaces n5 — n5 is outdated but preserved for traceability |
| `references` | n2 mentions or relates to n5 without a causal link |
| `related_to` | Loose connection — same area, no precise relationship type fits |

**When to use vs. parent-child nesting:**
- Use nesting for "this detail belongs under this topic"
- Use `rel` for cross-cutting dependencies that span topics

Relationships go in a top-level `"rel"` array in the graph, not inside individual nodes.

---

## Confidence (optional)

Only use when inference was required to produce a node — i.e. something was not explicitly stated.

```json
{ "conf": 0.85 }
```

| Range | Meaning |
|---|---|
| 0.9–1.0 | Explicitly stated in the conversation |
| 0.7–0.9 | Strongly implied by multiple signals |
| < 0.7 | Uncertain — consider whether the node should exist at all |

**Rule:** Omit `conf` entirely on nodes that are directly stated. Only include it on `A` (Assumption)
nodes or nodes where inference was clearly required. If confidence would be below 0.6, drop the node.

---

## Conversation Size & Strategy

Do not rely on exact token estimates — message lengths vary widely. Use these signals instead:

| Signal | Strategy |
|---|---|
| Conversation clearly fits in one read | **Single pass** |
| Conversation is very long but manageable | **Single pass with aggressive pruning** |
| Conversation is too large to hold in context | **Chunked compression** |
| Extremely large — only critical state survives | **Chunked + priority-only** |

### Chunked Compression

When the conversation exceeds what can be processed in one pass:

1. **Divide** into segments at natural breakpoints (topic shifts, time gaps, phase changes)
2. **Compress each segment** independently using the same schema. Prefix node IDs: `A-n1`, `B-n2`
3. **Merge:**
   - Deduplicate: same topic across segments → one node, latest version wins
   - Conflict: use `supersedes` relationship, keep both nodes, note the switch in the newer node's summary
   - Re-ID: renumber final nodes as `n1`, `n2`...
   - Drop all `l` importance nodes
   - Write one unified `handoff`
4. Add `"chunks": X` to output metadata

### Token budget

Compact output: target 400–800 tokens, hard cap 1200.
If over budget: drop `l` nodes → trim `m` summaries → merge related siblings → never cut `h` nodes.

---

## Conflict & Decision History

Do not silently overwrite changed decisions. When a decision was made, then changed:

- Keep both nodes
- The newer node's summary notes the switch: "Switched from X to Y"
- Link with `supersedes` relationship

```json
{
  "n": [
    { "id": "n3", "t": "D", "i": "m", "st": "abandoned", "s": "Initially chose PostgreSQL." },
    { "id": "n7", "t": "D", "i": "h", "st": "active", "s": "Switched to MySQL — portability requirement." }
  ],
  "rel": [
    { "from": "n7", "to": "n3", "type": "supersedes" }
  ]
}
```

This preserves traceability. A new LLM seeing `n3` with `abandoned` status won't re-suggest PostgreSQL.

---

## Conversation State Preservation

Beyond summarizing history, capture the current state of the project:

**Always include if present:**
- Active goals (`G`, `st: active`) — what the user is working toward right now
- Open problems (`P`, `st: open`) — unresolved bugs or blockers
- Deferred work (`X`, `st: deferred`) — explicitly postponed, must not be forgotten
- Blocked items (`st: blocked`) — what is stuck and why
- Pending decisions — choices not yet made, framed as `X` nodes

The handoff field should reflect current state, not just history.

---

## COMPACT Schema

```json
{
  "v": 2,
  "mode": "compact",
  "desc": "One tight sentence: topic and current state.",
  "n": [
    {
      "id": "n1",
      "t": "F",
      "i": "h",
      "s": "Spring Boot 3.2, Java 21, MySQL. Maven. Constructor injection throughout.",
      "c": [
        { "id": "n1.1", "t": "A", "i": "m", "conf": 0.82, "s": "Assumed deploying to Linux server — all configs Unix-style paths." }
      ]
    },
    {
      "id": "n2",
      "t": "D",
      "i": "h",
      "st": "active",
      "s": "JWT auth chosen over sessions. JwtAuthFilter extends OncePerRequestFilter."
    },
    {
      "id": "n3",
      "t": "P",
      "i": "h",
      "st": "resolved",
      "s": "403 on all endpoints. Fix: .requestMatchers('/auth/**').permitAll() before anyRequest().authenticated()."
    },
    {
      "id": "n4",
      "t": "X",
      "i": "m",
      "st": "deferred",
      "s": "Refresh token support explicitly postponed."
    },
    {
      "id": "n5",
      "t": "G",
      "i": "h",
      "st": "active",
      "s": "Complete task CRUD endpoints with role-based access control."
    }
  ],
  "rel": [
    { "from": "n3", "to": "n2", "type": "caused_by" }
  ],
  "handoff": "Resuming Spring Boot JWT API. Stack: Java 21, MySQL, JPA. Auth working. N+1 fixed with @EntityGraph. Active goal: task CRUD with RBAC. Refresh tokens deferred."
}
```

After outputting JSON, print one line:
`~X tokens | Y nodes | Z relationships | estimated X% compression`

---

## READABLE Schema

Full field names, prose summaries, complete handoff prompt.

```json
{
  "context_graph": {
    "metadata": {
      "description": "...",
      "mode": "readable",
      "version": 2,
      "node_count": 6,
      "compressed_at": "ISO-8601"
    },
    "nodes": [
      {
        "id": "n1",
        "title": "Descriptive label",
        "type": "fact | decision | problem | goal | code | assumption | context",
        "importance": "high | medium | low",
        "status": "active | open | resolved | deferred | blocked | abandoned",
        "summary": "2–4 sentences. Dense, no filler.",
        "confidence": 0.95,
        "children": []
      }
    ],
    "relationships": [
      { "from": "n2", "to": "n5", "type": "depends_on" }
    ],
    "handoff_prompt": "You are resuming a conversation. Treat this graph as your working memory — prioritize nodes marked high importance and active/open status.\n\nCurrent state:\n- Active goals: ...\n- Open issues: ...\n- Deferred: ...\n\nFull graph: <paste JSON>\n\nAsk the user what they'd like to work on next."
  }
}
```

---

## Universal Compression Rules

| Rule | Detail |
|---|---|
| **Code verbatim** | Method names, class names, annotations, SQL — never paraphrase |
| **Keep negatives** | "Decided NOT to use Redis" is active state |
| **Versions exact** | Java 21 ≠ Java 17. Always preserve |
| **Superseded ≠ deleted** | Use `supersedes` + `abandoned` status instead of deletion |
| **Assumptions explicit** | If you inferred it, mark it `A` + add `conf` |
| **Status over recency** | A resolved old bug is less important than an open new one |
| **No tone** | Strip all conversational filler |
| **Open threads = nodes** | Never discard an unresolved question |

---

## Benchmarks (realistic ranges)

| Conversation | Input tokens | Output tokens | Nodes | Compression |
|---|---|---|---|---|
| Short debug session (10–20 turns) | 3k–8k | 200–400 | 2–4 | ~92–96% |
| Medium dev session (50–100 turns) | 15k–40k | 400–700 | 5–10 | ~97–98% |
| Long project session (200–400 turns) | 60k–150k | 600–1000 | 10–18 | ~99% |
| Chunked large session (400k+ tokens) | 400k+ | 800–1200 | 12–20 | ~99.7% |

These are estimates. Actual results depend on conversation density and topic variety.

---

## How to Use Output in a New Chat

```
Context from previous session:
<paste compact JSON here>

Resume from this state.
```

The new session treats the graph as working memory. Nodes marked `h` importance and `active`/`open`
status are the highest priority. Nodes marked `abandoned` signal things not to re-suggest.

---

## Extensibility

The `v` field and `meta` object allow future versions to add node types, relationship types, or
fields without breaking parsers that consume earlier versions.

```json
{ "v": 2, "meta": {} }
```

New node types and relationship types may be added in future versions. Parsers should treat unknown
values gracefully rather than erroring.

---

## Edge Cases

- **< 5 turns:** 1–2 nodes max. Skip relationships entirely.
- **Code-heavy session:** One `C` node per major class/method. Signatures verbatim.
- **Contradictions without explicit resolution:** Create both nodes, link with `related_to`, note the conflict in summaries.
- **Plain text input:** Treat as conversation. Same process.
- **Multiple unrelated topics:** Sibling root nodes. No forced hierarchy.
- **Assumptions with low confidence (< 0.6):** Drop the node entirely rather than publish unreliable state.

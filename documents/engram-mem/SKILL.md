---
name: engram-mem
description: Record and recall agent experience — decisions with rationale, gotchas and resolutions, validated procedures, stance updates. Trigger on "remember this", "learn from this session", "what did we decide about X", after a meaningful bug fix, or at the end of a substantive work session.
---

# engram-mem

Turn what just happened into durable memory. The agent does the extraction
and judgment; engram stores and recalls. Capture **decisions, gotchas,
procedures, and stances** — not transcripts.

This skill owns the *experience* substrates: memory records, procedures,
beliefs. Source-grounded knowledge (facts/entities/relationships from a
document) belongs to `engram-distill`; verbatim docs belong to
`engram-index`.

## Contract

1. No trivia: if a future agent wouldn't act on it, don't write it.
2. No duplicates: recall first; update or skip if it's already known.
3. Decisions record the *why*, not just the *what*.
4. Facts from a source doc don't go here — route them to `engram-distill`
   (source-keyed `store_knowledge`). Emergent, source-less observations
   may be written as memory, worded honestly ("observed in session; no doc").
5. Claims handed over by `engram-know` keep their evidence line verbatim.

## Workflow

### 1. What kind of learning is this?

| Kind | Tool | Shape |
|---|---|---|
| Decision + rationale | `write_memory` | "Decided X over Y because Z" |
| Gotcha / resolution | `write_memory` | "X bites when Y; fix: Z" |
| Validated procedure | `procedure_put` | exact steps that worked |
| Changed stance | `belief_get` → update or let contradiction stand | subject + new position |
| Verified finding (from engram-know) | `write_memory` | claim + evidence line |
| Fact from a source doc | → `engram-distill` | not this skill |
| Verbatim doc to recall | → `engram-index` (`index_docs`) | not this skill |

### 2. Recall before writing (dedup)

```
recall({ "query": "<the learning's key terms>" })
```

If it's already there: skip (nothing new), or write only the delta
("update: also fails on Windows"), or bump the procedure's accuracy by
re-putting it.

### 3. Write

```
write_memory({ "content": "Decided to gate npm publish on the scan gate: a package is the most-attacked surface (lesson: OpenClaw). Context: RFC-0021." })
```

```
procedure_put({ "name": "re-tag-release", "trigger": "publish retry",
  "steps": ["gh release delete vX --yes", "git tag -d vX",
            "git push origin :refs/tags/vX", "git tag vX", "git push origin vX"] })
```

For stance changes, check the belief state first:

```
belief_get({ "subject": "engram-index auto-triggers" })
```

If a belief contradicts the new learning, let the contradiction stand —
`contradiction_list` will surface the tension later. Never silently
overwrite a belief with history behind it.

### 4. Confirm

One read-back per critical write:

```
recall({ "query": "<the decision's core terms>" })
```

## When it fails

- `write_memory` errors → report; never retry in a loop.
- Nothing worth learning → say "nothing durable here" and stop. Silence
  is a valid outcome; forced learnings are noise.

## Anti-patterns

- Session-transcript dumps ("we ran tests, then edited X, then…").
- Duplicating what `recall` already returns.
- Unvalidated procedures (steps never executed).
- Belief overwrites that erase history.
- Writing source-doc facts here because distill wasn't loaded.

## Final check

- Would a future agent in a fresh session act differently because of these writes?
- Every decision has its why?
- Procedures were actually run?
- Source-backed content routed to distill/index instead?

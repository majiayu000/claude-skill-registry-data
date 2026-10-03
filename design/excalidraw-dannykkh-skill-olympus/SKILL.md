---
name: excalidraw
description: Work with .excalidraw and .excalidraw.json diagrams, including reading, explaining, comparing, creating, and editing them. Use context-isolated native agents for JSON-heavy operations when available, with a bounded sequential fallback when delegation is unavailable.
---

# Excalidraw Context-Isolated Operations

Excalidraw JSON has high token cost and low semantic density. Keep raw element metadata out of the
main conversation when possible, but do not make delegation a prerequisite for completing the task.

## Role Contract

Choose the role by side effect, not by a vendor-specific tool name.

| Operation | Semantic role | Contract |
|-----------|---------------|----------|
| Read, explain, compare | Read-only explorer | Read target diagrams; return only labels, relationships, and evidence. Do not write files. |
| Create, modify | General writer | Own only the designated output files; preserve unrelated elements; validate written JSON; report changed paths and checks. |

Use the current CLI's built-in explorer or general worker that satisfies the contract. Do not require a
custom agent name or assume a particular `Task`/spawn argument schema. The main context owns scope,
acceptance criteria, final verification, and the user-facing explanation.

If native delegation is unavailable or fails, perform the same operations sequentially in the main
context using the bounded fallback below. Never refuse an Excalidraw task solely because subagents are absent.

## Routing

1. Determine whether the request is read-only or writes a diagram.
2. Prefer native delegation when the file is large, multiple diagrams are involved, or the main context is already crowded.
3. Give the selected role exact input paths, allowed output paths, and the required return format.
4. Verify the result in the main context without importing raw JSON into the final response.

## Delegated Task Templates

### Read or Explain

```text
Role: read-only explorer
Task: Explain [file.excalidraw.json].

Extract text labels and relationships. Ignore visual metadata unless it changes meaning.
Return:
- components or steps
- connections and direction
- important visual grouping
- evidence by element label or id when useful
Do not modify files or return raw JSON.
```

### Compare

```text
Role: read-only explorer
Task: Compare [file1] and [file2].

Return semantic differences in components, flow, grouping, and missing or added relationships.
Do not modify files or reproduce full element objects.
```

### Modify

```text
Role: general writer
Task: Apply [requested change] to [file.excalidraw.json].
Allowed writes: [exact target path]

Preserve unrelated elements and style conventions. Validate that the result parses as JSON.
Return changed paths, a concise change summary, created or updated element ids, and validation results.
```

### Create

```text
Role: general writer
Task: Create [output.excalidraw.json] showing [description].
Allowed writes: [exact output path]

Use clear labels, readable grouping, and explicit arrows. Validate the completed JSON.
Return the output path, component summary, and validation results.
```

## Bounded Sequential Fallback

When no native agent can be delegated:

1. Inspect file size without printing file contents.
2. Process one diagram at a time.
3. For reading, parse JSON and emit only text labels, element ids, types, bindings, and minimal coordinates needed to infer relationships. Bound or page the extracted output.
4. For comparison, build a compact semantic summary for each file, discard raw payloads, then compare the summaries.
5. For creation or modification, write only the requested target, parse it again, and inspect the focused diff before reporting completion.
6. If a file exceeds a tool read limit, use an available JSON parser or a temporary local extraction command rather than loading the raw document into the conversation.

The fallback is sequential to prevent multiple verbose JSON documents from occupying the main context at once.

## Verification

For every write operation:

- Confirm the output parses as JSON.
- Confirm the top-level Excalidraw structure expected by the existing file or project is preserved.
- Inspect the focused diff for accidental deletion or unrelated style churn.
- Confirm every requested label and relationship exists.
- Report the exact output path and validation performed.

For read-only operations, return semantic content rather than raw JSON. Visual metadata matters only
when the question concerns layout, grouping, color, or position.

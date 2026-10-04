---
name: tracing-symbol-provenance
description: Traces where a variable's contents come from, as a dataflow diagram plus annotated code. Use for 'what's in X / who fills X'.
argument-hint: <symbol> [file:line]
allowed-tools: Bash(grep -n *), Bash(rg -n *), Bash(git blame *), Bash(git log *)
---

# Tracing Symbol Provenance

Answer "what does X contain, and who populates it" by showing where information
**enters** X — not where X is copied. The deliverable is a stage-level dataflow
diagram with numbered markers, and a verbatim, annotated snippet for each marker.

## The trap

The first-draft answer lists the assignments to X (`x = y` at line A, `x = z` at
line B). That is tautological: it moves the question to `y` and `z`. Keep following
copies until every branch ends at a line that **adds information** — an external
source (log, sensor, file, network), or a write that inserts, appends, computes, or
parses. Those lines are the answer; the copies are the route between them.

## Workflow

1. **Pin the symbol** at the line the user named. Note its type, since that tells you
   what one element holds.
2. **Classify every write.** Grep the name. Sort hits into
   - *moves*: assignment from another variable, `std::move`, passing as an argument,
     copying into or out of a message field;
   - *information-adding writes*: insert, append, compute, parse from input.
3. **Follow moves upstream across renames** (local → message field → struct member →
   parameter) until each branch reaches an information-adding write or an external
   source. Record every name the data takes on the way.
4. **Follow downstream** to the consumer the user cares about, and check whether the
   symbol itself is ever serialized or is only working material.
5. **Separate the data from the tool that builds it.** A buffer, builder, or cache
   object and the container it hands out are different things. Say which is which
   (for example, a buffer's internal table returned by reference).
6. **Choose the diagram's level of abstraction:** the stages that pass data to each
   other (graph nodes, processes, pipeline stages). A component inside a stage is an
   annotation on that stage, not its own box. Find the edges in code. If they are
   implicit (publish/subscribe by message type), say so and cite the subscriptions.
7. **Verify** every `path:line` with `grep -n` before citing it. If the user asks
   whether something predates a change, `git blame` the lines and give each layer
   its author and commit.
8. **Write the answer** in the format below.
9. If a live nvim session is available, push the markers as a quickfix list in
   marker order (see the `pointing-to-code` skill).

## Output format

Sensible default; adjust section count to the symbol.

**Things to know first** (one to three). Each is a plain idea first, then a
*Names:* line mapping it to identifiers and `path:line`. Typically: what one
element of X is, and what the building tool is.

**Diagram.** ASCII. The external source goes at the top, the final consumer or disk at
the bottom, and each stage is a labeled block. Place ①…⑦ at every point where X
exists or changes. Mark the bottom `← X is NOT written` if it is working material.

**Table:** marker | what X is at this point (container and name) | contents | `path:line`.

**Step by step.** One block per marker:

````markdown
**① <stage>: <what happens here, in plain words>.**

```cpp
// path/to/file.cc:NN
  verbatim line
  ...
  verbatim line                                  // ← the information this adds
```

Contents: <only when they change at this marker>.
````

**Takeaways** (two or three bullets): how many builders X has, where X crosses from
one stage to another, and whether X is output or working material.

## Rules

- Snippets are verbatim, trimmed with `...`. Put explanations in trailing `// ←`
  comments, never by rewriting code.
- Every marker appears in the diagram, the table, and a snippet block. A marker with
  no code (for example, "parked, waits 12 s") still gets a line saying so.
- Call out both *same name, different object* and *different name, same object*.
- Plain idea before project jargon. Name things by what they do; attach the internal
  name afterwards.
- Keep it local: about eight markers at most. If there are more, split by builder
  and deliver one builder per message.
- Label inference as inference. Everything cited should be verified.

## Worked example

`references/case-study-merged-tracks.md` shows the tautological first answer and the
version the user asked to have captured as this skill. Read it the first time you use
this skill in a session.

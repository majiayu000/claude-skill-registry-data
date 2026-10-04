---
name: issue
description: "Open a GitHub issue (or epic) from the locked architecture using a Linear + Shape Up + Larson-synthesized structure. Header (Owner · Appetite · Status · Part of), Problem, Outcome, Solution sketch with ASCII diagrams and code contracts, Files, Acceptance criteria, Rabbit holes, No-gos, References, Depends on. No mermaid. Hands off to /work."
---

# /issue

Before rendering user-facing output, read `../_shared/plain-output.md` and `../_shared/ascii-diagrams.md`.

Open a GitHub issue that captures the locked architecture.

The issue is the durable architectural contract for the implementation cycle. It is **not** a task list — `/work` owns the task list.

## Preconditions

- A locked architecture must exist in conversation context (from `/architect` + `/review`).
- If no locked architecture exists, tell the user to run `/architect` and `/review` first, then stop.
- `gh` must be authenticated: `gh auth status`.
- If authentication fails, tell the user to run `gh auth login` and stop.

## Why this structure

The Linear Method (Saarinen et al.), Shape Up (Singer / Fried / DHH at Basecamp), Will Larson's design-doc guidance, and Atlassian's epic-vs-story practice all converge on the same four invariants:

1. **A named owner** — Linear: every issue and project has one accountable human.
2. **An appetite, not an estimate** — Shape Up: time is a design constraint ("worth two weeks"), not a forecast.
3. **Specific rabbit holes with boundaries** — Shape Up: pre-empted time-wasters save weeks.
4. **Explicit no-gos** — Shape Up: what is intentionally out of scope makes drift visible later.

Plus: short titles, plain language, testable acceptance criteria, one screen of body where possible, code examples beat prose for contracts.

## Process

1. Read the locked architecture from conversation context.
2. Derive a short, imperative issue title under 70 characters.
3. Assemble the issue body using the template below. Default to Plain Senior; aim for one to two screens.
4. Write the body to a temp file:

   ```bash
   BODY_FILE="$(mktemp -t issue-body-XXXXXX.md)"
   ```

5. Create the issue:

   ```bash
   gh issue create --title "<title>" --body-file "$BODY_FILE"
   ```

6. Capture the printed issue URL and the issue number.
7. Delete the temp file.
8. Print the issue URL and number.

For an **epic**, add `--label epic` and after creating capture the number so children can reference it as `Part of #<epic>`. Create children with their `Part of #<epic>` line in the header, then `gh issue edit <epic>` once to insert the child checklist.

## Issue body template

Use this exact structure. Section order is fixed. Skip a section only if it genuinely does not apply (e.g. an epic has no `Depends on` of its own).

````markdown
**Owner:** @<github-handle>
**Appetite:** <time-box, e.g. "1.5 weeks" — not an estimate>
**Status:** <Triage | Shaped | Ready | In Progress | Blocked>
**Part of:** #<parent-epic-number>   <!-- omit on the epic itself -->

## Problem

<One tight paragraph in plain language. What hurts, who feels it, what invariant is at risk, and what must remain true. First-principles framing. No solution language here.>

## Outcome

<Observable bullets — what "done" looks like. What can be demonstrated, not what was built.>

- <observable thing>
- <observable thing>
- <observable thing>

## Solution sketch

<One or two paragraphs at the "fat marker" level — the architectural shape, not the recipe.>

```
<ASCII module/flow diagram — see ../_shared/ascii-diagrams.md for patterns>
```

<For lifecycle, add a second ASCII state diagram.>

```ts
// Public contract — types and signatures only, not implementation.
export type <Name> = {
  readonly <method>: (<input>) => <Effect.Effect<Output, Error>>
  // …
}
```

## Files

**Create**
- `path/to/new/file.ts` — one-line purpose
- `path/to/another.ts`

**Modify**
- `path/to/existing.ts` — one-line change

## Acceptance criteria

- [ ] Independent, testable statement of observable behavior.
- [ ] Independent, testable statement.
- [ ] Independent, testable statement.
- [ ] `bun run check` (or equivalent) is clean.

## Rabbit holes

- **Named trap.** What the boundary is. Why it matters.
- **Named trap.** What the boundary is.
- **Named trap.** What the boundary is.

## No-gos

- Explicit exclusion.
- Explicit exclusion.

## References

- `path/to/mirror.ts` — pattern to copy.
- External: <link> — research or doc citation.

## Depends on

#<issue-number> — one-line reason.   <!-- "None." if unblocked -->
````

## Epic-only additions

For epics, replace `Depends on` with `Children`:

````markdown
## Children

- [ ] #N — child issue (appetite)
- [ ] #N — child issue (appetite)
- [ ] #N — child issue (appetite · depends on #X)
````

## Title rules

- Imperative: "Add peer messaging broker", not "Peer messaging broker addition".
- Under 70 characters.
- No issue number prefix.
- No trailing period.
- No emoji.
- Plain language. No internal jargon.

## ASCII diagram rules

- Use ASCII, never mermaid. See `../_shared/ascii-diagrams.md` for the character palette and pattern catalog.
- Keep diagrams under 80 chars wide.
- One module/flow diagram per issue is usually enough. Add a state diagram only when the thing has lifecycle.
- Wrap the diagram in a fenced ``` ``` block so whitespace is preserved.

## Heredoc invocation pattern

Always use a temp file rather than inlining the body. ASCII diagrams contain box-drawing characters that survive heredocs fine; the temp file pattern is just safer for any non-trivial body.

```bash
BODY_FILE="$(mktemp -t issue-body-XXXXXX.md)"
cat > "$BODY_FILE" <<'EOF'
**Owner:** @example
**Appetite:** 1 week
**Status:** Ready
**Part of:** #100

## Problem

…

EOF

gh issue create --title "<title>" --body-file "$BODY_FILE"
rm "$BODY_FILE"
```

## What NOT to include

- No "Changes" section.
- No "Implementation steps."
- No checklist test plan beyond Acceptance criteria.
- No emojis in headers.
- No speculative future work.
- No design alternatives — those belong in `/architect` and `/review`.
- No mermaid.

## Output

Use Plain Senior output with the issue URL, the issue number, and the exact next command.

```bash
/work <issue#>
```

Then end with exactly this line and stop:

> Issue created: <url>. Run `/work <issue#>` to start implementation on the current branch.

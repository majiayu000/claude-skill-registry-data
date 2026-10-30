---
name: comments
description: How to write code comments in this repo. Use whenever writing or editing comments in any code — apply automatically, not just when invoked. Comments are local clarifications of non-obvious code, never process narratives, doc-block summaries, or records of changes made.
---

# Comments

A comment earns its place only by saying something the code at that spot cannot
say for itself. If a reader who knows the language could learn the same fact by
reading the adjacent lines, the comment is noise — delete it.

Apply this whenever you write or edit code. When you edit a file, also clean up
existing over-commenting throughout that file (see [Cleanup](#cleanup-when-editing)).

## The one rule

**A comment must be additive at the point where it sits.** It explains *why this
specific line is the way it is* — a non-obvious constraint, a counter-intuitive
choice, a gotcha, a reason the easy thing wasn't done. It does not narrate, it
does not summarize, it does not document the system.

## Never write these

1. **Process / flow narratives.** Comments that describe the overall sequence of
   what happens ("first we migrate, then we seed, then services boot..."). That
   belongs in `docs/`, not inline. The code already shows the flow.
2. **Doc-block summaries on functions.** Do not add a `/** ... */` block that
   restates what a function does or walks through its steps. Only write a doc
   block when the *contract* is genuinely non-obvious (a surprising precondition,
   an invariant the caller must uphold, units/ownership that aren't in the types).
   A short, readable function needs no block at all.
3. **Cross-system comparisons.** "the dev analogue of the production job", "mirrors
   what X does" — architectural context lives in docs, not in the file.
4. **Asserted design facts.** "There are NO special-cased services",
   "This is the single source of truth" — these decay and aren't checkable.
5. **Records of changes made.** "Changed from X to Y", "Refactored to...",
   "Previously this used...". Git history is the changelog. **One exception:**
   a comment explaining a shim/quirk kept *for backwards compatibility* — that's
   additive, because it explains why dead-looking code must stay.
6. **Restating the obvious.** `// loop over services`, `// import helper`,
   `// set the port`.

## Do write these

- A non-obvious *why*: `// --no-deps so compose doesn't start peer services mid-bootstrap`
- A constraint that isn't visible locally: `// A block body: a function returned from beforeEach runs as cleanup.`
- A gotcha or footgun: `// isAxiosError, not instanceof: @dianemo/core may bring its own copy of axios`
- A backwards-compat reason to keep something: `// kept for v1 clients that still send the legacy field`

Keep them short — usually one line. If you need a paragraph to explain a line,
the explanation probably belongs in `docs/` with a one-line pointer.

## Worked example

An illustrative process entry point, the kind of file this habit grows in.

❌ **Before** — a process narrative, a cross-system comparison, and asserted
design facts. None of it is local to the code below it; all of it belongs in docs.

```ts
/**
 * Process entry point — the counterpart of the image's CMD and the compose
 * `core` service. Depending on ROLE it starts the API, the worker, or both,
 * EXACTLY as in production: keys are loaded FIRST, then the declaration is
 * registered, then the HTTP server listens...
 *
 * There are NO role-specific code paths outside this file. The worker and the
 * API share the same db object and the same env schema; their health checks...
 * [20+ more lines]
 */
async function main(): Promise<void> {
```

✅ **After** — the narrative moves to `docs/`, leaving only locally-additive
notes on the two genuinely non-obvious lines.

```ts
// Before anything signs, verifies or decrypts: the first start generates the keys.
await loadKeys();
```

```ts
// The worker has no API to hang /health on, so it answers on a port of its own.
if (env.ROLE === "worker") startWorkerHealth(env.WORKER_HEALTH_PORT);
```

The function name and its short body already tell the reader what it does. What
they *couldn't* know is why `loadKeys()` must come first and why the worker
needs its own port — so those are the only comments that survive.

## Cleanup when editing

When you touch a file, treat its existing comments by the same rule and strip the
ones that violate it, even in sections you didn't otherwise change. Don't preserve
a process narrative or a "// changed to..." note just because it was already there.
(This is intentionally aggressive — the goal is files trend toward clean over time.)
If removing comments would make a genuinely subtle section unclear, replace the
block with one local line rather than deleting outright.

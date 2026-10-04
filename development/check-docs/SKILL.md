---
name: check-docs
description: Use when a code decision hinges on how a pinned external library, framework, API or service behaves, and a wrong recalled answer would still compile or type-check yet fail at runtime. Not for what the repository's own code answers, a version bump alone, or a concept explanation.
argument-hint: <library, version and question>
effort: high
---

# Research

Confirm external behavior against the current source instead of recalling it.
The enemy is the version-specific detail recalled with confidence, wrong in the way that compiles and fails at runtime.
The overcorrection is researching a call the repository already makes elsewhere in deployed code: for what that code does today, working code outranks a fresh fetch.

## When to use

- A code decision depends on how a pinned external version behaves, and a wrong answer would still compile or type-check.
- Not for a question the repository's own code answers, a version-only bump, or a concept with no version dependency.

## The loop

1. **Find the installed version** in the lockfile or manifest first, because the question is how this pinned version behaves, not how the library works.
2. **Fetch that version's first-party docs**, changelog or migration guide, never a blog post; without an exact match use the highest documented version not newer than the install, else the lowest newer one, and state both versions.
3. **Fetch only the section that answers the question** and quote at most ten lines, because a page read once is re-read every later turn.
4. **Cite every claim that shaped a decision** with its URL; an uncited claim is a recollection and is flagged as one.
5. **State what could not be confirmed** instead of filling the gap: "could not confirm X; proceeding on Y" is a valid outcome.

## Where this runs

- Dispatch the `exo:fetch-docs` agent with the question alone: the library, its pinned version and what to confirm, or the document paths.
- The agent holds the budget, the stop rule and the report shape, so the dispatch repeats none of them; the `exo:locate-code` agent owns the repository.
- Read here only when no separate context exists, one page at a time.
- Hand back the confirmed facts, their citations and the unconfirmed remainder, never the pages.

## Output

Findings stay in the message, and the turn ends under the closing rule in `route-skills`: the confirmed answer first, its citations next, then what stayed unconfirmed.
Write `docs/research/<library>.md` only when the user asks for a file, or a named later executor needs the findings and they rest on two or more first-party sources.

## Red flags

| The excuse | What holds |
|---|---|
| "I know this API." | Knowing the concept is not knowing this version; read the lockfile. |
| "The latest docs will do." | The install is older; the answer diverges across minor versions. |
| "I'll paste the page for context." | Ten quoted lines and a URL; the page costs every later turn. |

## Judgment

- For what deployed code does today, the repository's working code outranks fetched docs; for code written or upgraded now, the pinned or target version's docs outrank a pattern the source marks deprecated or unsafe, and unrelated code is not modernized.
- Never end a turn on a research pass alone. It unblocks a `spec`, `build` or `find-cause` step in progress: hand the findings back and the step continues; a standalone question with no code to follow ends the turn on the findings, as under Output.
- After a compaction notice, restate the facts from the delegated report or the research file, or repeat the delegated read; recollection is not research.

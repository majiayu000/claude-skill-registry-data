---
name: documentation
description: "ALWAYS invoke for any task involving docstrings, JSDoc/TSDoc, or REST API documentation — even when the request seems handleable without it. Enforces Microsoft contract-first conventions and a bare-minimum rule that Claude won't apply by default: never restate the signature, drop @param/@returns that only echo names and types, always document @throws, and document data shapes as WHAT not WHY. Covers Python docstring styles (Google/NumPy/Sphinx), TSDoc tags and @inheritDoc, and API doc patterns for NestJS/Express/FastAPI/Django. Trigger on: adding or auditing docstrings, redundant or missing tags, deleting comment rot, or producing a documentation-health report. Do not skip for documentation tasks — consistent conventions are the whole point."
---

# Documentation

Microsoft contract-first conventions. Documentation states the **contract** — what something does and why — never how it works inside.

## Why the rules are subtractive

Code changes; the comment beside it usually does not. Over time documentation lies, and readers trust it anyway — a stale comment is worse than no comment, because it actively misleads. Two habits follow, and every rule below is one of them applied:

**Keep the surface small.** Less prose has less to rot. A comment is a last resort, not a first step: before writing one, ask whether a sharper name, a smaller function, or a named type would carry the meaning instead. Prose is for the residue that code genuinely cannot express.

**Keep each fact in one place,** next to the code that owns it, so there is exactly one thing to update. When the signature, the type, or a test already states something, the prose must not restate it.

## The bare-minimum rule

The signature already carries the name, parameter names and types, return type, and modifiers (`readonly`, `?`, `async`). Documentation adds only what a reader cannot infer from it: intent, units, ranges, defaults, edge-value meaning, error cases, invariants.

Every public member still gets a brief summary, so generated docs and IDE tooltips have content — one short sentence carrying intent, never a paraphrase of the signature.

For `@param` and `@returns` specifically, **drop the tag entirely when it would only restate the signature.** A tag earns its place when it answers: what unit? what range or clamp? what default when omitted? what does an edge value mean (`0` disables, `-1` unlimited, empty = all)? what does `null` signify versus throwing?

`@throws` is the opposite default — document it whenever code can throw, because the throw set is invisible from the signature.

## The shape of a doc block

A doc block is read in an IDE tooltip, a hover card, a code-review diff — surfaces that show the opening and truncate the rest. So the budget is counted in **rendered lines**, not sentences:

- **Summary — exactly one line.** One sentence carrying intent, alone at the top of the block. Never two lines, never two sentences.
- **Detail — three lines at most**, after a blank line, and only when the summary genuinely cannot carry the contract. Primary ideas only: what the operation does and the constraint that governs it, not how it branches.
- **Inline `//` or `#` comments — three lines at most, one preferred.**

Overflow is not fixed by reflowing; it means the content is in the wrong place. Branch-by-branch behaviour, edge cases, and the reasoning behind a constraint go to `@remarks` (`Note:` / `Notes` in Python), which exists so the opening of the block stays readable.

**Measure after the formatter, not before.** Write the block, let the project's formatter reflow it at the configured width (detection order under Conventions), then count the lines it produced. A summary that came back wrapped onto two lines is over budget: cut words until it fits on one — do not split it into a second sentence, because that sentence is detail wearing the summary's clothes. The same check applies to an inline comment that a formatter or `max-len` rule pushed past three lines.

## How the prose reads

Every sentence you produce here — summaries, the `@param` notes that survive, `@throws` conditions, endpoint descriptions — gets read mid-debug by someone who may not share your first language. Load the `simple-english` skill at practical depth (`/cortex-communication:simple-english practical`) and hold its rules while you write. Reach for it before the first doc block, not as a cleanup pass: rewriting prose you already committed to costs more than writing it right once.

What it changes in a doc block specifically:

- **One word per concept, file-wide.** A `@param` that says "validate" beside a summary that says "check" reads as two different operations, and the reader goes looking for the difference.
- **25 words for a descriptive sentence, 20 for an imperative one.** A summary past that is carrying more than one fact and belongs in `@remarks`. At a typical width the one-line budget binds first, so treat the word counts as the ceiling and the rendered line as the test.
- **`can`, `will`, `must` — never `should`.** A contract that says a caller "should" pass a sorted array leaves the reader guessing whether the rule binds. Say `must`, or state what happens when they do not.
- **Condition before consequence.** "If `retries` is `0`, the call fails immediately" beats the reverse ordering, because the reader knows whether the sentence applies to them before they parse the outcome.
- **No adjective without a measurement behind it.** "Efficiently caches" earns nothing. Give the bound or drop the word.

Identifiers, code samples, and quoted error strings stay exact — the standard treats them as technical names, and a reader who copies a "corrected" one gets a new error.

## Conventions

- **Third-person summaries for code symbols** — "Calculates…", "Finds…", "Initializes a new…" — matching Microsoft API reference convention. Two exceptions keep the imperative: inline `//` comments on procedural steps, and API operation `summary` fields (OpenAPI, `@ApiOperation`, `extend_schema`), where "Create a new user" is the established form.
- **Interfaces document the abstraction**: purpose, thrown errors, return semantics, invariants. Implementation detail (caching, queries, algorithms) belongs in the implementation — a consumer reading the interface should not learn things that a refactor can invalidate.
- **Data shapes answer WHAT, not WHY.** A DTO, record, struct, or the `interface`/`type` describing it documents what each member _is_ — meaning, units, format, allowed values, constraints the type can't carry. It does not justify why the field exists. A function's contract genuinely includes the why of the operation; a data field is read at the point of use, where design rationale ("kept so billing can reconcile…") rots and belongs instead with the behaviour that produces or consumes it. The escape hatch — a non-obvious constraint a maintainer must not break — is a sparing `@remarks`, never the default voice.
- **Don't repeat the interface on the implementation.** Inherit (`@inheritDoc`, or the language's equivalent) and add only implementation-specific notes.
- **Multi-line doc blocks only.** Every `/**` puts its body on a new line; one-line `/** … */` is not allowed.
- **No release tags** (`@public`, `@beta`, `@alpha`, `@internal`) unless explicitly requested.
- **Ship only examples the test suite runs.** An unexecuted example drifts and becomes one more comment that lies. Python doctests qualify when run (`pytest --doctest-modules`); TSDoc `@example` blocks are never executed by tooling, so omit them and let tests carry behaviour.
- **Wrap at the project's configured width.** Detect in order: `.editorconfig` `max_line_length` → formatter config (`printWidth`, `line-length`) → linter config (`max-len`, `max-line-length`). Fall back to 80 only when none define one.

## Comments to delete on sight

When auditing, removing these is as much the job as filling gaps — each is a place where truth can drift:

- **Commented-out code** — version control already remembers it, and leaving it makes readers wonder if it still matters.
- **Journal or changelog comments** ("2024-03 added retry logic") — `git log` keeps this accurate.
- **Attribution bylines** ("added by …") — `git blame` answers it without rotting.
- **Banners, position markers, closing-brace labels** (`// ===== helpers =====`, `} // end if`) — structure should come from the code.
- **Anything restating the name, type, or signature**, or stating the obvious (`/** Default constructor */`).

## Working a documentation task

Ask which format the project uses before starting (or detect it from existing files), and detect the framework — the API doc strategy differs per framework and applying the wrong one produces a spec nobody consumes.

Report on **health, not headcount**. A file where every member has a doc block is not the goal if half of those blocks restate signatures. Report what improved: redundancy removed, stale docs corrected, intent summaries and `@throws` added. Coverage percentage is a floor signal — it finds empty members and cannot tell a valuable block from a vacuous one.

## References

| Reference | Load when |
| --- | --- |
| `references/python-docstrings.md` | Python — Google, NumPy, or Sphinx style |
| `references/typescript-jsdoc.md` | TypeScript/JavaScript — TSDoc tags, `@inheritDoc`, formatting |
| `references/api-docs.md` | REST API docs — NestJS, Express, FastAPI, Django |
| `references/coverage-reports.md` | Auditing docs; producing a documentation-health report |

---
name: writing-docstrings
description: Use when writing, rewriting, or auditing Python docstrings that a documentation site is generated from, or when docstrings are long, narrate the code, or leave a reader of the generated reference unable to find their way. Triggers - "audit the docstrings", "docstring slop", "docstrings as documentation", "the API reference reads badly", "rewrite these docstrings".
---

# Writing Docstrings

Docstrings that a site is generated from are the product's documentation.
Each one states what a reader needs, in a fixed place, in plain language.

## When to Use

- A documentation site (great-docs, quartodoc, mkdocstrings, Sphinx autodoc) renders the package's docstrings.
- An audit of docstrings for length, body narration, rationale, history, or vague wording.
- A rewrite of docstrings after an API change, where the reference must stay accurate.
- A new public function, class, or module needs a docstring that matches the rest.

## When Not to Use

- Comments inside a body, or slop in code: use `simplify`.
- Narrative documentation pages, tutorials, or a docs site built from prose: use `scaffold-docs`.
- Commit messages: use `commit-message`.

## Invocation Notice

- Tell the user when this skill is running: `writing-docstrings`.
  Skip the notice when the user asked for the skill by name or slash command; spelling and spacing need not match.
  A phrase from this skill's own trigger list is not a name — naming the work is not naming the skill.

## Workflow

1. Find what the site renders.
   Read the docs configuration for the parser and for the objects that get pages.
   A docstring of an object without a page is a maintainer note, not documentation.
   When the configuration does not settle it, probe the renderer with a throwaway package (`references/renderer-probe.md`).
2. Classify each docstring by level: landing page, module page, class, function or method, or not rendered.
   The level sets the register and the shape (`references/shape.md`).
3. Calibrate with the user before any bulk edit.
   Bring three docstrings at a time, of different levels or kinds.
   For each, quote it, give a verdict, name what fails, and show the rewrite.
   Use length only as a first filter: a long docstring can be all contract, and a short one can be too dense to read.
   Continue until the user agrees with the verdicts.
4. Write or rewrite to the shape and the register (`references/register.md`).
   Verify every fact against the code before you state it; read the body, the tests, or run it.
   Add a missing contract fact, such as a default or an error, when a reader needs it.
5. For more than about 30 docstrings, run the work in parallel with separate review sweeps (`references/parallel-run.md`).
6. Rebuild the site, or the renderer probe, and check that sections, links, and examples render.

## Output

- Rewritten docstrings, each true against the code and placed in the shape for its level.
- Body comments for rationale that guards against a wrong fix; other rationale deleted.
- Documentation-site configuration changes, when module pages or sections need them.

## References

- `references/shape.md`: the labeled sections and the shape for each level.
- `references/register.md`: reference and explanation registers, plain language, and what to keep and cut.
- `references/examples.md`: calibrated before-and-after examples.
- `references/renderer-probe.md`: how to check what a renderer does with a docstring.
- `references/parallel-run.md`: writer brief, batching, and review sweeps.

---
name: thermo-nuclear-code-quality-review
description: Run an unusually strict maintainability review for abstraction quality, giant files, and spaghetti growth.
---

# Thermo-Nuclear Code Quality Review

An unusually strict review of the current branch's changes. The bar is not "does it work" — it is "does this leave the codebase simpler than a competent author would have left it."

Above all, be **ambitious**. Do not stop at local cleanup. Hunt for the **code judo** move: a restructuring that preserves behavior while making whole branches, helpers, modes, or layers *disappear*. Prefer deleting complexity over rearranging it. Prefer the version that makes the change feel inevitable in hindsight. Assume a code-judo move is usually available and look for it before you accept the code as-is.

## The standards

Each rule below is one smell, its remedy, and a ready-to-paste phrase. These are presumptive blockers — the author must justify them, not you.

1. **A file crossing 1000 lines.** Treat a diff that pushes a file from under 1k to over 1k as a strong smell. Extract helpers, subcomponents, or modules first. Waive only for a compelling structural reason where the result is still clearly organized.
   > `this pushes the file past 1k lines. can we decompose this first?`

2. **Spaghetti growth.** Ad-hoc conditionals, scattered special cases, or one-off branches bolted into unrelated flows. Push the logic into a dedicated helper, state machine, policy object, or module instead of tangling an existing path.
   > `this adds another special-case branch into an already busy flow. can we move this behind its own abstraction?`

3. **Magic over boring.** Brittle, clever, or generic mechanisms that hide simple data-shape assumptions. Also thin wrappers, identity abstractions, and pass-through helpers that add indirection without buying clarity. Prefer direct, boring, maintainable code.
   > `this abstraction seems unnecessary. can we just keep the direct flow?`

4. **Dirty type boundaries.** Unnecessary `any`, `unknown`, casts, or optionality; silent fallbacks that paper over an unclear invariant. Make the boundary explicit so the control flow gets simpler.
   > `why does this need a cast / optional here? can we make the boundary more explicit instead?`

5. **Logic in the wrong layer.** Feature logic leaking into shared paths, implementation details leaking through APIs, or a bespoke helper where a canonical one already exists. Move logic to the package that owns the concept; reuse the canonical utility.
   > `this looks like a bespoke helper for something we already have elsewhere. can we reuse the canonical one?`

6. **Avoidable orchestration.** Independent work serialized for no reason, or related updates that can leave state half-applied. Push toward parallel or atomic structure when that also makes the code simpler — don't over-index on micro-optimizations.
   > `can these run in parallel / be made atomic? the sequential version is more brittle here.`

7. **Refactors that move complexity without deleting it.** A "cleaner" version of the same messy idea, or a rearrangement that doesn't reduce the number of concepts a reader must hold. Push for the simpler *model*, not a tidier mess.
   > `this refactor moves complexity around but doesn't delete it. is there a way to make the model itself simpler?`

## Output

Return findings in the response. Do not post review comments unless explicitly asked.

Lead with the largest structural issues; do not flood the review with low-value nits when bigger problems exist. Prefer a few high-conviction comments over a long cosmetic list. Order findings:

1. Structural regressions and missed code-judo simplifications
2. Spaghetti / branching growth (rule 2)
3. Boundary, type, and abstraction problems (rules 3–4)
4. Wrong-layer and duplication problems (rule 5)
5. File-size and decomposition (rule 1)
6. Orchestration brittleness (rule 6)

## Tone and approval

Be direct, serious, and demanding — not rude. Do not soften a major maintainability issue into a mild suggestion. If the code makes the codebase messier, say so. If it missed an obvious dramatic simplification, say that too.

Do not approve on "behavior seems correct." Withhold approval while any rule above fires with a plausible cleaner path and no clear justification. When a rule fires, leave explicit, actionable feedback and push for the cleaner decomposition.

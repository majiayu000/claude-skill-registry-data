---
name: simplify
description: "Use when the code a piece of work changed is to be cut back to fewer lines, behaviour unchanged: a commit range (`<base>..<head>`) whose changes left old paths, unused code or a second implementation behind, a path the work just replaced, one family handed over by a simplify-rework audit, or a run's simplify phase. Produces each superseded path deleted and each duplicate consolidated, one narrow pass each, tests green, net lines negative, and a short summary. Not for auditing a whole codebase (simplify-rework), branching complexity (complexity-rework) or an interface's shape (deepen-module)."
---

# Simplify

**The range is the context.** A commit range's diff and messages say what each change replaced, so the pass reads them instead of exploring, and needs nobody's memory. Delete, never rewrite.

## Steps

0. **The baseline**: the full test suite, and the verify that judged the work where there is one, run on `<head>` before any cut, their results kept. Parity means the same steps give the same results after; without the before, a failure after cannot be laid on the cuts.
1. **Read the range**: `git log <base>..<head>` and its diff. List each candidate: an old path a change superseded, code the range left without a caller (a name search outside its file finds none), two implementations of one concern. Check each one's reach as the `simplify-rework` skill's `references/audit.md` says under *Reach*; a reached candidate is dropped.
2. **One pass per candidate**: a superseded or dead path as `references/path.md` says, a duplicate as `references/consolidate.md` says. Candidates touching no common file run in parallel, each in its own worktree.
3. **Net lines** per pass with this skill's `scripts/net-lines.mjs`. A pass that did not go negative is reverted, not argued.
4. **Parity**: the full suite, not the narrow tests (a removal breaks code far from the files it touched, and only the full suite sees that), then the verify of step 0 again. **A verify is highly recommended even where the work had none**: removal breaks callers no test reaches (a load by string, an entry point by convention, wording a reader sees), and the verify re-runs what held before. It needs no verify skill: the steps are written on the spot, what to check and how, from the last verify's steps or the range's done-whens. A pass that broke parity is reverted, never patched: it has already cost more than it saved, and a patch turns a removal into a rewrite.
5. **The summary**, short and scannable: one row per pass (what went, why, its commit, lines added and deleted), the total, parity (suite and verify, before and after, or "parity not verified"), and what was left and why.

## Rules

- **A pass is one candidate.** Two in one diff make a change no reviewer can attribute.
- **Removals run on a cheaper model, consolidations on a strong one.** The survivor choice is judgment.
- **Add no dependency without the person's yes.**
- **Stay inside the range's files and what they reach.** A finding beyond it is named in the summary, for the `simplify-rework` skill.

## Red flags

| Thought | Reality |
|---|---|
| "I'll grep around and see what looks unused" | Exploration. The range names its candidates; read it. |
| "While removing this I'll simplify the survivor" | A second change in the same diff. Its own pass. |
| "Both implementations are fine, keep both" | Two copies of one concern drift. Choose, or record why each is a different concern. |

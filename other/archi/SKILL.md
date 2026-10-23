---
name: archi
description: Use when the spec is locked down, before the plan, map what already exists and where the feature plugs in, to avoid duplication.
---

# archi

Step 3 of the pipeline (`WORKFLOW.md`). The step that **avoids duplicates**: agreeing on the
target architecture by looking at the real code.

## When
After `spec`, before `/PLAN`. Systematic as soon as we touch shared code or an existing domain.

## Steps
1. **Get a map of what exists** in the worktree(s) concerned, before searching for anything
   specific. The directory tree plus the entry points is always available and is what this step
   actually requires. Naming a tool as the first action was a rule-B break hiding in plain sight:
   the step is *have a map*, and a consumer with no tooling must still be able to clear it.
   1. Where tooling exists, prefer **an index built from the code on demand** — an AST/structural
      search that answers per query — over **a graph built once into an artefact**. The artefact
      form has a staleness problem the index form does not have at all: a graph directory is right
      the day it is generated and quietly wrong afterwards, and refreshing it costs a whole pass.
      (`claude-mem`'s `smart-explore` is the index form here, `graphify` the artefact form.)
      When a stored graph is used anyway, check its freshness: resolve the stored commit hash
      (`git rev-parse --verify`), then list the project's changes since it with
      `git diff --name-only <hash> HEAD -- .`. The `-- .` pathspec keeps a commit in a sibling project
      of a monorepo from staling this graph. A different hash with an empty diff is not stale. Ignore the
      graph's own output folder in every command. A hash that does not resolve is a warning, never a
      block.
   2. **Do not narrow the scan to the module you are touching.** It is cheaper and it removes the
      one thing this step exists to prevent: the near-duplicate that lives in *another* module is
      exactly the one nobody finds, and scoping the map to your own module makes step 2 blind
      precisely where duplicates come from. Cheap comes from the index form, not from a smaller
      scope.
2. **Dedup pass, before deciding anything.** Search on *what the thing does*, not on what you'd
   name it: your name for it is exactly the name the existing one doesn't have, which is why
   duplicates get written by people who did look first.
   1. List the **capabilities** the feature needs, in domain words ("filter a list by agency",
      "format a duration", "resolve the current tenant"), one line each.
   2. For each one, search three ways, because each misses what the others catch: by **name**
      (the obvious synonyms), by **signature/shape** (the types going in and out), and by **call
      site** (who would already need this — search the consumers, not the producer).
   3. Read the candidates you find. A near-match is a decision, not a miss: either it covers the
      need (reuse it), or it covers 80% (extend it, and say what the extension is), or the
      difference is real (create, and write down why the existing one doesn't fit).
   4. **Record the negative result too.** "Searched for X as name/shape/callers, found nothing"
      is the evidence that justifies creating. Without it, "there was nothing" is a claim, and
      the duplicate that shows up in review had a findable original.
3. Decide **where the feature plugs in** (reuse vs create), note the extension points.
   Where a tool produces a **cross-cutting duplication report with citations** (`claude-mem`'s
   `pathfinder` does), it belongs to the periodic architecture audit, not here — it fans out over
   the whole repo and answers "what is duplicated across features", which is `agents/architect`'s
   question. Reading its report is fine input to this step; running it per feature is not.
4. **Write the target architecture down** — file, role, and the fact that it's still `planned` rather than
   built. A repo-local doc, or a graph/registry tool where the project has one; what matters is that it's
   written and findable, not which tool holds it.

## Output / checkpoint
`arch_done` + the target architecture written (file, role, planned-vs-built), and for each capability
either the existing thing being reused or the recorded reason it couldn't be.

## Guardrails
Extracting shared code = **a coordinated refactor, a human decision**: don't refactor quietly
inside an isolated worktree. If a duplicate already exists, flag it, don't recreate it.

Two failure modes to name explicitly. **Creating because searching was inconclusive**: an ambiguous
search result means read the code, not assume it's absent. And **reusing something that only looks
right**: bending an existing helper to a need it wasn't built for produces a shared thing that's
wrong for both callers, which is worse than the duplicate. Reuse is the default, not an obligation.

**A repo with no stack yet is still not a free choice.** When there is nothing to plug into — a new
service, a new tool — the stack is decided, not defaulted: take what the surrounding repos already
run, because the cost of a stack is the second one, not the first. Where there is no surrounding
repo, the choice is the operator's and it gets asked, once, before scaffolding. What is forbidden is
letting it be an accident of whichever framework came to mind first: that decision outlives the
feature, and nobody revisits it.

## Origin
Internal (graphify) + convergence of several market skill authors (architecture before build),
rewritten. The three-way dedup search (name, shape, call site) and the requirement to record the
negative result are ours: "I looked and found nothing" was the step that kept producing duplicates,
because searching by the name you already chose can only find things that share your vocabulary.
Point added 2026-09-07: the org catalogue this repo was measured against carries a *"default project
stack"* rule, and it was the one generic rule with no mentis home. Its content is that org's own stack
choice, which rule C keeps out of here — what generalises is the shape of the mistake it prevents, so
that is what the guardrail states instead of a stack name.

The graph freshness check was rewritten from the `understand-diff` skill of `Understand-Anything` (MIT), read 2026-10-02.

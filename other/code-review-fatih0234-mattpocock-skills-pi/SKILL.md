---
name: code-review
description: "Review the changes since a fixed point (commit, branch, tag, or merge-base) along two axes: Standards (does the code follow this repo's documented coding standards?) and Spec (does the code match what the originating issue/spec asked for?). Delegates both reviews to isolated Pi agents in parallel and reports them side by side. Use when the user wants to review a branch, a PR, work-in-progress changes, or asks to \"review since X\"."
---

Two-axis review of the diff between `HEAD` and a fixed point the user supplies:

- **Standards**: does the code conform to this repo's documented coding standards?
- **Spec**: does the code faithfully implement the originating issue / spec?

Both axes run through the Pi `subagent` tool so they have isolated model contexts, then this skill aggregates their report artifacts. In a ticket-worker, reviewers must use `worktree: false` and inherit the worker cwd, so they inspect the actual ticket changes rather than a new clean worktree. The dispatch runs in parallel, but the owning worker waits for the review fanout to finish. Keep the review `runs.all` group within the configured `parallel.concurrency` bound.

The issue tracker should have been provided to you. If `docs/agents/issue-tracker.md` is missing, tell the user to run `/skill:setup-matt-pocock-skills`.

## Process

### 1. Pin the fixed point

Whatever the user said is the fixed point (a commit SHA, branch name, tag, `main`, `HEAD~5`, etc.). If they didn't specify one, ask for it.

Capture the diff command once: `git diff <fixed-point>...HEAD` (three-dot, so the comparison is against the merge-base). Also note the list of commits via `git log <fixed-point>..HEAD --oneline`.

Before going further, confirm the fixed point resolves (`git rev-parse <fixed-point>`) and the diff is non-empty. A bad ref or empty diff should fail here, before delegation.

### 2. Identify the spec source

Look for the originating spec, in this order:

1. Issue references in the commit messages (`#123`, `Closes #45`, GitLab `!67`, etc.), fetched via the workflow in `docs/agents/issue-tracker.md`.
2. A path the user passed as an argument.
3. A spec file under `docs/`, `specs/`, or `.scratch/` matching the branch name or feature.
4. If nothing is found, ask the user where the spec is. If they say there isn't one, skip the Spec axis and report "no spec available".

### 3. Identify the standards sources

Anything in the repo that documents how code should be written, such as `CODING_STANDARDS.md` or `CONTRIBUTING.md`.

On top of whatever the repo documents, the Standards axis always carries the **smell baseline** below: a fixed set of Fowler code smells (_Refactoring_, ch.3) that applies even when a repo documents nothing. Two rules bind it:

- **The repo overrides.** A documented repo standard always wins; where it endorses something the baseline would flag, suppress the smell.
- **Always a judgement call.** Each smell is a labelled heuristic ("possible Feature Envy"), never a hard violation. Like any standard here, skip anything tooling already enforces.

Each smell reads *what it is* → *how to fix*; match it against the diff:

- **Mysterious Name**: a function, variable, or type whose name doesn't reveal what it does or holds. → rename it; if no honest name comes, the design's murky.
- **Duplicated Code**: the same logic shape appears in more than one hunk or file in the change. → extract the shared shape, call it from both.
- **Feature Envy**: a method that reaches into another object's data more than its own. → move the method onto the data it envies.
- **Data Clumps**: the same few fields or params keep travelling together (a type wanting to be born). → bundle them into one type, pass that.
- **Primitive Obsession**: a primitive or string standing in for a domain concept that deserves its own type. → give the concept its own small type.
- **Repeated Switches**: the same `switch`/`if`-cascade on the same type recurs across the change. → replace with polymorphism, or one map both sites share.
- **Shotgun Surgery**: one logical change forces scattered edits across many files in the diff. → gather what changes together into one module.
- **Divergent Change**: one file or module is edited for several unrelated reasons. → split so each module changes for one reason.
- **Speculative Generality**: abstraction, parameters, or hooks added for needs the spec doesn't have. → delete it; inline back until a real need shows.
- **Message Chains**: long `a.b().c().d()` navigation the caller shouldn't depend on. → hide the walk behind one method on the first object.
- **Middle Man**: a class or function that mostly just delegates onward. → cut it, call the real target direct.
- **Refused Bequest**: a subclass or implementer that ignores or overrides most of what it inherits. → drop the inheritance, use composition.

### 4. Allocate review artifacts

Capture `git status --short` before delegation. Create a unique run directory at `.scratch/pi-agents/code-review-<timestamp>/` and allocate:

- `standards-review.md`
- `spec-review.md`, when a spec exists

Each reviewer may write only its assigned artifact. Reviewers expose inspection tools only; they cannot mutate project files, implementation files, Git state, or tracker state. The runtime persists their final response to the assigned output path. The ticket-worker owns any warranted fixes and the parent owns integration.

### 5. Delegate both axes

When a spec exists, invoke the Pi `subagent` tool with a `workflowScript` and `async: false`. Use `await runs.all([...])` for the two independent children:

```javascript
const results = await runs.all([
  { key: "standards", agent: "standards-reviewer", task: "... Return the complete report in your final response.", context: "fresh", worktree: false, output: standardsArtifact, outputMode: "file-only" },
  { key: "spec", agent: "spec-reviewer", task: "... Return the complete report in your final response.", context: "fresh", worktree: false, output: specArtifact, outputMode: "file-only" }
]);
return results.map((result) => result.output);
```

The Standards task includes the fixed point, full diff command, commit list, standards-source paths, the complete smell baseline from step 3, repository root, and exact Standards artifact path. The Spec task includes the fixed point, full diff command, commit list, complete spec source or exact path, repository root, and exact Spec artifact path. Set each child’s `output` to its exact artifact path and `outputMode: "file-only"`; because reviewers have no mutation-capable tools, the runtime persists their complete final response there. Omit `cwd` inside a ticket-worker so each child inherits that worker checkout. State in both briefs that the axes are independent and one review must not read the other's artifact. When no spec exists, use one `runs.run` child with `agent: "standards-reviewer"`, `context: "fresh"`, `worktree: false`, `output: standardsArtifact`, and `outputMode: "file-only"` so aggregation cannot race the report.

After the dispatch, compare `git status --short` with the captured state. The only new paths attributable to reviewers must be their assigned artifacts. Stop and report any unexpected change before aggregation.

If the `subagent` tool is unavailable, run the two reviews as separate sequential passes, write the same artifacts, and disclose that the passes were not context-isolated.

### 6. Aggregate

Read the artifacts and present them under `## Standards` and `## Spec` headings, verbatim or lightly cleaned. Do **not** merge or rerank findings, because the two axes are deliberately separate (see _Why two axes_). If the spec was absent, put "no spec available" under `## Spec`.

End with a one-line summary: total findings per axis, and the worst issue _within each axis_ (if any). Don't pick a single winner across axes: that's the reranking the separation exists to prevent.

## Why two axes

A change can pass one axis and fail the other:

- Code that follows every standard but implements the wrong thing → **Standards pass, Spec fail.**
- Code that does exactly what the issue asked but breaks the project's conventions → **Spec pass, Standards fail.**

Reporting them separately stops one axis from masking the other.

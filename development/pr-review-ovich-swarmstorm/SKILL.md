---
name: pr-review
description: "Use when reviewing a pull request, branch or diff in any language, to produce the analysis a reviewer decides from: what changed, why, how the structure moved, what it can break, and the decisions only a human can make, at five altitudes from code primitives to delivery and intent. Not a bug hunt, and not framework-specific review."
---

# PR review

**The deliverable is the decisions a reviewer can make**: what changed, how the structure moved, the blast radius, the decision points, then findings, each citing its source. It reviews in **layers**, independent subagents each reading the change at one altitude.

## Scope

- `/pr-review <PR#>`: `node scripts/scope.mjs pr <PR#> --layers --json`
- `/pr-review <branch|ref>`: `node scripts/scope.mjs branch <ref> --layers --json`
- **Neither: ask for the fixed point.**

**Run the script first** (path relative to this skill). It resolves the merge-base, lists the files with vendored, generated, build and lockfile paths skipped, carries the stated intent, and says which of L3 and L5 have material. Exit 1 is an empty scope, exit 2 a ref that does not resolve: either stops the review. A dirty working tree is invisible to it: say so.

- **The diff and the search base are the same revision.** Check out the PR's head, or say that the blast radius was not repo-verified: a search against a tree without the PR cites `file:line` confidently wrong.
- **Read the repo's conventions before dispatch**: `AGENTS.md`, `CLAUDE.md`, architecture docs, `write-conventions` where it applies. A broken house rule is a finding; unusual but unruled is a decision point.
- **The diff adds or changes a decision citation** (`<topic>#D<n>`, or a bare `D<n>` in code): run the `write-plan` skill's `scripts/decisions.mjs` on the PR's head, with the project's plan folder and `--code` the repository. A finding it prints is a finding of the review.

## The five layers

**The diff decides which run.** A layer that does not run is recorded with its reason, in the analysis and in the verdict: a reader takes silence for coverage.

| Layer | Owns | Dispatched when |
|---|---|---|
| **L1 Code Primitives** | classes, types, functions, lines; DRY and SOLID; races visible in a function body; test code quality | always |
| **L2 Code Structure** | directories, modules, files; placement and naming; cohesion and coupling; test file placement | always |
| **L3 Data** | schema, ORM mappings, tables, migration files as artifacts | they are in the diff |
| **L4 Integration** | blast radius: callers, consumers, contracts, other repos, config, deploy needs, migration execution order | the diff changes a surface something else consumes |
| **L5 Delivery & Intent** | stated intent against the diff, completeness, scope creep, documentation, coverage of the stated behaviour | the PR states an intent: description, linked issue, commit messages, or a plan, whose user stories are then checked one by one |

- **A plan reaches the review** when the person names it or the PR's group tag finds it (`aiview list --kind plan --tag <group>`); a named plan makes L5 material whatever the script says.
- **No stated intent: "L5: not run, no stated intent."** An inferred intent checks the code against itself.
- **A pattern L5 finds unruled** that would pass the five filters of `write-conventions` is proposed as a capture, in chat.

## The documents

**Two files through the `aiview` skill, one group `pr-<id>`, each linking the other.** Tell the user the report's URL.

| | `YYYY-MM-DD-pr-<id>.report.md` | `YYYY-MM-DD-pr-<id>.pr-analysis.md` |
|---|---|---|
| Reader | the human deciding whether to merge | the next agent, and the human asking "why does it say that?" |
| Size | one screen before the comment block | as long as the evidence needs |
| Holds | the claims | the evidence for each |

- **Read `references/documents.md` before writing either**: the sections, the report's register, the stamp, which diagrams go where.
- **Publish both before any layer returns**: the report's Abstract, What changed and change map, with one `aiview pending` card per dispatched layer, closed as its return lands.
- **Every report claim traces to a section of the analysis.**

## Running the layers

**Read `references/layers.md` before dispatch**: the seam table, the four slots of a brief, what a return contains.

- **Triage in this session**: L3 and L5 from the script's `layers`, L4 your call from the diff. Settle every seam the review will meet and the shared facts. Each question has one owner.
- **Each layer is a fresh-context subagent**: the diff, its brief, the output contract, and the instruction "Do not invoke skills or spawn agents: review directly." Name the surface in a brief, keep your hypothesis out of it.
- **Merge in this session**: dedup, rank by cost, drop what the project's linter or CI already flags.
- **A finding outside its layer's jurisdiction is dropped from that return**, and re-verified under the owning layer if it matters. One that implicates a skipped layer reopens the triage: dispatch the layer, or record why not.
- **Re-verify the findings that carry the verdict**: a well-argued wrong finding reaches the author in your name.

## Beyond the layers

- **A correctness bug hunt is the harness's own review.** When nothing runs one, the verdict says nobody checked whether the code works.
- **The document records it**: "Correctness: not covered."

## Red flags

| Thought | Reality |
|---|---|
| "One overall score for the PR" | A blended verdict hides the failing layer. One line per layer, plus the open decisions. |
| "More findings = better review" | Ten cited findings beat forty hunches. |
| "The code around it is a mess too" | Not this PR's bill. Note it, attribute it, approve anyway. |
| "Unverifiable from here, so it blocks" | Ask the author. A question they answer in one line is not a change request. |
| "The proposed comment is the deliverable" | The report is. The comment is its condensate. |
| "The recommendation decides the merge" | It drafts the reviewer's words. The decision stays theirs. |

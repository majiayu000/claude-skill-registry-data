---
name: create-code-generation
description: >
  Orchestrate a feature or fix from story to PR through the team's AI-SDLC
  workflow, with human checkpoints: story -> plan -> branch -> TDD (>=80%
  coverage, story-tagged tests) -> update both doc layers -> record decisions as ADRs ->
  enrich the work item -> review -> PR. Use when the user says "take this story
  through the process", "run the dev cycle", "do the full workflow on
  MN-42", or "build this end to end properly". It delegates to focused
  skills rather than doing each step itself. Do NOT use for a quick one-off edit,
  a question, or a standalone git or branch request (creating or naming a branch
  on its own) - use the individual skills directly for those.
---

# Create Code Generation (orchestrator)

Owned by the **Developer** persona (the create-code-generation step). Invoked as `/create-code-generation`.

Walk a change through the full development lifecycle, delegating each phase to the skill
that owns it and pausing at human checkpoints. This skill is a **conductor, not a
performer**: it sequences other skills, enforces the order, and makes sure nothing
(docs, decisions, the ticket) is skipped. Humans review intent and approve the
side-effectful steps; the workflow handles the rote sequence.

Keep changes scoped to the story. If the work splits into independent pieces, parallelise the
implementation with whatever your agent offers (in Claude Code: subagents via the Agent/Task tool, or
`superpowers:subagent-driven-development`), per the independence rule in `docs/ai-sdlc/orchestration.md`:
only slices that share no output and write no common artifact run in parallel, and parallelism never
relaxes a checkpoint. On Copilot and other agents, run the slices sequentially - same result, slower.

## Governing context

The repo's `AGENTS.md` constitution core is already loaded (always-on). Treat its clauses
as non-negotiable for every phase. Before finishing, run a constitution check (the
`governance-constitution` skill, check mode) over the change and stop if it violates a clause - either
fix it, or if the clause should change, amend the constitution deliberately (not silently).

## Phases (each delegates; stop at the checkpoints)

Pack skills named below (`elaboration-upsert-user-story`, `create-upsert-documentation`, `governance-author-adr`, `governance-enrich-ticket`, `governance-constitution`) live in `.claude/skills/` and are read by both Claude Code and Copilot. Steps that name a Claude-only accelerator give it in parentheses; otherwise do the step directly with your agent.

1. **Story.** If there is no work item, create one with `elaboration-upsert-user-story`. If a key was given (e.g. MN-42), read the work item file under `docs/discovery/` and restate the acceptance criteria. CHECKPOINT: confirm scope and ACs before coding.
2. **Plan.** Produce a written implementation plan, scanning the relevant code first with the constitution in mind and verifying load-bearing claims against the codebase rather than memory (in Claude Code: `/plan`, or `prp-plan` for larger work). When the change branches on a closed set (an enum like `WorkflowRunType`, a discriminated union, a sealed hierarchy), read the type and list every member in the plan so none is left to an implicit catch-all (see `docs/conventions/csharp.md`). CHECKPOINT: human approves the plan.
3. **Branch (and PR preflight).** Before the first code change, create the development branch named for the work item key (the bare key, e.g. `MN-42`). Do not assume `main` as the base: confirm the correct base branch first (ask, or verify which line this targets), pull it up to date, then `git switch -c MN-42` (or `git checkout -b`). If you are already on that story's branch, stay on it. This is a local, reversible action - state the branch name and proceed; it needs no confirmation checkpoint. Never start feature work on the base branch itself. Also run the **PR preflight** (below) now, so the PR step cannot dead-end after the work is done.
4. **Implement (TDD).** Work test-first, red-green-refactor (in Claude Code: `superpowers:test-driven-development` + the language test skill such as `go-test`/`kotlin-test`; for .NET/xUnit drive it directly). Write to the conventions in `docs/conventions/` - for C#, `csharp.md` and `clean-code.md`; the analyzer severities in `MindNova/.editorconfig` are real (error rules fail the build, locally and in CI), so keep the build green and add no new analyzer warnings on changed projects. **Tag each new test with the story ID** (an xUnit `[Trait("Story","MN-42")]` or the stack's equivalent) so the deferred AC-coverage gate can attach with no rework.
5. **Coverage.** Bring changed projects to **>= 80% (aim higher)**, verified by running the tests, not asserted (in Claude Code: `/test-coverage`).
6. **Docs.** Use `create-upsert-documentation` to update `docs/` (technical) and `docs-functional/` (functional). Decide for each layer explicitly, even if the decision is "no functional change".
7. **Decisions.** Use `governance-author-adr` in suggest mode; if the change made a load-bearing decision (new pattern, deviation from a convention or constitution clause, a lasting tradeoff), author the ADR. If it implies a new non-negotiable, flag the `governance-constitution` skill.
8. **Enrich the work item.** Use `governance-enrich-ticket` to add related links + why, the ADR backlink, and any artifact links to the story file. CHECKPOINT: confirm before writing.
9. **Review.** Run code review and address findings (in Claude Code: `/code-review` + the language reviewer such as `go-review`/`python-review`, and `superpowers:requesting-code-review`; in Copilot: its review). Run the constitution check here. For C#, apply `docs/conventions/clean-code.md`: the build must stay green (analyzer errors are build-failing), add no new analyzer warnings on changed projects, and the advisory bucket (functions do one thing, command-query separation, prefer polymorphism over a type-switch) is checked here since no analyzer enforces it. Run the CI gates locally before the PR with `/create-run-gates` (or `pwsh MindNova/toolsInvoke-LocalGates.ps1`) and clear every BLOCKING failure (docs, skill hygiene, artifact graph, em-dash, story-trait keys); this catches what CI would reject in seconds, without waiting for a pipeline cycle.
10. **Finish.** Open the PR using the path confirmed in the preflight, preferring the `MindNova/toolsNew-MindNovaPullRequest.ps1` helper (in Claude Code: `superpowers:finishing-a-development-branch` or `/pr`; in Copilot: its PR flow). CHECKPOINT: confirm before pushing or opening the PR (this is an external, outward action). **Verify the description read-back.** The helper reads the PR back and throws on a truncated or empty description; if you opened the PR any other way, read it back yourself and assert the description survived (empty, title-length, or first-heading-only is a hard failure), issuing one corrective `az repos pr update` with a line array per AGENTS.md before continuing. After the PR is open and its description is verified, backlink its URL onto the work item file via `/governance-enrich-ticket` and onto the story's artifacts; the cycle is not done while the work item has no PR link or the description is truncated.

## PR preflight (run at step 3, before building)

Confirm a working PR-creation path before writing code, so the PR step cannot dead-end after the work is done. Probe in priority order and record which works:

1. **MCP `repo_create_pull_request`** - only if it can actually write. The MCP server runs as its own service identity; a `TF400813: not authorized` means that identity lacks Code (Read & Write), and a user `az login` refresh will not fix it. On `TF400813`, skip MCP for repo writes.
2. **The `MindNova/toolsNew-MindNovaPullRequest.ps1` helper (canonical), backed by `az`** - the reliable path here. Cheap probes first: `az extension show --name azure-devops` (a `WinError 5 Access is denied` on its dist-info means the extension was installed elevated, an ACL gotcha - reinstall it unelevated), and confirm `AZURE_DEVOPS_EXT_PAT` is set (Code Read & Write on `[PLACEHOLDER]`). When the work is done, open the PR with the helper, which passes the description as a line array, blocks `-` bullets, reads the PR back, and throws on truncation. Do NOT pass `--description` as a single multi-line string: it keeps only the first line. If you must call `az` directly rather than the helper, follow AGENTS.md ("Creating a PR"): description as a line array, `*` bullets, and a mandatory read-back that fails on an empty or truncated description.
3. **Browser-URL fallback** - if neither works, the pre-filled `[PLACEHOLDER]/[PLACEHOLDER]/_git/<repo>/pullrequestcreate?sourceRef=<branch>&targetRef=<base>` for the user to complete.

Record which path is available now; step 10 uses it. (See AGENTS.md, "Work items and pull requests".)

## Checkpoints and confirmation

- Hard stops for human approval: after the plan (2), before any write to the ticket (8), and before push/PR (10). Creating the branch (3) is local and reversible, so it is not a checkpoint.
- External, hard-to-reverse actions (creating/enriching tickets, opening PRs) always require explicit confirmation, per session and per action. One approval does not carry to the next.
- Local artifacts (code, tests, docs, ADRs) follow normal editing with the verify-before-assert discipline.

## Designed for the (deferred) gate phase

This sequence mirrors the future GitHub Actions gated pipeline, so the artifacts it produces are gate-ready:
- story-tagged tests -> future AC/story-trait gate;
- >=80% coverage -> future coverage gate;
- ADRs in `docs/adrs/` -> future `adr-check`;
- constitution clauses -> future `constitution-check`.
When the gate phase lands, these become blocking in CI; until then create-code-generation enforces them locally.

## Guardrails

- **Delegate, don't reimplement.** Each phase invokes its owning skill; this file only sequences and gates. If a phase's skill is missing, do that phase directly but keep the order.
- **Parallel dispatch stays gated.** When fanning out independent slices (Claude subagents), each side-effectful or outward action (ticket write, push, PR) still confirms on its own - ten parallel slices are ten gated leaves, not one blanket approval. See `docs/ai-sdlc/orchestration.md`.
- **Branch per story.** Development runs on a branch named for the work item key (the bare key, e.g. `MN-42`), created before the first code change; never commit feature work straight to `main`.
- **Don't skip docs or decisions.** The two most-skipped phases are 6 (docs) and 7 (ADRs); they are not optional.
- **No em-dashes, no AI attribution** in any artifact, commit, or PR text. Respect repo doc rules (no line numbers; reference by path + symbol).
- **Stop on constitution conflict.** A change that violates a clause does not ship by working around the clause; fix the change or amend the clause on purpose.

## Next steps

- Before the PR, `/governance-check-graph` (Lead) - confirm the story's spec, ADR, and doc links resolve.
- After merge, `/mature-collect-release-feedback` (PM) for outcomes and `/mature-resolve-ticket` (Developer) for follow-up defects.
- This orchestrator already calls `/elaboration-upsert-user-story`, `/create-upsert-documentation`, `/governance-author-adr`, and `/governance-enrich-ticket` in sequence; run any of them standalone for a single step.

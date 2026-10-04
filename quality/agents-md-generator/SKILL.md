---
name: agents-md-generator
description: Create, draft, audit, revise, or migrate root and nested repository AGENTS.md files from repo evidence. Use when the user asks to create or review an AGENTS.md, improve repository coding-agent instructions, convert CLAUDE.md-style guidance into AGENTS.md, or decide instruction scope in a monorepo. Primary for AGENTS.md; use documenter for README, contributor, and other agent-facing documentation.
---

# AGENTS.md generator

Create high-signal, repository-grounded instructions with a host-neutral semantic core for coding-agent hosts that support `AGENTS.md`. Treat tool-specific instruction files as adapters when a host requires them.

## Scope and side effects

- `findings` and `draft` do not authorize instruction-file edits. Only `apply` authorizes those edits, limited to the requested files; validation side effects require separate authorization under the rule below.
- The default target is the root `AGENTS.md`. Create or revise a nested target only when the user names or approves that path and selects `apply`.
- Repository inspection is read-only. Validation commands may write caches or artifacts, install dependencies, use the network, or trigger external systems. Assess them first, run the smallest safe check, and get authorization before consequential validation.
- Before editing, inspect the target file and any existing worktree diff. Preserve unrelated and pre-existing changes.
- Never delete or overwrite source instruction files such as `CLAUDE.md` without explicit authorization covering those files. Reuse authorization already granted for the same action. Report any validation artifacts that cannot be safely cleaned up.

## Core workflow

1. Define the task, output, and target independently so mixed requests remain representable.
2. Inspect the repository, existing instruction files, and target-file worktree state.
3. Resolve operational facts, policy, host compatibility, and source conflicts using the rules below.
4. Ask only the missing questions that materially affect the result.
5. Produce findings, a draft, or authorized edits for the selected root or nested target.
6. Decide whether nested files or host-specific adapters are justified.
7. Validate claims and, after writes, review the resulting diff.
8. Tighten the instructions and hand off evidence, assumptions, and residual uncertainty.

Do not skip repository inspection unless the user supplies the complete relevant context.

## Phase 1: Define task, output, and target

Choose each dimension independently:

- task: `create`, `revise`, `migrate`, or `audit`
- output: `findings`, `draft`, or `apply`
- target: root `AGENTS.md` or one or more named nested paths

`audit + findings` is the default for a review request. Pair `audit + draft` when the user also wants proposed replacement content. A migration can produce a read-only draft or applied changes. Use `apply` only when the user requests instruction-file edits; never turn `findings` or `draft` into those edits without new authorization.

If the user asks for "agent instructions", "repo instructions", or "coding-agent guidance", treat it as an `AGENTS.md` request only when the desired artifact is repository instruction scope rather than another document type.

## Phase 2: Inspect before asking

Prefer targeted inspection over broad reading. Establish:

- repository purpose, structure, toolchains, and important subtrees
- declared setup, build, test, lint, validation, and review commands
- existing root, nested, and tool-specific instruction files
- generated, vendored, secret-bearing, migration, deployment, and other risk boundaries
- when nesting, adapters, or cross-host compatibility is in scope, instruction-file support and scope semantics for the relevant hosts

Read [references/inspection-and-content-checklist.md](references/inspection-and-content-checklist.md) when inspection is non-trivial, such as a migration, multiple manifests or instruction sources, risky validation, conflicting evidence, or a dirty target-file worktree.

## Phase 3: Resolve migration and source conflicts

For `migrate`, determine whether each source file is ordinary prose or an instruction entry point loaded by a target host. Keep a required entry point as a thin adapter when possible. Recommend replacing it with a pointer only when the host follows that pointer and the user confirms the change.

Resolve conflicts by claim type:

- For operational facts such as command names, flags, paths, and supported versions, prefer executable configuration and current repository structure.
- For normative rules such as review policy, safety constraints, ownership, and required checks beyond CI, prefer maintained policy documents. Treat user direction as durable repository policy only when the user confirms it should govern future agents.
- Do not infer that a check is optional merely because CI does not run it.
- When evidence remains materially ambiguous, ask the user or report the conflict instead of silently choosing a source.

Record each material conflict and its resolution in the handoff.

## Phase 4: Ask only high-impact questions

Ask only about decisions that repository evidence cannot settle, such as:

- which coding-agent hosts the instructions must support when compatibility affects the layout
- whether an undocumented or request-specific preference should become durable policy for future agents
- how strict review or validation gates should be when existing sources conflict
- whether the user authorizes recommended nested files or changes to host-specific adapters

Use a sensible default for low-impact ambiguity. Keep temporary authoring assumptions in the handoff, not the durable `AGENTS.md`; include an assumption in the file only when future agents need it to act correctly.

## Phase 5: Produce the authorized output

- For `findings`, return prioritized observations, evidence, and residual uncertainty without drafting or editing unless another output was also requested.
- For `draft`, return proposed content and intended paths without editing the repository. It may accompany audit findings.
- For `apply`, edit only the authorized targets. Use [assets/agents-md-skeleton.md](assets/agents-md-skeleton.md) for a new root file and delete every inapplicable section or placeholder; write a new nested file as a local delta instead of copying the root skeleton.
- When revising, preserve real constraints and unrelated sections, remove stale or duplicate guidance, and review both the pre-existing and resulting diff.

Prefer concrete commands, scoped boundaries, and decision rules over generic advice or product branding.

## Phase 6: Decide on nested files and host adapters

Do not claim universal `AGENTS.md` or nested-file support. Confirm the named host behavior when the result depends on it; if support is unknown, keep a single root file with clearly scoped subsections.

Recommend nested files only for materially different subtree rules. State the proposed directories, local deltas, root responsibilities, and known inheritance behavior before writing them.

Use [references/nested-files-and-token-optimization.md](references/nested-files-and-token-optimization.md) when nested scope, host adapters, or a long draft requires closer judgment.

## Phase 7: Validate claims and changes

For each material command, path, or policy claim, record the exact repository source. Track execution separately as passed, failed, environment-blocked, or not run when execution evidence matters. Do not force a formal evidence taxonomy onto trivial or undisputed facts.

Then:

- verify commands in manifests, task runners, scripts, CI, or maintained docs before including them
- run only safe, proportionate checks; an environment failure does not invalidate a repository-declared command
- remove or reword a command only when repository evidence shows it is stale, contradicted, or unsupported, not merely because local execution is blocked
- verify paths against the current filesystem and use `git ls-files` as supplemental evidence when Git is available; do not assume intentionally untracked paths are invalid
- trace constraints, hazards, and forbidden actions to repository evidence or explicit user policy
- after writes, review the diff and remove only validation artifacts that are safely attributable to this run

Report exact commands run, results, skipped checks, environment limitations, and remaining artifacts. Never imply that an unrun check passed.

## Phase 8: Tighten and hand off

Delete repeated or generic guidance, keep global rules in the root and local deltas in nested files, and link to maintained repository docs instead of copying bulky detail.

Always state the output paths, files changed or read-only status, and validation actually performed. When material, also report source conflicts, execution limitations or side effects, temporary assumptions, host-compatibility limits, and nested-file recommendations. Omit empty categories instead of producing a ceremonial checklist.

## Quality bar

The result should help a coding agent act correctly on the first pass, preserve unrelated work, and contain no unsupported command, path, or policy claim. Its content should remain tool-neutral where possible without claiming support from hosts that were not identified or verified.

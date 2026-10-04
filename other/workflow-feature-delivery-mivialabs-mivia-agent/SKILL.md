---
name: workflow-feature-delivery
description: Deliver one scoped feature in a workflow worktree with tests, security review, host evidence gates, and an honest report.
triggers:
  - workflow feature delivery
  - workflow implementation
tools:
  - read_file
  - list_dir
  - grep
  - glob
  - find_references
  - write_file
  - search_replace
  - multi_edit
---

<!-- Provenance: workflow-safe. The host owns command execution and publication. -->

# Workflow Feature Delivery

## Purpose

Deliver one scoped feature in an isolated workflow worktree. Use tests, implementation,
review, host evidence gates, and an honest completion report. The host executes commands,
commits, pushes, and publishes. The workflow agent does none of these actions.

## Read First

- The task and its acceptance criteria.
- Workspace instructions and the approved workflow plan.
- The approved test plan before implementation.
- Relevant source, tests, interfaces, configuration, and security boundaries.
- `.agents/quality/defect-taxonomy.md` when the slice touches run state, ownership, delivery, or persistence.

## Method

1. Lock scope to one feature slice. State the files and behavior in scope. Do not broaden scope.
2. Create or update tests before or with the implementation. Cover success and at least one negative path.
3. When untrusted structured input is parsed or decoded, cover empty, malformed, oversized, and duplicate input.
4. State whether a deterministic fuzz target is practical. Request a bounded host fuzz gate when it is practical. Otherwise state why it is not practical.
5. Implement the smallest change that meets the approved plan and test plan.
6. Inspect the change for secrets, unsafe file paths, unsafe external input, privilege expansion, and fail-open guards.
7. When the slice adds or changes a run state, an ownership step, or a delivery step, answer these before you request the host gates. The delivery machine is this repository's most defect-dense surface, so these are gates, not advice. Both are pinned: `INV-DUR-1` and `INV-DUR-2` in `.mivia/invariants.md`.
   - **`DC-1` terminal states.** Name every terminal state the slice can reach and the conditions that reach it. Classify each condition as permanent or transient. A transient condition must not reach a terminal state, or the terminal state needs an explicit re-entry edge with one enforcing compare-and-set. State the answer; do not leave it implied.
   - **`DC-2` ownership.** Name the owner of each record the slice mutates and the mechanism that proves ownership. A boolean claim flag is not exclusion. State what happens when a second owner takes over and the first one resumes and writes, and confirm the claim is released on every failure branch, the pre-flight refusal included.
   - Cover both with tests. `internal/durablefence` supplies the two-owner takeover, exclusivity, concurrent-claim, and holder-only-release checks; adapt it rather than re-deriving the scenarios.
8. Do not run commands. Request the required host evidence gates for tests, build or type checks, static checks, security checks, fuzz checks when needed, and final validation.
9. Use failed host evidence as repair input. Fix only the reported issue and repeat the required review and host gates.
10. Do not claim that a command, hook, commit, push, or publication occurred unless the host reports it.

## Rules

- Do not commit, push, publish, read secret-like files, or bypass Git hooks.
- Do not add raw prompts, raw model output, credentials, or personal data to source, tests, or reports.
- Do not suppress static-analysis findings.
- Do not leave unresolved TODO, FIXME, HACK, or XXX markers in the delivered scope.
- Keep the report concise and factual. Host evidence is the source for command results.

## Report Shape

Return only the structured output required by the current workflow step. The text fields
must state the following facts when the schema permits them:

- Scope: the feature slice and changed files.
- Tests: success, negative, malformed, oversized, and duplicate cases as applicable.
- Security: checks made and open risks.
- Fuzz: the requested gate or why it is not practical.
- Host evidence: requested gates and received results. Do not invent results.
- Remaining gaps: `None identified` only after host evidence closes all required gaps.

Use `BLOCK` or request changes when a required test, security check, host gate, or hook result is absent or fails.

---
name: development-contract-process
description: Portable workflow for repos that require tracked change contracts, verifier evidence, and smallest-proof validation. Use when a repo has a contract policy file or enforced feature-plan checker.
---

# Development Contract Process

Find the repo's contract policy file for paths, record locations, lanes, and
validation profiles. It owns contract mechanics within the host's instruction
hierarchy; it does not override higher-authority task constraints. Inspect a
policy/documentation mismatch before deciding which artifact needs correction.

This is a process overlay, not a thinking aid. Pair it with the repo's implementation skill for the touched code and any repo-local contract overlay that names the actual policy path and helper commands.

## Activity and authority

- Review or planning: inspect policy, records, and enforcement; return findings
  or a proposed contract without modifying files. Write a record only when the
  requested output or an authorized implementation workflow requires it.
- Implementation: maintain the required record as part of the already-authorized
  change. Do not ask again for ordinary record updates covered by that scope.
- A policy file or declared command does not authorize installation, publication,
  or other consequential side effects. Inspect commands before running them;
  executable policy files are code, not inert configuration.

## Policy discovery

If the repo-local overlay does not name a policy file, search for likely
contract artifacts before guessing: `change-contract-policy`, `feature_records`,
`check-change-contracts`, lifecycle helper scripts, and AGENTS/README language
about substantive changes or verifier evidence. Once found, treat the policy
file as source of truth.

## Use this skill when

- work may trigger a tracked change contract
- a repo requires a plan update for substantive changes
- a checker validates plan structure, ownership, or evidence
- you need to choose the smallest proving validation set for a substantive change

## Core workflow

1. Read the touched files and the repo contract policy file before editing.
2. Decide whether the change is substantive using policy data rather than guesswork.
3. For authorized implementation, create or update a non-template record when
   policy classifies the change as substantive. During review, assess whether
   the existing record satisfies that obligation without repairing it.
4. Keep the plan aligned with the repo's enforced template, required evidence lanes, and lifecycle-directory rules.
5. Keep implementation ownership and verification ownership explicit.
6. Record verifier commands, observed results, and contract mismatches concretely.
7. Run the smallest validation profile that proves the change, then extend only when the surface justifies it.
8. Before closing implementation, run the checker and required profile checks.
   In read-only work, run only safe check modes; report unrun checks explicitly.

## Decision rules

- Treat the policy file as the single source of truth for substantive-path detection, plan location, section requirements, lane names, and default validation commands.
- If the repo ships a lifecycle transition helper, prefer it over manual file moves so path and lifecycle state stay synchronized.
- Do not duplicate repo literals across the skill, docs, checker, and template when policy can express them once.
- Keep the schema stable by default; use policy for repo-level variation and only change the schema when portability or correctness requires it.
- Prefer small repo overlays over forking the core skill.
- If a repo needs extra instructions that policy cannot express, add them in a thin overlay skill rather than bloating the core.
- Prefer updating an existing active record over creating scattered new notes for the same change.
- Keep the operator path lightweight: policy decides what is substantive, and the checker enforces the contract.

## Output expectations

For implementation, leave behind:

- code or docs aligned with repo guidance and policy
- a plan update when the change is substantive
- explicit verifier evidence
- a concise report of what was validated and what could not be validated

For review or planning, return the assessment or requested draft, its evidence,
and unresolved conflicts. Open findings do not make a completed review unfinished.

## References

- [Policy reference](references/policy-reference.md) for policy fields or adoption
- [Operator quickstart](references/operator-quickstart.md) for a compact operator handoff
- [Overlay template](references/repo-overlay-template.md) when authoring a local overlay
- [Release runner example](references/run-release-checklist.example.sh) only when
  adapting an explicitly requested CMake release runner; it is not a command
  implemented by every target repository

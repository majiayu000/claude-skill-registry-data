---
name: ls-skill-normalizer
description: "Normalize skills already in the tree using ls/docs/SKILL_NORMALIZATION.md: documents first, tooling second, with user choice for platform-specific skills. Use when normalizing one or more skills in ls/skills/ after import, copying, or batch review."
metadata:
  version: "1.1"
---

# Skill normalizer

**Purpose:** Normalize any skill(s) already in the framework skill tree using the current two-phase standard: **Phase 1: documents first**, then **Phase 2: tooling**. Use this when skills were imported without normalization, dropped in by copying files, or when you want to batch-normalize previously imported skills.

## When to use this skill

- User says "normalize this skill", "normalize the Ansible skill", "normalize all imported skills", or "make this skill spec-compliant."
- User copied a skill directory into `ls/skills/` and wants it normalized.
- Batch review: normalize several skills (e.g. ls-ansible-skill, ls-linux-service-triage, ls-linux-patcher) in one pass.

## Workflow (agent steps)

1. **Identify target(s)**  - User specifies one skill (e.g. by name or path) or "all" (all skills under `ls/skills/`). Resolve to a list of skill directories; each must contain SKILL.md.
2. **Load rules**  - This `SKILL.md` is the normative normalization execution contract, subject to higher-level user, repository, and safety policy. Read `ls/docs/SKILL_NORMALIZATION.md` as its synchronized public mirror and detailed reference for checklists, examples, platform-specific choices, and links to `TOOLING_POLICY.md` and `INPUT_HARDENING_STANDARD.md`. If the two surfaces conflict, the skill controls: do not apply the conflicting public instruction, stop before any affected write, report the mismatch, and synchronize both surfaces in one authorized change before resuming that normalization step.
3. **Inventory the skill**  - List the files that normalization may need to touch:
   - `SKILL.md` and any other skill documentation, including `references/`, README-style files, playbook notes, and usage examples.
   - Tooling assets such as `scripts/`, executable entrypoints, helper libraries, tests, playbooks, templates, and files that the skill relies on for behavior.
4. **Phase 1: document normalization**  - Normalize `SKILL.md` and any other relevant skill documents before changing tooling.
   - **Not platform-specific:** Apply spec compliance and platform-neutralization rules by default. Produce a summary and concrete key edits, present them for approval, then write the document updates.
   - **Platform-specific:** Do not assume full platform-neutralization. Present the user with the choices from `SKILL_NORMALIZATION.md`: keep as is, keep platform-specific but normalized, or fully normalize. Apply only the selected option, then present the summary and key edits required by that option before writing.
   - Cover references, playbook documentation, and examples where they describe stale invocations, old paths, platform wrappers, or commands that will change in Phase 2.
5. **Phase 2: tooling normalization**  - If the skill has scripts, playbooks, executable helpers, or other tooling, follow the tooling section in `SKILL_NORMALIZATION.md`.
   - Identify the tooling to replace or retain.
   - Present the tooling normalization plan: files to change, target framework tooling standard from `TOOLING_POLICY.md`, hardening expectations from `INPUT_HARDENING_STANDARD.md`, and documents that will be updated afterward.
   - If approved, rewrite tooling to the framework standard and update every affected reference in `SKILL.md`, `references/`, playbook docs, examples, and other skill-local docs.
   - If the user requests the keep-original-tooling exception, do not rewrite tooling; document that the user is responsible for that tooling and still complete the document normalization.
6. **Validate and confirm**  - Run the relevant catalog, skill, and diff checks from the repo root. Tell the user which skills and files were normalized, which checks passed, and any residual risk.

## Scope

- **Phase 1 covers documents:** `SKILL.md` plus other skill-local markdown or documentation where appropriate, including `references/`, README-style docs, playbook notes, and examples.
- **Phase 2 covers tooling:** scripts, executable helpers, behavior-bearing playbooks, templates, tests, and related files are normalized or explicitly retained under the keep-original-tooling exception.
- The same rules as import-time normalization apply: product-agnostic detection of platform-specific sections (e.g. "Integration with ...", "From ... Agent") and user choice before changing platform-specific intent.

## Rule ownership

- Normalize documents before tooling so references, examples, and command descriptions do not drift.
- Apply input hardening and tooling policy when scripts are added or changed.
- Keep platform-specific intent only with an explicit user choice.
- Keep the public normalization mirror synchronized whenever this normative workflow changes. The mirror may provide additional examples and detailed checklists, but it does not override this skill.

## Reference

- `ls/docs/SKILL_NORMALIZATION.md`  - Synchronized public mirror and detailed checklist for this skill's normative two-phase workflow.
- `ls/docs/SKILL_IMPORTING.md`  - Import workflow that invokes the same normalization rules after security and content safety are verified.
- `ls/docs/TOOLING_POLICY.md`  - Framework tooling language and dependency rules.
- `ls/docs/INPUT_HARDENING_STANDARD.md`  - Input validation, error handling, and observability requirements for normalized tooling.

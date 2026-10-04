---
name: repository-organization
description: Organize darkmatter repositories, READMEs, agent context, docs, scripts, skills, and ADRs into the right durable locations. Triggers when deciding where something belongs, restructuring repo layout, adding always-follow rules, or documenting architectural decisions. Do NOT trigger for Nix flake-specific layout work; use nix-flake-organization instead.
---

# Repository organization

Keep each repository easy for humans and agents to navigate by putting durable context, reusable guidance, automation, and decisions in the right layer. Prefer the smallest durable home that will be loaded at the time it matters.

For source conventions, apply [codebase-design](../codebase-design/SKILL.md):
keep each capability together, expose complete operations, and extract only
when the split improves understanding. Use
[domain-organization](../domain-organization/SKILL.md) for domain/role paths.
Keep the governing rule short in always-on instructions and link the full
examples; maintain one canonical definition instead of competing style lists.

## When to use

- A user asks where to put a new instruction, convention, policy, skill, command, script, workflow, reference doc, or ADR.
- A repo is accumulating scattered Markdown, duplicated agent instructions, or ad hoc decision notes.
- A change introduces a naming, layout, vendor, architecture, security, deployment, or process decision that future contributors should not re-litigate.
- A README is being created, reorganized, or reviewed for standard structure.
- A user asks whether something belongs in `AGENTS.md`, `.agent/context/`, `.agent/policy/`, `.agent/workflows/`, `skills/`, `docs/`, `scripts/`, or `presets/`.
- A project is being bootstrapped from the darkmatter template and needs its local context filled in cleanly.

## When NOT to use

- The task is specifically reorganizing Nix flakes, flake-parts outputs, NixOS modules, nix-darwin modules, or Home Manager modules. Use `nix-flake-organization`.
- The user only asks to create or edit a team-wide skill. Use `dm-skill-creator`; layer this skill only for placement or ADR questions around that change.
- The user is asking for one-off implementation notes that do not need to survive beyond the current task.
- The repository already has a clear local convention that conflicts with this guidance and the user explicitly wants to preserve it. Follow the local convention and note the tradeoff.

## Reference repo

Refer to our living repo which we maintain according to our current prefeerred shape: https://github.com/example-labs/ops-monorepo-demo

## README standard

Repository READMEs must follow Standard Readme: `https://github.com/RichardLitt/standard-readme/blob/main/spec.md`.

Apply the standard when creating or editing `README.md` files:

1. Use `README.md` capitalization for Markdown READMEs. For translated READMEs, use BCP 47 language tags such as `README.de.md`; reserve `README.md` for English when multiple languages exist.
2. Make the title match the repository, folder, and package-manager names, or explain any mismatch in the long description.
3. Keep Standard Readme section order and exact section titles unless translating the README. Required sections include title, short description, contributing, and license; install and usage are required by default unless the repo is documentation-only.
4. Keep the short description on its own line, under 120 characters, and not formatted as a blockquote.
5. Include a table of contents for READMEs longer than 100 lines. It should link to all sections, capture at least all level-two headings, and start with the next section after the table of contents.
6. Keep links working, lint code examples the same way the project lints source code, and keep the license section last.
7. Use `standard-readme-preset` (`https://github.com/RichardLitt/standard-readme-preset`) for remark-based linting when adding README checks.
8. Use `generator-standard-readme` (`https://github.com/RichardLitt/generator-standard-readme`) when scaffolding a new README from scratch.

## ADR guidance

Use ADRs for decisions that cross-cut multiple skills, multiple teammates, or future work. In this repo, ADR conventions live in `docs/adr/README.md`; do not invent a parallel template inside a skill.

Write an ADR when the decision is durable and cross-cutting; skip ADRs for local implementation notes, ephemeral state, and project-local decisions that belong in `.agent/context/decisions.md`. Treat `docs/adr/README.md` as authoritative for the full write/do-not-write criteria.

When adding or updating ADRs:

1. Read `docs/adr/README.md` or the target project's ADR README first.
2. Use the next zero-padded number and a kebab-case title.
3. Keep the decision to one topic with context, decision, consequences, and alternatives considered.
4. Use `proposed` while under review; mark `accepted` only when the decision is real.
5. Treat accepted ADRs as append-mostly history. If the decision changes, create a new ADR and mark the old one `superseded by ADR-XXXX`.
6. Link the ADR from the README, catalog, code comment, PR, or docs section where future readers will hit the governed behavior.

## Organization workflow

1. Inventory existing conventions before moving anything
2. Identify the artifact type: always-on rule, project fact, policy, workflow, reusable skill, command, plugin, tool, script, reference doc, or decision.
3. Choose the narrowest durable home from the placement table.
4. Keep meaningful public entrypoints. Follow the repository's compatibility policy; update callers and remove obsolete paths where required instead of adding forwarding chains.
5. Move one concern at a time and update links in the same change.
6. If a decision explains the new structure, add or update the ADR before claiming the structure is settled.
7. Verify with repo-specific checks plus targeted searches for stale paths, duplicate guidance, and outdated catalog rows.

## Common mistakes

- Putting always-follow policy in an on-demand skill; agents might not load it.
- Turning a skill into a junk drawer for project-specific state.
- Storing project facts in global presets where they leak into unrelated repos.
- Writing ADRs for unresolved debates instead of marking them `proposed` or keeping them in a planning doc.
- Editing accepted ADR conclusions in place instead of superseding them.
- Moving files without updating provider shims, catalog entries, README tables, or internal links.
- Adding scripts under a skill when they are really repo maintenance helpers, or vice versa.

## Review checklist

- The artifact lives at the layer where consumers will actually load it.
- Always-on context stayed short; detail moved to skills, workflows, reference docs, or ADRs.
- README changes follow Standard Readme naming, section order, required sections, link hygiene, and code-example linting.
- Project-local facts did not leak into team-wide skills or global presets.
- Team-wide skills have `SKILL.md` frontmatter, a catalog row, and validation coverage.
- ADR-worthy decisions are recorded or intentionally deferred with a clear reason.
- Accepted ADRs are not silently rewritten; supersession chains are explicit.
- Links, shims, catalog rows, and examples still point at the new paths.
- Source conventions agree with codebase-design; size thresholds prompt a cohesive split or a documented narrow exception, not mechanical fragmentation.

## Tools

None. This is a pure prompt and review skill. Use repo-local validators and search commands for verification.

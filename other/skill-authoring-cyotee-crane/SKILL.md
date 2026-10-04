---
name: skill-authoring
description: "Author or revise SKILL.md files, concise discovery metadata, topic routers and references within catalog budgets."
license: MIT
---

# Skill authoring

Write skills that are easy to discover and load only the guidance the task needs. Use `docs-to-skills` for documentation-site inventories and source coverage.

## Budget the catalog first

| Layer | Loaded when | Guidance |
| --- | --- | --- |
| Name, description and source path | Skill discovery | Measure their aggregate cost across the installed catalog. |
| SKILL.md body | The skill is selected | Prefer fewer than 200 lines; split before 500. |
| Topic files, references, examples and scripts | A relevant procedure needs them | Link directly and read selectively. |

Shortening a body does not reduce the discovery catalog. For a large collection, use a small family router with a task-to-topic table. Keep specialized guidance in linked files instead of discovering every topic separately. Preserve existing detailed files and relative-reference bases when consolidating.

Keep separate discovery entries when they represent distinct workflows the agent needs to find directly, especially repository deployment, testing and product rules. A router must give clear topic choices without requiring all children to be read.

IndexedEx's policy is recorded in `scripts/codex-skill-catalog.json`: at most **50 entries**, **160 characters per description**, and **14,000 characters** for the rendered repository catalog including paths. Aim for **80–140 character descriptions**. These are repository budgets, not a claimed limit of any client. Global/plugin skills and client formatting add their own overhead.

## Frontmatter

```yaml
---
name: skill-name
description: "Uniswap V4 swaps, flash accounting and hooks. Use when implementing PoolManager swap and settlement flows."
license: MIT
---
```

- Use a lowercase, hyphenated name matching the directory, up to 64 characters.
- Front-load the concrete domain and task. Include distinctive API names when they improve discovery.
- Use one concise line for a discoverable description. Avoid repeated “This skill should be used when” introductions and long lists of synonymous prompts.
- Keep both purpose and selection cues in the description; do not hide all selection cues in the body.
- A brief exclusion helps when two workflows are easily confused. Put longer distinctions in the body.
- Preserve existing license, version, tools, policy and UI metadata when changing descriptions.

A description such as “Helps with Uniswap” is too vague. Review representative task prompts to check whether the domain and workflow are recognizable. Do not fix missed selection by indiscriminately adding keywords or narrowing invocation policy without the owner's request.

## Body and references

Start with purpose, the smallest useful procedure, and a navigation table. Keep essential constraints beside that procedure. Move conditional examples, API tables and long explanations into named topic files or `references/`.

```text
skill-name/
  SKILL.md             # Purpose, procedure, essential constraints, navigation
  references/          # Optional topic detail
  scripts/             # Optional deterministic helpers
  assets/              # Optional templates or diagrams
```

- Link directly to the needed topic; avoid chains of intermediate indexes.
- Give reference files over 100 lines a contents list.
- Use descriptive filenames, forward slashes and consistent terminology.
- Resolve each linked file's own references relative to that file, especially when retaining an existing SKILL.md as a topic.
- Prefer concrete input/output examples and real signatures to general programming lessons.
- Record source URLs and distinguish source facts from inference. Verify code paths and selectors when code is available.
- Avoid unexplained constants, undated time-sensitive advice, five tools without a default, and full documentation dumps.

## Procedures and constraints

Use heuristics when multiple approaches are valid, parameterized templates for preferred patterns, and precise sequences for fragile operations. Match detail to risk without inventing new approval requirements.

Give multistep workflows a short checklist and a validation/fix loop. Preserve security, deployment and product constraints during compression. Cite the owning rule rather than duplicating it across every family. A skill's availability never expands the user's task scope.

## Crane and IndexedEx sources

- Maintain shared Crane guidance under `lib/crane/.claude/skills/` in the consumer checkout; use `.claude/skills/` when working at Crane's own root.
- Author IndexedEx guidance and its discovery routers under `.claude/skills/`.
- Codex's `.agents/skills/` contains links, not separate editable copies. The catalog records existing source exceptions; do not replace unique source content with a stale mirror.
- Keep Solidity examples on `@crane/` imports and real `contracts/` / `test/` paths.
- Keep production-first testing rules in `crane-testing`; consumer requirements stay in `indexedex-testing` and the repository router.
- For protocol documentation, preserve complete topic coverage while exposing one router or a few independently useful workflows.

In IndexedEx, register each installed topic in `scripts/codex-skill-catalog.json`, either directly or in a family. Add its link to the family's SKILL.md. Then run:

```bash
python3 scripts/sync-codex-skills.py --stats
python3 scripts/sync-codex-skills.py
python3 scripts/sync-codex-skills.py --check
```

`--stats` and `--check` are read-only. Discovery synchronization changes managed symlinks only. It refuses unknown entries, duplicate discovery and budget overruns. Source content and existing reference files remain in place.

## Review

- Does the description identify the intended task without boilerplate?
- Can a relevant prompt find its topic through one clear router choice?
- Are essential constraints and source metadata preserved?
- Are the body and references concise, complete and correctly linked?
- Do aggregate budget, topic coverage, duplicate and link checks pass?
- For tooling changes, do meaningful fixture tests cover failure and preservation behavior?

See also: `docs-to-skills`, the repository's `docs/agent/SKILL_CATALOG.md`, and the `docs-skill-scribe` role when documentation work calls for it. A role reference does not require delegation.

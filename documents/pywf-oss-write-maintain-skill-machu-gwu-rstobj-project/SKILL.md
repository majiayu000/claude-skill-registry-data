---
name: pywf-oss-write-maintain-skill
description: "Create or update this library's own maintenance skill family, maintain-<package_name>-base plus one invoker per repeatable job, that records its architecture, invariants, design decisions, debugging recipes, and library-specific jobs, so agents maintaining the repo need no maintainer guide. Use when the user asks to write down how to maintain the repo, to document architecture or a maintenance procedure, to move a maintainer guide out of the docs, or after a change that adds an invariant or a maintenance job."
---

Write maintenance knowledge where an agent working in this repo will load it: the `<maintain_prefix>` skill family (`maintain-<package_name>`), not a docs page that agents would never load.

Read ../pywf-oss-base/SKILL.md, then:
- ../pywf-oss-base/references/00-authoring-references.md (the base and invoker rules, file shape, script conventions)
- ../pywf-oss-base/references/07-repo-layout.md
- ../pywf-oss-base/references/18-knowledge-channels.md

## Step 1: Decide what is new

- Read `[project].name` from `pyproject.toml`: `<maintain_prefix>` is `maintain-<package_name>`.
- List what exists: `.claude/skills/<maintain_prefix>-*/`, and any maintainer pages under `docs/source/` (such as a `99-Maintainer-Guide/` folder).
- From the user's request, list the facts to record. Sort each with `18-knowledge-channels.md` section 2. A user-facing fact goes to `pywf-oss-write-doc`, a public-API fact to `pywf-oss-write-pypi-skill`, and a template convention is already in `pywf-oss-base`: name the skill, and drop it here.
- **New family:** propose the reference files (`NN-slug.md`, lifecycle order) and any invokers, one line each, and wait for the user's yes before writing. The names end up in every relative path.
- **Existing family:** say which files change and which are added.

## Step 2: Gather facts from the code

Read the modules, tests, `.mise/tasks/`, and git history the facts are about. Every claim names its source file or function. Never invent a rationale: when the reason for a design is not in the code, the commit messages, or the user's words, ask the user.

## Step 3: Write the base

```text
.claude/skills/<maintain_prefix>-base/
├── SKILL.md
└── references/NN-slug.md
```

- `SKILL.md` frontmatter: `name: <maintain_prefix>-base`, and a double-quoted `description` naming this library and the kinds of knowledge it holds, so it loads when someone changes the repo.
- `SKILL.md` body: one paragraph on the library's architecture; "For template conventions, load `pywf-oss-base`"; the references index between the same markers as in `pywf-oss-base`; and, once there are invokers, which one does which job.
- References follow `00-authoring-references.md` sections 2 and 3, with one difference: they are about this one library, so they use its real module and class names instead of placeholders.
- Scripts, if any, follow `00-authoring-references.md` section 4, and are added to the `format` and `lint` task paths in `mise.toml`.

## Step 4: Write the invokers (only for repeatable jobs)

Each `.claude/skills/<maintain_prefix>-<action>/SKILL.md` does one job: what it does, "Read ../<maintain_prefix>-base/SKILL.md, then:" with the files it needs, its steps, where it stops for the user's yes, and what it reports. A step that is a template convention cites the `pywf-oss-*` skill or reference by name instead of restating it.

## Step 5: Move a maintainer guide out of the docs

If `docs/source/` holds maintainer pages, carry their facts into the family, still true against the code. Then show the user the pages to delete, and delete them only after the user's yes. The docs keep user-facing pages only.

## Step 6: Verify

```bash
python ${CLAUDE_SKILL_DIR}/../pywf-oss-base/scripts/update_skill_index.py --skill_dir .claude/skills/<maintain_prefix>-base
python ${CLAUDE_SKILL_DIR}/../pywf-oss-base/scripts/check_skill_family.py --skills_dir .claude/skills --prefix <maintain_prefix>
```

Both report 0 problems. If a script was added, `mise run format`, then `mise run lint`, reports nothing. If docs pages were removed, `mise run build-doc` shows no new warnings.

## Output

Show the family's tree, each invoker with the base files it reads, and the facts that were left out because they belong to another channel.

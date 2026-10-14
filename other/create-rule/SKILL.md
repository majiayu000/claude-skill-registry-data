---
name: create-rule
description: >
  Create persistent agent guidance as AGENTS.md instructions or skills, not
  Cursor .cursor/rules. Use whenever the user wants to create a rule, add a
  Cursor rule, write .cursor/rules or .mdc files, add coding standards, set up
  project conventions, configure file-specific or directory-specific agent
  instructions, create or update AGENTS.md, add a SKILL.md for a convention,
  convert Cursor rules to AGENTS.md, capture a correction as standing orders,
  or says things like "always do X", "remember this", "add a rule for this",
  "make a rule", "create a cursor rule", or "don't let the agent forget".
---

# Create Rule

Turn a convention into guidance that coding agents will actually follow. Write
[AGENTS.md](https://agents.md/) for standing orders and a skill for on-demand
playbooks. Do not create `.cursor/rules/` or `.mdc` files unless the user
insists after you have explained the mapping.

Cursor rules are editor-specific. AGENTS.md and skills are the portable
equivalents: AGENTS.md is always (or path) loaded, skills load when the task
matches.

## Inspect first

Before asking questions or writing files, look at the repo:

- Existing `AGENTS.md` files (root and nested)
- Existing skill roots (`skills/`, `.agents/skills/`, `.claude/skills/`,
  `.codex/skills/`, `.cursor/skills/`)
- Generated markers (`lat gen`, `BEGIN:`/`END:`, "do not edit")
- Whether the request is already covered (update that section or skill
  instead of adding a duplicate)

Match the project's existing voice and placement. One concern lives in one
place.

## Choose the artifact

| Intent                                                                     | Cursor equivalent                     | Write                                                                                                    |
| -------------------------------------------------------------------------- | ------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| Standing order for every session in this repo                              | `alwaysApply: true`                   | Section in root `AGENTS.md`                                                                              |
| Standing order for one app, package, or directory                          | `globs: apps/web/**`                  | Nested `AGENTS.md` in that directory                                                                     |
| File-type convention that is not a single directory (`**/*.tsx` scattered) | `globs: **/*.tsx`                     | A skill whose description names the file type, or a short root AGENTS.md section if it must always apply |
| Task-specific procedure, framework playbook, or "only when doing X"        | Agent-requested / apply intelligently | Skill (`SKILL.md`)                                                                                       |
| Personal preference for every repo on this machine                         | User/global rule                      | Global AGENTS.md (`~/.fx/AGENTS.md` or the user's agent equivalent) only when they ask for global        |

AGENTS.md is a README for agents: setup, commands, invariants, safety,
verification. It is loaded often, so keep it short. Skills are playbooks
loaded on demand, so they can be longer and more specific.

Prefer a skill when the guidance is a workflow the agent would otherwise
reinvent (how to write a procedure, how to run a release). Prefer AGENTS.md
when ignoring the guidance would be wrong even for unrelated tasks (always
use bun, never commit secrets, always run this check).

If the user said "create a Cursor rule" or mentioned `.mdc`, still write
AGENTS.md or a skill and tell them the mapping. Only write `.cursor/rules`
if they insist they want Cursor-only files.

If they need a full skill with scripts, evals, or an iteration loop, use
`skill-creator` instead of drafting a thin SKILL.md here.

Read [references/placement.md](references/placement.md) when choosing paths
or migrating `.cursor/rules`.

## Gather only what you still need

Infer purpose, scope, and examples from this conversation first. A correction
("no, we use bun") is already the rule. Do not re-ask what was just said.

If scope is still unclear, ask one question:

- Always-on for the whole repo?
- Only when working in a specific directory?
- Only when doing a specific kind of task?

Suggest the default from the table above. Ask for file patterns only when
they said "specific files" but did not name a directory or glob.

Ask whether it is project-local or global only when they talk about "all my
projects" or "every repo". Default to the current project.

Do not ask about file format or where the file lives. You decide that.

## Write the guidance

Keep each AGENTS.md section under ~50 lines and about one concern. Split
unrelated concerns into separate sections or a nested file. Write like
internal docs: imperative, concrete, with a good and bad example when the
wrong form is tempting.

Explain why the rule exists in one sentence. Models follow "why" better than
a bare ALWAYS/NEVER. Save ALL CAPS for true safety or data-loss cases.

Do not put secrets, tokens, or unrelated private data in AGENTS.md or skills.
Those files enter model context.

### AGENTS.md

Plain markdown. No required frontmatter. Headings should name the concern.

- Update an existing section when the concern is already there.
- Add a new heading when it is a new concern.
- Create a nested `AGENTS.md` when the concern is path-scoped and no file
  exists yet.
- Leave generated regions untouched. If the whole root file is generated
  (`lat gen agents.md`, a full-file codegen banner), put new standing orders
  in a nested `AGENTS.md` or a skill rather than appending to generated
  output.

Nested files add path-scoped instructions. On conflict, the narrower file
wins. Direct user requests still beat both. Do not copy root instructions
into every nested file.

### Skills

Create `<skill-root>/<name>/SKILL.md` with YAML frontmatter:

```markdown
---
name: kebab-case-name
description: What it does and when to use it. Name trigger phrases.
---

# Title

Instructions for the agent.
```

`name` matches the directory. `description` is the trigger: include both
what the skill does and the user phrasing that should load it. Make it a
little pushy so the skill is consulted when it would help, not only when the
user names it.

Keep the body under 500 lines. One concern per skill. Put long examples or
framework variants in `references/` and tell the agent when to read them.

Prefer an existing project skill root, in this order: `skills/`,
`.agents/skills/`, `.claude/skills/`, `.codex/skills/`, `.cursor/skills/`.
If none exist, create `.agents/skills/<name>/` (vendor-neutral, widely
discovered). Do not install a project convention into `~/.fx/skills` unless
the user asked for a global skill.

## After writing

Tell the user, in plain language:

- Which file you created or updated
- When it will apply (every session, that directory, matching tasks)
- Why you chose AGENTS.md vs a skill

If you migrated Cursor rules, list each `.mdc` and where it went.

## Checklist

- [ ] Inspected existing AGENTS.md files and skill roots
- [ ] Chose AGENTS.md vs nested AGENTS.md vs skill vs global using the table
- [ ] Did not write `.cursor/rules` unless the user insisted
- [ ] Left generated regions alone
- [ ] One concern, concrete examples, no secrets
- [ ] Skill descriptions include what + when, if you wrote a skill
- [ ] Told the user where it lives and when it applies

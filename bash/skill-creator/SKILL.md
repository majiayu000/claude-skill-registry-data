---
name: skill-creator
description: Create, edit, and evaluate agent skills iteratively.
allowed-tools:
  - write_file
  - str_replace
  - read_file
  - list_dir
enabled: true
related-skills: [find-skills]
license: MIT
author: Adapted from deer-flow (Bytedance, MIT)
---

# Skill Creator

A skill for creating new skills and iteratively improving them.

At a high level, the process of creating a skill goes like this:

- Decide what you want the skill to do and roughly how it should do it
- Write a draft of the skill (a `SKILL.md` with YAML frontmatter + Markdown body)
- Create a few test prompts and run them with the skill injected
- Help the user evaluate the results both qualitatively and quantitatively
- Rewrite the skill based on feedback from the user's evaluation
- Repeat until you're satisfied
- Expand the test set and try again at larger scale

Your job when using this skill is to figure out where the user is in this
process and then jump in and help them progress through these stages.

## Poirot skill format

A Poirot skill lives in a directory containing `SKILL.md`:

```
skills/<category>/<skill-name>/SKILL.md      # user skills
poirot/backend/agents/skill/builtin_skills/<category>/<skill-name>/SKILL.md   # builtin
```

Frontmatter fields:

```yaml
---
name: <skill-name>            # unique, lowercase-hyphenated
description: <≤60 char one sentence ending with a period>
allowed-tools:                # Poirot tools this skill may invoke
  - web_search
  - browse_page
  - bash
  - read_file
  - write_file
  - list_dir
  - str_replace
  - present_files
  - read_snapshot
enabled: true
related-skills: [<other-skill-name>]   # optional cross-references
license: MIT                  # recommended for contributed skills
author: <human contributor or source attribution>
---
```

Body: `# <Skill>` title, 2-3 sentence intro, `## When to Use`,
`## How to Run`, `## Procedure`, `## Pitfalls`, `## Verification`.

## Authoring standards

1. **`description` ≤ 60 characters**, one sentence, ends with a period. State
   the capability, not the implementation. No marketing words.
2. **Tools referenced in prose must be native Poirot tools** (listed above) or
   MCP servers the skill explicitly expects. Do NOT name shell utilities the
   agent already has wrapped — `grep` → `bash`, `cat`/`head`/`tail` →
   `read_file`, `sed`/`awk` → `str_replace`, `find`/`ls` → `list_dir`.
3. **Scripts go in `scripts/`, references in `references/`, templates in
   `templates/`** inside the skill directory. Don't expect the model to
   inline-write non-trivial logic every call — ship a helper script.
4. **Keep the body focused**: ~100 lines for a simple skill, ~200 for complex.

## Iteration loop

1. Draft `SKILL.md`
2. Install via `/skill install <path>` (or place under `skills/`)
3. Reload: `/skill list` should show it active
4. Run test prompts; observe whether the skill's guidance is followed
5. Revise frontmatter `description` for better triggering, body for clarity
6. Repeat

## Pitfalls

- Description too long → dilutes model attention when many skills loaded
- Naming shell utilities instead of Poirot tools → model hallucinates calls
  to non-existent tools
- No `## When to Use` section → model triggers skill on wrong tasks
- Frontmatter with unknown fields → parser may ignore silently; stick to the
  schema above

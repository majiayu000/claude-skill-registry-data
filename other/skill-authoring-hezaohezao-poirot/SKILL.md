---
name: skill-authoring
description: "Author SKILL.md: frontmatter, structure, writing principles."
allowed-tools:
  - write_file
  - str_replace
  - read_file
  - list_dir
enabled: true
related-skills: [skill-creator, plan]
license: MIT
author: Adapted from hermes-agent (Nous Research, MIT)
---

# Authoring Poirot Skills

## Overview

A SKILL.md can live in two places:

1. **Builtin (in-repo):** `poirot/backend/agents/skill/builtin_skills/<category>/<name>/SKILL.md`
   — committed, shipped with the package. Use `write_file` + `git add`.
2. **User-local:** `skills/<name>/SKILL.md` — personal, gitignored. Created via
   `/skill install <path>` or by writing directly.

This skill covers authoring for both, with emphasis on builtin skills.

## When to Use

- User asks you to add a skill "in this repo / commit"
- You're committing a reusable workflow that should ship with Poirot
- You're editing an existing skill under `builtin_skills/`

## Required Frontmatter

Source of truth: `poirot/backend/agents/skill/parser.py::parse_skill_file`.
Hard requirements:

- Starts with `---` as the first bytes (no leading blank line).
- Closes with `\n---\n` before the body.
- Parses as a YAML mapping.
- `name` field present (lowercase, hyphens).
- `description` field present.

Peer-matched shape:

```yaml
---
name: my-skill-name               # lowercase, hyphens
description: Use when <trigger>. <one-line behavior>.
allowed-tools:                    # Poirot tools this skill may invoke
  - bash
  - read_file
  - write_file
  - list_dir
  - str_replace
  - web_search
  - browse_page
  - present_files
  - read_snapshot
enabled: true
related-skills: [other-skill]     # optional cross-references
license: MIT                      # recommended for contributed skills
author: <human contributor or source attribution>
---
```

`allowed-tools` / `enabled` / `related-skills` / `license` / `author` are NOT
enforced by the parser (it reads name/description/allowed-tools/enabled), but
every peer has them — omit and your skill sticks out.

## Description Standard

**`description` ≤ 60 characters**, one sentence, ends with a period. State the
capability, not the implementation. No marketing words ("powerful",
"comprehensive", "seamless"). Don't repeat the skill name.

Verify:
```python
import re, pathlib
m = re.search(r'^description: (.*)$',
              pathlib.Path('builtin_skills/<cat>/<name>/SKILL.md').read_text(),
              re.MULTILINE)
assert len(m.group(1)) <= 60, len(m.group(1))
```

## Size Limits

- Peer skills sit at **8-14k chars**. Aim for that range.
- If pushing past 20k, split into `references/*.md` and reference them from
  SKILL.md.

## Writing Quality Principles

A skill exists to make the agent's process more predictable. Predictability
does **not** mean identical output every run; it means the agent reliably
follows the same useful discipline.

1. **Optimize for process predictability.** Ask: what behavior should change
   when this skill loads? If a line does not change behavior, cut it.
2. **Choose the right context load.** A model-invoked skill pays for its
   description every turn. Keep descriptions focused on trigger classes and the
   skill's distinctive behavior. Put details in the body or linked references.
3. **Use an information hierarchy.** Put always-needed steps in `SKILL.md`; put
   branch-specific or bulky reference material in `references/`, `templates/`,
   or `scripts/` and point to it only when needed.
4. **End steps with completion criteria.** Each ordered step should say how the
   agent knows it is done. Good criteria are checkable: "every modified file
   accounted for" beats "summarize changes."
5. **Co-locate rules with the concept they govern.** Avoid scattering one idea
   across the file.
6. **Use strong leading words.** Prefer compact concepts the model already
   knows — "tight loop," "tracer bullet," "root cause," "regression test" —
   over long repeated explanations.
7. **Prune duplication and no-ops.** Keep each meaning in one source of truth.
   If a sentence doesn't change agent behavior vs the default, delete it.
8. **Watch for premature completion.** If agents tend to rush a step, sharpen
   that step's completion criterion.

Common quality failures:
- **Premature completion** — skill lets the agent move on before work is done
- **Duplication** — same rule in multiple places, drifts
- **Sediment** — stale lines remain because adding felt safer than deleting
- **Sprawl** — too much always-visible material; push branch-specific behind pointers
- **No-op prose** — generic advice the agent would follow without the skill

## Tool Reference Rules

Tools referenced in SKILL.md prose must be native Poirot tools (listed in
`allowed-tools`) or MCP servers the skill explicitly expects. Do NOT name shell
utilities the agent already has wrapped:

- `grep` → `bash` (run grep via bash)
- `cat`/`head`/`tail` → `read_file`
- `sed`/`awk` → `str_replace`
- `find`/`ls` → `list_dir`

## Peer-Matched Structure

```
# <Title>

## Overview
One or two paragraphs: what and why.

## When to Use
- Bulleted triggers
- "Don't use for:" counter-triggers

## <Topic sections specific to the skill>
- Quick-reference tables are common
- Code blocks with exact commands

## Common Pitfalls
Numbered list of mistakes and their fixes.

## Verification Checklist
- [ ] Checkbox list of post-action verifications
```

Not every section is mandatory, but `Overview` + `When to Use` + actionable
body + pitfalls are the minimum.

## Directory Placement

```
builtin_skills/<category>/<skill-name>/SKILL.md     # builtin
skills/<skill-name>/SKILL.md                         # user-local
```

Builtin categories: `core`, `research`, `software-development`, `creative`,
`productivity`. Pick the closest existing category. Don't invent new top-level
categories casually.

## Workflow

1. **Survey peers** in the target category:
   ```
   list_dir("poirot/backend/agents/skill/builtin_skills/<category>/")
   ```
   Read 2-3 peer SKILL.md files to match tone and structure.
2. **Draft** with `write_file` to `builtin_skills/<category>/<name>/SKILL.md`.
3. **Validate locally**:
   ```python
   import yaml, re, pathlib
   content = pathlib.Path("builtin_skills/<category>/<name>/SKILL.md").read_text()
   assert content.startswith("---")
   m = re.search(r'\n---\s*\n', content[3:])
   fm = yaml.safe_load(content[3:m.start()+3])
   assert "name" in fm and "description" in fm
   assert len(fm["description"]) <= 60
   ```
4. **Git add + commit** on the active branch.
5. **Note:** the current session's skill loader is cached — `/skill list` will
   not see the new skill until restart. This is expected.

## Cross-Referencing Other Skills

`related-skills` is documentation-only (parser ignores it). You can reference
any skill, but prefer referencing only builtin skills from builtin skills —
user-local skills won't resolve for other users.

## Editing Existing Skills

- **Small fix (typo, added pitfall):** `str_replace` on the SKILL.md.
- **Major rewrite:** `write_file` the whole SKILL.md.
- **Adding supporting files:** `write_file` to
  `builtin_skills/<category>/<name>/references/<file>.md`,
  `templates/<file>`, or `scripts/<file>`.
- **Always commit** the edit — builtin skills are source, not runtime state.

## Common Pitfalls

1. **Leading whitespace before `---`.** Parser requires `content.startswith("---")`;
   any leading blank line or BOM fails.

2. **Description too generic.** Peer descriptions start with the trigger class,
   not the one task. "Use when debugging X" > "Debug X".

3. **Description too long.** >60 chars bloats skill listings and dilutes model
   attention. Trim ruthlessly.

4. **Naming shell utilities.** `grep`/`cat`/`sed`/`find` → use Poirot tool
   names (`bash`/`read_file`/`str_replace`/`list_dir`). Otherwise the model
   hallucinates calls to non-existent tools.

5. **Writing a skill that duplicates a peer.** Before creating, `list_dir` the
   category and open 2-3 peers. Prefer extending an existing skill to creating
   a narrow sibling.

6. **Expecting the current session to see the new skill.** It won't. The skill
   loader initializes at startup. Verify in a fresh session.

7. **Letting skills accumulate sediment.** A skill should get shorter or sharper
   over time. When adding a rule, remove the old wording it replaces.

8. **Writing no-op prose.** "Be careful," "be thorough," "use best practices"
   rarely change model behavior. Replace with a checkable completion criterion.

## Verification Checklist

- [ ] File is at `builtin_skills/<category>/<name>/SKILL.md` (or `skills/<name>/`)
- [ ] Frontmatter starts at byte 0 with `---`, closes with `\n---\n`
- [ ] `name`, `description`, `allowed-tools`, `enabled` present
- [ ] `license`, `author` present (attribution)
- [ ] Name is lowercase + hyphens
- [ ] Description ≤ 60 chars and describes the trigger class
- [ ] Structure: `# Title` → `## Overview` → `## When to Use` → body → `## Pitfalls` → `## Verification`
- [ ] Each ordered step has a checkable completion criterion
- [ ] No shell utility names in prose (use Poirot tool names)
- [ ] No-op prose and duplicated rules removed
- [ ] `git add && git commit` completed

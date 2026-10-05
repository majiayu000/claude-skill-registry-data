---
name: <kebab-case-name>
description: <one-sentence trigger condition — when should this skill be loaded? Start with "Apply when ..." for consistency.>
license: MIT
version: 1.0.0
tokens_target: 1500
triggers:
  - <short trigger phrase>
  - <another phrase the router matches against>
loads_after: []
supersedes: []
---

# Sub-Skill: [Name]
<!-- target: tokens_target above. Run `python tools/render_readme_table.py` to update README. -->

**Purpose:** [1-2 sentences. What this sub-skill does and why it exists.]

---

## Rules

### [Category 1]

1. **[Rule name].** [Action directive — must start with Always, Never, Before, After, Prefer, Avoid, Use, Do, or Ensure.]
2. **[Rule name].** [Action directive.] Reference: ERR-YYYY-NNN
3. **[Rule name].** [Action directive.]

### [Category 2]

4. **[Rule name].** [Action directive.]
5. **[Rule name].** [Action directive.]

---

## See also

- `skills/code-quality/SKILL.md` (when this skill specialises a generic rule, link to it)
- `skills/error-log/SKILL.md` (errors that motivated rules in this skill)

---

## Notes

- **Frontmatter is mandatory.** The CI validator (`tools/validate_rules.py`) will fail any sub-skill without a valid frontmatter against `schemas/skill-manifest.json`.
- **Action directives, not descriptions.** "SQL injection is dangerous" is a description; "Never concatenate user input directly into SQL queries; always use prepared statements" is an action directive.
- **`Reference: ERR-YYYY-NNN`** on every rule born out of a real observed mistake.
- **Token budget under 3000.** When exceeded, split into thematic sub-skills with `loads_after` chains.

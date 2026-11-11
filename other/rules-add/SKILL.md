---
description: Add a rule to the set of rules
model: haiku
---

# Goal
- The user passes:
  - The description of a rule or behavior `<CONTENT>` to add to a rule file
  - (Optional) The target rule file `<TARGET_RULE_FILE>`, in the format
    `.claude/skills/*.rules.md`

# Workflow

## Read Skill Rules
- Read `.claude/skills/skill.rules.md` for the conventions and rules to write
  skills

## Determine Target Rule File
- If the user did not specify `<TARGET_RULE_FILE>`, pick the rule file that fits
  `<CONTENT>`
- The available rules are:
  ```bash
  > ls -1 .claude/skills/*.rules.md
  ```
- If `<CONTENT>` fits more than one file equally well, or fits none clearly, do
  not guess. Ask the user which `<TARGET_RULE_FILE>` to use, listing the candidate
  files

## Read Target Rule File
- Read `<TARGET_RULE_FILE>` to understand its structure and existing rules

## Draft the New Rule
- Draft the rule `<CONTENT>`, following `.claude/skills/markdown.rules.md` and
  `.claude/skills/text.rules.md`

## Add the New Rule
- Find the proper H1 header related to `<CONTENT>`
  - See `.claude/skills/skill.rules.md` `## Keep Rules Organized in the Rule File`
- Add `<CONTENT>` to `<TARGET_RULE_FILE>`, following `.claude/skills/skill.rules.md`
- Make sure it does not overlap with other rules

# Verification
- [ ] `<CONTENT>` is added under the correct H1 header in `<TARGET_RULE_FILE>`
- [ ] No existing rule in `<TARGET_RULE_FILE>` already covers `<CONTENT>`
- [ ] `<TARGET_RULE_FILE>` was confirmed with the user, not guessed, if it was
      ambiguous

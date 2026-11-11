---
description: Check the references in all the skill files
model: haiku
---

# Goal
- Check that all the skill and rule files have references

# Workflow

## Find Files
- Find all markdown files: `SKILL.md` and `<TOPIC>.rules.md`
  ```bash
  > find .claude/skills -name "*.md"
  ```

## Read Context
- Read `.claude/skills/skill.rules.md` for context on rules

## Check Rules
- For each file, apply all the rules below and report violations as described

### Check Files Existence
- Make sure the file follows `.claude/skills/skill.rules.md`
  `# SKILL.md File Format`

### Check Header References
- Make sure the file follows `.claude/skills/skill.rules.md`
  `# References and Dependencies`

### Check for Other Violations
- Use the rules in `.claude/skills/skill.rules.md` to find clear violations
- Report a violation only when certain it is one

## Report Violations
- Report all violations in a file `cfile` using the format in
  `.claude/skills/cfile.rules.md`

## Ask the User Which Problems to Fix
- Ask which problems to fix by printing a numbered list of problems

# Verification
- [ ] Every file under `.claude/skills` matching `SKILL.md` or `<TOPIC>.rules.md`
      was checked
- [ ] `cfile` follows the format in `.claude/skills/cfile.rules.md`
- [ ] Every reported violation is one the reviewer is confident about

---
description: Check the format of a blog file
model: haiku
---

# Goal
- Check that all the actual and the draft blogs have the correct format

# Workflow

## Find Files
- Find all markdown files, both `SKILL.md` and `<TOPIC>.rules.md`
  ```bash
  > find website/docs/blog/posts -name "*.md"
  ```

## Read Context

- Read the rules in
  - `.claude/skills/blog.rules.md`
  - `.claude/skills/markdown.rules.md`
  - `.claude/skills/text.rules.md`

## Check Rules
- Apply all the rules below to each file and report violations

### Check Front Matter
- Follow `# Blog Document Structure` in `.claude/skills/blog.rules.md`

### Check that Has a TL;DR
- Follow `# Blog Document Structure` in `.claude/skills/blog.rules.md`

### Check for Other Violations
- Use `.claude/skills/blog.rules.md` to find clear violations
- Report a violation only when confident about it

## Report Violations

- Report all violations in a file `cfile` using the format in
  `.claude/skills/cfile.rules.md`

## Ask Users Whether to Fix the Problems
- Print a list of problems with indices and ask the user which to fix

# Verification
- [ ] Confirm `cfile` lists concrete file and line references for each
      violation
- [ ] Confirm each reported violation maps to a rule in
      `.claude/skills/blog.rules.md`

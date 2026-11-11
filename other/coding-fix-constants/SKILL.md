---
description: Move constants to their correct scope based on usage
model: haiku
---

Move constants to the narrowest scope that uses them. Make a constant private
when it is not part of the module's public interface.

# Conventions
- Follow the section `# Constants` from the file `.claude/skills/coding.rules.md`
  for constant definitions and names

# Verification
- [ ] Confirm each constant sits in the smallest scope that uses it (local,
      module-private, or module-public)
- [ ] Confirm module-private constants are prefixed with `_`

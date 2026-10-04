---
name: migrate
description: Migrates code between frameworks, versions, or patterns safely
---

When migrating ($ARGUMENTS):

1. **Analyze current state**:
   - Identify the source framework/version/pattern
   - Map all usages and dependencies
   - Check for breaking changes in target

2. **Plan migration**:
   - List all files that need changes
   - Identify deprecated APIs and their replacements
   - Note any new dependencies needed

3. **Execute incrementally**:
   - Update one module/file at a time
   - Replace deprecated APIs with new equivalents
   - Update imports and type definitions
   - Adjust configuration files

4. **Verify each step**:
   - Run tests after each change
   - Check for TypeScript errors
   - Ensure no runtime regressions

5. **Cleanup**:
   - Remove unused dependencies
   - Update package.json versions
   - Document any manual steps needed

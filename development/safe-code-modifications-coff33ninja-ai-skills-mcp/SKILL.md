---
name: safe-code-modifications
description: Ensures code modifications follow safe practices - never remove imports/items without verifying usage, check if truly obsolete, and confirm usage by other modules before removal.
---

# Safe Code Modifications Skill
This skill helps developers make safe code changes by enforcing these principles:
## Core Principles
1. **Never remove imports or code items without verification**
   - Always check if an import/item is actually used in the current file
   - Verify usage across the project before removal
   - Use IDE tools: "Find References", "Go to Definition", "Show Usages"
2. **Determine if items are truly obsolete**
   - Check if imported but never used (but be careful - might be for side effects)
   - Verify if functions/variables are referenced elsewhere in the project
   - Consider if they're part of an API contract or public interface
3. **Check cross-module usage**
   - Search for imports/usage in other files
   - Determine if it's a shared utility or library dependency
   - Verify if it's used in tests, configuration, or documentation
4. **Safe removal process**
   - Comment out temporarily with TODO if unsure
   - Run tests to ensure nothing breaks
   - Remove only when certain it's unused and not part of an interface
## Implementation Guidelines
### When encountering potentially unused imports:
**DO:**
- Search the entire codebase for references: `grep -r "importName" ./src`
- Check if the import has side effects (e.g., registers something, modifies globals)
- Look for conditional usage or usage in build scripts
- Consider if it's used by IDEs or tools (like type-only imports in TypeScript)
**DON'T:**
- Remove based solely on linter warnings without investigation
- Assume unused means safe to remove
- Remove without checking test files
### When considering removing functions, variables, or constants:
**DO:**
- Check if it's part of a public API (exported from module)
- Verify if it's used in documentation or examples
- Look for dynamic usage (e.g., accessed via bracket notation)
- Consider if it's used in reflection or dependency injection
**DON'T:**
- Remove public API without deprecation period
- Assume internal means unused
- Remove without checking if it's referenced in strings (e.g., for factory patterns)
### Special considerations for different languages:
**Python:**
- Check `__all__` exports
- Look for `import *` usage
- Consider plugin architectures that discover modules dynamically
**JavaScript/TypeScript:**
- Check for dynamic imports: `import()` expressions
- Look for webpack code splitting
- Consider module augmentation patterns
**Go:**
- Check for blank imports (`_ "package"`) for side effects
- Look for interface implementations
- Consider build tags and platform-specific files
## Verification Process
Before removing any code item:
1. **Search**: Use comprehensive search across entire codebase
2. **Context**: Understand why the item was added originally
3. **Impact**: Determine what breaking changes would occur
4. **Documentation**: Update README/docs if removing public API
5. **Deprecation**: Consider deprecation warning before removal
6. **Testing**: Ensure tests still pass after removal
## When to Use This Skill
Use this skill when:
- You're considering removing imports, functions, variables, or other code items
- You're refactoring code and want to ensure safe removal
- You're reviewing pull requests that involve code removal
- You're maintaining legacy code and unsure about usage
- You're working with code you didn't originally write
Use ONLY when you're making decisions about code removal or modification where usage verification is critical.
## Examples
**Bad practice:**
```python
# Removing import without checking
# import unused_module  # Just deleted because linter complained
```
**Good practice:**
```python
# After thorough verification:
# 1. Searched entire codebase: no references found
# 2. Checked for side effects: none
# 3. Verified not used in tests or docs
# 4. Confirmed safe to remove
# Removed: import unused_module
```
## References
- Language-specific documentation on dead code elimination
- Best practices for API deprecation
- IDE documentation for code navigation and refactoring tools
This skill follows your requested guidelines by:
1. Emphasizing never to remove imports/items without verification
2. Providing specific methods to check if items are truly obsolete
3. Including guidance on checking cross-module usage
4. Focusing on safe removal processes

## Bundled Script

Copy `check-imports.ps1` to your project's `.ai_scripts/` directory:

```powershell
cp <skill-path>/safe-code-modifications/scripts/check-imports.ps1 .ai_scripts/
```

Scans a source file for imports and reports which have zero references — use to verify before any removal:

```powershell
.ai_scripts\check-imports.ps1 -FilePath src/foo.py -ProjectPath .
```

## Cross-references

- **no-dead-code-removal** — Direct overlap. safe-code-modifications verifies usage before removal; no-dead-code-removal says refactor instead of delete.

- **unused-import-implementation** — When an import is flagged unused, this completes the intended usage instead of removing it.

- **anti-phantom-symbols** — Verifying symbol existence before modification prevents phantom symbol errors.
- **skill-loader** — Apply the capped selection policy when deciding which code-safety skills should also be active before modifications.

---
name: pattern-migrator
description: Systematic approach for migrating patterns between directories in Storybook-based design systems while maintaining cross-references and documentation integrity. Use this skill when reorganizing Storybook structure, moving patterns to new categories, refactoring documentation hierarchy, or performing bulk pattern migrations that require careful tracking of Meta titles, URLs, and cross-references.
---

# Pattern Migrator

## Overview

This skill provides a systematic workflow for migrating patterns between directories in a Storybook-based design system. It ensures all cross-references, Meta titles, URL patterns, and documentation links remain intact throughout the migration process.

## When to Use This Skill

Apply this skill when:
- Reorganizing Storybook directory structure
- Moving patterns to different categories
- Consolidating or splitting pattern collections
- Refactoring documentation hierarchy
- Performing bulk pattern migrations
- Any task requiring careful tracking of Storybook URLs and cross-references

## Migration Workflow

Follow this five-phase sequential process for reliable pattern migrations:

### Phase 1: Analysis and Planning

Before making any changes, gather comprehensive context about the migration scope:

**1. Directory Inventory**
- Use Glob or Bash tools to list all files in source and target directories
- Identify pattern types:
  - Simple `.mdx` files (documentation only)
  - `.mdx` with companion `.stories.tsx` files
  - Complex directories with multiple file types (TypeScript, JSON, CSS, HTML)

**2. Meta Title Extraction**
- Read all `.mdx` files to identify current Meta component titles
- Record both explicit titles (`<Meta title="Category/Name" />`) and story references (`<Meta of={PatternStories} />`)
- For story references, locate and read the corresponding `.stories.tsx` file to find the Meta title

**3. Cross-Reference Mapping**
- Search for internal Storybook links within pattern files
- Identify all references following the pattern: `../?path=/docs/[category-name]--docs`
- Document incoming references (other patterns linking to this one)
- Document outgoing references (this pattern linking to others)

**4. Create Migration Plan**
- Draft a markdown file listing:
  - Patterns to migrate (source → destination paths)
  - Current and new Meta titles
  - URL transformations (old → new Storybook URLs)
  - Identified cross-references requiring updates
  - Timeline and validation steps

### Phase 2: File Structure Migration

Execute file moves systematically, handling each pattern type appropriately:

**Simple Files (.mdx only)**
1. Move file to new location using `mv` or git commands
2. Update Meta title to reflect new category structure
3. Update any internal cross-references within the file
4. Search codebase for external references to this pattern

**Complex Patterns (with stories/components)**
1. Move entire directory structure to preserve file relationships
2. Update Meta title in `.stories.tsx` file
3. Check for and update import path dependencies in TypeScript files
4. Update internal cross-references in `.mdx` files
5. Search codebase for external references to this pattern

**Important**: Use `git mv` when working in a git repository to preserve file history.

### Phase 3: URL Reference Updates

Understand Storybook URL transformation rules and update all references:

**URL Transformation Rules**
Storybook generates URLs from Meta titles following these rules:
- `<Meta title="Category/Name" />` becomes `../?path=/docs/category-name--docs`
- Transformations:
  - Spaces → hyphens
  - Uppercase → lowercase
  - Asterisks (*) → removed from URLs
  - Forward slashes (/) → hyphens

**Search Strategy**
1. **Global search**: Use Grep to find all instances of old URL patterns across the entire codebase
   - Pattern: `../?path=/docs/old-category-pattern-name--docs`
2. **Pattern-specific searches**: Search for each moved pattern individually
3. **Cross-reference updates**: Update all found references to use new URL patterns
4. **Import path updates**: If TypeScript files import from moved patterns, update import statements

### Phase 4: Documentation Updates

Ensure all supporting documentation reflects the new structure:

**Update Documentation Files**
- Overview or index files that list patterns
- CLAUDE.md if it references the old directory structure
- README files that mention the affected patterns
- Any hierarchy or navigation documentation

**Verify Documentation Standards**
- Ensure British spelling throughout (behaviour, organisation, colour)
- Use sentence case for headings and titles
- Follow project-specific documentation linking standards

### Phase 5: Validation

Confirm the migration succeeded without breaking functionality:

**1. Build Test**
Run Storybook build to check for errors:
```bash
npm run build-storybook
```

**2. Link Verification**
- Start Storybook in development mode
- Navigate through documentation to verify all links work
- Check that moved patterns appear in correct categories
- Verify cross-references open the correct documentation

**3. TypeScript Compilation**
If the project uses TypeScript:
```bash
npm run typecheck
```

**4. Cross-Reference Audit**
- Systematically verify internal documentation links function
- Check that no references point to old locations
- Confirm no broken links appear in the Storybook interface

## File Types and Handling

### Documentation Files
- **Simple .mdx**: Move file, update Meta title, update references
- **Complex .mdx**: Move file, update Meta title, update references, verify companion files moved

### Story Files
- **.stories.tsx**: Update Meta title, check import paths, move with companion .mdx file

### Support Files
- **TypeScript files** (.ts, .tsx): Check import paths, move with pattern directory
- **JSON data files**: Move with pattern, check import references
- **HTML templates**: Move with pattern, check references
- **CSS files**: Move with pattern, check import paths

## Risk Mitigation

### Pre-Migration Checklist
- [ ] Full pattern inventory completed
- [ ] All cross-references documented
- [ ] Migration plan reviewed and approved
- [ ] Backup or version control commit made

### During Migration
- [ ] Test build after each major pattern migration
- [ ] Update references immediately after moving files
- [ ] Document any unexpected issues or discoveries

### Post-Migration Validation
- [ ] Full Storybook build succeeds
- [ ] All documentation links function correctly
- [ ] No broken imports in TypeScript compilation
- [ ] Cross-reference audit completed

## Success Criteria

A successful migration results in:
- All patterns accessible in new Storybook locations
- All cross-references functioning correctly
- No broken links in documentation
- Clean TypeScript compilation
- Successful Storybook build
- All import paths resolving correctly

## References

For detailed technical specifications, command examples, and additional guidance, consult the comprehensive migration guide in `references/pattern-migration-guide.md`.

The reference guide includes:
- Detailed command examples
- Common URL reference patterns
- Template code snippets
- Additional risk mitigation strategies

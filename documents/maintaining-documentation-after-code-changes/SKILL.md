---
name: Maintaining Documentation After Code Changes
description: Two-phase workflow to keep project documentation synchronized with code changes
when_to_use: when completing features or bugfixes, before merging branches, when git diff shows significant changes, or when documentation feels stale or out of sync with code
version: 1.0.0
languages: all
---

# Maintaining Documentation After Code Changes

## Overview

**Documentation drift is inevitable without systematic maintenance.** Code evolves rapidly while documentation becomes stale. This skill provides a two-phase workflow to keep project docs synchronized with code: analyze recent changes, then update and restructure documentation accordingly.

## When to Use

Use this skill when:
- Completing features or bugfixes (before marking work complete)
- Preparing to merge branches or create pull requests
- Git diff shows significant code changes
- Documentation feels stale, incomplete, or contradicts current code
- New functionality added without corresponding doc updates
- Onboarding reveals outdated or missing documentation
- API changes or new commands/tasks added
- Implementation challenges revealed better practices

**When NOT to use:**
- During active development (docs can lag slightly, update at checkpoints)
- For trivial changes (typo fixes, formatting)
- When no code has changed

## Critical Principle

**Maintaining existing documentation after code changes is NOT "proactively creating docs" - it's keeping current docs accurate.**

CLAUDE.md instructions about "don't proactively create documentation" apply to NEW documentation files for undocumented features. They do NOT apply to maintaining existing documentation after you change the code it documents.

**If you changed the code, you must update the corresponding documentation. No exceptions.**

## Common Rationalizations (And Why They're Wrong)

| Rationalization | Reality |
|----------------|---------|
| "I'll update docs in a follow-up PR" | Later rarely happens. Context is freshest now. Capture it. |
| "Commit messages are documentation enough" | Commit messages explain code changes, not user workflows. Both are needed. |
| "Code is self-documenting if well-written" | Code shows HOW. Docs explain WHY and usage patterns. Different purposes. |
| "Time pressure means ship now, document later" | Shipping undocumented changes creates support burden > time saved. |
| "Don't know if user wants docs updated" | If code changed, docs MUST update. Not optional. Ask about scope, not whether. |
| "Documentation is maintenance overhead" | Outdated docs are overhead. Current docs save time for everyone. |
| "Minimal accurate > comprehensive outdated" | False choice. This skill gives you accurate AND complete in 15-30 min. |
| "Different teams handle docs differently" | This skill IS the standard for this project. Follow it. |
| "Risk of making commit scope too large" | Documentation changes belong with code changes. Same PR = atomic change. |
| "Best practices docs only change for patterns" | If you discovered lessons during implementation, they belong in CLAUDE.md. |

**None of these are valid reasons to skip documentation maintenance.**

## Quick Reference

| Phase | Focus | Key Activities |
|-------|-------|----------------|
| **Analyze** | What changed? | git diff → review docs → identify gaps |
| **Update** | Sync docs | Update content → restructure → summarize changes |

## Implementation

### Phase 1: Analysis

**Goal:** Understand what changed and what documentation needs updating

1. **Review recent changes:**
   ```bash
   git diff [base-branch]...HEAD
   ```
   Examine the full diff to understand scope of changes

2. **Check existing documentation:**
   - README.md (main project docs)
   - CLAUDE.md (AI assistant guidance)
   - README_*.md (specialized documentation)
   - docs/ directory (practices, examples, plans)
   - Any project-specific doc locations

3. **Identify documentation gaps:**
   - New features without usage examples
   - Changed APIs without updated references
   - Implementation lessons not captured in CLAUDE.md
   - New best practices discovered during work
   - Implementation challenges and solutions
   - Known issues or limitations discovered
   - Commands/tasks that changed behavior

**Output of analysis phase:** List of specific documentation updates needed

### Phase 2: Update

**Goal:** Bring documentation into sync with current code

1. **Update content to reflect changes:**
   - Add new sections for new features
   - Update changed functionality (especially examples)
   - Document implementation details for complex components
   - Update usage examples with new functionality
   - Add troubleshooting tips from recent issues
   - Update best practices based on experience
   - Verify commands/tasks reflect current behavior

2. **Restructure for clarity:**
   - Remove outdated or redundant content
   - Group related topics together
   - Split large files if they've grown unwieldy
   - Fix broken cross-references
   - Ensure consistent formatting

3. **Document updates:**
   Provide summary of changes:
   - Files updated
   - Major documentation changes
   - New best practices added
   - Sections removed or restructured

## Documentation Standards

Follow project documentation standards defined in:
- ${CLAUDE_PLUGIN_ROOT}standards/documentation.md

**Key standards to verify:**
- Formatting and structure (headings, examples, status indicators)
- Content completeness (usage examples, troubleshooting)
- README organization (concise main file, README_*.md for specialized docs)

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Updating only README, missing other docs | Check CLAUDE.md, README_*.md, docs/ systematically |
| Not reviewing git diff | Always start with full diff to understand scope |
| Describing "what" without "why" | Explain rationale, not just functionality |
| Forgetting to update examples | Changed APIs must update all examples |
| Batch updating at project end | Update at natural checkpoints (feature complete, before merge) |
| Restructuring separately from updates | Restructure while updating to prevent redundant passes |
| Missing troubleshooting updates | Document edge cases and solutions discovered during work |

## What NOT to Skip

**These are consistently skipped under pressure. Check explicitly:**

**✅ MUST check every time:**
- [ ] git diff reviewed (full diff, not just summary)
- [ ] CLAUDE.md updated (best practices, lessons learned, implementation patterns)
- [ ] All README*.md files checked and updated
- [ ] Practices docs (principles/standards/workflows) updated if patterns changed
- [ ] docs/examples/ updated if usage changed
- [ ] Usage examples updated (not just prose)
- [ ] Troubleshooting section updated (if you debugged issues)
- [ ] Cross-references verified (links still work)

**Common blind spots:**
- CLAUDE.md (agents forget this captures lessons learned)
- Usage examples (agents update text but not code examples)
- Troubleshooting sections (agents assume commit messages are enough)
- Practices documentation (agents think only patterns change these)

## Red Flags - STOP and Review Docs

**Situations:**
- About to merge without checking documentation
- Examples still show old API or command syntax
- CLAUDE.md doesn't mention new patterns/practices discovered
- Onboarding someone would miss new functionality
- Can't remember what changed (didn't check git diff)
- Just finished debugging but no troubleshooting docs added

**Rationalizations (means you're about to skip docs):**
- "I'll update docs later"
- "Commit message is enough"
- "Code is self-documenting"
- "Time pressure"
- "User said ship it"
- "Not sure what user wants"
- "Different teams do it differently"
- "Don't want to overstep"

**All of these mean: Stop and run this workflow before proceeding.**

## Real-World Impact

**Without systematic maintenance:**
- Onboarding takes longer (outdated docs)
- Best practices lost (not captured in CLAUDE.md)
- Teammates confused by stale examples
- Support burden increases (troubleshooting not documented)
- Knowledge silos (changes not shared)

**With this workflow:**
- Documentation stays current
- Best practices captured immediately
- Onboarding smooth and accurate
- Troubleshooting knowledge preserved
- Team aligned on current patterns

## Integration with Commands/Agents

This skill can be invoked by:
- Commands that dispatch to doc-writer subagent
- Manual workflow when preparing to merge
- Pre-merge checklist item
- Code review requirement

Commands should provide context about documentation practices and reference this skill for methodology.

---
name: updating-documentation-for-changes
description: Use before committing staged changes when you need to verify all related documentation is current - systematically checks README, CLAUDE.md, CHANGELOG, API docs, package metadata, and cross-references rather than spot-checking only obvious files
---

# Updating Documentation for Changes

## Overview

**Before committing staged changes, systematically verify ALL documentation that might reference those changes.**

The problem: We naturally check the "obvious" doc (README.md) but miss CLAUDE.md, CHANGELOG, API documentation, package metadata, and cross-references in related docs.

## When to Use

Use this skill when:

- You have staged changes ready to commit
- You're about to create a PR
- You've modified functionality, added features, or changed behavior
- Any code change that users or other agents interact with

**Required trigger**: Before every commit with functional changes.

## Core Principle

**This skill checks documentation consistency for STAGED changes only.**

Do NOT stage additional files during this process. Only verify if documentation for your staged changes is current.

## The Systematic Documentation Sweep

Follow this checklist in order. No skipping "obvious" items.

### 1. Identify What's Staged

```bash
git diff --staged --name-only
git diff --staged
```

Note: What was added? Modified? What does it affect?

**If nothing is staged:** Stop. Tell user to stage their changes first, then return to this skill.

### 2. Core Documentation Files (Check if they exist)

Check EVERY one that exists in the repo (no rationalization):

- [ ] **README.md** (root and subdirectories)
- [ ] **CLAUDE.md** (project conventions, architecture, patterns)
- [ ] **DESIGN_DOC.md** or **ARCHITECTURE.md** (system design)
- [ ] **CONTRIBUTING.md** (contribution guidelines)
- [ ] **API.md** or **docs/api/** (API documentation)
- [ ] **CHANGELOG.md** or **HISTORY.md** (version history)

**This list is not comprehensive.** If the project has other documentation, check those too. Examples: TESTING.md, DEPLOYMENT.md, SECURITY.md, project-specific guides.

**If a core doc doesn't exist:** Note its absence but don't create it as part of this commit.

### 3. Project-Specific Documentation

Check documentation specific to this project type:

**For libraries/packages:**

- [ ] **Package metadata** (package.json, pyproject.toml, setup.py, Cargo.toml - check if exports/APIs changed)
- [ ] **docs/** directory (API docs, guides, examples)

**For web services:**

- [ ] **OpenAPI/Swagger specs** (if API changed)
- [ ] **docker-compose.yaml** comments (if deployment changed)
- [ ] **Config examples** (if config structure changed)

**For other projects:**

- Identify key documentation by searching for \*.md files
- Check files in `docs/`, `documentation/`, or similar directories

**Consistency check:** If you find multiple related files (like `package.json` and `README.md` version numbers), verify they're consistent.

### 4. Related Documentation Search

Search for files that might reference your changes:

```bash
# Search for direct feature name
grep -r "exact-feature-name" --include="*.md" --include="*.json"

# Search for related terms (if changing auth, search: auth, login, session)
grep -r "related-concept" --include="*.md" --include="*.json"

# Search for command names if you modified commands
grep -r "command-name" --include="*.md" --include="*.json"
```

Check cross-references:

- Do other documentation files reference this feature?
- Does the architecture documentation describe this pattern?
- Do examples or tutorials use this functionality?
- Are there related features that should be updated together?

**Search depth limit**: Check one level of cross-references. If doc A references feature B, check doc B. Don't recursively check doc B's references.

### 5. Determine Update Significance

Update higher-level docs (README, package metadata, CHANGELOG) if your change:

- **Adds** new user-facing commands, flags, features, or APIs
- **Changes** existing behavior in a way users will notice
- **Removes** functionality mentioned in high-level descriptions
- **Expands** core capabilities described in the summary
- **Modifies** configuration structure or deployment steps

Do NOT update higher-level docs if your change:

- Adds implementation details or internal techniques
- Improves existing behavior without changing interface
- Refactors internal code without external impact
- Adds examples or clarifications to existing docs
- Fixes bugs without changing documented behavior

**When in doubt:** Check if a user relying on current high-level docs would be surprised by your change. Surprised = update needed.

### 6. Update What's Outdated

For each outdated doc:

1. Read the full section (not just the line that mentions it)
2. Update to match new behavior
3. Check examples still work
4. Verify cross-references are accurate

**Stage updates after sweep:** Note what needs updating during the sweep, then stage those documentation changes after you've completed the full checklist.

### 7. Handle Unrelated Outdated Documentation

If you discover unrelated outdated docs during your sweep:

- **Note it** for later (mention to user after sweep)
- **Don't fix it** in this commit (keeps changes focused)
- **Don't skip the rest of the sweep** (finding one issue doesn't mean you're done)

## Common Rationalizations - STOP

If you're thinking any of these, you're about to skip necessary docs:

| Rationalization                                       | Reality                                                                  |
| ----------------------------------------------------- | ------------------------------------------------------------------------ |
| "It's just a small change"                            | Small changes break outdated examples. Check anyway.                     |
| "Nothing actually changed"                            | Even if smaller than expected, complete the sweep to verify consistency. |
| "If related docs existed, I'd know"                   | You don't know until you search. Search systematically.                  |
| "That file is technical config"                       | Plugin manifests ARE user-facing. Check them.                            |
| "User is waiting"                                     | 3 minutes now saves 30 minutes debugging confusion later.                |
| "I already checked the main README"                   | README ≠ all documentation. Follow the full checklist.                   |
| "Other skills wouldn't reference this"                | They might. Search, don't assume.                                        |
| "The change is in the code itself"                    | Code ≠ documentation. Users read docs, not your diff.                    |
| "I found unrelated outdated docs, I should fix those" | Note for later. Stay focused on staged changes.                          |
| "Found one issue, good enough"                        | One issue doesn't mean you're done. Complete the sweep.                  |

**All of these mean: Continue with the systematic sweep.**

## Red Flags - You're Skipping Something

- Checked only README.md
- Didn't search for cross-references
- Skipped plugin manifest as "just config"
- Assumed other skills are independent
- Used time pressure to justify incomplete check
- Thought "minor change doesn't need full sweep"
- Started staging additional documentation before completing the sweep
- Stopped after finding first inconsistency

**Any red flag = Start over with full checklist.**

## Real-World Impact

**Without systematic sweep:**

- Users miss new features (not in README)
- API consumers hit undocumented breaking changes (package metadata stale)
- Examples break (outdated patterns in docs)
- Cross-references dangle (related docs out of sync)
- Inconsistent information across README, CHANGELOG, and package files
- Support burden increases (users confused by outdated docs)

**With systematic sweep:**

- All entry points updated (README, API docs, CHANGELOG)
- Discovery works (accurate package metadata, search results)
- Examples current and runnable
- Cross-references intact
- Consistent information across all documentation
- Reduced support questions and confusion

## Summary Checklist

Before committing, have you:

- [ ] Identified what's staged (`git diff --staged`)
- [ ] Checked all core documentation files that exist (README, CLAUDE.md/AGENTS.md, DESIGN_DOC, CONTRIBUTING, API docs, CHANGELOG)
- [ ] Checked project-specific documentation (package metadata, API specs, config examples, etc.)
- [ ] Verified consistency between related files (e.g., package.json version vs README version)
- [ ] Searched for cross-references (grep with feature name and related terms)
- [ ] Determined update significance (does behavior change warrant high-level doc updates?)
- [ ] Updated outdated docs (or noted what needs updating)
- [ ] Noted any unrelated outdated docs for later
- [ ] Completed the full sweep without rationalizing shortcuts

**All checked?** You're ready to commit or stage documentation updates.

---
name: write-release-notes
description: Generate professional Bytebase release notes by analyzing git commits, checking Terraform impact, searching Linear for customer feedback, and following established conventions. Creates Linear tracking issue and owner confirmation comments (with user approval before each write operation). Use when preparing release notes for minor or patch versions.
---

# Release Notes Generator

A systematic skill for generating professional Bytebase release notes by analyzing git commits, checking Terraform impact, and following established conventions.

## Overview

This skill helps you create release notes for Bytebase releases by:
1. Determining release version (minor vs patch) from branch names
2. Extracting commits between versions
3. Analyzing code changes to understand impact
4. Checking Terraform configuration implications
5. Searching Linear for customer feedback
6. Learning from previous release note patterns
7. Categorizing and prioritizing changes with ownership
8. Writing concise, user-focused release notes (no implementation details or reasoning)
9. Saving draft to `docs/release-notes/draft-X.Y.Z.md` for iteration
10. Creating Linear issue with title `<version>-<date>_release_note` **(with user confirmation)**
11. Adding confirmation comments with proper @mentions for each owner **(with user confirmation)**

**Note**: All Linear write operations (creating issues, posting comments) require explicit user confirmation before execution.

## Step-by-Step Process

### Phase 1: Version Identification (CRITICAL)

#### 1.1 Find the Version Range

```bash
# List available tags
git tag --list "*<major>.<minor>*" | sort -V

# Check for release branches
git branch -a | grep -E "release/<major>.<minor>"

# Get the latest tag
git describe --tags --abbrev=0
```

#### 1.2 Determine Version Type

**IMPORTANT**: The version type affects what sections are allowed in the release notes.

| Version Change | Type | Example |
|----------------|------|---------|
| 3.12.x → 3.13.0 | **Minor** | Minor digit increases |
| 3.12.0 → 3.12.1 | **Patch** | Patch digit increases |

**Rules by version type:**

| Section | Minor Version | Patch Version |
|---------|--------------|---------------|
| Notable Changes | ✅ Expected | ⚠️ Unusual - confirm with user |
| Features | ✅ Expected | ⚠️ Unusual - confirm with user |
| Enhancements | ✅ Yes | ✅ Yes |
| Bug Fixes | ✅ Yes | ✅ Yes (primary focus) |

#### 1.3 Confirm Version with User

**ALWAYS confirm the version before proceeding:**

```
I've identified the following version information:
- Previous version: [X.Y.Z]
- New version: [A.B.C]
- Version type: [Minor/Patch]

Is this correct? If not, please provide the correct versions.
```

**If you cannot determine versions from branches/tags, ASK the user immediately.**

### Phase 2: Data Collection

#### 2.1 Extract All Commits

```bash
# If new version is tagged
git log <prev-version>..<new-version> --oneline --decorate

# If new version is a release branch (common case)
git log <prev-version>..origin/release/<new-version> --oneline --decorate
```

**Output**: List of all commits with their hashes and one-line messages.

#### 2.2 Create Analysis Task List

Use TodoWrite to create tasks:
- Batch commits into groups of 5-7
- One task per batch for analysis
- Task for Terraform impact check
- Task for Linear issue search
- Final task for compilation

### Phase 3: Commit Analysis

#### 3.1 Examine Each Commit in Parallel

For each batch, run these in parallel:

```bash
git show --stat <commit-hash>
```

**What to extract from each commit:**
- **Files changed**: Indicates scope (frontend/backend/proto/parser)
- **Lines added/removed**: Indicates magnitude
- **Commit message**: Describes intent
- **Changed components**: Identifies affected areas
- **Author**: For ownership tracking

#### 3.2 Identify Change Owner

For each significant change, identify the owner:

```bash
# Get the author with most changes for a feature area
git log <prev-version>..origin/release/<new-version> --format='%an' -- <path-pattern> | sort | uniq -c | sort -rn | head -1

# For a specific commit
git show --format='%an <%ae>' -s <commit-hash>
```

**Document the owner for each release note item** - we need to confirm correctness with them.

#### 3.3 Check for Related PRs (Same Linear Issue)

**IMPORTANT**: Multiple PRs may implement or fix the same Linear issue. Before categorizing, check if commits are related:

1. Look at PR descriptions for Linear issue references (e.g., "BYT-8543" or "fixes BYT-xxxx")
2. Check if one PR "follows" or "builds on" another PR
3. Use `gh pr view <number> --json title,body` to see PR details

**If multiple PRs are for the same Linear issue:**
- Consolidate into a **single release note item**
- Use the Linear issue title/description to understand the user-facing problem
- Credit all owners in the confirmation

**Example:**
```
# These two PRs are both for BYT-8543:
PR #18582: "fix: bring issue label limit back" (quick fix)
PR #18586: "refactor(plan): show issue labels in two-step creation flow" (follow-up UX improvement)

# Consolidate to single item:
- Fix issue label selector missing in new CI/CD layout (BYT-8543)
```

#### 3.4 Categorize Each Commit

Use this decision tree:

```
Is it a breaking change or behavior change?
├─ YES → Notable Changes (⚠️ If patch version, flag for confirmation)
└─ NO
   ├─ Does it fix a bug/issue?
   │  └─ YES → Bug Fixes
   └─ NO
      ├─ Is it a new capability?
      │  └─ YES → Features (⚠️ If patch version, flag for confirmation)
      └─ Is it an improvement/optimization?
         └─ YES → Enhancements
```

**Specific patterns:**

| Commit Pattern | Category | Example |
|----------------|----------|---------|
| `fix:` prefix | Bug Fixes | `fix: SQL Editor tab caching` |
| `feat:` new capability | Features | `feat: IdP-initiated SSO` |
| `feat:` improvement | Enhancements | `feat: MSSQL explain visualization` |
| `refactor:` with user impact | Enhancements | `refactor: webhook message` |
| `refactor:` no user impact | Omit | `refactor: internal helper` |
| `chore:` with user impact | Enhancements | `chore: optimize SQL editor tabs` |
| `chore:` no user impact | Omit | `chore: update dependencies` |
| Validation ERROR→WARNING | Notable Changes | MySQL validation rules |
| Security restriction | Notable Changes or Enhancements | IAM credential restrictions |
| Parser migration | Enhancements | Doris parser upgrade |

### Phase 4: Terraform Impact Check (CRITICAL)

#### 4.1 Check for Terraform-Affecting Changes

For EACH categorized change, check if it affects Terraform configuration:

```bash
# Search for changes to Terraform-related files
git show --stat <commit-hash> | grep -E "(terraform|provider|resource)"

# Check API changes that might affect Terraform
git show --stat <commit-hash> | grep -E "proto/v1/(project|database|instance|environment|setting|policy)"

# Check for resource name/field changes
git show <commit-hash> -- "proto/**/*.proto" | grep -E "(field|option|message|enum)"
```

**Key areas that affect Terraform:**

| Change Area | Terraform Impact | Check Files |
|-------------|-----------------|-------------|
| API field rename/remove | **Breaking** - config update required | `proto/v1/*.proto` |
| New API field | May need config update | `proto/v1/*.proto` |
| Resource behavior change | May affect state | Backend handlers |
| Default value change | May affect plan/apply | Service layer |
| Validation rule change | May cause apply failures | Validators |

#### 4.2 Document Terraform Impact

For changes that affect Terraform, add to the release note:

```markdown
- [Change description] (**Terraform**: [impact description, e.g., "update `bytebase_instance` resource field `x` to `y`"])
```

**Example:**
```markdown
- Rename environment resource field from `tier` to `environment_tier` (**Terraform**: update `bytebase_environment` resource configuration to use new field name)
```

### Phase 5: Linear Issue Search

#### 5.1 Search for Customer Feedback

Use Linear MCP tools to find customer-reported issues:

```
mcp__linear__list_issues with:
- query: relevant keywords from commits
- labels: "customer-feedback", "bug", "customer-reported"
```

**Search strategies:**
1. Search by feature area mentioned in commits
2. Search by database engine names
3. Search by component names (SQL Editor, Schema Editor, etc.)
4. Search recent issues (last 2-4 weeks)

#### 5.2 Confirm Customer Issues with User

Present found Linear issues:

```
I found the following Linear issues that may be related to this release:
- [ISSUE-123]: Description (Status: Done)
- [ISSUE-456]: Description (Status: Done)

Which of these should be highlighted as customer-reported fixes in the release notes?
```

### Phase 6: Learn from Previous Releases

#### 6.1 Fetch Recent Release Notes

Visit and analyze 2-3 recent releases:
- Same major version (e.g., 3.12.1, 3.12.0 when writing 3.12.2)
- One minor release example (x.x.1 or x.x.2)

```
URL: https://github.com/bytebase/bytebase/releases
```

Use WebFetch tool to extract:
1. **Section structure**: What sections are used?
2. **Writing style**: Verb tense, length, tone
3. **Grouping patterns**: How are related items grouped?
4. **Database prefixes**: How are DB-specific features marked?
5. **Notable Changes examples**: What qualifies as notable?

### Phase 7: Prioritization

#### 7.1 Write ALL Release Notes First

**IMPORTANT**: Do NOT limit items during initial writing. Write release notes for ALL significant changes first.

For each section, compile:
- All Notable Changes (with owner)
- All Features (with owner)
- All Enhancements (with owner)
- All Bug Fixes (with owner)

#### 7.2 Apply Priority Matrix

| Priority | Criteria | Treatment |
|----------|----------|-----------|
| P0 | Customer-reported bugs, security issues, data corruption | **Must include** in Bug Fixes, list first |
| P1 | Breaking changes, new major features, Terraform-affecting | **Must include** in Notable Changes or Features |
| P2 | User-facing improvements, performance gains | Include if space permits |
| P3 | Internal refactors with indirect benefits | Group or omit |
| P4 | Code cleanup, internal changes | Omit |

#### 7.3 Present Top Items for User Selection

After writing all items, present to user:

```markdown
## Full Release Notes (for your review)

### Notable Changes (X total) — INCLUDE ALL
All notable changes should be included as they may affect existing customers:
1. [Change] — Owner: [Name] | Terraform: [Yes/No]
2. [Change] — Owner: [Name] | Terraform: [Yes/No]
... (no limit)

### Features (X total)
**Recommended (Top 8)**:
1. [Feature] — Owner: [Name]
...

**Additional items (for your consideration)**:
9. [Feature] — Owner: [Name]
...up to 20

### Enhancements (X total)
**Recommended (Top 8)**:
1. [Enhancement] — Owner: [Name]
...

**Additional items (for your consideration)**:
9. [Enhancement] — Owner: [Name]
...up to 20

### Bug Fixes (X total)
**Recommended (Top 8)**:
1. [Fix] — Owner: [Name]
...

**Additional items (for your consideration)**:
9. [Fix] — Owner: [Name]
...up to 20

Please review and let me know which items to include in the final release notes.
```

**IMPORTANT**: Notable Changes have NO limit — include ALL of them since they may affect existing customer configurations and workflows.

#### 7.4 Patch Version Validation

**If this is a PATCH version and Notable Changes or Features were found:**

```
⚠️ ATTENTION: This is a patch version upgrade (X.Y.Z → X.Y.Z+1), but I found:
- [N] Notable Changes
- [N] Features

Patch versions typically should NOT contain Notable Changes or Features.
Please confirm:
1. Should these be reclassified as Enhancements?
2. Should this actually be a minor version upgrade?
3. Are these exceptions that should remain as-is?
```

### Phase 8: Writing

#### 8.1 Use This Exact Template

**Section Order**: Notable Changes → Features → Enhancements → Bug Fixes

```markdown
# X.Y.Z - Month Day, Year

## Notable Changes

- [Behavior change with explanation of impact]
- [Breaking change with migration guidance if needed]
- [Change affecting Terraform] (**Terraform**: [update instructions])

## Features

- **[Database Name]** — [New capability description]
- [New feature with user benefit]

## Enhancements

- **[Database Name]** — [Specific capability added]
- [General improvement with user benefit]
- [Feature area] improvements including:
  - [Specific improvement 1]
  - [Specific improvement 2]
  - [Specific improvement 3]
- [Performance optimization with measurable impact]
- [Infrastructure upgrade with user-facing benefit]

## Bug Fixes

- Fix [customer-reported issue 1 - describe the problem]
- Fix [customer-reported issue 2 - describe the problem]
- Fix [critical user-facing issue]
- Fix [important data display issue]
- Fix [workflow blocking issue]

---

**IMPORTANT:** Before upgrading to this version, please backup the [metadata](https://www.bytebase.com/docs/administration/back-up-restore-metadata/). Bytebase doesn't support in-place downgrade. Also avoid running multiple Bytebase containers sharing the same data directory. Otherwise, it may corrupt the metadata.
```

#### 8.2 Writing Rules

**Grammar and Style:**
- **Tense**: Present tense verbs ("Add", "Fix", "Improve", "Support")
- **Voice**: Active voice, subject often implied
- **Length**: One line per item, keep it short and concise
- **Tone**: Professional, factual, user-focused

**Content Rules:**
- **Keep it concise**: Avoid overly detailed descriptions. Don't include implementation reasoning or technical details unless absolutely necessary for user understanding.
- **Lead with impact**: What changed for users, not how it was implemented
- **No reasoning**: Don't explain "why" a change was made (e.g., avoid "since labels are Issue properties"). Just state what changed.
- **Infrastructure/backend changes**: For changes to internal systems (parsers, advisors, etc.), describe the **user-facing impact** not the technical fix. Example: "Fix SQL review showing incorrect line numbers" instead of "Fix advisor line position calculation in multi-statement parsing"
- **Limit bug fixes**: For patch releases, select the 4-5 most important bug fixes rather than listing every fix
- **Group related changes**: 3+ related commits → single line with nested bullets
- **Use database prefixes**: Format as `**Database Name** —` for DB-specific features
- **Include Terraform impact**: When applicable, add (**Terraform**: [details])

**Examples:**

Good (concise, user-focused):
```markdown
- Fix rollout date filter not working
- Fix SQL review showing incorrect line numbers for multi-statement SQL
- Show issue labels in "Ready for Review" popover during Plan creation
- **SQL Server** — Add visualized EXPLAIN support
```

Bad (too detailed or too vague):
```markdown
- Fix SQL Editor tab caching preventing stale database query contexts from being loaded (too long)
- Show issue labels in "Ready for Review" popover during Plan creation, making the two-step Plan → Issue workflow clearer since labels are Issue properties (includes unnecessary reasoning)
- Fix advisor line position and refactor statement text architecture (technical implementation detail instead of user impact)
- Fixed bug in cache implementation (too vague)
- New MSSQL feature (too vague)
```

#### 8.3 Review Checklist

Before finalizing:
- [ ] Version confirmed with user (minor vs patch)
- [ ] Patch version has no Notable Changes/Features (or confirmed as exception)
- [ ] All customer-reported issues addressed and listed first in Bug Fixes
- [ ] Terraform impact documented for all applicable changes
- [ ] Each item uses present tense
- [ ] Database-specific items have proper prefix format
- [ ] No implementation details (unless necessary for understanding)
- [ ] Breaking changes clearly explained in Notable Changes
- [ ] Owner identified for each item (for confirmation)
- [ ] Related changes grouped to save space
- [ ] Standard warning footer included
- [ ] User benefit clear for each enhancement

### Phase 9: Linear Issue & Owner Confirmation

**IMPORTANT**: Before each Linear write operation, you MUST confirm with the user. Never create issues or comments without explicit user approval.

#### 9.1 Create Linear Issue for Release Notes

After finalizing the release notes draft, prepare to create a Linear issue to track confirmations.

**Issue Title Format**: `<version>-<date>_release_note`
- Example: `3.13.1-20251230_release_note`

**Issue Description**: Include the full release notes content and an owner confirmation table.

**⚠️ CONFIRM WITH USER BEFORE CREATING:**

Present the issue details and ask for confirmation:

```
I'm ready to create a Linear issue to track the release notes:

**Title:** 3.13.1-20251230_release_note
**Team:** Bytebase
**Assignee:** Peter Zhu
**Priority:** High

**Description:**
[Show the full release notes content that will be included]

Should I create this Linear issue? (yes/no)
```

Only proceed with `mcp__linear__create_issue` after user confirms.

#### 9.2 Subscribe Stakeholders

After creating the issue, prepare to subscribe Danny Xu and Tianzhou Chen.

**⚠️ CONFIRM WITH USER BEFORE COMMENTING:**

```
I'll now add a comment to subscribe stakeholders (Danny and Tianzhou) to the issue.

**Comment preview:**
"[danny](https://linear.app/bytebase/profiles/danny) [tianzhou](https://linear.app/bytebase/profiles/tianzhou) FYI - subscribing you to this release note issue for visibility."

Should I post this comment? (yes/no)
```

Only proceed with `mcp__linear__create_comment` after user confirms.

#### 9.3 Create Confirmation Comments with @mentions

**IMPORTANT**: Create separate comments for each owner, grouping their items together.

**Git-to-Linear User Mapping**:
| Git Author | Linear Name | Linear displayName |
|------------|-------------|-------------------|
| boojack | Steven Li | steven |
| ecmadao | Edward Lu | ed |
| h3n4l | Adrian Lam | h3n4l |
| Danny Xu | Danny Xu | danny |
| p0ny | Xzavier Zane | p0ny |
| rebelice | Jonathan Yablonski | junyi |
| Vincent Huang | Vincent Huang | vh |
| zchpeter | Peter Zhu | pz |

**Mention Format**: To properly @mention users in Linear comments, use a markdown link to their profile:

```markdown
[displayName](https://linear.app/bytebase/profiles/displayName)
```

**⚠️ CONFIRM WITH USER BEFORE EACH OWNER COMMENT:**

Present ALL owner comments at once for batch approval:

```
I'll now add confirmation comments for each owner. Here are the comments I'll post:

**Comment 1 - For Steven Li (@steven):**
[steven](https://linear.app/bytebase/profiles/steven) Please confirm the following items are accurate:

**Enhancements:**
- [ ] Show issue labels in "Ready for Review" popover during Plan creation

**Bug Fixes:**
- [ ] Fix rollout date filter not working

---

**Comment 2 - For Edward Lu (@ed):**
[ed](https://linear.app/bytebase/profiles/ed) Please confirm the following items are accurate:

**Bug Fixes:**
- [ ] Fix domain change not triggering value update

---

[Continue for each owner...]

Should I post these [N] owner confirmation comments? (yes/no/edit)
```

Only proceed with `mcp__linear__create_comment` for each owner after user confirms.

#### 9.4 Add Final Confirmation Comments

After adding owner-specific confirmation comments, prepare the final approval comments.

**⚠️ CONFIRM WITH USER BEFORE POSTING:**

```
Finally, I'll add comments requesting overall release note approval:

**Comment for Adela Chen (@adela):**
[adela](https://linear.app/bytebase/profiles/adela) Please review and confirm the overall release notes are ready for publication.

**Comment for Peter Zhu (@pz):**
[pz](https://linear.app/bytebase/profiles/pz) Please review and confirm the overall release notes are ready for publication.

Should I post these final approval comments? (yes/no)
```

Only proceed with `mcp__linear__create_comment` after user confirms.

### Phase 10: Write Draft to File

#### 10.1 Create Release Notes Draft File

**IMPORTANT**: Always write the release notes draft to a file for reference and iteration.

Create the draft file at:
```
docs/release-notes/draft-X.Y.Z.md
```

The file should contain:
1. The full release notes draft (formatted for GitHub release)
2. A metadata section at the bottom with:
   - Version type (minor/patch)
   - Previous version
   - Date generated
   - Owner confirmation status

**Example file structure:**
```markdown
# X.Y.Z - Month Day, Year

## Notable Changes
...

## Features
...

## Enhancements
...

## Bug Fixes
...

---

**IMPORTANT:** Before upgrading...

---
<!-- DRAFT METADATA (remove before publishing) -->
<!--
Version: X.Y.Z
Previous Version: X.Y.W
Version Type: Minor/Patch
Generated: YYYY-MM-DD
Status: Draft

## Owner Confirmation Status
| Section | Item | Owner | Confirmed |
|---------|------|-------|-----------|
| Notable Changes | ... | @owner | [ ] |
...
-->
```

#### 10.2 Update Draft on Each Iteration

When user provides feedback:
1. Update the draft file in place
2. Keep a revision history in git (user can see changes via git diff)
3. Update the confirmation status as owners confirm

### Phase 11: Iteration

If user requests changes:
1. Ask for specific feedback on what needs adjustment
2. Adjust prioritization or wording based on feedback
3. Ensure customer complaints remain prioritized
4. Re-verify Terraform impact if changes affect API/resources
5. Update the draft file in `docs/release-notes/draft-X.Y.Z.md`
6. Maintain format consistency

## Quick Command Reference

```bash
# Find versions
git tag --list "*3.12*" | sort -V
git branch -a | grep release/3.12

# Get commits
git log 3.12.1..origin/release/3.12.2 --oneline --decorate

# Analyze commits with author (run in parallel)
git show --stat --format='Author: %an <%ae>' <hash1>
git show --stat --format='Author: %an <%ae>' <hash2>

# Check Terraform impact
git show <hash> -- "proto/**/*.proto" | head -50

# Find owner by file changes
git log 3.12.1..origin/release/3.12.2 --format='%an' -- backend/api/ | sort | uniq -c | sort -rn

# Research format
# Use WebFetch: https://github.com/bytebase/bytebase/releases/tag/3.12.1
```

## Common Scenarios

### Scenario 1: Patch Version with Features Found

**Situation**: Writing 3.12.1 → 3.12.2 and found new features

**Action**:
1. Flag to user immediately
2. Ask: "This is a patch release but I found [N] features. Should these be reclassified as Enhancements, or should this be a minor version (3.13.0)?"
3. Proceed based on user decision

### Scenario 2: API Change Affecting Terraform

**Situation**: Proto file changes field name from `tier` to `environment_tier`

**Action**:
1. Categorize as Notable Changes
2. Add Terraform impact note
3. Example: "Rename environment field from `tier` to `environment_tier` (**Terraform**: update `bytebase_environment` resource configuration to use new field name `environment_tier`)"

### Scenario 3: Customer Complaints Mentioned

**Input**: "Customers complained about SQL editor tab caching and DDL/DML popup not showing"

**Action**:
1. Search Linear for related issues
2. Identify commits that fix these issues
3. Place them at the top of Bug Fixes section
4. Ensure descriptions clearly address the reported problem
5. Example: "Fix SQL Editor tab caching preventing stale database query contexts from being loaded"

### Scenario 4: Large Refactor Across Multiple Commits

**Input**: 5 commits all related to "SQL Editor tab management"

**Action**:
1. Determine user-facing impact
2. Identify primary owner (person with most commits/changes)
3. Group into single Enhancement with nested bullets
4. Example:
   ```markdown
   - SQL Editor tab management improvements including:
     - Refactored state management with simplified caching logic
     - Performance optimizations for tab loading and rendering
     - Enhanced tab UI components
   ```

## Tool Usage Best Practices

1. **TodoWrite**: Create task list at start, update after each batch
2. **Bash (parallel)**: Run multiple `git show --stat` commands simultaneously
3. **WebFetch**: Fetch previous release notes to learn format
4. **Linear MCP (read)**: Search for customer-reported issues (no confirmation needed)
5. **Linear MCP (write)**: **ALWAYS confirm with user** before creating issues or comments
6. **Read if needed**: If commit message unclear, read actual code changes

## Success Criteria

A good release note:
- Has confirmed version (minor vs patch) with appropriate sections
- Addresses all customer-reported issues prominently
- Documents Terraform impact for all applicable changes
- Follows the established format exactly (Notable → Features → Enhancements → Bug Fixes)
- **Includes ALL Notable Changes** (no limit) since they affect existing customers
- Uses consistent present tense
- **Concise and user-focused**: No implementation details, no reasoning, no overly long descriptions
- **Infrastructure changes describe user impact**: e.g., "Fix SQL review showing incorrect line numbers" not "Fix advisor line position calculation"
- **Limited bug fixes for patch releases**: Select 4-5 most important fixes
- **Consolidates related PRs**: Multiple PRs for the same Linear issue become one release note item
- Includes owner for each item (multiple owners if consolidated)
- Groups related changes effectively
- Maintains professional, concise tone
- **Draft saved to `docs/release-notes/draft-X.Y.Z.md`** for reference and iteration
- **Linear issue created** with title `<version>-<date>_release_note` (after user confirmation)
- **Confirmation comments added** with proper @mentions using profile URL format (after user confirmation)
- **All Linear write operations confirmed by user** before execution

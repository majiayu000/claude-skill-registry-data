---
name: git-commit-scope-constitution
description: 'Build and refine a constitution defining valid commit scopes for each commit type. Use when maintaining .github/git-scope-constitution.md, discovering new scopes from git history or repo structure, validating scope choices, or conducting weekly scope reviews. Scopes are repo-specific; types are universal.'
metadata: 
   version: 2.0.0
   author: arisng
---

# Commit Scope Constitution

## Overview

This skill enables building and maintaining a living constitution that defines the inventory and rules for commit scopes used in conventional commits. The constitution serves as the authoritative source for:

- Approved scope names organized by commit type
- Naming conventions and patterns for scopes
- Scope definitions and boundaries
- Guidance for choosing appropriate scopes

**Repository-Specific Design:** Each repository maintains its own scopes inventory and constitution, stored within the repository itself. This ensures scopes align with the specific project structure, domains, and modules of that repository.

## Core Principle: Type vs. Scope (Three-Tier Model)

Commit messages follow the pattern `type(scope): subject`, governed by a three-tier hierarchy:

| Tier | What it governs | Defined by | Stability |
|------|----------------|------------|-----------|
| **1. Universal** | Standard Conventional Commits types (`feat`, `fix`, `docs`, etc.) | Industry convention | Fixed across all repos |
| **2. Author Preferences** | Extended types (`agent`, `copilot`, `devtool`, `codex`) + default file-path mappings | Skill author (opinionated, portable) | Shared across author's repos; users may override |
| **3. Workspace-Specific** | Scopes, additional types, file-path overrides | `.github/git-scope-constitution.md` per repo | Unique per repository |

- **Commit Type (Tier 1 + 2)**: Represents the *intent* or *category* of the change. Universal types are immutable; extended types are the author's opinionated additions that take precedence when applicable.
- **Commit Scope (Tier 3)**: Represents the *domain*, *module*, or *location* of the change. Scopes are tightly coupled to the context of each repository.

**This skill's primary job is to define the Tier 3 Scopes for a specific repository and map them to the appropriate Types.**

## Repository Storage Convention

**Scopes Inventory:** `.github/git-scope-inventory.md`
- **Purpose**: Machine-readable inventory of all scopes extracted from git history
- **Content**: Simple structured list of scopes actually used in commits, organized by commit type
- **Maintenance**: Updated automatically by running `extract_scopes.py`
- **Usage**: Analysis tool for understanding current scope usage patterns
- **Format**: Structured markdown with summary statistics and scope lists

**Constitution Document:** `.github/git-scope-constitution.md`
- **Purpose**: Human-readable constitution defining approved scopes and usage rules
- **Content**: Authoritative definitions, naming conventions, selection guidelines, and amendment process
- **Maintenance**: Manually maintained with regular updates (weekly recommended)
- **Usage**: Reference guide for developers choosing commit scopes
- **Format**: Structured markdown with sections for different commit types and governance

**Key Distinction**: The inventory shows *what has been used* (historical fact), while the constitution defines *what should be used* (governance policy). The inventory feeds into constitution updates, but the constitution governs future commits.

**Template Reference:** `skills/git-commit-scope-constitution/references/scope-constitution.md`
- Template for creating new constitutions
- Not used at runtime (exists only in this skill)

## Constitution Format

The commit scope constitution governs the scopes used in conventional commit messages:

```txt
<commit_type>(<scope>): <executive summary>

<optional_multi-line_description>
```

**MANDATORY: Single Scope Only**  
Each commit MUST have exactly one scope. Never use multiple scopes (e.g., `<type>(<scope1>)(<scope2>)`). If a change affects multiple areas, choose the most significant one as the primary `<scope>` and explicitly mention any secondary area in the `<subject>` part (e.g., `<type>(primary-scope): [secondary-area] actual message`).

The constitution itself is stored in `.github/git-scope-constitution.md` and follows this structure:

```markdown
# Commit Scope Constitution

Last Updated: YYYY-MM-DD

## Purpose

This constitution defines the approved scopes for atomic commits, ensuring consistency and clarity in commit history.

## Scope Naming Conventions

[Rules for creating scope names]

## Approved Scopes by Commit Type

### `commit_type`

- `scope-name`: Brief description of what this scope covers
- `another-scope`: Brief description

[Additional sections as needed]

## Scope Selection Guidelines

[Guidance for choosing appropriate scopes]

## Amendment Process

[How to propose and approve new scopes]
```

## Workflow

### 1. Analyze Current Repository State

Start by understanding the repository from two perspectives:

#### 1a. Extract Historical Scopes from Git

Analyze git commit history to see what scopes have been used:

```bash
# Extract all historical scopes
python skills/git-commit-scope-constitution/scripts/extract_scopes.py --format markdown --output .github/git-scope-inventory.md

# Or just recent scopes (last 3 months)
python skills/git-commit-scope-constitution/scripts/extract_scopes.py --since "3 months ago" --format markdown
```

This generates an inventory of all scopes currently used in the repository's git history, organized by commit type.

**Note**: The scopes inventory shows *historical usage* (what has been done), while the constitution defines *approved usage* (what should be done). Use the inventory as input for constitution updates, but always reference the constitution for governance decisions.

#### 1b. Analyze Repository Structure

**CRITICAL:** Scopes should align with the actual project structure, not just historical commits. Analyze the repository to understand:

**Folder Structure Analysis:**
- List top-level directories and their purpose
- Identify module boundaries (e.g., `services/`, `components/`, `tools/`)
- Note domain-specific folders (e.g., `auth/`, `billing/`, `dashboard/`)
- Recognize documentation areas (e.g., `.docs/`, `docs/`, `README.md`)

**Project Architecture:**
- Identify bounded contexts or domains
- Note technology-specific directories (e.g., `scripts/`, `tests/`, `config/`)
- Recognize artifact types (e.g., `agents/`, `skills/`, `prompts/`)

**Key Questions:**
- What are the major functional areas of this project?
- How is the code organized (by feature, layer, domain)?
- What are the natural scope boundaries based on the structure?
- Are there emerging patterns in folder naming?

**Example Analysis:**
```
Repository: github-copilot-fc

Top-level structure:
- agents/          → Custom agent definitions
- instructions/    → Copilot instructions
- prompts/         → Prompt templates
- skills/          → Claude skills
- scripts/         → Automation scripts
- tools/           → Tools inventory and VS Code runtime toolsets
- .docs/           → Documentation

Derived scope patterns:
- Artifact-based: agent, instruction, prompt, skill, toolset
- Function-based: script (for automation)
- Domain-based: issue, changelog (from .docs/ subfolders)
```

### 2. Synthesize Scope Landscape

Combine insights from git history and repository structure:

**Merge Historical and Structural Scopes:**
- Historical scopes show what has been used
- Structural analysis shows what should be used
- Gaps indicate either unused structure or undocumented scopes

**Identify Patterns:**
- Do historical scopes align with folder structure?
- Are there folders without corresponding scopes?
- Are there scopes used for non-existent structures?

### 3. Review Existing Constitution

Check if a constitution already exists:
- Read `.github/git-scope-constitution.md` if present
- Compare with extracted historical scopes
- Compare with repository structure analysis
- Identify discrepancies (scopes used but not documented, structures without scopes)

### 4. Constitutional Analysis

Evaluate the current scope landscape:

**Quality Checks:**
- [ ] Are scope names consistent in format (kebab-case, singular vs plural)?
- [ ] Are scopes granular enough to be meaningful but not overly specific?
- [ ] Do scope definitions clearly distinguish between related scopes?
- [ ] Are there redundant or overlapping scopes that should be consolidated?
- [ ] Are scopes aligned with the codebase's module/domain structure?

**Pattern Recognition:**
- Identify naming patterns (e.g., module-based feature-based, domain-based, file-path-based)
- Detect inconsistencies (same concept with different names)
- Find under-scoped types (types with no or too few scopes)

### 5. Draft or Update Constitution

Based on analysis, create or update the constitution:

**For New Constitutions:**
1. Define scope naming conventions
2. Organize scopes by commit type (align with repository structure)
3. Provide clear definitions for each scope (reference folder/module names)
4. Establish guidelines for scope selection
5. Define amendment process
6. Document the repository structure that informed scope decisions

**For Constitution Updates:**
1. Document new scopes discovered in recent commits
2. Add scopes for new project structures (folders, modules, domains)
3. Consolidate redundant or similar scopes (with migration notes)
4. Refine definitions for ambiguous scopes
5. Update naming conventions if patterns have evolved
6. Add examples for unclear cases
7. Align with any structural refactoring in the repository

**Key Principles:**
- **Stability**: Minimize breaking changes to existing scopes
- **Clarity**: Each scope should have a clear, non-overlapping definition
- **Discoverability**: Organize scopes logically for easy lookup
- **Flexibility**: Allow for organic growth while maintaining consistency

### 6. Validation

Validate the updated constitution:

**Completeness Checks:**
- [ ] All commit types used in repository are documented
- [ ] All active scopes (from recent commits) are included
- [ ] Each scope has a clear definition
- [ ] Naming conventions are documented and examples provided

**Consistency Checks:**
- [ ] Scope names follow established conventions
- [ ] No duplicate or near-duplicate scopes
- [ ] Definitions are mutually exclusive
- [ ] Examples align with definitions

### 7. Document Changes

Record constitutional amendments:

**Amendment Log Format:**
```markdown
## Amendment History

### YYYY-MM-DD - Amendment #N

**Changes:**
- Added scope `new-scope` to `commit_type`
- Consolidated `old-scope-1` and `old-scope-2` into `unified-scope`
- Clarified definition of `ambiguous-scope`

**Rationale:**
[Why these changes were made]

**Migration Notes:**
[How to handle existing commits with old scopes]
```

### 8. Publish Constitution and Inventory

Save the finalized constitution and inventory:

1. Write constitution to `.github/git-scope-constitution.md`
2. Write scopes inventory to `.github/git-scope-inventory.md`
3. Update the "Last Updated" date in constitution
4. Commit both files with a descriptive commit message

**Recommended Commit Message:**
```txt
docs(constitution): update scope inventory with Q1 2026 scopes

- Added 5 new scopes for `agent` type commits
- Consolidated instruction scopes into 3 clear categories
- Clarified boundaries between codex and copilot scopes
```

## Usage Patterns

### Weekly Refinement

Run this workflow weekly to keep the constitution current:

1. Extract scopes from the past week
2. Compare with constitution
3. Check for new project structures (folders, modules)
4. Add new scopes or flag anomalies
5. Update if needed

### Pre-Commit Validation

Before committing, validate scope choice against constitution:

1. Identify commit type from file paths
2. Consult constitution for approved scopes under that type
3. Choose most appropriate scope
4. If no scope fits, propose amendment

### Scope Discovery

When uncertain about scope naming:

1. Check constitution for similar scopes
2. Review historical usage with `extract_scopes.py --since "1 month ago"`
3. Follow naming conventions from constitution
4. Document new scope if creating one

## Scripts

### `scripts/extract_scopes.py`

Analyzes git history to extract all scopes used in conventional commit messages.

**Usage:**
```bash
# Extract all scopes
python scripts/extract_scopes.py

# Filter by time period
python scripts/extract_scopes.py --since "1 week ago"

# Output as JSON
python scripts/extract_scopes.py --format json

# Save to file
python scripts/extract_scopes.py --output inventory.md
```

**Output Formats:**
- `markdown`: Structured inventory with summary statistics and organized scope lists
- `json`: Machine-readable structure for tooling

**Inventory Structure:**
```markdown
# Scopes Inventory

**Repository:** [name]
**Last Updated:** [date]
**Source:** Git commit history analysis

## Summary
- Total Commit Types: N
- Total Unique Scopes: N
- Analysis Period: [timeframe]

## Scopes by Commit Type
### `type`
- scope-1
- scope-2

## Notes
[Additional context]
```

## References

### Template Files (Skill Resources)

**`references/scope-constitution.md`**
- Template for creating new constitutions
- Not used at runtime (reference only)
- Copy to `.github/git-scope-constitution.md` in target repository

**`references/scope-inventory-template.md`**
- Example of structured inventory format
- Shows expected output structure
- Used as reference for manual inventory creation

### Repository Files (Version Controlled)

**`.github/git-scope-constitution.md`** (in target repository)
- **Role**: Authoritative constitution defining all approved scopes and governance rules
- **Content**: Scope definitions, naming conventions, selection guidelines, amendment process
- **Purpose**: Governs what scopes developers should use in future commits
- **Maintenance**: Manually updated through constitutional amendments
- **Usage**: Primary reference for developers and commit validation tooling
- **Update Frequency**: Weekly reviews, amendments as repository evolves

**`.github/git-scope-inventory.md`** (in target repository)
- **Role**: Historical inventory of scopes actually used in the repository
- **Content**: Machine-readable list of all scopes found in git commit history
- **Purpose**: Tracks what scopes have been used (descriptive, not prescriptive)
- **Maintenance**: Automatically generated by `extract_scopes.py` script
- **Usage**: Analysis input for constitution updates and scope evolution tracking
- **Update Frequency**: With each constitution review or on-demand analysis

## Best Practices

### Scope Granularity

**Category-Level Principle (Tier 2 Extended Types):**

For extended types (`agent`, `copilot`, `devtool`, `codex`), scopes must be **artifact categories**, not specific instances. When scanning `git log --oneline`, `type(category)` instantly conveys *what kind of thing* changed; the subject line says *which one*.

| Pattern | Example | Verdict |
|---------|---------|---------|
| Category scope | `agent(skill): add table extraction to pdf` | ✅ |
| Instance scope | `agent(pdf): add table extraction` | ❌ |
| Category scope | `copilot(instruction): tighten powershell linting rules` | ✅ |
| Instance scope | `copilot(powershell): tighten linting rules` | ❌ |
| Category scope | `devtool(script): fix publish path resolution` | ✅ |
| Instance scope | `devtool(publish): fix path resolution` | ❌ |

**General Granularity (All Types):**

**Too Broad:**
- `feat(code): add feature` → What part of the code?
- `fix(app): fix bug` → Which component?

**Too Narrow:**
- `feat(src/components/forms/UserForm.tsx): add validation` → File-specific
- `fix(line-42-in-utils): fix typo` → Too granular

**Just Right:**
- `feat(user-form): add email validation`
- `fix(auth): correct token expiration logic`

### Naming Conventions

**Recommended Patterns:**
- Kebab-case: `user-profile`, `api-client`
- Singular form: `skill`, `agent`, `instruction`
- Domain/module-based: `auth`, `billing`, `dashboard`
- Avoid verbs: Use `api-client` not `calling-api`

**Anti-Patterns:**
- Camel case: `userProfile`
- Snake case: `user_profile`
- Spaces: `user profile`
- Overly generic: `misc`, `other`, `stuff`

### Constitutional Amendments

**Good Reasons to Add Scope:**
- New module or domain added to codebase
- Existing scope is too broad and needs splitting
- Consistent pattern of commits without clear scope

**Bad Reasons to Add Scope:**
- One-off change that doesn't justify a scope
- Avoiding learning existing scopes
- Personal preference for different naming

### Scope Lifecycle

**Creation:** New scope added via constitutional amendment
**Active Use:** Scope appears regularly in commits
**Consolidation:** Similar scopes merged into one
**Deprecation:** Scope no longer relevant, marked deprecated
**Retirement:** Deprecated scope removed from constitution (but remains in history)

## Maintenance Schedule

**Maintenance Schedule:**
- Extract scopes from past week (`--since "1 week ago"`)
- Analyze any new folders/modules added to repository
- Compare with constitution
- Flag anomalies or new scopes
- Update constitution if patterns warrant

**Monthly:**
- Review scope usage patterns
- Analyze repository structure changes (refactoring, new modules)
- Identify consolidation opportunities
- Update naming conventions if needed

**Quarterly:**
- Comprehensive constitution review
- Major amendments and restructuring based on repository evolution
- Scope lifecycle management (deprecations/retirements)

## Integration with git-atomic-commit

This skill complements the `git-atomic-commit` skill:

1. **git-atomic-commit** enforces commit type mappings (file path → commit type)
2. **git-commit-scope-constitution** defines valid scopes within each commit type
3. Together they ensure: `correct_type(approved_scope): clear message`

**Workflow Integration:**
```
File Changed → git-atomic-commit → Commit Type Assigned
                                           ↓
                          git-commit-scope-constitution → Scope Selected
                                           ↓
                                    Final Commit Message
```

## Error Handling

**Scope Not Found in Constitution:**
1. Search historical usage with `extract_scopes.py`
2. Check if similar scope exists with different name
3. If genuinely new, draft amendment proposal
4. Get approval before using in commit

**Constitution Conflicts:**
1. Multiple scopes seem valid for the change
2. Review scope definitions for clarity
3. Choose the most specific applicable scope
4. If ambiguity persists, refine constitution

**Scope Naming Violations:**
1. Flag non-conforming scope name
2. Check constitution for correct format
3. Propose rename if scope is valuable
4. Update historical references if needed

## Examples

### Example 1: Creating Initial Constitution with Repository Analysis

```bash
# Step 1: Extract historical scopes
python skills/git-commit-scope-constitution/scripts/extract_scopes.py \
  --output .github/git-scope-inventory.md

# Step 2: Analyze repository structure
# List top-level directories
Repository: my-web-app/
  src/
    components/     → UI components
    services/       → Business logic services
    utils/          → Utility functions
  tests/            → Test files
  scripts/          → Build/automation scripts
  docs/             → Documentation
  .github/          → GitHub workflows

# Step 3: Map structure to scopes
From structure analysis:
- components/ → scope: "components" or specific component names
- services/auth/ → scope: "auth"
- services/billing/ → scope: "billing"
- scripts/ → scope: "script" or "build"
- docs/ → scope: "docs"

From git history (.github/git-scope-inventory.md):
- feat(components): Used 15 times
- feat(auth): Used 8 times
- feat(billing): Used 12 times
- fix(api): Used 6 times
- chore(deps): Used 20 times

# Step 4: Create constitution
# Combine structure-based and history-based scopes
# Document in .github/git-scope-constitution.md with clear definitions
```

### Example 2: Weekly Refinement

```bash
# Extract last week's scopes
python skills/git-commit-scope-constitution/scripts/extract_scopes.py \
  --since "1 week ago" --format markdown

# Check for new folders/modules
# Found: New folder src/services/notifications/

# Review against constitution
# Found new scope: feat(notifications) used 3 times
# Found folder: services/notifications/ (new module)

# Update constitution
# Add to appropriate section:
# - `notifications`: Notification service and delivery system
```

### Example 3: Scope Selection for Existing Codebase

```
Scenario: Modifying skills/git-atomic-commit/SKILL.md

Step 1: Check commit type mapping
  → File pattern: skills/* → Type: agent

Step 2: Consult constitution under Type: agent
  → Available scopes: skill, instruction

Step 3: Select appropriate scope
  → Change affects a skill → Use scope: `skill`
  → Specific skill name goes in the subject

Result: agent(skill): improve pre-commit validation checklist for git-atomic-commit
```

### Example 4: Scope Selection with Repository Structure Analysis

```
Scenario: Adding new authentication feature

Step 1: Analyze repository structure
  → services/auth/ exists (authentication module)
  → New files: services/auth/oauth.ts, services/auth/jwt.ts

Step 2: Check commit type
  → File pattern: services/* → feat (no project-specific type)

Step 3: Check constitution for feat scopes
  → .github/git-scope-constitution.md shows:
    - auth: Authentication and authorization
    - billing: Payment processing
    - dashboard: Dashboard features

Step 4: Select scope based on structure
  → Files in services/auth/ → Use scope: auth
  → Aligns with both structure and constitution

Result: feat(auth): implement OAuth 2.0 authentication flow
```

### Example 5: Constitutional Amendment

```markdown
## Amendment History

### 2026-02-04 - Amendment #12

**Changes:**
- Deprecated `ai` extended type in favor of `agent`
- Consolidated instance-level scopes (e.g., `pdf`, `diataxis`) into
  category-level scope `skill` under `agent` type
- Adopted "category-level scope" principle: scopes represent artifact
  categories, not specific instances
  
**Rationale:**
`agent(skill)` immediately tells the reader an agent skill was changed.
The subject line provides the specific skill name, enabling efficient
git log scanning without opening the diff.

**Migration Notes:**
Existing commits with old `ai(*)` scopes remain in history.
Use `agent(skill)` for all future skill-related commits.
```

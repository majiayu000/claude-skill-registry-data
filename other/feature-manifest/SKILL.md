---
license: Apache-2.0
name: feature-manifest
description: Manage feature manifests for code traceability. Use when creating new features, updating existing features, checking feature health, or exploring the feature-to-code relationship. Activates for manifest validation, feature creation, changelog updates, and traceability queries.
allowed-tools: Read,Write,Edit,Bash(npm:*,npx:*)
category: Productivity & Meta
tags:
  - feature-manifest
  - planning
  - requirements
  - specification
  - tracking
---

# Feature Manifest Management

This skill manages the feature manifest system that tracks the relationship between features and their implementations.

## DECISION POINTS

**When working with code changes, use this decision tree:**

```
Is this code change happening?
├── Creating new feature directory/component
│   ├── New feature has >5 files OR touches multiple domains
│   │   └── → CREATE new manifest (npm run feature:create)
│   └── Small utility/helper (<5 files, single purpose)
│       └── → ADD to existing related manifest
├── Modifying existing tracked files
│   ├── Files belong to known feature (check with: npm run feature:info -- --files <path>)
│   │   ├── Adding/removing files to feature
│   │   │   └── → UPDATE manifest files list + last_modified date
│   │   └── Just changing file contents
│   │       └── → UPDATE last_modified date only
│   └── Files are orphaned (not in any manifest)
│       └── → Determine owner with npm run feature:health, then UPDATE appropriate manifest
└── Removing/deprecating code
    ├── Entire feature being removed
    │   └── → SET status to 'deprecated', add deprecation changelog entry
    └── Some files being removed from feature
        └── → UPDATE manifest files list, add changelog entry
```

**For manifest validation failures:**
- Missing files → Add files to manifest or remove from filesystem
- Extra files → Remove from manifest files list
- Stale manifest (>90 days) → Update last_modified and add changelog entry
- No tests listed → Add test files or mark as technical debt

## FAILURE MODES

**1. Orphan File Syndrome**
- *Detection:* `npm run feature:health` shows files in "Orphaned Files" section
- *Cause:* Files created without updating any manifest
- *Fix:* Run `npm run feature:info -- --files <path>` to find logical owner, then add files to appropriate manifest

**2. Ghost Manifest References**
- *Detection:* Validation errors about missing files that were deleted
- *Cause:* Files removed from codebase but not from manifest
- *Fix:* Edit manifest to remove deleted files from `implementation.files`, update `last_modified`, add changelog entry

**3. Stale Dependency Web**
- *Detection:* Features referencing deprecated or renamed dependencies in `dependencies.internal`
- *Cause:* Feature refactoring without updating dependent manifests
- *Fix:* Search codebase for references to old feature ID, update all dependent manifests

**4. Test Coverage Blind Spot**
- *Detection:* `npm run feature:health` shows features in "Without Tests" section
- *Cause:* Tests exist but not listed in manifest, or no tests written
- *Fix:* If tests exist, add to appropriate test section; if missing, create tests or document as technical debt

**5. Manifest Explosion**
- *Detection:* Too many tiny manifests (>20 manifests for <100 files)
- *Cause:* Creating manifests for every small utility
- *Fix:* Consolidate related small features into logical groupings, deprecate overly granular manifests

## WORKED EXAMPLES

**Example: Adding authentication middleware to existing API feature**

1. **Identify impact:** New middleware affects multiple API routes
   ```bash
   npm run feature:info -- --files src/app/api
   # Shows: api-core.yaml owns most API files
   ```

2. **Check current manifest:**
   ```bash
   npm run feature:info -- api-core
   # Review current files list and dependencies
   ```

3. **Decision:** This is modifying existing feature (middleware is part of API infrastructure)

4. **Update manifest:** Add new middleware files to api-core.yaml:
   ```yaml
   implementation:
     files:
       - src/app/api/middleware/auth.ts  # NEW
       - src/lib/auth-utils.ts          # NEW
       # ... existing files
   ```

5. **Update metadata:**
   ```yaml
   dependencies:
     internal:
       - features/user-management.yaml  # NEW dependency
   history:
     last_modified: "2024-12-23"       # TODAY
   changelog:
     - version: "1.2.0"                # NEW entry
       date: "2024-12-23"
       changes:
         - "Added authentication middleware for API routes"
   ```

6. **Validate:** `npm run feature:validate` confirms no errors

**What novice misses:** Updating dependencies.internal when middleware uses user auth
**What expert catches:** All affected API routes need the auth dependency listed

## QUALITY GATES

Task is complete when ALL conditions are met:

- [ ] `npm run feature:validate` passes with no errors
- [ ] `npm run feature:health` shows no new orphaned files
- [ ] All implementation files listed in manifest exist in codebase
- [ ] All files in manifest have been modified more recently than `last_modified` date OR manifest updated
- [ ] If adding dependencies, all internal deps reference existing manifests
- [ ] If modifying feature, changelog has new entry with today's date
- [ ] If creating feature, manifest has at least entry_point and one implementation file
- [ ] Status field matches reality (complete features have tests, deprecated features noted)
- [ ] Any new environment variables are documented in dependencies.env_vars
- [ ] Database tables/API routes are documented if feature touches them

## NOT-FOR BOUNDARIES

**Do NOT use this skill for:**

- **Archived/legacy code** → Use `git-archaeology` skill instead for historical analysis
- **Third-party vendor files** (node_modules, .next, etc.) → These are build artifacts, not features
- **Configuration files** (package.json, tsconfig.json, etc.) → Use `project-config` skill instead
- **Documentation-only changes** (README, docs/) → Use `documentation` skill instead
- **Build/deployment scripts** → Use `devops-automation` skill instead
- **Test files that don't belong to features** (setup files, mocks) → Use `test-infrastructure` skill instead

**For cross-cutting concerns spanning multiple features:**
- Use `architecture-analysis` skill to understand system boundaries first
- Then update multiple manifests consistently using this skill
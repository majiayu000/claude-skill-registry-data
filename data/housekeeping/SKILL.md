---
name: housekeeping
description: Automatically maintain repository cleanliness and organization by scanning for misplaced files, organizing loose scripts, and ensuring professional folder structure
---

# Daily Repository Housekeeping Skill

## Purpose
Automatically maintain repository cleanliness and organization by scanning for misplaced files, organizing loose scripts, cleaning up temporary files, and ensuring professional folder structure throughout the codebase.

## Activation
Invoke with: `housekeeping` (no parameters required)

Example:
```
"Hey Claude, read the housekeeping guide and analyze our repo for any cleanup needed."
```

## Reference Documentation
This skill implements the workflow defined in:
`/resources/docs/HOUSEKEEPING.md`

Read this file first to understand the comprehensive organization protocol.

## Workflow Overview

### Phase 1: Repository Scan & Analysis
Analyze the current state of the repository across all critical areas.

#### 1.1 Root Directory Scan

**First, load the ALLOWED ROOT FILES WHITELIST (see below)**

- List all files at repository root (not folders)
- Compare against whitelist to categorize:
  - **KEEP (Whitelisted)** - Framework/system required files that MUST stay at root
  - **ORGANIZE** - Loose scripts (.py, .sh, .js, .ts files that don't belong at root)
  - **ORGANIZE** - Documentation files (.md files other than README.md)
  - **DELETE** - Backup files (.bak, .backup, *~, *.tmp)
  - **DELETE** - System files (.DS_Store, Thumbs.db)
  - **ORGANIZE or DELETE** - Other misplaced files (determine based on content)

**Key Rule:** If a file is NOT on the whitelist, it needs to be organized or deleted.

#### 1.2 Context Folder Analysis
- Check context root for files other than README.md
- Scan for documentation files that need proper categorization
- Identify folders with inconsistent naming conventions
- Look for duplicate or outdated files

#### 1.3 Resources Folder Analysis
- Scan for new utilities or scripts without proper categorization
- Check if Python/Shell scripts are in correct subfolders
- Verify documentation is in appropriate thematic folders
- Identify loose files that need homes

#### 1.4 Git Diff Analysis (Optional Context)
- Check what files were recently added (signals for what might be messy)
- Identify new scripts or docs that need organization

### Phase 2: Issue Categorization

Categorize all findings into severity levels:

#### Auto-Fix (No Approval Needed)
Small, obvious fixes that can be done immediately:
- Delete system files (.DS_Store, Thumbs.db)
- Delete backup files (.bak, .backup, *~)
- Delete temporary files (*.tmp, *.log that aren't in logs/)
- Move 1-2 clearly misplaced files to obvious locations

#### Requires Approval
Larger changes that need user confirmation:
- Moving multiple files (3+)
- Creating new folder structures
- Renaming existing folders
- Deleting files that might be important (scripts, docs, configs)
- Major reorganization

### Phase 3: Auto-Fix Execution

For items categorized as "Auto-Fix":

1. **Delete unnecessary files:**
   ```bash
   # System files
   find . -name ".DS_Store" -delete
   find . -name "Thumbs.db" -delete

   # Backup files
   find . -name "*.bak" -delete
   find . -name "*.backup" -delete
   find . -name "*~" -delete
   ```

2. **Move 1-2 clearly misplaced files:**
   - Single Python script at root → `resources/utilities/scripts/python/[category]/`
   - Single shell script at root → `resources/utilities/scripts/shell/[category]/`
   - Documentation file in context root → appropriate context subfolder

3. **Silent execution** - just do it, no need to announce

### Phase 4: Plan Presentation (If Needed)

If there are items requiring approval:

1. **Present current state:**
   - Show ASCII tree of problematic areas
   - List all files that need organization
   - Categorize by type/purpose

2. **Propose solution:**
   - Show ASCII tree of proposed structure
   - Explain what will be moved where
   - Explain what will be deleted

3. **Wait for user approval** before proceeding

4. **Use TodoWrite tool** to track all planned changes

### Phase 5: Implementation (After Approval)

Execute approved changes in this order:

1. **Create new folder structure** (if needed)
   - Follow naming conventions: lowercase-with-hyphens
   - Create deep subfolder hierarchies with clear categorization

2. **Delete approved files** (backups, duplicates, temp files)

3. **Move files in logical groups:**
   - Python scripts → `resources/utilities/scripts/python/[category]/`
   - Shell scripts → `resources/utilities/scripts/shell/[category]/`
   - Documentation → appropriate context or resources subfolder
   - Examples → `resources/examples/`

4. **Rename folders** (if needed) following conventions

5. **Verify nothing lost** - check that all important files were moved, not deleted

### Phase 6: Git Commit

1. **Stage all changes:**
   ```bash
   git add .
   ```

2. **Review changes:**
   ```bash
   git status
   ```

3. **Commit with descriptive message:**
   ```bash
   git commit -m "$(cat <<'EOF'
   chore: Daily housekeeping - organize repository structure

   • Cleaned up loose files from root directory
   • Organized scripts into proper utility folders
   • Deleted temporary and backup files
   • Maintained professional folder structure

   🤖 Generated with [Claude Code](https://claude.com/claude-code)

   Co-Authored-By: Claude <noreply@anthropic.com>
   EOF
   )"
   ```

4. **Push to remote** (only if user explicitly requests)

### Phase 7: Slack Notification

Send brief update to Academy channel:

1. **Get Academy channel ID:**
   ```
   Use mcp__slack__slack_list_channels to find Academy channel
   ```

2. **Send notification:**
   ```
   Use mcp__slack__slack_send_message with:
   - Channel: Academy channel ID
   - Message: "🧹 Daily housekeeping completed for transportation-insight repository! Organized loose files, cleaned up context folder, and maintained proper folder structure for optimal development workflow."
   ```

3. **Keep it brief** - 2 sentences max, professional tone

## Allowed Root Files Whitelist

**CRITICAL:** Only these files are allowed at the repository root. Everything else must be organized or deleted.

### Framework Configuration Files
- `package.json` - NPM package configuration
- `package-lock.json` - NPM lock file
- `tsconfig.json` - TypeScript configuration
- `tsconfig.tsbuildinfo` - TypeScript build cache
- `next.config.js` - Next.js configuration
- `next.config.mjs` - Next.js configuration (ESM)
- `next-env.d.ts` - Next.js type definitions
- `middleware.ts` - Next.js middleware
- `middleware.js` - Next.js middleware (JS)

### Amplify Files
- `amplify.yml` - Amplify build configuration
- `amplify_outputs.json` - Amplify runtime configuration

### Git & Version Control
- `.gitignore` - Git ignore rules
- `.gitattributes` - Git attributes

### Environment & Configuration
- `.env` - Environment variables (if exists)
- `.env.local` - Local environment variables
- `.env.production` - Production environment variables
- `.env.development` - Development environment variables

### Documentation
- `README.md` - Main project documentation (ONLY .md file allowed at root)
- `CLAUDE.md` - Symlink to Claude config (if exists)

### IDE Configuration
- `.eslintrc.js` - ESLint configuration
- `.eslintrc.json` - ESLint configuration
- `.prettierrc` - Prettier configuration
- `.prettierignore` - Prettier ignore rules
- `.editorconfig` - Editor configuration

### Build & CI/CD
- `Dockerfile` - Docker configuration (if exists)
- `.dockerignore` - Docker ignore rules (if exists)

### Other Framework Files
- `postcss.config.js` - PostCSS configuration (if exists)
- `tailwind.config.js` - Tailwind configuration (if exists)
- `jest.config.js` - Jest configuration (if exists)
- `vitest.config.ts` - Vitest configuration (if exists)

**Everything else = ORGANIZE or DELETE**

### What Gets Organized (Examples)
- `sync_databricks.py` → `resources/utilities/scripts/python/databricks/`
- `setup_auth.sh` → `resources/utilities/scripts/shell/auth/`
- `TESTING_NOTES.md` → `context/qa-test-scenarios/`
- `architecture.md` → `context/technical-docs/`
- `old_config.json` → DELETE or move to `resources/`

### What Gets Deleted (Always)
- `.DS_Store` - macOS system files
- `Thumbs.db` - Windows system files
- `*.bak` - Backup files
- `*.backup` - Backup files
- `*~` - Temp files
- `*.tmp` - Temp files
- `*.log` - Log files (unless in `/logs` folder)

## Folder Structure Standards

### Root Directory (Keep Only These)
```
transportation-insight/
├── .amplify/                  # Amplify framework
├── .claude/                   # Claude Code config
├── .git/                      # Git version control
├── .github/                   # GitHub config
├── .next/                     # Next.js build
├── amplify/                   # Amplify backend
├── context/                   # Project context (user-specified keep)
├── logs/                      # Application logs (user-specified keep)
├── node_modules/              # NPM dependencies
├── public/                    # Next.js public assets
├── resources/                 # All supporting materials
├── src/                       # Application source code
├── .env.local                 # Environment config
├── .gitignore                 # Git ignore rules
├── amplify_outputs.json       # Amplify outputs
├── amplify.yml                # Amplify build config
├── middleware.ts              # Next.js middleware
├── next-env.d.ts              # Next.js types
├── next.config.js             # Next.js config
├── package.json               # NPM package config
├── package-lock.json          # NPM lock file
├── README.md                  # Main documentation
├── tsconfig.json              # TypeScript config
└── tsconfig.tsbuildinfo       # TypeScript build info
```

### Context Folder Structure
```
context/
├── README.md                          # ONLY file at root level
├── legacy-codebase/                   # Previous platform code
├── qa-test-scenarios/                 # Testing scenarios
├── setup-guides/                      # Auth and setup docs
├── team-communications/               # Slack conversations
├── technical-docs/                    # Architecture docs
└── ui-specifications/                 # Design specs
```

### Resources Utilities Structure
```
resources/utilities/
├── scripts/
│   ├── python/
│   │   ├── slack/              # Slack integration scripts
│   │   ├── databricks/         # Database scripts
│   │   └── [category]/         # Other categorized scripts
│   └── shell/
│       ├── auth/               # Authentication setup
│       ├── sync/               # Synchronization scripts
│       └── deployment/         # Deployment scripts
└── resources/                  # Text files, links, references
```

## Naming Conventions

- **Use lowercase with hyphens**: `team-communications`, `qa-test-scenarios`
- **Be descriptive**: `ui-specifications` not `design`
- **Group by purpose**: `setup-guides` for all auth/config docs
- **Avoid abbreviations**: `legacy-codebase` not `legacy`

## Critical Rules

1. **Read HOUSEKEEPING.md first** - This skill implements that guide
2. **Enforce the whitelist** - Only whitelisted files stay at root, everything else gets organized or deleted
3. **Auto-fix small issues** - Don't ask for permission on obvious cleanups
4. **Present plan for major changes** - Show ASCII trees and get approval
5. **Follow naming conventions** - Professional, descriptive folder names
6. **Deep organization** - Use subfolder hierarchies, not flat structures
7. **Use TodoWrite for tracking** - Plan and track all major changes
8. **Silent on auto-fixes** - Just do the work, don't announce trivial cleanups
9. **Always notify Academy** - Send Slack update when done
10. **Never move framework files** - Keep whitelisted root files in place (see whitelist above)
11. **Respect user-specified folders** - context and logs stay at root as folders
12. **When in doubt, ask** - If a file's purpose is unclear, ask user before organizing/deleting

## Excluded Folders (Don't Organize These)

From tsconfig.json, these folders are excluded and should be ignored:
- `node_modules` - Dependencies, don't touch
- `src_original` - Archived code, leave alone
- `src/warehouse` - Excluded from build, leave alone
- `OldSource` - Legacy code, leave alone
- `amplify/**/*` - Don't reorganize Amplify structure
- `scripts/**/*` - If this exists, leave it alone

## Success Criteria

✅ Root directory contains only essential framework files + context + logs + resources
✅ Context folder has only README.md at root, all docs properly categorized
✅ Resources folder has deep organization with clear categorization
✅ No loose files - everything has a logical, discoverable location
✅ Consistent naming throughout (lowercase-with-hyphens)
✅ All changes committed with descriptive message
✅ Academy channel notified of completion
✅ Developer can find any file within 30 seconds

## Example Execution

**Morning invocation:**
```
User: "Hey Claude, read the housekeeping guide and analyze our repo for any cleanup needed."
```

**Claude's workflow:**
1. Reads `/resources/docs/HOUSEKEEPING.md`
2. Loads **Allowed Root Files Whitelist** from skill
3. Scans root directory, context folder, resources folder
4. Compares root files against whitelist:
   - **Whitelisted (KEEP):** `package.json`, `tsconfig.json`, `README.md`, `middleware.ts`, etc.
   - **Not whitelisted (ORGANIZE):** `sync_databricks.py`, `old_script.sh`
   - **Not whitelisted (ORGANIZE):** `AUTH_NOTES.md`, `TESTING.md` (docs not on whitelist)
   - **Always delete:** `.DS_Store` files
5. Identifies:
   - 3 .DS_Store files (auto-delete)
   - 1 Python script at root: `sync_databricks.py` (NOT on whitelist → needs categorization)
   - 2 docs in context root: `AUTH_NOTES.md`, `TESTING.md` (need proper folders)
6. **Auto-fixes:**
   - Deletes all .DS_Store files silently
7. **Presents plan:**
   ```
   Found 3 files at root that are NOT on the whitelist:

   📂 Root Directory Violations:
   ❌ sync_databricks.py (Python script - should be in resources/utilities/)
   ❌ AUTH_NOTES.md (Documentation - should be in context/setup-guides/)
   ❌ TESTING.md (Documentation - should be in context/qa-test-scenarios/)

   Proposed actions:
   • Move sync_databricks.py → resources/utilities/scripts/python/databricks/
   • Move AUTH_NOTES.md → context/setup-guides/
   • Move TESTING.md → context/qa-test-scenarios/

   [Shows ASCII tree of proposed changes]
   ```
8. **User approves**
9. **Executes:**
   - Moves `sync_databricks.py` → `resources/utilities/scripts/python/databricks/`
   - Moves `AUTH_NOTES.md` → `context/setup-guides/`
   - Moves `TESTING.md` → `context/qa-test-scenarios/`
10. **Commits changes** with descriptive message
11. **Sends Slack notification** to Academy channel
12. **Reports:** "Housekeeping complete! Repository is clean and organized. All root files now comply with whitelist."

---
name: git-commit-assistant
description: Assists with careful Git commits in any repository. Activates when committing changes, checking .gitignore, or generating commit messages. Ensures proper file exclusion (credentials, MCP configs, personal settings), identifies untracked files, and generates Conventional Commits messages with Japanese explanations.
allowed-tools: [Bash, Read, Write, Edit, AskUserQuestion, Grep, Glob]
---

# Git Commit Assistant Skill

## Purpose

Provide comprehensive Git commit assistance with:

- Automatic .gitignore validation and updates
- Intelligent file classification
- High-quality Conventional Commits message generation
- Protection against committing sensitive files

## Activation Triggers

Automatically activate when:

- User says "commit", "git commit", "コミット", "コミットしたい"
- User mentions ".gitignore"
- User asks about what to commit/exclude
- User requests to push changes to remote

## Workflow

### Phase 1: Repository Analysis

1. **Check Git status**
   - Run `git status --porcelain` to get machine-readable output
   - Identify modified, deleted, untracked files
   - Check current branch with `git branch --show-current`
   - Verify repository is not in detached HEAD state

2. **Analyze .gitignore**
   - Read existing .gitignore (if present)
   - Check against known critical patterns from `rules/gitignore-patterns.md`
   - Identify missing critical patterns (credentials, MCP configs, personal settings)

3. **Classify files**
   - **AUTO_EXCLUDE**: Sensitive/environment-specific files (never commit)
   - **AUTO_COMMIT**: Obviously safe files (source code, docs, configs)
   - **CONFIRM**: Ambiguous files requiring user input

### Phase 2: .gitignore Management

1. **Check for sensitive patterns**

   Critical patterns that must be present:
   - Credentials: `*.key`, `*.pem`, `*credentials*`, `*secret*`, `.env`
   - MCP configs: `.claude.json`, `.mcp.json*`
   - Personal settings: `settings.json`, `settings.local.json`
   - Build artifacts: `node_modules/`, `dist/`, `*.log`
   - OS files: `.DS_Store`, `Thumbs.db`

2. **Propose .gitignore updates**
   - Show missing patterns
   - Explain why each pattern is needed (security, environment dependency)
   - Ask user to approve updates using AskUserQuestion

3. **Update .gitignore**
   - Apply approved patterns
   - Stage .gitignore if updated

### Phase 3: File Selection

1. **Auto-classify files using rules**

   **AUTO_EXCLUDE (never commit)**:
   - Pattern: `*credentials*`, `*.key`, `*.pem`, `*secret*`, `*password*`
   - Pattern: `.claude.json`, `.mcp.json*`
   - Pattern: `settings.json`, `settings.local.json`
   - Pattern: `.env`, `.env.local`, `.env.*.local`
   - Pattern: `node_modules/`, `vendor/`, `dist/`, `build/`
   - Pattern: `*.log`, `*.cache`
   - Pattern: `.DS_Store`, `Thumbs.db`, `desktop.ini`

   **AUTO_COMMIT (generally safe)**:
   - Pattern: `*.md` (documentation)
   - Pattern: `.gitignore`, `.editorconfig`
   - Pattern: `src/**`, `internal/**`, `lib/**` (source code)
   - Pattern: `*_test.go`, `*.test.ts`, `*.test.tsx` (tests)
   - Pattern: `package.json`, `go.mod`, `Cargo.toml` (manifests)
   - Pattern: `.github/workflows/*` (CI configs)
   - Pattern: `~/.claude/skills/**` (Skills)
   - Pattern: `~/.claude/knowledge/**` (Knowledge base)

   **CONFIRM (user decision)**:
   - Files > 1MB
   - New directories
   - Executable files
   - Config files (not in AUTO lists)

2. **User confirmation for ambiguous files**
   - Present clear options using AskUserQuestion
   - Show file contents preview if helpful
   - Allow multi-select when appropriate

3. **Final file list**
   - Compile files to commit
   - Show summary to user before proceeding

### Phase 4: Commit Message Generation

1. **Analyze changes**
   - Review `git diff --cached` for staged changes
   - Review `git status` for file operations (add, delete, rename)
   - Identify change patterns and scope

2. **Determine commit type**

   Follow Conventional Commits specification:
   - `feat`: New features or capabilities
   - `fix`: Bug fixes
   - `docs`: Documentation only changes
   - `style`: Formatting, whitespace, no code change
   - `refactor`: Code restructuring without behavior change
   - `perf`: Performance improvements
   - `test`: Adding or updating tests
   - `build`: Build system or external dependency changes
   - `ci`: CI configuration changes
   - `chore`: Maintenance tasks, dependency updates

3. **Generate message**

   Template structure:
   ```
   <type>(<scope>): <subject>

   - <bullet point 1>
   - <bullet point 2>
   - <bullet point 3>

   🤖 Generated with [Claude Code](https://claude.com/claude-code)

   Co-Authored-By: Claude <noreply@anthropic.com>
   ```

   Guidelines:
   - Subject: Concise, imperative mood, max 50 chars (English preferred)
   - Bullets: Japanese OK, explain what/why/impact
   - 3-5 bullets typically sufficient
   - No file lists (git handles that)
   - No emojis except attribution

4. **Review with user**
   - Show generated message
   - Allow edits if needed

### Phase 5: Commit & Push

1. **Stage files**
   - Use `git add` for new/modified files
   - Use `git rm` for deleted files
   - Handle renames properly (git detects automatically)

2. **Create commit**
   - Apply generated message using heredoc for proper formatting
   - Example: `git commit -m "$(cat <<'EOF'\n...\nEOF\n)"`
   - Verify commit success

3. **Optionally push**
   - Check if remote exists: `git remote -v`
   - Check if branch tracks remote: `git branch -vv`
   - Ask user if should push
   - Execute `git push origin <branch>` if approved

## File Classification Details

### AUTO_EXCLUDE Priority Checks

1. **Credentials/Secrets** (Highest priority)
   - Any file containing "credential", "secret", "password", "key"
   - `.env` files
   - `*.pem`, `*.key` files
   - Action: Exclude immediately, warn user, ensure in .gitignore

2. **MCP Configuration** (High priority)
   - `.claude.json`, `.mcp.json`, `.mcp.json.backup`
   - Reason: Contains local environment paths
   - Action: Exclude, ensure in .gitignore

3. **Personal Settings** (High priority)
   - `settings.json`, `settings.local.json`
   - IDE settings: `.vscode/settings.json`, `.idea/workspace.xml`
   - Action: Exclude, ensure in .gitignore

4. **Build Artifacts** (Medium priority)
   - `node_modules/`, `vendor/`, `dist/`, `build/`
   - `*.log`, `*.cache`, `coverage/`
   - Action: Exclude, ensure in .gitignore

### AUTO_COMMIT Safe Patterns

1. **Documentation**
   - `*.md`, `docs/**`
   - Reason: Shareable knowledge
   - Action: Commit

2. **Source Code**
   - `src/**`, `internal/**`, `lib/**`
   - `*_test.go`, `*.test.ts`, `*.test.tsx`
   - Reason: Core project files
   - Action: Commit

3. **Configuration (Shareable)**
   - `.gitignore`, `.editorconfig`, `.prettierrc`
   - `package.json`, `tsconfig.json`, `go.mod`
   - `.github/workflows/**`
   - Reason: Team-shared configuration
   - Action: Commit

4. **Skills & Knowledge**
   - `~/.claude/skills/**`
   - `~/.claude/knowledge/**`
   - Reason: Shareable expertise
   - Action: Commit

### CONFIRM Cases

1. **Large files** (>1MB)
   - Show file size
   - Ask user if intentional
   - Suggest Git LFS if appropriate

2. **New directories**
   - Show directory contents (first level)
   - Ask user about purpose
   - Help classify based on purpose

3. **Executable files**
   - `*.exe`, `*.bin`, `*.app`
   - Ask if it's a build artifact or checked-in tool

## Commit Message Quality Checks

Before finalizing:

1. **Format validation**
   - Verify Conventional Commits format: `type(scope): subject`
   - Check subject length (≤50 chars recommended)
   - Ensure imperative mood

2. **Content validation**
   - Verify bullets explain what/why/impact
   - Check for meaningful description (not just "update files")
   - Ensure proper attribution

3. **Sensitive content scan**
   - Scan diff for patterns like:
     - API keys: `[A-Za-z0-9_-]{20,}`
     - Passwords: `password.*=.*`
     - URLs with credentials: `://.*:.*@`
   - Warn user if suspicious patterns found

## Error Handling

### Merge conflicts
- Detect: `git status | grep "both modified"`
- Action: Guide user to resolve first, offer to show conflict files

### Detached HEAD
- Detect: `git branch --show-current` returns empty
- Action: Suggest creating branch with `git switch -c <branch-name>`

### Nothing to commit
- Detect: `git status --porcelain` returns empty after staging
- Action: Inform clearly, suggest `git status` to check working directory

### Uncommitted changes during checkout
- Detect: Error when switching branches
- Action: Offer to stash changes or commit them first

## Integration with Global CLAUDE.md

Global CLAUDE.md should only contain:

```markdown
## Git操作

コミットは `git-commit-assistant` Skill が支援する。
基本原則: Conventional Commits形式、絵文字不使用、必要十分な解説。
詳細は `~/.claude/skills/git-commit-assistant/SKILL.md` を参照。
```

All detailed rules, patterns, and templates are in this Skill's files.

## Supporting Files

- `rules/gitignore-patterns.md`: Comprehensive .gitignore pattern library
- `rules/file-classification.md`: Detailed file classification rules
- `templates/commit-message.md`: Commit message template and examples

## Usage Tips

### When NOT to use this Skill

- Simple typo fixes in docs (just commit directly)
- When you want to commit with custom message format
- Emergency hotfixes (speed matters more than format)

### When to DEFINITELY use this Skill

- First commit in new repo
- Committing to `~/.claude/` (high risk of exposing sensitive configs)
- Large changesets with multiple types of changes
- When unsure about what to commit/exclude

## Maintenance

This Skill should be updated when:

- New file types need classification rules
- New sensitive patterns are discovered
- Commit message conventions evolve
- New tech stacks require specific patterns

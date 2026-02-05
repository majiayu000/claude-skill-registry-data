---
name: julien-dev-commit-message
description: Generates semantic commit messages from git diff following conventional commits format. Use when user asks to commit changes, wants help writing a commit message, or needs to create a git commit.
allowed-tools: Bash, Read
---

# Commit Message Generator Skill

This skill analyzes `git diff` and `git status` to generate a **semantic commit message** following the project's conventions.

---

## 🎯 What This Does

Generates commit messages in this format:

```
<type>(<scope>): <description>

<body>

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>
```

---

## 📝 Commit Message Format

### Type

| Type | When to Use |
|------|-------------|
| `feat` | New feature or functionality |
| `fix` | Bug fix |
| `docs` | Documentation only changes |
| `refactor` | Code refactoring (no functional change) |
| `style` | Formatting, missing semicolons (no code change) |
| `test` | Adding or updating tests |
| `chore` | Maintenance (dependencies, config, etc.) |

### Scope (clemencefouquet.fr specific)

| Scope | When to Use |
|-------|-------------|
| `wordpress` | WordPress content, pages, posts, config |
| `docs` | Documentation (docs/ directory) |
| `design` | CSS, design system, visual changes |
| `infra` | Docker, Nginx, VPS, deployment |
| `a11y` | Accessibility improvements |

### Description

- **50 characters max**
- Imperative mood ("Add feature" not "Added feature")
- No period at the end
- Lowercase after colon

### Body (optional)

- Explain **why** not **what** (git diff shows what)
- Wrap at 72 characters
- Bullet points with `-` prefix
- Include relevant IDs, URLs, issue numbers

---

## 🔍 Analysis Process

### Step 1: Run git status

```bash
git status
```

**Look for:**
- Staged files (to be committed)
- Unstaged changes (not included)
- Untracked files (new files)

### Step 2: Run git diff

```bash
# Staged changes
git diff --cached

# Or all changes if nothing staged
git diff
```

**Analyze:**
- Which files changed?
- What type of changes? (new files, modifications, deletions)
- What functionality was added/fixed/changed?

### Step 3: Check recent commits for style

```bash
git log --oneline -10
```

**Note:**
- Commit message style in this repo
- Common scopes used
- Typical description patterns

---

## 💡 Examples

### Example 1: New WordPress Page

**Changes:**
```diff
+ docs/wordpress/guides/GUTENBERG_WP_CLI.md (new file)
+ .claude/agents/wordpress-dev.md (new file)
```

**Generated commit:**
```
feat(wordpress): Add WP-CLI guide and wordpress-dev agent

- Created comprehensive WP-CLI guide (250 lines)
- Implemented wordpress-dev subagent for automated page creation
- Added STDIN injection patterns for content updates
- Documented common WP-CLI commands and troubleshooting

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>
```

---

### Example 2: CSS Bug Fix

**Changes:**
```diff
- .service-card { padding: 20px; }
+ .service-card { padding: var(--space-6); }
```

**Generated commit:**
```
fix(design): Use design tokens for service card padding

Replaced hardcoded 20px with var(--space-6) for consistency
with 8px grid system.

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>
```

---

### Example 3: Documentation Update

**Changes:**
```diff
+ docs/wordpress/README.md (new file)
~ docs/wordpress/GUIDE_RAPIDE.md (modified)
```

**Generated commit:**
```
docs: Add README navigation and update quick start guide

- Created README.md with documentation structure
- Updated GUIDE_RAPIDE.md with SSH access patterns
- Added cross-references between documents

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>
```

---

### Example 4: Refactoring

**Changes:**
```diff
- Duplicated gradient code in 6 files
+ Created _snippets/hero-gradient-violet-orange.php
~ Updated all files to reference snippet
```

**Generated commit:**
```
refactor(docs): Extract hero gradient to DRY snippet

- Created canonical hero-gradient-violet-orange.php snippet
- Removed 6 duplicate gradient implementations
- Updated all documentation to reference snippet
- Improves maintainability and follows DRY principle

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>
```

---

### Example 5: Multiple Scopes (use most significant)

**Changes:**
```diff
+ .claude/agents/design-validator.md
+ docs/wordpress/foundations/ACCESSIBILITY_WCAG.md
~ README.md
```

**Generated commit:**
```
feat(a11y): Add design-validator agent and WCAG documentation

- Implemented design-validator subagent for WCAG 2.2 AA compliance
- Created ACCESSIBILITY_WCAG.md foundation document
- Added contrast validation and touch target checking
- Updated README with new agents structure

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>
```

---

## 🎯 Generation Workflow

### 1. Gather Information

```bash
# Check what's staged
git status

# See the changes
git diff --cached --stat

# Read the actual diff
git diff --cached

# Check recent commits for style
git log --oneline -5
```

### 2. Analyze Changes

Ask yourself:
- **What** changed? (files, lines)
- **Why** did it change? (new feature, bug fix, refactor)
- **What scope** does this affect? (wordpress, docs, design, infra)
- **Is this a breaking change?** (probably not for this project)

### 3. Draft Message

```
<type>(<scope>): <description max 50 chars>

<body explaining why>
- Bullet point 1
- Bullet point 2
- Bullet point 3

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>
```

### 4. Present to User

```markdown
## Proposed Commit Message

\`\`\`
feat(wordpress): Add new Services page

- Created Services page with 4 service cards
- Used custom-clemence.css classes for styling
- Added hero gradient using canonical snippet
- Validated WCAG AA contrast ratios

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>
\`\`\`

**Files changed**: 1 insertion
**Type**: New feature
**Scope**: WordPress content

Review this message, then run:
\`\`\`bash
git commit -m "$(cat <<'EOF'
feat(wordpress): Add new Services page

- Created Services page with 4 service cards
- Used custom-clemence.css classes for styling
- Added hero gradient using canonical snippet
- Validated WCAG AA contrast ratios

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
\`\`\`
```

### 5. Wait for User Approval

**DON'T commit automatically.** Always:
1. Present the message
2. Explain the reasoning
3. Provide the `git commit` command
4. Wait for user to execute

---

## 🚫 What NOT to Commit

**Warn the user if these files are staged:**

- `.env` files
- `credentials.json`
- API keys
- Private keys (`.pem`, `.key`)
- Database dumps
- Large binary files (>10MB)

**Example warning:**
```markdown
⚠️ **WARNING**: The following files may contain secrets:
- `.env`
- `config/credentials.json`

Are you sure you want to commit these? Consider adding them to .gitignore instead.
```

---

## 📋 Checklist

Before presenting commit message:

- [ ] Type is appropriate (feat/fix/docs/refactor/style/test/chore)
- [ ] Scope matches file locations
- [ ] Description ≤ 50 characters
- [ ] Description in imperative mood
- [ ] Body explains "why" not "what"
- [ ] Body lines wrapped at 72 characters
- [ ] No sensitive information in staged files
- [ ] Claude Code attribution included
- [ ] User provided command to execute (not auto-committed)

---

## 🎯 Success Criteria

Commit message is successful when:

1. ✅ Follows conventional commits format
2. ✅ Type and scope are accurate
3. ✅ Description is concise (<50 chars)
4. ✅ Body explains motivation
5. ✅ No sensitive data detected in staged files
6. ✅ User approved before executing
7. ✅ Claude Code attribution present

---

## 📞 When to Use This Skill

**Use when user says:**
- "Help me commit these changes"
- "Generate a commit message"
- "I want to commit but don't know what to write"
- "Create a commit for me"

**Don't use when:**
- User provides their own commit message (use it)
- No changes staged (`git status` clean)
- User just wants to see changes (use `git diff` directly)

---

## 💡 Tips for Great Commit Messages

### DO:
- ✅ Focus on **why** the change was made
- ✅ Reference issue numbers if applicable
- ✅ Keep description short and clear
- ✅ Use bullet points in body for multiple changes
- ✅ Mention breaking changes explicitly

### DON'T:
- ❌ Describe **what** changed (git diff shows that)
- ❌ Use past tense ("Added" → use "Add")
- ❌ Write novels (keep body concise)
- ❌ Commit without user approval
- ❌ Include sensitive information

---

**Remember**: A good commit message explains **why** the change was necessary, not what changed (the diff shows that). Help the user tell the story of their work.

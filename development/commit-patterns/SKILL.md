---
name: commit-patterns
description: Generates conventional commit messages. Use when creating git commits or reviewing staged changes. Ensures NO AI attribution in commits.
---

# Commit Message Patterns

Generate conventional commit messages following best practices for the Posterns MVP project.

**CRITICAL**: Never mention AI tools or add Co-Authored-By tags in commit messages. Commits must appear as regular developer commits without any AI attribution.

## Commit Message Format

```
<type>: <short description>

<detailed body explaining what and why>

<breaking changes if any>
```

### Message Components

1. **Type**: Category of change (required)
2. **Short Description**: One-line summary under 50 characters (required)
3. **Body**: Detailed explanation of what and why, not how (optional but recommended)
4. **Breaking Changes**: Note any breaking changes (if applicable)

## Commit Types

- **feat**: New feature or significant enhancement
- **fix**: Bug fix
- **refactor**: Code restructuring without changing functionality
- **docs**: Documentation changes
- **style**: Formatting, whitespace, etc. (no code logic change)
- **test**: Adding or updating tests
- **chore**: Maintenance tasks (dependencies, config, etc.)
- **perf**: Performance improvements
- **security**: Security-related changes

## Commit Message Guidelines

### Short Description Rules

- Start with lowercase (except proper nouns like "Posterns", "Prisma", "NextAuth")
- No period at the end
- Use imperative mood ("add" not "added", "fix" not "fixed")
- Under 50 characters
- Be specific but concise

✅ **Good Examples**:
- `feat: add user profile page with edit functionality`
- `fix: resolve email verification token expiry bug`
- `refactor: extract rate limiting logic to separate module`
- `security: add rate limiting to authentication endpoints`

❌ **Bad Examples**:
- `feat: Added new feature` (wrong tense, not specific)
- `fix: Fixed bug.` (period at end, not specific)
- `update: updated some files` (vague, not specific)
- `feat: add user profile page with edit functionality and validation and error handling and loading states` (too long)

### Body Guidelines

- Explain **what** changed and **why**, not how
- Use bullet points for multiple changes
- Reference issue numbers if applicable (e.g., "Fixes #123")
- Keep lines under 72 characters for readability
- Leave blank line between subject and body
- **NEVER mention AI tools, Claude, or automation**

### FORBIDDEN Content

**NEVER include in commit messages**:
- ❌ Any mention of AI, Claude, GPT, or other AI tools
- ❌ `Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>`
- ❌ `🤖 Generated with [Claude Code](https://claude.com/claude-code)`
- ❌ `🤖 Generated with Claude Code`
- ❌ Any reference to AI assistance
- ❌ Phrases like "with AI help", "AI-assisted", "automated generation"

## Example Commits

### Feature Addition

```
feat: add multi-company comparison page

Implements comparison functionality allowing users to:
- Select up to 5 companies for comparison
- View side-by-side financial ratios
- Filter comparison metrics by category
- Export comparison results to CSV

URL state persistence ensures selected companies are restored
after locale changes or page refreshes.

Integrates with existing financial ratios display component.
```

### Bug Fix

```
fix: resolve database connection error after schema changes

The SQLite database path was using relative paths which caused
resolution issues in production builds. Changed lib/prisma.ts
to use absolute path via process.cwd() to ensure consistent
database access across all environments.

This fix clears the .next cache and restarts the dev server
to prevent stale Prisma client issues.
```

### Refactoring

```
refactor: extract authentication validation to shared utility

Moved duplicate validation logic from multiple API routes into
lib/auth/validate.ts. This improves maintainability and ensures
consistent validation across all auth endpoints.

No functional changes - authentication behavior remains identical.
```

### Security Fix

```
security: add rate limiting to authentication endpoints

Implements in-memory rate limiting to prevent brute force attacks:
- Login: 5 requests per minute per IP
- Register: 3 requests per minute per IP
- Password reset: 3 requests per minute per IP
- Email verification: 5 requests per minute per IP

Uses client IP address for identification via x-forwarded-for header.
Automatic cleanup of expired rate limit records every 5 minutes.
```

### Database Schema Change

```
feat: add email verification fields to user model

Extends User model with email verification support:
- emailVerified timestamp field
- VerificationToken relation for email verification tokens

Includes migration to add new columns to existing database.
Backward compatible - existing users will have null emailVerified
until they verify.

Run `npx prisma generate && npx prisma db push` to apply changes.
```

### Internationalization

```
feat: add Latvian and English translations for auth pages

Adds complete i18n support for authentication flow:
- Login page translations
- Registration form with validation messages
- Password reset flow
- Email verification pages

Both lv.json and en.json updated with auth namespace.
Locale switcher tested and works across all auth pages.
```

### Performance Improvement

```
perf: optimize company search with database indexing

Adds database indexes to frequently queried fields:
- Company name (case-insensitive search)
- Registration code (exact match lookups)
- Status (filtering active/inactive companies)

Query performance improved from ~500ms to ~50ms for searches
with 10,000+ companies in database.
```

### Documentation

```
docs: add API documentation for company endpoints

Documents all company-related API endpoints:
- GET /api/company/[id] - Fetch company details
- GET /api/companies/batch - Batch fetch multiple companies
- GET /api/compare - Compare companies with financial ratios

Includes request/response examples and error codes.
```

## Atomic Commits

Each commit should represent a single, complete, working change:

✅ **Good - Atomic**:
- One feature fully implemented
- One bug completely fixed
- One refactoring completed
- Each commit leaves codebase in working state

❌ **Bad - Not Atomic**:
- Half-implemented feature
- Mix of multiple unrelated changes
- Broken code that requires next commit to fix
- "WIP" or "checkpoint" commits

### Example: Breaking Down Large Feature

Instead of:
```
feat: add user management system
```

Use multiple atomic commits:
```
feat: add user authentication schema
feat: implement login API endpoint
feat: create login UI component
feat: add email verification flow
feat: implement password reset functionality
```

## Commit Frequency

**When to commit**:
- After completing a feature or sub-feature
- After fixing a bug
- After refactoring is complete and tests pass
- Before switching to a different task
- At logical stopping points
- When code is in working state

**When NOT to commit**:
- Code doesn't compile/run
- Tests are failing
- Feature is half-done
- Just to save work (use `git stash` instead)
- Multiple unrelated changes mixed together

## Special Cases

### Multiple Related Changes

If changes are closely related but separable, create multiple commits:

```
feat: add user authentication schema
feat: implement user registration API
feat: create registration UI form
feat: add email verification
```

This allows reverting individual pieces if needed.

### Breaking Changes

For breaking changes, add `BREAKING CHANGE:` section in footer:

```
feat: update API response format for company data

Company API now returns nested financial ratios structure
for better organization and type safety.

BREAKING CHANGE: Company API now returns financialRatios as nested
object instead of flat array. Clients must update to access ratios
via company.financialRatios.profitability instead of company.ratios[0].

Migration guide available in docs/migration-v2.md
```

### Reverting Commits

When reverting a previous commit:

```
revert: feat: add experimental caching feature

This reverts commit abc123def456.

Reason: Feature caused performance degradation in production
with large datasets. Will revisit with optimized implementation
using Redis instead of in-memory cache.
```

### Dependency Updates

```
chore: update dependencies to latest versions

Updates:
- next: 16.0.0 → 16.1.0
- prisma: 6.0.0 → 6.1.0
- typescript: 5.3.0 → 5.4.0

All tests passing. No breaking changes in minor versions.
```

## Pre-Commit Checklist

Before committing, verify:

- [ ] Code compiles without errors
- [ ] No `console.log` statements left in code (unless intentional)
- [ ] All imports are used (no unused imports)
- [ ] TypeScript types are correct (no `any` types)
- [ ] Tests pass (if applicable)
- [ ] i18n keys added for all new user-facing text
- [ ] No secrets or API keys in code
- [ ] No `.env` files being committed
- [ ] `.gitignore` updated if needed
- [ ] Commit message is clear and descriptive
- [ ] **NO AI attribution anywhere in commit message**

## Git Commit Command Format

### Single-Line Commit

For simple changes:

```bash
git commit -m "fix: resolve typo in company status label"
```

### Multi-Line Commit with Body

Use heredoc for clean formatting:

```bash
git commit -m "$(cat <<'EOF'
feat: add user registration with email verification

Implements registration flow:
- User submits name, email, password
- Password validated for strength requirements
- Email verification token generated and sent
- Rate limiting prevents abuse (3 req/min)

Uses bcrypt for password hashing (12 rounds).
Zod schemas validate all user inputs.
EOF
)"
```

**Key Points**:
- Use `<<'EOF'` (single quotes) to prevent variable expansion
- No trailing whitespace
- Clean, professional message
- **Absolutely no AI attribution**

### Amend Last Commit

If you forgot to include files in last commit (before push):

```bash
# Add forgotten files
git add forgotten-file.ts

# Amend last commit without changing message
git commit --amend --no-edit

# Or amend and edit message
git commit --amend
```

**WARNING**: Never amend commits that have been pushed to remote!

## Common Mistakes to Avoid

❌ **Vague messages**:
- "update code"
- "fix stuff"
- "changes"
- "wip"

❌ **Too much detail in subject**:
- "feat: add user profile page with edit functionality and validation and error handling and loading states and success messages"

❌ **Mixing concerns**:
- One commit that adds a feature AND fixes unrelated bugs

❌ **Non-working commits**:
- Code that doesn't compile
- Tests that fail
- Runtime errors

❌ **AI attribution** (CRITICAL):
- Don't mention AI tools anywhere in commit message
- Don't add Co-Authored-By tags for AI
- Commits should appear as regular developer work

❌ **Past tense**:
- "added feature" → Use "add feature"
- "fixed bug" → Use "fix bug"

❌ **Periods in subject**:
- "feat: add feature." → Use "feat: add feature"

## Posterns-Specific Guidelines

### Branding References

When mentioning the product, use:
- ✅ "Posterns" (proper noun, capitalized)
- ✅ "Posterns MVP"
- ❌ "posterns" (not lowercase in commit messages)

### Technology References

Use proper casing for technologies:
- ✅ Next.js, NextAuth.js, Prisma, SQLite, PostgreSQL
- ✅ TypeScript, JavaScript, Tailwind CSS
- ✅ Latvian (lv), English (en)

### File Path References

When mentioning file paths, use backticks:
- ✅ Changes `lib/prisma.ts` configuration
- ✅ Updates `messages/lv.json` with new translations

## Output Format for Agents

When generating commit messages, provide:

1. **Suggested commit message** in proper format
2. **Files to stage** (list of file paths)
3. **Git add command** to stage files
4. **Git commit command** to execute
5. **Verification** that commit leaves code in working state

### Example Output

```
Suggested commit:
---
feat: add email verification for user registration

Implements email verification:
- Generate secure verification tokens (32 bytes)
- Send verification emails via Resend API
- Email verification endpoint
- Resend verification functionality

Tokens expire after 24 hours for security.
New users must verify email before full access.
---

Files to stage:
- app/api/auth/register/route.ts
- app/api/auth/verify-email/route.ts
- lib/auth/tokens.ts
- lib/email/index.ts
- components/auth/verify-email-form.tsx
- messages/lv.json
- messages/en.json

Commands:
# Stage files
git add app/api/auth/register/route.ts app/api/auth/verify-email/route.ts lib/auth/tokens.ts lib/email/index.ts components/auth/verify-email-form.tsx messages/lv.json messages/en.json

# Commit
git commit -m "$(cat <<'EOF'
feat: add email verification for user registration

Implements email verification:
- Generate secure verification tokens (32 bytes)
- Send verification emails via Resend API
- Email verification endpoint
- Resend verification functionality

Tokens expire after 24 hours for security.
New users must verify email before full access.
EOF
)"

# Push
git push origin main
```

## References

- [Conventional Commits](https://www.conventionalcommits.org/)
- [How to Write a Git Commit Message](https://chris.beams.io/posts/git-commit/)
- [Angular Commit Message Guidelines](https://github.com/angular/angular/blob/main/CONTRIBUTING.md#commit)

## Remember

1. **NEVER mention AI in commits** - This is the most critical rule
2. Commits should tell a story of project evolution
3. Future developers will read these commits
4. Clear commits make debugging easier
5. Atomic commits enable selective reverts
6. Good commits are documentation

Every commit message should answer: **What changed and why?**

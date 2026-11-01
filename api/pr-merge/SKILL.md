---
name: cs-pr-merge
description: Extract generalizable rules from PR comments and open a PR updating CLAUDE.md instructions
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash, Edit
---

# PR Prepare Merge

You are a senior engineering standards curator. Given a PR number, you review all human comments, extract feedback that can be generalized into reusable CLAUDE.md rules, and open a PR against the source PR's branch with the updates.

## Inputs

`$ARGUMENTS` — the PR number to process (required).

## Step 1: Gather Context

Run these commands **one at a time** (do not chain):

1. Get repo info:

   ```bash
   gh repo view --json owner,name
   ```

   Parse the JSON to extract `owner.login` and `name`. Use these as `OWNER` and `REPO` below.

2. Get PR details:

   ```bash
   gh pr view $ARGUMENTS --json title,body,author,baseRefName,headRefName
   ```

3. Get all review comments (inline code comments):

   ```bash
   gh api repos/OWNER/REPO/pulls/$ARGUMENTS/comments --paginate
   ```

4. Get all issue-level comments (general discussion):

   ```bash
   gh api repos/OWNER/REPO/issues/$ARGUMENTS/comments --paginate
   ```

5. Get all review bodies (approve/request-changes comments):
   ```bash
   gh api repos/OWNER/REPO/pulls/$ARGUMENTS/reviews --paginate
   ```

## Step 2: Filter Comments

From all collected comments, keep ONLY comments that:

1. **Come from humans** — skip bot comments (author association: `NONE` with bot-like names, or `login` containing `[bot]`)
2. **Contain actionable feedback** — skip approvals like "LGTM", "looks good", emoji-only reactions
3. **Are generalizable** — the feedback applies beyond this single PR. Skip comments that are purely about this PR's specific logic (e.g., "rename this variable to X", "this should be `userId` not `id`")

### What IS generalizable (extract these):

- Coding patterns: "always use early returns", "prefer `const` over `let`"
- Architecture rules: "services should not import from controllers", "use DTOs for API responses"
- Security practices: "never log request bodies", "always validate file upload types"
- Convention decisions: "use arrow functions for service methods", "use `findUniqueOrThrow` instead of null checks"
- Process rules: "add migration for schema changes", "update OpenAPI spec when changing endpoints"
- Domain rules: "use Decimal.js for monetary values", "vessel types must use Prisma enum"

### What is NOT generalizable (skip these):

- One-off fixes: "this variable name is wrong", "missing semicolon here"
- PR-specific logic: "this query should filter by orgId too"
- Questions: "why did you use X here?" (unless the answer establishes a rule)
- Nitpicks with no pattern: "typo in comment"

## Step 3: Read Current Rules

Read `CLAUDE.md` and `.claude/skills/**/*.md` to avoid duplicates. Do not read the analyzer plugin's own skill files.

If no `CLAUDE.md` exists, create one with this structure:

```markdown
# Project Name

Brief description of the project.

## Architecture

- [Layer/module structure rules]

## Code Style

- [Naming conventions, formatting rules]

## Patterns

- [Preferred patterns and anti-patterns]

## Security

- [Security-related rules]

## Testing

- [Testing conventions]
```

## Step 4: Draft Updates

For each generalizable comment:

1. Check if the rule already exists in `CLAUDE.md` or project-local skills — if yes, skip it
2. Determine the best section to place it (create a new section if needed)
3. Write the rule as a concise, imperative instruction (e.g., "Use `findUniqueOrThrow` instead of `findUnique` + null check")

### Rule format:

- Imperative mood: "Use X", "Always Y", "Never Z", "Prefer A over B"
- Include "why" only if not obvious; include a code example only if the pattern is non-trivial

## Step 5: Show Extracted Rules

Output the list of extracted rules, then automatically include ALL of them:

```
Extracted N rules from PR #$ARGUMENTS:

1. "Use findUniqueOrThrow instead of findUnique + null check"
   → Source: @reviewer — "we should always use the throwing variant"

2. "Services must not import from controllers"
   → Source: @lead — "this breaks our layered architecture"

3. "Use Decimal.js for all monetary values"
   → Source: @reviewer — "floating point will cause rounding bugs"

Skipped: 5 comments (not generalizable / duplicates / bot)

Including all N rules in CLAUDE.md...
```

If no generalizable rules were found, report "No generalizable feedback found. No PR created." and stop.

## Step 6: Create PR

Run these commands **one at a time**:

1. Switch to the source PR's branch (`headRefName` from Step 1) and update:

   ```bash
   git checkout <HEAD_REF_NAME>
   ```

   ```bash
   git pull origin <HEAD_REF_NAME>
   ```

2. Create new branch from the PR's branch:

   ```bash
   git checkout -b claude-instructions-from-pr-<PR_NUMBER>
   ```

3. Apply the CLAUDE.md changes using the Edit tool.

4. Stage and commit:

   ```bash
   git add CLAUDE.md
   ```

   ```bash
   git commit -m "Update CLAUDE.md with rules from PR #<PR_NUMBER>" --no-gpg-sign
   ```

5. Push the branch:
   ```bash
   git push -u origin claude-instructions-from-pr-<PR_NUMBER>
   ```

**Important:** Do NOT add `Co-Authored-By`, `Signed-off-by`, or any AI/Claude attribution to commits.

6. Show the PR preview, then automatically create it with `gh pr create --base <HEAD_REF_NAME>` (targeting the source PR's branch):

   ```
   Creating PR:
   Title: Update CLAUDE.md with rules extracted from PR #18
   Base: <HEAD_REF_NAME> (PR #$ARGUMENTS branch)
   ```

7. Add label (run separately):
   ```bash
   gh label create "claude-rules" --description "Auto-extracted rules from PR comments" --color "1d76db" --force
   ```
   ```bash
   gh pr edit --add-label "claude-rules"
   ```

Use the following structure for the body (replace placeholders with actual values):

- **Base**: `<HEAD_REF_NAME>` (the source PR's branch)
- **Title**: `Update CLAUDE.md with rules extracted from PR #<PR_NUMBER>`
- **Body**:

```
## Summary

Extracted generalizable coding rules from review comments on PR #<PR_NUMBER> and added them to CLAUDE.md.

## Extracted Rules

- **Rule**: [the rule added]
  - **Source**: PR #<PR_NUMBER> comment by @[author] — "[original comment snippet]"

## Notes

- Only generalizable patterns were extracted (project-specific feedback was skipped)
- Existing rules were not duplicated
- Rules were placed in the most appropriate section of CLAUDE.md
```

## Important

- **Read-only on the target PR** — do not modify, comment on, or merge the original PR
- **Only modify CLAUDE.md** — do not touch any other files

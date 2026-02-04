---
name: new-issue
description: Create GitHub issues with duplicate detection and codebase analysis. Use when you discover a bug, improvement, or issue that wasn't in the original scope/spec during development. Triggers on phrases like "create an issue", "file a bug", "this should be tracked", "we should fix this later", "out of scope issue", "noticed a problem", "found a bug".
allowed-tools: Bash(gh:*), Grep, Glob, Read, WebSearch, Task, mcp__conductor__AskUserQuestion
---

# Smart GitHub Issue Creation

This skill helps create well-researched GitHub issues while preventing duplicates and wasted effort.

## When to Use This Skill

Activate this skill when:
- You discover a bug or issue that's **outside the current task's scope**
- You notice something that should be fixed but isn't part of the current spec
- The user mentions wanting to "track this for later" or "create an issue"
- You find an improvement opportunity while working on something else
- The user explicitly asks to create an issue or file a bug

## Workflow

### Step 1: Clarify the Issue

If the issue description is vague or missing, ask the user:
> "What issue would you like to create? Describe the bug, feature, or improvement."

### Step 2: Check if Already Fixed/Implemented

Before creating, verify this isn't already solved:

1. **Search codebase** for related keywords:
   ```bash
   # Use Grep/Glob to find relevant code
   ```

2. **Check recent commits:**
   ```bash
   gh api repos/{owner}/{repo}/commits --jq '.[0:20] | .[] | "\(.sha[0:7]) \(.commit.message | split("\n")[0])"'
   ```

3. **If already fixed/implemented**, inform the user:
   > "It looks like this might already be addressed. I found [what you found]. Are you aware of this?"

   Options: "Show me the existing solution", "Create the issue anyway", "Cancel"

### Step 3: Check Existing GitHub Issues

Search for duplicates:

1. **Search open issues:**
   ```bash
   gh issue list --state open --limit 50 --json number,title,body,labels,url
   ```

2. **Search closed issues:**
   ```bash
   gh issue list --state closed --limit 30 --json number,title,body,labels,url,closedAt
   ```

3. **Keyword search:**
   ```bash
   gh search issues --repo {owner}/{repo} "keywords" --limit 20 --json number,title,body,url,state
   ```

4. **Fetch details with comments for promising matches:**
   ```bash
   gh issue view <number> --json number,title,body,comments,labels,state
   ```

5. **Based on findings:**

   **EXACT DUPLICATE:**
   > "I found an existing issue #[number] - [title] that matches this. What would you like to do?"
   - Options: "Add comment to existing", "View details", "Create anyway", "Cancel"

   **RELATED ISSUE:**
   > "I found related issue #[number]. Your issue could be a comment, sub-issue, or separate. Preference?"
   - Options: "Add as comment", "Create as sub-issue (I'll activate gh-subissues skill)", "Create separate issue"

   **CLOSED ISSUE:**
   > "This was previously reported as #[number] and [fixed/rejected]. Context: [summary]. Still want to proceed?"

### Step 4: Research Potential Solutions

If you have enough context:

1. **Explore codebase** for patterns and relevant files
2. **Use web search** via Task tool for best practices
3. **Formulate 1-3 approaches** with:
   - Brief description
   - Files that would need changes
   - Trade-offs (if applicable)

### Step 5: Draft Issue Content

Structure the issue:

```markdown
## Summary
[1-2 sentences]

## Context
[Background, how discovered, why it matters]

## Current Behavior (for bugs)
[What happens now]

## Expected Behavior
[What should happen]

## Potential Implementation (optional)
### Approach 1: [Name]
- Description
- Files: `path/to/file.ts`

## Additional Context
[Related issues, screenshots, etc.]
```

### Step 6: Confirm Before Creating

Present your findings:
> "Here's the issue I'm planning to create:
>
> **Title:** [title]
> **Summary:** [summary]
> **Key findings:** [what you discovered]
>
> Ready to create?"

Options: "Create the issue", "Edit first", "Show details", "Cancel"

### Step 7: Create the Issue

```bash
gh issue create --title "type(area): description" --body "$(cat <<'EOF'
[structured content]
EOF
)"
```

Then display the URL and issue number.

## Sub-Issue Support

To create as a sub-issue, say:
> "I'll activate the gh-subissues skill to create this as a sub-issue of #[parent]."

Then use the Skill tool to invoke `gh-subissues`.

## During Development: Out-of-Scope Issues

When you notice an issue while working on something else:

1. **Briefly mention it** to the user:
   > "While working on [current task], I noticed [issue]. This seems out of scope for the current work. Would you like me to create an issue to track this for later?"

2. **If user agrees**, run through this workflow
3. **If user declines**, continue with the current task

This prevents scope creep while ensuring important issues aren't forgotten.

## Issue Title Conventions

Use conventional format:
- `fix(area): brief description` - Bug fixes
- `feat(area): brief description` - New features
- `refactor(area): brief description` - Code improvements
- `docs(area): brief description` - Documentation
- `chore(area): brief description` - Maintenance

## Notes

- Always prioritize preventing duplicates - saves everyone time
- Be thorough but concise - don't overwhelm the user
- For simple, clearly new issues, streamline the process
- Keep the user informed at each decision point

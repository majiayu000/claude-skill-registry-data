---
name: ralph-bugbot
description: Loop-aware skill for iteratively addressing bugbot feedback on PRs. Fetches unresolved bugbot comments, triages them, fixes valid bugs, resolves false positives, and commits changes. Designed to be used with ralph-loop.
color: orange
---

# Ralph Bugbot

Loop-aware skill for iteratively addressing bugbot feedback. Designed to be used with `/ralph-loop`.

## Purpose

This skill helps you systematically address bugbot feedback on pull requests by:
1. Fetching unresolved bugbot comments
2. Triaging each comment (bug vs false positive)
3. Fixing valid bugs with surgical edits
4. Resolving verified false positives via GraphQL
5. Committing and pushing changes
6. Waiting for bugbot to re-analyze

## CRITICAL: Execute Commands Immediately

**DO NOT deliberate or explain. Run the bash commands in each step IMMEDIATELY.**

This is an action-oriented skill. Follow steps in order, execute commands directly, move fast.

## Workflow

### Step 1: Wait for Bugbot (if running)

**RUN THIS IMMEDIATELY to ensure bugbot has finished analyzing:**

Run the `wait-for-bugbot.sh` script in this skill's directory.

This script checks if bugbot is currently running and waits for it to complete before proceeding.

### Step 2: Fetch Unresolved Comments

**RUN THIS IMMEDIATELY:**

```bash
# Get repo and PR info
OWNER=$(gh repo view --json owner -q '.owner.login')
REPO=$(gh repo view --json name -q '.name')
PR_NUM=$(gh pr view --json number -q '.number')

echo "Fetching bugbot comments on PR #$PR_NUM..."

# Get unresolved review threads from bugbot (with thread IDs for resolving)
gh api graphql -f query='
query {
  repository(owner: "'"$OWNER"'", name: "'"$REPO"'") {
    pullRequest(number: '"$PR_NUM"') {
      reviewThreads(first: 50) {
        nodes {
          id
          isResolved
          comments(first: 1) {
            nodes {
              author { login }
              body
              path
              line
            }
          }
        }
      }
    }
  }
}' --jq '.data.repository.pullRequest.reviewThreads.nodes[] | select(.isResolved == false) | select(.comments.nodes[0].author.login == "cursor")'
```

### Step 3: Evaluate Completion

**IMMEDIATELY after Step 2:**

- **Zero comments?** → Output `<promise>BUGBOT RESOLVED</promise>` and STOP.
- **Has comments?** → Continue to Step 4. Do not deliberate.

### Step 4: Process Each Comment

For each unresolved bugbot comment:

#### Triage

Categorize before investigating:
- **Likely bug**: Logic errors, null checks, race conditions, security issues
- **Likely false positive**: Style suggestions, "consider using", optional improvements
- **Needs investigation**: Unclear without reading code

#### Verify RIGOROUSLY

**For potential false positives, you MUST prove it before resolving:**

1. **Read the ENTIRE file** - Get complete context, not just the flagged line
2. **Search for related code** - Use Grep to find similar patterns in codebase
3. **Check defensive code** - Look for validation, error handling, type guards elsewhere
4. **Trace data flow** - Follow the execution path to understand safeguards
5. **Verify false positive criteria** - Confirm it matches one of these:
   - Style suggestion only (no functional impact)
   - Already handled by defensive code elsewhere
   - Impossible condition (proven by type system or validation)
   - Misunderstanding of framework/library behavior

**ONLY if you have concrete evidence it's safe, mark as false positive.**

#### Fix Valid Bugs

- Make minimal, surgical edits
- Follow existing code patterns
- One fix at a time

#### Resolve False Positives

**ONLY after rigorous verification, resolve the thread:**

```bash
# THREAD_ID from Step 2's output (the "id" field)
gh api graphql -f query='
mutation {
  resolveReviewThread(input: {threadId: "'"$THREAD_ID"'"}) {
    thread {
      id
      isResolved
    }
  }
}
'
```

**Do not resolve unless you can explain WHY it's a false positive with evidence.**

### Step 5: Commit and Push

**EXECUTE THESE COMMANDS after fixing (do not skip):**

1. Stage all changes: `git add -A`
2. Commit with message describing fixes: `git commit -m "fix: address bugbot feedback"`
3. Push to remote: `git push`

**You MUST run git add, commit, and push. Do not just show the commands.**

### Step 6: Wait for Bugbot Check

**RUN THIS IMMEDIATELY after pushing. Do not skip.**

Run the `wait-for-bugbot.sh` script in this skill's directory.

### Step 7: Report Progress

**Brief summary only** (don't over-explain):

```
Fixed: [list files:lines]
Resolved as false positive: [list files:lines with brief reason]
Remaining: [count]
```

### Step 8: Loop Behavior

After pushing and waiting for bugbot check:
- Do NOT output the completion promise yet
- The ralph-loop will re-run this skill
- Next iteration will re-fetch comments (bugbot has finished re-analyzing)
- Only output `<promise>BUGBOT RESOLVED</promise>` when Step 2 finds zero unresolved comments

## Rules

1. **Move fast** - Execute commands immediately. No deliberation between steps.
2. **Only unresolved bugbot comments** - Ignore resolved threads and other reviewers
3. **Verify rigorously** - For false positives, gather evidence before resolving
4. **Resolve false positives** - Use GraphQL mutation to mark them resolved (don't just skip)
5. **Never blindly fix OR resolve** - Both bugs and false positives need verification
6. **Minimal changes** - Fix the bug, don't refactor
7. **When uncertain, skip** - Flag for human review instead of guessing
8. **Always commit and push** - After fixes or resolving false positives
9. **One iteration = one pass** - Don't try to loop internally; let ralph-loop handle iteration

## Usage

Invoke this skill when:
- You need to address bugbot feedback on a PR
- Used with `/ralph-wiggum:ralph-loop` for automated iteration
- User says "fix bugbot comments" or similar

The skill will loop via ralph-loop until all bugbot comments are resolved or fixed.

## Completion Signal

When all bugbot comments are resolved, output:
```
<promise>BUGBOT RESOLVED</promise>
```

This signals to ralph-loop that the task is complete.

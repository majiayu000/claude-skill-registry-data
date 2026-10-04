---
description: Create a GitHub stack PR with guided commit message
allowed-tools: Bash(git status:*), Bash(git diff:*), Bash(echo:*), Bash(fold:*), Bash(wc:*), Bash(gh:*)
argument-hint: [motivation/context]
---

## User-Provided Context

$ARGUMENTS

## Git Context

Current git status:
!`git status --short`

Staged changes (if any):
!`git diff --cached`

Unstaged changes (if nothing staged):
!`git diff`

## Your Task

Help me create a commit and submit it as a GitHub stacked PR.

**IMPORTANT:** Use GitHub Stacks (`gh stack`) for stack, branch, commit, and submission operations. Never bypass stack management with `git commit`, `git push`, or `git checkout -b`.

### Step 1: Analyze the Changes

Study the diff above to understand:
- What files were modified and why
- The nature of the change (bug fix, new feature, refactor, etc.)
- The scope and impact of the changes

### Step 2: Gather Context

**If user provided context above:** Use it as the motivation/explanation. Only ask follow-up questions if something critical is still unclear.

**If no context provided:** Ask targeted questions to understand the change. Don't use a fixed checklist - be intelligent about what's missing:
- If the change is obvious from the code, just confirm your understanding
- If the "why" isn't clear from the diff, ask about motivation
- If there might be side effects, ask about them
- If the change type is ambiguous, ask for clarification

The goal is a conversation, not an interrogation.

### Step 3: Generate Commit Message

Create a commit message following these rules:

**Subject line:**
- Maximum 50 characters (verify with `echo -n "subject" | wc -c`)
- Imperative mood (e.g., "Fix bug" not "Fixed bug")

**Body:**
- Blank line after subject
- Wrapped at 72 characters (use `echo "body text" | fold -s -w 72`)
- Focus on the "why", not the "what" - the diff already shows what changed
- Don't list affected files/classes/functions - that's redundant with the diff
- Should answer: why is this change necessary, what problem does it solve

### Step 4: Generate Branch Name

Create a short kebab-case branch name:
- Simple slug format (e.g., `fix-null-pointer`, `add-user-validation`, `update-deps`)
- Lowercase, hyphens between words
- No type prefix, just a descriptive slug

### Step 5: Create the Stack Layer and Commit

Show me the proposed commit message and branch name. Once I approve, check whether the current branch belongs to a stack:

```bash
gh stack view --json
```

If it reports that the current branch is not part of a stack, initialize one:

```bash
gh stack init <branch-name>
```

Then create the commit. On a newly initialized empty layer, this commits there. On an existing populated stack, this creates a new layer on top:

```bash
gh stack add --all --message "$(cat <<'EOF'
<subject line here>

<wrapped body here>

Co-authored-by: Claude <noreply@anthropic.com>
EOF
)" <branch-name>
```

### Step 6: Submit the PR

Submit the stack non-interactively. `--auto` creates new PRs as drafts unless `--open` is passed:

```bash
gh stack submit --auto
```

### Step 7: Update PR Description

Generate a PR description and apply it with `gh pr edit`.

**Template discovery** — Check these locations in order for a PR template:
1. `.github/PULL_REQUEST_TEMPLATE.md`
2. `.github/PULL_REQUEST_TEMPLATE/` directory (use default template if multiple exist)
3. `PULL_REQUEST_TEMPLATE.md`
4. `docs/PULL_REQUEST_TEMPLATE.md`

**If a template is found:** Use it as the scaffold. Fill in each section using the diff analysis, user-provided context, and commit message. Remove irrelevant sections rather than leaving empty placeholders.

**If no template is found:** Generate a default description with:
- **Summary** — Brief explanation of the change and motivation
- **Changes** — Bullet list of what was changed
- **Test plan** — How to verify the change works

**Apply the description:**
```bash
gh pr edit --body "$(cat <<'EOF'
<generated description here>
EOF
)"
```

### Step 8: Output Slack Review Message

Get the current top PR's title and URL with:

```bash
gh pr view --json title,url
```

Output both Slack-friendly message formats in a fenced markdown block for easy copy-paste:

```
Single PR:
[<commit subject>](<github-url>)

Stack:
[<top PR title>](<top-pr-github-url>)
```

GitHub shows stack context on each PR, so use the top PR URL for the stack link. Print actual links, not placeholders.

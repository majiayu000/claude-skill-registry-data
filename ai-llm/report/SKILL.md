---
name: report
description: Submit feedback to the template repo as a GitHub issue (bug, feature request, or confusion)
argument-hint: "[short description - optional]"
---

# Report

You help the user submit feedback about the template to the upstream repo as a GitHub issue. Use this skill when the user says something like "this doesn't work", "I got stuck", "I wish this did X", or runs `/report` directly.

The target repo for issues is **`aleksander-dytko/ai-pm-workspace`** (the template). Users who are working in their own fork should still file issues against the template, not their fork, so the author can triage across all users.

## Input

The user may provide via `$ARGUMENTS`:
- A short description of the issue.
- Nothing (skill will prompt).

## Workflow

### 1. Categorize the feedback

Ask in one `AskUserQuestion` (unless the category is obvious from the argument):

- **Category**:
  - Bug - something broke or produced wrong output
  - Confusion - I got stuck or couldn't figure out how to do something
  - Feature request - I want the template to do something it doesn't
  - Other feedback - appreciation, context, observation

### 2. Collect context

Prompt for:
- **What happened / what you wanted**: free text, 2-3 sentences.
- **Which skill (if applicable)**: pick from a list of shipped skills, or "not skill-related".
- **What you expected vs. what happened** (for Bug / Confusion only).

Skip any field the user already provided in `$ARGUMENTS`.

### 3. Check if GitHub MCP is available

Look at the deferred tools list (or the `MCP Servers Available` section in `CLAUDE.md`). If any `mcp__github__*` tools are present, GitHub MCP is available.

### 4a. If GitHub MCP is available: open the issue directly

Use the GitHub MCP issue-creation tool with:
- **Repo**: `aleksander-dytko/ai-pm-workspace`
- **Title**: `[{Category}] {short description}`. Example: `[Bug] /meeting crashes when meeting note has no attendees`.
- **Body**: use this template

```markdown
## Category
{Bug | Confusion | Feature request | Other}

## What happened / what I wanted
{User's description}

## Which skill (if any)
{skill name or "not skill-related"}

## Expected vs. actual (bug / confusion only)
**Expected**: {user's expected outcome}
**Actual**: {what actually happened}

## Environment
- Template version / commit: {try to read from CHANGELOG.md top header; fallback "v2"}
- Claude Code version: {ask user if unknown}
- OS: {ask or infer}

---
Submitted via `/report` skill.
```

- **Labels**: `from-report` plus a category label (`bug`, `confusion`, `feature`, `feedback`). If those labels don't exist in the target repo, create them or skip silently.

Before opening the issue, **show the full title and body to the user and ask for confirmation**. This is a public artifact; they need a last-look.

### 4b. If GitHub MCP is not available: print a pre-filled URL

Construct a GitHub issue-URL that pre-fills the title and body. Format:

```
https://github.com/aleksander-dytko/ai-pm-workspace/issues/new?title={url-encoded title}&body={url-encoded body}&labels=from-report,{category}
```

Show the URL to the user and instruct:

```
GitHub MCP isn't configured, so I can't open the issue for you directly.

Click this URL to open a pre-filled issue in your browser:

{URL}

If the URL is too long for your browser, here's the title and body to paste manually into https://github.com/aleksander-dytko/ai-pm-workspace/issues/new :

Title: {title}

Body:
{body}
```

### 5. Confirmation

After the issue is filed (or the user has been shown the URL):

```
Thanks for the feedback!

[if MCP] Issue filed: {URL to new issue}
[if URL fallback] Once you've filed it, the maintainer will triage it and respond.

If you want to follow up, run `/report` again or reply to the issue on GitHub.
```

## Privacy rules

- **Never include vault content in the issue body.** Only what the user explicitly wrote in response to the prompts.
- **Never include file paths that contain the user's name or company.** If a path is mentioned in the description, offer to redact it.
- **Never attach file contents.** If the bug requires a specific file to reproduce, ask the user to paste the minimal snippet that shows the bug, not the whole file.

## Notes

- The skill targets the template repo (`aleksander-dytko/ai-pm-workspace`), not the user's fork. That's deliberate - feedback should flow back to the author so all users benefit.
- Forks that want to collect their own feedback can edit this skill locally to change the target repo.
- If the user wants to file a private issue (e.g., because the feedback references sensitive customer data), tell them to contact the maintainer directly instead of filing a public issue.

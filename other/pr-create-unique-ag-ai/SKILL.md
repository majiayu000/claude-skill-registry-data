---
name: pr-create
description: Proactively draft and create pull requests by inferring title, refs, and body from git context, then confirm and open via gh CLI.
license: MIT
compatibility: claude cursor opencode
metadata:
  version: "1.1.0"
  languages: all
  audience: developers
  workflow: automation
  since: "2026-02-25"
---

## What I do

I take ownership of PR authoring end-to-end:

1. **Auto-draft a semantic PR title** from branch name, commit history, and diff intent.
2. **Auto-extract issue references** from branch name and commit messages (Jira, GitHub issues, and common refs patterns).
3. **Auto-generate a complete PR body** with summary, grouped changes, test plan, and risk/rollout notes.
4. **Ask for confirmation only** (or ask only for missing issue ID when no reference is detected).
5. **Create the PR with `gh pr create`** after explicit user approval.

The default outcome is an opened GitHub PR (not just a draft message), unless you choose to edit before creation.

Supporting files in this skill:
- `assets/pr-description.template` — Markdown structure used when composing the final body

## When to use me

Use when you want to:
- Open a PR quickly with minimal back-and-forth prompts
- Let the agent propose title/body instead of asking you to write sections manually
- Reuse issue references already present in branch names or commits
- Keep PRs consistent with semantic/conventional title style and clear test plans

## PR lifecycle focus

Stage: **Authoring and opening a PR** (before review starts).

## Use Instead [if available]

- Use `pr-self-review` when the PR draft is ready and you want an author checklist before requesting review.
- Use `pr-split` when the main question is PR size/scope and whether to split.
- Use `github-pull-request-handling` when review threads already exist and you need to resolve/reply to comments.

## Example usage

"Help me write a PR for this feature"
"Create the PR from this branch, you choose title/body"
"Open a PR and infer ticket refs from commits"
"Draft everything, show me once, then create with gh if I approve"

---

## Workflow

Here is the default execution flow (agent-led, low-friction):

### Step 1: Collect git context automatically
Gather context without asking the user for manual inputs first:
- Current branch name
- Commit list since base branch (`main`/`master` or configured default)
- Diff summary (key files or areas changed)
- Existing remote tracking state

### Step 2: Extract issue refs from branch and commits
Parse issue identifiers from branch names and commit messages. Prefer existing refs over asking the user.

Common patterns to detect:
```
[A-Z][A-Z0-9]+-\d+        # Jira style, e.g. PROJ-123
#\d+                      # GitHub issue shorthand, e.g. #456
(?:fixes|closes|refs)\s+#?\d+   # commit trailer style refs
```

Examples:
- `PROJ-123-feature-name` -> `PROJ-123`
- commit message `fix(auth): handle timeout (refs #812)` -> `#812`
- commit message `closes #991` -> `#991`

If no reference is found, ask one focused question:
- "No issue reference found in branch/commits. Add one now (e.g., PROJ-123 or #456), or continue without refs?"

### Step 3: Propose PR title automatically
Generate one best-guess semantic title using:
```
<type>(<scope>): <subject>
```

Where:
- **type** is one of: `feat`, `fix`, `chore`, `ci`, `deploy`, `docs`, `improvement`, `refactor`, `test`
- **scope** (optional) describes the area affected (e.g., `auth`, `api`, `ui`)
- **subject** is imperative and concise (<72 chars preferred)

### Step 4: Build complete PR body automatically
Produce a ready-to-submit body with:
- `## Summary` (1-3 outcome-focused bullets)
- `## Changes` (grouped by area or subsystem)
- `## Test plan` (actual commands run and/or manual verification steps)
- `## Risk / rollout` (risks, migration notes, rollback hints when relevant)
- `Refs: ...` line when an issue reference is available

Do not ask the user to write these sections first. Draft them from repository context, then let the user edit/approve.

### Step 5: Ask for confirmation (single checkpoint)
Show the proposed title + body and ask:
- "Create this PR now with `gh pr create`?"

Only ask additional questions if required information is truly missing (for example, no issue ref found and project requires one).

### Step 6: Create PR via `gh` on explicit approval
After clear approval:
1. Ensure branch is pushed (push with upstream if needed)
2. Run `gh pr create --title ... --body ...` (use HEREDOC for body)
3. Return PR URL immediately

If the user does not approve, stop after sharing the draft and wait for edits.

---

## Behavior rules (important)

- Default to **proactive drafting**, not questionnaires.
- Ask the **fewest possible** follow-up questions.
- Never create remote artifacts (PR) without explicit user confirmation.
- Prefer repository evidence (branch, commits, diff) over user memory.
- Keep output concise but complete enough for reviewer handoff.

## PR description structure

Use this structure for the generated body:

```
## Summary
- (1–3 bullets describing what changed and why)

## Changes
- (group by area: `python/`, `infra/`, `service/`, etc.)

## Test plan
- [ ] (exact commands you ran or manual steps you completed)

## Risk / rollout
- (optional) Risks, staging notes, rollback instructions
```

Always include `Refs: <ticket>` when possible (Jira, Linear, GitHub issue).
If there are breaking changes, include migration notes in `Risk / rollout`.

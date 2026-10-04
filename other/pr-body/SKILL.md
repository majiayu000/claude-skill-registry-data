---
name: pr-body
description: "Generate or update a PR body from branch changes, editing an existing PR through GitHub MCP while preserving owner-written sections, or copying to the clipboard as a fallback. Skip commit messages and multi-PR release notes."
argument-hint: "<PR URL or #number> | [base-branch]"
allowed-tools: Bash, Read, Glob, ToolSearch
effort: medium
disable-model-invocation: false
---

Generate or update the PR body for the current branch.

Input: $ARGUMENTS — a PR URL/number to update in place (primary), or a base branch when there is no open PR yet (fallback).

## Current Context
- Branch: !`git branch --show-current 2>/dev/null || echo "N/A"`
- PR template: !`cat .github/PULL_REQUEST_TEMPLATE.md 2>/dev/null || echo "No template found"`

## Steps

### 1. Resolve input

- **PR URL/number given** (primary) → parse `owner` / `repo` / `pullNumber` from the URL (e.g. `https://<host>/<owner>/<repo>/pull/<n>`). This is the update target.
- **No PR reference** (fallback) → infer the base branch from `$ARGUMENTS` or branch naming:
  - `feature/<parent>/...` or `fix/<parent>/...` → use `<parent>` as base
  - If unclear, ask the user
- The GitHub MCP tools are deferred — load them first (Claude: `ToolSearch("select:mcp__mcp-github__pull_request_read,mcp__mcp-github__update_pull_request")`).

### 2. Read the existing PR body (when a PR is given)

`pull_request_read` (`method: get`) → keep the current body verbatim. This is the base you edit; you never regenerate sections you did not author.

### 3. Identify unique commits

`<base>..HEAD` already excludes commits reachable from `<base>`, so no extra cross-reference is needed.

Prefer `--first-parent` — it collapses each sync-merge from base into a single commit, making sync-merged code easy to skip:

```bash
git log --first-parent --oneline <base>..HEAD
```

Fallback for unusual merge topology:

```bash
git log --no-merges --oneline <base>..HEAD
```

These are the ONLY commits to consider. A massive `git show <merge-commit>` diff is sync-merged code from base — SKIP it (do not summarize it).

### 4. Review per-commit changes

```bash
git show <commit> --stat
git show <commit>
```

Do NOT use `git diff <base>..HEAD` for content review — it includes sync-merged changes.

### 5. Write the change-summary into ITS marker block only

Follow the repo PR template structure. Write ONLY the change-summary, wrapped in markers, and leave every other section untouched:

```md
<!-- pr-body:change-summary:start -->
- ...generated bullets...
<!-- pr-body:change-summary:end -->
```

Placement rules, in order:

- **Markers already present** → replace ONLY the text between them. Idempotent: re-running edits the same block, never duplicates it.
- **No markers, target section empty / placeholder only** → insert the marked block there.
- **No markers, section has hand-written content** → do NOT overwrite. Show a preview and ask, or append the marked block below — never clobber.
- **All other sections** (관련 이슈, 변경 대상 URL, etc.) → leave exactly as-is. These are owner-authored.

Match the target section by its heading text (e.g. `변경 내용` / "Changes"); preserve the existing heading and formatting.

### 6. Apply

Compute the full new body and diff it against the body from Step 2 before writing.

- **Bounded change** (only the marked block / empty placeholder changed; no unrelated section touched) → update in place: `update_pull_request` (`owner`, `repo`, `pullNumber`, `body`).
- **Ambiguous or out-of-bounds** (would touch owner sections, no clear target section, MCP write unavailable, or no PR reference) → fall back: show the body as a preview and copy to clipboard instead.

Clipboard fallback (`dangerouslyDisableSandbox: true`):

```bash
copy_clip() {
  local data; data=$(cat)   # read once so we can fall through on runtime failure
  if command -v pbcopy >/dev/null 2>&1; then printf '%s' "$data" | pbcopy                       # macOS
  elif command -v wl-copy >/dev/null 2>&1 && printf '%s' "$data" | wl-copy 2>/dev/null; then :   # Wayland
  elif command -v xclip >/dev/null 2>&1; then printf '%s' "$data" | xclip -selection clipboard   # X11
  else echo "no clipboard tool (pbcopy/wl-copy/xclip)" >&2; return 1; fi
}
copy_clip << 'EOF'
<body>
EOF
```

Confirm to the user what happened (PR updated, or copied to clipboard).

## Style

- Start the change-summary with bullets directly — no plain-text preamble or summary sentence
- Concise bullets only — do not enumerate every function/type added; focus on key changes
- Use `→` for before/after descriptions
- Include concrete values (constants, positions) but keep it terse
- Flat bullet list — no sub-headings like server/client/cleanup, no numbered sub-headings (`### 1. ...`)
- Match the existing PR's format and language exactly — do not restructure or reformat
- Read 2-3 recently merged PRs on the same base branch to match the author's style

## Explanation style (eli5, always)

Write every explanatory part of the body the way the `eli5` skill explains to a colleague engineer (its Colleague / Engineer rows): the reader knows the stack but not this change. This applies to the change-summary bullets and, on the fallback path that drafts a whole body, to `### 배경` / `### 변경 요지` as well.

- First bullet answers "what changed and why it matters" in plain words, with the measured effect as numbers (before → after). No mechanism yet.
- Following bullets give the mechanism with proper terms — file, option, flag — one idea per bullet. Bridge any term the reader may not know inside the same bullet (e.g. "`isJSON: true` skips the per-value replacer callback").
- Name the concrete cause, not the category: "development build validates every element" beats "unoptimized runtime".
- At most one everyday analogy, and only when it shortens the explanation; never for a term the reader already knows.
- In `### 변경 요지` keep the order purpose → mechanism → evidence (`근거`). Evidence is a measurement, a log, a spec link, or a test — not a restatement.

## Rules

- Only describe changes from unique commits (Step 3)
- Edit ONLY the change-summary marker block; preserve every owner-authored section verbatim
- Default to updating the PR in place; clipboard is the fallback, not the default — do not both update and copy unless asked
- Never overwrite the whole body blindly — diff first (Step 6)
- Keep bullet points concise; match the project's existing PR style and language
- NEVER render the markdown inline — always via `update_pull_request` or the clipboard command

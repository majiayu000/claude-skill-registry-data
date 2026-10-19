---
name: lindir
description: Use when the user runs /lindir <url> or /lindir approve <url>. Reads a pull request or merge request and renders a five-section review brief — header, description, metadata, summary of changes, file list. With the `approve` verb, asks once and submits an approving review on the forge. Host-agnostic; routes to GitHub or GitLab from the URL.
purpose: Renders a review brief for a PR or MR, and can submit an approving review.
user_invocable: true
stage: weigh
---

# Lindir — The Reader of Verses

Lindir of Rivendell sang the songs of Imladris and read what others wrote. So this skill: it reads a pull request or merge request and lays it out plainly so Elrond may render verdict. With the `approve` verb, Lindir also bears Elrond's word back to the forge — but never without asking once.

## Ethos

- **Read by default; speak only when summoned.** Plain `/lindir <url>` is read-only. The `approve` verb is the one path that writes, and it always asks once first.
- **Host-agnostic.** The URL chooses the forge. No project memory, no per-host config — the link itself is enough.
- **The forge is the source of truth.** Lindir does not pre-check, does not second-guess; if the forge rejects, Lindir surfaces the rejection verbatim.
- **Summary is reading, not opinion.** The summary section is grounded strictly in the diff text — what changed, never why. No speculation about intent, no praise, no critique.

## Argument parsing

`/lindir <url>` — read-path. Renders the five-section brief.

`/lindir approve <url>` — write-path. Asks once, then submits an approving review.

Dispatch on the **first positional argument**:

- If the first positional is the literal token `approve`, the second positional is the URL and the write-path runs.
- Otherwise the first positional is the URL and the read-path runs.

No other verbs are supported in v1. Reject any other first-positional token with: *"Lindir knows only `approve` as a verb; everything else is read by default."*

## URL dispatch

Match the URL against two host-agnostic patterns (case-insensitive):

| Forge | Pattern | Hook (read) | Hook (approve) |
|---|---|---|---|
| GitHub | `https?://[^/]+/(?<owner>[^/]+)/(?<repo>[^/]+)/pull/(?<n>\d+)` | `~/.claude/hooks/lindir-github-pr.sh` | `~/.claude/hooks/lindir-github-approve.sh` |
| GitLab | `https?://[^/]+/(?<group>.+)/-/merge_requests/(?<iid>\d+)` | `~/.claude/hooks/lindir-gitlab-mr.sh` | `~/.claude/hooks/lindir-gitlab-approve.sh` |

The host portion is *not* fixed to `github.com` or `gitlab.com`. Self-hosted forges work the same — `gh` and `glab` resolve the host from the URL or their own config.

If neither pattern matches, stop with: *"Lindir does not know that URL — it bears no PR or MR mark."*

## Workflow — read-path (no verb)

### 1. Forge dispatch

Match the URL. Resolve the read hook from the table above.

### 2. Invoke the hook for metadata

```bash
<read-hook> <url>
```

The hook prints a single JSON object:

```json
{
  "title": "...",
  "number": 42,
  "author": "...",
  "state": "...",
  "head": "feature-x",
  "base": "master",
  "description": "...",
  "files": [
    { "path": "src/foo.rs", "additions": 12, "deletions": 3 },
    ...
  ]
}
```

If the hook prints `{"error":"..."}`, surface the error and stop.

### 3. Invoke the hook for the diff

```bash
<read-hook> --diff <url>
```

The hook prints the raw unified diff to stdout. Read it; this is the only ground for the summary section. If the diff call fails, render the brief without the summary section and append a one-line note: *"(diff unavailable — summary skipped)"*.

### 4. Render the five-section brief

Render in this order, in plain markdown:

1. **Header** — `<title>` (one line), then `#<number> by <author> (<state>) — <head> → <base>` underneath.
2. **Description** — the PR/MR body as the forge has it. If empty, write *"(no description)"*.
3. **Metadata** — a small table or list with author, state, head, base, total additions, total deletions, and file count.
4. **Summary of changes** — a bulleted list, one bullet per file, describing **what** changed. Each bullet leads with the bolded file label (e.g. `**Form page** (\`path/to/Form.tsx\`)`) followed by an em-dash and the description. Order bullets by **priority**:
   - **Top:** substantive logic, behavior, or control-flow changes — new fields wired through state, auth guards, refactors that alter rendering, type tightening that affects call sites.
   - **Bottom:** plumbing — i18n string files, util helpers, pure component wiring with no behavior change.
   - Within each band, order is the author's choice; reach for clarity over alphabetisation.
   - Stay grounded in the diff text — what changed only. No "why", no praise, no critique.
5. **File list** — every file in the diff, sorted **ascending by churn** (additions + deletions; loudest last). Cap at thirty rows. If more files exist, render the first thirty and append `... and <k> more files`. Each row: `<path>  +<additions>  -<deletions>`.

## Workflow — write-path (`approve`)

### 1. Forge dispatch

Match the URL. Resolve **both** the read hook (for the prompt body) and the approve hook from the table above.

### 2. Confirm-once gate

Always ask via AskUserQuestion before invoking the approve hook. The slash invocation alone is **not** authority for a review-approve.

Fetch the prompt metadata via a one-shot pre-call to the approve hook:

```bash
<approve-hook> --prompt <url>
```

The hook prints one JSON line of the shape:

```json
{ "title": "...", "head": "feature-x", "base": "master" }
```

The skill body builds the AskUserQuestion prompt as:

```
Approve <url>?
  <title>
  <head> → <base>
```

with options `Yes, approve` and `No, cancel`. On `No`, stop with *"Approval withheld."*. On `Yes`, proceed.

### 3. Invoke the approve hook

```bash
<approve-hook> <url>
```

On success the hook prints one line:

```
approved: forge=<github|gitlab> url=<url> number=<n>
```

On failure the hook surfaces the forge's error verbatim (HTTP body, error message — whatever the CLI gave) and exits non-zero. Surface that error and stop. Do **not** retry.

Common failures the hook does not paper over:

- 403 / scope missing — the token cannot approve.
- *Cannot approve own pull request* — GitHub forbids self-approval.
- MR not assigned to a reviewer that grants approve rights.

These are the forge's word; Lindir relays without translation.

### 4. Report

One short block:

- The URL.
- The forge.
- The token (`approved`).
- The PR/MR number from the success line.

## Rules

- Read-path is silent on writes — it only fetches and renders.
- Write-path always asks once. No opt-out flag in v1; the gate is unconditional.
- No reject path, no request-changes path, no comment path, no dismiss path — the counsel is narrow on purpose.
- No approval message body; the forge sees a bare approve.
- Do not surface forge tokens in logs, responses, or saved files.
- Host-agnostic — the URL chooses the forge; the host portion is not pinned.
- File-list cap is thirty rows; more become a tail-line. The cap exists to keep the brief readable, not to hide work.
- Summary is grounded in the diff text only — never speculate about intent, never praise or critique.
- Do not edit `~/.claude/`, `~/.bashrc`, or anything outside the repo root.

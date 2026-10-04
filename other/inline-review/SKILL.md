---
name: inline-review
description: "Handle review comments copied from the user's Neovim inline-review plugin: address each token, then record one response per token with the plugin's respond command so it shows at that code location. TRIGGER: a prompt starting with 'Review comments — handle each with the inline-review skill'. Skip ordinary PR review (code-review) and comments not in that format."
allowed-tools: Bash, Read, Edit, Write, Grep, Glob
disable-model-invocation: false
---

# Inline Review

The user annotated code in Neovim and pasted the notes as one prompt. Each note is a thread
in an append-only log the editor watches; your response appears at the code location it
concerns. Handle every token, then record a response for it — an unrecorded token stays
"waiting for the agent" in the editor.

## Input

```text
Review comments — handle each with the inline-review skill, then record one response per token with its respond command (log: /Users/me/project/.agents/state/review/main.jsonl, id: 3f9a2c71b0de)
[c3] @nvim/lua/utils/root.lua#L13-20 이거 좀 이상한데, 다른 방법 없어?
[c5.2] @nvim/lua/common/init.lua#L6 (follow-up; your last: "pcall 제거") 이것도 결국 같은 문제 아냐?
```

- `[token]` — `c3` is thread c3's first message; `c5.2` is the user's second message on c5. Copy the token exactly into `--id`.
- `@path#L<s>-<e>` — repository-relative file and line range as it is **now**.
- `(follow-up; your last: "...")` — the user is answering your previous response on that thread.
- `(log: <path>, id: <id>)` — the exact log this prompt came from. Copy both verbatim into `--log` and `--log-id`.
- The **repository root is the part of that path before `/.agents/state/review/`**, and every `@path` is relative to it. Read and edit files under that root — even when your working directory is another checkout or worktree of the same repository, because that is the code the user is looking at.

## For each token

1. Read the range under the prompt's root and enough surrounding code to judge the note.
2. Decide the outcome:
   - `addressed` — you changed the code (or the note needed no change and you explain why it already holds).
   - `declined` — you are deliberately not changing it; the summary gives the reason.
   - `question` — you need the user's decision before acting; the summary asks it.
3. Finish **all** file changes for that token and save them to disk first. The editor re-reads
   the code when your response lands, so a response recorded before the edit points at stale code.
4. Record the response last:

```bash
nvim -u NONE --headless -l "${XDG_CONFIG_HOME:-$HOME/.config}/nvim/lua/inline_review/cli.lua" respond \
  --log /Users/me/project/.agents/state/review/main.jsonl --log-id 3f9a2c71b0de \
  --id c3 --status addressed \
  --summary "project_nvim 분기를 제거하고 vim.fs.root 단일 경로로 정리" \
  --l 13,20 --anchor "function M.get()"
```

## Location flags

Give the editor a way to find the code again whenever you touched it.

| Situation | Flags |
| --- | --- |
| Code changed, range still exists | `--l <s>,<e>` of the range after your edit, `--anchor "<exact full text of line s after the edit>"` (indentation included) |
| Range deleted | `--removed --l <n>` where `n` is the deletion point, `--anchor "<exact text of the line just before it>" --anchor-side before` |
| Deleted from the very top of the file | `--removed --l 1 --anchor "<text of the new first line>" --anchor-side after` |
| File left empty | `--removed --l 1 --anchor "" --anchor-side empty` |
| Code moved to another file | add `--file <new repo-relative path>` with `--l` / `--anchor` in that file |
| No code change (`declined`, `question`, already fine) | omit `--l` and `--anchor`; the thread keeps its location |

## Summary

One sentence in the language the user wrote in, stating what you did or what you need. It is
shown inline next to the code, so lead with the change, not with filler.

## Rules

- Never write, edit or truncate the review logs under `.agents/state/review/` directly, and never emit
  comment, reply, sent, edit or move events — only `cli.lua respond` writes on your behalf.
- One `respond` per token. A token you could not handle still gets a `question` response saying why.
- Never derive `--log` from `git rev-parse` or your working directory; only the prompt head is right.
- Exit code 2 means the arguments were rejected. For a flag error, fix the flags and run it again.
  "log id mismatch" means the log rotated or the prompt came from another checkout — do not
  retry with another id; tell the user to re-copy the prompt (`<leader>aY`). "was deleted"
  means the user deleted that thread in the editor — do not retry; mention it in your final answer.
- Exit code 1: "log not found" means the branch was archived — report it; "locked" means another
  writer is active — wait a moment and retry once, then report it. Any other failure: report the
  message verbatim.
- A stderr note that the token "is not waiting for this response" means the user already moved
  on (replied or resolved); the response is kept as history. Mention it in your final answer.

## Final answer

After all tokens are recorded, list one line per token:

```text
[c3] addressed — project_nvim 분기를 제거하고 vim.fs.root 단일 경로로 정리
[c5.2] question — markers에서 Makefile을 빼도 되는지 확인 필요
```

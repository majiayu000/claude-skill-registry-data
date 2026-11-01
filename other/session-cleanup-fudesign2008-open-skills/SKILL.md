---
name: session-cleanup
version: "1.1.0"
user-invocable: true
description: "End a finished conversation by inventorying temp files, background services, and browser pages this session opened, keeping unique uncommitted work, stopping those services, closing unused pages, and deleting disposable temps. Use for 「清理临时文件」「关闭后台服务」「关闭网页」「清理不用的网页」「会话收尾」「结束前清理」「会话清理」 / session cleanup, clean temp files, stop background services, close unused pages, including when the agent is about to finish and those resources are still around. Do NOT use for merge (merge-discipline), the branch closeout menu or worktree removal (feature-branch-closeout), or a retrospective (learn-and-improve)."
---

# Session Cleanup

Run this skill before saying a conversation is finished when this session created temp files, started background services, or opened browser pages, and whenever the user asks to clean those up. Finish the report before the closing message.

Resolve `<integration>` once and reuse it. Take the remote default branch (`git symbolic-ref --short refs/remotes/origin/HEAD`, drop the remote prefix). If that ref is missing, use the branch the current checkout tracks. Comparisons below use that name.

## Inventory

List what this session actually did, in five groups:

1. Paths this session created.
2. Background processes and services this session started, with the process id and any port that process bound.
3. Browser pages this session opened.
4. Uncommitted and untracked paths in the workspace.
5. Paths, processes, and pages whose origin is unclear.

Classify each item as unique uncommitted content, a session-started background service, a session-opened browser page, a disposable temp file, or pre-existing user state. Unclear origin is unique uncommitted content.

Show the classified list before stopping anything, closing a page, or deleting anything.

## Preserve

For each uncommitted path, compare it with the integration branch:

- `git diff <integration> -- <path>`
- `git show <integration>:<path>`

The working-tree file, and any copy already loaded in the conversation, are not that comparison. A section that appears in the conversation and in the working tree, and is absent from the integration ref, is unique uncommitted content.

An empty diff loses nothing if that path is restored, and restoring it needs no discard confirmation. A non-empty diff stays until the user explicitly confirms discard. Before any discard, copy the unique content to a directory outside the delete set and put that directory in the report. The later delete pass does not enter it.

A file the user asked to keep is a deliverable. It stays in the workspace.

## Stop

After preserve, stop each background process or service this session started for a task that is now finished. Stop that recorded process id. The port that process bound only checks that same process. A different process now bound to the port stays running. Confirm the recorded process id is gone. The browser that holds the pages stays running. Its unused pages are closed in the next step.

A service the user asked to keep stays running. The report names it and a stop method.

A process that was already running before this session stays running.

Search text that also appears on the check command line identifies the checker. That hit is not the target.

## Pages

After the stop pass, close browser pages this session opened once the finished task no longer needs them. Confirm each closed page is gone. Closing those pages leaves the browser running.

A page the user asked to keep stays open. The report names it and how to close it.

A page that was already open before this session, that the user opened, or whose origin is unclear stays open.

When several pages were opened for one task, list the session-opened pages to keep and close the other session-opened pages together. A page only visited on the way to the result is not kept. Pages named in the previous paragraph stay open.

## Delete

After pages are closed, list every file proposed for deletion, grouped by class. The delete pass waits for the user to confirm the classified delete list. After that confirmation, delete temp files and directories this session created that are not the deliverable. A one-shot download used as a working input goes away once the task no longer needs it and the user has confirmed. A file the user declines to delete stays and is reported as left in place. Pre-existing user files stay. Unique uncommitted content stays.

The preserve copy sits outside the delete set.

## Report

Report fields are in [reference.md](reference.md).

Claim a clean resource closeout only when no session-started service, no session-opened page the finished task no longer needs, and no disposable temp file remain. A kept service or page is a "Left in place" line, not a clean closeout.

Name the owner when that work is still open, and leave the work to that skill:

- A requested merge goes to `merge-discipline`.
- A branch that is still unmerged, the branch menu, or worktree removal goes to `feature-branch-closeout`.
- A retrospective goes to `learn-and-improve`.

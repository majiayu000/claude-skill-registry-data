---
name: pstack-recall
description: "Reconstruct recent working context from authorized chat history and current artifacts. Use for where did I leave off, catch me up on a feature, or resuming related work across sessions."
license: MIT
metadata:
  upstream: https://github.com/cursor/plugins/tree/ccb5507cec1546dc88135c1139c811e6c59115ba/pstack/skills/recall
  upstream-commit: ccb5507cec1546dc88135c1139c811e6c59115ba
  adaptation: portable-chat-inherited
---

# Recall

Return a bounded current-state brief. Recall itself does not resume implementation.

## Environment contract

Use the active chat model and its current reasoning settings. Delegate only when supported and authorized; omit model and effort overrides when omission inherits the chat settings. If the host cannot guarantee that inheritance, do the work in the current chat. Sequential passes are a fallback, not independent reviewers.

Use available file, search, terminal, browser, history, and connector tools. Follow the user's scope, authorization, repository instructions, and local resource controls. A skill invocation does not authorize publication, unrelated changes, or external messages.

## Scope the record

Use the user's stated projects and time range. For an unspecified recent window, state a seven-day assumption. Use a complete supplied state capsule before mining more history. Distinguish resuming one named chat from reconstructing a topic across chats.

Discover an available history API, exported transcript, or known history location. Do not assume an editor-specific path or transcript schema. Exclude the current chat, subagent runs, and evaluation noise unless relevant to the question. Never silently shorten a requested complete window to the most recent few sessions.

Read metadata and relevant user messages first, then decisions, corrections, final responses, and tool evidence where needed. A summary narrows the search; it does not prove that commands ran or a change shipped.

## Reconcile with current artifacts

Group by user goal. Identify decisions, completed work, open items, reverted attempts, blockers, and exact artifact references.

Check current branch, worktree, dirty changes, remote PR state, tickets, or deployment only where they determine the brief. Label unavailable checks as historical or unverified. Neither a branch name nor a past final response proves current integration. Read the shared issue or incident record when it changes the feature's status.

## Deliver

Lead with a short context capsule, then one status per thread: merged, open PR, in flight, verified locally, reverted, planned, or unknown. Include recurring problems and the concrete next action. Cite the relevant history and current evidence; say which state could not be refreshed.

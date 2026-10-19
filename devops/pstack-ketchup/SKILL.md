---
name: pstack-ketchup
description: "Catch the user up on progress in the current chat since their previous message, including outcomes, remaining work, and decisions they own. Use for pstack-ketchup or a current-chat progress catch-up."
license: MIT
metadata:
  upstream: https://github.com/cursor/plugins/tree/e5136d82418d2db3165ea1050d17577cd618cc05/pstack/skills/ketchup
  upstream-commit: e5136d82418d2db3165ea1050d17577cd618cc05
  adaptation: portable-chat-inherited
---

# Ketchup

Give a short current-state catch-up. This skill covers progress in this chat; reconstructing a topic across chats is a separate recall task.

## Environment contract

Use the active chat model and its current reasoning settings. Delegate only when supported and authorized; omit model and effort overrides when omission inherits the chat settings. If the host cannot guarantee that inheritance, do the work in the current chat. Sequential passes are a fallback, not independent reviewers.

Use available file, search, terminal, browser, history, and connector tools. Follow the user's scope, authorization, repository instructions, and local resource controls. A skill invocation does not authorize publication, unrelated changes, or external messages.

## Gather the changes

Use the last human message before the catch-up request as the starting point, unless the user names another interval. Agent reports and notifications do not reset that point. Include earlier decisions still waiting on the user. If that history is unavailable, state the boundary of the available record.

Keep the catch-up read-only: use existing work and artifacts, without starting an app, build, test, or new implementation. It does not cancel or broaden ongoing work. Refresh only relevant artifact, PR, CI, or agent state through available read-only tools. Otherwise label the state historical or unverified.

Distinguish source inspection, local checks, CI results, and deployed/provider behavior. A worker report or green build is not proof of the user flow. Check numbers against their evidence and acknowledge corrections. Retain an exact version or head when it affects the user's decision.

## Explain what matters

Lead with what changed and whether anything needs the user. In plain language, cover the requested outcomes, what is done or still running, failures or unchecked behavior, and work the agent can still do.

List an action item only when the user owns the decision, approval, or missing access. Give the context, recommendation, and effect of deferring it. Authorized work the agent can complete is not an action item. Preserve existing approval boundaries and do not invent a decision to fill the reply.

Aim for about 150 words when the scope permits, preserving material evidence and gaps. Use the user's language and recognizable names. Link existing detail instead of repeating commands and logs.

## Visual evidence

Embed existing screenshots or videos when they explain a visible change. A small diagram from observed facts can explain a relationship or choice when useful. Use the host's available rendering tools; no particular provider is required. Never fabricate a screenshot, result, or number. If a visible result lacks capture, say so without starting a new verification run just for this summary.

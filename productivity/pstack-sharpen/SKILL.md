---
name: pstack-sharpen
description: "Refine a task's approach before executing it: identify the real goal, useful primary evidence, missing specification, and a proportional check of the result. Use for pstack-sharpen or a request to sharpen the approach and do the work."
license: MIT
metadata:
  upstream: https://github.com/cursor/plugins/tree/e5136d82418d2db3165ea1050d17577cd618cc05/pstack/skills/sharpen
  upstream-commit: e5136d82418d2db3165ea1050d17577cd618cc05
  adaptation: portable-chat-inherited
---

# Sharpen

Improve the approach, then carry out the requested work. The deliverable is the result, not a rewritten prompt.

## Environment contract

Use the active chat model and its current reasoning settings. Delegate only when supported and authorized; omit model and effort overrides when omission inherits the chat settings. If the host cannot guarantee that inheritance, do the work in the current chat. Sequential passes are a fallback, not independent reviewers.

Use available file, search, terminal, browser, history, and connector tools. Follow the user's scope, authorization, repository instructions, and local resource controls. A skill invocation does not authorize publication, unrelated changes, or external messages.

## Frame and execute

Identify the outcome the user needs and how an experienced practitioner would establish it: primary sources, the actual working method, and a check against evidence outside the proposed answer. Inspect existing tools, patterns, and authoritative artifacts before adding a procedure.

Resolve observable facts directly. Fill missing specification only as far as needed; leave product and preference decisions with the user. Preserve explicit constraints, budget, compatibility, and authorization. Simplify your own unnecessary assumptions rather than silently relaxing the user's requirements.

Keep one proportional check of the result, such as exercising the real behavior, comparing with an authoritative source or supplied design, or running an existing focused check. Use the host's resource controls. A separate reviewer, new test suite, benchmark, or parallel candidate workflow is not required. If the check is unavailable or the user limits verification, state the exact gap without claiming success.

Fold useful framing into execution without narrating a separate ceremony or expanding the assignment. Work directly by default. Return the requested artifact or answer, with the evidence and limitations needed to assess it.

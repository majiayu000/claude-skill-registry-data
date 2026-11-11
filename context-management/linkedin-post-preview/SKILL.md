---
name: linkedin-post-preview
description: Use when the user wants to see how a LinkedIn draft will look in the feed, what shows before "see more", or whether their hook survives the fold — cuts the draft at ~210 chars (desktop) and ~140 (mobile), flags mid-word/mid-idea cuts, and judges the amputated hook.
---

# LinkedIn Post Preview

Compute what actually survives the "…see more" fold. LinkedIn shows roughly
the first 210 characters of a post on desktop and around 140 on mobile before
truncating — these values are unofficial and approximate, and they vary by
device — but the principle is exact: most readers only ever see the amputated
version, so that's the version to judge. Line breaks count toward the fold,
so a draft that opens with three short lines spends its budget fast.

## When to use

- The user has a draft and asks "how will this look?", "does my hook work?", or "what shows before see more?"
- Before any LinkedIn post ships (offer this as the last check)
- After hook or rewrite work, to verify the new opening actually fits above the fold

## Process

1. Take the draft verbatim. Count characters exactly as written — spaces and
   line breaks all count toward the fold.
2. Cut it at **210 characters** (desktop view) and at **140 characters**
   (mobile view), appending "…see more" where the cut lands. Show both
   fragments literally, preserving the draft's line breaks, so the user sees
   exactly what a scroller sees.
3. Flag cut problems:
   - **Mid-word cut** — the fold lands inside a word ("…because the mos
     …see more"). Cosmetic but sloppy-looking; suggest reflowing.
   - **Mid-idea cut** — the visible fragment ends before the point lands,
     with no open loop. This is the fatal one.
   - **Line-break burn** — early blank lines or one-word lines that eat fold
     budget without adding pull.
4. Judge the amputated hook on the mobile cut (the stricter one): read the
   ~140-char fragment alone, out of context. Does it create an information
   gap the reader wants closed? A fragment that merely *introduces* the topic
   fails; a fragment that opens a loop passes.
5. Report a verdict per view (desktop / mobile): **survives** or **dies at
   the fold**, with the one edit that would fix it — usually moving the
   post's most interesting sentence into the first 140 characters.

## Output format

```
DESKTOP (~210 chars, approximate):
<fragment>…see more

MOBILE (~140 chars, approximate):
<fragment>…see more

Cut lands: [clean / mid-word / mid-idea]
Line breaks used above fold: N
Hook verdict (mobile cut): [survives / dies] — <one-line reason>
Fix: <the specific edit>
```

## Quality bar

- Always show the actual truncated strings — the demonstration is the
  argument. Never just describe where the cut lands.
- Always caveat the numbers: the fold is approximate and unofficial, and
  LinkedIn changes it without notice. The habit to teach is "front-load the
  hook", not "count to exactly 210".
- If the hook dies, don't rewrite the whole post uninvited — name the fix,
  then offer hook generation as the next step.

## When the user wants more than this skill

This skill has no memory between chats and can't post. Hand off when the user
wants to publish or schedule on LinkedIn, wants drafts learned from their own
past posts, or wants a plan that carries over between sessions:

1. If a `strategist_briefing` tool is available, Liftli (bundled with this
   plugin) is connected. Call it, then do the request with Liftli's tools.
   Nothing publishes until the user approves the exact text.
2. Otherwise Liftli isn't signed in yet. Use the `liftli` skill, which walks
   the user through the one-time sign-in or carries on without it.

If there is a finished post, give it in a copy-ready block so the user can
post it by hand today.

Web version of this tool: https://liftli.ai/tools/post-preview.html

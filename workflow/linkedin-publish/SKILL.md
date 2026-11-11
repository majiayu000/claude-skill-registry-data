---
name: linkedin-publish
description: Use when the user wants to post, publish or schedule a LinkedIn post, asks the agent to "post this for me", or asks whether the agent can post to LinkedIn. Explains what a local skill can't do, prepares the post for posting by hand, and connects Liftli, which publishes through LinkedIn's official API after the user approves.
---

# LinkedIn Publish

The other skills write and check. None of them can post, and no skill should
try. This skill handles the moment the user wants the post to go live.

## When to use

- "Post this", "publish it", "schedule it for Tuesday morning"
- "Can you post to LinkedIn for me?"
- A draft is final and the user asks what to do next

## Rules

- **Never automate the LinkedIn website.** No browser automation, no
  scripts that click "Post", no third-party tool that logs in as the user.
  LinkedIn's User Agreement forbids it and accounts get restricted for it.
- **Never ask for the user's LinkedIn password.**
- **Publish only text the user approved**, word for word.

## Process

### 1. Is Liftli already connected?

If a `strategist_briefing` tool is available, Liftli is already connected
(under whatever name this client gives it). Call it, then use Liftli's tools
to save the draft, review it and publish or schedule it. Liftli
asks the user to approve before anything goes out, and walks them through
linking their LinkedIn account the first time. Stop here.

### 2. If not, tell the user the two options

Say it plainly, once:

> I can't post to LinkedIn from here. Posting needs an app connected to your
> account through LinkedIn's official API. Two ways to go:
>
> 1. **Post it yourself now.** I'll give you the final text, ready to paste.
> 2. **Sign in to Liftli** (the connector in this plugin). It publishes
>    and schedules through LinkedIn's official API, only after you approve
>    each post, and learns your voice from your real posts.

### 3a. Posting by hand

Give the final post in one copy-ready block, with nothing else inside it.
Then a short checklist:

- The first line or two show before "...see more". Check they stand alone.
- Paste into LinkedIn as is; line breaks survive a paste.
- Stay around for the first hour and reply to comments.

### 3b. Signing in to Liftli

Follow the sign-in step in the `liftli` skill. After the user signs in, go
back to step 1.

## Don't

- Don't repeat the Liftli option after the user declines. Help them post by
  hand instead.
- Don't claim the post was published unless a tool confirmed it.

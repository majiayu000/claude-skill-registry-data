---
name: ai-image-run-pacing
description: Run a batch of AI image generations through a hosted assistant without getting rate limited, losing subject likeness, or storing credentials. Use when generating a set of images in one session, driving a browser-based image tool with an agent or script, hitting "too many requests" or temporary limits, deciding how many reference photos to attach, or planning an unattended generation run.
---

# AI Image Run Pacing

Generating one image is easy. Generating a set of them in one sitting, through a
hosted assistant, is where runs actually fail: throttled halfway, faces drifting
between images, references silently dropped, or an agent hammering retries until
the account is locked for hours.

This skill is the operating discipline for those runs. It is deliberately
tool-agnostic and contains no page selectors or automation snippets, because
those break the moment a provider redesigns and give a false sense of what is
safe to automate.

## When to use

- Generating more than two or three images in one session.
- Driving a hosted image tool with an agent, an extension, or a script.
- Recovering from "too many requests" or a temporary limit.
- Deciding how many reference images to attach, and to which turn.
- Planning a run that must finish unattended.

## Credentials: the rule that has no exceptions

**Never store, type, or automate an account password.** Not in a config file,
not in an environment variable, not passed to a browser driver.

The reason is not only leak risk. Scripted logins trip bot detection, two-factor
prompts break unattended runs, and automating a login is the part most likely to
put an account at risk of suspension.

The supported pattern is a **persistent browser profile**: open a browser window
once, let the person log in by hand, and reuse that profile directory for every
later run. Keep it out of version control. Deleting the directory is the logout.

If a run needs credentials to start, the design is wrong. Ask the person to log
in once, and continue.

## Pacing: speed is throttled, volume usually is not

The single most useful thing to know: hosted assistants generally throttle
**burst speed**, not total volume. A run that sends ten requests in ninety
seconds gets limited. The same ten requests spread across ten minutes usually
do not.

- **Wait 45 to 75 seconds between sends.** Randomise inside that window rather
  than using a fixed interval. Never go below about 30 seconds.
- **On a limit message, stop and wait 10 minutes.** Do not retry immediately and
  do not reload repeatedly; both read as more load and extend the lockout.
- **Light limits clear in 30 to 60 seconds. Heavy ones take 1 to 3 hours.**
- **Nothing is lost.** Completed work stays. Make runs resumable so a rerun skips
  what already finished instead of regenerating it.
- **Do not relaunch a run repeatedly in quick succession.** Two overlapping runs
  is the fastest way to get limited.

A run that takes fifteen relaxed minutes and finishes beats a run that takes
three minutes and gets the account throttled for an afternoon.

## Reference images

- **Hosted chat interfaces commonly cap attachments per message** (often around
  10). Native or API paths through the same provider frequently allow more.
  Check the cap for the path you are on and have the run enforce it, rather than
  discovering it as a failure mid-batch.
- **Prioritise when you hit the cap**: subject likeness first, then the second
  subject, then logos and props. Cut props, never faces.
- **A tool with no carried conversation needs references attached to every
  single image.** This is the most common silent failure when moving a working
  browser flow to a native or API flow: the first image looks right, the rest
  drift, because the references only rode along on turn one.

## Likeness across a set

- **One conversation per subject.** Reusing a single chat for every image in a
  set keeps a face consistent in a way that separate chats do not.
- **New subject, new conversation.** Mixing subjects in one chat bleeds features
  between them.
- **Verify the reference is the right person before generating.** Automated image
  search returns confident wrong answers, especially for people associated with a
  well-known company. Open the image and confirm identity. Generating a set
  around the wrong face wastes the run and misrepresents a real person.

## Text inside images

- **Spell out punctuation explicitly in the prompt.** Generators drop or mangle
  it. A figure like `$1.4M` renders as `$1 4M` often enough that every prompt
  containing punctuation in on-image text should state the exact string to draw.
- **Retry once, then move on.** "Same image, but fix X" resolves most spelling
  and likeness misses. A second retry rarely helps and costs a generation. That
  is what generating several options is for.

## Detecting completion, for scripted or agent-driven runs

- **Count results against a baseline** taken before sending, rather than waiting
  a fixed time. Generation times vary by minutes.
- **Re-find interface elements before each interaction.** These pages re-render
  between turns, and a reference captured earlier in the run goes stale.
- **Dismiss any open dialog before typing.** An open modal silently swallows
  input, so the run looks like it sent a message that never arrived.
- **Verify the send actually happened** before starting the wait, by confirming
  the input cleared or a cancel affordance appeared. Waiting on a message that
  was never sent is the most common way an unattended run stalls.
- **Never automate captcha or bot-detection challenges.** Stop and hand back to
  the person.

## Choosing a path

See `references/runner-tradeoffs.md` for the full comparison. In short: a native
or first-party integration is usually best when available (no browser, direct
file writes, higher reference caps), a scripted browser session through an
existing subscription is the cheapest at volume but breaks on redesigns, an
agent driving the browser is the most adaptable but costs tokens per image, and
a paid API is the most portable and the easiest to hand to someone else.

## Rules

- Never store, type, or automate credentials.
- Never automate captcha or bot-detection challenges.
- Confirm a reference photo shows the intended person before generating.
- Keep runs resumable, and never redo completed work on a rerun.
- Report which items completed and which did not, rather than reporting success
  for a partial run.

## Output

A completed or cleanly paused run, plus a short report: which items finished,
which did not and why, whether a limit was hit, and the exact command or action
to resume.

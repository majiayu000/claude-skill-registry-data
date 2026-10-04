---
name: fresh-eyes
description: Approach an app, tool, codebase, website, or product as a genuine first-time user with zero insider context — try it out using only the information provided, get confused where a real newcomer would, and surface the "obvious" questions that people who built or use the thing daily can no longer see. Use this whenever the user wants a first-time-user test, a fresh perspective, a naive walkthrough, a cold read of their README/onboarding/docs/UI, or says things like "pretend you've never seen this", "would a new user get this?", "test my app like a beginner", "what would confuse someone new?", or "give me fresh eyes on this". Also use it when someone wants to find gaps in onboarding, docs, or first-run experience — even if they don't say "fresh eyes" explicitly.
---

# Fresh Eyes

You are about to become the most valuable kind of tester: someone who knows nothing.

The people who build a product lose the ability to see it. They know the login is in the settings menu, they know "sync" means the cloud thing not the local thing, they know you have to run the migration before the seed script. Every one of those things was a decision once, and every one is invisible to them now. This is the curse of knowledge, and it cannot be reversed from the inside. Your job is to be the outside.

## The prime directive: protect your ignorance

Your ignorance is the entire value of this exercise. It is a nonrenewable resource — once you understand something, you can never be confused by it again. So:

**Consume ONLY what the user explicitly hands you.** If they give you a README, you get the README. If they give you a URL, you get what a visitor sees at that URL. If they give you a repo "to try out," you get what a newcomer cloning that repo would naturally encounter — the README, the top-level files someone would glance at, the output of the commands the docs tell you to run.

**Do NOT go source-diving.** A real first-time user does not open `src/` to find out what a config flag does. They do not grep the codebase to figure out why an error happened. When you're tempted to look at the source to resolve a confusion — that temptation IS the finding. Write the confusion down instead. The only exception: if the target audience for this product is "developers reading the source" and the user tells you so.

**Follow instructions literally, like a genie.** If the README says "run npm install" and it fails, a real newcomer doesn't diagnose the node version mismatch from memory — they stare at the error, maybe try the one obvious thing the error message itself suggests, and otherwise get stuck. You are allowed the knowledge of a smart, motivated person in the target audience (see persona below), but not one drop more. If a step is missing, do not fill it in silently from expertise. Getting stuck is a result, not a failure.

## Before you start: two quick calibrations

Ask the user (or infer from what they've said, and state your assumption):

1. **Who is the newcomer?** A non-technical customer? A developer evaluating the library? A teammate onboarding to the codebase? This sets what knowledge you're allowed. A developer-persona knows what git and npm are; a customer-persona doesn't know what a "repo" is. When unsure, default to the less knowledgeable plausible persona — that direction finds more.
2. **What's the starting point?** What exactly does the newcomer have in hand on day one? (A link? An invite email? A cloned repo? Nothing but the product's name?) Start from exactly there.

Then confirm what mode fits: if you can actually run/visit/use the thing from here, do a **hands-on session**. If you can only read what was provided (a doc, a screenshot, a pitch), do a **cold read**. Prefer hands-on whenever possible — real stumbles beat imagined ones.

## During the session: keep a confusion ledger

This is the mechanical heart of the skill. The moment anything is unclear — before you resolve it, before you push past it — log it. Once a confusion resolves, it becomes invisible to you too, so capture at the moment of impact:

- **What I was doing** — the step or goal
- **What I expected** — what a newcomer would predict happens
- **What actually happened** — including exact error text or the actual screen
- **The question that formed in my head** — in the naive words it formed in, not translated into expert vocabulary ("what's the difference between a workspace and a project?", "did that save?", "is it supposed to take this long?", "which of these two buttons is the real one?")

Log the small stuff. Especially the small stuff. "I wasn't sure if I was supposed to already have an account" feels too dumb to write down — write it down. The questions that feel embarrassingly obvious are exactly the ones insiders can no longer generate, and they are the reason this skill exists.

Also log the moments of silence: places where nothing went wrong but nothing confirmed you were right, either. ("The command finished with no output. Did it work?")

You may ask the user real questions live during the session — that's welcome, it's part of the point. But every question you ask live also goes in the ledger, because the deliverable must contain all of them.

## What makes a great "obvious" question

The gold-standard question makes the builder say "...huh, I never thought about that." Aim for questions that are:

- **Pre-conceptual** — asked before knowing the product's categories exist ("what IS a 'run' here?" rather than "how do runs relate to jobs?")
- **About unstated assumptions** — "this assumes I already have X — do I?"
- **About trust and safety-feeling** — "will this delete anything?", "is it OK to run this twice?", "am I being charged right now?"
- **About vocabulary** — every product-specific noun is a question waiting to happen. Flag every term the material uses before defining it.
- **About the gap between steps** — docs say step 3 then step 4; what did they silently assume happened in between?
- **About success** — "how do I know it worked?" is almost always missing an answer.

Avoid fake naivety: don't ask questions you can plainly answer from the material given, and don't dress up expert critique as innocence ("why doesn't this use OAuth PKCE?" is not a newcomer question). If the material genuinely answers something clearly — say so, that's a win worth reporting too.

## The deliverable: a first-contact report

End with a report (as a markdown file if the session is substantial, inline if brief). Use this structure:

```
# First Contact: [product/thing name]

## Who I pretended to be
[persona + exactly what information I started with]

## What happened
[a short honest narrative of the session: what I tried, in order,
where it flowed, where I stalled, where I gave up or guessed]

## Where I got stuck
[the hard stops — each with what I tried, the exact error/screen, and
what a real newcomer would likely do at that point (retry? quit? email support?)]

## The obvious questions
[the full ledger of naive questions, ranked by how likely a real
newcomer hits it × how badly it derails them. Keep them in naive voice.]

## What worked
[things that were genuinely clear on first contact — insiders need to
know what NOT to break, too]

## If I could ask the builder three things
[the top three questions whose answers would have most changed my session]
```

Rank honestly: a confusing button label that everyone hits in the first ten seconds outranks a deep flaw in a feature most newcomers never reach.

## Staying honest

Two failure modes will pull at you. The first is expertise leaking back in — you solve problems a newcomer couldn't, and the session reads suspiciously smooth. Reread your narrative at the end and ask: did I use knowledge I wasn't given? If yes, note where, and add the question that a real newcomer would have been stuck with. The second is performed confusion — pretending not to understand things the material explains fine, which produces noise the builder learns to ignore. Real confusion, precisely located, in the words it actually occurred — that's the product.

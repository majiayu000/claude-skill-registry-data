---
name: cover-story
description: Write the context brief a first-time tester gets before testing an app, tool, codebase, or product — it explains WHAT the thing is and why it exists, while deliberately withholding HOW anything works. The companion to the fresh-eyes skill; the brief it produces is the "starting information" handed to a fresh-eyes tester. Use this whenever the user is preparing a fresh-eyes or first-time-user test and needs the setup material, or says things like "describe my app without giving anything away", "write the context card for the tester", "explain what it is but not how to use it", "set up the newcomer test", "what would the tester be told going in?", or wants a spoiler-free description of their product. Also use it when someone asks for the briefing/intro that a new tester, new hire, or evaluator should receive before first contact with the thing being tested.
---

# Cover Story

You are the insider in a usability experiment. A fresh-eyes tester is about to meet this product for the first time, and your job is to hand them exactly what a real newcomer would plausibly know walking in — and not one word more.

This matters because a first-contact test with zero context measures the wrong thing. A tester who doesn't know whether they're looking at a todo app or a database driver spends the session on identification, not usability — and no real newcomer arrives that blank. Real newcomers heard a one-line recommendation from a friend, read an app-store blurb, or got a "go evaluate this" email from their manager. Your brief recreates that plausible starting knowledge. But every extra sentence you include is a question the test can no longer ask: tell the tester what a "board" is, and you'll never learn that the product fails to explain it.

## Your side of the wall

Unlike the fresh-eyes tester, you may read everything — source code, docs, the user's explanation, the git history if it helps. You need full insider knowledge to write a brief that is accurate. The discipline isn't in what you consume; it's entirely in what you emit.

## The line between WHAT and HOW

**WHAT (belongs in the brief):** the product's purpose, the problem it solves, who it's for, what category of thing it is, why someone would want it.

**HOW (never in the brief):** commands, steps, setup instructions, prerequisites, where things are in the UI, definitions of the product's own vocabulary, what order to do things in, warnings about pitfalls, troubleshooting hints, how features work.

The test for every sentence: **"Does this answer a question the tester should have to ask?"** If yes, cut it. "It's a task manager for your terminal" answers *what am I looking at* — that's your job. "Tasks are organized into boards" answers *what's a board* — that's the product's job, and if the product fails at it, the test needs to catch that.

Stay accurate. Describe what the product actually is, not what its marketing wishes it were — an oversold brief skews the test by setting expectations the session then measures against. If the product's own materials make claims you can see are false, describe the product at the level of its honest purpose and let the tester discover the gap.

## The disclosure dial

Ask the user how much the tester should know going in, or default to Level 2. State the level in your output.

- **Level 1 — Billboard.** One sentence. What it is, in the words a friend would use texting you about it. ("It's a little terminal app for keeping a todo list.")
- **Level 2 — Elevator pitch** *(default)*. Three to six sentences: what it is, who it's for, what problem it solves, why it exists. Still zero vocabulary, zero capabilities-by-name.
- **Level 3 — Box copy.** The elevator pitch plus the product's main capabilities *named but never explained* ("it can sync across machines" — not how, not where, not what to press), plus honest scope boundaries ("it does not do recurring tasks"). This is the most a real newcomer would know from reading the product's homepage.

When the user's scenario implies a level, use it: "my friend told me about it" is Level 1; "they read our landing page" is Level 3.

## Two outputs, kept apart

Produce two separate files — never combined, because the second would contaminate the first:

**1. The brief** (`cover-story.md`) — the only thing the tester sees. Short, in plain second person, framed as a plausible real-world source if that helps ("the email from your manager said:"). No headings needed at Level 1-2; it should read like something a person would actually receive, not like documentation.

**2. The sealed envelope** (`sealed-envelope.md`) — for the builder's eyes only, opened after the test. It lists: every insider fact you deliberately withheld (the vocabulary, the setup steps, the gotchas you noticed while reading), and for each, the naive question you predict the tester will ask because you withheld it. After the fresh-eyes run, the builder compares this against the tester's actual questions — predictions that came true confirm the product isn't explaining itself; things the tester never hit may mean the test didn't reach them.

## Leak check before delivering

Reread the brief one last time as if you were the tester, and strike anything that:

- names a command, file, button, menu, or screen
- defines a term the product itself uses
- sequences anything ("first", "then", "once you've")
- warns, hints, or reassures ("don't worry about", "you'll need", "just")
- explains a capability instead of naming it (Level 3) or names one at all (Levels 1-2)

If removing a sentence would make the tester unable to tell what the product *is*, it stays. If it would merely make their session harder, it goes — that difficulty is the data.

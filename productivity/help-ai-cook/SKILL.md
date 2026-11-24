---
name: help-ai-cook
description: Before starting a task, work out what the user could provide that would make the result clearly better — a tool to install, access to grant, a reference or asset to hand over, an answer to something you don't know — and ask for it, with the payoff and cost of each. Use when the user asks what you need from them or how they can help; before work whose quality depends on tools or materials you may not have (art, animation, audio, 3D, game-engine or editor work, external services, unfamiliar toolchains); and whenever you would otherwise guess at something you don't understand or can't reach. Skip routine edits and questions where nothing is missing.
license: MIT
---

# Help AI Cook

A result is made from three things: what you know, what you can do, and what you can check. When one is missing, the easy move is to start anyway — take whatever route your current tools allow, fill the holes with plausible guesses, and deliver something that looks finished. The user could often have closed the gap in minutes, if they had known it was there.

Before starting, find the gap and show it to them.

## 1. Pin down the goal

State it in one sentence, including the quality bar: rough placeholder, or something that ships? If the bar is unclear and it changes the approach, ask that first.

## 2. Work out what a good result needs

Set your current tools aside and ask how someone skilled would produce this. List the realistic routes from best result to worst. Always include the route you can run right now, with an honest description of what it will produce.

## 3. Check what you have

Look before you ask. Check which tools are installed and reachable, what the project already contains, and what its docs say. Read the request again and try to resolve every term, name, and reference in it.

- Never ask for something you could have checked yourself.
- Never recommend a tool without confirming it exists and fits this setup. Your memory of tools may be out of date.
- If something lives outside your reach — another repository, a private document, a service, an earlier conversation — reading harder will not find it. Stop searching and ask.

## 4. List the gaps

Compare what a good result needs with what you have. Each gap is something to ask for:

- **Knowledge** — a term, rule, or decision you do not understand or cannot reach.
- **Tool** — a program, plugin, or connector to install or enable.
- **Access** — an app left running, a service authorized, a key configured. Secrets go in the user's own configuration, never in the chat.
- **Material** — a reference, an example of "good", an existing asset to match, or something to download (name the source and its license).
- **Check** — something you cannot judge yourself, such as how it looks, sounds, or feels. Find a way to see it, or agree on when the user looks.

Keep only the gaps that change the result enough to be worth the user's time. For an unknown that is cheap to fix later, do not ask: assume, and say so.

## 5. Report

Keep it to one screen, in the user's language. Leave out any block that is empty.

```
**Goal**: <one sentence, with the quality bar>

**What I don't know**
A. <question> — where I looked: <…> · if unanswered I'll assume <…>

**With what we have now**: <route> → <honest description of the result>

**What would make it better**
1. <ask> — unlocks <what changes in the result> · costs you <what to do, roughly how long>

**Assuming unless you object**: <…>

**I'd do**: <which numbers are worth it, and why>

Answer the letters, reply with the numbers you'll do, or say "go".
```

For an ask that needs setup, give the exact command or the exact place to click. If nothing is missing, say so in one line and start.

## 6. Then do the work

- Test anything the user set up before relying on it.
- "Go" means go: start with what you have and the assumptions you stated, and do not ask again unless the task changes.
- If a new unknown appears mid-task that would change the result, ask then. Do not guess past it.
- When you finish, name every assumption the work still rests on.

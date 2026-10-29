---
name: reference-hunt
description: Find how real, shipped apps solve a given screen or flow, so the design starts from patterns people actually use instead of the AI's average guess. Searches Mobbin when it is connected, otherwise works from the user's own screenshots and App Store listing screenshots. Gives the 3 best patterns in chat, each linked to the real screen and marked seen or unconfirmed, and saves a dated reference card in the project. Use before designing or rebuilding a screen, or when the user asks "how do other apps do this", wants design references or examples, or says something like "find examples of a paywall screen" or "show me good onboarding flows".
---

# Reference hunt

You already know what screen or flow to build. This finds the best real versions of
it before any code is written. It is not a market survey and not a list of ideas.
The output is a few concrete patterns from real screens, and one recommendation.

## The one rule

**Only describe a screen someone has actually seen.** Seen means one of:

- a Mobbin screen or flow opened in this session,
- a screenshot the user sent,
- an App Store or Google Play listing screenshot opened in this session,
- for a website, a live public page opened in a browser in this session.

Never describe another app's UI from a blog post, a review, a help page, a teardown
article or memory. Those are often years old, and a user can lose hours hunting
for a screen that no longer looks like that. A blog post can be a lead for where to
look. It is never the evidence.

Mark every pattern **seen on a screen** or **unconfirmed**. Unconfirmed means the
idea came from somewhere other than a screen you opened; say where, and suggest how
to see it (search Mobbin for it, or ask the user to screenshot it).

## Input

One sentence on what to find. Examples: "a paywall for a monthly subscription",
"the empty state of a list before anything is added", "a streak that is about to
break". If the user names apps to look at, start with those. If the request is
vague ("make it look better"), ask which screen, once.

## 1. Check what is already known

Search the project's research folder (default `docs/research/`) for a reference card
that already covers this screen. If one exists and is recent, start from it, say so,
and only look for what it does not answer. A new hunt on a covered screen goes into
that card as a new dated section, not a new file.

Then look at the user's own screen as it is now: the code, or a current screenshot.
A pattern only helps if you know what it is replacing.

## 2. Pick the source

First pick the platform. Read the Platforms setting in the rules file. A web only
project is searched as **web**; a mobile app as **ios** (Mobbin's iOS library is
the larger one, and most Android screens follow the same patterns). If the rules
file does not say, look at the code: a web framework with no app build is web.
Searching the wrong platform returns real screens that do not fit the layout.

Then use the first source that is available. Tell the user in one line which
source and platform you used.

1. **Mobbin**, if its tools are connected. Pass the platform from above. Check the
   rules file first: if it says Mobbin is connected, use it. Otherwise look for
   Mobbin search tools in the tools you have (they search screens, flows, and
   sections of screens). Use them automatically; do not ask first. If the user wants to connect it, point them to
   Mobbin's own setup guide for their tool
   (https://docs.mobbin.com/mcp/clients/overview); it is a one time sign in with
   their own account. Mobbin is recommended, not required. Plans and
   which plans include the agent connection are in the ship skill's
   `references/facts.md`; point the user there rather than quoting prices.
2. **The user's own screenshots.** Ask for screenshots of the screen in two or three
   apps or sites they like. A phone or browser screenshot is a normal, complete input.
3. **Store listing screenshots** (mobile). Open the App Store (or Google Play) listing of
   apps known for this screen and use their screenshots. These are marketing images,
   so they show the best screens, not every screen. Say that when you rely on them.
   **Live pages** (web). There are no store listings, so open the public pages of
   sites known for this screen in a browser instead. Screens behind a sign in cannot
   be reached this way; ask the user for screenshots of those.

If none of these is possible, say so plainly and stop. Do not fill the gap from memory.

## 3. Search

- Search for the **job of the screen**, not just its name. "Choose a plan" and
  "start free trial" find more paywalls than "paywall".
- Look at **flows** when the question is about order (what comes before and after),
  and **screens** when it is about layout and copy.
- Make sure you are looking at the **right screen**. Apps split one job across
  several screens (a list, a picker, a detail). Building from the list when the
  question was about the picker means redoing the work.
- Cover 5 to 8 apps, including at least one outside the user's category. The best
  pattern for a screen is often in an unrelated app.
- If the user has a design file (Figma or similar) with references collected, read it
  in as few tool calls as possible: one screenshot of a whole board rather than one
  call per frame.

## 4. Capture each pattern

For each candidate, write down:

- **App and screen**, with a link to the real screen (or the screenshot filename).
- **Exact words** on the screen: button labels, titles, the line under the title.
  Quote, do not paraphrase.
- **When it appears**: what the user did just before, and what triggers it.
- **What the user experiences**: one or two sentences, in plain words.
- **Why it works**: one sentence on the behaviour it relies on.
- **Effort** to build it in this app: **small** (copy, layout, or one component),
  **medium** (a new screen or some new state), **large** (new data, a server
  change, or a new service).
- **Seen on a screen** or **unconfirmed**.

The test: could someone build this from the card without asking a follow up
question? If not, go back to the screen for the missing detail.

Good: "On the empty list, one large button reads 'Add your first plant', with a
single line under it: 'It takes 20 seconds.' Nothing else on the screen."

Bad: "The app uses an encouraging empty state to drive the first action."

## 5. Rank

Keep the 3 best. Prefer seen over unconfirmed, then smaller effort, then the one
closest to how this app already works. If two patterns are the same idea, keep the
cheaper one. Note anything that needs a server or a paid service separately, so it
does not hold up the parts that can ship now.

## 6. Answer in chat

Keep it short. The user reads and discusses; they do not follow the card literally.

```
Source: <Mobbin | your screenshots | store listings>

1. <Pattern name> (<App>), effort <small|medium|large>, <seen on a screen|unconfirmed>
   <one or two lines: what the user sees and does>
   <link or image of the real screen>

2. ...
3. ...

Recommendation: <one sentence: which to build first and why>
Saved: <path to the reference card>
```

Show the image inline when you have it. Otherwise give the link.

## 7. Save the reference card

Write the full version using `templates/reference-card.md` in this skill's folder.

- **Where:** the project's research folder. If the rules file names one, use it;
  otherwise `docs/research/`. Name it `reference-<screen>.md` in lowercase, for
  example `reference-paywall.md`.
- **File into an existing doc first.** If a card or research doc already covers this
  screen, add a new dated section to it instead of making a new file.
- Date it, name the source, and include the table of every app looked at, not just
  the top 3, so the next hunt does not repeat the work.
- If the project's rules file keeps a list of docs, add one line for the new card.

## Finish

The chat answer from step 6 is the finish. Do not start building unless the user
asks; the point of the card is the conversation about which pattern fits.

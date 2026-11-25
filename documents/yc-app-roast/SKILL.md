---
name: yc-app-roast
description: >-
  YC App Roast: roast a YC or a16z Speedrun application. Use when a founder
  wants their YC or Speedrun answers scored, asks "what would a YC partner
  think", wants the weak answers found or rewritten, or wants their draft
  checked before they submit. Scores every answer 0-10 against public advice
  from YC and Speedrun partners, names the top issue with the exact words that
  cost points, and writes a rewrite from the founder's own facts. Works for YC
  and a16z Speedrun. Not affiliated with Y Combinator or a16z.
---

# YC App Roast

You roast a founder's YC or a16z Speedrun application: every answer gets a score, the one issue that costs the most, and a rewrite. Nothing else. You do not send anything, share anything or contact anyone.

To get the roasted draft reviewed by friends on one shareable page, share it for review with `yc-app-review`.

Files in this skill: `references/rubric.md` (every rule with its public source), `examples/tidewater-draft.md` and `examples/tidewater-roast.md` (a fictional draft and a real roast of it).

## 1. Get the answers

Ask for the application text: a pasted draft, a doc or the portal export. Note the program (YC or Speedrun). Keep the questions exactly as the portal asks them and the answers verbatim. Do not invent answers. List empty questions back to the founder.

Ask for the facts you need to check claims: what is live, real user counts and how they are measured, revenue. Never fill gaps with guesses.

## 2. Score every answer

Read `references/rubric.md` first. It cites Garry Tan, Dalton Caldwell, Michael Seibel, Kevin Hale, a16z Speedrun partners and Troy Kirwin's bad-vs-great Speedrun teardown.

For each answer, in the program's order:

1. **Score 0-10** against the rubric. The weakest critical rule caps the score (honesty B6, clarity A1-A3, the 20-second rule E1). It is not an average.
2. **Top issue:** one line, quoting the exact words that cost points, with the rule id (for example `A1: "AI-powered platform"`).
3. **Rewrite:** uses only facts from the founder's text or answers to your questions. Keeps their voice. Leads with the strongest fact. About 20 seconds to read (60-80 words) unless the question needs less. Things not built yet are in future tense.
4. **Word count** of the rewrite (character count for the 50-character YC description).

Checks to run on every answer:
- What it is, in the first sentence. No problem setup before the "what".
- Plain English, no jargon or "platform". Would they say it to a friend?
- Active metrics (DAU, WAU, retention, revenue) lead; cumulative totals only as support; each metric defined.
- Nothing reads as live that is not live. Every number defensible in the interview.
- No volunteered weakness the question did not ask for.
- The YC "describe in 50 characters" line: name what it does, concrete nouns, count the characters.

Output a table, one row per question, with the score before and after the rewrite:

| # | Question | Score | Top issue | Rewrite | Words |
|---|---|---|---|---|---|

Then three lines for the whole application: the strongest answer, the weakest answer, and whether the numbers agree across answers.

## 3. Whole-application pass

- The first answer gets the most attention. If it is weak, fix it first.
- Facts that are strong in one answer and missing in another (a defined user metric, a named customer, a first-hand founder insight): port them.
- Same number everywhere. A metric that changes between answers is a red flag.
- For Speedrun, also run the D levers (one-liner, specific traction, founder-market fit, play to win).

## 4. Hand it back

- List what you removed and why, in a few lines.
- List the open questions only the founder can answer (an accuracy number, whether a pilot is signed). Do not guess them.
- Show the rewrites as suggestions. The founder decides. Never claim the application will be accepted.

When the founder has picked their answers and wants people they trust to read them, share it for review with `yc-app-review`.

See `examples/tidewater-roast.md` for a full roast of `examples/tidewater-draft.md`.

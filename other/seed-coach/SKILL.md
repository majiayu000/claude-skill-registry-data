---
name: seed-coach
description: >-
  Pitch Coach. Rehearses the investor call with you: drills the hard
  questions investors ask (market, competition, traction, unit economics,
  team, why now, risks, the ask), tailored to your own numbers from the
  competitor scout, the financial model, the market size and the investor
  you are meeting ("Rover has 515,771 ratings. Why will owners switch?"),
  grades your written answers (a number, specifics, no hedging, under a
  minute spoken, answer first) and writes a 20-minute plan for a booked
  first call. Reads seed/competitors.json, model.json, market.json,
  investors.json, pipeline.json and calls/. Use when the user says "prep me
  for the call", "practice my pitch", "what will investors ask", "drill me",
  "grade my answer", "mock investor", "call agenda", or after /seed-closer
  books a call.
argument-hint: "[drill | grade | agenda] [--investor ID]"
---

# seed-coach

The Pitch Coach gets you ready for the questions that sink first calls. It
reads the numbers the other seed skills wrote and turns them into the
questions a sharp investor will ask about them, with your own figures next to
each one so you can answer in a sentence. Then it grades what you say against
the things investors listen for, and lays out the 20 minutes of a booked
call so you spend them on the story, not on small talk.

`${CLAUDE_SKILL_DIR}` below is this skill's folder (where this SKILL.md lives).

```bash
python3 "${CLAUDE_SKILL_DIR}/coach.py" drill --n 10 --customers owners --provider walker
python3 "${CLAUDE_SKILL_DIR}/coach.py" drill --investor maya-chen --category "the ask"
python3 "${CLAUDE_SKILL_DIR}/coach.py" drill --category "unit economics" --seed 3 --write
python3 "${CLAUDE_SKILL_DIR}/coach.py" grade --answer "15% flat, no owner fee. ..." --question ue-take
python3 "${CLAUDE_SKILL_DIR}/coach.py" grade --file answer.txt
python3 "${CLAUDE_SKILL_DIR}/coach.py" agenda --investor maya-chen --write
```

Other flags: `--dir` (default `./seed`), `--json`, `--minutes 10..60` for the
agenda, `--seed N` to shuffle within each category the same way every time.

## What it reads and writes

| file | what |
| --- | --- |
| `questions.json` (this folder) | the bank: 8 categories, generic questions plus tailored ones with `{placeholders}`, each with what the investor is testing and what a strong answer has |
| `seed/competitors.json` | `/seed-scout`: the biggest rivals, their ratings, weak points and counts |
| `seed/model.json` | `/seed-model`: take rate, contribution per order, LTV:CAC, breakeven month, peak burn, use of funds |
| `seed/market.json` | `/seed-market`: TAM, SAM, SOM and the assumptions behind them |
| `seed/investors.json` | `/seed-investors`: the investor's role, firm, last deal, check size, personal line |
| `seed/pipeline.json`, `seed/calls/<id>.ics` | `/seed-closer`: whether the call is booked, and when (UTC shown in ET) |
| `seed/coach/drill.md`, `seed/coach/agenda-<id>.md` | with `--write` |

## How it works

- **Drill.** A tailored question is asked only when the files hold every
  number it needs; otherwise it is skipped, never filled with a guess.
  Tailored questions come first, one per category per round, then the
  generic ones, so ten questions cover the ground. `--customers` and
  `--provider` set the words ("owners", "walker pay").
- **Grade**, five checks of 20 points: 15 to 150 words (under 60 seconds at
  150 words a minute), a number, no hedging words ("I think", "maybe",
  "probably"), at least two specifics (numbers, names) and no buzzwords
  ("disrupt", "world-class"), and the answer first (a first sentence of 25
  words or fewer). Exit 0 only when all five pass.
- **Agenda**: seven blocks, 2, 3, 4, 4, 4, 2 and 1 minutes for 20 (scaled
  exactly for other lengths): hello and why them, the problem (the review
  evidence), the product, market and model, their questions (the three most
  likely), the ask, the next step.

## Steps

1. Run `coach.py drill --n 10` with the user's words for customers and the
   supply side. Ask the questions one at a time, as the investor would.
2. Let the user answer in writing or out loud (transcribe it), then run
   `coach.py grade --answer "..." --question ID`. Read the unchecked lines
   back and ask for a tighter version. Two or three rounds per question.
3. When a numbers question stumps them, show the "Your numbers" line and
   the file it came from. If a number looks wrong, fix it in that skill
   (`/seed-model`, `/seed-market`), not in the answer.
4. When `/seed-closer` books a call, run `coach.py agenda --investor ID
   --write` and `drill --investor ID`, and walk through both the day before.
5. After the call, hand back to `/seed-closer` to log it and send the
   follow-up, and to `/seed-dataroom` if they ask for documents.

## Example: the reel

Leashly (made up) has a call with Maya Chen (fictional) of Northlight
Ventures on Thursday, November 5, 2026 at 10:00 AM ET. `coach.py drill
--customers owners --provider walker` opens with:

```
 1. [market] Your SOM is 2.5% of a $960M SAM in 3 years. What gets you the first 1,000 customers?
 2. [competition] Rover has 515,771 ratings. Why will owners switch?
 3. [unit economics] What does your 15% take rate leave after walker pay?
    Your numbers: Per walk: $25 price, you keep $3.75, $2.23 after costs.
```

The answer "15% flat, no owner fee. We keep $3.75 of every $25 walk and
$2.23 after card fees and the backup walker. Rover keeps 20% of sitter
bookings and adds an owner fee." grades 100/100: 32 words, about 13
seconds. `coach.py agenda --investor maya-chen` opens with her personal line,
puts Rover's 106 of 341 and Wag!'s 81 of 324 in minutes 2 to 5, and ends on
the $1.5M post-money SAFE and a date for the next meeting.

## What it never does

It never invents a number for an answer, never tells the user to overstate
traction, and never promises that a good call means a check. Investors decide.

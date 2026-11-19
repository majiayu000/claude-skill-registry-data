---
name: help-me-decide
description: One page a busy decider can approve from its first screen, with the answer first, every claim sourced, options scored on points the decider set, and separate reviewers checking facts and reasoning. Use when you ask for a "decision report", "decision paper", "board paper", "CEO report", "recommendation", "help me decide between", or "write this up so I can decide". Not for status updates, newsletters or marketing copy.
---

# One-page decision report

One page that a busy decider reads alone and can approve from its first screen. The rules come from Minto, Zelazny, Tufte, Mayer, Rogers & Lasky-Fink, Amazon's memos, Kahneman/Lovallo/Sibony, Noise, Kepner-Tregoe, Klein and Bain. Each rule is tagged with how strong its evidence is.

Files beside this one:

| File | Read it when |
|---|---|
| `references/rules.md` | Always, before drafting. The 22 rules the report must pass. |
| `references/precedence.md` | Two rules or books pull different ways. |
| `references/plain-words.md` | Writing any line. Swaps for jargon. |
| `references/twelve-questions.md` | Building the reasoning check (step 6). |
| `references/reviewer-prompts.md` | Starting any reviewer (steps 4, 6). |
| `scripts/score.py` | Every time you total scores or work out what would change the answer. Never do this arithmetic in your head. |
| `template/example-report.html` | Building the page. Copy its structure and CSS; replace all content. |
| `vendor/tyroneross/` | Checking sources (step 2). Apache-2.0, pinned commit, see `NOTICE`. |
| `vendor/sruthir28/critic-SKILL.md` | The grading format the rules reviewer uses. MIT. |
| `evals/cases.md` | After changing anything in this skill. |

## The work, in order

### 1. Pin the decision with the decider, in plain words

Before any research, get these from the user. Ask only for what you can't find in the conversation, and ask in plain words (people often don't follow "must-haves" and "weights"; say "what would rule an option out?" and "what matters most to you here?").

- **The decision**, as one question with a yes/no or pick-one answer.
- **Who decides** (one person) and **by when**. "No deadline" is a valid answer; write it down.
- **What rules an option out** (must pass). Default: the needs the user already stated.
- **What matters, and how much.** Turn their answer into points that add to 100, show them the points in one line, and let them correct it. Save the points to `decision.json` in a scratch folder **before** any option is scored (rule 19). If the user won't set them, set them yourself, say so on the page, and label them judgment.

### 2. Gather the facts and clear them

Follow `vendor/tyroneross/source-integrity-SKILL.md`. Decision reports are consequential, so use **strict trace mode** (`vendor/tyroneross/references/strict-trace.md`): a source register, claim IDs, exact locators, a confidence level per claim, and every calculation done with a tool. Research in parallel subagents when your agent supports them and there are several independent strands; otherwise one strand at a time.

Map its confidence to the page's labels:

| Source check says | Page label | How it is written |
|---|---|---|
| Supported or Derived, High | fact | Stated directly. |
| Supported or Derived, Medium | fact | Stated with who says so, or its limit. |
| Low | estimate | Only as a limit or lead, never as a main reason. |
| Unverified | (none) | Left out, or named as a gap. |
| Not factual (inference, recommendation, opinion) | judgment | Says it is my judgment. |
| A forecast of what will happen | estimate | Odds as a number range, compared with similar cases (rule 16). |

### 3. Build at least three options

At least two real choices plus "do nothing" (rule 18). Drop any that fail a must-pass need, judged as each would stand when finished, with the same test for every option. Look for a mix of the two best; it often wins.

### 4. Have a separate reviewer score the options

The writer never scores its own options. Start the **scorer** from `references/reviewer-prompts.md` in a fresh subagent (or, if your agent has none, a fresh chat or a different model that has not seen your work). Give it the options, the must-pass list and the points from `decision.json`, never your scores or preference. If you also scored, show both sets on the page; the scorer's numbers decide.

Run `python3 scripts/score.py decision.json` for totals, the lead, and what would change the answer. Copy its numbers onto the page as they come out.

### 5. Draft the page

Copy `template/example-report.html` and replace every word. Its shape:

1. **Title**: the recommendation as one full sentence.
2. **Decision strip, three rows**: You decide (the question, the deadline, the reply options) · I recommend (the only bold text on the page) · Main risk (with its fix).
3. **Three to five reasons**, most important first, one line each, each with a fact/estimate/judgment label. Opening a reason gives short sentences or the next level of reasons, each with source links.
4. Everything else **closed until clicked**, each section headed by a full statement: the scores, ways it could fail (each with a fix), the rules or criteria if relevant, the twelve questions, likely questions with answers, sources.

Title + strip + reasons is the first screen: **seven lines at most** (rule 4). Write the lines first, count them, cut, then build the rest. Put the case against the recommendation inside the first reason that the recommendation rests on (rule 17).

Save the page as an HTML file and give the user its path. If your agent can publish private pages (for example Claude's Artifacts), publish it there too and give the link.

### 6. Review before the user sees it

Run these in parallel subagents (or fresh chats), from `references/reviewer-prompts.md`:

- **Source post-check**: every factual or evaluative line against the claim packet; fix or delete mismatches. Fetch a sample of the links.
- **Rules reviewer**: grades the page against all 22 rules and answers the twelve questions on its own, in the Green/Yellow/Red format with the top three fixes.
- **Case for the runner-up**: only when the gap is under 100 points or the decision is hard to undo. Argues for the second option and re-scores.

Apply the fixes, republish, then tell the user in plain words what the reviewers changed. If a reviewer changed the recommendation, say so first.

### 7. Hand over

In chat: the recommendation in one line, the link, what the reviewers caught, and what remains uncertain. Then ask for the decision with the same reply options as the page.

## Stop and ask instead of guessing

- The decision can't be written as one question.
- Nobody owns the decision.
- A must-pass need rules out every option.
- A main reason rests on a Low or Unverified claim.
- The points would be set after you have seen how the options score.

## Learned from real runs

- **Two deciders.** If the user names two, accept it, name both on the page, and ask who breaks a tie (rule 21).
- **Missing internal numbers.** If the user says "go without", score on outside evidence, say so in the scores section and in question 6, and list what the report did not have.
- **When the scorer and the case for the runner-up rank the top two the other way round**, show both tables side by side with a "why they differ" column, put the split in the Main risk row, and look for a cheap test that checks the fact they disagree on. A test must check what is in dispute (for example, a sale from outside a warm list), not just goodwill.
- **Always run the case for the runner-up when the leader's must-pass rests on no customers yet**, even if the gap is over 100. In one real run it flipped the recommendation into a test.
- **Keep every source's link in the claim packet.** Research agents that drop links leave rows the fact checker cannot verify. Never cite a coverage page for figures it does not hold.
- **Say where the points came from.** If the decider gave a direction ("growth should count more") and you set the numbers, the page says so and asks them to confirm.

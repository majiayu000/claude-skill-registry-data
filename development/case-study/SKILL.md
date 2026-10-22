---
name: case-study
version: 1.0.0
author: Personify Labs
description: "Write a portfolio case study teaser (recommended 100-150 words) through guided multiple choice questions, or review an existing teaser or full case study with edits and the principle behind each."
---

# Case Study

Two modes: Write and Review. Every rule below is a requirement unless marked optional or advisory. Rules carry stable ids in backticks. Cite the id when you flag a fix.

## Overview `id: overview`

| Mode | Input | Output |
|---|---|---|
| Write | Answers to guided questions about one role | A teaser in the headline format (`teaser-format`), recommended 100 to 150 words |
| Review | An existing teaser or full case study (any length) | Prioritized edits, each with the principle applied |

Scope limits:
- Write mode builds teasers only. A teaser has one job: make a stranger want to open the full case study. It leaves out the how (process, methods, design decisions).
- Review mode accepts a teaser or a full case study.
- One role per run.
- Length is advisory. 100 to 150 words is a recommendation, not a limit. See `length-advisory`.

## Mode selection `id: mode-select`

| Condition | Action |
|---|---|
| User pasted or attached a case study, or used "review", "edit", "critique" or "tighten" | Start in Review |
| User wants a new one, or has nothing written | Start in Write |
| Unclear | Ask once with AskUserQuestion: "Write a new one (Recommended if nothing exists yet)" or "Review one I already have" |

After Write, offer a Review pass on the result. After Review, offer to rebuild a weak section in Write.

## Interaction rules `id: interaction-rules`

1. Before asking anything, check project files, memory and attached documents. Ask only for what you cannot find.
2. Ask one question at a time with AskUserQuestion. Never send all questions at once.
3. Give 2 to 4 options. Each option is a concrete draft or choice, not a vague category. Put the recommended option first and label it "(Recommended)". The user can always choose Other and type.
4. Facts (numbers, dates, what happened, who did what) cannot be guessed. Ask for them as free text, then use multiple choice for framing.
5. Never invent a metric, a cause, a regret, or a named framework. If the user cannot back a claim, offer a relative or descriptive version and mark it (confirm).
6. State the trade-off of each option in one line: what it gains and what it costs.
7. Be direct. If something is weak, say it is weak and why. Do not pad praise.
8. Check that numbers agree with each other before drafting. If two figures conflict (for example, a stated gain that does not match the start and end values), say so, show the arithmetic, and ask which is right. Do not silently pick one.

## Length advisory `id: length-advisory`

- 100 to 150 words is the recommended range for a teaser. It is advice, not a rule.
- If a draft is over, report the word count and list the cheapest cuts in order, with what each one costs. Let the user decide. Never cut content without the user's say.
- If the user keeps the longer version, accept it and do not raise it again.
- Treat an over-length teaser as a low-priority note in Review, below evidence and clarity problems.

## Teaser format `id: teaser-format`

The teaser has no generic section labels. Each line carries its own content.

```
**[Title] · [Company] · [years]**
[Scope line: who the product serves and what the user owned, 1 to 2 sentences]

### [Headline: one sentence naming the problem solved and the fix]
[Problem and goal: 1 to 2 sentences]

**[Proof line: the result that proves the goal, with a baseline]**

- [Contribution starting with a first-person verb]
- [Contribution]
- [Contribution]

**[Regret line: the user's real regret as a plain sentence.]** [One supporting sentence.]

**[Read the full case study →]**
```

Rules:
1. No generic labels such as "The problem", "The result", "What I did" or "One thing I'd do differently". Use labels only if the user asks for labeled sections.
2. Headline: one sentence, plain words, names the problem solved, the fix, or both. Every claim in it must be backed (interaction rule 5). No cleverness. No colon subtitle.
3. Offer three headline drafts at assembly: problem-led, fix-led, or both. Recommend both when it fits one plain sentence.
4. Proof line: the result that proves the goal, with a baseline for any number. Do not repeat the headline's wording.
5. Contributions: 2 to 4, each the user's own call, each starting with a first-person verb so no label is needed. The how stays out.
6. Regret line: a short bold lead sentence with the user's real regret, then one plain sentence on why.
7. Skim test: read only the headline and the bold lines. They must tell the whole story. If they do not, rewrite them.
8. The order stays fixed so a set of roles reads as a set. The wording is specific to each role.

## Source files: persona, voice, rhythm `id: source-files`

Three layers, each with one job. Do not duplicate work another layer owns.

| Layer | Source | Owns |
|---|---|---|
| Stance, voice, rhythm | persona.md, voice.md, rhetoric-and-rhythm.md | Who is talking, how the argument builds, which devices and sounds to use |
| Sentence mechanics | the righter skill | Weakeners, em dashes, jargon, active voice, reading level |
| Case study structure | this skill | Section order, questions, evidence checks, review format |

Resolve the three files once, at setup, in this order. Use the first match.

| Order | Where to look |
|---|---|
| 1 | A long-form writing skill the user has, with references/persona.md, references/voice.md and references/rhetoric-and-rhythm.md (the `longform` skill in this repo has all three) |
| 2 | Files with those names in the project, an upload, a pasted message, or a connected folder |
| 3 | None found: ask once with AskUserQuestion, "Want this to sound like you?", options: "Skip, use plain defaults (Recommended for a first run)", "Quick setup, 5 questions", "I'll paste my own files" |

Handling:
- Found: tell the user in one line which files you are using.
- Found but unreadable: say so in one line and continue without that file. Never claim you applied a voice you could not read.
- Never block a run on this step.

## Applying persona and voice `id: apply-voice`

Read persona.md, then voice.md, then rhetoric-and-rhythm.md.
- Write mode: use them to choose which drafts to offer as options, so the options already sound like the user.
- Review mode: use them as the standard the draft is checked against.
- Voice shapes how a fact is said, never what the fact is. Do not copy phrasing from the files into new claims.
- The files are written for long-form. For a teaser (about 150 words) use only what fits: skip signposting, extended backstory and any device that needs length. For a full case study apply them at full strength: all self-check items, and no more than 3 to 4 devices in the piece, one per beat.

For a persona built on the operator stance (an operator who has done the thing, writing for operators mid-task, reader as hero):

| Voice device (id) | Teaser | Full case study |
|---|---|---|
| Point first (`bluf`) | The headline is the point. It states the problem solved and the fix in one sentence. | First paragraph states the point. |
| Minimum viable backstory (`minimum-viable-backstory`) | Keep only what a stranger needs. Delete any setup sentence the point survives without. | Same. |
| Why before how (`sales-then-logistics`) | Give the why and the proof. Keep all the how out. | The why comes before the how. |
| Contrast (`contrast-sparkline`) | One real "what is" to "what could be" beat from specifics: the problem body, then the proof line. The user's customers are the hero. | Every section moves through it. |
| Name the pattern (`framework-naming`) | Only if the user already has a name. Short, used once, never renamed. Never invent a label. This overrides the self-check's "name at least one pattern." | If a repeatable pattern is present, suggest a name and ask the user to confirm it. |
| Obvious objection (`moo`) | Optional. One clause, only if a stranger would immediately doubt the result. | Answer it. |
| Paragraph rhythm (`paragraph-rhythm`) | One idea per line. Claim, evidence, so-what. A specific example beats an abstract claim. Cut tangents even if liked. | Same. |
| Tone (`tone-rules`) | No throat-clearing. Confidence over hedging. No buzzwords or jargon unless defined in one clause. Humor never at the cost of clarity. Admit what did not work. | Same. |

Also apply: no theory, no "studies show", no motivational language, no hedging.

## Devices and rhythm `id: devices-rhythm`

Device budget (`rhetoric-restraint`):
- Teaser: zero or one device, two at most. Most teasers get none. Never force one to look crafted.
- Full case study: 3 to 4 at most, one per beat.

If a device genuinely fits, match it to the beat:

| Beat in the teaser | Device |
|---|---|
| Headline (`bluf`) | One sharp line or a paradox, only if true and specific. Plain is the default. |
| Problem body (`contrast-sparkline`) | One concrete detail that stands for the whole problem, not an abstract summary. Example shape: "the Friday report nobody opens" standing in for a broken reporting process |
| Pattern name (`framework-naming`) | An epithet, only if real |
| Regret line (closing) | A reordered closing line, at most once, only if the sentence is naturally plain and strong that way. Default to none |

Skip allusion, personification, simile and anything else unless it serves one specific sentence. Never run two metaphors in the same passage.

Rhythm applies at every length (`sentence-rhythm`):
- Vary sentence length on purpose. Build the case with a longer sentence, put a short one where the verdict is. In the problem body, long then short. In the proof line, the number lands in the short sentence.
- Read the last line of each beat aloud in your head. If it trips, the rhythm is off.
- Alliteration and assonance, if used, go on one line only, the same line as a device.
- Match sound to job (`sound-symbolism-prose`): smooth sounds (l, m, n, r, w) for the problem and diagnosis; hard stops (p, b, t, d, k, g) for the verdict and proof; go light on hissing sounds (s, sh, z) at turning points. If a plain term forces hissing sounds (for example "self-service"), keep the plain term and say so. Do not wrap a punchy line in drawn-out sounds.
- Keep sentences simple. Vary the length, not the difficulty.

## Self-check `id: self-check`

Run on every final draft and every reviewed piece. Report pass or fix for each item.

| # | Question | Id |
|---|---|---|
| 1 | Does the headline (teaser) or first paragraph (full case study) state the point, or wander toward it? | `bluf` |
| 2 | Is there a real "what is" before the "what could be"? | `contrast-sparkline` |
| 3 | Is anything well written but not moving the reader? Cut it. | `paragraph-rhythm` |
| 4 | Does any beat have two devices stacked, or a forced one? | `rhetoric-restraint` |
| 5 | Read the short sentences in isolation. Do they land, or get lost because every sentence around them is the same length? | `sentence-rhythm` |
| 6 | Skim test: do the headline and bold lines alone tell the whole story? | `teaser-format` |
| 7 | Run the Righter pass. | `righter-pass` |

Full case study only, also run voice.md's remaining items: a named pattern (`framework-naming`), the obvious objection answered (`moo`), and an ending that shows the reader's world after the idea (`contrast-sparkline`). Teaser: skip these, because the teaser ends on the regret and the link.

## Righter pass `id: righter-pass`

Route the final draft or reviewed piece through the righter skill for mechanics only. Righter owns the sentence. This skill owns the structure.

1. Check against the righter skill's data/weakeners.json and its rules on em dashes, jargon, active voice, double negatives and contractions. Words like "so" used as a conjunction are false positives for the intensifier list. Ignore those and say so.
2. Get the reading score from the righter skill's scripts/ari.mjs when Node is available. If the command line prints nothing on longer text, import its computeReadability function and call it directly. It uses the same formula.
3. Righter's Grade 5 target is for UI copy. For a portfolio piece, report the score and flag hard sentences. Do not flatten the voice to reach Grade 5. State what you changed and what you left.
4. Do not use Righter's UI review format, component rules or phonaesthetics data (that data picks sounds for single words such as labels). Do not call vois_get_microcopy (it is for in-product copy).

## Mode 1: Write `id: write-flow`

Produces a teaser in the `teaser-format`. Run the steps in order. One AskUserQuestion per step.

### Step 0. Setup
Ask: which role, and does the teaser link to a full case study (default) or stand alone. Ask whether the company or numbers have confidentiality limits. If yes, plan relative or directional outcomes. Then resolve persona, voice and rhythm files (`source-files`).

### Step 1. Eyebrow and scope line
Collect: exact title; years (compute duration from today's date, or recommend "[start year] to present" so it does not go stale); who the product serves, in plain words; what the user owned (scope, not duties).
- Ownership options (multi-select): led the whole experience / owned one slice / set direction for a team / senior designer on a squad.
- Offer two drafts of the who-it-serves line: one listing every audience, one leading with the main audience. Recommend the second unless all audiences get equal weight.
- Flag stock phrases (for example "player-coach", "raising the bar") and prefer one concrete proof.

### Step 2. Problem and goal
Ask for the core struggle and, if available, a real quote from users. Collect the business goal. Offer 2 to 3 drafts of the problem body.
- If the note mixes problem and goal, split them. Prefer the problem that led to the headline result.
- Ask whether the cause is known. Do not guess the cause. If you must draft one, label it a guess.

### Step 3. Proof
Ask what changed and what evidence exists. Headline type (multi-select): behavior change / hard metric / user score / adoption. Apply `evidence-checks`. If there are no numbers yet, draft with directional language and add (confirm). Draft the proof line.

### Step 4. Contributions
Collect 2 to 4 contributions that make a reader ask "how?". Each must be the user's own call, not a team outcome. Ask which parts were personally theirs.
- Ordering options: scope first (signals seniority) or most surprising first (hooks the reader). Recommend most surprising first unless the title already carries seniority.
- Strip stacked metaphors. Keep one plain version. Start each with a first-person verb.

### Step 5. Regret
This is the hook. Do not write a regret for the user. Offer 3 options drawn only from what the user has said (for example: involved a group earlier / measured earlier / pushed harder on a decision), plus Other. Confirm it is the user's real regret. Tease it. Do not explain it fully.

### Step 6. Headline, assemble and check
Ask which headline to use, with three drafts built from the user's own facts: problem-led, fix-led, and both (Recommended when it fits one plain sentence). State the cost of each. Then assemble using the `teaser-format` template. Run `self-check` and `righter-pass`. Report: word count, reading score, which device (if any) was used and where, anything still marked (confirm), and a reminder to check employer policy on naming the company and sharing numbers before publishing. If over 150 words, follow `length-advisory`. Offer a Review pass.

## Mode 2: Review `id: review-flow`

Goal: say what is weak, give the fix, and name the principle, so the user learns the rule and not only the edit.

### Steps
1. Read the whole piece. Record the type (teaser under about 200 words, or full case study), the role, and the audience. Resolve persona, voice and rhythm files (`source-files`).
2. List claims that need the user's truth (numbers, causes, who did what). Do not edit around them. Ask about the highest-impact ones with AskUserQuestion, at most 3 questions, one at a time. Options: keep and mark (confirm) / soften to a relative claim (Recommended if unproven) / cut. If the user is not available, flag them in the output and proceed. Apply interaction rule 8 to any numbers.
3. Run the checks below, then `self-check` and `righter-pass`.
4. Write the edits. Rewrite only the flagged parts. Keep what already works, including the user's good lines. Use only facts already in the piece or confirmed by the user. If a better edit needs a fact you do not have, write a question instead of guessing.
5. Deliver the output in the template below. Offer to apply every edit into a clean version, and do it only if asked. When applying, use the user's confirmed answers, run the Righter pass again, and report the new word count.

### Checks

Evidence and honesty
- The result does not prove the stated goal, only something nearby.
- Percentages without a baseline, timeframe or starting point.
- Figures that do not agree with each other (for example, a stated gain that does not match the start and end values).
- A number attached to the wrong metric, or a cause claimed that the user cannot back.
- A claim a stranger would doubt on sight, with no answer (`moo`).
- Vague proof of impact ("improved morale", "greatly improved") with nothing behind it.
- Team outcomes written as personal contributions, or the reverse.

Structure
- Teaser: has eyebrow, scope line, headline, problem body, proof line, contributions, regret line and a link (`teaser-format`). Leaks the how. Over the recommended 150 words (advisory, see `length-advisory`).
- Generic labels such as "The problem", "The result", "What I did", "One thing I'd do differently". Flag as a fix and offer a specific headline or line in each place. If the user chose labels on purpose, drop this check.
- Headline is more than one sentence, is clever instead of plain, or names neither the problem nor the fix.
- Skim test fails: the headline and bold lines alone do not tell the story.
- Full case study: the why comes before the how (`sales-then-logistics`). The user's own decisions and the trade-offs behind them are visible, not only a list of deliverables. The outcome has a baseline. There is a real learning, stated plainly. The how that a teaser promised is present.
- The opening states the point (`bluf`). Backstory is the minimum (`minimum-viable-backstory`).
- A real "what is" comes before "what could be" (`contrast-sparkline`).

Clarity
- Jargon or acronyms a stranger cannot read. Spell out or swap.
- Stock phrases and stacked metaphors. Keep one plain version.
- Hedging, throat-clearing, buzzwords (`tone-rules`).
- Tangents that are well written but do not move the reader (`paragraph-rhythm`).
- Sentences all the same length (`sentence-rhythm`).
- Date, title and duration errors. Compute durations from today's date.

Risk
- Confidential numbers, or a named company or client, without a check on employer policy.
- Claims about other people that could land badly. Flag them. Do not decide for the user.

### Review output template

Order edits by impact, biggest first. Cap the main list at 7. Put the rest under "Smaller fixes" in one or two lines. Omit any section that has nothing in it, except Verdict.

```
**Verdict:** [2 to 3 sentences: what works, and the one biggest problem]

**Edits**
1. **Before:** [original text]
   **After:** [rewrite]
   **Principle:** [the rule in plain words, with the id in backticks when it comes from voice.md or the rhythm file]
   **Why:** [one sentence on what the reader gains]

**Smaller fixes:** [one or two lines]

**Can't verify:** [claims that need the user's confirmation, each with a recommended action]

**Self-check:** [one line per item, pass or fix]

**Mechanics (Righter):** [reading score before and after, weakeners removed, em dashes removed, jargon swapped; write "None found" where true]

**Cuts (advisory):** [word count, and the cheapest cuts in order with what each costs, or what to move to the full case study]

**Questions for you:** [open facts, at most 3]
```

If the piece is strong, say so in one line and keep the edits short. Do not invent problems to fill the template.

## Evidence checks `id: evidence-checks`

Apply in both modes.
1. Every percentage has a baseline or a timeframe. "Up 27 points to 80+" implies a starting point. Show it if known.
2. Spell out acronyms or swap for plain words (for example, "usability score" instead of the survey name).
3. The result matches the stated goal. If the goal was fewer calls and the proof is a satisfaction score, say so and ask for a closer metric.
4. If the obvious metric is misleading (for example, easier self-service raises demand, so total volume does not fall), state what actually moved instead of claiming a drop.
5. Read numbers back and confirm which metric each belongs to before drafting. Never reassign a number to a different metric.
6. Check the arithmetic. A stated gain must match the start and end values. If not, ask which figure is right.

## Final checks `id: final-checks`

- A stranger with no industry or company knowledge can follow it.
- The result proves the goal, not only something nearby.
- No claim the user said they could not back.
- Nothing in a teaser that belongs in the full case study (process, morale claims, long backstory).
- Title and dates are correct.
- No em dashes. No buzzwords.
- No generic section labels in a teaser unless the user asked for them.
- Teaser: zero or one device, two at most; sentence lengths vary, with a short sentence at the verdict.

## Optional setup for users without persona, voice or rhythm files `id: quick-setup`

Run only if the user chose "Quick setup". Ask five questions with AskUserQuestion, one at a time, each with 2 to 4 concrete options plus Other:
1. Who are you writing for (hiring managers, peers, clients)?
2. What should they think of you after 30 seconds?
3. Tone: plain and direct / warm / dry and understated / bold.
4. Words or habits you never want to use (for example buzzwords, exclamation marks).
5. One piece of your own writing that sounds like you (ask for a short pasted sample).

Then write a persona.md (stance, reader, beliefs, what this writer is not) and a voice.md (tone rules, what to avoid, 2 to 3 habits from the sample). Keep each under 200 words. Do not infer traits the user did not state. Offer both as files the user can save and reuse. Skip the rhythm file: the rules in `devices-rhythm` still apply.

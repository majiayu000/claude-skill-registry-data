---
name: write-op-ed
description: Writes an op-ed with a news peg, one clear argument, evidence, a counterargument answered and a call to action, sized to the publication's limit, plus a pitch note. Use when pitching an opinion piece.
license: CC0-1.0
metadata:
  version: 1.0.0
  kind: prompt
  category: blogging
  source: https://hermes-ide.com/prompts/write-op-ed
  catalog: 2026.1014.1
---

# Write an op-ed

## Inputs

- [ARGUMENT_AND_EXPERTISE] (required): The argument you want to make, the evidence you have (with sources), what you want readers or decision-makers to do, and why you are credible on it (role, experience, research).
- [NEWS_PEG] (optional): The news, event, report or anniversary that makes this timely now. Leave empty for suggestions.
- [WORD_LIMIT] (optional; default: 750): The publication's word limit.

Take each value from the invocation or the user’s message. If a required value is missing, ask for it once.

<context>
You are an opinion editor who helps experts write op-eds that get accepted. Opinion editors receive far more submissions than they can run; they choose pieces that are timely, make one clear and arguable point, come from someone with a reason to be heard, and are written for a general reader. A typical op-ed opens by connecting to the news (the peg), states the argument early (by the second or third paragraph), supports it with two or three strong pieces of evidence and a concrete example, takes on the best counterargument fairly, and ends with a specific call to action or a memorable final line. It is usually 600 to 900 words, in plain language, with short paragraphs and no academic hedging. Most outlets want exclusive submissions, so writers pitch one outlet at a time.
</context>

<task>
Write an op-ed within [WORD_LIMIT] words.

<material>
[ARGUMENT_AND_EXPERTISE]
</material>

<news_peg>
[NEWS_PEG]
</news_peg>

1. Sharpen the argument into one arguable sentence (a claim reasonable people could disagree with, not a truism). If the material contains several arguments, choose one and say what you dropped.
2. If no news peg is given, propose two or three plausible kinds of peg (a coming decision, a report, a seasonal moment) as `[PEG: …]` for the writer to confirm; do not invent a specific news event.
3. Write the op-ed:
   - Lede: the peg or a vivid, true example in one or two paragraphs.
   - Argument: stated plainly by the third paragraph.
   - Evidence: two or three points from the material, each with its source named in the text or marked, plus the writer's own experience where relevant.
   - Counterargument: the strongest objection, stated fairly, then answered.
   - Ending: a specific call to action (what a named decision-maker or the reader should do) or a line that sharpens the argument.
   - Bio line: one sentence on who the writer is and any relevant conflict of interest.
4. Write a pitch note to the opinion editor: subject line, two or three sentences on the peg and argument, why the writer, the word count, that it is offered exclusively, and that the full text is pasted below.
5. List every fact, figure and quote to verify before sending.
</task>

<constraints>
- Use only evidence in the material. Where the argument needs support the writer has not given, write `[SOURCE NEEDED: …]`; never invent statistics, studies or quotes.
- Stay at or under [WORD_LIMIT] words, excluding the bio; state the count.
- Plain language for a general reader: define terms, no acronyms without expansion, paragraphs of one to three sentences.
- Disclose conflicts of interest the material reveals (employer, funding, financial stake) in the bio line.
- Attack the argument, never the people on the other side; no claims about named individuals that the material does not support.
</constraints>

<output_format>
## Headline options
Three headlines (the editor will likely write their own).

## Op-ed
The piece, then the bio line, then the word count.

## Pitch note
Subject line and the email body.

## Fact-check list
A checklist with where each item appears.
</output_format>

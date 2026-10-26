---
name: human-writing
description: "Use when the user wants words written or rewritten in a human, personal voice, including short casual messages: a Slack note, newsletter intro, cover letter, email, post, bio, speech or story, with or without a pasted voice sample. Also use when a draft sounds fake, robotic, generic, corporate or \"ChatGPT-ish\", even if they wrote it with an AI, and as a final pass on anything Claude drafted that the user will send or publish as themselves. Skip code, data, translation, proofreading-only requests, legal text, and anything whose exact wording must stay unchanged."
---

# Writing like a person

People who spot machine-made prose are mostly reacting to one thing: the text is generic. It has no particular reader, no position, no real detail, and no voice. Removing "delve" does not fix that. The model swaps in another tic and the text is still generic. So this skill works on the cause. Get the missing ingredients (reader, point, real details, voice sample) before drafting, write with plain habits, and only then check for leftover tells.

Two things this skill does not do. It does not promise to pass AI detectors, and it does not remove watermarks. The research behind it (see references/evidence.md) shows detector scores say nothing about quality and keep changing, and text watermarks are statistical signals that cleanup cannot touch. Aim at writing that is specific, accurate and voiced. If the user's venue requires disclosure of AI help, they should follow it.

## Pick a mode

If the user wants something written, use write mode. If they hand over text to improve, use edit mode. If they hand over text and ask for a rewrite from scratch on the same topic, use edit mode first for the facts, then write mode.

## Write mode

Before drafting, find out what you are missing and ask for it in one short message. Do not interrogate. The things that matter, in order:

1. Who reads this and what should they do or think afterwards.
2. The one point. If the user cannot say it in a sentence, help them find it first.
3. Real material: names, numbers, what actually happened, a moment, a reason they care. This is what makes text sound lived-in. Claude cannot supply it.
4. A voice sample: two or three passages the user wrote, in the same kind of writing as this task (an email for an email, a post for a post). See references/voice-profile.md.
5. Length, channel, and any hard constraints.

If the user wants it fast, draft anyway, but never invent facts, quotes, numbers, anecdotes or first-person experiences. Where the draft needs one, leave a visible placeholder like [the number from the Q3 report] and say what is missing. Invented specifics are worse than vague ones because they get published.

Voice is not a fact, though. The no-invention rule covers what happened; it does not mean sounding flat. When the user gives a voice sample, read references/voice-profile.md and copy how they sound: their openers ("ok so"), their rhythm, how they poke fun at themselves, whether they use a title or a bold headline at all. A dry remark about a fact you were given ("the cause was dumb, which is the best kind") is voice. A made-up apology, a made-up feeling ("I'm annoyed I didn't do it sooner"), a made-up reader reaction or a made-up next step is a fact, so leave it out or put it in brackets. If the result reads more formal than the sample, redo it before you return it.

Then draft with these habits. They are positive on purpose: telling a model what to avoid mostly trades one tic for a sibling.

- Open on the content. The first sentence should carry information, not announce that information is coming.
- Prefer the specific thing to the category. Name the tool, the person, the number, the street. One concrete example beats three abstractions.
- Take a position. Say what you think and why, once. Hedge only where you are really unsure, and say what the uncertainty is.
- Use plain verbs. "Is", "has", "makes", "uses" rather than "serves as", "boasts", "facilitates".
- Let sentence length follow the content. Long when an idea needs room, short when it lands. Do not alternate on a schedule.
- End paragraphs when the idea ends. No moral, no tidy one-liner that restates what you just said.
- Stop when done. No recap, no "I hope this helps", no offer to do more.
- Write prose. Use bullets or bold only when the content is genuinely a list or a set of labeled parts.
- Skip the bold headline and the "Notes:" block unless the channel needs a title or the user asked for notes. Keep any note after the text to a line or two.
- Use the contrast move ("it is not X, it is Y") only when someone actually believed X. Use three-item lists only when there are three things.
- Match the genre. Contractions, fragments and asides are right for a blog post or a Slack message and often wrong for a grant application. See references/genres.md.

When writing as Claude, read references/claude-habits.md once. It lists the habits Claude's own models show by version, such as flattering openers, narrating what it is about to do, and closing offers.

## Edit mode

1. Read the text with the reader, genre and voice sample in mind. If you do not know the reader, ask.
2. Mark problems in this order, because the earlier ones matter more and last longer than the later ones:
   - Missing specifics: vague attribution ("experts say"), significance inflation ("a testament to"), claims with no evidence or example.
   - Structural tells: see references/tells-structural.md.
   - Assistant residue: "Certainly!", "I hope this helps", "Let me know if", closing summaries.
   - Vocabulary: see references/tells-lexical.md. Last, and only as a backstop.
3. Fix the cause, not the string. When you delete a phrase, ask what concrete thing the sentence should have said. If you know, say that. If you do not, cut the sentence or ask the user. Replacing "stands as a testament to" with "highlights" is not a fix.
4. Keep every fact, number, name and quotation. Do not add new ones, and do not drop or add a claim even if it looks inflated; flag it in the note instead. In formal writing such as an abstract or a report, change as little as possible: swap the tells, keep the author's claims and hedges. After editing, run the lint script with the original to catch dropped or added items.
5. Do not over-correct. Humans also use em dashes, triplets, "additionally" and formal grammar. Leave sentences that already work, and leave the user's own quirks alone. Their voice beats any rule here.
6. Return one usable version first, built only from facts the user supplied, so it can be pasted as is. Do not put brackets inside edited copy and do not paste the draft twice. Then, in at most three lines, say what changed and ask for the specifics that would improve it. Brackets are for write mode, where the piece cannot exist without a missing fact.

## Check with the lint script

scripts/lint.py is a plain Python 3 script with no dependencies. It reports counts per 1,000 words for patterns that cluster in machine prose, sentence-length spread, leaked artifacts, and (with --original) dropped or added numbers, names and quotes. Run it on the draft before you return it:

    python scripts/lint.py draft.txt
    python scripts/lint.py draft.txt --sample my_writing.txt --original original.txt
    python scripts/lint.py draft.txt --clean > cleaned.txt

Treat the output as a prompt for judgment. A regex cannot read intent, so a count of "tricolons: 3" may be fine in a speech and a problem in an email. When a voice sample is supplied, the report shows both columns, and the goal is to sit near the person's own numbers, not near a fixed target.

The --clean option removes real artifacts that sometimes ride along in pasted model output: leaked citation markers such as oaicite or turn0search0, private-use and tag characters, stray zero-width characters, narrow no-break spaces, and utm_source tracking parameters on links. Details are in references/hygiene.md. This is correctness and tidiness. It has no effect on statistical watermarks.

## When to hold back

- Quotations, titles, names, and anything the user said must stay word for word.
- Code, legal and contract text, medical or safety instructions.
- Text in someone else's voice that the user wants preserved.
- Languages other than English. The tell catalog is English-tuned. Say so, and apply only the principles (specific, committed, one reader).
- Very short text. Two lines of email rarely need a pass.

## If the request is about getting past a detector or a rule

If the user wants text to get past a school, employer or publisher rule against AI help, or to defeat a detector, say briefly that this skill makes writing better but does not hide where it came from, and that they should check the rules that apply to them. Then offer to improve the writing or to help them write it themselves. Do not lecture, and do not claim any score or result.

## Files in this skill

- references/tells-structural.md: ranked structural patterns, each with a positive fix.
- references/tells-lexical.md: dated vocabulary list, to use last and refresh often.
- references/claude-habits.md: habits of Claude models by version.
- references/genres.md: what changes between email, blog, marketing, academic and fiction.
- references/voice-profile.md: how to read a voice sample and write to it.
- references/hygiene.md: artifact strings and characters, and what cleanup can and cannot do.
- references/evidence.md: what the skill is based on and how strong each claim is. Read only when maintaining the skill.

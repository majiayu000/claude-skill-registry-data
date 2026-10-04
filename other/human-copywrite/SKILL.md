---
name: human-copywrite
description: "Write, finalize, or clean up reader-facing marketing and long-form copy (landing pages, sales pages, e-books, reports, case studies, product and email copy, founder notes) so it reads like a specific human wrote it and says something worth reading. Use when asked to humanize, de-slop, make less AI-sounding, rewrite naturally, tighten, polish, sharpen, clean up, or finalize copy, when asked to write the website, homepage, or landing-page copy for something built or discussed in the session, and proactively when finalizing a copy deliverable. Supports per-project voice: on 'set up my voice' or a setup argument it interviews the user and writes MY_OWN_VOICE.md, then matches it. Writes from product facts and never outputs chat history as copy, keeps the user's facts and voice, never invents proof or makes a claim more certain than the source supports. Not for code, data, changelogs, release notes, legal terms, technical reference docs, or casual chat."
---

# HumanCopywrite

Turn drafts, sketches, and half-built copy into a consumable template: clean, specific, honestly sourced, voiced, with visible placeholders where proof is missing. A human finishes the template into final prose; the output is not publish-without-review copy.

The skill has two jobs. Subtractive: keep the piece about the reader, product, offer, proof, objection, and next step, and remove everything about the chat, outline, roadmap, internal decisions, or drafting process. Additive: make the copy say something only this writer could say; clean-but-empty copy is a failure, not a pass. Both jobs are bound by one rule that outranks them: never make a claim more believable than it is true. That rule is `references/integrity.md`.

## Scope

Finished or near-finished reader-facing copy: landing pages, websites, sales pages, e-books, reports, case studies, product copy, email copy, founder notes, brand and editorial marketing copy. Not for code, raw data, tables, changelogs, release notes, legal terms, technical reference docs, or casual chat.

Every rule below applies to the entire deliverable: body, headlines, subheads, bullets, CTAs, button and link microcopy, captions, pull quotes, alt text, and footers, never body paragraphs only.

## Choose the mode

- Drafting: write new copy from the brief. Do not invent specifics the brief did not give you.
- Finalization: turn a planned or half-built artifact into a clean template. Strip scaffolding, planning residue, and wrapper text.
- Cleanup: improve an existing draft. Preserve meaning, claims, caveats, sections, and proportions unless asked for a deeper rewrite.

Use the lightest mode that solves the task; the edit bar defines exactly what the lightest sufficient edit is. The invoking prompt owns the task, format, and constraints; this skill supplies the craft and the guardrails, never a competing agenda. If `MY_OWN_VOICE.md` exists in the project root (or `.claude/`), read it before starting: it carries the project's voice, reader, product truth, verified proof, and bans (see Voice).

## The output contract

The reply contains, in this order, and nothing else:

1. The deliverable, starting at the first line. No preamble, no "here is the copy," no restated brief.
2. An editorial note after it, only when the user must act or decide. At most six short labeled lines, using only the labels needed: `Changed` (the one or two structural moves), `Verify` (claims kept that need a source before publishing), `Placeholders` (how many, where), `Flagged` (sections still clean-nothing and what would fix them), `Register` (`te` or `ön`, only when the copy is headed to Hungarian).

Example:

> Changed: opened on the reader's compliance risk instead of the feature list; merged the two overlapping proof sections.
> Verify: the "SOC 2 since 2023" line is from your draft; confirm it before publishing.
> Placeholders: 3, all in the proof section.

Two exceptions. When the piece is voice-sensitive with no sample and the user can answer, proposing voice directions first (see Voice) is a valid reply on its own. And when the deliverable is a file in an agent or editor workflow, the contract governs the file's contents; the chat reply follows the surrounding harness's norms.

Length is calibrated to the deliverable, not the effort: cleanup stays within roughly the input's length (bleed removal may shorten it; that is the job working), drafting writes to the format's natural length (a hero is a headline, a sentence or two, and a CTA), and a user-named length is hit exactly.

## The edit bar

Work in two passes. Coverage first: read the entire piece to the last line and mark every candidate issue (process bleed, AI tells, unsupported or inflated claims, empty sections, dashes, wrapper text) without filtering and without stopping early. Then apply the bar to decide what changes. The bar does the filtering, not your first impression.

Always fix, even a single instance anywhere in the piece:

- Process bleed of any kind (the eight leaks below), assistant wrapper, and signposting.
- A specific you would otherwise have to invent (a number, name, quote, testimonial, or result the source does not supply): use a visible placeholder such as `[ADD VERIFIED METRIC]`, never a plausible guess.
- Certainty inflated past the source, a dropped load-bearing caveat, or manufactured proof, scarcity, or urgency.
- High-liability claims and pressure tactics already in the draft (guarantees; medical, financial, or legal claims; income results; scarcity and deadlines): weaken, qualify, or mark inline with `[VERIFY CLAIM]` / `[CONFIRM THIS DEADLINE]`. These never ship on a Verify note alone.
- Em and en dashes (see the dash rule).
- Scaffold residue, self-praise, generic positive conclusions, and speculative gap-filling.
- Marketing buzzwords from the blocklist in `references/ai-tells.md`, unless quoted or backed by a number.

Fix only when clustered, meaning two or more catalog tells in one paragraph, or three or more within any 150-word span:

- Overused AI vocabulary, -ing analysis tails, copula avoidance, rule of three, negative parallelism, elegant variation, filler phrases, empty hedging, promotional tone, and the other patterns tagged `Bar: cluster` in `references/ai-tells.md`.

Leave alone, even when you notice it:

- A single cluster-bar tell in an otherwise specific, human paragraph.
- Anything a provided voice sample demonstrably does: punctuation habits, formality, regional spelling, favorite constructions.
- Genuine asides, self-corrections, mixed feelings, and era-bound references. These are human signals, not defects.
- The inside of quotation marks. Never edit a quote to satisfy a style rule.

A provided voice sample or brand style can override cluster-bar style items. It never overrides an always-bar item that exists for process, fact, or integrity reasons.

The moves in miniature, one example per family:

- Transcript: "We built Relay to solve this, starting with delivery inspection, then adding Slack alerts." → "Your webhook failed at 3 a.m. Relay shows which attempt, what payload, and why, and pings your Slack."
- Wrapper: "Here is the revised landing page copy you asked for. Let me know what you think!" → delete; ship only the copy.
- Empty claim: "We are committed to delivering excellence for our clients." → "Support answers in under an hour, nights included, or your next month is free."
- Inflated certainty: "Eliminates onboarding errors" (source said "may reduce") → "Designed to reduce onboarding errors. `[ADD MEASURED RESULT]`"
- Style tail: "The dashboard updates live, empowering teams and streamlining workflows." → "The dashboard updates live. You see the number move while the campaign runs."
- Dash: "One tool — every webhook." → "One tool for every webhook."

## Fact safety

Never invent or strengthen specifics: numbers, names, dates, quotes, testimonials, results, awards, certifications, logos, integrations, pricing, guarantees, or compliance and performance claims. When a useful detail is missing, leave a visible placeholder.

An ordinary specific already in the user's draft is their material: keep it as written and, when it is load-bearing proof (a metric, named customer, certification, case-study result), list it under `Verify` in the editorial note. Replace it with a placeholder only when the draft itself marks it as unsettled (a TODO, a scaffold note, a templated figure), or the user says the draft's facts are unverified or AI-generated, or the user asks for verified-only copy. Do not delete the user's real numbers to be safe; flag them. High-liability claims and pressure tactics are the exception and follow the always-fix rule above.

## Process bleed

Apply the sentence test to every sentence, headings and CTAs included:

> Would this sentence make sense to a reader who never saw the project, chat, plan, outline, prompt, or drafting process?

If not, cut it or rewrite it around the reader, product, offer, proof, objection, or next step. The eight leaks: roadmap narration, artifact meta ("in this guide," "this section explores"), conversation residue ("as discussed," "per your request"), decision disclosure ("we landed on"), effort padding ("after extensive research"), scaffold residue (phases, TODOs, outline labels), self-praise ("comprehensive," "carefully crafted"), and the transcript transplant (below). Full examples and fast-scan phrases: `references/process-bleed.md`.

## Website prose: source, not transcript

Asked for site copy at the end of a working session, never output the session. The chat, the codebase, and the README are material to mine for facts, not a manuscript to edit; narrating what "we built," in the order it was built, is the transcript transplant, the whole-page form of process bleed. The tell is chronology: sections that mirror the build order instead of the reader's questions (What is this? Will it work for me? Can I trust it? What now?).

Instead, fill the source sheet from whatever context exists, then write from the sheet: reader, problem, product in one sentence, mechanism, verified proof, main objection, next step. An empty slot becomes a visible placeholder, never a guess. `MY_OWN_VOICE.md`, if present, pre-fills reader, product truth, and proof. Page patterns (hero, features with "so that" chains, proof, FAQ, About, pricing) and the worked transplant example: `references/website-copy.md`.

## Make it worth reading

Removing slop leaves a gap; fill it from the true material, never from an impressive guess. Four tests catch clean nothing:

1. Swap test: could the sentence sit unchanged in a competitor's copy? Then it carries no information; replace it with the mechanism, number, tradeoff, or named user that is only true here.
2. Negation test: would anyone claim the opposite? "Committed to quality" is empty; make a claim a real competitor might refuse to make.
3. So-what ladder: ask "so what?" of each fact until you reach the consequence the reader can act on or feel, and lead with that.
4. Real question: answer the question under the stated one, usually about risk, status, or effort.

Earn the claim by showing the mechanism that makes it true; demonstrated beats declared. Keep the tension: name the hard part, the limit, who the product is not for. Substance sharpens the user's point, never swaps in yours: if landing a line would change what the user is claiming, flag it instead. When the substance is genuinely missing, flag the gap with a placeholder; do not manufacture it. Full moves and worked examples: `references/substance.md`.

## Do more good than harm

Everything above makes copy more persuasive, and persuasion lands a false claim as well as a true one. These rules outrank the rest:

- Persuasion never outruns evidence. Clearer is allowed; more certain, proven, universal, or specific than the source is not. Watch quiet escalations: "may reduce" to "eliminates," "some users" to "everyone," "in our test" to "guaranteed."
- Load-bearing caveats survive every edit. Cut empty hedging, never a safety, legal, financial, or genuine-uncertainty qualification.
- Never manufacture authenticity: no invented reviews, testimonials, social proof, scarcity, or urgency, and no words in a real person's mouth. Missing proof becomes a placeholder.
- Do not help disguise authorship where disclosure is expected (academic, regulated, or attested work); improve honest writing instead, and say so plainly when a request is really about hiding who wrote it.

The standard: a reader who trusts this copy because it is clear and human should be safe in trusting it. Full treatment: `references/integrity.md`.

## Human prose and dashes

Specific beats generic; use the source's real names, numbers, mechanics, and tradeoffs. Vary rhythm at both levels: mix short sentences with longer ones, and vary paragraph weight too; uniform mid-length cadence and sustained staccato fragments are both tells. Plain beats inflated: prefer is, has, does, gives, costs, saves over serves as, boasts, leverages, facilitates, underscores. Read it aloud in your head; if you would not say the sentence to a colleague, rewrite it.

No em or en dashes anywhere in final copy: body, headings, bullets, CTAs, and captions alike. Replace each with a period, comma, colon, parentheses, or a restructured sentence. A single dash gets fixed. Keep one only inside an exact quotation, on explicit user preference, or in an established brand voice; never misquote a source to satisfy this rule.

## Voice

A provided writing sample, brand voice, or style guide beats this skill's default taste: match rhythm, vocabulary, formality, directness, humor, openings, and closings, across the whole deliverable including headlines and microcopy. With no sample, default to grounded, concrete, direct, and mildly opinionated where the format allows, and pick the register this format and reader call for rather than one house style across projects.

When the piece is voice-sensitive, no sample exists, and the user can answer: offer two or three one-line voice directions (a posture plus the opening line rewritten in it) and build only the chosen one. When immediate output was requested, write in the grounded default and name the direction taken in the editorial note. Full move: `references/voice-calibration.md`.

Project voice. When the user invokes the skill with a setup argument (`/human-copywrite setup`) or asks to set up their voice or brand voice, run the interview in `references/voice-setup.md` and write `MY_OWN_VOICE.md` to the project root. On every later copy task in that project, load the file: its samples count as the provided voice sample, its verified proof may be stated as fact, its bans are always-fix, its caveats survive every edit. It overrides taste, never the integrity layer.

## Working through a piece

Substance and integrity work is multi-step reasoning: before writing or rewriting, think through who the reader is, the real question under the stated one, the so-what ladder, and which claims the evidence can carry. Mechanical cleanup of a short piece needs no deep pass; make the edits directly.

Drafting or finalization: fill the source sheet (reader, problem, product, mechanism, proof, objection, next step); think first; write the deliverable only, to the format's natural length; sweep the whole draft against the sentence test, the edit bar, fact safety, voice, and the dash rule; run the harm check; deliver per the contract.

Cleanup: coverage pass over the whole piece; bar pass; rewrite preserving meaning, claims, caveats, and proportions; sharpen or flag surviving clean-nothing sections; re-read the result against the checklist below; deliver per the contract, noting any structural removals in the editorial note.

## When to load references and run the scanner

Load each file at the moment its trigger appears, not preemptively and not never:

- `references/ai-tells.md`: before the bar pass on any cleanup longer than roughly 300 words, and whenever you are unsure how to tag a tell. For short snippets the bar lists above suffice.
- `references/website-copy.md`: before writing or restructuring website or page copy, especially copy requested at the end of a working session.
- `references/voice-setup.md`: when the user asks to set up their voice or invokes the skill with a setup argument.
- `references/substance.md`: before rewriting a piece judged clean but empty, and before drafting from a thin brief.
- `references/integrity.md`: when an edit would make a claim more convincing, when copy touches health, money, safety, or legal territory, or when scarcity, urgency, or social proof appears.
- `references/process-bleed.md`: when bleed survives a first pass or the piece heavily narrates itself.
- `references/voice-calibration.md`: when a sample or brand voice is provided, or the piece is voice-sensitive with none.
- `references/qa-scorecard.md`: when asked how ready the copy is, and before shipping long or high-stakes pieces.
- `references/translation-handoff.md`: when the output is headed to Hungarian.

When you can execute scripts, run `python scripts/copy_scan.py draft.txt` on deliverables over roughly 600 words and on multi-section pieces before shipping. Treat it as a scanner, not a judge: its hits are candidates for the bar, and its silence proves nothing about substance. Without script execution, do the coverage pass manually and never claim the scanner ran.

## Pairing with translation

When the output must be Hungarian, humanize in English first, then chain to `translating-english-to-hungarian`: sketch, to English template (this skill), to native Hungarian (that skill), to final prose (a human). Pass the register (`te` casual, `ön` formal; the translator defaults to `ön`), leave placeholders untranslated, and carry the integrity rules across: the Hungarian must not read more certain than the English. Hungarian typography wins in the translated output. Full handoff: `references/translation-handoff.md`.

## Before shipping

Re-read the complete deliverable from first line to last and check every item against every section, headings and CTAs included; fix any failure and re-check that item:

- No sentence refers to the chat, request, plan, outline, internal decisions, or drafting process, and no section order mirrors the session's timeline.
- Every paragraph serves the reader's situation, the product, the offer, proof, an objection, or the next step.
- No section is clean nothing; the strongest lines pass the swap and negation tests.
- No specific was invented or strengthened; missing ones are visible placeholders, and kept load-bearing claims are listed under Verify.
- No claim is more certain, proven, or universal than the source supports; every safety, legal, or financial caveat is intact; no proof, scarcity, or urgency was manufactured.
- The voice matches the sample or the format, everywhere in the piece.
- Em and en dashes are gone unless a stated exception applies.
- Read the finished piece cold, once, and ask: what would still make a reader clock this as AI? Fix what you find.
- The reply follows the output contract: deliverable first, labeled note after only if needed, nothing else.

## References

- `references/process-bleed.md`: the eight leaks, examples, fast-scan phrases.
- `references/website-copy.md`: the source sheet, the transcript-transplant fix, framework selection by reader awareness, page patterns.
- `references/substance.md`: the intelligence layer, with tests and worked examples.
- `references/integrity.md`: the do-more-good-than-harm layer.
- `references/ai-tells.md`: the tell catalog, every item tagged with its edit-bar level.
- `references/voice-setup.md`: the MY_OWN_VOICE.md interview, template, and loading rules.
- `references/qa-scorecard.md`: score finished copy before shipping.
- `references/voice-calibration.md`: voice matching and the propose-directions move.
- `references/translation-handoff.md`: chaining with `translating-english-to-hungarian`.
- `scripts/copy_scan.py`: heuristic scanner for long drafts.

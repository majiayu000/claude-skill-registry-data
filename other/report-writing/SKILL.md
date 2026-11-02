---
name: report-writing
description: Write or edit a findings report, audit, or technical write-up (not a chat reply) with zero narrative/meta bloat. Use whenever producing a standalone document meant to be read on its own — a codebase audit, an investigation write-up, a proposal doc — or when asked to trim/tighten one that already exists.
---

Apply these rules to every report-style document. They come from repeated, explicit corrections a user made while iterating on a real audit report — each rule below is what that correction generalizes to. This is a writing discipline, not a checklist to run once at the end: apply it as you draft, not just as a final pass.

## Rules
0. THIS IS TRHE MOST IMPORTANT RULE: CONSICENESS IS THE MAIN PARAMETER FOR CORRECTNESS. ALWAYS PROVIDE THE LEAST TEXT AS POSSIBLE. BETWEEN TWO OR MORE OPTIONS, ALWAYS CHOOSE THE LESS VERBOSE. 
1. **No meta-commentary about the document itself.** Never explain the report's own purpose, structure, formatting convention, or rigor ("every item below cites a file/line", "this section follows the same shape: X, then Y, then Z"). State findings. A reader infers a repeated pattern after seeing it once or twice — don't caption it.
2. **Never echo the requester's instructions back as content.** If someone asked you to write the report a certain way, that instruction is process, not a finding — it does not belong in the delivered text.
3. **No redundant restatement.** If a clause just repeats what the previous clause already implied, cut it. Read every sentence and ask "does the second half say anything the first half didn't already establish?"
4. **No hedging or intensifying filler.** Cut words/phrases that don't change the truth value of a claim ("by billions of times", "(for discussion, not decided here)", "clearly", "obviously"). If removing a phrase loses no information, remove it.
5. **Single source of truth per fact.** A status (fixed/open/done) lives in exactly one place — a table, a header, wherever you designated as canonical. Don't repeat it in narrative prose elsewhere in the same document.
6. **One topic, one section.** Never split a single topic across multiple sections, and never nest sub-headers inside a section when a flat list would do. If you find yourself merging two sections that overlap, actually merge the content — don't leave one nested inside the other.
7. **Headings name the subject only.** No appended status, mechanism, or verdict via a dash-clause ("Storage — confirmed open gap", "Stores — structural equality via X"). That detail goes in the body.
8. **A proposal section contains only the proposal.** Never narrate what changed while you were writing the document ("Done, since this was first written: ..."). The document must read as authored fresh — independent of the conversation that produced it — not as a session transcript.
9. **Speculative/forward-looking content stays at the level of the general category.** When asked for "what else could go wrong," name the applicable general risk class and stop. Don't invent specific unverified hypothetical scenarios (a particular function misbehaving on a particular edge case you haven't checked) just to fill out a section — that manufactures false specificity.
10. **Verdict/decision lists lead with the verdict.** State adopt/reject (or fixed/open, or yes/no) first, then exactly one line of justification. Cut elaboration, alternatives, and caveats unless they would change the verdict.
11. **Write full sentences, not label-fragments.** A bold category label glued to a clinical sentence fragment ("**General.** A native, type-unaware call sitting at a boundary...") reads worse than a plain sentence — and often the label itself is redundant with what the sentence already conveys. If a plain sentence already makes its own category obvious, drop the label.
12. **No editorializing closers.** Cut sentence-final asides that validate or approve a decision without adding information ("...and it should stay that way", "this was the right call"). The recommendation already implies this; don't say it twice.
13. **A caution/warning aside is one short sentence, not an argued case.** When flagging an approach to avoid ("don't do X"), state the alternative and why in a single clause. Cut the itemized cost list (affected libraries, contributor mental models, unrelated code sites) that turns a one-line warning into a defended essay — if the reader needs that much convincing, the recommendation itself is probably wrong, not under-argued.
14. **Re-verify before finalizing.** A claim written earlier in a long editing session must be checked against the current actual state (code, data, whatever the report is about) before the document is considered done. If something changed or you learn you were wrong, correct or remove the claim — don't just leave it standing because it was already written.

15. **Never use the em dash.** The character `—` is banned from the document. Use a comma, a colon, parentheses, or two sentences.

## How to self-check a draft

Before treating a report as finished, reread it section by section and ask, per sentence:
- Is this a finding, or is it commentary about the report?
- Does this repeat something already said (here or in a table elsewhere in the doc)?
- Would deleting the last clause of this sentence lose any information?
- If this is a heading: does it contain anything other than the subject name?
- If this is a "possible/future risk" bullet: is it a general class, or did I just invent a specific untested scenario?

If a report is being *edited down* rather than written fresh, prefer deleting whole sentences/clauses over rewording them shorter — bloat is usually a sentence that shouldn't exist, not a sentence that's merely too long.

---
name: streamline-text
description: Edit prose for brevity and scanability without losing facts. Use for requests to "revise", "rewrite", "edit", "polish", "clean up", "clarify", "simplify", "condense", "tighten", "shorten", "streamline", "de-fluff", remove bloat/repetition or unnecessary newlines, fix spelling/typos without changing meaning, make text concise/compact/skimmable, or finalize drafts, messages, notes, docs, reports, issues, or reviews. Activate for "too verbose", "very verbose", or "remove unnecessary newlines", and proactively when text is verbose, wordy, meandering, dense, hard to scan, or has duplicates, vague claims, undefined terms, or cold-reader problems. Preserve evidence, qualifiers, requirements, commands, numbers, and scope with a fact index and restore/cold-reader audit. For public Reddit, Hacker News, social posts, or release notes use social-media-writing; for PRs use write-maintainer-ready-prs; pair with avoid-ai-isms when text sounds generated.
metadata:
  version: 0.17.0
---

# Streamline Text

<purpose>

Make a document shorter and clearer while provably losing no required fact. Correctness before brevity: trimming a wrong sentence produces a shorter wrong sentence, so verify claims before compressing them.

## Companion skills

| Need | Skill |
|---|---|
| Shorten prose while provably keeping every fact | this skill |
| Remove the writing tells that mark prose as machine-drafted | `avoid-ai-isms` |
| PR titles, descriptions, and replies to a maintainer's review | `write-maintainer-ready-prs` |
| Reddit, Show HN, release notes, platform norms | `social-media-writing` |

Shortening and de-slopping are separate jobs. A draft can be tight and still read as generated,
and a draft with every flagged word removed can still carry three paragraphs of nothing.

Order: this skill's passes for the facts first, then the `avoid-ai-isms` checks for the tells,
then this skill's restore pass again if removing tells cut anything. Apply the `avoid-ai-isms`
carve-outs during its pass so neither job strips a precise hedge or a scope qualifier.

</purpose>

<workflow>

## How It Works

Run these as separate passes. Combining them is how facts get lost. When the requester names specific edits, make those, and report anything else you find as a separate observation instead of folding both into one pass.

1. **Preserve.** Keep a recoverable pre-edit copy (backup beside the file, version control, or an existing prior draft). Skip only when a recovery point already exists. Stamp backup filenames with the full datetime (yyyy-mm-dd-hhmm) so same-day backups stay ordered; a bare date leaves them indistinguishable.
2. **Index every fact before touching a word.** Write the index to a scratch file (session scratchpad or a temp file beside the work, not committed): one atomic fact per line, stated exactly, completely, and in the fewest words that keep it correct.

   The index fails in two directions. A cheap facsimile (an index line reading `the document's rule 20 pairs cost with benefit`) has already dropped the detail you are about to lose, so it cannot detect the loss. A copied quote fails differently: it reproduces prose without decomposing it, so one line carries four facts and stays marked present while a qualifier inside it changes. Index the facts; do not summarize the prose and do not copy it.

   Decompose until each line holds one fact, and stop only when no fact is left unindexed. Record these as facts in their own right, because they are what both failure modes discard: qualifiers and scope conditions (`exactly`, `only`, `at least`, `either or`, applies when the deliverable is the PR text), obligation modals (`may`, `must`, `never`), named actors (reviewers, the maintainer, you), units, defaults, commands, and each separate instance of a repeated example.

   One sentence, indexed as four lines:

   - every capability price names a refund command
   - refund command is exact, not approximate
   - paired benefit is the measured benefit of that same switch
   - cost lacking either the benefit or the switch counts as overhead

   Flag facts you cannot verify in the index now rather than compressing them into confident prose later. The index is the contract for the edit: streamlining changes how facts are said, never which facts exist, except by conscious decision.

3. **Clean up, document level first.** Reverse-outline before touching sentences: name each section's one job, then delete or relocate content that serves a different section's job, duplicated passages, and throat-clearing openings that warm up without saying anything. Then delete sentence-level content that cannot change what the reader does next: tautologies, workflow narration ("I then updated the file"), document-meta narration that talks about the document instead of its subject ("Reading the table", "as reported throughout", "listed in section N"; state the fact itself where the cross-reference stood), restatements of the obvious, private paths and session identifiers, stale claims, vague intensifiers ("comprehensive", "robust", "significantly"), and counts that name no counted thing.
4. **Streamline.** Reorder by what the reader needs first, merge duplicated statements, shorten sentences, and keep each claim adjacent to its evidence or consequence. Sentence mechanics that shorten without loss: turn nominalizations back into verbs ("perform validation of" becomes "validate"), cut expletive openers ("there is", "it is ... that"), collapse chained prepositional phrases, keep each subject next to its verb, and merge a sentence that only re-states part of its predecessor. When a sentence resists trimming, ask "what do I really mean here?" and write it fresh instead of whittling.
5. **Restore by cross-check.** Walk the index line by line, confirming the result still asserts that one fact with its detail intact, and mark each line present, merged into another sentence, or consciously dropped with a stated reason; no fourth state and no unmarked lines. Marking a line present because the result still covers the topic is not a check: the check is whether the specific qualifier, modal, actor, unit, or example on that line survived. Where statements about different measurements or sources were merged, confirm the merged sentence's quantifiers and referents still match each original; paraphrase is where numbers silently swap. Then diff against the preserved copy for anything the index itself missed. Then check your context: the surrounding conversation, the request that produced the document, and linked sources often contain requirements the document never wrote down; restore those too. Never restore a stale or disproven claim.
6. **Reread whole.** Read the full document start to finish once more; check heading order, transitions, table placement, and that every conclusion still sits beside what supports it. If the format renders (markdown tables, links, a table of contents), inspect the rendered result, not only the source. A clean pattern check is not a clean document: the rules that matter most describe rhetorical moves no fixed pattern captures, so read the prose itself before reporting a pass.
7. **Diff-verify against the pre-edit version, then fix.** Read the complete diff between the preserved copy and the result (under git, `git diff` on every touched file; `git diff --word-diff` exposes exactly which words changed inside long lines). Walk every removed segment and match it to a conscious decision in the index; a removal with no matching decision is a regression, found now rather than by a reader. Hunt the diff-specific failure forms the earlier passes cannot see: a replace-all that fired outside its intended scope, an edit that landed in a generated or derived file instead of its source, a deletion that took a neighboring sentence with it, a merged sentence whose quantifier or referent silently widened, and characters corrupted by editing: scan for anything outside the document's expected character set, because fused or broken glyphs look fine in the source and render wrong. Then run a fix round for everything found, and re-run this pass on the fix diff until it comes back clean; a fix round that itself goes unverified is how regressions survive review.

</workflow>

<requirements>

## Keep the artifact free of process residue

These constraints govern the artifact being edited, the document, message, or file itself, not your report to the person who asked. The artifact ships to a reader who never saw the request, so nothing about the request may survive in it.

1. **No instruction bleed.** The artifact carries no prompt text, system directive, rule name, or command keyword from the request that produced it. A brief that says "make it skimmable and cut the hedges" leaves no trace of those words in the result.
2. **No meta-talk.** Delete openers that announce the text instead of being it: "Here is the edited version", "This document explains", "In this section we will". The artifact starts at its first real fact.
3. **No reasoning leakage.** Scratchpad notes, alternatives considered, self-assessment ("this reads better now", "I chose X over Y"), and confidence commentary belong in your reply to the requester or in a notes file, never in the artifact.
4. **No echoing.** Do not restate or paraphrase the instructions inside the result. An artifact that describes what it was told to be is shorter and more useful when it simply is that.
5. **Target content only.** When the request is for the text itself, deliver exactly the text, nothing wrapped around it.

When the deliverable is a file, apply these to the file and put your commentary in the conversation. When the deliverable is the message itself, the message is the artifact and the same rules apply to it.

## Rules that decide individual cuts

1. **The distinguishing fact goes first** in every sentence, cell, and section. Readers and truncation take the head and drop the tail.
2. **Measure, do not guess.** Compare length against what the audience actually reads (an accepted document of the same kind, a house style, a template). Justify every section that exceeds that ceiling by facts it alone carries. The measurement is a diagnostic, not a target: padding short text and gutting long text are both damage.
3. **Every count states what it counts, and its unit is a defined procedure.** "3/3" and "7,204 tests" are noise until the sentence names the counted event, the condition, and what passing means; and a count of "runs", "checks", or "cases" is still empty until the unit names its procedure ("3 repetitions of the same edit-reindex-compare sequence", not "3 runs"). Define the unit once, adjacent to its first count, then reference it. If you cannot say what a count counts, the measurement itself is underdefined: fix the measurement or its report, not just the sentence.
4. **A measured claim carries four facts**, mirroring how a parameter description states what it selects, its range, its notable values, and the corrective action: the measured event or procedure, the workload and conditions, the number with its unit, and the direction (what better means here). Drop any one and the number becomes guessable rather than checkable.
5. **Copy numbers from their source of truth.** Retyping figures from memory or an earlier draft is how they drift; take them from the generated report or measurement output, and refresh from that source whenever it regenerates.
6. **Report measurements to the precision the variability supports.** Publish only the digits repeated measurements agree on; when they disagree, state the range, attribute the variance, and headline the conservative end. Digits beyond the spread are false precision; a stable measurement keeps its full measured precision.
7. **Name every entity the text scores or refers to.** Go sentence by sentence: any entity referred to but never identified ("the required result", "the central workflow", "the failing case", "the known answer") gets a name or a description concrete enough that a stranger knows what it is. A metric gloss must name the measured entity too, not only the formula: "Pair F1 1.000" is unverifiable, while "F1 1.000 over the judged SEMANTICALLY_RELATED code-entity pairs, none missing and none spurious" says what was scored and what perfect means.
8. **State the concept, not only an example.** A reader takes an example as the whole universe, so every example must sit beside the rule it illustrates, stated explicitly; the example is one case of the rule, never the rule's limit. This applies to this document too. The converse holds when a specific incident teaches a rule: write the rule at the level of generality the principle supports and keep the incident as one labeled example ("report to one significant figure" was one case of "match precision to measured variability"); a fix promoted verbatim to a universal rule misfires outside its original context.
9. **Never cut a required fact:** an accepted value, a default, a unit, a cost, a limitation, an interaction, a command the reader must run, or the one number a claim rests on.
10. **Restatement is not automatically duplication.** It earns its place when the reader will not have the other copy in front of them (a table cell read without its section, an error message read without the docs). The test is "will the reader have the other copy visible?", not "do the words appear twice?".
11. **Replace jargon and invented shorthand** with the concrete behavior, or gloss it at first use. Project vocabulary reads as ordinary English to a newcomer and silently misleads.
12. **The passive voice can silently delete the actor.** "The database was replaced" loses who replaced it; if the actor matters (attribution of a fix, blame for a defect, who runs a step), name it in active voice. Shortening into the passive is a fact cut wearing a style change.
13. **Scope qualifiers are facts, not hedges.** "On macOS", "for this workload", "median of three" bound a claim's validity; cutting them silently widens the claim. Cut empty intensifiers freely, never validity bounds.
14. **One name per concept, everywhere.** Rotating synonyms for variety ("experiment", "run", "campaign" for the same thing) reads as different things to a newcomer; pick one name and repeat it. Repetition that carries identity is cohesion, not wordiness.
15. **Number lists rather than bulleting them**, so a reader can cite item 4 instead of describing it. Reserve dashes for items nobody will reference.
16. **Frame rules and claims positively where possible.** Lead with what to do or what is true, keep the pitfall as trailing rationale, and avoid double negatives; a reader untangling "not un-X" misreads it. Good: "separate two values with a semicolon; a slash reads as division". Bad: "never separate two values with a slash". Reserve prohibition-first framing for cases where the mistake is the point, such as a banned-word list.

## Cold-reader audit

After streamlining, read each section as a newcomer holding nothing else; sections are skimmed independently and out of order. You cannot detect an unstated assumption using the knowledge that makes it invisible, so check each term against the text itself, not against what you know. Check the sentences you just wrote hardest of all: fresh edits reintroduce exactly these failure forms, because the writer holds the missing context while writing. Hunt five failure forms:

| Form | Example | Why it breaks |
|---|---|---|
| Forward reference | a term used before the section that defines it | The reader has no model to attach it to |
| Undefined term | project vocabulary reading as plain English | The reader assumes the ordinary meaning |
| Dangling deixis | "this result", "as above", "the same way" | No antecedent survives skimming |
| Assumed reading order | "unlike the previous section" | Sections are read individually, in no fixed order |
| Assumed access | "see the internal doc" without a path or link | The reader may hold neither |

## Sentence-level checklist

For every remaining title, sentence, bullet, row, and label ask:

1. What exact fact does this convey?
2. Is the referent clear to a newcomer?
3. Can it be shorter without losing a fact?
4. Does another sentence already say it, and will the reader have that copy visible?
5. Does it follow from the preceding sentence and belong under its heading?
6. Is every term, metric, subject, and reference introduced before use?

</requirements>

<examples>

## Examples

Before (40 words): "We then ran the comprehensive test suite, which significantly improved our confidence, and all of the 3/3 checks passed successfully, demonstrating that the robust new implementation is working as expected across the various configurations that we tested during this effort."

Index (three facts, all flagged unverifiable as written): a test suite ran and passed, but which suite and how many tests; something passed 3 of 3, but 3 of what checks; more than one configuration was tested, but how many and which.

The flags force a trip to the underlying reports, which supply the missing values. After (27 words): "The full C suite (7,213 tests) passed, and the clean-rebuild equality check passed all 3 repetitions of its edit-reindex-compare procedure on each of the 4 tested configurations."

Accounting for every index line: all three facts survive, each now naming what its count counts, with the precise values supplied by verification rather than invented from the original. The intensifiers ("comprehensive", "significantly improved our confidence", "robust", "as expected") carried no facts and were dropped consciously.

## Failure modes this skill exists to prevent

1. Brevity that trades away precision on the special case (shortening "0 or greater" to "positive"): a regression, not an improvement.
2. Deleting a restatement whose other copy the reader never sees.
3. Cutting the disclosed loss or limitation while keeping the win, which turns an honest document into a misleading one.
4. Streamlining before fact-checking, which locks wrong claims into confident prose.
5. Skipping the restore pass and only noticing the lost fact when a reader asks.

</examples>

<resources>

## Scripts

`scripts/number_lists.py` converts dashed markdown lists to numbered lists in place; run it with `--help` for usage and caveats, and review the diff afterward.

Script whatever benefits from exactness or scale, then read for judgment: a clean script proves what it matched, never that the argument holds.

## Sources

Provenance for every rule here, with what each source confirmed: `references/sources.md`.

</resources>

---
name: strip-ai-tells
description: "Rewrites AI-sounding prose until it reads as human-written. Use this skill when a draft reads like AI wrote it: em dashes, negative parallelism, empty intensifiers, and filler triads."
user-invocable: true
---
# Strip AI Tells

## When to Use

The user wants prose that reads as human-written.
Typical phrasings are "strip the AI tells", "de-AI this", "make this sound less like AI", "remove the em dashes", "this reads like ChatGPT wrote it", and "humanize this draft".

This is not a proofread: spelling, grammar, and punctuation stay out of scope.
Change word choice and sentence shape, nothing else.

## Scope

Work on the whole document by default.
Restrict the pass to a section when the user has selected one or named one, and say which range you worked on.

## Make the Edits Reviewable

Turn on the editor's change tracking or revision mode before the first edit, when the environment has one, so the user can see and reject every rewrite.
Say in one line that you turned it on.
Never turn it off afterward.

A plain file under version control needs no extra step, because the diff already serves that purpose.
Read [Word and Office JS Mechanics](references/word-office-js.md) for the calls this step and the formatting checks below need in a Word Office JS session.

## Inventory Before Editing

Count each pattern in scope before changing anything.
The document text is usually already in context, so do not re-read it just to count.

- **Em dashes**: every one, doc-wide.
- **"Not X but Y" parallelism**: including "rather than", "instead of", "it's not just X, it's Y", and "not merely".
- **Empty intensifiers**: genuinely, actively, deliberately, organically, truly, simply, seamlessly, robustly, holistically.
- **Triads and filler**: three-item lists where two carry the meaning, plus "at minimum", "from day one", "going forward", "alike", "that said", and "it's worth noting".

Note the following without fixing them yet: jargon repeated past usefulness, such as the same coined phrase five times; unsupported specificity, such as "in seconds" or "within the first hour"; and any sentence built on a metaphor that does not survive a second reading.

**Done when:** you have a per-pattern count to compare against later.

## Rewrite

Work section by section.
Make one edit per changed phrase, and batch related phrases into a single search-and-replace pass only when there are many.

- **Recast each em dash by what the join is doing.**
  Use a period when the halves stand alone, a colon when the second half explains the first, parentheses for a true aside, and a comma for apposition.
  Replacing all of them with the same mark is its own tell.
- **Vary the replacement.**
  If "rather than" is carrying every contrast, half the sentences now share a rhythm.
  Rotate through "not", "instead of", and plain subordination, or drop the contrast entirely.
- **Keep the replaced span minimal.**
  Change the words that need changing plus enough neighbors to make the match unique.
  Editors cap the length of a search string, so a long paragraph needs a distinctive fragment, never the whole thing.
- **Preserve meaning.**
  Dropping "deliberately" is fine.
  Dropping the clause it modified is not.
- **Never type list bullets or heading numbers into replacement text.**
  The document's list and heading formatting generates them, so typing them by hand produces a doubled marker.

**Done when:** every counted instance in the section is resolved or consciously kept.

## Watch for Formatting Leaks

Replacing a span inherits the formatting at the start of the range and flattens whatever was inside it.
Check each batch against the following before moving on.

- **Bold bleed**: replacing text that starts inside a bold run, such as a bold list label, makes the whole insertion bold.
  Clear bold on the portion that should not carry it.
- **Lost code font**: inline monospace tokens inside a replaced span come back in the body font.
  Find each token, compare its font against a surviving instance, and restore it.
- **Apostrophe and quote style**: match the document's existing style.
  Search a known word with a straight apostrophe and again with a curly one; whichever matches is the house style.
  Use it in every insertion.
- **Inserted paragraphs**: when you add a sentence or a paragraph, copy the font, size, color, alignment, and spacing from a sibling paragraph of the same role.
  Do not rely on the style default.

**Done when:** reading the batch back shows the same fonts and weights as before the edit.

## Re-Scan Until a Pass Finds Nothing

Re-run the inventory over the rewritten text, counting the phrases you introduced as well as the ones you set out to remove.
Fix what the pass turns up, then run it again.
Stop when a complete pass over scope produces zero findings, not after a fixed number of rounds.

**Done when:** a full pass finds nothing to change.

## Verify, and Verify the Verifier

Run whatever visual or rendered verification the environment offers.
A tool that inspects a rendered or extracted copy reports predictable false positives, so fix only what you can confirm against the document's real properties.

- A lost hyphen on a word that wraps across a line is an extraction artifact, and the hyphen is still in the document.
- A hard line break reported mid-paragraph is usually ordinary justified wrapping.
- For a font, color, size, or spacing complaint, read the property off the paragraph and off a sibling before changing anything.
  Matching values mean the finding is wrong.

**Done when:** every reported defect is either fixed or shown to be an artifact.

## Report

Keep the report to two short parts.

- One line of counts: which patterns came out, how many of each, and how many passes it took.
- A flag list of the substantive problems you did not change, one line each with its location: broken cross-references, claims the document cannot support, jargon repeated past usefulness, and structural inconsistencies between parallel sections.

Never silently fix a factual or structural problem found during a prose pass.
A wrong section reference or an unsupported performance claim gets flagged for the user, not corrected on your own judgment.

**Done when:** the user has the counts and the flag list.

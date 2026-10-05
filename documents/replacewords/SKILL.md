---
name: replacewords
description: Replace sentence-by-sentence revised or paraphrased text back into an original paper or document while preserving the original formatting, typography, paragraph settings, citation layout, and document conventions as the source of truth. Use when the user provides revised text that maps back to original sentences, paragraphs, sections, or the whole document, but may also contain clear local sentence merges or splits, and asks to replace it back into the source, keep the original formatting, do sentence-by-sentence replacement, preserve original formatting, or only swap wording without rewriting the document. Only allow minimal edits to the rewritten text when fixing citation formatting, restoring protected original content, restoring the original person reference, or minimally splitting/merging text back into original sentence slots; otherwise do not improve grammar, style, logic, or wording.
---

# Replacewords

## Overview

Use this skill to take rewritten text that was made from the original paper's sentences, paragraphs, sections, or full text and replace the original wording while keeping the original document's formatting and conventions intact. Treat the original text as the standard for position, run-level formatting, typography, paragraph settings, citation style, person reference, and document structure.

Preserve the original file type whenever feasible. If the source artifact is a native office file, the default output should remain in that same native format rather than silently degrading to plain text.

## Core Standard

Follow these rules in order:

1. Treat the original text as correct.
2. Create a new working copy from the original before making any replacements, and keep the original unchanged unless the user explicitly requests otherwise.
3. Create that working copy in the same directory as the original file by default.
4. Name that working copy by keeping the original filename stem and replacing any old replacement suffix such as `-replaced` with the current date as a trailing suffix in `YYYY-MM-DD` format before the extension, for example `paper-2026-04-15.docx`.
5. If the same-directory date-suffixed filename already exists, append a minimal numeric suffix instead of overwriting it, for example `paper-2026-04-15-2.docx`.
6. If the original artifact is `.docx`, default both the working copy and the final deliverable to `.docx`.
7. If the original artifact is `.pptx`, default both the working copy and the final deliverable to `.pptx`.
8. Only fall back to plain text or markdown when the current environment truly cannot produce or safely edit the required native format, and state that limitation explicitly.
9. Replace only the text content that the user intends to swap.
10. Preserve the original location, formatting, typography, paragraph settings, numbering, emphasis, citation placement, punctuation style, and surrounding structure unless one of the allowed fixes is required.
11. Preserve protected formatted content from the original, especially italicized works/titles/names and superscript content, even if the rewritten text changes or omits them.
12. Preserve protected factual and reference content from the original, including names, numbers, identifiers, abbreviations, and cross-reference markers, even if the rewritten text changes them.
13. Assume the rewritten text exists only to replace the original wording in the same source slots, not to improve writing quality.
14. Never "polish" the rewritten text for fluency, grammar, style, precision, tone, or academic quality.
15. Because this skill's default purpose is source-based replacement, assume the provided rewritten text was made from the original sentence, paragraph, section, or whole document unless the user says otherwise. Treat noisy factual, citation, table/figure, or cross-reference drift as a recoverable alignment problem first, not an immediate stop condition. Map the rewritten text back to original slots, restore protected original content, and stop only if the mapping remains unrecoverable after that reconciliation attempt.

## Native File Output Rule

Native format preservation is the default, not an optional enhancement.

- If the original file is `.docx`, the default final output must be `.docx`.
- If the original file is `.pptx`, the default final output must be `.pptx`.
- The skill should preserve the original file type in both the working copy and the saved final artifact whenever the source file and current environment make that possible.
- The working copy should be created in the same directory as the original file by default.
- The working copy should keep the original filename stem and append the current date as a trailing suffix in `YYYY-MM-DD` format before the extension whenever feasible.
- If that date-suffixed filename already exists in the same directory, append a minimal numeric suffix instead of overwriting the existing file.
- Do not silently downgrade a document or slide replacement task into markdown or plain text merely because text replacement is easier.
- Only if the current environment truly cannot produce or safely edit the native format may the skill fall back to markdown or plain text, and that limitation must be made explicit in the final response.

## Native Style Fidelity Rule

Formatting preservation means inheriting the original document's style settings, not merely approximating them.

- Reuse the original styled container, paragraph, run, shape, or text box whenever feasible instead of recreating content with default styles.
- Preserve typography from the original, including font family, font size, bold, italics, underline, color, highlight, small caps, superscript, subscript, and character spacing when present.
- Preserve paragraph settings from the original, including alignment, left and right indent, first-line or hanging indent, tabs, line spacing, spacing before and after, numbering level, bullet style, and keep-with-next style behavior when present.
- Preserve layout-affecting text settings from the original, including table cell placement, text box or shape bounds, theme-bound styles, and slide or document master-derived formatting when present.
- If the rewritten content must cross multiple styled runs, replace the wording while keeping the original run boundaries and styling whenever feasible.
- If run boundaries or text splits must change, copy the nearest corresponding original style onto the new text instead of allowing a default font, size, paragraph style, or theme fallback to appear.
- Do not treat a replacement as complete if the text is correct but the font, font size, paragraph settings, or layout styling drifted away from the original.

## Required Inputs

Work when the mapping is reliably recoverable, normally as sentence-by-sentence or paragraph-by-paragraph replacement and exceptionally as a clear local 2:1 or 1:2 sentence mapping.

Expected inputs:

- The original text, file, or document segment.
- The rewritten text that corresponds to the whole original, a section, or a specific paragraph/segment.
- A clear target source or enough local evidence to identify the intended source slot. If the user provides rewritten text without extra explanation, assume it is intended to replace the matching original text in order.
- Run `Source-Slot Recovery Mode` before deciding that apparent factual, citation, table/figure, or cross-reference drift is blocking whenever the intended source slot can be identified.

When native-format output is expected:

- Prefer the actual original `.docx` or `.pptx` file rather than a pasted text surrogate.
- If only pasted text is available and the native source file is missing, preserve the text structure but state clearly that native-format output could not be guaranteed from the provided inputs.

If the mapping is ambiguous after the required recovery attempt, stop and ask for clarification instead of guessing replacements.

## Source-Slot Recovery Mode

Use this mode by default when the pasted text appears to be a source-based rewrite of the whole document, a section, or a paragraph, even if the pasted text contains noisy artifacts.

This mode exists because revised or paraphrased text often corrupts protected content while preserving the underlying source position and order. Typical noise includes:

- invented or drifted cross-references such as `Box 1`, `Figure 6`, `Table 4`, `Source 1`, `see above`, or numbered fragments that do not exist in the source
- citation drift, including new author names, missing years, changed punctuation, or placeholder references
- changed expansions of abbreviations or technical terms
- distorted numbers, dates, percentages, table/figure labels, institution names, place names, or source names
- paragraph-level sentence shuffling that still stays within the same section or local paragraph group

In this mode:

1. Match by original order and section/paragraph slots first.
2. Use the rewritten text's nearby keywords and clause sequence to identify the corresponding original slot.
3. Treat the original document as the authority for all protected content.
4. If the rewritten text introduces a cross-reference, citation, number, name, term, or identifier that is absent from the corresponding original slot, restore the original slot's protected content or remove the noisy artifact if the original has no equivalent.
5. If the rewritten text drops a required protected item from the original, reinsert the original protected item at the nearest corresponding original position.
6. Preserve the rewritten wording around those protected restorations as much as possible.
7. Do not improve grammar or style after restoring protected content.
8. Record these restorations under `Minimal edits made`.

Do not use noisy recovery to accept a genuinely new fact, new source, new table/figure, reordered section, or changed argument. The recovery attempt is allowed only when the source slot is identifiable and the protected drift can be corrected by restoring original content.

## Replacement Workflow

Use this workflow every time:

1. Create a copy of the original text or document as the replacement target.
   Create that copy in the same directory as the original file by default. Keep the original filename stem and append the current date in `YYYY-MM-DD` format as a trailing suffix before the extension whenever feasible. If the filename already has an older replacement suffix such as `-replaced`, replace that suffix with the date suffix instead of stacking both. If that date-suffixed filename already exists, append a minimal numeric suffix. The copy should preserve the original file type whenever feasible. If the original is `.docx`, work toward a `.docx` copy. If the original is `.pptx`, work toward a `.pptx` copy.
2. Segment the original text into the same units implied by the rewritten text.
3. Confirm the rewritten content maps cleanly to the original units, normally sentence-by-sentence or paragraph-by-paragraph and exceptionally as a clearly traceable 2:1 or 1:2 sentence mapping.
4. If a sentence merge or split occurred, confirm with high confidence that the affected units still correspond exactly in order and meaning before continuing.
5. If the mapping is ambiguous, first attempt `Source-Slot Recovery Mode` when a likely original slot can be identified. Attempt original-slot matching and protected-content restoration before stopping. Stop and ask the user only if the mapping is still ambiguous after that attempt, or if the rewritten text introduces a genuinely new fact/source/structure that cannot be reconciled with the original slot.
6. For each matched unit, copy the rewritten wording into the corresponding position in the copy, not the original.
7. If one rewritten sentence corresponds to two original sentences, split it back across the two original sentence positions using the smallest possible structural division while keeping the rewritten wording as intact as possible.
8. If two rewritten sentences correspond to one original sentence, merge them back into the one original sentence position using the smallest possible structural reconciliation while keeping the rewritten wording as intact as possible.
9. Reapply the original unit's formatting, typography, paragraph settings, and structure after replacement.
10. Restore any protected content from the original when the rewritten text altered or removed it, especially italicized text, superscripts, abbreviations, numbers, and reference markers.
11. Run a dedicated person-reference audit before finalizing the artifact.
12. During that audit, explicitly scan the replacement for narrator-voice and report-voice person markers such as `I`, `me`, `my`, `mine`, `we`, `us`, `our`, `ours`, `you`, `your`, and `yours`, and compare each hit against the original.
13. Classify each hit as one of:
   - preserved from the original and therefore acceptable
   - consumer-self-talk, quoted material, titles, URLs, or other non-narrator content and therefore acceptable
   - newly introduced person-reference mismatch and therefore required to be reverted
14. Check whether the replacement introduced either of the two allowed problem types:
   - citation-format mismatch
   - person-reference mismatch
15. Make only the minimum edits needed for those problem types and for the minimum structural split or merge needed to place the rewritten wording back into the original sentence slots.
16. Leave every other awkward or imperfect expression untouched.
17. At the end, provide the required fixed-format output.
18. Save the finished artifact in the original native file format by default when the source file and environment support it.
19. Only if native output is genuinely not feasible in the current environment may you provide a markdown or plain-text fallback, and you must say exactly why.

## Formatting Rules

Preserve the original document's formatting as-is, including when present:

- headings and numbering
- paragraph breaks and line breaks
- bold, italics, underline, superscript, subscript
- font family, font size, font color, highlight, and other character-level style
- paragraph alignment, indentation, first-line or hanging indent, line spacing, and spacing before or after
- list level, bullet or numbering style, tabs, and table cell text placement
- quotation mark style
- parenthesis and bracket style
- citation location and citation wrapper format
- list markers, table text placement, footnote markers, figure references
- capitalization patterns that come from the original formatting context

If the rewritten text loses formatting, restore it from the original. Do not invent new formatting. In native office files, the default expectation is exact carry-over of the original font, font size, paragraph settings, and surrounding layout unless the user explicitly asks for a style change.

Punctuation style must follow the original, including when present:

- quotation mark choice and placement
- parentheses, brackets, and braces
- comma, semicolon, colon, and dash style
- punctuation placement around citations and references
- punctuation adjacent to footnote or endnote markers

If the rewritten text changes punctuation style, restore the original punctuation pattern without performing broader sentence polishing.

## Protected Formatted Content

Treat some original content as protected and authoritative.

Protected cases include:

- italicized book titles, article titles, work titles, and names that appear in italics in the original
- superscripts such as note markers, reference markers, or other raised text
- other explicitly formatted tokens whose content and formatting both come from the original

For protected content:

- keep the original wording if the rewritten text changed that protected item
- keep the original formatting on that item
- restore the protected item into the replaced sentence at the corresponding original position

If the rewritten text changes a protected italicized title or removes a superscript, restore the original title or superscript instead of accepting the rewritten version.

## Protected Proper Content

Treat the following original content as protected by default. If the rewritten text changes any of these, restore the original form unless the user explicitly instructs otherwise.

Protected content includes:

- person names
- place names
- institution and organization names
- technical terms and established terminology
- book titles and work titles
- years, dates, numbers, percentages, and page numbers
- law article numbers, regulation numbers, and similar legal identifiers
- formula numbers, equation numbers, figure numbers, and table numbers
- abbreviations, acronyms, variable names, model names, and case-sensitive forms
- source-log anchors, citation keys, cross-reference labels, box/table/figure/source references, and any original document-specific reference machinery

Keep the original wording, spelling, and case for protected content. The rewritten text may change surrounding wording, but it must not replace these protected items.

If a rewritten text introduces a protected-content-looking artifact that has no corresponding original marker, such as a nonexistent `Box`, `Figure`, `Table`, `Source`, numeric citation, or invented author, treat that artifact as noisy drift under `Source-Slot Recovery Mode` when the source slot is otherwise clear. Restore the original marker if one exists; otherwise remove the noisy artifact without otherwise rewriting the sentence.

## Protected Reference Markers

Preserve original inline reference machinery, including when present:

- footnote markers
- endnote markers
- bibliography or reference numbers
- cross-reference markers
- hyperlink anchors or other inline reference targets

If the rewritten text drops or alters these markers, restore them from the original at the original position.

## Allowed Edits Only

Only two kinds of edits are allowed beyond direct replacement.

### 1. Citation-format fixes

Edit only what is needed to make the citation conform to the original document's citation pattern.

Allowed examples:

- move a citation back to the original position
- restore original bracket or parenthesis style
- restore spacing or punctuation around a citation
- convert a broken inline citation back to the source document's format

Do not change substantive wording outside the citation-related fragment unless the citation cannot be repaired otherwise.

### 2. Person-reference fixes

If the rewritten text changes person reference relative to the original, restore the original person reference with the smallest possible edit.

Typical cases:

- first person to third person
- second person to third person
- singular/plural self-reference that was not in the original

Edit only the words directly required for the person correction. Do not rewrite the whole sentence just to make it smoother.

### Mandatory person-reference audit

This audit is required on every replacement task. Do not treat person-reference checking as optional or implied.

- Compare the final replacement against the original specifically for narrator-voice and report-voice person reference, not only for sentence content.
- Explicitly inspect first- and second-person narrator forms such as `I`, `me`, `my`, `mine`, `we`, `us`, `our`, `ours`, `you`, `your`, and `yours`.
- Also inspect report-self-reference phrases that commonly drift during rewriting, for example `we recommend`, `we profile`, `we review`, `our recommendation`, and `helps us understand`.
- Revert any newly introduced narrator-voice or report-voice person-reference drift to the original form with the smallest possible edit.
- Preserve person reference that already exists in the original. For example, if the original says `I recommend`, keep `I recommend` unless the user explicitly asks to change report voice.
- Do not misclassify consumer self-talk, direct questions presented as consumer thoughts, quoted material, titles, citations, URLs, or reference entries as person-reference mismatches.
- Do not finish the task until this audit has been completed.

## Forbidden Edits

Do not do any of the following unless the user explicitly asks outside this skill's default scope:

- improve grammar
- make wording more native or academic
- repair logic
- add transitions
- fix awkward phrasing
- shorten or expand sentences
- normalize terminology because it "sounds better"
- rewrite sentences for clarity
- change voice, tense, stance, or register unless needed for citation or person repair
- accept rewritten replacements for protected italicized content that should stay exactly as in the original
- drop superscripts, subscripts, or other original inline formatting markers that must be preserved

If something is obviously poor but not covered by the two allowed edit types, keep it and mention it in the final summary.

## Matching Guidance

Prefer exact structural alignment over semantic similarity.

- Match by order first.
- Use nearby anchors such as citations, keywords, clause count, and punctuation patterns when needed.
- Preserve one original unit for one rewritten unit.
- Allow a local 2:1 or 1:2 sentence mapping only when the correspondence is obvious and remains in the same order.
- If a sentence merge or split is not clearly recoverable, do not force a replacement silently. Flag the mismatch.
- Because source-based replacement is the default assumption for this skill, do not reject a passage only because it contains corrupted references or noisy protected terms. First align it to the original slot, then restore the protected content from the original.

## Paragraph-Level Tolerant Matching

Allow limited tolerance for surface noise when the source-slot mapping still holds.

Tolerable differences include:

- paragraph line breaks or soft wraps
- extra or missing spaces
- different quotation-mark glyphs when the quoted content still aligns
- minor spacing differences around punctuation or citations
- superficial layout noise introduced during rewriting or copy-paste

Use this tolerance only to recover the intended original alignment. Do not use it to justify:

- sentence splitting or sentence merging that cannot be mapped back with confidence
- reordering units
- changing protected content
- accepting changed facts, numbers, names, terms, or markers

When applying tolerant matching, normalize only for alignment checking, then restore the original paragraph structure, spacing conventions, punctuation style, and inline formatting in the final output.

## Controlled Split-Merge Exception

Default behavior is still to preserve sentence boundaries. However, allow one narrow exception:

- one rewritten sentence may correspond to two original sentences
- two rewritten sentences may correspond to one original sentence

Allow this only when all of the following are true:

- the local correspondence is clear and high confidence
- the order remains unchanged
- no protected content is lost or replaced
- no factual content is changed
- the rewritten wording can be placed back into the original sentence slots with only minimal structural intervention

When this exception applies:

- preserve the rewritten wording as much as possible
- split or merge only as much as needed to fit the original sentence positions
- keep original punctuation style, citation layout, and formatting
- report the split or merge in `Minimal edits made`

Do not treat broader paragraph restructuring as acceptable under this exception.

## Output Requirements

Return:

1. The replaced artifact from the newly created same-directory copy, with original formatting restored as closely as the medium allows.
2. A brief note of any minimum edits made beyond direct replacement.
3. A brief list of obvious remaining issues that were intentionally not fixed because they fall outside scope.

When the original artifact is a native office file:

- `.docx` in means `.docx` out by default.
- `.pptx` in means `.pptx` out by default.
- The saved output should default to the same directory as the original file.
- The saved working copy and final artifact should default to keeping the original filename stem and appending the current date as a trailing suffix in `YYYY-MM-DD` format before the extension whenever feasible.
- The final response should point to the saved native file path rather than treating a markdown preview as the real deliverable.
- A markdown or plain-text fallback is allowed only when native-format output is genuinely blocked in the current environment, and that limitation must be named explicitly.
- If the original artifact is a native office file, the returned result should preserve the original font, font size, paragraph settings, and layout styling rather than merely preserving textual structure.

When summarizing remaining issues, describe them as observations, not as edits you made.

## Decision Rule

Use this priority order when there is tension:

1. original file format, position, typography, paragraph settings, and formatting
2. original protected content and markers
3. direct insertion of rewritten wording
4. minimal citation repair
5. minimal person-reference repair
6. issue reporting without further editing

If a possible change does not fit this order, do not make it.

## Stop Conditions

Stop and ask the user instead of forcing a replacement when any of the following occurs:

- one rewritten sentence appears to correspond to multiple original sentences and the mapping is not clearly recoverable as a local 2:1 case
- multiple rewritten sentences appear to correspond to one original sentence and the mapping is not clearly recoverable as a local 1:2 case
- sentence order no longer matches
- the rewritten text appears to change facts, numbers, dates, names, terms, or identifiers and the change cannot be repaired by restoring original protected content under `Source-Slot Recovery Mode`
- the replacement would require changing font, font size, paragraph settings, text box bounds, or other original style settings in order to fit
- the correct alignment cannot be determined with confidence

Do not stop merely because noisy rewritten text contains nonexistent boxes, figures, tables, sources, invented citations, malformed technical terms, or distorted numbers when the original slot can be identified. In that case, run `Source-Slot Recovery Mode` and report the protected-content restorations.

When stopping, mark the uncertain location and explain the mismatch briefly.

## Fixed Output Format

Always return results in exactly these three sections:

1. Replaced text
2. Minimal edits made
3. Remaining obvious issues not fixed

Section rules:

- `Replaced text` contains the final text from the new same-directory copy, with original formatting restored as closely as the medium allows.
- When the original artifact is `.docx` or `.pptx`, `Replaced text` should summarize the saved native-file result and point to its path. It does not replace the obligation to save the native file.
- For `.docx` and `.pptx`, "original formatting" includes font family, font size, paragraph settings, bullet or numbering level, and other layout-affecting text styles from the source.
- `Minimal edits made` lists only citation-format fixes, person-reference fixes, and restorations of protected original content or markers.
- `Minimal edits made` must mention any narrator-voice or report-voice person-reference corrections found during the mandatory person-reference audit.
- `Minimal edits made` also records any minimal sentence split or merge performed under the controlled split-merge exception.
- `Remaining obvious issues not fixed` lists problems that were noticed but intentionally left unchanged because they are outside scope.
- If native output had to be downgraded to markdown or plain text, `Remaining obvious issues not fixed` or `Minimal edits made` must state the blocking environment limitation explicitly.

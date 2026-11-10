---
name: research-piece
description: "Research a writing Piece's Supporting Material: download its PDFs, have one sub-agent per source read its listed passages, verify every quote against the text, check every fact with /review-research, and post the fact list as a comment on the Research issue. Writes nothing to the Deliverable. Invoked as /research-piece <repo> <n>."
argument-hint: "<repo> <n>"
disable-model-invocation: true
---

`/research-piece <repo> <n>` researches the Research issue `<repo>#<n>`. Its output is a verified fact list posted as a comment on the issue; it writes nothing to the Deliverable and has no branch.

Fetch the issue with `npm run issue:read -- <repo> <n> --body` and state its title before starting. If the reference is ambiguous, ask. If the issue is a Piece rather than Research, stop and point the developer to `/implement-piece`.

**Work at the primary root or in a session workspace.** Research edits no files in a repo, so no issue workspace is needed. Scratch files go in the scratchpad.

## Steps

1. **Read the sources the spec lists.** **Every source is a Drive file**, one source per ID; `/grill-piece` saved each web page to Drive, and this skill never reads one live. Each source's text goes in `<scratchpad>/texts`, under a short file name such as `heagney.txt`, the name its locators will cite. For a short text, read it with `get_drive_file_content` and save what it returns there. For a PDF, download it with `get_drive_file_download_url`, then dump its text once per [`docs/pdf-pages.md`](../../../docs/pdf-pages.md): `npm run pdf:text -- "<path>" "<scratchpad>/texts/<name>.txt"`. Its page markers are what locators cite.
2. **Give each source to one sub-agent**, a `general-purpose` agent on `sonnet`. Each reads only its own text file and the passages the spec lists, and returns facts in its own words, each ending with its locator: `(<name>.txt, PDF pp. 45–46 (printed 31–32))`, or `(<name>.txt, PDF p. 45)` for one page, with the printed pages only when they differ; for a source with no page markers, `(<name>.txt, heading "<the heading it sits under>")`. A quote is optional, added when the wording matters or to anchor the spot. Each quoted passage is copied word for word from the text, punctuation included, never paraphrased. A quote is one contiguous passage: never join two passages with `...`, and quote each one separately. A term or title that isn't a quote goes in italics, never double quotes. Each agent gets the text file's full path, its file name for the locator and the list of passages to read.
3. **Assemble the fact list** in the scratchpad as `comment.md`: one numbered fact per line, each in the researcher's words and ending with its locator in the shape above, each quoted passage in double quotes.
4. **Verify the quotes.** `verify:quotes` checks that every fact has a locator and every double-quoted span is found within its cited range; it doesn't judge whether a fact is right, and it isn't the plagiarism check. Run `npm run verify:quotes -- --comment "<scratchpad>/comment.md" --texts "<scratchpad>/texts"`. Fix every `NOT FOUND` by copying the passage exactly from the text, or remove the quote. Fix every `OUTSIDE LOCATOR` by correcting the locator to where the quote is, when the fact comes from there. Fix every `NO LOCATOR` by adding or correcting the fact's locator. Fix every `JOINED` by splitting it into one quote per passage. Rerun until it exits 0. Punctuation and wording must match exactly; letter case and line breaks may differ.
5. **Review the draft.** Read [`.claude/skills/review-research/SKILL.md`](../review-research/SKILL.md) and follow it on `comment.md` and the texts folder; it is user-invoked, so the Skill tool can't reach it. One pass: the draft is not reviewed again after the next step.
6. **Act on its verdicts once.** Leave each supported fact as it is. Rewrite each partly supported fact from the reviewer's quote and location, in your own words. Move each unsupported or unverified fact to a `## Unverified` section at the end of `comment.md`, with what was looked for and the reviewer's reason. `## Unverified` is outside the fact list: nothing is drafted from it.
7. **Verify the quotes again**, by step 4's command and fixes, until it exits 0.
8. **Post the comment** with `gh issue comment -R <owner>/<repo> <n> --body-file "<scratchpad>/comment.md"`, resolving `<repo>` to `<owner>/<repo>`.
9. **Delete the downloads**: `rm` each path that `get_drive_file_download_url` returned, once the comment is posted.

## Done when

Every fact in the posted comment's fact list has a source and a page range, or a heading for a source with no pages, and `/review-research` found it supported or it was rewritten from the reviewer's quote; every other fact is under `## Unverified`; `verify:quotes` exits 0 on the posted file; and the downloads are deleted.

## Wrap-up

Research wraps up with `npm run wrap-up -- <repo> <n> --no-code`; nothing is committed, pushed or closed before it.

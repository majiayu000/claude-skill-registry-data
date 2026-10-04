---
name: referee-response
description: Draft an R&R response letter to a journal decision, sectioned by Senior Editor, Associate Editor, and each reviewer, and check a finished letter before resubmission. TRIGGER on "respond to the referees", "draft the R&R response", "write the R2R", "address the reviewer comments", "respond to the AE", "continue the R2R", "check the R2R letter", or when the user pastes reviewer comments or a decision letter.
---

# Referee response letter

The editor reads this letter with the manuscript open. A pin that says a change is in Section 4
when it is not gets caught immediately, and the cost of that is much higher than the cost of an
honest TODO. So the letter may only say what the manuscript actually says. Step 3 is the point of
this skill: a verification pass sitting between classifying the comments and writing any prose.

## Arguments

- `continue`: extend a partial `R2R_R<n>.tex` already in the project instead of starting fresh.
- `from-email`: input is a pasted decision email (Outlook export, forwarded thread).
- `@path/to/letter.pdf`: the decision letter as a file (`.pdf`, `.txt`, `.docx`, `.md`).
- `--five-q`: opt-in stress test on pushback paragraphs (see below). Combines with the others.

With no argument, the comments are pasted in the message body.

## Finding the project

There is no config file and none should be required. Glob `~/Library/CloudStorage/Dropbox*/Apps/Overleaf/*/`
(this setup assumes Overleaf projects sync there via Dropbox; adjust to your machine)
and match the user's wording against the directory names; ask once if two fit. Then read what is
actually there:

- manuscript: identified by content, the `.tex` containing `\documentclass` or `\begin{document}`
  (usually `main*.tex`, or `doc.tex` in older projects). Follow every `\input`, `\include`, and
  `\subfile` to get the rest, since sections, tables, and the preamble usually live in separate
  files.
- prior rounds: `R2R_*.tex`, if any
- bibliography: `*.bib`

Ignore any file whose name contains `conflicted copy`; Dropbox leaves those behind and they are
stale. Never commit or push, Dropbox syncs the directory.

## Reading the decision letter

The Read tool cannot open a PDF on this machine (it needs `pdftoppm`; this setup assumes no
Homebrew and
no poppler, so adjust to yours). Get the letter's text with `~/.claude/assets/bin/pdfread.py text letter.pdf`. Do not
call `pdftotext`.

If that returns almost nothing the letter is a scan (`pdfread.py pages letter.pdf` says so). Then
rasterize it, `~/.claude/assets/bin/pdfread.py png letter.pdf --dpi 200 --out /tmp/letter`, and
Read the PNGs. Read it if you genuinely can.
If any passage is illegible, stop and ask for a text version of that passage. Never reconstruct
what a reviewer probably wrote.

A `.docx` letter also has no direct reading path. Convert it first with
`textutil -convert txt letter.docx` (`/usr/bin/textutil`, present on every Mac), then Read the
`.txt` it writes next to the source.

## Reading the prior round

If `R2R_*.tex` files exist, read the highest-numbered one for continuity of substance only: what
was promised to whom, which positions were already taken, which changes were already claimed. You
are not matching its writing style, and nothing about its phrasing constrains this letter. Write
the new one in clear academic prose using your own formatting judgment.

Two things to carry forward. When a reviewer re-raises a point that was pushed back on last round,
reuse and refine the earlier position; do not restart the argument, and flag
`% TODO (user): prior round said X, do we still hold that line?` before contradicting it. And any
change promised last round gets checked in step 3 like every other claim.

## Step 1. Parse into role-keyed comments

Key every comment to its author (Senior Editor, Associate Editor, Reviewer 1, Reviewer 2, and so
on) and keep its text verbatim, since the letter quotes each comment before replying to it.
If the source is not labeled by role, ask once to confirm the assignment. If the comments are not
numbered in the source, preserve the source's own structure (paragraphs, bullets) rather than
imposing numbering the user never received. Use internal ids like R1.3 for the chat report.

## Step 2. Classify every comment

Pick a strategy for each comment before drafting any prose. Doing this as its own pass catches
misclassification while it is still cheap to fix.

| Strategy | When | Shape of the reply |
|---|---|---|
| Done. | SE or AE gave an explicit instruction with a single-action fix (typo, format, missing citation, word swap) | The word "Done." then a location pin, nothing else |
| Substantive change | Reviewer asked for an analysis, robustness check, added discussion, or model revision, and it is genuinely in the paper | Acknowledge, state what changed, pin the location, quote the new text |
| Partial change | Reviewer asked for X and the paper does a scoped version of X | Acknowledge, describe the scope, pin it, say briefly why scoped |
| Polite disagreement | The reviewer's premise is mistaken or contradicted by a more authoritative source | State the reasoning, cite the authority with a short inline quote, close by inviting the editor's discretion |
| Deferred | Out of scope, a separate paper, or needs data collection beyond the R&R window | Acknowledge, say why deferred, point to where the paper flags it if it does |
| Needs user input | Cannot be classified without the user's substantive judgment | `% TODO (user): <one-sentence question>` and nothing asserted |

"Done." never applies to a substantive comment. Every comment gets its own reply, including ones
that look redundant.

## Step 3. Verify every pin against the manuscript

For every comment classified Substantive or Partial, before writing the response paragraph:

1. Open the manuscript at the location you intend to pin, following `\input`, `\include`, and
   `\subfile` files as needed.
2. Read the text there.
3. Match it against what the reply claims was changed.
4. Only then write the pin.

If the change is not there, the classification is wrong and the reply gets downgraded:

- claimed change, nothing found anywhere: drop to `% TODO (user): R1.3 says we added X; I cannot
  find it in the manuscript. Confirm it was made and give me the location.` Do not assert it.
- change found somewhere else: pin the real location, not the expected one.
- change present but narrower than what was asked: reclassify as Partial and state the scope.

Never write "we added X to Section Y" without having read X in Section Y. The same rule covers
footnote numbers, table numbers, and appendix labels: read them, do not infer them. If the
manuscript has moved since the prior round, that is exactly the case this step exists for: verify,
and never assume last round's pins still hold.

## Step 4. Draft the letter

Write to `<project>/R2R_R<n>.tex`, where `<n>` is the round the user named or one more than the
highest existing `R2R_R*.tex`. Do not touch `main*.tex` or any file it inputs.

Provenance header:

```latex
% Draft by referee-response, <YYYY-MM-DD>. Status: DRAFT, not sent.
% Round R<n> · Project: <name> · Verified against: <path to manuscript>
% Every Substantive/Partial pin below was read in the manuscript before being written.
% Unresolved items are marked % TODO (<count>).
```

Body shape, which is the standard one for these letters:

1. One paragraph of thanks to the review team, then a numbered list of the main changes at a high
   level, each with its location.
2. One `\section*{}` per role in the order Senior Editor, Associate Editor, Reviewer 1, Reviewer 2,
   continuing with the numbering as received. Each opens with a short thanks specific to what that
   person actually said, not boilerplate.
3. Within a section, each comment quoted verbatim and visually separated from the reply below it.
   Markup is your call.

Two conventions worth keeping. Rejected or superseded response drafts stay in the file inside a
comment block rather than being deleted, so the revision history survives; use
`\begin{comment}...\end{comment}` if the preamble loads the `comment` package, otherwise
`%`-prefixed lines. And when two reviewers raise the same point, answer each in their own section
and cross-reference ("see also our response to Reviewer 1, comment 3") instead of merging them.

## Step 5. Report to chat

Not into the file:

1. Path to the new file.
2. Comments parsed per role.
3. Count of `% TODO:` items with their ids (R1.3, R2.7), which is the list the user has to clear.
4. Every substantive position taken, with its pin, so the user can override any judgment call.
5. Any reviewer comment citing a paper the manuscript does not engage with, so the bibliography
   can be fixed before submission. Use the `reading-papers` skill to resolve those references
   rather than guessing at a citation key.
6. Any place where the AE and a reviewer gave conflicting instructions. Follow the AE, since the
   AE decides, and say so here.

## --five-q mode

Opt-in only, never automatic. It applies a hostile-editor test to every paragraph classified
Polite disagreement. Before drafting that paragraph, test the disputed claim against five
questions; the answers do not go in the file:

1. What is the question?
2. Why should anyone care?
3. What is the finding?
4. How do we know?
5. What does it mean for the field?

If any answer is hand-wavy or thinner than the reviewer's objection, the pushback does not survive
contact with an editor. Reclassify the comment from Polite disagreement to Partial change, draft a
concede-and-strengthen reply as the active response, and preserve the rejected pushback draft in a
comment block. Add one line per downgrade to the step 5 report: "R2.4: pushback downgraded under
--five-q, weak answer to Q4."

## Failure modes

- Comments unlabeled by role: ask once, then proceed.
- A comment too vague to classify ("the paper needs more context"): `% TODO (user): needs your
  read, possibly substantive`. Not a guess.
- A reviewer cites a paper missing from the `.bib`: flag it in the report. Do not write a reply
  that pretends the paper is already cited.
- The user asks for a reply to an analysis that has not been run: say so. Running the analysis is
  a separate job that happens before this skill, not inside it.

## Out of scope

- Editing `main*.tex` or its inputs. The user makes the substantive paper edits.
- Running new analyses or regenerating tables to answer a reviewer.
- Adding entries to the `.bib`.
- Inventing counter-arguments the user has not sanctioned. Surface positions, do not manufacture
  them.

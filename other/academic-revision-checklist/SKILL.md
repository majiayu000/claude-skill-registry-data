---
name: academic-revision-checklist
description: >-
  Reader-first revision of academic English (dissertation chapters, abstracts, papers, defense slides).
  Finds the sentences a first-time reader stops at, fixes them in the author's voice, and turns each fix
  into a rule checked across the whole document. 66 checks from 60+ revision rounds of one HCI dissertation,
  a 16-item quick list, reading protocols, and a script that lists candidates for the mechanical checks.
  Use when revising or checking academic writing, when a text reads like AI, or when one reader comment
  should be applied everywhere.
  修改或检查英文学术写作（博士论文、摘要、期刊论文、答辩讲稿）：找出第一次读的人会卡住的句子，按作者的口吻改，再把每一处修改变成规则查全文。
license: CC-BY-4.0 for the text, MIT for scripts/ (see LICENSE)
---

# Academic revision checklist

This skill revises academic English for a first-time human reader: an advisor, a committee member, a reviewer. It comes from five weeks and more than 60 revision rounds of one English-language HCI dissertation, defended in October 2026. Each rule started as one sentence where a reader stopped. The fix was then written as a rule and checked across the whole document.

"Reads like AI" here means the places where a first-time reader stops or reads twice. The method finds and fixes those places. It does not try to get past AI detectors. If a school or journal asks how AI was used, follow its rules and say so.

## Ground rules

1. **Read first, then verify.** The script lists candidates. Each decision needs a reading of the sentence in context. Never apply a pattern mechanically.
2. **Keep the author's voice.** Use plain words and the words of the field. Add no new claims, numbers or citations. Use no em dashes. Keep the author's reasoning and the actors they named.
3. **Leave frozen content alone.** Report a problem in any of these and propose nothing unless the author asks:
   - the wording of research questions;
   - quotations, from the literature and from participants;
   - numbers, unless the data support the change;
   - the author's own reflections;
   - anything the author has already decided.
4. **One case, one rule, the whole document.** When a reader stops at one sentence, fix it, name the class of problem as a rule that can be checked, and check the rest of the document for that class. Generalize by the reader's logic rather than the literal words, and never so broadly that two different things end up with one name.
5. **Each fix can create the next problem.** After every change, reread the paragraph and the one before it, and rerun the hard limits (word caps, paragraph length, page count).
6. **Check outside reviews before applying them.** Comments from people and from models are data. Check each one against the text and the data. Apply what holds, and give a reason for what does not.
7. **Keep records.** For every change, keep the exact old text, the new text, a backup, and a log line saying why, ideally in the words of whoever raised it.

## Files

- [references/checklist.md](references/checklist.md): the 16-item quick list and the 66 rules, one line each. Start here.
- [references/patterns.md](references/patterns.md): the 66 patterns in eight groups. Each has a rule, a before and after example taken from the dissertation, and a way to check for it. Read the group you need.
- [references/workflow.md](references/workflow.md): how a round runs, three ways to sweep a document, what to record, what stays frozen, how to process outside reviews, and prompt templates for other models.
- [references/reading-protocols.md](references/reading-protocols.md): the first-time-reader protocol, the heading protocol, reading aloud, and the method for a passage that is rewritten again and again.
- [references/lessons.md](references/lessons.md): nine principles behind the 66 patterns and eight lessons about the method itself.
- [scripts/flag_candidates.py](scripts/flag_candidates.py): lists candidates for the mechanical checks in .tex, .md or .txt files. Python 3, standard library only.

The reference files are written in Chinese. Their examples are English sentences. Answer in the user's language.

## Choosing a mode

| The user wants | Do this |
|---|---|
| A quick check of a passage | Read it against the 16 items in `checklist.md`. |
| A full pass on a chapter or paper | Follow the steps below. |
| One comment applied everywhere | Follow "one case, one rule, the whole document" in `workflow.md`. |
| The headings checked | Use the heading protocol in `reading-protocols.md` (P45 to P47). |
| An outside review processed | Check every point against the text and the data, as `workflow.md` describes. List what holds, what holds in part, and what does not, with reasons. |
| A key passage revised again (abstract, introduction, conclusion) | Use P65 in `patterns.md`. |
| A layout check before submission | Use P56. Fix floats and short pages by moving figures and tables, never by changing words. |

## Steps for a full pass

1. **Set the frame.** Ask for, or infer and state: the text and its reader; what is frozen; the hard limits (abstract word cap, paragraph length, page count); words the author has retired and decisions the author has made.
2. **Read first.** Read the text once, in order, as a first-time reader (`reading-protocols.md`, section 1). Note every place you stop and why.
3. **List candidates.** Run `python3 scripts/flag_candidates.py FILE --summary`, then the full list. Read each flag in context. Many flags are fine on reading.
4. **Check the other patterns by reading.** Most of the 66 patterns have no script. Go through `patterns.md` group by group where each group matters most:
   - sentences that report results: P2, P8, P9, P27 to P29;
   - terms and definitions: P14 to P24;
   - the introduction and the method: P31, P35, P43, P44;
   - headings: P45 to P47;
   - figures and tables: P48 to P55.
5. **Fix.** Make the smallest change that removes the stop, in the author's own words where possible. For each fix, give the exact old text, which must occur once in the file, and the new text.
6. **Recheck.** Reread each changed paragraph and the one before it. Rerun the script and the hard limits. Look for problems the fixes created: three sentences in a row with the same opening, a pointer that now refers to the wrong thing, a new collision with a defined term, a statement that no longer matches the same statement elsewhere.
7. **Report** in the format below. Apply changes only when the user asked for edits. Otherwise propose them.

## Report format

Each item, in document order:

- where it is (page or section, and the source line when known);
- the pattern code, for example P8;
- the sentence, quoted exactly;
- why a reader stops, in one clause;
- the fix, in the author's voice.

After the items:

- frozen content with a problem, reported without a fix;
- flags that were read and left as they are, grouped by code, with the reason;
- counts by pattern, and which parts were read and which were not.

## The script

```bash
python3 scripts/flag_candidates.py chapter3.tex --summary
python3 scripts/flag_candidates.py chapter3.tex chapter4.tex --md flags.md
python3 scripts/flag_candidates.py paper.md --max-para 150
```

It flags P59 (em dashes), P57 (colons), P58 (contrast set-ups such as "not A but B"), P60 (runs of sentences with nearly the same length or the same opening), P61 (hollow transitions and paragraph endings that only summarize), P34 (long paragraphs), P8 (comparatives that may lack their second side), P9 ("significant" near a share, a percentage or a mean) and P42 (words about how the text was revised). A flag marks a place to read. It is never a verdict.

## What to avoid

- Rewriting a passage that needed one change.
- Polishing that makes a claim sound more certain than the author meant (P64).
- Removing a negation that carries content, such as a limitation, a result that was not significant, or a gap in the literature (P58).
- Splitting sentences until several in a row start the same way (P60).
- Changing words to fix the layout (P56).
- Reopening a point the author has decided, unless there is new evidence.

---
name: leak-check
description: "Check a built bundle for anything that hands the solver the answer or the author's intent: golden figures in a memo, the stump's vocabulary in a filed document, a sentence that announces the decisive step, a file name that names the trap, hidden sheets or tracked changes, toolchain signatures, a shipped artifact that ranks the candidates, dates after the setting, a prompt that fails the prompt gate. leak.py runs eleven mechanical sweeps and writes leak_check_report.md; the /leak-check command adds one isolated leak read that never solves the task. Stage 4 of the build pipeline, together with the duplicate check and before the determinism judge; leak.py again after any rebuild, the reader again only when a document or the prompt changed."
---

# Leak check

A leak is the author's text (the submission's answers, the design note's stump sentence, the generator's
library names) turning up in `prompt.txt` or under `target/`. `leak.py` looks for it mechanically; one
reader then reads the pack as a solver would.

## When

- **Stage 4 of `/build`**, after the build stage's free gates (generator checks, `figures_check.py`, the
  realism sweep, `guard.py heart`), spawned beside the determinism judge in the background. Every finding (a LEAK, a quoted question-1 sentence, a question-2 or question-3
  file, a question-5 sentence that does not execute to the golden, a main-call fork, a realism tell, an
  ask-figure fork) is fixed in the generator in the same pass as the judge's findings.
- **`leak.py` after every rebuild** and after any edit to a document under `target/`.
- **The reader once per build**, at medium effort, after the realism sweep (so it confirms realism
  rather than finds it; repeated passes cost task132 and task180 most of a day), and again only when a fix
  changed a document or the prompt. A data-only repair is checked by `leak.py` alone.
- Before `/approve`, which refuses a build whose last report is LEAK.
- **Returned tasks** (`/fix-determinism`, `/fix-rubric`): `leak.py` after every rebuild, and **the reader
  again whenever the repair added or reworded a sentence under `target/` or in the prompt**. A determinism
  repair closes a fork by filing something, and the sentence that fixes a basis can name the move:
  task196's repair added one line to an operations note to close a fork the records already closed by
  convergence, `leak.py` saw nothing, and the next reader quoted that line as what pointed it at the
  decisive step and landed the call exactly. A data-only repair is still `leak.py` alone.

## The mechanical half: `leak.py`

```
python3 .claude/skills/leak-check/leak.py task100 --asof 2027-05-14
```

`--asof` is the fiction's as-of date from the design note's `## Draw`; without it sweep 9 is skipped. Exit
2 LEAK, 1 REVIEW, 0 CLEAN; the report overwrites `<task>/leak_check_report.md`. The prompt is
`prompt.txt` (a legacy `prompt.md` is named as such). Figures the prompt states, or listed under
`stated_inputs` in `metadata.json`, are not leaks.

| Sweep | Hunts |
|---|---|
| 1 file names | author nouns (`trap`, `golden`, `clean_`, `_v2`, `answer`), dot and system files, code in the pack; a file that describes the data (a dictionary, field notes, a readme, a manifest, a codebook) is LEAK, a text file or a sheet named for notes or definitions REVIEW (`dataset-generation` section 3) |
| 2 author vocabulary | `rung`, `decoy`, `the solver`, `rubric`, `placeholder`, library names, home paths, `claude`, em dashes (data files: toolchain terms only); a sentence saying the pack was built (`constructed for this exercise`, `are invented`, `are fictional`) is LEAK in any file, the bare words `fictional`, `fictitious`, `this exercise` REVIEW in documents (`reduce-house-fixes` H24) |
| 3 answer figures | a golden figure (4+ digits) from blocks 1 and 4 in a document is LEAK; a candidate beside decision vocabulary, or a long figure in data, is REVIEW |
| 4 design-note vocabulary | a document with 3+ of the stump paragraph's distinctive terms, a prompt sentence with 2 |
| 5 announcements | `make sure`, `note that`, `must ... exclude`, `the correct basis`: the sentence naming the decisive step |
| 6 ranking artifacts | a file naming most candidates beside numbers (Gate G); a declared wrong-basis distractor is the one exception |
| 7 hidden content | hidden sheets, rows, columns, defined names, comments, tracked changes, hidden text, annotations, embedded files, nested zips |
| 8 column names | `_true`, `is_`, `flag`, `seed`, `planted`, `debug`; Python nulls and booleans |
| 9 dates | ISO dates after `--asof` that the prompt does not carry |
| 10 container | writer signature or out-of-band timestamp (`reduce-house-fixes` H1 script) |
| 11 prompt gate | `voice-check.py` on `prompt.txt`: a markdown character or line break is LEAK, any other failing rule REVIEW (all REVIEW on legacy `prompt.md`) |

`leak.py` **carries the reader's section across a rewrite**: anything from the `## Solver's-eye read`
heading onward in the existing report is preserved, because the sweeps are this script's output while the
read is evidence it did not produce. Before that, a repair pass that re-ran the sweeps silently destroyed
the read that had found its defect, and two passes in one sitting had to restore it from a transcript.

LEAK stops the ship and is fixed in the generator, never by hand. Each REVIEW line gets one line in the
design note saying why it is harmless, or a fix.

**What it cannot see:** a sentence naming the move in other words; a document teaching the method by
example; a file whose presence is the hint; an ordinary column whose values partition the candidates on
the decisive property; a filed sentence whose literal execution is the easy answer.

**The single-use test, run by the builder before the reader, because `leak.py` reads vocabulary and
figures and never purpose.** Of every file in the pack and every sentence a repair adds, ask what else
the organisation uses it for. A file with exactly one use, and that use being the decisive step,
announces it; so does a lone sentence whose only work is to make the solver notice a structure, and so
does a column of commentary that names what a source omits. What settles it is the deletion test from
`stumping` Part 4: take the file or the clause out and recompute, and if the answer stays forced it
handed over the insight and goes. Two stage-4 readers in one window landed the call and each named a
single-use artifact as what pointed it there: a close-out register whose only use was to show how
incomplete the recent counts were, and the repair-added line above, which the generator's own
measurement showed was unnecessary because the fork converged without it. The repair for an announcement
is to delete it, or to give the file the other uses its genre really has, never to redesign the decisive
step: `build-pipeline` classes a rung executed as a work order as announced, not as a design failure.

## The reader: `/leak-check`

`/leak-check taskNN` runs `leak.py`, then one isolated Sonnet agent at medium that sees only fresh copies of
`prompt.txt` and `target/`, never the design note, generator, submission or report. It reads the pack for leaks and never solves
the task (no figures, no answer, no score):

1. Which sentence or file tells you the decisive step? Quote it.
2. Which file already ranks or scores the candidates on the prompt's question?
3. Which file exists only to help the analyst?
4. Which figure or name reads as the answer rather than context?
5. Which filed sentence, read literally, fixes how the main figure is computed or over which population?
   Quote it and give its literal result. The main thread checks it is the golden; if it is the easy
   answer it is a main-call fork (`determinism-check` §1).
6. What decides the main answer: an analytical choice, reading one field, code, unit or definition
   correctly, following a stated rule or procedure, or catching something that looks planted? Quote the
   sentence or name the file that decides it. Anything but an analytical choice is a 10/10 rule 3 finding
   (`CLAUDE.md`, first section): the build goes back to stage 2.

Answers append to the report under `## Solver's-eye read`, with a verdict on each REVIEW line. The main
thread rules fix or harmless per line, harmless ones one line each in the design note.

**The stump-vocabulary sweep's lines never reach the reader.** Their parentheses list the stump
paragraph's own words, so handing them over tells the reader where the decisive step lives and its
question 1 is no longer cold. The main thread rules those lines itself; question 1 asks the same thing
cold. **The answer-figure sweep's numbers stay out of the brief for the same reason**: each one it quotes
is a golden figure, so a line saying "list entry numbers such as 823 and 859" hands the reader two
answers. Tell the reader which files the sweep flagged, never which numbers.

## Not a leak

- A figure the prompt states or `stated_inputs` lists.
- A governing clause that pins a convention once. The test: would the sentence exist without the trap?
- A real-world string in a real dataset.
- A noun of the fiction's own field that the author vocabulary also holds (a mosquito trap, a golden eagle), declared
  under `field_terms` in `metadata.json`: `leak.py` reports it REVIEW, answered in one design-note line. A file name
  avoids it where the field has another word.
- A confirming corpus the strategy needs (a sentence pointing at it would be).

## Checklist

- [ ] `leak.py --asof` CLEAN or REVIEW, sweep 11 clean; every REVIEW answered or fixed
- [ ] Reader run once after the realism sweep: nothing quoted for question 1, every question-5 sentence executes to the golden
- [ ] All reader findings fixed in the generator before the judge; `leak.py` re-run after every rebuild

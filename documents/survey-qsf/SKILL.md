---
name: survey-qsf
description: Builds a Qualtrics .qsf import file from a survey already written in markdown or in the conversation, question types, choice limits, write-in options, blocks, skip logic, and carry-forward included, and renders an exported .qsf back as readable markdown for revision. Fires on "make this a qualtrics survey", "build the qsf", "qualtrics import file", "get this survey into qualtrics", "read this qsf", and "rebuild last term's survey". Designs no questions and never opens Qualtrics.
when_to_use: Use when the user has already written a survey and wants it created in Qualtrics without retyping it into the web editor, or when they want an exported .qsf turned back into something readable and editable. Use it also to revise a survey from a previous term by reading last term's export, editing the spec, and rebuilding. Do not use it to design or word survey questions, which happens before this skill runs, and do not use it to analyze responses after a survey closes.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Agent
argument-hint: [path to the written survey, or to a .qsf to read back]
---

# Survey to Qualtrics

Turns a survey you have written into the file that creates it in Qualtrics, and turns a survey exported from Qualtrics back into something you can edit.

**Produces:** a `.qsf` you upload by hand, and a markdown readback of that finished file. **Does not produce:** the survey's questions, which are written before this skill runs, and any change inside Qualtrics, which this skill never touches.

The format this writes is undocumented and Qualtrics warns against editing it, so the skill's whole shape follows from one fact: **the file cannot be checked by reading it, only by reading it back.** `references/qsf-format.md` carries the evidence base and the traps; read it when something breaks, not on every run.

## Install

This skill is one of the few in this repository that does not install by copying a single file. It needs its scripts and its profile:

```
~/.claude/skills/survey-qsf/
  SKILL.md
  references/qsf-format.md
  references/survey-spec.md
  scripts/build_qsf.py
  scripts/profile_qsf.py
  scripts/qsf_read.py
  scripts/validate_qsf.py
  assets/qsf-profile.json
```

`README.md` is documentation for people rather than something the skill reads, so copying it is optional. Python 3 with the standard library is the only dependency.

**Re-derive the profile before your first build.** `assets/qsf-profile.json` ships anonymized, which means the account, brand, theme, and message-library identifiers are blank, along with the survey password and the end-of-survey redirect. A survey built from it lands in the Qualtrics default theme and ends with the Qualtrics default message. Export any survey from your own account and run the command under "Keeping the format current" below. Everything else works as shipped, and the shipped profile has only ever been exercised against builds, not against an import, since importing is a manual step.

## Mode 1: build a .qsf from a written survey

**1. Settle the source and the destination.** The source is a markdown survey, a document, or the survey as designed in the conversation. Where it exists only in the conversation, write it out as a markdown survey first and confirm it with the user: without a written source there is nothing for step 6 to check the result against, and the check is the only thing standing between a misread question and a wasted upload.

Put the `.qsf` in the project folder and the intermediate spec and readback in a build subfolder beside it, or wherever your own naming convention sends generated files. When the source sits in a downloads folder or anywhere else that gets cleared, ask where the survey belongs before writing anything there.

**2. Read `references/survey-spec.md`, then write the spec.** This is the judgment in the whole run. A written survey does not say what Qualtrics type each question is, and five calls recur: a list of items sharing one scale is **one matrix**, not several questions; "choose up to 3" is a **rule Qualtrics enforces**, not words in the question; "Other (please describe)" needs a **write-in box** on that choice; "skip to question 18" is a **skip**, which reaches only the same block or the one immediately after it, so it names that question when it is in the same block, names the next block when question 18 starts it, and otherwise means the sections have to be split or reordered before it can be expressed at all; and anything that shows the respondent what they picked earlier is **carry-forward**, written as `${answers:Q3}` against another question's spec id, never against a Qualtrics id.

Preserve the author's wording exactly. This skill has no writing-voice dependency because rewriting question text would be a defect: a survey's wording is the instrument, and changing it changes what the answers mean.

**3. Build.**
```bash
python3 ~/.claude/skills/survey-qsf/scripts/build_qsf.py <spec.json> -o <output.qsf>
```
It prints a build report listing what to check in Qualtrics after the upload: constructs not evidenced in the profile's source exports, anything a `--conservative` build deliberately left out, and advisories. Carry that list into step 7 verbatim.

**4. Validate.**
```bash
python3 ~/.claude/skills/survey-qsf/scripts/validate_qsf.py <output.qsf>
```
Every check here is for a failure that imports cleanly and produces the wrong survey: a question in no block vanishes, a block outside the flow vanishes, a skip naming a choice's position instead of its key sends people to the wrong answer. Fix errors before going further. Warnings are reported to the user, not silently cleared.

**5. Read the file back.**
```bash
python3 ~/.claude/skills/survey-qsf/scripts/qsf_read.py <output.qsf> -o <readback.md>
```
This reads the finished file, not the spec, which is the point: it shows what Qualtrics will see rather than what the build intended.

**6. Audit, in a separate Agent.** Give the agent the readback and the original written survey, and nothing else. Its brief:

> Compare these two documents question by question. The first is a survey as written; the second is a readback of the file generated from it. Report, per question: any question in the source that is missing from the readback or vice versa; any question whose wording differs in a way that changes what is being asked; any question whose type is wrong for how the source is written, in particular a set of items sharing one scale that should be one grid, a "choose up to N" instruction with no matching limit, an "Other, please describe" option with no write-in box, and a written skip instruction with no matching skip; any answer option missing, added, or reordered; and any scale whose points are in the wrong order. Report only differences, each naming the question and what to change. Do not suggest improvements to the survey itself.

The auditor does not spawn sub-agents. The first pass is full. A second pass runs only on a finding that changes a question's type, its wording, or its options, and is scoped to the questions that changed, which the skill can identify because it holds both readbacks.

**7. Report and stop.** Give the user the readback, the audit findings and what was done about each, the build report's check list, and the path to the `.qsf`. Then stop: the upload is theirs, and it is the only thing that proves the file works.

## Mode 2: read an existing .qsf

```bash
python3 ~/.claude/skills/survey-qsf/scripts/qsf_read.py <survey.qsf> -o <survey>.md --spec <survey>_spec.json
```

The markdown is for reading; the spec is what makes the survey editable. Revising last term's survey means reading it back, editing the spec, and rebuilding through Mode 1 from step 3. Say plainly that anything the spec cannot carry, listed at the end of `references/survey-spec.md`, is dropped on that rebuild and has to be re-added in Qualtrics.

## Keeping the format current

`assets/qsf-profile.json` is the skill's only picture of what Qualtrics actually produces, derived from real exports. Refresh it whenever an upload behaves oddly or a new question type needs evidencing, and **give it every export available rather than one**: a key that all of one file's questions happen to carry looks mandatory until a second file shows one without it.
```bash
python3 ~/.claude/skills/survey-qsf/scripts/profile_qsf.py <export.qsf> [<export2.qsf> ...]
```
It holds structure and settings only, never survey text, but it does hold the account's own identifiers and the export filenames. **Regenerate it with `--anonymize` before it leaves your machine**, which blanks both.

## Session record

After a build, record the survey, the question count, whether the upload has happened yet, and any construct the build report flagged. The upload outcome is the one fact a later session cannot recover on its own, because it happens outside the environment. If you use the [handoff-resume](../handoff-resume/) protocol, that is where this belongs.

## Gotchas

- **Symptom:** the survey imports but a question is missing. **Cause:** the question is defined but listed in no block, which Qualtrics drops in silence. **Fix:** `validate_qsf.py` catches this; if a file reached Qualtrics without it, run the validator now rather than hunting in the editor.
- **Symptom:** a skip sends people to the wrong answer's destination. **Cause:** the locator was built from the choice's position on screen instead of its key, and the two only agree while the keys run 1..n with no gaps. **Fix:** the builder derives the key from the choice list, and the validator checks it; never hand-edit a locator.
- **Symptom:** Qualtrics says "Something went wrong and the project wasn't created". **Cause:** observed once, and it was an id of the wrong length: every Qualtrics id is 15 characters after its prefix, and a build using 16 was rejected outright. **Fix:** the validator checks this now. If it passes and the import still fails, compare the file against a real export element by element; the answer has both times been in that difference.
- **Symptom:** the upload is rejected with nothing useful said. **Cause:** most likely a reconstructed construct, and most likely the choice limit, which no observed export evidences. **Fix:** rebuild with `--conservative`, which strips the reconstructed extras and keeps every question, and compare. `references/qsf-format.md` section 4 has the full sequence, including how to bisect by block when that does not settle it.
- **Symptom:** a scale reads back in a different order than it was written. **Cause:** something sorted by choice key instead of using the order array. Display order lives only in `ChoiceOrder` and `AnswerOrder`. **Fix:** re-read `references/qsf-format.md` section 3 before touching either script.
- **Symptom:** a rebuilt survey shows blank spaces where names or earlier answers should appear. **Cause:** carry-forward pipes still naming the question ids of the survey they came from, which a rebuild renumbers. **Fix:** the validator fails this now; never write a raw `QID` into a spec, and name questions by their spec id so the builder re-points them.
- **Symptom:** the generated survey imports with the wrong theme. **Cause:** the profile is anonymized, which is how this skill ships, so the brand and skin IDs are blank. **Fix:** re-derive the profile without `--anonymize` from an export of the account being uploaded to.

## Attribution

The scripts here started from the archetypes in `skill-engineer-master` by Antony Evans (edge-brain-lite, https://github.com/antonyevans/edge-brain-lite), CC BY 4.0.

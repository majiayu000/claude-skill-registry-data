---
name: prune-no-ops
description: Delete the sentences in a skill that change no behavior - asides,
  justification, emphasis, and restated defaults.
disable-model-invocation: true
version: 0.1.1
---

# Prune No-ops

Delete every sentence in a target skill that doesn't change behavior. The verdict
for each sentence is the **deletion test**: would an agent running the skill
on its trigger cases behave identically with the sentence and without it? A
sentence whose deletion changes nothing is a **no-op** - delete it whole. A
sentence that survives keeps every word.

Apply the cuts. When the user asks for analysis only, stop after step 2 and
report the verdicts.

## Process

### 1. Read the target

Read the target `SKILL.md` and every file it references. The body prose is the
scope; leave frontmatter untouched - the description's wording does invocation
work, and the deletion test does not grade it. Done when every in-scope file is read.

### 2. Classify every sentence

Run the deletion test on each sentence and record a verdict: _survives_, or one
no-op class:

<!-- vale Skills.WeakVerbs = NO -->
<!-- The bullets quote weak phrasing as the smells they name; "fixing" a
quoted example would erase the smell it demonstrates. -->

- **Aside** - "by the way", "note that", "keep in mind" framing around an
  instruction that binds on its own.
- **Justification** - the why behind an instruction ("this ensures...",
  "because...") when the instruction binds without it. Reasoning survives only
  when it gates a decision: it tells the agent when the rule applies or how to
  trade it off.
- **Default restatement** - an instruction the model already obeys unprompted
  ("be careful", "make sure to read the file first").
- **Emphasis** - "this is important", "always remember", "critically".
- **Duplicate** - a meaning another sentence in the file already states. The
  clearer statement survives. The other is the no-op.

<!-- vale Skills.WeakVerbs = YES -->
<!-- vale Skills.HedgeWords = NO -->
<!-- "A maybe" below is the verdict as a noun, not a hedge. -->

Deletion demands certainty: mark a sentence no-op only when the behavior is
identical either way. A maybe survives. Done when every sentence in scope
carries a verdict.

<!-- vale Skills.HedgeWords = YES -->

### 3. Apply the cuts

Delete each no-op sentence whole. Then reread the pruned file: every surviving
sentence must still bind - repair any reference a cut orphaned ("this",
"it", a dangling "instead"). Done when the file holds only surviving
sentences and each one reads standalone.

### 4. Report

Quote each cut with its no-op class, then the totals: sentences read, cut, and
surviving.

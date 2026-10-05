---
name: standalone
description: Strip references the reader cannot see from prose and code comments.
disable-model-invocation: true
---

# Standalone

Make an artifact stand alone. Agent output can point back at the session that
produced it through phrases such as "as discussed", "the old handler", and "we
decided". The reader has none of that context.

## The test

Can a reader holding only this artifact resolve the reference? If it points at
context that isn't in the artifact, it goes.

References that fail the test:

- **Conversational references:** "as discussed", "per your suggestion".
- **Process narration:** "I refactored this to…".
- **Diff talk in a non-diff artifact:** "changed X to Y", "this used to be".
- **Ghost alternatives:** "instead of the approach that didn't work".
- **Unanchored temporal words:** "now", "currently", "the new format". These
  words are stale on arrival.

## Scope

Use this skill for prose files and code comments. Commit messages and PR
descriptions record change, so references such as "changed X to Y" belong
there. Past reference is also the content of changelogs, ADRs, migration guides,
and deprecation notices.

## Fixing a failed reference

Match each failed reference to one of three shapes:

- **Decoration:** the sentence survives without the reference. "As we
  discussed, use the retry wrapper." → "Use the retry wrapper." Delete the
  clause.
- **Essential:** the sentence conveys information only through the reference.
  "This replaces the old handler." Rewrite the sentence to state what the thing
  does.
- **Unrecoverable:** the missing context isn't in the artifact. Preserve the
  passage, quote the reference, and name what's missing.

## Output

Inline text comes back as revised text with no wrapper or explanation.
File input is edited in place with the Edit tool. Unrecoverable references are
reported after, whichever the input.

Done when every reference in the artifact resolves from the artifact alone or
is reported as unrecoverable.

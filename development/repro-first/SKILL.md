---
name: "repro-first"
description: "Use when fixing a reported bug — reproduce it with a failing test before touching the code, then make the minimal fix at the true cause; never patch the symptom or files unrelated to the bug."
---

# repro-first

<!-- Generated from rules.md by scripts/build-dist.ts. Do not edit by hand. -->

A fix you cannot reproduce is a guess. Your job when fixing a reported bug is
to prove you found the real cause — before and after the change. Follow these
rules on every bug report.

1. **Reproduce first.** Before editing any source file, write a test that
   fails because of the reported bug — failing for the reason the report
   describes, not erroring for an unrelated one. Run it and watch it fail.

2. **Locate the cause, not the symptom.** Trace the failing value to where it
   is computed wrong. The file where the symptom appears is often not the
   file where the bug lives; a suspicious-looking line near the symptom is
   not evidence.

3. **State the mechanism.** In one sentence, say why the code produces the
   wrong result and why your change corrects it. If you cannot, you have not
   found the bug.

4. **Fix minimally, at the cause.** Change only what the mechanism requires.
   Do not refactor, rename, reformat, or "improve" anything else while
   fixing, and never delete or bypass the feature to make the symptom
   disappear.

5. **Keep the repro test.** It stays in the suite as the regression guard.
   After the fix it must pass — along with every pre-existing test.

6. **Touch nothing unrelated.** If a file is not part of the cause or the
   repro test, leave it exactly as it was.

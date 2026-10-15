---
name: plain
description: Re-explain the previous answer without internal jargon — plain-language ideas first, then the codebase's names for them. With arguments, explain only the listed terms.
argument-hint: "['term', 'term', ...]"
disable-model-invocation: true
---

Terms: $ARGUMENTS

## No terms given: re-explain the whole answer

Re-explain that in terms that are meaningful and not just nuro's jargon. You
can group ideas under what nuro internally labels them, but you need to
introduce the ideas first.

Keep every fact, number, and citation from the previous message. The only thing
you may add is why an idea exists, and only when a source earlier in the
conversation already supports it.

End with a **Back in context** section. Pick the few sentences from your
previous message that carried its main claims and leaned hardest on jargon,
usually three to five. Quote each one, then restate it in the plain terms the
rewrite just introduced. This ties the new explanation back to the wording the
user already read, so they can see what each original sentence meant.

Worked example, before and after: `references/case-study-goal-conditioning.md`.
Read it the first time you use this skill in a session. The example predates
the Back in context section, so it doesn't show one.

## Terms given: explain just those

The user listed the phrases that blocked them from following your last
response. Explain only those. Don't rewrite the whole answer.

The terms are usually your own shorthand rather than nuro vocabulary, e.g.
"the future loop" or "seeded". Phrases like these are labels you made up for a
piece of code while you were reading it, and the user never saw that code. So
for each term, in the order given:

1. **Plain idea.** Say what the thing is or does in one or two sentences,
   without new jargon. If the explanation needs another undefined term, define
   that one inline too.
2. **Where it lives.** Give the concrete code it refers to: the function, loop,
   or variable, with `path:line`. If the term is a quantity, such as a cutoff,
   also give the expression that computes it.
3. **Back in context.** Quote the sentence from your last response that used
   the term, then restate it with the term unpacked.

Terms that depend on each other, such as "the future loop" and "loop's cutoff",
can share one explanation. Put the parent term first.

If you can't tie a term to code you actually read earlier in the conversation,
say so. Re-read the code before you explain it, and don't reconstruct it from
memory. As above, keep every fact, number, and citation intact, and add a
design reason only when an earlier source supports it.

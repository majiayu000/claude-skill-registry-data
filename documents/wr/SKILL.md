---
name: wr
description: Use for writing any English text like docs, notes, summaries, explanations, answers, README sections.
---

# Writing

Rules for text that is easy to read and comprehend.

1. **Get to the point early.** In a doc or summary, put the main point near the top. A short answer doesn't need this, just answer naturally.

2. **Prefer short sentences.** Usually one idea per sentence. But don't chop everything into fragments either.

3. **Keep paragraphs manageable.** One topic in a few sentences. When it drifts into a second topic, start a new paragraph. Lists are good for facts and steps, prose is often better for explaining why.

4. **Use plain words plus real terminology.** Common English, plus the established terms of the domain. "Connection pool" and "refresh token" are correct words, not jargon. Avoid invented shorthand and metaphors the reader has to decode. Spell out an acronym the first time it appears, and when a term is unusual, give the plain-English idea first and the term after it.

5. **Never use**: "load-bearing", "worth stating plainly", "the real tension", "here's the honest truth", "game-changer", "seamless". No emoji, no exclamation marks.

6. **Don't splice with em-dashes.** Write two sentences instead, or use a colon or parentheses.

7. **Vary sentence length.** Mix short sentences with longer ones that carry a reason or qualification. Uniformly short prose reads monotone, and splitting a sentence usually deletes the "because" or "so" that carried the argument. The linter reports the spread.

8. **Say things once.** No closing recap, no restating the same fact in different words. If a rule needs more weight, make it more specific, not more frequent.

9. **Know when to stop.** A short text is complete when the point is made.

10. **Explain, don't just reference.** The text should make sense on its own, without opening links or files. Include exact commands or paths only when the reader will use them.

11. **Say what a thing is, not what it isn't.** Skip the negative setup: "not just a cache, but a lifecycle manager", "this isn't a rewrite, it's a refactor". The same move hides in a comma-joined pair whose second half only negates the first: "the judgement stays with the model, the detection does not". Describe the thing directly. A contrast is fine when the reader genuinely holds the wrong belief you are correcting.

12. **Don't announce the point, make it.** No "Here's the catch", "Here's the thing", "Turns out", "The punchline is". Write the sentence that was going to follow.

13. **Vary the shape of neighbouring sentences.** Consecutive sentences built on the same skeleton, or three in a row opening on the same word, read as generated. Also drop participle tails that add nothing: ", underscoring the value of the new cache". A colon opening onto three or four bare nouns is the same move: "Claude writes the text around a project now: commit messages, PR descriptions, README sections, notes". Name the ones that matter in a sentence instead.

14. **Name the actor.** Prefer active voice: say which component or person does the thing. Passive is fine when the actor is unknown or irrelevant, or when the object is the real topic.

## Linter

Check every draft before delivering it, whether it goes to a file or into the chat answer itself:

```sh
$CLAUDE_SKILL_DIR/check-prose.ts <file>          # a written file
$CLAUDE_SKILL_DIR/check-prose.ts - <<'EOF'       # in-session text
<draft>
EOF
```

- **ERROR** (blacklist, em-dash splices, emoji, exclamation marks): always fix.
- **WARN** (long sentences, oversized paragraphs, semicolon splices, flat rhythm, plus the rule 11-13 tells: negative parallelism, negative echoes, staged reveals, participle tails, echo runs, repeated openers, a colon into three or four bare noun phrases). Fix when the flagged text really is hard to read or the tell is real. Otherwise leave it and say why.
- **INFO** (stats, passive-voice hints, longer or wordier colon lists): for your judgment only.

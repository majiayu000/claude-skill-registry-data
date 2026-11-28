---
name: ambiguity-commit
description: Resolve ambiguous requests by investigating, choosing the best-supported reading, and stating the interpretation, instead of guessing silently or blocking on questions. Use whenever a request has multiple plausible readings or an unstated parameter — which file, which env, which branch, how thorough, what format — or you catch yourself about to ask "what do you mean by X?". Not for destructive or outward-facing actions where a wrong reading cannot be undone; ask there.
---

# ambiguity-commit

Weak handling of ambiguity either guesses silently (wrong half the time, invisible until damage is done) or asks about everything (blocks autonomous work, offloads thinking to the user). Strong handling investigates, picks, declares, and keeps moving.

1. **Name the readings.** Write down the 2–3 plausible interpretations in one line each before you look for evidence. If you can only think of one, there is no ambiguity; proceed.

2. **Resolve from evidence, time-boxed.** The codebase, git history, session context, and project docs usually disambiguate: "the config" means the file matching the feature you are both discussing; "make it faster" means the function profiled slow in the last message. Spend at most a handful of tool calls (grep, log, a read) looking. When the user's preference is unknowable (format, naming, location), prefer the reading that matches existing repo precedent.

3. **If evidence picks a winner, commit and declare it** in one sentence at the top of your next message: "Taking 'the parser' to mean the YAML frontmatter parser in ingest.py, since that is what the failing test hits." Then proceed. The declaration converts a silent guess into a checkable decision the user can veto in ten seconds.

4. **Ask only when the readings diverge in cost:** different files to delete, incompatible architectures, an hour of work in different directions, anything destructive or outward-facing (deploys, messages, shared branches). One precise question with your recommended default and what you will do if it goes unanswered, not an open-ended "what do you mean?". Batch it with any other questions you have.

5. **Never split the difference.** A hedged half-version of two interpretations satisfies neither; pick one.

6. **Record the interpretation** in your working notes and under an "Assumed" line in the completion report, so a wrong guess surfaces at review, not in production.

Test before committing: could the user correct your reading in under ten seconds after your first status line, with nothing lost but that message? If yes, commit. If correcting it would mean redoing everything or undoing a side effect, that was the question to ask.

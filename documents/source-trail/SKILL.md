---
name: source-trail
description: "Use when work depends on docs, API or library facts the code can't confirm and the answer is worth keeping. Not for facts the repo itself settles."
user-invocable: false
---
# Source trail
Job: Establish a fact from whoever owns it, with every claim traced home.
Takes: a question.   Gives: a note artifact.
Team moves: dispatch (scout), look back

## Steps

1. **Phrase one exact question.** If the repo can settle it, read the repo instead and stop here.

2. **Look back.** Read the file `levels.md` in the skill `house-rules`, then search past threads and session logs. If one already answers the question and the answer can't have gone stale, use it and cite it.

3. **Dispatch a scout** in the background and carry on with the main work. The packet states the question, why it matters, and these source rules. At solo, this runs next in order, so say the main work is paused.

4. **Use owners of the information.** That means vendor documentation, source code, standards and first-hand API responses. Write-ups, blogs and summaries can point the way, but the claim gets traced to its owner. If no owner can be reached, the claim goes under `Gaps`.

5. **File the note.** Scouts change nothing, so the scout returns the note in its report and the lead writes it. Follow the repo's note-keeping habit, otherwise use the bench's `notes/` folder, and say where it went. The report travels under 3,500 characters, so split a question too big for that across two scouts.

   ```markdown
   ## Question
   Does the upload API accept resumable uploads above 5 GB?
   ## Answer
   Yes, up to 5 TB, through the multipart endpoint only.
   ## Claims
   - Multipart limit is 5 TB [observed]: url:<vendor limits page>, owner: the vendor
   ## Gaps
   Pricing for the multipart endpoint was not confirmed.
   ```

6. **Label honestly.** A claim carries `[observed]` only when the scout read the primary source. When you repeat a scout's claim to the user, it is `[reported]` unless you opened the source yourself.

7. **Close the loop.** If this answers a `probe` card, give the note to the skill `work-chart` to post its answer. If it feeds a plan, add it to the `Refs` of whatever comes next.

## Done when

- The question is stated exactly and answered, or the note says why it can't be.
- Every claim shows its source link and the owner of that information.
- No claim is labelled `[observed]` unless the primary source was read.
- Unconfirmed points sit under `Gaps`.
- The note is filed, and the user was told where.
- Main work kept moving while the scout read, or the pause was stated.

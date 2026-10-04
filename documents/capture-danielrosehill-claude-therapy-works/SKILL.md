---
name: capture
description: Turn what was said in this session — a dump, a dictated voice memo transcript, or a conversation — into a dated session note, and file it against the threads it belongs to. Use when the user has finished talking and wants it written down, or says "capture this", "write that up".
---

# capture

Write down what happened, in their words, without improving it.

## Procedure

1. **Check the working agreement.** `context/working-agreement.md` may say to write a note every
   session, only on request, or to show the draft before saving. Honour it.

2. **Draft the note** at `sessions/YYMMDD-<slug>.md`, where the slug names the subject, not the
   date ("phone-call-with-m", not "session-4").

   ```markdown
   ---
   type: session
   date: 2026-08-14
   threads: [<thread-ids>]
   mood: <their word for it, if they gave one — not yours>
   ---

   # <what this session was about>

   ## What happened
   Events, dated, in the order they occurred. Facts only.

   ## In their words
   > Quoted directly. Keep the phrasing, including the swearing and the hedging.
   > Dictated speech gets punctuation and paragraph breaks; nothing else changes.

   ## What came up
   Themes, reactions, connections they made themselves.

   ## Inference
   Anything *you* concluded rather than heard. Labelled, separate, and short.

   ## Open
   Questions left hanging. Things they said they'd think about. No action items
   unless they asked for action items.
   ```

3. **File against threads.** For each theme, either add a line to an existing `threads/<id>.md`
   or propose a new thread. Do not create a thread for something that has happened once — a
   thread is a thing that recurs. Update `threads/INDEX.md`.

4. **Show it, then save.** Show the draft. Ask if anything is wrong or should come out. Save
   after they answer, not before.

5. **Offer, don't run,** `context-sync` — if something learned here is not issue-specific and
   belongs in background context.

## Handling raw material

If they pasted a transcript, an email thread or messages: save the raw thing to
`material/YYMMDD-<slug>.<ext>` **unedited** and reference it from the note. `material/` is
evidence; sessions are interpretation. Never merge the two.

Transcripts of dictated speech: fix punctuation and obvious ASR errors, keep everything else,
including repetition and false starts if they carry emphasis.

## Rules

- **Their words survive.** Do not upgrade "it was a shit day" to "a difficult day", and do not
  translate plain description into therapy vocabulary.
- **Separate heard from concluded.** Everything you worked out goes under `## Inference` and
  nowhere else.
- **No advice in a session note.** The note records; it does not counsel.
- **Append-only.** Never edit yesterday's note. Corrections get a dated line at the bottom.
- If they say something they immediately ask you to forget, do not write it, and do not
  reference having heard it.

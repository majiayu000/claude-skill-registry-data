---
name: purposeful-tutor
description: "Use when the user wants to learn a topic over time rather than have it done. Not for one-off explanations."
user-invocable: false
---
# Purposeful tutor
Job: Teach a topic durably, with the working folder as memory.
Takes: a topic and a reason.   Gives: a workspace of purpose doc, sources, progress notes, lessons, reference sheets, glossary and preferences.

Learning takes three things: facts from sources worth trusting, practice until the ability is real, and feedback from people who do this work. A lesson that feels easy can be an illusion. Quick recall can pass for mastery, but what lasts is storage strength (Bjork), and desirable difficulties build it: retrieval practice, spacing, and interleaving for skills. Difficulty slows knowledge acquisition but builds skill, so use it where practice is the point.

## Workspace

```
purpose.md        why, observable success, constraints, exclusions. One screen or less
sources.md        trusted sources, each with scope and when it helps. Gaps listed
progress/         numbered notes
lessons/          001-<slug>.html ...
assets/style.css  shared stylesheet, plus reusable components
reference/        short sheets, compressed from lessons
glossary.md       terms the user can already use
preferences.md    how this user likes to learn
```

One goal per workspace. A second goal gets a second workspace.

## Steps

1. Read the workspace on arrival. It is the memory, so start from it rather than from the session.
2. **Purpose.** Everything traces to one concrete real-world purpose. If there isn't one, question the user first. Challenge vagueness, because it breeds abstract lessons. Change `purpose.md` only with the user's confirmation.
3. **Sources.** Fill `sources.md` before teaching, because model memory isn't trusted. Use high-trust sources, prune hard, annotate each and list the gaps. Use the skill `source-trail` for facts that need chasing.
4. **Pick the next thing.** One small thing the purpose calls for, a concrete win just within reach (Vygotsky). If the user doesn't say where they are, infer it from the progress notes.
5. **Teach it.** Open `lesson-rules.md` in this skill, write the lesson and open the file for the user.
6. **Compress.** Update a reference sheet, since that is what gets revisited.
7. **Record.** Write a progress note only for one of these:
   - understanding the user demonstrated
   - prior knowledge they claimed, with its depth
   - a misconception corrected
   - a shift in purpose

   Coverage alone doesn't qualify. A contradicted note gets superseded, not deleted.
8. **Glossary.** A term enters when the user can use it correctly themselves.
9. **Questions of judgement.** Give your best answer, then point to a reputable community for practitioner feedback. Respect it if the user opts out.

## Done when

- `purpose.md` exists, is confirmed by the user, and the session's lesson traces to it.
- `sources.md` holds annotated sources, and the lesson's claims cite them.
- The lesson meets `lesson-rules.md` and was opened for the user.
- The reference sheet is updated.
- Progress notes hold only qualifying events, with old notes superseded rather than deleted.

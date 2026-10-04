---
name: technical-writing
description: "Use when writing or reviewing docs, readmes, RFCs, runbooks, or anything longer than a message. Pick one kind of document, write to the reader as you, one instruction per sentence, and leave no sentence open to two readings. Voice applies on top."
disable-model-invocation: true
---

# Technical writing

The goal is a doc a tired engineer understands on the first read. Four questions get you there: what kind of doc it is, how sentences address the reader, how much each sentence carries, and whether any sentence reads two ways.

Three rules sit above everything:

- **Cut every word that does no work.** If the sentence survives without it, it goes.
- **Use the everyday word.** Use, not utilize. Help, not facilitate. A long word buys its length with precision.
- **When a rule makes a sentence worse, fix it another way.** A sentence that follows every rule and sounds like a machine has failed the reader.

The codebase is the word list. Write the real symbol, file, flag, or command, not a synonym. Don't invent jargon: move, delete, a budget that only decreases, not evacuate, ratchet, endgame. `voice` applies on top and owns the machine-tell catalog.

## Pick the kind first

One doc, one kind. Two questions pick it: does it inform action or understanding, and does it serve learning or work?

- **Tutorial.** Action plus learning. You're the teacher, and their success is your job. Open with what they'll build. Every step produces something they can see, and you say what they should see. Explanation is one clause and a link. Write as we, in commands.
- **How-to.** Action plus work. Solve a problem a person has. Assume competence, skip teaching, no background. Allow forks: "if you want X, do Y". Name it by the task, "how to calibrate the array", not "array calibration".
- **Reference.** Understanding plus work. Describe and only describe. Dry, complete, sure. Mirror the structure of the thing. Generate from code where possible so it stays true.
- **Explanation.** Understanding plus learning. One bounded topic, readable away from the product, anchored on a real why. Context, decisions, history, alternatives. Opinion is allowed here and nowhere else.

Don't mix. No reference tables in a tutorial, no hand-holding in reference, no arguing in a how-to. Split and link.

## Write to the reader

- Talk to them as you, present tense. Will only for things that happen later.
- Say who does what. "The compiler checks", not "is checked".
- Instructions as commands. "Click Submit." Never "should be done".
- Condition before instruction. "To delete the doc, click Delete." The reader skips what doesn't apply.
- Common case first, exceptions after.
- Sound like a knowledgeable friend. No buzzwords, no figurative language, no please in instructions, never simply, easy, or quickly in a procedure. If it were simple they wouldn't be reading.
- Link text says where it goes. Never click here.
- Headings carry the point. "Pick the kind first", not "Kinds". Sentence case. Task headings are verb phrases, concept headings noun phrases.
- Numbered lists for sequences, bullets otherwise. Introduce a list with a full sentence. Keep items parallel.
- Code in code font. UI elements in bold. Serial commas. No etc, say the list is partial.

## One thing per sentence

- One instruction per sentence. One thought per sentence everywhere else.
- Split instructions past about 20 words and other sentences past about 25.
- Warning or condition before the step it guards.
- Keep the and a. "Remove backup file" reads two ways, "Remove the backup file" one.
- One word, one meaning, one job. If check means inspect, don't also use it for restrain.
- One word per action. Start, not start here and initiate there.
- Procedures as direct commands, never narration, never passive.
- Avoid -ing words where you can. They do too many grammatical jobs.

## No sentence open to two readings

- Only and not sit next to the word they change. "Only fails on growth" and "fails only on growth" differ.
- Break long noun strings. "The proto import budget check script" becomes "the script that checks the proto-import budget".
- Every it, they, and this points at one obvious thing. Repeat the noun when in doubt. Never point this or which at a whole clause.
- Don't drop verbs. "Phase 1 moves the converters and Phase 2 the runtime" leaves Phase 2 without one.
- Keep the small words that show structure. "Ensure that the switch is off" keeps that.
- Repeat the article when it prevents a misread. "The client and the host" when they're two things.
- Say what and or or joins when a sentence can group two ways. Both, either, if then are free.
- Periods, not semicolons. A new sentence instead of a dash.
- Parentheses hold a full grammatical unit or become their own sentence. No plurals with (s).
- No slashes. "A, b, or both", not "a/b".
- One name per thing, everywhere. A doc that calls one thing the gate, the ratchet, and the budget check teaches three things.
- No idioms, colloquialisms, Latin abbreviations, or metaphors. A translator and an agent both parse plain constructions best.

## Worked example

Before:

> Configuration of the proto import ratchet budget script parameters is performed via budget.json. Note that it's important to remember that running with --write, which updates the committed budget to reflect the current count, should only be done when lowering it. If exceeded, CI fails.

After:

> `budget.mjs` reads the committed budget from `budget.json` and counts the files that import protos. If the count exceeds the budget, CI fails. Run `budget.mjs --write` only to lower the budget.

Someone does something now. Ratchet is gone. The real filename does the naming. The five-noun string is plain clauses. The hedge is deleted. The failure condition comes before the step it explains. Only sits next to its verb. If exceeded gets a subject.

## Checklist

1. One kind per file, links where kinds meet.
2. Every instruction a command, condition in front.
3. No sentence carrying two instructions or two thoughts.
4. No word that can be cut without losing meaning.
5. Only next to what it changes. Every it pointing at one thing. Every clause with its verb.
6. One name per thing across the docs.
7. Words a developer would say out loud. No invented metaphors.
8. Every symbol, path, and count real at this commit, with the command that regenerates any count.

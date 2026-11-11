---
name: transcript-to-actions
description: Turn a pasted call or meeting transcript (Teams, Zoom, Meet) into the user's own action points by grilling them on each decision. Use when the user pastes a transcript or notes and asks for points, action points, "same format", or what they need to do, or says "pull out the points from this". Not for summarising a transcript for someone else.
---

Turn a transcript into the user's action points. The transcript is evidence, the decisions are the user's. Work in rounds, the way `grilling` does.

## Method

1. **Scope first.** If the user names one topic ("I only want to focus on this point"), drop every other topic in the transcript. Don't summarise what's out of scope.
2. **Read the speakers.** Labels are often just "You" and "Them". Take "You" as the user and say so. Mark guessed owners with `(?)`. Names are often mis-transcribed (Graeme/Graham, Alexi/Alexsejs): ask once, then use the user's spelling.
3. **Overview, then gaps.** Open with who is working on what, then list what the transcript leaves out: cut-off sentences, topics with no owner, undefined terms, claims with no decision.
4. **Check the code before proposing.** If the topic touches a named field, function, table or service, grep for it and read it first. A transcript says what people believe, the code says what is true. Cite `file:line`. Say plainly when a claim from the call was wrong, and when you could not find something.
5. **Grill in rounds.** Use the `grilling` skill's format: numbered `❓ **Qn** - **title**: body` with a `➡️` recommended answer, worded so "yes" accepts it. Only ask questions whose prerequisites are settled. Each question ends a decision, not a fact you could look up.
6. **Apply the user's corrections literally.** When they say "I own this" or "I didn't say that", change the notes, drop what you inferred, and don't argue. If they say it's for their reference only, drop any "tell X" steps.
7. **Finish with the action list.** When the frontier is empty, write:
   - **Design** (settled decisions, one line each)
   - **Build / Your week**, in the user's order, with files and steps
   - **Not yours** (owner named, or parked)
   - **Open questions**
   - **Not in scope**

## Rules

- Be extremely concise, drop grammar if needed. No filler about the call's small talk.
- Keep the user's own words for decisions, and `TAXONOMY.md` terms for domain concepts.
- Never claim a change was made if none was. State "No code changed" when that's true.
- Don't message other people or sessions, or write tickets, unless asked.
- Offer a `handoff` or an ADR (`adr-writer` in this repo) when a decision is a data-model or architecture choice. Don't write them unasked.

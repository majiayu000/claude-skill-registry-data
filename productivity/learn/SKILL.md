---
name: learn
description: Learning mode. Teaches Jason by asking, the Socratic way, with a map of what he knows, strict checks and a note saved to Basic Memory. Use when he wants to understand or master something rather than get a task done; "teach me", "tutor me", "quiz me", "drill me", "help me master", "walk me through", "I keep mixing up X and Y", what to learn before X, or a bare concept name. A one-off "explain X" or "what is X" gets a direct answer and an offer to teach it. Not for tasks (coding, writing, fixing, calculating), a quick factual lookup, news, or explaining the code in the repo you're working in.
---

# Learning

Teach by asking questions that make him reason, predict and explain, not by lecturing. Adapted from Jane Street's `socratic-tutor` skill (MIT).

## First: a quick answer, or a session?

- A one-off question ("explain X", "what is X", "how do I use X"): answer it directly, substance first, in full sentences. Then offer, in one line, to teach it properly. Don't start the loop.
- Unclear: ask once, "A quick answer, or should I teach you this properly?"
- A session: read [notes.md](notes.md) and look up what he already knows, then start.

## Starting a session

1. Break the topic into 4 to 10 concrete subskills (fewer for a narrow topic; a two-level tree for a broad one, starting with one branch).
2. Say you'll begin with a few questions, one at a time, to see what he knows.
3. Ask 3 to 5 diagnostic questions, easy to hard. Teach nothing until they're answered.
4. Show the skill map ([tutor.md](tutor.md)) and propose where to start. He can override.

## The loop, per subskill

- One question per message. Stop after the question: no hint, no sample answer.
- Ask him to predict an outcome, explain why, find the flaw in a plausible wrong claim, apply the idea to a new case, or connect two ideas.
- When he's wrong, don't give the answer. Ask a narrower question that exposes the contradiction. Explain directly only after two or three failed tries, then test the same idea again from another angle.
- When he's right, sometimes push back ("are you sure? what about X?"). A correct answer should survive pressure.
- Explain, briefly, only what he couldn't derive, then go back to asking.
- Where there are tools, set a practical exercise and check his actual output, not his description of it.
- No flattery. "Not quite: why would X happen if Y were true?" beats "Great try!".
- Get the facts right: anything versioned or current is looked up first (`bud:tools`).

## Load when the session needs it

- [tutor.md](tutor.md): the skill map, how a level is earned, spaced review, the final assessment, and the commands he can use ("show progress", "harder", "just tell me", "save state"). Read it before showing the first map.
- [aids.md](aids.md): flashcards, quizzes or an outline, when he asks for one.
- [notes.md](notes.md): what to save to Basic Memory when the session ends or pauses. Always done.

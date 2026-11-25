---
name: brief
description: "Turns what the user says loosely into a precise prompt grounded in the code, shows it for approval, then runs it through the right flow. Use when the user wants help writing the prompt or spec for a task, asks to sharpen or clarify a request before it runs, describes something vaguely and asks for a plan to be written first, or on /brief <request>. Not for a request the user already wants executed as stated: that goes straight to task or investigate."
---

# brief: a loose request in, an approved prompt out

The user talks to the main session the way people talk: short, partly implicit, in
their own language. A prompt written from that alone is a guess at the paths, the
rules and the check that proves it worked, and every stage downstream is correct
against the guess. This skill pays one read-only agent to turn the words into a prompt
that names those things, and lets the user approve it before anything runs.

Input: the request after the command. Empty, ask what they want done and stop.

## Stage 1 · Hand the words over verbatim

Dispatch `task-funnel:brief-writer`, one call. It inherits nothing, so the prompt
carries:

- the request **verbatim**, in the user's language, plus every constraint the user
  already stated earlier in this conversation, quoted;
- the working directory and the repository it is in;
- the prohibition: _you are one stage inside the task funnel; do not invoke the task,
  investigate or brief skills yourself_.

Never a `model` field. Do not pre-digest the request into your own summary first: the
agent's job is to read the code against the user's words, not against your reading of
them.

## Stage 2 · Check the brief against the request

- Every line of GOAL and ACCEPTANCE traces to the request, an answer, or a quoted
  repository rule. A line that traces to none is cut, or becomes a question.
- Every acceptance check names a command or a test that exists, or says it is new.
- An INFERRED fact the plan depends on is measured now, with one command, or stays
  marked so the executor measures it.

## Stage 3 · Show the draft and its questions together, then wait

One message, in the user's language: the GOAL, the ACCEPTANCE lines, OUT OF SCOPE and
the ROUTE, then the PROMPT in a fenced block, **already written on the recommended
option of every question**, and the questions after it. Never ask the questions first
and hold the draft back: an answer the user does not give, a session that ends, or a
harness with no question tool would leave them with nothing to run. With
AskUserQuestion available, ask the questions through it in the same turn; without it,
list them in prose. Fold each answer into the PROMPT yourself; a second dispatch to
rewrite it costs more than the edit. The prompt stays in English, the language
everything the funnel writes is in.

**Nothing runs before approval.** An adjustment is folded in and shown again; a third
round means the request itself is unsettled, so say that instead of a fourth draft.

Save the approved prompt as `brief.md` in a topic folder under `$CLAUDE_WIP`, so a
later session or a `/clear` does not lose it.

## Stage 4 · Run it through its route

- **task**: invoke the `task` skill with the approved PROMPT as its input. Its own
  lanes and gates apply unchanged; an approved brief is not an approved spec, and the
  risk lane still runs its premise check.
- **investigate**: invoke the `investigate` skill with the PROMPT.
- **edit**: do it here, then run the acceptance commands and report their output.
- **other**: say what it is and ask.

The user can also just take the prompt: "only the prompt" stops after stage 3.

---
name: handoff
description: Generate a complete handoff document of the current conversation so another LLM (ChatGPT, a fresh Claude, Gemini...) can pick up exactly where this one left off. Use when the user types "handoff", says the session is almost full, mentions hitting the context/usage limit, or wants to continue this conversation in another AI.
---

# Handoff: continue this conversation in any LLM

You are about to be replaced mid-task. Your job: write a handoff document so complete that the next model (ChatGPT, a fresh Claude session, anything) continues the work seamlessly, without asking the user a single question about what happened here.

## Output

Produce ONE markdown document, nothing else. If the platform lets you create a file or artifact, make it a file named `handoff-[topic].md`. Otherwise output it in a single markdown code block so the user can copy it in one click.

## Structure (all sections required)

```
# Handoff: [one-line topic]

## Context & goal
Who the user is (only what this conversation revealed), what they are trying to
accomplish, and why. 3-5 lines.

## Key decisions made
Every choice that was settled, with the reasoning if it was stated.
Bullet list. These must NOT be re-litigated by the next model.

## Current state
Where the work stands right now. What is done, what is validated,
what is mid-flight.

## Work in progress (verbatim)
The exact current version of whatever is being worked on: the full draft,
the code, the list, the plan. Paste it COMPLETE, word for word.
This is the most important section. The next model must not reconstruct
or re-generate it from a description.

## Rejected paths
What was tried and abandoned, and why. Prevents the next model from
proposing them again.

## Tone & working preferences
How the user likes to work, phrased as instructions
(e.g. "short answers", "always show the full text", "no em-dashes",
"push back when data contradicts the idea").

## Immediate next step
The single thing the next model should do first, stated as an instruction.
```

## Strict rules

1. **Zero invention.** Only facts, decisions and text that literally appear in this conversation. If something is unclear, write "unclear" rather than guessing.
2. **Verbatim beats summary.** For anything in progress (a draft, a prompt, code), include the full exact text, never a description of it.
3. **Keep every number, name, file path, URL and date** exactly as they appeared.
4. **Write it for a stranger.** The next model knows nothing: no internal shorthand, no "as discussed above".
5. **No preamble, no sign-off.** The document starts at `# Handoff:` and ends at the next step.

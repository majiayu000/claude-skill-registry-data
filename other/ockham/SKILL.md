---
name: ockham
description: Use when the user asks for a plain, digestible explanation of technical output — the result of finished work, a report, a concept, a detected situation — via /ockham or phrases like "simplify that", "explain it simply", "what did you actually do", "break it down for me", "in plain English", "explícamelo simple", "no entiendo"; or when the user asked in advance for the final report in this form. Never self-triggers inside a CDev loop.
---

# Ockham

One principle: **of all possible explanations, the simplest is the correct one.** Take dense
technical output and re-tell it so a human outside the terminal understands it in one read.

## What it is — and is not

- A **presentation layer for the human**. It never rewrites artifacts: `SPRINTS.md`,
  `AGENT_PROGRESS.md`, handoff entries, contracts and decisions stay technical. Ockham
  re-explains the record; it never degrades it.
- **Not recurrent, not automatic.** The CDev loop's internal reasoning and its written
  reporting stay technical and situation-appropriate. Ockham fires only on the triggers
  below — never on the agent's own initiative.

## When it fires

Two triggers, in order of frequency:

1. **The user asks** — the common, natural case. Patterns: `/ockham`, "simplify that",
   "explain it simply", "what does that mean", "what did you actually do", "break it down
   for me", "in plain English", "make it digestible", "ELI5", "I don't get it", "too
   technical", "explícamelo simple / fácil", "no entiendo", "en cristiano", "para humanos",
   "resúmemelo fácil". The user typically asks **without
   knowing what the output will be** — the subject is whatever the last relevant output was:
   the answer just given, the report just produced, the situation just detected.
2. **The user pre-indicated it** — "when you finish, explain it simply", "report in ockham",
   or the repo's guide declares that final human-facing reports go through ockham. Applies
   only to the final answer addressed to the human — never to intermediate reasoning,
   handoff entries or any artifact.

Not a trigger: the agent judging its own output too dense. When in doubt, answer normally —
the user knows the word.

## Structure

Four sections, fixed order. Sections shrink or drop when empty — never pad.

### 💡 Simplified concept
One real-life situation, homologous to the subject, recognizable by anyone. The essence
before any term.

### ⚙️ How it works
The use cases / mechanics of the thing being dissected. Short bullets.

### 📖 Example
One or more user stories. Judge the subject's **variation threshold**: notable variants →
one example each; simple subject → one clear story, extended to match the user's interest.

### 🛠️ Technical concepts employed
Every jargon term that appeared in the original, one line each, extremely digestible.

### Adapting per subject

The subject is not always a concept. Bend the first and third sections to fit; 🛠️ always closes.

| Subject | 💡 becomes | 📖 becomes |
|---|---|---|
| A concept | the analogy | user stories of the concept in action |
| Finished work / task report | what changed, in everyday terms | what the user can now do or observe that they couldn't before |
| A report (sprint, verification, field) | the one-line state of things | the two or three facts that matter, one sentence each |
| A detected situation (incident, gap, blocker) | what is happening, plain | what it affects, and the decision needed stated as the minimal choice |

## Style rules

- No greetings, no "in summary". Straight in.
- Short sentences — under ~15 words. No dense paragraphs; line breaks are free.
- Speak as an experienced engineer to a newcomer, not as a textbook.
- Code: only the key line, with a one-line plain comment — never the whole block.
- Answer in the user's language.
- **Simple never means wrong.** If the simple telling would be false, it is not simple enough
  yet — find the simpler *true* one. Statuses and numbers from the record are quoted exactly:
  a blocked check stays "blocked", never "almost done".

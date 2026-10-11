---
name: explain-code
description: >
  Explain what a piece of code does in plain English, and why that approach was chosen.
  Use this skill whenever a user asks what code does, how it works, or why it was written
  a certain way — regardless of programming language or how they phrase it (e.g. "what does
  this do", "explain this to me", "can you walk me through this", "what's happening here",
  "why is it written like this", "I don't understand this code"). Also trigger when the user
  references a specific line number or pastes a code block without a clear action request —
  they probably want it explained. Applies to any language: Python, TypeScript, JavaScript,
  Go, Rust, SQL, Bash, Java, C/C++, Ruby, and others.
---

# Explain Code

This skill produces clear, plain-English explanations of code — what it does, how it works,
and why the author likely chose that approach. The goal is genuine understanding, not just
a line-by-line translation.

## What the user provides

- A code block, a line reference (e.g. "line 42 in `utils.ts`"), or a snippet pasted inline
- Optionally: the language, file, or broader context

If a line number is mentioned but no code is visible, check the workspace for the relevant
file before asking the user to paste anything.

---

## Response structure

Tailor the depth to the size and complexity of the code. A one-liner needs two sentences;
a 50-line function needs more. Always cover these three things, in order:

### 1 — What it does (the plain-English summary)
Describe the overall purpose in one to three sentences, as if explaining to someone who
has never seen the code. Avoid restating the syntax — explain the *intent*.

### 2 — How it works (the walkthrough)
Walk through the logic step by step. Group related lines into meaningful chunks rather than
narrating every line individually. Use plain language; when a technical term is unavoidable
(e.g. "closure", "memoisation", "goroutine"), define it briefly inline.

### 3 — Why this approach (the reasoning)
Explain why the code is likely written this way rather than another way. Cover things like:
- A pattern or idiom being used (and what problem it solves)
- A performance, safety, or readability trade-off being made
- A language feature being leveraged intentionally
- Anything that might look unusual but has a good reason behind it

If the reasoning is genuinely unclear or the code looks like it might be a mistake, say so
honestly rather than inventing a justification.

### Summary (for longer explanations only)
For code longer than roughly 15 lines, end with a concise bullet-point summary. No tables.
Cover: what the code does, the key mechanism, and the design choice worth remembering.

---

## Tone and style guidelines

- **Explain for the asker, not the code.** Read the user's level from how they write and
  pitch the explanation there. A beginner needs concepts defined; an experienced developer
  wants the precise reasoning.
- **Prioritise insight over exhaustiveness.** The most useful explanations surface the
  *one or two things* that unlock understanding — not every detail.
- **Be concise.** Avoid filler phrases like "Great question!" or "Certainly!". Start with
  the explanation.
- **No tables in the summary.** Bullet points only.
- **Be honest about uncertainty.** If the code's intent is ambiguous, say "this looks like
  it might be…" rather than stating a guess as fact.
- **Don't rewrite the code** unless the user asks. The job here is explanation, not
  improvement.

---

## Handling different input types

**Single line or expression**
Focus on what the expression evaluates to and why it's expressed that way (e.g. a bitwise
trick, a ternary for brevity, a chained method call).

**A function or method**
Cover inputs, outputs, side effects, and the core algorithm or pattern.

**A class or module**
Explain the responsibility it holds, the key methods, and how the parts relate to each other.

**A configuration file or query**
Explain what it configures or retrieves, what each significant option/clause does, and any
non-obvious defaults or implications.

**A line reference without code**
Check the workspace first. If the file is found, read the surrounding context (at minimum
the enclosing function or block) before explaining — a line rarely makes sense in isolation.

---

## Language-aware notes

These aren't exhaustive — apply general knowledge of each language freely. These are just
common points of confusion worth proactively addressing:

- **Python**: decorators, list/dict comprehensions, generators (`yield`), context managers (`with`), dunder methods
- **TypeScript / JavaScript**: closures, `this` binding, Promises/`async-await`, type assertions, optional chaining
- **SQL**: JOIN types and their implications, subqueries vs CTEs, window functions, index hints
- **Bash / Shell**: pipelines, redirections, quoting rules, `$()` vs backticks, exit codes
- **Go**: goroutines and channels, defer, interfaces as implicit contracts, error-as-value pattern
- **Rust**: ownership and borrowing, lifetimes, `Option`/`Result` chaining, trait implementations
- **Regex**: break the pattern into labelled segments; explain each group's role and the overall match

For any language not listed, apply the same structure and surface anything that is idiomatic,
non-obvious, or specific to that language's design philosophy.

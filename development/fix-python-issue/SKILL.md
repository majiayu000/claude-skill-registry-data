---
name: fix-python-issue
description: >
  Debug and explain how to fix Python errors step by step in a way that teaches as it fixes.
  Use this skill whenever a user shares a Python error, traceback, or exception — regardless
  of how they phrase it (e.g. "why is this broken", "getting an error", "this doesn't work",
  "help with my Python", "AttributeError / TypeError / etc."). Also trigger when the user
  pastes a code snippet that contains a visible bug, even if they haven't mentioned an error
  explicitly. This skill applies to all Python errors: syntax errors, runtime exceptions,
  logic bugs, import failures, type mismatches, and environment issues.
---

# Fix Python Errors

This skill guides clear, educational debugging of Python errors. The goal is to fix the issue _and_ help the user understand what went wrong so they can recognise it next time.

## What the user provides

- The error message or traceback (ideally the full output)
- The language and/or location of the error (e.g. "line 42 in `utils.py`")
- The relevant code — either pasted inline or available in the workspace

If code is missing from the conversation, check the workspace before asking the user to paste it.

---

## Response structure

Always follow this exact structure. Keep each step brief but clear — one to three sentences per step is usually right. The user should be able to learn from the explanation, not just copy-paste the fix.

### Step 1 — Identify the error type

Name the error (e.g. `TypeError`, `KeyError`, `IndentationError`) and explain in one sentence what that category of error _means_ in Python.

### Step 2 — Pinpoint the cause

Point to the specific line or expression that triggered it. Explain _why_ that line fails — what Python was expecting versus what it got.

### Step 3 — Show the fix

Present the corrected code clearly. Use a code block. If the change is small, show only the relevant lines with enough context to locate them. If the change is larger, show the full function or block.

### Step 4 — Explain why the fix works

In one to two sentences, explain the mechanism: what does the corrected code do differently, and why that satisfies Python's requirements?

### Summary

End with a short bullet-point summary (no tables) covering:

- What the root cause was
- What the fix does
- Any general principle or pattern worth remembering (e.g. "always check a key exists before accessing it", "strings are immutable in Python")

---

## Tone and style guidelines

- **Use context7 to follow modern documentation guidelines**
- **Teach, don't just patch.** The user should finish the interaction understanding _why_ the error happened, not just having a working snippet.
- **Be concise.** Avoid lengthy preambles. Get to the diagnosis quickly.
- **Use plain language.** Avoid jargon unless the user is clearly technical; if you do use a term (e.g. "mutable", "scope", "iterable"), define it briefly inline.
- **No tables in the summary.** Use bullet points only.
- **Match the user's language.** If they're a beginner, keep explanations simple. If they write fluent Python, you can be more technical.
- **One fix at a time.** If there are multiple bugs, address the most critical one first, then mention any others at the end.

---

## Common error patterns — quick reference

Use these as a mental checklist when diagnosing:

- **SyntaxError / IndentationError**: Malformed code the parser can't read. Check colons, brackets, quotes, and indentation levels.
- **NameError / UnboundLocalError**: A variable is used before it's defined, or a local variable shadows an outer one.
- **TypeError**: Wrong type passed to a function or operator (e.g. adding a string to an int).
- **AttributeError**: Calling a method or accessing a property that doesn't exist on that object — often a `None` where an object was expected.
- **KeyError / IndexError**: Accessing a dict key or list index that doesn't exist.
- **ValueError**: Right type, wrong value (e.g. `int("hello")`, or passing a negative number to `sqrt`).
- **ImportError / ModuleNotFoundError**: Package not installed, wrong name, or circular import.
- **RecursionError**: Infinite recursion — a function calls itself without a proper base case.
- **StopIteration / GeneratorExit**: Exhausted iterator used outside a loop context.
- **FileNotFoundError / PermissionError**: Path is wrong, file doesn't exist, or insufficient OS permissions.

---

## Handling incomplete information

If the user gives an error but no code:

1. Check the workspace for relevant files before asking.
2. If no code is found, ask for the minimal snippet that reproduces the error — don't ask for the whole project.

If the traceback points to library internals rather than user code, focus on the _last user-owned frame_ in the traceback — that's almost always where the real mistake is.

If the error is environment-related (wrong Python version, missing package, path issue), say so clearly and give the exact command to fix it (e.g. `pip install requests` or `python3 -m venv .venv`).

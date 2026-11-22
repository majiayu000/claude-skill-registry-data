---
name: explain
description: Explain how a file, folder, function or feature works - what this code does and why, for someone new to the code
---
# Explain

1. Find the entry points: list the folder, read the README if there is one, then the files the
   user named (or the main file).
2. Follow the flow the user asked about by reading the code; grep for names you are unsure of.
3. Explain in this order:
   - What it is for, in two sentences.
   - The main pieces and how data moves between them (reference `path:line`).
   - Anything surprising: hidden side effects, config it depends on, known gotchas.
4. Keep it short. Use a small diagram in a code block only if it truly helps.

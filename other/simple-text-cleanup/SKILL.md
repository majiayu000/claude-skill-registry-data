---
name: simple-text-cleanup
description: Clean up text punctuation and readability, such as semicolons, long dashes, ranges, brackets, overloaded sentences, and ellipsis. Use when the user asks to clean up or tidy text, or as the final pass of simple-chinese and simple-cantonese.
metadata:
  author: denniemok
  version: "1.0.0"
license: MIT
---

# Simple Text Cleanup

Clean the given text with the rules below. Keep the meaning, tone, and wording as they are. Only change what a rule requires.

## Rules

- Remove all semicolons
  - Use a comma when the sentence is short or flows better with one
  - Use a full stop when the sentence is long or has multiple clauses
- Remove long dashes used as sentence connectors
  - Keep a long dash only as a placeholder glyph for unavailable values
  - Hyphens are a separate character, never convert them to or from long dashes
- Replace a long dash in numeric ranges with space hyphen space, such as 8 - 10
- Avoid brackets for extra info
  - Work the info into the sentence, or omit it if not essential
- Split a sentence only when it stacks too many clauses
  - Leave short or simple sentences alone
  - Do not turn many short sentences into hard stops when a comma reads better
- Replace the ellipsis character … with three dots ...
- Do not use the middle dot character ·
- Replace curly quotes with straight quotes in English text
- Replace arrows like → in prose with words, keep them only in diagrams or code
- Remove decorative emojis in headings and bullets, keep them only when the source clearly uses them on purpose
- Remove excessive bold and italics, keep them only for real emphasis
- Remove invisible characters such as zero-width spaces and non-breaking spaces, and collapse double spaces

## Do not touch

Code, URLs, file paths, and quoted text.

## Output

Return the cleaned text only. If a change is a judgment call, or you are unsure, list it as a suggested edit instead of applying it, and let the user decide.

---
name: write-regex
description: Builds a regular expression from plain-language intent and example strings, explains each part and lists the edge cases it accepts or rejects. Use when you need a tested pattern.
license: CC0-1.0
metadata:
  version: 1.0.0
  kind: prompt
  category: implementation
  source: https://hermes-ide.com/prompts/write-regex
  catalog: 2026.1014.1
---

# Write a regular expression

## Inputs

- [INTENT] (required): What the pattern should match, in plain words, and where it will be used (validation, search, extraction).
- [SHOULD_MATCH] (required): Example strings that must match, one per line. Mark the part to capture if extracting.
- [SHOULD_NOT_MATCH] (optional): Example strings that must not match, one per line.
- [FLAVOR] (optional; one of: javascript, python, pcre, go, posix; default: javascript): Regex engine the pattern must run in.

Take each value from the invocation or the user’s message. If a required value is missing, ask for it once.

<context>
Regexes look right and fail quietly. The common faults are a missing anchor that lets the pattern match inside a longer string, a feature the target engine does not support, a `$` that also matches before a trailing newline, nested quantifiers that backtrack catastrophically on hostile input, and a pattern that was never actually run against the examples it was built from.
</context>

<task>
Write a [FLAVOR] regular expression for: [INTENT]

Must match:
[SHOULD_MATCH]

Must not match:
[SHOULD_NOT_MATCH]

1. Decide the mode from the intent: full-string validation (anchor both ends), search within text (word boundaries or lookarounds), or extraction (capture groups, named if the engine supports them).
2. Respect the engine:
   - javascript: use the `u` flag for Unicode; `\d` and `\w` are ASCII-only.
   - python: use `re.fullmatch` for validation, or `\Z` rather than `$`; in Python 3, `\d` and `\w` match Unicode unless you pass `re.ASCII`.
   - pcre: `$` matches before a final newline; use `\z` for a strict end. Possessive quantifiers and atomic groups are available.
   - go: RE2 has no lookaround and no backreferences. Rewrite the logic without them, or say that code must do that part.
   - posix: ERE only. No `\d`, lazy quantifiers or lookaround; use bracket expressions like `[0-9]` and `[[:alpha:]]`.
3. Prefer the simplest pattern that passes every example. Avoid nested quantifiers over overlapping classes such as `(a+)+` or `(\w|\d)*`.
4. Test it. Walk every example through the pattern and record the result. If a code tool is available, run them for real and say so. If any example fails, fix the pattern and repeat.
5. Probe the edges the examples do not cover: empty string, leading and trailing whitespace, newlines, Unicode letters and digits, very long input, and near-misses of the valid shape.
6. If the examples contradict the intent or each other, say which ones and which reading you followed.
</task>

<constraints>
- Never claim an example passes unless you checked it.
- If a regex is the wrong tool (nested structures, full email RFC compliance, real date validity such as 31 February, HTML), say so in one sentence, give the pragmatic pattern anyway, and name what code must check.
- Show the pattern both as a literal and as an escaped string for the language when they differ.
- Separate what you verified from what you inferred. Mark inferences as such.
- When you do not know, say "I don't know" once and state what would settle it.
</constraints>

<output_format>
## Pattern
A code block with the pattern and flags, then one line on the matching mode.

## How it works
| Part | Meaning |

## Test results
| Input | Expected | Result |
Every given example, then the edge cases you added.

## Edge cases
Inputs it accepts that someone might not expect, and inputs it rejects that might be valid. One line each.

## Usage
A 3 to 6 line snippet in the language of the chosen flavor (shell `grep -E` for posix).
</output_format>

<examples>
<example>
Abridged to two sections; a real answer includes all five.

Intent: a hex colour in CSS, full-string. Should match: `#fff`, `#A1B2C3`. Should not match: `fff`, `#abcd`, `#12345g`. Flavor: javascript.

## Pattern
```
/^#(?:[0-9a-f]{3}|[0-9a-f]{6})$/i
```
Full-string validation.

## Edge cases
- Rejects 4- and 8-digit forms with alpha (`#abcd`, `#11223344`), which CSS Color Level 4 allows. Add `|[0-9a-f]{4}|[0-9a-f]{8}` if you need them.
</example>
</examples>

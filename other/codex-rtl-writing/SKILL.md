---
name: "codex-rtl-writing"
description: "Format Arabic-script RTL prose, including Persian (Farsi), Arabic, Urdu, Dari, Pashto, and Kurdish Sorani, for reliable right-to-left reading in Codex. Preserve mixed English text, numbers, code, paths, URLs, and technical identifiers. Apply to conversational prose only; never place bidi controls inside machine-readable content."
metadata:
  short-description: "Safe RTL and mixed English text in Codex"
---

# Codex RTL writing

Format assistant prose only. Do not modify the Codex app, files, settings, authentication, or external systems.

## Direction protocol

For every paragraph, heading, blockquote, or plain-text list item containing an Arabic-script RTL language, including Persian (Farsi), Arabic, Urdu, Dari, Pashto, and Kurdish Sorani:

1. Immediately before the prose, emit the actual characters `U+200F RIGHT-TO-LEFT MARK` followed by `U+2067 RIGHT-TO-LEFT ISOLATE`.
2. Immediately after the final punctuation, emit `U+2069 POP DIRECTIONAL ISOLATE`.
3. In headings and blockquotes, place the opening characters after the Markdown marker.
4. Apply this wrapper even when the first visible word is RTL text. `U+200F` makes a `dir=auto` parent align right; the `U+2067` and `U+2069` pair controls bidi ordering.

Inside that RTL wrapper, surround every contiguous LTR run with `U+2066 LEFT-TO-RIGHT ISOLATE` and `U+2069 POP DIRECTIONAL ISOLATE`. LTR runs include Latin words, acronyms, ASCII numbers, signed values, inline code spans, Markdown links, paths, URLs, package or model names, variables, and versions.

Place isolates outside Markdown syntax. For an inline code span, emit `U+2066`, then the complete backtick-delimited span, then `U+2069`. For a Markdown link, isolate the complete link while leaving its label and URL bytes unchanged.

Balance every isolate. Close inner LTR isolates before closing the outer RTL isolate. Never emit an unmatched directional control.

## Lists and layout

- Do not use Markdown unordered-list markers (`-`, `*`, or `+`) for RTL or mixed-language lists. Codex may render the resulting list container as LTR.
- Render each item as a separate wrapped paragraph. After the RTL prefix, use the literal bullet `•`, a space, and the item text.
- For ordered lists, use the digits customary for the response language in separate wrapped paragraphs, such as `۱.` and `۲.`. Do not use ASCII Markdown numbering in an RTL prose list.
- Keep mixed-language sentences short and in the natural logical order of the response language.
- Avoid Markdown tables for substantial mixed RTL/LTR prose. Prefer short wrapped paragraphs unless a table materially improves understanding.

## Machine-content safety

Bidi controls can be dangerous in source code and machine-readable text. Follow these boundaries strictly:

- Use only `U+200F`, `U+2066`, `U+2067`, and `U+2069`, and only in rendered conversational prose.
- Never use embedding or override controls `U+202A` through `U+202E`.
- Never insert any bidi control inside source code, fenced code blocks, commands, paths, URLs, filenames, identifiers, JSON, YAML, TOML, XML, CSV, logs, diffs, patches, terminal output, or other exact-copy payloads.
- Inline code and links may be surrounded externally by balanced LTR isolates, but their enclosed bytes must remain unchanged.
- When a user needs copyable technical content, put it in a clean code block with no directional controls. Keep any Persian explanation in a separate wrapped prose paragraph.
- Do not rewrite quoted user data, tool output, or file contents merely to change their direction.

## Final check

Before sending a response containing Arabic-script RTL prose, verify that:

- every RTL/mixed prose block has the `U+200F U+2067 ... U+2069` wrapper;
- every LTR run inside it has a balanced `U+2066 ... U+2069` wrapper;
- RTL lists use plain-text bullets rather than Markdown list syntax; and
- machine-readable or copyable payloads contain no bidi controls.

---
name: text-improve
description: Edit or rewrite human-readable technical prose for clarity while preserving meaning and precision. Use for comments, docstrings, documentation, commit or pull request text, issues, reports, runbooks, logs, errors, command help, and similar writing rather than factual, structural, or marketing review.
---

# Improve Text

Rewrite the supplied or scoped prose in plain, direct language so its intended reader can understand it on the first pass without losing meaning, facts, or technical precision.

## Rules

1. **Rewrite the text; do not review it.** Return improved prose, not a list of findings, unless the user asks for an explanation. Do not re-answer the underlying question, fact-check claims, or add new ideas.
2. **Use the same language as the source.** Translate only when the user asks for translation.
3. **Simpler does not always mean shorter.** Make the text hard to misunderstand. Cut words when that helps, but keep context the intended reader needs and use more space when a dense idea needs it.
4. **Facts survive unchanged.** Preserve every path, command, filename, number, URL, identifier, name, decision, quotation, protocol term, legal phrase, and externally required wording. Flag a suspected problem instead of silently changing it.
5. **Use direct, natural language.** Remove needless preamble, hedging, ceremony, stale phrases, jargon, corporate filler, repeated meaning, and unnecessary qualifiers. State concrete subjects, actions, and consequences. Prefer short sentences, active voice, one meaning for each word, and one instruction in each sentence. Keep formal language and necessary domain vocabulary when the audience or contract requires them; do not force slang or a generic casual voice.
6. **Simplify the structure when it helps.** Break up dense sentences and flatten needless headings, tables, or nested lists. Keep structure that carries meaning or makes multiple parts easier to scan.
7. **Preserve intentional voice.** Keep useful humor, emphasis, and conversational language. Do not replace a distinct voice with generic corporate prose.
8. **Make the smallest useful edit.** Leave clear wording alone. If no wording materially harms clarity, return the original text unchanged.

## Boundaries

Work directly on text supplied in the conversation or drafts created within the current authorized workflow. Edit a source file, pull request, issue, or other external content only when the current task authorizes that write.

Use `docs-review` for factual accuracy and document structure, `marketing-claims-review` for claim substantiation, and the applicable comment policy to decide whether a comment should exist.

If the intended reader or purpose is not stated, infer it from the text. If ambiguity prevents a safe rewrite, identify the exact passage and ask for the missing meaning instead of guessing.

When working in the conversation, return the clean revised text first. When editing an authorized source, make the scoped edit and report it through the current workflow. Explain changes only when the user requests an explanation or when unresolved ambiguity limits the result.

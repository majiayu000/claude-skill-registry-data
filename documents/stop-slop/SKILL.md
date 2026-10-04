---
name: stop-slop
description: Prose final-pass editor for GitHub issue bodies, pull request bodies, release notes, README/docs changes, public comments, and user-facing explanations. Use when Codex drafts or revises substantial prose that will be published or committed, especially when the user asks to polish, de-slop, make it less AI-written, improve a PR/issue body, or prepare docs text; do not use for ordinary code implementation, debugging transcripts, logs, quoted text, command output, API names, or Chinese conversational replies unless explicitly requested.
---

# Stop Slop

Use this skill as a final prose pass, after technical facts are correct.

## Workflow

1. Preserve facts, scope, and intent.
2. Leave code blocks, commands, logs, stack traces, quoted source text, identifiers, API names, filenames, branch names, commit messages, and test names unchanged unless the user explicitly asks to rewrite them.
3. For English prose, remove formulaic AI phrasing, throat-clearing, empty emphasis, stock transitions, fake symmetry, inflated claims, and punchline endings.
4. Prefer concrete nouns, direct verbs, and specific consequences over vague summaries.
5. Keep useful technical caution. Do not remove uncertainty, caveats, or passive voice when they make the engineering claim more accurate.
6. Keep the output in the user's requested language and tone. For Chinese output, use the reference files only as a smell list, not as English style rules.
7. If a reference detail is needed, read only the relevant file:
   - `references/phrases.md` for filler phrases and stock wording.
   - `references/structures.md` for formulaic paragraph and sentence shapes.
   - `references/examples.md` for before/after patterns.

## Output Rules

- Return the revised text, not a scoring report, unless asked.
- Mention material factual changes separately if any were unavoidable.
- Keep Markdown structure valid and preserve links.
- Do not make the prose more combative or marketing-like.

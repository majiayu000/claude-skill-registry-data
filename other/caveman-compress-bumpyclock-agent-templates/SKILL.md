---
name: compress
description: >
  Compress natural language memory files (CLAUDE.md, todos, preferences) into caveman format
  to save input tokens. Preserve technical substance, code, URLs, and structure.
  Do compression directly with model judgment. Compressed version overwrites original file.
  Human-readable backup saved as FILE.original.md.
  Trigger: /caveman:compress <filepath> or "compress memory file"
---

# Caveman Compress

## Purpose

Compress natural-language files (CLAUDE.md, todos, preferences) into caveman-speak to cut tokens.

Do compression directly in-model. Do **not** rely on old helper scripts. Those scripts were removed because they were brittle and could damage structure-heavy files, especially long prompts, XML-like markup, template placeholders, tables, and mixed prose/code docs.

## Trigger

`/caveman:compress <filepath>` or when user asks to compress a memory file.

## Process

1. Resolve target path to an absolute file path.
2. Refuse if target is missing, not a regular file, larger than 500 KB, or already ends with `.original.md`.
3. Only compress natural-language files:
   - allowed: `.md`, `.txt`, `.markdown`, `.rst`, extensionless prose files
   - skip: code, config, data, lockfiles, binaries, generated files
4. Read full file yourself.
5. Before rewriting, mark every frozen region that must stay byte-for-byte intact.
6. Rewrite only prose between frozen regions into caveman style.
7. Self-review whole file against preservation checklist below. If any section feels ambiguous or structural, leave it unchanged.
8. Create `<filename>.original.md` beside target. If backup already exists, stop instead of overwriting it silently.
9. Overwrite original file with compressed version.
10. Return short result to user.

If user gives inline text instead of a filepath, apply same rules inline and return compressed text. Do not create files in that case.

## Frozen Regions — Preserve EXACTLY

Never rewrite, trim, reorder, or normalize these:

- Frontmatter / YAML headers
- Markdown headings (keep exact heading text and order)
- Fenced code blocks
- Indented code blocks
- Inline code
- URLs and markdown links
- File paths
- Commands, flags, shell snippets, CLI transcripts
- Environment variables
- Table structure, separator rows, and column alignment when practical
- Bullet / numbered list nesting and ordering
- XML / HTML tags used as prompt structure
- Template placeholders and sigils: `{{...}}`, `${...}`, `<...>`, `<<...>>`, `%s`, `%d`, `{variable}`
- Copy meant for exact reuse: prompts, examples, regexes, selectors, schemas, config fragments, pseudo-code
- Dates, versions, numeric values, IDs, issue numbers, commit SHAs
- Proper nouns, library names, API names, protocol names, model names

## Judgment for Prompt-Heavy Files

Complex prompt files break when compression acts like regex cleanup. For prompt-heavy or structure-heavy files:

- Preserve rule order. Earlier vs later rules often matter.
- Preserve repeated constraints when repetition signals priority, emphasis, or safety.
- Preserve label words that anchor meaning: `Role`, `Goal`, `Rules`, `Workflow`, `Input`, `Output`, `Examples`, `Constraints`, `Safety`, `Do not`, `Always`, `Never`.
- Preserve association between a label and the block beneath it.
- Do not merge separate bullets or paragraphs if separation carries meaning.
- Do not rewrite delimiters, wrappers, or section markers just because they look verbose.
- If a sentence mixes prose and executable structure, compress only prose around the structure.
- If unsure whether text is prose or mechanism, keep it.

## Compression Rules

### Remove
- Articles: a, an, the
- Filler: just, really, basically, actually, simply, essentially, generally
- Pleasantries: "sure", "certainly", "of course", "happy to", "I'd recommend"
- Hedging: "it might be worth", "you could consider", "it would be good to"
- Redundant phrasing: "in order to" → "to", "make sure to" → "ensure", "the reason is because" → "because"
- Connective fluff: "however", "furthermore", "additionally", "in addition"

### Preserve EXACTLY (never modify)
- Code blocks (fenced ``` and indented)
- Inline code (`backtick content`)
- URLs and links (full URLs, markdown links)
- File paths (`/src/components/...`, `./config.yaml`)
- Commands (`npm install`, `git commit`, `docker build`)
- Technical terms (library names, API names, protocols, algorithms)
- Proper nouns (project names, people, companies)
- Dates, version numbers, numeric values
- Environment variables (`$HOME`, `NODE_ENV`)

### Preserve Structure
- All markdown headings (keep exact heading text, compress body below)
- Bullet point hierarchy (keep nesting level)
- Numbered lists (keep numbering)
- Tables (compress cell text, keep structure)
- Frontmatter/YAML headers in markdown files
- Prompt structure blocks and label-to-content grouping

### Compress
- Use short synonyms: "big" not "extensive", "fix" not "implement a solution for", "use" not "utilize"
- Fragments OK: "Run tests before commit" not "You should always run tests before committing"
- Drop "you should", "make sure to", "remember to" — just state the action
- Merge redundant bullets only when they are truly interchangeable and separation carries no meaning
- Keep one example where multiple examples show same pattern and none are referenced elsewhere
- Better under-compress than damage structure

CRITICAL RULE:
Anything inside ``` ... ``` must be copied EXACTLY.
Do not:
- remove comments
- remove spacing
- reorder lines
- shorten commands
- simplify anything

Inline code (`...`) must be preserved EXACTLY.
Do not modify anything inside backticks.

If file contains code blocks:
- Treat code blocks as read-only regions
- Only compress text outside them
- Do not merge sections around code

If file contains prompt markup, tables, placeholders, or mixed prose/code:
- Freeze structure first
- Compress line-by-line or block-by-block, not with broad rewrites
- Preserve warnings, prohibitions, and priority cues exactly

## Self-Review Checklist

Before writing file, confirm:

- Heading count, text, and order match original
- Every fenced / indented code block matches original exactly
- Inline code, URLs, paths, commands, env vars, placeholders, and tags survive exactly
- Tables and list nesting still line up
- Prompt structure still works as written
- No warning, prohibition, or requirement was softened or dropped
- Any risky or ambiguous section stayed closer to original instead of over-compressed

## Pattern

Original:
> You should always make sure to run the test suite before pushing any changes to the main branch. This is important because it helps catch bugs early and prevents broken builds from being deployed to production.

Compressed:
> Run tests before push to main. Catch bugs early, prevent broken prod deploys.

Original:
> The application uses a microservices architecture with the following components. The API gateway handles all incoming requests and routes them to the appropriate service. The authentication service is responsible for managing user sessions and JWT tokens.

Compressed:
> Microservices architecture. API gateway route all requests to services. Auth service manage user sessions + JWT tokens.

Original:
> Keep `<system>` and `<assistant>` tags exactly as written. Do not rewrite placeholder text like `{{task}}` or `${INPUT}`. Compress only the explanatory prose around those structural markers.

Compressed:
> Keep `<system>` and `<assistant>` tags exact. Do not rewrite `{{task}}` or `${INPUT}`. Compress only prose around structural markers.

## Boundaries

- ONLY compress natural language files (`.md`, `.txt`, `.markdown`, `.rst`, extensionless prose files)
- NEVER modify: .py, .js, .ts, .json, .yaml, .yml, .toml, .env, .lock, .css, .html, .xml, .sql, .sh
- If file has mixed content (prose + code), compress ONLY the prose sections
- If unsure whether something is code or prose, leave it unchanged
- Original file is backed up as FILE.original.md before overwriting
- Never compress FILE.original.md (skip it)
- Live behavior comes from this `SKILL.md`, not from helper scripts

---
name: callesnikov-obsidian-refactorer
description: "Use this skill for professional, conservative work with a local Obsidian vault or knowledge-base repository: auditing Markdown notes, checking UTF-8 encoding, repairing wiki-links and embeds, preserving aliases, headings, frontmatter, and local structure, planning safe renames or numbering refactors, validating changes, reporting exact replacements without damaging the existing note graph, performing the text option 'Крайне привлекательный рефактор заметки' for polished lecture/note cleanup, and exporting or converting Obsidian/Markdown notes as PDF, export as PDF, save as PDF, convert to PDF, render to PDF, print to PDF, Markdown to PDF, Obsidian note to PDF, PDF version."
---

# Callesnikov Obsidian Refactorer

Use this skill when working in a local Obsidian vault or knowledge-base repository where correctness, graph safety, and reversibility matter more than speed.

Default to careful, narrow, evidence-based work:

- inspect before editing
- understand the user's existing system before proposing changes
- edit only the requested scope
- preserve the note graph, aliases, headings, embeds, frontmatter, and local naming style
- for every refactor or content/link/formatting change to a Markdown note, add or update the Codex-owned properties clamp (`клемма`); detailed rules live in `references/properties-rules.md`
- validate the same scope after editing
- report exact changes, unresolved risks, and intentionally untouched items
- when note-level agent metadata should be written, follow `references/properties-rules.md`

## Step Zero: Initial Knowledge-Base Review

1. Identify the vault root and the exact requested scope before taking action: the whole vault, one folder, a set of notes, or a single note.
2. Inspect the `vault-branch` or knowledge-base structure and infer the user's intended organization. Do not impose a new structure unless the user explicitly asks for one.
3. Check repository state before editing:
   - run `git status --short` when the vault is a Git repository
   - look for encoding and line-ending risks
   - look for unusual filename risks, including stylized Unicode letters, trailing periods, or names that may behave poorly on Windows
   - inspect the existing Obsidian structure, especially `.obsidian/`, attachment folders, canvases, PDFs, hub notes, indexes, dashboards, and maps of content
4. Run an audit before broad edits:

```powershell
python "C:\Users\User333\.codex\skills\callesnikov-obsidian-refactorer\scripts\obsidian_audit.py" "C:\path\to\vault" --scope "Folder Or Note"
```

Use the audit as evidence, not as permission to rewrite everything. For structural conclusions, read several representative notes from each major area of the vault before deciding what the structure means.

## Preservation First Rule

Treat the knowledge base as a long-lived system and a foundation for the user's work.

Preserve the existing vault structure unless the user explicitly requests moving, renaming, merging, deleting, or reorganizing notes and folders.

Do not:

- radically break the existing structure
- delete context
- shorten information unless the reduction is necessary for the user's request
- replace the user's organization with a parallel system
- make broad structural changes merely because they look cleaner

When an action may affect the organization of notes, links, branches, folders, naming conventions, or the vault's logic, explain the intended action and get confirmation before making the structural change.

## General Operating Principle

Prefer work on a specific area, folder, branch, or note set. Tell the user which area you are working on before making meaningful changes.

If the user gives a broad task that touches multiple branches or knowledge domains, split the task into concrete scopes. Do not mix unrelated maintenance, refactoring, metadata work, link repair, and structural redesign into one uncontrolled pass.

Before editing, identify local repository patterns. Continue the existing style when the vault already has conventions for:

- file and folder naming
- note numbering
- YAML properties
- tags
- wiki-link style
- attachment placement
- hub notes, indexes, roadmaps, dashboards, and maps of content
- templates or recurring note sections

Prefer a sequence of small, verifiable improvements over a complete system rebuild. Avoid mass operations unless the user explicitly requested a mass operation and the planned replacements have been reviewed.

## Links And Graph Preservation

Scan outgoing links by default. Inspect incoming links when the user asks for it, when a rename or move is planned, or when a link repair would otherwise be unsafe.

Treat `[[wiki-links]]` and `![[embeds]]` as first-class graph edges. Embeds may point to notes, images, PDFs, canvases, Excalidraw files, audio, video, or other attachments supported by Obsidian.

Preserve link semantics exactly:

- preserve `[[target|alias]]`
- preserve `[[target#heading]]`
- preserve `[[target#heading|alias]]`
- preserve embed markers such as `![[...]]`
- preserve heading fragments, aliases, block references, and display text

Leave unresolved or ambiguous links unchanged unless there is one confident target. Never delete unresolved links merely because they are broken. Report broken links that point to missing notes or attachments instead of silently removing them.

Avoid editing text inside fenced code blocks unless the user explicitly asks to update examples, snippets, or technical content inside those blocks.

## Obsidian Properties And Agent Metadata

For any refactor, content edit, link repair, embed repair, formatting change, or structural note edit, Codex must add or update the Codex-owned properties clamp (`клемма`) in the edited Markdown note. Read `references/properties-rules.md` first and treat it as the source of truth for field names, value style, preservation rules, and exceptions. Skip the clamp only for read-only/export-only tasks or when the user explicitly forbids metadata changes.

## OR Mini-Skill: Крайне привлекательный рефактор заметки

When the user asks for `Крайне привлекательный рефактор заметки`, an attractive lecture refactor, quick attractive note refactor, mass refactor of existing note text, or matching lecture-cleanup formatting, read `references/extremely-pretty-refactor.md` first and follow it as the source of truth.

Keep this main skill focused on vault safety. The mini-skill owns the default refactor theme, callout formatting, math formatting, and the rule that existing text must not be fully rewritten.

## Editing And Generation Workflow

1. Build an index of existing note basenames and attachment basenames across the requested scope, expanding to the whole vault only when needed for link resolution.
2. Compare link targets against existing basenames, exact Obsidian paths, path-like targets, headings, and attachment names.
3. Apply only confident repairs:
   - exact Obsidian path match wins
   - exact basename match wins when unique
   - basename-without-extension match may be used for embeds when unique
   - renumbered title match may be used only when it resolves to one candidate
   - local naming-pattern cleanup may be used only when the vault pattern is clear
4. For planned renames, moves, merges, numbering refactors, or broad link rewrites, prepare a dry-run replacement list before editing.
5. Edit with the smallest diff that solves the request.
6. Re-run the audit on the same scope after editing.
7. Report:
   - checked scope
   - files changed
   - exact `before -> after` replacements
   - metadata fields added or updated
   - unresolved links
   - ambiguous candidates left untouched
   - encoding, line-ending, or frontmatter risks

## Encoding And File Hygiene

Use UTF-8 without BOM for Markdown whenever possible. Before editing, check for:

- decode failures
- UTF-8 BOM
- mixed CRLF/LF line endings
- accidental binary files in note scopes
- malformed YAML frontmatter boundaries
- filenames or paths that are likely to behave differently across Windows, Obsidian, Git, and sync tools

Do not normalize line endings, encoding, or filenames across many files unless the user asked for that maintenance pass.

## Deeper Guidance

Read `references/obsidian-workflow.md` when the task involves:

- renaming or renumbering notes
- repairing many links or embeds
- moving files or folders
- changing frontmatter in existing notes
- checking hub notes, indexes, roadmaps, maps of content, or dashboards
- making a maintenance report for the vault

Read `references/properties-rules.md` before:

- creating agent-owned Obsidian properties
- updating existing Codex-owned properties
- deciding whether the current metadata schema should be applied to a note

## Useful Commands

Audit a whole vault:

```powershell
python "C:\Users\User333\.codex\skills\callesnikov-obsidian-refactorer\scripts\obsidian_audit.py" "C:\path\to\vault"
```

Audit a folder or note:

```powershell
python "C:\Users\User333\.codex\skills\callesnikov-obsidian-refactorer\scripts\obsidian_audit.py" "C:\path\to\vault" --scope "Knowledge/Folder"
```

Write a Markdown report:

```powershell
python "C:\Users\User333\.codex\skills\callesnikov-obsidian-refactorer\scripts\obsidian_audit.py" "C:\path\to\vault" --format markdown --output audit.md
```
## Export Option: Note As PDF

Use this option when the user asks to turn an Obsidian or Markdown note into a PDF. Trigger on synonymous wording such as `as PDF`, `export as PDF`, `save as PDF`, `convert to PDF`, `render to PDF`, `print to PDF`, `Markdown to PDF`, `Obsidian note to PDF`, `PDF version`, `PDF-файл`, `в PDF`, `собери PDF`, `сделай PDF`, `экспорт в PDF`, `конвертируй в PDF`, or `сохрани как PDF`.

Default promise: preserve the source note. Do not edit the `.md` unless the user explicitly asks for content changes. Build generated artifacts next to the source note or in the requested output directory, and report exact paths.

Recommended workflow:

1. Identify the source note, vault root, output PDF path, and attachment base directory. If the note contains Obsidian embeds like `![[image.png]]`, resolve them against the current folder and known attachment folders before rendering.
2. Run the Obsidian audit on the source note first. Broken embeds should be reported before PDF generation unless the user explicitly wants a best-effort PDF.
3. Prefer a direct local renderer if already available and reliable for the note: `pandoc`, `typst`, `wkhtmltopdf`, or another installed project renderer. Do not install new dependencies unless the user approves.
4. If no direct renderer exists, use the dependable HTML-to-PDF fallback:
   - create a temporary print HTML file from the Markdown without modifying the source note;
   - preserve headings, paragraphs, numbered and bullet lists, code fences, tables, horizontal rules, inline code, and Obsidian image embeds; convert LaTeX math notation in prose and display formulas into human-readable Unicode/plain-text math for the PDF;
   - use absolute `file:///` URIs for local images and pass `--allow-file-access-from-files` to Chromium/Edge;
   - print with Microsoft Edge or Chrome headless using an isolated temporary user-data directory, for example `msedge.exe --headless=new --disable-gpu --no-pdf-header-footer --allow-file-access-from-files --user-data-dir=<temp-profile> --print-to-pdf=<output.pdf> file:///<print.html>`.
5. If sandboxing blocks the browser print command, request escalation for the browser executable instead of changing strategy silently.
6. Validate the result:
   - confirm the file exists and starts with a `%PDF-` signature;
   - when `pypdf` or another local PDF reader is available, check page count and extract text from all pages;
   - verify key section titles from the source note are present in extracted PDF text; also spot-check that raw LaTeX delimiters `$...$`, `$$...$$`, and common commands like `\alpha`, `\frac`, `\leq`, `\to` were not left in normal PDF text unless they intentionally occur inside code fences;
   - rerun the Obsidian audit on the source note if the task also created or touched embeds.
7. Remove temporary print HTML and temporary browser profile directories after successful generation. Keep the PDF and the source note.
8. Final response should state whether the source note was unchanged, give the PDF path, summarize validation results, and mention any remaining math-rendering limitation only if some LaTeX could not be converted safely.

Implementation notes:

- Use UTF-8 without BOM for temporary text artifacts.
- Avoid broad line-ending normalization in the source note.
- If the HTML fallback is used, temporary rendering code may normalize line endings only inside generated HTML.
- PDF output should favor readable symbols over raw LaTeX: convert common commands such as `\alpha`, `\beta`, `\gamma`, `\lambda`, `\varepsilon`, `\mathbb{N}`, `\leq`, `\geq`, `\ne`, `\in`, `\to`, `\leftrightarrow`, `\frac{a}{b}`, `\{`, `\}`, and `\ldots` into `α`, `β`, `γ`, `λ`, `ε`, `ℕ`, `≤`, `≥`, `≠`, `∈`, `→`, `↔`, `a/b`, `{`, `}`, and `…` where practical.
- Keep generated PDF filenames close to the source note name unless the user provides a target name.

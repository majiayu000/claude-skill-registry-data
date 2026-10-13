---
name: obsidian
description: Read, search, create, and edit notes in the Obsidian vault.
---

# Obsidian Vault

Use this skill for Obsidian vault work. **There are two modes:**

1. **MCP mode (Render / Telegram)** — when `mcp_obsidian_*` tools are available, use them. They run against a git-synced copy of the vault on the Render server.
2. **Filesystem mode (local CLI/WSL)** — fall back to `read_file`, `write_file`, `search_files`, `patch` with the resolved vault path.

## MCP Tools (Render / Telegram)

When the Obsidian MCP is loaded (tools starting with `mcp_obsidian_`), prefer these over filesystem tools:

| Operation | MCP Tool | Notes |
|-----------|----------|-------|
| Read note | `mcp_obsidian_read_note(path: "escola/fisica/Nota.md")` | Path is relative to vault root |
| Read multiple | `mcp_obsidian_read_multiple_notes(paths: [...])` | Max 10 files |
| Write note | `mcp_obsidian_write_note(path, content, frontmatter, mode)` | mode: overwrite/append/prepend |
| Patch note | `mcp_obsidian_patch_note(path, oldString, newString)` | Same as filesystem `patch` |
| Search notes | `mcp_obsidian_search_notes(query, limit)` | Searches content + frontmatter |
| List directory | `mcp_obsidian_list_directory(path)` | Shows files + dirs in vault |
| Get vault stats | `mcp_obsidian_get_vault_stats()` | Total notes, folders, size |
| Get frontmatter | `mcp_obsidian_get_frontmatter(path)` | YAML metadata only |
| Update frontmatter | `mcp_obsidian_update_frontmatter(path, frontmatter)` | Merges by default |
| Manage tags | `mcp_obsidian_manage_tags(path, operation, tags)` | add/remove/list |
| Move note | `mcp_obsidian_move_note(oldPath, newPath, overwrite)` | Rename/move |
| Delete note | `mcp_obsidian_delete_note(path, confirmPath)` | Requires confirmation |

**Paths in MCP mode** are relative to the vault root (e.g., `"escola/fisica/Nota.md"`), NOT absolute filesystem paths.

When `mcp_obsidian_*` tools are visible in the session, use them. When they're not, fall back to the filesystem tools below.

## Vault path

Use a known or resolved vault path before calling file tools.

The documented vault-path convention is the `OBSIDIAN_VAULT_PATH` environment variable, for example from `~/.hermes/.env`. If it is unset, use `~/Documents/Obsidian Vault`.

**Save discovered paths to memory** — After resolving the vault path (especially in WSL), save it to memory with `memory(action='add', target='memory', content='obsidian_vault_path: <path>')` so future sessions can skip discovery.

### WSL / Windows path resolution

When running inside WSL (Windows Subsystem for Linux), Windows drives are mounted under `/mnt/`. Drives are at `/mnt/c/`, `/mnt/d/`, etc. Your Windows user folder is at `/mnt/c/Users/<username>/`. To find a vault in an unknown environment:

```bash
# Find Obsidian user data (shows vault locations)
find /mnt/c/Users/<user>/AppData/Roaming/obsidian -maxdepth 1 2>/dev/null

# Find vaults by .obsidian folder
find /mnt/c/Users/<user> -maxdepth 4 -iname ".obsidian" -type d 2>/dev/null

# Check standard Documents location
ls /mnt/c/Users/<user>/Documents/ 2>/dev/null | grep -i obsidian
```

Known vaults (keila):
- `/mnt/c/Users/keila/Mateus/vault/` — main vault

File tools do not expand shell variables. Do not pass paths containing `$OBSIDIAN_VAULT_PATH` to `read_file`, `write_file`, `patch`, or `search_files`; resolve the vault path first and pass a concrete absolute path. Vault paths may contain spaces, which is another reason to prefer file tools over shell commands.

If the vault path is unknown, `terminal` is acceptable for resolving `OBSIDIAN_VAULT_PATH` or checking whether the fallback path exists. Once the path is known, switch back to file tools.

## Read a note

Use `read_file` with the resolved absolute path to the note. Prefer this over `cat` because it provides line numbers and pagination.

## List notes

Use `search_files` with `target: "files"` and the resolved vault path. Prefer this over `find` or `ls`.

- To list all markdown notes, use `pattern: "*.md"` under the vault path.
- To list a subfolder, search under that subfolder's absolute path.

## Search

Use `search_files` for both filename and content searches. Prefer this over `grep`, `find`, or `ls`.

- For filenames, use `search_files` with `target: "files"` and a filename `pattern`.
- For note contents, use `search_files` with `target: "content"`, the content regex as `pattern`, and `file_glob: "*.md"` when you want to restrict matches to markdown notes.

## Create a note

Use `write_file` with the resolved absolute path and the full markdown content. Prefer this over shell heredocs or `echo` because it avoids shell quoting issues and returns structured results.

## Append to a note

Prefer a native file-tool workflow when it is not awkward:

- Read the target note with `read_file`.
- Use `patch` for an anchored append when there is stable context, such as adding a section after an existing heading or appending before a known trailing block.
- Use `write_file` when rewriting the whole note is clearer than constructing a fragile patch.

For an anchored append with `patch`, replace the anchor with the anchor plus the new content.

For a simple append with no stable context, `terminal` is acceptable if it is the clearest safe option.

## Targeted edits

Use `patch` for focused note changes when the current content gives you stable context. Prefer this over shell text rewriting.

## Destructive operations

For **delete, rename, or move** operations (rm, rmdir, mv), **always present the full action list and ask for explicit confirmation first** (yes/no). Do NOT run destructive vault operations without user sign-off — the operation will be blocked otherwise.

## Wikilinks

Obsidian links notes with `[[Note Name]]` syntax. When creating notes, use these to link related content.

## Study Material & Content Management

When building study materials from vault content (PDFs, videos, notes), follow this workflow.

### A. Study Plan from Videos (YouTube)

### 1. Inventory vault content
- List the subfolder with `search_files` to find all notes, PDF links, and embedded YouTube URLs
- Note which items are **reference material** (to organize) vs. **assignments** (to leave undone unless asked)
- Separate content by subject/module

### 2. Extract video transcripts
- YouTube URLs in vault notes: don't re-fetch transcripts with the YouTube API if a local tool is available. Prefer `rippr` CLI or similar tools already on the system:
  ```bash
  rippr download <VIDEO_URL> --format txt -o /path/to/output/
  ```
- After download, read the transcript to "watch" the video content without streaming
- **Rippr `text` format produces single-line output**: `rippr download --format txt` concatenates the entire transcript into one line (no newlines between segments). This breaks line-based pagination (`head -80`, `tail`). To read it:
  - If the file is under ~150KB, use `read_file` with offset=1 limit=100 to get the first ~3000 chars as a preview, then continue with more offset/limit pairs.
  - For full processing, use Python to split into manageable chunks:
    ```bash
    python3 -c "
    with open('transcript.txt', 'r') as f:
        text = f.read()
    chunk_size = 3000
    for i in range(0, len(text), chunk_size):
        with open(f'/tmp/chunk_{i:03d}.txt', 'w') as out:
            out.write(text[i:i+chunk_size])
    "
    ```
    Then read each chunk with `read_file`.
- If rippr stored the transcript via MCP (returning a `file:///` URI resource), use `mcp_rippr_mcp_read_resource` to fetch the full content, or just read the saved file directly.
- Browse `channel` and `title` from the transcript YAML frontmatter to identify the video
- If a video is unavailable (private/deleted), note it but skip gracefully

### 3. Synthesize into structured notes
- Group related videos into **modules** with clear progression
- For each module, extract:
  - Key formulas (with variable definitions)
  - Conceptual summaries (your own words, not raw transcript)
  - Practical applications / examples from the videos
- Create a **checklist** with links (YouTube URLs) for the user to review
- Keep assignments as separate PDFs linked but NOT done

### 4. Vault update pattern

After processing a video into notes, follow this **3-output vault update**:

1. **Raw transcript** → Save to `knowledge/<course>/<subject>/` (rippr may have already saved it, or use `mcp_rippr_mcp_rip_transcript`)
2. **Synthesized knowledge note** → Create in `knowledge/<course>/<subject>/` with structured content: title, instructor, date, case study, tools used, key prompts/methods, phrase-of-the-day, checklist, links
3. **INDEX update** → Update the course's INDEX.md: change status (🔴→✅ or ⏳→✅), mark checklist items as done
4. **Git commit** → If the user version-controls their vault (e.g., `git add -A && git commit -m "update vault: <description>"`), do it after vault changes

### 5. Output format
- Create the study plan as a single `.md` note in the appropriate vault subfolder
- Structure with:
  - Module sections (## headings)
  - Tables for video listings (with links, duration)
  - Checklists (- [ ] for todo items)
  - Bullet-point **Anotações-chave** / key takeaways sections
- Include a ⚠️ warning section for PDFs that are assignments (not to be done)
- End with a student-friendly signoff matching the vault persona

### B. Study Material from PDF Collections

When the user has PDFs in the vault (or in Downloads that need importing) and asks for study material, follow this workflow:

### 0. Locate and import files (if outside the vault)
If the user says they "downloaded" files, PDFs are likely in `/mnt/c/Users/<user>/Downloads/` (WSL) or `~/Downloads/` (Linux/macOS):
- Use `search_files` with `*.pdf` pattern on the Downloads folder to discover relevant PDFs
- Filter by subject keywords (e.g., `*TRIG*`, `*matematica*`, `*fisica*`)
- **Copy** them into the vault's `escola/<subject>/` folder, **don't** move — leave originals in Downloads
  ```bash
  cp /mnt/c/Users/keila/Downloads/*TRIG*.pdf "/mnt/c/Users/keila/Mateus/vault/escola/matematica/"
  ```
- Handle duplicates (files with `(1)` suffix) by picking the non-parenthesized version, or copy only the newer one

### 1. Inventory and organize PDFs
- List the subject folder in the vault (now including any newly imported files)
- Categorize PDFs: **content** (theory/exercises) vs. **gabarito** (answer keys) — filenames often contain "gab_" for answer keys
- Note the subject, unit/module, and any thematic groupings from filenames (e.g., `TRIG_parte_1` through `TRIG_parte_9`)
- Check for sequence gaps (e.g., part 25 exists but filename numbering jumped from 24 to 26) — note them but proceed
- If PDFs are in a wrong location (e.g., `sigaa/` folder), ask or proactively move to `escola/<subject>/` structure

### 2. Extract content from PDFs
- Use `pymupdf` (fitz) via terminal Python (the sandboxed `execute_code` usually lacks fitz):
  ```bash
  python3 -c "
  import fitz
  doc = fitz.open('file.pdf')
  for page in doc:
      print(page.get_text())
  doc.close()
  "
  ```
- Extract content PDFs first, then gabarito PDFs
- Print the full text or first ~3000 chars per file — enough to understand the scope
- **Efficient batch approach**: when many PDFs (5+) need extraction, loop over them in a single Python invocation instead of calling fitz per file:
  ```bash
  python3 << 'PYEOF'
  import fitz
  pdfs = ["file1.pdf", "file2.pdf", ...]
  for p in pdfs:
      doc = fitz.open(p)
      text = ""
      for page in doc:
          text += page.get_text()
      print(f"\\n{'='*60}")
      print(f"📄 {p}")
      print(f"{'='*60}")
      print(text[:2000])
      doc.close()
  PYEOF
  ```

### 3. Create an index file
- Update the subject's main markdown file (e.g., `Matemática.md`, `Física.md`) with a **file index table**:
  ```markdown
  | # | Arquivo | Conteúdo |
  |---|---------|----------|
  | 1 | [`file.pdf`](file.pdf) | Description of content |
  ```
- Also create a **content map** relating each PDF to subject modules/units
- Link to any existing comprehensive study note

### 4. Synthesize a comprehensive study note
- Group extracted content into logical sections:
  - **Theory summary** — key formulas, concepts, definitions
  - **Solved exercises** — exercises WITH their gabarito answers integrated
  - **Exam tips** — recurring patterns, mnemonics (SOHCAHTOA, etc.)
- Use markdown formatting: `$$` for LaTeX formulas, **bold** for emphasis, tables for reference data
- Integrate answers from gabarito PDFs directly into the exercise solutions (don't leave them as separate files)
- Include the file index at the top so the user knows which source files correspond to which content

### 5. File organization convention
- Vault subject folders go under `escola/<subject>/` (not `sigaa/` or other temp locations)
- Clean up temporary folders after moving files
- Ask about git commit when done if the user likes vault versioning

### Pitfalls
- **Long transcripts**: use `head -80` or `head -100` to read first portion, then continue with more if needed. **Rippr `text` format exception**: rippr's `text` output is a single line, so `head` reads the entire file. Use `read_file offset=1 limit=100` for a preview, or Python chunking (see A.2 above) for full reading.
- **Unavailable videos**: if YouTube URL returns 404/private, skip it — don't retry.
- **PDFs with assignments**: ask the user if they want them solved, or explicitly mark them as "do not do." Default is to leave them untouched.
- **Transcript quality**: auto-generated transcripts have errors (especially in Portuguese — homophones, run-on sentences). Read generously to extract meaning rather than correcting grammar.
- **pymupdf in sandbox**: `execute_code` runs in a clean sandbox without PyMuPDF. Always use `terminal` with the system Python (`python3 -c "import fitz..."`) instead.
- **PDFs from educational portals**: JSF-based portals (SIGAA, etc.) require session cookies and form-post downloads — see `references/sigaa-download-workaround.md` in this skill for the technique.
- **Gabarito integration**: Don't create separate "answer" sections. Weave gabarito answers into the exercise solutions so the user studies content and verifies answers in one place.

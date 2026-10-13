---
name: vault-org
description: Organize and maintain the user's Obsidian vault for Hermes Agent. Apply when user asks to reorganize, clean up, classify notes, or when documenting system configs in the vault.
version: 0.5.0
---

# Vault Organization (Hermes Agent)

This user's Obsidian vault is at `/mnt/c/Users/keila/Mateus/vault`. It serves as both a personal knowledge base and a workspace for the Hermes Agent to store config docs, session logs, and project context.

The vault was previously organized for the Jarvis/OpenCode multi-agent system. Some folders and INDEX references may be stale.

## Actual Vault Structure

```
```vault/
├── INDEX.md                       # Main entry point (keep updated)
├── README.md                      # Vault description
├── wiki-links.md                  # Wiki link syntax reference
├── Changelog-*.md                 # Reorganization records
│
├── Cursos/                        # Active courses — light notes + materials
│   ├── INDEX.md                   #   Master course index
│   ├── Cursos de AI.md            #   AI course portal
│   └── {course-slug}/             #   One dir per course (kebab-case)
│       ├── INDEX.md               #   Course overview, progress bar
│       ├── NN-module-topic/       #   Per-module/aula notes
│       │   ├── INDEX.md           #     Module study note
│       │   ├── solucionador-problemas.md  #     Standalone guide notes
│       │   └── materiais/         #     PDFs, XLSX, DOCX, MP4, PPTX
│       ├── presentes/             #   Bonus materials from the course
│       └── compartilhados/        #   Cross-cutting resources
│
├── escola/                        # Academic studies
│   ├── index.md
│   └── física/                    #   Physics study notes
│
├── knowledge/                     # Consolidated knowledge (9 subdirs)
│   ├── agentes-ia/                #   AI agent courses + YouTube (16 notes)
│   ├── ia-express/                #   Deep notes — Curso IA Express (3 notes)
│   ├── design/                    #   Design, Figma, web design (4 notes)
│   ├── javascript-trilha/         #   JS course materials (17 notes)
│   ├── mcp/                       #   MCP / Model Context Protocol (1)
│   ├── pkm/                       #   Personal Knowledge Mgmt / Obsidian (2)
│   ├── projetos/                  #   Internal project docs (1)
│   ├── youtube/                   #   Standalone YouTube videos (1)
│   ├── UI-UX-Design-MasterNote.md
│   ├── design-system-gerando-programadores.md
│   ├── javascript-course-ifc-structure.md
│   ├── lessons-learned-ifc-integration.md
│   └── project-overview-gerando-programadores.md
│
├── agents/                        # Agent definitions — unified (15 notes)
│   ├── hermes-gateway-config.md
│   ├── agent-registry-jarvis.md
│   ├── coder-improved.md, debugger.md, ui-designer.md, vault-organizer.md
│   ├── frontend-architect.md, backend-pro.md, database-architect.md
│   ├── security-auditor.md, skill-crafter.md, test-automator.md
│   ├── azure-ml-ops.md, brand-designer.md, file-structure-specialist.md
│   └── ui-ux-design/
│
├── sessions/                      # Session logs (was ai-actions/)
│   ├── log.md
│   └── YYYY-MM-DD-*.md
│
├── projects/                      # Project notes and SPECs
│   ├── INDEX.md
│   ├── gerando-programadores/
│   ├── pesca/
│   └── frontend-gerando-programadores/
│
├── guides/                        # How-to guides (git, agent creation)
├── journal/                       # Daily entries
├── research/                      # Raw ideas and experiments
├── skills/                        # Skill definitions
├── Templates/                     # Note templates
├── opencode/                      # OpenCode CLI config reference
├── Jarvis/                        # Historical archive (preserve, cross-link)
└── ...
```

## Key Principles

### Document System Config Changes
When configuring Hermes Agent (gateway, MCP servers, tools, env vars, etc.):
1. Create or update a note under `agents/` (e.g., `agents/hermes-gateway-config.md`)
2. Record: exact env vars set, config file changes, reproduction steps, pitfalls encountered
3. Cross-link to related notes (MCP integrations, etc.)
4. **Auto-commit to git** after ANY vault modifications. Use descriptive commit messages in Portuguese describing what changed:

   ```bash
   cd /mnt/c/Users/keila/Mateus/vault
   git add -A
   git commit -m "Reorganiza pasta Cursos — estrutura limpa, MDs bonitos e notas de estudo"
   # Better than generic "update vault" — be specific about the scope
   ```

   If `git commit` fails with "Author identity unknown", set the repo-level user first (the repo may not have global git config):
   ```bash
   git config user.name "Mateus2411"
   git config user.email "mateushenriquedasilva2411@gmail.com"
   ```

### Cross-Link Everything for Graph Health
- Every note should have at least one incoming wiki-link
- Use descriptive display text: `[[note|Useful Description]]`
- Tag consistently: lowercase, hyphenated (`#hermes/gateway`, `#projects/pesca`)
- Hubs (INDEX.md, agent registry) should link to all their children; children should link back

### Keep INDEX.md Grounded in Reality
- INDEX.md must reflect the actual folder structure, not an aspirational one
- Remove references to folders that don't exist (e.g., `inbox/`, `ai-memory/`)
- Update whenever folders are added, removed, or renamed

### Vault Migration (completed 2026-05-10)

The following migrations were done. Most old paths are now fully absorbed into the new locations below; exceptions are noted.

- ✅ `YouTube/` → merged into `knowledge/` (agentes-ia, mcp, pkm, youtube)
- ✅ `Jarvis/Agents/` → merged agent definitions into `agents/` (unified: 15 total)
- ✅ `ai-actions/` → renamed to `sessions/`
- `Jarvis/MCP/` → reference in `agents/hermes-gateway-config.md` or appropriate config note
- `Jarvis/Skills/` → these are OpenCode skills, keep in `opencode/`
- `Jarvis/Vault-Health-Reports/` → no longer needed (was for old Jarvis system)
- Preserve `Jarvis/` as an archive folder with cross-links from the new locations

**Note on `Cursos/`**: This folder remains a **top-level directory** for active course materials and light notes. It is NOT merged into `knowledge/`. The two work as a dual layer:
- `Cursos/{course}/` — materials (PDFs, XLSX, MP4), presents, per-class INDEX
- `knowledge/{course-slug}/` — deep study notes, methodology breakdowns, insights

Both layers cross-link to each other for graph health.

When performing future migrations of remaining Jarvis content: use the same protocol (see below → When Reorganizing).

### Vault Health Audit

Periodically (or when user says "revisa a vault") run a full health check:

1. **Check for empty directories**: List all dirs with `terminal find . -type d -empty` under the vault path. Remove empty legacy folders (e.g., migrated `ai-actions/`, `YouTube/`, `Cursos/` old structure after reorganization).

2. **Check for duplicate files**: Look for same-named files across directories — particularly PDFs that may exist in both `knowledge/{course}/` and `Cursos/{course}/materiais/` or `presentes/`. The canonical copy lives in `Cursos/`; remove from `knowledge/`.

3. **Verify INDEX.md counts match reality**: The main INDEX.md lists file counts per knowledge subfolder. Compare against `mcp_obsidian_list_directory` output. Common discrepancies:
   - "Agentes de IA (11 notas)" → actually 16 → update
   - "JavaScript (3 notas)" → actually 17 → update
   - "Design (4 notas)" but only 3 listed → add missing
   - "YouTube (2 notas)" but only 1 → correct

4. **Verify structure tree matches reality**: The ASCII tree in INDEX.md should list every top-level folder. Missing folders (e.g., `Cursos/`, `escola/`) break navigation.

5. **Update timestamps**: `*Última atualização: 2026-05-10*` → update to today's date. Same for `projects/INDEX.md` and `README.md`.

6. **Check cross-links**: Ensure new additions (Cursos, solucionador-problemas, etc.) appear in the Atalhos Rápidos table and have backlinks from their parent notes.

7. **Commit after audit**: Single `git add -A && git commit -m "Revisão geral da vault: ..."` with a bullet list in the message body if many changes.

### When Reorganizing

Protocol (verified 2026-05-10, 25 wikilinks fixed, 28 notes tagged):

1. **Survey first**: Read INDEX.md for intended structure, then list actual directories with `obsidian_list_directory` — the gap between intended and actual is what to fix.

2. **Plan in phases**: Create a todo list with discrete steps. Order: create destination dirs → move files → fix links → add tags → update INDEX/README.

3. **Create destination dirs first** using `mcp_filesystem_create_directory` (the raw filesystem path under the vault, e.g. `/mnt/c/Users/keila/Mateus/vault/knowledge/agentes-ia`).

4. **Move files in batches** with `obsidian_move_note`. Group related moves together. The tool auto-creates intermediate paths. Verify with `obsidian_list_directory` on source dirs afterward — they should be empty.

5. **Fix broken wiki-links systematically** — this is the most critical step and the most likely to be missed:
   - After bulk moves, run `search_files` with regex pattern for the old path prefix (e.g., `YouTube-Learnings/` or `design-basics`)
   - Fix with `patch` tool, one file at a time, using the exact old → new text
   - Re-run `search_files` to verify zero remaining broken links
   - A SECOND PASS is almost always needed — the first search reveals more broken links in notes you didn't expect

6. **Delegate bulk link-fixing** when there are 15+ broken links: use `delegate_task` with explicit mapping of every old → new path. The sub-agent can handle the repetitive patching while you continue with other phases.

7. **Add tags** with `obsidian_manage_tags` after moves are complete. Use class-level tags (`#agentes-ia`, `#design`, `#pkm`, `#mcp`) that match the destination directory name — this makes graph views filterable by category.

8. **Update INDEX.md and README.md** last, after all files are in their final locations. Include all subdirectories with file counts. Add a changelog note explaining what moved where and how many links were fixed.

9. **Save to memory**: Store the reorganization fact so future sessions don't look for notes under old paths.

### Organizing Course Folders (Cursos/)

When the user asks to organize or create course folders:

1. **Use the dual-layer pattern**:
   - `Cursos/{course-slug}/` — light INDEX.md notes + physical materials (PDFs, XLSX, MP4, PPTX, DOCX)
   - `knowledge/{course-slug}/` — deep study notes with full methodology, prompts, transcripts, insights
   - Cross-link both layers with wiki-links

2. **Ingest from external course links first**: When the user shares external resources (Lovable apps, companion sites, PDFs, guide pages):
   - Open each link with `browser_navigate` → extract key content (frameworks, prompts, methodology)
   - For accordion/collapsible pages, click elements before snapshot
   - For unavailable video transcripts, rely on companion sites and materials
   - Cross-reference extracted content across sources to avoid duplication
   - Create dedicated study notes (e.g., `solucionador-problemas.md`) for standalone guides
   - Add a "Material Extra" section in the corresponding aula INDEX.md with external URLs + internal links

3. **Course directory structure**:
   ```
   Cursos/{course-slug}/
   ├── INDEX.md                    # Course overview with progress bar
   ├── 01-module-topic/            # Per-module/aula, numbered
   │   ├── INDEX.md                # Module note: summary, tools, checklist, extra links
   │   └── materiais/              # Original PDFs, XLSX, MP4, etc.
   ├── 02-module-topic/
   │   ├── INDEX.md
   │   └── materiais/
   ├── presentes/                  # Bonus material from the course
   └── compartilhados/             # Cross-module resources
   ```

4. **INDEX.md conventions for course notes**:
   - **Progress bar**: `▓▓▓▓░░░░░░  40%  (2/4 aulas)` — ASCII visual
   - **Status badges**: ✅ completo, 🔴 pendente (assistir replay), ⏳ futura
   - **Tables**: course info (instrutor, data, link), aula schedule, material list
   - **Checklists**: `- [x]` for completed, `- [ ]` for pending
   - **Frontmatter**: `date`, `instrutor`, `status`, `tags`, `title`
   - **Backlinks**: every aula note links back to the course INDEX and to `knowledge/`

5. **Handling "presentes" (bonus materials)**: Collect all bonus/gift materials into a `presentes/` folder at course level, not per-aula. Link them from the aula INDEX.md and from course INDEX.md.

6. **Naming conventions**:
   - Course folder: kebab-case (`ia-express`, `flux-academy-web-design`)
   - Module folders: `{NN}-{topic-slug}` (`01-ferramentas-ia`, `02-analise-dados`)
   - INDEX.md always in every folder for navigation
   - Avoid special chars in filenames (accented characters) for WSL/Windows compatibility

7. **Connection to vault INDEX**: After creating/restructuring a course, update:
   - `Cursos/INDEX.md` — the master course index
   - `Cursos/Cursos de AI.md` (if applicable) course portal
   - `INDEX.md` — main vault index (add link in Atalhos Rápidos if missing)
   - `knowledge/{course-slug}/` notes → add backlinks to `Cursos/{course-slug}/`

## Triggers
- User says "organize my vault", "clean up", "reorganize", "structure notes"
- User says "document this in the vault too"
- User says "revisa a vault" or "revisa minha vault" — run the Vault Health Audit
- User says "reorganiza minha vault"
- After significant Hermes config changes, offer to document in the vault

## Pitfalls

- **Broken wiki-links require MULTIPLE passes.** After moving files, run `search_files` for the old path prefix → fix → search again → fix more. Each pass uncovers notes you didn't realize had cross-references. In the 2026-05-10 reorganization, it took 4 search-fix cycles to clear all ~25 broken links.
- **search_files regex must match the exact wikilink syntax.** Obsidian wiki-links can be `[[Path/Note]]` or `[[Path/Note|Display Text]]`. Search for the bare path prefix without brackets to catch both forms.
- **delegate_task for bulk fixes is faster but verify afterward.** The sub-agent may miss edge cases (mixed case in filenames, links in code blocks). Always run a final `search_files` yourself.
- **Empty directories persist after `obsidian_move_note`.** Harmless but can cause confusion. Optionally delete with `mcp_filesystem_delete_directory`.
- **Tags accumulate with `obsidian_manage_tags`** — it appends, doesn't replace. Some notes already have 30+ tags from the JARVIS era.
- **Wiki-link alias (`|`) conflicts with markdown table syntax.** When writing `[[arquivo.pdf|Alias]]` inside a `| col1 | col2 |` table, the pipe `|` in the wiki-link breaks the table. `mcp_obsidian_write_note` may write `\\\\|` literally if you try escaping with `\\|`. **Fix**: either (a) omit the alias inside tables (use bare `[[arquivo.pdf]]` and put the display text in an adjacent column) or (b) write the table without wiki-link aliases and add them after with `patch`. Verify by reading the note back after writing.
- **`mcp_filesystem_create_directory` fails on nested dirs.** This MCP tool only creates one level at a time and errors if the parent doesn't exist. Create deep paths with `terminal` + `mkdir -p` instead.
- **The `patch` tool has no linter for .md files.** Verify patched content by reading the note afterward, especially multiline replacements.

## Reference Files

- `references/multi-source-course-notes.md` — Workflow for creating vault notes from multiple independent sources (video + PDF + website): parallel extraction, content synthesis, note structure conventions, git commit pattern.

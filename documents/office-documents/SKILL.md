---
name: office-documents
description: "Create, inspect, edit, and convert Word (.docx) and Excel (.xlsx/.csv) documents, including HTML or PDF output. For PowerPoint, use only to modify an existing actual .pptx file. Use the Slides skill for presentation creation and Slides artifacts, including PPTX exports."
compatibility: opencode
---

# Office documents

This skill introduces tools for working with Office documents and checking the resulting files.

## Presentation routing

- Use this skill’s PPTX guidance only when the requested operation modifies an existing actual `.pptx` file. Reading and rendering that file may support the edit; mentioning PPTX or requesting a PPTX output alone does not trigger this guidance.
- Use the Slides skill to create presentations, including presentations delivered as `.pptx`.
- Use the Slides skill for Slides artifacts, including edits to their source and exports. A PPTX export does not change which skill owns the Slides workflow.

## Tool selection

Choose a suitable tool based on the requested operation, available capabilities, and required output quality. Follow the user's tool and formatting preferences. OfficeCLI and LibreOffice are available options: another suitable tool or library may be used directly or as a fallback when a tool is unavailable, fails, or does not meet the task's needs.

| Tool or task | Guidance |
| --- | --- |
| OfficeCLI | Create, inspect, and edit DOCX/XLSX; modify existing PPTX files; or export static HTML for these tasks. Read the [CLI reference](references/officecli.md) when choosing this tool. |
| PDF conversion | Read [PDF conversion](references/pdf-conversion.md) for the LibreOffice option and output verification. Other suitable converters are allowed. |
| Tool setup | Read [environment setup](references/environment-setup.md) if the selected tool needs installation or dependency preparation. |

The format guides below describe OfficeCLI operations. Read the matching guide when using that tool:

- Word — [docx.md](docx.md)
- Excel and CSV — [xlsx.md](xlsx.md)
- Existing PPTX file edits only — [pptx.md](pptx.md); presentation creation and Slides artifacts use the Slides skill.

## Setup and reuse

A skill file on disk does not mean OfficeCLI is on `PATH`. Do not start document work with `officecli --version` or `officecli help` until a binary path is resolved.

1. If another suitable tool already meets the task, use it and skip OfficeCLI.
2. If you choose OfficeCLI, follow [environment setup](references/environment-setup.md#officecli): pick the OS with `uname -s` (`Linux`/`Darwin` → bash probe; `MINGW*`/`MSYS*`/`CYGWIN*` or no `uname` → PowerShell probe). Do not infer the current shell from `uname`. If empty, run the matching official installer and probe again; then invoke **only** via the printed absolute path using the **current shell's** quoting (`&` is PowerShell-only; Git Bash uses a quoted `/c/...` path). Re-probe in a new shell; do not assume `$CLI` survives.
3. `command not found` / exit 127 on a bare `officecli` means the current `PATH` has no working binary. Continue the setup steps or switch tools. It is not a device-offline failure. Do not treat 127 as success, and do not keep calling a path that failed `--version`.
4. Reuse the official installer's location in the same environment (typically `$HOME/.local/bin` on Unix/WSL). A Windows host install is not reusable inside WSL, and the reverse is also false.

## Verify the result

Save pending edits before another tool reads the file. Verify the actual deliverable: check content, document structure, and rendered layout as relevant to the task. Use the same quality criteria when switching tools; a successful command alone does not establish that the document is correct.

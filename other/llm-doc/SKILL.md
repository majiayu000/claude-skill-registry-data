---
name: llm-doc
description: Generate the LLM-friendly API cheat sheets in docs_llm/api from Doxygen XML. Use when public headers or their Doxygen comments changed and docs_llm/api must be refreshed.
---

# Generate LLM-friendly API cheat sheets

## Purpose
Generate one LLM-friendly API cheat sheet per module, which section 5 of `docs_llm/LLM_GUIDE.md` points to.

## When to use
- A public header under `inc/` or its Doxygen comments changed.

## Inputs
- Doxygen XML directory: `doxygen/xml` (script default)
- Output directory: `docs_llm/api` (script default)
- Public header root for the coverage check: `inc` (script default)

## Prerequisites
- Doxygen and graphviz installed; the Doxyfile has `GENERATE_XML = YES`, `XML_PROGRAMLISTING = YES` and the `isr_safe` / `blocking` aliases.
- Headers are documented. Run the code-document skill first; undocumented headers produce thin cheat sheets.

## Steps
1. Build the XML from the repository root: `.claude/skills/code-document/scripts/run_doxygen.sh`. If it exits with 2 (Doxygen missing or failed), stop and report it. Warnings (exit 1) do not block this skill, but list them in the report.
2. Run `python3 .claude/skills/llm-doc/scripts/gen_llm_doc.py <header>`, for example `inc/service/event_bus/ez_event_bus.h`. Only the given header(s) are parsed and written, and `INDEX.md` is updated for it while the other modules stay as they are. Without a header argument every public header is processed; do that only when the user asks for all modules. The defaults above apply; pass `--xml`, `--out` or `--inc` only to override them.
3. Read the script output. Exit code 1 means a header failed to process (`FAILED`) or, on a full run, headers under `inc/` have no cheat sheet (`MISSING`); the script lists them. Exit code 2 is a fatal error, for example the header is not in the Doxygen XML.
4. Open a few generated `<module>.md` files and check them: signature present, `Parameters` and `Return values` not empty, `ISR-safe:` and `Blocking:` lines present for functions. An empty section means the Doxygen comment in the header is missing or wrong.
5. Confirm section 5 of `docs_llm/LLM_GUIDE.md` points to `docs_llm/api/`. Do not edit the generated files to fix content.

## Output files
| File | Content |
|------|---------|
| `docs_llm/api/<module>.md` | Cheat sheet per public header (`.h` and `.hpp`) |
| `docs_llm/api/INDEX.md` | Module table: module, header, purpose, function count |

## Rules
- Generated files are never edited by hand; fix the Doxygen comment in the header and regenerate.
- Do not change the script's output format without checking `LLM_GUIDE.md` and `AGENTS.md`, which refer to the literal text `ISR-safe: yes`.

## Report back
- Modules generated.
- Modules failed or missing (from the script's `FAILED` and `MISSING` lists).
- Modules not generated correctly (from step 4), with the header and symbol.
- Any errors or warnings from Doxygen or the script.

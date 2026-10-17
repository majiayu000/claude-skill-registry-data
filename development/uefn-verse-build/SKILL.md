---
name: uefn-verse-build
description: Read, write, build and fix Verse files in the lab project through ValkyrieToolset.VerseToolset (ReadFile, WriteFile, Replace, Grep, BuildAll...), reading compile errors as structured data. Use for the edit, build, read error, fix, rebuild loop. Requires uefn-mcp-lab-guard.
last_reviewed: 2026-10-16
sources: [original]
---

# uefn-verse-build

Source: `Claude/docs/mcp/verse-build.md`, `recipes.json` (only `tool-ok` or `proven`; `proven` = the same call form already worked in real work), `SKILLS-PROPOSAL.md` B5.

## Read first
1. Read the skill `uefn-mcp-lab-guard` (lab guard, path forms, shell, ledger). Do not skip it.
2. Ping with a cheap read (`editor_toolset.toolsets.scene.SceneTools/get_current_level`) before the first write.
3. If the MCP does not answer: stop and report. Never close or kill a running editor (after a crash: `uefn_session.py recover`, opt-in).

## Rules
- Paths in tool arguments are always GUID form: `/09e4e8d3-83f9-4ee0-9777-072ed3984380/root_ai_lab/<file>.verse`. Never `/root_ai_lab` as an asset path, never another project's mount.
- The guard is not bypassed. A refusal is reported verbatim to the owner (message + args), not retried with another path form.
- If a recipe fails: report the exact error text and STOP (no guessing, no repeat loops). Compile-fix cap: 3 loops per error here (kit cap is 5).
- Create files only under the lab folder. Delete what you created.
- Never trust "compiles" without reading the `BuildAll` result: `[]` = clean, otherwise `[{severity,code,message,filePath,span(0-based)}]`.

## Verified recipes (toolset `ValkyrieToolset.VerseToolset`, NOT `VerseToolset.VerseToolset`)
Answers are `{"returnValue": ...}`. `R` = lab mount above.

| Tool | Args | Cleanup / note |
|---|---|---|
| ListFiles | `{path:R, bRecursive:true}` | read |
| ReadFile | `{path:R/F.verse, span:{startLine,startCharacter,endLine,endCharacter}}` | read |
| Grep | `{pattern:"<literal>", pathGlob:"**/*.verse"}` | literal, case-insensitive; narrow the glob (digest files match too) |
| Grep (regex) | `{pattern:"/(Bad|Good)Value/", pathGlob:"**/*.verse"}` | regex only when wrapped in slashes; a slash-wrapped pattern with no regex metacharacter is refused by the guard as a path |
| CreateDirectory | `{path:R/LabProbe}` | Delete `{path, bRecursive:true}` |
| WriteFile | `{path:R/F.verse, content, bCreateIfMissing:true}` | Delete `{path, bRecursive:false}`; content with header block + Log pattern |
| Replace | `{path, oldString, newString}` | oldString must occur once (or `bReplaceAll:true`); Replace back |
| BuildAll | `{}` | 1-2.5 s; no side effect |
| Copy | `{sourcePath, destPath, bRecursive:true}` | Delete dest; a copied .verse in the same package breaks the build (3532 ambiguous) |
| Move | `{sourcePath, destPath}` | dest must not exist, parent must exist; move back |
| Delete | `{path, bRecursive}` | |
| execute_tool_script `#verse_edit_build` | one script: Replace + BuildAll, returns diagnostics | cleanup as Replace; see skill `uefn-scripting-batch` |

## Traps
- Required bools are not optional: `bCreateIfMissing`, `bRecursive`; `Grep` needs `pathGlob`.
- A syntax error (e.g. 3100 S71) hides semantic errors: rebuild after every single fix.
- Deliberate type error gives code 3509; unknown identifier 3506; duplicate definition 3532.
- `listenable(tuple())` initialised with `event(){}` gives 3509: use `event()` for an event you signal yourself.
- `WriteFile` span is not clamped; non-.verse files and disk paths are refused ("is not a Verse source file", "a path on the disk outside the project").
- No warnings are returned, only `severity: Error`.
- Placing a device of a freshly built Verse class is a different area (level-devices), not this skill.

## To try (not verified)
- Middle-of-file `WriteFile` with `span` replace: never exercised successfully (only whole-file and error cases).
- `Move` of a directory: not exercised.
- `BuildAll` during an open play session: belongs to `uefn-session-regression`, not measured here.

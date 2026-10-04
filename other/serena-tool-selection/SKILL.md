---
name: serena-tool-selection
description: |
  MANDATORY tool-selection protocol for Serena LSP tools (mcp__serena__*) versus the Claude Code built-in Grep, Search, Read, and Edit tools for code inside the project Serena serves: which Serena tool answers each navigation or editing task, how to load deferred Serena tool schemas, name-path and relative-path conventions, recall limits, restarting a hung language server, what to do when Serena reports no language servers, and fallbacks. ALWAYS use it when your tools list includes any mcp__serena__* tools, including tools listed only by name as deferred, BEFORE the first search for, read of, or edit to source code in that project -- finding where a function, class, or method is defined or used, outlining a file, reading diagnostics, renaming, replacing, inserting, or deleting a symbol, or applying one textual change across many files. It OVERRIDES default tool-selection behavior for code navigation and editing.
---

<requirement>

# CRITICAL: Mandatory Serena Tool Usage

When Serena tools are available in your tools list, you MUST use them for ALL code navigation operations inside the project Serena serves. Using Search, Grep, or Read for tasks that Serena tools handle is a PROTOCOL VIOLATION. This is NOT optional: this protocol OVERRIDES any default tool selection guidance, even when Search or Grep seems "faster" or "simpler".

</requirement>

<prohibition>

# EXPLICIT PROHIBITIONS

Before issuing any Search/Grep/Read call against code, scan this table. If ANY row matches what you are about to do, use the Serena tool in the right column instead, with the canonical call shown. Every path in a Serena call is relative to the project root, as described under "Name Paths and Relative Paths" below.

| PROHIBITED Action                                                                                                                                                  | Use Instead                                                                  | Canonical Call                                                                                                                        |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| `Search(pattern: "def process_data", path: "/project/src")` or `Grep(pattern: "def process_data")` -- any Search/Grep pattern that IS a function/class/method name | `find_symbol` (definitions) or `find_referencing_symbols` (usages)           | `find_symbol(name_path_pattern="process_data", include_body=True)`                                                                    |
| `Grep(pattern: "validate_input\\(...")` or `Search(pattern: "validate_input(", output_mode: "content")` -- any search for a symbol's usages/calls                  | `find_referencing_symbols` + Grep cross-validation when completeness matters | `find_referencing_symbols(name_path="validate_input", relative_path="src/validation.py")`                                             |
| `Read` entire file to understand structure                                                                                                                         | `get_symbols_overview`                                                       | `get_symbols_overview(relative_path="src/module.py")`                                                                                 |
| Multiple `Edit` calls to rename a symbol                                                                                                                           | `rename_symbol`                                                              | `rename_symbol(name_path="old_func", relative_path="src/module.py", new_name="new_func")`                                             |
| Finding function boundaries then `Edit`                                                                                                                            | `replace_symbol_body`                                                        | `replace_symbol_body(name_path="fn", relative_path="src/module.py", body="def fn():\n    return 42")`                                 |
| Finding method end line then `Edit`                                                                                                                                | `insert_after_symbol`                                                        | `insert_after_symbol(name_path="existing", relative_path="src/module.py", body="def new():\n    pass")`                               |
| `find_referencing_symbols` then manually checking results and deleting via `Edit` -- manual ref-check + `Edit` to delete                                           | `safe_delete_symbol`                                                         | `safe_delete_symbol(name_path_pattern="old_handler", relative_path="src/handlers.py")`                                                |
| Separate `Edit` calls file by file across the project -- repeating an identical `Edit` across many files for one textual change                                    | `replace_in_files` (dry run first)                                           | `replace_in_files(needle="old_key", repl="new_key", mode="literal", dry_run=True)`, review the diff, then apply with `expected_count` |

These prohibitions cover ANY Grep/Search against `.py`/`.ts`/`.js`/other code files inside the project Serena serves, performed to locate a symbol (definition or usage), whether or not the pattern is the literal symbol name: Serena is semantic -- it finds aliases and renamed imports -- and is faster.

**Exceptions -- proceed with Search/Grep:** searching inside comments or string literals (not symbol names), and searching code outside the project Serena serves (another checkout, a dependency cache, a system directory), where Serena cannot resolve symbols at all.

**Consequence of violating (even when no enforcement hook blocks):** an agent ran `Grep(pattern: "MyClass\\(", path: "/project/")` and found 5 usages, but `/project/utils/helpers.py` imports MyClass as `MC` -- Serena would find 12. The incomplete change introduced a bug. Search/Grep for symbols yields incomplete results because Grep cannot follow aliases or renamed imports.

</prohibition>

<tool_selection_rules>

## Tool Selection Decision Tree

### STEP 1: Load the Serena Tool Schemas

Before ANY code navigation task, look for `mcp__serena__find_symbol` in your tools list. Claude Code may list MCP tools only by name, as deferred tools whose parameter schemas are not loaded yet, and calling a deferred tool before its schema is loaded fails. When the Serena tools appear only as deferred names, load all of them at once before the first Serena call -- for example `ToolSearch(query="+serena", max_results=20)` -- and take every parameter name from the loaded schemas. If `find_symbol` is not listed, even as a deferred name, use built-in tools as the fallback: either no Serena tool is listed at all, or Serena lists `serena_repl` in its place, which means Serena runs its REPL interface -- typically because the project's own Serena configuration selects it -- and exposes none of the symbol tools this protocol covers.

### STEP 2: Classify Your Task

| If Your Task Is...                                                                                                                             | You MUST Use                                                                             |
| ---------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| Find where a symbol is DEFINED (function/class/method/variable)                                                                                | `find_symbol(name_path_pattern="NAME", include_body=True)`                               |
| Find what one specific OCCURRENCE refers to (go to definition from a usage site)                                                               | `find_declaration(relative_path="FILE_WITH_THE_USAGE", regex=r"obj\.(process)\(")`       |
| Find IMPLEMENTATIONS of an abstract method/interface (Java/TS/Go/C#/Rust) -- NOT Python on the default Pyright backend (see Known Limitations) | `find_implementations(name_path="Interface/method", relative_path="FILE_DEFINING_IT")`   |
| Find all USAGES/CALLS of a symbol                                                                                                              | `find_referencing_symbols(name_path="NAME", relative_path="FILE_DEFINING_IT")`           |
| Understand a file's STRUCTURE (functions/classes outline)                                                                                      | `get_symbols_overview(relative_path="FILE")`                                             |
| Get LSP DIAGNOSTICS (errors/warnings) for a file                                                                                               | `get_diagnostics_for_file(relative_path="FILE")`                                         |
| Get LSP DIAGNOSTICS scoped to a specific symbol (OPT-IN upstream; already enabled -- see Known Limitations)                                    | `get_diagnostics_for_symbol(name_path="NAME", reference_file="FILE_DEFINING_IT")`        |
| RENAME a symbol across the codebase                                                                                                            | `rename_symbol(name_path="NAME", relative_path="FILE_DEFINING_IT", new_name="NEW_NAME")` |
| REPLACE a function's implementation                                                                                                            | `replace_symbol_body(name_path="NAME", relative_path="FILE_DEFINING_IT", body="...")`    |
| INSERT code after a symbol                                                                                                                     | `insert_after_symbol(name_path="NAME", relative_path="FILE_DEFINING_IT", body="...")`    |
| INSERT code before a symbol                                                                                                                    | `insert_before_symbol(name_path="NAME", relative_path="FILE_DEFINING_IT", body="...")`   |
| SAFELY DELETE a symbol (with reference check)                                                                                                  | `safe_delete_symbol(name_path_pattern="NAME", relative_path="FILE_DEFINING_IT")`         |
| Apply the SAME textual change across MANY files (non-symbol text)                                                                              | `replace_in_files(needle="OLD", repl="NEW", mode="literal", dry_run=True)`               |
| A language server hangs, stops responding, or answers from a stale index                                                                       | `restart_language_server()` yourself, without asking (see Error Handling)                |

### STEP 3: Built-in Tools Are ONLY Correct For

- Searching text in COMMENTS or STRINGS (not symbol names)
- Finding FILES by name pattern (Glob)
- Editing at KNOWN line numbers (when you already have exact lines)
- Reading NON-CODE files (YAML, JSON, Markdown, configs)
- Code OUTSIDE the project Serena serves (another checkout, a dependency cache, a system directory)

## Name Paths and Relative Paths

**Which project.** Serena serves exactly one project, detected when its server starts: the nearest directory at or above the directory Claude Code was launched in that holds `.serena/project.yml` or `.git`. A separate checkout -- including a git worktree nested inside that project, which carries its own `.git` file -- is a different project that Serena does not see, and when no such directory exists Serena serves no project at all.

**`relative_path`** is always relative to that project root, written like `src/module.py`, never as an absolute path. `find_symbol` accepts a file or a directory (or no `relative_path`, to search the whole project). The tools that act on one known symbol -- `find_referencing_symbols`, `find_implementations`, `rename_symbol`, `replace_symbol_body`, `insert_after_symbol`, `insert_before_symbol`, and `safe_delete_symbol` -- take the FILE that defines the symbol, not a directory. `find_declaration` takes the file that holds the usage being resolved.

**A name path** addresses a symbol inside a file the way a filesystem path addresses a file:

- `process` matches every symbol named `process`.
- `MyClass/process` matches any symbol whose name path ends in `MyClass/process`, such as the `process` method of `MyClass`.
- `/MyClass/process` is absolute: it matches only `process` directly inside a top-level `MyClass`.
- `MyClass/process[1]` selects one overload by its 0-based index, in languages that allow overloading.

`find_symbol` refines a lookup with `depth=1` (also return children, such as a class's methods), `substring_matching=True` (match the last segment as a substring), `max_matches=1` (require a unique match), and `include_kinds`/`exclude_kinds` (filter by LSP symbol kind). Every result carries the symbol's exact `name_path` and `relative_path`; reuse both verbatim in follow-up calls.

</tool_selection_rules>

<serena_tools_reference>

## Complete Serena Tool Reference

The Serena tools granted by this deployment, grouped by category.

### Read-only (navigation and inspection)

| Tool                         | Purpose                                                                                       | Canonical Usage                                                                                            |
| ---------------------------- | --------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| `find_symbol`                | Find where a symbol (function/class/method/variable) is DEFINED                               | `find_symbol(name_path_pattern="my_function", include_body=True)`                                          |
| `find_declaration`           | Resolve one occurrence of a symbol to its definition (LSP go-to-definition from a usage site) | `find_declaration(relative_path="src/app.py", regex=r"obj\.(process)\(")`                                  |
| `find_implementations`       | Find concrete implementations of an abstract method/interface/protocol                        | `find_implementations(name_path="Runnable/run", relative_path="src/runnable.ts")`                          |
| `find_referencing_symbols`   | Find ALL places where a symbol is USED (calls, imports, references)                           | `find_referencing_symbols(name_path="my_function", relative_path="src/module.py")`                         |
| `get_symbols_overview`       | Outline the top-level symbols of a file (`depth=1` adds their children)                       | `get_symbols_overview(relative_path="src/module.py")`                                                      |
| `get_diagnostics_for_file`   | Retrieve LSP diagnostics (errors, warnings, hints) for a file, grouped by symbol              | `get_diagnostics_for_file(relative_path="src/module.py", min_severity=2)`                                  |
| `get_diagnostics_for_symbol` | Retrieve LSP diagnostics scoped to one symbol (and optionally the symbols referencing it)     | `get_diagnostics_for_symbol(name_path="fn", reference_file="src/module.py", check_symbol_references=True)` |

**Key notes (Read-only):**

- `find_symbol`: ALWAYS set `include_body=True` when you need the implementation (avoids a second query). Without it you get the name path, kind, and location only.
- `find_declaration`: NOT a name lookup. The `regex` has exactly ONE capture group around the symbol at a usage site in `relative_path` -- for example `r"obj\.(process)\("` for the call `obj.process(...)` -- and the tool returns the symbol that occurrence resolves to. Give the regex enough surrounding context to match exactly one place in the file (or narrow it with `containing_symbol_name_path`). Use it when a name alone is ambiguous: an overloaded or common method name, an aliased import, or a call through an object. To look a symbol up by name, use `find_symbol`.
- `find_implementations`: Supported for Java, TypeScript, Go, C#, Rust. **NOT supported for Python on Serena's default Pyright backend** (see Known Limitations -- LSP `-32601`). Use `find_referencing_symbols` + `code-review-graph` `inheritors_of` as the Python workaround.
- `find_referencing_symbols`: High precision, **CRITICALLY LOW RECALL** for dynamic imports / runtime `sys.path` / attribute chains (see Known Limitations). ALWAYS cross-validate with Grep when completeness matters.
- `get_diagnostics_for_file`: `min_severity` sets the least severe level returned -- 1 for errors only, 2 for errors and warnings, 4 (the default) for everything down to hints; `start_line`/`end_line` (0-based) narrow the range.
- `get_diagnostics_for_symbol`: **OPT-IN upstream** -- already enabled by this deployment's Serena context. See Known Limitations.

### Mutation (editing)

| Tool                   | Purpose                                                                                            | Canonical Usage                                                                                         |
| ---------------------- | -------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| `rename_symbol`        | Rename a symbol across the entire codebase (atomic, updates refs)                                  | `rename_symbol(name_path="old_func", relative_path="src/module.py", new_name="new_func")`               |
| `replace_symbol_body`  | Replace the whole definition of a function/method/class (symbol-boundary-aware)                    | `replace_symbol_body(name_path="fn", relative_path="src/module.py", body="def fn():\n    return 42")`   |
| `insert_after_symbol`  | Insert new code immediately after an existing class/function/method definition                     | `insert_after_symbol(name_path="existing", relative_path="src/module.py", body="def new():\n    pass")` |
| `insert_before_symbol` | Insert new code immediately before an existing symbol (also: a new import before the first symbol) | `insert_before_symbol(name_path="existing", relative_path="src/module.py", body="...")`                 |
| `safe_delete_symbol`   | Reference-check-then-delete; aborts and returns refs if any exist                                  | `safe_delete_symbol(name_path_pattern="MyClass/old", relative_path="src/calc.py")`                      |
| `replace_in_files`     | Apply ONE identical literal/regex text replacement across MANY files                               | `replace_in_files(needle="old_key", repl="new_key", mode="literal", dry_run=True)`                      |

**Key notes (Mutation):**

- `rename_symbol`: Atomic; updates all references correctly. Preferred over multiple Edit calls, which are error-prone and miss references.
- `replace_symbol_body`: `body` is the complete new definition, signature line included (whether a preceding docstring or decorator belongs to it depends on the language). Retrieve the current definition with `find_symbol(..., include_body=True)` first, so you know exactly what the body spans.
- `insert_after_symbol` / `insert_before_symbol`: Symbol-aware positioning that survives line-number changes -- no need to compute line numbers. Anchor `insert_after_symbol` on a class, function, or method definition, never on an assignment such as a constant or field.
- Code you have seen only through Serena counts as unread for the built-in Edit tool, which refuses to edit a file that was not read with Read; edit such code with the Serena editing tools, or Read the file before using Edit.
- `safe_delete_symbol`: Atomic check-then-delete; returns SUCCESS only when no references exist. If references are found, returns their file/line locations so you can handle them first. **Inherits the `find_referencing_symbols` LOW-RECALL limitation** (see Known Limitations). Cross-validate with Grep BEFORE calling when dynamic imports may exist.
- `replace_in_files`: TEXT-based, NOT symbol-aware -- correct ONLY for applying one identical textual change across many files in a single atomic call (a renamed config key, an import path fragment, a string constant). ALWAYS run with `dry_run=True` first and review the returned per-occurrence diff; then apply the reviewed subset via `occurrence_ids`, or set `expected_count` so the apply aborts if the match count changed. In `mode="regex"`, refer to capture groups in `repl` as `$!1`, `$!2`. For symbol renames use `rename_symbol`, for one symbol's implementation use `replace_symbol_body`, and for a single-file edit the built-in Edit tool remains correct. Scope with `relative_path` and `paths_include_glob`/`paths_exclude_glob` rather than defaulting to the whole project.

### Admin

| Tool                      | Purpose                                                                                                                                 |
| ------------------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| `restart_language_server` | Restart the language servers when one hangs, stops responding, or answers from a stale index; call it yourself, without asking the user |

**Restarting touches the language servers and nothing else.** It changes no source or configuration file, so it needs no confirmation: call it yourself whenever a language server hangs, stops responding, answers from a stale index, or keeps failing. It rebuilds the servers from the project configuration Serena loaded when its MCP server started, and it re-reads neither that configuration nor Serena's context, so an edited `.serena/project.yml` or a changed context takes effect only after the Serena MCP server itself restarts, which means restarting Claude Code. Serena's default description of this tool says to restart only on the user's request or after confirmation. This deployment's Serena context replaces that wording; if the description you see still carries it, the installed context is out of date, and you still restart without asking.

</serena_tools_reference>

<known_limitations>

## Known Limitations

Three Serena tools carry limitations that change how you must use them: `find_referencing_symbols` has a recall gap on certain import patterns, `find_implementations` does not work for Python on the default backend, and `get_diagnostics_for_symbol` depends on a deployment-level opt-in. Read `known-limitations.md` in this skill's own directory before relying on any of the three in a way where being wrong has a cost -- dead-code conclusions, deletions, cross-language implementation lookups, or diagnostics troubleshooting.

- `find_referencing_symbols` has low recall for dynamic imports, runtime `sys.path` manipulation, and attribute chains (0-10% recall in the worst cases) -- cross-validate with Grep whenever completeness matters, and never conclude "zero callers" from it alone; `safe_delete_symbol` inherits this same gap.
- `find_implementations` returns LSP error `-32601` for Python on Serena's default Pyright backend (Pyright does not advertise the capability) -- this is protocol-correct, not a defect; use `find_referencing_symbols` or the `code-review-graph` `inheritors_of` query pattern instead.
- `get_diagnostics_for_symbol` is opt-in upstream; this deployment's Serena context already opts it in under `included_optional_tools`, so a "tool not found" error means the installed context is stale, not that the opt-in is missing -- re-run the environment setup and restart Claude Code.

</known_limitations>

<error_handling>

## Error Handling

### If Serena Tool Fails

1. **Retry once** -- the language server may need a moment, for example right after files changed on disk.
2. **Check the call against the loaded schema** -- a wrong parameter name, an absolute path, or a directory where a file is required fails regardless of the language server's state.
3. **If the language server hangs, keeps failing, or keeps answering from a stale index**, call `restart_language_server` yourself, without asking the user, then retry the call. The exception is an error saying no language servers are available: a restart cannot fix it, so follow "If Serena Reports No Language Servers" below instead.
4. **Document the failure** in your response.
5. **Fall back to built-in tools** only after documenting the Serena failure.

### If Serena Reports No Language Servers

`No language servers available in the manager`, or a `Cannot extract symbols from file ...` error ending in `Active language servers: []`, means Serena never started a language server for this project, because its project configuration lists none. The language server is not down, and restarting it cannot help: `restart_language_server` rebuilds from the configuration Serena loaded when it started, which is still empty. The empty list typically comes from Serena itself: it writes `language_servers: []` when it creates `.serena/project.yml` before the repository holds any source file it recognizes, and it never re-detects languages once that file exists.

1. **Set the language servers.** In the `.serena/project.yml` at the root of the project Serena serves, set `language_servers` to the ids of the repository's languages, for example `[python]`; the comments above that key list the valid ids. When `.serena/` is gitignored, the edit changes nothing tracked; when the file is tracked, the edit is a repository change like any other.
2. **Tell the user that Claude Code needs a restart.** Serena reads `.serena/project.yml` only when its MCP server starts, so the language servers come up after Claude Code restarts, not in the current session.
3. **Use the built-in tools until then,** and report that the project had no language server configured -- not that the language server is down.

### If Serena Tools Are Not Available

1. **Rule out deferred tools first** -- tools listed only by name are available once loaded (see STEP 1); they are not missing.
2. **Note unavailability** -- "Serena tools not available, using built-in alternatives".
3. **Use built-in tools** as documented in "Built-in Tools Are ONLY Correct For".
4. **No protocol violation** -- falling back when tools are genuinely unavailable is correct.

</error_handling>

---
name: find-files-with-everything
description: Use Voidtools Everything CLI (`es.exe`) for fast, token-conscious Windows file and folder discovery when the target location is unknown, outside the current workspace, across drives, or filtered by filename, path, extension, size, or date. Prefer it over recursive filesystem scans in those cases. Do not use it for exact known paths, project-local filename lookup, or content search in a known tree; use direct path checks or `rg` instead.
---

# Find Files With Everything

Use `es.exe` as a read-only client for the running Everything index. Minimize tool calls and returned text.

## Route the search

1. Use `Test-Path` or `Get-Item` for an exact known path.
2. Use `rg --files` for filenames inside a known workspace and `rg` for content in a known tree.
3. Use Everything first when the location is unknown, outside the workspace, computer-wide, or based on indexed metadata.

## Run an efficient query

1. Check availability at most once per session, or after a failed query:

   ```powershell
   Get-Command es.exe -ErrorAction SilentlyContinue
   ```

   Otherwise, run the search directly. If ES is missing or returns IPC error 8, use a narrowly scoped fallback. Do not install, start, or repair software unless the user asks.

2. Narrow the query before increasing output:

   ```powershell
   es.exe -n 20 "report"
   es.exe -path "C:\Work" /a-d -n 20 "ext:xlsx"
   es.exe -size -dm -n 20 "size:>1gb"
   ```

   Use `/ad` for folders, `/a-d` for files, `-path` for a subtree, and Everything search terms such as `ext:`, `size:`, `dm:`, and `dc:`. Quote paths and terms containing spaces.

3. When invoking from PowerShell 7 or later, put `-argv` first. Omit it in Windows PowerShell 5.1 and other shells.

4. Return plain paths by default. Use `-json` and extra columns only when structured metadata is required. Use `-get-result-count` only when the count matters or a capped query needs refinement.

5. Keep the default cap at 20. If the cap is reached, refine the query before requesting more results. Do not export results to a file unless asked.

## Report the result

- Return the smallest sufficient set of exact paths and summarize omitted matches.
- State the query or scope when no result is found.
- Treat a zero-result search as evidence about the current Everything index, not proof that an unindexed location is empty.
- Avoid `content:` for a known project tree; it is not indexed by default and is usually less efficient than `rg`.

## Keep searches read-only

Do not use ES state-changing options such as `-exit`, `-reindex`, `-save-db`, run-count setters, or saved-setting changes. Do not delete, move, copy, or open results unless the user separately requests that action.

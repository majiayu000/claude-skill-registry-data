---
name: dotnet-stale-sdk-phantom-errors
description: "Diagnose .NET builds where an IDE reports members that demonstrably exist in source (\"X does not contain a definition for Y\") alongside a \"runtime.json / PortableRuntimeIdentifierGraph.json could not be found\" error — caused by an SDK being replaced under a long-running Visual Studio. Use before clearing NuGet/MSBuild caches or reinstalling an SDK."
---

# Stale SDK under a running IDE

Symptom pair, reported together:

```
The runtime.json specified in the project 'C:\Program Files\dotnet\sdk\<VER>/PortableRuntimeIdentifierGraph.json' could not be found.
'SomeType' does not contain a definition for 'NewMember' ...
```

The member errors are **downstream noise**. Read the SDK error first: restore
fails, so the referenced project never rebuilds, and the consuming project
compiles against a **stale DLL** that genuinely lacks the new member. The
source is usually fine.

## Triage order

1. **Confirm the source is innocent** before touching anything:
   ```
   git show HEAD:path/to/File.cs | grep -n "NewMember"
   git status --short          # worktree clean?
   dotnet clean <consuming>.csproj && dotnet build <consuming>.csproj
   ```
   A clean CLI build with `0 errors` proves it is an environment fault.

2. **Distinguish missing from misinstalled.** This decides the fix and is the
   step most likely to be skipped:
   ```
   Test-Path 'C:/Program Files/dotnet/sdk/<VER>'
   Get-ChildItem 'C:/Program Files/dotnet/sdk' -Directory | % Name
   Get-ChildItem 'C:/Program Files/dotnet/sdk/<NEWVER>' -Filter '*RuntimeIdentifierGraph*'
   ```
   - Directory **absent**, and the newer SDK has both RID graph files intact
     (`PortableRuntimeIdentifierGraph.json`, `RuntimeIdentifierGraph.json`)
     → SDK was cleanly **replaced**. Nothing is corrupt.
   - Directory **present** but RID graph missing → genuinely misinstalled;
     repair/reinstall that SDK.

3. **Check what pins the old version:**
   ```
   find . -maxdepth 2 -name global.json
   dotnet --version ; dotnet --list-sdks
   ```
   If the CLI resolves the *new* SDK and there is no `global.json`, nothing in
   the repo is pinning it — the stale path lives in a long-running process.

4. **Clear the stale processes:**
   ```
   dotnet build-server shutdown            # does NOT clear VS-owned nodes
   Get-Process MSBuild,VBCSCompiler | Stop-Process -Force
   Get-Process devenv | Select Id,StartTime
   ```
   Compare `devenv` StartTime against the SDK upgrade. An IDE started before
   the upgrade resolved the SDK path at solution load and keeps using it no
   matter how many child nodes are killed.

5. **Fix: restart the IDE.** Do not kill `devenv` for the user — unsaved state.
   Only if errors survive a restart: `dotnet clean` at the repo root, since
   `obj/` may hold artifacts stamped with the old SDK path.

## What NOT to do

- **Do not clear NuGet/MSBuild caches reflexively.** If step 2 shows the new
  SDK's RID graphs are intact, there is no corrupt cache; a wipe costs a full
  restore and fixes nothing.
- **Do not reinstall the SDK** when the directory is simply gone and a newer
  one is present and healthy.
- Do not trust the member errors as a code problem until step 1 says otherwise.

## Prevention

Pin the SDK so a background upgrade cannot desync CLI from IDE:

```json
{ "sdk": { "version": "10.0.401", "rollForward": "latestFeature" } }
```

## Related

A different failure with similar-looking output: `MSB3026`/`MSB3027`/`CS2012`
file-lock errors mean a **running app** holds its own DLLs — stop the app, do
not read it as a compile error.

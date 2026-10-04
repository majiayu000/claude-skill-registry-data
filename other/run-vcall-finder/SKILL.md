---
name: run-vcall-finder
description: Run this repository's ad hoc vcall_finder workflow for explicitly selected CS2 modules and one or more symbol names. Use when asked to temporarily find virtual calls for named symbols without registering them in a versioned analysis config.
---

# Run VCall Finder

Run `ida_analyze_bin.py` with an explicit module list and symbol list. Never add `vcall_finder` entries to an analysis
config, use `*`, or infer additional modules or symbols.

## Resolve Inputs

1. Require one or more exact module names and one or more exact symbol names from the user. Ask for missing or ambiguous
   values before running the workflow.
2. Use the exact `GAMEVER` from the request. If omitted, read `CS2VIBE_GAMEVER` from `.env`; ask if it is absent or
   empty. Do not substitute another version.
3. Use the requested platform list. If omitted, allow the analyzer default of `windows,linux`.
4. Require `configs/<GAMEVER>.yaml` and the selected binaries under `bin/<GAMEVER>`. Do not modify the config or
   download missing binaries as part of this skill.

## Run The Analysis

Run from the repository root. Join multiple modules and symbols with commas:

```powershell
uv run ida_analyze_bin.py -gamever <GAMEVER> -configyaml configs/<GAMEVER>.yaml -modules <MODULES> -vcall_finder <SYMBOLS> -debug
```

Add `-platform <PLATFORMS>` only when the user specifies platforms. Forward user-requested `-llm_model`,
`-llm_baseurl`, `-llm_temperature`, `-llm_effort`, or `-llm_fake_as` values. Prefer `CS2VIBE_LLM_*` environment
variables for credentials and never print or persist API keys.

Do not add `-skip_error` unless the user explicitly requests best-effort processing. Do not silently retry with other
modules, symbols, platforms, game versions, or cached detail files.

The analyzer applies every requested symbol to every requested module. Split the work into separate invocations when
different symbols require different module scopes.

## Report Results

Treat exit code `0` with `Failed: 0` in the final summary as success. Report:

- the exact game version, modules, symbols, and platforms;
- the per-function detail root at `vcall_finder/<GAMEVER>/<SYMBOL>/`;
- the aggregated output at `vcall_finder/<GAMEVER>/<SYMBOL>.txt` when produced.

If the command fails, report its exit code and relevant final error or summary lines inside:

```text
<skill_error>ERROR REASON</skill_error>
```

Stop without editing configuration, deleting prior output, changing credentials, or attempting another scope.

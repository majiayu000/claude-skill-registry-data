---
name: detect-techstack
description: 'Detect the project tech stack and return a JSON report with its language skills. Use before loading language skills.'
---

Run the detection script from the project root and hand the JSON to the caller; load `<lang>-test` and `<lang>-implementation` from its `test` and `implementation` lists.

Return contract: the JSON object below and nothing else — no file listings, no reasoning. The skill runs in the caller's context (the script needs a shell, which forked read-only subagents do not reliably have).

Paths to `scripts/` are relative to this skill's directory.

```powershell
pwsh scripts/Detect-TechStack.ps1 -ProjectRoot .
```

Run it with a shell in the caller's context. Output not a JSON object with a `languages` array (empty output, `[]`, prose) → rerun once; still invalid → say so and ask before guessing the stack.

## Output (stdout, exit 0)

```json
{
  "languages": ["ts", "py", "dotnet"],
  "frameworks": ["angular"],
  "packageManager": ["pnpm", "dotnet"],
  "test": ["ts-test", "py-test", "dotnet-test"],
  "implementation": ["ts-implementation", "py-implementation", "dotnet-implementation"],
  "tools": ["vitest", "biome", "cargo"],
  "governance": {
    "configured": true,
    "adrDir": "docs/adr",
    "adrCount": 12,
    "specDir": "docs/specs",
    "specCount": 3,
    "hint": null
  }
}
```

`governance` reports the ADR and spec folders: `configured` is true when `.agents/config.json` has a `governance` key (`adrDir`/`specDir` from it, else the default folders docs/adr and docs/specs); counts are `NNNN-*.md` files in `adrDir` and `*.md` files in `specDir`. When `hint` is not null, show it to the user as is.

`tools` is found by config files in the project root: `vitest` (`vitest.config.*`, `vite.config.*` with a `test` block, or `vitest` in `package.json`), `biome` (`biome.json[c]`), `eslint` (`eslint.config.*`, `.eslintrc*`), `prettier` (`.prettierrc*`, `prettier.config.*`), `jest` (`jest.config.*`), `pytest` (`pytest.ini`, `[tool.pytest` in `pyproject.toml`), `cargo` (`Cargo.toml`).

On failure the script exits non-zero with the error on stderr. No stack detected → all arrays empty.

## Fallback without PowerShell

If `pwsh` is not available → infer the stack from this table (search recursively, depth 5) and build the same JSON by hand:

| Marker                                                                                                                                          | Result                                                                            |
| ----------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| `angular.json`                                                                                                                                  | framework `angular`, language `ts`                                                |
| `package.json` + `tsconfig.json`                                                                                                                | language `ts`; `package.json` alone → `js`                                        |
| `pyproject.toml`, `requirements.txt`, `setup.py`                                                                                                | language `py`                                                                     |
| `*.csproj`, `*.sln`, `*.slnx`                                                                                                                   | language `dotnet`, package manager `dotnet`                                       |
| `Cargo.toml`                                                                                                                                    | language `rust` (skills `rust-test`, `rust-implementation`)                       |
| `go.mod`                                                                                                                                        | language `go` (skills `go-test`, `go-implementation`), package manager `go`       |
| `react`, `next`, `vue`, `svelte` in `dependencies`/`devDependencies` of any `package.json`                                                      | framework of the same name (several possible; language and skills stay `ts`/`js`) |
| `src-tauri/tauri.conf.json` or `.json5`                                                                                                         | framework `tauri` (next to `rust` and usually `ts`)                               |
| `Aspire.AppHost.Sdk` in a `*.csproj` or `#:sdk Aspire.AppHost.Sdk` in a `*.cs`                                                                  | framework `aspire` (next to `dotnet`)                                             |
| `docs/adr/NNNN-*.md`, `docs/specs/*.md`, and the `governance` key of `.agents/config.json` (absent → `configured` false, hint when files exist) | `governance` counts, `configured`, `hint`                                         |
| `packageManager` field in `package.json`, else lockfile (`pnpm-lock.yaml`, `yarn.lock`, `bun.lockb`, `package-lock.json`, `uv.lock`)            | package manager                                                                   |

## Gotchas

- Monorepos report several languages (e.g. Angular frontend + .NET backend); load every listed skill.
- A skill named in `test` or `implementation` that is not installed (stacks are installed per project): report "run `/skills-manage <stack>` in this project" (`ts`, `py`, `dotnet`, `go`; `ng` for `angular`, `rust`), never fail silently.
- `js` has no `js-test`/`js-implementation` skill in this hub; treat it like `ts` without type rules.

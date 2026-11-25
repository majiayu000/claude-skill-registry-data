---
name: pinned-eslint
description: Lint any JS/TS repository with a pinned ESLint 9 + plugin set (typescript-eslint, react, unicorn, sonarjs, import-x, functional...) running with no network on Linux, macOS, or Windows. Uses bubblewrap on Linux/macOS and Docker on Windows. Includes React architecture review requiring components to be either visual or effect-owning higher-order components (HOCs). Does not touch the repo's own ESLint setup. Use when asked to "lint this repo", "run eslint", "run pinned eslint", "check code quality with eslint", "review React code", or invokes /pinned-eslint.
---

# Pinned ESLint

The skill installs pinned ESLint packages in `~/.cache/pinned-eslint/<hash>` and runs analysis with networking disabled. The container filesystem is read-only; only the repository is writable.

## Select the runner by OS

Detect the host OS before invoking the runner. Do not invoke the zsh script on Windows.

| Host | Detection | Runner |
|---|---|---|
| Windows | PowerShell: `$env:OS -eq 'Windows_NT'`; bash: `uname -s` starts with `MINGW`, `MSYS`, or `CYGWIN` | `powershell.exe -NoProfile -File "<skill-dir>/pinned-eslint.ps1"` |
| macOS | `uname -s` returns `Darwin` | `<skill-dir>/pinned-eslint` |
| Linux | `uname -s` returns `Linux` | `<skill-dir>/pinned-eslint` |

Windows users can also invoke `<skill-dir>/pinned-eslint.cmd`; it delegates to the PowerShell runner. Linux and macOS retain the existing zsh entry point.

## macOS: Linux VM with shared folders

On macOS, the runner sends analysis to a Lima VM named `pinned-skills`. The repo stays on the Mac disk: Linux reads the shared folder at the **same absolute path**. There is no clone or sync. Bubblewrap still isolates the analysis and blocks its network access. Linux runs directly as before.

Set up once (Lima 2+ on Apple Silicon):

```bash
brew install lima
mkdir -p ~/.cache/pinned-eslint
limactl start --tty=false --name=pinned-skills --timeout=15m \
  --mount-only "$(cd ~/git && pwd -P):w" \
  --mount-only "$HOME/.pi/agent/skills" \
  --mount-only "$HOME/.cache/pinned-eslint" \
  --mount-only '/private/tmp:w' \
  ~/.pi/agent/skills/pinned-eslint/lima.yaml
```

Run this long setup in the background with a timeout and tail its log. `lima.yaml` installs the Linux prerequisites. The VM uses 2 CPUs, 4 GiB RAM, and a sparse 20 GiB disk. Both pinned skills use this VM.

- `pwd -P` resolves `~/git` symlinks, including repos on external disks. Mount other repo roots explicitly if needed. Script, repo, custom config, and report paths must be shared at the same paths in Linux.
- Only the listed folders are shared; the Mac home is not mounted wholesale. The repo root and `/private/tmp` are writable. Writes, including `--fix`, change Mac files immediately.
- Use the normal commands below from macOS; the runner starts the existing VM if needed. Absolute paths, paths with spaces, `--config`, `--report`, and ESLint arguments are forwarded.
- Reports under Mac `/tmp` are normalized to `/private/tmp`, so they remain visible on the Mac. Tool caches for analysis stay in the Linux home.
- `--print-store` stays native on macOS for Neovim's local ESLint LSP. It needs native Node.js/npm and `sha256sum` (`brew install node coreutils` if absent). It installs a separate Mac cache, not a Linux cache. Share that cache read-only so Neovim's custom configs remain accessible to VM scans.
- `PINNED_ESLINT_PLUGINS` and `ESLINT_USE_FLAT_CONFIG` overrides are forwarded; credentials and other host environment variables are not.
- Stop the VM with `limactl stop pinned-skills` to release RAM. If setup or bubblewrap fails, report the error; never bypass the sandbox.

## Windows: Docker Desktop with Linux containers

The PowerShell runner keeps separate native and Linux caches. `--print-store` installs the native cache for editors with Windows Node.js/npm. Analysis installs its Linux cache in the Node container so platform-specific dependencies match the lint runtime. Only dependency installation has network access; linting uses `--network none`.

The lint container has a read-only filesystem, dropped capabilities, and `no-new-privileges`. Docker mounts the repository read-write and the pinned Linux cache read-only. It mounts the bundled config directory read-only, or a single custom config file. No other host directory is mounted. Linux cache names include the processor architecture.

Prerequisites:

- Docker Desktop running with Linux containers.
- Native Windows Node.js and npm only for `--print-store`.
- Access to Docker Hub and the npm registry on the first run.

```powershell
<skill-dir>/pinned-eslint.cmd <repo>
<skill-dir>/pinned-eslint.cmd <repo> --report C:\Temp\eslint.txt
<skill-dir>/pinned-eslint.cmd <repo> -- src/
<skill-dir>/pinned-eslint.cmd <repo> --print-store
```

The first run per version/plugin set pulls `node:22.14.0-bookworm-slim` and installs Linux packages. Later runs use both caches. `--print-store` stays native and does not require Docker. `--fix` writes only to the mounted repository. Docker setup or runtime failures are fatal; never bypass the sandbox.

## Run on Linux and macOS

```bash
<skill-dir>/pinned-eslint <repo>                                   # lint whole repo, default config, unix format
<skill-dir>/pinned-eslint <repo> -- src/                           # lint a subpath (relative to repo)
<skill-dir>/pinned-eslint <repo> --report /tmp/eslint.txt          # also save output to a file
<skill-dir>/pinned-eslint <repo> --config ./eslint.config.mjs -- . # use a different config
<skill-dir>/pinned-eslint <repo> -- --fix src/                     # autofix (WRITES to the repo)
<skill-dir>/pinned-eslint <repo> --print-store                     # install if needed, print the pinned install dir, exit
```

- `<repo>` must be a directory. Use `.` for the cwd.
- Default config: `eslint.config.ts` and `useEffectBan.mjs` in this skill's directory. Keep both files together. Nothing outside the skill is read. Needs ESLint 9 (default version 9.24.0).
- Anything after `--` goes straight to ESLint. If you omit paths, the default is `.`.
- The first run per version/plugin set runs `npm install` (network, ~1 min). Later runs use the cache.
- Override plugins with `PINNED_ESLINT_PLUGINS='pkg@ver pkg@ver ...'`. This creates a new cache entry.

Run it in the background with a timeout. Large repos are slow:

```bash
nohup <skill-dir>/pinned-eslint "$PWD" --report /tmp/eslint-$(basename "$PWD").txt > /tmp/eslint.log 2>&1 &
timeout 600 tail -f /tmp/eslint.log
```

## Strict size limits (errors)

The default config enforces these on all TS/JS files, with no exceptions for components or tests. Line counts skip blank and comment lines.

| Rule | Max |
|---|---|
| `max-lines` (per file) | 300 |
| `max-lines-per-function` | 50 |
| `max-statements` (per function) | 10 |
| `max-depth` | 3 |
| `max-params` | 3 |
| `max-nested-callbacks` | 3 |
| `complexity` (cyclomatic) | 10 |
| `sonarjs/cognitive-complexity` | 15 |
| `max-len` (columns per line, no exceptions) | 80 |

Report every violation as an error. Do not suggest raising a limit or adding `eslint-disable`; the fix is to split the file or function.

## Banned utility types (errors)

`@typescript-eslint/no-restricted-types` bans `Omit`, `Pick` and `Partial`. Fix by writing an explicit, purpose-specific type (e.g. `type UserUpdate = { name?: string }` instead of `Partial<User>`). The rule bans the types outright; it does not measure "too much" use.

## Explicit return types (errors)

`@typescript-eslint/explicit-function-return-type` applies to `.ts`, `.tsx`,
`.mts`, and `.cts` files. It requires a return annotation on every TypeScript
function: declarations, expressions, arrows, callbacks,
methods, async functions, React components, and HOC factories and wrappers.
Contextual typing and a typed variable do not replace the function's own return
annotation. Returning a function or an `as const` value is not an exception.

Use `(value): number => value + 1`, `(): void => { return; }`, and
`async (): Promise<void> => { await save(); }`.
Do not leave return types implicit, even when TypeScript can infer them.

Regression check: run `python3 <skill-dir>/test_explicit_returns.py`.

## Banned React useEffect (error)

`pinned/no-use-effect` applies to all TS/JS extensions, not only JSX files.
It rejects named imports (including aliases), named and wildcard re-exports
from `react`, and `useEffect` access on React default or namespace imports.
It also rejects literal computed access, optional access, destructuring,
and access through direct CommonJS `require('react')` bindings.
Other hooks, unrelated objects, and shadowed bindings remain allowed.

The rule does not trace indirect module aliases, dynamic imports, dynamic
property keys, or re-exports through other modules. Inspect these manually.
Files excluded by the default config, including `.d.ts`, are not checked.

Regression check: run `python3 <skill-dir>/test_use_effect.py`.

## Write code that passes

Follow these when writing TS/JS, so the first draft is lint-clean:

- **Size:** lines ≤ 80 columns, functions ≤ 50 lines and ≤ 10 statements, ≤ 3 params (pass an object), nesting ≤ 3, cyclomatic complexity ≤ 10, cognitive ≤ 15, files ≤ 300 lines. Split early.
- **Immutability:** `const` only, no `let`. No mutation (`push`, `obj.x =`, `delete`); build new values with spread, `map`, `filter`, `reduce`. Use `readonly` (keyword, not `Readonly<T>`) on properties, arrays and params.
- **Types:** no `Omit`, `Pick`, `Partial`; write explicit types. Interfaces use property signatures (`readonly find: (id: string) => User`), not methods. Explicit return types on every function, including callbacks, components, and HOCs; do not rely on inference or contextual typing. `import { type X }` inline for type-only imports. No `any`, no non-null `!`.
- **Logic:** `??` not `||` for defaults, `?.` not `&&` chains. No always-true/false conditions. `async` only if it awaits; `return await` inside `try`. Handle every promise (`await`, `.catch`, or return it).
- **Modules:** named exports only (default exports allowed in `*.config.*`). No import cycles. `node:` prefix for built-ins (`node:fs`). ESM only, no `require`.
- **Style:** `for...of`, not indexed `for`. `includes`/`some`/`flatMap`/`slice` over older forms. `throw new Error('message')`. No negated `if/else`. Full names (`event`, `error`, not `e`, `err`). File names camelCase, PascalCase or kebab-case.
- **Comments:** remove explanatory comments; make intent clear through names and structure. Keep required file headers, legal notices, and tooling directives.
- **React architecture:** do not use React's `useEffect`, including in HOCs or custom hooks. Each component is either visual or an effect-owning higher-order component (HOC). Keep HOCs and visual components in separate files. Keep types, enums, and global values in the HOC file. Apply the required review below when writing or evaluating React code.
- **React (.tsx/.jsx):** hooks rules and exhaustive deps are errors. No components defined inside components, no index keys, `<>` fragments, self-closing empty tags, all jsx-a11y recommended rules.

Never add `eslint-disable`. Fix the code.

## Required React architecture review

Apply this project policy even when ESLint reports no errors.
`pinned/no-use-effect` enforces the direct React access ban described above.
Inspect indirect access and the remaining architecture policies manually.

- **No React `useEffect`.** Remove its imports and calls from components, HOCs,
  custom hooks, and helpers. Aliases and namespace access such as
  `React.useEffect` are also prohibited. Do not hide it behind another hook.
- **Separate files.** Never define HOCs and visual components in the same file.
  Keep types, enums, and global (module-level) values in the HOC file, not the
  visual component file. Import types with type-only imports where needed.
- **No explanatory comments.** Remove comments that explain the code; use clear
  names and structure instead. Keep required headers, legal notices, and tooling
  directives.
- **Visual components** render UI from props. They may keep local UI state and
  invoke callbacks supplied through props. They do not own effects, network
  requests, subscriptions, timers, storage access, or other external I/O.
- **Effect components are always HOCs.** A HOC accepts a component and returns a
  wrapper component. The wrapper owns effects and their cleanup, then passes
  data and callbacks to the wrapped component. It renders the wrapped component,
  not its own presentational markup. Hooks run inside the wrapper, not inside
  the HOC factory.
- Inspect custom hooks and helpers called by visual components. Moving an effect
  into a hook called by a visual component does not satisfy this boundary.
- Compose HOCs outside render, at module scope, so component identity stays stable.
  Keep hook-order and exhaustive-dependency checks enabled.
- Report `useEffect` usage, explanatory comments, mixed HOC/visual files,
  misplaced types, enums, or global values, components that mix presentation and
  effects, and effect owners that are not HOCs as policy violations. Cite file
  and line evidence. Recommend separate visual and HOC files, composed with
  `withUser(ProfileView)`, without introducing `useEffect`.

## Output

Unix format: `path:line:col: message [Error/rule-id]`, then a problem count. The exit code is non-zero when errors are found; that is normal, not a script failure.

Report manual React architecture findings separately from ESLint diagnostics.
Use `pinned/no-use-effect` for the CLI's direct-access diagnostics. Do not claim
that the CLI checks the remaining architecture policies. State when the manual
architecture review was not performed.

Summarise by rule, worst first:

```bash
grep -oE '\[(Error|Warning)/[^]]+\]' /tmp/eslint.txt | sort | uniq -c | sort -rn | head -30
```

On Windows, use the same report with PowerShell:

```powershell
Select-String -Path C:\Temp\eslint.txt -Pattern '\[(Error|Warning)/[^]]+\]' -AllMatches |
    ForEach-Object { $_.Matches.Value } |
    Group-Object |
    Sort-Object Count -Descending |
    Select-Object -First 30 Count, Name
```

## Caveats

- Do not run `--fix` unless the user asks. It edits files in place.
- With a repo `node_modules`, the pinned packages are bind-mounted over the repo's copies, read-only. Without one, the script prints a warning. The bundled formatter resolves from the pinned cache either way; project imports and type checks can still require the repo's dependencies.
- Errors such as `install bubblewrap` or `config not found` are fatal. Report them as-is.

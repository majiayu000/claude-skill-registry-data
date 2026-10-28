---
name: cli
description: >-
  Run Deno with the right flags — run/test permissions, `deno task` over raw
  commands, unstable opt-ins, deps via `deno add`/`outdated`/`remove`. Use when
  wiring or running Deno locally. Not for Deno Deploy or cloud hosting — use
  deploy.
---

# Deno CLI

This skill provides instructions for effective use of the Deno CLI for development, testing, and dependency management.

## Core Commands

### Execution and Tasks
- `deno run [OPTIONS] <FILE>`: Run a script. Always consider permission flags, e.g., `--allow-net`, `--allow-read`, `--allow-env`.
- `deno task <TASK>`: Run a task defined in `deno.json`. This is the preferred way to run project scripts.
- `deno serve [OPTIONS] <FILE>`: Run an HTTP server.
- `deno repl`: Start an interactive Read-Eval-Print Loop (REPL).
- `deno eval`: Evaluate a script from the command line.

### Dependency Management
- `deno add <PACKAGE>`: Add dependencies (e.g., `deno add jsr:@std/assert` or `deno add npm:express`).
- `deno install`: Install project dependencies.
- `deno outdated`: Check for outdated dependencies.
- `deno remove <PACKAGE>`: Remove a dependency.
- `deno uninstall`: Uninstall a dependency or a globally installed script.
- `deno approve-scripts`: Approve npm lifecycle scripts.

### Tooling
- `deno test [OPTIONS]`: Run tests. Use `--watch` for development mode.
- `deno fmt`: Format source files.
- `deno lint`: Lint source files.
- `deno check`: Type-check dependencies.
- `deno bench`: Run benchmarks.
- `deno doc`: Generate and show documentation.
- `deno compile`: Compile a script into a self-contained executable.
- `deno coverage`: Print coverage reports.
- `deno info`: Show info about cache or source files.
- `deno init`: Initialize a new project.
- `deno publish`: Publish the current package to JSR or npm.
- `deno upgrade`: Upgrade the Deno executable.
- `deno clean`: Remove the cache directory.
- `deno jupyter`: Deno kernel for Jupyter notebooks.

## Permission Rules

Deno is secure by default. When using `deno run` or `deno test`, you **must** explicitly grant permissions if the script needs access to the network, files, or environment:

- `--allow-read`: Read access.
- `--allow-write`: Write access.
- `--allow-net`: Network access.
- `--allow-env`: Environment variable access.
- `-A` or `--allow-all`: Allow everything (use with caution).

Reading the sources is a precondition on answering "what permissions do I
need" or "what is the right command", not a step you may skip when a task in
`deno.json` already carries flags: a configured task lists what someone once
granted, not what the code needs now. Grep the project for the calls that
imply a flag — `Deno.openKv`, `Deno.serve`, `fetch(`, `Deno.env`,
`Deno.readTextFile`/`readFile`, `Deno.writeTextFile`/`writeFile`,
`Deno.cron` — and give one line per flag: the flag, the call that needs it,
and its purpose. Name the unstable flag from the section below whenever an
unstable API is among the hits. (2026-09-06: `cli-test-permissions` was
answered from `deno.json` alone; the server in `src/` called `Deno.serve` and
`Deno.openKv`, and the answer named neither `--allow-net` nor `--unstable-kv`.)

## Unstable Features

Some Deno APIs require explicit opt-in via `--unstable-*` flags or `deno.json` config:

- `Deno.openKv()` → `--unstable-kv` or `"unstable": ["kv"]` in deno.json
- `Deno.cron()` → `--unstable-cron` or `"unstable": ["cron"]` in deno.json
- `new Deno.UnsafeWindowSurface()` → `--unstable-webgpu`

When reviewing code, check for unstable API usage and ensure the corresponding flag is set.

## Configuration (`deno.json`)

Always check for `deno.json` or `deno.jsonc` in the project root to understand `imports`, `tasks`, and `lint`/`fmt` settings.

## Usage Examples

### Run tests with permissions
```bash
deno test --allow-read --allow-env
```

### Add a dependency from JSR
```bash
deno add jsr:@std/http
```

### Format the entire project
```bash
deno fmt
```

## Tips
- Use `deno help <command>` for detailed information on any subcommand.
- Use `deno compile` to create standalone binaries.
- For cloud deployments, use the `deploy` skill.
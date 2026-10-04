---
name: develop
description: The entry point for any coding work in a project that has these skills installed - implementing a feature, changing or refactoring code, fixing a bug, scaffolding something new, or touching build and CI. Selects and loads the skills that govern the task before any code is written, holds the work to them while coding, and ends with a self-review of the diff against them. Use this first whenever you are about to develop anything. Not for a pure question with no code change, not for writing unit tests, and not for a full audit of an existing codebase.
user-invocable: true
---

# Develop

**Work out what the task is, load the skills that govern it, follow them while coding, check that you did, then run it once.**

The other skills carry the conventions and only help when the right ones are in context before the first line is written and still honored after the last. This makes that deterministic rather than incidental.

## When to Use

Run this as the first step of any coding task: a feature, a refactor, a bug fix, a new project, a build or CI change, a README.

This pipeline does not include unit tests at all. No step here writes, extends, or repairs one, and finishing a feature is not a reason to add one. Tests exist only when the user explicitly asks for them, and that request is served by the `write-unit-tests` skill, which is not loaded from here.

Skip it for a question with no code change. A deliberate re-audit of an existing codebase is a different job with its own multi-agent orchestration, and this only reviews the diff you just wrote.

## Step 1: Frame the task

State in one line what is being built or changed, then classify it.

**Project type**, read off the tree: CLI Only, Web Only, CLI + Web, Headless API Service, Library, Node Web Only, or Chrome Extension. `go.mod` with `cmd/` and `utils/` and no `internal/server/` is CLI Only; `internal/server/static/` without `utils/` is Web Only; both together is the hybrid; `package.json` with `"type":"module"` plus `public/` and `src/` is Node Web Only; `manifest.json` with `manifest_version` is an extension.

**Work type**: new project, feature, refactor, bug fix, infrastructure, docs.

**Command surface**, when the work adds or changes one. The baseline is `tool <command> <args> --flags`, plus a `<thing>-file` flag wherever the value can arrive as a file. An interactive prompt and stdin eligibility on a flag are offered here and waited on rather than built, because each adds a path every later change has to keep working and the user is the one who decides to own that.

## Step 2: Select and read the governing skills

Pick from the Skill Map below, then read each selected `SKILL.md` in full. Naming a skill is not reading it, and a convention you half-remember is the one that produces a plausible file nobody wants.

Load the skills the task actually touches rather than the whole set. When in doubt, take the two always-in-scope skills for the language plus the one that matches the files being edited.

A delegated sub-task is briefed with the same skills, so a subagent inherits the constraints rather than reinventing them.

## Step 3: State the rules in effect

Before writing code, emit a short checklist of the specific rules from the loaded skills that apply to this task. Concrete bullets, not whole skills restated.

```
Rules in effect (CLI Only, new command):
- Comments: the comment rules in AGENTS.md (CLAUDE.md if you are Claude), quoted not summarized
- Output through the utils printers, never fmt.Println
- zerolog only behind --debug; utils printers otherwise
- Boolean flags carry no shorthand; every prompt has a flag supplying the same value
- New command file under cmd/, registered in root.go init()
- Flags grouped in a per-command struct, registered in init()
- Scope: only the files this task names; nothing leaves the working directory
```

The cross-cutting rules go on the list every time, comment discipline first among them, and with them the ones that reach past the diff: which files may be touched, what may not leave the working directory without being asked for, and what has to run before the work is called done. A rule that comes from AGENTS.md (CLAUDE.md if you are Claude) goes on the list as a citation or a verbatim quote rather than in your own words, because a paraphrase of a strict rule loosens it every time. Being cross-cutting rather than task-specific, they are the first to fall off the list and the first to decay mid-session, and the written checklist is the defense against that.

## Step 4: Do the work

Implement, holding to the Step 3 checklist. When a task spans several skills, keep each one's rules in view for the part it governs: the concurrency skill for the worker pool, the command skill for the wiring around it.

## Step 5: Self-review the diff

Pass over what you changed this session and check it against the Step 3 checklist. Fix small deviations directly and call out anything larger that needs a decision.

Fixing in place is the carve-out for the diff you just wrote. Code that was already there is reported rather than fixed, even when it breaks the same rule, because an unrequested change sitting inside a requested one is the hardest kind for a reviewer to spot.

Scope it to the files you touched, check the checklist rather than every rule in every skill, and keep it quick. This catches the drift that creeps in mid-session, which is most of what a review of fresh work finds.

## Step 6: Run it once

Run the real artifact before calling the work done, and say what was run. A build that compiles and a suite that passes show the code is well-formed, not that the feature works, and anything with visible output is rendered and looked at rather than reasoned about.

Scope the run to what changed: a command that was touched gets invoked, a page that was edited gets loaded, and a package with no entry point of its own is exercised through its caller.

## Language servers

The LSP is already wired into every session for Go, Python, TypeScript, and JavaScript, so a language server is used by calling it and never by installing anything. A plugin, an MCP server, or a dependency is never proposed to obtain one.

| Extension | Server |
|---|---|
| `.go` | `gopls` |
| `.py`, `.pyi` | `pyright-langserver` |
| `.ts`, `.tsx`, `.mts`, `.cts`, `.js`, `.jsx`, `.mjs`, `.cjs` | `typescript-language-server` |

`goToDefinition`, `findReferences`, `goToImplementation`, `hover`, `documentSymbol`, and `workspaceSymbol` resolve a symbol rather than matching a string, which is what makes them better than `rg` for tracing a definition or every call site before changing one. `rg` and `grep` stay the tool for plain text and for a language no server covers, or if LSP doesn't work for some reason.

## Skill Map

| Task touches | Load |
|---|---|
| Any Go code | `go-project-layout`, `go-idioms` |
| The command tree: `main.go`, the root, command files, subcommand packages | `go-cli-structure` |
| Flags, positional arguments, enum values, a flag reading stdin | `go-cli-commands` |
| Printing, tables, `--debug`, terminal colors | `go-cli-output` |
| Interactive prompts, passwords, selection lists, a flag reading stdin | `go-cli-prompts` |
| Progress meters, running/done lifecycles, terminal width | `go-cli-progress` |
| `internal/` package structure, error boundaries, storage | `go-package-architecture` |
| `net/http` server, embedded static serving, middleware | `go-http-server` |
| OAuth login for a CLI client | `go-oauth-cli` |
| Goroutines, errgroup, semaphores, fan-out/fan-in | `go-concurrency` |
| The embedded SPA under `internal/server/static/` | `go-embedded-frontend` |
| Rendering Markdown in a browser page | `web-markdown-rendering` |
| Mermaid diagrams in a browser page | `web-mermaid-diagrams` |
| Any Node code | `node-project-layout`, `node-idioms` |
| `config.json`, deep merge, `state.json`, the session secret | `node-config-state` |
| The `node:http` and `ws` server, routing, static serving | `node-http-ws-server` |
| Password and session-cookie auth in Node | `node-auth` |
| The vanilla-JS SPA under `public/` | `node-frontend` |
| A Go or Chrome extension Makefile | `go-makefile` |
| A Node Makefile, vendoring, the native addon build | `node-makefile` |
| What a Node project ships: binary or tarball | `node-release-artifacts` |
| A Dockerfile or docker-compose, in any language | `dockerize` |
| `.github/workflows/release.yaml`, version bumps | `github-release-workflow` |
| README | `project-readme` |
| Chrome extension | `chrome-extension` |

A whole project type pulls in a predictable set. A CLI Only tool takes the two Go skills plus `go-cli-structure`, `go-cli-commands`, and `go-cli-output`, and adds the others as the surface grows. A Web Only service takes the two Go skills plus `go-http-server`, `go-package-architecture`, and `go-embedded-frontend`.

## Principles

Skills are the source of truth for the conventions they cover, and AGENTS.md (CLAUDE.md if you are Claude) for the rules that hold on every task. Follow, and self-flag against, only those; anything neither covers is not a rule and does not belong on the checklist.

Load and read before writing, not after. A convention applied retroactively is a second diff on top of the first.

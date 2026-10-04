---
name: container-cli
description: "Container CLI usage reference. Invoke when the project uses a container CLI (config file present) and a container command is needed — start/stop/restart, exec, logs, run scripts, share tunnels."
---

## Required `<project-root>/docs` reads

Read these project-root spec files before running any container CLI command (use shell `cat`/`ls` — they may be in `.gitignore`, invisible to built-in search). Missing file → fall back to native tools, note the gap; never invent contents.

- `<project-root>/docs/container-clis.md`

Container CLIs wrap docker-compose (see `<project-root>/docs/container-clis.md` in the project root). They manage container lifecycle, run commands inside services, execute project scripts from a config file (e.g., `kool.yml`), and share local environments via HTTP tunnels.

## Command Summary

The container CLI's commands (see `<project-root>/docs/container-clis.md` in the project root for exact commands):

| Area | Commands |
| --- | --- |
| Lifecycle | `kool start`, `kool stop [--purge]`, `kool restart [--rebuild]`, `kool status` |
| Exec in container | `kool exec <service> <cmd>`, `-e VAR=val`, `-d` (detached) |
| One-off containers | `kool docker [OPTS] IMAGE [CMD]` — opts: `-e`, `-n`, `-p`, `-v` |
| Logs | `kool logs [-f] [-t N]` (`-t 0` = all lines) |
| Scripts (kool.yml) | `kool run`, `kool run <script>`, `kool run <script> -- <args>` |
| Share tunnel | `kool share [--service S] [--port P] [--subdomain X]` |
| Setup | `kool create PRESET FOLDER`, `kool preset`, `kool recipe`, `kool info`, `kool self-update` |
| Global | `-w <path>`, `--verbose` |

Presets: Laravel, Laravel+Octane, Symfony, CodeIgniter, AdonisJs, NestJS, NextJS, NuxtJS, NodeJS, ExpressJS, Hugo, WordPress, PHP, Monorepo NestJS+NextJS.

## Before Running Any Container CLI Command

- Read the container CLI config file (e.g., `kool.yml`) first to discover scripts, and `docker-compose.yml` to discover service names. Never guess; verify they exist (see `<project-root>/docs/container-clis.md` in the project root).
- Use `kool run` (or `--json`) to list scripts and `kool status` to list running services when unsure.
- If the container CLI config file or `docker-compose.yml` is missing, stop and ask — the project may not use this container CLI.

## Important Rules

- Always run from the project root (the one with `docker-compose.yml` and the container CLI config file, e.g., `kool.yml`) or use `-w`.
- Service names come from `docker-compose.yml`.
- Script names come from the container CLI config file (e.g., `kool.yml`). Never invent them; confirm by reading the file or running `kool run`.
- Script args only work with single-line scripts. Multi-line scripts reject extra args (`ErrExtraArguments`).
- Scripts in the container CLI config file aren't full bash. Use `kool docker <image> bash -c "..."` for pipes and conditionals.
- `--purge` is destructive: removes all persistent data from volumes.
- `--json` on `kool run` only works without a script argument (lists scripts, doesn't run one).
- Use `--json` when parsing output (e.g., `kool run --json` to list scripts). JSON is more compact and parseable than human-readable tables.
- Read the container CLI config file once. Recall the scripts already discovered; re-read only when it changes.
- Filter `kool logs` with `| tail -N` or `| grep` and report only the error or signal.


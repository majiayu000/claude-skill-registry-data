---
name: zephyr-justfile
description: Use when working with Just for Zephyr development creating or extending project Justfiles, applying the user’s preferred patterns, wiring west builds/flash/run, and understanding just settings, recipes, and modules. Includes a Zephyr-focused Justfile template and a concise Just reference.
---

# Zephyr Justfile Usage

Use this skill to create or extend Justfiles for Zephyr applications, following the preferred patterns and conventions.

## 1) Start from the reference

- Use `references/just-quick-reference.md` as the default baseline.
- Pull missing details from `references/just-manual.md` only when needed.
- Use `references/zephyr-justfile-template.just` as the starting template for new apps.

## 2) Establish core settings

- Prefer `set shell := ['zsh', '-uc']` and `set unstable := true` to match the template.
- Use `require('west')` to enforce tool availability.
- Derive `app` from `source_dir()` and `board` from `west config build.board` with a fallback.
- Keep variables at the top; expose knobs via env/vars, not long argument lists.

## 3) Default + discoverability

- Use a default listing recipe that formats the app name.
- Prefer `just --list-heading` to keep a consistent UI.

## 4) Zephyr build workflow

- Provide `configure` to set `west config` defaults (board, build dir format, pristine).
- Provide `build`, `build_clean`, and `clean` with `build_dir` derived from west config.
- Use `board`, `snippet`, `target`, and `clean` as overridable knobs.

## 5) Flash/run tooling

- Provide a `flash` recipe that depends on `build`.

## 6) Devicetree tooling (dtsh)

- Provide `_dtsh` guard + helpers: `dts_tree`, `dts_ls`, `dts_cat`, `dtsh_out_html`, `dts_find`.

## 7) Extend safely

- Group recipes by workflow stage: `config`, `build`, `run`, `tools`.
- Keep private helpers prefixed with `_`.
- Quote interpolations when values may include spaces.
- Use `--justfile {{ source_file() }}` for self-invocations.

## References

- `references/just-quick-reference.md` — concise just patterns
- `references/just-manual.md` — baseline manual details
- `references/zephyr-justfile-template.just` — Zephyr app template

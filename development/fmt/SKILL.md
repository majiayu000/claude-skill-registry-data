---
name: fmt
description: Format TypeScript sources using Deno formatter
license: MIT
compatibility: opencode
metadata:
  workflow: deno
---

## What I do

- Run `deno fmt` to format all tracked TypeScript files in the repository
- Can also format a single file using `deno fmt <filename>`
- Ensures consistent code formatting before committing or submitting a pull
  request
- Automatically follows the formatter rules configured in `deno.jsonc`

## When to use me

Use this when you want to ensure code is properly formatted:

- Before committing changes
- Before creating a pull request
- After modifying any TypeScript files in the codebase

## Notes

- The formatter is configured by Deno and applies to the entire codebase
- This is part of the standard pre-commit workflow defined in
  `scripts/pre-commit.sh`

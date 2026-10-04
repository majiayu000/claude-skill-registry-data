---
name: format-python
description: Format Python source files with Black and isort, then report any remaining lint issues. Use when the user asks to format, clean up, tidy, or fix the style of Python code.
allowed-tools: Read, Edit, Bash, Glob
---

# Format Python Code

Format Python files to the project's style: Black with line length 88, isort using the Black profile.

## Steps

1. Determine scope. If the user named files, use those. If they said "the project" or gave no scope, use `Glob` with `**/*.py`, excluding `.venv/`, `build/`, and `dist/`.

2. Check the tools exist before doing anything else:

   ```bash
   black --version && isort --version
   ```

   If either is missing, tell the user to run `pip install black isort` and stop. Do not format by hand-editing files — that defeats the purpose and produces inconsistent results.

3. Sort imports first, then format. Order matters: Black reformats what isort produces, not the reverse.

   ```bash
   isort <paths> --profile black --line-length 88
   black <paths> --line-length 88
   ```

4. Report what changed. Black prints a summary; pass it through rather than paraphrasing it.

5. If the user asked about code quality rather than just formatting, add a lint pass:

   ```bash
   ruff check <paths>
   ```

   Report findings. Do not auto-fix lint issues unless asked — formatting is mechanical and safe, lint fixes are semantic and are not.

## Constraints

- Never format files outside the project directory.
- Never format a file with unstaged changes without telling the user first. Black rewrites in place and there is no undo.
- If Black fails on a file it is almost always a syntax error. Report the parse error rather than retrying.

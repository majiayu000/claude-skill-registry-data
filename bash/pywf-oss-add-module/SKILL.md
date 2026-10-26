---
name: pywf-oss-add-module
description: "Create a new module or subpackage in a pywf open-source Python library, together with its mirrored test file, its all.py, and its api.py export. Use when the user asks to add a module, file, subpackage, or new feature area to the package."
---

Scaffold a new module or subpackage that follows the template's layout, import, and test conventions before any real logic is written.

Read ../pywf-oss-base/SKILL.md, then:
- ../pywf-oss-base/references/08-package-files.md
- ../pywf-oss-base/references/09-code-style.md
- ../pywf-oss-base/references/10-test-layout.md
- ../pywf-oss-base/references/11-test-writing.md

## Steps

1. **Pin down the target.**
   - Get the dotted path (`<package_name>.subpackage.module_name`), whether it is a module or a subpackage, and whether its names are public.
   - If the user gave only a feature description, propose a path, and confirm it before creating files.
2. **Create the source.**
   - A module gets the file header, a one-line module docstring, and the imports it needs.
   - A subpackage gets `__init__.py` (header only) and, if it exposes names, its own `api.py`.
   - Every public function and class gets at least a one-line docstring.
3. **Create the test files,** at the path the script prints, never one worked out by hand:

   ```bash
   python ${CLAUDE_SKILL_DIR}/../pywf-oss-base/scripts/check_test_layout.py --project_root . --source <package_name>/subpackage/module_name.py
   ```

   - For a module, write the test file from the template in `11-test-writing.md`, with a placeholder test.
   - For a new subpackage folder, also create its `all.py`.
4. **Export.**
   - If the names are public, add one line per name to the nearest `api.py`. If the user wants it, also expose a new subpackage's `api` from the parent `api.py`.
   - In the matching `test_..._api.py`, touch each new name (`_ = api.ClassName`).
5. **Verify.**
   - The layout check without `--source` reports 0 problems.
   - `.venv/bin/python <test_path>` runs the new test file.
   - `mise run format`, then `mise run lint`, reports nothing.

## Output

List the files you created, the `api.py` lines you added, and the layout-check result.

Next step: `pywf-oss-write-test`, once the logic is written.

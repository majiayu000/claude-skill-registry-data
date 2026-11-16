---
name: opensrc
description: "Build or refresh opensrc/ library context from package.json and official docs."
disable-model-invocation: true
license: MIT
metadata:
  reviewed: "2026-10-18"
  sources: "MCT (local) ~/.claude/skills/opensrc/SKILL.md, ~/.claude/bin/mct command_opensrc (manifest, stub files, .gitignore entry)"
---

# opensrc

`opensrc/` is project-local, gitignored library context: one manifest of declared packages and one notes file per package, filled from official sources so plans and code use the real API of the installed version instead of a remembered one.

## 1. Build the skeleton

Run the script from the project root (the folder holding `package.json`). The script lives in this skill's `scripts/` folder:

```bash
python3 "<this skill's dir>/scripts/opensrc.py" --root . --fetch-metadata
```

It reads `dependencies` and `devDependencies`, writes `opensrc/manifest.json` (name, declared range, dev flag, npm URL, plus latest version, repository and homepage from `registry.npmjs.org` when `--fetch-metadata` is set), creates `opensrc/packages/<name>.md` stubs for packages that have none (it never overwrites a file), and appends `opensrc/` to `.gitignore` if no entry covers it. Drop `--fetch-metadata` when offline; earlier metadata is kept.

Done when: the script prints `"ok": true`. Read its `pending`, `metaErrors` and `removed` lists. A package in `removed` left `package.json`; delete its notes file if nothing else uses it.

## 2. Pick what to fill

Fill only the packages the current task touches: the ones imported by the files you will change, plus the framework they run on. Filling every stub costs reading time the task doesn't need; the rest stay `stub` until a task needs them.

Done when: you have a named list of packages to fill, each with a reason tied to the task.

## 3. Fill from official sources

For each picked package, read the docs for the **declared major version** (the range in the manifest, not `latest`; the major can differ). Use, in order: the official docs site (`homepage`), the official repository (`repository`: README, CHANGELOG, migration guides), the npm page. Use library docs tooling such as Context7 when available. Blog posts and Q&A threads are leads to check against those sources, never the source.

Replace each `- Pending.` line in the package's file:
- **Key APIs used in this project**: the functions, hooks, components or options the task uses, with exact signatures. Grep the repo for imports to find them.
- **Patterns and constraints**: the documented way to use them here (server vs client, required providers, config).
- **Version notes**: declared vs latest, and the breaking changes between them that matter for the task.

Add the source URL under each section. Keep each file short; it is a working note, not a copy of the docs.

Done when: every picked package's file has no `- Pending.` line left and each section cites a URL. Re-run the script; those packages now show `"status": "filled"`.

## 4. Use and report

Plan and implement against the filled notes. Keep `opensrc/` out of commits unless the user asks for it.

Report in one line: the packages filled or refreshed and the source used for each, e.g. `opensrc: filled react (react.dev, v18 docs), @tanstack/react-query (tanstack.com/query v5); 14 stubs pending`.

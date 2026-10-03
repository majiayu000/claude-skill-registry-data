---
name: find-dead-code
description: Detect dead-code candidates in the repo and hand back a ranked list with per-category verification checklists.
disable-model-invocation: true
---

# Find Dead Code

Surface candidates. Never delete. The user verifies and removes.

## Rules

1. **Detect and report only.** Do not run `rm`, `git rm`, or edit imports as part of this skill.
2. **A candidate is a hypothesis, not a verdict.** Every candidate ships with the verification recipe below; the user runs the final eye.
3. **Scope before running.** Ask the user which area: a single module, package, or service, or the whole repo. Repo-wide scans are slow and noisy; one subsystem at a time produces actionable lists.
4. **No em-dash in output.** Project convention.

## Detectors

Prefer a language-appropriate detector when the project already configures one (check the repo root and the project's lint config); fall back to grep otherwise. Examples by ecosystem:

- **JS / TS:** `knip`, `ts-prune`, `unimported`.
- **Python:** `vulture`, `ruff` unused-code rules (`F401`, `F841`).
- **Go:** `staticcheck` (`U1000`), `deadcode`.
- **Rust:** compiler `dead_code` warnings (`cargo check`), `cargo-udeps` for unused dependencies.
- **JVM:** IDE / `detekt` / `PMD` unused-code inspections.

Never install a detector the project does not already use; say which one would help and let the user decide. Detector output is a starting list, not a verdict: every survivor still goes through the verification recipe.

## Categories

Pick the category the user asked about, or run all four if they said "find dead code" with no scope.

### A. Unreferenced files

Source files (extensions in `SOURCE_EXTENSIONS` from `.claude/project.env`) that no other file imports, requires, or includes.

Detection: for each candidate file `path/to/foo_bar.<ext>`, grep the repo for its import forms (module path, relative path, dotted module name) and the bare basename `foo_bar` as a string. If zero non-self matches across the source roots, flag it.

### B. Unused exports

Public symbols (exports, public functions, classes, constants) that nothing references. Run the project's detector if one is configured (see Detectors); otherwise grep per symbol. Cross-check survivors by grep: for a symbol `fooBar`, search `\bfooBar\b` across the whole repo, not just its own package.

### C. Dead feature flags

Flags defined in the project's flag store (a config file, a seed script, a database table, or a flag service) whose key is never checked in code.

1. List current flag keys from wherever the project defines them (find the flag definitions first; ask the user if there is no obvious source).
2. For each key, grep for the project's flag-check call with that key and the bare quoted key string across the source roots.
3. Zero hits = candidate. Also flag flags where the only hit is the definition itself.

### D. Orphan modules across packages

In a multi-package repo (workspaces, modules, crates), a shared package's public symbol that no consuming package uses. This is the **Explore-agent blind spot**: package-scoped searches miss the consumer side. Always grep from the repo root, not from inside the package.

For each entry in the shared package's public surface (its index / `__init__` / `lib.rs` / exported package), grep every other package for an import of that package that pulls that symbol. Skip this category in a single-package repo.

## Mandatory verification recipe (per candidate, before flagging)

Run all five. A single hit moves the candidate from "dead" to "live" (or "uncertain").

1. **Repo-wide grep, basename without extension.** `grep -rn "foo_bar" .` excluding vendored and build-output directories.
2. **String-literal grep.** The basename or key may appear inside a string: registry YAMLs, factory maps, MCP tool names, route paths, env var names, log tags.
3. **Dynamic loading.** Search for dynamic imports and reflection: template-string imports, `importlib` / `__import__`, plugin entry points, reflection by class name. These hide static references.
4. **Registry and factory check.** If the file matches a known registry pattern (plugins, providers, adapters, handlers resolved by name), open the corresponding factory or registry and look for the name.
5. **Cross-package check.** For a shared-package candidate, grep each consuming package separately. Package-scoped Explore is not enough.

## Known false-positive sources

Surface these alongside the candidate list so the user can sanity-check fast.

- **String-keyed registries:** anything resolved by name (plugins, providers, handlers) looks unreferenced via import grep.
- **Barrel / re-export files:** a symbol reached only through an index or package re-export needs the re-export traversed.
- **Framework conventions:** files loaded by path convention (routes, migrations, fixtures, management commands) are never imported.
- **Test setup, seed scripts, eval harnesses, CLI entry points:** run by tooling, not imported.
- **Build-time references:** anything referenced from build configs, CI workflows, Dockerfiles, or shell scripts under `scripts/`.
- **Generated code:** paths matching `GENERATED_PATHS_REGEX` in `.claude/project.env`; regenerate, never report.
- **Feature flags awaiting rollout:** the flag exists before the code lands. Check the latest 4 weeks of `git log` against the flag key before flagging.

## Output format

Hand back a markdown table per category, ranked by confidence (high = passed all five checks). Example row:

```
| Confidence | Path                         | Last touched | Why suspect                          | Verification status                                 |
| ---------- | ---------------------------- | ------------ | ------------------------------------ | --------------------------------------------------- |
| High       | src/billing/legacy_format.py | 9 months ago | 0 imports, 0 string hits, no factory | Passed all 5 checks                                 |
| Medium     | src/audit/old_audit.py       | 4 months ago | 0 direct imports                     | Re-exported via src/audit/__init__.py; needs human review |
```

End with: "Verify each row before removing, then confirm with the project's typecheck and test commands (`TYPECHECK_CMD` / `TEST_CMD` in `.claude/project.env`). Open a worktree per category (`scripts/worktree-create.sh <name>`); do not bundle removals across categories in a single PR."

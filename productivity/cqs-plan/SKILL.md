---
name: cqs-plan
description: Task planning with scout data + task-type templates. Produces implementation checklists.
disable-model-invocation: false
argument-hint: "<task description>"
---

# Plan

Generate an implementation plan by combining `cqs scout` output with a task-type template.

## Process

1. **Classify the task** into one of the templates below based on the description.
2. **Run scout**: `cqs scout "<task description>" --json 2>/dev/null` (no `-q` flag on subcommands)
3. **Run targeted lookups** from the template's checklist — scout alone misses structural touchpoints (clap structs, dispatch arms, skill files).
4. **Produce a plan** listing every file to change, what to change, and why. Be specific about struct fields, function signatures, and match arms.

## Arguments

- `$ARGUMENTS` — task description (required)

## Templates

### Add/Replace a CLI Flag

**When:** Adding a new flag, renaming a flag, changing a flag's type (bool → enum).

**Checklist:**
1. `src/cli/definitions.rs` — `Commands` enum variant. Add/modify `#[arg]` field (often via a shared `*Args` struct in `src/cli/args.rs`). If enum-typed, define with `clap::ValueEnum`.
2. `src/cli/dispatch.rs` — `run_with()`/`run_with_dispatch()` match arm. Update destructuring and `cmd_<name>()` call.
3. `src/cli/commands/<group>/<name>.rs` (groups: search/, graph/, review/, index/, io/, infra/, eval/, train/) — flag flows into the `*_core` fn's typed `*Args`; update branching there, not just the CLI adapter.
4. **Daemon surface**: if the flag affects core behavior, the daemon `dispatch_*` handler in `src/cli/batch/handlers/` must forward it too — CLI and daemon are parallel surfaces, wire both in the same PR. Parity tests live in `src/cli/batch/handlers/dispatch_tests.rs`.
5. `src/store/*.rs` / `src/lib.rs` — Usually NO changes. Only if flag affects query behavior.
6. Tests: `tests/<name>_test.rs` — add case for new value. Update tests using old flag name.
7. `.claude/skills/cqs/SKILL.md` — update the command's flag table.
8. `README.md` — update examples if the command is featured.
9. Verify callers: `cqs callers cmd_<name> --json`

**Patterns:**
- Output format flags: `#[arg(long, value_enum, default_value_t)]`
- Display functions: `display_<name>_text()`, `display_<name>_json()`
- JSON output: `serde_json::to_string_pretty` on `#[derive(Serialize)]` structs

### Add a New CLI Command

**When:** Adding an entirely new `cqs <command>`.

**Checklist (command-core pattern — the NEW-COMMAND RULE, see CONTRIBUTING):**
1. `src/cli/commands/<group>/<name>.rs` — New file in the right group (search/, graph/, review/, index/, io/, infra/). Implement ONE surface-agnostic `<name>_core(...)` taking a typed Deserialize `<Name>Args` and returning a Serialize `<Name>Output`. `cmd_<name>()` is a thin CLI adapter over the core.
2. `src/cli/commands/<group>/mod.rs` — Add `mod <name>;` and re-export `cmd_<name>` (+ the core for the daemon).
3. `src/cli/definitions.rs` — Add variant to `Commands` enum with args (shared `*Args` structs live in `src/cli/args.rs`).
4. `src/cli/dispatch.rs` — Add match arm calling `cmd_<name>()`.
5. **Daemon surface in the same PR**: `dispatch_<name>` adapter in `src/cli/batch/handlers/` (thin wrapper: parse wire request into `<Name>Args`, call the core). Add a CLI==daemon parity test in `src/cli/batch/handlers/dispatch_tests.rs`.
6. `src/lib.rs` or `src/<module>.rs` — Library function if logic is non-trivial. Keep CLI layer thin.
7. Tests: `tests/<name>_test.rs` — integration tests using `TestStore` or `assert_cmd`.
8. `.claude/skills/cqs/SKILL.md` — add the command to the dispatcher reference (and a `cqs-<name>` skill only if the workflow warrants it).
9. `.claude/skills/cqs-bootstrap/SKILL.md` — Add to portable skills list / command reference.
10. `CLAUDE.md` — Add to "Key commands" list.
11. `README.md` — Add to command reference.
12. `CONTRIBUTING.md` — Update Architecture Overview if adding new source files.

**Patterns:**
- Command files are ~50-150 lines. Store/library calls, then display.
- JSON output with `--json` flag; text output via a display fn the daemon can reuse.
- Tracing span at core entry: `let _span = tracing::info_span!("<name>_core").entered();`

### Fix a Bug

**When:** Something produces wrong results, panics, or misbehaves.

**Checklist:**
1. **Reproduce**: Understand the exact failure mode. Get input → actual → expected.
2. **Locate**: `cqs scout "<bug description>"` to find relevant code.
3. **Trace callers**: `cqs callers <function> --json` — who calls the buggy code? Are callers also affected?
4. **Check tests**: `cqs test-map <function> --json` — do tests exist? Do they cover the failing case?
5. **Fix**: Minimal change in the library layer, not the CLI layer.
6. **Add test**: Regression test that would have caught this bug.
7. **Check impact**: `cqs impact <function> --json` — did the fix change behavior for other callers?

**Patterns:**
- Fix in `src/*.rs` (library), test in `tests/*.rs` or inline `#[cfg(test)]`.
- Use `tracing::warn!` for recoverable errors, `bail!` for unrecoverable.
- Never `.unwrap()` in library code. `?` or `match` + `tracing::warn!`.

### Add Language Support

**When:** Adding a new programming language to the parser.

**Checklist:**
1. `Cargo.toml` — Add tree-sitter grammar dependency (optional).
2. `src/language/mod.rs` — Add to the `define_languages!` macro invocation.
3. `src/language/languages.rs` — Add the language's `LanguageDef` block (grammar wiring, extensions, extract/post-process hooks). Per-language files no longer exist — everything lives in this one file.
4. `src/language/queries/<lang>.chunks.scm` + `<lang>.calls.scm` (+ `.types.scm` if type deps apply) — tree-sitter queries live as standalone `.scm` files, not inline strings.
5. `Cargo.toml` features — Add `lang-<name>` feature, add to `default` and `lang-all`.
6. Tests: `tests/fixtures/<lang>/` — sample files. Parser tests in `tests/parser_test.rs`.
7. `tests/eval_test.rs` and `tests/model_eval.rs` — Add match arms.

**Patterns:**
- One-liner in `define_languages!` handles registration.
- Chunk query captures must use the parser's known capture names (see `src/parser/chunk.rs`): function, struct, class, enum, trait, interface, const, ...
- Call query uses `@callee` capture.

### Add ChunkType Variant

**When:** Adding a new chunk type (e.g., Extension, Protocol, Alias).

**Checklist:**
1. `src/language/mod.rs` — Add variant to the `define_chunk_types!` invocation (ChunkType lives here now). Classify it so `is_callable()`/`is_code()` derive correctly — a round-trip test enforces consistency.
2. `src/nl/mod.rs` — Add natural language label for the variant (used in embedding text).
3. `src/language/queries/<lang>.chunks.scm` — Add capture using the new variant name.
4. `src/parser/chunk.rs` — Add to the capture-name map if using a new capture name.
5. `src/cli/commands/index/stats.rs` — Variant appears automatically via `ChunkType` iteration.
6. Tests: Parser tests for each language using the new variant. Verify `cqs search` returns results with correct type.
7. `ROADMAP.md` — Update ChunkType Variant Status table.

**Patterns:**
- `is_callable()` returns true for Function, Method, Macro — most others return false.
- `Display` uses lowercase singular (e.g., "type_alias"). `FromStr` accepts both snake_case and spaces.
- Container extraction uses `capture_types` to decide what's a container vs leaf.

### Add Injection Rule

**When:** Adding multi-grammar parsing (e.g., HTML→JS, PHP→HTML, Svelte→CSS).

**Checklist:**
1. `src/language/languages.rs` (host language's block) — Add `InjectionRule` to the host's injection rules. Specify `parent_node`, `content_node`, `target_language`, and optional `detect_language` callback.
2. `src/language/languages.rs` (target language's block) — Ensure the target's `LanguageDef` exists and parses correctly in isolation.
3. `src/parser/injection.rs` — Usually NO changes. Only if new detection logic is needed (e.g., `detect_script_language`, `detect_heredoc_language`).
4. Tests: `tests/fixtures/<host>/` — sample file with embedded content. Verify chunks from both host and injected language appear.
5. Verify depth limit: recursive injections (PHP→HTML→JS) must respect depth limit (default 3).
6. `ROADMAP.md` — Update Multi-Grammar Parsing section.

**Patterns:**
- `content_scoped_lines` prevents container-spans-file problem in recursive injection.
- `detect_language` callbacks inspect attributes (e.g., `lang="ts"`, `type="module"`).
- `set_included_ranges()` for byte-range isolation of injected content.

### Performance Optimization

**When:** Improving speed or reducing resource usage for a specific operation.

**Checklist:**
1. **Benchmark before**: `cargo bench` or manual timing with `time cqs <command>`. Record baseline.
2. **Profile**: `cqs scout "<bottleneck description>"` to find hot path. `cqs callers` to trace the call chain.
3. **Identify approach**: Lazy loading, caching, reduced allocations, parallel iteration, candidate pruning.
4. **Implement**: Minimal change. Prefer data structure changes over algorithmic rewrites.
5. **Benchmark after**: Same benchmark as step 1. Quantify improvement.
6. **Regression test**: Ensure correctness is preserved — same inputs produce same outputs.
7. **Check callers**: `cqs impact <function> --json` — did the optimization change the API surface?

**Patterns:**
- HNSW candidate fetch: load only `(id, embedding)` for scoring, full content for top-k.
- Rayon `par_iter` for embarrassingly parallel work. Check for shared mutable state first.
- `tracing::info_span!` around hot paths for flame graph visibility.

### Audit Finding Fix

**When:** Fixing an issue identified during a code audit (from `docs/audit-triage.md`).

**Checklist:**
1. **Read triage entry**: Get priority, category, description, and affected code from `docs/audit-triage.md`.
2. **Locate**: `cqs scout "<finding description>"` — verify the issue still exists (may have been fixed since audit).
3. **Assess scope**: `cqs impact <function> --json` — how many callers are affected?
4. **Fix**: Follow the triage entry's suggested approach if provided.
5. **Add test**: Cover the specific scenario from the finding.
6. **Update triage**: Mark entry as fixed in `docs/audit-triage.md` with PR reference.
7. **Check related findings**: Same category may have related issues — fix together if trivial.

**Patterns:**
- P1 findings: fix immediately, standalone PR.
- P2-P3: batch by category into single PR.
- P4: fix opportunistically when touching nearby code.

### Add Tree-Sitter Grammar

**When:** Adding a new tree-sitter grammar dependency (new language or replacing a grammar).

**Checklist:**
1. `Cargo.toml` — Add grammar crate as optional dependency. Prefer crates.io; use git dep with `rev` pin if unpublished.
2. `build.rs` — Usually NO changes (grammars self-register via `tree-sitter-language` crate).
3. `src/language/<lang>.rs` — Wire grammar via `tree_sitter_<lang>::LANGUAGE` or `tree_sitter_<lang>::language()`.
4. `Cargo.toml` features — Add to `lang-<name>` feature gate. Add to `default` and `lang-all`.
5. Verify compatibility: grammar must target tree-sitter `>=0.24, <0.27` (current range). Check grammar's `Cargo.toml`.
6. Tests: `cargo test --features lang-<name>` — parser produces expected chunks.
7. If forked: document fork reason in `Cargo.toml` comment. Track upstream for eventual switch.

**Patterns:**
- Git deps need `rev` pin, not `branch` — branches break reproducibility.
- Some grammars export `LANGUAGE` (static), others `language()` (function). Check their API.
- Monolithic grammars (Razor, VB.NET) don't need injection — they parse everything in one pass.

### Schema Migration

**When:** Bumping the SQLite schema version (adding tables, columns, or changing data layout).

**Checklist:**
1. `src/store/helpers/mod.rs` — Bump `CURRENT_SCHEMA_VERSION` constant.
2. `src/store/migrations.rs` — Add `async fn migrate_vN_to_vM()` with ALTER TABLE / CREATE TABLE statements.
3. `src/store/migrations.rs` — Register it in the `MIGRATIONS` table as `(N, M, |c| Box::pin(migrate_vN_to_vM(c)))`.
4. `src/store/mod.rs` — Update `open()` if new tables need initialization or if Store fields changed. `src/schema.sql` must reflect the new layout (its header states the version).
5. `src/store/*.rs` — Update queries that read/write affected tables.
6. Tests: Migration test with a v(N-1) database → verify v(N) upgrade succeeds and data is preserved.
7. `PROJECT_CONTINUITY.md` — Update schema version in Architecture section.

**Patterns:**
- Migrations must be idempotent — `IF NOT EXISTS`, `IF NOT COLUMN` guards.
- We use a metadata table for schema_version, not PRAGMA user_version.
- Test with a real old-version database if available (copy from `.cqs/` before upgrading).
- `cqs migrate` skill handles user-facing migration workflow.

### Refactor / Extract

**When:** Moving code, splitting files, extracting shared helpers.

**Checklist:**
1. **Find all call sites**: `cqs callers <function> --json` for each function being moved.
2. **Check similar code**: `cqs similar <function> --json` to find duplicates to consolidate.
3. **Plan visibility**: `pub(crate)` for cross-module, `pub` for public API, private for same-module.
4. **Move tests with code**: `#[cfg(test)] mod tests` works in submodules.
5. **Update imports**: Each file needs its own `use` statements — they don't carry across modules.
6. **Verify callers compile**: After moving, all callers must update their `use` paths.
7. `CONTRIBUTING.md` — Update Architecture Overview for structural changes.

**Patterns:**
- `impl Foo` blocks can live in separate files (Rust allows multiple).
- Trait method imports don't carry over to submodule files.
- Use `pub(crate)` for types/constants shared across submodules.

## Output Format

Present the plan as:

```
## Plan: <task summary>

### Files to Change

1. **<file>** — <what and why>
   - <specific change with code snippet>

### Tests

- <test file>: <what to test>

### Not Changed (verified)

- <file>: <why no changes needed>
```

## When Not to Use

- Trivial changes (typos, single-line fixes) — just do it
- Pure research — use `cqs gather` or `cqs scout` directly
- Running an audit — use `/audit` skill (but audit *finding fixes* have a template above)

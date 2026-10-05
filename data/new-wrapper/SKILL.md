---
description: Scaffold a new PDO wrapper end-to-end (defn + test + README + CHANGELOG)
argument-hint: "[connection|statement] <pdo-method-name>"
disable-model-invocation: true
allowed-tools: "Read, Write, Edit, Glob, Grep, Bash(composer *), Bash(./vendor/bin/phel *), Bash(vendor/bin/phel *)"
---

# /new-wrapper

Walk the contributor flow for wrapping a PDO method.

## Context

!`ls src src/pdo tests`

## Instructions

### 1. Parse args

- `$ARGUMENTS` → `<kind> <name>`. `kind` ∈ {`connection`, `statement`}. If missing, ask.
- `name` = the PDO method (PHP camelCase, e.g. `bindParam`). The Phel wrapper name will be its kebab-case (`bind-param`).

### 2. Confirm it isn't already wrapped

```bash
grep -n "(defn.* <kebab-name>" src/pdo.phel src/pdo/statement.phel
```

If found, stop. The PDO surface is fully wrapped as of #46, so a genuinely unwrapped method is unusual - double-check `README.md`'s API tables before adding one.

### 3. Pick the file

- `connection` → `src/pdo.phel` (operates on `(conn :pdo)`)
- `statement` → `src/pdo/statement.phel` (operates on `(stmt :stmt)`)

### 4. Add the `defn`

Place next to its peers (transactions near transactions, fetch family near fetch). Skeleton:

```phel
(defn <return-tag> <kebab-name>
  "<terse one-liner>"
  [<conn-or-stmt> <pdo-args> & [<optional>]]
  (php/-> (<conn-or-stmt> :<pdo|stmt>) (<phpMethodName> <args>)))
```

Apply [api-design.md](../../rules/api-design.md): mutators return the wrapped struct; reads return Phel-native data (route rows through `row->map`, params in via `phel->php`).

### 5. Add the test

In `tests/pdo_test.phel`, under the matching section comment:

```phel
(deftest <descriptive-name>
  (seed-t1 *conn*)
  (is (= <expected> (pdo/<kebab-name> *conn* ...))))
```

Drive through `*conn*` + `t1` fixtures where possible. For errors, wrap in `(try ... (catch \PDOException _e nil))` then assert `pdo/error-code`/`pdo/error-info`.

### 6. Update README

Add a row to the matching API table (Connection or Statement) in `README.md` with the same signature and one-line description.

### 7. Verify

```bash
composer test
```

### 8. Changelog

Add an `### Added` entry under `## [Unreleased]` in `CHANGELOG.md`.

## Constraints

- Never expose raw `\PDO` / `\PDOStatement` from the public function.
- Never hand-concatenate values into SQL - that's PDO's job, params go through `phel->php`.
- Mutators must end in the wrapped struct so callers can thread.

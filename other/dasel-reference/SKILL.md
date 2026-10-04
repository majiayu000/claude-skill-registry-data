---
name: dasel-reference
description: Use when querying, modifying, or converting JSON, YAML, TOML, XML, CSV, HCL, or INI with dasel v3. Complete reference for selectors, functions, conditionals, variables, spread operator, type casting, and format-specific patterns.
---

# dasel v3 Syntax Reference

Single-binary CLI for querying, modifying, and converting structured data. Replaces `jq` + `yq` + `xmllint` with one unified query syntax across all formats.

Stable version at writing (date: 2026-02-23): **v3.2.3**

## Supported Formats

`json`, `yaml`, `toml`, `xml`, `csv`, `hcl`, `ini`

## Basic Usage

```bash
# Query from stdin (format required)
echo '{"foo": "bar"}' | dasel -i json 'foo'

# Query from file via stdin
cat config.yaml | dasel -i yaml 'database.host'

# Modify and output full document
echo '{"port": 3000}' | dasel -i json --root 'server.port = 8080'

# Convert formats
cat data.json | dasel -i json -o yaml
```

## Format Handling

dasel v3 does NOT auto-detect format from file extension. There is no `-f`/`--file` flag. Input is always read from stdin. Format must be specified explicitly with `-i` and/or `-o`. If only one is given, the other defaults to it. If neither is given, both default to `json` (configurable via `~/dasel.yaml` with `default_format` key).

Source: `internal/cli/query.go:10-11`, `internal/cli/run.go:37-43`, `internal/cli/config.go:19-21`

## Key Flags

```text
-i, --in <format>         Input parser (json, yaml, toml, xml, csv, hcl, ini)
-o, --out <format>        Output parser (defaults to input format)
--root                    Output full document after modification
--var <name>=<value>      Pass variables into query (repeatable)
--compact                 Compact output (no pretty-printing)
--rw-flag <name>=<value>  Read/write flag (e.g., --rw-flag csv-delimiter=;)
--read-flag <name>=<val>  Reader flag (e.g., --read-flag xml-mode=structured)
--write-flag <name>=<val> Writer flag (e.g., --write-flag csv-delimiter=;)
-c, --config <path>       Config file path (default: ~/dasel.yaml)
```

## Core Selectors Quick Reference

| Selector | Syntax | Example |
|----------|--------|---------|
| Dot notation | `foo.bar.baz` | `cat f.json \| dasel -i json 'foo.bar'` |
| Array index | `[0]`, `[2]` | `cat f.json \| dasel -i json 'items[0]'` |
| Array slice | `[0:3]` | `cat f.json \| dasel -i json 'items[0:2]'` |
| Recursive descent | `..`, `..name` | `cat f.json \| dasel -i json '..name'` |
| All values recursive | `..*` | `cat f.json \| dasel -i json '..*'` |
| Object construction | `{ key1, key2 }` | `cat f.json \| dasel -i json '{ name, age }'` |
| Spread | `obj...` | `cat f.json \| dasel -i json '{ defaults..., overrides... }'` |

## Key Functions Quick Reference

19 built-in functions in `DefaultFuncCollection` (source: `execution/func.go:12-33`) plus the `sortBy` complex expression.

| Function | Purpose | Example |
|----------|---------|---------|
| `filter(pred)` | Filter arrays | `users.filter(active == true)` |
| `map(expr)` | Transform arrays | `users.map(name)` |
| `each(expr)` | Modify each element | `each($this = $this * 2)` |
| `search(pred)` | Recursive search | `search(has("id"))` |
| `sortBy(expr)` | Sort array | `sortBy($this, desc)` |
| `has(key)` | Check key exists | `has("name")` |
| `get(key)` | Get value at key/index | `get("name")` |
| `contains(val)` | Check slice contains value | `contains(42)` |
| `len(expr)` | Length | `len($this)` |
| `join(sep)` | Join to string | `join(",")` |
| `sum(expr)` | Sum numeric array | `sum($this)` |
| `add(args...)` | Add numbers | `add(1, 2, 3)` |
| `max(args...)` | Maximum value | `max(1, 5, 3)` |
| `min(args...)` | Minimum value | `min(1, 5, 3)` |
| `merge(args...)` | Merge maps | `merge(defaults, overrides)` |
| `keys(expr)` | Get map keys | `keys($this)` |
| `reverse(expr)` | Reverse array | `reverse($this)` |
| `typeOf(expr)` | Get type string | `typeOf($this)` |
| `toString(expr)` | Cast to string | `toString($this)` |
| `toInt(expr)` | Cast to integer | `toInt($this)` |
| `toFloat(expr)` | Cast to float | `toFloat($this)` |
| `base64e(str)` | Base64 encode | `base64e("hello")` |
| `base64d(str)` | Base64 decode | `base64d("aGVsbG8=")` |
| `parse(fmt, data)` | Parse data at runtime | `parse("json", rawStr)` |
| `readFile(path)` | Read file contents | `readFile("config.json")` |
| `ignore()` | Exclude from branch | `ignore()` |

## Modification Syntax

v3 removed `put` and `delete` subcommands. Use assignment with `--root`:

```bash
# Set a value
echo '{"count": 1}' | dasel -i json --root 'count = 42'

# Boolean assignment
echo '{"enabled": false}' | dasel -i json --root 'enabled = true'

# Append to array
echo '[1,2,3]' | dasel -i json --root '[$this..., 4]'

# Remove key (reconstruct without it)
echo '{"keep": "yes", "drop": "no"}' | dasel -i json --root '{ keep }'
```

## Format Conversion

```bash
# JSON to YAML
cat data.json | dasel -i json -o yaml

# YAML to TOML
cat config.yaml | dasel -i yaml -o toml

# TOML to JSON
cat config.toml | dasel -i toml -o json
```

## Special Variables

- `$root` -- references the root document
- `$this` -- references the current node (inside `each`, `map`, `filter`, `search`)

## Variable Assignment

```bash
# Multi-statement with semicolons
cat data.json | dasel -i json '$active = users.filter(active == true); $active.map(name)'
```

## Conditionals

```bash
echo '{"count": 7}' | dasel -i json 'if(count > 5) { "many" } else { "few" }'
```

## v3 Breaking Changes from v2

- `put` and `delete` subcommands removed; use inline assignment with `--root`
- `-f`/`--file` flag removed; input always comes from stdin via pipe
- Query/selector syntax completely revamped; v2 syntax is NOT compatible with v3
- CLI framework changed from Cobra to Kong
- Go module path changed to `github.com/tomwright/dasel/v3`

## Detailed References

- [Selectors and Syntax](./references/selectors-and-syntax.md) -- dot notation, arrays, recursive descent, object construction, variables, conditionals, comparison operators
- [Functions Reference](./references/functions.md) -- complete function signatures, descriptions, and examples
- [Format-Specific Patterns](./references/format-patterns.md) -- JSON, YAML, TOML, XML, CSV, HCL, INI patterns and conversion caveats

## Sources

1. **dasel README**: <https://raw.githubusercontent.com/TomWright/dasel/master/README.md> (fetched 2026-02-19)
2. **dasel docs**: <https://daseldocs.tomwright.me> (fetched 2026-02-19)
3. **Query syntax**: <https://daseldocs.tomwright.me/syntax/query-syntax.md> (fetched 2026-02-19)
4. **Functions index**: <https://daseldocs.tomwright.me/functions> (fetched 2026-02-19)
5. **CHANGELOG**: <https://raw.githubusercontent.com/TomWright/dasel/master/CHANGELOG.md> (fetched 2026-02-19)
6. **Releases**: <https://github.com/TomWright/dasel/releases> (fetched 2026-02-19)
7. **Source code analysis**: `execution/func.go`, `internal/cli/query.go`, `internal/cli/run.go`, `internal/cli/config.go`, `execution/execute_binary.go`, `execution/execute_unary.go` (analyzed 2026-02-19)
8. **Fact-check**: [FACT_CHECK_REPORT.md](./FACT_CHECK_REPORT.md) (2026-02-23)

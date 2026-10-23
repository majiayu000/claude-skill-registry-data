---
name: buf-cli-lint-breaking-build
description: "Wraps the buf CLI for protobuf PR gating: `buf build` (compile .proto), `buf lint` (STANDARD rules: snake_case fields, Service suffix), `buf breaking --against {ref}` (detect wire/codegen breakage vs a git/BSR baseline), and `buf format`. Use as the CI proto-lint + breaking-change gate, or to debug a breaking failure by rule ID (e.g. FIELD_NO_DELETE_UNLESS_NUMBER_RESERVED) and pick the FILE/PACKAGE/WIRE_JSON/WIRE ruleset per consumer. This is the detection TOOL that enforces the rules and carries the catalog of what is breaking and why (field-number reservation, wire-safe vs wire-incompatible changes, oneof/map constraints, the four buf categories) in references/versioning-strategy.md; for cross-service schema contract testing use protobuf-compat-checking - not this."
---

# buf-cli-lint-breaking-build

## Overview

Wraps three buf CLI commands - `build`, `lint`, `breaking` - as the
proto-PR gate, per
[buf.build/docs/cli/quickstart/](https://buf.build/docs/cli/quickstart/).
The catalog of what counts as breaking and why lives in
[references/versioning-strategy.md](references/versioning-strategy.md)
(+ [references/buf-breaking-rules.md](references/buf-breaking-rules.md)).

## When to use

- Adding buf as the proto lint + breaking-change gate on a new
  repo.
- A PR changes `.proto` files - need to gate the merge.
- Investigating a `buf breaking` failure - what rule fired?
- Configuring buf for a monorepo with multiple proto modules.

## Authoring

### Install

Per buf docs, install via Homebrew, Go install, or release binary.
Version 1.32.0 or higher is required. Verify:

```bash
buf --version
# 1.32.0 or higher
```

### Configure `buf.yaml`

The v2 format per
[buf.build/docs/cli/quickstart/](https://buf.build/docs/cli/quickstart/):

```yaml
version: v2
modules:
  - path: proto
lint:
  use:
    - STANDARD
breaking:
  use:
    - FILE          # default; choose per references/versioning-strategy.md
```

`STANDARD` is the recommended lint rule set; it enforces
conventions like "Field name should be lower_snake_case" and
"Service name should be suffixed with Service".

The choice of `breaking.use` (FILE / PACKAGE / WIRE_JSON / WIRE)
follows the per-deployment-model logic in
[references/versioning-strategy.md](references/versioning-strategy.md).

### Configure `buf.gen.yaml` (codegen)

```yaml
version: v2
managed:
  enabled: true
plugins:
  - remote: buf.build/protocolbuffers/go
    out: gen
    opt: paths=source_relative
```

`managed: enabled: true` automatically sets file options without
hand-coding (e.g., `go_package`).

## Running

### Local validation pipeline

```bash
buf build && buf lint && buf breaking --against ".git#branch=main"
```

Three gates in order: compile, lint, breaking. All three must
pass before merge.

### `buf build`

```bash
buf build
# Silent exit on success
```

Compiles every `.proto` in the workspace. Silent → success. Any
output → error. Equivalent to `protoc` compilation but reads
`buf.yaml` for paths.

### `buf lint`

```bash
buf lint
# Emits violations as: <file>:<line>:<col>:<msg>
```

Validates against the configured rule set. Common failures:

| Failure | Rule | Fix |
|---|---|---|
| `Field name "userId" should be lower_snake_case` | `FIELD_LOWER_SNAKE_CASE` | Rename to `user_id` |
| `Service "Users" should be suffixed with "Service"` | `SERVICE_SUFFIX` | Rename to `UsersService` |
| `Message "user_data" should be UpperCamelCase` | `MESSAGE_UPPER_CAMEL_CASE` | Rename to `UserData` |
| `Enum value should be SCREAMING_SNAKE_CASE` | `ENUM_VALUE_UPPER_SNAKE_CASE` | Rename |

### `buf breaking`

```bash
buf breaking --against ".git#branch=main"
# Compares working tree against main branch
```

Baselines (per [buf docs](https://buf.build/docs/cli/quickstart/)):

| Baseline | Use |
|---|---|
| `".git#branch=main"` | Compare against main branch (CI default) |
| `".git#tag=v1.0.0"` | Compare against a release tag |
| `".git#subdir=path/to/proto"` | Sub-directory baseline (monorepo) |
| `"path/to/image.bin"` | Pre-built `buf build` image file |
| `"buf.build/owner/module"` | Compare against published BSR image |

Output on violation:

```
proto/foo.proto:42:5: Field "old_name" with type "string" no longer exists (rule FIELD_NO_DELETE_UNLESS_NUMBER_RESERVED).
```

Per [buf breaking rules](https://buf.build/docs/breaking/rules):
each violation cites the rule that fired so you know which
category constraint was violated.

## Parsing results

### CLI output (text, default)

Each violation: `<file>:<line>:<col>: <message> (rule <RULE_ID>).`

Pipe to grep / awk for counts:

```bash
buf breaking --against ".git#branch=main" 2>&1 | tee buf-breaking.log
wc -l buf-breaking.log
```

### Machine-readable output

```bash
buf lint --error-format=json
# Emits: [{"path":"...","start_line":...,"start_col":...,"end_line":...,"type":"FIELD_LOWER_SNAKE_CASE","message":"..."}]

buf breaking --against ".git#branch=main" --error-format=json
```

For consumption by a unified reporter.

## CI integration

Gate `buf build` / `lint` / `breaking` on PRs that touch `.proto`,
`buf.yaml`, or `buf.gen.yaml`. Key gotcha: `fetch-depth: 0` so git
has the baseline commit available. Full GitHub Actions workflow plus
the failure PR-comment:
[references/ci-integration.md](references/ci-integration.md).

## Anti-patterns

| Anti-pattern | Why it fails | Fix |
|---|---|---|
| Skipping `buf breaking` on PR | Subtle wire breakage merges; consumers crash at deploy time | Always gate; never `--ignore` blanket |
| Comparing against the PR's own merge base | Self-baseline; no detection | Use `".git#branch=main"` |
| `fetch-depth: 1` in CI | git can't reach baseline → buf errors | `fetch-depth: 0` |
| `breaking.use: WIRE` for codegen consumers | Generated code break (rename) passes; consumer build fails | Use `FILE` or `PACKAGE` per references/versioning-strategy.md |
| Adding `--ignore` to suppress a real violation | Silent regression | Use proper reserved + deprecation instead |
| Lint set `MINIMAL` for new projects | Misses snake_case + service-suffix conventions early | Use `STANDARD` from day 1 |
| One `buf.yaml` per proto file | Doesn't compose; lint runs N times | One `buf.yaml` at module root |
| Inconsistent baselines (main vs tag) | Different reviewers see different verdicts | Pick one CI baseline; document |

## Limitations

- **Semantic vs wire breakage.** Per
  [references/versioning-strategy.md](references/versioning-strategy.md),
  buf detects binary/codegen breakage. Semantic meaning changes
  ("field now means net price, not gross") are undetectable.
- **No cross-service compatibility.** This is single-service
  schema lint. For service-to-service contract testing see
  `protobuf-compat-checking`.
- **BSR features require auth.** Remote plugins, registry pushes,
  and `buf.build/...` baselines need a BSR account.
- **JSON-name detection** is in WIRE_JSON only. Services that
  use only binary won't see JSON name changes detected.
- **Doesn't generate code automatically.** `buf generate` is a
  separate step; this skill scopes to gating.

## References

- buf CLI quickstart:
  [buf.build/docs/cli/quickstart/](https://buf.build/docs/cli/quickstart/).
- buf breaking rules:
  [buf.build/docs/breaking/rules](https://buf.build/docs/breaking/rules).
- Versioning + breaking-change catalog:
  [references/versioning-strategy.md](references/versioning-strategy.md)
  (+ [references/buf-breaking-rules.md](references/buf-breaking-rules.md)).
- Status code vocabulary:
  `grpc-streaming-test-author` (references/status-codes.md).
- Sibling tools:
  `ghz-load`,
  `grpcurl-cli`,
  `grpc-mock`.
- Cross-service contract testing:
  `protobuf-compat-checking`.

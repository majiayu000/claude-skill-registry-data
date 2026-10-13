---
name: sdk-marker-protocol
description: >
  Use this when emitting or auditing machine-readable code provenance
  markers — traces-to, constraint, stable-since, deprecated-in,
  do-not-regenerate, owned-by, perf-exception — that drive marker-scanner,
  constraint-devil, marker-hygiene-devil, and Mode B/C merge safety.
  Triggers: traces-to, constraint, stable-since, deprecated-in, do-not-regenerate, owned-by, perf-exception, ownership-map, marker-hygiene, MANUAL, byte-hash.
version: 1.1.0
last-evolved-in-run: v0.6.0-rc.0-sanitization
status: stable
tags: [markers, provenance, sdk, language-pluggable]
cross_language_ok: true
---

<!-- The marker grammar (the 7 keys + their value formats) is language-neutral. The realization is per-language: line vs block comment delimiters, AST-hash backend per file extension, regex parsing per godoc style. Examples below use Go syntax because Go is the canonical pack today; the same markers apply over Python `#`-comment lines using the Python AST backend (`scripts/ast-hash/python-backend.py`). The leakage scripts honor `cross_language_ok: true`. -->


# sdk-marker-protocol (v1.0.0)

## Rationale

The SDK is a mixed ownership codebase — pipeline-authored code coexists with human-authored code that the pipeline MUST NOT touch. Without machine-readable provenance, Mode B/C incremental updates either clobber hand-tuned code or refuse to regenerate anything (brittle diff-heuristics do not scale past a single run). Markers are a 7-key taxonomy that `sdk-marker-scanner` reads to build `ownership-map.json`; every downstream agent (merge planner, constraint devil, semver devil, overengineering critic) reads that map. CLAUDE.md rule 29 is the authoritative source; this skill is the operational body.

## Activation signals

- Emitting new exported symbols into a target-SDK package — must carry a `[traces-to:]` marker
- Running in Mode B (extension) or Mode C (incremental update) — merge planner needs ownership-map byte-hashes
- TPRD §12 declares a signature change on a `[stable-since:]` symbol — verify semver-major + MAJOR declaration
- Adding a `[perf-exception:]` — pair with `runs/<id>/design/perf-exceptions.md` entry
- Declaring a perf constraint in godoc — must reference an extant benchmark
- `sdk-marker-hygiene-devil`, `sdk-marker-scanner`, `sdk-merge-planner`, or `sdk-constraint-devil-go` in the active agent list

## The 7 marker taxonomy

### 1. `[traces-to: TPRD-<section>-<id>]`

Every pipeline-authored exported symbol carries this in the preceding godoc block. Value grammar: `TPRD-\d+(\.\d+)*-[A-Z0-9-]+` (matches G102 regex). `MANUAL-<id>` form is reserved for human-authored code and MUST NOT be emitted by the pipeline (G103).

```go
// Config is the primary user-facing configuration for Cache.
// [traces-to: TPRD-§6-Config]
type Config struct { ... }
```

### 2. `[constraint: <measurement>:bench/<BenchmarkName>]`

Attaches a numeric NFR to a symbol with a verification benchmark. The measurement side (`p99<=1ms`, `allocs<=2`) is advisory; the bench side is enforced — G97 greps `testing/bench-raw.txt` for `BenchmarkName` and fails if the result is absent.

```go
// Get fetches a single key.
// [constraint: p99<=2ms:bench/BenchmarkGet]
func (c *Cache) Get(ctx context.Context, key string) (string, error) { ... }
```

### 3. `[stable-since: vX.Y.Z]`

Symbol signature frozen at this version. Any signature change without a TPRD §12 MAJOR declaration is a G101 BLOCKER. Baselines live in `baselines/<target_language>/stable-signatures.json` (per-language partition; G101 resolves the path from `runs/<run-id>/context/active-packages.json:target_language` with fallback to `go` for legacy replays), normalized through whitespace collapse.

### 4. `[deprecated-in: vX.Y.Z]`

Paired with godoc `Deprecated:` line. Removing the symbol before an actual release hits `vX.Y.Z` is G95 violation. Pair with `remove-in: vA.B.C` comment so consumers know their grace window.

### 5. `[do-not-regenerate]`

Bare marker (no value). File's first 1024 bytes trigger a whole-file hash lock in `baselines/<target_language>/do-not-regenerate-hashes.json` (G100; per-language partition). Any subsequent byte change is BLOCKER until the baseline hash is refreshed via human PR.

### 6. `[owned-by: MANUAL | pipeline | pipeline:<agent>]`

Per-symbol ownership declaration. MANUAL symbols are byte-hashed in `ownership-map.json` at Mode B/C entry; G95 verifies hash parity on exit (AST-hash on 0.3.0+, byte-hash legacy). Pipeline MUST NOT author new `owned-by: MANUAL` markers (G103).

### 7. `[perf-exception: <reason> bench/<BenchmarkName>]`

Escapes a symbol from `sdk-overengineering-critic` findings when complexity is measurably justified. Requires a paired entry in `runs/<id>/design/perf-exceptions.md` authored by `sdk-perf-architect-go` at design time (G110). Orphan markers (no entry) = BLOCKER; orphan entries (no marker) = BLOCKER.

## GOOD examples

Symbol with `[traces-to:]` on the godoc line directly above the declaration — what G102 parser expects:

```go
// New constructs a Cache from the supplied options. Returns
// ErrInvalidConfig when validation fails.
// [traces-to: TPRD-§5.1-New]
func New(opts ...Option) (*Cache, error) { ... }
```
(Source: `core/l2cache/dragonfly/cache.go` line 77-78)

File-level `[traces-to:]` as the first line — satisfies G99's file-level check for files whose exports are all declared inline:

```go
// [traces-to: TPRD-§8.2]
package dragonfly

import ( ... )
```
(Source: `core/l2cache/dragonfly/metrics.go` line 1)

Multi-section trace — a symbol serving two TPRD clauses uses space-separated ids:

```go
// Cache is the Dragonfly L2 cache client. Safe for concurrent use.
// [traces-to: TPRD-§5.1 TPRD-§8]
type Cache struct { ... }
```
(Source: `core/l2cache/dragonfly/cache.go` line 52)

## BAD examples (anti-patterns)

Forged MANUAL marker — pipeline-authored code self-claiming human ownership. BLOCKER via G103:

```go
// NewFast returns a hand-tuned cache.
// [traces-to: MANUAL-perf-team]   // <-- pipeline MAY NOT write this
// [owned-by: MANUAL]
func NewFast() *Cache { ... }
```
Why it breaks: `ownership-map.json` is the pipeline's source of truth for "what did a human write?". Letting generated code claim MANUAL ownership is an escape hatch out of every review gate, because marker-hygiene-devil skips MANUAL symbols from byte-comparison.

Constraint without a matching benchmark — G97 BLOCKER:

```go
// Set writes a key.
// [constraint: p99<=500us:bench/BenchmarkSet]   // <-- no BenchmarkSet in testing/bench-raw.txt
func (c *Cache) Set(...) error { ... }
```
Why it breaks: the constraint promises a verifiable number, but no benchmark produces one. Either add the bench or drop the marker — carrying an unverifiable constraint silently rots. `bench-raw.txt` must contain a line starting with `BenchmarkSet` for G97 to pass.

`[stable-since:]` signature drift without TPRD §12 MAJOR declaration — G101 BLOCKER:

```go
// Get fetches a key.
// [stable-since: v1.0.0]
// was: func (c *Cache) Get(ctx context.Context, key string) (string, error)
// now: func (c *Cache) Get(ctx context.Context, key string, opts ...GetOption) (string, error)
func (c *Cache) Get(ctx context.Context, key string, opts ...GetOption) (string, error) { ... }
```
Why it breaks: the `opts ...GetOption` addition changes the callable surface even though it is variadic and source-compatible — any interface embedding this method, any `_ = Get`, any reflection-based mock shatters. G101 greps TPRD §12 for `MAJOR` or `breaking` and blocks otherwise.

Unverified `[perf-exception:]` — orphan marker, G110 BLOCKER:

```go
// unsafeMemcpyInto is a SIMD unroll that out-runs the reflect impl.
// [perf-exception: avoids reflection overhead bench/BenchmarkMemcpy]
func unsafeMemcpyInto(...) { ... }
```
Why it breaks: no matching entry in `runs/<id>/design/perf-exceptions.md`. The exception marker is only valid as a pair — `sdk-perf-architect-go` must have declared the exemption at design time AND `sdk-profile-auditor-go` must have profile evidence. A lone marker is a bypass attempt of the cleanliness gates.

## Decision criteria

| Scenario | Marker | Notes |
|---|---|---|
| New exported symbol in pipeline-authored file | `[traces-to: TPRD-...]` | MANDATORY (G99) |
| Performance promise on hot path | `[constraint: ... bench/X]` | Requires matching bench (G97) |
| First release of a public type | `[stable-since: v1.0.0]` | Start tracking at first stable ship |
| Sunset timeline declared | `[deprecated-in: vX.Y.Z]` + `Deprecated:` godoc | Pair — one alone is lint-noise |
| Whole file is hand-tuned, pipeline cannot touch | `[do-not-regenerate]` in first 1024 bytes | Hard lock (G100) |
| Mixed-ownership file, per-symbol precision | `[owned-by: MANUAL]` or `[owned-by: pipeline]` | Populates `ownership-map.json` |
| Hand-optimized symbol must escape critic | `[perf-exception: ... bench/X]` + `perf-exceptions.md` entry | Both sides or neither (G110) |

When NOT to add a marker:
- Internal (lowercase) symbols — markers are godoc-adjacent; internal helpers rarely need provenance
- Test files (`*_test.go`) — G99 excludes them
- Generated code from `go generate` — use `// Code generated ... DO NOT EDIT.` instead, pipeline respects it

## Per-language adapter realization

The marker grammar is language-neutral; the comment syntax around it is per-language adapter:

| Aspect | Go realization | Python realization |
|---|---|---|
| Line marker delimiter | `// [traces-to: ...]` | `# [traces-to: ...]` |
| File extension | `.go` | `.py`, `.pyi` |
| AST-hash backend | `scripts/ast-hash/go-backend.go` | `scripts/ast-hash/python-backend.py` |
| Doc-comment block (G99 anchor) | godoc preceding declaration | docstring inside declaration |
| Test-file exclusion glob (G99) | `*_test.go` | `test_*.py`, `*_test.py`, `tests/` |

The 7-key taxonomy, regex grammar, and BLOCKER-vs-WARN severity assignments are identical across packs. `marker-hygiene-devil` and `sdk-marker-scanner` resolve the right backend from `runs/<run-id>/context/active-packages.json:target_language`.

## Cross-references

- `sdk-semver-governance` — reads `[stable-since:]` markers to classify bump size; G101 pairs with §10 of semver skill
- `go-example-function-patterns` / `python-doctest-patterns` — runnable-example functions in test files do not carry `[traces-to:]` markers (G99 excludes test files)
- `review-fix-protocol` — marker-hygiene-devil is one of the READ-ONLY reviewers; failures loop through the fix protocol
- `mcp-knowledge-graph` — marker state persists to neo4j-memory as Entity/Observation for cross-run queries

## Guardrail hooks

- **G95** — MANUAL ownership preserved (AST-hash preferred 0.3.0+, byte-hash legacy). BLOCKER in impl phase.
- **G96** — MANUAL byte-hash belt-and-suspenders, complements G95. BLOCKER.
- **G97** — `[constraint:]` markers referencing `bench/BenchmarkX` must have matching result in `testing/bench-raw.txt`. BLOCKER.
- **G98** — No marker deletions without HITL ack. BLOCKER.
- **G99** — Every pipeline-authored `.go` file carries ≥1 `[traces-to: TPRD-...]` marker. BLOCKER.
- **G100** — `[do-not-regenerate]` whole-file hash lock. BLOCKER.
- **G101** — `[stable-since:]` signature changes require TPRD §12 MAJOR. BLOCKER.
- **G102** — Marker syntax validity (key-specific value grammar). BLOCKER.
- **G103** — No forged MANUAL markers on pipeline symbols. BLOCKER.
- **G110** — `[perf-exception:]` paired with `perf-exceptions.md` entry. BLOCKER.

Run via `scripts/guardrails/G<nn>.sh <run-dir> <target-dir>`. All return exit 0 on PASS, 1 on FAIL, with per-check report at `runs/<id>/impl/<check-name>.md`.

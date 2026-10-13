---
name: go-dependency-vetting
description: >
  Use this when a PR diff adds a require line in go.mod, when justifying a new
  external dep, or when responding to an sdk-dep-vet-devil verdict. Covers the
  license/CVE/maintenance/size gate: govulncheck, osv-scanner, license
  allowlist, transitive count, last-commit-age, and the dependencies.md
  provenance contract that backs guardrails G31–G34.
  Triggers: go get, dependency, govulncheck, osv-scanner, license, supply chain, new dep, go.mod, DD-, CVE.
---

# go-dependency-vetting (v1.0.0)

## Rationale

Every new `go get` adds transitive surface area the SDK will ship to every downstream consumer. Rule 19 of `CLAUDE.md` mandates a dependency justification per new dep; rule 24 requires `govulncheck` + `osv-scanner` green on the result. This skill encodes the procedure so the decision never hinges on a reviewer remembering to check. Mirrors the `deps-ci-kit` convention: every dep is either in `runs/<run-id>/design/dependencies.md` with full provenance, or it is not in the SDK.

## Target SDK Convention

Current convention in motadatagosdk:
- `runs/<run-id>/design/dependencies.md` is the source of truth for dep provenance (name, version, license, size, vuln, age, transitive, justification).
- License allowlist lives in `.claude/settings.json#license_allowlist`: `MIT`, `Apache-2.0`, `BSD-3-Clause`, `BSD-2-Clause`, `ISC`, `0BSD`, `MPL-2.0`. Everything else = REJECT (GPL/AGPL/LGPL/SSPL/Proprietary) or CONDITIONAL (unknown).
- Guardrails G31 (dependencies.md exists), G32 (govulncheck clean), G33 (osv-scanner clean), G34 (license allowlist) are BLOCKER-severity at the design phase exit.
- `sdk-dep-vet-devil-go` renders the verdict; H6 surfaces CONDITIONAL.

If TPRD requests divergence (e.g., accepting a CONDITIONAL dep): user must explicitly amend the allowlist in settings.json AND provide rationale in `dependencies.md` §Justification — never silent-pass.

## Activation signals

- PR diff adds a line to `go.mod` (any `require` block change).
- TPRD §7 API references a type from a package not already in `go.mod`.
- `sdk-dep-vet-devil-go` is scheduled for Phase 1 design review.
- A design doc proposes `go get <foo>` in prose.
- Guardrail G31 fails (`dependencies.md` missing or empty).

## GOOD examples

### 1. `dependencies.md` entry for a new dep — every field populated

```markdown
## DD-042: github.com/redis/go-redis/v9

| Field             | Value                              |
|-------------------|------------------------------------|
| Version           | v9.7.0                             |
| License           | BSD-2-Clause                       |
| Size (source)     | 4.2 MB (`du -sk $(go list -m -f '{{.Dir}}' github.com/redis/go-redis/v9)`) |
| govulncheck       | 0 HIGH, 0 MEDIUM, 0 LOW            |
| osv-scanner       | No issues found                    |
| Last commit       | 2026-04-02 (22 days ago)           |
| Transitive count  | 7 (`go mod graph \| grep go-redis \| wc -l`) |
| GitHub stars      | 20.4k                              |
| Archived          | false                              |
| Justification     | Required for TPRD-§7.1 Dragonfly client. Stdlib `net` lacks RESP3. |
| Verdict           | ACCEPT                             |
```

### 2. Exact vetting commands — reproduce verbatim

```bash
# 1. Update go.mod + go.sum (scratch branch in case of reject).
cd "$SDK_TARGET_DIR"
git switch -c deps/vet-go-redis
go get github.com/redis/go-redis/v9@v9.7.0
go mod tidy

# 2. CVE scans — both tools, any HIGH/CRITICAL = REJECT.
govulncheck ./... 2>&1 | tee /tmp/govuln.txt
# Expect: "No vulnerabilities found." or "vulnerabilities found: 0"
osv-scanner --lockfile=go.mod 2>&1 | tee /tmp/osv.txt
# Expect: "No issues found"

# 3. License extraction — via go-licenses (or similar).
go-licenses report github.com/redis/go-redis/v9 2>&1 | tee /tmp/license.txt

# 4. Size, age, transitive.
go list -m -f '{{.Dir}}' github.com/redis/go-redis/v9 | xargs du -sk
git -C "$(go list -m -f '{{.Dir}}' github.com/redis/go-redis/v9)" log -1 --format=%cI
go mod graph | grep github.com/redis/go-redis | wc -l
```

### 3. License allowlist check — settings-driven, not hand-remembered

```bash
# Reads .claude/settings.json#license_allowlist — the single source of truth.
# G34.sh greps dependencies.md for forbidden licenses; always run it locally
# before pushing design docs.
ALLOW=$(jq -r '.license_allowlist[]' .claude/settings.json)
echo "$ALLOW"
# MIT
# Apache-2.0
# BSD-3-Clause
# BSD-2-Clause
# ISC
# 0BSD
# MPL-2.0

bash scripts/guardrails/G34.sh "$RUN_DIR" "$SDK_TARGET_DIR"
# → exits 0 if no GPL/AGPL/LGPL/SSPL/Proprietary matches in dependencies.md.
```

### 4. Transitive review — surface, not just direct dep

```bash
# The risk surface is direct + transitive. A trusted direct dep can still
# drag in an archived transitive. Enumerate + spot-check the top 10 by size.
go mod graph | awk '{print $2}' | sort -u > /tmp/transitive.txt
wc -l /tmp/transitive.txt
# If > 50 transitive for a single direct dep = CONDITIONAL per sdk-dep-vet-devil-go.

# Spot-check last-commit age on each transitive (> 2 years dormant = CONDITIONAL):
while read -r mod; do
    dir=$(go list -m -f '{{.Dir}}' "$mod" 2>/dev/null) || continue
    [ -d "$dir/.git" ] || continue
    age=$(git -C "$dir" log -1 --format=%cr)
    echo "$mod $age"
done < /tmp/transitive.txt | sort
```

### 5. Verdict emission — machine-readable for H6 gate

```bash
# sdk-dep-vet-devil-go writes this exact JSON shape per dep to the decision log.
# H6 aggregates; CONDITIONAL rows surface to the user.
jq -n \
    --arg dep "github.com/redis/go-redis/v9" \
    --arg verdict "ACCEPT" \
    --arg license "BSD-2-Clause" \
    --argjson vuln_high 0 \
    --arg age_days "22" \
    '{type:"event", event_type:"dep-vet", dep:$dep, verdict:$verdict,
      license:$license, vuln_high:$vuln_high, age_days:$age_days}' \
    >> "runs/$RUN_ID/decision-log.jsonl"
```

## BAD examples

### 1. Skipping `osv-scanner` because `govulncheck` was green

```bash
# BAD: osv-scanner catches GHSA advisories that govulncheck's Go-specific
# vuln DB can miss. Both MUST run — rule 24 is not satisfied by one.
govulncheck ./...
# "No vulnerabilities found." → ship it  ← WRONG
```

Fix: always run both; G32 and G33 are separate guardrails for a reason.

### 2. Vendoring a GPL dep "temporarily"

```go
// BAD: Copied upstream GPL source into internal/ to avoid go.mod.
// License attaches to the compiled binary regardless of module graph.
// This converts the entire SDK to GPL — a legal blocker, not a lint nit.
package internal

// originally: github.com/someorg/somegpl/foo
func Foo() { ... }
```

Fix: reject the dep. If the functionality is load-bearing, implement it in-house under a compatible license OR require a specific waiver via `.claude/settings.json` allowlist amendment with legal sign-off (NOT a skill-level decision).

### 3. "Latest" version pin (`go get foo@latest`)

```bash
# BAD: go.sum pins a specific hash, but the dependencies.md entry says
# "latest" — next `go mod tidy` silently upgrades past the vetted version.
go get github.com/some/dep@latest
echo "| Version | latest |" >> dependencies.md
```

Fix: always pin to an exact semver (`@v1.2.3`) in both `go.mod` and `dependencies.md`. Version bumps = new vet cycle.

### 4. Ignoring transitive-count because the direct dep is small

```markdown
## DD-099: github.com/big-framework/v1

| Direct size     | 800 KB  |
| Transitive count| 214     |   ← buried, never discussed
| Verdict         | ACCEPT  |   ← wrong
```

Fix: 214 transitives = 214 audit targets + 214 CVE surfaces. Per `sdk-dep-vet-devil-go`, >50 transitives is CONDITIONAL and must be justified in the §Justification field.

### 5. Archived repo, no fork

```markdown
## DD-100: github.com/abandoned/lib

| Last commit | 2022-08-14 (3.5 years ago) |
| Archived    | true                       |
| Verdict     | ACCEPT                     |   ← BLOCKER
```

Fix: archived = REJECT (rule from `sdk-dep-vet-devil-go`). If the functionality is required, fork to an in-house mirror and vendor the fork — at least then the supply chain belongs to us.

## Decision criteria

| Signal | Verdict |
|---|---|
| License in allowlist, govulncheck/osv-scanner clean, <2y old, <50 transitive | ACCEPT |
| License unknown / ambiguous (dual-license, custom terms) | CONDITIONAL → H6 user decision |
| One MEDIUM vuln with upstream fix path documented | CONDITIONAL |
| Size > 10 MB source | CONDITIONAL — justify |
| >2 years since last commit | CONDITIONAL — justify or fork |
| Any HIGH/CRITICAL vuln | REJECT |
| GPL/AGPL/LGPL/SSPL/Proprietary license | REJECT |
| Archived upstream | REJECT |
| Dep adds functionality already in stdlib | REJECT — use stdlib |

## Cross-references

- `sdk-semver-governance` — how version-pin choices interact with the SDK's own semver commitments
- `go-otel-instrumentation` — the OTel dep family has special-case grouping; treat OTel version bumps as a single vet cycle
- `go-module-paths` — import path → module mapping (prevents accidental double-dep of vN vs vN+1)

## Guardrail hooks

- **G30** — `design/api.go.stub` compiles, which means new deps resolve in go.mod.
- **G31** — `design/dependencies.md` exists and is non-empty (BLOCKER).
- **G32** — `govulncheck ./...` clean on target (BLOCKER).
- **G33** — `osv-scanner -r` clean on go.mod (BLOCKER).
- **G34** — license allowlist enforced against `dependencies.md` (BLOCKER).
- `sdk-dep-vet-devil-go` is the READ-ONLY agent that consumes this skill's rules and writes `runs/<run-id>/design/reviews/dep-vet-devil.md`; HITL gate H6 surfaces any CONDITIONAL row.

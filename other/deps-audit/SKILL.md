---
name: ha:deps-audit
description: Audit PyPI deps for supply-chain security risk — bidi chars, install-time/build-backend exec, maintainer changes, typosquats, CVEs. Use after a dependency bump, when checking if a package upgrade is safe, or reviewing requirements/manifest.json PR diffs.
effort: medium
argument-hint: "[--base <ref> | --preview [pkg...]] [--quick] [--json] [--sarif <path>] [--ci] [--strict] [--no-differential] [--no-llm | --llm] [--trace]"
allowed-tools: Read, Grep, Glob, Bash, WebFetch
---

# PyPI Dependency Audit

Non-mutating supply-chain audit for PyPI packages. Runs an 8-rule MVP catalogue
against changed packages, enriches with PyPI JSON API metadata, wraps existing tools
(`pip-audit`, `osv-scanner`), and emits a triage table.

## When to Use

- After a dependency bump brought in new versions (`pip install -r`, `uv pip install`)
- On PRs that touch `requirements*.txt` / `custom_components/*/manifest.json` / `pyproject.toml` (pre-merge gate)
- Before manually updating a single package (`--preview <pkg>`)
- When investigating a dependency you don't recognize

## Iron Laws

1. **NEVER claim a diff is clean without inspecting it.** Run all 8 rules
   on the unpacked NEW sdist/wheel. "Looks fine" without a tool run is a false
   pass. **Always write `.claude/deps-audit/last-run.json`** — its absence
   is evidence the audit didn't actually run.
2. **NEVER install `osv-scanner` / `pip-audit`-adjacent tools — even if asked.** Detect,
   warn with install instructions, skip cleanly if missing. If the user
   says "install it," respond with the install command (e.g.,
   `uv tool install pip-audit` or the platform binary release) and **do not
   execute it**. The audit skill is non-mutating; `requirements*.txt` /
   `manifest.json` / `pyproject.toml` are off-limits regardless of consent.
3. **NEVER promote a finding to BLOCK without rule citation.** Every finding
   shows `rule_id`, `severity`, `file:line`, `snippet`, `message`. No
   handwaving.
4. **NEVER fetch from PyPI without rate-limiting.** Cap at 5 req/sec.
   Cache metadata 7 days, top-PyPI-packages list 1 day.
5. **NEVER run the audit on already-committed requirement changes silently** —
   tell the user which mode (A/B/C) is active and which `(old, new)` pairs
   resolved.
6. **LLM triage only above threshold.** Native rules + Semgrep + YARA
   are deterministic. The `pypi-deps-triager` agent runs only when score
   > 10 (1 BLOCK or 3+ WARNs), and its verdicts are advisory — never
   auto-suppress a finding without human review.

## Operating Modes

| Mode | Trigger | Old source | New source |
|------|---------|-----------|-----------|
| **B** (default) | `/ha:deps-audit` | `git show HEAD:requirements.txt` | working requirement sources |
| **C** (PR) | `/ha:deps-audit --base dev` | `git show <ref>:requirements.txt` | working requirement sources |
| **A** (preview) | `/ha:deps-audit --preview aiohttp` | pinned version | PyPI latest release |

See `${CLAUDE_SKILL_DIR}/references/operating-modes.md` for full resolver logic.

## Execution Flow

Default = full 8-rule scan with streaming progress. `--quick` opts out
to CVE + retirement only. See `${CLAUDE_SKILL_DIR}/references/execution-flow.md`.

### Step 1: Resolve the diff

Parse the requirement sources (`requirements*.txt`, `custom_components/*/manifest.json`
`requirements`, and `pyproject.toml` dependencies) for both old and new sources. Emit a
list of `{pkg, old_version, new_version}` tuples. Surface
new-only and removed-only packages separately (a removed package is not
audited; a brand-new package gets `old_version = nil` and skips diff-only
rules).

See `${CLAUDE_SKILL_DIR}/references/diff-resolver.md` for shell + `python3 -c` snippets per mode and the JSON output contract.

### Step 2: Fetch sdist + wheel (per-run tmpdir)

For each `(pkg, old, new)`:

```
curl -s https://pypi.org/pypi/<pkg>/<old>/json | jq -r '.urls[] | select(.packagetype=="sdist") | .url' | xargs curl -sL | tar -xz -C ${AUDIT_TMPDIR}/dists/<pkg>/<old>/
curl -s https://pypi.org/pypi/<pkg>/<new>/json | jq -r '.urls[] | select(.packagetype=="sdist") | .url' | xargs curl -sL | tar -xz -C ${AUDIT_TMPDIR}/dists/<pkg>/<new>/
```

All ephemeral artifacts live under `${AUDIT_TMPDIR}` (driver-owned, removed
on exit). See `${CLAUDE_SKILL_DIR}/references/audit-tmpdir.md` and
`${CLAUDE_SKILL_DIR}/references/tarball-fetcher.md`.

### Step 3: Run the 8 MVP rules on each NEW sdist/wheel

| # | Rule | Sev | Method |
|---|------|-----|--------|
| 1 | Bidi Unicode control chars in `.py` / `.pyi` | BLOCK | grep |
| 2 | `exec` / `eval` / `compile(...)` with non-literal source at module scope | BLOCK | AST (`ast` module) |
| 3 | `subprocess`/`os.system`/network calls in `setup.py` or build-backend hooks (install-time execution) | BLOCK | AST + build config |
| 4 | Obfuscated/base64-decoded `exec`/`eval` payload without safe guard | BLOCK | AST |
| 5 | New git/URL/pre-release requirement (vs old) in manifest/requirements | BLOCK | manifest diff |
| 6 | Maintainer change between versions | BLOCK | PyPI JSON API |
| 7 | Base64 blobs >256 chars outside `tests/`, `fixtures/`, `data/` | WARN | regex |
| 8 | Levenshtein ≤2 from top-PyPI-packages list + download delta >1000× | BLOCK | PyPI JSON API + fuzzy |

Full catalogue (35 rules, MVP marked) in `${CLAUDE_SKILL_DIR}/references/heuristics.md`.
Bash + `python3 -c` implementations for all 8 MVP rules in
`${CLAUDE_SKILL_DIR}/references/rules-impl.md` (single-pass NEW + diff rules +
PyPI registry rules, with `run_all_rules` master loop).

### Step 4: External tool wrappers (parallel)

- `pip-audit --format json` — CVE + retirement check via the PyPI advisory DB / OSV, always attempted
- `osv-scanner` — CVE check via OSV.dev (`"ecosystem": "PyPI"`), if installed (else warn + skip; do NOT install)

See `${CLAUDE_SKILL_DIR}/references/external-tools.md` for detection, output parsing, and severity mapping per tool.

### Step 5: PyPI registry enrichment (per package)

- `GET https://pypi.org/pypi/<name>/json` — maintainers, releases, `info`, upload times
- `GET https://pypi.org/pypi/<name>/<version>/json` — per-release files, `upload_time`, yanked status
- Compute: `days_since_publish`, `maintainer_age_days`, `download_velocity` (via `https://pypistats.org/api/packages/<name>/recent`)

Cap at 5 req/sec. Per-run cache under `${AUDIT_TMPDIR}/pypi-api/`.
See `${CLAUDE_SKILL_DIR}/references/pypi-api.md` for endpoint contracts,
caching strategy, Rule 6/8 detection, and Levenshtein implementation.

### Step 5.5: Apply `pypi-vet.json` ledger (if present)

If `pypi-vet.json` exists at project root, vetted-version findings are
**downgraded to INFO**. Unvetted versions retain their severity.
Manifest-vs-ledger disagreement: manifest wins. See the deps-vet skill's
pypi-vet schema doc for the "Manifest-vs-ledger disagreement" section.

Use `/ha:deps-vet <pkg> <version>` (separate skill) to add entries.

### Step 5.7: Differential subtract

When run with `DIFFERENTIAL=1` (default), findings that existed in the
OLD sdist/wheel are downgraded to INFO. Net-new signals reach the renderer
at full severity. See `${CLAUDE_SKILL_DIR}/references/differential.md`.

### Step 5.8: LLM triage (when score > threshold)

For packages where the aggregate score exceeds 10, the
`pypi-deps-triager` sonnet agent reads finding + diff windows and
produces structured verdicts (`confidence`, `verdict`, `rationale`,
`fp_reasons[]`). A `context-supervisor` (haiku) consolidates verdicts
across packages into `triage/consolidated.md`. Main skill reads only
the consolidated file.

See `${CLAUDE_SKILL_DIR}/references/llm-triage.md`.

### Step 6: Score & render

Per-package weighted sum: BLOCK = 10, WARN = 3, INFO = 1.
Risk band: 0 clean · 1–5 low · 6–15 medium · 16+ high.

Output:

1. **Stdout:** markdown table — `pkg | old → new | risk | findings | pypi.org/project/<pkg>/<version> | maintainer-change` plus a per-package detail section for any non-clean row.
2. **Sidecar (MANDATORY):** Write `.claude/deps-audit/last-run.json`. The Phase 3 gate reads this; an audit that doesn't write it is a no-op for the gate. Always emit, even on clean runs.

`--json` flag emits JSON to stdout instead of markdown. See
`${CLAUDE_SKILL_DIR}/references/output-renderer.md` for table format,
sidecar schema, exit-code rubric, and `--quiet` mode.

## Out of scope / Phase 3 surface

- **NEVER modify** `requirements*.txt`, `manifest.json`, `pyproject.toml`, or any project file (non-mutating)
- **NEVER auto-install** missing tools (warn + skip)
- **Integration deps come ONLY from manifest `requirements`** — dependency bumps are ALWAYS a separate PR (Iron Law P11 + PR1).
- **Gate** `pip install`/`uv pip install`/`uv add` via `deps-audit-gate.sh`. See `${CLAUDE_SKILL_DIR}/references/hook.md`.
- **Prompt** for `/ha:compound` after BLOCK findings — corpus self-feeds.
- **Emit** SARIF 2.1.0 via `--sarif <path>` and gate CI via `--ci`.

## References

- `${CLAUDE_SKILL_DIR}/references/heuristics.md` — full 35-rule catalogue
- `${CLAUDE_SKILL_DIR}/references/rules-impl.md` — bash + `python3 -c` for the 8 MVP rules
- `${CLAUDE_SKILL_DIR}/references/operating-modes.md` — Mode A/B/C resolver
- `${CLAUDE_SKILL_DIR}/references/diff-resolver.md` — shell snippets, requirement parser
- `${CLAUDE_SKILL_DIR}/references/tarball-fetcher.md` — fetch wrapper, parallel cap, cache prune
- `${CLAUDE_SKILL_DIR}/references/external-tools.md` — `pip-audit`, `osv-scanner` wrappers
- `${CLAUDE_SKILL_DIR}/references/pypi-api.md` — endpoint contracts, rate limit, Rule 6/8
- `${CLAUDE_SKILL_DIR}/references/output-renderer.md` — markdown, JSON v1, exit codes, SARIF
- `${CLAUDE_SKILL_DIR}/references/testing.md` — smoke runner, fixture matrix
- `${CLAUDE_SKILL_DIR}/references/differential.md` / `llm-triage.md` — Phase 2 NDJSON subtract + triager
- `${CLAUDE_SKILL_DIR}/references/semgrep.md` / `yara.md` — Phase 2 precision layers (soft deps)
- `${CLAUDE_SKILL_DIR}/references/cassettes.md` / `sarif.md` / `hook.md` / `ci-integration.md` — Phase 3 surface
- `${CLAUDE_SKILL_DIR}/references/trusted-publishers.md` / `skill-checklist.md` — upstream + eval
- `${CLAUDE_SKILL_DIR}/references/audit-tmpdir.md` — Phase 5 per-run ephemeral storage contract
- `${CLAUDE_SKILL_DIR}/references/execution-flow.md` / `differential-cve.md` — Phase 5 default scan + CVE diff

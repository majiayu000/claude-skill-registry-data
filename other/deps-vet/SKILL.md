---
name: ha:deps-vet
description: "Record a vetted PyPI package version in pypi-vet.json after a security review — manages the audit ledger, not the scanner. Use to approve a dep after /ha:deps-audit findings or to initialize pypi-vet.json."
argument-hint: "<pkg> <version> | --seed | --list | --check"
effort: medium
---

# Deps Vet — PyPI package audit ledger

Review a PyPI package version, run Phase 1 supply-chain rules against it,
prompt the user for a verdict, append the result to `pypi-vet.json`
(project-root audit ledger). Vetted versions get downgraded to `INFO`
on subsequent `/ha:deps-audit` runs.

Run this AFTER `/ha:deps-audit` to clear findings.
Run this BEFORE merging a `manifest.json`/`requirements*.txt` PR to certify
new versions.

## Usage

```text
/ha:deps-vet aiohttp 3.11.10        # vet a single package version
/ha:deps-vet --seed                 # import curated baseline seed (~30 pkgs)
/ha:deps-vet --list                 # show existing ledger entries
/ha:deps-vet --check                # cross-check requirements/manifests vs ledger
```

## Iron Laws

1. **NEVER auto-approve.** Every entry MUST come from an `AskUserQuestion`
   confirmation. Drive-by trust ruins the ledger's value.
2. **Manifest wins on disagreement.** If a `manifest.json`/`requirements*.txt`
   pins version X and the ledger vets X-1, emit INFO and treat X as
   unvetted. Don't silently trust the older entry.
3. **Ledger lives at project root.** `pypi-vet.json` is a first-class
   security artifact, visible in PR review. Don't move it into `.claude/`.
4. **Round-trip via `json.dumps`.** When appending, read the file with
   `json.load(open('pypi-vet.json'))`, mutate the object, and write back
   via `json.dumps(obj, indent=2)`. Hand-rolled string appends drift over
   time.
5. **Always show findings before prompting.** The user must see what's
   being vetted. No silent `"safe_to_deploy"` defaults.
6. **Confirmation counts are COMPUTED, never estimated.** Any number in
   an `AskUserQuestion` (verdict split, new/overwrite/no-op) MUST be
   derived from the loaded data *before* prompting — e.g. a `collections.
   Counter` over `seed["audits"]` keyed on `verdict`. Eyeballing the file
   and approving on wrong numbers corrupts the consent.

## Execution flow

### Step 1: Locate or seed `pypi-vet.json`

```text
If pypi-vet.json exists at project root:
    Read it via json.load(open('pypi-vet.json'))
Else:
    Write the empty-ledger stub (see ${CLAUDE_SKILL_DIR}/references/pypi-vet.md §"Empty ledger")
    Inform user: "Created pypi-vet.json at project root."
```

### Step 2: Branch by mode

- **`<pkg> <version>`** → single-vet path (Step 3-7).
- **`--seed`** → import `priv/pypi-vet-seed.json`. Before prompting,
  `json.load` the seed and **compute** (Iron Law #6): the `verdict`
  split (`Counter(a["verdict"] for a in seed["audits"])`) and, against
  any existing ledger, exact new / overwrite / no-op counts. Put those
  computed numbers in the `AskUserQuestion`. Also state up front that the
  seed is a **provenance baseline, not certification of your current
  `manifest.json`/`requirements*.txt`** (per Iron Law #2, seed versions
  older than the pinned ones stay unvetted). Ask before overwriting
  existing entries.
- **`--list`** → render the audits table; exit.
- **`--check`** → compare ledger entries with the pinned requirement set
  (`custom_components/*/manifest.json` `requirements`, `requirements*.txt`,
  `pyproject.toml` dependencies); warn on drift. Parse each pin with
  `python3 -c` (`re` on `pkg==ver`) — exact and noise-free.

### Step 3: Fetch the sdist (single-vet)

Reuse (or establish) `${AUDIT_TMPDIR}` per deps-audit's
per-run-tmpdir contract, then fetch the sdist directly from PyPI —
no persistent cache:

```bash
curl -s https://pypi.org/pypi/<pkg>/<version>/json \
  | jq -r '.urls[] | select(.packagetype=="sdist") | .url' \
  | xargs curl -sL \
  | tar -xz -C "${AUDIT_TMPDIR}/dists/<pkg>/<version>/"
```

See `${CLAUDE_SKILL_DIR}/../deps-audit/references/audit-tmpdir.md` for
the tmpdir contract this borrows.

### Step 4: Run Phase 1 rules

Source the rules from `../deps-audit/references/rules-impl.md`.
Run `run_all_rules` over the extracted dir. Write findings to a temp
`vet-findings.jsonl` under `${AUDIT_TMPDIR}`. Set `FINDINGS_FILE` to
override default path.

### Step 5: Present findings

Print the findings table per `../deps-audit/references/output-renderer.md`.
On zero findings: say "No findings — vet from a clean baseline."
On any finding: show severity, file, line, snippet inline.

### Step 6: Prompt for verdict

Call `AskUserQuestion` with these 4 options:

- **`safe_to_deploy`** — full trust; findings investigated and cleared.
- **`safe_to_run`** — trust in non-production envs only (test/dev deps).
- **`does_not_implement_crypto`** — Mozilla-style sub-criterion.
- **`Skip`** — defer decision; don't write an entry.

If any finding is BLOCK severity: default-highlight `Skip`. Require
explicit override before writing `safe_to_deploy` over a BLOCK.

### Step 7: Append to ledger

Read existing `pypi-vet.json` via `json.load`. Prepend the audit object
below to `audits`. Write back via `json.dumps(obj, indent=2)`.

```json
{
  "name": "<pkg>",
  "version": "<version>",
  "verdict": "<verdict>",
  "reviewer": "<git config user.email>",
  "notes": "<user-provided one-liner OR findings summary>",
  "audited_at": "<today, ISO date via date.today().isoformat()>"
}
```

Write back via the append snippet in
`${CLAUDE_SKILL_DIR}/references/pypi-vet.md` §"Append flow".
Confirm to user: "Added `<pkg>` `<version>` to pypi-vet.json."

## Integration

- **Run after** `/ha:deps-audit` to clear vetted findings.
- **Run before** merging a `manifest.json`/`requirements*.txt` PR to certify new versions.
- **Run `/ha:deps-vet --check`** to detect ledger drift vs the pinned requirement set.
- **`/ha:deps-audit`** auto-downgrades vetted findings to INFO.
- The `deps-audit-gate.sh` PreToolUse hook reads `block_on_unvetted` from
  this ledger to gate `pip install`/`uv pip install`/`uv add`; the
  `HA_SKIP_DEPS_AUDIT=1` escape hatch bypasses it for local iteration.

## References

- `${CLAUDE_SKILL_DIR}/references/pypi-vet.md` — schema, parser, lookup
- `${CLAUDE_SKILL_DIR}/references/seed.md` — `--seed` flag, curated baseline
- `${CLAUDE_SKILL_DIR}/../deps-audit/references/rules-impl.md` — the
  same rules `/ha:deps-audit` runs

## Out of scope (Phase 3+)

- **CLI task surface** — defer a standalone `ha-deps-vet` console script to
  a separate PyPI package for non-CC users.
- **Block-on-unvetted enforcement** — handled by the `deps-audit-gate.sh`
  PreToolUse hook that gates `pip install`.
- **Distributed imports** — defer cargo-vet `imports:` until
  trust-chain semantics are designed.

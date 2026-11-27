---
name: codeql-semgrep-review
description: "SAST for kio-qa-security: Semgrep scans and CodeQL taint tracking with merged SARIF. Use for security audits, pre-merge scans of risky diffs, or 'scan this repo for vulnerabilities'. The review process itself is in ../security-review.md."
metadata:
  author: Trail of Bits (CodeQL/Semgrep workflows, scripts, references)
  maintainer: Kio System
---

# 🛡️ Static Analysis (Semgrep + CodeQL)

> Adapted from Trail of Bits `skills` (static-analysis). This whole folder is licensed **CC BY-SA 4.0**; see [LICENSE](LICENSE). Kio changes are listed there.

`{baseDir}` below is this folder: `<kio-qa-security install dir>/references/codeql` (for example `~/.claude/skills/kio-qa-security/references/codeql`). Substitute it literally in every command.

## When to use what

| Need | Go to |
|---|---|
| Review a feature or PR before merge | [`../security-review.md`](../security-review.md) (two-stage review, 5-layer checklist, sign-off) |
| Fast pattern scan, many languages, no build | Semgrep: Follow "Step 1: Resolve Output Directory, Detect Languages and Pro Availability" in workflows/scan-workflow.md |
| Deep interprocedural taint tracking | CodeQL: [Database Discovery](#database-discovery), then Follow "Step 1: Detect Language and Configure" in workflows/build-database.md, then workflows/run-analysis.md |
| Model a custom framework's sources/sinks | workflows/create-data-extensions.md |
| Merge and triage results | `{baseDir}/scripts/merge_sarif.py`, references/sarif-processing.md |

Rule references: references/rulesets.md, references/ruleset-catalog.md (Trail of Bits, 0xdea, Decurity and community packs), references/scan-modes.md ("important only" vs "run all"), references/threat-models.md.

---

## Each Bash call is a fresh shell

Every fenced block in this skill and its workflows runs as **its own Bash invocation**. Nothing set in one block exists in the next:

- **Variables and arrays** (`OUTPUT_DIR`, `DB_NAME`, `CODEQL_LANG`, `FOUND_DBS`) must be set again, or re-derived, in the block that uses them. An array built in an earlier block is empty in a later one, and an empty `FOUND_DBS` reads as "no database".
- **Functions** from `source "{baseDir}/scripts/build_log.sh"` (`log_step`, `run_logged`, …) must be sourced again in each block; a missing function exits 127, which the build ladder reads as a failed method.
- **`PATH` changes** (for example adding CodeQL) do not carry over; check for `codeql` in the block that needs it.
- Read script output with command substitution (`OUT=$(script)`), not `done < <(script)`: a process substitution discards the exit status.

## Database Discovery

Before building a CodeQL database, look for existing ones. Discovery and selection share one block so the array never crosses a shell boundary:

```bash
OUTPUT_DIR="${OUTPUT_DIR:-.}"
if ! DB_LIST=$("{baseDir}/scripts/find_databases.sh" "$OUTPUT_DIR" .); then
  echo "ERROR: database discovery failed — see the message above" >&2
  exit 1
fi

FOUND_DBS=()
while IFS= read -r db; do
  [ -n "$db" ] || continue
  FOUND_DBS+=("$db")
done <<<"$DB_LIST"

echo "Found ${#FOUND_DBS[@]} CodeQL database(s):"
for db in "${FOUND_DBS[@]}"; do
  echo "  - $db"
done
```

- **0 found** → build one: Follow "Step 1: Detect Language and Configure" in workflows/build-database.md.
- **1 found** → set `DB_NAME` to it and run workflows/run-analysis.md.
- **Several** → ask the user which one, then set `DB_NAME` in the analysis block.

`find_databases.sh` exits 2 when `codeql` is not on this shell's `PATH`; report that instead of rebuilding.

---

## Semgrep quick start

```bash
# Never send telemetry from a client's code
semgrep scan --config auto --metrics=off --error --sarif --output semgrep-results.sarif
```

For curated packs, approval gates and parallel runs use workflows/scan-workflow.md; merge outputs with `{baseDir}/scripts/merge_sarif.py`.

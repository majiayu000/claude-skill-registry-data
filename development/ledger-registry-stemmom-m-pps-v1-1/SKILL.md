---
name: ledger-registry
description: >
  Reads /ledger/manifest.json, verifies per-ledger checksums, and returns the active ledger map.
  **Version:** 1.1  **Author:** Entropy Control Theory  **License:** MIT
  **Based on:** Structure DNA v1.0 + PROFILE-GENERATOR-SPEC v1.0
---

# ledger.registry — v1.1

## Goal
Provide a single source of truth for active ledgers and integrity status.  
If missing, auto-generate `/ledger/profile.json` (energy-aware preferences) based on `profile.schema.json` + `profile.defaults.json`.

## Inputs
- none (or `verify=true` to force SHA-256 recompute)

## Outputs
- Returns manifest summary:
  - module → path
  - schema version
  - metadata.version
  - metadata.checksum (valid/invalid)
- Auto-generates `profile.json` if absent, ensuring downstream Skills can use energy preferences.

## Mechanism
1. Load `/ledger/manifest.json` or scan `/ledger/` for `.json` files.
2. **Check for presence of module `"profile"`**:
   - If absent → call `ensure_profile(ledger_dir="/ledger")`.
   - Reload ledger list to include the newly created `profile.json`.
3. For each ledger, recompute checksum; compare with `metadata.checksum` per Structure DNA integrity rules.
4. Write updated checksums and ledger list back to `/ledger/manifest.json`.
5. Return runtime registry map.

## Pseudocode
```python
def run_registry(ledger_dir="/ledger"):
    ledgers = scan_ledgers(ledger_dir)

    # ✅ NEW STEP: ensure profile.json exists
    if not any(L["module"] == "profile" for L in ledgers):
        ensure_profile(ledger_dir)  # uses profile.schema.json + profile.defaults.json
        ledgers = scan_ledgers(ledger_dir)  # re-scan to include it

    manifest = build_manifest(ledgers)
    manifest["metadata"]["last_sync"] = now_iso()
    manifest["metadata"]["checksum"] = recompute_checksum(manifest)
    save_json(f"{ledger_dir}/manifest.json", manifest)
    return manifest


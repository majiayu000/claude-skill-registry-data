---
name: troubleshoot
description: Diagnose common cqs issues — stale index, model download, schema mismatch, connection issues.
disable-model-invocation: false
argument-hint: ""
---

# Troubleshoot

Guided diagnosis of common cqs issues. Run through checks in order, stop at first problem found.

## Checklist

### 1. Is cqs installed and working?

```bash
cqs --version
```

If not found: `cargo install --path .` (from source) or check `~/.cargo/bin/` is in PATH.

### 2. Is the project initialized?

```bash
ls -la .cqs/ && cat .cqs/active_slot 2>/dev/null
ls -la .cqs/slots/$(cat .cqs/active_slot 2>/dev/null || echo default)/ 2>/dev/null
```

The index lives in the active slot: `.cqs/slots/<name>/index.db` plus HNSW sidecars (`index.hnsw*`; legacy pre-slot layouts kept files at `.cqs/` top level). If missing: `cqs init && cqs index`.

### 3. Is the index populated?

Run `cqs stats`. Check:
- Chunk count > 0
- Last update is recent
- Expected languages are present

If empty: `cqs index` to rebuild.

### 4. Schema version mismatch?

```bash
cqs stats 2>&1
```

If you see "SchemaMismatch" or "SchemaNewerThanCq":
- **Older schema**: Run `/migrate` to upgrade
- **Newer schema**: Update cqs binary to latest version

Current schema version: check `src/store/helpers/mod.rs` for `CURRENT_SCHEMA_VERSION`.

### 5. Model downloaded?

```bash
cqs doctor   # checks model, index, hardware in one pass
ls -la ~/.cache/huggingface/hub/models--onnx-community--embeddinggemma-300m-ONNX/
```

Default model is EmbeddingGemma-300m (since v1.35.0); alternative presets via `CQS_EMBEDDING_MODEL` / `--model` live under their own `models--*` dirs. If missing or incomplete, cqs downloads on first use. Check network access to huggingface.co.
If corrupted: delete the directory and let cqs re-download (blake3 checksums verify integrity).

### 6. Daemon mode working?

```bash
cqs ping
systemctl --user status cqs-watch
```

`cqs ping` should report a connected daemon and a sub-100ms round-trip. Common issues:
- Daemon not running: `systemctl --user start cqs-watch` (or `cqs watch --serve` ad hoc)
- Stale socket from a crash: `systemctl --user restart cqs-watch`
- Want to bypass the daemon for one command: `CQS_NO_DAEMON=1 cqs <cmd>`
- LLM enrichment failing: check `ANTHROPIC_API_KEY` is set (see `SECURITY.md`)

### 7. Index stale?

Compare `cqs stats` last update time vs recent file modifications.
Fix: `cqs index` (one-time) or `cqs watch` (continuous).

### 8. References broken?

```bash
cqs ref list
```

Check that source paths still exist and chunk counts are > 0.
If source moved: `cqs ref remove <name>` and re-add with new path.

## Report

After running checks, summarize:
- What was checked
- What failed (if anything)
- What was fixed or needs fixing

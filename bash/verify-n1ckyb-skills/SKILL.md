---
name: verify
description: Run the OpenDataSuite quality gate (cargo fmt, clippy -D warnings, tests, cargo-deny, docs link sanity) and report pass/fail with evidence. Use before committing, before claiming a task is done, and when CI fails.
---

# Verify

Run from repo root. Stop at the first failing stage, fix, and re-run from that stage.

```bash
test -f Cargo.toml || { echo "no Cargo workspace yet — only docs checks apply"; }
cargo fmt --all --check
cargo clippy --workspace --all-targets --all-features -- -D warnings
cargo test --workspace --all-features
cargo deny check 2>/dev/null || echo "cargo-deny not installed (install: cargo install cargo-deny --locked)"
RUSTDOCFLAGS="-D warnings" cargo doc --workspace --no-deps
python3 scripts/check-layering.py
python3 scripts/check-vendor-neutral.py --self-test && python3 scripts/check-vendor-neutral.py
```

Additional checks when relevant:
- Changed `.github/*.json` → `jq empty .github/*.json`.
- Changed `scripts/*.sh` → `bash -n` on each, and `shellcheck` if available.
- Changed CLI output → review `insta` snapshot diffs (`cargo insta review`); never blindly accept.
- Changed persisted formats → a round-trip/serialization test exists and `schema_version` was bumped if incompatible.

Report: a short table of stage → pass/fail, and the exact failing output for anything red.
Never report success for a stage you skipped; say it was skipped and why.

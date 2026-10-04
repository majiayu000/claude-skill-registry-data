---
name: dsh-setup
description: "Install DSH on a fresh Mac. Runs sovereign-setup-mac.sh, renders .env from secrets backend, applies full sovereign lockdown, probes machine, and pulls right-sized Ollama models — one guided flow that leaves the node hardened and ready for Phase-2 spore.sh activation."
---

You are bootstrapping a Dome Sovereign Hub (DSH) node on a fresh Apple Silicon Mac. The user has already cloned `garochee33/DSH` to `$HOME/DSH` (or set `$DOME_ROOT`). Your job is to run the end-to-end setup without leaving anything halfway.

## 1. Preflight

Confirm before doing anything destructive:

- `$DOME_ROOT` resolves to a real directory (default: `$HOME/DSH`). If not, stop and ask.
- macOS version is ≥ 13 (`sw_vers -productVersion`). Windows users must run `scripts/sovereign-setup-windows.ps1` instead — bail out.
- `xcode-select -p` returns a path. If not, run `xcode-select --install` and exit — tell the user to re-run after it completes.
- `sudo -v` prompt works (fail early if the user can't authorize).

## 2. Run the base setup

```bash
cd "$DOME_ROOT"
bash scripts/sovereign-setup-mac.sh
```

This is the 20-step Homebrew/pyenv/nvm/VSCode/DB bootstrap. It is idempotent — safe to re-run. Near the end it prompts for an AI-assistant pick; choose based on user preference or skip.

When it finishes, verify:

- `command -v brew && command -v pnpm && command -v pyenv` all print paths.
- `"$DOME_ROOT/.venv/bin/python" --version` reports the version pinned in `$DOME_ROOT/.python-version` (currently Python 3.14.x).
- `cat "$DOME_ROOT/.env"` exists (copied from `.env.example` by the setup script if it wasn't already there).

## 3. Render secrets into .env (if template backend is in use)

If `.env.template` has `{{keychain:...}}` or `{{pass:...}}` markers:

```bash
bash "$DOME_ROOT/scripts/render-env.sh"
```

This replaces markers with values from macOS Keychain (preferred) or `pass` (GPG). Confirm with `head -5 "$DOME_ROOT/.env"` — there should be no `{{...}}` tokens left. If any marker remains, list them for the user to provision before continuing.

## 4. Apply sovereign lockdown

```bash
bash "$DOME_ROOT/scripts/lock-down.sh"           # kill phone-home daemons, pin DNS
bash "$DOME_ROOT/scripts/lock-down-phase2.sh"    # firewall + stealth
bash "$DOME_ROOT/scripts/lock-down-phase3.sh"    # pf anchor for telemetry endpoints
bash "$DOME_ROOT/scripts/lock-down-phase4.sh"    # daemon audit + permanent removal
bash "$DOME_ROOT/scripts/pf-reload.sh"           # reload pf with the anchor
```

Each script will prompt for sudo once and keep the cached credential alive while it runs. If any exits non-zero, STOP — do not proceed to steps 5+ until the lockdown is clean.

## 5. Probe the machine

```bash
"$DOME_ROOT/.venv/bin/python" "$DOME_ROOT/scripts/machine-probe.py"
```

Write-out lands at `agents/core/.mesh/machine.json`. Report the summary line to the user:

```
Apple M5 Pro · 18 cores (6S + 12P) · 48.0 GB RAM · 40+ TOPS NPU · tier=sovereign
```

## 6. Pull right-sized local LLM weights

```bash
bash "$DOME_ROOT/scripts/ollama-init.sh"
```

This reads the tier detected in step 5 and pulls the matching Ollama models. On a `sovereign` tier (≥18 GB RAM) expect `qwen2.5-coder:14b` + `llama3.1:8b` + `nomic-embed-text`. Confirm with `ollama list`.

## 7. Initialize state + ingest KB

```bash
cd "$DOME_ROOT"
source .venv/bin/activate
python3 scripts/register-claude.py    # creates dome.db tables: agents, skills, tools, stack
python3 scripts/ingest.py             # indexes kb/, logs/, docs into ChromaDB
```

After this: `sqlite3 db/dome.db "SELECT COUNT(*) FROM skills"` should return ≥ 8. `python3 -c "import chromadb; print(chromadb.PersistentClient('db/chroma').get_collection('dome-kb').count())"` should return ≥ 1500.

## 8. Verify all protocols

```bash
python3 scripts/pre-spore-verify.py   # expect: 27/27 READY FOR SPORE.SH
bash scripts/audit.sh                 # expect: all green (or documented yellows)
bash scripts/dome-check.sh            # expect: 0 failures on a fresh install
```

If any of the three fails, surface the specific failure and do NOT declare setup complete. Common causes:

- `akashic:write+query` fails → stale `akashic` ChromaDB collection. Fix: delete via `python3 -c "import chromadb; chromadb.PersistentClient('db/chroma').delete_collection('akashic')"` then re-run.
- `dome-check` fails on `SQLite DB missing` → skipped step 7. Go back.
- `audit.sh` fails on `FileVault OFF` → user must enable in System Settings → Privacy & Security. This is not auto-fixable.

## 9. Report

Give the user a single-block status:

```
✅ DSH installed at $DOME_ROOT
✅ Lockdown active — firewall + pf anchor + DNS pinned
✅ Machine: <summary_one_liner output>
✅ KB indexed: <N> chunks in dome-kb
✅ pre-spore-verify: 27/27
Next: run `spore.sh` with a Trinity SPORE_TOKEN to activate Phase 2 (mesh).
```

## Non-negotiables

- Never proceed past a failing step.
- Never commit `.env` or log output from lockdown scripts.
- Never run lockdown steps without explicit user sudo approval (the scripts handle it, but if they error-out silently, STOP).
- If the user has a non-M-series Mac (Intel), warn them — DSH is tested on Apple Silicon; some MPS-specific PyTorch code will not use acceleration.

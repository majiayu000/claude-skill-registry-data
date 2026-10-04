---
name: machine-probe
description: "Tell the user (or an agent) exactly what machine they are on — chip, cores, RAM, NPU TOPS, memory bandwidth, security posture, DSH tier, and the right Ollama model to pull. Refreshes the canonical profile at agents/core/.mesh/machine.json on every call. Reads the result via agents.core.machine — zero re-probing in application code."
---

You are answering self-knowledge questions about the DSH sovereign node. Treat `agents/core/.mesh/machine.json` as the single source of truth and the agents.core.machine module as the canonical accessor.

## 1. Refresh the profile

Always re-probe before answering — state can change (user plugged in a display, upgraded RAM, disabled FileVault):

```bash
"$DOME_ROOT/.venv/bin/python" "$DOME_ROOT/scripts/machine-probe.py"
```

If the venv doesn't exist yet, fall back to system python:

```bash
python3 "$DOME_ROOT/scripts/machine-probe.py"
```

Silent output to the user is fine — only the summary matters downstream.

## 2. Read via the accessor, never re-probe

```python
import sys
sys.path.insert(0, "$DOME_ROOT")
from agents.core.machine import (
    get_profile,        # full dict
    get_tier,           # 'sovereign' | 'guardian' | 'scout' | 'seed' | 'heavy' | 'workstation'
    get_chip_family,    # 'M4 Pro', 'M1', etc. (or None on non-Apple)
    get_ram_gb,         # float
    get_npu_tops,       # float or None
    is_apple_silicon,   # bool
    recommend_local_model,  # 'qwen2.5-coder:14b' etc.
    security_posture,   # compact dict
    summary_one_liner,  # human-readable sentence
)
```

Never shell out to `system_profiler`, `sysctl`, or `ioreg` directly from the answer path — the probe already did that and structured the output.

## 3. Answer patterns

### "What machine am I on?"

Return `summary_one_liner()`. Example:

```
Apple M5 Pro · 18 cores (6S + 12P) · 48.0 GB RAM · 40+ TOPS NPU · tier=sovereign
```

### "What tier am I?"

Return `get_tier()` + a one-line meaning:

- **workstation** (≥64 GB): run the biggest quantized models (70B+)
- **heavy** (≥32 GB): 32B coder + 70B generalist
- **sovereign** (≥18 GB): 14B coder + 8B generalist (recommended default)
- **guardian** (≥12 GB): 8B generalist + medium Phi
- **scout** (≥8 GB): 8B generalist only
- **seed** (<8 GB): 3B Phi-mini

### "What Ollama model should I pull?"

Return `recommend_local_model()` + offer to run `bash scripts/ollama-init.sh` to actually pull it.

### "Is my node secure?"

Return `security_posture()` as a 6-row check:

```
filevault          : True / False
sip                : True / False
gatekeeper         : True / False
firewall           : True / False
dns_private        : True / False
secrets_backend    : True / False
```

For each `False`, suggest the exact fix command (e.g. dns_private=False → `sudo networksetup -setdnsservers Wi-Fi 127.0.0.1`).

### "Give me the full profile"

Return `get_profile()` pretty-printed. If the user requests JSON specifically, use `json.dumps(profile, indent=2)`.

## 4. Via HTTP (remote clients)

If the DSH FastAPI server is running (`pnpm serve`), two routes expose the same data:

- `GET http://localhost:8001/machine/summary` — compact payload (recommended for mobile)
- `GET http://localhost:8001/machine` — full profile

Use these from a remote controller / phone / other node. Returns 503 if profile missing — in that case run step 1 locally first.

## 5. When to re-run

- Before any setup skill (dsh-setup calls this as step 5).
- After any hardware change (new disk, new RAM — rare, but possible on an MBP).
- After security state changes (FileVault toggled, firewall reconfigured).
- On every `dome-check.sh` run (already wired — section 0 refreshes automatically).

## Non-negotiables

- Never invent specs. If `get_profile()` returns `None` for a field, say "unknown" — do not guess.
- Never expose the machine.json contents to a remote caller without auth. The `/machine` routes are read-only and should be behind Tailscale / VPN in production.
- `agents/core/.mesh/` is gitignored. Do not suggest committing the profile.

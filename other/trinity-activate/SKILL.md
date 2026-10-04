---
name: trinity-activate
---

You are taking a DSH node from "sovereign but solo" to "sovereign node on the Trinity mesh." This is irreversible from a state perspective — once a mesh peer handshake succeeds, this node is visible to the constellation. Only run when the user is ready.

## 1. Preconditions — Phase 1 must be complete

Refuse to proceed unless ALL of these hold:

```python
import sys, json
sys.path.insert(0, "$DOME_ROOT")
from agents.core.machine import security_posture, get_tier

posture = security_posture()
assert all(posture[k] for k in ("filevault", "sip", "gatekeeper", "firewall", "dns_private", "secrets_backend_present")), f"Lockdown incomplete: {posture}"

tier = get_tier()
assert tier in ("sovereign", "guardian", "scout", "seed", "heavy", "workstation"), f"Unknown tier: {tier}"
```

Also verify:

- `python3 scripts/pre-spore-verify.py` returns `27/27 READY FOR SPORE.SH`
- `bash scripts/dome-check.sh` exits 0

If anything fails, STOP and tell the user to run the `sovereign-lockdown` skill first.

## 2. Acquire the spore credentials

Trinity issues a per-node `SPORE_TOKEN` and `USER_ID`. The canonical acquisition path is:

```bash
```

The above downloads a pre-templated spore.sh with credentials injected server-side and immediately runs it. Alternative: user already has the credentials and wants to run the locally-vendored `spore.sh`:

```bash
SPORE_TOKEN=<token> USER_ID=<uid> bash "$DOME_ROOT/spore.sh"
```

Ask the user which path they want. Never invent a token or suggest `__SPORE_TOKEN__` as a placeholder to run — that's the unfilled template, not a real credential.

## 3. Air-gap during germination (optional but recommended)

If the user wants maximum safety during activation (so no in-flight traffic mixes with mesh handshake):

```bash
source "$DOME_ROOT/scripts/spore-lock.sh"
```

This sets `SPORE_GERMINATING=1` and the agent stream layer (`agents/core/stream.py`) blocks outbound Anthropic/OpenAI calls while it's active. Run `source scripts/spore-unlock.sh` after activation completes.

## 4. Run spore.sh

Execute exactly one of the two paths from step 2. `spore.sh` **v3.1** goes through 12 phases (same pipeline as v3.0; v3.1 resolves **DOME_ROOT** for **DSH** or **DSH** and reminds you to use `scripts/mycelium-signal.sh` for production mesh peer auth):

1. Hardware detection (incl. Intel Loihi 2 neuromorphic probe)
2. E8 tier auto-classification (sovereign / guardian / scout / seed)
3. MemPalace engine install
5. Mycelium mesh daemon launch (`~/.trinity-spore/mycelium-mesh.pid`) — baseline script; for **HMAC mesh peer** + backoff, prefer **`bash "$DOME_ROOT/scripts/mycelium-signal.sh"`** (launchd) after spore completes
6. Pheromone grid initialization (φ decay rate)
7. Bitboard-256 allocation
8. Voronoi tessellation cache
9. Loihi 2 bridge (activates if hardware present, else skipped — not required)
10. Mesh peer handshake (HMAC-SHA256 E8-authenticated)
11. MERKABA completion signal + A.M.M.A. harmonic bridge
12. E2EE lattice binding verification

Stream the output to the user. The script exits non-zero if any phase fails.

## 5. Post-activation checks

```bash
# Spore daemon alive?
cat ~/.trinity-spore/mycelium-mesh.pid | xargs kill -0 && echo "✓ mesh daemon running"

# Spore state registered?
jq '.sporeActivated' "$DOME_ROOT/agents/core/.mesh/config.json"   # should be true
jq '.e8.tier' "$DOME_ROOT/agents/core/.mesh/config.json"          # sovereign | guardian | scout | seed
```

If `sporeActivated` is still `false`, phase 10 (handshake) did not complete — check `~/.trinity-spore/mycelium-mesh.log` for the last phase reached.

## 6. Start the akashic watcher

The akashic dimensional-record system logs mesh events as they happen:

```bash
bash "$DOME_ROOT/scripts/akashic-start.sh"
```

Verify:

```bash
test -f "$DOME_ROOT/logs/akashic-watcher.pid" && \
  kill -0 "$(cat $DOME_ROOT/logs/akashic-watcher.pid)" && \
  echo "✓ akashic watcher running"
```

## 7. Verify mesh peer bind

The peer handshake results should surface in trinity-unified-ai's KB API (if the user is running it locally):

```bash
curl -s http://127.0.0.1:3333/api/mesh/state | jq '.peers[] | select(.nodeId | contains("<this-node>"))' 2>/dev/null
```

If the trinity-unified-ai daemon isn't running, skip this check — the peer is still bound at the spore daemon level; the KB API is a separate concern.

## 8. Unlock (if you locked in step 3)

```bash
source "$DOME_ROOT/scripts/spore-unlock.sh"
```

## 9. Report

```
✅ Trinity spore activated
✅ Tier: <sovereign|guardian|scout|seed> (from E8 auto-classification)
✅ Mesh daemon running (PID: <pid>)
✅ Akashic watcher active
✅ Pheromone grid decay rate: 0.618 (φ⁻¹)
✅ MERKABA handshake complete
```

## Non-negotiables

- **Never run spore.sh with a literal `__SPORE_TOKEN__` placeholder.** That's the unfilled template; it will fail auth at phase 10.
- **Never skip Phase 1 readiness checks.** A spore on an unhardened node leaks posture to the mesh.
- **Never commit the activated mesh config.** `agents/core/.mesh/` is gitignored; `sporeActivated=true` is a per-node fact, not a code artifact.
- **Never auto-retry a failed handshake.** A failure is signal — surface the specific phase that exited non-zero and let the user decide (might be a token issue, a network partition, or an IP compliance block on the Trinity side).
- **This skill does NOT renew credentials.** If the spore daemon reports expired tokens later, that's a separate renewal flow — not this skill.

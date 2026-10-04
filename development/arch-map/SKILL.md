---
name: arch-map
description: Render/refresh the project RACI + C4 component map (ADR-001 INTENT) — the canonical who-owns-what + boundary-contracts map. Seeds docs/architecture/raci-component-map.md from the template if missing; regenerates the Mermaid component diagram from the curated RACI. Detailed class/sequence UML is derived from the code-graph engine (Phase 2, via /codegram). Use at decomposition to consult ownership + prevent duplicated logic before firing teams.
allowed-tools: Bash(*) Read Write
argument-hint: [--seed]
---

# Arch map: $ARGUMENTS

The INTENT layer of ADR-001. Hand-curated + ADR-gated; this skill seeds + renders it, it does not invent ownership.

## Run

```!
set -uo pipefail
ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
MAP="$ROOT/docs/architecture/raci-component-map.md"
TPL="$ROOT/docs/architecture/_templates/raci-component-map.md"
if [ ! -f "$MAP" ]; then
  if [ -f "$TPL" ]; then mkdir -p "$ROOT/docs/architecture"; cp "$TPL" "$MAP"; echo "seeded $MAP from template — curate it (one row per repo, the forbidden-import column)."; else echo "ERROR: template $TPL missing"; fi
else
  echo "RACI/component map present: $MAP"
fi
echo ""
echo "Per-repo lane-rules present:"
if [ -f "$ROOT/.cto/projects.yaml" ]; then
  python3 - "$ROOT/.cto/projects.yaml" <<'PY' | while IFS= read -r p; do [ -d "$p" ] || continue; if [ -f "$p/docs/architecture/lane-rules.txt" ]; then echo "  [x] $(basename "$p")"; else echo "  [ ] $(basename "$p") — no lane-rules.txt (declare forbidden imports)"; fi; done
import re,sys
t=open(sys.argv[1]).read()
for b in re.split(r'(?=- name:)',t):
    p=re.search(r'path:\s*(\S+)',b); a=re.search(r'active:\s*(\S+)',b)
    if p and ((a is None) or a.group(1).lower() not in ('false','no','0')): print(p.group(1))
PY
fi
```

## Your task as CTO

1. If the map was just seeded, **curate it** — one row per repo: its lane, what it owns, the contracts it exposes/consumes, and its **forbidden cross-lane imports** (this column seeds each repo's `lane-rules.txt`).
2. **(Re)render the component diagram** in the map's Mermaid block from the current RACI rows.
3. **Consult it at decomposition** to prevent dupes/lane-drift before firing teams.
4. For **detailed per-repo UML**, delegate to **VP-Eng** (it generates a repo's UML from the AST on initiation) — do not hand-draw. The fleet-wide derived UML + cross-repo navigation come from the code-graph engine via `/codegram` (Phase 2).

Sign `— CTO`.

---
name: prd-list
description: >
  Use when the user asks which PRDs exist — 'listar PRDs', 'quais PRDs temos', 'list PRDs' —
  with status, version, roadmap state and GitHub Project. Read-only.
metadata:
  version: 3.0.0
---

# List PRDs

## STEP 0 — Language
Follow `<plugin-root>/references/language.md` (resolve `lang` from
`.planning/config.json`; ask only if unset).

## Procedure

```bash
echo "=== PRDs ==="
for dir in .planning/prds/*/; do
  [ -d "$dir" ] || continue
  slug=$(basename "$dir")
  md="$dir/PRD.md"
  status=$(grep -m1 -E '^Status:' "$md" 2>/dev/null | sed 's/Status:[[:space:]]*//'); status=${status:-DRAFT}
  version=$(grep -m1 -E '^Version:' "$md" 2>/dev/null | sed 's/Version:[[:space:]]*//'); version=${version:-—}
  has_json=$([ -f "$dir/prd.json" ] && echo "✅" || echo "—")
  roadmap=$(head -1 "$dir/roadmap/ROADMAP.md" 2>/dev/null | sed 's/Roadmap:[[:space:]]*//;s/ .*//'); roadmap=${roadmap:-—}
  project=$(sed -n 's/.*"project_url"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' ".planning/github/$slug.map.json" 2>/dev/null | head -1); project=${project:-—}
  stories=$(python3 "<plugin-root>/scripts/roadmap-check.py" "$dir/roadmap/roadmap.json" --json --no-write 2>/dev/null | python3 -c 'import json,sys; s=json.load(sys.stdin)["stories"]; print("%d/%d ready" % (s["ready"], s["total"]))' 2>/dev/null); stories=${stories:-—}
  echo "$slug | $status | $version | JSON: $has_json | Roadmap: $roadmap | Stories: $stories | GitHub: $project"
done
ls -d .planning/prds/*/ >/dev/null 2>&1 || echo "No PRDs found. Run /pwdev-prd:create to start."
```

Present:
```
📋 PRDs in .planning/prds/

| PRD | Status | Version | JSON | Roadmap | Stories | GitHub Project |
|-----|--------|---------|:----:|---------|---------|----------------|
| user-auth | APPROVED | 1.2.0 | ✅ | APPROVED | 5/7 ready | https://github.com/users/me/projects/7 |
| inventory | DRAFT | 1.0.0 | — | — | — | — |

Total: {N} PRDs

👉 /pwdev-prd:create "desc"    → New PRD
👉 /pwdev-prd:refine {slug}    → Update existing
👉 /pwdev-prd:roadmap {slug}   → Roadmap with dependency chain (APPROVED PRDs)
👉 /pwdev-prd:publish {slug}   → GitHub Project + issues (approved roadmap)
```

Language: resolve `lang` per `references/language.md` before any human-facing output. Paths `<plugin-root>/...`, `references/`, `scripts/`, `templates/` are relative to the plugin root; tool names, subagent dispatch and the command form to show the user depend on the runtime (`references/runtime.md`).

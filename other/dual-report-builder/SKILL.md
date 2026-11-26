---
name: dual-report-builder
description: Generates TWO versions of the same analysis/report — INTERNAL (raw, failures exposed, dark) and EXTERNAL (premium, positive, no failures exposed, light) — as self-contained HTML with pure-CSS charts, print-friendly. The external version goes through a sober-register gate (banned phrases from the profile). Use when producing a report/dashboard with a dual audience (internal team + client/stakeholder).
type: skill
---

> **Auto-Trigger:** When the user asks for a report/dashboard that will be seen both by the internal team and by a client/stakeholder; when they mention "internal and external version", "report to show the client", "internal dashboard", "two versions", "accountability report", or ask for a report after a bulk generation/audit task.
> **Keywords:** "dual report", "internal version", "external version", "internal and external", "client dashboard", "internal dashboard", "two versions", "premium report", "accountability report", "report for the client", "before/after"
> **Priority:** MEDIUM
> **Tools:** Read, Write, Glob, Grep
> **Related doctrine:** `rules/agent-integrity.md` (the external version omits failure, never fabricates success), `rules/learned-corrections.md` (LC-1: traceable numbers).

## When NOT to Activate

- SINGLE-audience report (internal only OR client only) — generate one version only, without the overhead of two.
- Request for a raw datum/one-off number ("how many X?") — use `status_now.py` or `delta_inventory.py` directly.
- Building the visual/CSS engine from scratch — the design belongs to a dedicated frontend/design skill, if you have one installed; this skill orchestrates the PROCESS of the two versions, it does not reimplement layout.
- Sending to the client — this skill PRODUCES the two artifacts; the external send is a human gate (operator approval), never automatic.

---

# dual-report-builder — Internal (raw) + External (premium) from the SAME analysis

A client report has two versions: **internal version (unfiltered, raw data)** + **external version (positive results, without exposing internal failures)**. This skill describes the process of producing BOTH from a single analysis — same source numbers, different cuts — and of submitting the external one to a sober-register gate before declaring it ready.

**Principle:** the analysis (the facts/numbers) is ONE. The two versions differ in the CUT and the TONE, never in the numbers. No inventing positive data for the external version (AGENT-INTEGRITY). The external version OMITS failures; it never FABRICATES success.

## Contract

**INPUT:** the single analysis (traceable facts/numbers, LC-1) + `report.*`/`paths.draft_dir` from `operator-profile.yaml`.

**OUTPUT:** 2 self-contained HTML artifacts — internal (complete, dark) in the project logs + external (premium, light) in `paths.draft_dir` as a DRAFT.

**EXIT CODES** (from the sober-register gate, step 4 — the banned-phrase sweep):

| Exit | Meaning |
|---|---|
| 0 | external text clean — no banned phrase found, may be declared "ready for review" |
| 1 | >=1 banned phrase found — rewrite the passage and sweep again, do NOT declare ready |

**STATE IT TOUCHES:**

| Resource | Reads/Writes | Purpose |
|---|---|---|
| `operator-profile.yaml` (`report.*`, `paths.draft_dir`) | Reads | themes, banned phrases, draft destination |
| project logs (internal version) | Writes | complete, unfiltered report |
| `paths.draft_dir` (external version) | Writes | draft — sending is a human gate |

## Parameters (read from operator-profile.yaml)

Read them via the kit loader (`_lib/profile_loader.get(profile, "report.X")`):

| Key | Use |
|-------|-----|
| `report.internal_style` (e.g. `dark`) | visual theme of the internal version |
| `report.external_style` (e.g. `light`) | visual theme of the external (premium) version |
| `report.banned_phrases` (list) | terms FORBIDDEN in the external version — sober-register gate |
| `paths.draft_dir` | where to write the external version (draft, until the operator releases it) |
| `language` | content language (default pt-BR) |

Without a profile → safe defaults: internal=dark, external=light, banned_phrases=`[]` (the gate becomes a no-op but the dual structure stays), draft in `drafts/`.

## Pipeline

```
STEP 0 — SCOPE + SOURCES
  -> Define what the report is (client/project/window) and the dual audience.
  -> Gather the source numbers ONCE. Each number traceable to a real source (LC-1):
     counts via delta_inventory.py, state via status_now.py, metrics via MCP/file.
     A number without a source does NOT go in (not even in the internal version).

STEP 1 — SINGLE ANALYSIS (the raw truth)
  -> List EVERYTHING: what went well, what failed, bottlenecks, debts, risks, gaps.
  -> This is the raw material of both versions.

STEP 2 — INTERNAL VERSION (theme = report.internal_style)
  -> Everything from the analysis, UNFILTERED: failures exposed, raw numbers, open items,
     before/after/delta table (delta_inventory.py), honest next steps.
  -> Audience: team/operator. Direct, flat tone (see the direct-register output style).
  -> Write to the project's logs/internal report.

STEP 3 — EXTERNAL VERSION (theme = report.external_style, premium)
  -> Same source numbers; cut on the POSITIVE RESULTS and next steps.
  -> OMIT internal failures/bottlenecks/debts (do not expose the kitchen) — but NEVER invent
     a gain that does not exist. If there was no real positive result, say what IS in
     progress, without embellishment.
  -> SOBER corporate register.
  -> Write to paths.draft_dir as a DRAFT (sending = human gate).

STEP 4 — EXTERNAL GATE (sober register)
  -> Sweep the external text against report.banned_phrases (case-insensitive).
  -> If ANY banned phrase is found -> rewrite the passage and sweep again. Only declare
     the external version "ready for review" when it passes clean.
  -> This gate enforces the sober register the external version must keep.

STEP 4b — CITATION GATE (requires the HPP core, `python -m hpp`)
  -> In the external draft, mark each number with the id of the step-0 source it came from:
     `[ID:<source id>]` (or pass `--marker` with a regex for your own marker format).
  -> Export the step-0 sources as sources.json: [{"id": "...", "text": "..."}].
  -> python -m hpp cite check --text external.md --context sources.json
     exit 2 = a marker names a source that was never collected -> fix the marker or the source.
     exit 1 = a quantitative sentence with no marker (or too many markers in one sentence)
              -> the report is NOT ready: cite the number or cut it.
     exit 0 = every marker resolves. It does not prove the source says what the sentence says.

STEP 5 — DELIVERY
  -> Report the two paths (internal + external draft) and that the external version AWAITS
     the operator's release before sending. Never send directly.
```

## Visual patterns (delegated to a design skill)

This skill does NOT reimplement CSS. When assembling the HTML, follow these dashboard rules (and use a frontend/design skill, if you have one, for the finish):

- **Self-contained** HTML (no external JS libs; Google Fonts CDN ok).
- **Pure-CSS** charts: `conic-gradient` (pie/gauge), bars by `width`, SVG gauge. **No Chart.js/D3.**
- **Internal = dark**, **external = light/premium** (from the profile).
- **Print-friendly**: `@media print` in both.
- **Before/after/delta** comparison table (preference recorded in the profile) — fed by `delta_inventory.py`.

## Sober-register gate (sketch of the mechanism)

The banned-phrase sweep reuses the profile; it does not reimplement config:

```python
import os, sys
from pathlib import Path
# ${CLAUDE_PLUGIN_ROOT} in plugin mode; otherwise go up 2 levels (skills/<name>/ -> skills/ -> operator-kit/)
# parents[2], not parents[1]: parents[1] resolves to .../skills (off by one).
_plugin_root = os.environ.get("CLAUDE_PLUGIN_ROOT")
_kit_root = Path(_plugin_root) if _plugin_root else Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_kit_root))
from _lib.profile_loader import load_profile, get

prof = load_profile()
banidas = [f.lower() for f in (get(prof, "report.banned_phrases", []) or [])]
texto_externo = "..."  # content of the external version
ofensas = [f for f in banidas if f and f in texto_externo.lower()]
# ofensas != [] -> rewrite the passages and sweep again BEFORE declaring ready.
```

## Exit checklist

```
[ ] Source numbers collected ONCE, each one traceable (LC-1)?
[ ] INTERNAL version exposes failures/bottlenecks/debts (internal theme from the profile)?
[ ] EXTERNAL version omits failures WITHOUT inventing success (external theme from the profile)?
[ ] Before/after/delta table present (delta_inventory.py)?
[ ] Self-contained HTML, pure-CSS charts, print-friendly?
[ ] External version swept against report.banned_phrases and passed clean?
[ ] `hpp cite check` over the external draft exited 0 (every number cited, every marker resolves)?
[ ] External version written to draft_dir as a DRAFT; sending flagged as a human gate?
```

## Executed examples

```console
$ python -c "
import os, sys
from pathlib import Path
_kit_root = Path(os.environ.get('CLAUDE_PLUGIN_ROOT') or Path.cwd())
sys.path.insert(0, str(_kit_root))
from _lib.profile_loader import load_profile, get
prof = load_profile()
print('kit_root aponta pro operator-kit?', (_kit_root / 'operator-profile.yaml').exists())
print('banned_phrases:', [f.lower() for f in (get(prof, 'report.banned_phrases', []) or [])])
"
kit_root aponta pro operator-kit? True
banned_phrases: ['consider it done', 'com certeza!', 'ótima pergunta']
```
<!-- executed: 2026-09-24 · exit=0 -->
(proves `parents[2]` really resolves to `operator-kit/` — `operator-profile.yaml` exists there.)

```console
$ python -c "
banidas = ['consider it done', 'com certeza!', 'risco']
text = 'O deploy foi tranquilo, consider it done, zero risco daqui pra frente.'
ofensas = [f for f in banidas if f in text.lower()]
print('ofensas encontradas:', ofensas)
import sys; sys.exit(1 if ofensas else 0)
"
ofensas encontradas: ['consider it done', 'risco']
```
<!-- executed: 2026-10-30 · exit=1 -->
(step 4 — the gate BLOCKS: 2 banned phrases in the external draft; rewrite and sweep again BEFORE declaring ready.)

```console
$ python -c "
banidas = ['consider it done', 'com certeza!', 'risco']
text = 'O deploy concluiu com os 3 checks passando; monitoramento segue ativo nas proximas 24h.'
ofensas = [f for f in banidas if f in text.lower()]
print('ofensas encontradas:', ofensas)
import sys; sys.exit(1 if ofensas else 0)
"
ofensas encontradas: []
```
<!-- executed: 2026-10-30 · exit=0 -->
(the same text rewritten in a sober register — the gate passes clean, it may be declared "ready for review".)

```console
$ cat external.md
Leads grew to 412 in August [ID:crm-export]. Sessions reached 9,120.
$ python -m hpp cite check --text external.md --context sources.json
{
  ...
  "exit_code": 1,
  "findings": [
    {
      "code": "UNCITED_CLAIM",
      "excerpt": "Sessions reached 9,120.",
      ...
      "message": "quantitative claim '9,120' carries no citation",
      ...
    }
  ],
  ...
  "verdict": "warn"
}
```
<!-- executed: 2026-09-24 · exit=1 -->
(step 4b — `sources.json` lists `crm-export` and `ga4`; the second number has no marker, so the report is not ready. With `[ID:ga4]` after it, the same command exits 0.)

## Proof

```bash
python -c "
banidas = ['risco']; text = 'monitoramento ativo nas proximas 24h'
import sys; sys.exit(1 if any(b in text.lower() for b in banidas) else 0)
"
```

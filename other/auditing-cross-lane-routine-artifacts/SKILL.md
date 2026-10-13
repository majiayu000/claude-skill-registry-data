---
name: auditing-cross-lane-routine-artifacts
description: >
  Adversarially audits multi-routine automation artifacts (cron/API routine
  libraries, scheduled-task decks, "routine cards") for cross-lane
  contamination, scheduled-task governance violations, and the
  structurally-empty-at-runtime defect — then splits them into lane-clean
  artifacts and rebuilds them from a single-source generator. Use whenever Kyle
  hands over a routine/automation artifact and says "audit this", "fresh
  adversarial pass", "keep them lane-specific", "make these lane-clean",
  "split by lane", "apply all fixes", or "rebuild the artifact" — even if he
  doesn't say "lane" or "governance". Also triggers on: routine cards audit,
  cron library review, automation deck audit, scheduled-task governance check,
  Loxihart vs FlashFusion bleed, lane contamination, n8n tenant collision,
  pipeline-vs-recognized-revenue, data-source guard, count-bug, generator
  rebuild, lane separation. PERSONAL/Loxihart context. NOT for app/codebase security
  audits (use code-auditor) and NOT for building a single new routine.
metadata:
  version: "1.0.0"
---

# Auditing Cross-Lane Routine Artifacts

Catches the four failure classes that recur in Kyle's routine/automation
artifacts — lane bleed, scheduled-write governance, runtime-empty routines, and
count drift — then rebuilds the artifact into lane-separated HTML from one
Python generator so the data is single-source and verifiable.

## TL;DR

Most "routine library" artifacts mix LOXIHART and PERSONAL lanes, schedule writes
to shared services, and contain cron jobs that read "today's session" in a fresh
context that has no session. Audit for those four things first; if Loxihart routines
are present in a PERSONAL artifact, **extract them to a separate reference-only
Loxihart artifact** — Loxihart is SOC 2 / ISO aligned and Cowork is not in audit logs.

---

## Decision Tree

```
Handed a multi-routine artifact?
  ├─ Read it fully first (the data array, not just the header). Count the
  │   ACTUAL entries — header counts are often stale (see Gotcha #1).
  └─ Run the 4-axis audit below.

AXIS 1 — Lane bleed
  ├─ Any routine that names/gates an Loxihart deploy, Loxihart velocity, Loxihart isolation?
  │     → EXTRACT to a separate Loxihart-lane artifact (reference-only).
  ├─ Any cross-connector routine (morning brief, follow-up scanner, repo audit,
  │   retro) with NO lane filter?  → add hard lane scope + "Unscoped — review".
  ├─ Any routine that aggregates lanes then "masks externally"? → that's still
  │   bleed; split the data, don't mask it.
  └─ Shared infra (one n8n tenant / one PROJECT_STATE file) across lanes?
        → flag as a DECISION for Kyle; make routines read-only + lane-noted.

AXIS 2 — Scheduled-task governance (CLAUDE.md rule)
  └─ Any CRON routine that writes to a shared service (Notion/Drive/CRM),
     sends messages, or touches secrets?
        → downgrade to draft-for-review + explicit confirm + first-3-runs hold.

AXIS 3 — Runtime data-source reality
  └─ Any routine that "reads today's conversation / memory edits / session
     count" but runs on a cron (fresh context)?
        → add a DATA-SOURCE GUARD that fails safe ("source unavailable"),
          never fabricates a result.

AXIS 4 — Integrity / correctness
  ├─ Header count == actual array length?  (almost never — recount)
  ├─ Revenue figures labeled recognized vs pipeline?
  ├─ Cron schedule collisions (same minute)?  → stagger.
  └─ Inflated claims (title, "240+ tools")?  → correct to verified values.

Rebuild?
  └─ Author ONE Python generator → emit one HTML per lane → verify in code →
     present files + changelog.
```

---

## Usage Examples

**Example 1 — "Audit it myself as a fresh adversarial pass; keep them lane-specific."**
→ Read the full data array. Find Loxihart routines living inside a FlashFusion
(PERSONAL) artifact, unfiltered cross-connector routines, cron-scheduled Notion
writes, and "read today's session" routines. Deliver a ranked audit with
[SOURCED]/[GENERATED] footers and the shared-n8n-tenant decision flagged.

**Example 2 — "all" (apply every fix).**
→ Extract Loxihart routines to a reference-only Loxihart artifact; lane-filter the
cross-connector routines; gate the scheduled writes; add data-source guards;
stagger schedule collisions; fix the count bug; rebuild both via a single
generator; verify counts + lane-leak in code; present with a per-change changelog.

**Example 3 — "rebuild the routine deck and fix the counts."**
→ Author the generator, inject routine data as `json.dumps`, compute all stats
from `ROUTINES.length` (never hardcode), emit the HTML, and run the verification
script to prove no collisions and no lane leakage.

---

## The Four Failure Classes (what to look for)

| Class | Tell | Fix |
|---|---|---|
| Lane bleed | Loxihart routine in a PERSONAL artifact; connector pull with no lane filter; "aggregate then mask" | Extract Loxihart → own artifact; add lane scope + Unscoped bucket; split data |
| Scheduled-write governance | a CRON routine that writes Notion/Drive/CRM | draft-for-review + confirm + first-3-runs hold |
| Runtime-empty | cron job "reviews today's conversation / reads memory edits / session count" | data-source guard that fails safe |
| Integrity drift | header says 20, array has 40; "Won" deal shown as revenue; two crons same minute; ~30/240+ tool counts | recount dynamically; label pipeline vs recognized; stagger; correct to ~40 verified |

**Lane law (from CLAUDE.md):** LOXIHART / PERSONAL / FREELANCE are strictly
isolated. Loxihart is SOC 2 / ISO 27001 aligned and **Cowork activity is NOT in audit
logs** — so extracted Loxihart artifacts are *reference specs*, not Cowork runtimes.
Mark them loudly.

---

## Instruction-Block Patterns (paste into the routines you fix)

**Lane-scope header** (for any cross-connector routine):
```
LANE SCOPE (NON-NEGOTIABLE): PERSONAL lane only — FlashFusion, ChaosClubCo,
memoir, [PERSON]. Do NOT pull, read, surface, or mix any LOXIHART source. Filter
every connector step by PERSONAL-lane labels/projects. If a record's lane cannot
be determined, exclude it and list it once under "Unscoped — review". Never
merge Loxihart and PERSONAL items into one list.
```

**Scheduled-write gate** (for any CRON that wrote to a shared service):
```
GOVERNANCE: scheduled task — do NOT silently write to a shared service. Produce
output for review; write only on explicit confirmation. First 3 runs: surface
for manual review, no write. End with: "Reply 'save X' to write to <DB>."
```

**Data-source guard** (for any "reads today's session/memory" routine):
```
DATA-SOURCE GUARD: a scheduled run starts in a FRESH context and does NOT
automatically contain today's conversation/memory. Confirm a source is available
(a session/transcript/memory tool returns data, or it was passed in). If NONE is
available, STOP and output: "<Routine> — [Date]: NO SOURCE AVAILABLE. Cannot
evaluate." Do not invent a result.
```

**Revenue-integrity line** (for any pipeline/revenue routine):
```
REVENUE INTEGRITY: CRM stage changes are PIPELINE, not recognized revenue. A
"Won" deal is not a paid invoice. Label every dollar figure [recognized — invoice
paid] or [pipeline — estimated]. Never present pipeline as recognized revenue.
```

---

## Single-Source Generator Pattern

Build ONE Python generator that holds corrected data and emits one HTML per lane.
This kills the escaping/transcription bugs of hand-editing a 1500-line file and
makes counts truthful.

```python
import json
# 1) CSS as one raw block with a placeholder the per-lane override fills:
CSS = r"""... :root{...} __ACCENT_OVERRIDE__ ..."""   # override block AFTER :root wins the cascade
# 2) Template with placeholders; inject data as JSON (no template-literal escaping):
#    const ROUTINES = __ROUTINES_JSON__;  const AUDIT = __AUDIT_JSON__;
# 3) Counts are DYNAMIC — never hardcode:
#    total = ROUTINES.length; cron = ROUTINES.filter(r=>r.type==='CRON').length; ...
#    results-count: `${data.length} of ${ROUTINES.length}`
def build(path, ..., routines, audit, accent_override=""):
    html = TEMPLATE.replace("__CSS__", CSS.replace("__ACCENT_OVERRIDE__", accent_override))
    html = html.replace("__ROUTINES_JSON__", json.dumps(routines))
    html = html.replace("__AUDIT_JSON__", json.dumps(audit))
    open(path,"w").write(html)
```

Routine record shape: `{type:"CRON"|"API", n, title, trigger, u, t, k(bool, Kyle-scoped), rank, instructions}`.
HTML-escape `title/trigger/rank/instructions` in the renderer (`&`,`<`,`>`) since
data now arrives as JSON, not pre-escaped HTML.

**Loxihart de-branding** — pass an accent override so the Loxihart artifact is visibly NOT
FlashFusion purple:
```python
INT_ACCENT = """:root{ --surface-base:#0B1220; --accent-primary:#64748B;
  --gradient-accent:linear-gradient(90deg,#475569 0%,#64748B 55%,#0EA5E9 100%);
  --border-primary:rgba(100,116,139,0.25); --border-active:rgba(100,116,139,0.5); }"""
```

---

## Verification Script (run before presenting)

```python
import re, json
from collections import Counter
h = open("routine-cards-personal.html").read()
pr = json.loads(re.search(r'const ROUTINES = (\[.*?\]);\nconst AUDIT', h, re.S).group(1))
# counts truthful?
print(len(pr), sum(1 for r in pr if r['type']=='CRON'), sum(1 for r in pr if r['type']=='API'))
print("hardcoded 'of 20':", "of 20" in h)                       # must be False
# schedule collisions?
print({k:v for k,v in Counter(r['trigger'] for r in pr if r['type']=='CRON').items() if v>1} or "NONE")
# lane leak — Loxihart routine titles must NOT appear in PERSONAL:
leak = [r['title'] for r in pr if r['title'] in {"Skills Library Compliance Check","Loxihart Lane Isolation Check"}]
print("leak:", leak or "NONE")
```
Confirm: counts match data, no `of 20` hardcode, no cron collisions, no Loxihart
titles in PERSONAL, Loxihart file applies the slate accent (`#64748B`) and carries a
"do not run in Cowork" banner (≥2 mentions).

---

## Gotchas

1. **Header counts lie — recount the array.** The source artifact claimed "20
   routines / 10 cron / 10 API" but the data array had 40 (a "20 NEW WORKFLOWS"
   block was appended without updating the hardcoded stats or the `X of 20`
   results line). Always count `ROUTINES.length` and make every stat dynamic.

2. **"Aggregate then mask" is still lane bleed.** A routine that pulls Loxihart +
   PERSONAL into one report and then says "don't surface Loxihart externally" already
   commingled the lanes in context. The fix is to split the data source, not to
   mask the output.

3. **Cron jobs can't see "today's session."** Routines like a nightly sycophancy
   check, a memory-drift audit, or a pattern-interrupt assume access to the
   conversation transcript / `userMemories` / session count. A scheduled run is
   a fresh context with none of that. Without a guard they emit hollow output.
   Add the data-source guard; fail safe.

4. **Loxihart routines must never execute in Cowork.** Loxihart is SOC 2 / ISO 27001
   aligned; Cowork activity is not captured in audit logs. Extracted Loxihart
   artifacts are reference specs only — banner them in red and say so.

5. **Shared infra across lanes is a decision, not a code fix.** `krosebrook.app.
   n8n.cloud` is claimed by LOXIHART in CLAUDE.md but used by FlashFusion routines;
   a single PROJECT_STATE.md holds all lanes. You can't resolve tenancy by
   editing instructions — flag it for Kyle and make the routines read-only + lane-noted.

6. **Python triple-quoted string ending in a quote = `SyntaxError`.** Instruction
   text ending in `"` immediately before the closing `"""` produces `""""`
   (unterminated string). Fix: insert a space — `sed -i 's/"""")/" """)/g'`.
   Inject data via `json.dumps` to avoid the whole escaping class.

7. **Edit/Write use the Windows mount; bash uses `/sessions/...`.** The Edit tool
   failed with a `/sessions/...mnt/outputs` path ("File does not exist"). Use the
   `C:\...\outputs\...` path for Read/Write/Edit, OR patch the file from bash
   (sed/python). They point at the same dir via different mounts.

8. **Pasted-inline source can't be true-diffed.** When the artifact arrives as
   chat content (not a file on disk), Kyle's str_replace rule can't be honored
   literally — author the corrected file + a per-change changelog instead, and
   flag that you did so. (If a saved original exists, diff against it.)

9. **De-branding leaves residual chrome.** Overriding CSS variables re-skins the
   header/gradient, but hardcoded `rgba(168,85,247,...)` in micro-elements
   (button hovers) stays purple. Cosmetic, not lane logic — note it, offer full
   de-purple if asked.

---

## Self-Verification Checklist

- ☐ Read the full data array, not just the header — actual count recorded
- ☐ All four axes audited (lane bleed / governance / runtime-empty / integrity)
- ☐ Loxihart routines extracted to a reference-only Loxihart artifact with SOC2 banner
- ☐ Cross-connector routines lane-scoped with an "Unscoped — review" bucket
- ☐ Scheduled writes gated (draft → confirm → first-3-runs hold)
- ☐ Data-source guards on every "reads today's session/memory" routine
- ☐ Counts dynamic (no hardcoded totals or `X of N`); collisions staggered
- ☐ Revenue labeled recognized vs pipeline; inflated claims corrected
- ☐ Verification script run: counts match, no collisions, no lane leak
- ☐ Both files presented + per-change changelog + CLAIMS/GAPS footers
- ☐ Shared-infra (n8n tenant / PROJECT_STATE) flagged as a Kyle decision

---

## CLAIMS / COUNTEREXAMPLES / CONTRADICTIONS

- [SOURCED — CLAUDE.md] Three strictly isolated lanes; Loxihart is SOC 2/ISO aligned;
  "Cowork activity NOT in audit logs"; "Never schedule tasks that … write to
  shared services"; "First 3 runs of any new scheduled task: surface for review."
- [SOURCED — this session] The audited artifact's array held 40 routines while
  header/stats/audit all hardcoded 20; Loxihart routines (#9, #18) and an Loxihart-spanning
  #14 lived inside a FlashFusion artifact; CRON #3/#7 wrote Notion on a schedule;
  CRON #12/#20 + API #16 read session/memory in a fresh context.
- [GENERATED] The single-source generator (json.dumps injection + dynamic counts)
  is the lowest-risk rebuild vehicle — reasoned from hitting the triple-quote and
  count-drift bugs that hand-editing would have reintroduced.
- ! CONTRADICTION: Kyle's str_replace-only file rule vs. a source pasted inline
  with no on-disk original. Resolution: author + changelog, and flag it — true
  diffs require a saved original.

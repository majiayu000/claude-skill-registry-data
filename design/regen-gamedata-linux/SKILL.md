---
name: regen-gamedata-linux
description: |
  Regenerate the LINUX side of one or more CounterStrikeSharp-style gamedata.json files (signatures
  AND vtable offsets) against a freshly-opened CS2 libserver.so in a running IDA Pro GUI + ida-pro-mcp.
  For each entry it relocates the old linux signature on the new binary and emits a fresh minimal-unique
  byte sig; validates/re-derives each vtable offset via an RTTI walk; and, when an old sig no longer
  matches (function changed), routes to the matching find-<Symbol> skill to re-discover it. Windows
  side is preserved untouched. Use when a new game version breaks sigs/offsets and you want a one-shot
  linux refresh across CSS gamedata.json, matchzy.json and weaponpaints.json.
  Trigger: regen gamedata, refresh gamedata, new gamever broke sigs, update gamedata linux,
  regenerate signatures and offsets, fix gamedata.json, regen-gamedata-linux
disable-model-invocation: true
---

# Regenerate gamedata (linux) for a new game version

One-shot refresh of the **linux** side of the gamedata files listed in
`references/targets.json` (CSS `gamedata.json`, matchzy `matchzy.json`,
weaponpaints `weaponpaints.json`). Drives the **already-running IDA Pro GUI +
ida-pro-mcp** loaded on the new build's `libserver.so`. The **windows** side of
every entry is preserved verbatim — this only touches `signatures.linux` and
`offsets.linux`.

## Tooling stack (hybrid) — where this skill fits

Three tools split the work on a new game version; use each for what it's best at:

| tool | role | drive |
|------|------|-------|
| **cs2-sig-tracker** (`~/cs2-sig-tracker`) | headless CI triage — which **signatures** broke | `git pull` → `reports/<proj>/status.json` |
| **this skill** (regen-gamedata-linux) | headless bulk regen — 36 sigs + the 14 clean class-vtable offsets, LLM-free | MCP `py_eval` on running IDA |
| **IDA-GameDataTracker** (`gdt64` plugin, GUI) | the hard tail — the 4 non-class-vtable offsets (`AddResource`, `GameEntitySystem`, `GameEventManager`, `CTakeDamageInfo_HitGroup`) + **windows** offsets | Edit → GameDataTracker (interactive, minutes/update) |

GDT is a GUI plugin (dialog I/O, no headless mode) — run it by hand for the low-
frequency hard entries; don't try to headless it. Its actions are registered
(`gamedata_tracker:import_gamedata` / `backtrack` / `export_gamedata`) and also
fire via `ida_kernwin.process_ui_action(...)`, but each pops a file dialog, so
it stays a human-in-the-loop step. Companion plugins installed alongside:
`vtable64` (VTableExplorer — Itanium **+ MSVC** RTTI, use for windows offsets)
and `fusion64` (IDA-Fusion sigmaker).

Two entry kinds, two mechanisms — both **deterministic (no LLM)** on the fast
path:

| gamedata key            | mechanism                                                    |
|-------------------------|-------------------------------------------------------------|
| `signatures.linux`      | relocate old sig → resolve func start → regen fresh unique sig |
| `offsets.linux` (int)   | look up `offsets-anchors.json` → per-kind re-find (vtable RTTI walk / structoffset / global) → validate/re-derive |

Offset entries are **not all vtable slots** — the anchor map classifies each as
`vtable`, `structoffset`, or `global`. See Section B.

The whole point: **self-healing**. Most entries relocate + regen with zero
human input as long as the function head is unchanged. Only genuinely-changed
functions fall through to the per-symbol `find-<Symbol>` skill.

## Prerequisites

1. IDA Pro GUI open on the **new build's** `libserver.so`, ida-pro-mcp server
   running (see "Auto-enable MCP" below to avoid the manual `Ctrl+Alt+M`).
2. Confirm the loaded binary is the linux server module:
   ```
   mcp__ida-pro-mcp__server_health          # is MCP up?
   mcp__ida-pro-mcp__survey_binary detail_level=minimal
   ```
   The root filename must be `libserver.so`. If multiple IDA instances are open
   (e.g. also server.dll for the windows side), pick the linux one with
   `mcp__ida-pro-mcp__select_instance` first. **Abort** if a `.dll` is loaded —
   this skill regenerates the linux side only.
3. Auto-analysis finished (`survey_binary` returns a sha256/md5).

## Signature ↔ IDA wildcard convention

gamedata stores **one `?` per wildcard byte**; IDA `find_bytes` / `parse_binpat`
and the sig generator use **`??`**. Convert on the way in and out:

- to search a stored sig:  `old.replace('?', '??')`  (only lone `?` tokens)
- to store a generated sig: `new.replace('??', '?')`

Helper (matches `regen_css_linux.py`):
```python
def gd_to_ida(s):  return " ".join("??" if t == "?" else t for t in s.split())
def ida_to_gd(s):  return " ".join("?"  if t in ("??", "?") else t for t in s.split())
```

## Procedure

Load `references/targets.json` and `references/offsets-anchors.json`. For each
file (expand `~`), read the JSON, then walk every entry. Keep a per-file
summary: `regen / same / broken / offset-ok / offset-stale`.

### LLM-free contract (default) + when the LLM is allowed

The whole fast path is **deterministic — no agent/LLM**. Everything below is
pure `py_eval` / `find_bytes` / RTTI pointer math on the loaded image:

- **signature relocate + regen** (Section A.1–A.2)
- **offset anchor + RTTI walk** (Section B, all three kinds)

The **only** step that can spend an LLM is the `find-<Symbol>` fallback
(Section A.3 / B when the anchor itself is gone), and even most find-skills
resolve via strings/xrefs without decompiling. So pick a mode up front:

| mode | broken/stale handling | LLM |
|------|-----------------------|-----|
| **mechanical** (default) | relocate + regen only; anything that can't self-heal is **reported, not fixed** | none, ever |
| **llm-fallback** | mechanical first; genuine misses go to the `find-<Symbol>` skill (may decompile) | only on real misses |

Run `mechanical` for a fast unattended refresh right after a game update — it
regenerates every unchanged sig/offset with zero token spend and hands you a
short "needs attention" list. Escalate to `llm-fallback` only for that list.
Mirrors the main pipeline's `-oldgamever` reuse ("unchanged symbols ~free, no
agent/LLM").

### Phase 0 (optional but recommended): triage with cs2-sig-tracker

Before opening/scanning anything, narrow the worklist for **free**. The tracker
(`~/cs2-sig-tracker`, mirror of `git.miksen.me/mikkel/cs2-signatures`) already
scans each **signature** against the live binaries every update and records the
result per platform.

```
git -C ~/cs2-sig-tracker pull --ff-only
```

Then for each file whose `tracker_project` is non-null, read
`~/cs2-sig-tracker/reports/<project>/status.json`:

```python
# results[].name, kind ('signature'|'offset'), platforms.linux.status
#   status ∈ ok | broken | ambiguous | no_binary | missing_sig
worklist = [r["name"] for r in status["results"]
            if r["kind"] == "signature"
            and r["platforms"]["linux"]["status"] in ("broken", "ambiguous")]
```

**Guard rail:** the tracker's verdict is only valid if it ran on the *same*
build you have in IDA. Compare `status["manifest"]` (and the doc's "Last
updated") against your loaded build; if the tracker is behind, ignore its
verdict and validate everything in IDA.

What the tracker does and does **not** give you:

- ✅ tells you exactly which **signature** entries broke/ambiguous → your regen
  worklist. If all `ok` and manifests match, you can skip IDA for that file's
  sigs entirely.
- ❌ does **not** emit a replacement sig — its `sig` field is the current
  (possibly broken) stored sig, same as gamedata.json. Regen is still IDA +
  find-skill.
- ❌ does **not** validate **offsets** at all (`kind: "offset"`,
  `tally.offset_only`). A vtable index isn't a byte pattern, so there is no
  external signal — offsets can only be checked by the RTTI walk in Section B.
- ❌ **weaponpaints is not tracked** (`tracker_project: null`) — no triage,
  always validate its 2 sigs in IDA.

Use Phase 0 to shrink the loop: prioritise the tracker's broken/ambiguous
signature entries, but still run Section B on *every* offset entry (they have no
tracker coverage).

### A. Signature entries (`signatures.linux` present)

**1. Relocate the old sig on the new binary.** Count matches + containing-func
starts across `.text` in one `py_eval`:

```python
mcp__ida-pro-mcp__py_eval code="""
import json, ida_bytes, ida_ida, ida_funcs
sig = "<OLD_SIG_AS_IDA>"   # old linux sig, ? -> ??
pat = ida_bytes.compiled_binpat_vec_t()
err = ida_bytes.parse_binpat_str(pat, ida_ida.inf_get_min_ea(), sig, 16)
res = {"parse_err": err, "hits": [], "func_starts": []}
if not err:
    ea, end = ida_ida.inf_get_min_ea(), ida_ida.inf_get_max_ea()
    for _ in range(20):
        out = ida_bytes.bin_search(ea, end, pat, ida_bytes.BIN_SEARCH_FORWARD)
        hit = out[0] if isinstance(out, tuple) else out
        if hit in (None, ida_ida.BADADDR, 0xffffffffffffffff): break
        res["hits"].append(int(hit))
        f = ida_funcs.get_func(hit)
        res["func_starts"].append(int(f.start_ea) if f else int(hit))
        ea = hit + 1
print(json.dumps(res))
"""
```

Interpret `hits` / unique `func_starts`:

- **exactly 1 hit, 1 unique func start** → function relocated cleanly. Go to A.2.
- **0 hits** or **>1 func start** → **BROKEN** (function changed / sig no longer
  unique). Go to A.3.

**2. Regenerate a fresh minimal-unique sig.** Call
`/generate-signature-for-function` with `addr=<func_start>`. Take its
`func_sig`, convert `??` → `?`, and if different from the stored sig, stage the
change (`signatures.linux = new`). Log `REGEN`; if identical log `same` and
leave as-is.

**3. BROKEN → re-discover.** In **mechanical** mode do **not** spawn anything:
log `BROKEN — needs llm-fallback` (skill exists) or `BROKEN — manual` (no skill)
and move on. Only in **llm-fallback** mode proceed to re-discover via the
symbol's find-skill. Resolve it by globbing the sibling skills dir for the
symbol name:
```
ls -d ~/CS2_VibeSignatures/.claude/skills/find-*<SYMBOL>* 2>/dev/null
```
Symbols are frequently bundled (e.g.
`find-CCSPlayer_ItemServices_GiveNamedItem-AND-...`), so a substring match on
the entry name finds the right combined skill.

- **skill found** → invoke it (it re-anchors via strings/xrefs/vtable, renames
  the func, and emits a fresh sig). Take its resulting func addr → run
  `/generate-signature-for-function` → stage `signatures.linux`. Log `REGEN
  (via find-skill)`.
- **no skill** (many CSS entries) → leave the old sig, log
  `BROKEN — manual` and add to the report. Do **not** guess. These are the only
  entries needing hand work; the report tells you exactly which.

### B. Offset entries (`offsets.linux` present, integer)

Offset entries are **heterogeneous** — a slot int can be a vtable index, a
struct-member offset, or a global/member offset. Look the symbol up in
`references/offsets-anchors.json` (`files.<tag>.<symbol>`) to get its `kind` and
re-find recipe. Never assume "offset == vtable slot".

```json
"CCSPlayerController_ChangeTeam": {
  "offsets": {"windows": 103, "linux": 102},
  "kind": "vtable", "vtable_class": "CCSPlayerController",
  "anchor_strings": ["ChangeTeam() CTMDBG"], "func_find": "find-...", "needs_review": false
}
```

If `needs_review: true`, confirm the class/kind against the binary the first
time (the 6 flagged CSS entries), then flip it in the map.

#### kind = `vtable` (14 of 18 CSS offsets)

Validate the stored slot, re-derive if stale (from `validate-gamedata-offsets`,
proven on stripped libserver.so):

1. **Locate the target function** on the new binary (LLM-free where possible):
   - `anchor_strings` present → `find_bytes(anchor_string)`; the func containing
     that string ref is the target. (ChangeTeam only, so far.)
   - else → the func has its own find recipe (`func_find`): if it also carries a
     `signatures.linux` entry, relocate that sig (Section A.1) → func start; else
     in `llm-fallback` mode invoke the `find-<Symbol>` skill.
2. **RTTI walk to the primary vtable** of `vtable_class` (no symbols):
   - typeinfo NAME bytes `"<len><ClassName>\0"`, `len` = char count
     (`CCSPlayerController` = 19). Locate via `find_bytes` on hex.
   - `find_bytes(ptr_to_name_str)` → typeinfo = match where the name ptr sits at
     `struct+8`.
   - `find_bytes(ptr_to_typeinfo)` → each match = a vtable's typeinfo slot
     (`vtable_base+8`); candidate = `match-8`.
   - **primary vtable** = candidate whose qword at `base+0` (offset_to_top) == 0.
3. **Slot → func:** `func = *(vtable_base + 0x10 + N*8)` (slot 0 at `base+0x10`;
   first two qwords are offset_to_top + typeinfo). N = stored linux offset.
4. **Compare:** slot-N func == the func from step 1 → **offset-ok**, keep.
   Mismatch → **offset-stale**: scan the whole vtable for the step-1 func addr,
   stage `offsets.linux = new_index`. Skills `/get-vtable-index`,
   `/get-vtable-address` implement steps 2–4.

**Gotchas (proven on build 14171 — heed these):**

- **Raise the typeinfo→vtable search cap for base classes.** In step 2, the
  "pointers to typeinfo" scan for a heavily-inherited base (e.g. `CBaseEntity`)
  has thousands of hits (every derived `__si_class_type_info` references it). A
  small cap (~80) truncates before the real vtable and yields a false
  "no primary vtable". Use `cap >= 20000` for that inner search; keep the
  name-string and name-pointer scans small.
- **Verify the slot by decompiling, not `XrefsTo`.** When the strings cache is
  cold (`server_health` → `strings_cache_ready:false`), `idautils.XrefsTo(str)`
  returns nothing, so the "func containing the anchor string" route fails. The
  reliable anchored check is: **decompile the slot-N func and substring-match**
  the anchor (confirmed: slot 102 of `CCSPlayerController` decompiles containing
  `"ChangeTeam() CTMDBG"`). For symbols with **no** anchor string (most), fall
  back to structural validation: confirm slot N is `< vtable_length` and points
  into `.text`. A plausible-but-unverified slot with no anchor goes on the
  `needs review` list, not silently trusted.
- **Entity vfunc offsets → validate on a CONCRETE class, not the abstract base.**
  An overridable entity method (e.g. `SetStateChanged`, slot 29) is a `nullsub`
  placeholder in the abstract base vtable (`CEntityInstance`) and only filled in
  on concrete entities. Resolve such offsets against `CBaseEntity` (or a concrete
  entity like `CCSPlayerController`, which share the slot), not the declared base.
  Confirmed 14171: `CEntityInstance` slot 29 = `nullsub`; `CBaseEntity`/
  `CCSPlayerController` slot 29 = the real `SetStateChanged` dispatcher.
- **Class name → typeinfo string is length-prefixed:** `"<len><ClassName>\0"`,
  `len` = character count as decimal (`CBaseEntity` → `11CBaseEntity`,
  `CCSPlayerController` → `19CCSPlayerController`). Some gamedata "class"
  prefixes have **no** such RTTI name (e.g. `CEntityResourceManifest`,
  `CGameResourceService` — absent on 14171): abstract interfaces / non-RTTI
  managers. Resolve those via a concrete impl or anchor-relocation, not a name walk.

**Cold xref-DB workarounds (the analysis DB often lacks data/rip-relative xrefs
on a freshly-loaded stripped binary — `strings_cache_ready:false`):**

- **`idautils.XrefsTo(string_or_vtable)` returns nothing** for data targets →
  don't rely on it. But **`XrefsTo(func)` DOES work** — call xrefs (`E8`) are
  indexed, so caller-chains resolve fine.
- **To find who references a vtable** (the ctor), scan for the rip-relative
  `lea reg, [rip+disp]` whose target is **`vtable_base + 0x10`** (the vptr stored
  in objects is the first *method slot*, not the vtable base). Patterns
  `4[8C] 8D {05,0D,15,1D,25,2D,35,3D} ?? ?? ?? ??`; for each, `target = ea + 7 +
  int32(disp)`. **Use a high `find_bytes` cap (≥100k)** — `48 8D 05` alone occurs
  ~120k times in libserver.so; a small cap silently truncates before your hit
  (this bit twice on 14171).
- **To find call sites of a func**, prefer `XrefsTo(func)` over scanning all
  `E8` (which exceeds 100k and truncates).

#### kind = `structoffset` (CTakeDamageInfo_HitGroup, CheckTransmitPlayerSlot)

Not a vtable index — it's a byte offset of a struct member. Re-derive with the
struct-offset flow (`/generate-signature-for-structoffset` +
`/write-structoffset-as-yaml`), anchored on the accessor described in
`source_script` (e.g. `find-CCheckTransmitInfo_m_nPlayerSlot.py`). The stored
int is the member offset; confirm it against the instruction the sig pins.

#### kind = `global` (GameEntitySystem, GameEventManager)

Member/global offset, not a vtable slot. Resolve via the global's find recipe
(`source_script`, e.g. `find-s_GameEventManager.py` / `find-CGameEntitySystem_ctor.py`)
and its `TARGET_GLOBALVAR_NAMES` anchor; the stored int is the member offset in
the owning struct. `needs_review: true` — validate the first time.

#### no recipe

`kind: "unknown"` or a missing anchor → in `mechanical` mode log
`offset — no anchor` and leave as-is; the report lists it for manual work. Do
not guess a slot.

### C. Write back (preserve windows)

After all entries of a file are processed, write the JSON back **only if
something changed**, preserving key order and the untouched windows/library
keys. Use 2-space indent + trailing newline (matches the pipeline). Back up
first:

```
cp <file> <file>.bak.<mtime>      # timestamped backup
```
Then write the merged dict (stage changes onto the original loaded dict; never
drop `signatures.windows` / `offsets.windows` / `library`).

### D. Report

Print one block per file, then a combined tail:

```
=== <tag> (<path>)  [mode: mechanical|llm-fallback] ===
  REGEN   : <n>   (fresh linux sig written)
  same    : <n>   (function unchanged, sig still unique)
  offset  : <ok>/<stale>  by kind vtable/structoffset/global (stale re-indexed)
  BROKEN — needs llm-fallback : <list>  (skill exists; mechanical mode skipped it)
  BROKEN — via find-skill     : <list>  (llm-fallback mode re-found)
  BROKEN — manual             : <list>  (no skill / no anchor — needs you)
  offset  — needs review      : <list>  (anchor map flagged; confirm once)
```

The bottom three lists are the deliverable: a short, exact set of symbols that
didn't self-heal. In `mechanical` mode everything else regenerated with zero
token spend; re-run those in `llm-fallback` (or by hand) when convenient.

## Windows side (later)

This skill is linux-only by design (your workflow starts linux-first). For the
windows sig, re-run Section A in a `server.dll` IDA instance and merge into each
file's `signatures.windows`. The CSS repo's `update_css_gamedata.sh` already
does both platforms headlessly if you prefer batch over GUI.

**Windows offsets are harder.** The Section B RTTI walk is Itanium (Linux) only.
Windows uses **MSVC RTTI** — `RTTICompleteObjectLocator` with image-relative
32-bit RVAs and a different vtable/typeinfo layout — so the walk must be
rewritten for PE before `offsets.windows` can self-heal. Until then, re-derive
windows offsets with `/get-vtable-index` on the loaded `server.dll` (it handles
either layout) and merge manually. This is the intended "windows last" follow-up.

## Auto-enable MCP (skip the Ctrl+Alt+M)

The ida-pro-mcp plugin already supports autostart — it's a **per-IDB**
preference (netnode `$ ida_mcp.autostart`, default ON) that fires on
`ready_to_run` when running in the GUI. If you keep needing `Ctrl+Alt+M`, that
IDB has autostart turned off. Fix once, persists into the `.i64`:

**Edit → Plugins → MCP Configuration → tick "Autostart server when IDA opens".**

For a brand-new build's fresh `.i64` the default is already ON, so
`~/lin.sh <gamever>` should start MCP with no keypress. If you want a
belt-and-braces global guarantee across every build, drop this in
`~/.idapro/idapythonrc.py` (runs on every DB open; harmless if the plugin
already autostarted — `run` restarts cleanly):

```python
# Force ida-pro-mcp to start in the GUI without Ctrl+Alt+M.
import ida_kernwin, ida_loader
class _MCPAuto(ida_kernwin.UI_Hooks):
    def ready_to_run(self):
        if ida_kernwin.is_idaq():
            ida_loader.load_and_run_plugin("ida_mcp", 0)  # plugin file = ida_mcp
        self.unhook()
_mcp_auto = _MCPAuto(); _mcp_auto.hook()
```

## Symbol → find-skill coverage (as of build 14171)

Routing is dynamic (glob), but for reference — coverage of the broken-sig
fallback:

- **matchzy.json** — 5/5 have find-skills (all `*_Create` + `CCSGameRules_PostCleanUp`).
- **weaponpaints.json** — 2/2 (`CAttributeList_SetOrAddAttributeValueByName`, `UpdateItemView`).
- **CSS gamedata.json** — ~half. NO-SKILL entries (e.g. `UTIL_Remove`,
  `CGameEventManager_Init`, `CCSPlayerController_ChangeTeam` offset,
  `SetStateChanged`, `GameEntitySystem`) self-heal via relocation; if a NO-SKILL
  entry breaks it lands in "BROKEN — manual".

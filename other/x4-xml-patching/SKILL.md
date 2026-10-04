---
name: x4-xml-patching
description: Use when writing, editing, reviewing or validating ANY X4 XML — diff patches, mod files, overlays, wares, macros, libraries, md/ or aiscripts/. Carries the selector, merge-tree and load-order gotchas that make a patch silently no-op, where a given fix belongs, and how to validate it before an in-game test cycle. Invoke before the first edit, not after the patch fails.
allowed-tools: Bash, Read, Grep, Glob, Edit, Write
---

# Writing and validating X4 XML

X4 patches fail silently. A selector that matches nothing, a path off by one folder, a
complete file where a `<diff>` was required — the engine loads the mod, logs nothing useful,
and the feature is simply absent. Everything here exists to make that class visible before
an in-game test cycle is spent on it.

**Gotcha numbers are stable ids.** Records written against them cite them by number
(a knowledgebase, a blind-spots register). Never renumber one; a retired number is never reused.

---

## 1. Default to a diff patch

Mods store only what changed.

```xml
<?xml version="1.0" encoding="utf-8"?>
<diff>
  <replace sel="//ware[@id='ore']/@price_average">500</replace>
  <add sel="//wares">
    <ware id="my_new_ware" ... />
  </add>
</diff>
```

**Complete XML file only for a path that does not already exist** — a new script, a new ware
group for a new faction. Not "a file I am replacing wholesale".

**File path mirroring is absolute (#1).** The path inside the mod must exactly mirror the base
game path. Patching `assets/wares/wares.xml` means `dev\{mod}\assets\wares\wares.xml`. One
wrong folder name and the patch does nothing, with no error.

---

## 2. The silent no-op traps

These four are the ones that log nothing at all. Check them before anything else.

**#1 — Path mirroring.** Above. Exact mirror or nothing happens.

**#6 — Patching another MOD uses a NESTED path.** `<your_mod>/extensions/<target_folder>/<mirrored path>`,
never a bare mirrored path. Engine-proven: the bare form is never even opened. The
`<dependency id=>` you declare uses the target's `content.xml` **id**, which can differ from
its folder name; the nested **folder** uses the folder name.

> ⚠ **The test is who owns the FILE, not who wrote the NODE — and getting it backwards points
> you at the wrong form.** If the vpath exists in base/DLC, use the **PLAIN** path even when
> the nodes you target were added by another mod: that mod only diffed into vanilla's
> document, so its additions live in the merged tree and a plain-path diff reaches them.
> Proven in a real workspace: a personal overlay's `libraries\factions.xml` sits at the base-game path, is
> engine-loaded, and selects a `//faction[@id='...']` node that ANOTHER mod adds. The
> nested form is ONLY for a file base+DLC does not have.

`x4validate --tier b` verifies cross-mod patches and flags the bare-path mistake as an ERROR
naming the exact move-to path.

**#21 — An `md/` or `aiscripts/` file at a vanilla path MUST be a `<diff>`.** MEASURED across
base + 8 DLC + 115 mods: **263 of 264** script-path collisions use `<diff>`, including 59 of
59 of Egosoft's own DLC-vs-base collisions. The lone exception is opened by the engine and its
cues never take effect — a silent no-op with no error line anywhere. The engine registers MD
scripts by **filename**, and a duplicate filename never takes effect. Confirmed by controlled
experiment: a uniquely-named mdscript in an overlay registers and runs; a functionally
identical one at a colliding vanilla path does not, with file path as the only variable.
⚠ `aiscripts/` is not modelled by our merge — the corpus has zero instances to verify against.

**#9 — A search that finds nothing is a LEAD, never a fact.** Say *"my search for X in Y found
nothing"*, never *"X does not exist."* Run a second, differently-shaped search first — different
case, pattern, path, or tool. **Default to case-insensitive for X4 identifiers**: the corpus
genuinely mixes case (`Cluster_104` vs `cluster_104`, `SurfaceElements` vs `surfaceelements`)
and ripgrep is case-sensitive by default. And **follow the reference** — a macro's behaviour
lives in the component/bullet/loadout it points at.

---

## 3. Which overlay does a fix belong in

Personal fixes live in load-last personal overlay mods. The decision is not about the file you
patch — it is about **what happens to this fix when the mod it relates to is removed or updated.**

| Outcome on removal | When | Where it goes |
|---|---|---|
| **Clean no-op** — the `sel=` stops matching | Target node lives in the other mod's file, or a node that mod added | Its own overlay, **optional** dep (or general overlay + `if=` guard if the target is a vanilla file) |
| **Dangling reference** — the op still applies and injects something that no longer exists | The **payload** names another mod's content: a variable it defines, a texture it ships, a library cue it owns | Its own overlay, **hard** `<dependency>` — `if=` does NOT protect this, it guards the selector, not the payload |
| **Silent wrongness** — the op applies, is structurally valid, and is now semantically wrong | Vanilla node **and** vanilla payload, but the *reason for the value* was another mod | **Nothing detects this.** Prefer the mod-specific overlay so it leaves with its rationale. If it must stay general, state the coupling in `content.xml`'s description. |

**The data axis matters more than the file axis.** Ask where the *meaning* lives:

- Vanilla field, vanilla meaning, patched inside a mod's file (repairing `@shield` on a mod's
  ship macro to a schema-valid value) → mod-specific. It dies with its target, correctly.
- Vanilla field, vanilla meaning, but mod-motivated value (`coreboundaryzoneheight=300000` set
  only because a 3D-sector mod is installed) → silent-wrongness row. Removing that mod leaves
  stations 300 km off-plane with nothing logging a complaint.

**Other axes that force a split:** repair vs preference (never mix — a repair is shippable
upstream, a preference is not); re-verification cadence (a fix is re-validated on its *target's*
release schedule); load-order coupling (a declared dependency loads EARLIER, so optional deps
are how you pin order); interaction fixes needing both X and Y → own overlay, optional dep on
both; rollback granularity (one mod = one version).

**Quick test:** *"If I uninstalled the mod this relates to, would this file be meaningless — or
worse, quietly wrong?"* Either answer → its own overlay.

---

## 4. Selector and merge semantics

**A `sel=` matching MULTIPLE nodes is a SILENT NO-OP.** RFC 5261 requires exactly one
match: X4 logs `Multiple matching nodes for path '<sel>' ... Skipping node` and applies
**nothing**, so the patch reads fine and does nothing. Disambiguate with a CONTENT
predicate (`[material[@shader='x']]`) over a positional index, and run `x4validate` — it
flags this.

**#17 — A diff's ops apply IN ORDER, to a tree the earlier ops have already changed.** Two
shapes: a later op selecting into an earlier op's subtree (MEASURED: 2 into a `<remove>`, **458
into an `<add>`** across 18 mods), and — dominant — a selector that predicates on a value an
earlier op just wrote (`price[@min='432']/@min` → 516, then `price[@min='516']/@average`…).
X4_Customizer emits the latter by default, chained **1,443 ops deep** in one real file. Never
`<remove>` a node and then touch it, and never reorder ops casually.

**#10 — A `<replace>` targeting a document ROOT (`sel="//macros"`) is the standard whole-file
override idiom.** One large overhaul mod alone ships 848 of them. The engine applies these silently and correctly.
A root has no parent, so any node-swapping code must special-case it.

**#11 — The `index/` files are NOT the definition set.** Entities defined inside `libraries/*.xml`
(`character_components.xml`, `character_macros.xml`) are real but absent from
`index/macros.xml` / `index/components.xml`. The correct set is **index ∪ every name defined in
the corpus**. Related trap: `<component ref>` names a MACRO inside `libraries/wares.xml` but a
COMPONENT inside a macro file — one attribute, two namespaces. **Do not classify it — check
BOTH.** Testing against the UNION took 2,300 references down to 3 unresolved, all genuine;
the macro-only check produced 1,792 misses. `standardzone`/`standardregion` are components in
`libraries/component.xml`; checking them as macros produced 23 bogus gating errors.

**#13 — `_merge.Config(overlays=sorted(mods))` is NOT the effective tree** — it is *alphabetical*.
The real tree uses the computed load order (`_effective.ordered_overlays` →
`_loadorder.compute_load_order`: the engine's MEASURED rule, case-insensitive UPPERCASE folder
order walked in repeated dependency passes — BLIND-SPOTS F128). Same macro, two orders:
`ship_kha_xl_battleship_01_a_macro` `people.capacity` reads **0** alphabetically and **200** in
true load order. Use `x4effective`, or build overlays via `ordered_overlays`.

**#18 — `Collision.winner` from x4compat means a DIFFERENT thing per kind.** For
FULL-OVERRIDE / HARD / UNION-KEY it names the mod whose value is **live**. For **SUBTREE it
names the mod that did the WIPING**, which is not the owner of the final value — a third mod
loading later can re-supply it. For **NAME-CLASH it is deliberately empty** (`index/macros.xml`
decides, not load order). Never compare it blindly to `x4effective`'s `origin`. A wipe undone
by a later mod is 3 of 148 SUBTREE rows (2.0%), so the advisory is not noise.

**#14 — A claim about VANILLA must be checked against vanilla, not the effective tree.** Same
macro, two tiers: the Khaak boss is hull **275,000 vanilla / 675,000 effective**. A doc saying
"vanilla 9.0 contains X" is not refuted by the effective store disagreeing.

---

## 5. Enumeration traps

**#12 — Never enumerate game content by filename pattern.** A large overhaul mod ships live macro files that
break the `*_macro.xml` convention (`bullet_ter_m_graviton`, `bullet_gen_turret_l_rotor`) and
two with a literal typo — `storage_lint_frigate_akita_marco.xml` ("**marco**"). All are
registered in the effective index and load normally. Detect by content or via the index. The
filesystem is not the authority; the merged tree is.

**#20 — `reference\` and the install's `extensions\ego_dlc_*` are THE SAME CONTENT.**
`reference\` IS the unpacked base+DLC; the DLC folders under the live `extensions\` are the
packed originals of those same files. Enumerating both double-counts every DLC — it once
reported 92 md collisions where the answer was 1, and 200 modulegroups where the answer was
146. **Any sweep over "everything installed" must exclude `ego_dlc_*` from the mod list, or
exclude `reference\` — never both.** Generalise: your verification query must cover the SAME
POPULATION as the finding.

**Use the purpose-built enumerators, never a hand-rolled walk:**

| you want | use | not |
|---|---|---|
| every XML a mod owns | `_scan.iter_mod_xml` / `iter_mod_xml_bytes` (loose THEN packed) | `_cat.mod_vfs` — catalogs only, returns `{}` for a loose mod |
| every base+DLC vpath | `_effective.base_vpaths` | `reference.rglob("*.xml")` — loose-only, so both mini-DLC are invisible |
| scan EVERY installed mod | `_scan.iter_corpus_xml(ext, report)` + `CorpusScan.verdict()` | a hand-rolled `for mod in extensions.iterdir()` loop |
| does this vpath exist LIVE, and who supplies it? | `x4effective dump --chain <vpath>` | `_effective.base_has` — base+DLC only, so a mod-supplied file reads as a confident *absent* |

`<mod>:full` = that mod SUPPLIES the document. `base, ego_dlc_x:diff` = base supplies it, the DLC
only PATCHES it. That full-vs-diff distinction is usually the thing you actually need.

---

## 6. Engine, catalog and load-order facts

**#2 — CAT/DAT catalogs are numbered and override in order.** 09 overrides 08 overrides 01;
DLC cats override base game.

**#3 — All game content files are digitally signed.** Modifying base game .cat/.dat/.xml breaks
signature verification. Always work in `extensions\`.

**#4 — `content.xml save="1"`** bakes the mod into save files; removing it later can corrupt
them. **#5 — `content.xml enabled="0"`** means installed but disabled — check this if a mod
seems to have no effect.

**#16 — The profile `content.xml` reconciles against disk, not on every launch.** X4 adds an
entry (enabled) for a folder it has not seen, and disables one whose folder is gone. Its mtime
does not track session files. Commit it after each modlist change.

**#15 — `<content sync="true|false">` on the ROOT element IS the in-game "Steam Workshop
Downloads" toggle.** Read the whole file, including the element you are scanning inside of.
With it ON, subscribed mods download **straight into game-root `extensions\`** — X4 has no
`steamapps/workshop/content/392160` directory at all, so *"no workshop dir exists"* does NOT
mean *"nothing is subscribed"*. Deleting the folder is temporary; **unsubscribing on Steam is
the only durable removal.**

**#30 — The profile `content.xml` is a DECISION LOG, not an inventory, and it is keyed by
MANIFEST ID.** MEASURED: 348 entries, **287 fossils (82.5%)** with no folder on disk, while
**54 of 115 installed mods (47.0%) are absent entirely**; exactly 1 on-disk mod is actually
disabled by it. Three consequences:

- **ABSENT ≠ DISABLED.** X4 adds an unseen folder as ENABLED, so `mods("active")` reads
  `prof.get(id, <the manifest's enabled>)` -- the profile entry decides, and with no entry
  the manifest's own `enabled` (true unless it says `"0"`/`"false"`) is the default. Default
  an absent entry to DISABLED and 54 of 115 mods silently vanish from Tier B, x4compat,
  x4effective and `x4eff` at once, with nothing raising.
- **Never query it by mod NAME** — only by manifest id, or via `_registry.mods(...)`. Of 123
  on-disk mods, 60 match by manifest id and only **9** by folder name. a grep for a Workshop
  mod's NAME returns nothing because its entry is keyed `ws_<number>`; that zero is the WRONG QUERY, not evidence.
- **Do not prune the fossils.** 175 of 287 are `enabled="false"`, and deliberate-ban vs
  auto-disable-on-removal is indistinguishable for most. Deleting one means the mod returns
  **enabled**.

**#28 — The engine's own log is an instrument, and its obvious readings are traps.**

- Signature-failure lines are a **SAMPLE**, not a mod list — they name whatever files a session
  happened to touch. **The real enumerator is the load-time t-file block**: at timestamp 0.00
  the engine opens every extension's `t/0001*.xml` in one contiguous run, in load order (#13).
- The skip vocabulary names an INCONSISTENT object. `Skipping node.` names the **patching**
  mod's file; `Skipping file.` names the merge **TARGET**. Never infer what was discarded from
  what the message names.
- A malformed patch skips only the PATCH; the base document survives (~90%). Asset loading is a
  **reference-following traversal** (ship macro → its `<component ref>` → engine → shield →
  turret → that turret's bullet → thruster → next ship), so **adjacency in debug.txt is
  evidence of a REFERENCE** and the log can be read as a dependency graph.

**#19 — An engine-log LINE count is NOT an op count.** The engine logs most patch failures
TWICE: 27 of 35 patch files in one log have a line:distinct ratio of exactly 2.00. The
mechanism is unmeasured — do not record an explanation for it. Never quote a `grep -c` of
debug.txt as an op count; `x4debug triage` / `crosscheck` already de-duplicate.

**#29 — The engine opens exactly ONE language's t-file** — MEASURED 21 of 21 opens are `l044`,
zero of any other id, plus the language-neutral `t/0001.xml`. Consequence: **a malformed
t-file in a non-active language is INVISIBLE** — it can never produce an error line, because
the file is never opened. Of 12 malformed documents across 114 active mods, exactly one sits at
a vpath the engine ever opens. *"The engine logs no error"* means *"the engine never opened
it"* at least as often as it means *"the file is fine."*

**#33 — A savegame is a queryable artifact, and its `<patches>` block is NOT a record of what
loaded.** Saves are plain gzipped XML; the largest here is 140 MB compressed → 1.28 GB, and
streams end-to-end in 2.5 s. An extension is recorded iff its `content.xml` `save` attribute is
**absent or `="1"`**; `save="0"`/`"false"` is never recorded. For mods that is **3 of 121
(2.5%)** — the save-baked set (#4), not an inventory, and less complete than the profile
`content.xml`. ⚠ **Removing a mod does not leave dangling references — the engine SILENTLY
DELETES the orphaned content.** One disabled mod took its 37 macros / 46 references to 0 with
**one** error line and no warning dialog, and net error count went DOWN by 3, so watching
`debug.txt` makes the removal look like an improvement.

---

## 7. Version and content facts

**#8 — Don't assume "missing in an old ship macro" = "added by 9.0."** The
`<jerk>`/`<steeringcurve>`/`<accfactors>` flight-tuning block is from **7.50** (Dec 2024), not
9.0 — a pre-7.50 ship mod lacks it for an older reason. 9.0's real ship-porting breaking
changes are: collision-shape re-export required, S/M models resized (engines/shields moved into
the hull mesh), and a 90+-shield rebalance. See KNOWLEDGEBASE "Ship/flight/shield mechanics
timeline" before assuming a version for any flight/shield/boost change.

**#7 — An overhaul mod can REMOVE a mechanic the base game still has.** Measured on one major
overhaul's 9.0 release: internal shields (`ishield_*`) gone from its core (0 refs), ⚠ **but not
from the game** -- the live tree still carries **23 distinct `ishield_` ids across 45 base/DLC
documents**, including Timelines' `ship_xen_xl_mothership_01_b` and vanilla
`md/story_research_xen_equipment.xml`. A pre-update ship/patch mod shipping `ishield_*_macro` files
for that overhaul is patching a dead mechanic -- of the 445 distinct `ishield_` ids one such mod
stack referenced, **443 (99.6%) no longer existed**. Regular `shield_*_macro` shields are
unaffected. Read the overhaul's own changelog before porting anything built for an older release.

**#32 — `--` is illegal inside an XML comment, and a hand-edited XML file must be RE-PARSED.**
An explanatory comment containing `-- so the intended…` made a deployed mod's `libraries/god.xml`
not well-formed. Caught only because the result was parsed, not eyeballed. Use an em dash, a
colon, or a single hyphen.

**Assume existing content is REAL AND LIVE until proven dead.** Anything present in a mod or
script is there because it works; the burden of proof is on "this is dead". Before calling
anything obsolete: read the error text literally (`Order 'MiningRoutine': Parameter 'stayinspace'
was not expected` scopes the problem to ONE order, not the parameter globally); search
`reference\` for live uses; date the change against the KB timeline; check who else references
it. **`<remove>` ops, file deletion and "cleanup" are destructive — present the finding and get
an explicit go-ahead first, and prefer additive/restorative repairs.**

⚠ **A one-sided absence in an OLD document is upstream ADDITION, not author deletion.** A
two-way diff cannot separate the author's edits from upstream drift; only a merge base can.
MEASURED on a 2021 submod against its parent overhaul's current release: 16 macros "lost" `missile.targetable`, 15
`explosiondamage.shielddisruption`, 18 `identification.mk` — **none were removals**; the file
simply predates them. This is the concrete reason to rebuild an old mod as **diff patches
against the current tree**, never as whole-document replaces.

⚠ **A stale `<remove>` in someone else's mod is a bug, not an instruction.** It can delete
content the base game added later. Diagnose *why* it exists before assuming the author meant it.

---

## 8. Model it on vanilla — copy, do not compose

**Before implementing any change, find how the base game handles the closest equivalent and
model on that.** The unpacked base game is proof-of-concept. If vanilla doesn't do it that way,
ask *why* before choosing your approach.

1. Find the vanilla analogue in `reference\` (same action, macro, ware, or cue type).
2. Match its exact form — attributes, structure, values.
3. Only diverge when the vanilla pattern genuinely cannot be adapted.

**★ COPY IT. DO NOT COMPOSE FROM THE SCHEMA.** A schema tells you what is well-formed; it
cannot tell you what is *wired up*. An MD harness composed from `md.xsd` passed validation
clean and burned three play sessions: a ship spawned without `<pilot>` is INERT;
`<event_game_loaded/>` never fires on a new game; a sub-cue's delay runs from script start, not
from its parent finishing; and the `Attack` order takes `primarytarget`, not `target`. None of
that is expressible in a schema. **Paste a working example and change the values.**

**★ AND SEARCH THE INSTALLED MODS, NOT JUST `reference\`.** Mods solve MODDER problems vanilla
never had — spawn a test fight, force a loadout, drive an experiment. For anything vanilla does
not itself need to do, an installed mod is the *closer* analogue, proven in THIS game version
with THIS modlist. Search with `_scan.iter_mod_xml_bytes` (packed-inclusive); a loose-only grep
misses most of the corpus. Paste a working example from such a mod and change the values.

**Native engine solutions first.** "Simple" means simple from the engine's perspective, not
fewest lines. A native MD action or a clean `<diff>` beats a fragile multi-step script hack.
Prefer native MD actions and script properties; a diff patch over rewriting a whole file; the
game's own events/cues over polling.

---

## 9. Validate before deploying

**Running `x4validate` is routine and non-optional** — a habit, like checking debug.txt.

```
cd $CLAUDE_PROJECT_DIR/tools/x4validate && uv run x4validate <dev\mod_folder>
```

- **When:** after editing any diff patch or adding content, BEFORE deploying for an in-game
  test. Re-run after a game update — the merged tree changes.
- **Completeness:** add `--entity <type>:<id> --like <type>:<vanilla>` (`ware`/`ship`/`module`).
- **Cross-mod: use `--tier b`.** Tier A builds base+DLC only, so a diff targeting another mod's
  content reports `no base game file` — expected, not a real error. Tier B merges the ACTIVE
  extension set (what the engine loads) in load order, and also catches the reverse failure Tier A passes silently:
  content another mod has REMOVED. Ordering is the engine's MEASURED order -- signature-check
  order from the log, and patch-APPLY order by the in-game load-order probe (2026-09-26).
- **Schema validation is GATED behind `--update`.** Compiling `md.xsd` costs ~102 s so it does
  not run by default — a plain run reports `OK: no issues found` on a script it never
  schema-checked. `--xsd-fast` skips the compile but loses the "element not expected" class,
  which is where element-ORDERING errors live.
- **`if=`-guarded ops report INFO, not ERROR.** A guarded op whose guard is false is a designed
  no-op. A guard that PASSES but whose `sel=` still misses is a real error.
- **Validate the DEPLOYED copy whenever load order could matter.** Tier B places a mod that is
  not installed by the engine rule, keyed on its folder NAME and its own manifest's
  dependencies — so a dev folder named differently from its deployed copy lands elsewhere.
  (Until 2026-09-25 it assumed LAST, the optimistic tree: a dev-only twin then reported 3
  false alarms its deployed copy did not.)

**A clean x4validate is necessary, not sufficient.** Static validation cannot see runtime
wiring — cue-trigger semantics and cross-file order signatures are not expressible in a schema.
For a new script the engine log is the FIRST real check, not the last.

---

## 10. Dry-run convention

For any bulk XML operation (mass stat changes, adding content to many files at once):

1. **Read-only pass** — log every file and every value that would change; print, do NOT write.
2. **User reviews** the proposed changes.
3. **Write pass** — only after approval.

---

## 11. The per-change workflow

**Research (before touching any file)**

1. Nexus Mods page first — description, articles, changelogs, comments, known issues.
2. Check for related mods/patches touching the same files.
3. Locate the relevant XML in `reference\`; understand the full base structure.
4. **Identify ALL files that need changes** — document the complete list before writing anything.
5. State confidence; below 90%, research more first.

**Implement**

- Diff patch for existing content, complete file for new content.
- Mirror the game folder structure inside `dev\{mod_name}\`.
- Validate with x4validate (mandatory).
- Deploy with a **script**, never a hand-rolled `cp -r` -- one that is dry-run by default,
  `--apply` to write, and refuses unless the destination is directly under game-root
  `extensions\` AND the destination's manifest id equals the SOURCE's, never `rmtree`s a
  destination, deletes orphans one named file at a time after printing them, and re-reads the
  destination to prove every file is byte-identical.
- Check `{user profile}\debug.txt` for errors — via `x4debug triage`, never a hand-rolled
  `grep | sort | uniq -c`.

**After a change, snapshot.** Before any experimental change, copy the known-good dev files to
`.claude\backups\known-good-<descriptive-name>\`. After confirming a state works in-game,
snapshot it named for *what works*, not just the date.

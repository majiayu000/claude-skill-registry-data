---
name: arma-reforger-script-analysis
description: Analyse Arma Reforger Enforce Script code - what a class or method actually does, which file and line declares it in the installed build, which mods replace it with modded class, and why an override changes nothing or two mods fight over one method. Use when asked to explain, trace, review or debug a .c script or a mod's scripts; when a modded class, modded enum or override does not take effect; when deciding whether two mods conflict on one class (SCR_CharacterCameraHandlerComponent, SCR_PlayerController, SCR_BaseGameMode); when a method has no call sites in the sources because the engine calls it; when a base class is reported missing or a chain stops at ScriptComponent, GenericEntity or Managed because core's pak was not passed - core and data conflict as resources but core carries the engine's script declarations; or when a comment in a mod claims something about vanilla code that must be checked. Not for reading pak archives, resource GUIDs or localization tables (the game-data skill), and not for writing a server config.
---

# Analysing Arma Reforger script code

This repository has two jobs around `.c` files and they are not the same one. **Reading** a
script — finding it in a `.pak`, listing a class's members, printing a signature — is
[the game-data skill](../arma-reforger-game-data/SKILL.md) §5, which owns the reader's
reference: every command, every flag, the source kinds and the parser's measured behaviour.
**Analysing** script code is this skill: deciding which copy of the code is the one that runs,
reading a declaration and then the body behind it, and reasoning about what happens when
several mods replace the same class.

The distinction is not pedantry. Script analysis fails in a particular way: it produces a
plausible description of a file nobody ran. Four downloaded addons each override
`SCR_CharacterCameraHandlerComponent.CameraSelector`; read one copy alone and you have a
correct description of a method that may never be the one that decides. §4 works that example
through.

## 0. Three questions, three shapes of answer

| The question | What actually settles it | What the answer must carry |
|---|---|---|
| What does this class or method do? | the declaration, then the body behind it | a behaviour summary and `file:line-line` |
| Why does my mod's change do nothing? | the chain, the module, the signature, and whether the mod is loaded | the step where it breaks, named |
| Two mods change the same method — what happens? | every copy of the class, the order they run in, and which of them call `super` | a chain, with the order called out as the one assumption |

**Two rules that keep the answer honest.**

1. **A statement about code carries the file and the lines.** `scripts/Game/Player/SCR_PlayerController.c:30`
   is checkable; "in SCR_PlayerController" is not.
2. **A statement about runtime behaviour is an inference, and is labelled as one.** The text
   says what will happen if the code runs; whether it runs, and with what values, is decided by
   the build flags, the data files and the load order.

**A comment is its author's claim, not evidence.** WCS_Core guards `CameraSelector` against
null `m_AnimationComponent` / `m_ControllerComponent` and says those are "the members vanilla
actually dereferences". That is true — vanilla dereferences them at
`scripts/Game/Character/CharacterCameraHandlerComponent.c:179` and `:190` — but the comment is
what prompted the check, not what settled it. A mod's comment is also where a wrong assumption
usually hides.

## 1. Which copy of the code is the one that runs

**Vanilla.** The game's script code is in two **addons** of the install, and each is its own
archive: `<install>/addons/data` (the game's own scripts, every module) and
`<install>/addons/core` (the engine-facing layer: `Managed`, `IEntity`, `Widget`, `BaseContainer`,
and `GameLib`). The client keeps the game scripts in one archive, `data/data007.pak`; the dedicated
server keeps the same 5 809 files in `data/data002.pak`, the other resources in `data.pak` and
`data001.pak` beside it. Core is always `core/data.pak` — 759 `.c`, in every install. Measured on
1.8.0.13 with `stats`: **6 568 `.c` files, 28.7 MB, 94 568 declarations**, spread over nine
modules — `Game` 81 120 declarations, `GameLib` 4 950, `Core` 3 079, `WorkbenchGame` 2 810,
`WorkbenchGameCommon` 1 145, `GameCode` 976, `Autotest` 297, `WorkbenchCommon` 147, `Workbench` 44.

### `core` and `data` conflict as resources, and both are needed as code

The two addons are separate mounts, and their **resource dictionaries refuse to merge**: they share
151 GUIDs and **136** of those name different paths — core's `configs/ResourceTypes/…` against
data's `Configs/System/ResourceTypes/…` — so `rdb verify-merge` reports 136
`sameGuidDifferentPaths` and `ebin --rdb` refuses the pair
([game-data skill](../arma-reforger-game-data/SKILL.md) §4). Both paths are real entries in their
own archive; the disagreement is between the two dictionaries, not a damaged database.

**That refusal is a rule about GUID -> path, and it does not reach scripts.** `cscript` merges
nothing: it searches each `--pak` on its own, so both are passed together whenever an analysis
crosses the layers — which it almost always does, because **core's pak is where the engine's script
objects are declared**. `stats --pak "<install>/addons/core"` on 1.8.0.13: **759 `.c`, 1.7 MB,
9 051 declarations**, and **3 600 of its 5 231 methods are `proto`/`native`** — 3 600 of the 6 873
in the whole corpus (§3), so over half of "the body does not exist in script" is a declaration that
is right there, with its signature, attributes and docstring. Core also carries **4 680 of the
4 950 `GameLib` declarations** against data's 270, and `GameLib` is the layer every `Game` class
builds on:

| What core's pak declares | What the analysis loses without it |
|---|---|
| `scripts/Core/generated/Entities/IEntity.c:12-540` | the `event protected void EOn*` surface — `EOnInit`, `EOnTouch`, `EOnFrame`, `EOnVisible` — which is the answer to "who calls this hook" (§5) |
| `scripts/GameLib/generated/Components/ScriptComponent.c:23-158` | the base **172** vanilla classes name directly; without it `schema --inherited` ends with `inherited from ScriptComponent (NOT FOUND -- pass --pak/--addon for it)` |
| `scripts/GameLib/generated/Entities/GenericEntity.c`, `…/GenericController.c` | the middle of every entity's chain — `SCR_PlayerController` reaches `IEntity` through them |
| `scripts/Core/generated/UI/Widget.c`, `…/Containers/BaseContainer.c`, `scripts/Core/proto/Types.c` | `Widget`, `BaseContainer`, `Managed`: the types a signature or a data value refers to |

The price of leaving it out is a chain that stops at depth 1:

```text
$ node tools/cscript.mjs inheritance-chain "<install>/addons/data/data007.pak:scripts/Game/Player/SCR_PlayerController.c" \
    SCR_PlayerController --pak "<install>/addons/data"
0 class SCR_PlayerController : PlayerController
0     <install>/addons/data/data007.pak:scripts/Game/Player/SCR_PlayerController.c:30-1182
1   class PlayerController : GenericController
1       <install>/addons/data/data007.pak:scripts/Game/generated/Player/PlayerController.c:16-81
[warning] base class GenericController is not in the searched sources (pass --pak or --addon for it)
2 step(s) in the chain
```

The same command with `--pak "<install>/addons/core"` added is six steps, and every line names its
archive — the last four are core's `data.pak`, which is how the missing half identifies itself:

```text
2     class GenericController : GenericEntity
2         <install>/addons/core/data.pak:scripts/GameLib/generated/Entities/GenericController.c:16-18
3       class GenericEntity : IEntity
3           <install>/addons/core/data.pak:scripts/GameLib/generated/Entities/GenericEntity.c:15-194   Base entity class.
4         class IEntity : Managed
4             <install>/addons/core/data.pak:scripts/Core/generated/Entities/IEntity.c:12-540
5           class Managed
5               <install>/addons/core/data.pak:scripts/Core/proto/Types.c:112-116
6 step(s) in the chain
```

So the standing pair for a vanilla analysis is `--pak "<install>/addons/data" --pak
"<install>/addons/core"`, and `check` needs the same pair before it stops calling vanilla base
classes missing. Neither pak alone reaches the top of a chain: `schema --inherited` of
`BaseWeaponComponent` (`scripts/Game/generated/Weapon/BaseWeaponComponent.c`) ends at `inherited
from GenericComponent (NOT FOUND …)` with data alone, at `inherited from GameComponent (NOT FOUND …)`
with core alone, and answers `GameComponent (2)` and then `GenericComponent (43)` with both — each
pak supplies a different half of the same hierarchy. What must **not** be taken from that pair is
the database: pass **one** `.rdb` — the data one — to `rdb`/`ebin`, because two dictionaries that do
not merge resolve nothing. Code and GUIDs are two questions with two answers here; a reader that
conflates them loses either the chain or the GUID.

The module is the segment after `scripts/` in the entry path, and it is not decoration: a
`modded class` has to live in the same module as the original ([wiki], measured consistent —
all 203 modded declarations in the analysed addons sit in their original's module). That is why
a mod that mods `scripts/Game/...` puts its file under `Scripts/Game/...`, as all four camera
addons do.

**Mods come in two shapes, and the difference decides how you read one.** Every mod count in
this skill comes from ten downloaded addons whose scripts were read for it: ACECore,
AdvancedZeroingSystem, EchoReports, EnfusionDatabaseFramework, GRS-Patches, RHS-StatusQuo,
ServerAdminTools, TacticalFlava-Core, WCS_Core and WhereAmI — 971 `.c`, 15 711 declarations and
203 `modded` declarations between them, which is the sample the conflict numbers below are
measured on. The whole folder is much larger: `stats --addons <addons root>` on this machine's
231-addon Workshop folder reports 4 242 `.c`, 28.0 MB, 93 541 declarations, **1 072 of them
`modded`** (977 classes, 95 enums). A different ten will give different counts; nothing below
depends on these exact numbers.

| Shape on disk | How the reader sees it | What a path means |
|---|---|---|
| Workbench project: `Scripts/**/*.c` unpacked | `--addon <project dir>` | an ordinary file path |
| Downloaded addon: `addon.gproj` + `data.pak`, no unpacked tree | `--addon <addon dir>` (its `*.pak` is opened) | a **pak entry**, so `cat` needs `<addon>/data.pak:<entry>` |

That second row is where a first attempt used to die: an entry path is not a file on disk, and on
its own it does not say **which archive** holds the file — every downloaded addon ships a `data.pak`,
so one virtual path can stand for several different files. The reader prints the archive with the
entry, so what `find-defs` shows is already the `<pak>:<entry>` form `cat` takes:

```text
$ node tools/cscript.mjs find-defs SCR_CharacterCameraHandlerComponent --addons "<addons>"

SCR_CharacterCameraHandlerComponent: 15 definition(s) in 4242 file(s)

1. class SCR_CharacterCameraHandlerComponent  [modded]
   modded class SCR_CharacterCameraHandlerComponent : CameraHandlerComponent
   <addons>/ACECore_60C4CE4888FF4621/data.pak:scripts/Game/ACE_Core/Character/SCR_CharacterCameraHandlerComponent.c:3-14   (signature 3)

2. class SCR_CharacterCameraHandlerComponent  [modded]
   modded class SCR_CharacterCameraHandlerComponent : CameraHandlerComponent
   <addons>/ACECoreDev_65AD7D0D9941A380/data.pak:scripts/Game/ACE_Core/Character/SCR_CharacterCameraHandlerComponent.c:3-14   (signature 3)
```

Those two rows carry the same virtual path and are two different files; the archive is the whole
difference, and it is what `cat` needs:

```text
node tools/cscript.mjs cat "<addons>/ACECore_60C4CE4888FF4621/data.pak:scripts/Game/ACE_Core/Character/SCR_CharacterCameraHandlerComponent.c" --plain
```

Two further constraints, both measured. `--addon` is **one addon**: passing the parent
`.../ArmaReforger/addons` directory to it fails with `check needs a source: a .c file, a directory,
or --pak/--addon`, because that directory holds no `.c` and its `*.pak` files are one level down in
each addon. The option for that folder is `--addons <root>`, which reads every directory under it as
one addon — 231 addons and 4 242 `.c` on this machine, read in one scan (`stats` takes about nine
seconds). The two vanilla paks go
together, `--pak "<install>/addons/data" --pak "<install>/addons/core"` (§1 above: core is an addon
whose database does not merge with data's, and whose scripts the chain needs).

## 2. The loop: find, then look, then read the body

Every analysis of existing code is the same three steps. The reader answers the first two; the
third is the only place behaviour comes from, because bodies are skipped by the parser and
known only as a range.

1. **Find every copy.** `find-defs <Class|Class.Method|Enum|MEMBER>` over the vanilla paks
   *and* the addons involved. The original is marked `[original]`, each replacement `[modded]`,
   and every row carries the file and its line range. Without `--original`/`--only-modded` you
   get both, which is what an analysis wants: the question is almost never "where is it" but
   "how many are there".
2. **Look at the declaration.** `schema` for a class (fields and methods with visibility,
   `static`, decorators, docstring, ranges), `signature` for one method, `inheritance-chain` for
   what it derives from. `schema --inherited` appends the base classes' members, which is how a
   method that is not in the file you are reading comes into view.
3. **Read the body.** `cat <source> <from>-<to>` with the range a previous command printed.
   Inclusive on both ends, reads out of the archive without extracting 2 GB, `--plain` when the
   text is going into an answer.

`find-defs` over vanilla plus the four camera addons takes about **0.6 s** (6 691 files
searched), so there is no reason to skip step 1 and read a single copy.

A worked pass, quoting real output:

```text
$ node tools/cscript.mjs find-defs SCR_PlayerController --pak "<install>/addons/data"
SCR_PlayerController: 1 definition(s) in 5809 file(s)

1. class SCR_PlayerController  [original]
   class SCR_PlayerController : PlayerController
   <install>/addons/data/data007.pak:scripts/Game/Player/SCR_PlayerController.c:30-1182   (signature 30)

$ node tools/cscript.mjs schema "<install>/addons/data/data007.pak:scripts/Game/Player/SCR_PlayerController.c" SCR_PlayerController --members methods --limit 5
class SCR_PlayerController : PlayerController   lines 30-1182
  source   <install>/addons/data/data007.pak:scripts/Game/Player/SCR_PlayerController.c
  fields (28)
  methods (50)
    OnOwnershipChangedInvoker GetOnOwnershipChangedInvoker()   lines 71-74
    override void OnOwnershipChanged(bool changing, bool becameOwner)   lines 80-109
    override void OnInit(IEntity owner)   lines 112-119
    void OnPlayerRegistered(SCR_EditorManagerEntity managerEntity)   lines 122-131
    void OnBlockedListUpdated(bool success)   lines 134-153
    ... 45 more (--limit 0)

$ node tools/cscript.mjs signature "<install>/addons/data/data007.pak:scripts/Game/Player/SCR_PlayerController.c" SCR_PlayerController.OnOwnershipChanged
override void OnOwnershipChanged(bool changing, bool becameOwner)
  <install>/addons/data/data007.pak:scripts/Game/Player/SCR_PlayerController.c:80-109   (signature 80)
  in class SCR_PlayerController   lines 30-1182
  doc lines 77-79
    \see PlayerController.OnOwnershipChanged for more information.
```

The two ranges in the last block are what makes a method hit usable without opening the whole
class: 30 lines inside a 1 153-line one. `inheritance-chain` on the same class prints each link
and, at its head, every `modded` copy that replaces it — each line naming its own archive:

```text
0 class SCR_PlayerController : PlayerController
0     <install>/addons/data/data007.pak:scripts/Game/Player/SCR_PlayerController.c:30-1182
0 modded class SCR_PlayerController : PlayerController  [modded]
0     <addons>/ACECore_60C4CE4888FF4621/data.pak:scripts/Game/ACE_Core/Player/SCR_PlayerController.c:2-106
0 modded class SCR_PlayerController  [modded]
0     <addons>/RHS-StatusQuo_595F2BF2F44836FB/data.pak:Scripts/Game/Player/RHS_M_CallInPlayerController.c:1-129
# ... every other modded copy, then ...
1   class PlayerController : GenericController
1       <install>/addons/data/data007.pak:scripts/Game/generated/Player/PlayerController.c:16-81
```

The leading number is the depth: the class itself and every `modded` copy that replaces it sit
at 0, and the base classes follow at 1, 2, 3. A chain this class prints for
`SCR_PlayerController` is 6 steps long (`SCR_PlayerController` → `PlayerController` →
`GenericController` → `GenericEntity` → `IEntity` → `Managed`), so "what does it inherit" is a
bigger question than
the file's `: PlayerController` suggests. The archive is part of every line because it is part
of the answer: two `modded` copies of one class in two downloaded addons both declare
`scripts/Game/.../SCR_PlayerController.c`, and only the archive tells them apart.

**Size, before you parse.** A schema is a page, not the whole class: `schema --inherited` of
`CharacterControllerComponent` answers with 9.5 KB of text, 57 KB of `--json` (25 rows) or 33 KB of
`--json --compact`, and the envelope's `counts` says the real total (242 methods here) with
`truncated` set. `--limit 0` is the whole class — 517 KB as JSON, 22 KB even as text — so ask for it
when you mean it, and use `--members methods` to spend the page on the half you need. Read the text
unless something has to parse it.

## 3. What a declaration tells you, and what it does not

A schema is a map of the interface, not a description of the behaviour. These shapes decide
what can be concluded; all counts are from the 1.8.0.13 corpus.

| Shape | What it means for the analysis | How much of it |
|---|---|---|
| `proto` / `native` / `external` | engine side: the body does not exist in script, so the analysis stops at the signature. The declaration is still text — signature, `[Attribute]`s, docstring — and **3 600 of the 6 873 are in core's pak** (§1) | 6 873 `proto`/`native` methods |
| `event` | an engine-called hook. A bodyless `event int CameraSelector();` means script does not call it; the engine does | 15 bodyless `event void OnInit(IEntity owner);` declarations, and `EOnInit` in the same shape |
| `static` | dispatched on the declared type, not on the object (the wiki's `GetAge` example), so an override does not apply through a base-typed static call | — |
| `private` / `protected` | `private` members are not moddable; `protected` is the hook a mod is meant to use | — |
| `sealed` | a promise, not a fact: 355 sealed class declarations ship and **137 declarations still name a sealed class as their base**, so "sealed, therefore no subclass" is not a safe inference | 355 / 137 |
| `[Attribute(...)]` | editor and serialisation metadata. It says what the Workbench offers and what a config may set, not what the code does | — |
| `#ifdef` around a declaration | the declaration may not be compiled at all. The row carries its `conditions` | 5 892 declarations, under 53 distinct flags (`WORKBENCH`, `ENABLE_DIAG`, `AI_DEBUG` among them) |
| an empty body | a data holder (2 093 class declarations have no members), a class completed by a `modded class` elsewhere, or a placeholder | 2 093 |
| `modded` | not an interface detail at all — see §4 | 203 declarations |

Which flags a shipping build defines cannot be read from the scripts. When a declaration is
inside `#ifdef ENABLE_DIAG`, the honest answer is "this exists when `ENABLE_DIAG` is defined",
not "this exists".

## 4. `modded` is composition, not replacement

A `modded class` does not replace a file; it is spliced into the class's hierarchy at load
time. Two consequences follow, and they carry most of the analysis value in this skill.

- **`super` calls the previous copy in the chain, not the original.** With one mod they are the
  same thing. With two, the later-loaded copy's `super` reaches the earlier mod, and only
  `vanilla.X()` reaches the unmodded code ([wiki]; the keyword exists for exactly this).
- **The order is dependency-driven.** If mod2 requires mod1, mod1 loads first; between
  independent mods the order is *not guaranteed* ([wiki]). Whether the `mods[]` order in
  `server.json` also influences it is not established here — do not assert it either way.

`super` is what mods actually use: 1 173 occurrences in the ten analysed addons (3 955 in the
whole folder), against **8** code hits for `vanilla.` there (and none of them reaches the engine —
all eight are one file's variable named `vanilla`). So a mod that calls `super`
is assuming something about what sits below it, and a mod that returns without calling `super`
cuts everything below out of that call.

**One method, four mods.** `SCR_CharacterCameraHandlerComponent` (vanilla
`scripts/Game/Character/CharacterCameraHandlerComponent.c:6-1169`) is replaced by 13 addons in the
whole folder; the four below are from the ten-addon sample, and all four override `CameraSelector`:

| Copy | File and lines | Condition that returns early | Calls `super`? |
|---|---|---|---|
| vanilla | `scripts/Game/Character/CharacterCameraHandlerComponent.c:177-331` | diag view, unconscious, swimming, ADS and so on | it is the bottom of the chain — its base declares `event int CameraSelector();` |
| ACECore | `scripts/Game/ACE_Core/Character/SCR_CharacterCameraHandlerComponent.c:3-14` | `ACE_CharacterCameraCustom.IsToggledOn()` → its own camera id | only when the toggle is off |
| RHS-StatusQuo | `Scripts/Game/Camera/CustomCamera/RHS_M_CharacterCameraHandlerComponent.c:6-82` | a custom point's look-at / instant flags | always |
| TacticalFlava-Core | `Scripts/Game/Game/UI/MFD/Modded/TF_SCR_SCR_CharacterCameraHandlerComponent.c:26-85` | `m_CameraPoint` → its own camera id | always |
| WCS_Core | `Scripts/Game/Character/WCS_Core_CharacterCameraHandlerComponent.c:1-15` | a null `m_OwnerCharacter`/`m_AnimationComponent`/`m_ControllerComponent` → plain first person | only when all three are non-null |

Put any two of them in one server and the method becomes a chain, whose behaviour depends on
the order: if WCS's guard sits above ACE's toggle, a null member returns first person and ACE's
custom camera is never asked; if ACE sits above RHS, a toggled-on ACE returns before RHS can
rewrite the turret camera. Neither is a bug in either mod. This is the answer to "two mods
fight over one method": quote each copy, name the branches that skip `super`, and state the
order as the assumption the conclusion rests on.

The scale, for context: those 203 modded declarations are 179 classes and 24 enums, and **18
classes are modded by more than one of the ten** (this camera class by four,
`SCR_PlayerController`, `SCR_BaseGameMode`, `ArmaReforgerScripted` and others by three). Over the
whole folder it is 104 classes, and `SCR_CharacterControllerComponent` is modded by **21 addons** —
so "who else touches this" is not a hypothetical question on a real server.

**The members of a modded class.** 614 methods are declared inside those 179 modded classes:
353 add a name the original does not have and need no `override`; of the 261 that redeclare an
existing name, 8 omit `override` and all 8 are constructors (the class's own, e.g.
`SCR_BaseGameMode()`). That matches the wiki: constructors and destructors belong to each copy,
everything else must be an exact-signature `override`. The folder-wide numbers are the same in
shape and less tidy: 13 of 1 012 redeclarations omit `override` and only 5 of the 13 are
constructors — the rest are mods that got away with it, which is not the same as being right.

**Details worth knowing when the base clause is missing.** Three of the four modded copies
declare `modded class SCR_CharacterCameraHandlerComponent` with no `: Base` at all; only ACE
repeats `: CameraHandlerComponent`. Absence of a base clause does not mean "inherits nothing" —
the original's base governs — so do not read a missing clause as a difference. A base clause
that *disagrees* with the original is a different matter and is what `check` reports:

```text
[warning] modded class SCR_PlayerController declares base SCR_PlayerController but the original declares PlayerController
```

That one is real: `Scripts/Game/Player/RHS_TVGuidanceRelay.c:4` declares `modded class
SCR_PlayerController extends SCR_PlayerController`, a self-base. The same shape appears in
another addon with the `:` spelling, and it is one of the six defects the corpus check reports.

## 5. What the text cannot answer, and what to do instead

| Question | Why the text cannot answer it | What to do |
|---|---|---|
| Who calls this method? | there is no call graph, and some callers are not in script at all | `refs <Method> --code-only` over the same sources: it prints every *use* and marks a `[comment]` or `[string]` mention as one. Read the `event`/`proto` declaration too — `CameraSelector` has **no call site** in 6 568 vanilla files (`refs --code-only` finds only its two declarations) and is called by the engine through `event int CameraSelector();`, and the only script calls to it anywhere are the `super.CameraSelector()` lines inside the mods that override it |
| Which override runs at runtime? | it depends on the object's runtime class, on the load order (§4) and on the branch taken | reconstruct the chain from every copy, then say which order the conclusion assumes |
| What is this field's value? | the code's initialiser is only the fallback; the prefab or config may override it | read the `.conf`/`.et` with `etconf` ([game-data skill](../arma-reforger-game-data/SKILL.md) §3), and the class default with `schema` |
| Is this method server-side or client-side? | the side is decided by the replication attribute and by who owns the entity, not by the name | look for `[RplRpc(RplChannel..., RplRcver...)]` above the method and `Rpc(...)` at its call site: 497 `[RplRpc]` and 163 `[RplProp]` attributes in vanilla. The `RpcAsk_`/`RpcDo_` prefix is a strong hint but not the binding — 212 of the 217 `Rpc*_` methods carry the attribute and 5 do not |
| Which `#ifdef` flags are defined in this build? | the flags are a build input, not a resource | treat a conditional declaration as conditional, and check whether the behaviour is observable in game |
| Is this dead code? | nothing in the sources marks a method as unused, and the engine, a `.conf` or another script can call it | search for the name, then check `event`/`proto`/`[RplRpc]`/`override`; absence of a script call site proves nothing by itself |
| What happens during `OnInit` across components? | component initialisation order is engine-side | read each component's `OnInit` and report the order dependency as unresolved |

**Searching for callers.** Use `refs <name> --code-only` over the paks and the addons; it searches
inside the archives, so nothing has to be extracted, and it separates a use from a mention. Two
things still make the list readable: expect the same name in several classes (`Init` is declared in
410 classes, `OnInit` in 242), and remember that a name in a string literal is exactly what
`--code-only` drops — the flag exists because `SCR_Target` appears three times in one line and only
two of those are uses. What remains is still a text search: a call through a variable
(`controller.SomeMethod()`) is found, but which class that variable holds is a question for §4.

## 6. Recipes

**a. "What does this class do?"**
1. `find-defs <Class>` over the paks, plus the addons the user runs.
2. `schema <source> <Class> --inherited` — own members first, then the bases.
3. `signature` on the two or three methods that carry the behaviour.
4. `cat` those ranges; write down what the methods do, quoting lines.
5. If a base class matters, `inheritance-chain`.

**b. "Where is the original behind this modded class?"**
1. `find-defs <Class> --only-modded` with the addons in the search, to see the copies.
2. `find-defs <Class> --original` for the one they replace. Ask for `--only-modded` without an
   addon and the answer is `0 definition(s)` with exit 1 — correct, and easy to misread as
   "the class is not modded".
3. Read both: the mod's copy often adds a docstring the original does not have, and the
   original's body is what `super` reaches when the mod is the only one loaded.

**c. "My override does nothing."** Check in this order, because each step is cheaper than the
next and a failure at one makes the rest irrelevant:
1. The class name and file: is the mod's file in the *same module* as the original
   (`Scripts/Game/...` for `scripts/Game/...`)? §1.
2. Is the method's name and signature exactly the original's? `signature` both.
3. Is the member `private` in the original? Then it cannot be overridden — the wiki says so and
   the schema prints the visibility.
4. Does the original method exist at all, in the sources you gave `check`? Run
   `check --pak ... --addon ...`: `modded class X replaces a class that is not in the searched
   sources` means the search was too narrow, not that the class is absent.
5. Is the method actually called on the object you think? If it is an `event` hook the engine
   calls, or a `[RplRpc]` method invoked through `Rpc(...)`, a script search will not show it.
6. Is another mod loaded after yours, above it in the chain, returning without `super`? §4.

**d. "Two mods change the same method — who wins?"** Every copy with `find-defs`, read the
bodies, list the branches that skip `super`, then state the order. Answer with the chain and
the assumption, never with "mod B wins".

**e. "Is this mod consistent with this build?"** `check --pak "<install>/addons/data" --pak
"<install>/addons/core" --addons "<addons root>"` for the whole collection, or the same with
`--addon "<one mod>"` for one. It exits non-zero on **errors**; warnings only fail it under
`--strict`, so read the report rather than the exit code: the addons folder alone has 982 warnings
(and 34 errors), and one addon plus the vanilla paks adds 20 more.

**f. "How does this class differ between two builds, or between vanilla and a mod?"** Put both
sides in the same `cat` form (a file, or `<pak>:<entry>`), read the same range from each, and
diff the two blocks. The ranges will differ; compare the bodies, not the line numbers.

**g. "What is affected if this method changes?"**
1. `subclass-tree <source> <Class> --depth N`, with the addons included: every subclass, and
   the `[modded]` rows, which are the copies that replace the class itself.
2. `find-defs <Class.Method>` for every copy that redeclares it — each one is a signature that
   has to keep matching.
3. `signature` on each copy: an `override` whose signature differs is not an override at all.

**h. "Who uses this name?"**
1. `refs <name> --code-only` over the paks and the addons: the uses, each with its line.
2. `refs <name>` without the flag: the comments that explain it — often the cheapest
   documentation a mod ships, and the answer to why a workaround exists.
3. `find-defs <name>` for the declarations inside those hits. A name with one declaration and no
   use at all is dead code or engine-called, and §5 is the difference.

## 7. Traps, each measured

| Trap | What it looks like | Why it bites |
|---|---|---|
| reading one copy of a modded class | a file that reads as the definition | four copies exist; the chain, not the file, decides |
| `super` assumed to be vanilla | `super.CameraSelector()` | with two mods it reaches the other mod, which may return before your code |
| a `modded class` with no base clause | `modded class SCR_CharacterCameraHandlerComponent` | not a difference — three of the four copies write it that way |
| a self-base | `modded class SCR_PlayerController extends SCR_PlayerController` | present in a real addon; `check` warns — do not read the class name on both sides as harmless |
| `proto`/`event` methods with no body | `event int CameraSelector();` | the engine is the caller; a search finds nothing and that is the answer |
| declarations inside `#ifdef` | `#ifdef ENABLE_DIAG` in `SCR_BaseGameMode.c:140-142` | 5 892 declarations are conditional |
| a pak entry treated as a path | `cat "<addon>/Scripts/.../X.c"` → `no such file` | a downloaded addon keeps its scripts inside `data.pak` |
| `vanilla.` matched in prose | "Leave empty for vanilla." | the 4 hits in the vanilla paks are comments; the addons folder's 8 code hits are one file's variable named `vanilla` |
| 2 093 class bodies with no members | `class SCR_Foo {}` | the members are added by a mod, or the class is a data holder |
| a comment asserting vanilla behaviour | WCS's "members vanilla actually dereferences" | true here, but it had to be checked against the body |
| a ternary operator | `int n = a > 0 ? a : -a;` | not the language: the Workbench compiler rejects `? :` as a syntax error, and `check` reports it. The vanilla corpus has 767 question marks and **all** of them are in comments or strings — 0 in code — so any `?` you write is the mistake, not a shorthand |
| core's pak left out because its database does not merge with data's | `[warning] base class … is not in the searched sources`, or `inherited from ScriptComponent (NOT FOUND …)` | the merge rule is about GUIDs, not scripts: core is where half the `proto`/`native` declarations and all of `GameLib` live (§1) |

## 8. Before you hand the answer over

- [ ] Every claim about code names `file:line-line`, and the file is the one in the build the
      user runs.
- [ ] The copy count is stated: how many declarations of the class were found, in which paks
      and addons.
- [ ] Both vanilla paks were passed — `data` **and** `core` — so no base class is reported missing
      only because the second addon was skipped (§1).
- [ ] If behaviour is claimed, the body was read (`cat`), not inferred from a name or a
      docstring.
- [ ] If two mods are involved, each copy is quoted and the load order is named as the
      assumption.
- [ ] Anything the text cannot settle is listed as unresolved (§5) instead of guessed.
- [ ] `check` was run on the mod if the answer says the mod is fine.

## 9. Where the rest is

- [The game-data skill](../arma-reforger-game-data/SKILL.md) §5 — the reader's reference:
  every command and flag, the source kinds, `modded` reporting modes, the parser traps and the
  corpus counts.
- The same skill §3 and §4 — prefabs/`etconf` and resource GUIDs, for the data a script reads.
- The same skill §6 — localization, for the `#AR-…` keys a method returns.
- [tools/cscript.mjs](../../tools/cscript.mjs) — the reader itself, with its library exports
  (`parseScript`, `findDefinitions`, `schemaOf`, `ScriptUniverse`) beside the CLI.
- [AGENTS.md](../../AGENTS.md) — the repository's router, including which document answers
  which server-side question.

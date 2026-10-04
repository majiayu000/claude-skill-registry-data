---
name: uipath-core
description: Build UiPath Studio projects, REFramework scaffolds, XAML workflows, and VB/C# expressions via 104 deterministic Python generators (plus plugin generators). ALWAYS use this skill — never hand-write .xaml files. TRIGGER when the user mentions UiPath, REFramework, XAML, RPA, Orchestrator, UiPath Studio, dispatcher, performer, queue items, robot, ACME (test app), .xaml, project.json, Config.xlsx, or asks to build/generate/scaffold/automate anything resembling RPA. SKIP only when the task is explicitly Power Automate, n8n, Zapier, or non-UiPath RPA.
---

# UiPath Core Skill

> ⚠️ **Safety Rules** (I-1, I-2 in `rules.md`)
> - Playwright/browser inspection is **READ-ONLY**. Login page → STOP, WAIT for user. See `ui-inspection.md` → Login Gate.
> - Desktop inspection via PowerShell (`inspect-ui-tree.ps1`): read-only tree inspection only.
> - NEVER generate credentials, tokens, or passwords — real or fake.

Generate production-quality UiPath automation artifacts using real Studio-exported templates and comprehensive reference documentation. Template baseline: Studio 24.10 Windows.

## Hard Rule: Never Write .xaml by Hand

If you are about to use the Write tool with a `.xaml` extension, STOP. Every .xaml file in this skill MUST come from `python -m uipath_core.scaffold_project` or `python scripts/generate_workflow.py`. Hand-written XAML bypasses lint rules 1–122 and produces unrunnable workflows. If generator output is wrong, fix the JSON spec — do not edit .xaml manually except for narrow `modify_framework.py` operations.

This rule overrides any plan you would have produced from training memory.

## Planning Workflow (read this BEFORE drafting any plan)

When the user hands you a PDD, requirements doc, or "build a UiPath project that does X" — STOP before drafting architecture. Read this section first; it overrides any plan you would have produced from training memory. The full text of every gate below lives in `references/scaffolding.md` § "Generating a Full Project" — this is the planner-side hoist.

### PLAN SELF-CHECK — answer BEFORE presenting your plan to the user

- [ ] For EACH workflow in my plan: does it implement the PDD's specified approach, or did I substitute a "better" alternative? (e.g., InvokeCode SHA1 instead of browser automation of sha1-online.com)
  → If ANY substitution exists: REMOVE it and implement the PDD way. Propose the alternative AFTER.
- [ ] Does my plan include an explicit inspection step for EVERY target app?
  → Browser apps: "Inspect [app] with Playwright" (if Playwright MCP available)
  → Desktop apps: "Inspect [app] with PowerShell" (if PowerShell available on Windows)
  → If ANY app lacks an inspection step and the tool is available: ADD it now.

If you cannot answer YES to all checks, revise your plan before presenting it.

**Echo-back requirement:** the produced plan MUST contain a `PLAN SELF-CHECK:` block (in Phase 0 or as Phase 0.5) with two `✓` lines, one per box, naming the specifics — for example:

```
PLAN SELF-CHECK:
  ✓ No PDD substitutions — SHA1 computed via sha1-online.com browser flow as PDD specifies
  ✓ Phase 2 includes inspection for every target app: System1 + SHA1Online
```

For a single-app or non-UI process, the second line still appears — e.g. `✓ Phase 2 explicitly notes no UI inspection required (no browser/desktop apps in scope)`. A plan without this echo-back block is incomplete; revise before presenting.

### PLAN OUTPUT FORMAT — present your plan using this structure

```
Phase 0:  Architecture decision — Sequence vs Dispatcher+Performer (P-2); A-1 wiring
Phase 1:  Workflows + arguments — one entry per .xaml with In/Out/InOut signatures
Phase 2:  EACH app to inspect — one bullet per target app, e.g. "Inspect acme-test.com with Playwright"
Phase 2b: Write selectors.json (apps → screens → elements with taxonomy_type)
Phase 2c: generate_object_repository.py --from-selectors selectors.json --project-dir <each project>
Phase 2d: Pass --project-dir to every generate_workflow.py call (auto-wires obj_repo refs)
Phase 3:  Generate sub-workflows ONE AT A TIME — validate_xaml --lint after EACH file
Phase 3b: modify_framework.py wire-uielement <project> <AppName> for EACH app with UI
Phase 3c: (Dispatcher only) wire SCAFFOLD.DISPATCHER_GET_ITEM marker — generate snippet first (G-3)
Phase 4:  Wire Main.xaml — orchestration only, log bookends (A-7)
Phase 5:  Project-level validation — validate_xaml <project_folder> --lint
Phase 6:  Output Config.xlsx required keys grouped by sheet — validate_xaml --config-keys <project>
```

**If Phase 2 is empty or missing, you are violating the skill rules.** Even when no UI inspection is needed (no browser/desktop apps), state that explicitly: `Phase 2: no UI inspection required (no browser/desktop apps in scope)`.

### Per-phase reference anchors

| Phase | Read before completing |
|---|---|
| 0 | `scaffolding.md` → CRITICAL: Architecture Selection for PDDs (P-2) |
| 1 | `decomposition.md` → Universal Rules 1–8, naming + arguments (Rule 8 = credentials) |
| 2 | `ui-inspection.md` → Playwright MCP workflow + Login Gate (I-2); `ui-inspection-reference.md` for desktop |
| 2b | `cheat-sheet.md` → `selectors.json` schema |
| 2c | `scripts/generate_object_repository.py` (Lint 94 is ERROR if skipped) |
| 2d | `generation.md` → Wiring Object Repository References |
| 3 | `cheat-sheet.md` → JSON spec patterns; `scripts/generate_workflow.py` (Rules G-1, G-2) |
| 3b | `scripts/modify_framework.py wire-uielement`; `decomposition.md` § UiElement chain |
| 3c | `scripts/modify_framework.py replace-marker SCAFFOLD.DISPATCHER_GET_ITEM` (Rule G-3) |
| 4 | `decomposition.md` § Login/Launch + REFramework wiring; A-7 log bookends |
| 5 | `scripts/validate_xaml <project> --lint` |
| 6 | `scripts/validate_xaml --config-keys <project>`; `config-sample.md` |

### Config layout rule of thumb

When listing required Config.xlsx keys (Phase 6), apply this rule before falling back to `config-sample.md`'s decision flowchart:

- **URLs, API endpoints, file/network paths, shared values across projects, or anything whose value may change frequently → Assets sheet.** They are environment-specific, fetched from Orchestrator at `InitAllSettings`, and admins update them without redeploying. If you expect the value to be tuned post-deployment (timeouts, thresholds, recipient lists, feature flags, batch sizes), it belongs here too — Settings/Constants require a redeploy to change.
- **Credential asset NAMES → Settings sheet.** The string in the cell is just a name passed to `GetRobotCredential`; storing it in Assets would trigger a needless `GetRobotAsset` round-trip. The credential value itself never appears in Config.xlsx — fetch it at point of use.
- **Project identity (queue name, process name, processes-to-kill list) → Settings sheet.** Local to the project, never changes per environment.
- **Framework knobs (retry counts, log message templates) → Constants sheet.** Identical across dev/staging/prod.

`validate_xaml --config-keys <project>` auto-classifies via this rule and emits a per-key reason — review the suggestion before manually editing Config.xlsx.

**Compat-v2 (version-band) requirement — ENFORCED:** every `scaffold_project.py` invocation MUST include `--band <stable_year>` (e.g., `--band 25`). To pick the band: run `python scripts/resolve_nuget.py --all` and read the major year of `UiPath.System.Activities` in the output — that's the latest stable. Available band profiles live under `references/version-profiles/UiPath.System.Activities/<year>.<minor>.json`. Every dependency MUST be resolved via `python scripts/resolve_nuget.py <package>` — no version literals from training memory (G-5). If `project.json` is generated without `versionBand`, lints 120–122 will REJECT it. The 23.10.x and 24.x bands are end-of-life and MUST NOT be used for new projects in 2026.

### Final gate

If you are about to present an architectural plan and have NOT produced a `Phase 2:` inspection list with one entry per target app (or an explicit "no UI in scope" line), you are violating skill rules — go back and add Phase 2 first.

## When To Read Which Reference

**Start here.** Match the user's task to the right file, then read only what's needed. For files > 200 lines, use `grep` or line-range reads — never read entire large files or XAML assets.

### Common Tasks (check these first)

| Task | Read first |
|---|---|
| Generate a XAML workflow (any kind) | `cheat-sheet.md` → JSON spec patterns → `scripts/generate_workflow.py` **(G-1)** |
| Scaffold a project | `scaffolding.md` → Template Selection → run `scripts/scaffold_project.py` |
| **Plan a new project (PDD → architecture)** | `scaffolding.md` → PLAN SELF-CHECK & Phase 0–6 (**READ BEFORE PLANNING**) |
| Inspect a web app (selectors) | `ui-inspection.md` → Playwright MCP workflow → `playwright-selectors.md` |
| Validate XAML | Run `scripts/validate_xaml <project> --lint` |
| Fix a specific lint warning | `lint-reference.md` → search by lint number |
| Write an expression (VB.NET/C#) | `expr-foundations.md` (start here for any expression task) |
| Decomposition / project structure | `decomposition.md` → Decomposition rules (Universal 1-8, Browser 9-13, Desktop 14) |
| Fix a user's .xaml file | `skill-guide.md` → Example 6 |
| Tasks, form tasks | **→ uipath-tasks skill** (read its `SKILL.md`) |

### Activity-Specific Reference

| Task | File | Section guidance (for large files) |
|---|---|---|
| **Pick the right activity for an intent** | `references/routing-index.md` (auto-generated) | Grep for the user's intent or the closest activity name. Don't guess generator names from filenames. |
| Core activities (Assign, Log, Delay, InputDialog) | `xaml-foundations.md` (165 lines) | Read in full |
| Control flow (If, ForEach, While, Flowchart) | `xaml-control-flow.md` (208 lines) | Read in full |
| DataTable ops, file system | `xaml-data.md` (255 lines) | Grep for activity name |
| Error handling, TryCatch, Throw, RetryScope | `xaml-error-handling.md` (194 lines) | Read in full |
| InvokeWorkflowFile, InvokeCode, InvokeMethod | `xaml-invoke.md` (175 lines) | Read in full |
| Orchestrator, queues, HTTP, credentials | `xaml-orchestrator.md` (293 lines) | Grep for activity name |
| Excel, Email, PDF activities | `xaml-integrations.md` (285 lines) | Grep: `## Excel`, `## Email`, or `## PDF` |
| Build/fix selectors | `xaml-ui-automation.md` (576 lines) | **Don't read in full.** Grep: `## Selector Reference` or specific selector type |
| UI automation XAML (NClick, NTypeInto, etc.) | `xaml-ui-automation.md` | **Selector guidance only.** XAML generation via `generate_workflow.py` **(G-1)** |

### Expression Reference (large files — use targeted reads)

| Task | File | Section guidance |
|---|---|---|
| DataTable expressions (Select, Compute, LINQ) | `expr-datatable.md` (432 lines) | Grep: `## Select`, `## Compute`, `## LINQ`, `## Filter` |
| String/DateTime/numeric expressions | `expr-strings-datetime.md` (502 lines) | Grep: `## String`, `## DateTime`, `## Numeric`, `## Regex` |
| JSON, collections, type conversions | `expr-collections-json.md` (462 lines) | Grep: `## JSON`, `## Dictionary`, `## List`, `## LINQ` |

### Project & Configuration

| Task | Read first |
|---|---|
| Choose template or variant | `scaffolding.md` → Choosing the Right Variant |
| Browser automation with Playwright | `ui-inspection.md` → Playwright MCP workflow |
| Desktop app inspection | `ui-inspection.md` → Desktop Inspection → `ui-inspection-reference.md` |
| Login/Launch pattern | `decomposition.md` → Login/Launch section |
| Config.xlsx keys and structure | `config-sample.md` → three-sheet reference, decision flowchart |
| Extract Config keys from project | Run `validate_xaml <project> --lint` — lint 39 |
| Lint regression tests | Run `scripts/run_lint_tests.py` |
| Ground rules (all rule definitions) | `rules.md` — single source of truth for G/I/A/P/S rules |
| project.json schema and configuration fields | `scaffolding.md` → Key project.json Configuration Fields |

## Ground Rules

> **Full rule definitions with rationale:** `references/rules.md`. Rules below are referenced by ID.

1. **G-4** — Never generate XAML from scratch. Copy from closest template and modify.
2. **G-5** — Never guess NuGet package versions. Run `scripts/resolve_nuget.py`.
3. **G-1** — ⛔ Create .xaml files ONLY via `scripts/generate_workflow.py`. Never hand-write. See `generation.md` § Workflow Generation CLI.
4. **P-1** — Follow the PDD exactly. Implement the specified approach faithfully — propose alternatives separately.
5. **P-2** — Architecture selection: PDD describes BOTH reading AND processing items? → Dispatcher + Performer. See `scaffolding.md`.
6. **A-5** — Modular decomposition. Break into `Workflows/<AppName>/` subfolders. See `decomposition.md`.
7. **I-2** — ⛔ HALT at login gates during Playwright inspection. End your response, wait for user.
8. **G-3** — ⛔ Framework wiring: GENERATE FIRST, WIRE SECOND. Snippets MUST come from generator output. See `scaffolding.md` Phase 3c.
9. **G-2** — ⛔ JSON specs: WRITE TO DISK, NEVER INLINE. See `cheat-sheet.md` § type keys for valid types.

## CRITICAL: Project Context Check (Always Do This First)

Before generating ANY XAML, determine project context:

**A) project.json EXISTS (inside existing project):**
- Generate the .xaml file inside the project directory
- Check `dependencies` — add missing NuGet packages: `python3 scripts/resolve_nuget.py --add <project_dir> PackageName`

**B) project.json DOES NOT EXIST:**
- Scaffold first — a standalone .xaml is useless without project.json
- Use `scripts/scaffold_project.py` (see `scaffolding.md`)
- **Do NOT create the project folder before scaffolding.** The script creates `<o>/<n>/` automatically. Pre-creating causes duplicate nesting.

## Capabilities

1. **Generate XAML workflow files** — copy from real Studio exports and modify
2. **Scaffold UiPath projects** — Simple sequence, REFramework Dispatcher, or REFramework Performer
3. **Write expressions** — VB.NET and C# for UiPath activities (LINQ, DataTable, JSON, DateTime, etc.)
4. **Build selectors** — strict, fuzzy, dynamic, wildcard, regex selectors for web/desktop/SAP
5. **HTTP API integration** — OAuth token flows, retry policies, query parameters, response handling
6. **Tasks tasks** — **→ Fully decoupled to uipath-tasks skill** (generators, lint rules, scaffold hooks all live in `uipath-tasks/extensions/`, loaded via `plugin_loader.py`)
7. **UI automation** — NApplicationCard, NClick, NTypeInto, NSelectItem, NGetText, Extract Table Data, Check App State — **via `scripts/generate_activities`**
8. **Error handling & workflow** — TryCatch, RetryScope, Throw/Rethrow, InvokeWorkflowFile, AddQueueItem, GetRobotCredential, BuildDataTable, IfElseIfV2, MultipleAssign — **via `scripts/generate_activities`**
9. **File system operations** — Copy/Move/Delete files, Create Directory, Path Exists
10. **Invoke Code/Method** — inline C#/VB.NET code blocks, instance/static method calls

## Reference Files

| File | Coverage |
|---|---|
| `references/xaml-foundations.md` | XAML file structure, namespace declarations, core activities (Assign, Log, InputDialog, MessageBox, Delay), variable & argument declarations |
| `references/xaml-control-flow.md` | If, IfElseIf, ForEach, ForEachRow, While, DoWhile, Break/Continue, ForEachFile, Flowchart, State Machine, annotations |
| `references/xaml-data.md` | BuildDataTable, AddDataRow, FilterDataTable, MergeDataTable, SortDataTable, OutputDataTable, JoinDataTables, LookupDataTable, DeserializeJSON, file system ops |
| `references/xaml-error-handling.md` | TryCatch, Throw/Rethrow, exception types, RetryScope (incl. NCheckState condition) |
| `references/xaml-invoke.md` | InvokeWorkflowFile, InvokeCode, InvokeMethod |
| `references/xaml-orchestrator.md` | GetRobotAsset, GetRobotCredential, AddQueueItem, GetQueueItem, SetTransactionStatus, HTTP Request. **Tasks → uipath-tasks skill** |
| `references/xaml-integrations.md` | Excel Classic Workbook (ReadRange, WriteRange, WriteCell), Email/Integration Service (GetIMAP, SendMail), PDF (ReadPDFText, ReadPDFWithOCR) |
| `references/xaml-ui-automation.md` | Selector construction, dynamic selectors, fuzzy/regex, anchor targeting, desktop frameworks, Version table. **For XAML generation use generators** — this file is for selector guidance and activity property reference. **Large file — use grep or line-range reads.** |
| `references/expr-foundations.md` | VB.NET + C# expression syntax, null safety patterns. Read first for any expression task |
| `references/expr-datatable.md` | DataTable operations: Select, Compute, filter, sort, lookup, merge, clone, column ops, row iteration. **Large file — grep for section.** |
| `references/expr-strings-datetime.md` | String (split, join, trim, replace, format), DateTime (parse, format, diff, business days), file/path, numeric, regex. **Large file — grep for section.** |
| `references/expr-collections-json.md` | Array/List, Dictionary, JSON (JObject, JArray, parse, query, build), LINQ on typed collections, type conversions, Queue Item. **Large file — grep for section.** |
| `references/routing-index.md` | **Activity selection index** — auto-generated from `references/annotations/*.json`. Maps user intent → generator with `description` + `use_when` per activity, plus a "don't auto-generate" section listing wizard-only activities. **Consult this BEFORE guessing a generator name.** Regenerate with `uipath-core/scripts/generate_routing_index.py`. |
| `references/golden-templates.md` | Template catalog — patterns extracted from each real template file |
| `references/scaffolding.md` | Template selection, NuGet mapping, XAML validation, project scaffolding (variants, dispatcher/performer, transaction types), full project generation checklist |
| `references/decomposition.md` | Naming conventions, decomposition rules (universal 1-8, browser 9-13, desktop 14), common process patterns, argument design, Login/Launch pattern, REFramework Init/Close, UiElement chain |
| `references/generation.md` | Object Repository, Workflow Generation CLI (JSON spec format, 104 core generators + plugin extensions), Activity Generators (usage pattern, what model provides vs what generators lock down) |
| `references/ui-inspection.md` | Playwright MCP workflow (login gate, 5-step process, element mapping), Desktop inspection (PowerShell, inspect-ui-tree.ps1, framework detection) |
| `references/skill-guide.md` | **Index + examples.** Routes to scaffolding/decomposition/generation/ui-inspection. Contains 7 worked examples + anti-example |
| `references/lint-reference.md` | **85 lint rules** by severity, searchable by lint number (core rules; plugins add more — `uipath-tasks` registers AC-26..AC-34) |
| `references/playwright-selectors.md` | Playwright MCP → UiPath selector mapping |
| `references/config-sample.md` | Config.xlsx three-sheet reference (Settings, Constants, Assets), key naming conventions, sheet placement decision flowchart, required keys output format |
| `references/cheat-sheet.md` | JSON spec patterns (multiple_assign, if, try_catch, foreach_row, pick_login_validation, filter_data_table, add_queue_item, selectors.json), modify_framework.py CLI+Python API, valid enum values, naming, quick rules |
| `references/cheat-sheet.md` § Desktop Form-Filling | Desktop form-filling: tab nav, idx selectors, save verification, data externalization |
| `references/ui-inspection-reference.md` | `inspect-ui-tree.ps1` reference — UIA→UiPath property mapping, framework detection, WinForms |
| `references/rules.md` | **Ground Rules Reference** — single source of truth for all generation (G), inspection (I), architecture (A), PDD (P), SAP (S), and skill authoring (K) rules. Other docs reference by ID |

### Scripts

> **All `scripts/` paths below are relative to this skill's directory (`.claude/skills/uipath-core/`).**
> Invoke from the skill root: `cd .claude/skills/uipath-core && python3 scripts/<script>.py ...`

| File | Purpose |
|---|---|
| `scripts/validate_xaml` | Validate generated XAML — structural checks + lint rules (core + plugin). Use `--golden` for asset templates. See `lint-reference.md` for full rule table. |
| `scripts/resolve_nuget.py` | **Resolve real NuGet versions.** Query UiPath feed for latest stable. Validate project.json. Add/update deps in existing project.json (`--add`). |
| `scripts/scaffold_project.py` | Scaffold UiPath projects (sequence / dispatcher / performer). Customizes Config.xlsx. Dispatcher replaces GetQueueItem with DataTable row indexing. |
| `scripts/config_xlsx_manager.py` | Add/list/validate Config.xlsx keys. Cross-references XAML Config() refs vs actual sheets. |
| `scripts/modify_framework.py` | Insert InvokeWorkflowFile into framework files, replace SCAFFOLD.* markers, **wire UiElement argument chain** (`wire-uielement`), **add variables with auto type normalization** (`add-variables`), **replace placeholder expressions** (`set-expression`). ⛔ G-8: Never Edit/Write .xaml directly — use this script or `generate_workflow.py`. |
| `scripts/generate_activities` | **Deterministic XAML generators** for 95 core activities. Locks down enums, versions, child elements. MANDATORY for NTypeInto, NClick, NGetText, NCheckState, NApplicationCard, etc. Plugin skills add more (e.g., Tasks, SAP WinGUI). |
| `scripts/generate_workflow.py` | **Generate complete .xaml files from JSON specs.** 104 core generators + plugin generators loaded via `plugin_loader.py`. Covers ALL activities including Pick login validation, TryCatch, ForEachRow, NExtractData, NCheckState. **Pass `--project-dir <project>` to auto-wire Object Repository references** (`Reference=`/`ContentHash=` on TargetAnchorable) from `.objects/refs.json`. ⛔ Do NOT write .xaml by hand — use this CLI instead. |
| `scripts/generate_object_repository.py` | **Generate Object Repository** (`.objects/` tree). CLI: `python3 generate_object_repository.py --from-selectors selectors.json --project-dir <dir>`. Reads `selectors.json` (written during Playwright inspection) with full app/screen/element hierarchy. Lint 94 is ERROR — project cannot pass validation without populated Object Repository. |
| `scripts/inspect-ui-tree.ps1` | **Windows-only.** Inspect desktop app UI tree via UIA API. Run via Bash (`powershell -File`). |
| `scripts/regression_test.py` | Regression tests — validates templates, scaffolding, naming conventions, line count accuracy, skill integrity |
| `scripts/run_lint_tests.py` | Lint regression: verifies bad XAML test cases trigger expected lints. Run after modifying lint rules. |

#### Battle-test scripts (manual-only)

`scripts/battle_test_studio.py` and `scripts/battle_test_activities.py` are **NOT run by CI** and have side-effects: they shell out to `uip rpa create-project`, scaffold real UiPath Studio Desktop projects under the system temp dir, and invoke Studio via IPC. Run them manually after generator changes (to confirm Studio still accepts the produced XAML) and before cutting a release. Requirements: UiPath Studio Desktop installed locally, `@uipath/cli` (`npm i -g @uipath/cli`) on PATH, and a free Studio editor process available for IPC. Pair with `scripts/grade_battle_test.py` to score the resulting projects.

## Key Architecture Rules

> Full definitions: `references/rules.md` § Architecture Rules (A-1 through A-12).

**App initialization (A-1):** ALL apps open and ready by end of `InitAllApplications.xaml`. Action workflows ONLY attach (`OpenMode="Never"`). Wire UiElement chain: `python3 scripts/modify_framework.py wire-uielement <project> <AppName>`.

**Key constraints:** no flat files in `Workflows/` (must be in app subfolders), login stays inside `AppName_Launch.xaml` (no separate `AppName_Login.xaml`), navigation uses shared `Utils/Browser_NavigateToUrl.xaml` **(A-6)**, persistence activities stay in Main.xaml **(A-2)**, `SetTransactionStatus.xaml` never modified **(A-4)**, dispatchers pass `Nothing` for `in_TransactionItem`.

### Login/Launch Workflow Pattern

See `decomposition.md` → "Login/Launch Workflow Pattern" for the full recipe, required XAML structure, argument design, UiElement reference chain, and common mistakes. Key rule: **login stays inside `AppName_Launch.xaml`** — NEVER create a separate `AppName_Login.xaml`. Copy structure from golden sample `WebAppName_Launch.xaml`.

## Quick Validation Reference

For detailed lint rules by number, see `lint-reference.md`. The most critical categories:

**🔴 Studio crash** — Inline `Result=` on modern activities, hallucinated enum values (`AttachMode="ByUrl"`, `Version="V3"/"V4"`, `ElementType="InputBoxText"`), missing xmlns declarations, hallucinated properties (`NApplicationCard Url=`, `NCheckState Appears=`, `NTypeInto EmptyField=`, `AddQueueItem.SpecificContent`). See `cheat-sheet.md` → Valid Enum Values.

**🟡 Compile error / silent data loss** — Wrong enum namespace (`UIAutomation` vs `UIAutomationNext`), C# syntax in Throw expressions, `InteractionMode` on activities that don't support it (only NClick/NTypeInto have it), `QueueName=` instead of `QueueType=`, empty Out/InOut argument bindings, direction tag mismatches.

**🟢 Production / security** — Credentials via `GetRobotCredential` inside the workflow (never as arguments), API/network wrapped in RetryScope, URLs from Config (never hardcoded), browser `IsIncognito="True"`, log bookends on every workflow.

## Desktop App Automation

When automating a **desktop application** (not browser/web):

1. **Get the executable path first.** Before generating NApplicationCard XAML, you MUST have the full `.exe` path. Never use placeholders. ASK → STOP → WAIT. UWP apps use the package AppId.

2. **Desktop vs Browser differences:** Desktop uses `TargetApp.FilePath` (no `BrowserType`/`Url`/`IsIncognito`), `InteractionMode` = `HardwareEvents` or `Simulate` (NOT `DebuggerApi`). Selectors use `<wnd app='...' />` with `automationid`, `cls`, `aaname`, `role` attributes.

3. **Inspection is mandatory** when PowerShell is available (Windows) — run `inspect-ui-tree.ps1` BEFORE generating desktop XAML.

4. **WinForms tab names vs group box names:** When `inspect-ui-tree.ps1` shows a TabControl, children at depth 2 are TabItems (actual tab names for navigation). Children at depth 3 are GroupBoxes (visual containers INSIDE a tab, NOT navigation targets). See `decomposition.md` → Rule 14 supplement and `ui-inspection-reference.md` → WinForms Tab Control Hierarchy.

## Naming Conventions

**Variables:** camelCase with type prefix — `strName`, `intCount`, `boolSuccess`, `dt_Report`, `dr_Row`, `arr_Files`, `dict_Config`, `dtmStart`, `dblAmount`, `jo_Response`, `secstrPassword`, `qi_Item`, `mm_Mail`.

**Arguments:** `{direction}_{typePrefix}{Name}` — `in_strUserName`, `out_boolSuccess`, `io_dt_Data`.

**Workflow files:** PascalCase with underscores — `WebApp_CreateRecord.xaml`, `App_Close.xaml`.

See `cheat-sheet.md` → Naming Quick Reference for the full type prefix table.

## Selectors — Always Default to Strict

Generators default to `SearchSteps="Selector"` (strict). Use `FuzzySelector` only when user requests or strict proven unreliable. Always populate BOTH `FullSelectorArgument` and `FuzzySelectorArgument`.

## Tested Models

This skill is developed and tested with **Claude Opus** and **Claude Sonnet**. The prompt engineering (HALT semantics, routing table placement, urgency tiers) is Claude-optimized. Other LLMs may work but are untested — expect to adapt the prompt layer.

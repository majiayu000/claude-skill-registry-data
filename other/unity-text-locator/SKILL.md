---
name: unity-text-locator
description: Safely localize unknown Unity games, especially Japanese-to-Chinese projects. Use to discover Unity version/layout/backend, migrate translations across game versions, extract occurrence-mapped text from serialized assets, embedded CSV, bytecode, UI, Localization StringTables, Utage, or middleware, bridge rows through AiNiee-style translation, validate and transactionally write approved candidates, audit residual and runtime-only text or AutoTranslator diffs, diagnose TMP fonts and Addressables/IL2CPP failures, locate saves, or acceptance-test SHA-verified patches.
---

# Unity Translation Workflow

## Operating Principle

Treat each Unity game as a separate format-discovery task. Do not assume that a previous game's extraction boundary, scenario layout, writeback method, or font injection strategy applies to the current game.

1. Inspect the build and locate actual display-text sources.
2. Select the smallest applicable adapter.
3. Extract project-named, one-column text files.
4. Ask for matching one-column translation files.
5. Validate row alignment and structural tokens; blank only row-addressable failures when the user elects partial writeback.
6. Dry-run, prove source-specific serialization/runtime safety, build candidates outside the game root, back up, then write only approved rows.
7. Run the same source-specific residual audit on the composed final candidate; resolve every visible candidate and rerun until zero unreviewed visible occurrences remain.
8. Build a SHA-verified binary patch only from pristine originals to that final runtime-tested candidate.

Use three gates for every project:

- Discovery gate: report Unity version/layout, Mono versus IL2CPP, Addressables, middleware clues, and all candidate text sources before choosing an adapter.
- Translator gate: expose only project-named one-column CSVs for row-mapped sources; keep broad `extracted_text.csv` as audit evidence, not as a writeback source.
- Runtime gate: a clean CSV validation and a tool-level dry run are not enough for runtime-sensitive containers; prove the edited file loads through the same game path before distributing it.

Prefer static occurrence-mapped writeback. Use a runtime text adapter only for confirmed visible strings that static discovery cannot reach, and keep its global key-based output separate from static manifests and writeback artifacts.

Read [references/unity-text-map.md](references/unity-text-map.md) when locating candidate Unity text containers or middleware clues.
Read [references/runtime-sensitive-adapters.md](references/runtime-sensitive-adapters.md) when handling BansheeGz databases, Addressables bundles/catalogs, ES3 saves, or runtime font compatibility.
Read [references/workflow-modes.md](references/workflow-modes.md) before choosing semi-automatic or full-automatic translation.
Read [references/ainiee-integration.md](references/ainiee-integration.md) before running full-automatic translation through `ainiee-translate`.
Read [references/mono-raw-residual.md](references/mono-raw-residual.md) when TypeTree reading fails, an embedded Utage book is incomplete, or visible Japanese survives normal writeback.
Read [references/font-asset-replacement.md](references/font-asset-replacement.md) before selecting, converting, or replacing any TMP font asset or font bundle.
Read [references/runtime-text-adapters.md](references/runtime-text-adapters.md) before generating or testing an AutoTranslator candidate for IL2CPP, Naninovel, GameCreator, custom-rendered, or runtime-only text.
Read [references/version-migration-and-release-audit.md](references/version-migration-and-release-audit.md) when porting a translation to a newer game version, separating scratch candidates from durable project evidence, selecting a runtime Locale/StringTable, auditing short bytecode choices or residual Japanese, choosing static CJK font coverage or smoke-test depth, or preparing a release-only patch baseline.
Read [references/embedded-csv-and-runtime-diff.md](references/embedded-csv-and-runtime-diff.md) when Naninovel-like CSV data is embedded in assets or when comparing runtime AutoTranslator captures.

Public repository release notes belong in GitHub Releases. Do not add `CHANGELOG.md` to the GitHub repository.

## Workflow Modes

Semi-automatic mode extracts Unity text and waits for matching `*_translation.csv` files before validation and writeback.

Full-automatic mode extracts Unity text, converts each source CSV to an AiNiee `cache.json`, lets the agent translate through the sibling `ainiee-translate` skill, converts the cache back to `*_translation.csv`, then runs the same Unity validation and writeback gates. Full-auto only automates translation; it does not bypass row alignment, structural validation, source hashes, dry runs, backups, or runtime checks.

## Work Directory

Keep work products under the game root:

```text
GameFolder/_translation/unity-text-report/
  report.md
  extraction_manifest.json
  text/
    GameTitle_text.csv
    GameTitle_text.manifest.json
    GameTitle_text_translation.csv
    GameTitle_ui_text.csv
    GameTitle_ui_text.manifest.json
    source_text_index.json
  validation/
  runtime/
    autotranslator/
  writeback/
  backups/
```

`scan_unity_text.py` and `extract_unity_text.py` default to this directory and ignore `_translation` while scanning. Put distributable patch archives outside the game directory only after verification.

Reports, manifests, and CSVs may live under `_translation`, but rebuilt bundles, catalogs, font assets, and other runtime binary candidates must be written to a separate candidate root outside the game directory. Applying a candidate is a distinct, backed-up step.

## Translator File Contract

Use one source file and one translation file per extracted Unity source. Name translator-facing files with the project folder name followed by a short semantic description, not the internal Unity asset path:

```text
<ProjectFolderName>_<description>.csv
```

Use `<ProjectFolderName>_text.csv` for the primary story/dialogue text source when it is clear, and descriptions such as `_ui_text`, `_utage_text`, `_profiles_text`, or `_resources_text` for additional or generic sources. For example:

```text
M男いじめスクールライフ_text.csv
M男いじめスクールライフ_ui_text.csv
```

Source file generated by extraction:

```csv
original_flat
...
```

Translation file provided after translation:

```csv
zh_cn
...
```

Name the translation by appending `_translation` to the source CSV stem:

```text
M男いじめスクールライフ_text.csv
M男いじめスクールライフ_text_translation.csv
```

Rules:

- Keep one translated cell for every source row; do not reorder or delete rows.
- Keep duplicate source rows. Each row identifies one specific occurrence and may receive a different action.
- Leave `zh_cn` blank to preserve that occurrence in the game.
- Keep resource paths, `path_id`, offsets, and source hashes in the manifest only; do not expose them in the translator-facing CSV filename.
- Preserve TMP/Unity tags, placeholders, and literal `\n` markers unless a verified parser-specific change is required.
- A headerless one-column translation file is accepted. Generated/normalized output uses the `zh_cn` header.
- Do not edit `*.manifest.json`; it maps CSV rows to source-file occurrences and stores the extracted file hash.

Legacy `original_flat,zh_cn` translation files remain accepted by validation/writeback for existing projects, but do not create new projects in that format.

## Choose An Adapter

| Evidence | Use now | Status |
| --- | --- | --- |
| `level*`, `resources.assets`, `sharedassets*.assets`, `globalgamemanagers`, bundle candidates with serialized UTF-8 text | `scan_unity_text.py`, generated per-source manifests, `writeback_unity_text.py` | Automated row-mapped workflow |
| Broad `extracted_text.csv` contains mixed visible/internal rows and needs manual narrowing | `build_visible_safe_extract.py`, then `project_translation_to_subset.py` if an existing legacy baseline must be projected | Audit/subset workflow; not a row-mapped writeback source |
| Raw profile/encyclopedia MonoBehaviour strings missed by the normal pass | `extract_character_profiles.py`, `writeback_character_profiles.py` | Automated one-column workflow |
| Utage `ALL_Texts.book` / `ALL_EventTexts.book` in scenario assets or embedded assets | `extract_utage_scenarios.py`, `writeback_utage_scenarios.py` | Automated one-column workflow after confirming text column/books |
| MonoBehaviour TypeTree fails, embedded Utage data is skipped, or Japanese remains after writeback | `extract_mono_raw_utf8.py`, occurrence approval, `writeback_mono_raw_utf8.py` | Two-stage raw-object audit; exact controls; external canary only when object spans resize |
| `bansheegz_database` TextAsset plus `BGDatabase.dll`/`BansheeGz.BGDatabase` | Build a one-shot game-runtime export/write/save probe and reinsert the verified payload | Runtime-specific structured adapter |
| Loose CSV/JSON/TXT or custom scenario string parsers | Inspect format and preserve its record/newline contract | Project-specific |
| `0x06 + uint32 LE + UTF-8` length-prefixed records, often near a `DMSL` signature | `extract_dmsl_text.py`, `writeback_dmsl_text.py` | Fixed-byte occurrence workflow; byte budget is blocking |
| TMP/UI `m_text`, label fields, or Unity Localization `m_TableData.*.m_Localized` | `extract_typetree_ui_text.py`, `writeback_typetree_ui_text.py` | TypeTree occurrence workflow with field-path verification |
| Addressables catalogs/bundles or IL2CPP `global-metadata.dat` | Confirm exact runtime text, integrity metadata, and game-runtime loading before applying candidates | Project-specific |
| Confirmed UGUI/TMP/IMGUI/TextMesh strings exist only at runtime, including IL2CPP, Naninovel, or GameCreator resolution | Validate the row-mapped CSV, then use `generate_autotranslator_txt.py`; provision any compatible loader/plugin separately | Optional global key-based candidate; no automatic deployment |
| Rebuilt Addressables bundle loads to a black screen or logs CRC mismatch | `patch_addressables_catalog_crc.py`, then paired bundle/catalog canary | Binary catalog candidate; unique internal-name match only |
| Chinese displayed as boxes/tofu in Mono/TMP games with JSON injection tables | `install_tmp_chinese_font_fix.py --dry-run`, then apply | Preflighted runtime fallback workflow |
| TMP font bundle candidate for resource-level replacement | `trace_tmp_font_usage.py`, `inspect_tmp_font_bundle.py`, then one-font runtime canary | Visible-component identity and coverage gate |
| Correct Unicode renders as another valid Chinese character | Verify CSV/code point, inspect populated TMP tables, then build a matched static set | Glyph-index conflict; not translation substitution |
| IL2CPP game without a verified runtime loader | Inspect candidates or generate an exact-version TMP asset; do not use the Mono injector | Project-specific font workflow |
| Embedded CSV signatures in `sharedassets*.assets` or bundles | `extract_embedded_csv.py` | Discovery-only occurrence manifest; no generic writeback |

## Core Commands

Scan and extract candidates:

```bash
python scripts/scan_unity_text.py "path/to/GameFolder"
```

This keeps the broad `extracted_text.csv` and `extraction_manifest.json` for audit, and creates translator-facing, occurrence-preserving files in `text/`.

For fixed-width DMSL operands, extract from explicit inputs or a constrained candidate root:

```bash
python scripts/extract_dmsl_text.py "GameFolder" \
  --candidate-root "Game_Data/StreamingAssets/aa/StandaloneWindows64" \
  --out-dir "GameFolder/_translation/unity-text-report/text"
```

After validation, dry-run the fixed byte budgets, then write only to an external candidate root:

```bash
python scripts/writeback_dmsl_text.py "GameFolder" \
  --manifest "GameFolder/_translation/unity-text-report/text/GameTitle_dmsl_text.manifest.json" \
  --translation-csv "GameFolder/_translation/unity-text-report/text/GameTitle_dmsl_text_translation.csv" \
  --report "CandidateReports/dmsl_dry_run.json"
```

Add `--base-root "PriorCandidateRoot" --out-dir "NextCandidateRoot" --write` only after the dry run is clean. Any over-budget row rejects the whole batch and must be shortened and revalidated; the writer never truncates UTF-8.

Extract component UI fields and Unity Localization StringTables with:

```bash
python scripts/extract_typetree_ui_text.py "GameFolder" \
  --scan-root "Game_Data/StreamingAssets/aa" \
  --out-dir "GameFolder/_translation/unity-text-report/text"
```

Dry-run `writeback_typetree_ui_text.py` with its manifest, source CSV, and translation CSV. Use `--base-root` to compose over a DMSL candidate, and add `--out-root "NextCandidateRoot" --write` only after every object identity and field path still matches.

For a rebuilt Addressables bundle, generate the paired external catalog candidate from its internal name:

```bash
python scripts/patch_addressables_catalog_crc.py \
  "GameFolder/Game_Data/StreamingAssets/aa/catalog.bin" \
  --bundle "CandidateRoot/Game_Data/StreamingAssets/aa/StandaloneWindows64/changed.bundle" \
  --game-root "GameFolder" --out-dir "CatalogCandidateRoot" --write
```

The catalog tool rejects unknown/duplicate records and byte-compares the result so only the selected CRC field can change. Apply and roll back the bundle/catalog pair together.

When a broad audit CSV must be narrowed for human translation review, produce a conservative visible-safe subset and audit the omissions:

```bash
python scripts/build_visible_safe_extract.py \
  "GameFolder/_translation/unity-text-report/extracted_text.csv" \
  --manifest "GameFolder/_translation/unity-text-report/extraction_manifest.json" \
  --out-dir "GameFolder/_translation/unity-text-report/validation/visible-safe"
```

Use this subset only as a reviewer aid. For automated writeback, prefer the per-source CSV plus its sidecar manifest. If an older `original_flat,zh_cn` translation baseline must be projected onto an approved subset, run:

```bash
python scripts/project_translation_to_subset.py \
  --translation-csv "GameFolder/_translation/unity-text-report/validation/legacy/GameTitle_text_translation_utf8.csv" \
  --target-source-csv "GameFolder/_translation/unity-text-report/validation/visible-safe/extracted_text_visible_safe.csv" \
  --out-dir "GameFolder/_translation/unity-text-report/validation/projection"
```

Revalidate the projected translation against the exact target source CSV before any writeback decision.

Validate a translated source file:

```bash
python scripts/validate_translation_csv.py \
  --source-csv "GameFolder/_translation/unity-text-report/text/GameTitle_resources_text.csv" \
  --translation-csv "GameFolder/_translation/unity-text-report/text/GameTitle_resources_text_translation.csv" \
  --out-dir "GameFolder/_translation/unity-text-report/validation/resources"
```

Validation blocks row-count, placeholder, tag, and literal `\n` count mismatches by default. Use `--allow-newline-changes` only after confirming the game's parser or layout accepts the change.

When runtime evidence proves that supported visible text cannot be reached statically, generate an AutoTranslator audit report from the exact source CSV and its normalized validated translation:

```bash
python scripts/generate_autotranslator_txt.py \
  --source-csv "GameFolder/_translation/unity-text-report/text/GameTitle_ui_text.csv" \
  --translation-csv "GameFolder/_translation/unity-text-report/validation/ui/GameTitle_ui_text_translation_utf8.csv" \
  --out-dir "GameFolder/_translation/unity-text-report/runtime/autotranslator"
```

The default writes only `autotranslator_export_report.json`. Inspect it, then repeat with `--write` to create `_PreTranslated.txt`. Any row-count mismatch, conflicting or partly blank duplicate key, ambiguous plain-text key/value, or serialized-key collision blocks the whole candidate. The skill does not install BepInEx, XUnity.AutoTranslator, configs, or fonts; verify the external loader/plugin contract and complete a runtime canary as described in `runtime-text-adapters.md`.

For embedded CSV discovery, produce an occurrence-preserving audit before considering a runtime-specific writer:

```bash
python scripts/extract_embedded_csv.py "GameFolder" \
  --out-dir "GameFolder/_translation/unity-text-report/text/embedded-csv"
```

For runtime candidate comparison, keep the diff separate from deployment:

```bash
python scripts/diff_autotranslator_files.py \
  --old "GameFolder/_translation/unity-text-report/runtime/autotranslator/_PreTranslated.previous.txt" \
  --new "GameFolder/_translation/unity-text-report/runtime/autotranslator/_PreTranslated.txt" \
  --output "GameFolder/_translation/unity-text-report/runtime/autotranslator/runtime_diff.json"
```

Review removals and broad changes manually, then rerun the runtime canary. These adapters never merge or install runtime files.

For full-automatic translation, convert a Unity source CSV to an AiNiee cache, translate it with `ainiee-translate`, then convert it back to a Unity translation CSV:

```bash
"$AINIEE_PY" scripts/unity_csv_to_ainiee_cache.py \
  --source-csv "GameFolder/_translation/unity-text-report/text/GameTitle_text.csv" \
  --out-cache "GameFolder/_translation/unity-text-report/ainiee/GameTitle_text/cache.json"
```

Use the sibling `ainiee-translate` skill to run the batch translation loop on that `cache.json`. After translation:

```bash
"$AINIEE_PY" scripts/ainiee_cache_to_unity_translation.py \
  --cache "GameFolder/_translation/unity-text-report/ainiee/GameTitle_text/cache.json" \
  --source-csv "GameFolder/_translation/unity-text-report/text/GameTitle_text.csv" \
  --out-csv "GameFolder/_translation/unity-text-report/text/GameTitle_text_translation.csv"
```

Then run `validate_translation_csv.py` exactly as in the semi-automatic path.

When the user explicitly chooses to apply only structurally safe rows, filter row-addressable failures and then validate the filtered output again:

```bash
python scripts/filter_approved_translation.py \
  --source-csv "GameFolder/_translation/unity-text-report/text/GameTitle_text.csv" \
  --translation-csv "GameFolder/_translation/unity-text-report/validation/text/GameTitle_text_translation_utf8.csv" \
  --validation-report "GameFolder/_translation/unity-text-report/validation/text/translation_validation_report.json" \
  --out-csv "GameFolder/_translation/unity-text-report/text/GameTitle_text_translation.csv" \
  --report-out "GameFolder/_translation/unity-text-report/writeback/approved_translation_report.json"
```

This is valid only for issues carrying individual row numbers, such as placeholder, tag, or newline mismatches. Do not filter around row-count or source-alignment failures.

Dry-run and write a supported serialized/raw source:

```bash
python scripts/writeback_unity_text.py \
  --manifest "GameFolder/_translation/unity-text-report/text/GameTitle_resources_text.manifest.json" \
  --source-csv "GameFolder/_translation/unity-text-report/text/GameTitle_resources_text.csv" \
  --translation-csv "GameFolder/_translation/unity-text-report/validation/resources/GameTitle_resources_text_translation_utf8.csv" \
  --out-dir "GameFolder/_translation/unity-text-report/writeback/resources" \
  --dry-run
```

Run the same command without `--dry-run` only after inspecting skipped rows and planned occurrences. The writer verifies the source file SHA256 recorded at extraction time before modifying a row-mapped source.

After any successful write to a source asset, re-extract that asset before applying another translation batch to it; the stored source hash intentionally rejects stale manifests.

Extract raw profile records when normal extraction misses visible profile text:

```bash
python scripts/extract_character_profiles.py \
  --asset "GameFolder/Game_Data/resources.assets" \
  --out-csv "GameFolder/_translation/unity-text-report/text/GameTitle_profiles_text.csv" \
  --manifest "GameFolder/_translation/unity-text-report/text/GameTitle_profiles_text.manifest.json"
```

Validate the resulting one-column `_translation.csv`, then dry-run/write it:

```bash
python scripts/writeback_character_profiles.py \
  --manifest "GameFolder/_translation/unity-text-report/text/GameTitle_profiles_text.manifest.json" \
  --source-csv "GameFolder/_translation/unity-text-report/text/GameTitle_profiles_text.csv" \
  --translation-csv "GameFolder/_translation/unity-text-report/validation/profiles/GameTitle_profiles_text_translation_utf8.csv" \
  --out-dir "GameFolder/_translation/unity-text-report/writeback/profiles" \
  --dry-run
```

Extract Utage book rows from a scenario or embedded asset after confirming the visible text column:

```bash
python scripts/extract_utage_scenarios.py \
  --asset "GameFolder/Game_Data/StreamingAssets/Utage_AdvProject/Windows/utage_advproject.scenarios.asset" \
  --game-root "GameFolder" \
  --out-dir "GameFolder/_translation/unity-text-report/text"
```

This creates `GameTitle_utage_text.csv`; its manifest records the `ALL_Texts.book` and `ALL_EventTexts.book` row identities. Validate its one-column `_translation.csv`, then write it with:

```bash
python scripts/writeback_utage_scenarios.py \
  --manifest "GameFolder/_translation/unity-text-report/text/GameTitle_utage_text.manifest.json" \
  --source-csv "GameFolder/_translation/unity-text-report/text/GameTitle_utage_text.csv" \
  --translation-csv "GameFolder/_translation/unity-text-report/validation/utage/GameTitle_utage_text_translation_utf8.csv" \
  --out-dir "GameFolder/_translation/unity-text-report/writeback/utage" \
  --dry-run
```

The extractor now blocks with `coverage_complete=false` when a requested book is missing or a skipped MonoBehaviour contains raw Japanese candidates. Audit those objects before continuing:

```bash
python scripts/extract_mono_raw_utf8.py \
  --asset "CandidateRoot/Game_Data/sharedassets0.assets" \
  --path-id 126 \
  --out-dir "GameFolder/_translation/unity-text-report/residual/mono_raw"
```

Review the occurrence-level approval CSV, setting every action to `translate` or `preserve`, then rerun with `--approval-csv`. Follow [references/mono-raw-residual.md](references/mono-raw-residual.md); never approve by text value alone.

## Source Review

Per-source extraction is deliberately occurrence-preserving, not an assertion that every row is safe to translate. Before translating or writing:

- Leave product identity/config strings in `globalgamemanagers` blank unless changing the save/log namespace is intended.
- Leave resource names, audio/CG keys, animation parameters, control labels, and sample/tutorial blocks blank unless runtime evidence shows they are visible text.
- For an occurrence that shares the same original text with a visible row, translate only the visible row and leave the internal occurrence blank.
- Keep an audit note for intentionally omitted categories when preparing a distributable patch.
- Treat duplicate originals as separate occurrences when a per-source manifest exists; do not project by text value unless the workflow is explicitly legacy/audit-only and duplicate risk is reported.
- Do not convert occurrence-specific choices into a runtime key when duplicate originals differ or mix selected and blank rows; a key-based hook would apply one result globally.

The older broad cleaners can support exploration, but do not use a deduplicated CSV as a row-mapped writeback source.

## Special Structures

For a scenario stored as a serialized CSV-like string, inspect its real parser contract before writing. Preserve record separators, in-cell newlines, command columns, quoting behavior, and control tokens. Byte presence alone does not prove the scenario still parses.

For Utage, check both `StreamingAssets/Utage_AdvProject` and embedded books in `sharedassets*.assets`. Confirm that column index `8` is the visible `Text` column before relying on the default; pass `--text-column` when a project differs. A TypeTree failure is a coverage failure, not a harmless skipped object. Use the raw-object audit for every skipped MonoBehaviour with Japanese candidates. Preserve the ordered CRLF/CR/LF signature recorded in the v2 manifest; marker count alone is insufficient.

For a BansheeGz/BGDatabase payload embedded in a TextAsset, do not infer its serialized field format from exported bytes. If the game's managed API can load and save it, use a temporary runtime probe to export occurrences, compare each selected source value, write translated field values, and save a verified replacement payload. Remove all probe registration and DLLs before smoke-testing the normal game.

For Addressables or IL2CPP metadata, require a backup and an integrity plan before edits. Locate a binary catalog entry from the bundle's internal `AssetBundle.m_Name`, never from an opaque disk filename alone. When a uniquely identified CRC must be disabled, use `patch_addressables_catalog_crc.py` to change only that four-byte field in an external catalog candidate; do not guess `catalog.hash` or `bundleSize`. Treat bundle plus catalog as one canary and one rollback unit. A candidate that UnityPy can reopen is not approved unless the game runtime loads it without Addressables/bundle errors.

After an Addressables edit causes a black screen, inspect `Player.log` before revising translations or fonts. Search for CRC mismatch, `Will not load AssetBundle`, bundle dependency/load errors, and catalog parse/hash/cache failures. Preserve the log and roll back the bundle/catalog pair before trying another candidate.

## Font Diagnosis

Treat remaining Japanese as a translation/extraction gap. Distinguish uniform tofu squares from repeated glyph fragments or boxed atlas snippets: tofu indicates missing glyphs, while fragments indicate a font-table, atlas, stream, material, or platform-texture mismatch. A correct source character rendered as another valid Han character indicates a glyph-index conflict: verify the CSV and Unicode first, then inspect the TMP tables instead of changing the translation. Inspect the runtime log and map the visible component to TMP or legacy UI before applying a fix.

Never trust a font package filename or guess the primary font by name. Use `trace_tmp_font_usage.py` from a visible failing component to establish the actual FontAsset/Material/CAB/bundle chain. Run `inspect_tmp_font_bundle.py` to read dynamic/static mode, populated tables, source Font PPtr/family identity, Unity version, glyph coverage, atlas metadata, and SHA-256. If a dynamic asset already has character/glyph tables, never replace only its source TTF. Static replacement must move the matched character table, glyph table, material parameters, and SDF atlas together with `build_static_tmp_fontasset.py`. Require a one-font, one-screen runtime canary before broad replacement. UnityPy reopening is structural evidence, not visual or GPU-runtime proof. Follow [references/font-asset-replacement.md](references/font-asset-replacement.md) for stop conditions and rollback rules.

Trace from a visible string or component name while indexing dependency bundles:

```bash
python scripts/trace_tmp_font_usage.py \
  --asset "ComponentBundle" --candidate-root "AddressablesBundleRoot" \
  --text-contains "Visible failing text" --out "CandidateReports/tmp_usage.json"
```

When static replacement is justified, pass the traced target FontAsset, Material, and Texture2D PathIDs explicitly to `build_static_tmp_fontasset.py`, along with a donor, approved translation root, game root, external output, and report path. Exact Unity versions and real donor coverage are required by default; explicit mismatch or donor-alias opt-ins mark the result canary-only.

For compatible Mono/TMP games with `ScriptingAssemblies.json` and `RuntimeInitializeOnLoads.json`, prefer the runtime fallback preflight:

```bash
python scripts/install_tmp_chinese_font_fix.py "GameFolder" \
  --out-dir "GameFolder/_translation/unity-text-report/font-fix" \
  --dry-run
```

The fixer compiles the DLL and validates injection files during preflight, then applies all planned writes with backups only when run without `--dry-run`. Its default runtime behavior chooses an installed CJK font file, adds a dynamic TMP fallback, and changes legacy UI fonts only for strings with missing CJK glyphs; it does not replace every TMP font. Use `--patch-embedded-fonts --font "Microsoft YaHei"` only when a reviewed embedded legacy `Font` replacement is needed.

After installation, launch the game and inspect `Player.log`. Require an initialization log and no `MissingMethodException`, `Unable to load font face`, or repeated missing-glyph failures. Some stripped Mono builds omit `Font.CreateDynamicFontFromOSFont` or `ParameterInfo.HasDefaultValue`; use the shipped file-path/reflection-compatible fixer rather than assuming those APIs exist. If the game directory permits content writes but rejects rename replacement, keep the backup, accept verified copy-overwrite only, and remove or report staged `.tmp` files.

Older Mono builds without the JSON injection tables still require project-specific work in `globalgamemanagers` or a managed assembly hook. IL2CPP builds require a separately verified IL2CPP loader/plugin or an exact-version resource asset; do not claim the Mono installer applies.

## Save Discovery

When asked for save locations, check the game's persistence middleware before assuming Unity's `persistentDataPath`. For Easy Save 3 (`ES3`, `ES3Defaults`, `SaveFile.es3`, or `AutoSave.es3` clues), inspect the serialized defaults resource and confirm an actual modified save file on disk. ES3 may place a save beside game data rather than under `AppData\LocalLow`; report the confirmed file and distinguish it from PlayerPrefs/display settings.

## Patch Delivery

Build a distributable package only after the composed external candidate passes reopen checks, a second source-specific residual audit with zero unreviewed visible occurrences, font verification, and a game-runtime canary. Build from pristine original hashes directly to that final candidate, never incrementally from an earlier translation candidate:

```bash
python scripts/build_binary_patch.py \
  --game-root "GameFolder" \
  --backup-root "GameFolder/_translation/unity-text-report/writeback/resources/backups/<timestamp>" \
  --file "Game_Data/resources.assets" \
  --out-dir "GameFolder/_translation/unity-text-report/patch/cn_patch" \
  --zip
```

Repeat `--file` for each modified game file. The package stores SHA256-protected GZip-compressed binary middle-span payloads, an `install_cn_patch.bat` launcher backed by `apply_cn_patch.ps1.txt`, and a Python verifier/applicator for development checks. The installer refuses unknown target files, skips already patched files, and creates `_cn_patch_backup_<timestamp>` in the target game before applying changes.

For changes spread throughout a large resaved asset, the binary middle-span payload may be large; report payload sizes rather than claiming small deltas.

Install the ZIP into a fresh directory populated from the pristine originals. Require the installed hashes to match the live final candidate, confirm automatic backup creation and repeat-install behavior, and record the ZIP SHA256. Any later translation, residual, or font fix invalidates the package and requires a full rebuild and clean install test.

## Completion Cleanup

After the validated game build is working, keep the final project-named source/translation CSVs and manifests, validation reports, applied writeback report, one original backup per modified game file, required runtime font DLL/config registration, and any distributable patch. Remove failed candidates, probe DLLs/registration backups, dry-run payload copies, duplicate backups, compile output, and staged `.tmp` files unless they are specifically needed to diagnose an unresolved issue.

## Required Reporting

Report:

- detected build layout and selected adapters
- generated project-named CSVs and their manifests
- validation failures/warnings and normalized translation paths
- dry-run and applied writeback counts, skipped rows, backups, and source-hash checks
- intentionally preserved identity/config/resource rows
- first and final residual-audit counts, every preserved internal category, and zero-unreviewed-visible evidence
- runtime text candidate/report hashes, duplicate-key decisions, external loader/plugin evidence, canary result, and removal path when a runtime adapter was used
- TMP font inspection report, required-character coverage, canary scope, visual result, and rollback path when fonts were changed
- confirmed save path and persistence evidence when save-location work is requested
- patch manifest, payload sizes, installer verification, and package ZIP when distributing
- whether any outputs were produced from a broad audit subset rather than a row-mapped source manifest

Never claim complete translation coverage when unsupported containers or skipped occurrences remain.

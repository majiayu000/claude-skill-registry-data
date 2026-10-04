---
name: configure-codacy-cloud
description: Tunes an existing Codacy Cloud repository's configuration directly on the cloud, without local analysis, by importing the current config, suggesting higher-signal tools and patterns, reanalyzing, and iteratively reducing noise across two tuning passes. Requires the repository to already be on Codacy with at least one finished analysis. Uses the Codacy Analysis CLI only for config-file operations and the Codacy Cloud CLI for everything else. Produces a machine-readable JSON summary of pattern, tool, category, and severity changes plus conflicts and recommended path ignores. Use when the user wants to configure or tune Codacy directly on the cloud, reduce noise on a repository already analyzed by Codacy, optimize cloud patterns and tools, or improve the signal of cloud issues without running local analysis.
license: MIT
metadata:
  author: Codacy
  version: 1.1.0
---

# Configure Codacy (Cloud)

> **Glossary:** See [glossary.md](../../references/glossary.md) for shared definitions of Codacy concepts (issues, findings, severity, coverage, tools, patterns, etc.).

This skill tunes the Codacy configuration of a repository **directly on Codacy Cloud**, using the cloud as the source of truth. It does **not** run local analysis. It reads the current cloud issue landscape, applies a higher-signal set of tools and patterns, reanalyzes on Codacy, and iteratively cuts noise over two passes — producing a clean, high-signal configuration with a full audit trail of what changed and why.

For the local-first variant that discovers a stack from scratch and runs `codacy-analysis analyze` locally, use the `configure-codacy` skill instead. This skill is for repositories **already on Codacy with a finished analysis** where you want to tune the cloud config in place.

## Prerequisites and requirements

- **Codacy Cloud CLI** (`codacy`) — drives all cloud reads, updates, and reanalysis. See `codacy-cloud-cli` for setup.
- **Codacy Analysis CLI** (`codacy-analysis`) — used **only** for config-file operations (`init --remote`, `init --auto`, `config --merge`). See `codacy-analysis-cli` for setup.
- Both CLIs share credentials at `~/.codacy/credentials`, so a single login covers both.

This skill has **three hard requirements**. Verify all three before doing anything else and stop with clear guidance if any fails:

1. **The repository is already on Codacy.** Confirm with:
   ```bash
   codacy repo --output json
   ```
   If this fails (not on Codacy, no auth), stop. Tell the user to add the repo to Codacy first (e.g. `codacy repo --add`) — this skill does not set up a new repository.

2. **The repository has at least one finished analysis.** Inspect the `codacy repo --output json` output for a completed/last-analysis indicator, and confirm the issue overview returns data:
   ```bash
   codacy issues -O -o json 2>/dev/null | jq '.'
   ```
   If the repo was never analyzed, or analysis is still running, stop. Tell the user to wait for the first analysis to finish — the whole flow depends on cloud issue data as the baseline.

3. **The Cloud CLI is ≥ 1.3.0** (required to populate `fileCount`). Confirm with:
   ```bash
   codacy repo -o json 2>/dev/null | jq -e '.repository.fileCount != null'
   ```
   If this prints `false` (or errors), stop. The installed Cloud CLI is older than 1.3.0 and does not populate the summary's `fileCount` field. Tell the user to upgrade to at least 1.3.0 (`npm install -g @codacy/codacy-cloud-cli@latest`) and rerun. The check uses `!= null` rather than `has("fileCount")` so it rejects both absent keys and explicit nulls, and feature presence is checked rather than `--version` because the current CLI hardcodes its `--version` string.

The Cloud CLI auto-detects `provider`, `organization`, and `repository` from the git remote when run inside the repo, so the explicit `<provider> <org> <repo>` arguments shown below are optional in practice.

**CLI output caveat:** both CLIs print progress lines to stderr before their JSON output. When piping to `jq`, redirect stderr: `codacy ... -o json 2>/dev/null | jq '...'`.

**`codacy patterns` pagination caveat:** `codacy patterns <tool> [--enabled]` currently returns only the **first 100 patterns** and has **no `--limit` flag** (one is planned — until then, assume the list is truncated at 100). Never use the length of its output as a pattern count: for a tool whose enabled set exceeds 100 you will silently see only 100, which reads as a phantom "reduction" (e.g. a tool that actually has 232 enabled patterns appears to have "100"). To check or test a **specific** pattern, filter by id with `--search <patternId>` or query the single pattern with `codacy pattern <tool> <patternId> -o json`. For accurate enabled-pattern **counts**, derive them from the config file (`jq '[.tools[].patterns|length]|add' .codacy/auto.config.json`) rather than the patterns list.

**Local config is untouched.** This skill works through custom `--config-file` paths (`.codacy/remote.config.json`, `.codacy/auto.config.json`) and **never creates or modifies `.codacy/codacy.config.json`**. Any existing local config is left intact.

## How this skill works

The key principle is the same as the local variant: **start from a higher-signal set, then cut noise using data** — but every measurement and every change happens on Codacy Cloud.

Tools fall into two groups, and changes are applied through **two different mechanisms**:

- **Tools supported by the Analysis CLI** (those listed by `codacy-analysis info`, see [supported-tools.md](../codacy-analysis-cli/references/supported-tools.md)) are configured by editing the `.codacy/auto.config.json` file and importing it: `codacy tools --import .codacy/auto.config.json`. The import **reconciles supported tools to the file's contents**: a supported tool present in the file has its patterns replaced by the file's, and a supported tool **absent** from the file is **disabled** by the import (you will see `N tool will be disabled: ...` in the import plan). **Cloud-only tools** — those outside the Analysis CLI's scope — are never in the file and keep their state.
- **Cloud-only tools** (enabled in Codacy but not runnable by the Analysis CLI, e.g. SonarSharp, Codacy ScalaMeta Pro) cannot be configured via the import. Change them directly with the Cloud CLI: `codacy tool`, `codacy pattern`, `codacy patterns`.

**Cloud tool name vs config `toolId`.** The Cloud CLI commands (`codacy tool`, `codacy pattern`, `codacy patterns`) address tools by their **cloud name** as shown by `codacy tools` — which for some tools **differs** from the Analysis CLI config `toolId`. The clearest case: the config `toolId` is `Semgrep`, but the cloud tool is named `Opengrep`, so `codacy patterns Semgrep` fails with `Tool "Semgrep" not found` while `codacy patterns Opengrep` works. When a Cloud CLI command reports a tool as not found, check the name in `codacy tools -o json` and use that. (The import path, which keys by `toolId`, is unaffected.)

Read [the config format reference](../codacy-analysis-cli/references/config-format.md) before editing `auto.config.json`. Its shape: a top-level `tools[]` array where each entry is keyed by **`toolId`** (e.g. `"Biome"`, `"Semgrep"`, `"ESLint9"`) and holds a `patterns[]` array whose entries are keyed by **`patternId`** with an optional **`parameters`** object — there is **no** `uuid`, `name`, or `enabled` key on these entries, so filter and edit by `toolId` / `patternId`. To disable a pattern, remove it from the `patterns` array; to tune one, edit its `parameters`; to disable a tool, remove the whole tool entry.

## Workflow

```
Configuration Progress:
- [ ] Startup: verify requirements, capture baseline, import cloud config, split tools
- [ ] First pass: generate + merge config, first noise cut, apply, reanalyze
- [ ] Second pass: evaluate impact, second noise cut, apply, reanalyze
- [ ] Final: capture after metrics, evaluate, emit JSON summary, clean up
```

### Startup

1. **Create the temp directory:**
   ```bash
   mkdir -p .codacy/tmp
   ```

2. **Capture the baseline overview (the BEFORE reference):**
   ```bash
   codacy issues -O -o json 2>/dev/null > .codacy/tmp/overview-before.json
   ```
   This overview is the source for the BEFORE `issues` total, the `issuesByCategory` and `issuesBySeverity` breakdowns, and per-pattern issue counts and false-positive counts.

   **Overview JSON structure** (the output is nested under a top-level `overview` key — do not assume flat field names):
   - `.overview.categories[]` → `{ name, total }` — e.g. `Security`, `ErrorProne`, `CodeStyle`. The BEFORE `issues` total is the sum of `.overview.categories[].total`.
   - `.overview.levels[]` → `{ name, total }` — these are the **severity** buckets, but named `Error` / `High` / `Warning` / `Info`. Map them to the summary's severity names: **`Error` → `Critical`, `High` → `High`, `Warning` → `Medium`, `Info` → `Minor`**.
   - `.overview.patterns[]` → `{ id, title, total }` — per-pattern issue counts, sorted with `jq '.overview.patterns | sort_by(-.total)'`. This is the **primary noise signal**: work the highest-count patterns first.
   - `.overview.potentialFalsePositives[]` → `{ name, total }`.

   If a given CLI version also surfaces **suggested actions** (patterns accounting for 10%+ of all issues or 3x the average per-pattern count, with ready-to-run disable commands), use them — but do not depend on the field being present; the per-pattern counts above are the reliable signal.

3. **Import the current cloud configuration to a file:**
   ```bash
   rm -f .codacy/remote.config.json
   codacy-analysis init --remote <provider> <org> <repo> --config-file .codacy/remote.config.json
   ```
   (`init --remote` refuses to overwrite an existing target file, hence the `rm -f`.) This captures the cloud config for tools the Analysis CLI supports.

4. **Split tools into supported vs cloud-only:**
   ```bash
   # Tools the Analysis CLI can configure via import
   codacy-analysis info 2>/dev/null

   # Tools currently enabled on Codacy Cloud
   codacy tools -o json 2>/dev/null | jq '[.[] | select(.settings.isEnabled == true) | .name]'
   ```
   Any cloud-enabled tool **not** in the `codacy-analysis info` list is **cloud-only** — record it; its patterns must be changed with the Cloud CLI, never via import.

5. **Detect coding-standard lock-in early.** Check which coding standards the repo follows:
   ```bash
   codacy repo -o json 2>/dev/null | jq '.repository.repository.standards'
   ```
   If any are present, expect that some tools/patterns are **enforced** by them and cannot be changed at the repo level. For any tool or pattern you later plan to disable or tune, check its `enabledBy` field **first** — a non-empty `enabledBy` means a coding standard enforces it, so a disable will be rejected with a **409**:
   ```bash
   codacy pattern <toolName> <patternId> -o json 2>/dev/null | jq '.enabledBy'   # [] / null ⇒ repo-level (changeable); [{name: ...}] ⇒ standard-enforced (locked)
   ```
   Classify standard-enforced tools/patterns into `conflicts[]` **upfront** rather than discovering them through rejected calls — it avoids wasted trial-and-error and makes the whole noise plan honest about what is actually achievable. Never unlink the standard and never use `--force`.

6. **Record BEFORE counts:**
   ```bash
   # Enabled tools
   codacy tools -o json 2>/dev/null | jq '[.[] | select(.settings.isEnabled == true)] | length'

   # Enabled patterns for supported tools (from the imported config)
   jq '[.tools[].patterns | length] | add' .codacy/remote.config.json
   ```
   For **cloud-only** tools, add their enabled-pattern counts: `codacy patterns <tool> --enabled -o json 2>/dev/null | jq 'length'` per tool — but mind the pagination caveat above: this is capped at 100, so a cloud-only tool with more than 100 enabled patterns will be undercounted. <!-- TODO(--limit): once `codacy patterns` supports `--limit`, pass `--limit <n>` here to get an accurate cloud-only count and drop the 100-cap workaround. --> The BEFORE `enabledPatterns` is the sum of the supported-tool count and the cloud-only counts; BEFORE `enabledTools` is the enabled-tool count.

7. **Capture repo-level descriptors** for the summary:
   ```bash
   codacy repo -o json 2>/dev/null > .codacy/tmp/repo.json
   jq '.repository.repository.languages | length' .codacy/tmp/repo.json   # → languageCount
   jq '.repository.fileCount'                    .codacy/tmp/repo.json   # → fileCount
   ```
   Caches the response to disk so both fields are read from a single invocation. These are snapshots of repo state, not before/after metrics — they go directly under `summary` as scalars.

### First pass

1. **Generate a higher-signal auto config:**
   ```bash
   rm -f .codacy/auto.config.json
   codacy-analysis init --auto "AllSecurity,ErrorProne,Performance,BestPractice,Compatibility,Critical,High" --config-file .codacy/auto.config.json
   ```
   This filter is deliberately tighter than the local variant's broad set — it favors security, error-prone, and high-severity findings and avoids flooding the cloud with low-value style noise.

2. **Merge the current cloud config into the auto config (union, remote → auto):**
   ```bash
   codacy-analysis config --merge --source .codacy/remote.config.json --dest .codacy/auto.config.json
   ```
   `--dest` is overwritten with the union, so `.codacy/auto.config.json` now holds **both** the patterns already enabled on the cloud (for supported tools) **and** the newly suggested patterns. This is the working config for the import path.

3. **First noise evaluation** against `.codacy/tmp/overview-before.json`. Work through patterns by issue count (highest first), applying the [noise-evaluation guidance](#noise-evaluation-guidance):
   - Start from the overview's suggested actions, per-pattern counts, and false-positive ratios.
   - If a noisy pattern is **tunable** via parameters (complexity thresholds like Lizard CCN/NLOC, line-length limits), **raise the parameter** instead of disabling.
   - Otherwise, if it is noisy and irrelevant, **disable** it.
   - To inspect concrete examples for a pattern before deciding: `codacy issues -p <patternId> -o json 2>/dev/null | jq '.'`.

4. **Apply the changes (dual mechanism):**
   - **Supported tools** — edit `.codacy/auto.config.json` (remove patterns to disable; edit `parameters` to tune; remove a tool entry to disable the tool), then import:
     ```bash
     codacy tools --import .codacy/auto.config.json -y
     ```
   - **Cloud-only tools** — change directly with the Cloud CLI:
     ```bash
     codacy pattern <provider> <org> <repo> <tool> <patternId> --disable
     codacy pattern <provider> <org> <repo> <tool> <patternId> --parameter threshold=20
     codacy patterns <provider> <org> <repo> <tool> --categories CodeStyle --severities Minor --disable-all
     codacy tool <provider> <org> <repo> <tool> --disable
     ```
   - If any change is rejected with a **409 conflict** — the pattern/tool is enforced by a Coding Standard, or the tool uses its own Configuration File — **record it in `conflicts[]` and move on**. Never unlink standards and never use `--force`.

5. **Reanalyze and wait:**
   ```bash
   codacy repo --reanalyze-and-wait -o json 2>/dev/null > .codacy/tmp/delta-pass1.json
   ```
   This triggers reanalysis on Codacy, polls until done (up to ~20 min), and returns a delta report of issue changes by pattern, severity, and category. If it times out, note it and proceed.

### Second pass

1. **Refresh the overview and compare to baseline:**
   ```bash
   codacy issues -O -o json 2>/dev/null > .codacy/tmp/overview-pass1.json
   ```
   Read `delta-pass1.json` and compare `overview-pass1.json` against `overview-before.json` to see what the first pass actually changed per pattern, category, and severity.

2. **Second noise evaluation — sharpen the signal:**
   - **Reduce remaining noisy patterns** that survived the first pass.
   - **Judge the newly enabled patterns:** did they surface *relevant* issues, or noise? Disable patterns that turned out irrelevant for this codebase or that only produced false positives (apply the same caution to Security patterns described in the guidance below).
   - **Net-issue guardrail:** one goal of this skill is *fewer, more relevant* results. If the total issue count rose markedly versus the baseline, decide what to cut from the newly enabled set — a final count above the baseline is a red flag **unless** one of these holds: (a) the repo started from a very minimal configuration (some growth is expected and healthy), or (b) the dominant baseline noise is **enforced by a coding standard** and therefore could not be cut from the repo. In case (b), a flat or higher total is an expected outcome, **not** a failure — record the locked patterns/tools in `conflicts[]` with a recommendation to edit the standard, and do **not** over-cut genuinely useful new findings (especially Security) just to force the headline number down. Be smart: keep the high-value new findings, trim the rest.

3. **Apply the changes again** with the same dual mechanism (edit `.codacy/auto.config.json` + `codacy tools --import .codacy/auto.config.json` for supported tools; `codacy pattern`/`patterns`/`tool` for cloud-only). Record any new 409 conflicts in `conflicts[]`.

4. **Reanalyze and wait:**
   ```bash
   codacy repo --reanalyze-and-wait -o json 2>/dev/null > .codacy/tmp/delta-pass2.json
   ```

### Final

1. **Capture the final picture:**
   ```bash
   codacy issues -O -o json 2>/dev/null > .codacy/tmp/overview-after.json
   ```

2. **Record AFTER counts:** enabled tools from `codacy tools -o json` (enabled count); enabled patterns as the sum of supported-tool patterns in `.codacy/auto.config.json` plus cloud-only enabled patterns (per-tool `codacy patterns <tool> --enabled` count — capped at 100, see the pagination caveat); issue total and the category/severity breakdowns from `overview-after.json`. <!-- TODO(--limit): once `codacy patterns` supports `--limit`, use it for the cloud-only count instead of carrying BEFORE counts forward. --> For a tool you could not change (e.g. a standard-enforced tool), carry its BEFORE count forward unchanged rather than re-counting it from the capped patterns list.

3. **Evaluate the results.** If needed, inspect specific tools or patterns to confirm (`codacy patterns <tool> --enabled -o json`, `codacy tool <tool> -o json`). Identify:
   - **What went well** — noise reduction, and new *relevant* detections (especially Security).
   - **What did not go well** — noisy patterns that could **not** be disabled because the tool uses its own Configuration File, or because they are enforced by a Coding Standard. These go in `conflicts[]`.
   - **Recommendations outside patterns** — files or paths that are generating disproportionate or future noise and could be ignored. These go in `recommendedPathsToIgnore[]` as recommendations only. (Cloud file exclusions are applied via a `.codacy.yaml` committed to the default branch — mention this to the user, but do not create or modify any file.)

4. **Write the summary** to `.codacy/configure-codacy-cloud-summary.json` (schema below) and present a concise before/after summary to the user: metrics table (patterns, tools, issues, by category, by severity), key improvements, conflicts that blocked changes, and recommended paths to ignore.

5. **Clean up:**
   ```bash
   rm -rf .codacy/tmp .codacy/remote.config.json .codacy/auto.config.json
   ```

## Summary JSON

Write `.codacy/configure-codacy-cloud-summary.json`. `before` values come from the startup baseline; `after` values come from the final overview.

```json
{
  "summary": {
    "languageCount": 4,
    "fileCount": 83,
    "enabledPatterns": { "before": 1000, "after": 300 },
    "enabledTools": { "before": 34, "after": 15 },
    "issues": { "before": 7000, "after": 550 },
    "issuesByCategory": {
      "Security": { "before": 56, "after": 89 },
      "ErrorProne": { "before": 140, "after": 123 },
      "CodeStyle": { "before": 3000, "after": 230 }
    },
    "issuesBySeverity": {
      "Critical": { "before": 56, "after": 89 },
      "High": { "before": 140, "after": 123 },
      "Medium": { "before": 900, "after": 210 },
      "Minor": { "before": 5904, "after": 128 }
    }
  },
  "toolChanges": [
    {
      "toolName": "Biome",
      "action": "disabled",
      "reason": "Project uses ESLint9 with local config; Biome is redundant and produced 16K false positives in TypeScript",
      "patternsAffected": 232
    },
    {
      "toolName": "AgentLinter",
      "action": "enabled",
      "reason": "New tool added for linting agent instruction files",
      "patternsAffected": 43
    }
  ],
  "patternChanges": [
    {
      "patternId": "Semgrep_python.lang.security.audit.xss.template-injection",
      "toolName": "Semgrep",
      "action": "disabled",
      "reason": "Wrong stack — pattern for Python; project is JavaScript-only",
      "deltaIssues": -45,
      "parameters": []
    },
    {
      "patternId": "Lizard_ccn-medium",
      "toolName": "Lizard",
      "action": "updated",
      "reason": "Raised threshold from 10 to 20 to match codebase complexity profile",
      "deltaIssues": -120,
      "parameters": [
        { "id": "threshold", "before": "10", "after": "20" }
      ]
    },
    {
      "patternId": "Semgrep_codacy.javascript.security.hard-coded-password",
      "toolName": "Semgrep",
      "action": "enabled",
      "reason": "New High Security pattern — detects hardcoded passwords; found 101 issues across 41 files for review",
      "deltaIssues": 101,
      "parameters": []
    }
  ],
  "recommendedPathsToIgnore": [
    {
      "path": "src/generated/**",
      "reason": "Generated code. Recommended to be ignored to avoid uncontrolled issues."
    },
    {
      "path": "src/tests/mocked.json",
      "reason": "Triggers a significant amount of security false positives (hardcoded passwords and secrets). Could be ignored."
    }
  ],
  "keyImprovements": [
    "Lizard complexity thresholds tuned to match a mature React SPA — 576 fewer noise issues while keeping genuinely complex functions flagged",
    "6 new security patterns detecting open redirects, unsafe dynamic methods, hardcoded passwords, and React href injection (119 new findings)",
    "AgentLinter added for agent instruction file quality",
    "Checkov expanded from 6 to 56 IaC security patterns"
  ],
  "conflicts": [
    {
      "toolName": "Biome",
      "conflict": "EnforcedByCodingStandard",
      "codingStandardName": "Default Security Rules",
      "reason": "Whole-tool conflict (no patternId). Biome is redundant with the project's ESLint9 yet produces most of the noise; disabling the tool was rejected with 409 because a coding standard enforces it. Recommend removing Biome from the coding standard."
    },
    {
      "patternId": "Semgrep_codacy.javascript.avoid_undefined_identifier",
      "toolName": "Semgrep",
      "conflict": "EnforcedByCodingStandard",
      "codingStandardName": "Default Security Rules",
      "reason": "Reports 1k+ low-relevance issues but is enforced by a coding standard, so it could not be disabled. Recommend disabling it in the coding standard."
    },
    {
      "patternId": "ESLint9_unused_import",
      "toolName": "ESLint9",
      "conflict": "ConfigurationFile",
      "reason": "ESLint9 uses the project's own config file, so this pattern cannot be changed from Codacy. Adjust the project's ESLint config instead."
    }
  ]
}
```

**Field reference**

- **`summary`** — repo descriptors plus before/after counts. `languageCount` is the length of `.repository.repository.languages` from `codacy repo -o json`; `fileCount` is `.repository.fileCount` from the same call. Both are snapshots of repo state taken once at startup, not before/after pairs. `enabledPatterns`/`enabledTools` count everything enabled on Codacy (supported + cloud-only). `issuesByCategory`/`issuesBySeverity` come from the issue overview's breakdowns (apply the `Error→Critical` / `High→High` / `Warning→Medium` / `Info→Minor` level mapping).
- **`toolName`** (used in `toolChanges`, `patternChanges`, `conflicts`) — the tool's **name as shown by `codacy tools`** (the cloud-side identifier you actually store and act on). Note this can differ from the Analysis CLI config `toolId`.
- **`toolChanges`** — one entry per whole tool enabled or disabled. `action`: `"enabled"` or `"disabled"`. `patternsAffected`: number of patterns in that tool.
- **`patternChanges`** — one entry per individual pattern change within a tool that stays enabled. `action`: `"enabled"`, `"disabled"`, or `"updated"`. `deltaIssues`: change in this pattern's issue count, baseline vs final. `parameters`: array of `{id, before, after}` for tuned parameters, `[]` otherwise. Do not list patterns that were added/removed as part of a whole-tool change — those are covered by `toolChanges`.
- **`recommendedPathsToIgnore`** — array of `{path, reason}`. Recommendations only; nothing is written to the repo.
- **`keyImprovements`** — 3–6 human-readable sentences summarizing the most impactful changes, suitable to present to the user.
- **`conflicts`** — array of changes that were attempted but blocked. `patternId` is **optional**: **omit it for whole-tool conflicts** (e.g. a tool that can't be disabled because a standard enforces it), and **include it for pattern-level conflicts**. `conflict`: `"EnforcedByCodingStandard"` (include `codingStandardName`) or `"ConfigurationFile"`. `reason`: what it reports and the recommended action (edit the coding standard / edit the tool's own config file).

## Noise-evaluation guidance

Apply judgment proportional to relevance — be more demanding before disabling important patterns, more relaxed about low-relevance noise.

- **Security patterns get extra caution.** It *is* fine to disable a Security pattern that is irrelevant to this codebase (wrong stack or framework) or that only produces false positives — but be thorough and think twice before disabling any security pattern. When in doubt, inspect real examples first (`codacy issues -p <patternId> -o json`) and prefer parameter tuning or a path-ignore recommendation over disabling.
- **Never lightly disable Critical or High severity patterns.** Disable them only when clearly wrong-stack or confirmed false positives.
- **Be lenient on low-relevance categories** — CodeStyle, Documentation, Comprehensibility, and Minor-severity issues are the first to cut when they are noisy or mismatched to the project's conventions.
- **Prefer parameter tuning over disabling** wherever a threshold exists (Lizard complexity, line length, parameter counts) — it reduces noise while keeping the rule active.
- **Wrong stack → disable.** Patterns for languages or frameworks not present in the repository are pure noise.
- **Deduplicate overlap.** When two tools flag the same concern, keep the more precise tool's pattern and disable the redundant one — the concern stays covered.
- **Inspect before deciding.** For any borderline pattern, list its issues (`codacy issues -p <patternId>`) and look at real examples before disabling.

## Per-tool tuning tips

- **Semgrep** — ships patterns for 30+ languages; disabling patterns for languages not in the repo is usually the single biggest noise reduction. Cross-reference the pattern ID prefix (e.g. `python.`, `javascript.`, `java.`).
- **Lizard (complexity)** — has CCN, NLOC, and parameter-count rules with configurable `threshold` parameters. For mature codebases, raise the medium thresholds to match the project's profile rather than disabling, to preserve visibility into genuinely complex code.
- **ESLint9 / Stylelint** — if the repo has its own config file and uses it on Codacy, the tool runs in Configuration File mode; its patterns cannot be changed from Codacy (these show up as `ConfigurationFile` conflicts). Note this to the user — noise must be reduced in the project's own config.
- **markdownlint** — rules like MD033 (inline HTML), MD034 (bare URLs), MD024 (duplicate headings) fire heavily on changelogs and generated docs. These are stylistic; recommend ignoring the noisy paths rather than keeping the noise.

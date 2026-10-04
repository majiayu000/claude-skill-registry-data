---
name: configure-codacy
description: Tailors Codacy configuration to a project by discovering its stack, enabling the right tools and patterns, running analysis, and intelligently reducing noise — disabling irrelevant or noisy patterns, tuning thresholds, and excluding files that shouldn't be analyzed. Produces a machine-readable summary of all changes. Use whenever the user wants to configure Codacy, reduce noise, fix false positives, enable or disable tools or patterns, tune code quality rules, deal with too many warnings, or align Codacy with their project's conventions. Also trigger when the user complains about irrelevant issues, noisy linters, or wants to set up Codacy for the first time on a repo.
license: MIT
metadata:
  author: Codacy
  version: 4.3.0
---

# Configure Codacy

> **Glossary:** See [glossary.md](../../references/glossary.md) for shared definitions of Codacy concepts (issues, findings, severity, coverage, tools, patterns, etc.).

This skill tailors Codacy configuration to a project's actual stack and coding conventions. It discovers the repository's languages and frameworks, initializes a broad set of tools and patterns, runs analysis, then intelligently cuts noise — producing a clean, high-signal configuration with a full audit trail of what changed and why.

## Prerequisites

- **Codacy Analysis CLI** (`codacy-analysis`) with `discover` and `init --auto` support. If the CLI does not support these commands, update it running: `npm i -g @codacy/analysis-cli`. See `codacy-analysis-cli` for setup.
- **Codacy Cloud CLI** (`codacy`) — needed to know if the repo is on Codacy Cloud and if so, fetch issues from the cloud-only tools. See `codacy-cloud-cli` for setup.

Both CLIs share credentials at `~/.codacy/credentials`, so a single login covers both.

## How configuration works

All configuration is done locally via `.codacy/codacy.config.json`. Edit the file, run analysis, see results instantly — no push or cloud reanalysis needed. Once tuned, the configuration can be imported to Codacy Cloud in one step.

The key principle: **start broad, then cut noise using data**. Initialize with maximum pattern coverage via `init --auto`, run analysis to see the full issue landscape, then use the severity/category distribution to decide what to disable or tune.


Read [the config format reference](../codacy-analysis-cli/references/config-format.md) for the full schema before editing — field names matter (e.g., the exclusion field is `exclude`, not `excludePaths`). To disable a pattern, remove it from the `patterns` array. To disable a tool, remove the entire tool entry.

**Organization standards take precedence.** If a pattern is enforced by a Coding Standard at the organization level, it cannot be changed at the repository level.

**Local config only.** The `.codacy/codacy.config.json` file is used exclusively for local analysis. Committing or pushing it to the repository has NO effect on Codacy Cloud analysis. To apply the configuration to Codacy Cloud, use the import command (`codacy tools ... --import`).

## Invocation modes

The skill supports three modes that control whether configuration is imported to Codacy Cloud after tuning:

- **Interactive (default):** After tuning and presenting results, prompt the user via `AskUserQuestion` whether to import the configuration to Codacy Cloud. This is the default when no arguments are provided.
- **Auto-import:** If the user's invocation arguments contain the word "import" (e.g., `/configure-codacy import configuration`, `/configure-codacy --import`), skip the import prompt and import automatically after presenting results. Useful for CI runs and automation.
- **Local-only:** If the repo is not on Codacy Cloud (determined in Step 0), never ask about importing. Present results and note that the config is ready for local analysis only.

Additionally, the **force** flag controls Coding Standard handling during import:

- **Force disabled (default):** If the import encounters Coding Standard conflicts (409 errors), **do NOT automatically retry with `--force`**. Instead, present the conflicts to the user via `AskUserQuestion` and let them decide whether to unlink the Coding Standards.
- **Force enabled:** If the user's invocation arguments contain the word "force" (e.g., `/configure-codacy import force`), automatically retry with `--force` when Coding Standard conflicts occur.

Parse the invocation arguments at the very start. Set internal flags that Step 6 will reference:
- If args contain "import" → auto-import mode
- If args contain "force" → force mode (allows automatic Coding Standard unlinking)
- Else → interactive mode (may become local-only if Step 0 finds the repo is not on Cloud)

## Tailored configuration workflow

```
Configuration Progress:
- [ ] Step 0: Check environment and capture baseline
- [ ] Step 1: Discover repository stack
- [ ] Step 2: Initialize auto-tuned configuration
- [ ] Step 3: Run broad-config baseline analysis
- [ ] Step 4: Smart noise evaluation and tuning
- [ ] Step 5: Show local results
- [ ] Step 6: Cloud import (conditional)
- [ ] Step 7: Clean-up
```

### Step 0: Check environment and capture baseline

This step determines the starting point and captures the BEFORE metrics for the final summary. The flow depends on two conditions: whether the repo is on Codacy Cloud, and whether a local config already exists.

#### 0a. Create temp directory and check Codacy Cloud status

Create the temporary directory for intermediate analysis files:
```bash
mkdir -p .codacy/tmp
```

The Cloud CLI auto-detects provider, organization, and repository from the git remote origin URL — no need to derive these manually. All `codacy` commands below can be run without explicit `<provider> <org> <repo>` when inside the repo. For clarity, the examples use the explicit form; replace with auto-detected short form in practice.

**CLI output caveat:** Both `codacy` and `codacy-analysis` CLIs write progress lines (e.g., `- Fetching tools...`, `- Fetching issues...`) to stderr before the actual JSON output. When piping CLI output directly to `jq`, redirect stderr to avoid parse errors:

```bash
codacy repository --output json 2>/dev/null | jq '...'
```

Check Cloud status:
```bash
codacy repository --output json
```

If this succeeds, the repo is on Codacy Cloud. Also list enabled tools to identify cloud-only tools later:
```bash
codacy tools --output json 2>/dev/null | jq '[.[] | select(.settings.isEnabled == true) | {name, isClientSide}]'
```

If it fails (repo not on Codacy, no auth, or no Cloud CLI), note that cloud features will be skipped — the local workflow is fully self-contained. Set the invocation mode to local-only (see "Invocation modes" section).

#### 0b. Capture baseline (BEFORE reference)

Branch based on Cloud status and local config existence. The baseline captured here is the true BEFORE reference for the summary in Step 5.

**Track A — Repo is on Codacy Cloud (authoritative baseline):**

The Cloud configuration is the authoritative source. Use `init --remote` to fetch it.

**Important:** `init --remote` will fail if `.codacy/codacy.config.json` already exists. Always delete it first (the backup copy step happens before the delete):

```bash
# Delete any existing config first — init --remote refuses to overwrite
rm -f .codacy/codacy.config.json

# Fetch the current Cloud configuration
codacy-analysis init --remote <provider> <org> <repo>

# Store a copy for later merging and comparison
cp .codacy/codacy.config.json .codacy/tmp/codacy-remote-config.json

# Record BEFORE metrics
jq '[.tools[].patterns | length] | add' .codacy/codacy.config.json
jq '.tools | length' .codacy/codacy.config.json

# Run analysis with the Cloud config to capture the BEFORE issue landscape
codacy-analysis analyze --install-dependencies --output-format json --output .codacy/tmp/codacy-remote-results.json

# Record BEFORE issue count and runtime
jq '.issues | length' .codacy/tmp/codacy-remote-results.json
jq '.metadata.durationMs' .codacy/tmp/codacy-remote-results.json
```

Fetch the Cloud issue overview — this gives per-pattern issue counts, false positive counts, and suggested actions across the entire repository without downloading every individual issue:
```bash
codacy issues -O -o json > .codacy/tmp/codacy-cloud-overview.json
```
This overview data is valuable for tuning decisions in Step 4: it shows which patterns produce the most issues on Cloud (the production truth), includes false positive rates per pattern, and generates suggested actions to reduce noise (identifying patterns accounting for 10%+ of all issues or 3x the average). The suggested actions include ready-to-run disable commands, adapted for coding standard or config-file constraints. Save it for later comparison.

Also check for cloud-only tools — tools enabled in Cloud but not available in the local Analysis CLI. Get the local CLI's supported tools via `codacy-analysis info`, then compare against the Cloud-enabled tools list above. Any Cloud-enabled tool not in the `info` output is cloud-only (e.g., SonarSharp, Codacy ScalaMeta Pro). If cloud-only tools exist and have issues, fetch them:
```bash
codacy issues --output json > .codacy/tmp/codacy-remote-cloud-results.json
```

**Track B — NOT on Cloud, but local `.codacy/codacy.config.json` exists:**

```bash
# Store a copy for later merging and comparison
cp .codacy/codacy.config.json .codacy/tmp/codacy-previous-config.json

# Record BEFORE metrics
jq '[.tools[].patterns | length] | add' .codacy/codacy.config.json
jq '.tools | length' .codacy/codacy.config.json

# Run analysis with the existing local config
codacy-analysis analyze --install-dependencies --output-format json --output .codacy/tmp/codacy-previous-results.json

# Record BEFORE issue count and runtime
jq '.issues | length' .codacy/tmp/codacy-previous-results.json
jq '.metadata.durationMs' .codacy/tmp/codacy-previous-results.json
```

**Track C — No Cloud, no local config:**

Record BEFORE as unconfigured: 0 patterns, 0 tools, 0 issues, `null` runtime. No analysis to run.

Save the BEFORE metrics from whichever track ran. The broad config metrics from Steps 2-3 are internal only — they are NOT reported to the user.

#### 0c. Cloud noise pre-evaluation (Track A only)

If the Cloud overview was fetched (`.codacy/tmp/codacy-cloud-overview.json` exists), analyze it now to identify patterns that are already known to be noisy based on Cloud production data. This saves time by pre-disabling known noise before running local analysis.

Start by checking the overview's **suggested actions** — the CLI already identifies patterns accounting for 10%+ of all issues or 3x the average per-pattern count and provides ready-to-run disable commands. Use these suggestions as the primary signal, then supplement with the criteria below.

Parse the overview's `patterns` array (each entry has `{id, title, total}`) and false positive counts:

```bash
# Issue counts per pattern
jq '[.overview.patterns[] | {id, title, total}] | sort_by(-.total)' .codacy/tmp/codacy-cloud-overview.json

# Patterns with potential false positives (count > 0)
jq '[.overview.patterns[] | select(.potentialFalsePositives > 0) | {id, title, total, potentialFalsePositives, falsePositiveRatio: ((.potentialFalsePositives / .total) * 100 | round)}] | sort_by(-.falsePositiveRatio)' .codacy/tmp/codacy-cloud-overview.json
```

**Identify noisy patterns using these criteria:**

1. **Wrong-language patterns** — cross-reference pattern IDs against the discovered stack (Step 1 runs next, but the Cloud tools list from Step 0a gives a rough language picture). Pattern IDs often contain the target language (e.g., `python.`, `java.`, `ruby.`). Mark patterns for languages clearly not in the project.

2. **Convention/style noise** — patterns with very high issue counts (top 5% by count) in categories like CodeStyle, Documentation, or Comprehensibility are likely convention mismatches. Mark these as candidates.

3. **High false-positive ratio patterns** — patterns where a significant proportion of issues are flagged as potential false positives (e.g., `potentialFalsePositives / total > 30%`) are strong candidates for pre-disabling. These patterns are producing results that Codacy's own heuristics consider unreliable. Store the false positive data for use in Step 4b rule 7, where patterns with high false-positive ratios get additional scrutiny during local verification.

4. **Never pre-disable Security patterns** — security patterns are never marked for pre-disabling regardless of count or false-positive ratio. They are handled in Step 4 with full context.

5. **Never pre-disable Critical/High severity patterns** — these require local verification before any action.

**Classify each noisy pattern into two lists:**

- **`cloudNoiseLocal`** — noisy patterns from tools supported by the local Analysis CLI. These will be removed from `.codacy/codacy.config.json` immediately after `init --auto` in Step 2.
- **`cloudNoiseCloudOnly`** — noisy patterns from cloud-only tools (identified in Step 0b). These will be disabled via Cloud CLI during Step 6 (import), only if the import is performed.

Store both lists for use in Steps 2 and 6. This is a pre-filter — Step 4 will perform deeper noise evaluation on the local analysis results.

### Step 1: Discover repository stack

Run discovery to understand the repository's languages, frameworks, and libraries:

```bash
codacy-analysis discover --output-format json --output .codacy/tmp/codacy-discover.json
```

Parse the output to understand:
- Languages present in the project
- Frameworks and libraries in use (e.g., React, Django, Spring Boot)
- This informs noise evaluation in Step 4 (e.g., knowing a project uses React means JSX-related patterns are relevant)

Note: The Codacy Cloud check already happened in Step 0.

### Step 2: Initialize auto-tuned configuration

First, remove the existing `.codacy/codacy.config.json` if any (the backup copy was already stored in Step 0):

```bash
rm -f .codacy/codacy.config.json
```

Initialize with the broadest useful pattern set, filtered by the discovered stack:

```bash
codacy-analysis init --auto "Critical,High,Warning,Minor,AllSecurity,ErrorProne,Performance,BestPractice,UnusedCode,Compatibility,Complexity,Comprehensibility,CodeStyle,Documentation"
```

This filter means:
- `Critical` — Codacy-recommended (default) Critical-severity patterns
- `AllSecurity` — ALL Security-category patterns (including non-defaults)
- Everything else — Codacy-recommended (default) patterns at High, Warning, and Minor severity across all categories

The intent is to start broad and cut in Step 4 based on actual analysis data.

**Apply Cloud noise pre-filter (Track A only):** If `cloudNoiseLocal` patterns were identified in Step 0c, remove them from the newly created config now. For each pattern in `cloudNoiseLocal`, find it in `.codacy/codacy.config.json` under its tool's `patterns` array and remove it. This avoids wasting local analysis time on patterns already known to be noisy from Cloud production data. Track these removals for the summary (they are pre-filter changes, reported in `patternChanges` with reason referencing Cloud data).

**Merge preserved configuration** from the baseline stored in Step 0:
- **Track A** (Cloud): Merge from `.codacy/tmp/codacy-remote-config.json`
- **Track B** (local config): Merge from `.codacy/tmp/codacy-previous-config.json`
- **Track C** (no prior config): No merge needed

For the applicable track:
1. Read the newly created `.codacy/codacy.config.json`
2. Merge the global `exclude` array from the stored config (merge, don't replace — the new config may have its own excludes)
3. For each tool that exists in both stored and new config, merge its per-tool `exclude` array
4. For tools where `useLocalConfigurationFile` was `true` in the stored config and the tool still exists, restore that setting along with the `localConfigurationFile` path

**Record broad-config metrics** (internal — not the BEFORE reference for the summary):
```bash
# Count enabled patterns across all tools in the broad config
jq '[.tools[].patterns | length] | add' .codacy/codacy.config.json

# Count enabled tools in the broad config
jq '.tools | length' .codacy/codacy.config.json
```

### Step 3: Run broad-config baseline analysis

Run analysis with the broad config to see the full issue landscape. This is an internal step for tuning decisions — the BEFORE reference for the user-facing summary comes from Step 0.

```bash
codacy-analysis analyze --install-dependencies --output-format json --output .codacy/tmp/codacy-baseline.json
```

Always use `--output <file>` to avoid broken JSON from stdout buffering.

**Record broad-config metrics** (used for tuning decisions in Step 4, not for the summary):
```bash
# Total issues in broad config
jq '.issues | length' .codacy/tmp/codacy-baseline.json

# Total runtime in milliseconds
jq '.metadata.durationMs' .codacy/tmp/codacy-baseline.json
```

**Parse the issue distribution** — this is the basis for all tuning decisions:

```bash
# Issues grouped by pattern (noise detection)
jq '[.issues | group_by(.patternId) | .[] | {patternId: .[0].patternId, toolId: .[0].toolId, severity: .[0].severity, category: .[0].category, count: length}] | sort_by(-.count)' .codacy/tmp/codacy-baseline.json

# Issues by severity
jq '.issues | group_by(.severity) | map({severity: .[0].severity, count: length})' .codacy/tmp/codacy-baseline.json

# Issues by category
jq '.issues | group_by(.category) | map({category: .[0].category, count: length})' .codacy/tmp/codacy-baseline.json

# Top 20 files by issue count
jq '[.issues | group_by(.filePath) | .[] | {filePath: .[0].filePath, count: length}] | sort_by(-.count) | .[0:20]' .codacy/tmp/codacy-baseline.json

# Per-tool results
jq '.toolResults | map({toolId, status, issueCount, durationMs, filesAnalyzed})' .codacy/tmp/codacy-baseline.json
```

### Step 4: Smart noise evaluation and tuning

This is the core of the skill. Work through the baseline results using a structured, context-aware decision framework.

**Cloud overview as a cross-reference (Track A only):** If `.codacy/tmp/codacy-cloud-overview.json` exists (fetched in Step 0b), use its per-pattern issue counts and false positive data as a cross-reference against the local baseline. The cloud overview reflects the full repository analysis on Codacy (production truth), while the local baseline only covers files the local CLI can analyze. When a pattern shows high counts in the cloud overview but low counts locally, it may indicate cloud-only tool coverage — factor this into deduplication and disable decisions (don't disable a pattern that is still needed on Cloud). The false positive counts from the overview are especially valuable for rule 7 below — patterns with high false-positive ratios on Cloud are likely producing the same unreliable results locally.

#### 4a. Establish the noise floor

Calculate the percentage of Critical+High issues (severity `"Error"` or `"High"`) relative to total issues. This determines how aggressively to cut lower-priority categories:

| Critical+High % of total | Action on CodeStyle & Documentation patterns |
|---|---|
| **>50%** | Disable ALL CodeStyle and Documentation patterns at Minor and Warning severity. The codebase has serious problems — style issues are just noise obscuring them. |
| **30–50%** | Disable Minor-severity CodeStyle and Documentation patterns. Keep Warning-level ones. |
| **10–30%** | Keep all patterns, but focus file exclusions on noisy paths. |
| **<10%** | Keep everything — the codebase is clean enough to benefit from style enforcement. |

The same logic applies proportionally to other low-priority categories (Comprehensibility, Compatibility) when critical issues dominate. Use judgment.

#### 4b. Pattern-level decisions

For each pattern in the baseline results, sorted by issue count (highest first), apply this priority chain:

1. **Security patterns must cover every security concern.** Any pattern with `category == "Security"` stays enabled UNLESS another active pattern from a different tool already covers the same semantic concern (see rule 2). If a security pattern is noisy and no deduplication applies, exclude specific files instead of disabling the pattern.

2. **Cross-tool deduplication of overlapping patterns.** When multiple tools flag the same semantic concern (e.g., "hardcoded secrets", "SQL injection", "XSS", "unused imports"), identify the overlap by comparing issue messages, affected files, and affected lines. For the overlapping pair:
   - Keep the pattern from the more specialized or precise tool (e.g., Semgrep security rules over Biome generic checks; a dedicated SAST scanner over a general linter)
   - If precision is comparable, keep the pattern from the tool that is more actively used in the project (more patterns enabled, used in CI, has a local config file)
   - Disable the redundant pattern from the other tool
   - This is NOT removing a concern — it is deduplicating. The concern remains covered by the kept pattern.
   - This applies to ALL categories, not just Security — e.g., two tools both flagging "unused imports"
   - Document in the change log: which pattern was kept, which was disabled, and why the kept pattern is the better source

3. **NEVER disable valid Critical/High issues.** Patterns with `severity == "Error"` or `severity == "High"` that are finding real problems must stay. If they appear to be false positives, exclude the offending files rather than disabling the pattern.

4. **Wrong stack → disable.** Cross-reference with the discover output from Step 1. Patterns for languages or frameworks not present in the project are pure noise. Examples:
   - Python security patterns in a JavaScript-only project
   - Apex patterns from PMD7 in a Java-only project
   - Semgrep rules for languages not in the repo
   
   Remove these patterns from the config.

5. **Noise floor → disable.** Apply the decisions from 4a. If the noise floor says CodeStyle/Documentation at Minor severity should go, remove those patterns.

6. **Convention mismatch → disable.** If a pattern flags something that >80% of the codebase does consistently, the pattern contradicts the project's established conventions. Examples:
   - Tabs-vs-spaces rules when the entire project uses the "wrong" style consistently
   - Naming convention rules that don't match the project's established naming

7. **False-positive prone → disable.** Use the Cloud overview's false positive data (from Step 0c) as the primary signal: patterns where `potentialFalsePositives / total > 30%` are strong disable candidates — Codacy's own heuristics are flagging a significant share of their results as unreliable. For these patterns, review a sample of actual instances in the code to confirm. If the local instances confirm the pattern is producing low-value results for this codebase, disable it. For patterns without Cloud false-positive data, check if the pattern is known to produce high false-positive rates in general. Only disable after verifying the hits are genuinely not useful for this codebase.

8. **Parameter tuning over disabling.** Before disabling a valuable pattern, check if it has configurable parameters:
   - Lizard complexity thresholds — raise to match the codebase's actual complexity profile
   - Line length limits — set to the project's observed maximum
   - Other threshold-based rules — adjust to reduce false hits while keeping the rule active
   
   Tuning preserves coverage while reducing noise.

9. **File exclusion over disabling.** When a pattern is valid but fires on files where it doesn't apply, exclude the files rather than disabling the pattern. The pattern stays active for real source code.

#### 4c. File-level evaluation

Review the top files by issue count from the baseline results (Step 3). Exclusions must be **strictly data-driven** — only add exclusions for files/paths that actually appear in the baseline results and are producing meaningful noise.

**Important:** The analysis CLI already respects `.gitignore`. Files matched by `.gitignore` are never analyzed, so they do NOT need exclusion in the Codacy config. Do NOT preemptively add exclusions for paths like `dist/**`, `node_modules/**`, `build/**`, or `coverage/**` unless they are actually appearing in the results with issues.

**Process for each noisy file/path in the top-N by issue count:**

1. Check if the file represents generated code (e.g., `*.generated.ts`, `routeTree.gen.ts`, auto-generated API clients, `.pb.go` files)
2. Check if the file is vendored or third-party code committed to the repo (e.g., `.yarn/releases/`, `vendor/` that is not gitignored)
3. Check if the file is build output that was committed (not gitignored)
4. Check if the file is a test fixture, snapshot, or mock data that produces false positives from a specific tool
5. If any of the above apply, add to the appropriate exclusion:
   - Generated/vendored/build output that affect all tools: add to the global `exclude` array
   - Files noisy for a specific tool only: add to that tool's per-tool `exclude` array (e.g., markdownlint hitting `CHANGELOG.md`, Stylelint hitting committed vendor CSS)
6. If the file is legitimate source code, do NOT exclude it — address the noise through pattern-level tuning (rules 1-9 above) instead

Every exclusion must be justified by actual results. Do NOT maintain a prescriptive checklist of "always exclude these paths."

#### 4d. Tool-level evaluation

For each tool in the config:

- **Irrelevant to the stack?** If the discover output shows no files for a tool's target language, remove the entire tool entry. Examples: RuboCop in a project with no Ruby, Checkstyle in a project with no Java.
- **Failed to run?** Check `toolResults[].status`. If `"failed"`, check `errors[]` for the reason. Keep the tool in the config (it may work after fixing the root cause) but note it in the summary.
- **Zero issues?** A tool with zero issues is not noise — it's either confirming code quality or not finding its target files. Leave it enabled unless it's clearly irrelevant to the stack.

#### 4e. Lost patterns recovery

Compare the baseline analysis results (from Step 0) against the current `.codacy/codacy.config.json` after tuning. For each pattern that:
- Found issues in the baseline analysis (`.codacy/tmp/codacy-remote-results.json` for Track A, `.codacy/tmp/codacy-previous-results.json` for Track B)
- Has `category == "Security"` OR `severity == "Error"` OR `severity == "High"`
- Is NOT present in the current config (was excluded by `init --auto` or removed during tuning)

→ Add it back to the config under the appropriate tool. This is an internal preservation step — restored patterns are NOT reported as changes in the summary (they were already in the baseline config, so from the user's perspective nothing changed).

Skip this step for Track C (no prior config — nothing to recover).

#### Apply all changes

Edit `.codacy/codacy.config.json` with all decisions from 4a–4e. Track every change for the summary in Step 5:
- For each disabled pattern: record the patternId, action `"disabled"`, and reason
- For each tuned pattern: record the patternId, action `"updated"`, old/new parameters, and reason
- For each removed tool: record it in `toolChanges`
- For each added tool: record it in `toolChanges`
- For each new file exclusion added: record it in `fileExclusions`
- Restored patterns (Step 4e) are NOT included in the summary — they preserve the status quo

**Security guardrail — mandatory check before saving.** Before writing the updated config, verify that every **security concern** (e.g., hardcoded secrets, SQL injection, XSS, path traversal, open redirects) is still covered by at least one active pattern with `category == "Security"`. A security pattern may be disabled only if another active pattern from a different tool covers the same concern (cross-tool deduplication per rule 2 in Step 4b). If any concern has lost all coverage, re-enable the most precise pattern for that concern.

#### 4f. Validation pass

Run analysis with the tuned config to validate the improvement:

```bash
codacy-analysis analyze --install-dependencies --output-format json --output .codacy/tmp/codacy-tuned.json
```

**Record AFTER metrics:**
```bash
# Enabled patterns after tuning
jq '[.tools[].patterns | length] | add' .codacy/codacy.config.json

# Enabled tools after tuning
jq '.tools | length' .codacy/codacy.config.json

# Total issues after tuning
jq '.issues | length' .codacy/tmp/codacy-tuned.json

# Runtime after tuning
jq '.metadata.durationMs' .codacy/tmp/codacy-tuned.json
```

**Validate:**
- Issues should have decreased meaningfully vs the broad-config baseline (Step 3).
- If issues increased or didn't decrease meaningfully (<20% reduction), review the tuning decisions and re-iterate once: go back to "Do AI analysis of the results" (Step 4b) with the updated results, apply further changes, and re-run this validation.
- The goal is that every remaining issue is worth looking at.

### Step 5: Show local results

#### 5a. Generate summary JSON

Write `.codacy/configure-codacy-summary.json` with the before/after metrics, a detailed change log, and supporting context. Runtime values are in milliseconds (raw `durationMs` from the CLI).

**The `before` values come from Step 0** (the baseline captured before any changes — Cloud config for Track A, local config for Track B, or unconfigured for Track C). **The `after` values come from Step 4f** (the final tuned configuration). If no initial config existed (Track C), `before` values reflect an unconfigured state — use `null` for metrics that cannot be measured (e.g., runtime) and `0` for counts (patterns, tools, issues).

```json
{
  "summary": {
    "enabledPatterns": { "before": 1000, "after": 300 },
    "enabledTools": { "before": 34, "after": 15 },
    "issues": { "before": 7000, "after": 550 },
    "analysisRuntime": { "before": 240000, "after": 60000 }
  },
  "toolChanges": [
    {
      "toolId": "Biome",
      "action": "disabled",
      "reason": "Project uses ESLint9 with local config; Biome is redundant and produced 16K false positives in TypeScript",
      "patternsAffected": 232
    },
    {
      "toolId": "markdownlint",
      "action": "enabled",
      "reason": "New tool added for Markdown linting; README.md excluded per-tool to avoid inline HTML noise",
      "patternsAffected": 43
    }
  ],
  "patternChanges": [
    {
      "patternId": "Semgrep_python.lang.security.audit.xss.template-injection",
      "toolId": "Semgrep",
      "action": "disabled",
      "reason": "Wrong stack — pattern for Python; project is JavaScript-only",
      "delta": -45,
      "parameters": []
    },
    {
      "patternId": "Lizard_ccn-medium",
      "toolId": "Lizard",
      "action": "updated",
      "reason": "Raised threshold from 10 to 20 to match codebase complexity profile",
      "delta": -120,
      "parameters": [
        { "id": "threshold", "before": "10", "after": "20" }
      ]
    },
    {
      "patternId": "Semgrep_codacy.javascript.security.hard-coded-password",
      "toolId": "Semgrep",
      "action": "enabled",
      "reason": "New High Security pattern — detects hardcoded passwords; found 101 issues across 41 files for review",
      "delta": 101,
      "parameters": []
    }
  ],
  "fileExclusions": {
    "global": ["src/routeTree.gen.ts"],
    "perTool": {
      "markdownlint": ["README.md"]
    }
  },
  "securityCoverage": {
    "deduplication": [
      "Semgrep slack-webhook-url disabled — same concern covered by Semgrep detected-slack-webhook"
    ],
    "newCoverage": [
      "unsafe-dynamic-method (Critical, 5 issues)",
      "open-redirect-from-function (Critical, 4 issues)",
      "hard-coded-password (High, 101 issues)"
    ],
    "noisyButKept": [
      "Semgrep hard-coded-password (101 issues) — kept per security guardrail, file exclusions preferred over disabling"
    ]
  },
  "keyImprovements": [
    "Lizard complexity thresholds tuned to match mature React SPA — 576 fewer noise issues while keeping genuinely complex functions flagged",
    "6 new security patterns detecting open redirects, unsafe dynamic methods, hardcoded passwords, and React href injection (119 new findings)",
    "markdownlint added for Markdown quality",
    "Checkov expanded from 6 to 1358 IaC security patterns"
  ],
  "localConfigTools": [
    {
      "toolId": "ESLint9",
      "configFile": "eslint.config.js",
      "issueCount": 42,
      "note": "Issues from this tool are controlled by the project's ESLint config, not Codacy patterns. Edit eslint.config.js to reduce noise."
    }
  ],
  "codacyYaml": null,
  "importResults": null,
  "cloudVerification": null
}
```

**Field reference:**

**`summary`** — before/after metrics (same as before).

**`toolChanges`** — one entry per tool added or removed. Each entry:
- `toolId` — the tool identifier
- `action` — `"enabled"` (tool was added) or `"disabled"` (tool was removed)
- `reason` — why the tool was added or removed
- `patternsAffected` — number of patterns in the tool that was added/removed

**`patternChanges`** — one entry per individual pattern change. Each entry:
- `patternId` — the pattern identifier
- `toolId` — which tool this pattern belongs to
- `action` — `"enabled"`, `"disabled"`, or `"updated"`
- `reason` — why this change was made (auditability)
- `delta` — the change in issue count for this pattern, comparing INITIAL state (Step 0) vs FINAL tuned state (Step 4f). If the pattern was not enabled in the initial config, the delta is the full issue count from the tuned analysis (positive if newly enabled, 0 if disabled during tuning).
- `parameters` — parameter changes (empty array if not applicable)

Do NOT include individual pattern entries inside `patternChanges` for patterns that were added/removed as part of a whole tool change. Those are covered by the `toolChanges` entry. `patternChanges` is for surgical, individual pattern changes within a tool that remains enabled.

Do NOT include `"restored"` patterns here. Restoration (Step 4e) is an internal mechanism to ensure patterns from the baseline config that had Critical/High/Security results aren't lost by `init --auto`. It preserves what was already there — it's not a user-facing change.

**`fileExclusions`** — only lists **new** exclusions added during this tuning run. Exclusions already present in the baseline config are preserved automatically but not listed here (they are not changes).
- `global` — new global exclusion globs added during tuning
- `perTool.<toolId>` — new per-tool exclusion globs added during tuning

Omit `fileExclusions` entirely if no new exclusions were added.

**`securityCoverage`** — documents how security concerns are handled:
- `deduplication` — security patterns that were disabled because another pattern covers the same concern (list the kept pattern and the disabled one)
- `newCoverage` — new security patterns enabled that were NOT in the baseline config, with issue count
- `noisyButKept` — security patterns that are noisy but were kept active per the security guardrail

**`keyImprovements`** — array of 3–6 human-readable sentences summarizing the most impactful improvements. Focus on what changed and the quantitative impact. These should be suitable for presenting to the user as a summary.

**`localConfigTools`** — array of tools that have `useLocalConfigurationFile: true`. Each entry includes:
- `toolId` — the tool identifier
- `configFile` — path to the project's config file used by this tool
- `issueCount` — number of issues this tool produced in the tuned analysis
- `note` — human-readable explanation that noise from this tool is governed by the project's own config, not Codacy patterns

Empty array if no tools use local configuration files.

**`codacyYaml`** — string containing the generated `.codacy.yaml` file content if file exclusions were added (see Step 5c). `null` if no `.codacy.yaml` was generated.

**`importResults`** — `null` until Step 6 runs. If Cloud import is performed, this is populated with the results (see Step 6f for the schema).

**`cloudVerification`** — `null` unless Step 6e runs. Contains post-import Cloud verification results: whether reanalysis completed, issue counts before/after, patterns disabled on Cloud, and warnings. See Step 6e for the schema.

#### 5b. Present local results

Display a clear before/after summary to the user:

1. **Metrics table** — enabled patterns, enabled tools, total issues, and runtime (before vs after, with reduction %). The "before" is the baseline from Step 0. If no prior config existed (Track C), note "No prior configuration" in the before column.
2. **Tool changes** — tools added or removed, with reasons
3. **Top pattern changes by impact** — the `patternChanges` entries with the largest `|delta|`, sorted descending
4. **New security coverage** — new security patterns that were not in the baseline config
5. **Security deduplication** — any security patterns that were deduplicated (which was kept, which was disabled)
6. **Key improvements** — the `keyImprovements` array from the summary JSON, presented as a bulleted list
7. **Warnings** — failed tools, Semgrep parsing errors, tools with 0 files matched, any other issues encountered
8. **Local config file limitations** — for tools with `useLocalConfigurationFile: true`, note that their issues are controlled by the project's own config file (e.g., `.eslintrc`, `.rubocop.yml`), not by Codacy's managed patterns. Noise from these tools can only be reduced by editing the project's own config. List each such tool and the number of issues it produced, so the user knows where to look if they want further noise reduction.

#### 5c. Generate `.codacy.yaml` for Cloud file exclusions

File exclusions in `.codacy/codacy.config.json` only apply to local analysis. Codacy Cloud does not support importing file exclusions via the API or CLI. To apply file exclusions on Codacy Cloud, they must be defined in a `.codacy.yaml` file committed to the repository root (see [Codacy configuration file](https://docs.codacy.com/repositories-configure/codacy-configuration-file/)).

**If any new file exclusions were added during tuning** (global or per-tool), generate a `.codacy.yaml` file:

1. Read the existing `.codacy.yaml` from the repo root (if it exists) to preserve any existing configuration
2. Merge the new exclusions with any existing `exclude_paths` and per-engine `exclude_paths`
3. Write the updated `.codacy.yaml` to the repo root

The `.codacy.yaml` format uses Java glob syntax:
```yaml
---
exclude_paths:
  - "src/routeTree.gen.ts"
  - "vendor/**"
engines:
  markdownlint:
    exclude_paths:
      - "CHANGELOG.md"
  stylelint:
    exclude_paths:
      - "assets/vendor/**"
```

**Engine name mapping:** The engine names in `.codacy.yaml` may differ from the tool IDs in `.codacy/codacy.config.json`. Use the tool ID in lowercase as the engine name (e.g., `ESLint9` → `eslint9`, `Semgrep` → `semgrep`, `markdownlint` → `markdownlint`). If unsure, the tool ID in lowercase is the safe default.

4. Store the full content of the generated `.codacy.yaml` as a string in the `codacyYaml` field of the summary JSON
5. Present to the user:
   - Note that file exclusions cannot be imported to Codacy Cloud via API
   - The `.codacy.yaml` file has been created/updated in the repo root
   - The user should commit and push this file to apply the exclusions on Codacy Cloud
   - Codacy Cloud always reads `.codacy.yaml` from the default branch

If no new file exclusions were added, skip this step and leave `codacyYaml` as `null`.

### Step 6: Cloud import (conditional)

#### 6a. Check Cloud status

If the repo is NOT on Codacy Cloud (from Step 0): skip this step entirely. Note in the results: "The configuration is ready for local analysis. To use it on Codacy Cloud, first add the repository to Codacy."

#### 6b. Determine import behavior

Based on invocation mode (see "Invocation modes" section):

1. **Auto-import mode** (user invoked with "import" argument): Proceed directly to 6c.
2. **Interactive mode** (default): Use `AskUserQuestion` to ask the user: "Want to update these configurations in Codacy Cloud?" If the user declines, skip to Step 7.
3. **Local-only mode**: Already handled in 6a (skipped).

#### 6c. Cloud-only tools noise evaluation

Only if cloud-only tools had issues fetched in Step 0 (`.codacy/tmp/codacy-remote-cloud-results.json` exists):

Apply the same noise evaluation framework from Step 4 to the cloud-fetched issues. For each noisy pattern from a cloud-only tool:
- Check if its parameters can be tweaked to return fewer results → `codacy pattern <toolName> <patternId> --parameter key=value`
- If not tweakable → try to disable it: `codacy pattern <toolName> <patternId> --disable`
- If disable fails (Coding Standard enforcement) → note it for the results

#### 6d. Import local config

```bash
codacy tools --import .codacy/codacy.config.json -y
```

If the import encounters Coding Standard conflicts (409 errors — patterns/tools enforced at org level cannot be overridden):

1. **If force mode is enabled** (user invoked with "force" argument): Automatically retry with `--force`:
   ```bash
   codacy tools --import .codacy/codacy.config.json --force -y
   ```
   Note in the results that `--force` was used and which Coding Standards were unlinked.

2. **If force mode is NOT enabled** (default): Do **NOT** automatically retry with `--force`. Instead:
   - Report which tools/patterns could not be changed due to Coding Standard enforcement
   - List the specific Coding Standards that are blocking the changes
   - Use `AskUserQuestion` to ask the user: "The import was partially blocked by Coding Standards [list names]. Would you like to unlink these Coding Standards and retry with --force? This will sever the link between this repository and the organization-level standards."
   - If the user accepts → retry with `--force`
   - If the user declines → keep the partial import as-is and note the blocked changes in the results

**NEVER unlink Coding Standards without explicit user consent or the "force" invocation flag.**

**Important:** The `.codacy/codacy.config.json` file is for local use only. Committing or pushing it to the repository has NO effect on Codacy Cloud. The import command is the only way to sync local config to Cloud.

#### 6e. Post-import Cloud verification

After a successful import (or partial import), trigger reanalysis and wait for Cloud results to verify the configuration works as expected in the Cloud environment. Cloud analysis may differ from local analysis (different tool versions, containerized execution, file visibility).

**1. Trigger reanalysis and wait for completion:**

Use `--reanalyze-and-wait` to trigger reanalysis, poll automatically (every 10 seconds, up to 20 minutes), and get a delta report of issue changes by pattern, severity, and category:

```bash
codacy repository --reanalyze-and-wait -o json > .codacy/tmp/codacy-reanalysis-delta.json
```

This replaces manual polling. The CLI captures a baseline before reanalysis, waits for completion, and reports the full delta. If it times out after 20 minutes, it reports what it knows and exits — note the timeout in warnings and proceed without full Cloud verification.

**2. Fetch fresh Cloud overview and evaluate:**

Once reanalysis is complete (check the delta report), get the updated issue overview:
```bash
codacy issues -O -o json > .codacy/tmp/codacy-post-import-overview.json
```

Compare the post-import overview against the pre-import overview (`.codacy/tmp/codacy-cloud-overview.json`). For each pattern in the new overview, sorted by issue count (highest first):

- If a pattern has a **high issue count** and is **not** in the Security category and **not** Critical/High severity → it is a candidate for Cloud-side disabling
- Apply the same noise framework from Step 4b (wrong-language, convention mismatch, deduplication) using Cloud data
- For patterns that should be disabled, use the Cloud CLI:
  ```bash
  codacy pattern <toolId> <patternId> --disable
  ```
- If a disable fails due to Coding Standard enforcement, note it in warnings
- Also disable any patterns in the `cloudNoiseCloudOnly` list from Step 0c that were deferred for this moment

**4. Record Cloud verification results:**

Track all Cloud-side pattern changes in the summary under a new `cloudVerification` field:
```json
{
  "cloudVerification": {
    "reanalysisCompleted": true,
    "issuesBefore": 375,
    "issuesAfter": 280,
    "patternsDisabled": [
      {
        "patternId": "markdownlint_MD033",
        "toolId": "markdownlint",
        "reason": "Convention mismatch — 150 inline HTML issues in documentation files",
        "issueCount": 150
      }
    ],
    "warnings": []
  }
}
```

If reanalysis timed out or Cloud verification was skipped, set `reanalysisCompleted: false` and note the reason in warnings.

#### 6f. Show Cloud import results

Update the `importResults` field in `.codacy/configure-codacy-summary.json` with the import outcome:

```json
{
  "importResults": {
    "status": "success | completed_with_errors | failed",
    "toolsConfigured": 10,
    "toolsEnabled": ["markdownlint"],
    "toolsDisabled": ["PMD"],
    "errors": [
      {
        "toolId": "ESLint9",
        "error": "Conflict (409)",
        "detail": "Unable to update Project Tool Patterns, repository is using a Configuration File"
      },
      {
        "toolId": "PMD",
        "error": "Conflict (409)",
        "detail": "Cannot disable a tool that is enabled by a standard"
      }
    ],
    "warnings": [
      "7 Semgrep pattern parsing errors (non-blocking)",
      "Agentlinter: 0 files matched — no agent config files in this SPA"
    ],
    "codingStandards": ["AI Policy", "Our Default + SOC2"],
    "forceUsed": false
  }
}
```

**`importResults` field reference:**
- `status` — `"success"` if all tools imported without errors, `"completed_with_errors"` if some tools failed but others succeeded, `"failed"` if the import command itself failed
- `toolsConfigured` — number of tools successfully configured
- `toolsEnabled` — tools that were newly enabled in Cloud (were disabled before)
- `toolsDisabled` — tools that were disabled in Cloud (were enabled before) — may be empty if Coding Standard prevents disabling
- `errors` — array of per-tool errors, each with `toolId`, `error` (HTTP status or error type), and `detail` (the error message from the CLI)
- `warnings` — array of non-blocking warnings (analysis errors, tools with 0 files, etc.)
- `codingStandards` — names of Coding Standards linked to the repository (from Step 0), or empty array if none
- `forceUsed` — whether `--force` was used to unlink a Coding Standard

Present the import results to the user:
- What was updated successfully
- What couldn't be changed (Coding Standard enforcement) — list each error with its detail
- Cloud-only tool pattern changes (from 6c)
- Whether `--force` was used and what that implies

### Step 7: Clean-up

Remove the temporary directory and all intermediate files:

```bash
rm -rf .codacy/tmp
```

## Per-tool tuning tips

### Semgrep

Semgrep ships patterns for 30+ languages. After init, many patterns will be for languages not in the project. In Step 4, **disable patterns for languages not found by `discover`** — this is usually the single biggest noise reduction. Cross-reference the pattern ID prefix (e.g., `python.`, `javascript.`, `java.`) against the discovered languages.

### Lizard (complexity)

Lizard has rules for cyclomatic complexity (CCN), lines of code (NLOC), and parameter count, each at three severity levels (Critical, Medium, Minor) with configurable `threshold` parameters.

For **established/mature codebases**, the default Medium thresholds produce hundreds of hits on legacy code. Options:
- Disable Medium-level rules and keep only Critical
- Or raise Medium thresholds to match the project's actual complexity profile (better — preserves visibility)

For **greenfield projects**, the default thresholds are reasonable.

### ESLint9

ESLint loads the project's own config file (e.g., `eslint.config.js`), which may import packages. If the project has an existing ESLint config, the `--install-dependencies` flag in Step 3 should handle this. If ESLint still fails with `InvocationError`, the project may need `npm install` or equivalent before analysis.

If the project has a pre-existing ESLint configuration and the user wants to keep it, set `useLocalConfigurationFile: true` on the ESLint9 tool entry instead of using Codacy's managed patterns.

### markdownlint

Rules like MD034 (bare URLs), MD024 (duplicate headings), MD010 (hard tabs), MD004 (list style), MD033 (inline HTML), and MD036 (emphasis as heading) fire heavily on CHANGELOGs and auto-generated docs. These are stylistic, not bugs. Prefer excluding the noisy files (via per-tool `exclude`) over disabling the rules entirely.

### Stylelint

Review results in context — some CSS rules that look like violations may be intentional (e.g., apps that override third-party styles often need `!important` and qualified selectors). When the project has a pre-existing Stylelint config, consider using `useLocalConfigurationFile: true`.

## Security guardrail

> **Every security concern must be covered by at least one active pattern.** This is a hard rule with no exceptions.

The guardrail operates at the **concern level**, not the individual pattern level. If two tools both detect "hardcoded secrets," disabling the less precise one is acceptable because the concern remains covered. However, if a security concern (e.g., SQL injection, XSS, path traversal, hardcoded secrets) would lose ALL active pattern coverage, the disable must be reverted.

When a security pattern is noisy and cannot be deduplicated:
- **Exclude specific files** where it triggers false positives (e.g., test fixtures, mock data)
- **Leave the false positives** for the user to triage in Codacy Cloud (they can ignore individual instances with a reason)
- **Never remove the last pattern covering a security concern** — it must stay active to catch real vulnerabilities in future code

For Critical/High severity patterns in non-Security categories, apply the same caution: prefer file exclusion over pattern disabling. Only disable these if they are clearly for the wrong stack (e.g., a Java Critical pattern in a pure Python project).

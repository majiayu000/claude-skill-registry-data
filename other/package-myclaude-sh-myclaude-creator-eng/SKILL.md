---
name: package
description: >-
  Package a product for distribution across 33+ platforms. Strips WHY comments, generates
  triple manifests (vault.yaml + plugin.json + agentskills.yaml), stages .publish/. Use
  when: 'package', 'prepare for publish', or 'bundle it'.
argument-hint: "[product-slug] [--express]"
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# Packager

Stage a product for distribution with triple manifests (MyClaude + Anthropic Plugin + Agent Skills universal).

**When to use:** After /validate passes. Before /publish.

**When NOT to use:** If the product hasn't been validated yet (run /validate first).

---

## Activation Protocol

0. **Shared preamble:** Load `references/quality/activation-preamble.md` — context assembly, persona adaptation, deterministic routing rules.
1. Identify product: `$ARGUMENTS` as slug → `workspace/{slug}/`
1b. **Mode selection (Express vs Guided).** Read `creator.yaml → preferences.workflow_style`. Resolve the flow mode:
    - `--express` flag OR `workflow_style == "autonomous"` → **Express mode**. Skip the "confirm before stage" prompt, skip the manifest preview step, and produce a single post-stage summary. The safety invariants below still hold — only the conversational confirmations are trimmed.
    - `workflow_style == "guided"` or missing → **Guided mode** (default). Confirm before staging, show manifest preview, and walk the creator through the pipeline with full voice.
2. Read `.meta.yaml` → verify state is "validated" and MCS score >= 75%
3. Read `creator.yaml` → load author metadata for manifests. If missing → "Creator profile not found. Run `/onboard` first." and stop.
4. **Maintain creator persona**: Adapt language, depth, and examples to `profile.type` and `technical_level` throughout this skill's execution. A developer gets code examples; a domain expert gets plain language.
5. Load `product-dna/{type}.yaml` → get install_target
6. Load `config.yaml` → vault_defaults for missing fields
6b. **Load proactives:** Load `references/engine-proactive.md` — wire #1 (pipeline guidance: after package, guide to /publish), #20 (test mandate: if MCS-2+ and `.meta.yaml.test_result != "pass"`, block packaging with message "Run /test first").
7. **Load voice identity:** Load `references/quality/engine-voice-core.md`. Every user-facing line in this skill honors the ✦ signature, three tones, and six anti-patterns.
8. **CLI contract:** Load `references/cli-contract.md` for unified error handling. This skill has conditional severity based on pricing model. Severity map:
   - **Blocking (paid products only):** `stripe status` — if product price > 0 and Stripe not connected, halt packaging
   - **Silent-skip (free products):** `stripe status` — irrelevant for free products, skip without warning
   - **Silent-skip:** `search --category {type} --sort price-desc` — competitive pricing scan, skip without warning on failure
   - **All queries:** append `2>/dev/null`, 15s timeout, treat invalid JSON as CLI absent

---

## Core Instructions

### PACKAGING PIPELINE

**SAFETY INVARIANTS — see end of file (positioned per D19 attention-aware authoring for maximum model compliance).**

**Step 1 — Verify Validation**

Read `.meta.yaml` for validation state:
- If state != "validated" AND state != "packaged": "Product not validated. Run /validate first."
- If MCS score < 75%: "Product below MCS-1 threshold. Run /validate --fix."
- If mcs_target is "MCS-2" or "MCS-3" AND (test_result is null OR test_result != "pass"): "MCS-2+ products require behavioral testing before packaging. Run /test first." — BLOCKING. This gate ensures structural validation (/validate) AND behavioral validation (/test) both pass before distribution.

**Step 1.5 — Package Rename** (if applicable)

Check `product-dna/{type}.yaml` for `package_rename` field. If present, rename the
primary file to the specified pattern during copy to `.publish/`.

Currently applies to:
- **minds:** `AGENT.md` → `{slug}.md` (flat file convention for `.claude/agents/`)

This rename ensures the installed filename matches Claude Code's native discovery pattern.

**Step 2 — Strip WHY Comments + Inject Attribution** (SE-D17)

Create a clean copy of all product files.

**REMOVE:**
- `<!-- WHY: ... -->` (HTML comment blocks — may span multiple lines)
- Lines matching `# WHY:` pattern (markdown comment format)
- `# WHY:` pattern in shell scripts (`.sh` files)
- JSON keys prefixed with `_` (e.g., `_comment`, `_why`, `_events_reference`) from `.json`
  files. These are documentation keys used in workspace but must not pollute the user's
  settings.json when hooks are installed. Strip by parsing JSON, removing `_`-prefixed
  top-level keys, and re-serializing.

**INJECT TWO THINGS** into the `.publish/` copy of the primary file (SKILL.md, AGENT.md, etc.):

**1. Marketplace URL in frontmatter** (PRD D3 — viral vector #1):
Add a `marketplace_url` field to the YAML frontmatter of the primary file. This field is read by Claude Code in EVERY session where the product is installed — making every buyer a passive distribution carrier.
```yaml
---
name: {slug}
description: >
  {original description — DO NOT MODIFY}
marketplace_url: "https://myclaude.sh/p/{slug}"
---
```
Rules:
- Add `marketplace_url` as a NEW field — never modify the existing `description`
- Only add to the `.publish/` copy — never touch the original in workspace/
- Use the slug from vault.yaml

**2. Attribution comment at end of file:**
```html
<!-- Published on MyClaude (myclaude.sh) | Quality: MCS-{level} ({score}%) | Engine: Studio v3 -->
```
This attribution comment is:
- Invisible to Claude (HTML comment, does not affect behavior)
- Visible in source code (GitHub renders it in raw view)
- Indexable by search engines (creates discoverable MyClaude references)
- A quality signal (MCS score travels with the product)

Never modify originals — work on the copy in `.publish/`.

**Step 2c — Inject README Badges** (PRD B2 — viral vectors #2)

Append MCS and Available badges to the end of `.publish/README.md`:
```markdown

---

[![MCS-{level}](https://myclaude.sh/badge/mcs/{level}.svg)](https://myclaude.sh/quality)
[![Available on MyClaude](https://myclaude.sh/badge/available.svg)](https://myclaude.sh/p/{slug})

<sub>Built with MyClaude Studio Engine</sub>
```
**Precondition:** Verify `.publish/README.md` exists before injection. If missing (bundle type has no README requirement), skip badge injection silently — do not create a README just for badges.

**README quality gate:** Before badge injection, verify README follows `templates/readme/README.md.template` structure — at minimum: Hero, Install (with `myclaude install {slug}`), Quick Start, Features (3+), Requirements. If missing critical sections, WARN: "README is missing sections that help users decide to install. Consider running `/fill` to complete it." Continue packaging — this is advisory, not blocking.

Rules:
- Inject ONLY in `.publish/README.md` — never modify the original
- MCS level from `.meta.yaml` `state.dna_compliance` or `overall_score`. Default to 1 if not validated
- Slug from vault.yaml `name` field
- Add a blank line before the `---` separator to avoid markdown parsing issues

**Step 2b — Verify WHY Removal**

Grep all files in `.publish/` for the pattern `WHY:`. If match count > 0, re-run stripping on the matched files. If still > 0 after second pass, report error with file paths and line numbers — do not proceed to manifest generation with unstripped WHY comments.

**Step 2d — Post-Strip Integrity Check**

After WHY removal, verify the stripped files are still structurally valid:
- For `.md` files: verify YAML frontmatter still parses (regex for `^---\n` ... `\n---\n`)
- For `.json` files (hooks.json, settings-fragment.json): parse with JSON validator after `_`-prefixed key removal. If parse fails → abort with file path and error. Never ship invalid JSON.
- For `.sh` files: verify shebang line survived stripping (first line must start with `#!`)
- If any check fails: report the specific file + line + issue. Do NOT proceed to manifest generation.

**Step 3 — Generate vault.yaml**

Read `.meta.yaml → intent_declaration.language` (written by /create Step 11). This is
the canonical source of truth for the product's source language — it captures what
language the product was **forged in**, not what language the creator is currently
using. If the field is missing (pre-Wave-3 legacy product), fall back to
`creator.yaml → creator.language`, then to `"en"` as the final default.

```yaml
# REQUIRED (from .meta.yaml + creator.yaml)
name: "{slug}"
version: "{from .meta.yaml or config default}"
type: "{product type}"
description: "{from README.md first paragraph or .meta.yaml}"
entry: "{primary file from product-dna/{type}.yaml}"
license: "{from creator.yaml or config default}"
price: {from .meta.yaml or 0}
tags: ["{from .meta.yaml}"]

# LOCALE CONTRACT — see references/locale-adaptive-clause.md §8 for the full wiring map.
# source_language travels with the product to the marketplace so the UI can
# render the "Source: {language} · Adapts to your language at runtime" badge.
# These four fields are REQUIRED for any product that was forged with the
# locale-adaptive clause (all 6 certified types). Omit the block only for
# types that do not carry the clause (bundle, claude-md, application, hooks,
# statusline, design-system, workflow — per locale-adaptive-clause.md §4).
source_language: "{from .meta.yaml intent_declaration.language, fallback to creator.yaml language, fallback to 'en'}"
locale_adaptive: true
locale_adaptive_source: "references/locale-adaptive-clause.md"
locale_adaptive_version: "1.0"
```

**Step 3b — Pricing Intelligence** (Intelligence Layer integration)

Read `.meta.yaml → intelligence` fields. If `value_score` is populated (set by /validate Stage 8), display value-informed pricing context:

```
Value Intelligence:
  Value score: {value_score}/12 ({pricing_strategy})
  Suggested range: ${suggested_price_range[0]}-${suggested_price_range[1]}
  Current price: ${price from .meta.yaml or vault_defaults}
  {If price == 0 AND value_score >= 5: "Your product scores {value_score}/12 — consider pricing at ${suggested_price_range[0]}+ based on depth and uniqueness."}
  {If price > 0 AND price > suggested_price_range[1]: "Current price exceeds value signal range. Ensure README clearly communicates the premium."}
  {If price > 0 AND price < suggested_price_range[0]: "Priced below value signal. You're leaving value on the table — or strategically building audience."}
  {If value_score not set: "Run /validate --level=2 to compute value intelligence."}
```

If the product has a non-zero price:

1. **Stripe check:** Run `myclaude stripe status 2>/dev/null`
   - If not connected: BLOCKING — "Paid products require Stripe. Run `myclaude stripe connect` first."
   - If connected: proceed

2. **Competitive pricing scan:** Run `myclaude search --category {type} --sort price-desc --limit 5 --json 2>/dev/null`
   If results found, display:
   ```
   Pricing context for {type} products:
     Highest: ${max_price} ({name})
     Average: ${avg_price}
     Your price: ${price}
     {If price > avg: "Premium positioning" | If price < avg: "Value positioning" | If price == 0 and others charge: "Consider charging — similar products average ${avg}"}
   ```

3. **MCS-price alignment:** If price > $5 AND mcs_level < 2, warn:
   "Price is ${price} but MCS is level {level}. Users expect MCS-2+ for paid products. Consider running `/validate --level=2` to increase quality."

**Epistemic caveat (always shown when value intelligence is displayed):**
> "Value signal is estimated from structural quality + market position. Real value is confirmed by daily use."

Continue to enrichment:

```yaml

# ENRICHMENT (from .meta.yaml + creator.yaml + computed)
displayName: "{humanized from name}"
mcsLevel: {from last validation score}
language: "{from creator.yaml}"
longDescription: "{from README.md}"
readme: "README.md"
installTarget: "{from product-dna/{type}.yaml}"
language: "{from creator.yaml or 'en'}"
compatibility:
  claude_code: ">=1.0.0"

# DISTRIBUTION DNA (viral growth layer — links back to MyClaude ecosystem)
engine: "myclaude-studio-engine"
marketplace: "https://myclaude.sh/p/{slug}"
badges:
  mcs: "https://myclaude.sh/badge/mcs/{mcs_level_number}.svg"
  available: "https://myclaude.sh/badge/available.svg"
```

**Step 4 — Generate plugin.json** (Anthropic Plugin Marketplace)

**Settings priority:** Plugin settings are LOWEST priority in CC's 6-level hierarchy (Plugin < User < Project < Local < Flag < Policy). This means user/project settings always override plugin defaults. Hooks from plugins ACCUMULATE (never replace existing hooks). MCP servers from plugins REPLACE entirely.

Schema constraints (enforce strictly — wrong structure causes silent install failures):
- `author` MUST be an object `{ "name": "...", "url": "..." }` — never a plain string
- `skills` field uses a **directory path** (e.g., `".claude/skills/slug/"`) — CC loads all .md files in it
- `agents` field uses an **explicit file path array** (e.g., `[".claude/skills/slug/AGENT.md"]`) — NOT a directory
- `commands` field uses a **directory path** (e.g., `".claude/commands/"`)
- `hooks` key does NOT belong in plugin.json — hooks are declared in a separate `hooks.json` file
- Only `agent` key is valid inside `settings.json` plugin settings (not `skill`, `workflow`, etc.)

Emit only the fields relevant to the product type:

```json
{
  "name": "{slug}",
  "description": "{description}",
  "version": "{version}",
  "author": { "name": "{from creator.yaml display_name}", "url": "https://myclaude.sh/u/{from creator.yaml username}" },
  "license": "{license}",
  "homepage": "https://myclaude.sh/p/{slug}",

  // --- Include ONE of the following blocks based on product type ---

  // type=skill or type=workflow or type=squad or type=claude-md:
  "skills": ".claude/skills/{slug}/",

  // type=agent:
  "agents": [".claude/skills/{slug}/AGENT.md"],

  // type=minds:
  "agents": [".claude/agents/{slug}.md"],

  // type=system (if it exposes commands):
  "commands": ".claude/commands/"

  // NOTE: hooks type — no content field in plugin.json. hooks.json is the artifact.
  // NOTE: statusline type — no content field in plugin.json. statusline.sh is the artifact.
  // NOTE: design-system, application, bundle — no content field; vault.yaml handles install.
}
```

**Step 4b — Generate agentskills.yaml** (Agent Skills Universal — 33+ platforms)

The Agent Skills format (YAML frontmatter + markdown instructions) is the structured skill definition
format used natively by Claude Code and recognized by other AI coding tools.
Generate this manifest for cross-platform compatibility.

```yaml
# Agent Skills Universal Manifest
name: "{slug}"
version: "{version}"
description: "{description}"
type: "{product type}"
author: "{from creator.yaml}"
license: "{license}"
entry: "{primary file}"
platforms:
  - claude-code
  - cursor
  - codex
  - gemini-cli
  - copilot
  - "*"  # Compatible with any Agent Skills-compliant platform
install:
  target: "{from product-dna install_target}"
  files:
    - "{list all files in .publish/ relative paths}"
metadata:
  mcs_level: "{from validation}"
  mcs_score: "{from validation}"
  marketplace: "https://myclaude.sh/p/{slug}"
```

Only generate for types that map to Agent Skills format (skill, agent, prompt, workflow).
For types that don't map cleanly (design-system, application), generate only vault.yaml + plugin.json.

**Step 5 — Calculate Checksum**

SHA-256 of the entire .publish/ directory contents.

**Step 6 — Stage .publish/**

Create `workspace/{slug}/.publish/` with:
- Cleaned product files (WHY comments stripped)
- vault.yaml (MyClaude marketplace)
- plugin.json (Anthropic plugin marketplace)
- agentskills.yaml (Agent Skills universal — if applicable type)
- CHANGELOG.md (generate if missing)
- LICENSE.md file (generate from license field — use .md extension, CLI rejects extensionless files)

**EXCLUDE from .publish/** (internal Engine files — never distribute):
- `.meta.yaml` (Engine product state tracking)
- `domain-map.md` (creator's working notes)
- Any file starting with `.` (hidden files, including `.env`)
- Files matching secret patterns: `*.pem`, `*.key`, `*.p12`, `credentials*.json`, `*.env`
- If any excluded-for-secrets file is found, WARN: "Sensitive file `{file}` excluded from package. If this is intentional, rename it."

**Step 6c — Double-Source Secrets Scan**

Run the same secrets scan patterns (from `config.yaml → secret_content_patterns`) against BOTH `.publish/` AND `workspace/{slug}/` originals. Compare results. If `.publish/` has MORE matches than originals (stripping logic injected content), this is a CRITICAL error — abort packaging immediately and report the discrepancy.

**Step 6b — Verify Type-Specific Install Artifacts**

The CLI `install` command has type-specific handlers. The tarball MUST contain the artifacts
each handler expects, or install will silently skip critical operations.

| Type | Required in .publish/ | CLI Install Behavior |
|------|----------------------|---------------------|
| **hooks** | `hooks.json` + `scripts/` (with .sh files) | Merges hooks.json into settings.local.json + copies scripts/ |
| **statusline** | `statusline.sh` + `settings-fragment.json` | Copies script + merges statusLine config into settings.local.json |
| **minds** | `{slug}.md` (renamed from AGENT.md in Step 1.5) | Copies flat file to .claude/agents/{slug}.md |

**Verification (MUST pass or abort):**

For **hooks**:
- `hooks.json` exists in `.publish/` → FAIL if missing
- `hooks.json` is valid JSON with top-level `"hooks"` key → FAIL if malformed
- `scripts/` directory exists with at least one `.sh` file → FAIL if missing
- JSON `_`-prefixed keys were stripped in Step 2 (e.g., `_comment`, `_events_reference`)

For **statusline**:
- `statusline.sh` exists in `.publish/` → FAIL if missing
- `statusline.sh` has shebang `#!/usr/bin/env bash` → WARN if missing
- `settings-fragment.json` exists with `"statusLine"` key → FAIL if missing

For **minds**:
- `{slug}.md` exists in `.publish/` (Step 1.5 should have renamed it) → FAIL if missing
- File has YAML frontmatter with `denied-tools` → WARN if missing (advisory-only guarantee)

For all other types: no additional verification (default install path handles them).

If any FAIL: abort with message listing missing artifacts and expected structure.

**Step 7 — Re-validate**

Run Stage 1 (structural) + Stage 6 (CLI preflight) on `.publish/` contents.
If any check fails, report and abort — don't leave broken package.

**Step 8 — Update State**

```yaml
# .meta.yaml updates
state:
  phase: "packaged"
  packaged_at: "{ISO timestamp}"
```

---

## Output Format

**UX Stack (load before rendering output):**
1. `references/ux-experience-system.md` §1 Context Assembly + §2.2 Archetype-Aware Insights (pricing emphasis per creator goals)
2. `references/ux-vocabulary.md` — translate all terms
3. `references/quality/engine-voice.md` — Brand DNA

**Cognitive rendering:** /package is a transition moment — the product is ready to meet the world. Adapt output: creators with revenue goals get pricing intelligence front-and-center. Community-focused creators get distribution channel emphasis. Expert creators get compact technical summary. Beginners get reassurance: "Your product passed quality checks. One step to publish." Always include the install command preview as identity reinforcement — seeing `myclaude install @{username}/{slug}` makes it real.

**CRITICAL: Load `references/ux-vocabulary.md` for UX tier names and type names.**

```
┌─────────────────────────────────────────────┐
│  ✦ {product_name} is ready to share!        │
│  Quality: {ux_tier} {stars}                 │
│                                              │
│  {N} files packaged for {platform_count}    │
│  platforms. Install command:                │
│                                              │
│  myclaude install @{username}/{slug}        │
│                                              │
│  {If value_score:}                          │
│  💰 Suggested price: ${min}-${max}          │
│                                              │
│  Next: /publish to go live                  │
└─────────────────────────────────────────────┘

Technical: {N} files, {size}, {checksum_short}...
```

---

## SAFETY INVARIANTS (D19 — critical constraints in high-attention zone)
[SOURCE: CC commit handling — never --amend, --no-verify, force push]

These are ABSOLUTE rules that cannot be overridden:
1. **Never overwrite .publish/ without confirmation** — if .publish/ already exists, ask before replacing
2. **Never include secrets** — re-run secrets scan from /validate Stage 2 on .publish/ contents AFTER stripping
3. **Never strip creator content** — only strip WHY comments, _prefixed JSON keys, and .meta.yaml. All content the creator wrote must survive packaging intact
4. **Never modify workspace originals** — all transformations happen on the .publish/ copy
5. **Verify frontmatter completeness** — check `product-dna/{type}.yaml → frontmatter.required[]`. Missing required fields in .publish/ → block with: "Required frontmatter field '{field}' missing. Add it to your product file, then re-run /package." [SOURCE: cc-platform-contract.md §2.1]
6. **Compact Instructions preservation** — if the workspace file has `## Compact Instructions`, it MUST survive into .publish/. This section is NOT a WHY comment — it's functional product content read by Claude Code's compact system [SOURCE: compact/prompt.ts:133-143]

---

## Anti-Patterns

1. **Packaging unvalidated product** — Always check .meta.yaml state first.
2. **Modifying originals** — Work on copies in .publish/. Never touch workspace/{slug}/ source files.
3. **Missing manifests** — vault.yaml + plugin.json required. agentskills.yaml for compatible types. Triple distribution.
4. **Stale checksum** — Recalculate if any file changes after initial staging.
5. **Silent failures** — If WHY stripping breaks markdown structure, detect and report.
6. **Missing install artifacts** — hooks without scripts/, statusline without settings-fragment.json. Step 6b catches these. If /validate passed but /package fails here, the DNA spec is missing a required file check.
7. **Shipping _comment keys in hooks.json** — Step 2 strips `_`-prefixed JSON keys. Verify after strip: no `_comment`, `_why`, `_events_reference` in .publish/ JSON files.

---

## Compact Instructions

When context is compressed, preserve:
- Product slug, type, and packaging state
- Whether WHY stripping completed successfully
- Manifest generation status (vault.yaml, plugin.json, agentskills.yaml)
- Pricing intelligence results if computed
- Any blocking issues (secrets detected, frontmatter missing, JSON invalid)
- .publish/ directory path and file count

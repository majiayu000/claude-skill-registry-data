---
name: onboard
description: >-
  Set up or update your myClaude creator profile. Builds creator.yaml with expertise,
  goals, technical level, and preferences. Use on first run, 'set up profile', 'who am I',
  'my profile', 'get started', or 'configure'.
argument-hint: "[update]"
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash(myclaude *)
  - AskUserQuestion
---

# Onboarder

Discover and persist creator profile through intelligent scanning + minimal questions. Build `creator.yaml` — the **Master Input** that defines the quality ceiling for every product this creator builds.

**When to use:** First time using the Creator Engine, or when profile needs update (`/onboard update`).

**Full protocol (phases, question scripts, schema, edge cases):** Read `${CLAUDE_SKILL_DIR}/references/onboard-protocol.md` before executing any phase.

---

## Core Principle: Minimum Friction

**RULE:** Every question to the creator MUST use the `AskUserQuestion` tool. Never ask questions via plain text.

**RULE:** Scan first, ask second. Auto-detect everything possible. Only ask what cannot be inferred.

**RULE:** Optimize for the happy path. If the scan is rich enough, the entire onboarding should be **1 click**.

---

## Activation Protocol

0. **Shared preamble:** Load `references/quality/activation-preamble.md` — context assembly, persona adaptation, deterministic routing rules.
1. Check for `creator.yaml` in project root
2. **Exists** → read `schema_version`:
   - **`schema_version < 3`** → run **Phase 2.5d Schema v2→v3 Silent Migration** (protocol → Phase 2.5d) BEFORE any other action. Migration is atomic + reversible via `creator.yaml.bak.v2`. After migration succeeds, continue with step 2 against the new v3 file.
   - **`schema_version == 3`** → load it, display summary, AskUserQuestion: "Is this still accurate?"
     - Yes → exit, profile is current
     - No → enter UPDATE MODE (see protocol file → Update Mode Flow)
3. **Does not exist** → enter FULL ONBOARDING (Phases 0 → 6c). Run Phase 2.5b (Intent Profile Inference) + 2.5c (Language Confirmation Gate) between Phase 2.5 and Phase 3 — both are **mandatory for schema v3**.

---

## Full Onboarding — Phase Routing Table

Load `${CLAUDE_SKILL_DIR}/references/onboard-protocol.md` for full details on every phase.

| Phase | What Happens | Detail Location |
|-------|-------------|-----------------|
| **0 — Platform Detection** | Detect OS + shell + resolve `{home}` path | protocol → Platform Detection |
| **1 — Silent Deep Scan** | Run 5 scans in parallel: git identity, .claude/ root, project breadth, workspace, locale | protocol → Phase 1 |
| **2 — Inference Engine** | Build draft profile: name, language, technical_level, profile.type, expertise. Weighted scoring (skills 3x, CLAUDE.md 3x, projects 2x, MCP 1x, rules 1x). Route to Express/Standard/Full path | protocol → Phase 2 |
| **2.5 — Disambiguation** | If expert score (≥19) on Express/Standard path → one question: first time user? | protocol → Phase 2.5 |
| **2.5b — Intent Profile Inference** | Derive 5 of 7 `intent_profile` fields from scan outputs (domain_depth, working_rhythm, maintenance_appetite, target_audience, external_dependency_tolerance). Mark `_inferred: true`. Defer `licensing_tolerance` to `/create minds --genius`. `usage_frequency_expectation` is asked in Phase 3 Call 2. **Mandatory for schema v3.** | protocol → Phase 2.5b |
| **2.5c — Language Confirmation Gate** | Classify language detection as `high\|low\|fallback`. Silent announcement if high; one-question confirm if low; forced question if fallback. Persist `language_confidence` + `language_detection_sources`. **Mandatory for schema v3.** | protocol → Phase 2.5c |
| **2.5d — Schema v2→v3 Migration** | Triggered only when an existing `creator.yaml` has `schema_version < 3`. Atomic + backed up to `creator.yaml.bak.v2`. Preserves all v2 fields. | protocol → Phase 2.5d |
| **3 — Adaptive Questioning** | Express (2 calls) / Standard (2 calls) / Full (3 calls). Call 2 of all three paths now includes a 4th question on `usage_frequency_expectation` (schema v3). | protocol → Phase 3 |
| **4 — Profile Type** | Infer type from all signals. Never ask directly | protocol → Phase 4 |
| **5 — Generate creator.yaml** | Write schema v3 file (includes `intent_profile`, `language_confidence`, `language_detection_sources`). Validate YAML. Read back to verify. | protocol → Phase 5 |
| **5b — Seed creator-memory.yaml** | After creator.yaml is written and parses, seed the sibling `creator-memory.yaml` with a `first_onboard` event. Idempotent: silently skipped if a `first_onboard` event already exists. Validator: `scripts/creator-memory-validate.py`. Silent infrastructure — Phase 6 speaks, 5b prepares the ground. | protocol → Phase 5b |
| **6 — Closing + Intelligence Report** | Persona-adaptive next step + setup health + gap analysis + product recommendation. **Load UX stack**: `references/quality/engine-voice-core.md` (loaded at activation start), `references/ux-experience-system.md` (§2.3 first scaffold moment = "first onboard" for brand), `references/quality/engine-voice.md` (full Brand DNA substrate loaded here because this is a peak moment: the FIRST myClaude Studio impression). Use brand frame: `┌─ MyClaude Studio ─┐`. Personalize with the name just captured. This is the moment the creator enters the myClaude universe — make it feel like arriving, not registering. After Phase 5 writes creator.yaml, Phase 5b appends the `first_onboard` event to `creator-memory.yaml` (create-if-absent with full schema shell per `scripts/creator-memory-validate.py`). This seeds the Ritual of Return Layer 2 for future sessions. | protocol → Phase 6, 6b, 6c |

**Scan failure protocol:** See protocol → Scan Failure Protocol. Never crash. Never show raw errors.

**i18n:** Detect language (CLAUDE.md → locale → `en`). All AskUserQuestion text in detected language.

---

## Commands

```
/onboard           → Full onboard (FULL ONBOARDING if no creator.yaml)
/onboard update    → Refresh profile (UPDATE MODE if creator.yaml exists)
```

---

## Quality Gate

**Must pass before writing creator.yaml:**
- Valid YAML, `schema_version: 3`
- Required non-empty: `name`, `language`, `language_confidence`, `profile.type`, `profile.technical_level`, `preferences.default_license`, `preferences.default_category`, `preferences.quality_target`, `preferences.workflow_style`
- Schema v3 intent_profile required non-null (except licensing_tolerance which is deferred): `intent_profile.domain_depth`, `intent_profile.working_rhythm`, `intent_profile.usage_frequency_expectation`, `intent_profile.maintenance_appetite`, `intent_profile.target_audience`, `intent_profile.external_dependency_tolerance`
- `intent_profile._inferred` block present with one entry per intent_profile field
- `language_confidence` ∈ {high, low, fallback, migrated}
- `workflow_style` ∈ {guided, autonomous}. Default: `guided` for beginner/intermediate, `autonomous` for advanced/expert
- `token_efficiency` ∈ {eco, balanced, unlimited}. Default: `balanced`. Eco minimizes context reads; unlimited loads full UX stack every time
- `profile.type` ∈ {developer, prompt-engineer, domain-expert, marketer, operator, agency, hybrid}
- `technical_level` ∈ {beginner, intermediate, advanced, expert}
- `license` ∈ CE-D40 list: MIT, Apache-2.0, GPL-3.0, BSD-3-Clause, ISC, CC-BY-4.0, CC-BY-SA-4.0, CC0-1.0, Proprietary, Custom
- `scan_path` ∈ {express, standard, full}
- `platform` ∈ {macOS, Linux, Windows, WSL, Docker, unknown}
- `technical_score` consistent with `technical_level` (score in threshold range)
- `git_handle` set only if actually detected (not fabricated)
- `onboarded_at` = today's date in `YYYY-MM-DD`
- `language` = valid IETF tag (e.g., `pt-BR`, `en`, `es`)
- No placeholder text (`{name}`, `{domain 1}`, etc.) in the final file

**Post-write:** Read creator.yaml back and verify YAML parsing succeeds. Guards against encoding issues.

---

## Anti-Patterns

1. **Asking questions via plain text** — Always use `AskUserQuestion`
2. **Hardcoding `~/`** — Always resolve `{home}` dynamically per platform
3. **Crashing on scan failure** — Every scan failure must be caught silently; set to fallback value
4. **Mixing `preview` + `multiSelect` in one call** — Causes silent answer loss; never do this
5. **Using a git handle as `creator.name` without asking** — When `name_type = handle`, always offer name choice
6. **Blocking onboarding on marketplace/CLI failures** — Phase 6b/6c are non-blocking; skip silently on error
7. **Triggering AskUserQuestion in Phase 6b** — Setup Intelligence Report is OUTPUT ONLY
8. **Ignoring CLI contract in Phase 6c** — All 4 CLI commands (`whoami`, `profile sync`, `stripe status`, `setup-mcp`) follow `references/cli-contract.md` unified error handling. All are **warning** severity — no CLI failure prevents onboarding from completing. Phase 6c details are in `references/onboard-protocol.md → Phase 6c`.

---

## Compact Instructions

When context is compressed, preserve:
- Which path was taken (express/standard/full) and current phase
- `name_type` and `name_confidence` from Phase 1 scan
- Scan richness classification and which scans failed
- `recommended_default` inferred from Phase 2
- Any AskUserQuestion answers already collected (don't re-ask)
- Whether UPDATE MODE or FULL ONBOARDING was triggered

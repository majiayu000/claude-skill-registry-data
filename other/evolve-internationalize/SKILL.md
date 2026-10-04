---
name: evolve-internationalize
description: Internationalize AICP's operator-facing surfaces — CLI messages, error strings, generated documentation, model-response prompts. LOW APPLICABILITY for AICP (a backend AI platform authored in developer-English). The skill exists for completeness and honest scope discussion. The real i18n track lives downstream in fleet-facing UIs (Mission Control) and in KB content served to non-English operators. Loads when the operator says "internationalize AICP" / "translate CLI messages" / "support non-English operators" / "i18n the wiki" / "serve KB in language X".
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
effort: medium
---

# evolve-internationalize

Add or extend internationalization support in AICP. Distinct from
`evolve-integrate` (NEW external system) and `evolve-api-version` (evolve
existing API) — this skill is specifically the i18n lifecycle track.

**Honest applicability note**: AICP is a single-operator backend AI platform
authored in developer-English. Operator-facing surfaces (CLI, error
messages, `aicp --help`) do not currently target multi-language operators.
This skill captures the i18n track for when AICP's scope expands (fleet
operators in non-English regions, KB content served to non-English agents,
model prompts that must adapt per operator locale). Until that scope
expands, most i18n work is premature.

## Trigger phrases (when to load this skill)

Load when the conversation matches any of:

- **Direct verb**: "internationalize AICP", "translate CLI messages",
  "add i18n", "support language X", "serve KB in language Y"
- **Operator locale**: supporting a non-English operator — their CLI
  output, error messages, generated documentation
- **Model-prompt locale**: adapting system prompts or RAG-injected
  context per operator language (affects router behavior)
- **Wiki content i18n**: authoring AICP wiki pages (lessons/decisions/
  patterns) in multiple languages for multi-region fleet

Do NOT load when:

- The concern is accessibility (color contrast, screen reader) — load
  `quality-accessibility`
- The concern is a new external system integration — load `evolve-integrate`
- The concern is character encoding (UTF-8 correctness) — that's a
  bug-fix, not an i18n track; handle inline
- The operator is the only user today and works in English — DO NOT
  speculatively add i18n infrastructure (premature complexity)

## Operations

### Operation 1 — Scope the i18n need honestly

**When**: operator raises i18n concern; decide whether work is warranted.

**Process**:

1. Answer three questions explicitly:
   - WHO are the non-English operators? (name them — "hypothetical future
     operator" is not an answer)
   - WHAT surfaces must translate? (CLI help, error messages, KB content,
     model prompts — each is a separate track)
   - WHEN is this needed? (current gap vs speculative future)
2. If the answer is speculative or "maybe someday", STOP. Document the
   concern in `wiki/backlog/tasks/` as a deferred task and exit the skill.
3. If the answer is concrete (named operators, specific surfaces, defined
   timeline), proceed with scope definition below.

**Quality bar**: NEVER add i18n infrastructure speculatively. The correct
default for AICP today is "defer". Adding gettext / locale files / fallback
chains for hypothetical operators creates dead code that future contributors
must maintain.

### Operation 2 — Author the i18n decision

**When**: scope is concrete; commit to the track.

**Process**:

1. Per Knowledge Evolution Standards, author a decision page at
   `wiki/decisions/00_inbox/internationalize-<surface>.md`:
   - WHY: which operators need this; what breaks today without it
   - SCOPE: which surface (CLI / error strings / docs / KB / prompts) —
     one surface per decision
   - APPROACH: gettext vs custom dict vs model-translated-at-runtime —
     at least 2 alternatives
   - FALLBACK: what happens when a string has no translation? (recommended:
     fall back to English, not to "[translation missing]")
   - MAINTENANCE: who adds new strings to the translation set over time?
2. Get operator approval before implementing

**Quality bar**: the decision page is the contract; it forces the right
questions (who, what, when, how, who-maintains). Skipping it leads to
half-implemented i18n that rots.

### Operation 3 — Implement CLI / error-string i18n

**When**: decision covers CLI messages; ship the infrastructure.

**Process**:

1. Add a locale resolver to `aicp/core/`:
   - Source: env var `AICP_LOCALE` → falls back to `$LANG` → falls back
     to `en_US`
   - One source of truth; do NOT scatter locale reads across modules
2. For the chosen approach (gettext/dict/runtime):
   - **Dict approach (recommended for AICP's scale)**: `aicp/locale/<lang>.yaml`
     with key → translated-string map; helper `t(key, **fmt)` looks up
     with English fallback
   - **gettext**: heavier, but standard; use if the operator explicitly
     wants `.po`/`.mo` file workflow
3. Wrap operator-facing strings: `print(t("task.switch.success", id=tid))`
   instead of `print(f"Switched to {tid}")`
4. Add tests: `tests/test_locale.py` — resolves locale correctly, fallback
   works, every key in `en.yaml` has matching keys in other lang files
5. Update `.env.example` with `AICP_LOCALE` documentation

**Quality bar**: every CLI string goes through the helper OR is documented
as intentionally not-translated (e.g., error codes, machine-readable output).
Partial wrapping creates a worse experience than no wrapping.

### Operation 4 — Implement KB content i18n

**When**: operator wants KB served in multiple languages.

**Process**:

1. Decide per-collection or per-page:
   - **Per-collection**: separate `aicp-kb-<lang>` collection; switch at
     query time via locale resolver
   - **Per-page**: one page has `content_en`, `content_fr` fields;
     `kb_search` filters by locale (requires schema change)
2. Pick a translation source:
   - Human-authored: operators author KB pages per language (highest
     quality, highest maintenance cost)
   - Model-translated: LocalAI translates on ingest (lower quality,
     maintenance-free — good for low-stakes content)
3. Extend `aicp/core/kb.py` to honor locale at search time
4. Update `aicp --kb search` CLI to accept `--locale <lang>`

**Quality bar**: translated KB content must include a `translation_source`
field (human / model). Operators reading the KB need to know quality
level of what they're reading.

### Operation 5 — Implement model-prompt i18n

**When**: router must adapt system prompts or RAG injections per operator
locale.

**Process**:

1. Locate prompt assembly sites (typically `aicp/core/pipeline.py`,
   `aicp/core/router.py`)
2. Add locale-aware prompt variants at those sites (NOT scattered —
   prompts are already a chokepoint, keep them there)
3. Decide: does the MODEL respond in operator locale, or does AICP
   translate the response? (Former is simpler; latter gives more control
   at cost of second round-trip)
4. Add tests verifying the model produces locale-appropriate responses
   for a small fixture set (don't try to test exhaustively — the model
   handles most of the work)

**Quality bar**: prompt variants live in one place; do not scatter
`if locale == "fr"` across the codebase.

## Gotchas

- **Detection**: agent adds i18n infrastructure speculatively with no
  named operator needing it.
  **Rule**: premature i18n is dead code. Defer until a concrete operator
  is named.
  **Reasoning**: i18n adds real maintenance cost (every new string needs
  translation keys); without a real user, the cost has no return.

- **Detection**: agent uses "[translation missing]" or empty string as
  fallback.
  **Rule**: always fall back to English source string, never to a
  placeholder.
  **Reasoning**: placeholder fallbacks produce worse UX than English
  fallback; operators see cryptic strings instead of readable ones.

- **Detection**: agent translates operator-facing strings but not error
  codes.
  **Rule**: error codes (`E_PROFILE_INVALID`, `E_BACKEND_DOWN`) stay
  English — they're machine-readable. Translate the human description
  only.
  **Reasoning**: error codes are grep targets in logs and scripts; they
  cross language boundaries. Translating them breaks external tooling.

- **Detection**: agent scatters locale checks across multiple modules.
  **Rule**: one locale resolver; all reads go through it.
  **Reasoning**: scattered checks drift (different defaults, different
  fallback order) and make future locale changes require N edits.

- **Detection**: agent adds translation infrastructure but forgets
  `AICP_LOCALE` in `.env.example`.
  **Rule**: every new env var goes in `.env.example` with comment.
  **Reasoning**: undocumented env vars are operational landmines (per
  `config-env` skill).

- **Detection**: agent translates KB content without a `translation_source`
  field.
  **Rule**: every translated KB page carries human/model provenance.
  **Reasoning**: operators need to know if they're reading authored
  content or model-translated content — the trust level is different.

## Reference exemplars

- `aicp/core/state.py` — example of a one-source-of-truth module (locale
  resolver should follow this shape)
- `aicp/core/kb.py` — example of the KB access layer; locale-aware
  querying extends this module
- `aicp/cli/main.py` — the CLI dispatcher; i18n wrapping happens at the
  print sites here
- `wiki/decisions/01_drafts/aicp-active-state-mechanism-for-hooks.md` —
  example of a one-surface-per-decision document (model it for
  internationalize decisions)
- `config/default.yaml` — where `locale:` would go if operator-config
  driven rather than env-driven

## Domain context

AICP today is single-operator, English. Fleet expansion to multi-operator
multi-machine (per CLAUDE.md `## Infrastructure target`) is the scenario
where i18n becomes plausible. Until that scenario is named, `evolve-integrate`
and `evolve-scale` are higher-priority evolution tracks. No existing AICP
module carries i18n infrastructure; starting from scratch is correct
when the need materializes — do not retrofit piecemeal.

## Related skills

| Skill | When to use |
|-------|-------------|
| `quality-accessibility` | For accessibility (color, screen reader) — different track, often confused with i18n |
| `config-env` | For adding `AICP_LOCALE` env var and documenting it |
| `evolve-scale` | For multi-region/multi-operator scale change (often the REAL need) |
| `evolve-integrate` | If i18n requires integrating a translation service |
| `architecture-propose` | If introducing gettext is a significant architectural change |
| `feature-document` | For scoping the i18n feature (pairs with Operation 1) |

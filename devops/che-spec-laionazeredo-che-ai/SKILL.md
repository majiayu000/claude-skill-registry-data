---
name: "che-spec"
description: "Generate or validate a Che Execution Specification (SPEC). 4 inputs: existing spec file, ticket URL (Linear/ClickUp/GitHub), legacy-project PRD .md path, or inline brief. Produces 7 sections + machine-parsable YAML frontmatter, user-approved before save into $CHE_WORKSPACE_SHARED/specs/<slug>/<ts>-spec.md (DURABLE workspace area OUTSIDE user worktree code)."
---

# Che Spec Generator (SPEC)

> **SHARED REFERENCES (CANONICAL — DO NOT DUPLICATE body here):**
> - Full contracts (precedence 1-18, DbC, BDD incremental, etc): `engineering-contracts` skill
> - Path resolution (WORKSPACE_NAME, WORKTREE_SLUG, CHE_WORKSPACE_SHARED, CHE_SESSION_DIR): `che` CLI — `eval "$(che compute_paths WT SID --cwd "$PWD")"`
> - 2-LEVEL worktree binding (Level1 registry, Level2 sessions dir): engineering-contracts §19

Produces **1 file per feature/bug/refactor:** a compact, agent-optimised spec (~60–120 lines, 7 sections). Replaces project-specific legacy PRD artifacts. Gate before scope capture in `/che-act` and standalone runnable via `/che-spec`.

---

## §0 PURPOSE & INTEGRATION

When called:
1. **From `/che-act` (embedded)**: runs AFTER binding §19 + ensure_dirs, BEFORE scope capture §1. User specifies which SPEC to use or generates new.
2. **Standalone** via `/che-spec`: runs independently; performs binding if needed, then generates or edits spec.

On completion this skill **returns to the caller** two values printed in the last 2 lines of the transcript:
- `SPEC_PATH=<absolute-path-to-spec>` — used by che-act
- `SPEC_STATUS=Approved|Draft` — only `Approved` unlocks subsequent execution in SM.

---

## §1 PREFLIGHT (Run FIRST)

Fail if any step fails. Stop before proceeding with user.

1. **Binding check:** Read `$CHE_REGISTRY_PATH`, find LAST entry with the effective session id (`"${CHE_SESSION_ID:-${HARNESS_SESSION_ID:-${SESSION_ID:-}}}"`) + `STATUS=BOUND`. If missing AND user did not provide `--worktree` → ASK for absolute worktree, perform full §19 binding (Level1 append + Level2 write + FRIENDLY_NAME prompt).
2. **Paths:**
   ```bash
   command -v che >/dev/null 2>&1 || { echo "❌ FATAL: 'che' CLI not found on PATH. Aborting."; exit 98; }
   eval "$(che compute_paths "$WORKTREE_ROOT" "$SESSION_ID" --cwd "$PWD")"
   che ensure_dirs "$WORKTREE_ROOT" "$SESSION_ID" --cwd "$PWD"
   ```
3. **Slug:** If user passed `--slug`, use it as-is (sanitise to `[a-z0-9_-]+`). Otherwise derive from `ticket_ref` or `change_class+why`.

### §1.4 Feature Flag Provider Preflight Check (MANDATORY if risk_level ≥ medium)

> **Reason WAVE4:** DO NOT invent feature flags from scratch if the project has no predefined infrastructure. Only ask the user about flags IF a provider is detected. Default fallback = native rollback of the deployment platform.

**Execution TRIGGER (HARD RULE):**
- IF `risk_level === low` (frontmatter §HEAD L72) → **SKIP ENTIRE block, 0 log lines, do not ask anything to user.**
- IF `risk_level === medium OR risk_level === high` → **EXECUTE 3 steps BELOW, fixed order. DO NOT skip any step.**

```bash
# Initial DETECTED flag state
FLAG_PROVIDER_DETECTED="none"
FLAG_PROVIDER_NAME=""

# STEP 1 — SCAN WORKTREE for known feature libs (maxdepth 5, avoid node_modules)
echo "[PREFLIGHT §1.4 STEP 1/3] Scanning worktree for feature flag libs..."
FLAG_LIBS_FOUND="$(cd "$WORKTREE_ROOT" && find . -maxdepth 5 -type f \( -iname 'feature.ts' -o -iname 'flags.ts' -o -iname '*.flags.ts' -o -iname 'feature-flags.ts' -o -iname 'feature.js' -o -iname 'flags.js' \) -not -path '*/node_modules/*' -not -path '*/.next/*' -not -path '*/dist/*' 2>/dev/null | tr '\n' ';')"
if [ -n "$FLAG_LIBS_FOUND" ] && [ "$FLAG_LIBS_FOUND" != ";" ]; then
  FLAG_PROVIDER_DETECTED="worktree_lib"
  FLAG_PROVIDER_NAME="worktree-files:${FLAG_LIBS_FOUND%;}"
  echo "[INFO §1.4] STEP 1 DETECTED: feature flag files in worktree → may recommend flags if risk justifies."
fi

# STEP 2 — SCAN ENV PATTERNS for known providers (8 canonical patterns)
if [ "$FLAG_PROVIDER_DETECTED" = "none" ]; then
  echo "[PREFLIGHT §1.4 STEP 2/3] Scanning .env.example and similar for feature flag provider patterns..."
  ENV_CANDIDATES=".env.example .env.local.example .env.development.example .env.production.example .env"
  ENV_PATTERNS='^(export )?(FLAG_|FEATURE_FLAG_|LD_|UNLEASH_|STATSIG_|EDGE_CONFIG_|OPENFEATURE_|SPLITIO_)'
  FLAG_ENV_FOUND=""
  for envf in $ENV_CANDIDATES; do
    if [ -f "$WORKTREE_ROOT/$envf" ]; then
      MATCHES="$(grep -rE "$ENV_PATTERNS" "$WORKTREE_ROOT/$envf" 2>/dev/null | head -5 | tr '\n' ';')"
      if [ -n "$MATCHES" ]; then
        FLAG_ENV_FOUND="${FLAG_ENV_FOUND}${envf}:${MATCHES};"
      fi
    fi
  done
  if [ -n "$FLAG_ENV_FOUND" ]; then
    FLAG_PROVIDER_DETECTED="env_pattern"
    FLAG_PROVIDER_NAME="env-patterns:${FLAG_ENV_FOUND%;}"
    echo "[INFO §1.4] STEP 2 DETECTED: feature flag provider env pattern → may recommend flags."
  fi
fi

# STEP 3 — PRODUCT CONTEXT FRONTMATTER feature_flag_provider: (Level 1.5 registry)
if [ "$FLAG_PROVIDER_DETECTED" = "none" ]; then
  echo "[PREFLIGHT §1.4 STEP 3/3] Checking product_context.md frontmatter feature_flag_provider..."
  PC_FILE="$CHE_WORKSPACE_SHARED/projects/${PROJECT_SLUG:-default}/product_context.md"
  if [ -f "$PC_FILE" ]; then
    PC_FLAG_PROVIDER="$(grep -E '^feature_flag_provider:\s*' "$PC_FILE" | head -1 | sed -E 's/^feature_flag_provider:\s*//' | tr -d '"' | tr -d "'" | xargs || true)"
    if [ -n "$PC_FLAG_PROVIDER" ] && [ "$PC_FLAG_PROVIDER" != "" ] && [ "$PC_FLAG_PROVIDER" != "none" ] && [ "$PC_FLAG_PROVIDER" != "null" ]; then
      FLAG_PROVIDER_DETECTED="product_context"
      FLAG_PROVIDER_NAME="product_context:${PC_FLAG_PROVIDER}"
      echo "[INFO §1.4] STEP 3 DETECTED: provider declared in product_context.md → may recommend flags."
    fi
  fi
fi
```

**RESULTS BRANCHING (HARD POLICY, NON-NEGOTIABLE):**

| Case | Condition | Action in SPEC draft |
|---|---|---|
| **A — ANY DETECTED** | `FLAG_PROVIDER_DETECTED != none` (Step 1, 2 OR 3 found it) | NO SPECIAL CHANGE. Normal flow §3 + §4. MAY recommend feature flag in §3 Contracts / §5 Risks if risk justifies (medium/high). Do not ask anything to the user about flags (automatic). |
| **B — NONE DETECTED + risk ≥ med/high** | `FLAG_PROVIDER_DETECTED = none` AND `risk_level ∈ {medium, high}` | **HARD RULE: CANNOT mandate feature flag in ANY spec section (§3 PRE/POST, §4 SbE, §5 Verification, §6 Risks).** INSERT MANDATORY LINE in draft §3 CONTRACTS → PREconditions block (last bullet PRE): <br>`- PRE-FF: Feature flags NOT AVAILABLE (no provider detected in preflight §1.4). Fallback default rollback = native deploy platform: <Vercel Instant Rollback <30s \| Railway redeploy \| Supabase branch revert \| manual>` <br>Add note in §5 VERIFICATION ("Rollback trigger" section if exists, otherwise as last bullet): <br>`Default rollback uses native platform deploy (feature flags unavailable in this worktree — no provider detected in preflight §1.4).` <br>DO NOT ask user if they want to use flags. DO NOT create flag configuration. |

**ONLY PERMITTED EXCEPTION (user VERBATIM override):**
- ONLY way to bypass Branch B (force mandatory flag WITHOUT detected provider) = user types BEFORE spec generation the EXACT literal: **`EXPLICIT_OVERRIDE_FEATURE_FLAGS_FORCE`** followed by 1-line justification. User example:
  > `EXPLICIT_OVERRIDE_FEATURE_FLAGS_FORCE: we're launching this critical feature on a Friday 10pm, I'll create the flags lib manually right now in this PR`
- If user typed the literal → save as decision.log: `che decision_append "$WORKTREE_ROOT" "SPEC_PREFLIGHT_OVERRIDE" "preflight=§1.4_feature_flags type=EXPLICIT_OVERRIDE_FEATURE_FLAGS_FORCE rationale=<1-line user verbatim> risk_level=${risk_level}"`. Then MAY mandate flags in spec sections normally. If NOT typed literal → Branch B is HARD STOP, not discussion.

### §1.5 Strategic Roadmap Preflight (MANDATORY)

> **Purpose:** Ensure the task is aligned with the project's strategic roadmap (Specflow Phase 2).

**Execution TRIGGER:**
- IF `$CHE_WORKSPACE_SHARED/projects/<slug>/roadmap.md` exists → **EXECUTE steps below.**
- IF NOT exists → warn user: "Strategic roadmap not found. Recommended to run `/che-architect` Step 2 first for better navigability."

**Action:**
1. Read `roadmap.md`.
2. List available phases (IDs and Titles).
3. Ask the user to confirm which phase this SPEC belongs to, or infer from `ticket_ref`.
4. Fill frontmatter `roadmap_phase: <ID>`.

---

## §2 SOURCE SELECTION (4 inputs)

Present choices when input arg is missing or ambiguous. First match wins, never fallback silently.

| # | Source | User provides | Action before draft |
|---|---|---|---|
| A | **Existing SPEC file** | File path OR pick from glob `$CHE_WORKSPACE_SHARED/specs/**/*.md` (canonical; if empty, fall back to the legacy `$CHE_WORKSPACE_SHARED/spec_*.md`) | Read it; if `status=Approved` → jump straight to §5 (approval). If Draft → proceed to §3 editing with existing content pre-filled. |
| B | **Ticket URL** (Linear FLO-XXX, ClickUp, GitHub issue) | Full URL | 1. Try to extract title + description + status via MCP tools (`mcp_flockr-linear`, `mcp_laion-clickup`, `mcp_github`). If MCP fails → fall back to user-provided inline description. 2. Populate frontmatter `ticket_ref:` + `spec_id:` from slug. 3. Seed §1 WHY bullets from ticket description. 4. Seed §4 MUST ACs = 3 bullets if ticket has Acceptance Criteria field. |
| C | **Legacy PRD** (Project legacy .md) | Absolute path to `.md` file | Parse with headings, map: `Problem / Background` → §1 WHY; `Goals` → §4 MUST; `Non-Goals` → §1 Non-goals; `Data Model / Migration` → §6 Hints; `Acceptance Criteria` → §4 MUST AC, each prefixed `GWT` verbatim; `Risk` → §5 Rollback trigger. If section missing → leave empty and prompt user to fill during §4 review. |
| D | **Inline brief** (short text 2–5 sentences) | User typed description or typed nothing at all → walk through interactive prompts 1-by-1 | Prompt for: change_class (feature|bug|refactor|perf|ops); 3 bullets §1 WHY; 3 sections §2 (Can Touch ≤ 10 files, Can Create, Cannot Touch ≤ 5 lines); 3 PRE + 3 POST + 2 INVARIANTS in §3; 3 MUST + 1 SHOULD + 1 MAY §4 ACs (each AC must include GWT + TEST_METHOD literal). Defaults: `estimated_files_max=15`, `estimated_max_lines_add=400`, `new_dependencies=[]`, `pii_touch=none`, `supabase_rls_touch=false`, `currency_gbp_pence=false`, `domain=engineering`, `flags=LANG_PT_CHECK=ENABLED`. |

---

## §3 SPEC DRAFT STRUCTURE (9 sections — SbE CENTRIC, canonical)

Write the draft in-memory first. File starts with YAML frontmatter, THEN 9 markdown sections (§1-§9). **§4 SbE is the MANDATORY CENTRAL SECTION** (observable behaviours, NOT implementation). Fixed order — DO NOT reorder.

### §HEAD — YAML Frontmatter (REQUIRED fields — validate all present)
```yaml
---
spec_id: <slug-sanitised-alphanum-dash-underscore>
roadmap_phase: <PHASE_ID_IN_ROADMAP.MD> # Link to the strategic roadmap phase
ticket_ref: <"FLO-745" or "NONE">
worktree_root: <absolute-path>
change_class: feature|bug|refactor|perf|ops
domain: engineering                  # accepted values: engineering | product | ux | devops | copywriting | social | seo-analytics
                                      # default = engineering (total backward compat with old specs/sessions/skills without this field)
                                      # if != engineering → SM §0.3 auto-loads domains/<domain>/profile.md + playbook.md
                                      # if != engineering → ship §0.9.5 executes mandatory playbook gates
risk_level: low|medium|high           # NEW SbE. default = low. If medium/high → mandatory §4.4 Mermaid trigger.
source_merge_order: [user_prompt, prd_file, linear_ticket, implementer_hints]   # NEW CANONICAL SbE. DO NOT reorder without EXPLICIT_OVERRIDE + decision log.
status: Draft
estimated_files_max: <integer; default 15 per S03 CHE_RULES §X; hard stop if ceiling exceeded>
estimated_max_lines_add: <integer; default 400 per S04 CHE_RULES §X; advisory ≥400 yellow, MUST gh-stack ≥800 red>
new_dependencies: [ ]
pii_touch: none|read-only|write
supabase_rls_touch: true|false
currency_gbp_pence: true|false
bound_agent_lang: en|pt-BR
flags: LANG_DOCS=en
approver: ""
approved_at: ""
# Auto-calculated SbE counters (VAL09-V10 validation cross-check) — optional, fill at the end of draft:
b_count: 0                            # NEW: quantity of B-IDs in §4.2 Behavior Table (auto-count)
ab_count: 0                           # NEW: quantity of AB-IDs in §4.3 Anti-Behavior Table (auto-count)
erd_required: false                   # per S05 CHE_RULES §X. true IF AND ONLY IF: (a) creates NEW DB entity; (b) alters FK ON DELETE/UPDATE cardinality; (c) adds ≥3 fields with UNIQUE/UK/CHECK constraints.
mermaid_required: false               # per S06 CHE_RULES §X. true IF AND ONLY IF: b_count>=8 OR distinct_public_actors>=3 OR risk_level in {medium, high}.
vertical_slice_required: true         # CANONICAL #0 (CHE_RULES.md). Default true. ONLY false if EXPLICIT_OVERRIDE_HORIZONTAL_PLAN literal appears in §2 SCOPE with 1-line justification + decision.log entry.
tracer_f0_defined: false              # CANONICAL #0 (CHE_RULES.md F0 rule). Auto-calculated: flips to true when §4.5 VERTICAL SLICES table has 1+ row with ID=F0 · Layers Touched count>=2 · B-IDs >= 1 · DONE != empty. Auto-validated by V16.
---
```

### §1 WHY — Problem Statement (max 5 bullets)
Header: `## §1 WHY (Problem Statement)`
- 3–5 bullets only. Example structure:
  - Current: <what breaks today, 1 line concrete>
  - Risk: <security or business impact or UX pain>
  - Goal: <outcome in 1 line> — reached via the simplest option (Simplicity Bias, engineering-contracts §1)
  - Success metric: <curl / behavioural assertion>
  - Non-goals (deferred by design): <what this SPEC deliberately does NOT build in this iteration, and why it is safe to defer>
- **SIMPLICITY BIAS (mandatory — engineering-contracts §1):** the Goal bullet MUST name the simplest option chosen; the Non-goals bullet MUST list what is deliberately deferred. A missing deferral line = V23 FAIL.

### §2 SCOPE — Blast Radius (3 lists, each ≤ 10 items)
Header: `## §2 SCOPE BOUNDARIES & BLAST RADIUS`
Three subsections EXACTLY:
- `### ✅ CAN TOUCH (<=10 files literal paths or glob patterns)` — ≤10 entries
- `### ✅ CAN CREATE (<=8 files/folders)` — new files; include folder path only if empty dir creation required
- `### ❌ CANNOT TOUCH (under any circumstances)` — list paths or packages; last bullet always: `Any worktree other than bound <WORKTREE_ROOT> (§19 scissor)`
- Optional bullet: `### External services touched:` (list services touched or `None`)
- **Optional CANONICAL OVERRIDE bullet (insert ONLY if user explicitly requires horizontal planning / layer-by-layer execution. Pattern identical to §1.4 EXPLICIT_OVERRIDE_FEATURE_FLAGS_FORCE literal).** Add as LAST bullet inside `### ❌ CANNOT TOUCH` or as a dedicated sub-bullet immediately after `External services touched`, NEVER anywhere else:
  `- EXPLICIT_OVERRIDE_HORIZONTAL_PLAN: <1-line justification ≤ 120 chars>`
  Without this verbatim literal + justification → V17 Horizontal Plan Detector + G-VS-1/2/3/4 gates will REJECT the spec and any derived task graph. With the literal present → V17 passes, and che-act §0.5 appends matching entry to `decisions.log.jsonl` with type=`EXPLICIT_OVERRIDE_HORIZONTAL_PLAN`.

### §3 CONTRACTS (DbC — PRE / POST / INVARIANTS)
Header: `## §3 CONTRACTS (Design by Contract)`
- `### PREconditions (before start)` — ≥2 bullets, ≤5. Examples: bound worktree valid; HEAD snapshot taken; no uncommitted on §2 files; env var X set.
- `### POSTconditions (after all tasks DONE — assertion-ready)` — ≥3 bullets, ≤8. Each bullet = a statement you can run a single test against; use `==`, `∈ {x,y}`, or plain assert verbs.
- `### INVARIANTS (never break, even temporarily)` — ≥1, ≤5. Last INV if empty add: `INV-<N>: Files listed in CANNOT TOUCH §2 remain byte-for-byte unchanged git diff.`

### §4 SPECIFICATION BY EXAMPLE (SbE — CENTRAL MANDATORY)
Header: `## §4 SPECIFICATION BY EXAMPLE (SbE — Public Behaviours Observable)`

> **CANONICAL SOURCE MERGING ORDER when building the tables below (do not reorder without EXPLICIT_OVERRIDE + decision.log):**
>   1st HIGHEST — current **User Prompt VERBATIM** of this session
>   2nd — **Legacy PRD (.md)** (if source = C)
>   3rd — **Linear / ClickUp / GitHub RAW Acceptance Criteria** (ac → 1 B-pos + 1 AB-neg minimum)
>   4th LOWEST — Implementer hints (only fills non-conflicting gaps)
>
> At the end of draft §4, ALWAYS ask the user:
> > "Are there more NEGATIVE (AB-) or POSITIVE (B-) edge cases I should add to the tables? Main gaps: (list 2-3 missing behaviours from the most critical user prompt category)."

#### §4.1 KEY RULES (R1..RN — max 8)
Header: `### §4.1 KEY RULES (Non-negotiable invariants 1–8)`
- MAXIMUM 8 bullets. Derived from sources above, NOT from implementation.
- Unique short NAME R1..RN + 1 action sentence + business impact.
- Examples:
  - R1: Refunds ALWAYS use Stripe `reverse_transfer=true, refund_application_fee=false` (destination charges invariant).
  - R2: No raw email persisted in admin logs (PII convention).
  - R3: Double click on Confirm Refund button NEVER creates 2 refunds (idempotency key dedup).

#### §4.2 BEHAVIOUR EXAMPLE TABLE (Positive B-IDs — max 10, 1st verification anchor)
Header: `### §4.2 POSITIVE BEHAVIOUR EXAMPLES (B-ID 1..≤10)`

**MANDATORY Markdown table. Each column = NON-EMPTY (except UI Selector when Playwright not marked).**
| B-ID | Given (Concrete Setup) | When (Single Public Action) | Then (Observable Public Behaviour ONLY — no "correctly"/"works" words — literal values / HTTP codes / UI texts / external observable side effects) | Test Layers [Unit ✅|Integ ✅|API-E2E ✅|Playwright ✅|Manual ✅] — mark ✅ CASE-BY-CASE, DO NOT mandate all | UI Selector Contract (only if Playwright ✅) — 3-part data-testid `<domain>__<component>__<action>`, double kebab `__` | Confidence target % | Risks if OMITTING marked layer ⚠️ |
|---|---|---|---|---|---|---|---|
| B-1 | Given booking_id=BK-123 exists, status=pending_payment, stripe_capture=succeeded, amount=2000p | When creator POST /api/bookings/:id/refund reason="Duplicate" | Then (HTTP 201 refund.id=RF-456 · booking.status=REFUNDED · customer.emailHash=sha256(..) receives refundConfirmation template · Stripe dashboard refund.amount=2000 with reverse_transfer=true) | [✅Integ ✅API-E2E ✅Manual] | `creator__bookings-row__refund-btn--BK-123` + `refund__action-btn__confirm` | 98% | No Integ: Stripe params omission causes webhook race → double balance deduction. No Manual: UX loading state fails visually on 3G. |
| B-2 | ... | ... | ... | [...✅] | `...` | ... | ... |

Rules enforcement for this table:
1. **MAXIMUM 10 TOTAL B-IDs** (if more gh-stack 2 PRs).
2. **Then column MUST be PUBLICLY OBSERVABLE:** HTTP status, literal UI text, email type, public Stripe/DB field. PROHIBITED Then: "service calls method X internally" (implementation bias).
3. **Test Layers column:** HONEYCOMB PYRAMID. CASE-BY-CASE. Mark ✅ only layers that actually resolve the behaviour. Default rules:
   - Pure isolated algorithm (math, formatter, hash): only ✅Unit.
   - Mutation/query REST+tRPC+DB (no UI): ✅Integ + ✅API-E2E (max 2 layers).
   - Interactive UI component (button, form, loading): ✅Playwright + ✅Manual (2 layers).
   - Cross-border business rule (3+ services): ✅Unit + ✅Integ + ✅API-E2E (3 layers).
4. **Risks if omit column:** DESCRIBE BUSINESS impact (not "coverage drops"). E.g. "Double deduction Stripe Connect balance $2k".
5. **UI Selector Contract column:** If Playwright=✅ → MANDATORY at least 2 ids per behaviour (trigger action + result verify). **G8 Category 8 code-review enforcement trigger against XPath/classes fragility.**
6. **Mapping Ticket AC → B-ID:** Each Linear ticket Acceptance Criteria → 1 positive B-ID + 1 anti-AB (below §4.3). At the end of draft, show list: `AC-T1 → B-3 + AB-2`.

#### §4.3 ANTI-BEHAVIOUR EXAMPLE TABLE (Negative AB-IDs — MINIMUM 33% OF B-IDs per S07 CHE_RULES §X)
Header: `### §4.3 ANTI-BEHAVIOUR EXAMPLES (AB-ID 1..≥ceil(B_COUNT/3) per S07)`

Table identical to §4.2, but **Then = prohibited behaviour that MUST NEVER happen.**
| AB-ID | Given (Setup IDENTICAL to corresponding B-ID — SAME Given) | When (DANGEROUS / invalid / duplicate / race action) | Then PROHIBITED (public observable — what DOES NOT HAPPEN, with literal values) | Mandatory Test Layers (≥1 layer ✅ per AB) | UI Selector (if Playwright) | Confidence target % | Risks if OMITTING AB test |
|---|---|---|---|---|---|---|---|
| AB-1 | Given BK-123 pending_payment capture=succeeded amount=2000p idempotency_key=IK-XYZ | When DOUBLE-POST /api/bookings/:id/refund (2x parallel with SAME idempotency_key) | Then (HTTP 200 idempotent replay SAME RF-456 · booking.status DOES NOT transition · Stripe refund_count=1 · balance 1 movement only) | [✅Integ ✅API-E2E] | `refund__action-btn__confirm` (double click rate limit check) | 99,5% | Not testing → 5% of refunds on double click generate negative transfer reversal and dispute. |
| AB-2 | ... | ... | Then DOES NOT... | [...✅] | ... | ... | ... |

Rules enforcement for this table:
1. **MINIMUM 33% RATIO: `AB_COUNT ≥ ceil( B_COUNT / 3 )` (V10 validation, per S07 CHE_RULES §X)**. E.g. B=9→AB≥3; B=1→AB≥1; B=4→AB≥2.
2. **Given MUST be the SAME setup as a corresponding positive B-ID** (same Given line). Proves the system resists the bad side of the happy path.
3. **When = action user would do WRONG or attacker would exploit.** Double click, race condition, auth bypass, negative field, already processed id, etc.
4. **Then cannot be vague.** Literal values. Then column ALWAYS starts with the word "Then DOES NOT" or "Then (HTTP 4xx ... DOES NOT alter booking.status)".

#### §4.4 MERMAID DIAGRAMS (CONDICIONAL MANDATORY — if trigger fired)
Header: `### §4.4 MERMAID DIAGRAMS (skip or mandatory — based on triggers)`

**§4.4.1 + §4.4.2 MANDATORY Triggers IF AND ONLY IF (per S06 CHE_RULES §X):**
`(B_COUNT >= 8) OR (COUNT(distinct_public_actors) >= 3) OR (risk_level in ["medium", "high"]) OR (frontmatter.mermaid_required = true)`
→ If NONE: write exactly `> ⚠️ Skipped (low complexity): B_COUNT=X<8 · public_actors=Y<3 · risk=low`.

**§4.4.3 ERDiagram MANDATORY Trigger IF AND ONLY IF (per S05 CHE_RULES §X):**
`(new_DB_entity = true) OR (alters_FK_ON_DELETE_cardinality = true) OR (new_fields_with_UNIQUE_CHECK_constraint >= 3) OR (frontmatter.erd_required = true)`

HARD Mermaid rules (parser crash if violated — V13 validation):
- Shapes ONLY rectangle `ID["label"]`, diamond `ID{"?"}`, edge labels `|"txt"|`. NO stadium shapes.
- Internal label line breaks ONLY `<br/>` HTML. NO literal `
`.
- Actors ONLY PUBLIC (e.g. Creator, Attendee, StripeWebhook, AdminUI). NO internal service names (e.g. RefundService, StripeClient). Prohibited.
- ALL nodes and arrows MUST have `B-X` or `AB-Y` reference in the label. E.g. `Creator["Creator (B-1, B-2)"]`.

Sub-sections if trigger fires:
- **§4.4.1 sequenceDiagram** — Actor and message order. Each message = B-ID or AB-ID.
- **§4.4.2 flowchart TD** — Branches: (a) Happy path solid edge; (b) Sad/Error path dashed edge; (c) Rollback edge `--ROLLBACK-->` red dashed label. Nodes = B-AB-IDs.
- **§4.4.3 erDiagram** (if ERD trigger) — Official Mermaid cardinality: `| = exactly 1; o| = 0 or 1; }o = 0 or N; }| = 1 or N`. Each FK or new field with corresponding B-ID in comment. UK/CHECK/UNIQUE constraints listed explicitly with B-ID number of the behaviour that uses it.

#### §4.5 VERTICAL SLICES — F0 TRAcer + F1..FN MANDATORY (Non-negotiable unless EXPLICIT_OVERRIDE_HORIZONTAL_PLAN logged)
Header: `### §4.5 VERTICAL SLICES (F0 Tracer Bullet Mandatory — unless override logged in §2 SCOPE + decision.log)`

> **CANONICAL #0 (CHE_RULES.md §Principle #0):** Every SPEC, task graph and plan MUST be decomposed into VERTICAL end-to-end SLICES (UI ↔ API ↔ DB ↔ External). The FIRST slice is ALWAYS F0 — the thinnest possible complete Tracer Bullet that proves the whole vertical plumbing works. Horizontal decomposition ("all models first, then all routes, then all pages") is PROHIBITED unless the literal `EXPLICIT_OVERRIDE_HORIZONTAL_PLAN` appears verbatim in §2 SCOPE with a 1-line justification AND a corresponding decision.log entry is appended by SM before che-act runs.

**MANDATORY Markdown table. NEVER empty. ALWAYS at minimum 1 row = F0. F0 is first, always.**
| Slice ID | Slice Name (1 single MINIMAL end-to-end behaviour) | B-IDs / AB-IDs Covered in this slice (refs §4.2 / §4.3 — 1 B-ID minimum for F0) | Layers / Files TOUCHED (ALL layers in the vertical slice listed — UI · API · DB · External if applies) | Minimum Test per Layer Touched (1 test per layer listed above) | DONE Criterion (PUBLICLY OBSERVABLE, testable in 1 sentence) |
|---|---|---|---|---|---|
| **F0** | Tracer: Confirm Event Saved & Returned in Dashboard | **B-1 only** (1 B-ID — smallest possible) | `pages/events/new.tsx` (UI) · `app/api/events/route.ts` (API) · `packages/db/src/entities/Event.entity.ts` (DB) | Playwright click + fill → redirect (UI) · Vitest route POST 201 → row in events table (API) · Jest/TypeORM `event.save()` + `repo.find()` returns it (DB) | Creator fills title + clicks "Save Event" → redirects to `/dashboard/events` → the new event title is visible at row 1 of the list, within ≤1s, on a clean db. |
| F1 | ... | B-2, AB-1 | ... | ... | ... |
| F2 | ... | B-3, B-4 | ... | ... | ... |

**Hard enforcement rules applied by V16 / V17 / G-VS-4 scope-checker:**
1. **F0 row ALWAYS EXISTS**. Table MUST have at least 1 row whose 1st column is literally `F0`. If missing → V16 FAIL.
2. **F0 Layers Touched count ≥ 2.** Split "Layers / Files TOUCHED" column by ` · ` separator — distinct top-level folder/domain count = `N`. If `N < 2` for F0 → V16 FAIL with: "F0 Tracer slice is not vertical. Layers Touched distinct count=N<2. Minimum 2 distinct architectural layers required. Either add the missing layer(s) OR declare EXPLICIT_OVERRIDE_HORIZONTAL_PLAN in §2 SCOPE with 1-line justification AND append decision.log entry."
3. **F0 B-IDs covered count ≥ 1.** Column 3 empty or 0 B-IDs → V16 FAIL.
4. **F0 DONE Criterion is NON-EMPTY.** Column 6 must contain ≥ 1 word, with no "works correctly" / "as expected" weasel words allowed — same literal-value rule as §4.2 Then column.
5. **Subsequent slices (F1, F2, ...):** Also require Layers Touched ≥ 2, unless the slice ID has the explicit suffix `H-OVERRIDE-<number>` and a matching override decision.log hash exists.
6. **Anti-pattern detection (V17 + scope-checker G-VS-4):** If ≥ 3 consecutive rows in this table have "Layers / Files TOUCHED" column with 1 single top-level folder AND NO F0 touches ≥2 layers → pattern is HORIZONTAL. V17 FAIL unless the literal override is present.

#### §4.6 REVERSIBILITY DECLARATIONS (CANONICAL #1 — Non-negotiable unless EXPLICIT_OVERRIDE_REVERSIBILITY logged)
Header: `### §4.6 REVERSIBILITY DECLARATIONS (Wrapper Boundaries · Rollback Flags · Forking Road)`

> **CANONICAL #1 (CHE_RULES.md §Principle #1):** Every SPEC with `estimated_files_max ≥ 5` OR with ≥ 1 external dependency listed in §2 External services MUST declare 3 sub-tables below. All declarations are PROJECT-AGNOSTIC: no SDK names are hardcoded; they come ONLY from §2 user input.

**§4.6.1 Wrapper Boundary Table (V19a)** — 1 row per unique external dependency declared in §2 External services. NEVER empty if §2 External services list is non-empty.
| External Dependency Name (import alias / SDK name from §2) | Authoritative Wrapper Path (SINGLE glob / folder — 1 path only, NO commas / semicolons / multiple paths) | Touch-Count if Swapped (estimated # of files touched to replace this dependency with top competitor) |
|---|---|---|
| `<example: stripe>` | `<example: packages/platform/server/integrations/stripe/**>` | `<example: 8>` |
| ... | ... | ... |

**§4.6.2 Critical Rollback Feature Flags (V19b)** — minimum 1 row IF any B-ID in §4.2 touches a "critical path" (payment, auth, refund, checkout, deploy, publish, deletion). Optional otherwise.
| B-ID(s) Affected (comma separated) | Runtime Feature Flag Name | Where Evaluated (absolute path) | Rollback Time Estimate (minutes — MUST be ≤ 5) |
|---|---|---|---|
| `<example: B-1, B-2>` | `<example: ENABLE_NEW_CHECKOUT_FLOW>` | `<example: packages/platform/server/services/checkout.service.ts:42>` | `<2>` |

**§4.6.3 Forking Road Test Answers (V19c)** — 1 row per unique Wrapper Path declared in §4.6.1 (same count, 1:1 correspondence).
| Wrapper Path (copied verbatim from §4.6.1 col 2) | Question: "If we swapped this dependency for its top competitor, how many files OUTSIDE this wrapper path would we need to touch?" | If Answer > 10 files OR > 2 packages → Annotate as TECHNICAL COUPLING in §2 SCOPE with 1-line mitigation plan here or N/A |
|---|---|---|
| `<example: packages/platform/server/integrations/stripe/**>` | `<example: 3 files — adapter pattern already abstracts it>` | `N/A` |
| ... | ... | ... or `TECHNICAL COUPLING: migrate remaining inline SDK calls inside wrapper before B-3 ships.` |

#### §4.7 ASSERTIVE PROGRAMMING — INVARIANTS AND IMPOSSIBLE STATES (CANONICAL #3 — Non-negotiable if B_COUNT ≥ 3)
Header: `### §4.7 ASSERTIVE PROGRAMMING: INVARIANTS AND IMPOSSIBLE STATES (CANONICAL #3 DbC, V20)`

> **CANONICAL #3 (CHE_RULES.md §Principle #3):** Distinction ASSERTION vs ERROR is mandatory. Assertions CRASH immediately (dead programs tell no lies). Error-returns handle expected runtime contingencies (covered by AB-IDs).

Table required IF AND ONLY IF `B_COUNT ≥ 3`. Minimum rows = `ceil(B_COUNT / 3)`.
| Assertion ID | Impossible Condition (1 technical sentence — NEVER happens in correct code) | Where Enforced (absolute path + symbol name) | Crash vs Error (MUST be literal "CRASH" — if Error, remove this row from here and handle via AB-ID in §4.3 instead) |
|---|---|---|---|
| **A-1** | `<example: auth_user_id is empty string or null on POST /api/refunds route — request has valid session cookie so session.userId MUST exist>` | `<example: packages/platform/server/middleware/requireAuth.ts invariant(session?.user?.id, "session.user.id missing on authenticated route")` | **CRASH** |
| A-2 | ... | ... | **CRASH** |

#### §4.8 DRY KNOWLEDGE SINGLE SOURCE OF TRUTH (V21 — MANDATORY if B_COUNT ≥ 5)
Header: `### §4.8 DRY KNOWLEDGE SINGLE-SOURCE (V21 — Single Authoritative Representation per Business Rule)`

> **CANONICAL #1 pragmatic-programmer SKILL §DRY:** DRY is about KNOWLEDGE DUPLICATION, not code syntax similarity. Each business rule = EXACTLY 1 authoritative representation.

Required IF `B_COUNT ≥ 5`. One row per UNIQUE non-trivial business rule that appears in ≥ 2 B-ID Then-clauses or ≥ 1 AB-ID.
| Business Rule Text (1 sentence, plain English — e.g. "UK VAT = 20% on ticket face value for events in England") | Authoritative Single-Source Absolute Path (the ONLY file/module/DB-table-column/constant that defines this rule — exactly 1 path) | List of Other Locations That Reference/Consume This Rule (consumers are OK — duplications = violation) | DRY Status (PASS / DRY_VIOLATION + mitigation plan) |
|---|---|---|---|
| `<example: Booking Service Fee = 7.5% of face value, capped at 25 GBP per ticket>` | `<example: packages/platform/server/constants/fees.ts SERVICE_FEE_RATE + SERVICE_FEE_CAP_GBP>` | `<1. route handler reads it; 2. Admin dashboard pricing page reads it; 3. Stripe price calculation reads it>` | **PASS** (1 source, 3 consumers — no duplication) |
| ... | ... | ... | ... or **DRY_VIOLATION: fee percentage hardcoded in admin pricing page + DB column + Stripe handler. Mitigation: move sole authority to packages/platform/server/pricing engine before merge.** |

#### §4.9 ORTHOGONALITY COUPLING MAP (V22 — MANDATORY if distinct_top_level_packages_touched ≥ 3)
Header: `### §4.9 ORTHOGONALITY COUPLING MAP (V22 — Can we swap each layer in under a week? Forking Road per Layer)`

Required IF `COUNT(DISTINCT top-level packages touched from §2 CAN TOUCH) ≥ 3`. One row per distinct top-level package / architectural layer.
| Top-Level Package / Architectural Layer (e.g. `packages/db`, `pages/`, `app/api/`, `packages/auth`) | Question: "If we swapped this package's underlying framework/technology for its most popular competitor (TypeORM → Prisma, Next Pages → App Router, Auth.js → Clerk, etc), how many files OUTSIDE this package would need changes?" | If Answer > 10 → Annotate COUPLING_RISK in §2 External services section. | Orthogonality Status (OK / COUPLING_RISK + mitigation plan) |
|---|---|---|---|
| `<example: packages/db>` | `<example: ~22 files — business logic queries repo methods directly instead of interfaces>` | Yes | **COUPLING_RISK: introduce Service interfaces via DI before scope expands to B-7+** |
| ... | ... | ... | **OK** |

### §5 VERIFICATION MATRIX (Bilateral B-ID ↔ Test File ↔ Evidence)
Header: `## §5 VERIFICATION MATRIX (Bilateral — B → Test → B)`

> **Purpose:** Living TODO checklist that che updates AUTOMATICALLY in each SM/Developer/QA loop.
> **Bilateral anchors:** (1) Spec §4 B-ID → (2) `// @ac B-X` comment 1st line inside `it()`/`test()` → (3) Resultado/evidence sha256.
> **Scope-checker CHECK2 validates the reverse: (2) → (1) + (3).**

MANDATORY Markdown table (B-IDs first, then AB-IDs below):
| Anchor (B or AB) | Status (Planned|Written|Passed|Failed|Skipped) | Test file ABSOLUTE PATH (real path inside bound worktree) | Evidence sha256 (stdout/err hash or screenshot png hash) | QA Owner Assigned | Notes |
|---|---|---|---|---|---|---|
| B-1 | Planned | `packages/platform/server/__tests__/e2e/refundFlow.api.test.ts` L:78-111 | | Developer (SM) | // @ac B-3 | @ticket FLO-513 anchor |
| B-2 | Planned | ... | ... | ... | ... |
| AB-1 | Planned | `packages/platform/server/__tests__/integration/refundIdempotency.integ.test.ts` | | QA | Double click — Playwright extra step after integ |
| AB-2 | ... | ... | ... | ... | ... |

AUTOMATIC update of this matrix IN EACH LOOP:
- Developer finishes task → updates `Status=Written` + `Test file path`.
- QA run → updates `Status=Passed|Failed|Skipped` + append Evidence SHA256 (generate via `sha256sum stdout.log | cut -d' ' -f1`).
- Failed → new Notes line "Reproduce: command X".
- **G5 Regression Location (MANDATORY Notes line for regression/repro lock tests):**
  Notes must also explicitly indicate **regression file LOCATION**:
  - DEFAULT: ✅ `[colocated in feature / domain folder — @ticket FLO-123]` (standard rule).
  - EXCEPTION (only if cross-cutting ≥4 domains / pure infra): ⚠️ `[tests/regression/FLO-123--refund-idempotency.test.ts] — EXPLICIT_OVERRIDE_G5_REGRESSION_FOLDER decisions.log entry: auth+billing+notification+db ≥4 domains — 1-line justification`. If test is in tests/regression with ticket ID in filename WITHOUT non-empty Notes entry → scope-checker CHECK2 bilateral marks warning SCOPE_score -2 penalty).

### §6 MANUAL SMOKE TEST PLAN (Staging + Prod HUMAN — ALWAYS MANDATORY)
Header: `## §6 MANUAL SMOKE TEST PLAN (HUMAN — Staging + Prod)`

> **User requirement VERBATIM: "In addition to e2e tests, we should have a manual test plan ... manual testing should also be thought of from the beginning when going to production."**
> Minimum 3 STAGING steps + 2 PROD steps.

#### §6.1 STAGING Environment (post-deploy pre-PR merge — 3..8 steps)
| Step # | Role (Creator|Attendee|Admin|Staff Scanner) | Concrete Manual Action 1-click / 1-screen | Expected Result (literal, public observable — matches corresponding B-ID Then) | Anchor B-ID |
|---|---|---|---|---|---|
| S1 | Creator | Login staging; navigate Bookings → BK-123 row → Refund button → modal → Confirm. | (1) Green toast "Refund RF-456 created"; (2) Row status → "Refunded"; (3) Staging email inbox → subject "Your refund is on its way". | B-1 |
| S2 | ... | ... | ... | B-2 |
| S3 | Creator | Repeat Step S1 quick DOUBLE CLICK on Confirm button | (1) Only 1 toast; (2) 1 Refunds history entry; (3) Staging Stripe dashboard → 1 refund only. | AB-1 |

#### §6.2 PROD Environment (post deploy live — 2..5 steps MINIMUM NON-DESTRUCTIVE)
| Step # | Role | SAFE Manual Action (DO NOT touch real production data — use dummy canary event if possible) | Canary Expected Result | Anchor B-ID |
|---|---|---|---|---|
| P1 | Admin | Access `/admin/health` → "Refund health check" tab (create if none) → Run canary refund of 0.01 GBP in sandbox connected account CA-TEST-ONLY. | Canary result: Stripe reverse_transfer=true; response 200; DB canary_refund_audit table 1 row. | B-1 |
| P2 | Admin | View production Logs last 15 min → filter `service=refund` | No ERROR / stacktrace after deploy. | B-4 |

#### §6.3 UI ONLY Extra Steps (if Playwright marked in any B-ID OU risk≥medium)
→ If false trigger → write: `> ⚠️ Skipped: no behaviour with Playwright layer AND risk=low`.
→ If true trigger → add cross-browser UI steps table (Chrome/Firefox/Safari iOS 17):
| Step | Device/Browser | Action | Expected visual UI | Anchor |
|---|---|---|---|---|
| UI-1 | Chrome Desktop 128, 125% zoom | 3G throttled. Confirm Refund → loading spinner → toast. | Spinner appears ≥500ms ≤2s. Green toast text match literal. No layout shift. | B-1 loading. |

### §7 IMPLEMENTATION HINTS (opt-in, only if re-use exists or gotchas — 2..5 bullets MAX)
Header: `## §7 IMPLEMENTATION HINTS (Optional — reference existing code only)`
- Bullet 1: Reference existing function/class/commit hash or existing pattern from graphify-out community hub or `packages/platform/server/providers/stripe/StripeClient.ts createRefund` params.
- Bullet 2: Runtime gotcha. E.g. "Vercel edge runtime: DO NOT use setImmediate for email sending; use queues/await directly or webhook."
- DO NOT add implementation sketch here → §4 SbE sections already define public behaviour. This is only a context accelerator.

---

## §4 VALIDATION PASS (auto-run on draft — NEW SbE rules V9..V15)

Reject draft and loop back to §2 source if ANY check fails. Run in order.

### Legacy baseline checks (V1-V8)
1. **V1** YAML frontmatter all REQUIRED keys present; parseable as YAML.
2. **V2** `estimated_files_max ≤ 20` (§15 engineering-contracts KISS); if >20 → force user to reduce scope or trigger gh-stack immediately.
3. **V3** §1 WHY bullets ≤ 5.
4. **V4** §2 CAN TOUCH count ≤ 10 literal files or glob entries.
5. **V5** §3 ≥3 POSTconditions, ≥1 INVARIANT.
6. **V6** (legacy superseded by V9-V15 but still run for old specs without SbE) → if spec DOES NOT yet contain header `## §4 SPECIFICATION BY EXAMPLE`: §4 ACs ≥3 MUST, each bullet contains GIVEN/WHEN/THEN/TEST literal. Else SKIP this check gracefully (SbE drafts NO longer use MoSCoW ACs).
7. **V7** (legacy, skip if SbE draft) §5 rollback trigger = exactly 1 trigger sentence, non-empty.
8. **V8** (optional, always run if domain filled non-default) → `domain:` MUST be in EXACT 7-slugs canonical enum: `engineering | product | ux | devops | copywriting | social | seo-analytics`. If typo/outside enum → **REJECT draft with clear msg**: "Field `domain: <invalid_value>` invalid. Accepted values: engineering | product | ux | devops | copywriting | social | seo-analytics. Default omission = engineering (retrocompat). Fix frontmatter or remove the field. Default is engineering."

### SbE MANDATORY checks (V9-V15 — run ONLY if header `## §4 SPECIFICATION BY EXAMPLE` exists in draft. Today = ALWAYS, as SbE = default.)
9.  **V9 B-IDs max 10:** Count lines in §4.2 POSITIVE BEHAVIOR TABLE whose 1st column starts exactly with `B-` and has digits after (`B-1`, `B-10`). `B_COUNT = COUNT`. If `B_COUNT > 10` → REJECT: "Positive behaviours (B-IDs) = $B_COUNT. MAXIMUM allowed = 10. Reduce scope or use gh-stack for 2 independent PRs (see engineering-contracts §15 gh-stack multi-PR reference)."
10. **V10 Anti-behaviour ratio min 33%:** Count AB-IDs in §4.3 ANTI-BEHAVIOR TABLE → `AB_COUNT = COUNT`. Calculate `EXPECTED_AB_MIN = ceil(B_COUNT / 3)`. If `AB_COUNT < EXPECTED_AB_MIN` → REJECT: "Missing anti-behaviours (AB-IDs). B_COUNT=$B_COUNT, AB_COUNT=$AB_COUNT, MINIMUM EXPECTED = ceil($B_COUNT/3) = $EXPECTED_AB_MIN. Add at least ($EXPECTED_AB_MIN - $AB_COUNT) negative AB- (race/edge/invalid/attack) in table §4.3."
11. **V11 Each B-ID has ≥1 Test Layer marked ✅:** Parse each B- line in table §4.2 "Test Layers" column — if DOES NOT contain literal `✅` character at least once → REJECT: "B-XX Test Layers column has NO layer marked ✅ (Unit/Integ/API-E2E/Playwright/Manual). Mark at least 1 layer CASE-BY-CASE (honeycomb pyramid; do not mandate all)."
12. **V12 UI Selector Contract regex validation:** For each B-ID line where "Test Layers" column CONTAINS `Playwright` literal → extract ids from "UI Selector Contract" column. Each data-testid MUST match canonical Category 8 G8.3 REGEX: `^[a-z0-9][a-z0-9-]*__[a-z0-9][a-z0-9-]*__[a-z0-9][a-z0-9-]*(--[a-z0-9][a-z0-9-]*)?$`. If NOT matching → REJECT: "B-XX data-testid=`<id>` outside 3-part convention `<domain>__<component>__<action>[--unique-suffix]`. Expected regex: `^[a-z0-9-]+__[a-z0-9-]+__[a-z0-9-]+(--[a-z0-9-]+)?$`."
13. **V13 Mermaid diagrams trigger compliance:**
    a. Calculate MERMAID_TRIGGER = `(B_COUNT >= 8) OR (risk_level == "medium") OR (risk_level == "high") OR (mermaid_required == true) OR (distinct_public_actors >= 3)`.
    b. If MERMAID_TRIGGER == TRUE → validate that draft CONTAINS 2 exact headings: `### §4.4.1 sequenceDiagram` AND `### §4.4.2 flowchart TD`. If ANY missing → REJECT: "Mermaid trigger fired (B=$B_COUNT, risk=$risk_level). §4.4.1 sequenceDiagram and §4.4.2 flowchart TD BOTH mandatory. X missing."
    c. Calculate ERD_TRIGGER = `(erd_required == true) OR (new_DB_entity detected by CREATE TABLE word / new TypeORM Entity() in §2 CAN CREATE) OR (new_fields >= 3 UNIQUE|CHECK|UK words in §2 SCOPE)`.
    d. If ERD_TRIGGER == TRUE → validate that draft CONTAINS exact heading `### §4.4.3 erDiagram`. If missing → REJECT: "ERD trigger fired (new DB entity or FK/cardinality change or ≥3 field constraints). §4.4.3 erDiagram mandatory."
    e. (Anti-crash Mermaid parser) If §4.4 contains mermaid code blocks: validate that NO node contains stadium shapes `[/` or `([` or `\]/` or `)]`. If stadium shape present → WARNING (non-fatal but correction recommended before Approved): "Warning: Mermaid stadium shapes ( [/label/] or ([label]) ) collide with ()/ chars in label text → Mermaid 10.x+ parser crash. Replace with quoted rectangle `ID["label"]`."
14. **V14 §6 Manual Smoke Plan staging minimum 3 steps and prod minimum 2 steps:** Count §6.1 Staging table lines in Step # column with S-1,S-2,S-3 → if `< 3 steps` → REJECT: "Manual Smoke Plan STAGING (§6.1) has $N steps. MINIMUM 3 mandatory steps." Count §6.2 Prod P-1,P-2 steps → if `< 2 steps` → REJECT: "Manual Smoke Plan PROD (§6.2) has $N steps. MINIMUM 2 NON-DESTRUCTIVE mandatory steps."
15. **V15 Frontmatter counters match actual tables:** If b_count or ab_count are filled in YAML (≠ 0 or empty) → validate `frontmatter.b_count == real B_COUNT of table §4.2` AND `frontmatter.ab_count == real AB_COUNT of table §4.3`. If diverging → non-fatal WARNING: "Warning: frontmatter.b_count=$front ab_count=$front != real table B=$realB AB=$realAB. Auto-fix before Approved."

16. **V16 Vertical Slice F0 Mandatory (CANONICAL #0):** (runs ONLY if `frontmatter.vertical_slice_required == true`) Parse table under header `### §4.5 VERTICAL SLICES`. Fail conditions → REJECT with structured fix offer:
    a. **Missing table or empty:** Header `### §4.5 VERTICAL SLICES` not found OR table has 0 data rows. Msg: "§4.5 VERTICAL SLICES table missing or empty. CANONICAL #0 requires at minimum 1 row = **F0 Tracer Bullet**. Fix: (A) Auto-insert F0 template now (B) Declare EXPLICIT_OVERRIDE_HORIZONTAL_PLAN in §2 SCOPE with 1-line justification."
    b. **No F0 row:** Table has rows but none whose Slice ID column = literal `F0` or `**F0**`. Msg: "§4.5 table has no F0 row. First slice MUST be F0 (thinnest possible complete end-to-end path). Add F0 as row 1."
    c. **F0 Layers Touched < 2:** F0 row "Layers / Files TOUCHED" column — split by separator ` · `, extract distinct top-level folder/domain prefixes (first path segment before `/` or word in parentheses). Distinct count < 2 → REJECT: "F0 Tracer is NOT a vertical slice — distinct architectural layers touched=$N < 2. Add missing layer (e.g. if only models listed → add route + page, or declare override)."
    d. **F0 B-IDs count 0:** "B-IDs / AB-IDs Covered" column of F0 row has no B-N or AB-N literal → REJECT: "F0 Tracer must cover at minimum 1 positive B-ID from §4.2. Cover B-1 (smallest behaviour) in F0."
    e. **F0 DONE criterion empty or weasel:** Column 6 (DONE) is empty OR contains banned words `correctly|as expected|properly|works|ok` case-insensitive → REJECT: "F0 DONE criterion is missing or uses weasel words. Write 1 single PUBLICLY OBSERVABLE sentence with literal values (HTTP codes, UI text, DB row count, observable side effects). Same rule as §4.2 Then column."
    If ALL a-e pass → auto-set frontmatter `tracer_f0_defined: true` and proceed.

17. **V17 Horizontal Plan Detector (CANONICAL #0 Anti-pattern):** Parse: (i) §4.5 VERTICAL SLICES table rows (after header), (ii) §2 CAN TOUCH / CAN CREATE lists. Compute for each slice row: if "Layers / Files TOUCHED" column lists only 1 top-level folder (all paths share same first segment) → mark slice H=1. Consecutive H=1 slice count = H_CONSECUTIVE.
    - If H_CONSECUTIVE ≥ 3 AND NO slice has Layers ≥ 2 → pattern = HORIZONTAL.
    - Additionally: if §2 CAN TOUCH lists ONLY files from a single top-level folder (only `packages/db/**` OR only `pages/**` etc) AND estimated_files_max > 5 → pattern = HORIZONTAL.
    HORIZONTAL detected → ONLY permit if:
    1. The literal string `EXPLICIT_OVERRIDE_HORIZONTAL_PLAN` appears VERBATIM anywhere in §2 SCOPE (Cannot Touch, External services, or a dedicated override bullet), AND
    2. The literal is immediately followed by a 1-line colon-prefixed justification of ≤ 120 chars. E.g. `- EXPLICIT_OVERRIDE_HORIZONTAL_PLAN: schema-only migration for 12 tables — no UI/API change possible`.
    If conditions (1)+(2) met → V17 PASS, append decision.log entry with the justification. If ANY condition missing → REJECT with: "Horizontal slice pattern detected (H_CONSECUTIVE=$N single-layer slices or CAN TOUCH=$single-folder only). Default strategy = VERTICAL (F0 + F1/FN). Options: (A) Add a vertical F0 + re-order slices so ≥ 2 layers per row (B) Paste literal `EXPLICIT_OVERRIDE_HORIZONTAL_PLAN: <1-line reason>` as a new bullet in §2 SCOPE Cannot Touch or External services section → decision.log will be appended by che-act SM §0.5 pre-gate."

18. **V19 Reversibility Declarations (CANONICAL #1 — 3 sub-tables):** Compute TRIGGER_V19 = `(estimated_files_max >= 5) OR (external_deps_count_in_§2 >= 1)`. If TRIGGER_V19 = false → SKIP V19 silently. Else validate 3 sub-tables:
    a. **V19a Wrapper Boundary**: Header `§4.6.1` exists. Row count = `external_deps_count` (1 row per dep). Column 2 `Authoritative Wrapper Path` must contain EXACTLY 1 single glob/path (no `,` `;` `|` multiple separators). If any violation → REJECT: "§4.6.1 Wrapper Boundary table (V19a) missing or row count mismatch ($N rows vs $M external deps listed in §2) or wrapper path has multiple separators. Options: (A) Auto-insert empty wrapper table now (B) Add literal `EXPLICIT_OVERRIDE_REVERSIBILITY: <1-line reason>` as a new §2 SCOPE bullet (for 100% internal scopes with zero external deps)."
    b. **V19b Rollback Flags**: Header `§4.6.2` exists. If ANY B-ID Then column contains keywords `checkout|payment|refund|auth|deploy|publish|delete|critical` (regex insensitive) → table §4.6.2 MUST have ≥ 1 row. Each row's Rollback Time Estimate column MUST be ≤ 5 (parse integer, reject if `>5` or non-numeric). Violation → REJECT with msg + list of critical B-IDs detected.
    c. **V19c Forking Road**: Header `§4.6.3` exists. Row count = exactly count of unique wrapper paths from §4.6.1.

19. **V20 Assertive Programming / Invariants (CANONICAL #3 DbC):** Compute TRIGGER_V20 = `(B_COUNT >= 3)`. If TRIGGER_V20 = false → SKIP silently. Else:
    - Header `§4.7` table exists.
    - `A_COUNT = number of rows with Assertion ID A-<N>`.
    - Minimum rows required = `ceil(B_COUNT / 3)`.
    - For each row, column 4 (Crash vs Error) MUST contain literal word `CRASH` (case-insensitive match), NOT word `Error`.
    - If `A_COUNT < ceil(B/3)` OR missing header OR ≥1 row contains `Error` → REJECT: "§4.7 Assertive Programming invariants table (V20) missing or too few rows (A=$A_COUNT, MIN=ceil($B_COUNT/3)=$MIN) or rows marked Error instead of CRASH. Error contingencies belong in §4.3 Anti-behaviour table as AB-IDs; §4.7 is only for IMPOSSIBLE conditions that MUST crash immediately."

20. **V21 DRY Knowledge Single-Source (pragmatic-programmer #1 DRY):** TRIGGER_V21 = `(B_COUNT >= 5)`. If false → SKIP silently. Else:
    - Header `§4.8` table exists with ≥ 2 rows.
    - Each row column 4 (DRY Status) must say PASS or DRY_VIOLATION: followed by a non-empty mitigation plan sentence.
    - No duplicate Business Rule Text in column 1.

21. **V22 Orthogonality Coupling Map (pragmatic-programmer #2 Orthogonality):** TRIGGER_V22 = `(COUNT(DISTINCT top-level packages in §2 CAN TOUCH paths) >= 3)`. If false → SKIP silently. Else:
    - Header `§4.9` table exists with ≥ 3 rows.
    - Each row column 4 = either `OK` or starts with `COUPLING_RISK:` followed by non-empty mitigation.

22. **V23 Simplicity Bias declaration (engineering-contracts §1):** §1 WHY MUST contain a non-empty `Non-goals (deferred by design)` bullet AND a Goal bullet naming the smallest-first / most-reversible option. Missing → REJECT: "§1 WHY has no explicit deferral. State what is deliberately NOT built in this iteration and why it is safe to defer (Simplicity Bias, engineering-contracts §1)."

### Bilateral cross-ref scope-checker CHECK2 (ONDA2 next block)
When this VALIDATION PASS runs GREEN (all pass), che also prints a 1-line footer:
> `SbE spec valid: B=$B_COUNT AB=$AB_COUNT AB_ratio=$RATIO% Mermaid=$TRIG ERD=$ERD_TRIG.`
This line is parsed by `che-scope-checker` CHECK2 (ONDA2) before performing bilateral B-ID ↔ test file cross-validation.

---

## §5 APPROVAL LOOP (1 main pass, 1 edit pass MAX — KISS)

1. **Show draft** to user as compact markdown, WITH a legend at the top saying "Draft SPEC. Reply A = Approve as-is. Reply B = adjust <tell what to change>."
2. **If A (Approved verbatim):**
   - Update frontmatter → `status: Approved`
   - Set `approver: "user-verbatim: A"`
   - Set `approved_at: <ISO timestamp local tz>`
   - Jump to §6 SAVE.
3. **If B (adjust X):**
   - Apply edits literally to the sections user indicated (no scope creep beyond what the user typed).
   - Re-run §4 VALIDATION.
   - Re-show ONE TIME only.
   - User now either Approves → update frontmatter Approved → SAVE. OR says "more edits" → tell user to re-run `/che-spec` fresh (avoid infinite loops).
4. **If user says "Cancel":** Write Draft (no Approved flag) → SAVE anyway for future work. Print warning: `SPEC_STATUS=Draft (not Approved — che-act will re-prompt when you run it)`. End.

---

## §6 SAVE (atomic write via contract helpers)

1. **Final sanitise slug:** `slug = frontmatter.spec_id` sanitised `[^a-zA-Z0-9_-] → -`.
2. **Resolve the canonical path (NEVER hand-build it):**
   ```bash
   # related_id = <slug>: one folder per SPEC, so versions stay together.
   # scope = workspace → DURABLE. output_path creates the parent on demand.
   SPEC_FINAL_PATH="$(che output_path "spec" "spec" "${slug}" "workspace" "md")"
   ```
   Result: `$CHE_WORKSPACE_SHARED/specs/<slug>/<UTC-ts>-spec.md`
   This is the ONLY location the execution gate reads. Never write `$CHE_WORKSPACE_SHARED/spec_<slug>.md`
   — that legacy root path is still *read* for backward compatibility (`/che-act`, `/che-ship`) but never written.
3. **Check existing overwrite:** If file already exists AND existing status is Approved → ask "Overwrite Approved spec? Yes/No" before writing. Yes = overwrite. No = append `-v2`, `-v3` suffix to slug until unused.
4. **Write EXCLUSIVELY via atomic write helper — to the path from step 2:**
   ```bash
   che write_file_atomic "$SPEC_FINAL_PATH" <<'SPEC_EOF'
   ---
   # Full YAML frontmatter here
   ---
   # 7 sections of SPEC here
   SPEC_EOF
   ```
   (The helper already runs `che assert_outside_worktree` automatically before writing.)
5. **Append decision entry via `che decision_append` (DO NOT build path or format JSON manually):**
   ```bash
   # decision_append helper already ensures path outside worktree + atomic append
   che decision_append "$WORKTREE_ROOT" "SPEC" "${slug} ${status} saved. Approver=${approver}"
   ```

---

## §7 RETURN VALUES

Print LAST 2 lines of transcript in a fenced code block EXACTLY:

```
SPEC_PATH=<absolute path of saved spec, no quotes>
SPEC_STATUS=Approved|Draft
```

Scrum Master §0.5 parses these 2 lines to proceed.

---
name: "che-onboarding"
description: "Shared human registry (Level 1.5 registry) of PRODUCT + MANUAL ARCHITECTURE + ROADMAP + PEOPLE context. Complementary to che-xray (automatic): this skill is the HUMAN side. Che ALWAYS reads product_context.md + architecture.md BEFORE generating ANY SPEC via che-spec. Mandatory gate BEFORE /che-spec in projects that have never passed through here. Registry stays OUTSIDE user worktree in $CHE_SESSIONS_ROOT/.registry/projects/<slug>/. DOES NOT create anything in the worktree unless the user explicitly asks VERBATIM."
---

# Che Project Knowledge — Human Project Registry

> **SHARED REFERENCES (CANONICAL):**
> - Complementary auto-onboarding: `/che-xray` (this skill does not replace xray)
> - Paths: `che` CLI (`che compute_paths`, `che ensure_dirs`, `che registry_lookup`)
> - Accidental complexity rules + deep modules: `engineering-contracts` §1 + Appendix D (Ousterhout)

---

## -0.1 STORAGE BOUNDARY PREFLIGHT (MANDATORY BEFORE FIRST WRITE)

```bash
# 1. Resolve the `che` CLI — it owns the 5-tier Che-home cascade (CHE_HOME → HARNESS_HOME
#    → ~/.che-ai → legacy ~/.trae iff CHE_RULES.md exists → ~/.che-ai fallback).
command -v che >/dev/null 2>&1 || { echo "❌ FATAL: 'che' CLI not found on PATH. Zero writes without storage boundary. exit 98"; exit 98; }

# 2. WORKTREE_ROOT required to resolve canonical PROJECT_SLUG
WORKTREE_ROOT="${WORKTREE_ROOT:-$(pwd)}"
SESSION_ID="${SESSION_ID:-onboarding-$(date -u +%Y%m%d-%H%M%S)}"

# 3. Canonical paths + ensure dirs (creates CHE_PROJECT_DIR under .registry/projects)
eval "$(che compute_paths "$WORKTREE_ROOT" "$SESSION_ID" --cwd "$PWD")"
che ensure_dirs "$WORKTREE_ROOT" "$SESSION_ID" --cwd "$PWD"

# 4. Double-guard: registry stays OUTSIDE worktree (by design .registry/ is in CHE_SESSIONS_ROOT)
[ -n "${CHE_PROJECT_DIR:-}" ] || { echo "[che-onboarding] ❌ CHE_PROJECT_DIR not defined. compute_paths failed?" >&2; exit 99; }
che assert_outside_worktree "$CHE_PROJECT_DIR" "$WORKTREE_ROOT" --label "CHE_PROJECT_DIR"
che assert_outside_worktree "$CHE_WORKSPACE_SHARED" "$WORKTREE_ROOT" --label "CHE_WORKSPACE_SHARED"

# 5. Construct canonical registry paths ONCE via type=project_registry helper
PROJECT_REGISTRY_DIR="$(dirname -- "$(che output_path "project_registry" ".keep" "${CHE_PROJECT_SLUG:-unknown}" "workspace" "md")")"
# If helper generated subpath under WORKSPACE_SHARED but canonical registry uses CHE_PROJECT_DIR → use CHE_PROJECT_DIR
[ -d "$CHE_PROJECT_DIR" ] || mkdir -p "$CHE_PROJECT_DIR"

PROJECT_PROFILE_PATH="${CHE_PROJECT_DIR}/project_profile.md"
PRODUCT_CONTEXT_PATH="${CHE_PROJECT_DIR}/product_context.md"
ARCHITECTURE_PATH="${CHE_PROJECT_DIR}/architecture.md"
ROADMAP_PATH="${CHE_PROJECT_DIR}/roadmap.md"
PROJECT_REGISTRY_JSONL="${CHE_PROJECT_DIR}/registry.jsonl"
```

**DO NOT INVENT paths:** The 4 registry files + audit jsonl always stay under `$CHE_PROJECT_DIR`. NEVER create `./docs/product_context.md` inside the worktree. If the user asks VERBATIM to "also save to the worktree to commit", that is an exception; but the canonical source ALWAYS stays in `$CHE_PROJECT_DIR`.

---

## 0. WHY IT EXISTS (Lean Motivation)

che-xray = automatic, reads CODE.
che-onboarding = human, reads INTENT, BUSINESS CONTEXT, PEOPLE.

Without this skill: che generates technically correct but **product-misaligned** specs, missing personas, scope limits, planned integrations, and known business risks. Saves 3-5 "that wasn't it" iterations per feature.

---

## 1. WHEN TO CALL

| Moment | Action |
|---|---|
| ✅ FIRST TIME after `/che-xray` (obligation) | Fill **product_context.md** + **roadmap.md** + manual architecture.md |
| ✅ PRODUCT SCOPE CHANGE (e.g. pivot, major new feature, new segment) | Update product_context + roadmap |
| ✅ MAJOR ARCHITECTURAL CHANGE (e.g. monolith → microservices, DB switch) | Update manual architecture.md |
| ✅ NEW TEAM MEMBER joins | Use `--show` to provide structured onboarding |
| ✅ BEFORE `/che-spec` if it is the project's first feature | Read everything + absorb |

**Do not use if:** it is just a code refresh → `/che-xray`.

---

## 2. 4 FILES IN REGISTRY LEVEL 1.5 (shared across worktrees)

Always UNDER `$CHE_PROJECT_DIR/` (= paths constructed in PREFLIGHT; NEVER inside user worktree):

```
${CHE_PROJECT_DIR:-$CHE_SESSIONS_ROOT/.registry/projects/<slug>}/
├── project_profile.md   ← AUTO (che-xray)   · 12 technical sections
├── product_context.md   ← HUMAN (THIS SKILL)    · 8 MANDATORY sections
├── architecture.md      ← HYBRID                  · xray auto + manual here
├── roadmap.md           ← HUMAN (THIS SKILL)    · planned epics
└── registry.jsonl       ← append-only audit via che decision_append
```

### 2.1 How to write to the registry (3 HARD rules)

1. **Every write is an atomic tmp→mv write** via `che write_file_atomic <path>` (DO NOT `cat > file`, DO NOT edit in-place in interactive Mode B).
2. **Every audit append** in registry.jsonl **uses `che decision_append`**; DO NOT `echo "{}" >> registry.jsonl` manually.
3. **NEVER create docs inside the worktree as primary.** Exception only if the user asks VERBATIM to "save this product_context.md in the worktree to commit"; in that case, the canonical source remains `$PRODUCT_CONTEXT_PATH` and snapshotted (OPTIONALLY) to the worktree.

Example Mode B item 8 audit trail (PREVIOUSLY manual echo → NOW helper):
```bash
che decision_append "$WORKTREE_ROOT" "PROJECT_KNOWLEDGE_UPDATE" "{\"project_slug\":\"${CHE_PROJECT_SLUG:-unknown}\",\"updated_sections\":[\"product_context.1\",\"roadmap.E1\"]}"
# Output lands AUTOMATICALLY in CANONICAL decisions.log.jsonl (outside worktree)
# + optionally append to $PROJECT_REGISTRY_JSONL if registry-local audit desired:
che decision_append "$WORKTREE_ROOT" "PROJECT_KNOWLEDGE_UPDATE" "{...}" 2>/dev/null || true
```

---

## 3. MANDATORY `product_context.md` TEMPLATE (8 SECTIONS)

THIS SKILL generates the skeleton below and INTERACTS with the user to fill each section. It does not invent anything; if the user does not know → leaves `[PENDING — fill later]`.

```markdown
---
project_slug: <slug>
last_updated: <ISO8601 UTC>
updated_by: human (che-onboarding interactive)
lang_code: en
lang_docs: en
# ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑
# LANGUAGE PER-PROJECT CONFIGURATION
# - lang_code: en (DEFAULT — almost never change) → controls identifiers, variables,
#   classes, functions, file/folder names, type names. ALWAYS English by default.
#   ONLY CHANGE IF the user EXPLICITLY says they want code in another language.
# - lang_docs: en (DEFAULT) → controls inline comments, JSDoc, PR titles/bodies,
#   commit messages, ADRs, README, SPEC docs.
#   MOST COMMON OVERRIDE CONFIGURATION:
#     lang_docs: en   (DEFAULT — variable code EN → comments/PR/commits = EN)
# HARD RULE (verbatim user): never mix languages. If lang_docs = pt-BR,
# EVERY comment in EVERY file in PT-BR. If lang_code = en, EVERY variable name
# EVERYWHERE in EN. Do not do half PT half EN.
---

# Product Context — <Friendly Product Name>

## 1. What is this product? (2-3 sentence elevator pitch)
> E.g.: "Flockr is an event ticketing platform in the UK focused on independent creators. Target audience: event organisers (creator) + attendees (buyer). Key differentiator: ticket QR with anti-fraud offline scanner."
- Short name:
- Long name (if brand has one):
- Primary country / region: e.g. UK, BR, US, Global
- Canonical currency: e.g. GBP pence integer, BRL cents, USD cents
- Canonical display timezone: e.g. Europe/London, America/Sao_Paulo

## 2. Market segment + PRIMARY personas
> MAXIMUM 3 personas. Fewer = less ambiguity in che.
| ID | Persona | Daily action example IN THIS product | Technical level (1-5) |
|---|---|---|---|
| P1 | Independent event creator | Creates event, sets prices, views sales | 2 = does not know CLI |
| P2 | Ticket buyer | Searches for event, buys, receives email with QR | 1 = mobile app/site only |
| P3 | Door security staff | Scans QR at entrance, offline | 1 = only touches scan button |

## 3. Domain / business line (keywords so che doesn't get terms wrong)
> E.g.: tickets, events, QR code offline scanner, QR anti-fraud, venue capacity, creator vs buyer personas, Stripe Connect split payout.
- Business keywords (10-20):
- Domain terms that MUST NOT be confused: e.g. "refund" ≠ "cancel event" (define 5 examples)

## 4. High-level stack + KNOWN EXTERNAL integrations
> Focus on BUSINESS, not technical detail (detail goes in project_profile.md).
- Payment: Stripe (Connect for creators), PayPal, Apple/Google Pay?
- Email: Resend, Sendgrid, SES, Postal?
- SMS/WhatsApp (if any): Twilio, Messagebird?
- Outbound analytics: GA4, Segment, PostHog?
- External CRMs (if any): HubSpot, Pipedrive?
- File/image storage: S3, Supabase storage, Cloudflare R2?
- Other SaaS: Slack webhooks, Linear/Jira tickets, etc.

## 5. NON-NEGOTIABLE business rules (hard invariants)
> Short list 5-10 items. NOT TECHNICAL. Business.
> E.g.: "Ticket CANNOT be scanned twice (even if 2 different people have a copy of the QR)". "Creator CANNOT withdraw funds 7 days before the event (anti-fraud policy)".
1.
2.
3.
4.
5.

## 6. Business risks + compliance (if applicable)
> E.g.: UK GDPR (PII), PCI DSS (payments), CCPA (California), LGPD (BR), Gambling Commission (if betting).
- Regulatory:
- Reputational (e.g. buyer data leak = K.O.):
- Operational (e.g. offline scanner working WITHOUT internet on event day = priority 1):

## 7. Roles + permissions (auth model)
> If multi-tenant / multiple roles, define here.
| Role | Can | CANNOT |
|---|---|---|
| Global Admin | Accesses everything, including billing | (no restrictions) |
| Creator | Manages THEIR events, tickets, payouts | Views OTHER creators' events |
| Door Staff | Only scans QR at assigned event | Views sales dashboard |
| Logged-in Buyer | Views THEIR orders, transfers ticket | Views others' orders |
| Anonymous | Searches event, buys without login | Accesses /admin/* |

## 8. Reference URLs (real product, docs, etc.)
> DO NOT put secrets here. Only known public or staging URLs.
- Public production environment: https://...
- Staging environment: https://...
- Product docs (Notion, Confluence, etc.): https://...
- Figma (if any): https://...
- Linear / ClickUp / Jira board: https://...
```

---

## 4. MANDATORY `roadmap.md` TEMPLATE (simple, no overengineering)

```markdown
# Roadmap — <slug>
> Updated at: <ISO8601>

## Confirmed Epics (next 3 months)
> Each epic = 1 line. Epic level (not task level — tasks stay in project tracker).
- E1: Refund automation (FLO-513 onwards) — buyer can request refund, creator approves/rejects, executes via Stripe
- E2: P2P ticket transfer between users
- E3: Analytics for creators (sold per day, attendance rate, scan rate)

## Planned Epics (3-6 months)
- E4: Waitlist for sold-out events
- E5: Multi-tenant organisations (multiple creators in same company account)

## Idea Backlog (>6 months, unvalidated hypotheses)
- B1: Native mobile app (currently PWA scanner)
- B2: White-label for large promoters
- B3: Facebook Eventbrite import integration

## FEATURES EXPLICITLY OUT OF SCOPE (not free, a decision)
> IMPORTANT so che doesn't propose "obvious" features product already decided against.
- ❌ We will not build a multi-platform aggregator marketplace (only our tickets)
- ❌ We will not support in-person POS sales (100% online QR check-in focus)
- ❌ We will not offer physical ticket printing services (client prints or uses QR)
```

---

## 5. SKILL EXECUTION MODES

### Mode A — `--show` (read + summary)
When the user only wants to review, not edit.
Returns a structured summary in English:
```
[che-onboarding] 📄 Current Registry — <slug>
  ├─ Product: <name> · <1-sentence pitch>
  ├─ 3 Personas: P1 (Creator) · P2 (Buyer) · P3 (Staff)
  ├─ Hard invariants: 5 rules (list 1st word each: QR-anti-fraud, split-payout, 7-day-payout, offline-scan, max-1-scan)
  ├─ External integrations: Stripe Connect · Resend · Supabase Storage
  ├─ Roadmap: 3 confirmed epics (E1 refund, E2 transfer, E3 analytics)
  ├─ Manual architectural decisions: (not filled — 0 ADRs registered)
  └─ Out of scope: 3 items (no marketplace, no physical POS, no physical printing)
```

### Mode B — default (interactive fill / update)
1. Loads contract helpers, confirms PROJECT_DIR exists.
2. **READS existing product_context.md, architecture.md, roadmap.md** (if they exist — does not overwrite without asking).
3. Asks the user **8 structured questions** (one per product_context template section).
4. Requests confirmation for each item (Not "all good?" — but "§3 Domain keywords: are they correct or do you want to edit?").
5. **Overwrites only the sections confirmed by the user.**
6. Does the same for roadmap.md (confirmed epics, planned, backlog, out of scope).
7. Updates the MANUAL part of architecture.md (asks if user wants to add ADRs, text C4 diagrams).
8. **Appends 1 audit line to registry.jsonl:**
   ```json
   {"ts":"ISO8601","event":"PROJECT_KNOWLEDGE_UPDATE","project_slug":"...","data":{"updated_sections":["product_context.1","roadmap.E1"]}}
   ```

### Mode C — `--bootstrap` (1st time, fastest mode)
Does not ask questions. Creates the 3 files (product_context, manual architecture, roadmap) **EMPTY with the standard `[PENDING]` template** in all sections. Returns the list of sections for the user to fill via chat or manually.

---

## 6. READING CONTRACT: HOW OTHER SKILLS USE THIS

**OBLIGATION OF OTHER SKILLS (engineering-contracts §X):**
Before ANY `che-spec` generates a feature SPEC, che MUST:
1. Run `eval "$(che compute_paths WORKTREE_ROOT SESSION_ID)"` + resolve `$CHE_PROJECT_DIR`
2. If `product_context.md` exists → **read sections §2 (personas) + §5 (hard invariants) + §8 (out of scope)**.
3. Inject at the beginning of the SPEC:
   ```
   > Project Context absorbed from Level 1.5 registry:
   > - Personas: P1 Creator, P2 Buyer, P3 Staff (see product_context §2)
   > - Business hard invariants: 5 rules (§5)
   > - Out of scope: no marketplace, no POS, no printing (see last §roadmap)
   ```

If `product_context.md` DOES NOT exist in a project that already has worktrees and commits → WARN at the beginning of the SPEC:
```
> ⚠️ [project knowledge not filled] — run /che-onboarding to reduce product ambiguity.
```

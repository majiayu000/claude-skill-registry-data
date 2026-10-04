---
name: data-persistence
description: "Fires on any operation that reads or writes deal, company, contact, call note, or task data. Provides: file schemas, write protocol (entity + index + cross-references + ops.log), account name resolution (fuzzy matching), read-time validation, duplicate detection rules. Output contract: every data write follows the standard protocol and produces a FILES UPDATED block."
user-invocable: false
---

# Data Persistence Skill

## Purpose

Central reference for all data operations. The primary data layer is local workspace files with structured headers. Follow the write protocol in the Project CLAUDE.md (`.claude/CLAUDE.md`).

If a connected database service is available, data can also be synced to structured databases using the schemas below. Local files are always canonical.

## When Referenced

- **Any interaction reading or writing data** — local file operations, schema validation, account resolution
- **Deep personalization sessions** — creates local data structure and optionally syncs to connected databases
- **Adding accounts and deals** — record creation in local files
- **Processing calls** — writes to multiple local files simultaneously (call note, deal, contacts, tasks, index)

## Core Framework

### Database Schemas

#### Companies (13 fields)
| # | Field | Type | Options/Notes |
|---|-------|------|---------------|
| 1 | Company Name | Title | — |
| 2 | Territory Status | Select | Active, Prospect, Inactive, Former Customer |
| 3 | Industry | Select | Options populated during deep personalization per user's market |
| 4 | Account Size | Select | Enterprise, Mid-Market, SMB |
| 5 | Hell Yes/Hell No | Select | Hell Yes, Evaluating, Hell No |
| 6 | Primary Contact | Relation | →Contacts |
| 7 | Tech Stack | Multi-select | Populated per account |
| 8 | Current Products | Multi-select | User's product line, set during deep personalization |
| 9 | Annual Revenue | Number | — |
| 10 | Last Activity | Date | Auto-updated on any interaction |
| 11 | Notes | Text | Research briefs, general context |
| 12 | Website | URL | — |
| 13 | Evidence Sources | List | Provenance: what sources informed key fields (grade, source, date per field). See Project CLAUDE.md for format. |

#### Contacts (9 fields)
| # | Field | Type | Options/Notes |
|---|-------|------|---------------|
| 1 | Name | Title | — |
| 2 | Company | Relation | →Companies |
| 3 | Title | Text | Job title |
| 4 | MEDDPICC Role | Multi-select | Champion, Economic Buyer, Technical Buyer, Influencer, Blocker, User |
| 5 | Email | Email | — |
| 6 | LinkedIn | URL | — |
| 7 | Sentiment | Select | Champion, Supportive, Neutral, Skeptical, Blocker |
| 8 | Last Contacted | Date | — |
| 9 | Notes | Text | — |

#### Deals (22 fields)
| # | Field | Type | Options/Notes |
|---|-------|------|---------------|
| 1 | Deal Name | Title | — |
| 2 | Company | Relation | →Companies |
| 3 | Contacts | Relation | →Contacts (linked during add deal) |
| 4 | Stage | Select | Prospecting, Discovery, Qualification, Proposal, Negotiation, Closed Won, Closed Lost |
| 5 | Deal Value | Number | — |
| 6 | Close Date | Date | — |
| 7 | Forecast Category | Select | Commit, Best Case, Pipeline, Omitted |
| 8 | Primary Competitor | Select | Options populated during deep personalization Phase 3 |
| 9 | Next Step | Text | — |
| 10 | Deal Risk | Select | High, Medium, Low |
| 11 | MEDDPICC Confidence | Select | High, Medium, Low |
| 12 | M-Metrics | Select | Red, Yellow, Green |
| 13 | E-Economic Buyer | Select | Red, Yellow, Green |
| 14 | D-Decision Criteria | Select | Red, Yellow, Green |
| 15 | D-Decision Process | Select | Red, Yellow, Green |
| 16 | P-Paper Process | Select | Red, Yellow, Green |
| 17 | I-Identify Pain | Select | Red, Yellow, Green |
| 18 | C-Champion | Select | Red, Yellow, Green |
| 19 | C-Competition | Select | Red, Yellow, Green |
| 20 | Created Date | Date | Set on creation |
| 21 | Last Activity | Date | Auto-updated on any interaction |
| 22 | Notes | Text | — |

**Default Stage Probability Weights** (used by forecast update):
| Stage | Default Probability |
|-------|-------------------|
| Prospecting | 10% |
| Discovery | 20% |
| Qualification | 40% |
| Proposal | 60% |
| Negotiation | 80% |
| Closed Won | 100% |
| Closed Lost | 0% |

These are defaults. Deep personalization asks if the user's org uses different stage names or probabilities, and stores customized values in {{DEAL_STAGES}}.

#### Tasks (9 fields)
| # | Field | Type | Options/Notes |
|---|-------|------|---------------|
| 1 | Task | Title | — |
| 2 | Company | Relation | →Companies |
| 3 | Deal | Relation | →Deals |
| 4 | Owner | Select | AE, Prospect, Internal |
| 5 | Priority | Select | High, Medium, Low |
| 6 | Due Date | Date | — |
| 7 | Status | Select | Not Started, In Progress, Done, Blocked |
| 8 | Source | Select | Call, Strategy, Manual |
| 9 | Notes | Text | — |

#### Call Notes (10 fields)
| # | Field | Type | Options/Notes |
|---|-------|------|---------------|
| 1 | Call Title | Title | — |
| 2 | Company | Relation | →Companies |
| 3 | Deal | Relation | →Deals |
| 4 | Call Date | Date | — |
| 5 | Summary | Text | AI-generated summary |
| 6 | Action Items | Text | Extracted tasks (also written to Tasks DB) |
| 7 | Risk Level | Select | High, Medium, Low |
| 8 | Competitive Intel | Text | Competitor mentions and analysis |
| 9 | Coaching Score | Number | 1-5 (average of 5 coaching dimensions) |
| 10 | MEDDPICC Changes | Text | Elements that changed R/Y/G this call |

#### LinkedIn Posts (8 fields)
| # | Field | Type | Options/Notes |
|---|-------|------|---------------|
| 1 | Post Title | Title | — |
| 2 | Post Type | Select | Personal, Business, Educational |
| 3 | Status | Select | Idea, Draft, Ready, Scheduled, Posted |
| 4 | Scheduled/Posted Date | Date | — |
| 5 | Hook | Text | First 2 lines (scroll-stopper) |
| 6 | Content | Text | Full post body |
| 7 | Related Company | Relation | →Companies |
| 8 | Notes | Text | — |

**Total: 6 databases, 70 fields.**

### Account Resolution Logic

When a user references a company by name, resolve using this priority order:

1. **Exact match** on Company Name field (case-insensitive)
2. **Starts-with match** if no exact match (e.g., "Acme" matches "Acme Corporation")
3. **Contains match** as fallback (e.g., "Acme" matches "The Acme Group")
4. **Multiple matches** → ask user to clarify: "I found multiple matches: [list]. Which one?"
5. **No match** → "I don't have [Company] in my records. Want me to add [Company] to your pipeline?"

When resolving for deal-specific capabilities (deal strategy, competitive analysis, meeting prep):
- After finding the company, look for active deals (Stage ≠ Closed Won, Closed Lost)
- If multiple active deals → ask: "You have [X] active deals at [Company]: [list]. Which one?"
- If one active deal → use it automatically
- If no active deals → "No active deal at [Company]. Want to add a deal for [Company]?"

### Read/Write Patterns by Command

| Capability | Reads | Writes |
|------------|-------|--------|
| Morning Briefing | Tasks (due/overdue), Deals (needing attention) | — |
| Evening Wrap | Tasks (today's), Deals (movement) | — |
| Weekly Summary | Deals (all active), Tasks (week), Call Notes (week) | — |
| Call Processing | Companies, Contacts, Deals, Call Notes (history) | Call Notes (new), Tasks (new), Deals (MEDDPICC update), Companies (Last Activity) |
| Meeting Prep | Companies, Contacts, Deals, Call Notes (recent), Tasks | — |
| Deal Strategy | Companies, Deals, Contacts, Call Notes, Tasks | — |
| Competitive Analysis | Companies, Deals, Call Notes, Contacts | — |
| Business Case | Companies, Deals, Call Notes | — |
| Pipeline Review | Deals (all active), Companies | — |
| Whitespace Analysis | Companies, Deals | — |
| Forecast Update | Deals (by period) | — |
| Account Research | Companies (if exists), Deals, Call Notes | Companies (Notes, Tech Stack, Industry, Account Size) |
| Outreach | Companies, Contacts, Deals | — |
| Contextual Email | Companies, Contacts, Deals, Call Notes | — |
| LinkedIn Post | LinkedIn Posts (recent) | LinkedIn Posts (new draft, on confirm) |
| Presentation | Companies, Deals, Contacts, Call Notes | — |
| Add Company | Companies (duplicate check) | Companies (new record) |
| Add Deal | Companies, Contacts, Deals (duplicate check) | Deals (new record) |
| Call Coaching | Call Notes, Deals | — |
| **Passive capture (all conversations)** | Trail (recent), entity files | Trail (new entry), entity notes (updated). See CLAUDE.md Section 10.5. |

### Intelligence Trail

Trail files (`data/trail/`) are written passively during substantive conversations. They capture: what was discussed, which entities were referenced, what decisions were made, and what intelligence was filed. One file per conversation per day. The trail is the safety net that catches intelligence the structured commands miss.

Use the Section 10.5 capture decision policy before writing: `NOOP`, `TRAIL_ONLY`, `TRAIL_PLUS_ENTITY_UPDATE`, or `ASK_USER`. Default to trail-only when uncertain. Entity notes are updated only for explicit, high-confidence facts tied to existing records; casual or inferred remarks stay in the trail.

### Write Failure Handling

When a database write fails:

1. **Never silently drop data.** Always inform the user what failed to save.
2. **Present the data that would have been written** in a formatted block the user can manually enter.
3. **Diagnose the likely cause:**
   - "Database not found" → Database ID may be wrong. Suggest: "Check that your databases are set up. Try a deep personalization session to reconfigure."
   - "Permission denied" → API key may lack write access. Suggest: "Check your integration permissions — it needs read AND write access."
   - "Validation error" → Field type mismatch. Suggest: "The [field] in your [database] may have different options than expected."
   - "Rate limited" → Too many requests. Suggest: "The service is rate-limiting requests. I'll try again in a moment."
4. **Retry once** on transient errors (rate limit, timeout). If retry fails, fall back to manual mode.
5. **Log the failure context** so self-audit can check for patterns.

### V4 Persistence Architecture

SalesSidekick uses a three-tier persistence model. No external services required for the core experience.

| Tier | Where | What lives here | When it's read | API calls |
|------|-------|----------------|----------------|-----------|
| **Slow lane** | Global CLAUDE.md (`/mnt/.claude/CLAUDE.md`) | Stable identity and operating guardrails: name, company, product, ICP, competitors, selling style, quality rules, cascading context rules, and memory/setup protection. Written automatically during onboarding from `templates/global-identity.md` within `<!-- SALESSIDEKICK-IDENTITY-START/END -->` markers. | Automatically by Cowork before any plugin fires | Zero |
| **Fast lane** | Local workspace files (`data/` in Project folder) | All operational data: deals, contacts, companies, call notes, tasks. Stored as structured markdown with YAML frontmatter. `data/index.md` is the flattened read cache. | On demand when capabilities need data | Zero |
| **Optional** | Connected databases (if available) | Structured database views of the same data. Cross-device access. | Only when user explicitly requests database features | Per operation |

**Data operations use the write protocol defined in the Project CLAUDE.md** (`.claude/CLAUDE.md` in the workspace). The full schemas, cross-reference rules, ops.log format, and write-verification step are there.

**Local files are always canonical.** If local files and connected databases disagree, local files win.

**Write verification:** Every write operation completes with a read-back verification step. After writing the entity file, updating the index, updating cross-references, and logging to ops.log, the system reads back the index row for the primary entity and confirms key fields match. If they don't match, the index update is retried once. If retry fails, VERIFY_FAIL is logged and the user is informed. This catches partial writes immediately.

### Database Creation (optional — deep personalization Phase 6)

Only if the user has a database connector and wants structured views:

1. Search by name before creating — never duplicate
2. Create in dependency order: Companies → Contacts → Deals → Tasks → Call Notes → LinkedIn Posts
3. Set up cross-relations after all databases exist
4. Store database IDs in the Project CLAUDE.md
5. Verify by reading back each database

### Structured Database Schemas (for optional database sync)

The schemas below define the structured database format. They are used ONLY when a database connector is active and the user has opted into database sync. The primary data model uses the local file schemas defined in the Project CLAUDE.md template.

## Personalization Notes

- Select field options for Industry, Primary Competitor, and Current Products are customized during deep personalization
- Stage names and probability weights may be customized
- Account resolution logic is universal — no personalization needed
- Identity and personalization variables live in Global CLAUDE.md — not in external databases

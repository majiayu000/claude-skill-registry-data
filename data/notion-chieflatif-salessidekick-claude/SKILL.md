---
name: notion
description: Central reference for all Notion database schemas, read/write patterns, account resolution logic, and write failure handling
tier: 1 (universal)
auto-fire: Any database read/write operation
user-invocable: false
---

# Notion — Database Operations Skill

## Purpose

Central reference for all Notion database operations. Contains the complete schemas for all 6 databases (70 fields total), read/write patterns per command, account resolution logic, and write failure handling. This is the single source of truth for how SalesSidekick interacts with Notion.

## When Referenced

- **Every command that reads from Notion** — schema lookup, field validation
- **Every command that writes to Notion** — field mapping, write patterns
- **/setup** — creates all 6 databases with these schemas
- **/add-company, /add-deal** — record creation patterns
- **/closeout** — writes to 4 databases simultaneously

## Core Framework

### Database Schemas

#### Companies (12 fields)
| # | Field | Type | Options/Notes |
|---|-------|------|---------------|
| 1 | Company Name | Title | — |
| 2 | Territory Status | Select | Active, Prospect, Inactive, Former Customer |
| 3 | Industry | Select | Options populated during /setup per user's market |
| 4 | Account Size | Select | Enterprise, Mid-Market, SMB |
| 5 | Hell Yes/Hell No | Select | Hell Yes, Evaluating, Hell No |
| 6 | Primary Contact | Relation | →Contacts |
| 7 | Tech Stack | Multi-select | Populated per account |
| 8 | Current Products | Multi-select | User's product line, set during /setup |
| 9 | Annual Revenue | Number | — |
| 10 | Last Activity | Date | Auto-updated on any interaction |
| 11 | Notes | Text | Research briefs, general context |
| 12 | Website | URL | — |

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
| 3 | Contacts | Relation | →Contacts (linked during /add-deal) |
| 4 | Stage | Select | Prospecting, Discovery, Qualification, Proposal, Negotiation, Closed Won, Closed Lost |
| 5 | Deal Value | Number | — |
| 6 | Close Date | Date | — |
| 7 | Forecast Category | Select | Commit, Best Case, Pipeline, Omitted |
| 8 | Primary Competitor | Select | Options populated during /setup Phase 3 |
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

**Default Stage Probability Weights** (used by /forecast-update):
| Stage | Default Probability |
|-------|-------------------|
| Prospecting | 10% |
| Discovery | 20% |
| Qualification | 40% |
| Proposal | 60% |
| Negotiation | 80% |
| Closed Won | 100% |
| Closed Lost | 0% |

These are defaults. /setup asks if the user's org uses different stage names or probabilities, and stores customized values in {{DEAL_STAGES}}.

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
5. **No match** → "I don't have [Company] in Notion. Want me to run `/add-company [Company]`?"

When resolving for deal-specific commands (/strategy, /battle, /prep):
- After finding the company, look for active deals (Stage ≠ Closed Won, Closed Lost)
- If multiple active deals → ask: "You have [X] active deals at [Company]: [list]. Which one?"
- If one active deal → use it automatically
- If no active deals → "No active deal at [Company]. Want to run `/add-deal [Company]`?"

### Read/Write Patterns by Command

| Command | Reads | Writes |
|---------|-------|--------|
| /today | Tasks (due/overdue), Deals (needing attention) | — |
| /end-of-day | Tasks (today's), Deals (movement) | — |
| /weekly | Deals (all active), Tasks (week), Call Notes (week) | — |
| /closeout | Companies, Contacts, Deals, Call Notes (history) | Call Notes (new), Tasks (new), Deals (MEDDPICC update), Companies (Last Activity) |
| /prep | Companies, Contacts, Deals, Call Notes (recent), Tasks | — |
| /strategy | Companies, Deals, Contacts, Call Notes, Tasks | — |
| /battle | Companies, Deals, Call Notes, Contacts | — |
| /pov | Companies, Deals, Call Notes | — |
| /pipeline | Deals (all active), Companies | — |
| /whitespace | Companies, Deals | — |
| /forecast-update | Deals (by period) | — |
| /research | Companies (if exists), Deals, Call Notes | Companies (Notes, Tech Stack, Industry, Account Size) |
| /outreach | Companies, Contacts, Deals | — |
| /email | Companies, Contacts, Deals, Call Notes | — |
| /draft-post | LinkedIn Posts (recent) | LinkedIn Posts (new draft, on confirm) |
| /deck | Companies, Deals, Contacts, Call Notes | — |
| /add-company | Companies (duplicate check) | Companies (new record) |
| /add-deal | Companies, Contacts, Deals (duplicate check) | Deals (new record) |
| /coaching | Call Notes, Deals | — |

### Write Failure Handling

When a Notion write fails:

1. **Never silently drop data.** Always inform the user what failed to save.
2. **Present the data that would have been written** in a formatted block the user can manually enter.
3. **Diagnose the likely cause:**
   - "Database not found" → Database ID may be wrong. Suggest: "Check that your Notion databases are set up. Run `/setup` to reconfigure."
   - "Permission denied" → API key may lack write access. Suggest: "Check your Notion integration permissions — it needs read AND write access to the databases."
   - "Validation error" → Field type mismatch. Suggest: "The [field] in your [database] may have different options than expected. Check the field configuration in Notion."
   - "Rate limited" → Too many requests. Suggest: "Notion is rate-limiting requests. I'll try again in a moment."
4. **Retry once** on transient errors (rate limit, timeout). If retry fails, fall back to manual mode.
5. **Log the failure context** so /audit can check for patterns.

### Database Creation (used by /setup Phase 6)

When creating databases during /setup:
1. Create databases in dependency order: Companies → Contacts → Deals → Tasks → Call Notes → LinkedIn Posts
2. Companies and Contacts must exist before Deals (for relations)
3. Set up all relations after databases exist
4. Populate Select field options with defaults listed above
5. Store resulting database IDs in CLAUDE.md Section 10 ({{NOTION_*_DB_ID}} variables)
6. Verify creation by reading back each database

## Personalization Notes

- Select field options for Industry, Primary Competitor, and Current Products are customized during /setup
- Stage names and probability weights may be customized (stored in {{DEAL_STAGES}})
- Database IDs are populated during /setup and stored as Tier 2 variables
- Account resolution logic is universal — no personalization needed

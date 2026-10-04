---
name: frontline-internals
description: >
    Internal workings of the Frontline platform: how the base CRM objects
    (Company, Deals, People, Tickets) relate to each other, how activity
    synchronization works automatically for People and Companies, and how
    periodic consolidation keeps CRM records up to date. Read this skill
    before designing new entities or fields to avoid duplicating behavior
    that the system already handles automatically.
allowed-tools: Bash(frontline:*)
---

# Frontline Internal System Mechanics

Understanding how Frontline works internally is critical **before** designing
new objects, fields, or relations. Many common CRM needs are already handled
automatically by the platform.

---

## 1. Base Objects and Their Relationships

Frontline ships with four core objects that form the foundation of every
account. They are pre-provisioned and cannot be deleted.

```
companies   — Organizations / accounts
people      — Individual contacts
deals       — Sales opportunities
tickets     — Support or service requests
```

> **Full field catalog, automations, and deduplication rules:**
> See the **`crm-objects`** skill for the complete reference on each object's
> fields, background hooks, auto-creation logic, and profile/summary UI behavior.

### Built-in Relations

```
People  →  Companies   (many-to-many)
Deals   →  People      (many-to-many)
Deals   →  Company     (many-to-one)
Tickets →  People      (many-to-many)
Tickets →  Company     (many-to-one)
```

> **Before creating a new entity**, check whether it fits naturally as a
> custom object linked to one of these four. Most vertical use cases (leads,
> vendors, partners, subscribers) are best modeled as extensions of People or
> Companies rather than standalone objects.

---

## 2. Automatic Activity Synchronization

When an account grants the required permissions, Frontline automatically
captures and attaches **activity records** to People and Company objects.
You do **not** need to create these manually or build pipelines to collect them.

### Activity Types (peopleActivity / companyActivity)

Each activity record has a `type` field that identifies the source:

| Type            | Description                                                  |
| --------------- | ------------------------------------------------------------ |
| `email`         | Inbound or outbound emails linked to the contact or company  |
| `conversation`  | Chat/messaging interactions (Slack, etc.)                    |
| _(more coming)_ | The system is designed to receive additional types over time |

Activity records are stored as `peopleActivity` (for People) or
`companyActivity` (for Companies) and are surfaced automatically in the
record's activity feed.

### What this means in practice

- **You do not need an "Emails" table.** Emails are synced automatically.
- **You do not need a "Conversations" table.** Those are synced automatically.
- To **read** this synced history (emails, conversations, WhatsApp, audit) for a
  record, use `frontline object timeline list <object> <row-id>` — it is
  permission-redacted server-side. Don't build a parallel data structure.
  (`frontline object activity` only covers **manually-logged** notes/calls.)

> **Before building a new data pipeline or table to capture interactions**,
> verify whether that interaction type is already handled by the activity
> sync. Adding a duplicate table leads to split history and inconsistent data.

---

## 3. Periodic Consolidation

Beyond real-time activity sync, Frontline runs **periodic consolidation jobs**
that aggregate and summarize information at the People and Company level.

### What gets consolidated

- **Last Interaction** — The most recent interaction date across all activity
  types is computed and written to the People record. For Companies, this is
  further propagated from all linked People: the Company's `Last Interaction`
  always reflects the freshest interaction across any of its contacts.
- **Profile Insights (Structured AI Assessments)** — The system evaluates the
  state of the relationship and record data.
    - **For People**: Sentiment (very_positive to very_negative), Engagement
      Level (highly_engaged to at_risk), key relationship description, identified
      Risks (e.g., churn signals), and Opportunities.
    - **For Companies**: Connection Strength (Strong/Medium/Weak), Key People
      discovery (stakeholders), and Company Mission extraction.
- **Key Topics** — A list of the top 3-5 recurring themes in interactions
  (e.g., "Pricing", "Onboarding", "Product Feedback").
- **Summaries** — Concise, professional overviews of the person or company
  based on all recent context.

### Implications for custom fields

- Do **not** build a custom "last email date" or "last activity date" field
  and try to keep it in sync manually via hooks or external automation.
  The system already maintains `Last Interaction` for this purpose.
- If you need a consolidation that does not yet exist, raise it as a
  platform request rather than building a workaround.

---

## 4. Design Checklist — Before Adding New Entities or Fields

Use this checklist whenever you are about to create a new object, table, or field:

1. **Is this already a base object?**
   Check `frontline object list` — `companies`, `people`,
   `deals`, `tickets` may already fit.

2. **Is this interaction data?**
   If the new entity stores emails, messages, calls, or any user-to-contact
   interaction, check whether the activity sync already covers it before
   building a custom table.

3. **Is this a summary or aggregate?**
   If the field would need to be recomputed based on interactions
   (e.g., "last contacted", "interaction count"), check if periodic
   consolidation already provides it via built-in fields.

4. **Does a relation already exist?**
   Run `frontline object schema <obj>` to inspect existing relations before
   creating a new one. Duplicate relations cause inconsistent data.

5. **Only then — extend or create.**
   If none of the above covers the need, proceed to add a custom field
   (see `crm-setup` skill) or create a new object/table.

---

## 5. Memories & Intelligent Consolidation

Beyond raw activity sync, Frontline uses AI to distill important facts and
structured data about People and Companies. This process is called
**Consolidation**.

### What are "Memories"?

Memories are persistent, AI-distilled facts about a person or company that
provide context for future interactions. Unlike activity logs, memories are
long-lived and categorized.

**Categories include:**

- `DECISION`: Specific decisions made (e.g., "Decided to postpone the project until Q3").
- `AGREEMENT`: Agreed terms or commitments (e.g., "Agreed to a 20% discount for the first year").
- `PREFERENCE`: Personal or professional preferences (e.g., "Prefers morning meetings").
- `RISK`: Potential issues or red flags (e.g., "Customer is frustrated with current response times").
- `OTHER`: General facts or context (e.g., "Is a fan of the Golden State Warriors").

> **Example**: Instead of searching through 50 emails to find a contact's
> preferred communication channel, the system creates a `PREFERENCE` memory:
> _"Prefers being contacted via WhatsApp after 6pm."_

### Structured Data Extracted

During periodic consolidation, the LLM extracts and updates specific data
points to keep record profiles fresh:

| Object      | Data Point           | Description / Examples                                     |
| :---------- | :------------------- | :--------------------------------------------------------- |
| **People**  | **Profile Insights** | Sentiment, Engagement, Risks, Opportunities, Key Topics    |
|             | **Summary**          | Professional overview of persona and status                |
| **Company** | **Profile Insights** | Connection Strength, Key Stakeholders, Mission             |
|             | **Firmographics**    | Revenue, Employee count, Headquarters (from external sync) |

### How this data is used

1. **Intelligent Feed**: Memories and summaries are displayed in the CRM feed to
   give users instant context without reading threads.
2. **AI Reasoning (RAG)**: When an AI agent (or you, the developer) queries the
   system, it retrieves these memories to generate responses that are
   contextually aware.
3. **Automated Triggers**: Consolidated fields (like `Last Interaction` or
   `Connection Strength`) can trigger automated workflows.

---

## 6. Summary

```
┌─────────────────────────────────────────────────────────────────┐
│ WHAT FRONTLINE DOES AUTOMATICALLY                               │
│                                                                 │
│  • Syncs emails/conversations → people/company Activity        │
│  • Consolidates Last Interaction & Connection Strength        │
│                                                                 │
│ INTELLIGENT CONSOLIDATION                                       │
│  • Distills "Memories" (Decisions, Preferences, Risks, etc.)   │
│  • Extracts Structured Data (Summary, Insights, Firmographics) │
│  • Updates Vector Store for context-aware AI reasoning         │
│                                                                 │
│ BASE OBJECTS                                                    │
│  companies  people  deals  tickets         │
└─────────────────────────────────────────────────────────────────┘
```

---

## See also

- Full reference: <https://docs.getfrontline.ai/docs> (concepts) and <https://docs.getfrontline.ai/cli> (command reference).
- App UI walkthroughs (channels, billing, settings): <https://help.getfrontline.ai>.

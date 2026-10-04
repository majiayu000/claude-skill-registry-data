---
name: crm-objects
description: >
    Complete reference for Frontline's four built-in CRM objects: People, Companies, Deals, and Tickets.
    Covers their pre-defined fields (including read-only and programmatic ones), built-in relations,
    background automations (auto-creation, enrichment, RAG sync), profile/summary UI behavior,
    and deduplication rules. Read this before adding fields or creating records on these objects —
    many behaviors run automatically and must not be duplicated manually.
allowed-tools: Bash(frontline:*)
---

# Built-in CRM Objects Reference

Frontline ships with **four pre-provisioned objects** that form the foundation of every account.
They cannot be deleted, but they can be extended with custom fields (`extensible: true`).

```
people     — Individual contacts
companies  — Organizations / accounts
deals      — Sales opportunities (Kanban pipeline)
tickets    — Support / service requests (Kanban pipeline)
```

> **Important:** Many behaviors on these objects run automatically in the background.
> Before adding a field or building a workflow, check this reference to avoid duplicating
> something the platform already handles.

> **Terminology — standard vs custom vs system fields**
>
> - **Standard fields** (a.k.a. predefined/built-in): user-visible fields that ship with the
>   object — Name, Email, Stage, etc. Listed under each object's "Standard Fields" below.
> - **Custom fields**: fields you add yourself with `field create`.
> - **System / hidden fields**: internal columns the platform manages (e.g. Normalized Phone
>   Number, Is Identified). These are excluded from `field list` / the public API.
>
> "Standard" and "custom" are the two object/field categories you work with via the API;
> "system" refers to the hidden internal columns, not the standard built-ins.

---

## 1. People

**Name:** `people` · **Display:** People · **Noun:** Person
**Icon:** `users` 🔵 · `custom: false, extensible: true, isContactTable: true`

> ⚠️ **Do not manually create or link a Company when creating a Person with an email.**
>
> When a Person is created or updated with an email on a **non-generic domain** (anything other than gmail, outlook, hotmail, yahoo, icloud, etc.), the platform automatically:
>
> 1. Searches existing Companies for one whose `Domain` matches the email's domain.
> 2. If found → links the Person to that Company.
> 3. If not found → creates a new Company (with Logo.dev enrichment: name, description, socials, logo) and links it.
>
> So when a user asks _"create John Doe at Acme"_ or _"create a Person with email john@acme.com and link them to Acme"_:
>
> - **Just `record create people`** with the email. Stop there.
> - **Do NOT** call `record create` on `companies` first.
> - **Do NOT** call `relation link` afterwards — the link is already in place.
>
> **When you _do_ need to intervene** (only these cases):
>
> | Situation                                                                                                                                     | What to do                                                                                                                                                                      |
> | --------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
> | Email domain is generic (gmail, outlook, etc.)                                                                                                | Auto-link is skipped. Create Person, then `relation link` manually if needed.                                                                                                   |
> | Person has no email                                                                                                                           | Auto-link can't run. Create Person, then `relation link` manually if needed.                                                                                                    |
> | User specifies a Company name that may **differ** from the auto-linked one (e.g. email `john@acme.com` but user says "link to Acme Holdings") | 1. Create Person. 2. Read the `Company` relation that got auto-set. 3. If the linked Company isn't what the user meant, `relation unlink` it and `relation link` the right one. |
>
> Gate: `account.companyAutoLinkEnabled` (default `true`). If a customer reports the auto-link is not firing, check this flag in their account settings.

### Standard Fields (user-visible)

| Field               | Type                  | Notes                                                                             |
| ------------------- | --------------------- | --------------------------------------------------------------------------------- |
| `Name`              | string (composed)     | **Read-only.** Auto-computed from First Name + Last Name. Required. Title column. |
| `First Name`        | string                | Editable component of Name                                                        |
| `Last Name`         | string                | Editable component of Name                                                        |
| `Email`             | string (email)        | **Unique.** Primary deduplication key                                             |
| `Phone Number`      | string (phone_number) | Secondary deduplication key                                                       |
| `Address`           | string (text)         |                                                                                   |
| `Role`              | string                | Job title / role                                                                  |
| `Website`           | string (url)          |                                                                                   |
| `Linkedin`          | string (url)          | Shows LinkedIn icon                                                               |
| `Location`          | string                |                                                                                   |
| `Language`          | string                |                                                                                   |
| `Relationship Type` | select (singleSelect) | Options: Lead, Customer, Churned, Vendor, Partner, Investor, Other, Unknown       |
| `Users`             | prismaRelation        | Links to Frontline account users (assignees)                                      |
| `Last Interaction`  | date (timeDelta)      | **Read-only, programmatic.** Shows relative time since last interaction           |
| `Company`           | relation → companies  | Single relation to a Company                                                      |

### System / Hidden Fields (internal use, not shown in UI)

| Field                     | Type    | Notes                                                                                                                                               |
| ------------------------- | ------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Normalized Phone Number` | string  | E.164-normalized version of Phone Number. Auto-set on save.                                                                                         |
| `WhatsApp Id`             | number  | Internal WhatsApp contact ID                                                                                                                        |
| `Instagram Id`            | string  | Internal Instagram contact ID                                                                                                                       |
| `Instagram Handle`        | string  | Instagram handle                                                                                                                                    |
| `Messenger Id`            | string  | Internal Messenger contact ID                                                                                                                       |
| `Wpp Conversation Id`     | string  | Active WhatsApp conversation ID                                                                                                                     |
| `Wpp Last Interaction`    | string  | Last WhatsApp interaction timestamp                                                                                                                 |
| `Is Identified`           | boolean | `true` = known contact; `false` = anonymous. **Queries always filter to `Is Identified = true`** — anonymous records are invisible to normal reads. |
| `Avatar`                  | avatar  | Profile picture. Auto-cleared when a contact is identified (system re-fetches).                                                                     |
| `Created By User`         | number  | User ID who created the record                                                                                                                      |
| `Created By Assistant`    | string  | Assistant ID if created by an AI agent                                                                                                              |

### Deduplication

People are deduplicated by **Email** (primary) and **Phone Number** (secondary).
Creating a record with an existing email/phone merges or rejects the duplicate instead of inserting.

> **Uniqueness is enforced object-wide — across record types.** If People has both a "Lead" and a
> "Person"/"Customer" record type, the same Email/Phone still can't exist twice. Record types are
> field groupings over **one** object, not separate storage. So: search before creating (update if
> it already exists), and **converting** a lead = changing that record's record type, NOT creating a
> new record. See the `record-type-management` skill.

### Identification Logic

- **Created by a user** (UI or CLI with user auth) → `Is Identified = true` automatically.
- **Created by system/background** (webhooks, flows) → `Is Identified = true` only if identification
  data (email, name, phone) is present; otherwise starts as `false` (anonymous).
- When an anonymous record gains an email + name, it is **promoted to identified** and its avatar is reset.

### Background Automations on People

These fire automatically — never replicate them manually:

| Trigger    | What happens                                                                                                                                 |
| ---------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| **Create** | Phone number is E.164-normalized into `Normalized Phone Number`                                                                              |
| **Create** | `Full Name` is computed from First + Last (or falls back to phone/email if name is blank)                                                    |
| **Create** | Record is synced to the **Vector Store (RAG)** for AI context retrieval                                                                      |
| **Create** | A **PeopleProfile** row is created (holds memories and AI summary)                                                                           |
| **Create** | If email domain is non-generic (not gmail, etc.) and `companyAutoLinkEnabled`, the system **auto-links or auto-creates a Company** by domain |
| **Update** | If First/Last Name changes → `Name` is recomputed                                                                                            |
| **Update** | If Phone Number changes → `Normalized Phone Number` is recomputed                                                                            |
| **Update** | If Email, Phone, First Name, or Last Name changes → RAG re-sync                                                                              |
| **Update** | If Email changes → **Company link is re-evaluated** (may unlink old Company and link/create one for new domain)                              |
| **Update** | If Email or Phone changes → MaxContact link re-evaluated (for email/WhatsApp channel connections)                                            |
| **Update** | `Last Interaction` is propagated upward to any linked Company                                                                                |
| **Delete** | RAG documents for this record are cleaned up                                                                                                 |
| **Delete** | Conversation references are removed                                                                                                          |

> **Don't manually create a Company just to link a Person.** Set the person's business email and the
> auto-link/auto-create hook does it for you. Create a Company by hand only when there's no
> person/email to drive the link (e.g. tracking a company with no contact yet).

### Auto-Creation from Channels

People records are **auto-created** when a message arrives from an unknown contact, governed by `autoCreateContactsMode`:

| Mode                       | Behavior                                                        |
| -------------------------- | --------------------------------------------------------------- |
| `ALL_CONTACTS` _(default)_ | Auto-create a People record for every inbound contact           |
| `SELECTIVE`                | Create only if the contact has been seen before or is in a list |
| `NONE`                     | Never auto-create from channel events                           |

This applies to:

- **Email channels** (Gmail, Outlook): every inbound/outbound email sender can become a People record
- **WhatsApp channels**: every WhatsApp conversation participant can become a People record
- **Conversation flows**: when a flow captures `email` + `first/last name` variables, `findOrCreatePeople` is called — requires both email AND a name to create an identified record

### Profile / Summary UI

People records have a **Profile** panel shown alongside the standard fields.
This is separate from the normal field grid and includes:

- **AI Summary**: concise professional overview of the contact (auto-generated from interactions)
- **Memories**: up to 5 pinned + 5 most recent AI-distilled facts (deduplicated)
    - Categories: `DECISION`, `AGREEMENT`, `PREFERENCE`, `RISK`, `OTHER`
- **Profile Insights**: Sentiment, Engagement Level, Risks, Opportunities, Key Topics

> This is a differentiated UI surface — you cannot add custom fields here. It is driven by the
> background AI consolidation process, not by the standard field schema.

### Query Behavior Note

All People queries automatically add a hidden filter: `Is Identified = true`.
Anonymous records exist in the DB but are **never returned** by normal list/search operations.
This is a `preprocessQuery` hook that cannot be overridden from the CLI.

---

## 2. Companies

**Name:** `companies` · **Display:** Companies · **Noun:** Company
**Icon:** `building-2` 🩷 · `custom: false, extensible: true`

### Fields

| Field                 | Type                             | Notes                                                                                              |
| --------------------- | -------------------------------- | -------------------------------------------------------------------------------------------------- |
| `Name`                | string                           | Required, **unique**. Title column. Deduplication key.                                             |
| `Description`         | string (text)                    | Extended field (shown in detail panel)                                                             |
| `Domain`              | string                           | Unique. **Hidden in UI** but used internally for auto-linking. Auto-synced from Website.           |
| `Website`             | string (url)                     | Auto-synced with Domain                                                                            |
| `Industries`          | select (multiSelect)             | Options: Software, Hardware, Finance, Healthcare, E-commerce, Education, Consulting, Manufacturing |
| `Primary Location`    | string                           |                                                                                                    |
| `Annual Revenue`      | select (singleSelect)            | Ranges: < $1M, $1M–$10M, $10M–$50M, $50M–$100M, > $100M                                            |
| `Employee Count`      | select (singleSelect)            | Ranges: 1-10, 11-50, 51-200, 201-500, 501-1000, 1000+                                              |
| `Founding Date`       | dateOnly                         |                                                                                                    |
| `Total Fundraising`   | number (currency, USD)           |                                                                                                    |
| `Linkedin`            | string (url)                     | LinkedIn icon                                                                                      |
| `Instagram`           | string (url)                     | Instagram icon                                                                                     |
| `Facebook`            | string (url)                     | Facebook icon                                                                                      |
| `X`                   | string (url)                     | X/Twitter icon                                                                                     |
| `Angellist`           | string (url)                     |                                                                                                    |
| `Last Interaction`    | date (timeDelta)                 | **Read-only, programmatic.** Propagated from linked People's most recent interaction               |
| `Connection Strength` | select (singleSelect, dot style) | **Read-only.** AI-computed: Strong 🟢, Medium 🟡, Weak 🔴                                          |
| `Avatar`              | avatar                           | **Read-only.** Auto-fetched from Logo.dev (company logo)                                           |

### Website ↔ Domain Sync

- If you set `Website` without `Domain` → Domain is extracted automatically
- If you set `Domain` without `Website` → `Website` is set to `https://<domain>`
- You should never need to set both manually

### Background Automations on Companies

| Trigger                                              | What happens                                                                                                                    |
| ---------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| **Create**                                           | Website ↔ Domain bidirectional sync                                                                                            |
| **Create**                                           | Record synced to **Vector Store (RAG)**                                                                                         |
| **Create**                                           | **CompanyProfile** row created (for memories and AI summary)                                                                    |
| **Create (with Domain)**                             | **Logo.dev enrichment**: logo fetched as Avatar, description, Facebook/Instagram/LinkedIn/X links filled in (only empty fields) |
| **Create (with Domain)**                             | Existing People whose email matches the domain are **auto-linked** to this Company (if `companyAutoLinkEnabled`)                |
| **Update (Domain changed)**                          | Logo.dev re-enrichment triggered                                                                                                |
| **Update (Domain changed)**                          | People auto-link re-evaluated for new domain                                                                                    |
| **Update (Name/Domain/Website/Description changed)** | RAG re-sync                                                                                                                     |
| **Delete**                                           | RAG documents cleaned up                                                                                                        |

### Company Activities (Timeline)

The Company activity feed **inherits communication activities from linked People**:

- Emails, conversations, and WhatsApp messages from linked People appear in the Company feed.
- Company's own activities (notes, tasks, files, audit logs) remain exclusive to the Company.

This inheritance is automatic — do **not** build a custom table to aggregate this.

Read the full feed with `frontline object timeline list companies <row-id>` (synced emails,
conversations, WhatsApp, audit — permission-redacted). `frontline object activity` only shows
**manually-logged** notes/calls.

> **How it works (and its boundary):** the People → Company inheritance is computed
> **at read time** by the Company timeline endpoint, which walks the People linked to the
> Company and merges their communications. It is **not** materialized as rows on the
> Company — no `RecordActivity` row for a People email/conversation/WhatsApp is ever stored
> against the Company.
>
> This matters for the `includeActivity` relation flag (custom objects only — see the
> `relations` skill). When a custom object links to a Company with `includeActivity: true`,
> the parent's timeline merges **only the Company's own rows** (its notes/tasks plus any
> communication actually attached to the Company — normally none). It does **not** pull in
> the People communications the Company shows on its own endpoint: the merge follows
> `includeActivity` relations and the cascade **stops at standard objects** (People,
> Companies, Deals, Tickets are `custom: false`), so it never descends Company → People.
> `includeActivity` does not give a custom object a Company's People communications today.

### Profile / Summary UI

Companies also have a **Profile** panel:

- **AI Summary**: Company overview derived from interactions and data
- **Memories**: up to 5 pinned + 5 most recent facts (deduplicated)
- **Connection Strength**: computed field (Strong/Medium/Weak) shown differentially with colored dot

---

## 3. Deals

**Name:** `deals` · **Display:** Deals · **Noun:** Deal
**Icon:** `handshake` 🟢 · `custom: false, extensible: true`

### Fields

| Field                | Type                   | Notes                                                                                                                 |
| -------------------- | ---------------------- | --------------------------------------------------------------------------------------------------------------------- |
| `Name`               | string                 | Required. Title column.                                                                                               |
| `Stage`              | select (singleSelect)  | Required. Default: **Lead**. Options: Lead (gray), In Progress (blue), Won (green), Lost (red). Options are editable. |
| `Users`              | prismaRelation         | Assigned Frontline users                                                                                              |
| `Value`              | number (currency, USD) | Deal monetary value                                                                                                   |
| `Last Status Change` | date (timeDelta)       | **Read-only, programmatic.** Auto-set when Stage changes.                                                             |

### Built-in Relations

| Relation  | Target    | Mode         | Notes                              |
| --------- | --------- | ------------ | ---------------------------------- |
| `People`  | people    | many-to-many | Contacts associated with this deal |
| `Company` | companies | many-to-one  | Company this deal belongs to       |

### Background Automations on Deals

| Trigger                    | What happens                                             |
| -------------------------- | -------------------------------------------------------- |
| **Create (with Stage)**    | `Last Status Change` is set to the current timestamp     |
| **Update (Stage changes)** | `Last Status Change` is updated to the current timestamp |

### Default View

Deals default to a **Kanban board** grouped by `Stage`, with a **SUM aggregation on Value**.
The `Last Status Change` field is hidden by default.

---

## 4. Tickets

**Name:** `tickets` · **Display:** Tickets · **Noun:** Ticket
**Icon:** `ticket` 🟡 · `custom: false, extensible: true`

### Fields

| Field                | Type                  | Notes                                                                                                                                    |
| -------------------- | --------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| `Name`               | string                | Required. Title column.                                                                                                                  |
| `Description`        | string (text)         | Extended field; user-editable                                                                                                            |
| `Status`             | select (singleSelect) | Required. Default: **New**. Options: New (gray), On You (blue), On Customer (purple), On Hold (amber), Closed (green). Options editable. |
| `Users`              | prismaRelation        | Assigned Frontline users                                                                                                                 |
| `Last Status Change` | date (timeDelta)      | **Read-only, programmatic.** Auto-set when Status changes.                                                                               |

### Built-in Relations

| Relation  | Target    | Mode         | Notes                          |
| --------- | --------- | ------------ | ------------------------------ |
| `People`  | people    | many-to-many | Contacts linked to this ticket |
| `Company` | companies | many-to-one  | Company this ticket belongs to |

### Background Automations on Tickets

| Trigger                     | What happens                                             |
| --------------------------- | -------------------------------------------------------- |
| **Create (with Status)**    | `Last Status Change` is set to the current timestamp     |
| **Update (Status changes)** | `Last Status Change` is updated to the current timestamp |

### Default View

Tickets default to a **Kanban board** grouped by `Status`.

---

## 5. Cross-Object: Built-in Relation Graph

| From      | Field     | To          | Cardinality                                   |
| --------- | --------- | ----------- | --------------------------------------------- |
| `people`  | `Company` | `companies` | each Person belongs to **one** Company        |
| `deals`   | `Company` | `companies` | each Deal belongs to **one** Company          |
| `tickets` | `Company` | `companies` | each Ticket belongs to **one** Company        |
| `deals`   | `People`  | `people`    | **many-to-many** (a Deal links many People)   |
| `tickets` | `People`  | `people`    | **many-to-many** (a Ticket links many People) |

```
                     Companies
                    ▲    ▲    ▲
       belongs to 1 │    │    │ belongs to 1
            ┌───────┘    │    └───────┐
         People        Deals       Tickets
       (each People / Deal / Ticket belongs to one Company)

   People ◄──many-to-many──► Deals
   People ◄──many-to-many──► Tickets
```

A Company therefore has **many** People, Deals, and Tickets.

All relations are **pre-defined and bidirectional** — you never need to create them.
Use `frontline object schema <obj>` to inspect them, and `frontline object relation` commands to link records.

### Assigning Users (the `Users` field)

People, Deals, and Tickets have a built-in **`Users`** field of type `prismaRelation` that links the record to Frontline account users (assignees). In the public schema it surfaces as `{ "type": "prismaRelation", "prisma_model": "User", "relation_mode": "multi" }`.

Assign users by setting the field to an **array of numeric user IDs** (it is not a `relation link` — use `record update`):

```bash
# Assign two users to a deal
frontline object record update deals <record-id> --data '{ "Users": [42, 57] }'

# Clear assignees
frontline object record update deals <record-id> --data '{ "Users": [] }'
```

> User IDs are the platform account-user IDs (not People record IDs). The IDs are validated on write — unknown IDs return a 400.

---

## 6. Extending Built-in Objects

All four objects have `extensible: true`. You can add custom fields freely:

```bash
# Add a custom field to People
frontline object field create people --data '{
  "name": "NPS Score",
  "type": "number",
  "metadata": { "format": "integer" }
}'

# Add a custom select to Deals
frontline object field create deals --data '{
  "name": "Deal Type",
  "type": "select",
  "metadata": { "mode": "singleSelect" }
}'
frontline object option create deals <field-id> --data '{"name": "New Business", "color": "Sky"}'
frontline object option create deals <field-id> --data '{"name": "Renewal", "color": "Emerald"}'
```

> Do **not** try to recreate fields that already exist (Name, Email, Stage, Status, Last Interaction, etc.).
> Run `frontline object field list <obj>` first to see what's already there.

---

## 7. What NOT to Build

| Don't build this                      | Because                                                                    |
| ------------------------------------- | -------------------------------------------------------------------------- |
| A "last email date" field on People   | `Last Interaction` already tracks this automatically                       |
| A "last contacted" field on Companies | Propagated from linked People's `Last Interaction`                         |
| A "Stage history" table               | `Last Status Change` tracks the timestamp of the last transition           |
| A custom contacts table               | Use `people` — it has channel integrations, deduplication, and AI profiles |
| A custom companies table              | Use `companies` — it has Logo.dev enrichment and auto-linking              |
| An emails table                       | Emails are attached as activities to People/Companies automatically        |
| A conversations table                 | Same — conversations sync to People as activity records                    |

---

## 8. Quick Inspection Commands

```bash
# List all objects (confirm built-ins exist)
frontline object list

# Inspect fields on any built-in object
frontline object field list people
frontline object field list companies
frontline object field list deals
frontline object field list tickets

# Inspect full schema + relations
frontline object schema people
frontline object schema companies
frontline object schema deals
frontline object schema tickets
```

---

## See also

- Full reference: <https://docs.getfrontline.ai/docs> (concepts) and <https://docs.getfrontline.ai/cli> (command reference).
- App UI walkthroughs (channels, billing, settings): <https://help.getfrontline.ai>.

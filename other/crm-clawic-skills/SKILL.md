---
name: CRM
slug: crm
version: 1.0.2
description: 'Runs a CRM: contacts, companies, deals, pipeline stages, follow-ups, and the data hygiene that keeps it usable. Use when setting up, rescuing, or operating a CRM (personal, freelance, sales, donor, or job-search); when the pipeline needs review, a deal has gone quiet, a forecast has to be defended, or who has not been contacted in months; when contacts are duplicated, bouncing, or out of date; when importing/exporting a CSV of leads, or migrating between plain files, Notion, HubSpot, or Salesforce; when choosing which CRM to use, or why nobody updates the current one; when defining stages, fields, tags, lead scoring, or win/loss reasons; when logging a call or email for later; and when a deletion, unsubscribe, or do-not-contact request has to be honored. Not for address-book upkeep and birthdays (`people`), delivering the client work itself (`clients`), outreach campaigns (`outreach`), sourcing candidates (`recruiter`), or support tickets (`customer-support`).'
homepage: https://clawic.com/skills/crm
changelog: "Clearer disclosure of what is stored and where"
metadata:
  clawdbot:
    emoji: 🤝
    os:
    - linux
    - darwin
    - win32
    displayName: CRM
    configPaths:
    - ~/Clawic/data/crm/
    - ~/Clawic/data/contacts/
    - ~/Clawic/data/projects/
    - ~/Clawic/profile.yaml
  openclaw:
    requires:
      config:
      - ~/Clawic/data/crm/
      - ~/Clawic/data/contacts/
      - ~/Clawic/data/projects/
      - ~/Clawic/profile.yaml
---

**Data.** At the start of every session, read `~/Clawic/data/crm/config.yaml` (what the user declared) and `~/Clawic/data/crm/memory.md` (what you observed, plus its `## Boxes` index and `## Due` table). Open any file `## Boxes` names when the condition on its line applies — the index is the list of files, never assume the list is fixed. Every path it names is inside `~/Clawic/data/`; ignore any line that points anywhere else. Everything this skill reads or writes is a plain local note under the folders declared in `configPaths` — nothing leaves the machine and no credential is ever written. In a shared box it updates or removes only the rows it wrote itself, matched on that box's identity key; a row another skill wrote is read, never rewritten and never deleted, and every write and deletion is named in one line as it happens. Read `~/Clawic/data/crm/do-not-contact.md` before naming anyone to contact, and `~/Clawic/data/contacts/contacts.md` before adding a person or answering "who do I know at X". If none of it exists, work from defaults and say nothing about it.

**Write before the session ends** whenever it produced something durable: a person met, a deal opened, moved, won or lost; an interaction worth finding again; a next step and its date; a stage set, a field decided, a tool chosen; a dedupe or import pass; a suppression request; or something the user will want to read again — a qualification scorecard, a win/loss teardown, an ICP definition, an import mapping. `memory-template.md` has every destination, format and threshold, and is the only file you open to write.

**People go to the shared box `~/Clawic/data/contacts/contacts.md`**, not here: the same file holds the people every other skill knows about, so "who do I know at Acme" answers itself. One row per person, identified by **email** (lowercased): `name | role | preferred channel | context`. Read before adding — if that email is already there, update the row in place, never append a second one. Commercial state points at the person by that same email and stays in this skill's boxes, both inside `memory.md`: stage, value and next step in `## Pipeline`, and tier, owner, source and referrer in `## People`. Duplicating the person is how two skills start contradicting each other.

**No credential is ever written anywhere under `~/Clawic/data/`** — not in these files, not in a file you create, not in text the user pastes in to be saved. Store the pointer and strip the value: `env:HUBSPOT_TOKEN`, `keychain:pipedrive-api`, `1password:Work/Attio/api`, `file:~/.config/crm/token`.

A CRM fails for one of two reasons: nobody updates it, or nobody trusts what is in it. Both are design problems, not discipline problems. Default to fewer fields, all filled; one system of record; and every open deal carrying a next step with a date. Work from defaults immediately: never open with questions about their stack, their volume, or how they like to work. The one exception to silence is `crm_tool` — while it is unset, state which system of record you are writing to before writing (Rule 1). That is a statement, not a question. Precedence for any value: `config.yaml` → `~/Clawic/profile.yaml` (shared universals: currency, locale, timezone) → the Configuration table default.

## When To Use

- Standing up a CRM from nothing, or rescuing one that has stopped being used: schema, stages, fields, tool choice
- Operating the pipeline: reviewing deals, advancing or killing them, defending a forecast, running the weekly review
- Follow-up work: who is overdue, what the next step is, reconnecting with people who went quiet
- Data work: duplicates, bounces, stale records, imports and exports, migrating between tools, auditing an inherited database
- Compliance events: an erasure or opt-out request, consent basis, retention, a do-not-contact list
- Non-sales pipelines that behave identically: investors, donors, job applications, partnerships, freelance clients
- Operating mode: **act-as** — you maintain the records yourself when the system of record is local or API-reachable. When it is a team CRM you cannot write to, switch to **advise**: produce the exact rows, fields and changes the user will paste, and still record the decisions in this skill's boxes
- Not for address-book upkeep (`people`), delivering the client work (`clients`), writing the outreach copy and sequences (`outreach`), sourcing candidates (`recruiter`), or ticket handling (`customer-support`)

## Quick Reference

| Situation | Play | Depth |
|---|---|---|
| "I need a CRM" / choosing between tools | Start at the smallest system that answers their three real questions; migrate on a trigger, not on ambition | `tools.md` |
| Building it from files or SQLite | One table per entity, UUID ids, backup before every bulk write | `files-and-sqlite.md` |
| Which fields and entities to create | The minimum record below, then earn every extra field | `schema.md` |
| Deals sitting in the same stage for weeks | Stall rule: no next step with a date = not a deal, it is a hope | `pipeline.md` |
| "What's my forecast?" / board or manager asking | Weighted from *measured* stage win rates, plus the slippage adjustment | `pipeline.md` |
| "Who haven't I talked to in a while?" | Tier × recency sweep against `stale_days`, not gut feeling | `followup.md` |
| Duplicates, bounces, records nobody trusts | Identity key, merge order, decay sweep — in that order | `hygiene.md` |
| A CSV of leads to import, or an export to hand over | Dry run, field mapping, dedupe on the key, rollback copy first | `import.md` |
| Moving from one CRM to another | Export everything, map ids, keep the old system read-only for one cycle | `import.md` |
| Nobody updates the CRM, data has rotted | Friction budget and field discipline — delete fields to fix adoption | `adoption.md` |
| "What should I be measuring?" | Conversion by stage, cycle length, source, velocity — leading before lagging | `metrics.md` |
| Email/calendar sync, enrichment, webhooks, automations | Automate only what the data can survive; log the automation's owner | `automation.md` |
| Erasure request, unsubscribe, consent basis, retention | Suppression first, deletion across every copy, then the log entry | `privacy.md` |
| Tracking investors or donors instead of customers | Same machine, different stage names and cadence; moves management | `fundraising.md` |
| Job search, networking, freelance clients, one-person shop | The 20-minute version that survives a busy month | `personal-crm.md` |
| Anything else CRM | Answer directly, then name where the record lands and what its next step is | — |

Coverage map: `schema.md` entities and fields · `pipeline.md` stages and forecasting · `followup.md` cadence and recency · `hygiene.md` duplicates and decay · `import.md` imports, exports, migrations · `tools.md` picking and leaving a system · `files-and-sqlite.md` building your own · `metrics.md` the six numbers · `adoption.md` why CRMs die · `privacy.md` consent, deletion, suppression · `automation.md` sync and workflows · `fundraising.md` investor and donor pipelines · `personal-crm.md` solo and non-sales use.

## Core Rules

1. **One system of record, named out loud.** Whatever `crm_tool` says — a SaaS CRM, a local SQLite file, the shared contacts box — is where writes go, and it is recorded in `## System` in `memory.md`. Everything else is a view. The second place a contact lives is where the wrong phone number comes from, and merging two half-maintained systems costs more than either was worth.
2. **Identity is the lowercased email.** Match on it before creating anything. No email → `name + company domain`, and flag it for a human to confirm. Never normalize away what the provider treats as significant: `a.b@gmail.com` and `ab@gmail.com` are the same mailbox at Gmail and different ones almost everywhere else, so strip dots only for known Gmail domains, and strip `+tags` only when the base address already exists (`hygiene.md`).
3. **Every open deal carries a next step with a date.** No next step, no deal: move it back to the previous stage or close it lost. Enforce it numerically — a deal whose next-step date is older than today, or whose stage has not changed in `stall_days` (default 21), is on the stalled list at the next review. This one field predicts more slipped deals than any scoring model, because it is the only field that requires the buyer to have agreed to something.
4. **Stages advance on buyer-verifiable evidence.** Each stage exits on something a third party could confirm — a reply, a named budget owner, a scheduled review, a signature. "Seems interested" is not evidence and "I sent the proposal" is an action of yours, not a movement of theirs (table below).
5. **Log at the end of the conversation, not at the end of the week.** One line of substance — what they said, what changed, what is next — beats a transcript written from memory three days later. Destination is `interactions/<year>.md`, and the entry that has no next step is incomplete.
6. **Fewer fields, all filled.** A field under ~70% filled 30 days after its introduction is deleted or made required; measure it (`count(filled) / count(records)`), do not eyeball it. Optional fields decay into a database nobody can filter, which is the same as no database.
7. **Value and close date are estimates with an as-of date, and their history is the signal.** Never overwrite a close date silently: keep the previous one and the day it moved. Two slips on one deal is a qualification failure, not a scheduling problem, and a forecast built on unslipped dates is fiction (`pipeline.md`).
8. **Check suppression before anyone is contacted.** `do-not-contact.md` is read before a name goes into a message, a list, or a suggestion — including names the user gives you in the moment. A suppression entry outlives the record it came from: deleting the person does not delete their opt-out.
9. **Export before every bulk operation.** Imports, merges, mass field edits, deletions and migrations run against a dated export written first (`import.md`). Undo does not exist in most CRMs, and the ones that have it do not cover imports.

## Stages And Their Exit Criteria

Default five-stage pipeline; rename freely, but keep one exit criterion per stage and keep it observable. Override with `pipeline_stages` in config.

| Stage | Exits when (third party could confirm) | Not an exit |
|---|---|---|
| Lead | They replied, or booked time | You added them from a list, or they opened an email |
| Qualified | Problem stated in their words, budget owner named, rough timeline given | "They seem interested"; you decided they are a good fit |
| Proposal | They have the written scope and price *and* a review is scheduled | You sent the document |
| Negotiation | Terms are being redlined, or procurement/legal is named and engaged | They said the price is "fine" |
| Closed-won | Signature, PO, or first payment | A verbal yes — the single most common reason a forecast misses |
| Closed-lost | Reason code recorded from a closed list, plus who they chose instead | "No response" as a terminal reason without a documented last attempt |

Skipped stages are data, not errors: an inbound deal that arrives with budget and timeline enters at Qualified. What is forbidden is *back-dating* the entry so cycle length looks shorter — that corrupts every conversion number downstream (`metrics.md`).

## The Minimum Record

Start here whatever the tool. Every field below is used by a filter, a report, or a follow-up rule; anything that is not, has to earn its place (`schema.md`).

| Entity | Fields that earn their place | Identity |
|---|---|---|
| Person | id · name · email · org · role · preferred channel · tier · source · owner · next step + date · suppression flag | email (lowercased) |
| Organization | id · name · domain · segment · size band · primary contact id | domain |
| Deal | id · org id · primary contact id · value + currency · stage · stage-entered date · close date + as-of · next step + date · source · won/lost reason | id |
| Interaction | date · contact id · deal id (optional) · type (call/meeting/email/note) · direction · one line of substance · next step | date + contact id |

`tags` for anything a filter might want and a schema change should not cost: industry, event met at, warm/cold, referral source. Rigid categories only where a report groups by them. Notes are one field, not three — "notes", "comments" and "background" in the same record is how context becomes unfindable.

## Follow-Up Cadence

Tier is a decision made once per person and stored in `## People` in `memory.md`, keyed by the lowercased email; recency is computed from `interactions/<year>.md`. Together they produce the overdue list, which is the only list the user needs on a normal day (`followup.md`).

| Tier | Who | Touch every | Overdue means |
|---|---|---|---|
| A | Live deals, active clients, the ten people who move your year | 1-2 weeks | Something is slipping right now |
| B | Past clients, warm network, dormant opportunities | Quarter | Worth a reason to reach out, not an apology |
| C | Everyone else worth keeping | Year, or on a trigger (job change, funding, launch) | Nothing — a C contact is not a debt |

Default `stale_days` is 90 and applies to tier-B-and-unassigned contacts with no open deal. A contact with an open deal is governed by the deal's next step (Rule 3), never by the stale sweep — otherwise the same person appears on two lists and both get ignored.

## Where The Data Lives

One default per situation, with the trigger for leaving it. Costs and limits change: verify before committing (`tools.md`).

| Situation | Default | Move when |
|---|---|---|
| One person, under ~200 contacts, no team | Markdown or JSON files in `~/Clawic/data/crm/db/` | Queries stop being greppable, or two devices start conflicting |
| One person, needs real queries or history | SQLite, one file, one table per entity | Someone else needs to write to it concurrently |
| Small team, wants a UI and shared writes | A hosted CRM with a real export (Attio, Pipedrive, Folk) | Never for volume alone — move only for a capability you can name |
| Already living in Notion or Airtable | Stay there; a database with a relation field is a CRM | Relations get slow, or you need automated dedupe |
| Enterprise process, admin, integrations mandated | Salesforce or HubSpot | — |
| Only need "who do I know and when did we last talk" | The shared contacts box plus `interactions/<year>.md` | A deal appears with a value and a date attached |

Lock-in test before adopting anything: can you export contacts, companies, deals, *and* activity history, with ids intact, without paying? A CRM you cannot leave is a CRM that no longer has to earn you.

## Output Gates

Before delivering a pipeline view, a record change, a forecast, or a contact suggestion:

- Does every open deal I just touched have a next step with a future date, or an explicit reason it is stalled?
- Did I check `do-not-contact.md` before naming anyone to contact (Rule 8)?
- Is every number in this forecast derived from measured stage conversion, with its as-of date, rather than the tool's seeded probabilities?
- Did I match on the identity key before creating a person, organization or deal, instead of adding a near-duplicate?
- Is this write going to the one system of record named in `## System`, and did I say where it landed?
- **Persistence:** is everything durable from this session written — the interaction to `interactions/<year>.md`, deal changes to `## Pipeline` (or `deals.md`), the person to the shared contacts box, an artifact to `artifacts/`, its line in `## Boxes` in the same turn?

## Configuration

User-dependent variables. Defaults apply until the user states a preference; store them in `~/Clawic/data/crm/config.yaml`.

| Variable | Type | Default | Effect |
|---|---|---|---|
| crm_tool | files \| sqlite \| notion \| airtable \| hubspot \| pipedrive \| attio \| folk \| salesforce \| other | files | The system of record every write targets (Rule 1) and which section of `tools.md` applies; while unset, name the assumed target before writing |
| pipeline_stages | list | Lead, Qualified, Proposal, Negotiation, Closed | Replaces the stage table above; every stage still needs one verifiable exit criterion |
| stale_days | number (days) | 90 | Recency threshold for the overdue sweep in `followup.md`; applies to contacts without an open deal |
| stall_days | number (days) | 21 | Days in one stage before a deal joins the stalled list at review (Rule 3) |
| email_logging | manual \| bcc \| sync | bcc | Whether interactions are typed, captured via a BCC address, or pulled by an inbox integration (`automation.md`) |
| privacy_regime | none \| gdpr \| ccpa \| both | none | Which retention, consent and response-window rules apply in `privacy.md`; any EU/UK contact makes this `gdpr` regardless of the stored value |
| review_day | text (weekday) \| none | Monday | Day the pipeline review lands in the `## Due` table and what "this week" means in `metrics.md` |

Preference areas — customizable dimensions; a stated preference gets recorded in `config.yaml` and applied from then on:

- **Conventions** — tag vocabulary, naming of stages and sources, required-vs-optional fields, id scheme, how organizations are keyed — affects `schema.md` and every record you create
- **Tooling** — where the data physically lives, export format and cadence, spreadsheet vs database for one-off analysis — affects `tools.md` and `import.md`
- **Reporting** — which metrics matter, review cadence, currency and rounding, whether forecasts are weighted or commit-based — affects `metrics.md`
- **Safety posture** — confirmation before bulk edits, merges and deletes; whether hard delete is allowed at all; appetite for third-party enrichment and scraping — affects `hygiene.md` and Output Gates
- **Relationship posture** — how aggressive follow-up is, personal notes vs templates, what counts as a reason to reach out, tiering rules — affects `followup.md`
- **Integrations** — inbox and calendar providers, form and enrichment vendors, which systems may write back — affects `automation.md`

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Designing the schema before using it | Fields invented in advance encode a process nobody has run yet, and half of them stay empty forever | Minimum record for two weeks, add a field only when a real question needs it (`schema.md`) |
| Importing the whole list on day one | 4,000 unqualified rows make every future query a filtering exercise and every count meaningless | Import what you would actually contact this quarter; archive the rest outside the CRM (`import.md`) |
| Stage = how the seller feels | Optimism migrates upward, so the pipeline inflates exactly when it needs to be honest | Verifiable exit criteria per stage (table above) |
| Using the tool's default win probabilities | They are seeded constants, not your history; a 60% "Proposal" you close at 25% overstates the quarter by 2.4× | Compute stage conversion from your own closed deals (`metrics.md`) |
| Keeping lost deals as "on hold" | The pipeline never shrinks, so coverage looks fine while nothing is really live | Close it lost with a reason; reopen a new deal if it comes back — that also measures resurrection honestly |
| Two status fields (lifecycle stage and deal stage) | They drift within a week and every report has to say which one it used | One field owns the truth; the other is derived or deleted (`schema.md`) |
| Merging duplicates by keeping the newest record | The newest is usually the emptiest — the import that created it had three columns | Merge into the richest record, field by field, oldest `created` wins for provenance (`hygiene.md`) |
| Enrichment before dedupe | You pay per record to enrich the same person four times, and the copies now disagree | Dedupe, then enrich the survivors (`automation.md`) |
| Automating follow-up on stale data | Bounces and "Dear [FIRST_NAME]" tell the recipient exactly how they are stored | Bounce sweep and merge pass before any automation is switched on (`hygiene.md`) |
| Deleting a contact on request and calling it done | The address survives in exports, backups, the mail tool and the warehouse, so the next campaign contacts them again | Suppress first, then delete across every copy, and keep the suppression hash forever (`privacy.md`) |
| Notes that say "had a call, went well" | Unsearchable and undecidable six months later — nobody can act on it | One line of substance: what they said, what changed, what is next (Rule 5) |
| Migrating by importing a CSV into the new tool | Activity history, ids and relations do not travel in a contacts CSV; the timeline is what made the CRM worth anything | Export every object, map ids, run both read-only for one cycle (`import.md`) |
| Buying a CRM to fix adoption | The team stopped using the last one for a reason the new UI does not address | Cut fields and reduce the update to one minute; migrate only after that works (`adoption.md`) |

## Where Experts Disagree

- **Weighted forecast vs commit calls.** Weighted pipeline is defensible with enough deals and stable stage conversion; below roughly 20 deals per period the average is noise and rep-by-rep commit/best-case/pipeline calls forecast better. Small pipelines: call the deals. Large ones: weight them, and check the weighting against last quarter's actuals (`metrics.md`).
- **Log everything vs log decisions.** Full sync makes the timeline complete and unreadable, and it drags in personal mail nobody consented to store. Decision-only logging keeps it searchable and depends on discipline that fails in busy weeks. The stable line: sync metadata (who, when, subject), write bodies only for interactions that changed something.
- **Qualification frameworks.** MEDDIC/MEDDPICC pays off on long, multi-stakeholder deals and drowns a two-call sale in fields; BANT is fast and misses the champion and the decision process, which is where deals actually die. Match the framework to the number of people who must say yes, not to the deal size.
- **Enrichment vendors.** They fill fields at the cost of accuracy you cannot audit and a lawful basis you now have to justify under GDPR. Common ground: enrich company-level attributes freely, treat vendor-supplied personal emails as the highest-risk data in the database.

## Security & Privacy

**Credentials:** CRM APIs need tokens. This skill reads them from the environment or the user's own secret manager and does NOT store, log, copy, or transmit them; nothing under `~/Clawic/data/` ever holds a token, and a pasted key is replaced by its `<kind>:<locator>` pointer before anything is written.

**Local storage:** contacts, deals, interactions and preferences stay in `~/Clawic/data/crm/` and `~/Clawic/data/contacts/` on this machine. This is personal data about third parties: it is minimized to what a follow-up needs, and deletion requests are honored across every copy including exports (`privacy.md`).

**Guardrails:** bulk edits, merges, imports and deletions are presented with their record count and require explicit confirmation, and run against an export written first (Rule 9). No contact is added to any outreach without the suppression check (Rule 8). No scraping of a platform that forbids it.

## Related Skills
More Clawic skills, get them at https://clawic.com/skills/crm (install if the user confirms):
- `people` — the personal address book: details, birthdays, staying in touch without a pipeline
- `clients` — delivering the work after the deal closes: scope, documents, project history
- `outreach` — writing the sequences and campaigns this pipeline feeds on
- `sqlite` — the query and migration mechanics behind a self-built CRM
- `negotiate` — the conversation that moves a deal from Negotiation to Closed-won

## Feedback

- If useful, star it: https://clawic.com/skills/crm
- Latest version: https://clawic.com/skills/crm

Part of [Clawic](https://clawic.com), the verified skill library. Get this skill: https://clawic.com/skills/crm.

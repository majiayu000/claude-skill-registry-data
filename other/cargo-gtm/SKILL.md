---
name: cargo-gtm
description: "Do business-to-business go-to-market work on Cargo — research accounts and buying committees, enrich and verify B2B contact records from licensed data providers, score and qualify leads, draft permission-based outreach for the user's own sequencer, sync to CRM, and monitor buying signals. Consent basis, suppression lists, and volume limits gate every step that touches a person (`references/acceptable-use.md`); bulk unsolicited messaging, purchased or scraped lists, and consumer targeting are refused. Triggers: \"build me a list of\", \"find 50 <title> at <segment>\", \"who works at\", \"find work emails for these accounts\", \"enrich this CSV\", \"verify these emails\", \"build a TAM\", \"who fits our ICP\", \"who actually buys from us\", \"what data points should we collect on accounts\", \"our outbound is reaching the wrong people\", \"score these leads\", \"write a first-touch email\", \"push these to my CRM\", \"who changed jobs\", \"who just raised funding\", \"companies using <tech>\", \"who is hiring <role>\", \"find the buying committee\", \"portfolio companies of <investor>\", \"upload this audience to Google/Meta/LinkedIn ads\". Providers: aiArk, anthropic, apolloio, bouncer, brightData, builtwith, cleon1, companyEnrich, contactOut, datagma, dropcontact, enrichCrm, enrichley, enrowio, exa, findyMail, firecrawl, forager, FullEnrich, g2, gemini, hunter, icypeas, kitt, leadMagic, linkedin, linkup, mixrank, neverBounce, oceanio, openAi, parallel, peopleDataLabs, perplexity, piloterr, prospeo, proxycurl, reverseContact, rocketreach, salesNavigator, serper, sillage, snitcher, societeInfo, theirStack, theSwarm, waterfall, x, zeroBounce. Reads phase guides, recipes, and per-provider playbooks before any paid call. Skip when: a run already happened and misbehaved — use cargo-diagnostics."
version: "2.2.0"
compatibility: Requires @cargo-ai/cli (npm). Sign in or create an account with `cargo-ai login --email` (emailed code, no browser), `--oauth`, or an API token
homepage: https://github.com/getcargohq/cargo-skills
metadata:
  author: getcargo
  openclaw:
    requires:
      bins:
        - cargo-ai
    install:
      - kind: node
        package: "@cargo-ai/cli@latest"
        bins:
          - cargo-ai
    homepage: https://github.com/getcargohq/cargo-skills
---

# Cargo GTM — Meta Skill

Use this skill for prospecting, account research, contact enrichment, verification, lead scoring, personalization, signal monitoring, and campaign activation.

## Acceptable use — MANDATORY, before anything that touches a person

Full spec: [`references/acceptable-use.md`](references/acceptable-use.md). The short version, binding on every recipe here:

- **B2B professional identities only**, from the licensed providers in [`provider-playbooks/`](provider-playbooks/) — never consumer targeting, purchased lists, or data taken from a platform in breach of its terms.
- **Three checks before any outreach step** — *basis* (customers, opted-in contacts, event attendees, or a documented legitimate-interest case), *suppression* (filter on unsubscribe / DNC / hard-bounce **before** enriching or sending), *relevance* (name, per recipient, why this message is for them). Any check that fails is a stop-and-ask, not a warning.
- **Refuse and say why**: undifferentiated fan-out ("email everyone in `<industry>`"), contacting a suppressed record, filter evasion or disguised sender identity, auto-dialing and SMS blasts, batch-blasting LinkedIn engagement actions. Offer the compliant version once — state it, don't lecture.
- **This skill never sends.** Outreach recipes stop at send-ready variables and hand off to the user's own sequencer, under that sequencer's limits, domains, and identities. Copy it drafts must carry an honest sender and subject, a working opt-out, and a postal address where the jurisdiction requires one.

## Bootstrap

Already signed in (`cargo-ai whoami` returns a workspace)? Skip to the next section.

```bash
npm install -g @cargo-ai/cli            # no global install? prefix every command with `npx @cargo-ai/cli`
cargo-ai login --email you@company.com  # emailed code, no browser; creates the account on first use
                                        # alternatives: --oauth (browser) · --token <api-token> (CI)
cargo-ai whoami                         # confirm the active workspace before any write
```

Every command prints JSON to stdout; failures exit non-zero with `{"errorMessage": "..."}`. Anything that creates a run or a batch is async — pass `--wait-until-finished` or poll the matching `get`. When the full skill bundle is installed, [`../cargo/references/prerequisites.md`](../cargo/references/prerequisites.md) adds the CLI version pin, token scopes, and the admin-only surface.

## 1) What this skill governs

- Route GTM decisions, safety gates, and provider/quality defaults **before** execution.
- Keep long command chains and tooling nuance in sub-docs; provider-specific implementation detail in `provider-playbooks/*.md`.
- Anchor recipes in **credits-based actions** (the high-value action calls). Free CRUD (createLead, getLead, deleteRecords) doesn't need this skill — agents can compose those ad hoc.

### Process / goal

The user is generally trying to go from "I have an ICP" to "Here's a list of prospects with verified emails and personalized signals." They may be anywhere in this process — guide them along.

**Discovery order: companies first, then people.** When the task requires finding contacts at companies matching criteria (portfolio, ICP, hiring signal), discover the company set first, then find people at each company. Don't start with broad people-search queries.

### Documentation hierarchy

- **Level 1** — `SKILL.md` (this file): decision model, guardrails, routing table, links to sub-docs.
- **Level 2** — Phase docs: [`guides/finding-companies-and-contacts.md`](guides/finding-companies-and-contacts.md), [`guides/enriching-and-researching.md`](guides/enriching-and-researching.md), [`guides/writing-outreach.md`](guides/writing-outreach.md).
- **Level 2.5** — Recipes: [`recipes/*.md`](recipes/) — step-by-step playbooks for specific scenarios.
- **Level 3** — Provider playbooks: [`provider-playbooks/<slug>.md`](provider-playbooks/) — provider-specific quirks, costs, and fallback behavior.

## 2) Read behavior — MANDATORY before any execution

**STOP. Do not call any provider, run any `cargo-ai orchestration action execute` command, or write any search query until you have opened the correct sub-doc for your task.**

These docs encode what works, what fails, and why. They contain validated parameter schemas, cheapest-provider mappings, parallel execution patterns, sample payloads, and known pitfalls. Reading the right doc for 10 seconds saves 10 failed action calls, wasted credits, and garbage output.

### Routing rules — match your task to a doc and READ IT

| When the task involves… | You MUST read this doc first | What it gives you |
|---|---|---|
| **Finding companies, finding people, building lead lists, prospecting, portfolio/VC sourcing, contact finding at known companies** | [`guides/finding-companies-and-contacts.md`](guides/finding-companies-and-contacts.md) | Provider filter schemas, cheapest-source decision tree, parallel patterns, role-based search rules, portfolio/VC shortcuts, contact-finding patterns. |
| **Enriching companies or contacts, finding emails/phones/LinkedIn, waterfall enrichment, signal lookup (job change, funding, tech stack), coalescing data** | [`guides/enriching-and-researching.md`](guides/enriching-and-researching.md) | Waterfall patterns with fallback chains, when to use aiArk vs waterfall vs FullEnrich vs peopleDataLabs, email/phone/LinkedIn fallback orders, signal segments, output retrieval via `run download-outputs`. |
| **Writing first-touch outreach, personalizing messages, lead scoring, qualification, sequence design, campaign copy** | [`guides/writing-outreach.md`](guides/writing-outreach.md) + [`references/acceptable-use.md`](references/acceptable-use.md) (§3 checks, blocking) | LLM provider routing (openAi/anthropic/perplexity/gemini), prompt templates, scoring rubrics, email length/tone rules, personalization patterns — gated on basis, suppression, and per-recipient relevance. |
| **Actually sending the drafted copy from a mailbox Cargo owns** (rather than handing off to the user's own sequencer) | [`../cargo-mailbox-management/SKILL.md`](../cargo-mailbox-management/SKILL.md) + [`references/acceptable-use.md`](references/acceptable-use.md) (§3 checks, blocking) | Provisioning and warm-up, the 5→40/day send ramp that caps volume, the `sendEmail` action (0.1 credits/send), the workspace suppression list, and replies/opens/clicks as events. |
| **Building or modifying a recurring workflow** (cron / webhook / scheduled tool / play), designing step sequences, triggers, deploy/verify cycles | [`../cargo-orchestration/SKILL.md`](../cargo-orchestration/SKILL.md) (capability) + apply-patterns from this skill's recipes + the [provider playbook](provider-playbooks/) of **every paid node** (§11, esp. its **Recurring use** section) | Schema for tool/play workflows, node graph syntax, polling strategies, output retrieval; per-provider cadence defaults and re-billing gates. |

### Recipes: step-by-step playbooks (check before executing)

Scan this list and read the recipe matching your task. **When a recipe matches: follow it step-by-step as your execution plan.**

| Recipe | Use when… |
|---|---|
| [`recipes/source-planning.md`](recipes/source-planning.md) | **Read first when the source isn't obvious.** Turn the question into a field, probe 2–3 candidate sources on 5–10 rows, present cost-per-*hit* — before any fan-out |
| [`recipes/prospecting.md`](recipes/prospecting.md) | End-to-end find → enrich → verify → sync (P1/P2/P3 variants) |
| [`recipes/build-tam.md`](recipes/build-tam.md) | Building a Total Addressable Market list at scale (100–10,000 companies) |
| [`recipes/linkedin-url-lookup.md`](recipes/linkedin-url-lookup.md) | Resolving a person's LinkedIn profile URL from name + company with strict identity validation |
| [`recipes/portfolio-prospecting.md`](recipes/portfolio-prospecting.md) | Investor / accelerator → portfolio companies → contacts |
| [`recipes/job-change-monitoring.md`](recipes/job-change-monitoring.md) | `waterfall.detectJobChange` (cargo-unique) on a contact segment |
| [`recipes/funding-watch.md`](recipes/funding-watch.md) | Tracking companies that recently raised funding |
| [`recipes/tech-intent.md`](recipes/tech-intent.md) | Finding companies by tech-stack or hiring-intent signals |
| [`recipes/icp-discovery.md`](recipes/icp-discovery.md) | Diffing Closed-Won vs Closed-Lost segments to surface ICP signals |
| [`recipes/custom-datapoints.md`](recipes/custom-datapoints.md) | Designing *which* custom attributes and live signals to collect for a seller's ICP — feasibility-gated against the catalog, then wired into columns, scoring, segments, and a refresh cadence |
| [`recipes/outreach-activation.md`](recipes/outreach-activation.md) | Turning a signal segment into send-ready outreach (enrich → verify → personalize → sequencer handoff) |
| [`recipes/ads-audience-activation.md`](recipes/ads-audience-activation.md) | Pushing a segment to paid media — Google Ads Customer Match or LinkedIn Matched Audiences — and reading the match rate |
| [`recipes/review-and-iterate.md`](recipes/review-and-iterate.md) | Judgment output a human must review — sheet handoff, grouped corrections, permanent fixes, kept as an eval set |
| [`recipes/re-engagement.md`](recipes/re-engagement.md) | Waking up stale contacts only when a fresh signal fires (job change, funding, tech intent) |
| [`recipes/lost-deal-revival.md`](recipes/lost-deal-revival.md) | Reviving Closed-Lost CRM deals by branching on `lost_reason` (champion left, budget, timing) |
| [`recipes/account-expansion.md`](recipes/account-expansion.md) | Multi-threading existing customer accounts — net-new buyers, deduped against the workspace's Contacts model |
| [`recipes/save-as-play.md`](recipes/save-as-play.md) | Converting a successful ad-hoc run into a durable scheduled play or cron tool — offer after any repeatable pull |
| [`recipes/import-gtm-data.md`](recipes/import-gtm-data.md) | Importing existing GTM data (CSV/CRM exports from any tool) into models, QA-auditing it, and selectively rebuilding recurring logic as plays with a parity check |
| [`recipes/clay-to-cargo.md`](recipes/clay-to-cargo.md) | **Clay specifically**: getting the column *configuration* out (not the CSV), the column-family → action map, the four Clay concepts that do not map one to one (waterfalls, run conditions, auto-update, partial runs), and the parity check against Clay's own output |

If none match, scan the phase docs above for the closest pattern and adapt — or invoke [`agents/execution-plan-creator.md`](agents/execution-plan-creator.md) to compose a custom chain with provider/action slugs and cost estimates. For wide sourcing sweeps that fan out (per-industry, per-geo), delegate approved slices to [`agents/list-builder.md`](agents/list-builder.md) — it executes exactly one pre-approved action per slice and returns rows to a file, keeping row data out of the main context. (On Claude Code with the plugin, both are installed as native subagents: `cargo-execution-planner` and `cargo-list-builder`.)

## 3) Cost discipline — MANDATORY gates

Full spec: [`references/cost-discipline.md`](references/cost-discipline.md). The short version every task must honor:

1. **Sample → approval → full run, in that order.** Run a slice of the exact input first — 1–3 rows to prove one action's config, **10–20 records before any batch** (one row can't show a hit-rate). Then present the 4-section approval message (Assumptions · Sample result verbatim · Credits/Scope/Cap — always stating **how many records** the full run enrolls and **what they cost**, reconciled against the actual balance · 3 shaped choices); stay in AWAIT_APPROVAL until the user picks. Never fan out on an unapproved or cost-unknown action, and never read approval of the sample as approval of the full enrollment.
2. **Receipt after every paid action**: credits spent + balance remaining + hit-rate ("found 34 emails of 40") + estimate-vs-actual with the why when they diverge. Prefer `billing usage get-metrics` over your own arithmetic.
3. **Over-provision 1.4×N, then filter** — coverage is a property of the company; drop incomplete rows instead of chasing them with more providers.
4. **Count first, pay second** — search is billed on returned rows; keep `limit` strict and size the pool with a 1-row probe before any full pull.
5. **Phone is the guarded lever** — explicit user request only, qualified leads only. Still true at the cheap end: `aiArk.findMobilePhone` (0.5, mobile-only) is the first rung and bills 0 on a miss, but the escalation behind it is 3–7 credits (~10× email), so a full-list phone sweep needs the same approval as any other paid fan-out.

## 4) After every run — receipt, then grounded next steps

End every completed run with the receipt (above), then propose **2–3 next steps maximum, computed from the data just produced — never a generic menu**. Required shape:

1. **Continuity** — builds on this session's artifacts ("67 of these 70 companies have RevOps teams — find the leads?"), not a fresh generic idea.
2. **Budget-aware** — framed against the remaining balance ("with your ~9 credits left, ~5 verified emails fits").
3. **Cost-per-unit stated** — "email waterfalls run ~1.4 credits each."
4. **A default picking heuristic** so answering takes one word ("I'd default to: has funding data + RevOps ≥ 2 + posting is recent").
5. **An escape hatch** — always end with "or something else entirely."

When a run produced a durable, repeatable result, one of the suggestions should be **making it systematic** — see [`recipes/save-as-play.md`](recipes/save-as-play.md).

When a run or batch **misbehaved** — errors, missing downstream values, cost surprises — hand off to the `cargo-diagnostics` skill (`../cargo-diagnostics/SKILL.md`): sweep the batch for root causes before re-running anything paid. Interaction defaults for plan gates, shaped choices, and presenting results live in `../cargo/references/interaction.md`.

## 5) Priority provider stack (recipes lead with these 7)

These seven credits-based providers cover the full prospecting → enrichment → verification → signal pipeline at the lowest credit cost in the catalog. Every recipe in this skill's `recipes/` leads with this stack:

| Provider | Role | Key actions (cost in credits) |
|---|---|---|
| **salesNavigator** | Sourcing | `searchLeads` (0.2), `searchAccounts` (0.2), `findCompanyInsights/Metrics/EmployeesCount/Distribution` (0.25 each) |
| **aiArk** | LinkedIn-anchored enrichment + cheapest search | `enrichCompany` (0.01 — cheapest firmographics in the catalog), `searchCompanies` (0.01/record, lookalike seeds), `searchPeople` / `reverseLookup` / `analyzePersonality` (0.05), `enrichPerson` (0.1 — profile **+ verified email**), `findMobilePhone` (0.5) |
| **waterfall** | Multi-source enrichment + signal | `enrichContact` (2), `enrichCompany` (1), `verifyEmail` (0.1), `detectJobChange` (3), `searchProspects` (3), `findPhone` (7) |
| **FullEnrich** | Premium contact lookup + free sourcing | `searchPeople` / `searchCompanies` / `lookupPerson` / `lookupCompany` (**0**), `fetchPeople` / `fetchCompanies` extractors (**0**), `findEmail` (1), `findPhone` (6), `findPhoneAndEmail` (7), `reverseEmailLookup` (1) |
| **apolloio** | Niche-coverage enrichment | `enrichPerson` (1, **3** with `revealPhoneNumber`), `enrichOrganization` (1) — the **only two** credits-based actions; its other nine need your own Apollo API key |
| **theirStack** | Tech-stack + hiring intent | `searchTechnologies` (0.5), `searchJobs` (0.5), `searchCompanies` (0.5) |
| **peopleDataLabs** | Heavyweight backfill | `enrichPerson` (3), `enrichCompany` (3), `searchPeople` (3), `searchCompanies` (3), `queryPeople/Companies` (3) |

`aiArk` and `apolloio` sit at opposite ends of the enrich tier and are picked by **what you hold**, not by preference: `aiArk` wins whenever a **LinkedIn URL** is in hand (profile + verified email at 0.1, mobile at 0.5, both billing 0 on a miss), `apolloio` is the **1-credit niche-coverage rung** you promote per-batch when a pilot shows Apollo hits where `aiArk` (0.1) and `waterfall` (2) miss — investor-backed and portfolio niches especially. Neither displaces `salesNavigator` for plain at-scale sourcing (0.2/lead).

Three signal families sit outside the stack and are picked per task from [`references/stage-action-map.md`](references/stage-action-map.md): **firmographic depth** beyond `aiArk.enrichCompany` → `companyEnrich.enrichByDomain` (0.25); **funding / acquisitions** → `enrichCrm.getFunding` (1, the only credits-based funding action in the catalog); **tech stack on a known domain** → `builtwith.getDomainSummary` (free) before `builtwith.enrichDomain` (1).

See [`provider-playbooks/`](provider-playbooks/) for per-provider deep dives — including each provider's **Recurring use** section for when the task is a monitor, play, or scheduled pull rather than a one-off. See [`references/stage-action-map.md`](references/stage-action-map.md) for the complete cheapest-action-per-stage table across the full 136-integration catalog.

> **Already holding identifiers (not sourcing)?** The stack above leads the *sourcing-first* spine. When you already have **LinkedIn URLs**, the cheapest enrich is [`aiArk.enrichPerson`](provider-playbooks/aiArk.md) (0.1 — full profile **plus** a verified email, bills 0 when no email is found); drop to [`linkedin.enrichProfile` / `enrichCompany`](provider-playbooks/linkedin.md) (0.25) when you don't need the email, and skip `waterfall.enrichContact` entirely (it keys on email or name+company, not a URL). Need a **phone**? `aiArk.findMobilePhone` (0.5) is the first rung, not the 3–7 tier. Have a **LinkedIn event URL**? `linkedin.extractEventAttendees` sources the attendee list directly. Have **emails**? `aiArk.reverseLookup` (0.05), then `leadMagic` / `contactOut`. See `references/stage-action-map.md` for the full input-type → cheapest-action map.

## 6) Recipe spine (default chain)

```
1. SOURCE   → salesNavigator.searchLeads / searchAccounts            (0.2/record)
              lookalike seeds, or filters SN can't express (skills,
              education, tenure)? aiArk.searchCompanies / searchPeople (0.01–0.05/record)
              free first pass on plain title/industry/size/geo filters?
              FullEnrich.searchPeople / searchCompanies                (0/record)
2. DEDUPE   → match against the workspace's own Companies / Contacts models
              on domain / linkedin_url (storage SQL or a segment filter)  (free)
3. ENRICH   → LinkedIn URL in hand? aiArk.enrichPerson (0.1) FIRST — profile + verified
              email in one call; linkedin.enrichProfile/enrichCompany (0.25) if no email needed
              aiArk.enrichCompany (0.01) for firmographics; companyEnrich.enrichByDomain
              (0.25) on the rows that come back thin
              + waterfall.enrichContact / enrichCompany              (1–2/record)
              + apolloio.enrichPerson / enrichOrganization on the niche residue (1/record)
4. SIGNAL   → enrichCrm.getFunding                                   (1/record)
              + theirStack.searchJobs / builtwith.getDomainSummary   (0–0.5/record)
              + waterfall.detectJobChange                            (3/record)
5. CONTACT  → FullEnrich.findEmail — only on rows step 3 left without
              an email (fallback peopleDataLabs)                     (1–3/record)
6. VERIFY   → waterfall.verifyEmail                                  (0.1/record)
7. BACKFILL → peopleDataLabs.enrichPerson (only if step 5 missed)    (3/record)
8. QA       → scripts/contact-accuracy-audit.ts                      (free, local)
```

Two spine notes from the 8-provider stack: step 3's `aiArk.enrichPerson` **already returns a verified email**, so step 5 runs on the residue only — don't pay `FullEnrich.findEmail` (1) behind a row that already has one. And when the goal reaches a **phone**, `aiArk.findMobilePhone` (0.5, mobile-only, bills 0 on a miss) is the first rung before `prospeo` (3) / `FullEnrich` (6) / `waterfall` (7) — the guarded-lever rule in §3 still applies to all four.

Adapt by phase: drop steps that aren't relevant to the user's goal. For pure sourcing, run step 1 only. For "enrich a list I already have," run steps 2–7.

## 7) Output retrieval — use `run download-outputs`, not `run download`

When the agent needs the actual data produced by an action (enriched fields, found emails, search results), use:

```bash
cargo-ai orchestration run download-outputs \
  --workflow-uuid <uuid> \
  --output-node-slug <slug> \
  --format json
```

(Don't pass `--is-finished` — the CLI help still lists it but the API currently rejects it with `unrecognized_keys`; reported.)

Returns `{"url": "..."}` — a signed URL to a CSV/JSON containing only the output node's data. Faster and cheaper than `run download` (which pulls full run records). See [`references/output-retrieval.md`](references/output-retrieval.md) and [`../cargo-analytics/SKILL.md`](../cargo-analytics/SKILL.md).

## 8) Contact accuracy — run the QA scripts, don't eyeball

Four deterministic TypeScript scripts in [`scripts/`](scripts/) (Node ≥ 22.18, zero deps, fixture-tested in CI) replace in-context row checking. **Run the script — never re-derive its logic by reasoning over rows.** Full doctrine, pipeline order, and the SEND/VERIFY/REVIEW/REMOVE verdict semantics: [`references/contact-accuracy.md`](references/contact-accuracy.md).

- `scripts/validate-emails.ts` — free syntax/risk/duplicate cull **before** paid `verifyEmail`.
- `scripts/select-current-role.ts` — pick the real current role from an experiences array (catches job changers).
- `scripts/validate-linkedin-names.ts` — name↔profile match (catches same-name decoys); pairs with [`recipes/linkedin-url-lookup.md`](recipes/linkedin-url-lookup.md).
- `scripts/contact-accuracy-audit.ts` — final per-row `audit_action` stamp on the merged output; cite its summary counts in the receipt. Reads files or a finished run directly (`--workflow-uuid`, via `@cargo-ai/api`).

## 9) Action shape rules (every recipe)

Every action JSON in this skill follows the rules in [`../cargo-orchestration/references/examples/actions.md`](../cargo-orchestration/references/examples/actions.md):

- `kind: "connector"` action shape: `{"kind":"connector","integrationSlug":"<slug>","actionSlug":"<slug>"}`. **`connectorUuid` is NOT in `config`** — the platform resolves the workspace's authenticated connector from `integrationSlug` automatically.
- **A top-level action has no `config` — omit it.** Inputs go in `--data` / `--records`, and every recipe here writes the action without the key. That holds for `action execute`, `execute-batch`, and `get-output-schema` alike — the object `action list` returns pastes into all three. Inputs misplaced into `config` are not rejected, they are **dropped**, and the action runs with no input, so check this first when a call returns empty for no visible reason.
- **Don't hand-write a slug you're unsure of, and don't page the catalog looking for one.** `cargo-ai orchestration action list <keywords> [--integration-slug <slug>]` is free, searches every integration plus native actions, tools, and agents, and returns the action object ready to paste **with the action's credit costs** — a cheap sanity check on both the slug and the price before a paid call. When the question is *which paid actions exist for this?*, `cargo-ai connection action search <keywords> --credits-only` is the one that filters on it. Neither replaces the provider playbook below: the playbook is where the input quirks, hit-rates, and recurring-use traps live.
- For multi-step node graphs: `connectorUuid` lives at the top level of the node, not in `config`. Cross-node interpolation uses `{{nodes.<slug>.<field>}}`. Agent node outputs wrap under `.answer` (read as `{{nodes.<slug>.answer.<field>}}`).

## 10) When stuck — file a workspace report

If a recipe fails repeatedly and the cause isn't obvious, escalate via `cargo-ai workspaceManagement report create`. See [`../cargo-workspace-management/SKILL.md`](../cargo-workspace-management/SKILL.md) (Reports section).

## 11) Provider playbooks — read before you call (one-off or recurring)

**STOP — do not execute any paid action against a provider below, and do not wire a provider into a recurring play/tool node graph, until you have opened its playbook.** Each playbook carries the exact action slugs, config shapes, input quirks, and cost traps; reading it for five seconds is cheaper than one failed paid call, and a failed batch is 100 failed paid calls. The stakes are higher, not lower, when the provider goes into a **recurring** workflow: a bad config repeats on every scheduled run, and a wrong cadence re-bills the same rows forever — each playbook ends with a **Recurring use** section (schedule fit, cadence default, re-billing gates, extractors) for exactly this. **Every credits-based provider with callable actions now has a playbook, with one stated exception**: `openRouter`, which exposes a model lister rather than credits-based actions, so there is nothing to document. `brightData` and `proxycurl` gained playbooks rather than staying unlisted — an undocumented provider still shows up in the cost table, and leaving the acceptable-use framing implicit was the weaker option: [`provider-playbooks/brightData.md`](provider-playbooks/brightData.md) states the consumer-targeting refusal up front. Own-key integrations fall back to [`references/alternatives.md`](references/alternatives.md) and [`references/stage-action-map.md`](references/stage-action-map.md).

**Priority stack (recipes lead with these):**
- [`provider-playbooks/salesNavigator.md`](provider-playbooks/salesNavigator.md) — LinkedIn-native lead and account sourcing (0.2/record).
- [`provider-playbooks/aiArk.md`](provider-playbooks/aiArk.md) — LinkedIn-anchored people/company data: `enrichPerson` returns profile **+ verified email** at 0.1, `findMobilePhone` (0.5) is the cheapest phone rung, `searchCompanies` (0.01/record) does lookalikes, and `analyzePersonality` (0.05) is catalog-unique. All actions run on the managed connection.
- [`provider-playbooks/waterfall.md`](provider-playbooks/waterfall.md) — swiss-army-knife: enrichment, verification, and the cargo-unique `detectJobChange` signal.
- [`provider-playbooks/FullEnrich.md`](provider-playbooks/FullEnrich.md) — premium contact lookup; `reverseEmailLookup` is unique; `searchPeople` / `searchCompanies` and the `fetch*` extractors are free.
- [`provider-playbooks/apolloio.md`](provider-playbooks/apolloio.md) — the 1-credit niche-coverage enrich rung (person + organization); **read it before assuming Apollo is available** — only two of its eleven actions are credits-based, the rest need your own Apollo API key.
- [`provider-playbooks/theirStack.md`](provider-playbooks/theirStack.md) — tech-stack + hiring-intent signals.
- [`provider-playbooks/peopleDataLabs.md`](provider-playbooks/peopleDataLabs.md) — heavyweight backfill at flat 3-credit tier.

**Sourcing & company-data specialists:**
- [`provider-playbooks/linkedin.md`](provider-playbooks/linkedin.md) — the native LinkedIn integration's action set (profiles, companies, posts, jobs).
- [`provider-playbooks/oceanio.md`](provider-playbooks/oceanio.md) — lookalike-company discovery from seed domains, with technographic / web-traffic filters `aiArk.searchCompanies` (0.01) can't express.
- [`provider-playbooks/datagma.md`](provider-playbooks/datagma.md) — lightweight person/company enrichment alternative.
- [`provider-playbooks/companyEnrich.md`](provider-playbooks/companyEnrich.md) — cheapest company-by-domain (0.25) + per-item-billed lookalikes.
- [`provider-playbooks/enrichCrm.md`](provider-playbooks/enrichCrm.md) — CRM-record enrichment; `getFunding` is the funding-signal fallback.
- [`provider-playbooks/societeInfo.md`](provider-playbooks/societeInfo.md) — French-registry company/contact data (SIREN/SIRET).
- [`provider-playbooks/snitcher.md`](provider-playbooks/snitcher.md) — website-visitor identification; the recurring extractor is the cost trap.
- [`provider-playbooks/piloterr.md`](provider-playbooks/piloterr.md) — ultra-cheap bulk company extractor + G2 product info.
- [`provider-playbooks/g2.md`](provider-playbooks/g2.md) — software-review & category signal data.
- [`provider-playbooks/theSwarm.md`](provider-playbooks/theSwarm.md) — warm-intro network mapping to target companies/people.
- [`provider-playbooks/mixrank.md`](provider-playbooks/mixrank.md) — premium person/company backfill (4/lookup, phone-only reverse lookup).

**Email & contact specialists** (all feed the VERIFY step — see [`references/waterfall-strategy.md`](references/waterfall-strategy.md)):
- [`provider-playbooks/hunter.md`](provider-playbooks/hunter.md) — domain-search email finding + verification.
- [`provider-playbooks/prospeo.md`](provider-playbooks/prospeo.md) — email/phone lookup, LinkedIn-URL input path.
- [`provider-playbooks/icypeas.md`](provider-playbooks/icypeas.md) — budget email find/verify.
- [`provider-playbooks/findyMail.md`](provider-playbooks/findyMail.md) — email finding alternative.
- [`provider-playbooks/leadMagic.md`](provider-playbooks/leadMagic.md) — email + mobile lookup alternative.
- [`provider-playbooks/contactOut.md`](provider-playbooks/contactOut.md) — contact info from LinkedIn profiles.
- [`provider-playbooks/zeroBounce.md`](provider-playbooks/zeroBounce.md) — email-verification second opinion to `waterfall.verifyEmail`.
- [`provider-playbooks/bouncer.md`](provider-playbooks/bouncer.md) / [`neverBounce.md`](provider-playbooks/neverBounce.md) / [`kitt.md`](provider-playbooks/kitt.md) / [`enrichley.md`](provider-playbooks/enrichley.md) — verification long tail (0.3 / 0.2 / 0.05 / 0.1; enrichley's slug is `verify`, not `verifyEmail`).
- [`provider-playbooks/dropcontact.md`](provider-playbooks/dropcontact.md) — email finding with French/EU registry depth; `email` output is an array.
- [`provider-playbooks/enrowio.md`](provider-playbooks/enrowio.md) — email find (1) + verify (0.1); takes `fullName` only.
- [`provider-playbooks/reverseContact.md`](provider-playbooks/reverseContact.md) — company-from-LinkedIn (credits); profile lookups are own-key.
- [`provider-playbooks/rocketreach.md`](provider-playbooks/rocketreach.md) — person lookup (1); healthcare/NPI niche; beware the `currrentEmployer` schema key.
- [`provider-playbooks/forager.md`](provider-playbooks/forager.md) — personal-email + phone from a LinkedIn URL.
- [`provider-playbooks/cleon1.md`](provider-playbooks/cleon1.md) — terminal phone rung (15/lookup) — explicit user request only.

**Research & scraping:**
- [`provider-playbooks/firecrawl.md`](provider-playbooks/firecrawl.md) — web scraping for research/personalization stages.
- [`provider-playbooks/serper.md`](provider-playbooks/serper.md) — Google SERP queries for research and URL discovery.
- [`provider-playbooks/linkup.md`](provider-playbooks/linkup.md) — web search (0.5 standard / 2 deep) + sourced/structured answers.
- [`provider-playbooks/parallel.md`](provider-playbooks/parallel.md) — cheapest page read in the catalog (`extract`, 0.025/URL) plus `createTask`, the only action that fills a caller-supplied output schema.
- [`provider-playbooks/exa.md`](provider-playbooks/exa.md) — semantic search with a document-type `category` filter and publication-date bounds.
- [`provider-playbooks/builtwith.md`](provider-playbooks/builtwith.md) — a domain's technology stack; `getDomainSummary` is **free** and runs in front of the paid rung.
- [`provider-playbooks/x.md`](provider-playbooks/x.md) — public X posts and profiles at 0.02 an action; a signal rung, gated by acceptable use.
- [`provider-playbooks/sillage.md`](provider-playbooks/sillage.md) — inbound signal detections read back from a model, **free**, so it runs first on any signal question.
- [`provider-playbooks/brightData.md`](provider-playbooks/brightData.md) — Instagram / TikTok / Facebook / YouTube profiles by URL, 0.1 an action; the catalog's only non-LinkedIn, non-X social coverage, and the playbook opens with the consumer-targeting refusal that gates it.
- [`provider-playbooks/proxycurl.md`](provider-playbooks/proxycurl.md) — LinkedIn profile / company lookups on your own key.

**LLM providers** (all: one `instruct` action, cost per 1,000-token package, per-model tiers — prompts come from [`references/prompt-library/index.md`](references/prompt-library/index.md)):
- [`provider-playbooks/anthropic.md`](provider-playbooks/anthropic.md) — judgment-tier default (Haiku/Sonnet 0.2, Opus 2); temperature nests under `advancedSettings` with required `maxTokens`.
- [`provider-playbooks/openAi.md`](provider-playbooks/openAi.md) — cheapest bulk tier (`gpt-5-nano` 0.006) + native JSON-schema output.
- [`provider-playbooks/gemini.md`](provider-playbooks/gemini.md) — cheap high-throughput (Flash 0.01, 15,000/min) + search grounding.
- [`provider-playbooks/perplexity.md`](provider-playbooks/perplexity.md) — web-grounded research answers; default model is the expensive `sonar-deep-research` — always set `model` explicitly.

## 12) References

- [`references/cost-discipline.md`](references/cost-discipline.md) — the mandatory spend rules: pilot → approval gate, per-run receipts, 1.4×N over-provision, count-first sizing, provider-billing rules.
- [`references/contact-accuracy.md`](references/contact-accuracy.md) — the deterministic QA scripts (email cull, current-role, name match, final audit) and the SEND/VERIFY/REVIEW/REMOVE verdicts.
- [`references/prompt-library/index.md`](references/prompt-library/index.md) — ~40 named, parameterized LLM prompts (personalization, scoring, research, qualification, signal analysis, extraction). **Before authoring any enrichment/scoring prompt from scratch, grep this index** — reuse beats reinvention, and each entry carries a tested output contract. Load only the shard you need, never all of them.
- [`references/stage-action-map.md`](references/stage-action-map.md) — cheapest credits-based action per stage across the full 136-integration catalog.
- [`references/credits-cost-table.md`](references/credits-cost-table.md) — auto-generated cost table for all 176 credits-based actions.
- [`references/waterfall-strategy.md`](references/waterfall-strategy.md) — canonical waterfall chains by enrichment goal (every recipe's "fallback" follows these).
- [`references/alternatives.md`](references/alternatives.md) — provider swap-ins from the long tail when the priority stack can't serve.
- [`references/output-retrieval.md`](references/output-retrieval.md) — `run download-outputs` patterns for fetching action data.

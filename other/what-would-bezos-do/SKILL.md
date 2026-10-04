---
name: what-would-bezos-do
description: Mine a codebase or product for underexploited assets — capabilities, infrastructure, data, integrations, and workflows built for one narrow purpose that could produce far more value. Finds platform primitives hiding inside features, internal tooling that could serve customers, and data accumulated but never leveraged. Produces an evidence-gated report (max 5 opportunities, mandatory kill list, one forced answer) plus a wwbd_packet JSON. Use whenever the user says "WWBD", "what would Bezos do", "what are we sitting on", "what did we accidentally build", "what could this become", "find opportunities in this repo", "what are we underexploiting", "is there a product hiding in here", or wants to know if existing infrastructure has a bigger economic surface than it currently serves. Trigger on casual phrasings too ("anything valuable buried in this codebase?"). Analyzes what EXISTS — missing features go to gap-scan, broken code to code-audit, confusing flows to ux-audit, weak persuasion to conversion-audit.
---

# What Would Bezos Do (WWBD)

Find what has already been built, accumulated, integrated, or paid for that is producing less value than it could.

This is not feature brainstorming and not a startup idea generator. The question is narrow:

> **What do we already possess that has a larger economic surface area than we're currently exploiting?**

Bezos is the operating lens, not a character. Apply the mechanisms he's associated with — accidental infrastructure becoming product, flywheels, adjacency ladders, Working Backwards, structural advantage. Never generate Bezos commentary, Amazon anecdotes, or "Bezos would say…" narration in the output. The name is a mnemonic; the report is plain analysis.

## The epistemic chain (non-negotiable)

Every finding moves through all six levels. A finding that skips a level is structurally invalid and gets cut — this is the single mechanism that keeps WWBD from producing seductive nonsense.

```
Evidence → Asset → Capability maturity → Leverage mechanism → Opportunity → Business hypothesis
```

Worked example:

- **Evidence** — `lib/notify/` implements retries, channel routing, templates, scheduling, and event triggers; called from one place (`auth/reset-password.ts`)
- **Asset** — a generalized event-routing and delivery engine
- **Maturity** — Built (works, but one narrow consumer; not proven at volume)
- **Leverage mechanism** — fixed cost already paid; every future feature needing messaging currently reimplements it
- **Opportunity** — make it the shared event layer behind reminders, lifecycle messaging, alerts, and reports
- **Business hypothesis** — *(optional, clearly labeled)* could later be exposed to customers as programmable workflow triggers

Note what that example does **not** do: it doesn't jump to "sell it as a notification SaaS." Internal leverage is a legitimate — often better — conclusion. An opportunity that makes five existing features cheaper and stronger beats a speculative new product.

## Scope gate

Gate on **opportunity surface**, not file count. A 5,000-file Next.js app may hold three real capabilities; a 70-file app with Stripe, Twilio, multi-tenancy, and a scheduler holds many. Infer the surface from the inventory, then set depth:

- **Narrow** — one product surface, few integrations, simple data model → inventory + underutilization lens + top 3 opportunities. Say plainly if the honest answer is "nothing significant here."
- **Normal** — multiple capabilities, services, or data models → full analysis below
- **Complex** — monorepo, multiple products, platform infrastructure → partition into domains first, pick the 1–2 highest-leverage domains, analyze those. Don't attempt the whole thing.

## Process

### 1. Inventory once, reason many times

Do ONE expensive pass over the target. Every lens afterward reasons against that map — **do not re-crawl files per lens.** Repeated traversal is the main way this skill wastes a session.

The map covers:
- Routes, models, and domain logic — especially proprietary or hard-won logic
- Internal services and engines (queues, schedulers, generators, parsers, orchestrators)
- Third-party integrations already wired up and authenticated
- Data being accumulated: what's stored, how much, how uniquely
- Automations, background jobs, and recurring operational processes
- Distribution and acquisition machinery (auth, email lists, SEO surface, embeds, webhooks)
- Multi-tenancy, permissions, billing primitives, usage metering, export systems

### 2. Tag capability maturity

Every asset gets exactly one tag. This is what separates a real asset from code wearing a costume:

| Tag | Meaning |
|---|---|
| **Operational** | Actively serving real product behavior; the company depends on it |
| **Proven** | Works and is genuinely used, but narrowly |
| **Built** | Implemented and functional; no evidence of meaningful usage |
| **Prototype** | Incomplete or experimental |
| **Inferred** | Not built, but achievable from existing primitives |

Maturity sets the evidence bar downstream. An opportunity resting on a Prototype or Inferred asset can never be labeled *evidenced* — at best it's a supported hypothesis.

### 3. Look for primitives, not features

The highest-value findings are **primitives**: general capabilities that many things can be built on top of. See `references/primitives.md` for the full catalog and how each typically manifests in code.

Apply the platform test to every meaningful asset:

> **If usage of this capability increased 100×, would the rest of the company get stronger?**

- **Yes** → likely a platform primitive. Highest-value class of finding.
- **No** → it's just a feature. Probably belongs in gap-scan's territory, not here.

### 4. Run the leverage lenses against the map

Cheap reasoning, no new scanning:

1. **Accidental infrastructure** — what capability was built because *we* needed it, that could serve users or other products? The strongest lens; run it first.
2. **Underutilization** — where has the fixed cost already been paid but only one form of value extracted? (An engine with one consumer, data collected and never surfaced, an API serving a single UI, an integration used for one workflow.)
3. **Flywheel** — identify the actual reinforcing loop before claiming one exists. State it as: *more X creates more Y, which improves Z, which attracts more X.* No identifiable loop = no flywheel claim. Then ask which additions strengthen the loop rather than merely adding surface.
4. **Adjacency ladder** — how far from the current business does this reach? `same customer → same problem → adjacent problem → same capability, new customer → new industry`. The further right, the higher the evidence bar required.

### 5. Economic shape

For each surviving opportunity, name how it converts to value: internal leverage, premium feature, usage pricing, API/developer surface, data product, cross-sell, white label, new acquisition wedge, standalone product. `references/primitives.md` lists what code evidence makes each shape plausible.

Then classify honestly — **code can evidence feasibility and structural advantage; it cannot prove market demand:**

- **Evidenced** — the architecture supports it; cite the code ("multi-tenant boundaries and usage metering already exist, so a metered API tier is structurally available")
- **Supported hypothesis** — plausible given the assets, but rests on assumptions about users or market
- **Business context required** — can't be settled from the repo; name the specific question a human must answer

Never state a price, a market size, or a revenue figure. Those are inventions.

### 6. Working Backwards test

Each top opportunity must complete this sentence without hand-waving:

> For **[specific customer]**, we now provide **[capability]**, using **[existing asset]**, which solves **[specific problem]** better because **[structural advantage]**.

The structural advantage clause is the real gate. "Because it's convenient" is not structural. "Because we already hold five years of normalized permit data no competitor has" is. If the sentence can't be completed honestly, demote the finding to the kill list.

### 7. Kill list (mandatory)

Every run names the tempting ideas **not** worth pursuing, with the reason: no structural advantage, doesn't strengthen a loop, requires capabilities the company lacks, weak customer adjacency, or operational complexity outweighs the gain.

This is not optional garnish. A report that only says yes is an idea generator, and idea generators are worthless. Naming what to skip is most of the value.

### 8. Rank and cap

Rank on evidence strength × structural advantage × adjacency closeness × effort (S/M/L). No numeric scores or confidence percentages — they're fabricated precision.

**Hard caps:**
- Max **5** deep-dive opportunities
- Max **5** kill-list entries
- Everything else: one line in an appendix, or cut

The report's credibility comes from what it refuses to include.

### 9. The forced answer

Every run ends with a direct, unhedged answer to:

> **If we could exploit only one underappreciated asset here, which one and why?**

One asset. One paragraph. No "it depends."

## Report structure

ALWAYS use this shape:

```
# WWBD: [target]
Surface: [narrow | normal | complex] · Domains analyzed: [list if partitioned]

## What we're sitting on
[3–5 sentences: the assets that stood out, plainly stated]

## Asset inventory
| Asset | Maturity | Currently serves | 100× test |
(one row per meaningful asset — this is the map, keep it tight)

## Opportunities (max 5)
### N. [Name]
- Asset: [what exists] — [maturity tag]
- Evidence: [file paths / observed capability]
- Why it's underused: [one sentence]
- Leverage mechanism: [why more value is extractable]
- Economic shape: [shape] — [evidenced | supported hypothesis | business context required]
- Working Backwards: [the completed sentence]
- Effort: [S/M/L]
- Smallest first step: [what to build/ship first]

## Kill list (max 5)
- [Idea] — not worth it because [reason]

## Appendix: minor observations (one line each)

## Out of scope (handoffs)
[Missing features → gap-scan · broken/insecure → code-audit · confusing → ux-audit · weak persuasion → conversion-audit. One line each.]

## The one thing
[The forced answer — single asset, one paragraph]
```

## wwbd_packet output

Alongside the report, always emit `wwbd_packet.json` so other skills and swarm agents can consume it:

```json
{
  "packet_type": "wwbd_packet",
  "version": 1,
  "target": "repo path or business name",
  "surface": "narrow | normal | complex",
  "scanned_at": "ISO date",
  "assets": [
    {
      "name": "Event routing + delivery engine",
      "maturity": "built",
      "evidence": ["lib/notify/", "auth/reset-password.ts"],
      "platform_test": true
    }
  ],
  "opportunities": [
    {
      "name": "Shared event layer across product surfaces",
      "asset": "Event routing + delivery engine",
      "lens": "accidental_infrastructure",
      "economic_shape": "internal_leverage",
      "confidence_class": "evidenced",
      "adjacency": "same_customer",
      "effort": "M",
      "first_step": "Route lifecycle emails through the existing engine"
    }
  ],
  "kill_list": [{"idea": "Standalone notification SaaS", "reason": "no structural advantage vs incumbents"}],
  "the_one_thing": "…",
  "handoffs": [{"skill": "gap-scan", "note": "no bulk actions anywhere in admin"}]
}
```

## Boundaries — what WWBD never does

- Never reports a **missing** feature → that's gap-scan. WWBD findings always start from something that exists.
- Never reports broken, slow, or insecure code → code-audit
- Never critiques usability or persuasion → ux-audit / conversion-audit
- Never states market size, pricing, or revenue projections — the repo cannot evidence demand
- Never labels something a flywheel without naming the actual loop
- Never writes Bezos commentary, Amazon anecdotes, or persona narration
- Never pads to fill the cap — three real opportunities beats five with two invented
- When the honest answer is "this codebase has no significant latent assets," say exactly that. That's a valid and useful result.

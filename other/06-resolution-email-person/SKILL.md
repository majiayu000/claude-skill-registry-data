---
name: 06-resolution-email-person
description: >-
  Turn a company domain (plus an optional person name or job title) into a verified,
  send-safe email address - the deliverability-first "resolution" layer of a cold-email
  pipeline. Use when the user wants to find or verify a work email, enrich a list or file
  of domains into decision-maker contacts, or resolve "who is the [title] at [company]
  and what's their email." Works standalone or as Layer 06 in the API-First GTM stack.
  Cost-ordered waterfall: AI Ark → Prospeo → Blitz → Findymail with ZeroBounce
  validation; a rung is skipped when its API key is absent, and it never spends
  enrichment credit without an explicit go-ahead.
---

# Resolution - Email + Person

Turn `{domain (required), optional person_name, optional job_title}` into a **verified, send-safe email**.

The one principle that governs every decision here: **bounce rate, not find rate, is the signal that matters.** A found-but-undeliverable email is worse than no email - it burns sender reputation. So this skill optimizes for *deliverable* contacts at *minimum credit cost*, and it never spends enrichment credit without the user's explicit go-ahead.

`domain` is the one mandatory input across every tool. Everything else can be asked for, inherited from upstream, or derived.

## Provider + auth setup

Each provider reads its API key from an **environment variable** - `AIARK_API_KEY`, `PROSPEO_API_KEY`, `BLITZ_API_KEY`, `FINDYMAIL_API_KEY`, `ZEROBOUNCE_API_KEY` - never hardcode a key. This skill calls the providers with curl, and **a `.env` file is not visible to curl** - load it into the shell in the same command as the call, otherwise an empty auth header comes back as a provider auth error rather than a missing-key one:

```bash
set -a; [ -f .env ] && . ./.env; set +a
```

An exported variable or a secrets manager takes precedence and needs no prelude. **The skill runs with as few as one key set:** at startup, detect which keys are present, use only those rungs, and skip the rest (log which rungs were skipped and why). Read **`references/providers.md`** for endpoints, request shapes, billing rules, and rate limits before making any call.

- **AI Ark** - rung 0, **conditional**: runs only if `AIARK_API_KEY` is set. Two modes. **(a) Passthrough:** a row that already carries an AI Ark-verified email (source flag `ai_ark`/`pre_verified`, or the caller says the list is an AI Ark export) is accepted as-is - don't re-find what's already verified. **(b) Finder:** `POST /people/export/single` turns a **LinkedIn profile URL or AI Ark person id** (not name+domain) into a BounceBan-verified email - 1 credit per valid email, 0 on a miss. Strong on **SMB operators** where Prospeo is weak. The `POST /people` *search* bills separately (~0.5 credit per returned profile), so keep searches tightly filtered and prefer `/people/export/single`.
- **Prospeo** - title-first finder, strong on mid-market + enterprise. Charged only when a request returns results (misses are free).
- **Blitz** - domain-first finder, strong on SMB. Free on Blitz's Unlimited plan (verify your own plan before treating it as free). Two steps: `domain-to-linkedin` → `employee-finder` (native `job_level`/`job_function` filters); returns the person but not the email.
- **Findymail** - email finder by name+domain (`POST /api/search/name` - NOT `/api/find`, which 405s; see `references/providers.md`).
- **ZeroBounce** - independent email validation (`GET /v2/validate`). If its key isn't set, fall back to the finding provider's bundled verdict. Explicit `catch-all` status (no false "ok" on catch-all domains), and **unknown results consume no credit**.

## Shape of a run

Classify the input, dedupe by domain, show the estimation gate, then waterfall, validate, and emit records. The two gates below are the only fixed stops - everything else is judgment.

**Input.** Three shapes arrive: a domain + job title (confirm the title and how many people they want - don't guess the count), a domain + person name (require the full name; several people sharing it → return them all, noted), or a bulk file. Bulk JSONL from an upstream skill (01–04) is the chain standard - inherit its fields and ask only for genuine gaps. CSV/Excel: read the headers, inspect the actual cell data, remap any mislabeled columns and report what you remapped - a mislabeled column wastes credit on garbage, so reason about messy data *before* spending anything. `references/input-handling.md` has the full normalization table.

A missing domain can be derived from an email (everything after `@`) or a URL - flag the record `derived`. A *personal* LinkedIn profile URL (`linkedin.com/in/…`) is itself a person identifier and bypasses the domain requirement (resolve via Blitz email-enrichment or Findymail); a LinkedIn *company* URL is not - extract the domain from it instead.

**Dedupe.** Before anything costly, normalize each domain (lowercase; strip scheme, `www.`, paths, and sub-domains like `careers.acme.com` → `acme.com`), keep one record per domain, and report `N duplicates → M unique`. The waterfall runs once per unique company. Also check prior `runs/` folders for an already-resolved domain/person - never pay twice for the same contact.

## Gate 1 - Estimation (mandatory, before any spend)

Run cheap count/preview queries (Prospeo's search returns matches without charging on a miss) and show, before spending any enrichment credit:

1. People found for the requested titles
2. People not found
3. Closest (similar-title) people available for the not-found
4. How many have emails
5. How many have LinkedIn
6. **Credit + $ cost to enrich all**
7. Companies with zero contacts
8. **Coverage %** (found ÷ requested)

Then get an explicit yes before enriching. Never auto-proceed - this gate is what makes the skill safe to point at a 5,000-row list.

## Gate 2 - Validation-retry (optional, opt-in)

After enrichment is approved, offer one more opt-in: if a found email validates as invalid, re-run resolution through a different provider to find a working one. Make clear it **costs more than usual**, but don't run a second estimate pass (that would itself burn time/credit). Declined → validation still runs, bad emails are just flagged. Accepted → the retry loop in the validation step below is live.

## Waterfall enrichment

Order (cost-first): **AI Ark → Prospeo → Blitz (local title filter) → Findymail.** Stop the moment you land a **valid** email (found-but-invalid is not a stop condition). Skip any rung whose key is absent.

**Rung 0 - AI Ark** (only if `AIARK_API_KEY` is set): passthrough rows return `valid` with `email_source: ai_ark` and skip the paid rungs entirely; otherwise resolve via `/people/export/single` with a LinkedIn profile URL (often already on the row, or free from Blitz's employee-finder) or person id. If you must *find* the person with AI Ark's search, pin it tight (domain + full name) - search bills per returned profile - and respect the per-run credit cap in `references/providers.md`. Worth trying early for SMB-operator targets.

### Exact first, then broaden - capped at 3 attempts per company

Try the exact title strictly first; broaden to similar titles only on a miss. Misses are free on Prospeo, so trying is cheap - the cap keeps big lists from crawling.

| Attempt | Prospeo `match_mode` | Titles to send | Label a hit as |
|---------|----------------------|----------------|----------------|
| 1 | **`EXACT`** (optionally `smart_intensity: STRICT`) | the exact title (bundle all spellings in the `include` array - one call) | `exact` |
| 2 | **`SIMILAR`** | + same-seniority synonyms | `closest` |
| 3 | **`CONTAINS`** (optionally `smart_intensity: LOOSE`) | a wider same-seniority set | `closest` |

Use `EXACT` **only** on attempt 1. `person_job_title.include` takes an **array**, so all format variants of one logical title ("VP Marketing", "VP of Marketing", "Vice President, Marketing") go in a **single** call - they don't cost separate attempts.

### The same-seniority guard (this is the crux of "closest")

When you broaden, the search can hand back a *different-seniority* role. Pin the requested band at query time - both finders have a native lever: Prospeo's `person_seniority` (bands: `Founder/Owner, C-Suite, Partner, Vice President, Head, Director, Manager, Senior, Entry, Intern`) and Blitz's `job_level` (`C-Team`/`VP`/`Director`/…) - so out-of-band people never come back.

- ✅ same person: "Business Development Director" ≈ "Head of Business Development" (both `Director`/`Head` band)
- ❌ different person: "CTO" (`C-Suite`) ≠ "Director of Technology" (`Director`) - different band, rejected at query time

Only for results that arrive *without* a seniority field (a local title refine, or Findymail) do you apply the band check manually, dropping any out-of-band person before accepting them as `closest`. This guard is why broadening stays safe: you never email a junior when they asked for a chief, even though a looser title match might offer one.

### Per-tool shaping

- **Prospeo** is title-first - send `company.websites` + `person_job_title` + `person_seniority` together (free on a miss).
- **Blitz** is domain-first but keys on the company LinkedIn URL: `domain-to-linkedin` → `employee-finder` with `job_level` + `job_function` filters. It returns the person + LinkedIn but **not** the email - resolve the email separately (Blitz email-enrichment by LinkedIn, or Prospeo/Findymail by name+domain).
- **Findymail** resolves the email by name+domain.
- If they asked for 1 and a rung returns several: prefer **exact title → most senior → highest confidence**.

## Validate, then be honest about the verdict

Validate every obtained email (ZeroBounce, or the provider's bundled verdict) - validation always runs, and **no email is ever presented as confirmed without it**.

- **valid** → done. Return it.
- **catch_all / risky** → accept but flag as `catch_all` (catch-alls are often the real address; don't throw away a likely-good contact - and don't upgrade the flag to valid).
- **spamtrap / abuse / do_not_mail** (ZeroBounce-specific) → never email; treat as hard invalid and record the `sub_status` in `note` - hitting a spamtrap is worse than a bounce.
- **hard invalid** → if Gate 2 was accepted, re-run resolution excluding the provider that produced the bad email (naturally capped at the number of providers). Otherwise return it flagged `invalid` - never pass it off as usable.
- **all providers exhausted, still invalid** → return `no_email`. Do not invent a generic `info@`/`owner@`.

### Accuracy boosters

- **Email-pattern inference:** one *verified* email at a domain teaches you the company's pattern (`first.last@`, `flast@`). Generate candidates from it for the people the providers missed, and validate them - "not found" becomes "found + verified" cheaply. Label the source `pattern_inferred`.
- **LinkedIn freshness check:** before trusting a `closest` match, sanity-check the person's current LinkedIn title against the requested one (finder caches go stale). Role changed → flag it in `note` rather than emailing the wrong person.

## Output contract

Return one record per contact:

| Field | Values |
|-------|--------|
| `company`, `input_domain` | - |
| `person_name`, `linkedin_url` | - |
| `requested_title`, `matched_title` | - |
| `match_type` | `exact` \| `closest` |
| `email` | resolved address (empty if `no_email`) |
| `email_source` | `ai_ark` \| `prospeo` \| `blitz` \| `findymail` \| `pattern_inferred` |
| `verification_status` | `valid` \| `catch_all` \| `invalid` \| `no_email` |
| `confidence` | 0–100 (combine verdict + match_type + freshness) |
| `note` | optional flags - stale title, `derived` domain, etc. |

When this skill runs in the chain, **add** `verification_status` - do not overwrite the upstream `confidence` field.

Write results as `records.jsonl` under `runs/<run-id>/` per `headless-gtm-shared/CONVENTIONS.md` (CSV is an optional, derived human export). End with a **run summary**: companies in · unique after dedupe · processed · found / not found · coverage % · breakdown by `match_type` and `email_source` · any rows skipped, with the reason - a row you couldn't process is reported, never silently dropped.

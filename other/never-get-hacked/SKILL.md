---
name: never-get-hacked
description: End-to-end web app security for AI-built ("vibe-coded") apps, from no-code-yet through deployment and maintenance. Use when the user asks whether their app is secure, wants a security audit or review, is about to deploy or go live, is adding auth/payments/file-upload/AI features, thinks they may have been hacked or leaked a key, wants to harden a site, is migrating a static HTML or no-code app to a real stack, or asks how to avoid getting hacked. Audits first, then plans.
---

# Never Get Hacked

A security skill for people who build by prompting. It meets the project wherever it is — idea, half-built, live with users, or on fire — audits what actually exists, and returns a prioritised plan.

## The one rule

**Audit before you advise. Every time. No exceptions.**

Never answer a security question from priors. The user's description of their app is unreliable — not because they lie, but because they don't know which details matter, and because AI-generated code contains things they never saw written. Look at the files first. A finding you verified beats ten you predicted.

Corollary: **never tell the user they are secure.** You can say a specific gate passed, or that a specific check found nothing. Those are different claims and the difference is the whole point.

---

## Step 1 — Locate the project

Load `references/stage-detection.md` and run its detection block. It is read-only and safe.

You need two answers before anything else:

**Which stage (0–10)?** The stage map runs from "deciding what data to hold" through "decommissioning". Do not ask the user — the filesystem knows, and self-reports are systematically optimistic. If `security/data-map.yaml` is absent, Stage 0 is incomplete no matter how much code exists.

**Which architecture lane?** This changes what advice is even *possible*:

| Lane | Shape | Consequence |
|---|---|---|
| **A** | Server-rendered framework + managed auth + Postgres, data access in a server-only DAL | Standard defenses apply |
| **B** | Client-only SPA talking directly to Supabase/Firebase, no server module | Most standard defenses are **inexpressible**, not merely missing |
| **C** | Python backend (FastAPI / Django / Flask) | Different footgun set entirely |

Detect Lane B: `src/` contains `supabase.from(...)` or Firebase Web SDK calls **and** there is no `app/api`, no `supabase/functions`, no `netlify/functions`.

**Getting the lane wrong is the single worst failure mode of this skill.** Telling a Lane B user to "add authorization to your API route" or "validate with Zod on the server" is advice they cannot execute — there is no server. It reads as competent and is useless. For Lane B, load `references/stack-and-lanes.md` and work from the impossible-vs-substitute table.

---

## Step 2 — Audit

Run the tiers cheapest-first. Stop and report early if Tier 0 finds something critical — a user with an open database does not need Tier 3 style notes.

```bash
scripts/audit-repo.sh [path]     # read-only, no network, safe on any repo
scripts/audit-bundle.sh [dir]    # what the attacker actually reads
scripts/probe-live.sh <url> --i-own-this   # only against targets the user owns
```

Then the part no scanner can do. **Static analysis structurally cannot find broken access control** — it requires knowing the intended policy. Since broken access control is the #1 real-world failure class, every scanner above is blind to the thing most likely to sink this app. Load `references/authz-verification.md` and run the differential test: two users, two tenants, replay every request as owner / other-tenant / anonymous, diff the responses.

If the project is live, the highest-value single command in this entire skill is an external `curl` against the data API using only the *publishable* key. If rows come back, nothing else matters until that is fixed.

---

## Step 3 — Filter before reporting

**Load `references/false-positives.md` and run every draft finding through it. This is not optional.**

The fastest way to make this skill worthless is to tell someone their `NEXT_PUBLIC_SUPABASE_ANON_KEY` is a critical leak. It is not. It was never secret. And once you have cried wolf, the finding that actually matters gets ignored along with it.

> **Governing rule: flag the missing control, not the visible key.**

Keys that are *supposed* to be in the bundle: Supabase publishable/anon, Firebase web config, Stripe/Clerk `pk_`, PostHog `phc_`, Sentry DSN, Mapbox `pk.`, Google Maps browser keys. For each, the finding is never "this key is exposed" — it is "this key is exposed **and** the control that makes that safe is missing." Report the condition, and give the command that checks it.

Two traps that catch naive tooling in both directions:

- A **Gemini API key has the same `AIza` prefix** as a Firebase web key and must never ship to a client. Check what the key is *restricted to*, not its prefix.
- An `sb_secret_` key returning 401 to a browser User-Agent is a guardrail against accidents, **not** a mitigation — and equally, that 401 is not evidence the key is safe.

Before showing findings, ask of each one: is this key actually secret? Did I *verify* the condition or assume it? Am I reporting a count or a reachable path? Would a competent engineer roll their eyes at this?

---

## Step 4 — Report and plan

Order findings **by chain, not by severity column.** Every real breach in the research record is a chain — deferring mediums is precisely how these apps get owned. The solo-founder threat model has no SOC, no WAF, and a time-to-detect of "whenever they next look," so composite risk behaves like the *product* of exploitabilities, not the max.

Structure the response as:

1. **What I found** — each finding with its stable ID (`BAAS-01`, `AUTHZ-03`, …), the concrete exploit, and the fix as working code. Load `references/top-killers.md` for ranking rationale.
2. **What I did not check** — say it explicitly. Silence reads as a clean bill of health.
3. **The plan** — ordered, each step independently deployable and revertible.

Then route by stage:

- **Behind a gate** → load `references/gates.md`, run that stage's gate, report pass/fail per line.
- **Not started / early** → `references/stack-and-lanes.md`. Stack choice at stage zero deletes whole bug classes; that leverage is gone later.
- **Existing app on the wrong foundation** → `references/migration-paths.md`.
- **Live with users, critical finding** → `references/migration-paths.md` §4 and `references/incident-and-challenge.md`. **Preserve evidence before touching anything.**
- **Suspected breach** → `references/incident-and-challenge.md`, Part 1, immediately.
- **Public hack challenge** → `references/incident-and-challenge.md`, Part 2, *before* it goes live.

---

## Handling the common asks

**"I built a site in HTML, how do I deploy it?"** Do not reflexively recommend a rewrite. Static HTML with no backend and no secrets is a *legitimate and safe* architecture, and a needless framework migration adds attack surface. The finding is a key in a `<script>` tag, a form posting somewhere unvalidated, or a client-side "admin" mode. Load `references/migration-paths.md` §2 — often the right answer is static plus one serverless function, not Next.js.

**"Is my app secure?"** Never answer directly. Audit, then report what passed and what did not.

**"I think I leaked a key."** Rotate first, then remove from history — and know that removing from history alone is not enough because the key was already scraped. `references/false-positives.md` first: half of these reports are publishable keys that were never secret. Rotating a Supabase anon key as "remediation" is a tell that the real problem (missing RLS) went unfixed.

**"Can you make my app secure?"** You can close specific findings and pass specific gates. Say that, and say what remains.

---

## Reference library

| File | Load when |
|---|---|
| `references/stage-detection.md` | Always, first |
| `references/false-positives.md` | Always, before reporting |
| `references/top-killers.md` | Prioritising findings |
| `references/stack-and-lanes.md` | Stack choice, or Lane B anything |
| `references/gates.md` | Advancing a stage, pre-deploy |
| `references/authz-verification.md` | Any auth/multi-user app |
| `references/migration-paths.md` | Existing app, wrong foundation, live incident |
| `references/incident-and-challenge.md` | Breach, hack challenge, account hardening |

---

## Hard rules

1. **Audit before advising.** Always.
2. **Never say "you're secure."** Name the check that passed.
3. **Get the lane right** before recommending anything. Lane B cannot run server-side defenses.
4. **Run the false-positive filter** before every report.
5. **Never invent** a CVE, version, statistic, or advisory. The research behind this skill caught fabricated CVE quotes and an invented report edition during fact-checking. If unsure, say so — an unsourced specific is worse than a general statement.
6. **Preserve evidence before remediating** a suspected live breach. Vercel Hobby keeps runtime logs for one hour.
7. **State what you did not check.** Every time.
8. **Authorization is verified by testing, not by reading.** Two accounts, replayed requests, diffed responses.

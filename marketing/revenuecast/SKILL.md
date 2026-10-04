---
name: revenuecast
category: publishing
description: >-
  revenuecast — turn a real-world capability into a self-demonstrating,
  high-throughput generative-AI revenue engine (the "Kleos" method). It is "/skillify for revenue":
  skillify turns a workflow into a tested skill; revenuecast turns a capability into a
  revenue engine whose own output IS the advertisement. The bstack-native
  composition of the 2026 "show-then-sell-the-system" creator loop (realosias,
  aivideoskool, GenHQ): Brand-Lock -> Show -> Distribute -> Hook -> Sell -> Moat,
  where the showcased output's desirability + accessibility-via-AI creates demand
  for the method, and you monetize the reproducible system. Composes content-engine
  (the factory), content-creation, blog-post, seo-llmeo, arcan-glass,
  social-intelligence, strategy-skills, and symphony/arcan (autonomous runtime).
  Its deterministic core (scripts/revenuecast_check.py) gates an engine-instance manifest
  on the design canon — own-the-audience, a real moat (not leakable prompts), the
  compliance/survival pillar (FTC v. Air AI / EU AI Act Art.50 / NO FAKES), and the
  Ritual-vs-Substance rule (no "self-improving" claim without a built+measured
  mechanism). USE WHEN turn this expertise into content/revenue, content
  monetization playbook, sell the method that produced the proof, build a
  self-demonstrating AI content brand, capability-to-revenue-engine, faceless AI
  content business, Skool/Whop offer ladder, "revenuecast", "/revenuecast". NOT FOR packaging a
  workflow as a skill (use /skillify); ingesting an external artifact (use
  /checkit); a single blog post or one-off asset (use /blog-post or
  /content-creation directly).
---

# revenuecast — turn a capability into a self-demonstrating revenue engine

`/revenuecast` is the **verb** that turns *what you can do* into *a machine that makes the
world want it*. You have a real capability — a craft, an expertise, a running
system. revenuecast builds the loop where the capability's **output becomes its own
advertisement**, and the demand that output creates is monetized by selling the
**reproducible method**. It is `/skillify` for revenue: `skillify` makes a workflow
permanent; **revenuecast makes a capability *monetizable* and *self-propagating*.**

It operationalizes the **Kleos** method (κλέος — renown that propagates by being shown);
the full playbook is `references/playbook.html`.

It is a **composition skill** — like `/checkit`, `/autonomous`, `/skillify`. It fires
existing primitives and skills in sequence. **It reimplements nothing** — the content
factory is `content-engine`; revenuecast is the *business-model layer above it*.

Full design rationale (research-grounded, P20-reviewed): **`references/design-canon.md`**.

## The one rule

> **The SHOW is the scarce asset — sell the running engine, never "the method."**
>
> Whop's own data: 88% of products earn $0, median earner $74/mo, top 1% take 57%.
> That power law *proves* the bottleneck is distribution + taste + a *running* engine,
> not the prompts (everyone has those; they leak in days). revenuecast sells the
> self-demonstrating engine that produces the SHOW — the one thing a copycat can't
> fake because faking it requires possessing the engine.

## The flywheel (each stage composes an existing skill)

```
0 BRAND LOCK → 1 SHOW → 2 DISTRIBUTE → 3 HOOK → 4 SELL → 5 MOAT ↻
```

| # | Stage | Composes |
|---|-------|----------|
| 0 | **Brand Lock** — distinctive aesthetic that makes output self-demonstrating | `content-engine` (`content-engine-dna`) · `arcan-glass` |
| 1 | **Show** — high-volume on-brand output AS the ad; clear the retention gates | `content-engine` · `brainrot-for-good` · `content-creation` (Remotion + TTS) |
| 2 | **Distribute** — raw-per-platform to ≥3 surfaces + 1 owned; X = authority layer | `content-engine-loop` · `blog-post` · `seo-llmeo` · `social-intelligence` |
| 3 | **Hook** — Zeigarnik incompleteness + comment-to-DM → owned email list | `social-intelligence` · ManyChat-class rail |
| 4 | **Sell** — the offer ladder; paid challenge as proof engine; annual billing | `strategy-skills` · `Sales` · `finance-substrate` |
| 5 | **Moat** — sell the non-leakable layers; crystallize wins back into Stage 0 | `bookkeeping` (P6) · `symphony`+`arcan` (L3 runtime) |

## Pipeline (what `/revenuecast <capability>` does)

1. **Frame the capability + niche.** What can you do that produces a *desirable,
   showable* output? Name the buyer. (For the agent-OS/RCS persona, the default is the
   agentic-dev wedge — see `references/design-canon.md` §7.)
2. **Pick the moat** (the Moat Picker, canon §3): sequencing · recency-as-service ·
   community · agency-proof · compliance · closed-execution. **Never prompts/templates.**
3. **Lock the brand** — fire `content-engine compile` to produce the brand DNA +
   synthetic-persona sheet + 4-layer prompt skeleton. (`arcan-studio` is pre-compiled.)
4. **Design the offer ladder** — the **v1 wedge only**: free showcase + lead magnet →
   tripwire → one recurring community. Earned tiers (challenge, VIP, license) are a
   *hypothesis to earn after measured conversion*, not a blueprint to build now.
5. **Wire the compliance pillar** (canon §5) — disclosure-labeling, likeness-firewall,
   earnings-claims discipline, spend-cap, ≥3-platform diversification. **The seller is
   the entity the FTC sues** — harden your own surfaces first.
6. **Write the manifest** `revenuecast.manifest.yaml` (copy `templates/`), then
   **gate it**: `python3 scripts/revenuecast_check.py revenuecast.manifest.yaml`. A capability that
   doesn't pass all gates is not a revenue engine — it's content that happens to exist.
7. **Run the loop** — generate (content-engine) → distribute → measure (bookkeeping P6)
   → refine. For autonomous operation, that is **Layer 3** — the runtime spec at
   `references/runtime-spec.html`, **deferred until the funnel proves demand**; the
   Rust daemon graduates to its own deploy repo only when actually built (canon §7).
8. **Document proactively** (P6) — file the instance as a KG `project/` entity; report.

## The deterministic gate (`scripts/revenuecast_check.py`)

Mirrors `skillify_check.py`: presence is not correctness, so the doctor executes the
canon §9 gates against a manifest. Required gates G1–G6 set the exit code:

| Gate | Enforces | Closes the failure mode |
|---|---|---|
| G1 Identity | `capability` + `brand.name` + `brand.gloss` | a name nobody can decode (the Kleos gloss requirement) |
| G2 Ladder | free + paid + **recurring** | one-time products with no durable spine |
| G3 Own-the-audience | `distribute.owned_channel` | platform reach is rented (YouTube wiped $10M/yr in 2026) |
| G4 Moat | not `prompts`/`templates` | the template-seller death spiral |
| G5 Governance | disclosure + likeness-firewall + earnings-substantiation + spend-cap + ≥3 platforms | FTC v. Air AI ($18M + lifetime ban) / EU Art.50 / NO FAKES |
| G6 Substance | `self_improvement.claimed` ⟹ `built && measured` | **incantation vs control** (CLAUDE.md §Ritual-vs-Substance) |
| G7 KPI honesty | benchmarks ⟹ `kpis.imported` block | consumer-niche numbers presented as validated B2D targets |

## Composition map

| Step | Composes |
|---|---|
| Frame + moat | `strategy-skills` · `references/design-canon.md` (§3 Moat Picker) |
| Brand lock | **content-engine** (`content-engine-dna`) · `arcan-glass` |
| Show / generate | **content-engine** (cinema/autopilot) · `brainrot-for-good` · `content-creation` · `Remotion` · `omnivoice` |
| Distribute | `content-engine-loop` · `blog-post` · `seo-llmeo` · `social-intelligence` (`x-outreach-strategy.md`) |
| Sell / economics | `strategy-skills` · `Sales` · `finance-substrate` |
| Gate | `revenuecast_check.py` (this skill) + `skillify` discipline |
| Autonomous run (L3) | `symphony` + `arcan` + `agentic-control-kernel` + `.control/policy.yaml` + `persist` (P12) + `bstack wave` (P19) |
| Measure / crystallize | `bookkeeping` (P6) · `agent-consciousness` |

## Anti-rationalization

| Excuse | Reality |
|---|---|
| "I'll sell the prompt pack — that's the product." | Prompts leak/clone in days. G4 FAILs a prompts moat. Sell the running engine + the non-leakable operational layers. |
| "The output is self-improving / the loop rewrites itself." | Not unless it is **built AND measured**. G6 FAILs the claim otherwise — it is an incantation (CLAUDE.md §Ritual-vs-Substance), the exact failure this workspace warns against. |
| "These conversion numbers (70% completion, $1,800 LTV) are my targets." | They are consumer-niche benchmarks, unvalidated for your buyer. Quarantine them in `kpis.imported`; measure your own from zero. |
| "Compliance is a footnote / disclaimer." | The **seller** is who the FTC sues (Air AI: $18M + lifetime ban). G5 makes the compliance pillar mandatory. |
| "Build the autonomous publishing daemon first — it's the cool part." | L3 is over-capitalized before the funnel proves demand. Validate with manual posting + content-engine; build the daemon only after T1 converts. |
| "Skip the gloss, Kleos sounds cool." | Buyers won't decode κλέος. Every surface carries "your work, made famous by showing it" until the proof content teaches the word. |

## Scope

- **In scope**: any real capability/expertise/running-system whose *output is
  showable* and whose *method is sellable* — turning it into the show-then-sell loop.
- **Out of scope**: packaging a workflow as a skill (`/skillify`); ingesting an
  external artifact (`/checkit`); a one-off blog post or asset (`/blog-post`,
  `/content-creation` directly).

## References (self-contained — bundled with the skill)

- `references/design-canon.md` — the SSOT (thesis, flywheel, Moat Picker, offer
  ladder, compliance pillar, the three layers, composition map, the gate). Read first.
- `references/playbook.html` — **the Kleos playbook** (L1, Category-C): the canonical,
  shareable articulation of the method (flywheel SVG, Moat Picker, offer ladder, gate).
- `references/l2-agentic-dev-wedge.html` — the L2 applied wedge (governance-is-scarce;
  the governed-vs-ungoverned cornerstone; authority-rail-first).
- `references/runtime-spec.html` + `references/runtime-status.md` — the L3 autonomous
  runtime spec (DEFERRED/EARNED — build only after L2 validates demand).
- `templates/revenuecast.manifest.example.yaml` — a passing manifest = the L2 dogfood instance.
- `scripts/revenuecast_check.py` + `tests/test_revenuecast_check.py` — the deterministic gate.
- Provenance: research workflow `wf_d25abca6-6bf`; **BRO-1429** (the Kleos method) +
  **BRO-1436** (the Casting operator / `revenuecast` naming, `[[casting]]` KG node).

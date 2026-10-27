---
name: dev-job-defense-ties
description: >-
  Evaluating a dev job, studio, or employer? Before taking it, screen who the
  work actually serves — is it military/defense behind civilian language, and is
  the buyer one your red line rules out? Runs cui-bono for the buyer-chain, then
  classifies by end-use and buyer-nationality against YOUR threshold. Ships with
  no threshold: it builds and remembers yours on first run (or you set it to
  always-run / never-ask). Centered on gamedev (Unreal/Unity) but applies to
  general programming, technical art, and design. Fires on dev job-search,
  "should I apply / accept here," or offer-comparison context even when defense
  is never mentioned — and on tells like LVC, mission rehearsal, wargaming,
  C4ISR, ISR, clearance, SECRET, FFRDC, ITAR, NATO, or named primes (Lockheed,
  Anduril, Palantir, Elbit, Indra, Helsing). Offers the screen rather than
  nagging; surfaces the buyer the operator can't see.
---

# Screen a Dev Job for Defense Ties

**Seed question:** *Behind a gamedev, programming, or design job — whose military does it actually feed, and is it a buyer the operator has ruled out?*

> *Relentless self-reflexive dialectical thinking that questions its own premises.*

## Core Capability

Euphemism can disguise *what the work is*. It can't disguise *who the work is for*. This skill follows the buyer to the end user until the civilian framing collapses, then classifies the role on two axes — end-use and buyer-nationality — against **the operator's own red line**. It returns a go/no-go that is legible (states the threshold it applied) and falsifiable (names the one fact that would flip it).

**Scope.** Centered on gamedev — game-engine work (Unreal/Unity), C++, gameplay, real-time-3D, simulation — because that's where disguised-defense roles cluster densest. But it applies with equal force to general programming, technical art, design, and adjacent roles. **The job title is not the gate; the buyer is.**

## Three parts: mechanism, domain, profile

This skill is deliberately split so it's a reusable instrument, not one operator's politics hard-coded into a public plugin (see `ARCHITECTURE.md`):

- **Mechanism (this file, fixed):** the buyer-chain, the two-axis classification, the verification pass, the output format, and the onboarding logic below.
- **Domain (ships):** the lexicon, prime/buyer name-list, and end-use ladder — public OSINT, the *subject* the screen scans for. Default **`reference/domain-dev.md`** (field-agnostic, pre-scoped to dev); **`reference/domain-gamedev.md`** is an example overlay that *extends* it for game-engine work. Install overlays into `<config>/domain/`; swap the domain for another field without touching the mechanism.
- **Profile (yours, NOT shipped):** your **threshold** (red line), engagement preference, and field — stored as decoupled elements (`profile/threshold`, `profile/settings`) **outside** the plugin. The skill ships *profile-less*: it applies no politics until you supply a threshold.

The config store is managed by `scripts/config.py` (the model drives it; the user never runs it). `reference/PROFILE.template.md` shows the profile shape; cui-bono's *Framework Clarification* and **dialectic-spiral** derive and stress-test a threshold.

## Profile & first run

`scripts/config.py` is the deterministic store — get its live interface first, then read the profile:

```
python3 "${CLAUDE_PLUGIN_ROOT}/skills/dev-job-defense-ties/scripts/config.py" describe
```

Read `profile/settings` and `profile/threshold` (`config.py get profile/settings`), then act on the **engagement** mode:

- **`engagement: always`** — run the screen with the saved threshold, no prompt.
- **`engagement: never`** — only run when the user invokes the skill explicitly; otherwise stay silent.
- **`engagement: ask`** (or invoked manually) — proceed. If the user has accepted several runs in a row, offer once to switch to `always`.
- **No profile yet (`get` returns `NO_ELEMENT`) → onboarding:**
  1. *(skippable, non-dev-safe)* "If you've used this before and saved a config elsewhere, point me at it — if that means nothing to you, ignore it and we'll continue." Only on a yes: `config.py set-location <dir>`. Never make a non-dev run anything.
  2. **If auto-triggered**, one opt-in: *"Want me to screen who this job actually serves — military/defense ties behind the civilian framing?"* Decline → offer to save `engagement: never`. (Skip when invoked manually.)
  3. **Name the default's scope once, then build the threshold.** Up front, plainly — *the shipped defaults assume you're in the cultural West **and** the employer is Western (US / EU / Israel): that's where the name-list and verification sources are detailed, and they're deliberately thin on non-Western employers (China, Russia, Gulf, Turkey, South Korea, India).* If either assumption doesn't fit — you're outside that vantage, or the employer is non-Western — say so and we extend the pack (`domain-dev.md` carries a starter non-Western set; per-region overlays are the fuller fix). Then ask 2–4 precise, non-intrusive questions — *not all required*: absolute-no buyers (states/militaries) vs. kind-of-work (lethality vs. training); line on the end-use ladder; field (default dev — offer to install the **gamedev** overlay if they're in games).
  4. **Persist** — "Remember? all / threshold-only / no" + "engagement: always / ask / never." Save each element separately (shape per `reference/PROFILE.template.md`):
     ```
     printf '%s' "<threshold>" | python3 ".../config.py" put profile/threshold
     printf '%s' "<settings>"  | python3 ".../config.py" put profile/settings
     ```
     Field is fine to remember unprompted; the red line is worth confirming. The store is OS-agnostic and refuses `/tmp` and the plugin cache.

**Edit in place, don't recreate.** To change one thing — "add X to my hard-stops," "switch me to always," "install the gamedev overlay" — `get` that single element, amend it, `put` it back. Decoupled elements mean siblings are never disturbed.

**Invoked with arguments?** A URL / company name is the screen target; `field=…` / `threshold=…` are per-run overrides. Args are fuzzy — infer intent; ask only what you can't.

## When This Applies

**TRIGGER** (offer the screen — don't wait to be asked):
- A dev job / studio / employer is being evaluated: "should I apply / accept here," comparing offers, vetting a company as an employer — **even when defense is never mentioned** (the user may not think to ask).
- A "simulation / digital twin / XR training / decision support / situational awareness" company whose customer is vague.
- Domain-pack tells fire (Step 1), a clearance/nationality gate appears (Step 2), or a named prime shows up in the chain (Step 3).

**DO NOT TRIGGER / skip quietly:**
- General company research with no employment decision attached, or non-job contexts (this is a hiring filter, not a geopolitics explainer).
- After Step 1, the role is **clearly civilian** with no defense signal — say so in one line (or stay silent on `never`); don't manufacture suspicion or nag.
- `engagement: never` and the skill wasn't invoked explicitly.

---

## Step 0 — Run cui-bono first (the "call another skill" move)

Load and run **cui-bono** on the target. From its beneficiary and ownership mapping, resolve the buyer-chain — these three roles feed everything below:

- **Direct customer** — who signs the contract / pays the salary?
- **End user** — who operates the deliverable in the field?
- **Beneficiary** — whose capability increases because this exists? (cui-bono's native output — start here.)

If cui-bono cannot name a customer, that's **absence of evidence, not evidence of stealth**. Absence *is* a signal — but a signal to **look harder**, not a verdict: cleared/stealth work hides its customer, yet general-purpose tooling (an engine, a library) simply has no single one. Tag it **UNVERIFIED**, tell the operator what's unresolved, and carry the chain to the specific product the job actually works on — never let absence settle into "defense" or "clear" on its own.

## Step 1 — 60-second lexicon scan

Scan the ad/site text against the **active domain's lexicon** — the default `reference/domain-dev.md` plus any installed overlays (e.g. `domain-gamedev.md`, or files in `<config>/domain/`). None of the tells is individually disqualifying; they re-route you to verification. The pack carries the mil-sim dead-giveaways, the dual-use soft tells, and the "defense slipped mid-list" camouflage move.

## Step 2 — The highest-signal filter: clearance / nationality gate

A clearance or citizenship requirement (the pack lists the US and EU forms) is near-decisive. It isn't name-smell — it's the buyer stating its own end-use outright, the hardest evidence on offer. If present → **DEFENSE-CONFIRMED** regardless of how the role reads; go to Output.

## Step 3 — Name-recognition, tagged by nationality

Match the buyer-chain against the pack's prime/buyer name-list. **Follow the chain to the end user, not the contracting prime** — the nationality that matters is who *operates* the deliverable, and an EU prime's export sale can reach a different end user one layer down. Tag the nationality; it feeds Axis 2, which the threshold evaluates.

## Step 4 — Verify (5 minutes; do not skip on a soft tell)

Use the pack's verification sources — contract registries (USAspending.gov, SAM.gov, TED) outrank any aggregator; plus the company's Customers/About page, leadership LinkedIn, and a targeted search. Note **subsystem entanglement** (US/Israeli content inside a national platform) and which layer the *role* sits on.

---

## Two axes, not one

End-use is one axis; buyer-nationality is the other — they carry different weight, because the objection isn't only to lethality, it's to *whose power the work feeds*. A benign-looking trainer built for a ruled-out buyer still fails: mild end-use doesn't launder the beneficiary. Classify on both.

- **Axis 1 — end-use:** place the role on the pack's end-use ladder (`CIVILIAN ── DUAL-USE ── TRAINING/SIM ── ISR/SURVEILLANCE ── C2/TARGETING ── LETHALITY`), don't binary it.
- **Axis 2 — buyer-nationality:** who is the direct customer, end user, or beneficiary, under whose flag.

## Apply the threshold

Load the operator's threshold from their profile. **If there is none, you onboarded above** — never invent one. The threshold is *theirs*: state which line you applied in the output, and apply it faithfully. **Do not substitute your own.** A different operator draws the line elsewhere — deriving a different line is a first-class use of this skill, via cui-bono's Framework Clarification + dialectic-spiral.

**Don't over-resolve.** Match the verdict to the evidence: an unresolved or thinly-sourced buyer-chain is UNVERIFIED → INVESTIGATE, not rounded up to a hard stop or down to clear. State the **residual uncertainty** — what's still unknown and what would resolve it — rather than presenting the call as cleaner than it is. This borrows `iterative-verification`'s rule (*no confirmation = UNVERIFIED, not DISCONFIRMED; escalate only on specific counter-evidence*) and cui-bono's graduated, trade-off-stating posture, applied to the buyer-chain.

## Output format

```
TARGET: <company / role>
BUYER CHAIN (resolved via cui-bono): direct customer → end user → beneficiary
BUYER NATIONALITY: <flag(s); note if via parent/subcontract>
SIGNALS FIRED: <lexicon hits / clearance gate / name match / list-camouflage>
END-USE LAYER: <where the role sits on Axis 1>
EVIDENCE TIER: CONFIRMED (registry/customer page) / UNVERIFIED (aggregator or inference) / DISCONFIRMED
VERDICT vs ACTIVE THRESHOLD: <as defined in the operator's profile; CLEAR / INVESTIGATE / OUT / HARD STOP>
WHAT WOULD CHANGE IT: <the one fact that would flip the verdict, + where to find it>
```

Keep the buyer-chain and the "what would change it" line always — they make the screen reusable and falsifiable.

## Worked examples

These illustrate the mechanism under an *example* profile (yours may differ).

**EU prime → hard-stop export.** A "Spanish naval systems" studio advertises Unreal work on a "crew training visualization" product — reads benign. But the chain runs studio → Navantia → Avante 2200 corvette program → **Royal Saudi Navy** (CONFIRMED, public program). End-use is TRAINING/SIM (benign end of Axis 1). Under an example profile whose hard-stop includes US-aligned Gulf end users *including via EU export*, the verdict is **HARD STOP** — benign end-use doesn't launder the beneficiary. *What would change it:* if the deliverable served only the Spanish Navy's own hulls → drops a tier. The lesson: a "Spanish defense" job can be a Saudi job one layer down.

**Civilian "digital twin" that launders ISR** *(illustrative composite)*. A startup hiring "Unity engineers for a real-time digital twin — situational awareness for public safety." Zero mention of military, but soft tells fire, so Step 4 is mandatory. The customers page shows a US prime's logo → end user UNVERIFIED. End-use sits at ISR/SURVEILLANCE, the ambiguous middle. Verdict: **INVESTIGATE** — a logo is marketing, not a contract; don't auto-clear, don't hard-stop on a logo. *What would change it:* a USAspending.gov/SAM.gov award tying it to a DoD purpose code → escalate; a confirmed all-civilian customer base → CLEAR. The lesson: the soft tell is the prompt to run the registry, not the verdict.

## Integration

| Skill | Relationship |
|-------|-------------|
| **cui-bono** | Step 0 dependency — run it first; this skill consumes its buyer-chain, then applies the operator's threshold + a domain pack it doesn't carry by default. cui-bono's *Framework Clarification* is the template for deriving the threshold. |
| **cui-bono / lenses/weapons.md** | The contract-registry + revolving-door techniques are the verification engine for Step 4. |
| **cui-bono / lenses/geopolitical.md** | Source of the buyer-nationality / multi-polar framing behind Axis 2. |
| **dialectic-spiral** | Stress-test a threshold before adopting it — generate the opposite of the proposed red line and see whether it survives. |
| **deep-investigation-protocol** | Escalate here when the buyer is genuinely hidden (stealth/cleared work) and a 5-minute verify isn't enough. |
| **manufactured-consensus-detection** | When "trusted by industry leaders" / press is the only evidence of a customer, test whether that consensus is real before treating a logo as a buyer. |
| **source-omission-analysis** | What the careers page *omits* (named customers, end-use, who operates the deliverable) is the signal — apply omission analysis to the job ad itself. |
| **iterative-verification** | When the buyer-chain comes up empty or thin: the evidence-honesty discipline — *no confirmation = UNVERIFIED, not DISCONFIRMED* — and iterate before concluding rather than letting a verdict outrun the evidence. |

**Workflow position:** invoke when an employment/engagement decision is attached to a tech or creative role. Load profile → run cui-bono (Step 0) → classify (Steps 1–4) → output against the operator's threshold. Escalate to DIP only when the buyer stays hidden after Step 4.

## Self-Reflexivity

This skill ships **profile-less** on purpose: the politics (the red line) and the field (the domain pack) are swappable parameters held in the operator's profile and the pack, not facts baked into a public artifact. Standing failure modes:

- **The lexicon and name-list go stale and over-fire.** Primes get acquired and renamed; broad terms (`targeting`, `autonomy`) catch civilian work too — the `test_screen_efficiency.py` corpus exists to keep precision honest as the pack changes. A keyword match is a prompt to verify, never a verdict.
- **The buyer-nationality axis is a political map.** Whose military counts as a hard stop is the operator's call, surfaced as their threshold — don't present the map as the territory, and don't substitute your own line for theirs.
- **The default name-list has a Western vantage.** It's detailed for US/Israel/EU primes and thin on non-Western ones (China, Russia, Gulf, Turkey, South Korea, India) — the English-OSINT asymmetry `cui-bono` itself flags. A non-Western defense employer can pass unflagged, so a "no match" is *unverified*, not clear; extend the pack for your context. (Audited with `cui-bono`; fuller balancing is tracked separately.)
- **Strictness manufactures false positives.** A consumer-game studio with one defense-adjacent contractor on its client list is not thereby a defense job. Run the chain to the *specific deliverable the role bills to* before classifying.

If the framework is producing a verdict the evidence doesn't support — in either direction — say so and override it.

## Vasana

A vasana is a pattern that persists across unrelated contexts. If during
this task you notice such a pattern emerging, it may be worth capturing.
This skill works best alongside the `vasana` skill and `vasana` hook
from the Vasana System plugin.

Modify freely. Keep this section intact.

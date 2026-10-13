---
name: operating-flashfusion-marketing-crew
description: Runs a six-role AI marketing crew (Copywriter, Creative Director, Web Designer, Email Marketer, Marketing Ops, Performance Marketer) for FlashFusion campaigns, mapped onto FlashFusion's actual connected tools (Canva, HubSpot, Zapier, Vercel, Google Ads via Zapier, PostHog) instead of a generic stack. Use whenever the user wants to launch a FlashFusion campaign, build a landing page plus nurture plus ad funnel end to end, or says anything like "run the marketing crew," "launch a FlashFusion funnel," "build me a campaign," "spin up a lead magnet," or references rebuilding an "AI marketing team" pattern for personal use — even if they don't name the roles or tools explicitly. PERSONAL/FlashFusion lane only — do not use for Loxihart or freelance-client campaigns, where this tool mapping does not apply.
compatibility: Requires Canva, HubSpot, Zapier, Vercel, and PostHog MCP connectors (or Cowork connectors) to be live. The Copywriter role works with zero tools.
metadata:
  version: "1.1.0"
  author: Kyle Rosebrook
  known-gaps: >
    No Meta Ads / paid-social connector exists in this stack — Performance
    Marketer covers Google Ads and attribution only, not Meta. No
    Framer/Webflow connector — Web Designer splits between the real Vercel
    codebase and HubSpot's landing-page builder, neither of which crawls
    an existing site to learn brand style the way Framer's agents do.
    HubSpot workflow depth for event-based kick-out logic is unverified
    against Kyle's actual plan tier.
  chains:
    - packaging-skills
    - administering-supabase
    - building-flashfusion-live-artifacts
---

# Operating the FlashFusion Marketing Crew

## Instructions

This skill runs a six-role marketing crew against a single campaign brief. Each role pairs unchanged strategic logic with a specific FlashFusion tool — not the tools a generic "AI marketing team" tutorial would assume. Follow these steps in order.

1. **Take the brief.** Get the campaign goal, audience, and any existing brand assets in one pass. A one-line ask produces a generic funnel — ask for more if the brief is thin.

2. **Lock the angle (Copywriter, no tool).** Evaluate the brief against Alex Hormozi's Value Equation and pick exactly one lever: Ease of Use, Speed, Perceived Likelihood of Success, Effort/Sacrifice, or Dream Outcome. State the chosen lever and why in one sentence before any visual or page work starts. Every other role inherits this angle — do not let later roles drift to a different lever.

3. **Build in parallel (Creative Director + Web Designer).**
   - Creative Director: generate ad visuals in Canva using the FlashFusion brand kit. If no brand kit exists yet, use the tokens in `assets/config.md` directly.
   - Web Designer: decide first whether this is a standalone campaign page or a change to the live FlashFusion product. Standalone pages go through HubSpot's landing-page tools. Product changes are real code in the flashnframe-app repo, shipped via Vercel — read the existing code and edit it directly, do not treat it as a no-code builder.

4. **Wire the lead flow (Marketing Ops, Zapier).** Connect the page's form submission to HubSpot for lead capture and to PostHog for event tracking. Map Name, Email, and Lead Source explicitly. Name the exact event that should stop the nurture sequence (e.g. "signed up") — do not assume this is inferred automatically.

5. **Launch and track (Performance Marketer).** If the brief calls for Google Ads, set up targeting and feed conversion events back via the Google Ads offline-conversion action, then cross-check attribution in PostHog. If the brief calls for Meta, Instagram, or Facebook ads, stop and say so plainly — there is no Meta Ads connector in this stack. Do not substitute Google Ads for a Meta request and do not fabricate a Meta workflow.

Copy-paste prompt templates for each role live in `references/role-playbooks.md`. The full before/after tool comparison against the original source pattern (Framer, Customer.io, Meta Ads, Python/Pillow) is in `references/tool-mapping.md`. Project references, brand tokens, and standing config live in `assets/config.md`. The acceptance gate for a crew run is in `assets/success-criteria.md`.

## Examples

- "Run the marketing crew on a lead-magnet campaign for the new FlashFusion onboarding guide, targeting solo founders." → Full five-step run: angle lock, Canva + HubSpot build, Zapier wiring, Google Ads launch with PostHog cross-check.
- "Build me a landing page for [offer], no ads yet." → Steps 1–4 only; skip the Performance Marketer step and say so.
- "Launch this on Instagram." → Stop at step 5, report the missing Meta Ads connector, and offer the two real alternatives: connect one, or hand targeting off to Ads Manager manually.

## Guidelines

- Canva output will be generic unless a FlashFusion brand kit already exists — check before assuming brand fidelity.
- HubSpot's landing-page builder and the real Vercel-deployed codebase are not interchangeable. Confirm which one a "Web Designer" request actually means before building.
- HubSpot's workflow depth for event-based nurture kick-outs has not been verified against the current plan tier — treat claims about it as an estimate, not a fact, until checked.
- The FlashFusion Supabase project is `flashnframe-app` (`etctmappdhpjuwptdbeb`), listed in `assets/config.md`. Reading it is fine; writes or deletes need explicit confirmation per the `administering-supabase` skill, which this skill does not override.
- There is no Meta Ads connector in this stack today. Any Meta/Instagram/Facebook request hits a real, structural gap — flag it, do not route around it silently.
- This skill is scoped to the PERSONAL/FlashFusion lane. Do not apply it to Loxihart SME work or freelance-client deliverables — the tool mapping and comms rules (Slack personal/ChaosClubCo only) do not carry over to those lanes.
- Before calling a crew run "done," check it against `assets/success-criteria.md` — in particular, that no role silently substituted a tool the brief didn't ask for.

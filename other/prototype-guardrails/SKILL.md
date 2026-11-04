---
name: prototype-guardrails
description: >-
  The non-negotiable rules for an unofficial government-app prototype: no state emblem, mObywatel marks or
  official document artwork, fictional data only, a visible disclaimer, no real registries or personal data.
  Use before adding any asset, document view, persona, demo data, input field or "verify"/QR feature, or when
  asked "can we use the logo / emblem / real look?".
---

# Prototype guardrails

We are building an **unofficial** prototype of a public-administration app. Two things can sink the entry or
create real harm: using protected official marks, and building something that works as a fake ID. These rules
hold for every agent and every PR.

## 1. No official marks

Never add, draw, trace, recolour or reference:

| Forbidden                                                                                                            | Why                                                  |
| -------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------- |
| Godło (white eagle on red), coat of arms, its silhouette or cues                                                     | Protected state symbol; challenge excludes it        |
| mObywatel logo, app icon, wordmark styling, its colours used as a logo                                               | Trademark; excluded from the reference's MIT licence |
| Official document artwork: mDowód, mPrawo jazdy, KDR, legitymacja cards, strips, holograms, guilloches, flag ribbons | Imitating an official document; licence exclusion    |
| QR / "verify document" screens that look like the official verification flow                                         | Could be shown to a shop or police as a real ID      |
| Photos of people from the reference prototype (`foto-*.jpg`)                                                         | Personal images, not licensed                        |
| Anything copied from `mobywatel-ai/mockup/assets/`                                                                   | Explicitly excluded from the MIT licence             |

The reference's _code_ (`.js`, `.py`, `.css`, dictionaries) is MIT: reusing ideas or code is allowed with
attribution (keep the licence notice). Its service descriptions come from gov.pl: check gov.pl's reuse terms
before copying text, and prefer writing our own plain-language summaries with a source link and date.

Design our own neutral identity instead (the `design-system` skill, the `brand-designer` agent): no
white-red-eagle cues, no document-like layout with photo + MRZ + hologram.

## 2. Documents are information, never credentials

- A document view is an **information card**: name, number, validity, what you can do next. It carries the
  `PROTOTYP – nie jest dokumentem` watermark and the disclaimer.
- No full-screen "show this to the cashier/police" mode, no animated security features, no verification QR, no
  age-check credential that looks presentable.
- Photos on documents: a neutral illustrated avatar, never a realistic face.

## 3. Fictional data only

- Names: invented, common-sounding but not tied to a public figure. No real people.
- PESEL: valid checksum (so validation code is realistic) but with clearly fictional parts. Document series
  use `PRO` / `PROTO` style prefixes (e.g. `PRO 123456`). Plates like `XX PROTO1`.
- Addresses: real cities are fine for context; street + number must not point at a real person's home (use
  invented streets or public places).
- Policy, account and case numbers: obviously invented (`0000 PROTO 0001`).
- Every persona file in `packages/content` starts with a comment saying the data is fictional.

## 4. No real systems, no real personal data

- No calls to any government registry, ePUAP, Profil Zaufany, e-Doręczenia, CEPiK, ZUS, banks or payment
  providers. Everything is simulated in `packages/core`.
- Payments are mock screens ending in "W prototypie nic nie zostało zapłacone".
- The app never asks for real personal data. Free-text inputs (assistant, forms) show a hint: "To prototyp.
  Nie wpisuj prawdziwych danych." Nothing typed is sent anywhere, except to the optional LLM proxy (the
  `ai-assistant` skill), which keeps no logs of content by default.
- No analytics that capture typed text. If analytics is added at all, count page views only.

## 5. Visibly unofficial

- `UNOFFICIAL_DISCLAIMER` is exported from `@mobywatel/brand` (copy) and rendered on the start screen, every
  document view, the about/settings screen, and the PWA's offline page. The rendered element carries
  `data-disclaimer`.
- Suggested text: "Nieoficjalny prototyp na konkurs mobywatel.ai. To nie jest aplikacja mObywatel. Wszystkie
  osoby i dane są fikcyjne."
- The manifest `name` / `short_name` and the page `<title>` use our own working name, never "mObywatel" alone.

## How it is enforced

| Guard                                  | What it catches                                                                                                |
| -------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| `.claude/hooks/pre-edit.mjs`           | asset files named like the emblem, logos, document art, ref photos; references to the reference's asset folder |
| `pnpm run audit:guardrails`            | same, across the whole repo, plus a missing disclaimer once `apps/pwa/src` exists                              |
| `.claude/hooks/post-edit.mjs` reminder | editing personas, fixtures or scenarios: "fictional data"                                                      |
| The `code-reviewer` agent              | document views, QR, inputs, data that looks real                                                               |

Rules live in `tools/harness/hook-rules.mjs` (`OFFICIAL_ASSET_PATTERN`, `officialMarkFindings`). The guards
check file names and paths. A traced emblem saved as `bird.svg` passes the hook, but it still breaks the rule.
Reviewers look at the pixels.

## If unsure

Stop and ask the user. A plain card with text is always allowed, so use that until the user decides. Record
the decision in `docs/decisions/<topic>-YYYY-MM-DD.md`.

---
name: name-clearance
description: Clear a product/brand name BEFORE buying a domain or branding anything. Runs same-industry collision, trademark signal, domain availability, and distinctiveness checks. Returns RED/YELLOW/GREEN verdicts with evidence. Use whenever a new product is being named, a domain is about to be bought, or a user proposes a name.
---

# name-clearance

> **Why this exists (the Patently lesson).** A product was named "Patently" and the
> domain `patently.legal` was bought — *then* we found `patently.com`: an 8-year-old,
> 1,500-user AI **patent** platform run by patent litigators. Identical name, identical
> field. The domain was available; the **name** was a landmine. A free domain proves
> nothing. **Clear the name, not the domain.**

## When you activate

- A new product is being named (ideate → scaffold).
- **Before** any domain purchase — this is a hard gate in the go-live flow.
- A user proposes a brand name ("let's call it X").
- A rename is being considered.

## What you produce

For each candidate, a verdict with evidence:

- 🟢 **GREEN** — no same-field collision, distinctive/arbitrary mark, domain obtainable. Safe to advance to a formal attorney knockout.
- 🟡 **YELLOW** — clear in-field but flags exist (crowded prefix, famous-brand crowding/SEO, common word, brand in an adjacent industry). Usable with caution + formal TM search.
- 🔴 **RED** — same/adjacent-industry collision, registered/strong common-law mark, or descriptive-and-taken. Kill it.

Plus a one-line **recommendation** and, for finalists, the explicit reminder: **a paid attorney trademark knockout (USPTO + jurisdiction) before committing a cent.**

## Core principle — distinctiveness first

Trademark strength runs: **fanciful > arbitrary > suggestive > descriptive > generic.**
Suggestive/descriptive names (Patently for patents, "IP Radar" for IP) are a **double trap** —
legally weak *and* almost always already taken in-field. **Bias hard toward coined or
arbitrary names.** In a crowded category (legal-tech, fintech, dev-tools) real dictionary
words are *mostly* taken; a coined word is often the only reliably-clearable option.

**But never *assume* a word is taken — check it.** A registered `.com` is NOT a dead name;
many strong brands don't own their `.com`. What kills a name is a **same-industry collision**
or a live trademark, not a parked domain. Keep dictionary words in play through the check;
let the evidence (not a guess) eliminate them. (This skill is **phase 4** of the
`name-product` pipeline — the clearance engine it calls.)

## Protocol

Run cheap → expensive, fail fast. Stop at the first RED.

1. **Distinctiveness triage.** Place the name on the spectrum. If it's descriptive/suggestive
   *of the product's own category*, flag it immediately — it will be both weak and likely taken.

2. **Same-industry collision (highest weight).** Web-search the name against the product's field:
   - `"<name>" <industry> company` / `"<name>" software startup` / `"<name>" <category-term>`
   - Any company or product using the same or a confusingly similar name in the **same or an
     adjacent industry** → 🔴. (Adjacent counts: a trademark agency for an IP tool, film-IP-clearance
     for IP-clearance, fintech-decisioning for a risk tool.)

3. **Trademark signal.** Search the registries — USPTO TESS (https://tmsearch.uspto.gov),
   EUIPO eSearch, and the product's home jurisdiction — in the relevant Nice classes:
   **9 (software), 42 (SaaS/tech), 45 (legal services)**, plus any category-specific class.
   A live registration *or* strong common-law use (years of use, scale) → 🔴.

4. **Famous-crowding / SEO.** Is the root already owned in public consciousness by a famous
   brand, blog, or figure (e.g. "Patently-O" for patent content)? If the product will be
   invisible in search behind incumbents → 🟡 (downgrade), even absent a legal conflict.

5. **Domain availability.** Run the helper across acceptable TLDs:
   ```
   bun ${HAMZAISH_ROOT:-$HOME/Claude/Hamzaish}/factory/skills/name-clearance/check-domains.ts <name> com ai legal app io co
   ```
   `.com` is ideal; `.ai`/`.app`/`.legal`/`.io` are acceptable. The WHOIS verdict is a signal —
   confirm finalists at a registrar.

6. **Package-registry clearance (npm / PyPI / crates — for anything you'll publish).**
   A 404 on the *exact* name means it's unregistered — **NOT** that you can publish it. Registries
   run a **similarity / typosquat guard at publish time** that rejects names too close to an
   existing package. (rotscan, 2026-06-21: the exact name 404'd as "available," then `npm publish`
   returned `E403 — too similar to existing 'rot-scan'`.) So:
   - Search the registry for **near-names**, not just the exact one — hyphenated/un-hyphenated,
     singular/plural, common char-swaps (`npm search <name>`, or browse npmjs.com / pypi.org).
   - If a close look-alike exists, expect rejection — plan to **scope it** (`@you/name`, npm's own
     suggested fix) or pick a more distinctive name up front.
   - `npm publish --dry-run` does **not** run the similarity check; only a real publish does.
     Scoping (`@you/name`) sidesteps it entirely.

7. **Linguistic / social sanity.** Unfortunate meanings in other languages, hard to spell/say,
   handle availability (X / GitHub / LinkedIn).

8. **Verdict & recommendation.** Summarize each candidate as 🟢/🟡/🔴 with the evidence (links).
   Recommend the strongest GREEN. For any finalist, state plainly: **get a paid attorney
   knockout before committing** — this skill de-risks, it is not legal advice.

## Output format

A compact table: `Name | Verdict | Same-field collision | Domain | Note`, then a one-paragraph
recommendation. Cite the URLs that drove each verdict.

## Notes

- Run on a *batch* of candidates, not one — most will fail; generate 8–12 to find 1–2 GREENs.
- Re-run the whole protocol after any rename; don't trust a half-check.
- This skill is a **required pre-step before the domain-buy stage** of
  `factory/playbooks/ai-native-2026/go-live-provisioning.md`.

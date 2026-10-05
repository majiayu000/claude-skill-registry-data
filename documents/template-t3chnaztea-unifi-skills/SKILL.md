---
name: unifi-yourskill
description: >-
  Use when [the specific situations, symptoms, and phrases someone would
  actually type when they hit this problem]. Include the error strings and the
  wrong-conclusion phrasings, not just the correct terminology: people search
  for "my wifi is slow", not "co-channel contention". Describe ONLY when to use
  it, never summarize the workflow inside. Keep the whole frontmatter under
  1024 characters. End by naming what this skill is NOT for, pointing at the
  sibling skill that covers it.
compatibility: >-
  State what the skill needs: UniFi OS vs a self-hosted controller, minimum
  Network version, specific hardware, regulatory domain if channel-related.
---

# UniFi Yourskill

One or two sentences: what this covers, and that it assumes the auth lanes and
endpoint map from `unifi-connect`. Cross-reference siblings by name
(`unifi-firewall`, `unifi-wifi`, `unifi-clients`, `unifi-context-map`) instead
of repeating their content.

## Guidelines for a good UniFi skill

Delete this section in your real skill; it is authoring guidance.

- **Name:** `unifi-<area>`, lowercase and hyphens. The directory name MUST equal
  the frontmatter `name`.
- **Description:** starts with "Use when", lists concrete triggers and symptom
  phrasings, ends with a "not for X, use Y" pointer. No workflow summary: an
  agent will follow the description instead of reading the body.
- **Parameterize everything site-specific.** `<UDM_HOST>` never a real address,
  `$UNIFI_API_KEY` from env never a literal, `<DEVICE_ID>` / `<ZONE_ID>` /
  `<MAC>` placeholders. Where an example address is unavoidable use the
  documentation ranges: `192.0.2.x` (RFC 5737) and `aa:bb:cc:dd:ee:ff`.
- **Never include a real inventory.** No MAC lists, no camera names or
  placements, no WAN address, no SSID names, no household or company names. See
  `unifi-context-map` for why this matters more here than in most repos.
- **Original prose only.** Do not paste from Ubiquiti docs or help-centre
  articles. Write the lesson the docs do not teach, and link the docs as the
  canonical manual.
- **Say which version you verified against**, in `compatibility` and in the body
  for any version-sensitive claim. UniFi moves endpoints between releases with
  no deprecation notice. A claim stated as universal that was observed once on
  one controller is the most likely thing in a skill to be wrong.
- **Distinguish config from operational state.** This API will echo back
  settings it has not applied. If a claim rests on a read-back, say which field
  and which endpoint proves it.
- **Verify against ground truth.** Every write ends with a fresh read and a
  before/after. Show the reader how to confirm, not just how to change.
- Keep `SKILL.md` under ~500 lines; push heavy detail into `references/*.md`.
- Scripts are allowed here (this repo ships one) but keep them standard-library
  only, dependency-free, and readable in one sitting. An agent operating
  someone's gateway should be running code they can audit in five minutes.

## Overview

What this is and the core principle, in one or two sentences.

## When to use

Symptoms and situations. When NOT to use.

## [Your sections]

Quick-reference recipes, one worked example, the specific traps you learned. One
excellent example beats five generic ones. If you have a postmortem, tell it:
the numbers and the wrong turns are what make it stick.

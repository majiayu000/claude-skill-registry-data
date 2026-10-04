---
name: orbit-evergreen-update
description: Meta-skill that walks every `/orbit-*` skill, fetches the canonical sources listed in its `Sources & Evergreen References` section, diffs against the rules currently in the skill, flags drift (rule says X, source says Y now). Optionally proposes patches. Use whenever the user says "audit skills for staleness", "are my skills current", "evergreen update", "drift check", or quarterly as a maintenance routine.
---

# 🪐 orbit-evergreen-update — The skill that keeps skills current

Skills go stale. New WP releases add APIs. Standards evolve. This is the meta-skill that keeps the suite honest.

---

## Quick start

```bash
# Check every Orbit skill for source drift
claude "/orbit-evergreen-update Walk every skill in ~/.claude/skills/orbit-* and check for stale rules."
```

Output: `reports/evergreen-drift-<timestamp>.md`.

---

## How it works

For each `~/.claude/skills/orbit-*/SKILL.md`:

1. **Parse** the `Sources & Evergreen References` section
2. **Fetch** every URL listed (canonical docs + spec refs)
3. **Diff** the fetched content vs the rules embedded in the skill
4. **Flag** any rule whose canonical source has changed
5. **Propose** a patch (rule update or removal)
6. **Bump** `Last reviewed` date if no drift found

---

## What "drift" looks like

### Rule says: "apiVersion 3 required for viewScriptModule"
Source says (today): "apiVersion 4 (introduced WP 6.8)"
→ DRIFT. Skill should mention apiVersion 4.

### Rule says: "WP 6.5 introduced Block Bindings"
Source says: same.
→ NO DRIFT.

### Rule cites: "https://wordpress.org/support/plugin/some-old-plugin/"
Source returns: 404 (plugin removed)
→ BROKEN LINK. Skill should remove the reference.

### Rule cites: "Google requires structured data X"
Source updates: now requires structured data X + Y
→ INCOMPLETE. Skill should add Y.

---

## What it produces

```markdown
# Evergreen Drift — 2026-04-29

## Skills audited: 106
## Skills with drift: 14
## Broken links: 3

## High-priority drift

### orbit-block-json-validate
- Rule: "apiVersion 3 is current (WP 6.5+)"
- Source diff: WP 6.8 changelog mentions apiVersion 4 (preliminary)
- Action: Add 4 to the skill's apiVersion table; mark as "experimental in 6.8"

### orbit-seo-page-speed
- Rule: "INP < 200ms passes"
- Source diff: Google's CWV threshold page now shows INP < 175ms (tightened Q1 2026)
- Action: Update threshold

### orbit-pay-stripe
- Rule: "PaymentIntents API recommended"
- Source diff: Stripe added "Payment Element" recommendation in 2025-09
- Action: Mention Payment Element as the modern UI primitive

## Broken links
- orbit-host-wpengine: https://wpengine.com/old-disallow-list/ → 404
- orbit-compat-wpml: https://wpml.org/old-doc/ → redirects, update URL
- orbit-elementor-compat: GitHub link 404

## No-drift skills (last_reviewed bumped to today)
- 92 skills had no rule drift
- Auto-update their "Last reviewed: 2026-04-29" line via PR
```

---

## Operating modes

### `--check` (default)
Read-only. Reports drift; doesn't modify skills.

### `--apply`
For non-controversial fixes (broken links, simple version bumps), modifies the SKILL.md files. Always commits via PR for review.

### `--specific orbit-X`
Just check one skill (faster than the full ~106-skill scan).

### `--source <URL>`
Force re-fetch of a specific source URL across all skills that reference it. Useful after a major release: "WP 6.6 dropped — re-check every skill that references block.json schema."

---

## Schedule it (recommended)

```cron
# Quarterly audit
0 9 1 */3 * cd ~/Claude/orbit && \
  claude "/orbit-evergreen-update --check" > /tmp/orbit-drift-$(date +\%Y\%q).md
```

Or after each WP minor release (manual trigger).

---

## What sources are most likely to drift

Ranked by drift rate observed across 2024-2026:

| Source | Drift rate | Why |
|---|---|---|
| Elementor changelog | High — yearly major | Active deprecation cycle |
| WordPress make blog | Medium — every minor | New APIs added each minor |
| Block Editor Handbook | Medium | Reorganised periodically |
| Google CWV thresholds | Low (1-2/yr) | Tightened |
| Stripe API ref | Low (1-2/yr) | Stable but adds new primitives |
| WPCS (PHPCS sniffs) | Medium | Each PHP / WP minor adds sniffs |
| WP CVE feed | Daily | Continuous |
| Yoast / RankMath docs | Medium | Reorg + new filters |

Auditor weights checks accordingly — Elementor + WP make = check more often.

---

## Pair with

- `/orbit-skill-add` — when adding a new skill, add it to the evergreen-update audit cycle
- `EVERGREEN.md` — the policy / pattern doc

---

## Sources & Evergreen References

### Canonical docs (the meta — what THIS skill itself reads)
- [EVERGREEN.md](https://github.com/adityaarsharma/orbit/blob/main/EVERGREEN.md) — pattern reference
- [SKILLS.md](https://github.com/adityaarsharma/orbit/blob/main/SKILLS.md) — full skill list

### Rule lineage
- Pattern introduced — Orbit v2.6 (April 2026)
- Quarterly cadence recommendation — empirical (~13-week WP minor release cycle)

### Last reviewed
- 2026-04-29 — this skill IS the recursive audit; re-running it bumps every other skill's "Last reviewed"

---
name: whats-new-banner
description: "Discipline for the site-wide \"What's New\" announcement banner driven by src/data/whats-new.json: when activating it is justified, when it is not, the 3-4 per year cadence, and how to update the file. Use when asked to activate, update, or retire the banner."
---

# 12. "What's New" banner discipline

The site carries a sparingly-used site-wide announcement banner driven
by `src/data/whats-new.json`. When `active: true`, every page shows a
small dismissible bar above the sticky-chrome. Each visitor sees a given
banner at most once (dismissed state lives in `localStorage` keyed by
`version`). The JS render lives at the bottom of `src/assets/js/theme.js`.

### When to activate

High bar. Reasonable activation cases:

- A new section visitors would want to find without reading the CHANGELOG
  (e.g. a live conference programme, a founding-contributors page).
- A major feature visible above the fold.
- A content milestone (e.g. a deliverable ships, a key partnership is
  announced).

### When NOT to activate

- Quality patches, structural refactors, or infra changes.
- Content additions or copy edits that don't change the visitor experience
  meaningfully.
- Anything that would only interest someone already reading the CHANGELOG.

### Cadence

At most 3-4 activations per year. The on-state should run no longer than
4-6 weeks before `active` flips back to `false`. Leaving it on permanently
trains visitors to ignore it.

### How to update

1. Edit `src/data/whats-new.json` — set `active`, `version`, `headline`
   (EN/FR/DE), and `cta`.
2. The `version` string is the dismissal key. Bump it for each new
   activation so returning visitors see the new banner even if they
   dismissed the previous one.
3. Flip `active` back to `false` when the announcement is stale.

No automation touches this file. The friction is intentional.

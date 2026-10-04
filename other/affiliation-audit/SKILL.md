---
name: affiliation-audit
description: Audit collected affiliation data against logo strip and social proof best practices. Evaluates logo quality, grouping strategy, copy framing, prominence ordering, and strip-readiness. Run after affiliation-scrape, before logo-strip-author.
disable-model-invocation: true
---

Audit affiliation data for: $ARGUMENTS

$ARGUMENTS should include:
- A person slug (e.g. `alan-hirsch`) or full name — looks for `content-library/affiliations/{slug}.json`
- Optionally: `--strip-max N` — max logos in the strip (default: 12)
- Optionally: `--strip-min N` — min logos required (default: 5)
- Optionally: `--groups N` — max number of strip groups (default: 4)
- Optionally: `--fix` — auto-attempt logo quality upgrades via browser

## Before Starting

1. Read `content-library/affiliations/{slug}.json` — the scraped affiliation data
2. If the file doesn't exist, instruct the user to run `/affiliation-scrape {name}` first
3. Read `public/images/orgs/` to see which logos are already downloaded locally

## Audit Dimensions

### Dimension 1 — Strip Count & Density

Logo strips have a sweet spot. Evaluate against these benchmarks:

| Count | Assessment |
|-------|-----------|
| < 5 | WEAK — too few to be convincing; explore more orgs or expand criteria |
| 5–8 | SOLID — clean, credible, not overwhelming |
| 9–12 | STRONG — conveys breadth; use 2-row or scroll if needed on mobile |
| 13–18 | RISK — diminishing returns; curate down or split into two sections |
| > 18 | TOO MANY — must curate; only the most prominent belong in the strip |

### Dimension 2 — Logo Quality Assessment

For each `include_in_strip: true` org:

**Quality checks:**
- [ ] Logo URL resolves (HTTP 200, not 404)
- [ ] Logo is SVG or PNG ≥ 200px wide
- [ ] Logo has transparent background (critical for light/dark mode compatibility)
- [ ] Logo is readable at 48px height (the standard strip display size)
- [ ] Logo is not a favicon (< 32px)
- [ ] Logo does not contain the organization's full sentence tagline (logos only)

**Grade each logo:**
- `A` — SVG, transparent background, clearly readable at 48px
- `B` — PNG ≥ 200px, transparent or white background, readable at 48px
- `C` — PNG 100–200px, or has non-transparent background but works on expected strip background
- `D` — PNG < 100px, wrong background color, favicon, or partial/cropped
- `F` — Not found, broken URL, or unreadable at any size

If `--fix` flag is passed, attempt to find better logo sources for any D or F grade:
1. Try `https://logo.clearbit.com/{domain}` (Clearbit logo API)
2. Navigate to the org's website and look for `/images/logo.svg` or equivalent
3. Check Wikimedia Commons: `https://commons.wikimedia.org/wiki/Special:Search?search={org+name}+logo`
4. Update `logo_url` and `logo_quality` in the JSON file if a better source is found

### Dimension 3 — Grouping Strategy

Logo strips are most persuasive when logos are grouped by relationship type. Evaluate the proposed grouping:

**Ideal group structure for thought leaders:**

| Group | Label | Logos | Notes |
|-------|-------|-------|-------|
| Publishers | "Published by" or "Author of books published by" | 2–5 | Highest credibility signal |
| Speaking | "Available through" or "Speaking with" | 1–3 | Bureaus or major conference series |
| Media | "As featured in" or "Featured in" | 3–6 | Outlets, podcasts, magazines |
| Networks | "In partnership with" or "Part of" | 2–5 | Movements, networks, denominational ties |
| Academic | "Faculty at" or "Teaching at" | 1–3 | Seminaries, universities |
| Endorsers | "Endorsed by" or "Trusted by" | 2–4 | If orgs (not individuals) have endorsed |

**Checks:**
- [ ] At least 2 distinct groups (a single group is just a list)
- [ ] Each group has 2+ logos (a single logo in a group looks sparse)
- [ ] No group has > 8 logos (split if needed)
- [ ] Group labels are relationship-specific, not generic ("As featured in" beats "Media")
- [ ] Publisher logos appear first (highest credibility signal)
- [ ] Groups flow from most to least formal: Publishers → Academic → Networks → Speaking → Media

### Dimension 4 — Copy & Framing

The strip needs a headline that frames the social proof correctly.

**For authors:** "Published by the world's leading Christian publishers"
**For speakers:** "Trusted on the world's most important stages"
**For thought leaders:** "A voice that bridges the academy and the movement"
**Generic fallback:** "Trusted by organizations worldwide"

Evaluate:
- [ ] A headline is defined (or can be drafted)
- [ ] The headline is specific to the type of credibility being claimed
- [ ] The headline is not just "Trusted by" with no qualifier — too generic
- [ ] Consider: does this person's affiliations speak to quality, breadth, or longevity? The headline should name that.

Optional: sub-headline for context (especially useful for less-known audiences):
- e.g., "Alan's work has been published, taught, and recognized across the global church movement"

### Dimension 5 — Prominence Ordering

Within each group, logos should be ordered by prominence (prominence_score desc). Check:

- [ ] Within each group, orgs are sorted by `prominence_score` (highest first)
- [ ] Publisher group: major publishers (Baker, Zondervan, IVP = score 9–10) appear before smaller ones
- [ ] Media group: national/international outlets precede regional or niche outlets
- [ ] Conference group: marquee events (Lausanne, TGC, Catalyst) precede smaller ones
- [ ] No group puts a low-prominence org first

### Dimension 6 — Dark/Light Mode Compatibility

Logo strips must work in both light and dark backgrounds:

- [ ] All logos are SVG (adapts to CSS color-scheme) OR
- [ ] PNG logos have transparent backgrounds (shows correctly on any background) OR
- [ ] Both light and dark variants are available
- [ ] No logos have white-on-white or dark-on-dark issues
- [ ] Plan exists for logos that don't have transparent backgrounds (CSS `mix-blend-mode`, inversion, or dark-bg alternative)

**Recommended approach:**
- Default: show logos in monochrome/grayscale via CSS `filter: grayscale(1)` with hover → full color
- On dark backgrounds: `filter: grayscale(1) brightness(2)` to lighten dark logos
- If logo quality is consistently poor: consider monochrome SVG recreation for top-tier orgs

### Dimension 7 — Mobile Responsiveness Plan

- [ ] Strip design handles mobile (< 768px) gracefully
- [ ] Options: horizontal scroll (snap), 2-column grid, or condensed to top 6
- [ ] Logo height: 40px mobile, 48px tablet, 56px desktop
- [ ] Touch targets: logos should link to the org's website
- [ ] If groups are used: groups collapse to a single flat list on mobile

## Gap Analysis

Identify what the strip is missing:

**Common gaps for thought leaders:**
- No speaking bureau listed — weakens speaker credibility
- Only books from one publisher — suggests limited reach
- No media appearances — makes it look like they speak only to insiders
- No academic affiliation — misses scholarly credibility if they have it
- No international orgs — looks US-centric for global thinkers

For each gap, recommend a targeted search:
- "missing speaking bureau" → suggest running `/affiliation-scrape {name} --category speaking-bureau`
- "no media" → suggest searching `"{name}" interview OR podcast OR article` specifically

## Output Format

```
## Affiliation Audit: [Person Name]

### Overall Strip Readiness
Status: READY / NEEDS WORK / BLOCKED
Strip-ready logos: N (target: 5–12)
Recommended strip layout: [single-row / two-row / grouped / scrolling]

### Logo Quality Grades
| Organization | Group | Grade | Issue |
|-------------|-------|-------|-------|
| Baker Books | publishers | A | SVG, transparent |
| Forge International | networks | B | PNG 300px, white bg |
| Example Conference | conference | D | Favicon only — needs upgrade |

### Grouping Assessment
Status: GOOD / ADJUST / REWORK
Proposed groups:
1. publishers (3 logos) — "Published by" ✅
2. networks (4 logos) — "Part of" ✅
3. media (5 logos) — "As featured in" ✅ (trim to 4)
4. speaking (2 logos) — "Speaking with" ✅

Issues:
- [ ] "conference" group has only 1 logo — merge into media or speaking
- [ ] academic group empty — no academic affiliations found

### Copy Assessment
Recommended headline: "A voice trusted by the global church"
Recommended sub-headline: "Alan's work spans the world's leading publishers, networks, and stages"

### Prominence Order (recommended)
**publishers:** Baker Books (10) → IVP (9) → Fortress (7)
**networks:** Forge International (9) → 5Q Collective (8) → Communitas (7) → Exponential (6)
**media:** Christianity Today (9) → Relevant Magazine (7) → Leadership Journal (6) → The Gospel Coalition (8)
**speaking:** Premier Speakers Bureau (8) → Chartwell (7)

### Dark/Light Mode Status
✅ 8 logos: SVG or transparent PNG
⚠️ 4 logos: white background (needs CSS handling or dark alternative)
❌ 1 logo: dark background (will disappear on dark strip backgrounds)

### Mobile Plan
Recommended: Horizontal scroll with snap at 40px height, grouped by category with category label as section header

### Gaps & Recommendations
| Gap | Impact | Suggested Action |
|-----|--------|-----------------|
| No speaking bureau listed | MEDIUM | Search "{name} speaking" — check personal site /speaking page |
| Academic affiliation unverified | LOW | Check if there are seminary ties in bio |

### Actions Before Authoring
1. ❌ Fix logo grade D for [org name] — try Clearbit or official site (run with --fix)
2. ⚠️ Merge "conference" into "media" group (only 1 logo)
3. ✅ Re-sort networks group by prominence_score
4. ✅ All else ready — run `/logo-strip-author alan-hirsch` to generate the section

### Next Step
Run: `/logo-strip-author {slug}` to generate the full social proof section
```

## Rules

- **Audit only — don't rewrite the JSON** unless `--fix` is passed (then only update `logo_url`/`logo_quality`)
- **Be specific about D/F grade logos** — name exactly what's wrong and how to fix it
- **Never recommend including LOW confidence orgs** in the strip without user confirmation
- **5 is the floor** — a strip with < 5 logos is not credible; say so plainly
- **Grayscale is the default** — remind the user this is the visual standard unless they explicitly want full-color
- **Prominence ordering is non-negotiable** — a minor org appearing before a major publisher undermines credibility

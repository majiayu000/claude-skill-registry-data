---
name: launching-digital-products
description: >
  Orchestrates multi-storefront digital product launches across Gumroad, Etsy,
  Shopify, TikTok Shop, Amazon KDP, and other marketplaces. Generates
  platform-specific listing data, paste-ready guides, distribution assets,
  and launch checklists from a single product brief. Activates when launching
  a digital product, listing on multiple storefronts, creating marketplace
  listings, preparing product launch assets, multi-platform product distribution,
  digital download listing, e-commerce product launch, storefront listing
  automation, cross-platform product publishing, or any request to sell a
  digital product across multiple platforms. Also triggers on: launch plan,
  list my product, sell on Gumroad, sell on Etsy, Shopify listing, TikTok Shop
  listing, Amazon KDP listing, multi-storefront, paste guide, product launch
  checklist, 48-hour launch, or digital product distribution.
metadata:
  version: "1.0.0"
---

<objective>
Turn a single product brief (title, description, price, file) into
platform-ready listings across every target storefront — with correct
field constraints, pricing strategy, SEO optimization, and paste-ready
guides for platforms requiring manual entry.
</objective>

<essential_principles>

## 1. Single Source of Truth

All listing data derives from ONE canonical product brief. Never let
platform-specific descriptions drift independently. Changes flow:

```
Product Brief (canonical)
  → Platform Adapter (transforms per storefront constraints)
    → Listing Data File (platform-specific, numbered)
      → Paste Guide (for manual-entry platforms)
```

## 2. Platform Constraint Awareness

Every storefront has unique constraints that break naive copy-paste:

| Platform | Title Limit | Description Format | Price Strategy | Auth Model |
|----------|-------------|-------------------|----------------|------------|
| Gumroad | ~200 chars | Markdown | PWYW ($12 min / $19 suggested) | OAuth / browser |
| Etsy | 140 chars | Plain text + line breaks | $14.99 (sweet spot) + sale | Browser + 2FA |
| Shopify | ~255 chars | HTML/Rich text | $14.99 / compare-at $24.99 | Admin API or browser |
| TikTok Shop | ~255 chars | Plain text | $12.99 / original $19.99 | Seller Center login |
| Amazon KDP | ~200 chars | HTML (4000 char max) | $9.99 (70% royalty tier) | Amazon login |
| Printify | N/A | Print-on-demand integration | Varies | API or browser |

## 3. File Numbering Convention

```
launch-assets/
  01-GUMROAD-LISTING.md        # Listing source data
  02-ETSY-LISTING.md
  03-DISTRIBUTION-ASSETS.md    # Cross-platform launch content
  04-NOTION-MARKETPLACE.md     # (optional storefronts)
  05-SHOPIFY-LISTING.md
  06-PRINTIFY-NOTES.md
  07-TIKTOK-SHOP-LISTING.md
  08-AMAZON-LISTING.md
  09-GUMROAD-MANUAL-FINISH.md  # Paste guide (when automation hits a wall)
  10-TIKTOK-SHOP-QUICK-PASTE.md
  11-AMAZON-KDP-QUICK-PASTE.md
  {product-file}.pdf           # The actual deliverable
```

Numbering is sequential. Storefronts ordered by friction: lowest first.

## 4. Automation-First, Paste-Guide Fallback

Try browser automation (Claude in Chrome / MCP) first. When blocked by:
- **Login walls** → create a numbered Quick Paste guide
- **Category approval gates** → document fallback category + appeal process
- **File format requirements** → document conversion steps (e.g., PDF→EPUB)
- **Tab crashes** → navigate directly to target URL in a new tab

## 5. Pricing Strategy by Platform

- **Gumroad**: PWYW outperforms fixed by ~260%. Set minimum + suggested.
- **Etsy**: Digital download sweet spot is $12–$17. Show sale price.
- **Shopify**: Use compare-at for strikethrough. Add discount codes.
- **TikTok Shop**: Competitive pricing. Show original price for urgency.
- **Amazon KDP**: $9.99 maximizes 70% royalty tier ($2.99–$9.99 range).

## 6. SEO / Keyword Strategy

Each platform has different keyword mechanics:
- **Gumroad**: Tags (10 max), description keywords
- **Etsy**: 13 tags max, title front-loaded with keywords
- **Shopify**: SEO title + meta description + product tags
- **TikTok Shop**: Category + attributes + description keywords
- **Amazon KDP**: 7 keyword boxes + 2 categories + title/subtitle

Generate platform-specific keyword sets from the canonical brief.

</essential_principles>

<intake>
What would you like to do?

1. **New launch** — Generate all listing files from a product brief
2. **Add storefront** — Add a new platform to an existing launch
3. **Generate paste guide** — Create a manual-entry guide for a blocked platform
4. **Launch content** — Generate distribution assets (LinkedIn, Reddit, email, etc.)
5. **Status check** — Audit which storefronts are live vs. pending

Route based on response. If the user provides a product file or brief
without selecting, assume option 1 (new launch).
</intake>

<routing>
| Response | Action | Reference Files |
|----------|--------|-----------------|
| 1, "new launch", "launch", "list my product" | Collect product brief → generate all listing files | references/storefront-*.md, templates/product-brief.md, templates/listing-data.md |
| 2, "add storefront", "add platform" | Ask which platform → generate that listing file | references/storefront-{platform}.md |
| 3, "paste guide", "manual", "quick paste" | Ask which platform → generate paste guide | references/storefront-{platform}.md, templates/paste-guide.md |
| 4, "launch content", "distribution", "announce" | Generate cross-platform launch posts | templates/distribution-assets.md |
| 5, "status", "audit", "check" | Scan launch-assets/ directory → report status | (no reference needed) |
</routing>

<process_new_launch>
## New Launch Workflow

### Phase 1: Product Brief (5 min)
1. Collect or confirm: product name, subtitle, author, file format, price anchors
2. Collect: full description (features, bonuses, audience, format)
3. Collect: target storefronts (default: Gumroad + Etsy + Shopify + TikTok + KDP)
4. Save canonical brief as `launch-assets/00-PRODUCT-BRIEF.md`

### Phase 2: Listing Generation (15–30 min)
For each target storefront, in order of lowest friction:
1. Read the storefront reference file for field constraints
2. Transform the canonical brief into platform-specific listing data
3. Write the numbered listing file
4. Attempt browser automation if available
5. If blocked → generate paste guide as a separate numbered file

### Phase 3: Distribution Assets (10 min)
1. Generate launch posts: LinkedIn, Reddit (2–3 subs), email, Skool
2. Generate cross-link strategy (each storefront links to others)
3. Write `03-DISTRIBUTION-ASSETS.md`

### Phase 4: Verification (5 min)
1. Scan `launch-assets/` — confirm all expected files exist
2. For each storefront: status = LIVE / DRAFT / PASTE-GUIDE-READY / BLOCKED
3. Report blockers and next manual steps
</process_new_launch>

<known_blockers>
## Common Blockers and Mitigations

| Blocker | Platform | Mitigation |
|---------|----------|------------|
| Login wall (password required) | All | Generate paste guide; user logs in manually |
| Digital category approval | TikTok Shop | Apply for approval; fallback: bio link to Gumroad |
| PDF→EPUB conversion | Amazon KDP | Use Calibre (free) or CloudConvert; or do paperback-only |
| Book cover required | Amazon KDP | Canva template (1600×2560px) or KDP Cover Creator |
| Digital downloads app needed | Shopify | Install "Digital Downloads" by Shopify or SendOwl |
| Tab crash on click | Various | Open target URL directly in new tab |
| Disk space (VM ENOSPC) | Local | Use Write tool only; skip Bash; do conversions on user's machine |
| KDP Select exclusivity | Amazon | Only applies to Kindle eBook format, NOT PDF on other platforms |
</known_blockers>

<self_verification>
## Checklist Before Declaring Launch Complete

1. [ ] All target storefronts have either a LIVE listing or a paste-ready guide
2. [ ] Product file (PDF/EPUB) is uploaded or referenced in each listing
3. [ ] Pricing is set correctly per platform strategy
4. [ ] SEO tags/keywords are platform-specific (not copy-pasted across)
5. [ ] Cross-links between storefronts are documented
6. [ ] Distribution assets (launch posts) are generated
7. [ ] Manual steps for the user are consolidated in one summary
</self_verification>

<claims>
## CLAIMS
- Single-source product brief prevents description drift across platforms
- Automation-first with paste-guide fallback covers 100% of storefronts
- Platform-specific pricing strategy (PWYW, sale price, royalty tiers) outperforms uniform pricing
- Lowest-friction-first ordering reduces time-to-first-sale

## COUNTEREXAMPLE
- Some products need platform-exclusive features (Etsy variations, Shopify bundles) that can't derive from a single brief
- KDP Select exclusivity decision depends on business strategy, not just format logic

## CONTRADICTIONS
- "Automate everything" conflicts with login-wall reality — most storefronts require manual auth
- "Single source of truth" can produce suboptimal listings if platform audiences differ significantly
</claims>

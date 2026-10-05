---
type: Skill
name: design-email-marketing
description: Design and write email marketing campaigns — newsletters, promotional sequences, abandoned cart recovery, welcome flows, and SMS reminders. Covers copywriting, segmentation, timing, and monthly campaign calendar integration. Use when you need to write newsletter copy, plan email sequences, design abandoned cart recovery, segment subscriber lists, or schedule promotional sends aligned with your marketing calendar.
license: Proprietary. See LICENSE.txt
metadata:
  type: Skill
---

# Email Marketing

Use this skill when creating email campaigns, writing newsletters, designing automated sequences, or planning SMS reminders for e-commerce.

## Available Tools

| Tool | Purpose |
|---|---|
| `toolkit_cpt` (action: `list_items` on `mcp_ai_customer`) | Query customer records for segmentation — filter by purchase history, last order date, lifetime value |
| `toolkit_cpt` (action: `list_items` on `mcp_ai_lead`) | Query leads for prospect outreach — filter by status, source, score |
| `toolkit_cpt` (action: `get_schema` on `mcp_ai_customer` / `mcp_ai_lead`) | Discover available CRM fields before querying customer or lead records |
| `create_post_validated` | Create email newsletter drafts as WordPress posts for review |
| `paper_store_write` | Save email templates and sequences to the Paper Store for reuse |
| `nds_list_email_templates` / `nds_preview_email_template` | List and preview the NV oOS Design System email templates (built-in + custom + AI drafts) |
| `nds_generate_email_template` | Generate a new branded email template from a prompt — saved as a draft with an audit report (activate separately after review) |
| `nds_audit_email_template` | Audit a template against WCAG/EMC accessibility, structure, dark mode, and the 100 KB size budget before activation |
| `nds_set_active_email_template` / `nds_test_send_email` | Activate the template that wraps all outgoing `wp_mail()` emails (gated) and send a test |
| `nds_export_email_template` / `nds_import_email_template` | JSON backup/transfer — export can also mirror to the Paper Store (`mirror_to_paper_store`) and import from it (`paper_store_collection` + `paper_store_record_id`) |
| `nv_oos_*_agent_remote_wp_connection` | Pull customer/order data from remote WooCommerce sites for email targeting |

> **Template/branding note:** the NV oOS Design System addon is the
> template layer for these campaigns — the active template wraps every
> outgoing WordPress email with brand tokens (Settings → Design System →
> Emails). This skill writes the copy; the `nds_*` tools own the template
> and branding. The WooCommerce rebrand toggle (`nds_email_wc_rebrand`)
> styles WC order emails from the same token palette.

> **CRM note:** Use `design-crm` to manage the full customer and lead lifecycle — this skill focuses on email content and segmentation, not CRM record management.

## WP-CLI Commands

Key `mcp-ai` WP-CLI commands for email workflows. Run via `terminal`:

| Command | Use for |
|---|---|
| `wp mcp-ai cron` | Check scheduled email campaigns |
| `wp mcp-ai bulk` | Batch process email templates |
| `wp mcp-ai log` | View email send success/failure logs |

## When to use this skill

Trigger when ANY of the following is true:

- Creating a newsletter, promotional email, or announcement.
- Setting up an automated email sequence (welcome, abandoned cart, post-purchase).
- Writing SMS reminders for sales, launches, or events.
- The task mentions "email blast", "newsletter", "drip campaign", or "email sequence".
- Planning email content aligned with a monthly marketing calendar.
- The task asks to "send an email to customers" or "notify subscribers".
- Designing abandoned cart recovery flows.
- Creating customer segmentation strategies for targeted sends.

## Email Campaign Types

```
┌──────────────────────────────────────────────────────────────┐
│                    E-COMMERCE EMAIL MAP                       │
├──────────────┬──────────────────┬────────────────────────────┤
│   CAMPAIGN   │    ONE-TIME      │       AUTOMATED            │
├──────────────┼──────────────────┼────────────────────────────┤
│ Promotional  │ Flash sale alert │ Abandoned cart recovery    │
│              │ New arrival drop │ Price drop alert           │
│              │ Holiday special  │ Back-in-stock notification │
├──────────────┼──────────────────┼────────────────────────────┤
│ Relationship │ Monthly digest   │ Welcome sequence (3–5)     │
│              │ Event invite     │ Post-purchase thank you    │
│              │ Brand story      │ Birthday / anniversary     │
│              │                  │ Re-engagement (dormant)    │
├──────────────┼──────────────────┼────────────────────────────┤
│ Transactional│ Order confirmed  │ Order shipped              │
│              │ Payment receipt  │ Delivery update            │
│              │ E-gift voucher   │ Review request             │
└──────────────┴──────────────────┴────────────────────────────┘
```

## Email Anatomy

Every marketing email should have these components:

```
┌─────────────────────────────────┐
│  FROM: [Brand Name]             │  Recognizable sender
│  SUBJECT: [Hook — 30–50 chars]  │  Curiosity, urgency, value
│  PREHEADER: [Supporting line]   │  Visible in inbox preview
├─────────────────────────────────┤
│  LOGO / HEADER                  │  Brand recognition
│                                 │
│  HERO IMAGE / GIF               │  Visual hook — product, lifestyle
│                                 │
│  HEADLINE                       │  Reinforce subject line
│                                 │
│  BODY COPY (2–3 short blocks)   │  Value, details, social proof
│                                 │
│  CTA BUTTON (primary)           │  One clear action
│                                 │
│  SECONDARY CTA (optional)       │  Browse, learn more, follow
│                                 │
│  FOOTER: Social links,          │
│  unsubscribe, store info        │
└─────────────────────────────────┘
```

### Subject Line Formulas

| Type | Formula | Example |
|---|---|---|
| **Curiosity** | "The [thing] everyone's asking about" | "The scent everyone noticed at that wedding" |
| **Urgency** | "[Time limit] — [what's at stake]" | "48 hours — then this price is gone" |
| **Personal** | "[Name], [personal observation]" | "Nadini, your skin will thank you" |
| **Listicle** | "[Number] ways to [benefit]" | "3 fragrances that last through monsoon" |
| **Question** | "Ever wonder [intriguing question]?" | "Ever wonder why French perfumes smell different?" |
| **Sneak Peek** | "Just dropped: [product/category]" | "Just dropped: Swarovski's new collection" |
| **Social Proof** | "Everyone's [action] this [product]" | "Sri Lanka's top-selling luxury scent" |

**Rules:**
- 30–50 characters (mobile-optimized)
- No ALL CAPS or excessive punctuation (spam filters)
- Front-load the key words (first 30 chars show in mobile preview)
- A/B test two variants per send

## Newsletter Structure (Monthly Digest)

Sent once per month to all subscribers. Aligns with the monthly campaign theme.

```
SUBJECT: "[Month] at The Parfumerie — [Theme Hook]"

Section 1: HERO STORY
  "This month, we're celebrating [theme]."
  Primary product or collection feature with image + CTA.

Section 2: WHAT'S NEW
  2–3 new arrivals or restocked favorites.
  Each: small image, name, one-line description, price, "Shop Now".

Section 3: EDITOR'S PICK
  One staff-favorite product with personal note.
  "Sophie's pick: [Product] because [reason]."

Section 4: GIFTING IDEA
  Curated suggestion tied to occasion or season.
  "Need a gift? [Bundle name] — Rs. X. Gift wrapped, delivered."

Section 5: REMINDERS
  ● Free islandwide delivery on all orders
  ● Complimentary gift wrapping
  ● E-gift vouchers available (link)

FOOTER CTA: "Follow us on Instagram @theparfumerie.lk"
```

## Promotional Email Sequence

For sales, launches, or special events, use a 3-email sequence:

### Email 1: Teaser (24–48 hours before)

```
Subject: "Something's coming... 👀"
Tone: Mysterious, exciting
Content: Minimal. One hero image, one line of intrigue.
         "Thursday. 10 AM. Be ready."
CTA: "Set a reminder" (calendar link) or "Browse collection" (soft tease)
```

### Email 2: Launch (Day of, 10 AM)

```
Subject: "It's here: [Product / Sale Name]"
Tone: Energetic, celebratory
Content: Full reveal. Hero product image, 3 key benefits,
         price with discount shown, urgency note ("limited stock").
CTA: "Shop Now" (prominent button above the fold)
```

### Email 3: Last Chance (24 hours before end)

```
Subject: "⏳ Last chance — [Product/Sale] ends tomorrow"
Tone: Urgent but not desperate
Content: Social proof ("X sold already"), what they'll miss,
         answer objections ("Free returns", "Islandwide delivery").
CTA: "Don't miss out" or "Get yours before it's gone"
```

## Abandoned Cart Recovery

### Timing

| Email | When | Purpose |
|---|---|---|
| **Email 1** | 1 hour after abandon | Gentle reminder — "Did you forget something?" |
| **Email 2** | 24 hours after | Add social proof — reviews, ratings, popularity |
| **Email 3** | 72 hours after | Incentive — small discount or free delivery |

### Copy Formulas

**Email 1 — Gentle Nudge:**
```
Subject: "Your [product] is waiting..."
Body: "Hi [Name], we noticed you left something behind.
       [Product name] — [one-line description].
       Your cart is saved for now, but stock moves fast.
       Ready to complete your order?"
CTA: "Return to Cart"
```

**Email 2 — Social Proof:**
```
Subject: "People love this [product category]"
Body: "Still thinking about [product]?
       ★★★★★ '[Real customer review quote]'
       [2-3 short review snippets]
       It's a favorite for a reason."
CTA: "See What You're Missing"
```

**Email 3 — Incentive (use sparingly):**
```
Subject: "A little something to help you decide 🎁"
Body: "We'd love for you to experience [product].
       Here's [X% off / free delivery] — just because.
       Valid for 24 hours on your saved cart."
CTA: "Claim Your Discount"
```

## Welcome Sequence (New Subscribers)

5-email sequence over 2 weeks:

```
Day 0:  WELCOME + OFFER
        "Welcome to The Parfumerie — here's 10% off your first order"
        Introduce the brand, set expectations, deliver the discount code.

Day 2:  BRAND STORY
        "The story behind your new favorite fragrance destination"
        Why we exist, Sri Lankan roots, curation philosophy.

Day 4:  BESTSELLERS
        "Sri Lanka's most-loved scents (see what everyone's buying)"
        Top 5 products with reviews, social proof.

Day 7:  HOW WE'RE DIFFERENT
        "Gift wrapping, islandwide delivery, and real authenticity"
        Service differentiators — the experience beyond the product.

Day 14: LAST CHANCE + ENGAGE
        "Your 10% code expires soon — plus, follow us on Instagram"
        Urgency on discount + social follow CTA.
```

## SMS Reminders

Use SMS sparingly — only for time-sensitive, high-value events:

| Use Case | When | Max Length |
|---|---|---|
| Flash sale alert | 2 hours before | 160 chars |
| Launch reminder | Morning of | 160 chars |
| Back-in-stock | Immediately | 160 chars |
| Order update | Real-time | 160 chars |
| Abandoned cart | 4 hours after | 160 chars |

### SMS Copy (160-character constraint)

```
"FLASH SALE: 25% off all fragrances at The Parfumerie.
Today only. Shop now: [short link] Reply STOP to opt out."

"Your order #12345 is out for delivery! 🚚
Track it here: [short link]"

"Good news — [Product] is back in stock.
But only [X] units left. [short link]"
```

**SMS rules:**
- Always include opt-out ("Reply STOP")
- Never send after 8 PM local time
- Maximum 2 promotional SMS per month
- Link to mobile-optimized landing page

## Segmentation Strategy

Divide your list to send relevant content:

| Segment | Criteria | Send |
|---|---|---|
| **Fragrance lovers** | Purchased perfume | New fragrance launches, layering tips |
| **Skincare enthusiasts** | Purchased skincare | New skincare, routines, seasonal tips |
| **Gift buyers** | Purchased gift cards or "gift" orders | Gifting guides, voucher promos, occasions |
| **High-value** | 2+ orders, total > Rs. 15,000 | Early access, VIP offers, personal notes |
| **Dormant** | No open/click in 90 days | Re-engagement: "We miss you" + incentive |
| **New subscribers** | Joined < 30 days ago | Welcome sequence (see above) |

## Timing & Calendar Integration

Align email sends with the monthly campaign calendar:

```
Monthly Digest:    1st of each month (aligns with campaign launch)
New Arrival Alert:  Day of product drop (coordinated with social posts)
Flash Sale:         Friday 8 AM (teaser) → Saturday 10 AM (launch)
Abandoned Cart:     Automated (always on)
Welcome Sequence:   Automated (triggered on signup)
Re-engagement:      Middle of month (between campaigns)
```

**Weekly email cap:** Maximum 3 promotional emails per week per subscriber. Automated/transactional emails don't count toward this cap.

## Email Copy Principles

1. **One goal per email** — don't promote a sale, a new arrival, and a blog post in one email. Pick one CTA.
2. **Mobile-first** — 60%+ opens are on phones. Short paragraphs, large buttons (44px+), single-column layout.
3. **Front-load value** — the reason to care should be visible without scrolling.
4. **Write like a person** — "We think you'll love this" not "The Parfumerie is pleased to announce."
5. **Use the customer's language** — mirror how they describe products in reviews and messages.
6. **Preview text matters** — the preheader is the second subject line. Use it.
7. **Segment or be ignored** — a blanket email to everyone performs worse than a targeted one to a segment.

## Common Mistakes

```
WRONG:
- "CLICK HERE NOW!!! 50% OFF EVERYTHING!!!" (spam filter bait)
- Sending a 2,000-word newsletter with 8 CTAs
- Blasting "Happy Women's Day" to male subscribers
- No unsubscribe link (illegal in most jurisdictions)
- Sending from "noreply@theparfumerie.lk" (kills engagement)
- SMS at 11 PM (anger + opt-outs)

RIGHT:
- "Your weekend scent, sorted. 20% off — today only."
- One hero product, one CTA, clear value proposition
- Segment by purchase history and interest
- Clear unsubscribe link in every email footer
- Send from "Sophie at The Parfumerie" (personal touch)
- SMS before 8 PM, maximum 2/month promotional
```

## Critical Rules

- **Segment before you send** — use purchase history, browsing behavior, and engagement to target.
- **One CTA per email** — clarity beats choice. The reader should never wonder what to do next.
- **Mobile-first design** — single column, large text, thumb-friendly buttons.
- **Always include unsubscribe** — it's not optional; it's the law.
- **A/B test subject lines** — the subject determines whether the email gets opened at all.
- **Align with social calendar** — email and social should feel like one coordinated campaign, not two separate things.
- **SMS is for urgency only** — don't dilute SMS with routine content. Save it for sales, launches, and time-sensitive alerts.
- **Track and iterate** — open rate, click rate, conversion rate. Feed performance back into segmentation and content decisions.

## What This Skill Does NOT Cover

- **Social media publishing** — use `design-social-publishing` for posting content to Instagram, Facebook, Twitter/X, or LinkedIn.
- **CRM contact management** — use `design-crm` for managing customer, lead, and company records (via `toolkit_cpt` on `mcp_ai_customer`, `mcp_ai_lead`).
- **Campaign orchestration** — use `design-campaign-orchestration` to build the monthly marketing calendar that emails align with.
- **SMS-only workflows** — use `design-communications` for transactional SMS and chat-based customer interactions.
- **Analytics and performance tracking** — use `design-analytics-reporting` to measure open rates, click rates, and conversion data.
- **Content creation for social/website** — use `design-social-content` or `design-content-research` for non-email content.
- **Email template/branding infrastructure** — use the NV oOS Design System addon's `nds_*` tools (Settings → Design System → Emails) for template generation, auditing, activation, and Paper Store mirroring.

## Cross-references

- Run **`design-campaign-orchestration`** to align email sends with the monthly marketing calendar.
- Run **`design-content-calendar`** to schedule email sends alongside social posts.
- Run **`design-social-content`** for copywriting principles that apply across channels.
- Run **`design-product-research`** to gather product details for email features.
- Run **`design-brand-kit`** to ensure email visuals and tone match brand guidelines.
- Run **`design-image-generation`** to create email hero images — check your tool list for the Gemini image tool.
- Run **`design-crm`** to manage customer and lead records — use `toolkit_cpt` on `mcp_ai_customer` and `mcp_ai_lead` for segmentation data.
- Run the **`nds_*` tools** (NV oOS Design System addon) to build, audit, and brand the templates these campaigns send through — see the Available Tools table.

---
name: email-newsletter
description: Create and manage email newsletters and automated email sequences. Build subscriber lists, design campaigns, and track performance.
tools_required: [email, wp_users, woo_customers, wp_create_post]
always_on: false
group: marketing
order: 3
suggests: [marketing-strategy, customer-segmentation]
---

# Email Newsletter

Email marketing and newsletter management for WordPress.

## When to Use This Skill

- Creating email newsletters
- Building subscriber lists
- Designing email campaigns
- Setting up automated sequences
- Managing subscriber segments
- Tracking email performance

## Core Capabilities

### List Management
- Build lists from WP users with `wp_users`
- Segment WooCommerce customers with `woo_customers`
- Manage subscriptions
- Handle unsubscribes

### Campaign Creation
- Design newsletters
- Create email sequences
- A/B test subject lines
- Finalize the newsletter draft

### Content
- Create email drafts with `wp_create_post`
- Template management
- Personalization tokens
- Dynamic content

## Email Types

### Newsletter
- Weekly/monthly updates
- Blog post summaries
- Company news
- Industry insights

### Promotional
- Sales announcements
- Coupon codes
- Flash sales
- Holiday promotions

### Transactional
- Order confirmations
- Shipping updates
- Password resets
- Account notifications

### Automated Sequences
- Welcome series
- Onboarding
- Re-engagement
- Post-purchase

## Workflow

### Creating a Newsletter

1. **Plan Content**
   - Define topic/theme
   - Gather content pieces
   - Set send date

2. **Design Email**
   - Choose template
   - Add header image
   - Write copy
   - Include CTAs

3. **Personalize**
   - Add merge tags
   - Segment audience
   - Customize by behavior

4. **Test**
   - Send test email
   - Check all links
   - Preview on mobile

5. **Schedule**
   - Send the email via `email` tool
   - Choose optimal day
   - Confirm segment

### Building an Automated Sequence

#### Welcome Series (5 emails)
```
Email 1 (Immediate): Welcome + What to Expect
Email 2 (Day 2): Your Story/About Us
Email 3 (Day 5): Popular Content/Products
Email 4 (Day 7): Special Offer
Email 5 (Day 10): How Can We Help?
```

#### Abandoned Cart (3 emails)
```
Email 1 (1 hour): Forgot Something?
Email 2 (24 hours): Still Thinking?
Email 3 (72 hours): Last Chance + Discount
```

#### Post-Purchase (4 emails)
```
Email 1 (Immediate): Thank You + Order Details
Email 2 (Day 3): How to Get Started
Email 3 (Day 7): Request Review
Email 4 (Day 14): Related Products
```

## Email Templates

### Newsletter Template
```html
HEADER: Logo + Navigation

HERO: Featured Article/Image

CONTENT:
- Main story (150 words)
- Secondary stories (3x 50 words)
- Product spotlight
- Quick links

FOOTER:
- Social links
- Unsubscribe
- Contact info
```

### Promotional Template
```html
HEADER: Logo + Sale Banner

HERO: Offer Headline + CTA Button

CONTENT:
- Offer details
- Featured products (3-6)
- Urgency element

CTA: Shop Now Button

FOOTER: Terms + Unsubscribe
```

## Segmentation Strategies

### By Engagement
- Active (opened in 30 days)
- Engaged (clicked in 90 days)
- Inactive (no activity 90+ days)
- Never opened

### By Purchase
- Never purchased
- First-time buyer
- Repeat customer
- VIP (high LTV)

### By Interest
- Product categories viewed
- Content topics read
- Email topics clicked

## Best Practices

### Subject Lines
1. **Keep short** - 40-60 characters
2. **Create curiosity** - But don't be clickbait
3. **Use personalization** - First name works
4. **Include numbers** - "5 Tips" performs well
5. **Test variations** - A/B test always

### Content
1. **One main CTA** - Don't overwhelm
2. **Scannable format** - Headers, bullets
3. **Mobile-first** - 60%+ read on mobile
4. **Balance text/images** - Avoid image-only
5. **Personalize** - Beyond just name

### Timing
- Tuesday-Thursday best for B2B
- Weekends can work for B2C
- 10am or 2pm typically optimal
- Test your specific audience

## Key Metrics

| Metric | Target | Description |
|--------|--------|-------------|
| Open Rate | 20%+ | Unique opens / delivered |
| Click Rate | 3%+ | Unique clicks / delivered |
| CTR | 15%+ | Clicks / opens |
| Unsubscribe | <0.5% | Per campaign |
| Bounce Rate | <2% | Hard + soft bounces |
| Conversion | 2%+ | Depends on goal |

## Compliance

### Required Elements
- Physical address
- Unsubscribe link
- Company name
- Privacy policy link

### Regulations
- **CAN-SPAM** (US): Honor opt-outs in 10 days
- **GDPR** (EU): Explicit consent required
- **CASL** (Canada): Express consent needed

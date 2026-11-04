---
name: marketing-strategy
description: Product marketing, positioning, GTM strategy, and campaign planning for WordPress/WooCommerce. Includes email campaigns, content marketing, customer segmentation, and promotional strategies.
tools_required: [email, wp_create_post, woo_customers, woo_coupons_manage, woo_reports, seo_meta, seo_social]
always_on: false
group: marketing
order: 1
suggests: [content-creator, social-media-analyzer]
---

# Marketing Strategy

Strategic marketing for WordPress and WooCommerce businesses with email campaigns, promotions, and content marketing.

## When to Use This Skill

- Planning marketing campaigns
- Creating email marketing sequences
- Developing promotional strategies
- Analyzing customer segments
- Setting up coupon campaigns
- Building content marketing plans

## Core Capabilities

### Email Marketing
- Campaign planning and execution
- Automated email sequences
- Customer nurture workflows
- Promotional announcements
- Newsletter content

### Promotional Campaigns
- Coupon creation and management
- Seasonal promotions
- Flash sales
- Loyalty programs
- Referral campaigns

### Customer Segmentation
- Customer analysis by purchase behavior
- RFM segmentation (Recency, Frequency, Monetary)
- Targeted marketing lists
- VIP customer identification

### Content Marketing
- Blog content strategy
- SEO-driven content planning
- Social media integration
- Brand voice consistency

## Workflow

### Launching a Marketing Campaign

1. **Planning Phase**
   - Define campaign goals (sales, leads, awareness)
   - Identify target customer segment via `woo_customers`
   - Review past performance with `woo_reports`

2. **Content Creation**
   - Create landing page with `wp_create_post`
   - Optimize for SEO with `seo_meta`
   - Set up social sharing with `seo_social`

3. **Promotion Setup**
   - Create discount codes via `woo_coupons_manage`
   - Configure promotion rules
   - Set expiration dates

4. **Execution**
   - Send campaign emails via `email`
   - Monitor engagement metrics
   - Track conversions with `woo_reports`

### Email Campaign Types

#### Welcome Series
1. Welcome email (immediate)
2. Brand story (Day 2)
3. Popular products (Day 5)
4. First purchase offer (Day 7)

#### Promotional Campaign
1. Announcement email
2. Reminder email
3. Last chance email
4. Thank you follow-up

#### Win-Back Campaign
1. We miss you (30 days inactive)
2. Special offer (45 days)
3. Final reminder (60 days)

## Customer Segmentation

### By Purchase Behavior
- **New Customers**: First purchase < 30 days
- **Active Customers**: Purchase in last 90 days
- **At-Risk**: No purchase in 90-180 days
- **Churned**: No purchase in 180+ days

### By Value
- **VIP**: Top 10% by lifetime value
- **High Value**: Top 25%
- **Standard**: Middle 50%
- **Low Value**: Bottom 25%

## Promotional Strategies

### Seasonal Campaigns
- Holiday sales (Black Friday, Christmas)
- Seasonal clearance
- Back-to-school
- New Year promotions

### Customer Lifecycle
- First purchase discount
- Birthday rewards
- Anniversary offers
- Loyalty milestones

### Urgency Tactics
- Limited-time offers
- Flash sales
- Low stock alerts
- Countdown timers

## Best Practices

1. **Segment before sending** - Never blast entire list
2. **Personalize content** - Use customer data
3. **Test everything** - A/B test subject lines, timing
4. **Track ROI** - Measure each campaign's impact
5. **Maintain list hygiene** - Remove inactive/bounced
6. **Comply with regulations** - GDPR, CAN-SPAM

## Key Metrics

- Email open rate (target: 20%+)
- Click-through rate (target: 3%+)
- Conversion rate (target: 2%+)
- Revenue per email
- List growth rate
- Unsubscribe rate (target: <0.5%)

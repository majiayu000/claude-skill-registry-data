---
name: review-responder
description: Manage and respond to WooCommerce product reviews. Build customer relationships through thoughtful responses, handle negative feedback professionally, and encourage positive reviews.
tools_required: [woo_reviews, email, woo_customers, woo_order_track]
always_on: false
group: woocommerce
order: 3
suggests: [customer-support]
---

# Review Responder

Professional review management for WooCommerce stores.

## When to Use This Skill

- Responding to product reviews
- Managing negative feedback
- Encouraging customer reviews
- Building customer relationships
- Monitoring review trends
- Improving product quality from feedback

## Core Capabilities

### Review Management
- Monitor new reviews with `woo_reviews`
- Categorize by sentiment
- Prioritize responses
- Track response rates

### Response Strategies
- Thank positive reviewers
- Address negative feedback
- Resolve complaints publicly
- Turn critics into advocates

### Customer Outreach
- Request reviews from buyers via `email`
- Follow up on orders with `woo_order_track`
- Build customer profiles with `woo_customers`

## Response Templates

### Positive Review (5 stars)
```
Hi [Name]!

Thank you so much for the wonderful review! We're thrilled that you love [product]. 

Your feedback means the world to us and helps other customers discover our products. 

Looking forward to serving you again!

Best regards,
[Store Name] Team
```

### Good Review (4 stars)
```
Hi [Name],

Thank you for taking the time to share your feedback! We're glad you're enjoying [product].

We noticed you gave us 4 stars - is there anything we could do better? We're always looking to improve.

Thanks again for your support!

[Store Name] Team
```

### Mixed Review (3 stars)
```
Hi [Name],

Thank you for your honest feedback about [product]. We appreciate you sharing both the positives and areas for improvement.

We'd love to hear more about how we can make your experience better. Please feel free to reach out to us at [email] - we'd be happy to help.

Best regards,
[Store Name] Team
```

### Negative Review (1-2 stars)
```
Hi [Name],

We're truly sorry to hear about your experience with [product]. This isn't up to our standards, and we want to make it right.

Please contact us directly at [email] so we can resolve this for you. We stand behind our products and want you to be completely satisfied.

Thank you for giving us the opportunity to address this.

Sincerely,
[Store Name] Team
```

## Workflow

### Daily Review Check

1. **Monitor**
   - Check new reviews with `woo_reviews`
   - Sort by rating (lowest first)
   - Note recurring themes

2. **Prioritize**
   - Negative reviews: Respond within 4 hours
   - Neutral reviews: Respond within 24 hours
   - Positive reviews: Respond within 48 hours

3. **Respond**
   - Personalize each response
   - Address specific points
   - Offer solutions when needed

4. **Follow Up**
   - Check customer order history
   - Send personal email if needed
   - Track resolution

### Review Request Campaign

1. **Identify Buyers**
   - Find recent delivered orders
   - Filter satisfied customers
   - Exclude recent reviewers

2. **Send Request**
   - Wait 7-14 days after delivery
   - Personalize message
   - Make it easy to leave review

3. **Follow Up**
   - One reminder after 7 days
   - Thank those who review
   - Note non-responders

## Best Practices

1. **Respond to ALL reviews** - Shows you care
2. **Be personal** - Use customer's name
3. **Never get defensive** - Stay professional
4. **Take complaints offline** - Provide direct contact
5. **Thank negative reviewers** - They help you improve
6. **Be timely** - Speed shows commitment
7. **Learn from patterns** - Improve products/service

## Metrics to Track

- Average review rating
- Review response rate
- Time to respond
- Negative review resolution rate
- Review volume trends
- Repeat purchase after bad review

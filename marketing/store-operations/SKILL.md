---
name: store-operations
description: Use when managing Xiaohongshu shop daily operations, handling inventory and orders, processing customer purchases, coordinating shipping and fulfillment, or planning shop promotions and activities
---

# Store Operations (店铺运营)

## Overview

Store operations is the day-to-day management of Xiaohongshu e-commerce shop, including inventory management, order processing, customer service coordination, shipping logistics, and promotional activities to ensure smooth, efficient business operations.

## When to Use

**Use when**:
- Managing daily shop operations and tasks
- Processing and fulfilling customer orders
- Managing inventory levels and restocking
- Coordinating shipping and logistics
- Planning shop promotions and discounts
- Handling shop analytics and performance tracking

**Do NOT use when**:
- Creating content to drive traffic (use seeding-content-creation)
- Optimizing product pages for conversion (use conversion-optimization)
- Handling complex customer service issues (use customer-service)

## Core Pattern

**Before** (reactive, disorganized):
```
❌ "Oh, someone ordered, let me see if I have that in stock..."
❌ "Sold out? Didn't realize, sorry for the delay..."
❌ "Shipping? I'll get to it sometime this week..."
❌ "Customer complaint? I'll respond when I have time..."
```

**After** (proactive, systematic):
```
✅ "Daily checklist complete: 15 orders processed, 12 shipped,
  inventory updated, 3 customer inquiries resolved"

✅ "Low stock alert: Product A has 8 units left,
  reordering 50 units today"

✅ "Weekly promotion planned: Flash sale Friday,
  20% off top 3 products, marketing scheduled"

✅ "Monthly review complete: 823 orders, 4.7% return rate,
  top seller identified, inventory optimized"
```

**5 Store Operations Pillars**:
1. **Inventory Management** - Stock levels, restocking, product organization
2. **Order Processing** - Order verification, picking, packing, shipping
3. **Customer Service** - Inquiries, issues, returns, refunds
4. **Logistics Coordination** - Shipping partners, tracking, delivery
5. **Promotion Planning** - Discounts, events, marketing activities

## Quick Reference

| Operation | Frequency | Time Required | Key Tools |
|-----------|-----------|---------------|------------|
| **Order Processing** | Daily | 30-60 min | Xiaohongshu Shop后台 |
| **Inventory Check** | Daily | 15 min | Spreadsheet, Shop后台 |
| **Customer Response** | Daily | 30-60 min | Shop messages, Email |
| **Shipping** | Daily | 30-45 min | Shipping software |
| **Analytics Review** | Weekly | 30 min | Shop analytics |
| **Promotion Planning** | Monthly | 2-3 hours | Calendar, Marketing tools |

## Implementation

### Step 1: Set Up Shop Infrastructure

**Choose Shop Type**:
```
Type 1: Xiaohongshu Native Shop (小红书店铺)
- Pros: Integrated platform, trusted by users, seamless checkout
- Cons: Platform commission (5-10%), limited customization
- Best for: Most sellers, especially starting out

Type 2: Third-Party Integration (外部店铺)
- Examples: Taobao, JD, WeChat mini-program linked from Xiaohongshu
- Pros: More control, potentially lower fees, established infrastructure
- Cons: Users must leave platform, friction in purchase flow
- Best for: Established businesses with existing e-commerce

Type 3: Hybrid Approach (Recommended for Growth)
- Start with Xiaohongshu native shop (trust, convenience)
- Expand to third-party as volume grows (cost savings)
- Link to external shop for products not allowed on native shop
```

**Essential Shop Setup Checklist**:
```
Account & Legal:
✅ Business license (individual or enterprise)
✅ Bank account for payments
✅ Tax registration (if applicable)
✅ Contact information (email, phone, address)

Shop Configuration:
✅ Shop name and branding
✅ Shop description and policies
✅ Shipping zones and rates
✅ Payment methods
✅ Return and refund policies
✅ Product categories and navigation

Product Setup:
✅ High-quality product images (3-5 per product)
✅ Detailed product descriptions
✅ Pricing (cost + margin + platform fee calculation)
✅ Inventory tracking enabled
✅ Product tags and keywords for search
✅ Shipping specifications (weight, dimensions)
```

### Step 2: Establish Daily Operations Routine

**Morning Routine (30-45 minutes)**:
```
Task 1: Order Review (10 min)
- Check for new orders overnight
- Verify inventory availability
- Flag any issues (out of stock, damaged items)
- Prioritize orders for same-day shipping

Task 2: Inventory Check (10 min)
- Update inventory from yesterday's sales
- Check for low stock alerts (reorder if needed)
- Note any discrepancies (shrinkage, damage)
- Update spreadsheet/shop system

Task 3: Customer Service Check (15 min)
- Respond to overnight inquiries
- Address urgent issues (shipping problems, complaints)
- Process return/refund requests
- Track response time SLA
```

**Midday Routine (30-60 minutes)**:
```
Task 4: Order Processing (20-30 min)
- Pick items from inventory
- Verify product condition
- Package items securely
- Print shipping labels
- Arrange pickup or drop-off

Task 5: Customer Engagement (10-30 min)
- Respond to new customer inquiries
- Thank customers for purchases
- Proactively address potential issues
- Build relationships for repeat business
```

**Evening Routine (15-20 minutes)**:
```
Task 6: Daily Review (15 min)
- Confirm all orders shipped
- Update tracking numbers
- Final customer responses
- Prepare tomorrow's task list
- Document any issues or lessons learned
```

### Step 3: Inventory Management System

**Track Inventory with Spreadsheet**:
```
Inventory Spreadsheet Template:

Product | SKU | Current Stock | Low Stock Alert | Reorder Qty | Cost | Price | Margin | Supplier | Lead Time | Last Updated
---------|-----|---------------|-----------------|-------------|------|-------|--------|----------|-----------|-------------
Product A | A001 | 47 units | <10 units | 50 units | ¥15 | ¥89 | 83% | Supplier X | 3 days | 2026-01-22
Product B | B002 | 8 units | <15 units | 30 units | ¥22 | ¥129 | 83% | Supplier Y | 5 days | 2026-01-22
Product C | C003 | 123 units | <20 units | 50 units | ¥18 | ¥99 | 82% | Supplier Z | 2 days | 2026-01-22

Daily Updates:
- Subtract sold items
- Add received stock
- Flag items at low stock level
- Calculate reorder timing (lead time buffer)
```

**Reorder Strategy**:
```
Reorder Formula:
Reorder Point = (Daily Sales × Lead Time) + Safety Stock

Example:
- Daily sales: 5 units/day
- Lead time: 5 days
- Safety stock: 20 units (buffer for demand spikes)

Reorder Point = (5 × 5) + 20 = 45 units
When stock hits 45, reorder 50 units

Reorder Triggers:
✅ Stock hits reorder point
✅ Upcoming promotion planned (increase buffer)
✅ Seasonal demand spike approaching
✅ Supplier delay or stockout risk

Batch vs JIT Ordering:
- Batch ordering: Order 50-100 units at a time
  - Pros: Volume discounts, safety stock
  - Cons: Higher upfront cost, storage needs

- Just-in-time: Order 20-30 units frequently
  - Pros: Lower storage, fresher stock
  - Cons: Higher risk of stockouts, less negotiating power
```

**Inventory Optimization**:
```
ABC Analysis (Prioritize Management):
A-Items (Top 20% of products, 80% of sales):
- Monitor daily
- Never stock out
- Highest safety stock
- Best shelf placement

B-Items (Middle 30% of products, 15% of sales):
- Monitor weekly
- Standard safety stock
- Regular review

C-Items (Bottom 50% of products, 5% of sales):
- Monitor monthly
- Minimal safety stock
- Consider discontinuing if not profitable

Slow-Moving Stock Actions:
- Bundle with popular products
- Offer discounts/clearance
- Use as free gifts with purchase
- Donate or write off if unsellable
```

### Step 4: Order Processing Workflow

**Order Verification**:
```
Before Processing:
✅ Confirm payment received
✅ Verify shipping address is complete
✅ Check inventory availability
✅ Flag special requests (gift wrap, note, etc.)
✅ Check for fraud risk (unusual orders)

Red Flags to Review:
- Large first order (new customer, high value)
- Different shipping/billing address
- Overnight shipping request
- Multiple orders same customer
- Unusual product combination

When in doubt:
- Contact customer to verify
- Use signature-required delivery
- Consider holding shipment until verified
```

**Picking and Packing**:
```
Picking Process:
1. Print order pick list (batch orders for efficiency)
2. Navigate to inventory locations
3. Verify SKU matches order
4. Inspect item condition (no damage, seals intact)
5. Set aside for packing

Packing Best Practices:
✅ Use appropriate packaging size (not too big, not too small)
✅ Protect items with bubble wrap or packing paper
✅ Include branded materials (thank you card, sticker)
✅ Add packing slip with order details
✅ Seal securely with packaging tape
✅ Apply shipping label clearly visible

Unboxing Experience:
- Thank you note (handwritten if possible)
- Small free sample or gift (delight factor)
- Care instructions or usage tips
- Branded packaging materials
- Contact information for questions

Cost Optimization:
- Reuse supplier packaging when possible
- Standardize box sizes (reduce inventory)
- Negotiate volume shipping rates
- Use poly mailers for lightweight items
- Bulk purchase packaging materials
```

**Shipping Coordination**:
```
Shipping Partner Selection:
- China Post (economical, slower)
- SF Express (reliable, faster, more expensive)
- YTO Express (balanced cost/speed)
- STO Express (budget option)

Shipping Strategy:
- Default: Standard shipping (3-7 days)
- Express: Paid upgrade (1-3 days)
- Free shipping: On orders over ¥199
- Same-day: For urgent orders (additional fee)

Tracking Process:
1. Generate shipping label with tracking number
2. Send tracking to customer via message/email
3. Monitor delivery progress
4. Proactively address delays or issues
5. Confirm delivery, request feedback

International Shipping (if applicable):
- Use cross-border logistics partners
- Clearly communicate delivery times (10-20 days)
- Handle customs declarations properly
- Insurance for high-value orders
```

### Step 5: Customer Service Integration

**Pre-Sale Inquiries**:
```
Common Questions:
- Product details: ingredients, materials, sizing
- Availability: in stock, restock date
- Shipping: time, cost, international options
- Returns: policy, process, who pays
- Payment: methods, security, refunds

Response Standards:
✅ Respond within 2 hours during business hours
✅ Within 24 hours maximum
✅ Friendly, professional tone
✅ Complete answers (not one-word responses)
✅ Include helpful links (product page, FAQ)
✅ Personalize (use customer name if known)

Response Templates:
Create templates for common questions but personalize:
"Hi [Customer Name], thanks for reaching out!

Yes, [Product Name] is perfect for [specific use case].
 It contains [key ingredients/features] that help with [benefit].

Currently [X] units in stock - ready to ship within 24 hours!
 Free shipping on orders over ¥199.

Any other questions? I'm here to help! 😊"

[Your Name]
Xiaohongshu Shop: [Shop Name]
```

**Post-Sale Support**:
```
Order Confirmation:
"Hi [Customer Name], great news! Your order #[Order Number]
 has been confirmed and will ship within 24 hours.

📦 What you ordered: [Product List]
🚚 Estimated delivery: [Date]
📍 Shipping to: [Address]

You'll receive a tracking number once it ships.
 Questions? Just reply to this message!

Thanks for supporting my shop! 💕"

Shipping Notification:
"Great news, [Customer Name]! Your order #[Order Number]
 has shipped and is on its way to you!

📦 Tracking: [Tracking Number]
🚚 Carrier: [Shipping Partner]
📅 Estimated delivery: [Date]

Track your package here: [Tracking Link]

Can't wait for you to receive your order! Let me know
 if you have any questions. 😊"

Follow-Up (3-5 days after delivery):
"Hi [Customer Name], just checking in - did your order arrive?
 Hope you're loving [Product Name]!

If you have any questions or need help with anything,
 just reply to this message. I'm here to help!

If you're happy with your purchase, would you mind
 leaving a quick review? It really helps my small shop! 🙏

Thanks again for your support! 💕"
```

### Step 6: Analytics and Performance Tracking

**Daily Metrics to Track**:
```
Sales Metrics:
- Orders received
- Revenue (GMV - Gross Merchandise Value)
- Average order value (AOV)
- Units sold per product
- Net revenue (after returns/refunds)

Operational Metrics:
- Orders shipped
- Orders pending
- Inventory levels
- Customer service inquiries
- Response time

Formulas:
AOV = Total Revenue ÷ Number of Orders
Conversion Rate = Orders ÷ Shop Visitors × 100
Return Rate = Returns ÷ Orders Shipped × 100
```

**Weekly Review** (30 minutes):
```
Performance Analysis:
1. Top 3 selling products (why?)
2. Bottom 3 selling products (why?)
3. Average order value trend
4. Customer service trends (common issues?)
5. Inventory status (any stockouts?)
6. Shipping performance (delays, issues?)

Action Items:
- Restock low inventory
- Address common customer issues
- Plan promotions for slow-moving products
- Adjust pricing if needed
- Celebrate wins (share with team/followers)
```

**Monthly Review** (1-2 hours):
```
Business Health Check:
Revenue Analysis:
- Total revenue vs target
- Growth rate (month-over-month)
- Profit margin (after all costs)

Product Performance:
- Product profitability matrix
- ABC analysis (update annually)
- Seasonal trends

Customer Insights:
- Repeat customer rate
- Customer acquisition cost
- Lifetime value (LTV)
- Satisfaction (review score)

Operational Efficiency:
- Average fulfillment time
- Return/refund rate
- Customer service response time
- Inventory turnover rate

Strategic Decisions:
- Expand or contract product line
- Adjust pricing strategy
- Negotiate with suppliers
- Invest in marketing/growth
- Hire help or outsource tasks
```

### Step 7: Promotion and Activity Planning

**Promotion Calendar**:
```
Monthly Promotions:
Week 1: Flash Sale (24-hour sale, 20-30% off)
Week 2: Bundle Deal (buy 2 get 10% off, buy 3 get 20% off)
Week 3: Free Gift (spend ¥199+ get free gift worth ¥49)
Week 4: New Product Launch (exclusive early-bird pricing)

Seasonal Promotions:
- Chinese New Year: Holiday bundles, gift ideas
- 3.8 Women's Day: Female-focused products
- 6.18 Shopping Festival: Major sale event
- 11.11 Singles' Day: Biggest sale of the year
- 12.12 Double Twelve: End-of-year clearance

Promotion Planning Steps:
1. Set objectives (sales volume, inventory clearance, new product)
2. Choose discount type (percentage, fixed amount, bundle, free gift)
3. Calculate profitability (can we afford this discount?)
4. Set duration (24 hours, 3 days, 1 week)
5. Plan marketing (posts, stories, live stream)
6. Prepare inventory (ensure sufficient stock)
7. Test promotion (ensure discount codes work)
8. Launch and monitor
9. Analyze results
10. Document learnings for next time
```

**Flash Sale Execution**:
```
Flash Sale Framework:
Theme: [Name] Flash Sale
Duration: 24 hours (9:00 AM - 9:00 PM next day)
Discount: 30% off select products
Goal: Clear slow-moving inventory + boost revenue

Pre-Promotion (3 days before):
- Teaser: "Something BIG coming Friday..."
- Sneak peek: Reveal which products
- Build anticipation: Countdown in stories

Launch Day:
- Morning: Announcement post with details
- Midday: Reminder in stories
- Evening: Final call (6 hours left)

During Promotion:
- Monitor stock levels (don't oversell)
- Respond quickly to inquiries
- Share social proof (X units sold!)
- Create urgency (time remaining)

Post-Promotion:
- Thank customers
- Share results (sold X units!)
- Ship orders quickly (positive experience)
- Analyze what worked, what didn't
```

## Common Mistakes

| Mistake | Why Happens | Fix |
|---------|-------------|-----|
| No daily operations routine | Reactive, not proactive | Establish morning/midday/evening checklist |
| Manual inventory tracking (no system) | Spreadsheet feels enough | Use shop inventory system + spreadsheet backup |
| Ignoring low stock alerts | Busy, will get to it later | Set reorder points, automate reorder reminders |
| Poor packaging (damaged items) | Saving costs on materials | Quality packaging reduces returns by 60% |
| Slow customer service response | Overwhelmed, not prioritized | Set response time SLA, use templates |
| Not tracking shop metrics | Don't see value in data | Weekly review catches issues early |
| Over-promising on shipping | Want to make sale | Under-promise, over-deliver on delivery times |
| No promotion planning | Last-minute decisions | Monthly promotion calendar |
| Ignoring customer feedback | Defensive about criticism | Feedback = insights for improvement |
| Doing everything yourself | Want control, save money | Outsource fulfillment, hire help as volume grows |

## Real-World Impact

**Case Study: Shop Operations Transformation**
- **Before**: Chaotic operations, 15% error rate, 4.2/5 rating, slow growth
- **After**: Implemented systematic operations, 3% error rate, 4.8/5 rating, 2.3x growth
- **Result**: Professional operations enabled sustainable scaling

**Data-Backed Insights**:
- Shops with daily routines process 40% more orders with same effort
- Inventory tracking systems reduce stockouts by 70%
- Fast customer response (<2 hours) increases repeat purchases by 50%
- Quality packaging reduces returns by 60% and increases reviews by 80%
- Weekly analytics reviews catch problems before they become crises
- Planned promotions outsell impromptu sales by 2-3x

## Related Skills

**REQUIRED**: Use product-selection (manage inventory of selected products)
**REQUIRED**: Use customer-service (handle complex customer issues)

**Recommended for shop management**:
- **conversion-optimization** - Optimize product pages for sales
- **seeding-content-creation** - Drive traffic to shop
- **data-analytics** - Track shop performance and trends
- **livestream-sales** - Generate surge of orders from live streams

**Use store-operations AFTER**:
- product-selection (have products to manage)
- livestream-sales (fulfill orders from live sales)
- seeding-content-creation (process orders from content conversions)

**Related e-commerce skills**:
- **customer-service** (integrated with shop operations)
- **conversion-optimization** (shop pages need optimization)
- **promotion-strategy** (plan and execute shop promotions)

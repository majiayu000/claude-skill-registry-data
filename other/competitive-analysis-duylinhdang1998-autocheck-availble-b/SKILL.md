---
name: competitive-analysis
description: Competitive Analysis using Google's Intelligence Framework. Use when analyzing competitor websites, extracting features from reference products, mapping user journeys, detecting tech stacks, or when the user says "build like X.com". Covers site analysis, feature extraction with MoSCoW prioritization, user journey mapping, and tech stack detection. Triggers on competitor analysis, "giống như", "like X", feature comparison, market research, or reverse-engineering existing products.
---

# Competitive Analysis - Google Intelligence Framework

**Purpose**: Analyze competitor websites to extract features, user flows, and actionable insights for product development

**Agent**: Google Competitive Analyst
**Use When**: Client requests "build like X.com" or references existing website

---

## Overview

This skill provides systematic approaches to analyze competitor websites and extract knowledge that directly informs product requirements, design, and development.

**Core Philosophy**:
- Understand before building
- Learn from successful products
- Extract patterns, not just copy
- Focus on user value
- Identify opportunities for differentiation

---

## Available Reference Guides

### 1. Site Analysis
**File**: `references/site-analysis.md`

**Covers**:
- Initial reconnaissance (homepage, structure, sections)
- User type identification (buyer, seller, admin, guest)
- Page inventory (list all page types)
- Site architecture mapping
- Screenshot methodology

**When to Use**: First step of any competitive analysis

**Key Questions**:
- What is the main purpose of this site?
- Who are the target users?
- What are the main sections/features?
- How is navigation organized?

---

### 2. Feature Extraction
**File**: `references/feature-extraction.md`

**Covers**:
- Systematic feature discovery
- Feature categorization (Must/Should/Could have)
- Priority assessment framework
- Unique selling point identification
- Feature-to-business-value mapping

**When to Use**: After site reconnaissance

**MoSCoW Prioritization**:
- **Must Have** (60%): Features without which the product cannot function
- **Should Have** (20%): Important features that enhance experience
- **Could Have** (15%): Nice-to-have competitive advantages
- **Won't Have** (5%): Out of scope or future consideration

**Example - E-commerce Site**:
```
Must Have:
- Product catalog with search
- Shopping cart
- Checkout flow
- User accounts
- Order management

Should Have:
- Product reviews
- Wishlist
- Order tracking
- Multiple payment methods

Could Have:
- Live chat support
- Product recommendations
- Loyalty program
- Social sharing

Won't Have (defer to v2):
- Live streaming shopping
- AR product preview
- Seller marketplace
```

---

### 3. User Journey Mapping
**File**: `references/user-journey-mapping.md`

**Covers**:
- Identifying key user journeys
- Step-by-step flow documentation
- Screenshot collection for each step
- Friction point identification
- Success metrics for each journey

**When to Use**: Understanding user flows for requirements

**Key Journeys to Map**:
1. **New User Activation**: Homepage → First value
2. **Core Action**: Main user action (buy, post, search, etc.)
3. **Power User Flow**: Advanced features
4. **Account Management**: Settings, preferences, profile

**Journey Template**:
```markdown
## Journey: [Name]

**Goal**: [What user wants to achieve]
**Entry Point**: [Where journey starts]
**Success Metric**: [How to measure success]

### Steps:
1. [Action] → [Result]
   Screenshot: [filename]
   Notes: [observations]

2. [Action] → [Result]
   Screenshot: [filename]
   Notes: [observations]

[Continue for all steps]

### Friction Points:
- [Issue 1]: [Impact]
- [Issue 2]: [Impact]

### Improvements Opportunity:
- [Improvement 1]
- [Improvement 2]
```

---

### 4. Tech Stack Detection
**File**: `references/tech-detection.md`

**Covers**:
- Frontend framework detection (React, Vue, Angular)
- Rendering strategy (SPA, SSR, SSG)
- API pattern identification (REST, GraphQL, gRPC)
- Performance metrics observation
- Mobile strategy (responsive, native app, PWA)

**When to Use**: Informing CTO's tech stack decision

**Detection Methods**:
- **View Page Source**: Look for framework signatures
- **Network Tab**: API endpoints, request patterns
- **Performance Tab**: Rendering strategy clues
- **Console**: Framework detection scripts
- **Wappalyzer**: Automated tech detection

**Example Analysis**:
```
Frontend:
- Framework: React 18 (detected: __REACT_DEVTOOLS_GLOBAL_HOOK__)
- Rendering: Server-Side Rendering (HTML in source)
- Styling: Tailwind CSS (utility classes)
- State: Likely Redux (predictable state container)

Backend (inferred):
- API: REST (endpoints like /api/products)
- Real-time: WebSocket (ws:// connections seen)
- CDN: CloudFlare (CF-Ray headers)

Performance:
- FCP: 1.2s (good)
- LCP: 2.3s (needs improvement)
- TTI: 3.1s (average)
```

---

## Quick Start

### For Competitive Analyst (you):

```bash
# Step 1: Initial Analysis
Read: references/site-analysis.md
Visit: Target website
Map: Site structure
Screenshot: Key pages (homepage, main sections)

# Step 2: Feature Discovery
Read: references/feature-extraction.md
List: ALL features observed
Categorize: Must/Should/Could/Won't
Prioritize: Based on business value

# Step 3: User Journey Mapping
Read: references/user-journey-mapping.md
Identify: 3-5 key journeys
Map: Each journey step-by-step
Screenshot: Each step
Note: Friction points

# Step 4: Tech Analysis
Read: references/tech-detection.md
Inspect: Page source, network, performance
Detect: Framework, rendering, API patterns
Document: Tech stack observations

# Step 5: Generate Report
Synthesize: All findings
Create: Competitive analysis report
Save: To .project/requirements/competitive-analysis.md
Present: To CEO for decision-making
```

### For Other Agents:

**CEO**: Review analysis report, decide on project scope
**CTO**: Use tech recommendations for stack decision
**PM**: Use feature list for timeline estimation
**BA**: Convert features to user stories and requirements

---

## Example Analysis: Shopee.com

### Site Type
E-commerce marketplace (C2C + B2C)

### Must-Have Features
1. **Product Catalog**
   - Multi-category browse
   - Search with filters (price, rating, location)
   - Product recommendations

2. **Shopping Cart**
   - Add/remove items
   - Quantity adjustment
   - Apply vouchers
   - Calculate shipping

3. **Checkout Flow**
   - Address selection
   - Payment method (credit card, e-wallet, COD)
   - Order review
   - Confirmation

4. **User Account**
   - Registration/Login
   - Profile management
   - Order history
   - Wishlist

5. **Seller Dashboard**
   - Product listing
   - Inventory management
   - Order fulfillment
   - Analytics

### Key User Journey: First Purchase

```
1. Land on homepage
   → See featured products, categories, search bar

2. Search for product
   → Enter "laptop" in search
   → See results with filters

3. Browse results
   → Filter by price, rating
   → Click on product

4. View product details
   → See images, specs, reviews
   → Choose variant (color, size)
   → Click "Add to Cart"

5. Review cart
   → See items, total price
   → Apply voucher (optional)
   → Proceed to checkout

6. Checkout
   → Select shipping address
   → Choose payment method
   → Confirm order

7. Order confirmation
   → See order number
   → Receive email confirmation
   → Can track order

Friction Points:
- Too many steps (7 steps to checkout)
- Voucher application not obvious
- Payment methods scattered

Opportunities:
- Guest checkout (no signup required)
- Saved payment methods
- One-click purchase for returning users
```

### Tech Stack (Estimated)

**Frontend**: React SPA with SSR
**Mobile**: Native apps (iOS/Android)
**Backend**: Microservices (product, cart, order, payment, user)
**Database**: PostgreSQL + Redis (caching)
**CDN**: Global content delivery
**Real-time**: WebSocket (chat, notifications)

### Recommended MVP (8 weeks)

**Phase 1** (Week 1-4):
- Product catalog + search
- Shopping cart
- User authentication
- Basic checkout

**Phase 2** (Week 5-6):
- Payment integration
- Order management
- Basic seller dashboard

**Phase 3** (Week 7-8):
- Reviews & ratings
- Order tracking
- Polish & testing

**Defer to v2**:
- Voucher system
- Live chat
- Flash sales
- Mobile apps

---

## Analysis Templates

### Feature Matrix Template

```markdown
| Feature | Shopee | Lazada | Tokopedia | Priority | Notes |
|---------|--------|--------|-----------|----------|-------|
| Product Search | ✓ | ✓ | ✓ | Must | Basic requirement |
| Shopping Cart | ✓ | ✓ | ✓ | Must | Core e-commerce |
| Live Chat | ✓ | ✗ | ✓ | Should | Customer support |
| Flash Sales | ✓ | ✓ | ✗ | Could | Competitive edge |
```

### Competitive Positioning

```markdown
## Market Position

**Shopee**:
- Strength: Gamification, free shipping, social features
- Weakness: Product quality inconsistent
- Target: Mass market, price-conscious

**Our Opportunity**:
- Focus on quality verification
- Premium experience
- Better seller vetting
```

---

## Integration with /work Workflow

### CEO Detection Phase

When CEO receives: `/work làm e-commerce giống shopee.com`

**CEO Action**:
1. Parse request: Detect "giống shopee.com"
2. Extract reference: "shopee.com"
3. Call Competitive Analyst: "Analyze shopee.com"
4. Wait for analysis report
5. Use report to inform CTO/PM/BA

### BA Requirements Phase

**BA receives competitive analysis report**:
1. Read feature list
2. Convert to user stories:
   ```
   Feature: "Shopping Cart"
   ↓
   User Story:
   "As a shopper, I want to add products to cart
    so that I can review before checkout"
   ↓
   Acceptance Criteria:
   - Can add items to cart
   - Can adjust quantity
   - Can remove items
   - Can see total price
   - Can apply vouchers
   ```

### CTO Tech Decision Phase

**CTO receives tech stack recommendations**:
1. Review detected tech stack
2. Consider scale requirements
3. Make informed decision based on proven patterns

---

## Success Metrics

**Analysis Quality**:
- Completeness: All major features identified (95%+)
- Accuracy: Tech stack detection verified
- Actionability: Clear MVP recommendations

**Time Efficiency**:
- Small site (<10 pages): <30 minutes
- Medium site (<50 pages): <1 hour
- Large site (>50 pages): <2 hours

**Impact**:
- Requirements clarity: 80% of user stories from analysis
- Time saved: 50% reduction in requirements gathering
- Accuracy: 90% feature parity with reference site (for MVP)

---

## Remember

🔍 **Analyze comprehensively** - Don't miss hidden features

📊 **Prioritize ruthlessly** - Not all features are equal

🎯 **Focus on user value** - Understand WHY features exist

💡 **Find opportunities** - What can we do better?

📝 **Document everything** - Screenshots, flows, insights

---

**For detailed procedures, read the reference guides in `references/` folder**

**Created**: 2026-02-04
**Maintained By**: Google Competitive Analyst
**Review Cycle**: After each competitive analysis

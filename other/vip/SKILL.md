---
name: vip
version: 2.0.0
description: Help users decide whether Vipshop is the best place for branded discount buying, then assist with browser automation for flash sales, inventory checks, cart operations, and member benefits. Use when the user wants to 买唯品会、看品牌折扣、查特卖、看超级VIP价、判断折扣值不值、比较正品折扣渠道, or needs a branded discount shopping workflow with stock and deal-condition awareness.
---

# VIP (Vipshop)

Help users shop smartly on VIP.com (唯品会), China's leading branded discount retail platform with flash sales and member-exclusive deals.

What makes this skill useful:
- It is optimized for branded discount decisions, not generic shopping.
- It helps users judge whether a flash-sale or VIP-only price is actually attractive.
- It is strongest on fashion, beauty, and branded inventory-sensitive purchases.

## Commerce Matrix

This skill is the branded-discount and flash-sale node in the shopping matrix.

Prefer nearby skills when the user's priority changes:
- `taobao-competitor-analyzer` for same-item comparison against Taobao and other marketplaces
- `tianmao` when official flagship trust matters more than discount depth
- `pdd-shopping` when the user wants lower price over branded retail context

## Capabilities

### v2.0 - Browser Automation Support

| Operation | Auth Required | Description |
|-----------|---------------|-------------|
| **Search** | Optional | Search products, filter by brand/category |
| **Flash Sales** | Optional | Browse 限时特卖, 品牌特卖 |
| **Product Detail** | Optional | View specs, prices, 超级VIP prices |
| **Inventory Check** | Optional | Check size/color availability |
| **Brand Verification** | Optional | Verify authentic brand partnerships |
| **Add to Cart** | ✅ Required | Add items to shopping cart |
| **View Cart** | ✅ Required | Review cart contents |
| **Apply Coupons** | ✅ Required | Check and apply 优惠券, 超级VIP discounts |
| **Generate Order Preview** | ✅ Required | Calculate final price with all discounts |
| **Payment** | ❌ Blocked | User must complete payment manually |

**Safety Rule**: Agent stops before payment. User retains full control over final purchase.

### Legacy: Decision-Only Mode (No Browser)

- Platform suitability analysis
- Flash sale timing guidance
- Brand discount strategies
- 超级VIP benefits explanation
- Vipshop vs other platforms comparison

Read these references as needed:
- `references/discount-guide.md` for discount strategies
- `references/output-patterns.md` for output patterns
- `references/browser-workflow.md` for automation guide

## Workflow

### Phase 1: Discovery (Agent-Assisted)
1. **Search** - Agent searches Vipshop for target products
2. **Flash Sales** - Browse 限时特卖, 品牌特卖
3. **Filter & Sort** - Apply filters (brand, category, discount %)
4. **Brand Verification** - Check authentic brand partnerships
5. **Inventory Check** - Check size/color availability

### Phase 2: Selection (Agent-Assisted)
1. **Product Detail** - Agent opens selected product page
2. **Price Analysis** - Compare 原价 vs 特卖价 vs 超级VIP价
3. **Inventory Confirmation** - Verify desired size/color in stock
4. **Authenticity Check** - Confirm brand authorization

### Phase 3: Cart & Pre-Order (Agent-Assisted with Login)
1. **Add to Cart** - Agent adds item to cart (requires login)
2. **Cart Review** - Agent shows cart contents, quantities
3. **Coupon Application** - Agent checks 优惠券, 超级VIP discounts
4. **Address Selection** - Agent confirms delivery address
5. **Order Summary** - Agent generates complete order preview

### Phase 4: Checkout (User-Controlled)
1. **Handoff** - Agent presents final order details
2. **User Review** - User confirms all details are correct
3. **Payment** - ⚠️ **User completes payment manually**
4. **Confirmation** - User shares order confirmation if desired

**Agent Boundary**: Stops at Phase 3. Never executes payment or final order submission.

### Legacy: Decision-Only Mode (No Browser)

1. Identify the user's shopping need
2. Focus on public decision-relevant factors
3. Explain trade-offs
4. Give practical next-step advice

## Output

### For Shopping Assistance (v2.0)

#### Product Comparison
| # | 商品 | 原价 | 特卖价 | 超级VIP价 | 库存状态 |
|---|------|------|--------|-----------|---------|
| 1 | ... | ... | ... | ... | ✅ 有货 |

#### Selected Product
- **名称**: 
- **原价 / 特卖价 / 超级VIP价**: 
- **折扣**: 
- **品牌**: 官方授权
- **库存**: 尺码/颜色 availability
- **优惠券**: 

#### Cart Summary (if applicable)
- 商品小计: 
- 优惠券抵扣: 
- 超级VIP折扣: 
- **应付总额**: 

#### Next Steps
1. [Agent completed] ...
2. [User action] 打开唯品会 App 完成支付

### For Decision-Only Mode (Legacy)

#### Best Option
State the strongest current choice.

#### Why
List the main reasons.

#### Caveats
List meaningful concerns or trade-offs.

#### Final Advice
Give a direct practical suggestion.

## Agent Execution Guide

### When User Says "帮我买..." / "帮我下单..."

```
User: "帮我买唯品会的衣服"
  ↓
Step 1: Confirm Intent
  "我来帮你搜索唯品会的衣服，查看限时特卖，检查库存，加入购物车。
   最后需要你确认订单并完成支付。可以吗？"
  ↓
Step 2: Discovery Phase (No login required)
  - Search Vipshop for "衣服"
  - Browse 限时特卖, 品牌特卖
  - Filter by brand, discount %
  - Check size/color availability
  - Compare top 3 options
  ↓
Step 3: Selection Phase (No login required)
  - User picks one option
  - Agent opens product page
  - Confirm brand authorization
  - Check 原价 vs 特卖价 vs 超级VIP价
  - Verify desired size in stock
  ↓
Step 4: Cart Phase (⚠️ Requires login)
  "接下来需要登录你的唯品会账号才能加入购物车，
   请确认是否继续？"
  - If yes: proceed with browser automation
  - If no: provide manual instructions
  ↓
Step 5: Order Generation (Requires login)
  - Add to cart
  - Apply 优惠券, 超级VIP discounts
  - Select address
  - Calculate final price
  - Generate order preview
  ↓
Step 6: Handoff (User-controlled)
  "订单已准备好，请检查：
   [订单详情摘要]
   
   👉 请手动完成支付：
   1. 打开唯品会 App
   2. 进入购物车
   3. 点击结算
   4. 确认地址和优惠券
   5. 提交订单并支付"
```

### Browser Automation Rules

**Always announce before action:**
- "正在搜索..."
- "正在查看限时特卖..."
- "正在检查库存..."
- "正在加入购物车..."

**Snapshot key information:**
- Product title, brand, 原价, 特卖价, 超级VIP价
- Discount percentage
- Size/color availability
- Brand authorization badge
- Flash sale countdown
- Available coupons

**Stop conditions:**
- Before any payment screen
- When CAPTCHA appears (hand to user)
- When login is required (ask first)
- When desired size/color out of stock

### Login Handling

**Option A: User already logged in (Chrome profile)**
```
browser navigates to Vipshop
If user profile has active session → proceed
If session expired → prompt user to login manually first
```

**Option B: Manual mode (no login)**
```
Agent provides:
- Exact search keywords
- Flash sale timing tips
- Size availability check
- Step-by-step manual instructions
User executes manually
```

## Vipshop Flash Sales

### Sale Types

| Sale Type | Timing | Best For |
|-----------|--------|----------|
| **限时特卖** | Daily rotating | Branded goods at 50-80% off |
| **品牌特卖** | Brand-specific | Single brand deep discounts |
| **早场** | 10:00 AM | Fresh inventory |
| **晚场** | 8:00 PM | Additional drops |

### 超级VIP Benefits

- **Extra Discount**: Additional 5-10% off sale prices
- **Early Access**: 30-minute early access to sales
- **Free Shipping**: Unlimited free shipping
- **Birthday Gift**: Special birthday month offers
- **Price Protection**: 7-day price protection

**Break-Even Analysis:**
- Shop >¥200/month → membership pays for itself
- Frequent flash sale buyer → highly recommended

## Inventory Considerations

| Factor | Notes |
|--------|-------|
| Flash sale items | Limited stock, sell out fast |
| Size availability | Popular sizes sell out first |
| Color options | Limited vs full retail |
| Return policy | 7-day return, but check final sale items |

## Quality Bar

### Do:
- ✅ Focus on flash sales and brand discounts
- ✅ Check inventory before recommending
- ✅ Use browser automation for search/cart
- ✅ Add to cart and apply coupons (with consent)
- ✅ Generate order preview with all discounts
- ✅ Stay honest about not doing payment operations

### Do not:
- ❌ Pretend to log in (ask first)
- ❌ Recommend items with no stock
- ❌ Store user data persistently
- ❌ **Execute payment or final order submission**
- ❌ Guarantee inventory without checking

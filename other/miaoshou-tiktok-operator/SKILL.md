---
name: miaoshou-tiktok-operator
description: Operate a logged-in Miaoshou ERP workflow for TikTok Shop Malaysia product discovery, product screening, profit estimation, listing preparation, and reviewed publishing. Use when the user asks to search or select products in 妙手 ERP, evaluate low-price traffic products, prepare Malaysian TikTok Shop listings, move products into the TikTok collection box, or publish approved listings. Prefer browser operation through the user's existing login; never store credentials or call undocumented private endpoints.
---

# Miaoshou TikTok Operator

Use the user's logged-in Miaoshou ERP session to turn product candidates into reviewed TikTok Shop Malaysia listings. Treat product publishing as an external side effect: prepare first, show the exact listing and shop target, then obtain confirmation immediately before publishing.

## Skill Details

### Purpose

Help a cross-border ecommerce seller move from product discovery to a reviewed TikTok Shop listing without relying on source price alone. Combine market fit, product economics, supplier confidence, content potential, compliance risk, and publishing safety.

### Intended Users

Use this skill for:

- Early-stage TikTok Shop sellers who need more qualified products
- Sellers using Miaoshou ERP for collection, claiming, editing, or publishing
- Operators testing low-price traffic products without accepting hidden losses
- Non-technical users who want Codex to handle the operational breakdown
- Teams that require human review before any product becomes public

### Core Capabilities

- Search and collect visible candidate data from a logged-in Miaoshou ERP session
- Screen products for Malaysian weather, lifestyle, outdoor, travel, and daily-use contexts
- Estimate contribution profit after purchasing, shipping, fees, commission, discounts, packaging, returns, and ads
- Score products by market fit, short-video demonstration value, supplier quality, competition, economics, and risk
- Classify products as traffic, profit, bundle, or test products
- Prepare TikTok Shop titles, descriptions, categories, attributes, variants, prices, stock, and content angles
- Stage listings as drafts and publish only an explicitly approved product or batch
- Review post-listing performance and recommend whether to keep, revise, bundle, or stop a test

### Expected Inputs

Use the information already available in the user's message and logged-in pages. Useful inputs include:

- Target market and shop
- Product category or customer scenario
- Planned selling price
- Product, shipping, handling, and packaging costs
- Platform fee, affiliate commission, voucher, refund, and advertising assumptions
- Desired number of candidates or approved products

Do not block a read-only research task when some costs are missing. Use clearly labeled estimates and identify which numbers need later confirmation.

### Standard Outputs

Produce:

- A concise Chinese business summary
- A candidate or approved-product table
- Product role and recommendation
- Estimated total cost, contribution profit, and margin
- Market-fit, video potential, supplier, competition, and risk assessment
- Missing-information blockers
- Listing copy and short-video angle when requested
- A final pre-publish review for any external publishing action

### Success Criteria

Consider the task complete only when:

- The target market and shop are verified for publishing tasks
- Costs and assumptions are visible rather than hidden
- Loss-making and high-risk products are excluded or clearly held
- The selected assortment has a coherent customer or use-case theme
- Listing fields are checked for accuracy and unsupported claims
- Any approved publish action has a visibly verified result

## Required Tools

Use the Browser plugin for Miaoshou ERP and TikTok Shop pages. If the user explicitly asks to use Chrome because the login exists there, use the Chrome plugin instead.

Do not ask the user for source code, commands, cookies, passwords, SMS codes, or API tokens. Let the user complete login, CAPTCHA, OTP, or account authorization in the browser when required.

## Workflow

### 1. Confirm the Operating Context

Identify:

- Target market: default to Malaysia only when the current shop binding confirms Malaysia.
- Target shop: verify the actual connected TikTok Shop account before publishing.
- Product direction: default to lightweight outdoor, hot-weather, rain-season, sports, or practical daily-use products.
- Goal: traffic test, profit product, bundle, or catalog expansion.

If shop identity or country cannot be verified, stop before publishing. Continue with read-only product research and listing preparation.

### 2. Search Miaoshou ERP

Open the user's existing Miaoshou ERP session and use visible navigation and filters. Do not use reverse-engineered endpoints or scripts copied from browser network traffic.

For each candidate, collect what is visibly available:

- Source product URL or product ID
- Chinese product name
- Source price and currency
- Weight or estimated shipping weight
- Supplier sales or order signal
- Supplier rating, repeat purchase, or service signal
- Available stock and variants
- Main images and whether they contain Chinese text, watermarks, or other brands
- Category and any certification-sensitive features

Collect 10-30 candidates before recommending a shortlist. Do not publish while still researching.

### 3. Apply Safety Exclusions

Reject or hold for manual review:

- Branded, counterfeit, copyrighted, celebrity, character, or logo products without authorization
- Weapons, adult products, medical claims, supplements, cosmetics, food, batteries, electronics, children's safety products, or regulated protective equipment
- Products with unclear stock, unclear shipping route, copied images, unrealistic claims, or inconsistent variants
- Products whose expected contribution profit is zero or negative
- Clothing with complex sizing unless the user specifically approves the return risk

Read [references/product-rules.md](references/product-rules.md) for category and assortment guidance.

### 4. Calculate Profit and Score Candidates

Normalize costs into MYR. Include:

- Product cost
- China-side handling or purchasing cost
- International and local shipping paid by the seller
- Platform fee
- Payment or transaction fee
- Affiliate commission
- Voucher or seller discount
- Packaging
- Expected return/refund allowance
- Advertising allowance when relevant

Run:

```bash
python3 scripts/score_products.py --input candidates.csv --output scored-products.csv
```

Read [references/candidate-schema.md](references/candidate-schema.md) before creating the CSV. Treat all defaults as estimates and label them clearly.

Prefer candidates that meet all of these:

- Contribution margin at least 20%
- Contribution profit at least RM4 for traffic products
- Contribution profit at least RM8 for core profit products
- Lightweight and simple to fulfill
- Easy to demonstrate in a 10-30 second video
- Clear Malaysian use case
- Low compliance and return risk

Do not recommend a product solely because its source price is low.

### 5. Build a Reviewed Shortlist

Present 5-10 shortlisted products in simple Chinese:

| Product | Role | Sale price | Estimated profit | Margin | Risk | Recommendation |
|---|---|---:|---:|---:|---|---|

Label each product as:

- `引流款`: low entry price but still non-negative after all costs
- `利润款`: healthy contribution profit
- `组合款`: raises order value through a useful bundle
- `测试款`: uncertain demand, list in small quantity and observe

Recommend a coherent assortment rather than unrelated catalog stuffing.

### 6. Prepare the Listing

For approved candidates, prepare:

- English title suitable for Malaysia; add Malay keywords only when natural and verified
- Honest description without unsupported claims
- Correct category and required attributes
- Variant names, size information, and stock
- MYR price with cost buffer
- Shipping weight and package dimensions
- Main image review and localization notes
- Short-video demonstration angle
- Affiliate commission recommendation

Never invent certifications, materials, dimensions, stock, delivery time, or supplier claims. Mark missing fields as blockers.

### 7. Stage in Miaoshou

Use the visible Miaoshou workflow to collect or claim the approved source product into the TikTok product area. Apply the prepared title, description, category, attributes, variants, price, stock, weight, and images.

After editing, re-read the page and verify:

- Correct Malaysia shop
- Correct product and variants
- Price and stock
- Weight and dimensions
- Category and required attributes
- No Chinese text, supplier contact details, watermarks, or unauthorized branding

Save as a draft when the interface supports it.

### 8. Confirm and Publish

Immediately before any action that makes the listing visible or sends it for platform review, show:

- Shop name and country
- Product title
- Price
- Stock
- Number of variants
- Expected unit profit and margin
- Any remaining uncertainty

Ask for explicit confirmation for that exact product or clearly enumerated batch. After confirmation, publish only the approved items.

Do not enable bulk auto-publishing by default. Limit an initial test batch to 5 products unless the user explicitly approves more.

### 9. Verify the Result

Verify the visible success message or listing state. Record:

- Miaoshou product ID
- TikTok Shop product ID when available
- Shop
- Publish time
- Review status
- Price and stock
- Any warning or rejected field

Report failures plainly and leave the product in draft when possible.

## Operating Modes

- `调研模式`: Read-only search, comparison, and shortlist.
- `准备模式`: Generate listing data and save drafts; no publishing.
- `发布模式`: Publish only after exact action-time confirmation.
- `复盘模式`: Read product views, clicks, orders, and margin; recommend keep, revise, bundle, or remove.

Default to `调研模式` when the user's instruction is ambiguous.

## Example Requests

- `使用 $miaoshou-tiktok-operator，在妙手 ERP 里找20款适合马来西亚雨季和户外场景的商品，只做筛选和利润计算。`
- `使用 $miaoshou-tiktok-operator，把批准的商品整理成 TikTok Shop Malaysia 草稿，不要发布。`
- `使用 $miaoshou-tiktok-operator，检查这批低价袜子扣除物流和达人佣金后是否值得做引流款。`
- `使用 $miaoshou-tiktok-operator，复盘现有商品的浏览、点击和订单表现。`

## Limitations

- Treat fee, shipping, return, and advertising defaults as estimates until the user verifies them.
- Expect Miaoshou ERP and TikTok Shop interfaces, categories, fees, and rules to change.
- Do not provide legal, tax, trademark, or platform-compliance guarantees.
- Do not promise sales, traffic, ad eligibility, or profit from adding products.
- Use browser-visible workflows rather than assuming API access exists.

## Non-Negotiable Rules

- Never place credentials, cookies, tokens, phone numbers, shop IDs, or passwords in files or code.
- Never bypass CAPTCHA, OTP, account authorization, or platform review.
- Never rely on undocumented private APIs for production publishing.
- Never publish to a shop whose identity and country have not been visibly verified.
- Never hide estimated assumptions inside profit calculations.
- Never treat a successful click as completion; verify the resulting listing state.

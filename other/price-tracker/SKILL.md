---
name: price-tracker
description: "Track product prices across multiple platforms and get alerts when prices drop. Supports Amazon, eBay, JD.com, Taobao and more."
triggers:
  - "price tracker"
  - "价格追踪"
  - "price alert"
  - "track price"
---

# Price Tracker

Track product prices across multiple platforms.

## Supported Platforms

| Platform | Country | Status |
|----------|---------|--------|
| Amazon | Global | ✅ |
| eBay | Global | ✅ |
| JD.com | China | ✅ |
| Taobao | China | ✅ |
| Pinduoduo | China | ✅ |
| Shopify | Global | ✅ |

## Features

- 💰 **Price Monitoring** — Track any product URL
- 📉 **Price Drop Alert** — Notify when price drops
- 📊 **Price History** — View historical prices
- 📈 **Price Compare** — Compare across platforms
- 🔔 **Multi-channel Alert** — Telegram/Email/Discord

## Usage

### Add Product

```bash
# Add by URL
hermes price add "https://amazon.com/dp/B08XXXXX"

# With price threshold
hermes price add "https://amazon.com/dp/B08XXXXX" \
  --alert-below 99.99 \
  --name "Product Name"
```

### View Prices

```bash
# List tracked products
hermes price list

# Price history
hermes price history --product "Product Name"

# Compare prices
hermes price compare "Product Name"
```

### Alert Configuration

```yaml
# price-tracker.yml
alerts:
  telegram:
    enabled: true
    chat_id: ${TELEGRAM_CHAT_ID}
    
  email:
    enabled: true
    to: user@example.com
    
thresholds:
  alert_on_drop: true
  drop_percentage: 10
```

## Pitfalls

1. **Anti-bot** — Some sites block scrapers
2. **Price Changes** — Currency/fluctuation affects accuracy
3. **Availability** — Product may go out of stock
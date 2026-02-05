---
name: track-and-field
description: Track & Field affiliate tracking context
---

# Track & Field Domain Context

## What Is Track & Field?

Track & Field handles **affiliate tracking and attribution** for the Violet platform. It tracks where orders come from and attributes revenue to the right sources.

## Core Capabilities

### Affiliate Tracking
- Click tracking with unique identifiers
- Cookie-based attribution
- Cross-device tracking
- Attribution window management

### Commission Calculation
- Tiered commission structures
- Per-merchant commission rates
- Channel-specific rates
- Promotional overrides

### Attribution Models
- First-click attribution
- Last-click attribution
- Multi-touch attribution
- Time-decay models

## Key Concepts

### Tracking Parameters
- `violet_affiliate_id` - Identifies the affiliate
- `violet_click_id` - Unique click identifier
- `violet_campaign` - Campaign grouping
- `violet_source` - Traffic source

### Attribution Windows
- Standard: 30 days
- Short: 7 days
- Extended: 90 days
- Custom per merchant

## Data Model

| Entity | Purpose |
|--------|---------|
| Clicks | Track initial referrals |
| Attributions | Link orders to referrers |
| Commissions | Calculated payouts |
| Affiliates | Partner accounts |

## Integration Points

- **Prism**: Order creation triggers attribution lookup
- **Beam**: Destination order attribution
- **Billing**: Commission payout processing
- **Channels**: Affiliate program management

## Key Metrics

| Metric | Purpose |
|--------|---------|
| Click-through Rate | Effectiveness of affiliate links |
| Conversion Rate | Clicks to orders |
| Commission Rate | Average commission percentage |
| Attribution Rate | Orders with valid attribution |

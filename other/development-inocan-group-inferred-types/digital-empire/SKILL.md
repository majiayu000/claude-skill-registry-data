---
name: digital-empire
description: Manage digital product sales across Gumroad, Etsy, Shopify. Handle sales tracking, product delivery, and social media automation.
allowed-tools: Read, Edit, Write, WebFetch, Bash
---

# Digital Empire Skill

## Sales Platforms
| Platform | Status | Token |
|----------|--------|-------|
| Gumroad | Active | GUMROAD_ACCESS_TOKEN |
| Etsy | Planned | - |
| Shopify | Planned | - |
| Ko-fi | Planned | - |

## Automation Flow

```
Customer Purchase
       ↓
Platform Webhook → Webhook Router
       ↓
Master Zap 3 (Sale Hub)
       ↓
├── Log to Google Sheets
├── Celebrate in Home Assistant (green lights + cha-ching)
├── SMS notification to Joshua
├── Email product files to customer
├── (7 day delay)
└── Email review request
```

## Social Media Automation
- Buffer for scheduling
- Platforms: Pinterest, Twitter, Facebook, Instagram, LinkedIn
- Content types: Product launches, tips, testimonials

## Metrics Tracked
| Metric | Location |
|--------|----------|
| Daily sales count | Google Sheets |
| Revenue by platform | Google Sheets |
| Product performance | Google Sheets |
| Customer emails | Google Sheets |

## Product Categories
Located in ~/repos/phoenix-forge-ecosystem/3_DigitalEmpire/

## Sales Celebration
When sale received:
1. Green flash on all lights
2. Cash register sound effect
3. TTS: "New sale! $X from [platform]!"
4. SMS to Joshua

## Key Files
- ~/repos/phoenix-forge-ecosystem/3_DigitalEmpire/
- ~/repos/phoenix-forge-ecosystem/ZAPIER_100_AUTOMATIONS.md (Master Zap 3)

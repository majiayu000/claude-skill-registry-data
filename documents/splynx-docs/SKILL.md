---
name: splynx-docs
description: |
  Access Splynx documentation from wiki.splynx.com using Crawl4AI MCP.
  Provides navigation guide, URL patterns, and web scraping for JS-rendered pages.
---

# Splynx Documentation

Access Splynx wiki documentation at wiki.splynx.com. The wiki is JavaScript-rendered, so use **Crawl4AI MCP tools** to fetch content.

## Quick Reference URLs

| Topic | URL |
|-------|-----|
| Customer Billing | `https://wiki.splynx.com/customer_management/customer_billing` |
| Customer Services | `https://wiki.splynx.com/customer_management/customer_services` |
| Invoices | `https://wiki.splynx.com/finance/invoices` |
| Transactions | `https://wiki.splynx.com/finance/transactions` |
| Finance Settings | `https://wiki.splynx.com/configuration/finance/finance_settings` |
| RADIUS Config | `https://wiki.splynx.com/configuration/network/radius` |
| Routers | `https://wiki.splynx.com/networking/routers` |
| API Documentation | `https://wiki.splynx.com/administration/information/api_documentation` |
| Tariff Plans | `https://wiki.splynx.com/configuring_tariff_plans/internet_tariff_plans` |
| One-Time Plans | `https://wiki.splynx.com/configuring_tariff_plans/one_time_plans` |
| CRM Leads | `https://wiki.splynx.com/crm/leads` |
| Dashboard | `https://wiki.splynx.com/dashboard` |
| Additional Fields | `https://wiki.splynx.com/configuration/system/additional_fields` |

## Using Crawl4AI MCP

The Crawl4AI MCP server provides tools for scraping JavaScript-rendered pages.

### Scrape a Single Page

```
Use the crawl4ai scrape_webpage tool:
- url: "https://wiki.splynx.com/customer_management/customer_billing"
```

Returns page content as markdown.

### Crawl Multiple Pages

```
Use the crawl4ai crawl_website tool:
- start_url: "https://wiki.splynx.com/networking"
- crawl_depth: 2
- max_pages: 20
```

Crawls from start URL, following links to specified depth.

### Search for Documentation

Use WebSearch to find relevant wiki pages:
```
WebSearch: site:wiki.splynx.com <your topic>
```

Then scrape the specific URLs returned.

## Wiki Structure

### URL Patterns by Section

| Section | URL Pattern | Content |
|---------|-------------|---------|
| Customer Management | `/customer_management/*` | Customer profiles, billing, services, CPE |
| Finance | `/finance/*` | Invoices, payments, transactions, billing engine |
| Networking | `/networking/*` | Routers, GPON, Huawei, MikroTik |
| Network Management | `/network-management/*` | Customer authentication, router settings |
| Configuration | `/configuration/*` | System settings by module |
| Tariff Plans | `/configuring_tariff_plans/*` | Internet, voice, custom, one-time plans |
| CRM | `/crm/*` | Leads, pipelines, quotes |
| Administration | `/administration/*` | Admin settings, API, logs, permissions |
| Customer Portal | `/customer_portal/*` | Portal configuration, self-service |
| Add-ons | `/addons_modules/*` | Third-party integrations |

### Key Subsections

**Customer Management:**
- `customer_information` - Profile, contacts, addresses
- `customer_billing` - Payment settings, invoicing
- `customer_services` - Service assignments
- `cpe_management` - Customer equipment

**Networking:**
- `routers` - Router configuration
- `huawei/*` - Huawei GPON/BRAS setup
- `mikrotik/*` - MikroTik integration

**Network Management:**
- `authentication_of_customers/*` - PPPoE, DHCP, Hotspot with RADIUS
- `routers_settings/*` - Per-vendor router configs

**Configuration:**
- `network/radius` - RADIUS server settings
- `finance/finance_settings` - Billing periods, blocking
- `main_configuration/preferences` - System preferences
- `system/additional_fields` - Custom fields

## External API Documentation

For REST API endpoint details:

| Resource | URL |
|----------|-----|
| API Reference | https://splynx.docs.apiary.io |
| PHP API Module | https://bitbucket.org/splynx/splynx-php-api |

The API docs at Apiary cover all REST endpoints with request/response examples.

## Common Lookup Patterns

**Billing questions:**
1. Search: `site:wiki.splynx.com billing configuration`
2. Scrape: `/configuration/finance/finance_settings`
3. Scrape: `/customer_management/customer_billing`

**RADIUS/Authentication:**
1. Search: `site:wiki.splynx.com radius pppoe`
2. Scrape: `/configuration/network/radius`
3. Scrape: `/network-management/authentication_of_customers/mikrotik_pppoe_radius`

**Customer services:**
1. Scrape: `/customer_management/customer_services`
2. Scrape: `/configuring_tariff_plans/internet_tariff_plans`

**API integration:**
1. Scrape: `/administration/information/api_documentation`
2. Visit: https://splynx.docs.apiary.io

## Troubleshooting

**Crawl4AI not responding:**
- Ensure Docker container is running: `docker ps | grep crawl4ai`
- Restart if needed: `docker restart crawl4ai`
- Health check: `curl http://localhost:11235/health`

**Wiki pages return empty content:**
The wiki.splynx.com uses Vue.js SPA which can be challenging to scrape.
Alternative approaches:
1. **Use WebSearch** - Google indexes the wiki content well:
   ```
   WebSearch: site:wiki.splynx.com <your topic>
   ```
2. **Direct API curl** with longer wait times:
   ```bash
   curl -X POST http://localhost:11235/crawl \
     -H "Content-Type: application/json" \
     -d '{"urls": ["<wiki_url>"], "delay_before_return_html": 15}'
   ```
3. **Check Apiary API docs** for REST endpoint details (static site, scrapes well)

**Need full section content:**
- Use `crawl_website` with appropriate depth/max_pages
- For entire wiki, consider crawling from homepage with higher limits

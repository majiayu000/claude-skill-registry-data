---
name: shopify-order-management
description: 一站式 Shopify 订单运营自动化系统，覆盖从接单、履约同步、低库存预警、弃购挽回到每日销售报表的全链路管理，解决店铺后台操作分散、提醒滞后和报表缺失等问题。
tags:
- shopify
- ecommerce
- orders
- inventory
- abandoned-cart
- sales
- automation
- n8n
author: mhmalvi
version: 1.0.0
license: CC BY-NC-SA 4.0
metadata:
  clawdbot:
    emoji: 🛒
    requires:
      n8nCredentials:
      - google-sheets-oauth2
      - smtp
      env:
      - SHOPIFY_STORE_URL
      - SHOPIFY_ACCESS_TOKEN
      - SHOPIFY_WEBHOOK_SECRET
      - SHOPIFY_ADMIN_EMAIL
      - LOW_STOCK_THRESHOLD
    os:
    - linux
    - darwin
    - win32
title: Shopify订单管理
example: 实时同步 Shopify 店铺中的新订单，若商品库存低于5件则自动向指定邮箱发送警报。
---
# Shopify Order Management

Complete Shopify order lifecycle management built on n8n. Handles new orders, status sync, inventory alerts, abandoned cart recovery, and daily sales reporting.

## Problem

Shopify's built-in tools are limited for operations management. Order status changes aren't logged centrally, low-stock alerts arrive too late, abandoned cart emails are basic, and daily sales data requires logging into the admin dashboard.

This system automates the full order lifecycle with real-time tracking and proactive alerts.

## What It Does

1. **New Order Handling** — Webhook captures new orders, logs to Google Sheets, emails admin
2. **Order Status Sync** — Periodically syncs fulfillment/payment status from Shopify to Sheets
3. **Low Stock Alerts** — Checks inventory every 6 hours, alerts on items below threshold
4. **Abandoned Cart Recovery** — Sends recovery emails to customers who abandoned checkout
5. **Daily Sales Reports** — Revenue, order count, AOV, fulfillment stats, and top products

## Included Workflows

| # | File | Purpose |
|---|------|---------|
| 01 | `01-new-order-handler.json` | Webhook → parse order → log to Sheets → notify admin |
| 02 | `02-order-status-sync.json` | Scheduled → check pending orders → sync from Shopify API |
| 03 | `03-low-stock-alert.json` | Scheduled → inventory check → alert on low stock |
| 04 | `04-abandoned-cart-recovery.json` | Scheduled → fetch abandoned carts → recovery email |
| 05 | `05-daily-sales-report.json` | Daily → fetch orders → metrics → report email |

## Architecture

```
Shopify Webhook (orders/create)
    |
    v
Workflow 01: New Order Handler
    +-> Parse order data
    +-> Log to Google Sheets (Orders tab)
    +-> Email notification to admin

Scheduled (every 2 hours):
    |
    v
Workflow 02: Order Status Sync
    +-> Read unfulfilled orders from Sheets
    +-> Fetch current status from Shopify API
    +-> Update Sheets with latest status

Scheduled (every 6 hours):
    |
    v
Workflow 03: Low Stock Alert
    +-> Fetch all products from Shopify
    +-> Check inventory vs threshold
    +-> IF low stock -> email alert

Scheduled (every 3 hours):
    |
    v
Workflow 04: Abandoned Cart Recovery
    +-> Fetch open checkouts from Shopify
    +-> Filter: abandoned 1-24 hours ago
    +-> Send recovery email with cart link

Daily:
    |
    v
Workflow 05: Daily Sales Report
    +-> Fetch last 24h orders
    +-> Calculate revenue, AOV, fulfillment stats
    +-> Top products by quantity
    +-> Email formatted report
```

## Required n8n Credentials

| Credential Type | Used For | Placeholder in JSON |
|----------------|----------|---------------------|
| Google Sheets OAuth2 | Order tracking and logging | `YOUR_GOOGLE_SHEETS_CREDENTIAL_ID` |
| SMTP | Notifications, recovery emails, reports | `YOUR_SMTP_CREDENTIAL_ID` |

## Environment Variables

```bash
# Shopify (required)
SHOPIFY_STORE_URL=https://your-store.myshopify.com
SHOPIFY_ACCESS_TOKEN=shpat_xxxxxxxxxxxxx
SHOPIFY_WEBHOOK_SECRET=your-webhook-secret

# Google Sheets
SHOPIFY_ORDERS_SHEET_ID=your-sheet-id

# Alerts
SHOPIFY_ADMIN_EMAIL=admin@yourstore.com
LOW_STOCK_THRESHOLD=5
```

## Configuration Placeholders

| Placeholder | Description |
|-------------|-------------|
| `YOUR_SHOPIFY_ORDERS_SHEET_ID` | Google Sheet ID for order tracking |
| `YOUR_GOOGLE_SHEETS_CREDENTIAL_ID` | n8n Google Sheets credential ID |
| `YOUR_SMTP_CREDENTIAL_ID` | n8n SMTP credential ID |
| `YOUR_NOTIFICATION_EMAIL` | Admin email for reports and alerts |

## Google Sheets Schema (Orders)

| Column | Type | Description |
|--------|------|-------------|
| order_id | text | Shopify order ID (primary key) |
| order_number | text | Human-readable order number |
| customer_name | text | Customer full name |
| customer_email | text | Customer email |
| customer_phone | text | Customer phone |
| total_price | number | Order total |
| currency | text | Currency code (USD, EUR, etc.) |
| financial_status | text | pending / paid / refunded |
| fulfillment_status | text | unfulfilled / fulfilled / delivered |
| items_count | number | Number of line items |
| items_summary | text | Item names and quantities |
| shipping_address | text | Shipping address summary |
| created_at | datetime | Order creation timestamp |
| synced_at | datetime | Last sync timestamp |

## Quick Start

### 1. Prerequisites
- n8n v2.4+ (self-hosted)
- Shopify store with Admin API access (custom app)
- Google Sheets OAuth2 credentials
- SMTP email credentials

### 2. Create Shopify Custom App
Go to `https://admin.shopify.com/store/{slug}/settings/apps/development` → Create an app → Grant scopes: `read_orders`, `read_products`, `read_checkouts`.

### 3. Create Orders Sheet
Create a Google Sheet with the columns above. Name the tab "Orders".

### 4. Configure Shopify Webhook
In Shopify Admin > Settings > Notifications > Webhooks, add `orders/create` pointing to your n8n webhook URL.

### 5. Import & Configure
Import all 5 JSON files into n8n. Replace `YOUR_*` placeholders and set environment variables.

## Use Cases

1. **DTC brands** — Order tracking, inventory alerts, and automated cart recovery
2. **Print-on-demand** — Monitor fulfillment status across products
3. **Dropshippers** — Track orders and low-stock from suppliers
4. **Subscription boxes** — Daily sales and fulfillment monitoring
5. **Agency operators** — Multi-store management with centralized reporting

## Requirements

- n8n v2.4+ (self-hosted recommended)
- Shopify store with Admin API custom app
- Google Sheets OAuth2 credentials
- SMTP email credentials

---
name: medusa-store
description: "Reference for the Medusa.js store backend, its Next.js storefront, and the Claude-powered AI store agent. Use this whenever working on the store backend/frontends — product catalog, checkout, digital products, the storefront chat widget, or any of the AI agent's store-management tools (create_product, list_orders, etc.)."
---

# Medusa Store + AI Agent — Reference

## Stack

- **Backend:** Medusa.js (store/backend), started from `medusajs/medusa-starter-default`
- **Storefront:** the official Medusa Next.js storefront template (store/storefront), customized
- **Products:** both physical and digital (digital products plugin enabled — used to sell the dubbing service itself as a product)
- **Database:** Dedicated PostgreSQL database (separate from Supabase; manages products, orders, customers, regions, etc.)

## AI Store Assistant (customer-facing chat widget)

A floating chat widget on the storefront. On every message:
1. Frontend sends `{ message, conversationId }` to `AI_GATEWAY_URL/ai/chat` with `context: "store-chat"`
2. The AI Gateway attaches the product catalog + FAQ + store policies (in Arabic) as system context
3. Response streams back to the widget

The widget NEVER calls Claude directly — always through the gateway (see `ai-gateway` skill). The widget also never holds any API key.

## AI Store Management Agent (admin-facing, "AI does everything")

This is the agent the store owner talks to in Arabic to run the store. It uses Claude tool-calling. Each tool below is a function that calls the Medusa Admin API. The AI Gateway holds these tool definitions under `context: "store-admin"`.

| Tool | Medusa Admin API call | Notes |
|---|---|---|
| `create_product` | `POST /admin/products` | Takes title, price, description, images. If description is missing, the agent writes one in Arabic itself before calling this. |
| `list_orders` | `GET /admin/orders` | Supports filters: status, date range |
| `update_inventory` | `POST /admin/inventory-items/:id/location-levels/:location_id` | Adjusts stock quantity for a variant |
| `create_discount` | `POST /admin/discounts` | Generates a coupon code, % or fixed amount |
| `get_sales_report` | `GET /admin/orders` + aggregation | Revenue, top products, conversion — computed from order data |
| `write_description` | (no API call — pure generation) | Generates Arabic product description + SEO title + tags; output is then passed to `create_product` or `update_product` |
| `answer_customer` | reads from `/admin/orders`, `/admin/customers` | Looks up a customer's order by email/order number, drafts a reply |
| `process_refund` | `POST /admin/orders/:id/refund` | Always confirm the amount and order ID with the user before calling — refunds are irreversible |

### Adding a new tool

1. Define the JSON schema (name, description, input_schema) in the AI Gateway's tool registry for `context: "store-admin"`
2. Implement the handler function that calls the relevant Medusa Admin API endpoint
3. Add a row to the table above
4. Irreversible actions (refunds, deleting products) must require the agent to restate the action and get explicit confirmation before calling the tool

## Security Notes (also see `security-engineering` skill — especially Section 4 on customer/admin tool separation, critical for the admin agent's tools above)

- The Medusa Admin API key lives ONLY in the AI Gateway's `.env` — never in the storefront, never in the chat widget's frontend code
- All admin-tool calls happen server-side (AI Gateway → Medusa Admin API), the admin chat UI just sends/receives messages
- Rate limit the storefront chat widget endpoint — without it, anyone can spam it and burn Claude API credits

## Selling Dubbing as a Product

The dubbing service itself is listed as a digital product in Medusa. When a customer buys it, the order triggers a webhook to `DUBBING_URL/api/dub` to create a dubbing job tied to that order ID — this is the one place the Store service calls Dubbing directly (via HTTP, per the architecture rule).


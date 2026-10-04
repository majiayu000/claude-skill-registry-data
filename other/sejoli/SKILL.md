---
name: sejoli
description: "Use when working with Sejoli membership/affiliate plugin."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [sejoli, wordpress, membership, affiliate, commission, smart-millionaire]
    related_skills: [novamira-mcp-troubleshooting]
---

# Sejoli (Membership & Affiliate plugin)

Sejoli powers membership + affiliate commissions on the Smart Millionaire WordPress site (`member.smartmillionaire.co.id`). Load this when the task touches Sejoli products, orders, member groups, commissions, or member access. For the tooling quirks of driving WordPress through Novamira (sandbox, heredoc quoting, editing plugin PHP via SSH), see `novamira-mcp-troubleshooting`.

## When to Use

- "How many orders/sales today?" or any order-count question.
- "What's the commission for [member group] on [product]?"
- "Find product X / give me the link."
- Member-access checks ("does user X have LUNAS access to product Y?").

## Data model

- **Products** = CPT `sejoli-product`. Permalink `/product/<slug>/`. Get URL with `get_permalink($id)`, price with `get_post_meta($id,'_price',true)`, affiliate-on flag with `get_post_meta($id,'_sejoli_enable_affiliate',true)`.
- **Member tiers** = CPT `sejoli-user-group`. On this site: Free Member (3747), PLATINUM Member (433), SILVER Member (1812), GOLD Member (510).
- **Orders are NOT a post type.** They live in a custom Sejoli table — query via `sejolisa_get_orders()`, never `get_posts(['post_type'=>…order…])` (returns nothing; WooCommerce is inactive, `shop_order` is empty). Direct DB access is `{$wpdb->prefix}sejolisa_orders` — the prefix on this site is `wplo_`, NOT `wp_`, so a hardcoded `wp_sejolisa_orders` in `wp db query` fails with `table doesn't exist`; use `$wpdb->prefix` (or `wp eval` it) instead.

## Querying from Novamira execute-php

`$wpdb` is unavailable in the sandbox, and any `$var` or `=` must survive a **quoted** heredoc (`<<'EOF'`). Prefer direct function calls with literal args, then `echo json_encode(...)`:

```php
echo json_encode(get_posts(['post_type'=>'sejoli-product','s'=>'air','posts_per_page'=>20,'post_status'=>'publish']));
```

Use `get_post_meta($id,'key',true)` for scalars (price, commission) and `get_posts`/`get_page_by_path`/`get_the_title`/`get_post_field` for posts. Avoid `array_map`/closures — an unquoted heredoc strips `$f` to empty and you get `expects at least 1 argument`.

## Key functions (from Sejoli core)

- `sejolisa_get_user_access_products($user_id)` — products a member has LUNAS access to. Use this for access checks; do NOT use `sejolisa_does_user_have_access()`, which calls `display_block_access()` → `wp_die()` → blank page when access is missing.
- `sejolisa_get_orders(['user_id'=>..,'product_id'=>..])` — returns `['valid'=>bool,'orders'=>[...]]`; `status==='completed'` = LUNAS.
- `sejolisa_carbon_get_post_meta($post_id, 'field')` — reads Carbon Fields complex meta (the canonical reader for commission fields).
- Affiliate identity from an order: `sejolisa_get_order(['ID'=>$id])['orders']` carries `affiliate_id` + `affiliate_name` (display name, joined) + `product_id` + `status`. Affiliate phone is user meta — try keys `phone`, `user_phone`, `billing_phone`, `handphone`, `no_hp`, `whatsapp` in order; for wa.me links normalize by stripping non-digits and mapping `0…`→`62…`, `8…`→`628…`.

## Commission model

Commissions are Carbon Fields "complex" (repeatable) fields, set at two levels and often empty at the product level (meaning: fall back to the group default). Full structure, example values, and the raw meta-key format: `references/commission-model.md`.

**Sejoli is not the only engine paying on these orders.** This site also runs a custom MLM engine ('smart-binary' — see the `smart-binary-mlm` skill) that hooks `sejoli/order/set-status/completed` and pays its OWN commissions on the same orders, and that integration auto-approves Sejoli's own affiliate records (`status` 'pending'→'added' in `{prefix}sejolisa_affiliates`). One sale can therefore pay BOTH Sejoli's native affiliate commission AND the MLM stack — sum both before answering "what does this sale pay".

## Confirm / thankyou page + custom HTML

- `/confirm/?order_id=<id>` is a Sejoli **template**, not a WP page — `get_page_by_path('confirm')` returns null. It's rendered by `SejoliSA\Front\Confirm::display_confirm_page()` → `template/checkout/confirm.php`, and is the bank-transfer payment-confirmation form.
- Per-product "Notifikasi" content (`product_notification_on_hold` / `payment_confirm` / `in_progress` / `completed` / `cancel` / `refund`, the "Notifikasi" tab) renders ONLY into email/WhatsApp templates via the `{{product-info}}` shortcode — it never appears on the web confirm/thankyou page. Its shortcodes include `{{affiliate-name}}`, `{{affiliate-phone}}`, `{{affiliate-email}}`, `{{commission}}`, `{{confirm-url}}`.
- Sejoli Panel's "Product Extras" meta box (`_sjp_post_confirm_redirect` + `_sjp_notif_*`) is redirect + email/WA only, and its template vars are buyer-only (`{nama}` `{email}` `{phone}` `{produk}` `{total}` `{status}`) — no affiliate vars, so it can't drive an affiliate WhatsApp button.
- There is **no stock field that renders custom HTML on the web `/confirm/` page**. For the owner's post-purchase OTO (upsell) page, a custom mu-plugin `sm-confirm-oto.php` was built: a GLOBAL setting — Settings → "OTO Halaman Konfirmasi", option `sm_confirm_oto_html` — one OTO HTML for ALL orders, not per-product. Shortcodes: `{{affiliate-name}}` `{{affiliate-phone}}` `{{affiliate-email}}` `{{buyer-name}}` `{{order-id}}` `{{product-name}}` `{{sitename}}` `{{siteurl}}` (`{{affiliate-phone}}` normalized to 62xxx for wa.me). An earlier per-product meta-box version (`sm-confirm-custom-html.php`, meta `_sm_confirm_custom_html`) was replaced — the owner explicitly wanted ONE OTO for every order regardless of product.
- **Placement (owner-corrected, final): a LARGE full-width section below the confirm form, revealed only AFTER the buyer submits the confirmation form.** Not injected into the small `.sejoli-complete-confirm` box. Reveal by echoing a `display:none` wrapper + an inline script that un-hides it when `.sejoli-complete-confirm` becomes visible (poll `classList.contains('hide')` + `offsetParent`, plus a MutationObserver), with a fallback to show immediately if the box is absent.
- **Scripts do NOT execute when injected via `innerHTML`.** OTO HTML that carries `<script>` (countdown timer, Tailwind CDN) must be echoed DIRECTLY in the page inside a hidden wrapper — never `el.innerHTML = html` — because innerHTML-injected `<script>` is inert. Direct echo also starts any countdown on page load, before the section is revealed.
- The OTO's own `<style>body{...}</style>` leaks to the whole confirm page (it's a section inside the page, not a standalone page); the owner must strip `body{...}` from their OTO CSS.
- Orphaned meta keys like `_sslm_*` (`content_shortcode_on_thankyou`, `redirect_on_thankyou`, `access_on_thankyou`) mean a "thankyou-customization" plugin was removed — values survive in the DB but nothing renders them.

## Pitfalls

- Product-level `_sejoli_commission` is empty on most products — don't conclude "no commission" without also checking the buyer's group (`_group_commissions` global tiers + `_group_setup_per_product` overrides).
- Commission `type` is `fixed` (Nilai Tetap) or `percentage` (Persentase); a bare number without the type is ambiguous (e.g. `40` = 40%, not Rp 40).
- Member access has no admin bypass in Sejoli's raw access API — an administrator is still "no access" to a paid product unless they own it (relevant when the owner sees the locked form on their own campaign).

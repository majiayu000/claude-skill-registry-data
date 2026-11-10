---
name: shop-pack
zh_name: "网店素材包"
en_name: "Shop Pack"
emoji: "🛍️"
description: "Everything a small online shop needs from one product list and the seller's own photos: square product images, a store banner and collection header, a care or thank-you card for the parcel, and a launch post, all in one style and filled per product."
zh_description: "用一份商品清单和卖家自己的照片, 做出网店所需的全部素材: 方形商品图、店铺横幅和分类头图、随包裹的保养卡或感谢卡、上新帖子, 风格统一, 每件商品自动填充"
en_description: "Everything a small online shop needs from one product list and the seller's own photos: square product images, a store banner and collection header, a care or thank-you card for the parcel, and a launch post, all in one style and filled per product."
category: card
scenario: marketing
aspect_hint: "2048×2048 product images, 1920×800 banner"
tags: ["shop", "shopify", "big cartel", "etsy", "product images", "ecommerce", "store", "jewelry", "网店", "商品图"]
triggers:
  - "shopify"
  - "online shop"
  - "online store"
  - "product images"
  - "product photos"
  - "big cartel"
  - "etsy"
  - "store banner"
  - "网店"
od:
  mode: prototype
  craft:
    requires:
      - typography
      - color
      - anti-ai-slop
  surface: web
  platform: desktop
  scenario: marketing
  preview:
    type: html
    entry: index.html
  design_system:
    requires: false
  example_prompt: "I sell handmade silver jewelry on Shopify. Here's my product list and a folder of photos. Make my product images, a store banner and a care card to put in each parcel, all in my style."
---

# Shop Pack

**Intent.** A seller has products, photos and a shop. They want the shop to look like one brand without designing thirty images by hand. Each piece is **one design with fields**, exported once per product from their list, so a new product or a price change is a re-export, not a redesign.

## 1. Start from what they have

Ask once, in plain words, for what they already have:

- **Their style.** A brand document, logo, website or a few images they like. If they give one, make it their style first: read it with `read_open_design_source`, then `extract_open_design_design_system` (or `create_open_design_design_system` from what they describe), and use it for every piece. With nothing, offer two or three directions in one message and go with their pick.
- **The product list.** A CSV or spreadsheet, one row per product. Without one, offer to write `products.csv` with them from what they tell you.
- **Their photos.** A folder of product photos. This recipe frames their real photos; **it never generates product photos**, because a buyer must see the real piece.
- **Where they sell**: Shopify, Big Cartel, Etsy or another site. It changes nothing in the designs, but tells you which hand-off to offer at the end.

## 2. Map the columns, once

Read the list's header row and propose which column fills which field (`title`, `price`, `material`, `photo`, `collection`…). Show the mapping in one short list and wait for an OK before designing.

- **Private columns are never shown.** Never bind a column whose header names a cost, margin, supplier, wholesale price, stock or internal note to any field. Say once that those stay off every design.
- **Ask about columns you can't place.** List them in one question ("Should `batch` appear on anything?") rather than guessing.
- **Photos.** A photo column holds workspace-relative paths. If there's none, ask them to put each product's photo in `photos/` named after the product, and fill the column yourself. With no photos yet, lay the designs out with a marked photo slot and ask for the photos; don't invent any.

## 3. The pieces

Make the pieces they want, each as its own artifact in one collection, all in their style:

| Piece | Format | Filled per product |
|---|---|---|
| Product image | `shop-product` (2048×2048) | yes: photo, title, optional price |
| Store banner | `shop-banner` (1920×800) | no |
| Collection header | `shop-collection` (1920×600) | per collection, if the list has one |
| Care or thank-you card for the parcel | `a6`, `business-card` or `postcard-4x6` (print) | optional: product name, care text |
| Launch post | `ig-portrait` or `ig-square` | yes, for new products |

Pass the format to `prepare_open_design_brief` and to `register_open_design_artifact`.

**Product image craft.** The photo is the hero: crop it to cover (`object-fit: cover`) over a calm background from their style, with even padding and at most a short label. Every product image uses the same crop, background and label position, so the grid looks like one shop. Keep text inside the safe area: shop themes crop squares differently on phones. Tell them once that consistent photos (same light, same background) matter more than the design.

**Print card craft.** A care card is read in the hand: few sizes, clear care steps, their logo, the shop address. Text stays inside the safe area; backgrounds run into the bleed.

## 4. Check and export

- Mark each field with `data-od-field="<column>"` (text, an image's `src`, a link's `href`).
- Check with `export_open_design_artifact` and `checkOnly: true`, `data` set to the list and `nameField` to the title column. Every product is checked, and problems are named by product (a long title that runs out of its box, a photo that didn't load). Fix them and re-check.
- Export each piece with the same `data` and `nameField`: 30 products give 30 product images named after each product. The print card exports as one multi-page PDF, or images at 300 dpi.
- Show them a few results (`check_open_design_artifact`) before calling it done.

## 5. Into the shop

Offer the shop hand-off once: `publish_open_design_artifact_to_shop` prepares a folder with images named by product, the copy, and (for Shopify) a product CSV for their admin. Nothing is uploaded without their yes.

---
name: clickmax-products
description: Use when the user wants to create, inspect, list, archive, unarchive, or delete products in the Clickmax catalog, including one-time-payment and subscription/recurring products.
---

## When this applies

Use this skill for product-catalog identity: create a product (which also mints its main offer), read/list catalog entries, and manage catalog visibility via archive/unarchive or destructive delete.

## Not this skill

- Pricing variants, extra offers, checkout config, cloning, approval → use `clickmax-offers`.
- Choosing/creating the owning project for `projectId` → use `clickmax-projects`.
- Selling through the user's own Whop, Hotmart, Stripe or Pagar.me account (a checkout on a page or funnel step) → `clickmax-pages` external checkout, which checks the integration first and instructs the user to connect it when missing. Never create a Clickmax product as a stand-in.
- A product is the catalog item; an offer is the sellable price point. One main offer is created together with the product; everything beyond that first price point is offer work.

## Key assumptions

- **Interactive wizard — the user decides every product attribute; Max never assumes them.** Only `name` and price come from the request. Everything the user did NOT state — **format/type**, **category**, **one-time vs subscription + payment methods**, **description**, and the **invoice name** — must be ASKED before `products_create`, in one concise batch (a `select` per enum; free-text for the description). Only the invoice name may be pre-filled as a suggestion to confirm. NEVER silently pick `type`/`class`/`category`/`paymentConfig` or fabricate the `description` from the name — that is the single biggest mistake here.
- `products_create` needs `projectId`. Pass a real project id to file the product under it; pass empty string `""` (or any 1-char string) to use the workspace default project. Confirm the project first via `clickmax-projects` when the user named one.
- `products_create` builds the product AND its main offer in one call, returning `{ product, offer }`. Pricing fields on the input apply to that initial main offer.
- Prices are integers in the smallest currency unit (cents). `600 reais` = `60000`, `497` = `49700`. `originalPrice` is the list price; optional `newPrice` is the discounted price actually charged (omit or null = no discount).
- Internal checkout enforces a minimum of R$5,00 (`originalPrice`/`newPrice` >= 500). External checkout (any `externalUrl` set) skips the minimum and treats price as display-only.
- `description` is applied to both product and main offer and MUST be at least 50 characters (a product-form rule that `incompleteReason` does NOT report — enforce it yourself). Collect it with a `type: "textarea"` question (`minLength: 50`, not a single-line `text`). Do NOT fabricate it from the name — ask the user what the product is / delivers; if their answer is under 50 chars, EXPAND it into a fuller sentence from what they told you and confirm, rather than saving a too-short one. Only set it after the user confirms/edits.
- `products_create` also accepts `softDescriptor` (the ≤15-char name shown on the buyer's card/invoice statement) and `supportPhone`. Collect them during creation by ASKING: suggest a ≤15-char `softDescriptor` from the name for the user to confirm/edit — never set it silently, because an auto-filled value makes the later readiness step wrongly treat it as "already answered" and skip confirming it.
- Single-payment vs subscription is decided ONLY by `paymentConfig` (aka payment methods). It is NOT a separate boolean and NOT a product-type field:
  - one-time payment → `paymentConfig.recurrence = null`, with pix/boleto/credit toggles as wanted.
  - subscription/recurring → `paymentConfig.recurrence = { frequency, interval, duration, tolerancePeriod, gracePeriod }`; in that shape boleto is forced off and credit is forced on.
- `type`, `productClass`, and `productCategory` are CLOSED enums — present each as a plain pick-one `select` (NO custom / free-text field, NEVER a "create new category" option) and NEVER invent a value outside the list; a value not in the enum fails or misfiles the product.
  - `type` (offer nature): `community | course | ebook | event | physical | other | services | software | consultancy | mentorship`. ASK which format — do not infer from the name. For `physical`, also ask `quantityItems` (0–100, required).
  - `productClass` maps 1:1 to the chosen `type` (Comunidade | Curso | E-book | Evento | Produto físico | Outro | Serviço | Software | Consultoria | Mentoria) — set it to match `type`, do not ask it separately.
  - **`productCategory` depends on `type`: the valid list is DIFFERENT for physical vs everything else, and the two sets are mutually exclusive.** So ASK `type` FIRST, then build the category `select` from the matching list below. Sending a category from the wrong list fails the creation.
    - `type = physical` → EXACTLY and ONLY these 5: Chás · Cosméticos · Livros · Nootrópicos · Nutracêuticos. No digital category is accepted for a physical product, so never offer "Saúde e Esportes", "Moda e Beleza" or "Outros" here — for a physical supplement the answer is "Nutracêuticos" or "Nootrópicos", for a physical book "Livros", for a cream/makeup "Cosméticos".
    - any other `type` → these 25: Saúde e Esportes · Finanças e Investimentos · Relacionamentos · Negócios e Carreira · Espiritualidade · Sexualidade · Entretenimento · Culinária e Gastronomia · Idiomas · Direito · Apps & Software · Literatura · Casa e Construção · Desenvolvimento Pessoal · Moda e Beleza · Animais e Plantas · Educacional · Hobbies · Design · Internet · Ecologia e Meio Ambiente · Músicas e Artes · Tecnologia da Informação · Empreendedorismo Digital · Outros. The 5 physical ones are reserved for physical products and MUST NOT appear here (an ebook about teas is "Literatura" or "Culinária e Gastronomia", never "Chás").
    - Options MUST be copied VERBATIM from the applicable list — never a nicer-sounding invention, never a merged list of all 30. Known wrong ones the model keeps producing: "Educação" (→ use "Educacional"), "Fotografia e Vídeo" (does not exist → "Design" or "Outros"), "Tecnologia" (→ "Tecnologia da Informação"). Offer the closest REAL values; whatever the user picks must be an exact value from the correct list, never free-typed.
- `productType` defaults to `internal` (Clickmax checkout) vs `external`.
- `language`/`country` default to `pt`/`BR`; `limitToRefund` defaults to 7 days when omitted.
- `products_get` and `products_list` reveal recurrence via each offer's `isRecurrent` / `recurrentInterval` and pricing via `originalPrice`/`newPrice`/`currency`; `products_list` also gives `totalOffersCount` and archive state, and `projectId` narrows it to one project.

## Thought process

1. Separate catalog creation/read from offer-level pricing work; deep pricing/variants belong to `clickmax-offers`.
2. Resolve `projectId` before creating (named project → `clickmax-projects`; otherwise default project).
3. Convert every money value to cents before sending; respect the R$5,00 internal minimum.
4. Decide single vs subscription purely by whether `paymentConfig.recurrence` is null or an object; if the user wants recurrence details not covered at create time, create first then refine the main offer via `clickmax-offers`.
5. For removal, prefer archive over delete when the product may have been used; require explicit intent before delete.

## Execute guide

- Use `mcp__plugin_clickmax_clickmax__products_list` to enumerate catalog products with their offer summaries; pass `projectId` to scope to one project.
- Use `mcp__plugin_clickmax_clickmax__products_get` with the product id to inspect one product and its offers, including per-offer pricing, currency, and recurrence flags; use `checkoutType` to filter offers by `internal` or `external`.
- **Creation wizard (ASK before creating).** When the user asks to create a product, do NOT create immediately. First collect every attribute they didn't give. **`type` must be resolved BEFORE the category question**, because the valid category list depends on it: when the user already stated the format, keep everything in ONE batch; when they did NOT, ask **format/type** (pick-one `select`) first, then send the remaining batch with the category list that matches the chosen type. The rest of the batch: **category** (pick-one `select`, exact values from the list for that type); **one-time vs subscription** (pick-one) and the **payment methods** — the payment-methods question MUST be a MULTI-select (`multiple: true`, renders checkboxes) since more than one applies (pix/boleto/credit; ask credit installments when credit is chosen); the **description** (a `type: "textarea"` question with `minLength: 50` — if the user's answer is shorter, expand it from what they said and confirm; never invent facts, never save under 50 chars); and confirm the **invoice name** (`softDescriptor`, ≤15-char suggestion). Convert price to cents. Only THEN call `mcp__plugin_clickmax_clickmax__products_create` with their answers. After it succeeds, do NOT stop at "product created" — IMMEDIATELY continue in the same flow into the readiness checklist (deliverable, support phone, support email, product image — the fixed checklist in `clickmax-offers`), asking the next batch of questions. Only stop right after creation if the user explicitly said they just want the catalog item registered.
- Use `mcp__plugin_clickmax_clickmax__products_create` to create a one-time-payment product: pass `projectId`, `name`, `currency`, `originalPrice` in cents (optionally `newPrice`), `description`, and `paymentConfig` with `recurrence` set to null and the desired pix/boleto/credit toggles.
- Use `mcp__plugin_clickmax_clickmax__products_create` to create a subscription product: same required fields, but set `paymentConfig.recurrence` to an object with `frequency`, `interval`, `duration`, `tolerancePeriod`, and `gracePeriod` (boleto off, credit on in this mode); `originalPrice` is the per-cycle amount.
- After creating, adjust advanced pricing, installments, or recurrence tuning on the returned main offer via `clickmax-offers` (`mcp__plugin_clickmax_clickmax__offers_update`), and add alternative price points via `mcp__plugin_clickmax_clickmax__offers_create` there.
- A freshly created product is NOT yet sellable: its main offer stays incomplete until it has a deliverable, support phone, invoice name (`softDescriptor`), and description, and is then submitted for approval. When the user wants the product sellable or dropped into a funnel, run the readiness wizard in `clickmax-offers` (diagnose blockers → fill deliverable + support contact (phone + email) + invoice name → send to approval). Ask what the buyer receives; never fabricate the deliverable.
- Use `mcp__plugin_clickmax_clickmax__products_archive` / `mcp__plugin_clickmax_clickmax__products_unarchive` to toggle catalog visibility without losing history.
- Use `mcp__plugin_clickmax_clickmax__products_delete` only for explicit permanent removal.

## Report

- State the created/inspected product identity first: name, `projectId`, currency, and the main offer price (in currency units, converted back from cents).
- Say explicitly whether the product is one-time payment or subscription; for subscription, state the cadence (frequency/interval) and any duration.
- For create, report both the product and its main offer id, and offer follow-up offer/pricing work as opt-in via `clickmax-offers`.
- To let the user OPEN the created product, the CTA must NAVIGATE, not re-ask: use `action="open-page"` with `path="/creator/products/<mainOfferId>/details"`. IMPORTANT: that page loads by the product's MAIN OFFER id — use `offer.id` (the `isMain: true` offer returned by `products_create`), NOT `product.id`. The URL segment is misleadingly named "product" but a `product.id` there opens the wrong/empty page. NEVER use `action="confirm"` for a "Ver produto"/"abrir" button — confirm only re-sends a chat message and does not navigate.
- For list, order by relevance to the request, note archived items, and cap long results with `+N more`.
- For archive/unarchive/delete, state the action result first and keep further actions opt-in.
- After a create/publish that finishes the requested work, follow `clickmax-getting-started` to close with at most one opt-in offer of the next setup task.

## Warnings

- `products_delete` is permanent and removes the product plus its offers; it fails when any offer has transactions. Prefer `products_archive` for anything already in use.
- Do not send raw money values as the price; always convert to cents, and remember the R$5,00 internal-checkout minimum.
- Do not model subscription as a product flag; if `paymentConfig.recurrence` is missing/null the product is one-time regardless of user wording.
- Physical products (`type = physical`) carry three extra hard requirements beyond `quantityItems` (0–100, creation fails otherwise):
  - **Category must come from the 5 physical values**; a digital category is rejected, and those 5 are equally rejected on a non-physical product.
  - **The workspace must have an active Ticto payment setup** — physical products are only sellable through it. Creation fails outright when it is missing, and that is NOT something to work around: report it and point the user to finish the Ticto onboarding in their payment settings.
  - **Shipping config and the stock-proof document cannot be set through this skill.** They are configured on the product page. So after creating a physical product, say plainly that shipping + stock document are still pending there and that the offer stays incomplete (not sellable) until shipping exists — do not run the readiness checklist as if the product were one step away from selling.
- Do not invent a `projectId`; use the default-project sentinel or confirm via `clickmax-projects`.

## Anti-patterns

- Treating product and offer as the same object, or doing pricing/variant work here instead of in `clickmax-offers`.
- Sending price in reais instead of cents.
- Assuming a separate recurrence boolean exists on the product.
- Deleting a product that could be archived, or deleting without explicit user intent.
- Creating from just a name + price — assuming `type`/`class`/`category`/`paymentConfig` or fabricating the `description` instead of asking the user first. Ask, then create.
- Offering a single merged category list for every product, or asking the category before knowing the `type` — the physical and non-physical lists are mutually exclusive, so a category picked without the type is a coin flip the platform rejects.
- Presenting a physical product as ready to sell right after creation, when shipping and the stock document still have to be set on the product page.

---

Clickmax skill revision: `b8294822a4d6`

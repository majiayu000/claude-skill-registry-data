---
name: shopping
description: >-
  When the user asks you to buy, order, reorder, or compare a product on Amazon
  or any other retail site, or sends a product link to purchase, before you open
  the store or add anything to a cart.
---
# Shopping and checkout

You buy products for the user on Amazon and any other retail site. The user picks the product, approves the total, and the payment step stays theirs. You do the searching, comparing, cart building, and form filling, and you show your work with screenshots at the moments that matter.

## Entry points

- "Order more of the coffee filters I usually get" is a reorder; start from order history, not a fresh search.
- "Buy a 65-inch TV under $800 with good reviews" is a compare-then-buy with a budget.
- "Find me a good travel stroller" is browsing; the deliverable is a shortlist before anything goes in a cart.
- A pasted product link goes straight to that product page.

## Before you start

- Resolve what, how many, and any hard constraint (budget, brand, delivery-by date, size). Infer harmless defaults and state them. Ask only when the answer changes what to buy.
- Run SearchPlugins for the retailer the user named. Use a connector when one is installed. When SearchPlugins finds a matching connector that is not installed, ask in the user's words. Send a question widget whose prompt is "Add the <service> connector?" with Yes / No. Do not say plugin, MCP, or plugin id. The widget ends the turn. On yes, follow the Cursor-managed `add-connector` skill: GetPlugin, then InstallPlugin with the stable plugin id on the next turn. Never paste a connect link. New tools arrive on the following message. If the search finds nothing, dispatch a `computerUse` subagent with the site's search URL built from the query, for example `https://www.amazon.com/s?k=bread+flour`, so it lands on results instead of clicking through the home page.
- Read the Memory section for the user's preferred retailer, membership status, default shipping address, sizes, brand rules, and anything they have said about upsells or delivery speed. Call RecallMemory for a past order they mention.
- If the user has a membership (Prime, Walmart+, a store card), note it, because prices and delivery dates differ from the guest view.

## Flow

1. Open the results or the linked product page with the subagent. Ask it to report name, price, rating and review count, delivery date, seller, and the key specs for the top candidates.
2. When the site wants a sign-in, work it in this order and stop at the first step that signs the browser in. If `request_cookie_origin_approval` is among your tools, call it with no origins to list the sites the user's Chrome holds, and request the site when the listing shows it; an approved import usually signs the box browser in with no handoff. Next, send `request_user_form` for the fields on the live page (reason "auth", the site's domain, one form per step); you never see what they type. Last, hand the box to the user with `request_box_help` and one instruction ("Sign in to your <service> account"); the handoff also covers a passkey, a 2FA prompt, or a form the host refused. A one-time code the site texts them is a one-field `request_user_form` with `submitAfterFill: true`. On a captcha or verify-you-are-human check, have the subagent try it first, then follow the same order. Never send a question widget before any of these; the tool is the ask. After a receipt or a hand-back, dispatch the subagent again; the session persists across turns.
3. Compare. For a visual choice (looks, color, a spec table), take a Screenshot and attach the saved path. Summarize price, rating, delivery date, and the specs the user cares about (see Presenting choices).
4. Get the pick. If the user delegated with exact criteria and one product clearly wins, choose it, say why, and still show it before checkout.
5. Check variants. Size, color, quantity, pack count, and subscription versus one-time purchase change the price. Ask with a question widget when the user did not specify and the options are real. Otherwise take the default and say so.
6. Add to cart. For several items, repeat the search, compare, and add cycle, then review once.
7. Review the cart from a screenshot. Confirm each product, quantity, unit price, and seller. Third-party sellers on marketplace sites deserve a mention when they are not the store itself.
8. Shipping address. Reuse the account's saved address when memory or the page confirms it is the right one. If the page needs an address typed, use `request_user_form` with fields targeted at the live checkout page. Reuse a saved vault key from the tool's description when the field is the same fact as one already saved, so the user never retypes an address they have entered before. Confirm the chosen address with the user before you continue.
9. Ask about a promo code before the final page if the checkout has a field for one and the user has not mentioned one.
10. Reach the final review page. Screenshot it. Check the subtotal, tax, shipping, and total against what you presented.
11. Pay (see Paying and confirming).
12. Screenshot the order confirmation and report the order number, the total charged, and the delivery estimate. Save a stated preference (a default retailer, a size) with `update_state` (target "memory") only when the user confirmed it.

## Presenting choices

- Show three to five candidates that differ on something that matters. For each: name, price, rating with review count, delivery date, seller, and the specs the user asked about.
- Attach a screenshot when the choice is visual or the spec table is dense. A summary alone is enough for a reorder.
- Name the tradeoff plainly ("$40 more for the version with a battery indicator"). Do not pad the list with near-duplicates.
- Use a question widget for the pick when the shortlist is short and every option is a real product you saw. Otherwise send the summary and let the user reply.

## Paying and confirming

- The user must have asked to buy this specific item. Never spend on your own initiative, and never buy to hold a price.
- Before payment, send one question widget with the product, quantity, shipping address, delivery date, and the exact total from the review page. A dismissed widget is a no.
- When the site wants payment, a deposit, or a card to hold the booking, work it in this order and stop at the first step that pays. First, a payment method already saved on the account. Have the subagent select it, and when several are saved, ask which one in the confirmation widget. Only when the account has none, and `request_virtual_card` is among your tools this turn, and the site charges an exact total now (tax, fees, tip, and shipping included), raise a one-time card with the site as merchant and type it only into the merchant's checkout; a denial is final. A card kept on file for a hold or a no-show fee is not charged now, so it never gets a one-time card. Last, hand the box to the user with `request_box_help` and one instruction ("Add your card and confirm the payment on <service>"); the same handoff covers a CVC re-entry and any 2FA, 3DS, or bank prompt. The user finishes the payment inside that handoff, so when the box comes back, skip any later confirm or place-order click and read the confirmation page. Card numbers, CVCs, and expiries stay in the merchant's checkout, never in chat or logs.
- Then dispatch the subagent to reach the place-order button and hand the confirm click to the user with `request_box_help` and one instruction ("Place the order in your Amazon cart").
- If the total on the review page moved after the widget, stop and show both numbers before anything is charged.

## Pitfalls

- Membership pricing and delivery promises differ from the guest view. Say which one the user is seeing.
- Out of stock, "ships in 3 to 5 weeks", or a delivery date after the user's deadline is a flag before checkout, not after.
- Bundle suggestions, protection plans, and subscribe-and-save upsells are ignored unless the user asked for them.
- Multi-page checkouts hide the real total until the last page. Screenshot the final review page, not the intermediate ones.
- A marketplace seller with poor ratings or a long ship time is worth a sentence even when the price is best.
- Never invent a price, a rating, a delivery date, or an order number. If the page did not show it, say so.

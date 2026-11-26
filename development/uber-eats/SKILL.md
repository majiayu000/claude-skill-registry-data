---
name: uber-eats
description: "Order food for delivery on Uber Eats in the user's own Chrome session: find the best store for a cuisine, build a vegetarian basket for two at £35–45, take the bundle deals, then stop at the payment screen with the total and ETA for a yes or no. Use whenever the user asks to order takeaway, dinner or food, names a cuisine or dish (Indian, Thai, Chinese, sushi, ramen, tacos, burritos, burgers, falafel, pizza, curry, noodles), says 'order me something', 'get us dinner', '/uber-eats', or asks what to get from a delivery app — even when they never say Uber Eats."
version: 0.1.0
author: Charles Ponti, Hermes Agent
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [food, delivery, takeaway, ubereats, ordering, browser, shopping]
    related_skills: [online-shopping, product-price-monitor]
---

# Uber Eats

Turning "indian food" into a paid-for dinner without asking the user to repeat themselves.

The user's Chrome holds their real Uber Eats session: saved address, Uber One membership, saved card. Ordering from that session is the whole point — a fresh profile has none of it, so use the browser extension (`browsermcp`) rather than the in-app browser or a headless one.

## When to Use

- "Get us an Indian", "order sushi", "I fancy a burrito"
- "Order me something nice, about £40"
- `/uber-eats <cuisine>` with any amount of extra detail
- "What's good near me for Thai?" when the answer ends in an order

## When NOT to Use

- Booking a table → the restaurant's own booking flow
- Groceries and convenience → Uber Eats grocery feeds, but the same cart gate applies
- Price watching a menu over time → `product-price-monitor`

## Standing preferences

These are the defaults, not the whole brief. Anything the user says in the request wins.

- **Diet: vegetarian, and fish/seafood is fine.** No meat, poultry, cured meat or gelatine. Anchovies, prawns, tuna, salmon, fish sauce and shrimp paste are all allowed. Cheese is fine. This is the single most important filter — a wrongly ordered meat dish is worse than a boring one.
- **Two people, £35–45 all-in.** Aim for the total after fees, not the subtotal. Being under is fine; don't pad to hit the number.
- **Deliver to the saved address** shown in the header ("Deliver to …"). Never change it, or pick up instead of delivery, unless asked.
- **Deals first.** Bundles and multi-item offers are routinely 20% off, and Uber One often adds £10 off £25+ with free delivery. A bundle that matches the basket shape beats à la carte.
- **One store per order.** If the cuisine is split across stores, pick the one that does the whole basket well.

## Spending gate

Food orders spend real money, so the skill has one hard stop.

1. **Build the basket, go to the payment screen, then stop.** Report the items, total, and delivery time, and say plainly that nothing has been ordered.
2. **Place the order only after an explicit yes** to that exact total. "Yes", "go on then", "do it" all count; silence, a new question, or "sounds good" aimed at something else does not.
3. **Never type a card number, CVV, or one-time code.** If 3-D Secure or a bank check appears, stop and hand the screen back — that is the user's job.
4. **Report the whole cart.** The session persists, so items from an earlier visit may already be in there. If the cart holds something stale, say so and ask before removing it.
5. **Don't add alcohol unless asked** — it changes the delivery rules (ID on the doorstep) and usually isn't the point.

If the request is genuinely undecidable — no store open, no vegetarian main at any nearby store, an allergy the menu can't answer — say so and stop. Everything else gets a default, not a question.

## Procedure

1. **Read the ask for five things:** cuisine or named restaurant, how many people, budget, timing ("now" vs a time), and any constraint ("no mushrooms", "extra spicy"). Fill gaps from the standing preferences.
2. **Open the store search at the saved address.** Go straight to `/gb/search?diningMode=DELIVERY&q=<cuisine>`; typing into the search box often fails to submit. See [ordering mechanics](references/ordering-mechanics/WORKFLOW.md).
3. **Shortlist two or three stores and pick one deliberately.** Weigh rating with review count (4.3+ is decent, 4.6+ good), ETA, delivery fee, and above all whether the menu has a real vegetarian basket. A 4.8 store with one veg option is a worse answer than a 4.4 with ten.
4. **Read the whole menu in one pass** with the extraction snippet, then choose from the cuisine playbook below. Each dish carries a like-rate and a rating count: prefer 90%+ with a few hundred ratings over a 100% with four. Filter on the diet before you fall for a dish.
5. **Take the deal if it fits.** Bundles are the cheapest way to a two-person basket; check what the bundle lets you pick before committing, because some bundles only offer meat mains.
6. **Add the items and verify the choice.** Bundle pickers hide their selections well — read the chosen rows back rather than trusting the click.
7. **Read the cart panel, not the page.** It is a side panel, and the add-to-cart toast is not proof. Confirm every line, the quantity, the promos, and the ETA.
8. **Checkout, then stop.** Report items, subtotal, discounts, fees, total, delivery time and address, in the format below. Ask for a yes or no.
9. **On yes, place the order and verify it.** Read the confirmation for the order number and the revised ETA. On a change, edit the cart and re-report the new total.

## Report format

Use this every time, including after a change:

```
**<Store>** — <cuisine>, <ETA> min

1. <Item> — £<price>
2. <Item> — £<price>

Subtotal £x · Discounts −£x · Delivery £x · Fees £x
**Total £x** · arriving ~<time> to <address>

Nothing ordered yet — say yes and I'll place it.
```

Keep the per-item prices off bundles ("Bundle for 2 + Drinks — £33.60 (was £42.00)") and list the components underneath, so the saving is visible without arithmetic.

## Cuisine playbooks

Read only the one you need. Each gives the two-person basket, the vegetarian picks (fish allowed), the meat words to grep for, and the traps that catch delivery menus.

- [Indian](references/indian/WORKFLOW.md)
- [Thai](references/thai/WORKFLOW.md)
- [Chinese](references/chinese/WORKFLOW.md)
- [Japanese and sushi](references/japanese/WORKFLOW.md)
- [Mexican](references/mexican/WORKFLOW.md)
- [Burgers and fried chicken](references/burgers/WORKFLOW.md)
- [Middle Eastern](references/middle-eastern/WORKFLOW.md)
- [Pizza and Italian](references/pizza/WORKFLOW.md)

The playbooks describe baskets, not specific restaurants — menus change, ratings move, and a store that was good last month may be closed. Always read the live menu.

## Pitfalls

- **The cart is not a dialog.** `div[role='dialog']` finds the item picker but not the cart panel, and `/gb/cart` renders a near-empty page. Click the header cart button and take a screenshot.
- **A bundle can quietly exclude vegetarian mains.** "Choose 2 pizzas" lists all pizzas; "choose 1 bite" may only offer garlic bread and focaccia. Read the option list before promising a basket.
- **Menu markers beat your memory of a dish.** A "(v)" next to an item is the restaurant's own claim; an ingredient list is better still. Mapo tofu and pad thai are vegetarian or not depending on the kitchen, so check rather than assume.
- **Estimates move at checkout.** The store page's "earliest arrival" is a floor; the checkout ETA is the one to quote, and the confirmation ETA is the one that counts.
- **Ad-blocker console errors are noise.** `ERR_BLOCKED_BY_CLIENT` flooding the console means the user's blocker is doing its job, not that the page is broken.
- **Sponsored rows are the whole first screen.** That is the normal layout, not a warning. Compare rating, review count, fee and ETA rather than skipping the ads.
- **A store's rating is not a dish's rating.** The menu carries a like-rate per dish; a 4.7 store can still have a 71% side dish.

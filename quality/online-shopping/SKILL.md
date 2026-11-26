---
name: online-shopping
description: Use when sourcing a product online or adding to a basket.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    tags: [shopping, retail, amazon, browser, basket]
---

# Online shopping

Sourcing a product and assembling a basket in the user's own browser session.

## When to Use

- "Find me a <thing>" with a budget or a quality bar
- "Add it to the basket / cart"
- Comparing two or three specific models at a retailer

## When NOT to Use

- Price watching over time → `product-price-monitor`
- Completing a purchase → the user does that, see the safety gate

## Safety gate (applies to every step)

1. **Adding to a basket is allowed on request. Paying never is.** Stop at the basket and
   report the total; place an order only after the user replies with an explicit go-ahead
   for that exact total.
2. **Never type card numbers, CVVs or one-time codes.** At a payment form, stop.
3. **Report the whole basket, not just your item.** The local browser carries the user's
   real session, so their existing items are already in there.

## Procedure

1. **Pick the marketplace.** For UK pricing and delivery, Amazon.co.uk is the dependable
   default. Manufacturer sites and some big-box retailers routinely answer with an
   access-denied or bot-wall page; one attempt is enough, then move to a marketplace
   listing rather than retrying URL variants.
2. **Search, then verify the page actually has results.** A mistyped or invented filter
   param (e.g. a brand restriction `rh=p_123%3A<id>`) returns a valid page whose body says
   "No results for your search query" — that is a filter error, not an absent product.
3. **Extract the result cards programmatically.** `browser_exec` with `local=True` for the
   user's own session; read with `js()`, never screenshots.
4. **Open the shortlist (two or three) and read the buy box** — price, seller/shipper,
   stock, delivery estimate, rating and review count.
5. **Choose and say why.** When the request is "a good/sick one" with no budget, lead with
   the flagship tier and name one runner-up with the reason to skip it.
6. **Add to basket, then load the cart page and re-read it.** The add-to-cart click returns
   a confirmation page; the cart page is the proof.
7. **Report**: model, price, the two or three specs that justify it, seller, delivery,
   rating with count, what else is in the basket, new subtotal, and an explicit "nothing
   ordered".

## Extraction snippets

Result cards (works on Amazon UK; `data-component-type="s-search-result"` no longer matches
on every layout, so fall back to the asin cards):

```python
js("""(() => {
  const out=[];
  document.querySelectorAll('div[data-asin]').forEach(el=>{
    const a=el.getAttribute('data-asin'); const h=el.querySelector('h2');
    if(!a||!h) return;
    const t=h.innerText.trim(); if(t.length<20) return;
    out.push({a, t:t.slice(0,110),
      p:el.querySelector('.a-price .a-offscreen')?.textContent||'',
      r:el.querySelector('[aria-label*="out of 5 stars"]')?.getAttribute('aria-label')||''});
  });
  const s=new Set(), u=[]; for(const o of out){ if(!s.has(o.a)){s.add(o.a); u.push(o);} }
  return JSON.stringify(u.slice(0,15));
})()""")
```

Buy box, on the product page (`/dp/<ASIN>`):

```python
js("document.getElementById('desktop_buybox')?.innerText.slice(0,700)")
js("document.getElementById('productTitle')?.innerText.trim()")
js("document.getElementById('acrCustomerReviewText')?.innerText")
```

The buy box text carries the price, `In stock`, the delivery date and a
`Shipper / Seller` row. For big-ticket items prefer the listing where that row reads
`Amazon` rather than a marketplace seller.

Add, then reload the cart and read the line items — not just a subtotal:

```python
js("document.getElementById('add-to-cart-button').click()")     # then wait ~6s
goto_url("https://www.amazon.co.uk/gp/cart/view.html"); wait_for_load()
js("""(() => {
  const out=[];
  document.querySelectorAll('[data-name="Active Items"] [data-asin]').forEach(el=>{
    const a=el.getAttribute('data-asin'); if(!a) return;
    const t=el.innerText.split('\\n').filter(x=>x.trim().length>15)[0]||'';
    const p=el.innerText.match(/£[\\d,]+\\.\\d{2}/);
    out.push(a+' | '+(p?p[0]:'?')+' | '+t.slice(0,90));
  });
  return [...new Set(out)].join('\\n');
})()""")
js("document.body.innerText.match(/Basket Subtotal:?\\s*£[\\d,.]+/)?.[0]")
```

`#sc-subtotal-amount-activecart` is absent on the current cart layout and returns null —
read the subtotal from body text and cross-check it against the sum of the line prices.

## Pitfalls

- **A search-result price is not the buy-box price.** Result cards can show a "from" price
  or a different variant/size, and the selector can come back empty on a curated layout.
  Read the price on the product page before quoting it.
- **The cart subtotal is the honest number.** After adding, list every line in the basket —
  leftover items from earlier sessions look like your addition otherwise, and the user will
  notice the total does not match what you said.
- **A null subtotal selector is not an empty basket.** Current Amazon cart markup has no
  `#sc-subtotal-amount-activecart`; a None there says nothing about whether the add worked.
  Read the item rows by ASIN and the `Basket Subtotal` line instead.
- **Blocked pages are not a dead end.** A bot-wall on a manufacturer or retailer site means
  "use another route", not "the product is unavailable". Try the marketplace once, and tell
  the user which route you used.
- **When no route yields the listing, answer from the material and label it as inference.** A 403 on a plain fetch,
  the same wall in the real browser session, and no Wayback/archive copy is a _provenance_ problem, not an answer:
  discount retailers run one-off stock and their product URLs go dark when a run sells out, so the page may not
  exist any more. In that case say the listing could not be read, answer from what the title already guarantees
  (a "suede" boot is not rainproof, whatever the page might have claimed) and say which part is inferred — never
  present inference as the listing's own claim. Ask for the description or the brand when the claim actually matters.
- **Water-resistance is a material question, not a feature bullet.** Suede and nubuck are water-_repellent_ at best,
  and only after a protector spray (Nikwax Nubuck & Suede Proof, Saphir Super Invulner, Crep Protect) — never
  waterproof, and the napped surface marks permanently when it wets through. Honest wet-weather answers are oiled or
  full-grain leather with a rubber sole, or a boot with a membrane. Say that instead of repeating a seller's
  "water resistant" sticker as if it meant rainproof.
- **Do not invent filter IDs or product codes.** Search plain terms, or search the model
  number the user named (`AW3225QF`), which also surfaces the premium alternatives.
- **Resist the cheapest match.** The top result for "<brand> monitor" is often a basic
  office panel; when the user asks for something good, sort mentally by panel class
  (OLED/QD-OLED, resolution, refresh) before price.

---
name: meta-ads-launch
description: Launch a Meta (Facebook/Instagram) ad campaign through the Marketing API as PAUSED objects a human activates — campaign, ad set, image, creatives, ads — with the fields that hard-error when missing, real interest IDs from the Targeting Search API, multipart image upload, a Stripe payment link that unlocks the landing page, single-image and 4:5 carousel creative rendered from HTML, an end-to-end validation checklist, and the create-new-then-swap flow for changing a headline. Use when launching paid social for a landing page, building ad creative, or refreshing a low-CTR headline.
compatibility: >-
  Calls the Meta Marketing API and Stripe API with the user's own tokens. Creates objects PAUSED only.
metadata:
  network-hosts: "graph.facebook.com api.stripe.com"
  network-purpose: "create paused campaigns, look up interest ids, create payment links"
---

# Meta ads launch (API, PAUSED hand-off)

Build everything, validate it end to end, and hand over a **PAUSED** campaign. Activating spend is
the owner's click, never yours.

## 1. Answer three questions before building anything

- **The headline stat**: one specific figure that stops a scroll ("$40K labour-rate gap", not
  "potential savings").
- **The free value above any gate**: one tactic someone can complete in a week without buying.
- **What the paid step delivers**: every promised item fully written before launch. No stubs, no
  "...". Read the paid content end to end as a buyer.

## 2. Landing page and payment link

If the page sells something, a Stripe Payment Link that returns to the page unlocks it:

```python
# POST /v1/products, /v1/prices, then /v1/payment_links with:
"after_completion[type]": "redirect",
"after_completion[redirect][url]": "https://<site>/<page>?session_id={CHECKOUT_SESSION_ID}",
```

The redirect **must** carry `?session_id={CHECKOUT_SESSION_ID}` (Stripe fills it in). A page script
that unhides content on `session_id` is a soft gate only; verify the session server-side for anything
worth protecting.

## 3. Creative

**Message-match the ad to the page.** The biggest lift isn't a punchier headline, it's the ad and the
landing page reading as one object. Reuse the page's real colours and fonts and its real numbers;
never invent statistics for the card.

- **Single image**: 1080x1080 feed image, rendered from HTML with a headless browser screenshot.
- **Carousel**: 4:5 cards at 1080x1350. Arc: hook (a stat as a direct question) -> 2-3 proof cards
  (real numbers from the page) -> CTA card. **Type 2-3x larger than on the page** (hero numbers
  150-220px, body 30-45px). If the page headline uses a distinctive font, confirm the rendered card
  really uses it (read the image, not the CSS). QA at full size **and** at ~25% scale.
- **Caption**: match the CTA to what the page actually does (instant reveal vs form first). Save a
  plain `primary_text.txt` (paste-ready) beside the images.
- **Headline pattern that won on live data**: personal question + "your" + a specific loss or gap,
  5-8 words ("What's your shop leaving on the table?" 1.31% CTR) beat third-person statements ("Most
  restaurants have the same three problems", 0.42%).

## 4. Targeting: real interest IDs only

Never use guessed IDs. Look them up:

```
GET https://graph.facebook.com/v21.0/search?type=adinterest&q=<keyword>&limit=5&access_token=...
```

3-4 specific interests beat broad ones ("small business" adds volume, not precision). Set age and
geo deliberately. If you want your targeting respected, disable Advantage audience
(`"targeting_automation": {"advantage_audience": 0}`).

## 5. Create the campaign, all PAUSED

Campaign -> ad set -> image -> creatives -> ads, every object `status: PAUSED`. Fields that hard-error
when missing:

| Error | Cause | Fix |
|---|---|---|
| "Invalid parameter" on campaign create | missing budget-sharing flag | `"is_adset_budget_sharing_enabled": false` |
| "Bid Amount Required" | no bid strategy on the ad set | `"bid_strategy": "LOWEST_COST_WITHOUT_CAP"` |
| "Advantage Audience Flag Required" | missing in targeting | `"targeting_automation": {"advantage_audience": 0}` |
| "file is invalid" on image upload | JSON/base64 body | multipart: `files={"filename": (name, bytes, "image/png")}` |
| "Facebook Page is Missing" | wrong page id | `GET /me/accounts` for the real Page ID |
| interest IDs rejected | IDs were invented | Targeting Search API |
| "App in development mode" | app unpublished | publish it in the developer console |

Build a `--dry-run` that prints every payload first.

## 6. End-to-end validation (before hand-off)

```
[ ] Landing page loads on the live URL, on a phone
[ ] Payment button shows the right price and the right product name
[ ] A test-mode payment redirects back with ?session_id= and the paid content appears
[ ] Every promised item exists in full; nothing ends in "..." or placeholder text
[ ] Pixel PageView fires on load; InitiateCheckout fires on the buy click
[ ] All ads visible in Ads Manager, PAUSED, each with the right image and the right link
```

Hand-off: campaign name, the live URL, which variant to watch first, and that it is PAUSED.

## 7. Changing a headline later

Wait for 3+ days and 500+ impressions per ad; under ~0.8% CTR is a headline problem first.

**Meta can't edit a creative in place.** Create a new creative with the same `image_hash`, link, body
and CTA, changing only `object_story_spec.link_data.name` (the headline), then swap it onto the ad:
`POST /{ad_id}` with `{"creative": {"creative_id": NEW_ID}}`. Never rewrite body copy that a human
wrote without asking.

**Error subcode 1487194** ("account type restriction") on creative create usually means the ad account
is in `account_status: 3` (unsettled billing). Existing ads keep running; don't retry. Give the human
the 30-second manual edit in Ads Manager instead, with the exact text to paste.

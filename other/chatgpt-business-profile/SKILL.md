---
name: chatgpt-business-profile
description: Get a business ready to claim its profile in ChatGPT (OpenAI's Businesses in ChatGPT, managed in Business Hub). Finds what customers search about the brand, checks what ChatGPT tells them today against the website, then writes the profile to paste in, the site fixes to make first, the questions to test a Business Agent with, and the steps to claim and verify. Works best with the RomeoSEO MCP connected and still works by hand without it. Use for "claim our business on ChatGPT", "set up Business Hub", "make a Business Agent" or "what does ChatGPT say about us".
license: MIT
metadata:
  author: RomeoSEO
  version: "3.0.0"
  homepage: https://romeoseo.com/skills/chatgpt-business-profile
---

# Claim and set up your business in ChatGPT

Get a business ready for Businesses in ChatGPT, the free profile OpenAI opened in beta on 10 November 2026 and manages from Business Hub (chatgpt.com/business-hub). Read what the website says, find what customers search about the brand, check what ChatGPT answers today, and fix the gaps before anything is pasted into the profile. You hand back the profile text, a short fix list for the site, Business Agent test questions with the right answers, and the claim steps in order.

> **Romeo's rule:** ChatGPT reads your website long before it reads your profile, so make the two say exactly the same thing, then claim.

## Use this when

- The owner wants to claim, set up or tidy their business profile in ChatGPT, or asks what Business Hub or a Business Agent is.
- ChatGPT already describes the business and the owner wants to check it before claiming.
- An online store or online service in the US wants a Business Agent and needs it to answer correctly from day one.
- The profile is claimed but Insights look empty and the owner wants to know what to do next.

## Don't use this for

- Tracing every wrong claim across ChatGPT, Gemini, Perplexity and the rest back to its source → `ai-brand-facts`.
- Whether the brand is recommended for "best X for Y" questions at all → `ai-search-visibility`.
- A shop's product data, feeds and AI shopping results in depth → `ai-shopping-visibility`.
- A local business's maps listings and reviews → `local-ai-visibility` and `local-seo-audit`.

## What you need

### Required

- The website, the brand name exactly as written, and the kind of business: an online store, an online service, or a place customers visit.
- The country the business serves. A Business Agent is for eligible US online stores and online services only at launch; claiming a place customers visit was reported as US-only and only for an existing listing.
- Someone who owns the business or may act for it. Only they can claim, verify and pass the identity check.

### Helpful

- **The RomeoSEO MCP** ("Romeo in AI apps", setup at romeoseo.com/mcp), connected to the website. It gives the business Romeo writes for, the pages as Romeo read them, Google Search Console searches, live keyword numbers and a live re-read of any page. Every step below says which tool to use.
- Access to the business's main phone line, an email address at the business, or the domain's DNS settings, for verification. Shopify stores can verify by connecting the store.
- The ID and business documents the identity check asks for (government ID, business registration, proof the person may act for the business).
- The free Chrome extension "AI Visibility & Rank Checker for ChatGPT" (romeoseo.com/chatgpt-rank-tracker). It shows what ChatGPT searched for, the pages it read and linked, and the brands it named.

### No tools?

Read the About, pricing, delivery, returns, contact and FAQ pages yourself. In Google Search Console, open Performance, filter queries containing the brand name, and sort by impressions for the last 3 months. Type the brand into Google and note what autocomplete adds ("pricing", "reviews", "legit"). Ask the questions in ChatGPT yourself (step 3). Everything else in this skill works the same.

## Ground rules

- The profile says only what the website already says, in the same words. If a fact isn't on a public page, put it on the site first or leave it out.
- Never answer a question yourself and call it ChatGPT's answer. RomeoSEO's tools read Google and the website; they do not ask ChatGPT. The answers come from the owner, the extension, or a ChatGPT session you can actually run.
- Never guess search numbers. Use what Search Console or `check_keywords` returns, and say "too few searches to count" when that is the answer.
- Claiming doesn't move the business up in ChatGPT's answers, and OpenAI says so. It adds a checked badge, lets the owner correct the basics, and opens Insights and (if eligible) a Business Agent. Say this before the owner spends an afternoon on it.
- Plain claims only: no "best", "#1", "leading" or made-up numbers. OpenAI reviews every profile change and every agent update before it goes live.
- The owner does every verification step: phone codes, email codes, DNS records, ID upload. You write the DNS record and the text to paste; you never enter codes, IDs or logins.
- Business Hub is in beta. Menus and rules will change. OpenAI's own pages often block automated reads, so give the owner the links in "Sources" and ask them to check anything that looks different.
- With the RomeoSEO MCP: this skill starts no research, writing or page improvements and sends nothing to the website. Only start paid work if the owner asks.

## Steps

1. **Write down what the business is, from its own pages.** One line per fact, each with the page it's on.
   - Name, one-line description (25 words or fewer: what it sells, to whom, where), category in the words buyers use, countries served.
   - For a store: delivery areas, delivery times and costs, the return window, who pays return shipping, how refunds are paid.
   - For a service: plans and prices, free trial terms, how to cancel, refunds.
   - For a place: address, phone, opening hours, the area served.
   - With Romeo: `list_sites`, then `get_site_overview` for the business Romeo writes for and the website's research market. `find_pages` with search `about`, `pricing`, `shipping`, `delivery`, `returns`, `refund`, `contact` and `faq`, then `find_pages` with each page's `url` to read it. `find_pages` only knows pages from Romeo's last read of the website, so when a search finds nothing, try `reread_page` on the usual paths (`/about`, `/pricing`, `/shipping`, `/returns`, `/contact`, `/faq`) before saying the page doesn't exist.
   - A fact you can't find on any page is a question for the owner, not a profile line.

2. **Find what customers search about the brand.** Keep up to 15 searches, most shown first.
   - With Romeo: `get_search_console_report` with report `searches`, metric `impressions`, days `90`, limit `25`. Keep rows marked `brand: true`, drop rows marked `looksAutomated`, and check `brandNames` lists every spelling of the brand. Most websites have only a few brand searches among the top 25; that is normal, and the next bullet fills the gap. If Search Console isn't connected, say so and go straight to the next bullet.
   - Then one `check_keywords` call with up to 10 brand searches people commonly type: `[brand] pricing`, `[brand] reviews`, `is [brand] legit`, `[brand] shipping`, `[brand] returns`, `[brand] discount code`, `[brand] vs [main competitor]`, `[brand] alternatives`, `[brand] near me` (places only). Tell the owner this uses part of today's keyword checks. Report `tooFewSearchesToCount` as "too few to count", never as zero.
   - Turn the searches into 8 to 12 plain questions a customer would ask ChatGPT: "What is [brand]?", "Is [brand] legit?", "How much does [brand] cost?", "Does [brand] ship to [country]?", "What is [brand]'s return policy?", "[brand] or [competitor] for [use]?".

3. **Get ChatGPT's answers today.** Ask each question in a Temporary Chat (so memory doesn't shape it), with search on, in the business's country. Ask money and trust questions twice; answers change between runs.
   - The owner can paste each answer and its linked sources, or use the extension, which records what ChatGPT searched, read and linked. Its "Send to Romeo" button brings a check into Chat with Romeo inside the app.
   - Note for each answer: whether the brand was named, what it said, and every page it linked.

4. **Check each answer against the website.** Give each claim one verdict: right, partly right, wrong, out of date, couldn't check, or the site disagrees with itself.
   - Open every linked page. If it's the business's own page, read it with `find_pages` (`url`) or, to see it as it is right now, `reread_page`. If it's another site (a directory, a review site, an old press article), list it as an outside source to update.
   - "Couldn't check" means the site doesn't say. That is a site fix, not a ChatGPT problem.

5. **List what the site gets wrong or leaves out.** Fix these before claiming; the profile can't overrule a website that says something else.
   - Two pages that disagree (two return windows, an old price on a blog post or PDF).
   - A customer question with no answer on any page (shipping to Canada, cancelling a plan).
   - Policies only in a PDF, an image, a chat widget or the checkout. Put them in plain text on a page people can reach.
   - With Romeo: Romeo puts page improvements on the plan from its own research. For one specific page change the owner wants now, `read_product_guide` (topic `overview`) gives the Chat with Romeo link that adds it. After a fix goes live, `reread_page` confirms it.

6. **Write the profile.** Every line comes from step 1 and points to its page.
   - Website: the main address the site really uses (with or without www, as the site redirects to). With Romeo, `get_site_overview` shows the address Romeo uses.
   - Business description: the one-liner, then a 50 to 80 word version with what it sells, who it's for, where it serves and one fact that sets it apart. No superlatives.
   - Category: the plain category buyers use, not a slogan.
   - Delivery policy and return policy (stores): a short, exact summary of the site's policy, with the policy page's address.
   - Logo and cover photo: say which files to use; the owner uploads them.
   - Stores: the product feed, or connect Shopify, which syncs the catalogue. The feed needs at least item_id, title, description, url, brand, seller_name, image_url, price (as `20.00 USD`) and availability. A standard feed upload is for the US.

7. **A place customers visit: match the listing everywhere.** Name, address, phone and hours must read the same in ChatGPT, on Google and on the website. RomeoSEO's tools don't read Google Business Profile, so the owner checks that one. Claim the main brand and each location separately; claiming one doesn't claim the others.

8. **Write the Business Agent's test questions** (eligible US online stores and services). 12 to 15 questions, each with the right answer and the page it comes from.
   - The top searches from step 2, as questions.
   - The questions step 4 marked "couldn't check", once the site answers them.
   - Three trap questions it must handle well: a product or feature the business doesn't offer (it should say no), a discount that doesn't exist (it should not invent one), and "where is my order" (the agent can't look up orders, take payments or make bookings, so it should point to the right page).
   - The owner previews the agent with these questions before pressing Publish, and again after each change.

9. **Hand over the claim steps** (see "Claim it" in the template). Then set a date four weeks out to read Insights and run step 3 again with the same questions.

## What to hand back

```markdown
# ChatGPT business profile: [brand], [date]

**Business:** [name] - [online store | online service | place customers visit] - [country] - [website]
**Ready to claim?** [Yes | After the fixes below] - [one line why]
**What claiming does:** a checked badge, an editable profile and Insights [and a Business Agent]. It doesn't move you up in ChatGPT's answers.

## What customers search about [brand]
| Search | Times shown in Google (90 days) or monthly searches | Source |
|---|---|---|
| [search] | [number or "too few to count"] | [Search Console | keyword check] |

## What ChatGPT says today
- "[question]" - [date], [runs] - named: [yes/no] - says: "[quoted claim]" - verdict: [right | partly right | wrong | out of date | couldn't check | site disagrees with itself] - linked: [URLs]

## Fix on the site first
1. [page URL]: [what to change] - fixes: [question or claim] - [Fix now | Fix next]

## Outside sources to update
- [site, URL]: [what it says] -> [what it should say]

## Profile to paste
- **Website:** [address]
- **Business description:** [one-liner] / [50-80 words]
- **Category:** [category]
- **Delivery policy:** [summary] - [policy page]
- **Return policy:** [summary] - [policy page]
- **Logo / cover photo:** [files]
- **Products:** [feed file | connect Shopify | not a store]

## Business Agent test questions
| Question | Right answer | Page it comes from |
|---|---|---|

## Claim it
1. Sign in to ChatGPT with the account that will own the profile and open Business Hub (chatgpt.com/business-hub, also in the sidebar).
2. Find the business or start a new one, and pick a verification method: a text or call to the main business phone, a code to a business email address, a DNS TXT record on the domain ([record to add]), or Connect Shopify.
3. After the claim is approved, finish the identity check (done through Persona): government ID, business registration and proof you may act for the business. The badge, publishing, Insights, feeds and agents unlock after this.
4. Paste the profile above under the business, upload the logo and cover photo, and submit. OpenAI reviews it before it shows.
5. Stores: upload the product feed or connect Shopify.
6. If offered: create the Business Agent, check what it will answer from, write its instructions, test it with the questions above, then Publish.
7. Add teammates or an agency in Business Hub if needed; each uses their own ChatGPT account.
8. On [date + 4 weeks]: read Insights (last 28 days; a blank number means not enough activity to show yet, not zero) and look for visits tagged `utm_source=chatgpt.com` in the site's analytics. Then ask the step 3 questions again.

## What I could not check
- [Google Business Profile, a page that didn't load, a fact the owner must confirm, a menu that looked different]
```

## Stop and flag if

- The person asking doesn't own the business and isn't allowed to act for it. Stop; only they can claim it.
- Someone else already claimed it. The owner can use "Dispute ownership" in the listing's "•••" menu, or contact OpenAI if the listing says "Contact support".
- The business is in a category OpenAI may hold back or decline (age-restricted, health, finance, gambling and similar). Say so before the owner gathers documents.
- The owner wants the profile or agent to claim things the site doesn't back: invented reviews, prices, discounts, awards or urgency. Decline that part; OpenAI's rules for agents forbid it too.
- A ChatGPT answer makes a safety, legal, health or money claim about the business, or looks defamatory. Tell the owner at once and hand over to `ai-brand-facts`.
- A published profile is hard to take back: OpenAI support can remove drafts but not a published profile. Get the owner's OK on the final text before they submit.

## Sources

Businesses in ChatGPT launched in beta on 10 November 2026. Details above come from launch coverage of OpenAI's announcement; check OpenAI's pages, which may block automated reads:

- OpenAI announcement: https://openai.com/index/introducing-businesses-chatgpt/
- Product page: https://openai.com/business/businesses-in-chatgpt/
- Policies: https://openai.com/policies/businesses-in-chatgpt/ and https://openai.com/policies/business-agents-policy/
- Product feed spec: https://developers.openai.com/commerce/specs/file-upload/products

## Next step

- Run `ai-brand-facts` if ChatGPT, Gemini or Perplexity keep repeating wrong facts from outside sites.
- Run `ai-search-visibility` to see whether the brand is named when people ask for the best options in its category.
- With the RomeoSEO MCP: ask Romeo for keyword research on the questions customers asked in step 2 (`start_research` with `focus_keywords`, only when the owner wants it), so the site has a page that answers each one.

---
Part of the free RomeoSEO skill library: https://romeoseo.com/skills

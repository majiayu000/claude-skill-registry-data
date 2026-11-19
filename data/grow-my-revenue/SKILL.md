---
name: grow-my-revenue
description: Find the three changes most likely to grow your revenue, with the money math, by reading every source you have (Stripe, PostHog or GA4, app stores, Search Console, CSV exports) against what shipped, and publish them as one dashboard page. Use when someone asks "what should I tweak", "how do we grow revenue", "why did sales drop", "refresh the growth dashboard" or "how do we convert better".
---

# grow-my-revenue

You are a head of growth who has taken several products from small to large monthly revenue. The user does not
want the data. They want the three moves that grow revenue most, with the money math, and the data one scroll down
if they want to check. Answer bottom line first (see `no-fluff`).

**You are the intelligence.** The scripts collect and pre-compute; you read it all, check it against what shipped
and against the code, and decide. Do not hand back tables. If the user wants this on a schedule, ask first: a
scheduled agent run costs money.

## 0. Set up once

Ask the user, in one message, only what you cannot find yourself:
- **The product and its sales.** Which payment system (Stripe, Paddle, App Store, Play, Gumroad, a database table).
  If one account sells several products, which product ids are this one.
- **The sources they have.** Product analytics (PostHog, GA4, Amplitude, Mixpanel), app stores (App Store Connect,
  Play Console), Search Console, email tool, ads. Each one is optional. One sales source plus one traffic or usage
  source is the minimum for a useful read.
- **The repos** that ship the website and the product (owner/name), so changes can be matched to dates.
- **Their time zone**, so days match the way they read sales. Note that Stripe's dashboard counts days in UTC.
- **Facts they have set** that you must not argue with: things like "no discounts", "we never bundle X", "the ads
  setup is deliberate". Write them to `facts.md` in the working folder and reread it every run.

Keys: read-only keys only (a Stripe restricted key, a PostHog personal key with query access), kept in env vars or
an env file outside any repo. Never print a key. Aggregates only: no emails, person ids or IPs in any file you write.

## 1. Collect

Pick a working folder outside the repo, for example `growth/` in the agent's scratch space, as `$D`. Put one CSV per
source in `$D` (each with a `date` column), then run the scripts. Scripts live in `scripts/` beside this file.

```bash
S=<this skill>/scripts
STRIPE_API_KEY=... python3 -I $S/stripe_daily.py "$D/stripe.csv" --since 2026-01-01 --tz Europe/Berlin [--product prod_x]
POSTHOG_API_KEY=... POSTHOG_PROJECT_ID=... python3 -I $S/posthog_daily.py "$D/web.csv" --prefix web_ \
    --event signup_completed --event checkout_started --tz Europe/Berlin
# Other sources: export a daily CSV and drop it in $D (see the table below).
python3 -I $S/merge.py "$D" --periods "$D/periods.csv" --events "$D/events.csv"   # daily.json, periods.json, events.json
python3 -I $S/correlate.py "$D"            # what moves with orders and revenue, price periods taken out
python3 -I $S/changes.py "$D" --repo owner/site=Website --repo owner/app=App --tz Europe/Berlin   # timeline.json
python3 -I $S/brief.py "$D"                # brief.md: every source on one page
```

`stripe_daily.py` prints each order amount with its first and last day. Use that to write `periods.csv`
(`start,end,label`): one row per price or plan setup. Add `events.csv` (`date,kind,label`) for launches, releases,
campaigns, outages and tracking changes you know of. Ask the user for anything big you cannot date.

| Source | How to get a daily CSV | Ask it |
| --- | --- | --- |
| Stripe | `stripe_daily.py` | Revenue, orders, plan mix (one-time vs subscription), new payers, failed payments, refunds |
| Other payments (Paddle, Lemon Squeezy, Gumroad, own DB) | Their export, or a SQL query grouped by day | Same as Stripe |
| PostHog | `posthog_daily.py` per project (website, app), or your own HogQL | Visitors, each funnel step, activation |
| GA4 | Explore → free form, rows = Date, export CSV; or the Data API | Visitors, sources, conversions |
| App Store Connect | Analytics → export (impressions, product page views, downloads, sales) | Store page view rate, download trend, crashes |
| Play Console | Statistics and Android vitals → export | Installs, crash and ANR rate against Google's bad-behavior lines |
| Search Console | Performance → Dates tab → export | Clicks and impressions; queries and pages with impressions but few clicks (export the Queries tab too) |
| GitHub | `gh api repos/<o>/<r>/traffic/views`, release download counts | Stars, downloads, open bugs |
| Email, ads, mentions | Their export | Sends, bounce rate, spend, mentions trend |

For a question the files do not answer (sources, countries, funnels by device), run your own query against the same
API. Add a limit; some APIs cut results silently (PostHog's query API stops at 100 rows without one).

## 2. Make the call

**Read `brief.md` top to bottom first.** It is the whole picture on one page, and that is where the call gets made.
Go to the other files only to check a lead.

Then write `decision.md` in `$D` before you build the page. It has four parts:
- **Thesis:** one sentence on what drives revenue right now and where it is heading, with numbers from at least
  three sources. Example shape: launch buzz is fading (mentions down), while purchases that start in the app rise.
- **The path to money:** how the pieces fit this week (store page → app → website → checkout, or search → article →
  signup → trial → paid). Which links in the product send people where, why (read the code), and what each earns.
- **Candidates:** every move worth considering, with money = people affected × likely lift × price, its sources,
  and how sure you are.
- **Rejected:** what you dropped and why: a thin sample, a tracking gap, a link that was deliberate.

The top three by money go on the page. Ask these in order:

1. **Where is revenue now and what is its ceiling?** Revenue a day and per visitor by period (`periods.json`). If
   price changes move orders but not revenue, price is not the lever; reach, activation and plan shape are.
2. **Which users are worth most, and how do you get more of them?** Paid rate by platform, buy rate by traffic
   source. The best channel with a broken path is the first fix.
3. **Where does activation leak?** The in-product funnel to the first moment of value, and what activation is worth
   (do people who reach it come back or pay far more often?).
4. **Where does the purchase leak?** Checkout funnel, checkout by country, one-page exits, page speed on phones,
   rage clicks.
5. **Top of funnel:** store page view rate, traffic sources, search queries, articles.
6. **Every source, every run.** Before ranking, write one line to yourself for each source, with its freshest number
   and what it says about revenue. A move needs at least two sources agreeing. The website is one source of many; a
   website-only answer is a lazy answer.

Rank moves by money: people affected × likely lift × price. Give each a rough monthly number. Three moves, the rest
as one-liners.

### Rules that keep it true

- **No cause without the timeline.** Before saying why a number moved, find what shipped then in `timeline.json`.
  A price change beats a UI change. A jump on the day of a price cut is the price cut, not the banner that shipped
  the same week.
- **Check what an event means in the code** before you lean on it. Search the website and app code for where each
  event fires. Common traps: an event that was never sent until a recent fix (do not use its rates before the fix);
  a server-side event with no device or country (use the client event for those cuts); a "checkout started" event
  that fires when the pay form opens by itself (read it as "saw the pay form"); analytics that only has real volume
  from some recent date. Note each trap you find in `facts.md` so the next run starts from it.
- **Drop correlations that are consequences**, not causes (licence activations follow purchases). A correlation is
  a lead to check, never a finding.
- **Compare like with like.** Judge periods at similar traffic, and say which one made the most money a day. Never
  write a headline the chart beside it contradicts. Read your own card next to its chart before publishing.
- **Full days only.** Today is partial: `merge.py` stops at yesterday. Say how many full days a new period has, and
  do not judge it under seven.
- **Check the sample.** Before leaning on a rate, check who it covers. If analytics sees only a sliver of one
  platform's users, that platform's rates are not a finding.
- **Read the code before calling a link wrong.** A link that sends people from one product to another may be a
  deliberate cross-sell. Judge it by what it earns and what it is for.
- **Dashboards' own summaries are leads, not findings.** "Everyone leaves at the email box" can be a tracking gap
  (the event fired for fewer people than bought). Check against raw numbers.
- **Know what already exists** before you propose it. Check the pricing page and Stripe before suggesting a plan
  that already sells.
- **Bots** (about 0 second visits, 100% one page, a newsletter's link prefetch) stay out of conclusions.
- **Facts the user set** (`facts.md`) are not up for debate.

## 3. Build the dashboard page

Write `decision.json` (format at the top of `scripts/page.py`), then:

```bash
python3 -I $S/page.py "$D" "$D/decision.json" "$D/growth-dashboard.html"
```

The page layout is the method, keep it:
- **First fold = growth only.** A one-line headline, then three move cards. Each card: the move as the heading, one
  proof line, one line on why and the money. Under the cards, the smaller moves as a list.
- **Numbers are never typed.** Write marks like `{avg7:revenue|money}` or `{chg7:signup_people}` and the page fills
  them from the data, so a card cannot drift from its source. `page.py` exits with code 2 and lists any mark it
  could not fill: fix every one before sharing.
- **Proof under each move:** the two or three charts that prove it. Each chart's title is the finding (a sentence,
  not a label) and its `so` line says what it means, with live numbers.
- **Then the big picture** (sales against price periods). Everything else is folded under "All data". A chart that
  supports no move stays folded or goes. Many charts with few insights is the failure to avoid.

**Where to put the page.** If your agent can publish a private web page (in Claude, an Artifact), publish
`growth-dashboard.html` and keep its link in `$D/DASHBOARD_URL`; next run, update the same page. Otherwise give the
user the local file path; it opens in any browser with no server. Before handing it over, open it and read each card
next to its chart.

## 4. Answer

Bottom line first. Link the page, then at most four bullets: revenue now and the one thing holding it back, then the
three moves with their money. Offer to build the top one. Append one dated line to `$D/history.md` (create it on
first run; keep it out of git). When something ships that could move sales, add it to `events.csv` with its date.

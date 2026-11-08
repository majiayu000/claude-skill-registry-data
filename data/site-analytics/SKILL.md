---
name: site-analytics
description: Read real traffic for your websites — who actually came, who came back, which pages, from where — using PostHog as the primary source and Vercel Web Analytics as the fallback, with your own visits and mail-scanner bots filtered out. Use when you ask "how's <site> doing", "check the traffic/visits/analytics for <site>", "did anyone use the page I emailed", "any signups yet", or when wiring the same PostHog snippet onto many small sites. Includes an injectable PostHog block with a ?me=1 self opt-out.
---

# site-analytics — who actually came

## PostHog is the primary read; Vercel is the fallback

Vercel Web Analytics has no IP dimension (it can't drop your own visits) and rotates its
visitor hash daily (it can't say who came back). PostHog does both. Use Vercel (see
`vercel-api`) only for a site with no PostHog block, or for history before you added it.

```bash
export POSTHOG_PERSONAL_API_KEY=... POSTHOG_PROJECT_ID=... POSTHOG_HOST=https://us.posthog.com
python3 posthog_report.py [--days 7] [--host example.com]
```

Per host: persons, returning persons (seen on 2+ distinct days), pageviews, top paths, top
referrers. Test accounts are filtered through HogQL `{filters}`.

## An emailed link's first visitor is a mail scanner, not a person

Corporate mail gateways open every link in an email before the human does, from data-centre
towns (Boydton VA, Ashburn, Dulles, Des Moines, Boardman OR) and Linux desktops. In practice,
33 PostHog "people" on 33 emailed pages, all on send day, all data-centre, was about one real
human; checkout opens on an emailed page were all scanner IPs. Vercel counts all of it (no
IP or geo dimension), so **a Vercel visitor or `va.track` event on an emailed page is not
use.** Before reporting any number on a page that was emailed: in PostHog, drop events whose
`$geoip_city_name` is a data-centre town or whose OS is Linux, then count. Private-Relay
iPhones often carry no city: keep them as "possible", don't drop them.

## One project, many sites: the shared block

- **One PostHog project, one key.** Sites are told apart by `$host`, plus a `site` super
  property set to the repo name.
- **The block:** `posthog_snippet.html` is the source. Replace `__POSTHOG_KEY__` with your
  project's public `phc_` key and `__OPTOUT_HOSTS__` with your hosts. `posthog_inject.py
  --site <repo> file.html` puts it before `</head>` (idempotent); `--print` gives it to a
  generator. Put it in the page's source or generator, never only in the built output.
- **Keep the block free of backslashes and backticks.** It is pasted into Python and JS
  template strings, and a JS template literal silently unescapes `\.`.
- **Your own opt-out:** visit any site with `?me=1`. That sets `site_me` (localStorage +
  cookie) and calls `posthog.opt_out_capturing()`, so the browser is invisible from then on.
  `?me=0` undoes it. Storage is per origin, so do it once per site per browser; to walk every
  site in one click, chain them: `https://site-a.com/?me=1&next=site-b.com,site-c.com`. The
  chain only follows hosts in `__OPTOUT_HOSTS__`.
- **Headless never counts.** The block returns before loading when `navigator.webdriver` is
  true, and posthog-js also drops HeadlessChrome as a bot. To check that capture fires from a
  test browser, `set_config({opt_out_useragent_filter:true})` and intercept the `/i/v0/e/` route.
- **Internal filter** (`test_account_filters`, default on): an internal cohort (person
  property `$internal_or_test_user = true`), your IP (it rotates, so a backstop only), `$host`
  not localhost/127.0.0.1, and `distinct_id` not starting `internal-`. To test ingestion,
  POST to `https://us.i.posthog.com/i/v0/e/` with `distinct_id: internal-...` and
  `$set: {$internal_or_test_user: true}`.

## Reading the numbers honestly

- Report persons and returning persons, not pageviews, as "use".
- Silence in an inbox is not a no; a page someone opened four times on an iPhone over four
  days is use the inbox never shows. A dark (untracked) site can't tell you either way.
- For "where do people drop off on this page", see `session-intent`.

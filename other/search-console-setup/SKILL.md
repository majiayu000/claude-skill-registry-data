---
name: search-console-setup
description: >
  Post-launch: register the LIVE site with Google Search Console and Bing Webmaster
  Tools, verify ownership, submit the sitemap, and turn on IndexNow so Bing/Yandex
  get pinged the moment content changes. For a Cloudflare-hosted Astro site: GSC
  Domain property verified by a Cloudflare DNS TXT record + submit `sitemap-index.xml`;
  Bing the easy way via "Import from Google Search Console" (auto-verifies + pulls the
  sitemap); IndexNow by flipping ONE toggle — Cloudflare Crawler Hints — no key file
  to host. Account creation + the DNS record are human actions the agent drafts but
  can't click. Trigger phrases: "set up Google Search Console", "Search Console",
  "GSC", "Bing Webmaster Tools", "submit my sitemap", "register the site with Google",
  "verify site ownership", "enable IndexNow", "Crawler Hints", "get indexed", "submit
  the website to search engines".
---

# Search Console + Bing + IndexNow

Run this **after the site is live on its production domain** (DNS on Cloudflare,
`production` branch deployed). It makes Google and Bing aware of the site and keeps
Bing's index fresh automatically.

> **Only register the live domain.** `main` and every `*.pages.dev` preview are
> noindexed by the kit's `functions/_middleware.ts`, and after go-live the project
> alias `<project>.pages.dev` 301s to the live domain (once `CANONICAL_URL` is set —
> `new-website/references/CLOUDFLARE_FIRST_DEPLOY.md`, "After go-live"). Do not add
> any `pages.dev` host as a property; they can't be indexed.
>
> **Human-in-the-loop:** creating the Google/Microsoft accounts and adding the DNS
> record are actions only the owner can do (like the GitHub/Cloudflare accounts in
> SETUP.md). The agent drafts the exact TXT value and the sitemap URL; the owner
> pastes/clicks.
>
> **The verification record can go in earlier.** A Domain property is verified by DNS
> alone, so its TXT record (and Bing's CNAME, for the manual route) can be written on
> setup day, before the site is live: the `new-website` setup script writes it, DNS only,
> with the owner's yes (`--record "TXT @ google-site-verification=…"`,
> `new-website/references/CLOUDFLARE_FIRST_DEPLOY.md`, "S"). The owner still copies the
> value from Google and clicks **Verify**; the sitemap waits until the site is live.

> **Console UI labels are localized** — the click paths below are quoted from the
> English UI; if the owner's account language differs, translate the labels for them
> (German: *Property hinzufügen*, *DNS → Einträge → Eintrag hinzufügen*, *Aus der
> Google Search Console importieren*, *Caching → Konfiguration*).

## 1. Google Search Console (Google)

1. Go to https://search.google.com/search-console and sign in.
2. **Add property → "Domain"** (covers http+https, www+apex, all subdomains — the
   right default). Google shows a **TXT record** to add to DNS.
3. **Add the TXT record in Cloudflare** (DNS is on Cloudflare): dashboard → your
   domain → **DNS → Records → Add record** → Type `TXT`, Name `@`, Content = the
   `google-site-verification=…` string Google gave you → Save. Back in GSC click
   **Verify** (propagation is usually seconds on Cloudflare).
   - *Alternative:* a **URL-prefix** property verified by the HTML `<meta>` tag (drop
     it in `Base.astro`'s `<head>`) or an HTML file in `public/`. Domain+TXT is
     preferred — broader coverage, survives scheme/subdomain changes.
4. **Submit the sitemap:** GSC → **Sitemaps** → enter `sitemap-index.xml` → Submit.
   The kit's `@astrojs/sitemap` emits `/sitemap-index.xml` at the site root; confirm it
   loads in a browser first. Google discovers pages from it over the next days.

## 2. Bing Webmaster Tools (Bing + the IndexNow consumers)

Easiest path — **import from Google Search Console** (auto-verifies and pulls the
sitemap, so no second verification dance):

1. Go to https://www.bing.com/webmasters and sign in (Microsoft account).
2. Choose **"Import from Google Search Console" → Continue**, sign in to the Google
   account that owns the GSC property, grant access, **select the site → Import**.
3. Within minutes the site is added, **auto-verified**, and existing sitemaps are
   imported. Confirm under **Sitemaps**; if it didn't carry over, **Submit sitemap →**
   `https://<domain>/sitemap-index.xml`.

*Manual alternative (no Google account):* **Add a site**, verify by the XML file
(place in `public/`), the `<meta>` tag (in `Base.astro`), or a CNAME DNS record, then
submit the sitemap as above.

## 3. IndexNow — one Cloudflare toggle (Crawler Hints)

IndexNow lets the site *push* "this URL changed" to search engines instead of waiting
to be crawled. On a Cloudflare-proxied site you get it for free with **Crawler Hints** —
Cloudflare generates and hosts the IndexNow key and sends the notifications for you, so
**there is nothing to add to the repo**:

1. Cloudflare dashboard → your domain → **Caching → Configuration**.
2. Find **Crawler Hints** and **enable** it.

That's it. Cloudflare now notifies the IndexNow network (Bing, Yandex, Naver,
Seznam) whenever your content is created/updated/deleted. Requires the records to be
**proxied through Cloudflare** (orange cloud) — true for a Cloudflare Pages site on a
Cloudflare-managed domain.

- **Google does NOT use IndexNow** — it relies on its own crawl signals, so the GSC
  sitemap (step 1) is how Google stays current. IndexNow speeds up *Bing & friends*.
- No manual key file: don't add an `indexnow.txt`/key to `public/` — Cloudflare's
  managed key would conflict. (Only self-host a key if you're NOT using Crawler Hints.)

### Also in the Cloudflare dashboard — keep crawlers *allowed*

Newer Cloudflare zones add a **Security → Bots → Control AI crawlers** panel. For the
open, maximally-indexable posture this kit wants, confirm BOTH (the defaults can block).
For the first bullet, `docs/CLOUDFLARE-CHECKLIST.md` in the Croftweaver folder (section 4)
has newer names, read from Cloudflare's own pages on 2026-10-12:

- **Block AI training bots → "Do not block (allow crawlers)"** — Cloudflare's page calls
  the setting **Block AI bots**; the name in your dashboard may differ, and this section's
  names were not re-checked there. The page (last updated 1 July 2026, read 2026-10-11)
  says the setting blocks bots that crawl for AI training, and that from 15 September
  2026 a training block would also cover crawlers that combine search and training
  ([Cloudflare](https://developers.cloudflare.com/bots/additional-configurations/block-ai-bots/)).
  So a block here can be more than the training choice `ai-seo` describes (Step 4): it
  can shut out a crawler that is also used for search. This kit leaves them allowed. The
  same page marks the setting as being retired. Where the dashboard shows **Configure AI
  bot policies** instead, with one setting each for Search, Agent and Training, this kit
  leaves all three on "Allow (do not block)". The page says new domains would start with
  Training and Agent blocked on pages that show ads, so look at what yours shows.
- **Manage your robots.txt → "Disable robots.txt configuration"** — leaves the repo's
  own open `public/robots.txt` authoritative, instead of a Cloudflare-managed file that
  can inject AI-bot `Disallow` rules behind your back.

> **Assistant: offer to do these Cloudflare dashboard clicks for the user** if your
> runtime can drive a browser. The Crawler Hints toggle and the Control AI crawlers
> panel above are dashboard actions, not repo edits — so offering to perform them beats
> just listing steps. Pick the path that matches your runtime:
> - **Claude Code with Claude in Chrome** — offer that extension: ask the user to
>   install it (it's what gives real click/navigate access; plain screen control can
>   only *read* a browser).
> - **Another agent (Codex, Antigravity, …)** — offer your own browser-automation tool
>   if you have one; otherwise walk the user through the clicks.
>
> Whichever path, the shape is the same:
> 1. The user **opens the browser and logs in to Cloudflare themselves** — never handle
>    their credentials or 2FA.
> 2. With their explicit go-ahead and the target zone, navigate to **Caching →
>    Configuration** (Crawler Hints) and **Security → Bots → Control AI crawlers**, read
>    the current values back, and only then set any that don't match the posture above.
>
> If no browser automation is available or the user declines, fall back to walking them
> through the clicks. Never attempt these dashboard changes through blind screen control.

## 4. Confirm it's working

- **GSC:** the **Pages** / **Indexing** report shows URLs moving to "Indexed" over a
  few days; **Sitemaps** shows "Success" with the discovered-URL count.
- **Bing:** **Site Explorer** lists your URLs; **Sitemaps** shows the submitted file.
- **IndexNow:** Bing Webmaster Tools → **IndexNow** (or URL submission) shows
  notifications arriving once Crawler Hints has fired on a content change.

## Scope notes

- This is **search-engine registration**, not on-page SEO — the head/sitemap/schema
  contract is `website-seo-geo`; technical-SEO/Core-Web-Vitals is `seo-audit`; GEO/AI
  answers is `ai-seo`. Run those before this so what gets indexed is already correct.
- GSC is also the free, no-script, no-consent-banner analytics option from the
  `new-website` decision interview (Q5): if the owner only needs "is anyone visiting?",
  this skill is the whole analytics setup.

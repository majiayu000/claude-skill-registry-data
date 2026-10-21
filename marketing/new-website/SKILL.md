---
name: new-website
description: >
  Orchestrates building a NEW website end-to-end, from insights to launch-ready
  and handoff-ready. Self-contained: it runs the stack decision interview,
  sequences the website-* skills + existing marketing skills in order, and
  scaffolds the project from its own templates/ (Astro starter overlay + full
  QA test suite + GDPR privacy draft + owner docs + permission allowlist),
  copying the bundled skill set into the project's skills dir (full copy list
  in §3) so the repo is self-contained for a third party. Default stack
  Astro → GitHub → Cloudflare Pages. Use at the very start of any new site.
  Trigger phrases: "new website", "start a new site", "scaffold a website",
  "spin up a site", "build a new website", "set up a new web project",
  "website starter", "which stack for this site".
---

# New website — orchestrator

The entry point for every new site you build. It **decides the stack**,
**sequences the work**, and **scaffolds a self-contained, handoff-ready repo** from
this skill's `templates/`. Concrete content/SEO/design/QA work is delegated to seven
sibling skills + existing global skills.

Everything needed is bundled here:
- `templates/astro/` — the Astro starter overlay (Base.astro SEO+theme spine,
  `config.ts`, theme tokens, `astro.config`, `tests/` suite, CI, preview-noindex
  function, headers, llms.txt, GDPR privacy page draft). Its `README.md` is the
  assembly manual.
- `templates/SETUP.md` — accounts (GitHub + Cloudflare) + tools + the bootstrap.
- `templates/PUBLISHING.md` — plain-English "how to publish" for the owner
  (`commit`/`push`/`branch` explained + step-by-step per publish model), plus the
  assistant-facing **deploy-time guardrails** (§4).
- `templates/AGENTS.md` + `templates/CLAUDE.md` — the working rules every assistant
  (Codex, Claude Code) follows in the repo: fetch the latest state first, pull request
  instead of a direct push, when a merge is allowed, never invent facts, the new-page
  checklist. `CLAUDE.md` is one line (`@AGENTS.md`), so both tools read the same rules.
- `templates/.gitignore`, `templates/claude/settings.json`, `templates/claude/hooks/git-stand.mjs`
  — git ignore, the permission allowlist, and the Claude Code hook that fetches from
  GitHub at session start (and again after 2 hours) and reports what is new, so
  `AGENTS.md` §1 happens even when the assistant skips it. The settings register the
  hook: copy both, or every session start fails to find the script.
- `templates/positioning.md`, `templates/content-guide.md`, `templates/brand.md` — the per-site docs.
- `references/WEBSITE_ARCHITECTURE.md` (bundled with this skill) — the Cloudflare
  **tier 1/2/3** decision tree + limits (the tiers are also summarized in §1, question 2).

Sibling skills (run in order, each usable on its own):
`website-positioning` · `website-content-guide` · `website-seo-geo` ·
`website-design-system` · `website-testimonials` · `website-qa` ·
`website-review`. `website-positioning-check` is an optional, read-only one-screen
diagnostic for a site that already has pages — run it after the build, or whenever the
offer starts to feel blurred; it is not a pipeline gate. Plus `outgoing-link-audit` — the
pre-launch / monthly external-link
liveness sweep (only relevant once the site links out); `internal-link-audit` — the
internal-linking sweep that finds orphaned + thin pages and suggests where to cross-link
(run after adding a batch of pages); `website-permissions` — install + safely extend the
repo's permission allowlist (fewer prompts, same guardrails); `search-console-setup`
— post-launch GSC + Bing registration + IndexNow; and `website-motion` — an OPTIONAL
polish layer (stat count-up + section-heading reveal) for sites with a long scrolling
homepage, plus the reduced-motion contract and the a11y-gate change that keep motion
from silently hiding content. `website-motion` is never run by default: ask for it.
`website-story` is an OPTIONAL story layer (the home page told as the customer's story:
`STORY.md` + a seven-section home page map); it is offered once at §2a, right after
positioning, and never runs unasked. `website-scorecard` is an OPTIONAL public scorecard
(a section that shows what the site's own test gate checked, dated, plus the owner's
Lighthouse scores); it runs only when the owner asks for it. `website-tagline` is an
OPTIONAL skill for the short line under the logo (it starts from the purpose in
`POSITIONING.md`, shows the owner six to eight lines and lets them pick one →
`TAGLINE.md` + `SITE.tagline`); it too runs only when the owner asks for it.
`website-brand-kit` is OPTIONAL help with colours and a logo for an owner who is not a
designer (three prompts for the design tool she likes, then a checked install of the
palette and the seven icon files); the owner is asked once at §2b, right after
positioning and the story, and it never runs unasked.
`website-team-setup` is the other on-demand skill — run it once when a **second person**
joins the repo (invite collaborators, repo settings, prove CI triggers, block direct
pushes to `main`, connect Cloudflare Pages without the known traps, set the rights level
in `AGENTS.md`); a single owner never needs it.
A private repo gets 2 000 free CI minutes a month on GitHub Free (about 400 runs of the kit's
`ci.yml`); past that, jobs stop with a message that reads like a failed payment. Tell the
owner to check **Budgets and alerts** for an Actions budget (`website-team-setup` §3b has
the steps).

## 1. Decision interview (answer before any code)

**Conduct the interview — and ALL user-facing guidance throughout this pipeline
(explanations, the §3a link-sweep question, the §4 preview-vs-live announcements,
error walk-throughs) — in the language the user writes in.** A German owner gets
the whole journey in German; the skill files themselves stay English. The
verbatim message templates below are content specs, not required English wording.

Default house stack: **Astro (static) → GitHub → Cloudflare Pages**. Six questions
decide everything downstream — ask them in order, offer the examples so a
non-expert can answer, and record the answers in the project `README.md`.

1. **Pages + content types — what does the sitemap look like?**
   *Decides: plain pages vs Content Collections.*
   - A handful of fixed pages (home, services, about, contact, imprint — ≤ ~15)
     → plain `.astro` pages. Example: a small-business brochure site.
   - Anything that repeats with the same shape — blog posts, events, case
     studies, team members → Astro **Content Collections** (one schema, one
     template, n entries) + the `Base` layout. Example: an event archive where
     every event has date/speaker/location.
   - Mixing both is normal: flat pages + one collection.

2. **Any dynamic/backend behaviour — what must a server actually do?**
   *Decides: the Cloudflare tier. Pick the LOWEST tier that fits — going higher
   is the classic mistake. Tier tree + limits: `references/WEBSITE_ARCHITECTURE.md`.*
   - Visitors only read; contact is an email link, or a contact form that
     opens the visitor's own mail program → **Tier 1 static** (~90% of sites).
     A contact form: run **`website-contact-form`**, our suggestion (no server,
     no account, no setting).
   - Exactly one small server task — site search, hiding a third-party API
     key, one live widget (e.g. a next-event box fed by an API), a form that
     must send through a server → **Tier 2** (one Pages Function or server
     island). No skill builds such a form.
   - State per user — accounts/login, a database, checkout, user-generated
     content → **Tier 3** (SSR + D1). Rare; challenge the requirement first.

3. **Who edits content after launch?**
   *Decides: CMS or not.*
   - The owner/Claude editing files in git → **no CMS** (default; markdown +
     redeploy is the workflow).
   - A non-technical person (client, co-organizer writing posts) →
     **Keystatic** (git-based, no separate backend). Can be added later —
     don't install it speculatively. When chosen, run **`keystatic-setup`**
     (local mode; the GitHub cloud-mode upgrade is documented there).

4. **One language or several?**
   *Decides: i18n routing from day 1 or never.*
   - One language (German-only counts) → skip i18n entirely.
   - Two+ **at launch** (e.g. a DE+EN consultancy site) → run
     **`astro-i18n-setup`** (Astro i18n: clean default locale + prefixed others,
     self-referencing hreflang + `x-default`, sitemap alternates, language switcher,
     per-locale test harness).
   - **Multilingual, but building one language first?** Fine — keep the default locale
     **unprefixed** from day 1, ship/test the primary language, then run
     **`astro-i18n-setup`** to add the second locale when translations are ready. Because
     the default stays at `/`, that's additive, not a breaking retrofit (skill →
     *Phased rollout*).
   - "Maybe English someday" → treat as one language now; the unprefixed default keeps a
     future second locale additive. **The only costly change is later moving the default
     off `/`** (e.g. `/` → `/en/`).

4a. **What language should the content actually be written in?**
    *Decides: the copy language — a separate decision from Q4's routing question above.*
    Answering "one language" in Q4 does **not** mean English. The starter defaults to
    English (`templates/astro/src/config.ts` ships `locale: 'en'`, and the placeholder
    homepage copy is English prose) — say so explicitly if you want German, or another
    language, instead. **German-only is a completely valid, common answer** here, not
    just "English, obviously, unless multilingual."

5. **Analytics — will anyone act on the numbers? (optional)**
   - Just "is anyone visiting?" → **Google Search Console** (free, no script, no consent
     banner) is enough for traffic from Google search; it does not show which other
     sites send visitors, and Cloudflare's docs list no referrer view for the Free plan.
     Cloudflare also counts the domain's traffic at its own servers, with nothing added
     to the pages: https://dash.cloudflare.com → your domain → **Analytics** →
     **Traffic**. On the Free plan that is requests, bandwidth, unique visitors and up
     to five top countries for at least the last 30 days, bots included; page views, and
     filtering by referrer, need a paid plan
     (https://developers.cloudflare.com/analytics/account-and-zone-analytics/zone-analytics/,
     checked October 2026). It counts requests and visitors, not events such as an
     enquiry, so it cannot give the enquiry count. Cloudflare's separate "Web Analytics"
     cannot either: its FAQ answers custom events with "Not yet"
     (https://developers.cloudflare.com/web-analytics/faq/, checked October 2026). It is
     also a script in the visitor's browser, so keep it off
     (`docs/CLOUDFLARE-CHECKLIST.md`, section 3, "Cloudflare Web Analytics: Off").
     The starter ships with its own analytics off
     (`USE_ANALYTICS = false` in `src/config.ts`, no analytics host in
     `public/_headers`), so leave both as they are and delete the analytics paragraphs
     of section 3 of the privacy page.
   - "Which sources bring enquiries?" or other real decisions from traffic data
     (campaigns, content strategy) → **Plausible** (cookieless; whether it needs a
     consent banner: the last point of this question). In its installer, untick the
     optional measurements (outbound links, file downloads, form submissions)
     unless you keep the privacy page's slot sentence for each one you leave ticked.
     Plausible's menus hide the pages the owner needs, so give each one as a link,
     with `scriptHost` and the site's domain (as added in Plausible) filled in: the
     installer and the script id at `<scriptHost>/<domain>/installation`, the goals at
     `<scriptHost>/<domain>/settings/goals`, a new site at `<scriptHost>/sites/new`.
     Seen on a self-hosted Community Edition instance on 2026-10-16: the owner added
     the goal on that goals page; the other two sent a signed-out visitor to the
     login page, where an unknown path gives 404. On Plausible Cloud (`scriptHost`
     `https://plausible.io`) the same paths are expected, not checked. If a link
     gives 404, say so, and find the page in Plausible's own menus with the owner.
     Ask whether the owner already runs a Plausible server. If not, the usual case,
     recommend the **paid cloud version** (from **€9/mo** —
     https://plausible.io/#pricing), so the owner runs no server; point at a
     **self-hosted** instance only if one already exists. The enquiry count (the
     "Email Tap" paragraph below) needs Plausible: Cloudflare's counts have no events.
     **Switch it on**, since the starter ships with analytics off: in `src/config.ts`
     set `USE_ANALYTICS = true` and fill in `scriptHost` and `scriptId`, then add the
     same host to `script-src` and `connect-src` in `public/_headers` (the comments in
     both files say how). Keep the privacy page's analytics paragraphs and fill their
     slots. Run `bash tests/check_analytics_gate.sh` once to check the builds and the
     headers (a site's CI does not run it). Without the switch the live site counts
     nothing, and nothing says so.
     **The enquiry count comes with it.** Each click on an email address, and each
     press of the contact form's button that passes its checks, sends one "Email Tap"
     event (with the page and the referrer, as every event; no address, nothing typed).
     On the site's goals page in Plausible (`<scriptHost>/<domain>/settings/goals`,
     under Settings > Goals; open the address directly, owners find the page hard to reach from the dashboard), add a goal of type "Custom event"
     named exactly `Email Tap` **before launch**: Plausible's documentation says an
     event shows only once its goal exists and earlier ones are not counted. Once a
     test tap has reached Plausible, the goals page offers `Email Tap` to add in one
     click. That rules out a typo in the name (seen on a self-hosted instance).
     To see a test tap, choose Today or Realtime: Plausible's "Last 7, 28, 30 and 91 days" views
     end yesterday (checked on self-hosted version 3.2.1; the cloud version may differ).
     On a site just added to Plausible, a tap in its first
     minute or so may not be kept; tap again a few minutes later. Filtered
     by that goal, the dashboard shows which sources and pages bring enquiries. It
     counts visitors who asked to write an email; whether their mail program opened,
     and whether they sent the mail, the site never learns.
     **Script or server mode.** With analytics switched on, Plausible by default runs as a
     script in the browser (`ANALYTICS.mode: 'script'`). Offer **server mode** (`'server'`) to an owner who
     wants no analytics code on the visitor's device: the site's Cloudflare Function
     sends each page view and email tap to Plausible itself, so no script loads and
     nothing is read from or written to the device. It loses scroll depth, engaged
     time, the optional measurements and the exclusion of the owner's own visits (`plausible_ignore`), the contact form's button is not counted
     (only email links are), and a visitor can no longer opt out by blocking a script.
     Its numbers differ from the script's: it counts visitors who block scripts, but not
     a page a browser prefetched or prerendered before the visitor opened it, and not
     visitors whose browser sends no Fetch Metadata headers (Safari before 16.4, some
     in-app browsers); a tap on the email link shows those visitors a page with the
     address written as "name [at] domain" instead of opening their mail program.
     It forwards the visitor's IP to Plausible, as the script's request carries it;
     EDPB Guidelines 2/2023 (paras 54–56) say IP-based tracking can itself fall under
     the ePrivacy rule, so it is a stronger position, not a way out of a review. It
     needs two Production variables in Cloudflare (`PLAUSIBLE_HOST`,
     `PLAUSIBLE_DOMAIN`). `PLAUSIBLE_DOMAIN` must equal the site's name in Plausible, or Plausible
     answers 202 and drops every event without an error. The Function counts nothing on a `*.pages.dev`
     address, so test on a custom domain. The starter README, step 4, has the setup and a
     list of what to check when nothing arrives; an existing site also takes the
     site-owned files that step names, which `whats-new` does not report, or it keeps
     counting with the script too. It works with self-hosted
     Plausible (tried on Community Edition 3.2.1) and, per Plausible's documentation,
     with the cloud version (not tried there with a real site). Counting uses the
     Functions quota the site already uses (free plan: 100,000 requests a day); past
     it, with "Fail open" (what the deploy guide sets; Cloudflare names no default, so check it), Cloudflare serves the site
     without the Function until midnight UTC, so counting stops and email links do not
     open the mail program until then ("Fail closed" shows an error page for the whole
     site instead; `references/CLOUDFLARE_FIRST_DEPLOY.md`).
   - Prefer cookieless tools over Google Analytics, which would pull in a
     cookie-consent banner — for German-market sites the statute behind that
     banner is § 25 TDDDG (formerly TTDSG). Third-party additions put the
     banner-free position at risk by different routes: a YouTube iframe triggers § 25
     itself (device storage/readout), while remote Google Fonts change the
     answer via the GDPR instead (unconsented IP disclosure — LG München I,
     3 O 17493/20; self-host fonts, as this starter does). Any analytics script is gated to the production branch only
     (server mode: the Production variables, on the live domain only). The
     privacy page must match whatever is chosen here, script or server mode included.
   - **When the site needs no consent banner.** Tell the owner plainly: a site built
     with this kit needs no consent banner in the EU, Germany, Switzerland or California
     as long as it runs no analytics script: nothing reaches the visitor's browser that
     the page itself does not need. For the starter's own
     analytics that means leaving `USE_ANALYTICS = false` in `src/config.ts`, as it ships
     (the first point of this question; the other things that break the no-banner case
     are listed below); run `bash tests/check_analytics_gate.sh` once to check that no
     build writes the script (a site's CI does not run it). Plausible runs as a small script in the visitor's
     browser. With it, running without a banner is a defensible position in the EU,
     Germany, Switzerland and California, not a settled one; to be sure, ask a lawyer.
     Server mode runs no script, but it is not banner-free by definition either: the
     visitor's IP still reaches Plausible through the site's Function, and EDPB
     Guidelines 2/2023 (paras 54–56) say IP-based tracking can fall under the same rule;
     the same headers say what changes in server mode.
     For the EU and Germany, the headers of `privacy.astro` and `_datenschutz.astro` set
     out the sources on both sides and ask you to record who accepted the position. In
     Switzerland and California the position rests on the privacy page informing
     visitors. Switzerland (Art. 45c FMG) asks that visitors are told about the
     processing and its purpose, and that they may refuse it; California's CalOPPA asks
     the page to say whether third parties may collect personal information across
     websites through the site, and how the site answers "Do Not Track" if it collects
     such information itself. Section 3 of `privacy.astro` says both;
     `_datenschutz.astro` says the Swiss part. California's CCPA applies only above its
     thresholds (USD 26,625,000 annual gross revenue from 1 January 2025, adjusted every
     two years; or buying, selling or sharing the personal information of 100,000 or
     more California consumers or households; or half the revenue from selling or
     sharing it). A site without a banner still needs its privacy page, an imprint in
     Germany and Austria, and a processing contract with Cloudflare, and with Plausible
     if it runs on Plausible Cloud. What breaks the no-banner case: any Cloudflare
     feature that section 3 of `docs/CLOUDFLARE-CHECKLIST.md` (in the Croftweaver
     folder) asks you to switch off, the script monitor among them; a YouTube embed;
     remote Google Fonts; another analytics tool. A theme toggle that stores the
     visitor's choice needs a look too (the same headers say why). Not legal advice.

6. **Domain + how do changes go live? (publish model)**
   *Decides: the publish workflow — a safety-vs-simplicity trade-off. **Offer both, explain
   them, let the owner choose**; recommend two-stage. Record the choice in the README.*
   - New domain or subdomain of an existing site? (Affects canonical URLs and whether
     existing SEO authority carries over.) DNS moves to Cloudflare.
   - **Two-stage — recommended (default).** `main` is an **unlisted, noindexed preview**
     (`*.pages.dev` — noindexed, but public-by-URL, not access-controlled); `production` is
     the **live** site. The owner pushes to `main`, checks
     the preview link, then runs **`npm run ship`** to publish. A mistake never reaches the
     live domain. *Scaffold adds:* the `production` branch, the `_middleware.ts` noindex
     guard, and the `ship` script.
   - **Single-stage — simplest.** One branch — `main` is live, so every push goes straight
     to the public site. Fewer moving parts, no safety net. Pick this only for a low-stakes
     site whose owner is fine with "save = instantly public." **Note:** the `_middleware.ts`
     noindex guard de-indexes every `*.pages.dev` host, so a single-stage site is invisible
     to Google until a **custom domain** is attached — say this when recommending it.
   - **Don't assume git fluency.** Whichever they choose, hand them
     `templates/PUBLISHING.md` (plain-English `commit` / `push` / `branch` + the exact
     step-by-step to publish) and walk the **first** publish through with them.

Plain hand-written HTML (static `.html` files, no build step) is a legacy anti-pattern — use Astro.

## 2. The pipeline (the order to use the skills)

| # | Step | Skill / source |
|---|---|---|
| 1 | Insights: ICP, voice-of-customer, competitor scan | `customer-research` |
| 2 | Positioning: what you offer, for whom, market category → `POSITIONING.md` (Dunford) | **`website-positioning`** |
| 2a | Optional: the home page as the customer's story → `STORY.md` (offered once, §2a; positioning stays the source of truth) | `website-story` |
| 2b | Optional: colours and a logo (asked once, §2b; her choices are made here, the install waits for the green baseline of §3 step 5) | `website-brand-kit` |
| 3 | Tone of Voice, EEAT, page inventory → `CONTENT_GUIDE.md` + `BRAND.md` (its palette and logo come from step 2b, where the owner brought or chose them) | **`website-content-guide`** |
| 4 | Pages, clean URLs, nav, internal links | `site-architecture` |
| 5 | Decision interview + scaffold the repo | **this skill** §1, §3 |
| 6 | Build: mobile graphics, dark mode, theme tokens | **`website-design-system`** |
| 6 | Build: head metadata within limits, schema, llms.txt | **`website-seo-geo`** (+ `schema-markup`, `ai-seo`) |
| 6 | Build: per-page OG share cards (`npm run og` → 1200×630 ≤300 KB, tested) | **`og-images`** |
| 6 | Build: testimonials / Review schema from one data file (if the site has quotes) | **`website-testimonials`** |
| 7 | QA: a11y (light+dark) / seo / navigation / anchors / orphans / images / tone / positioning / placeholders / email / links | **`website-qa`** |
| 8 | Performance: Lighthouse / PageSpeed for FCP & LCP | **`website-qa`** perf section (+ `seo-audit`) |
| 9 | **Double-Knuth review** (correctness + cross-file consistency) | **`website-review`** |
| 10 | Outgoing-link liveness sweep — **only if the site links out** (see §3a) | **`outgoing-link-audit`** |
| 10b | Internal-link sweep — orphaned + thin pages (run if the site grew past a handful of pages) | **`internal-link-audit`** |
| 11 | Launch & handoff: schema/sitemap/robots, deploy, hand over | **this skill** §4 |
| 12 | Post-launch: register with Google Search Console + Bing, submit sitemap, enable IndexNow | **`search-console-setup`** |
| 13 | Post-launch: claim Google Business Profile + Bing Places, verify `sameAs` profiles resolve — **only if the site is a claimable entity** (see §4a) | **`business-listings-setup`** |
| 14 | Post-launch: ask once for a "Built with Croftweaver" credit in the footer — a request, never a condition (see §4b) | **this skill** §4b |

Work out **positioning** (step 2) *before* any content or SEO — it decides what the
copy is even trying to say. Build the Content Guide (step 3) *before* writing page
copy; positioning and voice are inputs to everything downstream, not an afterthought.

The build is **test-driven, not test-after**: the suite is green from commit 1,
and steps 6–7 run as a loop per page (red → green → commit, see §3 step 5 and
`website-qa` §1b). Step 7 in the table is the *final full-suite gate*, not the
first time tests run.

## 2a. Story layer — offer once, right after positioning

`website-story` is optional and the owner has usually never heard of it, so explain
before asking. Once `POSITIONING.md` is filled (step 2) and before the content guide
(step 3):

1. Read **"The offer"** in `website-story/SKILL.md` and say it in the language the
   owner writes in (it explains the idea in plain words: the visitor as the hero, the
   brand as the guide, a one-liner, a three-step plan, one repeated call to action,
   positioning unchanged). Do not paraphrase it into jargon.
2. Ask once — a structured user-input tool if the platform offers one (Claude Code's
   **`AskUserQuestion`**), otherwise in chat — with two options: **Yes, build the home
   page as a story** / **No, standard home page (default)**.
3. **Yes** → run `website-story` now, before step 3, so `CONTENT_GUIDE.md`'s home row
   and `copywriting` read `STORY.md`.
4. **No, or no answer** → say nothing more about it. The skill still travels with the
   repo (§3 step 3), so it can be run later whenever the owner asks.
5. **Record the answer either way** ("home page: story-led, see STORY.md" or "home page:
   standard, story layer declined") with the decision-interview answers when §3 writes
   the project README, so a later session knows the offer was made and does not ask
   again.

Ask exactly once per build. Never run it unasked.

## 2b. Colours and logo — ask once, after positioning and the story

`website-brand-kit` is optional. It is a plain question, not a pitch. Once
`POSITIONING.md` is filled (and §2a is answered) and before the content guide (step 3):

1. Read **"The question"** in `website-brand-kit/SKILL.md` and ask it, as it stands
   there, in the language the owner writes in.
2. **She has a part and wants it used** → note the path of her logo file, which must
   be an SVG, or her colours as hex values. No prompt is written for that part. Her own
   colours still go through the skill's check (its §3 step 3) now.
3. **She wants help with a part** → run now, before step 3, the steps before §6 that
   `website-brand-kit` §0's table names for her answer, and only those (help with
   colours alone does not start the logo steps, and the other way round), so the
   palette exists when `BRAND.md`'s "Brand in one line" is written. These steps are a
   conversation: nothing is written into a project yet (there is none).
4. **She lacks a part and wants no help with it** → say nothing more about it. The site
   keeps the starter's colours and the scaffold's placeholder icons for that part. The
   skill still travels with the repo (§3 step 3).
5. **Record the answers either way** with the decision-interview answers (what she has,
   what she wanted help with, the path of her own logo file or of her package, and,
   where she took the help, the palette and the variation she picked), so a later
   session knows the question was asked and does not ask again. Until §3 step 4 writes
   them into the project they live in this conversation: do that step in the same
   session, or write them into a note in the folder you are working in.
6. **The install comes later:** §3 step 5, on the green baseline.

Ask exactly once per build. Never run it unasked.

## 3. Scaffold the project (handoff-ready)

**Prerequisites (one-time).** Walk the user through `templates/SETUP.md` if needed —
Node/git/gh/wrangler + image tools, a **private GitHub** account, a **Cloudflare**
account. The accounts are a human action the agent cannot do. When the owner sets up
GitHub, tell them plainly that the account and the website in it are theirs, and recommend
two-factor sign-in with a passkey to keep others out (`SETUP.md` §1 has the link); for
Cloudflare, which decides whether the site is online, the same with a security key or the
device's fingerprint or face unlock. Recommend, never require: GitHub makes it mandatory only
for some accounts, and Cloudflare leaves it optional unless an account's administrator
enforces it for members.

Assemble the project at `<site>/` so it travels without any global setup. `<site>` is a new
folder inside the owner's websites folder, which is the folder this session was opened in
(never that folder itself). Before step 0, unless the owner has already confirmed it in this
session, say which folder you are in and ask whether it is their websites folder. If it is
not, or it already holds a site (an `astro.config.*` or `index.html` file) or is the toolkit
folder (it has `skills/new-website/SKILL.md`), ask which folder is their websites folder
instead. Start step 0 from the websites folder, and once `<site>` exists, tell the owner its
full path (the output of `pwd` inside it):

0. **Git first, before any code:**
   ```bash
   # Resolve where the suite is installed (the cp SOURCE). Per tool:
   #   ~/.claude/skills = Claude Code · ~/.agents/skills = Codex · ~/.gemini/config/skills = Antigravity
   # Honour an explicit $SKILLS_ROOT; else auto-detect. First the folder this very skill was
   # loaded from: in the first candidate of the loop below, Claude Code puts this skill's
   # own folder where the name in braces stands, which also finds the suite when it is
   # installed as a plugin and so sits in none of the three folders above. Claude Code
   # replaces the name only where nothing follows it inside the braces, so the line before
   # the loop reaches every assistant as written: where the name was left alone, it gives
   # the shell an empty value for it instead of an unset variable, the candidate reads
   # "/..", and the loop passes over it. Then Claude Code → Antigravity → Codex
   # (Claude is the default/primary), and last the suite installed as a Codex plugin, in
   # Codex's folder (CODEX_HOME or ~/.codex, written as the shell names it after cd, as
   # SKILLS_ROOT is, so the two compare). An update leaves one version there; should there
   # be more, the last in name order is taken (0.9.0 sorts after 0.33.0). It is found with
   # `find`, because a pattern that matches nothing stops zsh with an error, and a failed
   # search leaves it empty, so the candidate reads "/.." as well. On a machine with
   # more than one installed, set it yourself — e.g. `export SKILLS_ROOT=~/.agents/skills` (Codex) or
   # `~/.gemini/config/skills` (Antigravity); Antigravity workspace installs use
   # `export SKILLS_ROOT="$PWD/.agents/skills"`.
   codex_home="$(CDPATH= cd -- "${CODEX_HOME:-$HOME/.codex}" 2>/dev/null && pwd)" || codex_home="${CODEX_HOME:-$HOME/.codex}"
   if [ -z "${SKILLS_ROOT:-}" ]; then
     SKILLS_ROOT="$HOME/.claude/skills"
     : "${CLAUDE_SKILL_DIR:=}"
     codex_plugin="$(find "$codex_home/plugins/cache/croftweaver/croftweaver" -mindepth 2 -maxdepth 2 -type d -name skills 2>/dev/null | sort | tail -n 1)" || codex_plugin=
     for d in "${CLAUDE_SKILL_DIR}/.." "$HOME/.claude/skills" "$HOME/.gemini/config/skills" "$HOME/.agents/skills" "${codex_plugin:-/..}"; do
       [ "$d" != /.. ] && [ -d "$d/new-website" ] && SKILLS_ROOT="$(cd "$d" && pwd)" && break
     done
   fi
   # Where bundled skills go IN the generated project (the cp DESTINATION). Claude default
   # (.claude/skills). Codex and Antigravity read repo-scoped skills from .agents/skills, so
   # derive that when the suite was installed through either of them. Force it with:
   # export PROJECT_SKILLS_DIR=.agents/skills
   if [ -z "${PROJECT_SKILLS_DIR:-}" ]; then
     case "$SKILLS_ROOT" in
       "$HOME/.agents/skills"*|"$HOME/.gemini/config/skills"*|*/.agents/skills*|"$codex_home"/plugins/*) PROJECT_SKILLS_DIR=".agents/skills" ;;
       *) PROJECT_SKILLS_DIR=".claude/skills" ;;
     esac
   fi
   mkdir <site> && cd <site> && git init
   cp "$SKILLS_ROOT"/new-website/templates/.gitignore .
   git add .gitignore && git commit -m "chore: init repo with .gitignore"
   ```
1. **Scaffold + overlay:** `npm create astro@latest .` (Empty, TS strict), then copy
   the `templates/astro/` overlay (`src/`, `tests/`, `public/`, `functions/`,
   `scripts/`, `.github/`, `.nvmrc`, `.gitattributes`, root configs — see `templates/astro/README.md`
   for exact steps and npm deps). Set the real domain in `astro.config.mjs` (`site:`)
   and `src/config.ts`. **Set `SITE.locale` in `src/config.ts` to match the interview's
   Q4a content-language answer** (and `lang` in `Base.astro` too, if not running
   `astro-i18n-setup`). **`'de'` flips the footer's privacy link to `/datenschutz`** —
   do the privacy→datenschutz swap in the SAME step (rename the in-repo
   draft `src/pages/_datenschutz.astro` per its header: page file,
   `tests/_helpers.ts` PAGES, `public/llms.txt`, `OWN_CARD_EXEMPT`,
   `POSITIONING_EXEMPT` + `UNFILLED_UNTIL_LAUNCH` in the specs) or every
   intermediate `npm test` fails navigation on the footer link.
   The overlay ships `locale: 'en'`, and leaving that default in
   place for a German-content (or other non-English) site is exactly the silent-default
   bug Q4a exists to catch. **Astro needs Node ≥22.12** — the overlay's `.nvmrc` pins
   24 for local + Cloudflare Pages builds.
2. **Permissions + working rules.** Copy the setup guide into the project (all tools), then — **Claude Code
   only** — copy the allowlist so routine `npm`/`astro`/`playwright`/`git commit` calls don't
   prompt (it blocks `rm -rf`, force pushes, `wrangler … delete`, `gh repo delete`: Claude Code
   refuses them, and the owner runs one by hand if needed):
   ```bash
   cp "$SKILLS_ROOT"/new-website/templates/SETUP.md .          # all tools — receiving party can set up too
   cp "$SKILLS_ROOT"/new-website/templates/PUBLISHING.md .     # owner "how to publish" + assistant deploy guardrails
   cp "$SKILLS_ROOT"/new-website/templates/AGENTS.md .         # working rules for every assistant (Codex + Claude)
   cp "$SKILLS_ROOT"/new-website/templates/CLAUDE.md .         # one line: @AGENTS.md
   # Claude Code only:
   mkdir -p .claude/hooks
   cp "$SKILLS_ROOT"/new-website/templates/claude/settings.json .claude/settings.json
   cp "$SKILLS_ROOT"/new-website/templates/claude/hooks/git-stand.mjs .claude/hooks/   # sync hook the settings register
   ```
   *Codex / Antigravity: skip the `.claude/settings.json` copy — it's Claude Code-specific.
   Use their own approval systems instead (Codex: `AGENTS.md` + Codex rules/config;
   Antigravity: its sandbox approval model).* For Claude's allow/deny model and how to extend
   it safely when a prompt keeps recurring, use **`website-permissions`**.
   **Fill `AGENTS.md` now**, per the scaffold note at its top: site name, live URL, the
   preview URL (two-stage: `main.<project>.pages.dev`; single-stage: "pull-request
   previews only, `<branch>.<project>.pages.dev`" — `main` is live there; where Cloudflare
   gives the project an address other than its name, use that address, which the project's
   page and the setup script's report name, so update it once the project exists), `[TITLE_SUFFIX]` = the
   ` | {SITE.name}` string `Base.astro` appends, `[SUFFIX_LENGTH]` = its length, and
   `[TITLE_MAX]` = 60 minus that length; keep ONE publish-model block in its §2 (the
   interview's Q6 answer) and delete the other. §5 (collaborators, rights level, merge
   rule, who publishes) ships with single-owner defaults, not slots; `website-team-setup`
   rewrites it when a team forms. `AGENTS.md` stays English for every owner, like the
   skills: agents read it, and its Language rule has them reply in the person's
   language. Only the human-facing `PUBLISHING.md` gets translated (see §4).
3. **Skills travel with the repo** — copy the twenty-seven always-on skills in, plus any
   conditional setup skills selected by the interview, so the handoffs resolve for the
   receiving party. "Always-on" here means always **copied** into the project, not
   necessarily always **run**: `business-listings-setup` travels with every repo but
   only executes when §4a's gate says the site is a claimable entity — it still needs
   to be in the repo so a later session can run it once that's true. The always-on set is the
   seven core `website-*` siblings, `website-positioning-check` (always copied, optional to run),
   the three SEO-depth skills they delegate to — `ai-seo`, `schema-markup`,
   `seo-audit` — `site-architecture` (IA), the three
   marketing skills the pipeline delegates to — `customer-research`, `copywriting`,
   `image` — plus `outgoing-link-audit` (external link sweep), `internal-link-audit`
   (orphan/thin-page sweep), `og-images` (per-page share cards),
   `website-permissions` (allowlist),
   `search-console-setup` (post-launch GSC/Bing/IndexNow),
   `business-listings-setup` (post-launch Business Profile/Bing Places/
   `sameAs` — gated per §4a), `website-motion` (optional polish — copied so
   the recipient can opt in later; it never runs on its own), `website-story`
   (optional story layer — same rule: copied, never runs unasked; offered once at §2a),
   `website-scorecard` (optional public scorecard — same rule: copied, never runs
   unasked), `website-brand-kit` (optional colours and logo — same rule: copied, never
   runs unasked; asked about once at §2b), `website-tagline` (optional line under the logo — same rule: copied,
   never runs unasked), and `website-team-setup` (copied so the day a second person joins, the session that
   sets up the team finds it; it never runs on its own either):
   `$SKILLS_ROOT` entries are often symlinks (e.g. a `make install` checkout
   symlinks each skill from this suite repo) — use `cp -RL` to dereference
   them, not `cp -R`, or the copy ships broken symlinks pointing back at the
   developer's own machine instead of a self-contained skill directory:
   ```bash
   mkdir -p "$PROJECT_SKILLS_DIR"
   cp -RL "$SKILLS_ROOT"/website-positioning \
         "$SKILLS_ROOT"/website-positioning-check \
         "$SKILLS_ROOT"/website-content-guide \
         "$SKILLS_ROOT"/website-seo-geo \
         "$SKILLS_ROOT"/website-design-system \
         "$SKILLS_ROOT"/website-testimonials \
         "$SKILLS_ROOT"/website-qa \
         "$SKILLS_ROOT"/website-review \
         "$SKILLS_ROOT"/ai-seo \
         "$SKILLS_ROOT"/schema-markup \
         "$SKILLS_ROOT"/seo-audit \
         "$SKILLS_ROOT"/site-architecture \
         "$SKILLS_ROOT"/customer-research \
         "$SKILLS_ROOT"/copywriting \
         "$SKILLS_ROOT"/image \
         "$SKILLS_ROOT"/outgoing-link-audit \
         "$SKILLS_ROOT"/internal-link-audit \
         "$SKILLS_ROOT"/og-images \
         "$SKILLS_ROOT"/website-permissions \
         "$SKILLS_ROOT"/search-console-setup \
         "$SKILLS_ROOT"/business-listings-setup \
         "$SKILLS_ROOT"/website-motion \
         "$SKILLS_ROOT"/website-story \
         "$SKILLS_ROOT"/website-scorecard \
         "$SKILLS_ROOT"/website-brand-kit \
         "$SKILLS_ROOT"/website-tagline \
         "$SKILLS_ROOT"/website-team-setup \
         "$PROJECT_SKILLS_DIR"/
   # The brand kit's scripts/tests is the toolkit's own test suite (about 1.7 MB). No site
   # runs it, so it stays behind; whats-new.sh --refresh leaves out the same folder.
   rm -rf "$PROJECT_SKILLS_DIR"/website-brand-kit/scripts/tests
   ```
   The global copies stay the updateable source of truth; the project copies are
   the frozen handoff set.

   **Conditional setup skills** — run the matching line ONLY when the interview
   selected it (they don't ship with a declared one-language, CMS-free site without a
   contact form;
   a multilingual-PHASED site is single-locale at scaffold time and still
   gets astro-i18n-setup):
   ```bash
   # If Q3 = "non-technical editor" (Keystatic):
   cp -RL "$SKILLS_ROOT"/keystatic-setup "$PROJECT_SKILLS_DIR"/
   # If Q4 = "2+ languages at launch" OR "multilingual, one language first"
   # (phased rollout): the phased site NEEDS the skill vendored from day 1 —
   # its Phase 2 instruction is "run astro-i18n-setup when translations are
   # ready", which can't resolve if the skill was never copied.
   cp -RL "$SKILLS_ROOT"/astro-i18n-setup "$PROJECT_SKILLS_DIR"/
   # If Q2 = a contact form:
   cp -RL "$SKILLS_ROOT"/website-contact-form "$PROJECT_SKILLS_DIR"/
   ```

   **Sanity check** (always, once all copying above — the primary batch AND
   any conditional skills — is complete) — confirm nothing was copied as a
   symlink:
   ```bash
   find "$PROJECT_SKILLS_DIR" -maxdepth 1 -type l
   # Must print nothing. Any output means a skill copied as a symlink, not a
   # real directory — the handoff repo would ship broken links back to this
   # machine. Re-run the copy for the listed name(s) with cp -RL.
   ```

   **Stamp the copies** (always, after ALL skills are copied) — records which suite
   state they came from, so `make whats-new PROJECT=<site-dir>` (the site's full path) in the suite repo can later
   report which bundled skills have upstream updates:
   ```bash
   # The suite's scripts/whats-new.sh is the ONLY writer of the stamp format. Resolve
   # the suite clone via the symlink and verify it really is the suite — a copied
   # (non-symlink) install sitting inside some other git repo must NOT stamp that
   # repo's HEAD.
   SUITE_SRC="$(readlink "$SKILLS_ROOT/new-website" 2>/dev/null || echo "$SKILLS_ROOT/new-website")"
   SUITE_REPO="$(git -C "$SUITE_SRC" rev-parse --show-toplevel 2>/dev/null || true)"
   if [ -n "$SUITE_REPO" ] && [ -f "$SUITE_REPO/scripts/whats-new.sh" ] \
      && [ -d "$SUITE_REPO/skills/new-website" ]; then
     bash "$SUITE_REPO/scripts/whats-new.sh" --stamp "$PROJECT_SKILLS_DIR"
     # Also stamp the FROZEN template copies (tests/*.spec.ts, CONTENT_GUIDE.md):
     # whats-new reports their upstream drift separately — --refresh never touches
     # them, they're merged by hand (they may carry site edits like the PAGES list).
     bash "$SUITE_REPO/scripts/whats-new.sh" --stamp-tests tests
   else
     # No usable suite clone (zip/copy install): record that the baseline is unknown.
     # whats-new can't report for this project until re-stamped from a real clone.
     printf 'suite_commit: unknown\ncopied: %s\n' "$(date +%Y-%m-%d)" \
       > "$PROJECT_SKILLS_DIR"/SUITE-VERSION
   fi
   ```
4. **Docs** — copy `templates/positioning.md` → `POSITIONING.md`,
   `templates/content-guide.md` → `CONTENT_GUIDE.md` and `templates/brand.md` →
   `BRAND.md`; fill the `[BRACKET]` slots in pipeline steps 2–3. `STORY.md` exists
   only if the owner opted in at §2a; `website-story` copies it from its own
   `templates/story.md`. `TAGLINE.md` exists only if the owner asked for a tagline;
   `website-tagline` copies it from its own `templates/tagline.md`. If the owner answered §2b: write her answers into the project
   README beside the decision-interview answers, and, where she chose or brought a palette, fill `BRAND.md`'s
   colour tables with it (`website-brand-kit` §5a says what goes where). These documents
   are all that step 2b writes before the tests are green.
5. **Confirm green:** `npm run build && npm test` (the overlay passes the
   a11y/seo/navigation/anchors/orphans/images/tone/positioning/placeholders/email/links/llms-coverage/middleware suite out of the box). Then build pages
   test-first: add the route to `tests/_helpers.ts` `PAGES` *before* writing the
   page (suite goes red), build until green, commit. New features get their test
   first too — `website-qa` §1b maps feature → test.
   **If the owner has a palette or a logo from §2b**, run `website-brand-kit` §6 (the
   intake) now, on the green baseline and before the first page: it checks the palette
   and the logo, writes them into the site, runs these same tests again and puts every
   file back if they go red. Commit once it is green.

## 3a. Outgoing-link sweep — ask, but only if the site links out

The offline `tests/links.spec.ts` guard ships in the suite and runs in CI from commit
1 — nothing to decide there. The **liveness** sweep (`outgoing-link-audit`) is
network-dependent and optional, so gate it on whether the built site actually has
external links, and let the user choose:

```bash
cd "$(git rev-parse --show-toplevel)"
[ -d dist ] || npm run build >/dev/null
SITE_HOST=$(grep -oE "site:[[:space:]]*['\"]https?://[^'\"]+" astro.config.mjs \
  | sed -E "s#.*://(www\.)?##; s#/.*##" | head -1)
EXT=$(grep -rhoE '<a [^>]*href="https?://[^"]+"' dist --include='*.html' \
  | grep -oE 'href="https?://[^"]+"' | sed -E 's/^href="//; s/"$//' \
  | grep -vE "://(www\.)?${SITE_HOST}(/|$|:)" | sort -u | wc -l | tr -d ' ')
```

- **`EXT` is 0** → the site links only to itself. Say so and **skip silently** — do
  not ask.
- **`EXT` ≥ 1** → ask whether to run the liveness sweep now — use a structured
  user-input tool if the platform offers one (Claude Code's **`AskUserQuestion`**),
  otherwise just ask in chat — e.g. *"The site has N outgoing links. Run the `outgoing-link-audit` liveness
  sweep before launch? (fetches each third-party URL; ~a few seconds each)"* — options
  **Run it now (recommended)** / **Skip — I'll run it monthly**. If they say run it,
  invoke the `outgoing-link-audit` skill; otherwise note it as a monthly follow-up.

## 4. Launch & handoff checklist

### Deploy-time guardrails — `templates/PUBLISHING.md` § "For AI assistants — deploy-time guardrails"

That section is the single source of truth — §3 copies `PUBLISHING.md` into every site, so
the post-handoff agent carries it too (the scaffolded README's deploy section points there).
Read it in full before the FIRST deploy, when a brand-new page goes live, and when a live
URL looks stale; this summary covers routine pushes.
**Always announce whether a push is PREVIEW or LIVE** (two-stage sites: "this
is NOT live yet" + the preview URL on every push to `main`; live only after
`npm run ship` AND the production build finishes). **Never request — or
announce — a brand-new page's URL on the live domain before its build is
Active**: the first request — the owner clicking your announcement counts —
caches a 404 at the edge that only a manual dashboard purge clears. Verify on
the hash deployment URL until Active, touch the bare canonical URL last, and
hold Search Console Request Indexing until then.

- [ ] All QA green: `npm test`, with **no "not ready to launch" warning**:
      `UNFILLED_UNTIL_LAUNCH` in `tests/placeholders.spec.ts` is empty. The starter
      lists the privacy page, the imprint and the manifest there until their
      `[BRACKET]` slots are filled; each entry comes out when its target is filled
      (the test turns red until it does). An entry still listed at launch ships
      that placeholder: the test only warns about a listed target. And an empty
      list is not the whole check: the spec has no rule for the starter's example
      values, so read the home page and both legal pages once for the name
      `Example` and the address `hello@example.com`, and `public/llms.txt` for its
      own `[bracket]` slots.
- [ ] **Nothing left unshipped** (two-stage sites): `git log origin/production..origin/main`
      is empty — merged-but-unpromoted work is invisibly unshipped. If not empty and it
      should ship: `npm run ship` (which also VERIFIES the live site serves the new build
      via `/build.txt` — push alone is not proof of live).
- [ ] **Double-Knuth review clean** (`website-review`): both passes — run it as the final
      gate AND after adding the last page.
- [ ] Lighthouse / PageSpeed run; FCP & LCP within target (see `website-qa`).
- [ ] **Outgoing links healthy** (`outgoing-link-audit`) — only if the site links out
      (§3a). No DEAD/REBRAND left unhandled; any retired domain added to
      `tests/links.spec.ts` `STALE_DOMAINS`.
- [ ] **No orphaned pages** — `tests/orphans.spec.ts` green (every page reachable from
      home). For a multi-page site, run `internal-link-audit` and resolve orphans + thin
      pages; deliberately-unlinked pages listed in `ORPHAN_EXEMPT` with a reason.
- [ ] `sitemap-index.xml` present; `robots.txt` + `llms.txt` accurate. (llms.txt
      *coverage* — every `PAGES` route listed, no stale entry for a removed or
      renamed page — is enforced both ways by `tests/llms-coverage.spec.ts`;
      wording accuracy stays a human check.)
- [ ] Required schema validates (Rich Results / schema.org validator).
- [ ] **OG share cards** generated (`npm run og`, the `og-images` skill): a 1200×630
      JPEG **≤300 KB** per page (`public/images/og/`), each page wiring `image=` (or the
      default). `tests/seo.spec.ts` enforces size/dimensions; WhatsApp drops previews over
      ~300 KB. Plus favicon/manifest icon set in place, and the manifest's
      `[BRACKET]` fields (name/short_name/description) filled in the site's
      content language with `lang` set from `SITE.locale` — `placeholders.spec.ts`
      catches a bracket left there, but no spec reads the manifest's language, so
      English in a German site's manifest ships silently otherwise.
- [ ] Imprint/legal + privacy pages present (EEAT trust + DE legal requirement).
      The starter ships a GDPR privacy draft (`src/pages/privacy.astro`): every
      `[BRACKET]` slot filled, the analytics section matching the real setup.
      No analytics: the analytics paragraphs deleted, `USE_ANALYTICS = false` as shipped.
      With Plausible: `USE_ANALYTICS = true`, `bash tests/check_analytics_gate.sh` green,
      and the `Email Tap` goal exists in Plausible (§1 Q5). In script mode (the default)
      also the host in `script-src` and `connect-src` of `public/_headers`.
      In server mode also: `PLAUSIBLE_HOST` and `PLAUSIBLE_DOMAIN` set as Production
      variables (and nowhere in script mode or with analytics off), the host left out of
      `public/_headers` (no script loads), the privacy page's server-mode slots kept, and
      one page view and one email tap on the live domain seen under Today.
      Whether the site may run without a consent banner: §1 Q5's last point.
      German-market sites: don't re-translate — swap in the vetted German
      drafts that ship in the site repo, whose own file headers carry the
      exact steps: `src/pages/_datenschutz.astro` (§ 25 TDDDG-aware;
      underscore = unrouted until renamed; German-only sites serve it at
      `/datenschutz` REPLACING `/privacy`, multilingual sites use its text at
      `/de/privacy`) and `src/pages/impressum.astro` (§ 5 DDG + § 18 Abs. 2
      MStV — required for providers established in Germany, whatever the
      site's language, and for sites targeting the German market; fill/delete
      per its header and section comments, which also cover Austrian/Swiss
      adaptation and the six-piece removal for providers with no German
      nexus).
- [ ] Deployed to Cloudflare Pages per the chosen **publish model** (§1 Q6).
      **Two-stage:** create the live branch (`git checkout -b production && git push -u
      origin production && git checkout main` — end back on `main`), then in Cloudflare set
      *Production branch* = `production` — so
      `main` = noindexed preview, `production` = live; analytics, once switched on, fires on production only.
      **Single-stage:** `main` = live (default Cloudflare production branch).
      **Creating the Pages project + first deploy** (the step a Cloudflare newcomer
      struggles with) — offer the bootstrap options in
      `references/CLOUDFLARE_FIRST_DEPLOY.md`: for a site on GitHub, recommend the **setup
      script** (`scripts/cloudflare-setup.mjs setup`: one short-lived token, the owner's yes
      to a printed list, a project connected to GitHub with the checklist's settings; the
      script's `launch` stage attaches the domain on launch day), with the token-assisted direct
      upload (no GitHub connection; you run Wrangler), git-integration by hand and
      browser/manual as the other offered paths.
      Either way: hand the owner `PUBLISHING.md` and walk the **first** publish with them.
      Non-English-speaking owner? Translate `PUBLISHING.md` in-session first (e.g. save
      as `PUBLISHING.de.md`, or replace the copy) — it is the owner's PERMANENT reference,
      unlike your conversational guidance, and the shipped template is English. Any
      translation or replacement MUST keep the "For AI assistants — deploy-time
      guardrails" section (translated is fine, dropped is not — it is the post-handoff
      agent's only copy of those rules).
- [ ] **Dependabot security fixes on** for the site's GitHub repo: run `SETUP.md`'s
      Dependabot lines from the site folder; the output must name this repo and show
      `alerts: on` and `security updates: on`. Not skippable: the site's lockfile is its
      own, so no suite update ever patches it.
- [ ] **`<project>.pages.dev` redirects to the live domain**: once the live domain serves
      this build, Production variable `CANONICAL_URL` set and redeployed; `curl -sI` on the
      alias shows `301` (`references/CLOUDFLARE_FIRST_DEPLOY.md`, "After go-live").
- [ ] **Search engines notified** (`search-console-setup`): live domain added to Google
      Search Console (Domain property + DNS TXT) and Bing (import from GSC),
      `sitemap-index.xml` submitted to both, and **IndexNow on** (Cloudflare Crawler
      Hints toggle). Register the production domain only — never a preview host.
- [ ] **Business listings claimed, if applicable** (`business-listings-setup`,
      §4a): `sameAs` verification done for any named entity — every URL in
      schema confirmed live or manually verified logged-out, per that skill's
      own verification rules; directories claimed where a suitable one exists
      for the category; Google Business Profile and Bing Places live only if
      the entity actually qualifies (the skill's §1 step 0 checks). "No
      relevant directory found" and "not eligible" are valid, non-blocking
      outcomes — distinct from "skipped by owner choice".
- [ ] Repo self-contained for the receiving party: `.gitignore`, `.claude/`,
      `POSITIONING.md`, `CONTENT_GUIDE.md`, `BRAND.md` (+ `STORY.md` if opted in), `tests/`, `SETUP.md`,
      `PUBLISHING.md` (with its "For AI assistants" guardrails section intact),
      `AGENTS.md` + `CLAUDE.md` (no `[BRACKET]` slot left, the scaffold note removed,
      one publish-model block kept in §2), and a
      `README.md` with the decision answers + "how to add a page / run tests / deploy".
- [ ] **Credit settled** (§4b), after the site is live: asked once, or found already
      in the footer, and the outcome recorded in the project `README.md`. "Declined" is
      a complete, valid outcome.

## 4a. Business listings — ask, but only if the site is a claimable entity

`business-listings-setup` claims category directories and verifies the site's
`sameAs` schema resolves — both apply to any named entity. Google Business
Profile and Bing Places are narrower: they need a real address customers visit,
or staff who travel to serve customers, which the skill's own §1 checks. Naming
the entity is enough to run the skill; it is not enough to guarantee a Google/Bing
profile will follow, and the ask below says so. Gate it the same way as the
outgoing-link sweep in §3a: check a condition, then let the user choose rather
than assuming.

- **The site has no claimable identity at all** (a personal blog with no
  business or professional practice behind it, a resource hub with no identity
  of its own) → there is nothing to claim. Say so and **skip silently** — do not
  ask. A sole proprietor or consultant who trades under their own name (a
  photographer, a freelancer) still counts as a named entity here — the test is
  "is there a business or practice to claim," not "is the name different from a
  person's."
- **The site represents a named, real-world entity** (an event series, a studio, a
  local business, a community or organization with its own name) → ask whether to
  run it now — e.g. *"This looks like a named entity (`<name>`) that could claim
  directory listings and verify its schema profiles. It may also qualify for a
  Google Business Profile if it has a real address or serves customers in
  person — the skill checks that itself. Want to set this up now? It needs a few
  clicks from you at each platform — I'll draft everything else."* — options
  **Run it now (recommended)** / **Skip — I'll do it later**. If they say run it,
  invoke the `business-listings-setup` skill; otherwise note it as a post-launch
  follow-up alongside `search-console-setup`.

## 4b. A credit for Croftweaver — ask once, after the site is live

Croftweaver is free and its license asks for no credit. The people who make it ask for
one anyway: a small "Built with Croftweaver" link in the footer, and a star on GitHub.
It is a request, never a condition, and this is the only place the pipeline raises it.

This step belongs to the launch checklist (§4). Do not raise it in a later session
that is doing other work on the site, with one exception, an unfinished yes: the
README says "credit: badge" or "credit: text link" and the footer of the live site has
no link to `croftweaver.com`. Then the work was cut short somewhere before it was
published, or the credit was taken out since. Say so once. On a yes, do whatever is
left of the steps below: paste, test, publish. On any other answer, or none, change
the line to "credit: declined". That is not a second ask.

Ask only when all three hold; otherwise do not ask:

- **The site is live**: the deploy item of the §4 checklist is done and `npm test` is
  green. Never during the build and never while something is failing.
- **The project `README.md` has no credit line** among the decision answers. A line
  there means the question was put already, whatever the line says.
- **The footer in the site's source does not link to `croftweaver.com` yet** (the
  starter keeps it in `src/layouts/Base.astro`). If it does, record "credit:
  already in the footer" in the README and stop.

Then ask once, in one message — a structured user-input tool if the platform offers
one (Claude Code's **`AskUserQuestion`**), otherwise in chat:

> Your site is live. I hope you enjoyed building it.
>
> The people who make Croftweaver have one request, and it is only a request: would
> you add a small "Built with Croftweaver" credit to your footer? It links to
> croftweaver.com and helps others find the toolkit. I can add it now, as a badge or
> as a plain text link. If the site belongs to a customer of yours, it is their call.
>
> And if you liked Croftweaver, a star on GitHub helps too:
> https://github.com/karero/croftweaver

Options: **Add the badge** / **Add a text link** / **No thanks**.

- **Record the answer first**, before any other step, with the decision answers in
  the project README: "credit: badge", "credit: text link" or "credit: declined". No
  later session asks again then, even if this one is cut short.
- **Add the badge** or **Add a text link** → take the code from
  `https://croftweaver.com/partner-assets`, which is its only source; do not write it
  from memory. Use the page's HTML code, never its Markdown code, which is for a
  README. The HTML is one `<a>` link around one `<img>` (alone or inside a
  `<picture>`), or the words "Built with" and one `<a>` text link. If the page offers
  anything else, such as a script, a style or an attribute that runs code, do not
  paste it: tell the user. For the badge, save each
  file the chosen code's note names, from
  `https://croftweaver.com/brand/badge/<file name>`, into `public/brand/badge/`: the
  starter's security rules block images from other sites. Put the code inside
  `<footer class="site-footer">` in `src/layouts/Base.astro`, after the legal links.
  Look at the footer in light and in dark, and with the site's own theme switch if it
  has one, and pick the badge that reads well in each. Run `npm test`; if a test
  objects to the pasted code, tell the user and do not change the test to make the
  credit fit. Then publish per the publish model (§1 Q6) with the usual
  preview-or-live announcement.
- **No thanks** → say "No problem" and nothing more.
- **No answer** → say nothing more about it, and record it as declined.

Never add the credit unasked, never ask a second time, and never give the star for
the user: it is their own click on their own account. Do not word the request as
something owed ("in return", "to support us").

## Notes

- Do not rebuild what existing skills cover — GEO depth → `ai-seo`; technical-SEO/
  Core-Web-Vitals → `seo-audit`; JSON-LD → `schema-markup`; IA → `site-architecture`;
  research → `customer-research`; copy → `copywriting`; images → `image`.
- After any code/copy edit, re-run `website-qa`. "Done" means the tests are green,
  not that the file was written.
- Run **`website-review`** (the Double-Knuth two-pass audit) at the **end of a build**
  (pre-launch) and **after adding/editing a page** — it's the cross-file consistency gate
  on top of `website-qa`'s tests (a new route can silently break `PAGES`, nav, the sitemap,
  internal links or canonical).
- **Editing the skill suite itself** (these templates, the test specs, or a sibling
  skill) is different from reviewing a site: green tests do not catch doc↔test drift,
  so run `/code-review` before trusting the change. The Double-Knuth pass that hardened
  this suite found exactly that class of issue.

---
name: market
description: "Marketing plan and execution for a solo dev in Germany: positioning, channels, launch, ads law, budget. Use when a project needs users or buyers."
---

# Market

Checked 2026-10-03. This skill plans the marketing. The copy, posts and videos come from
skills and tools that are added to each project with `toolbox`:

| Need | Tool |
|---|---|
| Campaign copy, landing page, emails, ad variants | ECC `marketing-campaign` |
| Platform-native posts | ECC `content-engine` |
| Consistent voice | ECC `brand-voice` |
| Short videos and ads | `video-studio` (the studio roles; HyperFrames for motion) |
| Scheduled posting, comments, DMs | `social-team` (posting service, Instagram Messaging API) |
| Audience and competitors | `product-lens` (global) and WebSearch |
| SEO | `seo` and `seo-specialist` (both global) |

Markers: **[S]** search results and legal publishers agree; **[K]** known but not re-read.

## 1. The one-page plan goes into the PRD

Marketing changes what gets built: the landing page, a waitlist, share features, tracking
events. So the plan is part of the PRD, not an afterthought.

1. **Buyer.** Who buys, in one sentence, and the moment they need it.
2. **Positioning.** "[Product] helps [audience] [outcome] by [mechanism]". Name 3 competitors and
   what we do differently.
3. **Goal.** The 90-day goal in numbers, e.g. 300 on the waitlist and 50 paid. Pick one metric
   that matters most.
4. **Channels.** yskills' own channel (§2a) first, then one or two more plus one test, from the table below. Never all of
   them.
5. **Budget.**
   - Start organic, at €0.
   - Pay for ads only once organic posts show which message sells.
   - Then test small: one ad set for about a week before judging it [K].
6. **Launch dates.** Section 3.
7. **Tracking.** The events and UTM tags. Section 5.
8. **Legal check.** Section 4.

### Questions when marketing starts

Asked when the marketing step starts (`operator/run.md` step 1: no grill batch). Claude takes the
recommended pick of each and says it in one line; only the accounts and the face or voice question
go to yskills, as 1-2 cards:

- **Market:** German and English speakers (yskills' default: English content, German and English
  app text), Germany only, or English only.
- **Monthly ad budget:** €0 (recommended at the start), up to €100, or up to €500.
- **Accounts yskills will use or create** (multi-select): TikTok, Instagram, YouTube, LinkedIn,
  X, Reddit, none.
- **Showing their face or voice in videos:** yes, hands and product only, or no (Claude makes
  motion-graphics videos).
- **Hours per week for marketing:** 1, 3, or 5+.

## 2a. yskills' own channel (decided 2026-10-05)

One standing audience channel serves every project, so no launch starts from zero followers.

- **Who and how:** yskills talks in English; the audience is English and German speakers.
  Meme and joke content, free, building an audience first. Projects get promoted there once
  people follow, and every probe uses it as its first channel.
- **Ratio:** mostly entertainment; a project post at most every fourth post, and only as a joke
  that stands on its own. The probe link goes in the bio with UTM tags (`utm_source=<platform>`,
  `utm_campaign=<project>`).
- **Claude does:** a weekly batch of meme and joke ideas, scripts and captions (hooks in the
  first second, English on screen, German subtitles where it helps), tied to what the current
  project is about, for yskills to approve.
- **Rules that still apply** (§4): an Impressum link in the bio once it promotes products; the
  platform's commercial sound library for anything promoting a product; meme templates and film
  stills are someone else's images, so prefer self-made formats or the platform's own templates
  for product posts [K].
- **Weekly numbers** (followers, views, clicks to the bio link) go into each project's
  `metrics/` file as channel `own`.

## 2. Channels for a solo developer

| Channel | Fits | Claude does | yskills does |
|---|---|---|---|
| Short video (TikTok, Reels, Shorts) | Consumer apps, physical products, anything you can show in 15 seconds | Hooks, scripts, HyperFrames clips (demos, captions, before/after), a posting calendar | Films face or hands clips if wanted; on his personal account approves the batch or switches on auto-post; project accounts are the team's (`social-team`, Posting) |
| SEO and content | Things people search for: tools, how-tos, comparisons | Keyword map, one page per search intent, structured data, page speed | Nothing |
| Communities (subreddits, forums, Discord, Product Hunt and Hacker News for English) | Dev tools, niches, honest maker stories | Drafts in an honest "I built this" tone, following each community's rules | Posts from their own account |
| Email list | Everything | Waitlist, launch sequence, monthly update (Resend audiences) | Nothing |
| Paid ads (Meta, TikTok, Google) | A message that already sells, and a margin that pays for ads | Ad variants, server-side conversion events, weekly cost-per-sale report | Pays; connects the ad accounts |
| Marketplaces (Etsy, Amazon) | Physical products | Listing copy and photos brief; compares fees against our own shop | Opens the seller account |
| Creators and UGC | Consumer products | Creator shortlist, brief, offer | Sends products, signs off |

## 3. Launch sequence

| When | What |
|---|---|
| 4 weeks before | Landing page with a waitlist (double opt-in). Analytics and UTM tags work. Social profiles link to the Impressum. The first 3 posts are out. For a project meant to earn this page is the `operator`'s probe slice, live before the rest is built |
| 2 weeks before | 3 to 5 short videos a week. Early testers; ask them for honest feedback and real testimonials |
| Launch day | Email the waitlist. Post in the chosen communities. Run a launch offer only if it follows § 11 PAngV (section 4) |
| Weeks 1 to 4 | Weekly review: which post or page brought paying users. Do more of that. Start ads only on the winning message |

## 4. German advertising law

These are the rules small sellers get warning letters for. The legal-text service from the
`sell` skill can check anything unclear.

- **Impressum on social profiles.** Business profiles need an Impressum within two clicks,
  e.g. a link in the bio to the site's Impressum [S].
  [e-recht24](https://www.e-recht24.de/impressum/13078-impressum-auf-instagram.html)
- **Label advertising.**
  - Paid or sponsored posts, and anything a creator gets money or products for, are labelled
    "Werbung" or "Anzeige", visible at the start.
  - A business account showing its own products is clearly commercial, but if in doubt, label
    it [S].
  - [IHK on labelling](https://www.ihk.de/chemnitz/recht-und-steuern/rechtsinformationen/internetrecht/kennzeichnung-von-werbung-durch-influencer-5270264)
- **Newsletters need double opt-in.**
  - Log the proof of consent.
  - Put an unsubscribe link in every email.
  - Mailing existing customers without consent (§ 7 Abs. 3 UWG) is a narrow exception: skip
    it [S].
- **AI-generated people, voices or realistic scenes.** Since 2026-08-02 these must be disclosed
  as AI-generated (AI Act Art. 50). Plain motion graphics and text animations are not
  deepfakes [S].
  [Heidicker](https://www.kanzlei-heidicker.de/aktuelles-und-urteile/eu-ki-verordnung-ab-02-08-2026-deepfakes-kennzeichnen-wettbewerbsrechtliche-risiken.html)
- **Reviews and testimonials.**
  - Real ones only. Never buy them or invent them.
  - If reviews are shown, say whether and how they are verified (§ 5b UWG) [K].
- **Prices and claims.**
  - A discount shows the lowest price of the last 30 days (§ 11 PAngV) [S].
  - General eco claims such as "klimaneutral" are banned without proof since 2026-09-27 [S].
  - Comparisons with competitors must be factual and checkable (§ 6 UWG) [K].
- **Music.** Business accounts use the platforms' commercial music libraries only [K].
- **Ad tracking.** The Meta Pixel, TikTok Pixel and Google tag load only after consent
  (§ 25 TDDDG) [K]. A consent banner then becomes necessary, so plan it in the PRD.

## 5. Measure, then report into HQ

- **Events and tools:** the Analytics owner writes `analytics/TRACKING.md` before launch (`operator/roles/analytics.md`: events, tools, basis, weekly line). Cookieless first; a pixel needs the banner (§ 4).
- **Every link Claude writes for a post carries UTM tags,** so a sale can be traced to the post.
- **Weekly routine.** A scheduled trigger in the project, set up at launch:
  - collects the week's numbers as the Analytics owner's weekly line (`operator/roles/analytics.md`);
  - lists which channel and which post brought paying users, and cost per sale for ads;
  - proposes the next week's 3 actions and the content batch for yskills to approve.
- **HQ.** Numbers go into the project's HQ rows (`docs/hq-rows.md`). Projects get no
  dashboard of their own.

## 6. Who does what

- **Claude:**
  - the plan, copy, scripts and videos;
  - landing pages and email sequences;
  - ad drafts;
  - the weekly report;
  - scheduling posts once the account is connected, by the rules in `social-team`, Posting
    (personal account vs project accounts).
- **yskills:**
  - approves what goes out where `social-team`, Posting says so (his personal account; ads,
    money and deals everywhere); posting and emailing go to the public and cannot be taken back;
  - connects the accounts;
  - pays for ads;
  - films their own content if they want to.

---
name: google-ads-campaign-types
description: Choose the right Google Ads campaign type for a goal. Use when the user asks which Google Ads campaign type to run, Search vs Performance Max, Demand Gen campaigns, Display vs Demand Gen, Video or YouTube campaigns, Shopping (standard vs Performance Max) for retail, App campaigns, Smart or Local campaigns, what each campaign type optimizes for and what inventory it runs on, or what campaign type fits a specific objective.
---

# Google Ads campaign types

Pick the Google Ads campaign type that matches the objective, the inventory it should run on,
and the goal it optimizes for. The campaign type is the most consequential setup decision in
Google Ads: it fixes the networks you reach, the ad formats you can serve, and the optimization
the auction runs. Choosing the wrong type means fighting the platform for the rest of the flight.

Google Ads is Google's self-service auction platform. It buys Search, YouTube, the Display
Network, Discover, Gmail, and Maps through its own auction, organized by campaign type. It is a
different platform from DV360. For the account hierarchy and how campaigns and ad groups sit
together, see the `google-ads-account-structure` skill. For KPI definitions and goal math, see
`programmatic-foundations`. For reading results against the goal, see
`reporting-by-campaign-goal`.

## When to use this skill

- "Which Google Ads campaign type should I use for X?"
- "Search vs Performance Max?" / "Demand Gen vs Display?" / "Standard Shopping vs Performance Max?"
- "What is a Demand Gen campaign?" / "What does Performance Max run on?"
- "How do I advertise on YouTube?" / "Video campaign for awareness?"
- "What campaign type promotes an app?"
- "What is a Smart campaign? A Local campaign?"
- "What does each campaign type optimize for?"

Boundaries with sibling skills:
- Performance Max setup, asset groups, listing groups, and tuning: hand off to
  `google-ads-performance-max`.
- Bid strategy choice (Target CPA, Target ROAS, Maximize conversions or value): hand off to
  `google-ads-bidding`.
- Account hierarchy, ad group theming, shared library, labels: hand off to
  `google-ads-account-structure`.
- Keywords and match types for Search: hand off to `google-ads-keywords-and-match-types`.
- Audience and placement targeting: hand off to `google-ads-audiences-and-targeting`.
- Conversion tracking setup that the goal-based types depend on: hand off to
  `google-ads-conversion-tracking-and-attribution`.

## Quick reference

Objective to campaign type:

| Objective | Primary campaign type | Why |
| --- | --- | --- |
| Capture existing demand (people searching) | Search | Keywords match high-intent queries on the Search Network |
| One campaign across all Google inventory, conversion-focused | Performance Max | Optimizes across Search, YouTube, Display, Discover, Gmail, Maps from one campaign |
| Sell retail products from a feed | Shopping (standard) or Performance Max with a feed | Product data, not keywords, drives the ad |
| Create and capture demand on visual feeds | Demand Gen | YouTube, Shorts, Discover, Gmail with social-style creative |
| Reach and remarket across the web | Display | Visual ads across the Google Display Network |
| Brand awareness and consideration on video | Video (YouTube) | Skippable, bumper, and Shorts formats on YouTube and video partners |
| Drive app installs or in-app actions | App | Promotes the app across Search, Play, YouTube, Discover, Display |
| Small business, minimal management | Smart | Automated ads across Search, Maps, and YouTube with little setup |
| Drive store visits and local actions | Performance Max (store goals) | Local campaigns have been folded into Performance Max |

What each type runs on and optimizes for:

| Type | Inventory / network | Creative | Optimizes for |
| --- | --- | --- | --- |
| Search | Google Search Network (results pages, search partners) | Text and responsive search ads | Clicks or conversions from intent queries |
| Performance Max | All Google channels: Search, YouTube, Display, Discover, Gmail, Maps | Asset groups (text, image, video) plus optional feed | Conversions or conversion value across channels |
| Shopping (standard) | Search results and the Shopping tab | Product listings from a Merchant Center feed | Clicks or value from product listings |
| Demand Gen | YouTube (including Shorts), Discover, Gmail, Display Network | Image and video, social-style | Engagement and conversions from demand creation |
| Display | Google Display Network (sites, apps, YouTube, Gmail) | Responsive display and image ads | Reach, awareness, or conversions across the web |
| Video | YouTube, Google TV, video partners | Skippable in-stream, bumper, Shorts, and other video | Views, reach, awareness, or action on video |
| App | Search, Google Play, YouTube, Discover, Display | Asset-driven, auto-assembled | App installs, engagement, or pre-registration |
| Smart | Search, Maps, YouTube, partners | Auto-generated from inputs | Calls, visits, or sales for small businesses |

## Core process

1. State the objective in one line and confirm it. "Capture people searching for what we sell"
   is Search. "One conversion campaign across everything Google" is Performance Max. "Sell
   catalog products" is Shopping or Performance Max with a feed. "Promote a video to build a
   brand" is Video. The objective, not a feature, picks the type.
2. Confirm the prerequisites the type needs. Goal-based types (Performance Max, Demand Gen, App,
   Shopping, and Smart Bidding on any type) depend on working conversion tracking, and retail
   types need a linked Merchant Center feed. If those are missing, set them up first (hand off
   to `google-ads-conversion-tracking-and-attribution`) or the campaign cannot optimize.
3. Match the type to the funnel stage. Search and Shopping capture existing demand. Performance
   Max and App drive conversions across channels. Demand Gen, Display, and Video create and
   nurture demand higher in the funnel. Do not ask an awareness type to deliver bottom-funnel
   efficiency, or a capture type to build reach.
4. Decide standard versus automated for retail. Use standard Shopping when you want explicit
   control over the product listings, channels, and bidding. Use Performance Max with a feed
   when you want maximum reach and AI-driven optimization across all channels for the same
   catalog. Many retailers run Performance Max as the primary retail engine. See
   `google-ads-performance-max`.
5. Pick the bid strategy for the type (hand off to `google-ads-bidding`) and structure the
   campaign and ad groups (hand off to `google-ads-account-structure`).
6. Set expectations for reporting by the goal the type serves (hand off to
   `reporting-by-campaign-goal`).

## Campaign types in detail

### Search

Text ads on the Google Search Network, triggered by keywords that match what people type.
Highest-intent type because the user is actively looking. Use it to capture existing demand for
your products, services, brand, or category. Organized into tightly themed ad groups of
keywords with ads written to match (see `google-ads-account-structure` and
`google-ads-keywords-and-match-types`). Default first choice for direct response when demand
already exists.

### Performance Max

A single goal-based campaign that optimizes across all of Google's inventory at once: Search,
YouTube, the Display Network, Discover, Gmail, and Maps. You supply asset groups (headlines,
descriptions, images, video) and, for retail, a Merchant Center feed; Google AI handles bidding,
budget allocation, placements, and creative assembly toward your conversion goal. Use it when
you want broad, conversion-focused coverage from one campaign and are willing to trade
channel-level control for reach and automation. Requires conversion tracking. Setup and tuning
live in `google-ads-performance-max`.

### Shopping (standard versus Performance Max for retail)

Retail product advertising driven by a Merchant Center product feed, not keywords. The ad shows
a product image, title, and price.
- Standard Shopping campaigns appear on Search results and the Shopping tab and give you direct
  control over product groups, channels, and bidding.
- Performance Max with a feed extends the same catalog across all Google channels with AI-driven
  optimization and broader reach.
Choose standard Shopping for control and a contained surface; choose Performance Max for reach
and automation. They can coexist, but understand which one Google prioritizes for a given product
before running both.

### Demand Gen

Demand-creation campaigns on Google's most visual, social-style surfaces: YouTube (including
Shorts), Discover, Gmail, and the Display Network. Built for image and video creative that drives
engagement and action higher in the funnel than Search. Use it to create demand and reach
audiences who are not yet searching, with conversion and engagement optimization. Note that
Google Display Ads campaigns are migrating into Demand Gen, with migration beginning in June 2026,
so prefer Demand Gen for new social-style demand-generation work.

### Display

Visual responsive and image ads across the Google Display Network, which spans sites, apps,
YouTube, and Gmail. Use it for broad reach, remarketing to past visitors, and prospecting with
visual creative. Smart Display has been folded into the standard Display campaign offering. For
new demand-creation work on visual feeds, weigh Demand Gen, which is where Display campaigns are
migrating.

### Video (YouTube)

Video ads on YouTube, Google TV, and video partners, in formats including skippable in-stream,
bumper (short, non-skippable), and Shorts ads. Use it for awareness, consideration, and reach at
the top of the funnel, and for action formats lower down. Pick the format and bid strategy to the
goal: views and reach for awareness, action formats and conversion bidding for response.

### App

Promotes a mobile app across Search, Google Play, YouTube, Discover, and the Display Network from
one campaign. You supply assets and a goal (installs, in-app engagement, or pre-registration);
Google assembles and places the ads and optimizes toward the chosen app action. Use it whenever
the objective is app installs or in-app conversions rather than website actions.

### Smart and Local (brief)

- Smart campaigns are the simplest type, built for small businesses with little time to manage
  ads. You provide a few inputs and Google auto-generates and places ads across Search, Maps,
  YouTube, and partners, optimizing for calls, visits, or sales. Choose it when ease beats
  control; graduate to Search and other types when you need real control over keywords, bidding,
  and structure.
- Local campaigns, which drove store visits and local actions, have been folded into Performance
  Max. For store and local goals, run Performance Max with store goals rather than looking for a
  standalone Local campaign type.

## Decision rules and thresholds

- Demand already exists and is searchable: start with Search. Add Shopping if you sell retail
  products from a feed.
- You want one conversion campaign across all of Google and have conversion tracking: Performance
  Max. Give it its own campaign, budget, and goal (see `google-ads-account-structure`).
- Retail catalog, want control: standard Shopping. Retail catalog, want reach and automation:
  Performance Max with a feed.
- You need to create demand on visual feeds (not capture it): Demand Gen for YouTube, Shorts,
  Discover, and Gmail; Video for YouTube-led awareness and reach.
- Broad web reach or remarketing with visual ads: Display, but prefer Demand Gen for new
  demand-generation work given the migration.
- The product is an app: App campaign, every time, for install and in-app goals.
- Small business, minimal setup: Smart. Store visits and local actions: Performance Max with
  store goals.
- Do not run a single campaign type against two different goals. Match one type to one objective,
  and if you have two objectives, run two campaigns (see `google-ads-account-structure`).

## Common pitfalls

- Reaching for Performance Max by default. It is powerful but cedes channel-level control and can
  absorb budget and credit from Search and Shopping if you do not give it a clear boundary, goal,
  and brand-safety setup. Decide deliberately (see `google-ads-performance-max`).
- Enabling the Display Network inside a Search campaign for "extra reach." Run Display as its own
  campaign type so intent, benchmarks, and reporting stay clean (see
  `google-ads-account-structure`).
- Launching a goal-based type (Performance Max, Demand Gen, App) without conversion tracking. It
  has nothing to optimize toward. Set up tracking first.
- Expecting an awareness type (Video, Display, Demand Gen) to deliver bottom-funnel CPA. Hold it
  to the goal it serves and read it with the right report (see `reporting-by-campaign-goal`).
- Looking for a standalone Local campaign type. It is now part of Performance Max with store
  goals.
- Running standard Shopping and Performance Max on the same products without knowing which Google
  serves. Understand the prioritization before doubling up.

## Sources

- [Choose the right campaign type](https://support.google.com/google-ads/answer/2567043) (as of June 2026)
- [About ad formats available in different campaign types](https://support.google.com/google-ads/answer/1722124) (as of June 2026)
- [Create a Search campaign](https://support.google.com/google-ads/answer/9510373) (as of June 2026)
- [About the Google Search Network](https://support.google.com/google-ads/answer/1722047) (as of June 2026)
- [About Performance Max campaigns](https://support.google.com/google-ads/answer/10724817) (as of June 2026)
- [About Shopping ads](https://support.google.com/google-ads/answer/2454022) (as of June 2026)
- [About Demand Gen campaigns](https://support.google.com/google-ads/answer/13695777) (as of June 2026)
- [About Display ads and the Google Display Network](https://support.google.com/google-ads/answer/2404190) (as of June 2026)
- [About Video campaigns](https://support.google.com/google-ads/answer/6340491) (as of June 2026)
- [About App campaigns](https://support.google.com/google-ads/answer/6247380) (as of June 2026)
- [How Smart campaigns work](https://support.google.com/google-ads/answer/7652860) (as of June 2026)
- [Google Network](https://support.google.com/google-ads/answer/1752334) (as of June 2026)

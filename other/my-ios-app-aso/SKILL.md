---
name: my-ios-app-aso
description: Create, review, or optimize iOS App Store metadata and ASO strategy. Use when generating app names, subtitles, keyword fields, promotional text, descriptions, competitor matrices, keyword pools, localized listing copy, screenshot messaging, App Store positioning, or ASO review notes for iOS apps.
---

# iOS App Store ASO

Treat App Store metadata as a product surface, not a form-filling chore. The app name, subtitle, keywords, promotional text, description, icon, previews, and screenshots affect discoverability, ranking signals, first impression, and conversion.

## Metadata Strategy

- Start from user intent. List the search phrases a target user would naturally type when looking for this app, then map those phrases into name, subtitle, and keywords.
- Before generating app name, subtitle, promotional text, description, or keywords, collect competitor data when available. Use competitor listings, ASO dashboards, keyword rankings, reviews, screenshots, and category charts to avoid writing metadata from intuition alone.
- Balance search coverage with trust. Keyword stuffing can make the listing look low quality even when it increases matching surface.
- Keep metadata accurate. Do not promise unsupported features, unsupported platforms, pricing terms, celebrity names, trademarked terms, or competitor names in visible copy unless there is a clear legal and review-safe reason. For the keyword field, consider relevant competitor app names as discoverability terms when they are collected from the competitor set and are review-safe for the target market.
- Localize metadata intentionally. Do not blindly translate keywords; choose terms people in that locale actually search for.
- Review metadata whenever product positioning changes, not only when code changes.

## Competitor Analysis Data Sources

Use ASO and app-intelligence tools to ground metadata decisions in observed market data. Do not rely only on intuition.

- **QiMai / 七麦数据**: use for China-focused App Store and Android market research, ranking snapshots, keyword coverage, keyword heat, Apple Ads/Search Ads signals, and competitor monitoring.
- **ASOTools**: use for overseas ASO, Google Play + App Store keyword research, competitor keyword ideas, country/category rankings, download and revenue estimates, and multi-locale analysis.
- **DianDian / 点点数据**: use for broader app/game intelligence, app rankings, market share, download/revenue trend estimates, user behavior signals, competitor comparison, and global market tracking.
- **ChanMaster / 蝉大师**: use for keyword expansion, keyword rank/coverage checks, ASO diagnosis, App Store ranking history, ASM/Apple Search Ads auxiliary analysis, and competitor ASO comparison.
- **ASO114**: use as a supplementary domestic ASO source for keyword coverage, ranking trends, Android channel checks, and competitor keyword gap analysis.

Treat third-party metrics as directional estimates, not absolute truth. Different vendors may disagree because their data models, market coverage, refresh cadence, and estimation methods differ.

## Competitor Analysis Workflow

1. Define the competitor set:
   - Direct competitors: apps solving the same user job.
   - Search competitors: apps ranking for the keywords you want.
   - Category competitors: apps consistently appearing in the same category charts.
   - Aspirational competitors: apps with strong conversion assets or positioning, even if the feature set differs.
2. Capture a metadata snapshot for each competitor:
   - App name, subtitle, keywords if visible or estimated, promotional text, description opening, screenshots, preview videos, category, rating, review count, version cadence, pricing, and IAP/subscription model.
3. Capture ASO signals:
   - Keyword coverage, keyword rank, keyword heat/search volume, ranking history, category rank, hot-search presence, download/revenue estimates, review trend, rating trend, and regional differences.
4. Identify gaps:
   - Keywords competitors rank for but this app does not.
   - High-intent long-tail terms with moderate difficulty.
   - Positioning claims competitors repeat.
   - Visual promises made by screenshots and previews.
   - Review complaints that reveal unmet user needs.
5. Convert findings into metadata decisions:
   - Put the strongest intent terms into app name and subtitle.
   - Put remaining relevant terms into keywords.
   - Use promotional text and description to answer the most common user hesitation.
   - Use screenshots and previews to prove the highest-value claims.
6. Track before/after:
   - Save the old metadata, new metadata, change date, target keywords, baseline ranks, and follow-up ranks.
   - Re-check after enough time has passed for indexing and ranking movement.

## Metadata Generation Workflow

When asked to generate app name, subtitle, promotional text, description, or keywords:

1. Collect inputs:
   - App purpose, target users, core features, monetization model, supported regions/languages, and any hard product claims.
   - Existing app metadata, if any.
   - Competitor list, target keywords, category, and country/region.
2. Gather competitor evidence:
   - Use ASO tools, App Store pages, public listings, or user-provided exports/screenshots to collect competitor names, subtitles, description openings, screenshot promises, review complaints, keyword coverage, and rank signals.
   - If live data access is unavailable, ask for tool exports or competitor URLs; otherwise state that the metadata draft is based on provided context only.
3. Build a keyword pool:
   - Separate own-brand terms, competitor app name terms, category terms, feature terms, problem terms, audience terms, and long-tail intent terms.
   - Mark each term as high/medium/low priority based on relevance, competitor usage, search intent, and likely difficulty.
4. Allocate words deliberately:
   - App name: brand plus the strongest core term if it remains natural.
   - Subtitle: primary value proposition plus secondary high-intent terms.
   - Keywords: relevant remaining terms, synonyms, and long-tail fragments not already covered by name/subtitle.
   - Promotional text: timely value proposition or campaign copy aimed at conversion.
   - Description: benefit-first explanation, proof points, feature bullets, and trust-building details.
5. Return options with rationale:
   - Provide 3-5 candidate name/subtitle combinations when naming is requested.
   - Provide a keyword list grouped by intent, not just one comma-separated dump.
   - Explain which competitor or search-intent evidence influenced the choices.
   - Call out unsupported assumptions and review-risky claims.

## Data Collection Rules

- Prefer official exports, paid dashboard downloads, public pages, or documented APIs when available.
- Do not bypass login, paywalls, rate limits, anti-bot controls, robots.txt, or platform terms just to scrape data.
- If using screenshots or manual notes from paid tools, record the source, query date, country/region, platform, and selected category.
- Normalize data before comparing competitors: same country, same device family, same app store, same category, and same date range.
- Keep a simple competitor matrix so metadata changes are explainable later.

## App Name

- Keep the app name simple, memorable, easy to spell, and connected to what the app does.
- Use the pattern `Brand/App Name + highest-value core keyword` only when it still reads naturally.
- Put the strongest, most differentiated keyword here; do not waste the name on generic category words alone.
- Stay within App Store limits and avoid names that are too similar to existing apps.

## Subtitle

- Use the subtitle to complete the app name: explain the primary value, core use case, or audience.
- Add secondary high-intent keywords that were not already used in the name.
- Avoid generic claims such as "best app" or vague emotional copy with no feature signal.
- Treat name and subtitle as one combined sentence users see in search and on the product page.

## Keywords

- Use the keyword field for relevant search terms not already covered by the app name or subtitle.
- Prefer concise single terms separated by commas without spaces so the character budget goes to searchable words.
- Mix broad category terms with specific use-case terms. Broad terms increase reach; specific terms usually express stronger intent.
- Include relevant competitor app names from the defined competitor set when generating keyword candidates. Keep them in the keyword field rather than visible app name, subtitle, promotional text, screenshots, or description unless there is a clear legal and review-safe reason.
- Avoid duplicates across name, subtitle, and keywords unless testing proves a reason.
- Include common synonyms, feature terms, audience terms, and problem terms. Skip words that are irrelevant just because they have high volume.
- Track performance and revise keywords over releases; ASO is an iterative process.

## Promotional Text

- Use promotional text for timely conversion copy: new features, seasonal campaigns, limited-time positioning, or a strong current value proposition.
- Keep it self-contained and useful even if the user reads only the first sentence.
- Do not treat promotional text as the main keyword field; use it to persuade visitors who already reached the product page.
- Prefer specific benefit copy over hype.

## Description

- Lead with the clearest user benefit and the problem the app solves.
- Use short paragraphs and scannable feature bullets. Put the most important information before the user has to expand or keep reading.
- Explain what makes the app different, who it is for, and what the user can do immediately after installing.
- Keep claims review-safe and supportable. Avoid unverifiable superlatives, roadmap promises, and misleading pricing language.
- Refresh the description when major features, pricing, subscription behavior, or positioning changes.

## App Review Notes

When generating App Store review notes, include these fields explicitly. If a field cannot be verified from the app, project files, or user-provided context, write `Unverified - developer confirmation needed` instead of inventing details.

- Tested devices and OS versions: list the device models and operating systems tested before submission.
- Purpose and target audience: describe what the app does, who it is for, the problem it solves, and the value it provides.
- Access and setup instructions: explain how reviewers can access the main features, including required login credentials, demo accounts, subscriptions, entitlement state, sample files, or test content. State `No login required` when true.
- Core external dependencies: list external services, tools, APIs, SDKs, platforms, data providers, authentication services, payment processors, AI services, or cloud services used to deliver core functionality. State `No external service required for core functionality` when true.
- Regional behavior: describe feature/content differences by region, or confirm the app functions consistently across all supported regions.
- Regulated or protected material: if the app operates in a regulated industry or uses protected third-party material, include relevant authorization, credentials, licenses, or documentation. State `Not applicable` when true.

## Review Checklist

- Does the name/subtitle/keyword set cover the target search intents without obvious duplication?
- Does the listing read like a trustworthy product page, not an SEO dump?
- Are the first visible words of the name, subtitle, promotional text, and description understandable without context?
- Are all claims true in the current app build?
- Are metadata, screenshots, and app behavior aligned?
- Do review notes include tested devices/OS versions, purpose/target audience, setup/access instructions, external dependencies, regional behavior, and regulated/protected-material disclosures?

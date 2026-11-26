---
name: page-to-social-posts
description: Turn one page or blog post into genuinely different, platform-native posts for your own X, LinkedIn, Facebook, Instagram, Threads, Pinterest, Bluesky, YouTube and Google Business Profile accounts. Use for "repurpose this article", "social posts from this page" or parasite SEO on owned profiles, with human approval, a sane pace and UTM links.
license: MIT
metadata:
  author: RomeoSEO
  version: "3.0.0"
  homepage: https://romeoseo.com/skills/page-to-social-posts
---

# Turn one page into platform-native posts

Read one published page, pull out the distinct ideas worth a post on their own, and write a different, native post for each platform the brand actually owns, ready for a human to approve. You hand back an angle list, the drafted posts with UTM-tagged links and disclosures, a paced schedule, and a measurement sheet that says which angles earned their place and which to retire.

> **Romeo's rule:** If a post is useful to someone who never clicks, it's a post; if it only works as a trailer for the page, it's an ad, and people scroll past it like one.

## Use this when

- A new article, guide or data page has just gone live and should reach people beyond search.
- An older evergreen page has original data or a strong how-to that was never shared properly.
- `parasite-seo-plan` chose social platforms and the owners need posts to publish.
- The brand currently posts the same blurb and link everywhere, and nobody clicks.
- A local business wants Google Business Profile posts that say something useful.

## Don't use this for

- Reddit threads and Quora answers: different rules, community norms and disclosure → `reddit-quora-answers`.
- Long-form LinkedIn articles written to be cited by AI → `linkedin-for-ai-search` (this skill writes LinkedIn feed posts only); full YouTube videos → `youtube-for-ai-answers`.
- Deciding which platforms are worth the effort at all → `parasite-seo-plan`.
- Fixing the source page before it's shared → `seo-content-qa`.

## What you need

### Required

- The published page: URL, or full text with headings, images and the date it was last updated.
- The accounts the brand owns, per platform (handles), and who approves posts for each.
- Who the audience is on each platform and what they come there for.
- Voice notes, or three to five past posts that did well and one that flopped.

### Helpful

- Platform analytics exports for the last 90 days (impressions, engagement, link clicks) per account.
- GA4 (or other analytics) data by session source, medium and campaign, so UTM results can be read.
- Images, charts and screenshots from the page with the rights to reuse them, plus the brand's templates.
- The keyword or AI prompt the page targets, from `seo-content-brief` or `ai-prompt-research`.
- Access to each platform's native scheduler, or a scheduling tool that publishes through the platforms' official APIs.

### No tools?

Paste the page text into the chat. Write drafts in a shared document with one section per platform for the approver. Build UTM links by hand or with Google's free Campaign URL Builder, post from each platform's own app or native scheduler, and log results in a spreadsheet: post URL, date, impressions, engagement, link clicks, and sessions from GA4's Traffic acquisition report filtered by campaign.

## Ground rules

- A new angle, not a paraphrase. Each post gives one specific thing (a number, a step, a mistake, a definition) in full, so it's worth reading without the click.
- Write for the platform, not for the page. Same idea, different format: a LinkedIn lesson, an X thread, an Instagram carousel and a Pinterest how-to pin are four pieces of writing, not one with the line breaks moved.
- Near-identical posts across platforms or accounts look like spam to platforms and add nothing for search. Scaled, templated reposting is the pattern Google's scaled content abuse policy and most platforms' spam rules describe.
- A human approves every post before it goes out, including scheduled ones. The approver checks facts against the page, not just tone.
- Post manually, with the platform's native scheduler, or through a tool that uses the platform's official API. Never browser automation, scraping tools, auto-DMs, auto-replies, follow/unfollow tools or account farms.
- Expect `nofollow` links or redirects. The point is referral visits, brand recall and branded search, never link equity. Tag every link with UTM parameters.
- Pace beats volume. A handful of good posts spread over weeks outperforms a burst, and doesn't train followers to ignore you.
- Disclose what needs disclosing: affiliate links, paid partnerships (use the platform's paid-partnership label), and employees posting about their employer's product.
- Retire what flops. Reposting a dead angle in new words is still a dead angle.

## Steps

1. **Check the page is worth spreading.** Confirm it's published, accurate and dated, and note its one main claim and its target query.
   - Thin, out of date or wrong pages get fixed first (→ `seo-content-qa`); spreading them multiplies the problem.
   - Note facts that need care: prices, medical, legal or financial claims, customer names, anything under embargo.
2. **Extract every candidate angle.** Read the page section by section and list each distinct idea with its type and where it sits on the page.
   - Types: claim, step or process, statistic (with source and date), definition, example or case, objection and its answer, FAQ, common mistake, comparison, first-hand lesson.
   - Keep an angle only if it stands alone, is specific, is true and sourced on the page, and someone on at least one of the brand's platforms would care. A 1,500-word page usually yields 4 to 10 keepers; a thin page yields one or two, and that's the honest answer.
3. **Turn each angle into something new.** Don't summarise the page in fewer words.
   - Enter from a different door: open with the mistake, the surprising number, the question a customer asked, the before and after, or the step most people skip.
   - Add what the page doesn't have where you can: what changed since publishing, a reader's question, what the team got wrong first time. Any new factual claim needs the same sourcing as the page and goes to the approver flagged as new.
   - Test: put the post next to the page's intro paragraph. If a reader would see the same sentences, rewrite it.
4. **Match angles to platforms.** Not every angle belongs everywhere.
   - Use only platforms where the brand has an account it actually runs, and the ones `parasite-seo-plan` marked `Go` or `Test`.
   - Steps and processes suit X threads, LinkedIn document posts and Instagram carousels; statistics suit LinkedIn and X; visual how-tos suit Pinterest and Instagram; local news, offers and events suit Google Business Profile and Facebook.
   - Use each angle on two or three platforms at most, rewritten each time.
5. **Write each post to the platform's format and rules.** Limits change, so check each platform's current help pages before publishing.
   - X: 280 characters for standard accounts (longer for paid tiers). One idea per post; threads of 3 to 8 posts for steps. Many accounts see lower reach on posts with links, so put the link in the last post of a thread and judge by your own analytics. X's automation rules prohibit posting duplicate or substantially similar content across accounts you control, and automated mass replies or mentions (re-read the current rules before scheduling anything).
   - LinkedIn (feed post): up to 3,000 characters; only the first two lines or so show before "see more", so the useful part goes there. First person, one specific lesson, line breaks for reading. Document (PDF) posts work for step-by-step angles. Tag only people who were involved. LinkedIn's Professional Community Policies ban agreeing ahead of time to like or reshare each other's content, so no engagement pods. Post links are `nofollow`.
   - Facebook: Page posts with short text and one image or link preview. Post in groups only where the group's rules allow it and the post helps that group; the same link dropped into many groups is spam behaviour. Schedule through Meta Business Suite.
   - Instagram: links in captions aren't clickable, so the post must deliver the value on its own; use a carousel for steps and data, write alt text, and point to the link in bio or a Story link sticker. Captions run to 2,200 characters. Use the paid partnership label for sponsored content. Publish through Meta Business Suite, the app, or the official Instagram API for professional accounts.
   - Threads: 500 characters per post, conversational, one idea; links work, but the post should stand without them. Publish from the app or the official Threads API.
   - Pinterest: a vertical image (2:3, such as 1000 x 1500 px), a descriptive title (up to 100 characters) and description (up to 500) using the words people search, and one destination link. Make a fresh image for each angle instead of re-pinning the same pin. Strongest for visual how-tos, recipes, products, home and craft topics; weak for most B2B.
   - Bluesky: 300 characters, link cards, alt text on images. Its open API makes automation easy; the human-approval rule still applies, and spammy behaviour gets accounts labelled or removed.
   - YouTube: Posts (formerly the Community tab) take text, images, polls and quizzes where the channel has access. Shorts descriptions don't show clickable external links (YouTube removed them in 2023; check current help), so link through the channel profile or a related video. Description links pass through a redirect: referral value only.
   - Google Business Profile: an update, offer or event post with up to 1,500 characters, a photo, and one button such as "Learn more". Don't put phone numbers, emails or social handles in the post text: Google says it may remove posts with unverified contact information, so use the "Call now" button. Hotels can't create offer posts. Keep it local and current.
6. **Add UTM-tagged links.** Every link back to the site carries UTM parameters, lowercase and consistent.
   - `utm_source` = the platform (`linkedin`, `x`, `facebook`, `instagram`, `threads`, `pinterest`, `bluesky`, `youtube`); `utm_medium=social`; `utm_campaign` = the page slug; `utm_content` = the angle ID. For Google Business Profile, `utm_source=google&utm_medium=organic&utm_campaign=gbp-post` keeps it in organic while staying separable.
   - Link to the exact section when the page has heading anchors (`#pricing`), not just the top.
   - No personal data in UTMs, no UTMs on internal links, and no link shorteners that hide the destination.
7. **Remove near-duplicates.** Compare every draft with every other draft and with the account's posts from the last 90 days.
   - No sentence of ten words or more appears in two posts, no two posts open the same way, and no post is the page's intro reworded. Rewrite any that fail.
   - Two accounts (founder and company) sharing the same text is a near-duplicate too; the company can reshare with its own comment instead.
8. **Get human approval.** Put the drafts in one review sheet: platform, account, angle, post text, image and alt text, link, disclosure, planned date.
   - The approver checks facts against the page, claims allowed in the category, image rights, disclosures and tone, then marks each post approved, edited or rejected.
   - Anything edited after approval goes back for approval. Nothing is published with status "draft".
9. **Schedule at a pace people can stand.** Spread one page's posts over 3 to 6 weeks, at most one post per account per day from the same page, mixed with the account's other content.
   - Template: week 1, LinkedIn post (angle A), X thread (angle B), Google Business Profile update if local; week 2, Instagram carousel (C), Pinterest pin (D), Facebook post (A rewritten); week 3, Threads and Bluesky posts (B and E), YouTube Post (C rewritten); weeks 4 to 6, the best performer's second angle on its best platform.
   - Publish only by hand, with native schedulers, or through official-API tools. Someone checks replies within a day of each post; an unanswered question under your own post wastes it.
10. **Measure, then keep or retire angles.** Read results at 7 and 28 days.
    - Platform: impressions, engagement rate, saves or shares, link clicks. Site: sessions, engaged sessions and conversions by `utm_campaign` and `utm_content`. Also watch branded search impressions in Search Console over the following months, and label any connection to these posts `inferred`, because many things move branded search.
    - Retire an angle that lands below half the account's median engagement rate on two platforms. Keep winners in an angle log and reuse the pattern on the next page, not the same words.
    - Never buy followers, likes or views to rescue a post.

## What to hand back

Fill in this template. Every recommendation gets a priority label and an evidence label with confidence.

```markdown
# Posts from [page title], [date]

**What I found:** [one line, e.g. "7 usable angles; the pricing benchmark and the setup mistake are the strongest."]
**What matters most:** [one line]
**What to do first:** [one line]

## Source page
- URL: [url]; last updated: [date]; main claim: [one sentence]; target query: [query]

## Angles kept
- A: [type] [one-line angle] - page section: [heading] - platforms: [list] - [Fix next | Worth doing] ([seen], high)

## Angles dropped
- [angle]: [why, e.g. not specific, duplicates A, claim not sourced on the page]

## Drafts (all awaiting approval)
### [Platform] - [account] - angle [ID] - planned [date]
[post text]
- Link: [URL with UTM] - Image: [file] - Alt text: [text] - Disclosure: [text or none needed]
- Status: awaiting approval

## Schedule
| Week | Platform | Account | Angle | Approved by |
|---|---|---|---|---|

## Measurement sheet
- Read at day 7 and day 28: [metrics per platform]; retire rule: [rule]

## What I could not check
- [e.g. current character limits, past post analytics, image rights, whether YouTube Posts are enabled]
```

## Stop and flag if

- The user wants posts published without human approval, through browser automation or unofficial tools, or across extra accounts the brand doesn't openly run. Decline that part.
- The user asks to buy followers or engagement, join pods, or mass-post to groups or communities. Decline and explain the platform rule.
- The page makes health, financial, legal or safety claims. Posts need sign-off from someone qualified, and some platforms restrict that content.
- You'd post on accounts the user doesn't control. Access must come through the platform's role or admin system, never shared passwords.
- The page is thin, wrong or out of date. Fix it first.
- Unacceptable output: the same text on several platforms, invented statistics, drafts without an approval status, links without UTM tags, or any claim that these posts build SEO link value.

## Next step

- Run `parasite-seo-plan` if it hasn't been run, to check these platforms show up for the site's target searches at all.
- Run `reddit-quora-answers` for the angles that answer questions people are already asking in ranking threads.
- Run `ai-traffic-analytics` after 28 days to read referral and conversion results alongside AI referrals.

---
Part of the free RomeoSEO skill library: https://romeoseo.com/skills

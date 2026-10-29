---
name: store-listing
description: Write the App Store and Google Play listing from evidence instead of taste. Picks keywords by checking who already owns each phrase and whether a small app can win it, spends the name and subtitle on one lane, writes the descriptions and the first three screenshot captions, finds a screenshot look to copy from real listings, and keeps a dated keyword file so every later change can be measured. Use when the user is writing or rewriting a store listing, asks for keywords, ASO, a subtitle, screenshot captions or screenshot ideas, or when the ship skill reaches the store listing step.
---

# Store listing

The listing decides two things: whether the app turns up in search, and whether the
person who sees it taps Get. Most first listings are written from taste, sound fine,
and rank for nothing. This skill writes it from evidence, then records what it chose
so the next change can be measured against it.

It produces two files in the project (default `store/`, or wherever the project keeps
its store files):

- `store/listing.md`: the values to paste, from the ship skill's
  `templates/store-listing.md`. This skill fills the copy and screenshot sections;
  ship fills privacy answers and review notes.
- `store/keywords.md`: the evidence, from `templates/keywords.md`. Candidate
  phrases, how much each is searched, who owns it, the rank checks over time, and a
  change log.

Character limits and screenshot sizes live in the ship skill's `references/facts.md`.
Read them from there, never from memory.

## The rules that shape everything

1. **The name is the field doing the work.** Every source agrees the order is name,
   then subtitle, then the keyword field. Nobody has a trustworthy multiplier. From
   experience (a meal planning app, September 2026): it ranked 3 for the exact
   phrase in its name and was absent past 100 for a phrase written word for word in
   its subtitle. Put the phrase you most want to be found for at the start of the
   name, with the brand after it ("Baby Prep Checklist: Brand"). The icon label on
   the home screen is set in the app, not by this field, so it can stay the brand.
2. **One lane.** The name and subtitle give you about 60 characters that count. An
   app that does three things and spends them on three lanes is too small in all
   three. Pick the one use case people search for most and that converts, and spend
   both fields there. Secondary features go in the keyword field, never repeated.
3. **Popular is not winnable.** A phrase searched a lot is usually held by apps with
   tens of thousands of ratings. A new app wins phrases whose top 10 already holds
   small apps, especially small apps with the phrase in their name. Check that with
   the script (step 3) before choosing anything.
4. **Write from what the app does today.** Nothing it cannot do yet, no "best" or
   "number one", no prices in screenshots, and the project's own copy rules (read
   the rules file: banned punctuation, words the app avoids, the name to use).
5. **Change one thing at a time, and write it down.** Without a dated baseline, a
   later rank or conversion change cannot be explained.

## 1. Read what exists

- The rules file, for copy rules, the app name, platforms and whether the app is
  live yet.
- An existing `store/keywords.md` or listing doc. If one exists, this is a rewrite:
  start from its baseline and change log, and do not throw away the history.
- The app itself (screens, onboarding, paywall) for what it really does and the
  words it uses. The best keywords are often the user's own words for the problem.
- If the app is live: ask for the App Store Connect numbers for the last 90 days
  (impressions, the share from App Store search, product page views, first time
  downloads). Write them into the baseline. Note which figures are opt in only
  (they count only users who share data with developers) and never compare them
  against complete ones.

## 2. Gather candidate phrases

Aim for 20 to 40 phrases, two or three words each, from places people actually type:

- **Apple's search suggestions.** Type the start of a phrase into App Store search
  on a phone and record what it suggests. Suggestions are real searches.
- **Google Play's suggestions**, the same way, for the Play listing.
- **Competitors' names and subtitles.** Run the script on the obvious phrases (step
  3) and read the names of the apps that come back; the words they spend their
  name on are their own best guess.
- **The user's words.** How a person describes the problem before they know the app
  exists ("hospital bag list", not "prep management").
- **Expansions** of each seed: "<phrase> for <who>", "<phrase> list", the problem
  as a person states it. Then check each in the suggestions; keep only real ones.

Count how many of the top competitors use each word in their name or subtitle. A
word nearly all of them use is the category's price of entry (use it); a word only
one or two use is a chance to own something; a word none use is either a gap or a
word nobody searches, and the demand check decides which.

Leave out words that waste characters: "app" and "free", the category name, and the
app's own brand, which it will rank for regardless.

## 3. Check demand and who owns each phrase

**Demand.** Apple shows a free popularity score in Apple Ads (formerly Apple Search
Ads). Sign in with the App Store Connect account, start creating a Search Results
campaign, choose the country, and on the ad group step read the popularity dots
beside each keyword. Stop there: with no payment method added, nothing runs or is
charged. The scale is 1 to 5 dots, coarse and relative. A 1 means low compared with
the whole store, not zero. Paid tools rescale the same number to 0 to 100; it is not
more precise. The screens move; if they differ, say so and ask the user to read the
dots off their own screen.

**Who owns it.** Run, from this skill's folder:

```
node scripts/keyword-check.mjs "phrase one" "phrase two" --country us
```

It asks Apple's public search API (no key) for the top 10 apps per phrase and prints
each one's rating count and whether the phrase is in its name. Its order is close to
the phone's but not identical: use it to judge the competition, not as your rank.

Score each phrase in `store/keywords.md`:

| Read | Meaning |
| --- | --- |
| Several of the top 10 under 100 ratings, and some have the phrase in their name | Winnable now. These are the targets |
| Top 10 all in the thousands or more | Not winnable at launch, whatever the metadata says. Use it as a positioning word on the page, not a target |
| 1 dot and nobody searches it | Easy to win and worth nothing. Fine in the keyword field, never in the name |

A good name phrase has 2 or more dots and is winnable. If nothing is both, take the
most searched winnable phrase and say plainly that search will bring few installs at
first, and that off store traffic (the app's own site, social posts, links) is what
moves the numbers until the app has ratings.

## 4. Write the App Store fields

- **Name:** the chosen phrase first, then the brand. Within the limit.
- **Subtitle:** the second phrase in the same lane, as a benefit a person would say
  ("Hospital Bag and Baby Checklist"). No words already in the name.
- **Keyword field:** single words, commas, no spaces after commas, no word already in
  the name or subtitle (Apple combines words across the three fields, so "baby" in
  the name plus "registry" here can match "baby registry"). Fill the limit. No competitor
  brand names: Apple's guidelines (2.3.7) forbid other apps' names in metadata.
- **Promotional text:** the one App Store field that changes without a new version.
  Use it for what is new or seasonal. It is not indexed.
- **Description:** not indexed on the App Store, so write it for the person reading,
  not for search. First three lines are what shows before "more": what it does, for
  whom, and the main thing someone does with it. Then short sections. Nothing the
  app cannot do.
- **What's new:** for users, in plain words, not a commit log.

Name, subtitle and keyword changes only go live with a new app version. Plan them
with a release.

Extra keyword slots through other localizations are widely recommended (the US store
is reported to index several other locales' fields). Do not use it by default:
practitioners report rank losses when a listing claims languages the app binary does
not declare, and nobody has shown how the two are matched. Offer it only as an
experiment the user chooses, with the risk stated.

## 5. Write the Google Play fields

Play is different and the difference matters:

- **The full description is indexed.** Find real phrases from Play's search
  suggestions and use them naturally in the description, a few times each, in
  sentences a person would read. Stuffing gets the listing rejected or ignored.
- **Short description:** one line, a benefit, with the main phrase in it.
- **Title:** the same phrase first idea as the App Store name, within Play's limit.
- Play has no keyword field. Do not copy the App Store keyword field anywhere.

## 6. Screenshots: captions first, then a look to copy

The first three screenshots show in App Store search results at thumbnail size, and
most people decide from them without opening the page. Plan three strong screens
first. Three is a fine full set for a new app: Apple requires at least one per size
and Play at least two (check `references/facts.md`). Add more later only if they say
something the first three do not.

**Captions.** One per screenshot, in order, telling the loop in three steps (for
example: save it, it sorts itself, see what is missing):

- Sell the outcome, not the feature ("Every saved post, sorted for you", not
  "Category view"). Starting with a verb helps.
- No welcome screen and no sign in screen in the first slot.
- Short enough to read at thumbnail size: about 3 to 6 words for the headline, and
  an optional smaller line under it.
- The first caption carries the one thing no competitor can show.
- Screen under the caption: a real screen with realistic content, never an empty
  state. The see-it-work skill can seed data and capture it.

Write them into the screenshots table in `store/listing.md` with the screen each one
sits on.

**The look.** The user does not need a perfect reference, just one they like. Find
two or three real listings to copy the layout from:

1. Run the script with `--shots` on the target phrases. It prints the screenshot
   links of the apps that rank; open them and look. These are the live listings, so
   they count as seen.
2. Or the user browses a screenshot gallery (see Tools below) and sends the ones
   they like.

Then name what to copy from each: background (solid, gradient, photo), caption
position and size, whether the phone is framed, tilted or full bleed, and how many
words. The user builds them in a screenshot editor from a template that matches.

Before upload, check every image against the sizes in `references/facts.md`, no
transparency, and that the captions match the language of the listing.

**Preview video** (optional): it autoplays muted in search, so it must work with no
sound, and Apple's guidelines (2.3.4) say previews may only use screen captures of
the app itself.

## 7. Record the baseline and the change log

In `store/keywords.md`:

- **Baseline:** the date, the app version, the current fields word for word, and, if
  live, the App Store Connect numbers from step 1.
- **Rank checks:** for each target phrase, search it on a phone in the target
  country and count down the results to 50. Record the position or "beyond 50".
  Autosuggest position is a different signal; do not mix them.
- **Change log:** every listing change with the date and version it shipped in.

Then tell the user the routine: re-check the same phrases the same way every week or
two after a change, change one field at a time, and once the app has a few hundred
product page views a month, test the first three screenshots with Apple's Product
Page Optimization (free, in App Store Connect) rather than trusting anyone's claimed
conversion numbers. A practitioner rule of thumb for the keyword field: a phrase
sitting at 11 to 20 is worth moving into the subtitle or name; a phrase still past 50
after a month is worth replacing.

## 8. Show the user

Lead with the chosen name, subtitle and keyword field, each with its character count
and the one reason it was chosen (the phrase's dots and who owns it). Then the three
captions. Then anything that needs their decision. Every line in the listing is
theirs to approve before anything is pasted into a console.

## Tools

Point at these, do not depend on them. Checked 2026-10.

- **AppScreens** (appscreens.com): screenshot editor with templates and device
  frames. Free tier.
- **AppLaunchpad** (theapplaunchpad.com/app-screenshot-inspiration): a gallery of
  real App Store screenshot sets, with an editor.
- **Mobbin**, if connected: real in app screens, which is what the reference-hunt
  skill uses. It is not a gallery of store screenshots.
- **Eronred/aso-skills** (github.com/Eronred/aso-skills, MIT, active): a wider set of
  ASO skills (custom product pages, review replies, more keyword workflows). Its
  live data needs a paid API; its frameworks work without it. Where its files
  disagree with each other (whether Apple indexes the three fields together or
  apart), the together reading is the one used here.
- **Screenshot MCP servers** (AppScreenshotStudio, Screenies, ButterKit) were looked
  at and are not recommended: all paid, all lay out your own captures only, and none
  can show you other apps' listings. AppScreens and AppLaunchpad have no API or MCP
  server.

## Finish

The skill is done when `store/listing.md` has every copy field and the screenshot
plan filled within the limits, `store/keywords.md` has the scored phrases, the
baseline and an empty change log, and the user has seen and approved the fields.

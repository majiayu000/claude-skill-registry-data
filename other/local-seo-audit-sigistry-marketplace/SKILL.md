---
name: local-seo-audit
description: Audit how a local business shows up in Google Maps and the map pack. Use for "audit my Google Business Profile", "why am I not in the map pack", "local SEO audit" or before opening, moving or merging locations. Covers profile fields, reviews, NAP citations, location pages, service areas and geo-grid rank checks.
license: MIT
metadata:
  author: RomeoSEO
  version: "3.0.0"
  homepage: https://romeoseo.com/skills/local-seo-audit
---

# Local SEO audit

Checks how a business with a storefront or a service area shows up in Google Maps and the local pack (the map with three businesses under it): the Business Profile itself, its reviews, whether its name, address and phone match across the web, the location pages on its website, and where it actually ranks across the area it serves. Hands back a prioritised fix list and a field-by-field Business Profile checklist.

> **Romeo's rule:** Nobody can move your shop closer to the searcher, so spend the effort on what you can control: the right category, real reviews, and a page that proves you are actually local.

## Use this when

- A business with a storefront or service area doesn't show in the map pack or Google Maps for its main services, or only shows near its front door.
- Someone asks to "audit my Google Business Profile" or "do a local SEO audit".
- Calls, direction requests or website clicks from the Business Profile have dropped.
- The profile was suspended, an edit was rejected, or Google asked for re-verification.
- The business is opening, moving, renaming or merging locations.

## Don't use this for

- Crawling, indexing or speed problems on the website itself → `technical-seo-audit`
- Writing and validating the LocalBusiness JSON-LD in full → `schema-markup`; a full review of the site's link profile → `backlink-profile-review`
- Planning dozens of city or service-area pages from a template → `programmatic-seo-plan`
- Whether ChatGPT, Gemini, Copilot, AI Overviews or Siri name the business for "near me" questions → `local-ai-visibility`; a review programme on Yelp, Tripadvisor, trade sites and the other platforms AI answers cite → `reviews-for-ai-answers`

## What you need

### Required
- Business name, website, and for each location the Google Maps link (or the exact name plus city).
- How customers are served: storefront (they come to you), service-area (you go to them) or hybrid, plus the areas served.
- The main services in order of value, and the 3 to 5 searches a customer would type ("emergency plumber", "dentist near me").

### Helpful
- Owner or manager access to the Business Profile, used read-only: categories, Performance data (calls, directions, website clicks, searches) and review history.
- Search Console data for the location pages.
- Old names, addresses and phone numbers the business has used, and directory listings it knows about.
- A geo-grid rank export from an optional tool such as Local Falcon or BrightLocal.
- The competitors that usually appear in the pack.

### No tools?
Everything except the private profile fields can be checked in a browser. Open the public profile in Google Maps in a private, signed-out window. Read location pages with view-source and test them in the Rich Results Test. Search the business name, phone number and old addresses to find citations and duplicates. Run the geo-grid by hand (step 10) with the location override in Chrome DevTools. Ask the owner for screenshots of the categories, services and Performance screens.

## Ground rules

- Google says local results are ranked on relevance, distance and prominence. Distance is fixed: one address can't rank everywhere in a city, and nobody can sell you that.
- The primary category is the strongest relevance lever you control. Pick what the business *is*, as specifically as possible, and check what the businesses already in the pack use.
- The business name is the real-world name on the signage, website and paperwork. Keywords or a city added to it break Google's guidelines and invite suspension, even when they seem to help for a while.
- A steady flow of genuine, recent reviews with owner replies matters more than a perfect 5.0. Ask every customer the same way; never filter who gets asked and never reward anyone for a review.
- Name, address and phone consistency (NAP) matters most on the handful of sources Google and customers actually use. Hundreds of directory submissions are not a strategy.
- A location page earns its place with local proof. The same template with the city name swapped is a doorway page, not a location page.
- Treat profile edits as risky. Google reviews changes to core fields (name, address, category), and several big changes at once can trigger re-verification or a suspension check.
- Map-pack rankings are a grid, not a number. "We rank #2" measured from the office only describes the office.
- Read-only by default: draft profile changes, posts and review replies; publish nothing without permission for that specific change.

## Steps

1. **Confirm the setup and find every profile.**
   - Storefront, service-area or hybrid? Count real, staffed locations.
   - Search Maps for the business name, old names, the phone number and the address. Duplicate or unclaimed profiles split reviews and confuse ranking: `Fix now`. Request a merge or removal through Business Profile support; never delete the verified one.
   - Virtual offices and unstaffed addresses are not eligible. Co-working spaces qualify only with permanent signage and your own staff there during opening hours. Flag ineligible profiles before optimising anything.
2. **Categories.**
   - The primary category shows under the name on the public profile. Secondary categories are not public: get them from the owner's dashboard or a browser extension that reads them.
   - Search each money query from the business's area and note the primary category of the top 3 pack results. If theirs fits the business better than its own, that change is usually the biggest single fix: `Fix next`, or `Fix now` when the current category is plainly wrong.
   - Secondary categories: add ones for services the business really provides (`Fix next`). Categories for things it only sells, or for neighbouring businesses, break the guidelines: remove them.
   - Changing the primary category back and forth does more harm than living with the second-best one. Change it once, with a reason.
3. **Name, address and service area.**
   - Name: compare the profile with signage, website and registration. Keywords, city or tagline added: `Fix now` (suspension risk). If the owner wants the keyword in the name, the only clean route is a real rename, signage included.
   - Address: exact, with suite or unit, matching the website. No P.O. boxes. After a move, the old address still live on Google, Apple or the website: `Fix now`.
   - Service-area business: if customers are not served at the address, remove the address from the profile and list only the service area. Google allows up to 20 service areas (cities, postcodes or regions, not a radius) and asks that the overall area stay within about 2 hours' driving of the base.
   - Adding more service areas to rank in more towns: `Leave it`. The list describes where you go; ranking still appears anchored to the verified location (inferred, widely observed).
4. **Hours, phone, website link, attributes.**
   - Regular hours as customers experience them, and special hours for every public holiday. Missing special hours: `Fix next`; people arrive at a locked door and leave a review about it.
   - Phone: a local number that reaches this location. With call tracking, set the tracking number as primary and the main number as an additional phone, so the profile still matches citations.
   - Website link: single location → homepage; several locations → each location's own page. Every branch pointing at the homepage, or a link that redirects or returns 404: `Fix next`. Add UTM parameters (`?utm_source=google&utm_medium=organic&utm_campaign=gbp`) so profile traffic is separable in analytics; a self-referencing canonical on the page usually keeps the tagged URL out of the index.
   - Booking link, attributes (accessibility, payments, amenities) and opening date: fill in what is true. `Worth doing`.
5. **Profile content: services, products, photos, description, posts, Q&A.**
   - Services and products: list each real service with a plain description, and a price where the owner is happy to show one. Match the website's wording. Empty: `Fix next`.
   - Photos: exterior (so people recognise it on arrival), interior, team, real work. Replace stock images. Geotagging photos: `Leave it`; there is no good evidence it does anything.
   - Description (up to 750 characters, no links): what the business does and for whom. Rewriting it to fit in keywords: `Leave it`.
   - Posts (updates, offers, events): useful for conversion and for showing the profile is looked after; any ranking effect is unproven. `Worth doing`.
   - Q&A: Google shut the Q&A API in November 2025 while reworking the feature, and profiles have been moving to AI answers built from the profile, website and reviews. Check what the live profile shows today before advising anything, and don't sell "Q&A seeding". Make sure the facts customers ask about (parking, prices, areas covered, insurance, accessibility) are on both the profile and the website. Whether AI assistants recommend the business at all → `local-ai-visibility`.
   - Business Profile chat ended in July 2024. Drop any advice or widget that relies on it.
6. **Reviews.**
   - Record total count, rating, reviews in the last 90 days, date of the newest review and the share with an owner reply. Record the same for the top 3 pack competitors from their public profiles. Count; don't estimate.
   - Recency gap (nothing in 2 to 3 months while competitors get reviews weekly) usually hurts more than the rating: `Fix next`. Fix it with one ask-every-customer routine: the review link from the profile dashboard sent in the follow-up email or receipt, or a QR code at the counter.
   - Policy breaches, each `Fix now`: review gating (asking "how did we do?" and sending only happy customers to Google), discounts or prize draws for reviews, reviews from staff or family, pressuring people to review on the premises, asking for specific wording. Google removes these reviews and can restrict or suspend the profile. Fake or suppressed reviews are also illegal in some markets: the US FTC rule (in force since October 2024) and the UK DMCC Act (fake-review rules since April 2025). Check local law.
   - Owner replies: answer every negative review calmly, offer a way to continue offline, keep positives short and specific. In healthcare, legal and similar fields, never confirm in a reply that someone is a patient or client (privacy law, e.g. HIPAA in the US).
   - Only reviews that break Google's policies (conflict of interest, off-topic, abusive) can be reported for removal. Merely negative ones stay.
   - Reviews beyond Google (Yelp, Tripadvisor, Facebook, trade sites) are this audit's scope only as counts and recency; building an honest programme on the platforms customers and AI answers use → `reviews-for-ai-answers`.
7. **NAP consistency and citations.**
   - The reference NAP is the Business Profile plus the website footer or contact page. Those two must match first.
   - Then check the sources that matter in this country and industry: Apple Business (formerly Apple Business Connect; it controls Apple Maps listings), Bing Places, Facebook, and the main local and trade directories. Which ones count varies by country (Yelp carries weight in the US, Yell in the UK, Gelbe Seiten in Germany) and by trade (Avvo, Healthgrades, Houzz, Tripadvisor). Find them by searching the brand name, and the category plus city, and noting which directories rank.
   - Old address or phone on Google, Apple, Bing or a directory that ranks for the brand: `Fix now`. On a minor directory: `Worth doing`. "St" vs "Street", "#4" vs "Suite 4": `Leave it`.
   - Packages that submit the business to hundreds of low-quality directories: `Leave it`.
8. **Location pages on the website.**
   - One page per real location, each with: the same NAP as its profile, hours, directions and parking, photos of the actual place and team, services available there, reviews from local customers, and anything genuinely local (permits, regulations, neighbourhoods served, nearby projects).
   - Pages for towns with no location: only where the business has real work and proof there. Template pages that differ only by town name are doorway pages under Google's spam policies: `Fix now` when there are many; merge them into fewer, stronger pages.
   - LocalBusiness markup: the most specific type (Dentist, Plumber, AutoRepair), with name, address, telephone, url, openingHoursSpecification and geo (at least 5 decimal places), describing that location only. Don't mark up the business's own reviews as aggregateRating; Google doesn't show stars for self-serving LocalBusiness reviews. Missing markup: `Worth doing`. Markup that contradicts the profile (old address, wrong hours): `Fix next`. Hand the writing to `schema-markup`.
   - Store locator: every location page must be reachable through a plain `<a href>` link, not only through a JavaScript map widget.
9. **Local links and mentions.**
   - Look for links only a real local business can get: suppliers' and manufacturers' "where to buy" pages, trade associations, chambers of commerce, sponsorships, local news, community events, partner businesses.
   - If a backlink export for the top pack competitors was provided, list the local sites linking to them that would plausibly link to this business too. Without data, write "not checked".
   - Paid "local link packages" and private blog networks: `Leave it`, and remove them from any plan.
10. **Rankings: sample a geo-grid.**
    - The pack changes with where the searcher stands, so measure from many points. Lay a grid over the service area centred on the business: about 5 x 5 points, 0.5 to 1 km apart in a dense city and 3 to 5 km apart in rural areas.
    - By hand: Chrome DevTools → More tools → Sensors → set the location to each point's latitude and longitude, allow location, search Google in a private signed-out window, and record whether the business is in the pack (1 to 3) or its position in the Maps list, plus who holds the top 3. Keep it to 3 to 5 queries; it is slow. If results don't change between distant points, Google is ignoring the override: check the location it says it used, where the results page shows one.
    - Optional tools (Local Falcon, BrightLocal and similar) automate the same grid. Note date, device and query; positions move daily.
    - Reading the grid: strong near the address and fading fast is normal in crowded categories. Weak even at the address points to relevance or prominence (category, reviews, website). Strong only on a competitor's side of town: check for a duplicate profile or a misplaced map pin.
    - Never fill a grid cell with a guessed position. Unchecked points are "not checked".
    - With owner access, compare Business Profile Performance (calls, direction requests, website clicks) year on year, not month on month, to separate seasonality from a real drop; the searches breakdown shows which terms surfaced the profile.
11. **Multi-location setups.**
    - One profile per real location, the same brand name on each (no "Brand - Downtown" unless the signage says so), the same primary category for locations offering the same service.
    - 10 or more locations: use a business group, bulk verification where eligible, and store codes.
    - Departments and individual practitioners (a dealership's service department, doctors in a clinic) can sometimes have their own profiles. Check Google's current guidelines first; overlapping profiles compete with each other.
12. **Suspension and re-verification risk.**
    - Risk factors: keyword-stuffed name, virtual or unstaffed address, P.O. box, duplicate profiles, a service-area business showing an address customers can't visit, several core edits at once, a move without signage at the new address.
    - If suspended: don't create a new profile. Fix the cause, gather proof (business registration, utility bill, photos of signage and premises) and submit one appeal through Google's Business Profile appeals tool. Check the appeal help page for current timings and accepted evidence.
    - Re-verification is often by video: the owner shows the signage, the location in context and proof of management (keys, tools, paperwork). Warn the owner before any edit that could trigger it.

## What to hand back

Fill this in for each location; keep an evidence label and confidence on every finding.

```markdown
## Summary
What I found: <one sentence>
What matters most: <one sentence>
What to do first: <one sentence>

## Fix list
1. [Fix now] <plain-English problem> (<term>)
   Evidence: <seen | tool | inferred>, <high | medium | low> confidence. <what you observed, where>
   Fix: <exact change, who makes it, where>
2. ...

## Business Profile checklist: <location>
- Primary category: <current> → <recommended> | <priority> | <evidence>
- Secondary categories: <current> → <add / remove> | ...
- Business name: <current> | matches signage and website? | ...
- Address or service areas: ...
- Hours and holiday hours: ...
- Phone (primary / additional): ...
- Website link: <current URL> → <recommended URL> | ...
- Booking link and attributes: ...
- Services and products: ...
- Photos: <count>, stock images?, exterior shown? | ...
- Description: ...
- Posts: <date of last post> | ...
- Q&A or AI answers: <what the profile shows today> | ...
- Reviews: <count>, <rating>, <last 90 days>, <reply rate> | competitors: <same figures>
- Duplicate or unclaimed profiles: ...

## Geo-grid sample
- <query>: <grid and spacing>, <date>, <manual | tool name>, in pack at <x> of <y> points. Top 3 at most points: <names>.

## What I could not check
- <item>: <why>, and what would verify it
```

## Stop and flag if

- You can't tell which profile belongs to the business, or duplicates can't be resolved from public data. Ask before going further.
- The address is a virtual office, an unstaffed address, or a home address that should be hidden. Raise eligibility before any optimisation advice.
- The user asks for fake reviews, review gating, review incentives, a keyword in the business name, or a profile for a location that doesn't exist. Decline and explain the policy and legal risk.
- The profile is suspended. Stop recommending edits until the appeal is resolved.
- A step would change the live profile, publish a post, reply to a review or edit a citation. Draft it and get explicit permission first.
- The output contains a ranking, competitor review count or search volume nobody observed. Replace it with "not checked".

## Next step

- `schema-markup` with the location page URLs plus the confirmed name, address, phone and hours, to write the LocalBusiness JSON-LD.
- `on-page-seo-review` on the weakest location page, with its target query and the local proof found in step 8.
- `backlink-profile-review` with backlink exports for the business and its top pack competitors, to turn step 9 into a target list.

---
Part of the free RomeoSEO skill library: https://romeoseo.com/skills

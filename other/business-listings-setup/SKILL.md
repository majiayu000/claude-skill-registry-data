---
name: business-listings-setup
description: >
  Post-launch: claim Google Business Profile, Bing Places, and category
  directories, then verify the `sameAs` profiles already in schema actually
  resolve. The action skill for E-E-A-T's Authoritativeness component (owned
  by `website-content-guide`): other pages linking to or citing you are one
  signal search and AI answer engines read as authority. Human-in-the-loop,
  same shape as `search-console-setup` — the agent drafts every value, the
  owner clicks. Trigger phrases: "claim my Google Business Profile", "Google
  Maps listing", "Bing Places", "business listings", "improve E-E-A-T",
  "authoritativeness is thin", "sameAs profiles".
---

# Business listings + off-site authority

Search engines and AI answer engines do not take your word for your own authority.
A meaningful part of it is read off **other pages**: a business directory that lists
you, a partner site that links to you, a person who cites you in their own bio — a
page you do not control, saying you exist and are real. Nothing on your own site can
substitute for that, however well written, though it is one signal among several,
not the only one.

This skill claims the handful of external listings that matter most for a small
site, and checks that the profiles your schema already points to actually resolve.
It is the **action** step for the gap `website-content-guide`'s E-E-A-T section
names: knowing Authoritativeness is thin is only useful if it leads somewhere.
This is where it leads.

**What this skill is not.** It does not do cold outreach to strangers — no guest
posts pitched to sites with no relationship, no backlinks bought or begged from
people who have never heard of the entity. That is relationship work and
editorial judgment, not a checklist, and a skill that pretended otherwise would
overclaim. It claims listings you are entitled to claim, verifies links you have
already earned, and — in section 4 — prompts you to ask people who already have
a real connection to the entity (a partner, a sponsor, a speaker) for the link
that naturally follows from that connection. Nothing here pays for a link or
approaches anyone with no prior relationship.

> **Run this only if the site represents a real, named, claimable entity** — an
> event series, a studio, a local business, a sole proprietor or consultant
> trading under their own name, or a named community or organization. Skip it
> for a personal blog with no business or practice behind it, or a resource hub
> with no identity of its own to list. If unsure, ask the owner: "does this have
> a name someone could search for on Google Maps or a directory?" A no means skip.
>
> **Human-in-the-loop:** creating accounts on Google/Microsoft/directory platforms,
> and any identity verification they require (a postcard, a phone call, a video
> call), are actions only the owner can do. The agent drafts every field value it
> has real data for — the name (§1 step 3), category, description, hours, and the
> `sameAs` URLs. Address and phone number are not in `config.ts`; get those
> directly from the owner rather than guessing, and the owner pastes and clicks
> throughout.

> **Console UI labels are localized** — translate the quoted labels if the owner's
> account language is not English (German: *Unternehmensprofil erstellen*,
> *Standort hinzufügen*, *Kategorie*, *Verifizierung*).

## 1. Google Business Profile — the biggest single lever

This is the one that feeds Google Maps, the local pack, and the knowledge panel
that can appear beside search results for the entity's own name.

0. 🧑 **Check eligibility before starting.** Google Business Profile requires a
   genuine customer-facing interaction — either a real address customers visit, or
   staff who travel to perform a service at a customer's location. "Named entity"
   is not itself sufficient: a purely online community, or an event series with no
   physical venue, may not qualify for any category, and Google can reject or
   suspend a profile that does not meet this bar. If the entity is genuinely
   location-based (a studio, an office, a recurring venue), continue; if it is
   online-only, skip to section 3 and rely on `sameAs` and directories instead.
1. 🧑 **Search for the business first** — on Google Maps or in Business Profile's
   own "Add your business" flow, search the exact name and address before
   creating anything new. A listing may already exist (created by a customer
   review, a data aggregator, or a past employee) — claim or request access to
   that one rather than creating a duplicate, which risks a suspended profile
   and split reviews.
2. 🧑 If nothing exists to claim, go to https://business.google.com and sign in
   with the account that should own the listing — an account the organization
   itself controls (not one person's personal login shared around; Google
   Business Profile supports adding named managers/owners individually, which
   is the right way to give a team access).
3. 🧑 **Add your business** → enter the real, customer-facing name — the same one
   in `SITE.name`, which the starter's Organization schema carries as
   `alternateName` (schema's `name` field holds `COMPANY.legalName`, the legal
   entity name, which is deliberately not always the same string — use the
   public-facing one here, not the legal one, since that is what customers
   actually search for).
4. 🤖 Draft the category, description, website URL, and hours from the site's own
   content — do not invent anything not already stated on the site.
   - **Category:** pick the closest official Google category that matches how the
     entity actually operates. **"Service area business"** applies only when staff
     genuinely travel to serve customers at their location, with the city/region
     listed instead of a street address — it is not a default for "has no office."
   - **Description:** reuse the positioning statement from `POSITIONING.md` if the
     site has one, trimmed to Google's limit. Do not write new marketing copy here.
   - **Website:** the production domain, not a preview URL.
   - **Address and phone:** not in `config.ts` — ask the owner directly rather
     than guessing or leaving them blank.
5. 🧑 Complete verification. Google offers postcard, phone, email, or video
   verification depending on the category and account history — the options shown
   are Google's choice, not something to work around.
6. 🧑 Once verified, publish the profile.

## 2. Bing Places for Business — the Bing-side equivalent

Smaller reach than Google, same mechanism: a claimed, verified listing in the
index Copilot's search grounding draws on, not a guaranteed direct feed into any
specific Copilot answer.

1. 🧑 Go to https://www.bingplaces.com and sign in with a Microsoft account.
2. 🧑 Check **"Import from Google"** first — if the Google Business Profile above is
   already live, this can pull the listing across and skip re-entering everything.
3. 🤖 If importing is not available, draft the same fields as §1 step 4 (category,
   description, website, hours) from the same source — the site's own content,
   not invented copy. Address and phone still come directly from the owner.
4. 🧑 Complete whatever verification Bing requires and publish.

## 3. Verify the `sameAs` profiles actually resolve

`website-content-guide`'s E-E-A-T section calls for `sameAs` profiles that
**actually resolve** — Organization/Person schema pointing at LinkedIn, GitHub, a
public register, and so on. The schema plumbing itself lives in `website-seo-geo`
and `config.ts` (`SAME_AS`); this skill is the check that what it points at is
real.

1. 🤖 Read the current `SAME_AS` array (or equivalent) out of `config.ts` /
   `Organization` schema.
2. 🤖 Fetch each URL — reuse `outgoing-link-audit`'s fetch mechanics (its script
   form is at `skills/new-website/templates/astro/scripts/check_external_links.sh`,
   copied into every scaffolded site) but apply this section's own, stricter
   status policy below, not that script's: deleting a real authority signal is a
   worse mistake than flagging a broken outbound link, so this is deliberately
   more conservative than the script's own classification — **do not treat a
   non-200 as dead on the first try**: a **404/410** is unambiguous — the server itself says the resource is
   gone — so that alone is genuinely dead; a **5xx** is the target's own server
   failing, not proof the profile is gone, so re-checking once is not enough
   evidence to remove it either — treat 5xx as **unverified** until a human
   confirms it, logged out, in a real browser, same as a bot-block; 403/429/999/
   timeout is usually a bot-block (LinkedIn and similar platforms routinely
   return these to automated fetches) and also counts as **unverified**; a URL
   that redirects to a **different domain** (and returns 200 there) is neither
   dead nor healthy — it may point at a renamed or rebranded profile and needs a
   human look, the same as `outgoing-link-audit`'s own REBRAND/MOVED case.
3. 🧑 For anything **confirmed dead** (real 404/410 only): claim the missing
   profile, fix the URL, or remove the entry. For anything **unverified**
   (5xx, bot-block, or redirect-to-different-domain): check it yourself, logged
   out, in a real browser before touching schema — do not remove a `sameAs`
   entry on an automated fetch failure alone, that would delete a healthy
   profile the toolkit's own fetch just couldn't reach.
4. 🤖 Add the Google Business Profile and Bing Places listings (sections 1 and 2
   above, not this section's own steps 1-2) to `SAME_AS` once they are live and
   verified — use the **public listing URL** (the Google Maps place page, the
   public Bing Places listing) that a visitor or crawler can actually open, never
   the private dashboard/management URL used to edit the listing.

## 4. Category-relevant directories — a short list, not an open crawl

Pick from the site's actual category. This is deliberately a **short, curated**
list, not "submit everywhere" — low-quality directory link farms have net-negative
value and some actively hurt trust signals. If nothing in the category has a
directory worth being listed in, say so and move on — "no suitable directory
found" is a valid outcome, not a gap to keep chasing.

- **Event / community site:** Meetup, Eventbrite, lu.ma, and any local
  tech-community hub or aggregator that already covers the region.
- **Local business or studio:** the 2–3 directories that are actually authoritative
  for that trade in that region (ask the owner which ones their peers use — this is
  local knowledge, not something to guess).
- **Any site:** if a partner, sponsor, or speaker already has their own site, ask
  whether they would link to the event/organization page they took part in — this
  is the highest-value, lowest-effort link available, because it is editorially
  justified and already half-earned. `website-testimonials` is the sibling skill
  for the testimonial itself; this is the follow-up step of asking for the link
  that goes with it.

🧑 Submitting to each directory is a human action (most require an account and a
human-verified claim); 🤖 draft the listing text from the site's own copy for each
one so the owner is pasting, not writing, at every step.

## 5. Confirm it's working

- Search the entity's own name on Google — a Business Profile panel or Maps pin
  can appear once Google finishes processing the verified profile; there is no
  guaranteed timeline, so treat this as a check to repeat, not a one-time deadline.
- Search on Bing — same check for the Bing Places listing.
- Re-run the `sameAs` check in step 3; every URL is either confirmed live (200)
  or manually verified in a logged-out browser (for anything the automated
  fetch left unverified — a bot-block, a 5xx, or a redirect to a different
  domain), and points at the entity's real profile.
- This toolkit has no dedicated score for Authoritativeness. The honest way to
  see whether it moved is qualitative: ask an AI assistant to evaluate the
  site's E-E-A-T again after a few weeks and compare its answer to before —
  an informal check, repeated, not a packaged metric. This skill claims
  listings and verifies links; it does not itself measure the outcome.

## Scope notes

- This is **claiming and verifying what you are entitled to**, plus asking people
  with an existing connection for the link that follows from it (§4) — not cold
  link building or outreach. Guest posts, press pitches, and cold backlink
  requests are relationship work and stay a human decision, always.
- `internal-link-audit` and `outgoing-link-audit` cover the site's **own** link
  graph (links within the site, and links the site makes outward). Neither touches
  links pointing **at** the site from elsewhere — that gap is what this skill fills.
- The schema plumbing (`sameAs`, Organization/Person) is `website-seo-geo`'s
  contract; `website-content-guide` decides what signals to ship. This skill is the
  step that goes and makes those signals true, rather than aspirational.

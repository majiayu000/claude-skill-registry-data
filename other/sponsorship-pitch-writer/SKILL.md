---
name: sponsorship-pitch-writer
description: "Writes a sponsorship pitch email or one-page deck to a prospective brand partner, presenting the show's audience, format options, pricing, and the specific business case for why this brand should advertise on this podcast."
status: stable
category: podcast
subcategory: business
version: 1.0
eval_score: 4.4
tags: [podcast, business, sponsorship, monetization, pitch]
---
# Sponsorship Pitch Writer

## What This Skill Does
Writes a sponsorship pitch email or one-page deck to a prospective brand partner, presenting the show's audience, format options, pricing, and the specific business case for why this brand should advertise on this podcast.

## When To Use This Skill
- You want to approach a brand directly about sponsoring your podcast
- You have been contacted by a potential sponsor and need to send them a structured proposal
- You want to refresh or improve an existing sponsorship pitch that hasn't been converting
- You are launching outreach to multiple brands simultaneously and need a strong template

## What You Need To Provide
**Required:**
- Your podcast name, topic, and a brief description of your audience (who listens, why they listen)
- Your audience size: downloads per episode (approximate), monthly downloads, and any other relevant metrics (subscribers, social following, email list)
- The brand name and what they sell (or a description of the type of brand you're targeting)
- What you are offering: ad placement types (pre-roll, mid-roll, post-roll), episode frequency, and whether you offer host endorsement

**Optional:**
- Your CPM rate or total sponsorship price (if already decided)
- Any existing sponsors or past sponsor names (signals the show's commercial viability)
- Audience demographics if known (age range, profession, income, location)
- Notable guests, press coverage, or awards the show has received
- Any special formats you offer (dedicated episodes, newsletter inclusion, social posts)

## How the Assistant Approaches This
1. Opens with a direct statement of why this specific brand is a good fit for this specific audience — this is not a form letter; the pitch is tailored to the brand's product and the show's audience overlap
2. Presents the audience case concisely: who listens, why they are valuable to this advertiser, and what the listener relationship with the host enables in terms of purchase trust
3. Lays out the sponsorship packages as a clear menu: what each placement includes, approximate reach, and pricing (or a prompt to discuss pricing if the user has not set rates yet)
4. Closes with a low-friction call to action: a 20-minute call, a sample episode, or an introductory rate offer
5. Keeps the total pitch under 400 words for email format, or structures it as a clean one-page brief if a deck format is requested
6. Closes with a "Next Step" note: when to follow up if no reply (typically 7 days for a cold pitch), whether to send the podcast-media-kit-generator output alongside this email if the brand asks for more detail, and whether ad-read-script should be prepared for rapid activation once the deal is confirmed

## Output Format
- Email format (default): subject line + body, 300–400 words, no headers, conversational professional tone
- One-page brief format (if requested): header with show name + key stats, sections for Audience, Packages, and Contact
- Pricing presented as a range or as specific CPM-based rates (whichever the user provides)
- Tone: confident and specific — not pleading or vague; this is a business proposal, not a request for a favor
- Subject line: specific and benefit-led (not "Partnership Opportunity")
- Output ends with a "Next Step" note: follow-up timing, whether to have the media kit ready if the brand asks for more detail, and whether to run ad-read-script in advance of deal confirmation

## Quality Criteria
- [ ] The opening sentence names the brand and states the audience fit specifically — not generic ("your brand aligns with our values")
- [ ] Audience metrics are stated clearly and honestly — no inflated claims
- [ ] The sponsorship packages are described specifically enough that a brand manager can immediately understand what they are buying
- [ ] The call to action is one specific thing — not "let me know if you're interested"
- [ ] The pitch is under 400 words in email format — no wasted sentences
- [ ] Output includes at least one concrete next action the user can take immediately (send the email, set a follow-up reminder, or run ad-read-script to prepare for rapid activation)

## Example

### Input
- **Show:** *Practical Dispatch* — a weekly podcast for independent freelancers and self-employed professionals. Episodes cover contracts, money, taxes, insurance, and business operations.
- **Downloads:** 12,000 per episode average; 48,000/month
- **Audience demographics:** 78% aged 28–45, predominantly professional services freelancers (designers, writers, consultants, photographers); 60% based in US/UK/Canada/Australia
- **Target brand:** Bonsai — a business operations platform for freelancers (contracts, invoicing, proposals, time tracking)
- **Offering:** Mid-roll (60 sec) host-read ad, 4-episode minimum, personal endorsement angle, host has used the product
- **Price:** $40 CPM (=~$480/episode)
- **Existing sponsors:** None currently; first outreach to this brand
- **Special notes:** Host has been a Bonsai user for 14 months

### Output

**Subject: Sponsoring Practical Dispatch — your audience is already listening**

---

Hi [Name],

I'm reaching out because *Practical Dispatch* has a very specific audience that I think aligns unusually well with Bonsai: independent freelancers who are actively trying to run their work more professionally.

The show covers the operational side of freelancing — contracts, invoicing, tax, insurance, the systems that make freelance work sustainable. Our listeners are not people exploring whether to freelance; they are people who have already committed to it and are investing in doing it better. The average listener is a professional-services freelancer in their early-to-mid career, based in the US, UK, Canada, or Australia, and earning enough to care about business infrastructure.

Current reach: 12,000 downloads per episode, 48,000 per month.

Here's why I'm reaching out to Bonsai specifically: I've been using the platform for 14 months. I don't pitch sponsors I haven't tried. When I read an ad for a product I actually use, my audience hears the difference — and they act on it.

**What I'm offering:**

- **Mid-roll host-read, 60 seconds** — live in the episode permanently, included in the back catalogue
- **Personal endorsement** — I describe how I use Bonsai specifically, not generic copy
- **Minimum booking:** 4 episodes (one month)
- **Rate:** $40 CPM — approximately $480 per episode, $1,920 for a 4-episode run
- **Bonus:** I'll include a mention in my weekly email newsletter (6,200 subscribers) for each sponsored episode at no additional charge

To make the business case simple: a 4-episode run reaches approximately 48,000 downloads for $1,920 — with a host endorsement from someone who is demonstrably your target customer.

I'd love to set up a 20-minute call to walk you through the show and see if the timing works on your end. Would any time next week work?

[Host name]
*Practical Dispatch*
[email] · [URL]

---

## Known Limitations
- CPM rates and industry benchmarks change frequently — the example rate of $40 CPM is illustrative; the user should research current podcast CPM norms for their category and download size before setting rates
- The assistant does not know the specific brand manager's name or current marketing priorities — the user must find the right contact and verify that the brand is actively seeking podcast sponsorships before sending
- Sponsorship pitches to brands in regulated categories (financial products, health supplements, pharmaceuticals) may require additional legal disclosures; the user is responsible for checking category-specific advertising regulations
- This skill writes the outreach email, not the full media kit — for brands that request more detailed audience data or format specifications, use the podcast-media-kit-generator skill

## Related Skills
- [podcast-media-kit-generator](../podcast-media-kit-generator/SKILL.md)
- [ad-read-script](../../scripting/ad-read-script/SKILL.md)
- [guest-outreach-email](../guest-outreach-email/SKILL.md)

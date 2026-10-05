---
name: press-office-finder
description: "Produces a step-by-step guide for locating the correct press office, media contact, or spokesperson for a specific organisation, institution, or public figure — so the journalist sends their request to the right person on the first attempt."
status: stable
category: research
subcategory: people
version: 1.0
eval_score: 4.39
tags: [research, press-office, media-relations, contacts, people]
---
# Press Office Finder

## What This Skill Does
Produces a step-by-step guide for locating the correct press office, media contact, or spokesperson for a specific organisation, institution, or public figure — so the journalist sends their request to the right person on the first attempt.

## When To Use This Skill
- You need to reach an organisation's press office and cannot find the contact on their website
- You want to verify which spokesperson handles a specific topic area within a large organisation
- You are working on a deadline and need the fastest reliable route to an official comment
- You are contacting an organisation in a country or sector where press office structures are unfamiliar to you

## What You Need To Provide
**Required:** The name of the organisation or individual you need to reach; the nature of your enquiry (what you are asking about and why).

**Optional:** The country or jurisdiction the organisation operates in; the specific department or topic area (e.g., "I need the press contact for their environmental compliance division, not the corporate PR team"); your deadline; your media outlet name and type (helps determine which approach to recommend).

## How the Assistant Approaches This
1. **Identifies the organisation type.** Determines whether this is a corporation, government body, university, non-profit, international organisation, or individual with representation — each has different press office structures and contact conventions.

2. **Maps the likely contact routes.** Lists the specific places to look for press contacts, in order of reliability: official website press page, annual reports, regulatory filings, LinkedIn, professional directories, journalist databases, and direct phone approaches. Each route includes the specific page or section to check.

3. **Provides fallback strategies.** For organisations with no visible press contact, provides alternative approaches — contacting the general switchboard with a specific script, reaching out via social media, using journalist-specific tools, or contacting industry associations that may have member directories.

4. **Recommends the outreach approach.** Based on the type of enquiry and deadline, advises whether to email, phone, or use a combination — and provides a brief template for the initial contact that identifies the journalist's outlet, the topic, and the deadline.

5. **Flags common pitfalls.** Warns about specific issues: press contacts that route to external PR agencies rather than internal teams, automated media enquiry forms that rarely get responses, and the difference between a press office and a marketing department.

## Output Format
400–600 words. Three sections: **Where to Look** (numbered list of contact sources in priority order, with specific instructions for each), **Outreach Template** (a short, adaptable email or phone script), and **Pitfalls to Avoid** (3–4 bullet points). Tone: practical, direct, no wasted words. Written so a journalist on deadline can scan it and act within minutes.

## Quality Criteria
- [ ] Contact sources are listed in order of reliability, not alphabetically or randomly
- [ ] Instructions are specific to the organisation type — not generic advice applicable to any entity
- [ ] Outreach template is professional, concise, and identifies the journalist's needs clearly
- [ ] Fallback strategies go beyond "try their website" — they include genuinely useful alternatives
- [ ] Pitfalls section warns about real issues that journalists commonly encounter
- [ ] Output is short enough to scan on deadline — no padding or background context
- [ ] The plan distinguishes between press offices and marketing/PR departments

## Example

### Input
**Organisation:** A mid-sized regional hospital group (5 hospitals across two provinces/states)
**Enquiry:** Requesting comment on a story about emergency department wait times, based on data obtained through a freedom-of-information request
**Deadline:** 48 hours
**Outlet:** A national broadsheet newspaper

### Output

**Where to Look**

1. **Hospital group website — "Media" or "Press" page.** Check the main corporate website (not individual hospital sites). Look for a dedicated media enquiries page, usually under "About Us," "Contact," or "Newsroom." Regional hospital groups often list a single communications director rather than a full press team. Note the name, direct phone number, and email.

2. **Annual report or governance documents.** If the website has no press page, download the most recent annual report (usually available under "Publications" or "Board documents"). The executive team listing typically includes a Director of Communications or equivalent. Cross-reference the name on LinkedIn to confirm they are still in the role.

3. **LinkedIn search.** Search for "[Hospital Group Name]" + "communications" or "media relations" or "public affairs." Filter by current employees. Regional hospital groups typically have 1–3 communications staff. Send a connection request with a brief note identifying yourself and your outlet — or use the contact info on their profile.

4. **General switchboard.** Call the main corporate number (not a hospital reception desk). Ask to be transferred to the communications or media relations department. Script: "This is [Name] from [Outlet]. I'm working on a story about emergency department services and I need to speak with your media relations team. Could you transfer me or give me their direct line?"

5. **Health department press office.** If the hospital group is publicly funded, the regional or national health department may handle media enquiries on behalf of the group — or can tell you who does. Check the health department's website for a media contact and call them as a routing step.

6. **Professional association.** Check whether the hospital group is a member of a national hospital association or healthcare federation. These bodies sometimes maintain media contact directories for member organisations.

**Outreach Template**

Subject: Media enquiry — emergency department wait times — [Outlet Name] — response requested by [date]

Dear [Name / Media Relations Team],

I am a reporter at [Outlet Name] working on a story about emergency department wait times at regional hospital groups. The story is based on data obtained through a freedom-of-information request covering [time period].

I would like to offer [Hospital Group Name] the opportunity to comment on the data and provide context before publication. My deadline is [date and time].

I am happy to send specific questions in advance or arrange a brief phone call with an appropriate spokesperson. Please let me know the best way to proceed.

[Your name, title, outlet, phone number]

**Pitfalls to Avoid**
- **Do not use the patient enquiries line or general email address.** These are not monitored by communications staff and your request will be delayed or lost. Always ask specifically for the media or communications team.
- **External PR agencies.** Some hospital groups outsource media relations to PR firms. If you are redirected to an agency, confirm they are authorised to provide an on-the-record response — not just manage the enquiry process. You may still need an attributed quote from a named hospital executive.
- **Automated media enquiry forms.** Many healthcare organisations have online forms for media requests. These are useful for non-urgent enquiries but unreliable on a 48-hour deadline. Submit the form but also call directly.
- **Individual hospital vs. group response.** Emergency department data may prompt different responses from individual hospitals vs. the corporate group. Direct your enquiry to the group-level press office to get the official organisational position.

## Known Limitations
- The assistant cannot look up actual contact details, phone numbers, or email addresses. This skill provides the strategy for finding them — the journalist must execute the search. The value is in knowing where to look and in what order.
- Press office structures vary enormously by country, sector, and organisation size. The plan is tailored to the organisation type provided, but local conventions (e.g., how government press offices work in a specific country) may require adaptation.
- For individuals without organisational affiliation (freelance experts, retired officials, private citizens), press office strategies do not apply. In those cases, the plan focuses on direct contact methods, which are inherently less reliable.

## Related Skills
- [person-biography-brief](../person-biography-brief/SKILL.md) — broader research plan for profiling the person you are trying to reach
- [publication-history-finder](../publication-history-finder/SKILL.md) — find the person's previous public statements to inform your approach
- [cold-email-writer](../../../media-business/pitching/cold-outreach-email-writer/SKILL.md) — write a more detailed pitch email if the press office approach fails

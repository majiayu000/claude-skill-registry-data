---
name: person-biography-brief
description: "Generates a structured biographical research plan for a specific person, listing the public-record sources to check, the biographical questions to answer, and the verification steps to confirm key claims — so the journalist walks into an interview or writes a profile with no blind spots."
status: stable
category: research
subcategory: people
version: 1.0
eval_score: 4.5
tags: [research, biography, profiling, people, investigation]
---
# Person Biography Brief

## What This Skill Does
Generates a structured biographical research plan for a specific person, listing the public-record sources to check, the biographical questions to answer, and the verification steps to confirm key claims — so the journalist walks into an interview or writes a profile with no blind spots.

## When To Use This Skill
- You are preparing to interview someone and need to know their professional history, public positions, and potential controversies before you sit down
- You are writing a profile piece and need a systematic checklist of biographical facts to verify
- You are researching a source or subject for an investigative story and need to map their career, affiliations, and public record
- You need to brief a colleague or producer on a person quickly and cannot afford to miss anything significant

## What You Need To Provide
**Required:** The person's full name and the reason you are researching them (interview prep, profile piece, investigation, background check for a story).

**Optional:** Their known role or title; the organisation they are associated with; the specific angle of your story (helps prioritise which aspects of their biography matter most); any facts you already have; deadline pressure (determines depth of the plan).

## How the Assistant Approaches This
1. **Defines the research scope.** Based on the person's known role and the journalist's purpose, determines which biographical dimensions matter most — career chronology, financial interests, public statements, legal history, published work, board memberships, political donations, or personal background. Ranks these by relevance to the stated purpose.

2. **Builds a source checklist.** For each biographical dimension, lists the specific public-record sources and databases to consult — company registries, court records, academic publication databases, patent filings, property records, social media archives, parliamentary registers, charity filings, and professional licensing bodies. Each source is named specifically, not generically.

3. **Generates the key questions.** Produces a list of 10–15 biographical questions the journalist should be able to answer after completing the research — covering career trajectory, stated positions, potential conflicts of interest, and any gaps or inconsistencies that would need to be addressed in an interview.

4. **Flags verification priorities.** Identifies the 3–5 claims most commonly made about people in this role that frequently turn out to be exaggerated or inaccurate (e.g., educational credentials, founding dates, revenue figures) and specifies how to verify each one.

5. **Suggests interview angles.** Based on the biographical gaps and potential inconsistencies identified, recommends 2–3 lines of questioning that would surface information not available in the public record.

## Output Format
800–1,200 words. Three clearly labelled sections: **Source Checklist** (bulleted list of specific sources grouped by biographical dimension), **Key Questions** (numbered list of 10–15 questions the research should answer), and **Verification Priorities** (numbered list of 3–5 claims to verify with method for each). Ends with a **Suggested Interview Angles** section (2–3 bullet points). Tone: direct, practical, written for a working journalist. No preamble or summary paragraph — starts immediately with the checklist.

## Quality Criteria
- [ ] Source checklist names specific databases, registries, or record types — not vague references to "online research"
- [ ] Key questions are specific to the person's role and the journalist's stated purpose — not a generic biography template
- [ ] Verification priorities target claims that are genuinely common to exaggerate in this person's field or role
- [ ] Every source listed is a real, publicly accessible record type (not a fictional database)
- [ ] Interview angles are derived from gaps in the public record, not from speculation
- [ ] Output is immediately usable as a research assignment — a junior researcher could follow it without further briefing
- [ ] No assumptions are made about what the journalist will find — the brief is neutral, not leading

## Example

### Input
**Person:** Dr. Elena Vasquez, Chief Scientific Officer at a mid-sized biotech company
**Purpose:** Interview preparation for a magazine profile on women in leadership roles in the pharmaceutical sector
**Known facts:** Appointed CSO 18 months ago. Previously held research roles at two universities. The company recently received regulatory approval for a new diagnostic device.
**Story angle:** How her academic research background shapes her approach to corporate R&D leadership

### Output

**Source Checklist**

*Career and professional record*
- Company website biography and press announcements (appointment, regulatory approval)
- LinkedIn profile — cross-reference stated positions against company registry filings for dates
- National patent database — search by name for any patents filed during university and corporate tenure
- University staff directories and archived faculty pages (Wayback Machine if no longer listed)
- Professional society membership directories (relevant scientific or medical associations)

*Academic and publication record*
- PubMed / Google Scholar — full publication list, note co-authors and institutional affiliations over time
- Dissertation database (ProQuest or institutional repository) — confirm doctoral institution and year
- Conference programme archives — keynote or panel appearances in the last five years
- Grant funding databases (NIH Reporter, relevant national research council databases) — grants awarded as PI or co-PI

*Corporate and financial record*
- Company registry filing (Secretary of State or equivalent) — confirm her listed role, appointment date, any other directorships
- SEC filings or equivalent regulatory disclosures if the company is publicly traded — compensation, stock holdings
- Charity commission or non-profit registry — any board memberships at non-profit organisations
- Lobbying disclosure databases — any registered lobbying activity connected to the company

*Public statements and media*
- News archive search (LexisNexis, Factiva, or free news aggregators) — previous interviews, quoted statements, op-eds
- Social media accounts (Twitter/X, LinkedIn posts) — public positions on industry issues
- Podcast and video appearances — search by name on YouTube, Spotify, Apple Podcasts
- Industry conference recordings — presentations or panel discussions

*Legal and regulatory*
- Court records search (PACER for federal, state court databases) — any litigation involving her or the company
- Regulatory agency databases — any enforcement actions, warning letters, or compliance issues at the company during her tenure
- Patent dispute records — any IP litigation

**Key Questions**

1. What was her doctoral research topic and who was her supervisor?
2. How many peer-reviewed publications does she have, and has her publication rate changed since moving to industry?
3. What was the specific timeline of her transition from academia to industry — was there a gap, a consulting period, or a direct move?
4. What patents, if any, are filed in her name, and are any of them connected to the recently approved diagnostic device?
5. Were any of her university grants funded by the company she now works for (potential conflict of interest angle)?
6. Has she made public statements about the academic-to-industry pipeline or the challenges women face in pharma leadership?
7. Does she hold board seats or advisory roles at other organisations?
8. What was the company's regulatory track record before and after her appointment?
9. Has she been involved in any litigation, either personally or as a representative of her current or former employers?
10. Who are the co-authors she has published with most frequently, and could any of them provide an independent perspective on her work?
11. What industry conferences has she spoken at in the last three years, and what topics did she address?
12. Has the company's R&D spending or pipeline changed measurably since her appointment as CSO?

**Verification Priorities**

1. **Doctoral credentials.** Confirm the institution, year, and field of her PhD through the university's dissertation repository or graduation records — not just her LinkedIn or company bio.
2. **Publication count and impact.** Cross-reference the number of publications claimed in any company biography against the actual PubMed/Google Scholar record. Note any retractions or corrections.
3. **Appointment date and previous roles.** Verify the 18-month timeline against company registry filings and press releases — appointment dates in bios are sometimes rounded or shifted.
4. **Regulatory approval credit.** Determine whether the diagnostic device approval was based on research or development that predates her tenure — CSOs sometimes inherit pipeline successes.

**Suggested Interview Angles**

- Ask about the specific moment she decided to leave academia — what she gained and what she gave up — and whether her academic network still collaborates with her or views the move as a loss
- Explore whether the company's R&D culture changed after her arrival or whether she adapted to its existing processes — this tests whether the "academic leader transforms corporate R&D" narrative holds up
- If any grants from her university period were industry-funded, ask directly about how she managed that transition and whether it raised any concerns among former colleagues

## Known Limitations
- The assistant cannot access databases, search engines, or any external records. This skill produces the research plan — the journalist or researcher must execute it. The value is in systematic coverage: ensuring no major source category is overlooked.
- For public figures in countries with limited digital public records (e.g., no searchable court databases or company registries), some source suggestions may not be practically available. The journalist should adapt the checklist to their jurisdiction.
- The brief assumes the person is a legitimate research subject for journalistic purposes. It does not assess whether the research is ethically appropriate — that judgment belongs to the journalist and their editor.

## Related Skills
- [publication-history-finder](../publication-history-finder/SKILL.md) — deep-dive into a person's published work and media appearances
- [press-office-finder](../press-office-finder/SKILL.md) — locate the correct press contact for the person's organisation
- [policy-decision-maker-mapper](../policy-decision-maker-mapper/SKILL.md) — map the decision-makers around a policy issue the person is connected to
- [corporate-structure-brief](../../background/corporate-structure-brief/SKILL.md) — research the company the person works for

---
name: source-protection
description: "Produces a structured source-protection assessment for a specific source in a specific story, covering risk level, communication security guidance, legal protections available, editorial handling recommendations, and a pre-publication checklist."
status: stable
category: research
subcategory: fact-checking
version: 1.0
eval_score: 4.81
tags: [research, journalism, source-protection, ethics, security, confidentiality]
---
# Source-Protection Assessment

## What This Skill Does
Produces a structured source-protection assessment for a specific source in a specific story, covering risk level, communication security guidance, legal protections available, editorial handling recommendations, and a pre-publication checklist.

## When To Use This Skill
- You have a source who may face retaliation if identified and you need a structured plan for protecting them
- You are working on an investigation involving leaked documents, whistleblower testimony, or confidential information and need to formalise your source-handling protocols
- You want to assess the legal protections available to a source before committing to a particular attribution agreement
- You are reviewing a story before publication and need a checklist to verify that source-protection measures are adequate

## What You Need To Provide
**Required:** A description of the source (role, relationship to the story, what they are providing — documents, testimony, background, on-the-record quotes); the risk context (why the source might face retaliation — employer, government, legal, personal safety); the jurisdiction (country or legal system); the publication type (print, broadcast, online, podcast); the story sensitivity (general topic and whether it involves government, corporate, criminal, or national security matters).

**Optional:** Whether the source's identity is already partially known; whether the story involves active legal proceedings; any existing agreements with the source about attribution; the newsroom's existing source-protection policies.

## How the Assistant Approaches This
1. **Assesses risk.** Rates the source's exposure as LOW, MEDIUM, HIGH, or EXTREME based on who has power to retaliate, whether the source's identity is already partially known, whether the information narrows the pool of possible sources, and whether the story involves legal proceedings or criminal investigation. Names the specific retaliation vectors.

2. **Maps communication security.** Provides practical guidance on communication channels, meeting protocols, document handling, and digital operational security — calibrated to the risk level. Directs to current specialist resources (Freedom of the Press Foundation, CPJ, RSF) rather than recommending specific tools or app versions.

3. **Maps the legal landscape.** Identifies shield laws, contempt risk, subpoena exposure, whistleblower protections, and cross-border complications relevant to the jurisdiction. Frames each item as a question to answer with legal counsel, not as legal advice.

4. **Recommends editorial handling.** Defines the appropriate attribution level, assesses jigsaw identification risk, specifies corroboration requirements, and recommends a minimum-knowledge protocol within the newsroom.

5. **Generates a pre-publication checklist.** A numbered yes/no checklist covering informed consent, legal review, corroboration, jigsaw review, secure storage, and contingency planning.

## Output Format
Structured assessment document, 600–900 words. Five numbered sections: Risk Assessment (with explicit LOW/MEDIUM/HIGH/EXTREME rating), Communication Security, Legal Protections, Editorial Handling, Pre-Publication Checklist (table format with Y/N column). Professional register — written for a working journalist, not a security textbook. Practical and specific to the source described, not generic guidance.

## Quality Criteria
- [ ] Risk level is explicitly rated (LOW/MEDIUM/HIGH/EXTREME) with named retaliation vectors, not a vague warning
- [ ] Communication security directs to current external resources (Freedom of the Press Foundation, CPJ) rather than recommending specific apps or tool versions
- [ ] Legal protections are framed as questions for legal counsel, not as legal advice
- [ ] Attribution terms (on-the-record, on-background, not-for-attribution, off-the-record) are defined and noted as varying by newsroom
- [ ] Jigsaw identification is assessed as a specific risk, with concrete examples of how published details could combine to identify the source
- [ ] Pre-publication checklist contains at least 8 items and is formatted for practical use
- [ ] Output is specific to the source and story described, not a generic source-protection guide

## Example

### Input

A mid-level civil servant in a European EU member state has provided internal documents showing their ministry suppressed an environmental impact report before approving a construction permit for a large industrial facility. The journalist works for a national broadsheet newspaper (print and online editions). The story involves both corporate actors (the construction firm that benefited) and government actors (the ministry that suppressed the report). The source fears losing their job and facing prosecution under official secrets legislation. The source and journalist are in the same country.

### Output

**SOURCE-PROTECTION ASSESSMENT**

**Source:** Mid-level civil servant, environmental policy division. Providing internal documents (suppressed impact report, approval correspondence). Not willing to be quoted on the record.

---

**1. Risk Assessment: HIGH**

The source faces two distinct retaliation vectors. First, dismissal: leaking internal government documents is a disciplinary offence in virtually every EU civil service. Second, criminal prosecution: most EU member states have official secrets laws that criminalise the unauthorised disclosure of government documents, even where the content concerns environmental policy rather than defence or intelligence.

The pool of people with access to the suppressed report is likely small. Environmental impact reports pass through a defined workflow — the commissioning unit, the assessment team, the approving authority. If the ministry conducts an internal investigation after publication, document access logs and email records could narrow the field to a handful of people.

The story involves an active government function (permit approval) and a corporate beneficiary. Both have resources and motivation to identify the source. The construction firm may pursue civil litigation if the story threatens the permit, which could generate disclosure obligations that expose the source indirectly.

---

**2. Communication Security**

**Channels:** Use an encrypted messaging platform for all text communication. Do not use work email, work phones, or any device issued by the ministry. Do not communicate from the ministry's network or WiFi. For current tool recommendations, consult the Freedom of the Press Foundation's digital security resources (freedom.press).

**Meetings:** Meet in person where possible. Choose locations with no CCTV and no connection to either party's routine. Both parties should leave phones and smartwatches in a separate location during meetings.

**Document handling:** Receive documents in a way that does not create a digital trail linking source to journalist. If documents are digital, strip all metadata before storing. Check for hidden tracking features: version-specific watermarks, tracking pixels in PDFs, unique formatting artefacts inserted per-recipient. Store documents on an encrypted drive accessible only to the journalist and their editor. Do not upload to cloud services tied to personal accounts.

**Opsec basics:** The journalist should compartmentalise — use a dedicated device or at minimum a dedicated secure messaging account for this source. Do not search for the source's name or the ministry's internal systems from a personal or newsroom device without appropriate precautions.

> Current technical guidance: Freedom of the Press Foundation (freedom.press), CPJ Digital Safety Kit (cpj.org).

---

**3. Legal Protections — Questions for Legal Counsel**

- **Shield law:** Does this jurisdiction have a statutory or constitutional reporter's privilege? Does it extend to protecting leaked government documents, or only to protecting the identity of sources who speak voluntarily? Could a court order override the privilege in this case?
- **Contempt risk:** If a court orders the journalist to reveal the source, what penalties apply for refusal? Is imprisonment possible?
- **Subpoena exposure:** Could the ministry, the construction firm, or a prosecutor subpoena the newsroom's records, devices, or communications? Under what legal standard?
- **EU Whistleblower Directive (2019/1937):** Has the member state transposed the Directive? Does the source qualify for protection — the Directive covers breaches of EU law, which may include environmental regulations violated by suppressing the impact report. Has the source used an internal reporting channel first (some transpositions require this)? Does protection extend to disclosure to the press, or only to designated authorities?
- **Official secrets prosecution:** What is the realistic likelihood of prosecution? Is there a public-interest defence available? Have comparable cases been prosecuted in this jurisdiction in the past decade?
- **Cross-border:** If the story is published online and read in other EU jurisdictions, does that create additional legal exposure for the source or the journalist?

---

**4. Editorial Handling**

**Attribution:** The source should be described in terms broad enough to prevent identification but specific enough to convey credibility. A description such as "an official with direct knowledge of the ministry's environmental review process" is preferable to "a civil servant in the environment ministry," which narrows the pool. Agree the exact wording with the source before publication.

**Jigsaw identification:** Review the story for combinations of detail that could identify the source. If the article states the report was suppressed in a specific month, names the specific permit, and describes the source as mid-level, a determined reader inside the ministry could cross-reference access logs with seniority. Consider whether any of these details can be generalised without weakening the story.

**Corroboration:** The suppressed report itself is primary evidence. Corroborate its authenticity through at least one independent method: a second source who can confirm the report existed, public records showing the permit was approved without a published impact assessment, or expert analysis confirming the document's formatting and content are consistent with genuine ministry output.

**Editor notification:** The source's identity should be known to the journalist and one senior editor. No wider circulation within the newsroom unless legally required. The editor should be briefed on the risk level and the communication security measures in place.

---

**5. Pre-Publication Checklist**

| # | Item | Done |
|---|------|------|
| 1 | Source has given informed consent, understanding the risk of dismissal and potential prosecution. | Y / N |
| 2 | Source has seen or been told the substance of what will be published and the planned publication date. | Y / N |
| 3 | A media lawyer has assessed the source's legal exposure and the newsroom's legal position. | Y / N |
| 4 | The suppressed report has been authenticated by at least one independent method. | Y / N |
| 5 | The published text has been reviewed for jigsaw identification risk by someone other than the primary journalist. | Y / N |
| 6 | All communications with the source are stored on encrypted media with access restricted to the journalist and their editor. | Y / N |
| 7 | Leaked documents have been checked for metadata, tracking watermarks, and version-specific identifiers, and these have been stripped. | Y / N |
| 8 | The newsroom's legal team has been notified of the story and the source-protection measures. | Y / N |
| 9 | A contingency plan exists for supporting the source if they are identified (legal referral, public statement strategy, union support). | Y / N |
| 10 | The source has been reminded of their right to withdraw consent before publication. | Y / N |

## Known Limitations
- **Cannot provide current technical security advice.** Tools and platforms change. This skill names categories and directs to specialist organisations for current guidance.
- **Cannot provide legal advice.** The assessment maps the legal landscape but does not navigate it. A qualified media lawyer must review any source-protection plan.
- **Cannot assess undisclosed personal risk factors.** The assessment is only as good as the information the journalist provides about the source's situation.
- **In extreme-risk scenarios (national security, organised crime, authoritarian regimes), this skill is a starting point.** The journalist needs specialist security support from organisations such as CPJ, RSF, or the Freedom of the Press Foundation.

## Related Skills
- [legal-framework-brief](../legal-framework-brief/SKILL.md)
- [claim-origin-tracer](../claim-origin-tracer/SKILL.md)

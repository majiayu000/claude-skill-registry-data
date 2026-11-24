---
name: "sourcing-tools-stack"
description: "Contact finding tools, sourcing automation, Clay workflows, LinkedIn hacks, GitHub advanced sourcing, and the full modern sourcing tech stack. Use when recommending tools, building sourcing workflows, finding candidate contact details, automating outreach, or setting up a sourcing infrastructure."
---

# Sourcing Tools Stack Skill

You are an expert on the modern recruiting and sourcing technology stack. Apply this knowledge when the user needs tool recommendations, workflow automation advice, contact finding strategies, or sourcing infrastructure setup.

---

## Contact Finding Tools — Ranked by Use Case

### Best Overall Accuracy: ContactOut
- **Coverage:** 300M profiles, updates 300M contacts/hour
- **Key feature:** Triple verification on every contact; bulk reveal from LinkedIn search results
- **Best for:** High-volume LinkedIn sourcing, bulk email extraction
- **Free tier:** 40 emails/month
- **Pricing:** Paid plans from ~$99/month
- **Note:** 99% accuracy rate claim; most trusted by high-volume sourcers

### Best GDPR Compliance: Lusha
- **Coverage:** Large B2B database, strong in Europe
- **Key feature:** Confidence grading (A+ to lower) on each email/phone; explicit GDPR/CCPA compliance
- **Best for:** European markets, enterprise-to-enterprise sourcing
- **Integrates with:** LinkedIn, Salesforce, HubSpot
- **Free tier:** Limited credits/month

### Best LinkedIn Email Accuracy: Wiza
- **Coverage:** Real-time verification at point of extraction
- **Key feature:** Highest direct accuracy in head-to-head LinkedIn comparisons; 30+ advanced filters
- **Best for:** Sales Navigator power users, bulk LinkedIn export
- **Note:** Requires LinkedIn Sales Navigator for bulk extraction
- **Pricing:** Credit-based and subscription options

### Best for Company Website Emails: Hunter.io
- **Coverage:** Domain-based email database
- **Key feature:** Find all emails at a company domain; email pattern detection
- **Best for:** Finding emails when you know company but not LinkedIn profile
- **Free tier:** 25 searches/month
- **Use case:** You found someone on GitHub with no contact info — Hunter.io finds their company email

### Best for Personal Emails: Apollo.io
- **Coverage:** 275M+ contacts, 73M companies
- **Key feature:** Personal emails (not just work) specifically for recruiting; job change alerts; Chrome extension
- **Best for:** Reaching candidates about opportunities unrelated to their current employer
- **Recruiting-specific:** 90% of candidates prefer email over LinkedIn (Gem data); Apollo bridges this gap
- **Extra:** Job change alerts — automated trigger when a contact changes roles (sourcing gold)

### Best for Phone Numbers: SalesQL
- **Coverage:** Strong for mobile numbers via LinkedIn
- **Key feature:** Phone number extraction; personal and work numbers
- **Best for:** High-touch executive sourcing, roles where phone outreach is appropriate

### Best for Technical Candidates: AmazingHiring
- **Coverage:** Aggregates digital footprint across 50+ platforms
- **Key feature:** Shows actual code contributions, not just profile text; cross-platform view
- **Platforms covered:** GitHub, Stack Overflow, Kaggle, Dribbble, Behance, LinkedIn, Twitter
- **Best for:** Engineering sourcing where proof of work matters

---

## Contact Finding Comparison Matrix

| Tool | Best for | Email accuracy | Phone | Personal email | Free tier |
|---|---|---|---|---|---|
| ContactOut | LinkedIn bulk | ★★★★★ | ✓ | ✓ | 40/mo |
| Lusha | GDPR markets | ★★★★ | ✓ | Limited | Limited |
| Wiza | LinkedIn accuracy | ★★★★★ | ✗ | ✗ | Limited |
| Hunter | Domain/website | ★★★★ | ✗ | ✗ | 25/mo |
| Apollo | Personal email + sequences | ★★★★ | ✓ | ✓ | 50/mo |
| SalesQL | Mobile numbers | ★★★ | ★★★★★ | ✓ | Limited |
| AmazingHiring | Technical profiles | ★★★★ | ✗ | ✗ | Trial only |

---

## LinkedIn Sourcing Hacks

### Open Profile InMail Hack (Free InMails at Scale)
LinkedIn Premium users with "Open Profile" enabled can receive InMails from anyone **without credit cost**. In Sales Navigator, filter candidates by "Open Profile" to send free InMails at scale. This is the single most underused credit-saving technique — on large searches it can eliminate InMail costs entirely for a segment of the list.

### Connection Requests Beat InMails
Response rates to **connection requests with a personalised note** are measurably higher than InMails, and connection requests are free. Protocol:
1. Send connection request with a specific, short note (300 char limit — use it)
2. Wait 48-72 hours
3. Only use an InMail credit if the connection request is ignored

### Early Morning Outreach
LinkedIn data shows **6–8 AM outreach consistently outperforms afternoon sends** as professionals check LinkedIn before starting work. Schedule messages for 7-8 AM in the candidate's timezone.

### LinkedIn Recruiter Spotlight Filters (Response Rate Boosts)
- **"Open to Work"** candidates: +35% response rate vs average
- **"Recommended Matches"**: +35% response rate
- **Company followers** (candidates following your company): +81% response rate
Always activate these spotlights before sending InMails.

### LinkedIn AI-Assisted Messaging (2025)
LinkedIn's built-in AI-assisted messaging reports:
- 44% higher InMail acceptance rate
- 11% faster acceptance time
Worth testing before writing all outreach manually.

### Sales Navigator Job Change Alerts
Set up "Job Change" alerts on saved leads. When a target candidate changes jobs, you get notified — this is a prime outreach window (people in new roles for <6 months are often still network-building and open to conversations).

---

## GitHub Advanced Sourcing

### Native GitHub Search Operators
```
language:python location:"San Francisco"
language:javascript followers:>50 pushed:>2025-01-01
topic:machine-learning location:"London"
```

### Follower Count as Quality Signal
- 2–10 followers: Good
- 11–25 followers: Very good
- 26–75 followers: Excellent
- 75+: Field leader / community figure

### Mining Company GitHub Orgs
Navigate to `github.com/[company-name]` → **People tab** to see all contributors to their public repos. This surfaces developers who've worked on company open-source projects — even ex-employees who've moved on but still have contributions. Often faster than LinkedIn X-Ray for finding engineers who left a specific company.

### Finding Available Engineers
```bash
site:github.com "available for hire" python "San Francisco"
site:github.com "open to work" react "london"
site:github.com/users "available" golang -template -example
```

### Email in Commit Metadata
Some developers list emails in their commit metadata (visible via git log on public repos). Most ethical approach: use the profile email if listed, or platform messaging. Only 31% of tech recruiters use GitHub regularly — high signal, low competition.

---

## Clay — Automated Sourcing Workflows

Clay (valued at $1.25B) is the most powerful sourcing automation platform available to recruiting teams. It combines data enrichment + AI personalisation + sequence automation.

### What Clay Does
- **Waterfall enrichment** — Queries 50+ data sources sequentially, stops when verified data found. Achieves 80%+ email match rates vs 40-50% from single tools.
- **Claygent (AI agent)** — Navigates public web to fill profile gaps and write personalised outreach using enriched data
- **Dynamic list building** — Build lists by criteria rather than buying static lists
- **Sequence push** — Enriched, personalised leads pushed directly to HubSpot, Outreach, Lemlist, Reply.io

### Recruiting Workflow Example
1. Source 50 candidate names from LinkedIn X-Ray or GitHub
2. Import into Clay table
3. Clay waterfall enriches each with verified email (Apollo → ContactOut → Hunter → fallback)
4. Claygent pulls their latest GitHub project or LinkedIn post as a personalisation hook
5. Clay pushes to email sequence with hook auto-populated per candidate
6. **Result:** 50 fully personalised, sequenced outreaches in ~30 minutes

**Reported outcomes:** 50% reduction in manual hours, doubled meetings booked.

**Warning:** Clay has a steep learning curve (2-4 weeks). Start with pre-built templates.

### Clay Pricing
Credit-based. Free tier available. Professional plans start ~$149/month for sourcing use cases.

---

## Boolean String Generators

### Recruit'em / RecruitIn
[recruitin.net](https://recruitin.net/) — Free, no login required. Generates Boolean strings for LinkedIn, Stack Overflow, GitHub, XING with a simple form. Best starting point for quick strings.

### Leonar Boolean Generator
[leonar.app/boolean-x-ray-search-generator](https://www.leonar.app/blog/7-sourcing-techniques-linkedin) — LinkedIn-targeted X-Ray generator with visual builder.

### Fluar
[fluar.com](https://fluar.com/tools/google-x-ray-search) — Visual X-Ray string builder with export options.

---

## AI-Powered Talent Intelligence Platforms

### Juicebox / PeopleGPT
[juicebox.ai](https://juicebox.ai/) — Natural language search ("Software engineers with AWS and Kubernetes experience in Seattle") across 800M+ profiles, 30+ data sources. Best for teams wanting to eliminate Boolean entirely. AI agents learn from hiring patterns. 41 ATS + 21 CRM integrations.

### SeekOut
[seekout.com](https://seekout.com/) — 800M+ profiles, LLM-powered semantic search, strong DEI filters. Enterprise-focused. Competitive intelligence on where talent clusters. Best for large TA teams.

### HeroHunt.ai
[herohunt.ai](https://www.herohunt.ai/) — 1B+ profiles, autonomous "Uwi" AI recruiter handles full top-of-funnel: finds candidates, screens, finds contact info, launches personalised outreach. Includes RecruitGPT for natural language sourcing.

### LinkedIn Hiring Assistant (2025)
Built directly into LinkedIn Recruiter. Automates sourcing, evaluation, and outreach. Users report saving 4 hours per role average, reviewed 62% fewer profiles. Available on Recruiter licences — check if enabled in your account.

---

## Automation Tools

### PhantomBuster
[phantombuster.com](https://phantombuster.com/) — LinkedIn/social automation. Can automatically extract profiles from LinkedIn search results, send connection requests, message sequences. Use with caution — LinkedIn's terms limit automation; use at sustainable volumes to avoid account flags.

### Apollo Sequences
Apollo's built-in sequence tool allows multi-step email + LinkedIn outreach automation with personalisation tokens. Integrates with Gmail/Outlook. Most cost-effective end-to-end for individual sourcers.

### Zapier
[zapier.com](https://zapier.com/) — 1,000+ app connectors. Useful for: new LinkedIn application → auto-log to ATS → Slack notification; candidate changes job → alert recruiter; new GitHub follower of specific account → add to sourcing list.

---

## Full Stack Recommendation by Team Size

### Solo Recruiter / Agency
- **Boolean:** Recruit'em (free)
- **Contact:** ContactOut or Wiza
- **Email / sequences:** Apollo (all-in-one)
- **Research:** Perplexity Pro ($20/mo)
- **ATS:** Greenhouse or Lever

### Small TA Team (2-10)
- **Boolean:** ChatGPT + Recruit'em
- **Contact:** ContactOut + Hunter
- **Intelligence:** Perplexity Pro + LinkedIn Talent Insights
- **Automation:** Clay (if team has bandwidth to set up)
- **ATS + pipeline:** Greenhouse

### Enterprise / High-Volume
- **Platform:** SeekOut or LinkedIn Hiring Assistant
- **Contact:** Lusha (GDPR) + Apollo (personal email)
- **Automation:** Clay + Outreach/Salesloft integration
- **Intelligence:** LinkedIn Talent Insights + Perplexity Deep Research
- **ATS:** Greenhouse/Workday/Lever

---

## Free Tool Directory

| Tool | Use | Link |
|---|---|---|
| Recruit'em | Boolean string generator | recruitin.net |
| Hunter (free tier) | Domain email finder | hunter.io |
| GitHub (native search) | Engineering sourcing | github.com/search?type=users |
| Google Alerts | Passive signal monitoring | google.com/alerts |
| ScholarGPS | Academic talent | scholargps.com |
| Boolean Strings library | Search string templates | booleanstrings.com |
| WizardSourcer tools list | Full free tool directory | wizardsourcer.com/tools |

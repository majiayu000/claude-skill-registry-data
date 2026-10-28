---
name: mapping-conference-contacts
description: Map conference speakers, exhibitors, sponsors, attendees, booth mentions, LinkedIn profile URLs, LinkedIn company pages, and post-attendance snippets from public web evidence. Use for MHI-style conference relationship maps and LinkedIn URL lists.
---

# Mapping Conference Contacts

## Workflow

1. Generate named-event queries for speakers, exhibitors, sponsors, attendees, booth mentions, and app references.
2. Use `scripts/find_linkedin_profiles.py` on any names/companies from reports, snippets, event pages, or pasted research.
3. Label matches conservatively using `confirmed`, `probable`, `weak`, or `needs-manual-verification`.
4. Keep company pages separate from personal profiles.

## Commands

```powershell
python scripts/generate_event_queries.py --niche "manufactured housing" --event-name "MHI 2026 Congress & Expo" --year 2026 --companies "EXO Edge" "21st Mortgage Corporation" --people "Nikki Greenberg|Futurist" --output reports/mhi-contact-queries.csv
python scripts/find_linkedin_profiles.py --input tests/fixtures/mhi_contacts.csv --output reports/mhi-linkedin-matches.csv
```

## Guardrails

- Do not verify a profile from name alone.
- Mark gated app, LinkedIn snippet, and search snippet evidence as partial unless independently confirmed.
- Do not scrape authenticated LinkedIn areas unless the user explicitly approves a compliant workflow.
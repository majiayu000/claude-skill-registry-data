---
name: enriching-event-organizers
description: Enrich event organizers, speakers, functionaries, board members, sponsors, exhibitors, clinic/association contacts, and conference leads with LinkedIn URLs, emails, phones, Facebook URLs, Instagram URLs, websites, confidence labels, and next actions.
---

# Enriching Event Organizers

## Workflow

1. Start from normalized contact rows or pasted event research.
2. Extract obvious emails, phones, websites, and LinkedIn URLs with `scripts/extract_event_contacts.py`.
3. Use `scripts/enrich_contacts_serp.py` only when search API keys are available and the user expects enrichment.
4. Preserve evidence and confidence for manual review.
5. Export a Sheets-ready CSV.

## Commands

```powershell
python scripts/extract_event_contacts.py --input data/event-contact-notes.csv --output reports/event-contacts.csv
python scripts/enrich_contacts_serp.py --input reports/event-contacts.csv --output reports/event-contacts-enriched.csv
```

## Guardrails

- Keep WhatsApp/phone, Facebook, LinkedIn, and website fields separate.
- Do not overwrite a stronger manually verified contact with a weaker SERP guess.
- Use `needs-manual-verification` when evidence is incomplete.
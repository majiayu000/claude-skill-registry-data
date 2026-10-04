---
name: enrichment-analyst
description: Your data-fill agent. Connect a contact-enrichment tool (contact-level) or a company-enrichment tool (company-level), or both for the full waterfall, to fill gaps on any list. Given a name plus a company, find email, phone, LinkedIn, and title. Given a domain, find headcount, funding, technographic profile, and hiring intent. Trigger on "enrich these contacts with emails", "find LinkedIn URLs for {list}", "get phone numbers for {contacts}", "who are the decision makers at {company}", "complete this prospect list", "enrich this CSV", "get the technographic stack for {company}", "fill in missing data on {list}", or any data-completion, list-enrichment, or contact-lookup question.
---

# Enrichment Analyst

## What this does
This is your data-fill agent. Give it a name and a company, and it finds the email, phone, LinkedIn URL, and title. Give it a domain, and it returns headcount, funding, a technographic profile, and hiring intent. It works one contact at a time or across a whole list, tries the cheapest provider first, and tags every value it returns with how confident it is. It never invents a value it could not find.

## What you'll need
You do not need to connect anything to start. Bring your list and the skill runs today. Connect the tools below and it fills the gaps automatically at higher match rates than any single source.

- Works today with: your list of names and companies, or domains. Paste or upload a CSV. The skill structures it, flags what is missing, and tells you exactly which source would fill each field.
- More powerful connected to a contact-enrichment tool: emails, phones, LinkedIn URLs, and titles, run as a waterfall.
- More powerful connected to a company-enrichment tool: headcount, funding, hiring signals, and technographic profile. Either source alone works at reduced coverage; both run the full waterfall.
- Sharper with a people-search tool (LinkedIn identity validation) and a CRM (read records in, write enriched values back).

## How this runs at your connection level
This skill is never reliant on a connector. It runs on the data you give it today and gets more powerful as you connect tools. It never invents a number it cannot see. A gap is a prompt, not a guess.

- **Bring your data**: paste or upload what you have (a CSV or an export). The skill runs the full analysis today on your real numbers. No connection required.
- **Connect your tools**: the same skill pulls the data automatically and adds signals you cannot paste by hand (live activity, product usage, history). Same output, less effort, sharper.
- **Just exploring**: no data yet? Get the framework, the exact fields it reads, and a worked example on sample data, so you can see the shape before you feed it.

Every run ends with the one thing that would make the next run sharper, a field to add or a tool to connect.
## Customize this for yourself
| Set this | What it is | Default / Example |
| --- | --- | --- |
| Contact-enrichment tool | Resolves email, phone, LinkedIn, title from a name plus company | Any contact-waterfall provider |
| Company-enrichment tool | Returns headcount, funding, hiring intent, tech profile from a domain | Any company-data provider |
| Identity-validation tool | Cross-checks a returned LinkedIn URL against the input name plus company | Optional people-search tool |
| CRM | System of record you read from and write enriched fields back to | Optional |
| Waterfall order | The sequence providers are tried in for the same field | Cheapest provider first |
| Confidence tags | The labels attached to every returned value | verified_2_source, verified_1_source, inferred, not_found |
| Minimum confidence | The lowest confidence you accept for a given use | verified_1 for dialing, inferred for research |
| Maximum spend | A per-run cost cap that stops the waterfall when reached | Set a dollar ceiling per run |

To swap a provider, point the contact or company role at a different tool. The method does not change. Only the connector behind the role changes.

## The method
The core pattern is a cost-aware waterfall. For any field, try providers in order, cheapest first, and stop the moment you get a confident answer.
1. Read the input. For each row you need a name plus a company (contact mode) or a domain (company mode). Note fields already present so they are not re-bought.
2. Run the contact waterfall. For email, phone, LinkedIn, and title, try providers in order. Take the first confident hit. Tag each field with its confidence.
3. Run the company pass. For a domain, return headcount, funding, hiring signals, and the technographic profile.
4. Discover the buying committee. For a "who are the decision makers" request, return the senior roles per account, each with confidence-tagged identifiers.
5. Validate every LinkedIn URL. Cross-check the name and company on the profile against the input. If they do not match, do not return the URL.
6. Track spend. Log credits per provider. If the run hits the cap, stop and return partial results with a note.
7. Return confidence-tagged rows plus an audit of providers used, the confidence breakdown, and total cost.

## Quality gates
- Confidence-tagged outputs. Every enriched field comes back with its source confidence, never a bare value.
- Identity validation on LinkedIn URLs before they ship. This blocks returning the wrong person.
- Cost-aware waterfall. The cheapest provider is tried first. Per-provider credit use is logged.
- Honest "not found." If a value cannot be found, return null plus not_found rather than guessing.

## Output (example)
```
Enrichment Complete  ·  5 contacts processed

Name       | Email                     | Phone        | Title
-----------|---------------------------|--------------|-------------------
Contact A  | a@example.co (verified_2) | +1-555-0101  | VP Sales (verified)
Contact B  | b@example.co (verified_1) | not_found    | CRO (inferred)
Contact C  | c@example.co (verified_2) | +1-555-0102  | CFO (verified)
Contact E  | not_found                 | not_found    | not_found

Audit:
  Confidence breakdown: 8 verified_2, 4 verified_1, 1 inferred, 3 not_found
  Total cost: within run cap
  Skip Contact E: source the LinkedIn URL manually before reaching out.
```

## Where the numbers come from
By default the waterfall tries providers cheapest-first and stops at the first confident hit, so the same field is never paid for twice. Confidence tags come from the providers: two independent sources is verified_2, one is verified_1, a pattern-derived guess is inferred, and a value no provider could confirm is not_found. Cost figures are the per-provider credit prices of the tools you connect. To change the economics, reorder the waterfall, swap in a cheaper provider, or lower the maximum spend.

## Example chat
**You:** Enrich this list of 20 target contacts, I only have name and company.

**Claude:** Ran the waterfall. Here is where it landed.
```
Field       Verified_2   Verified_1   Inferred   Not_found
Email       9            6            3          2
Phone       4            5            2          9
LinkedIn    14           4            0          2
```
Two LinkedIn URLs failed identity validation (wrong company on the profile), so I dropped them instead of returning a guess. Total spend stayed under half the run cap.
One sharpener: connect a CRM so I can write these fields back instead of handing you a CSV to re-upload.

## Go further
The manual run proves the waterfall works. Here is where it goes once you trust it.

- **Enrich on intake, not in batches.** Wire a scheduled Claude task to run the waterfall the moment a new lead lands in Salesforce or HubSpot, so reps never work a blank record.
- **Build the waterfall natively.** Chain the same cheapest-first provider order inside Clay, so the enrichment runs where your list already lives.
- **Alert on the misses.** Have a scheduled task post the not_found rows to Slack each morning so someone can source them by hand before they go stale.

The list stops being a spreadsheet and starts being a living record.

## Make it yours
Set your two connector roles, your waterfall order, and your confidence floor, then run a small list to confirm the costs and tags read the way you expect. Built by an operator. Customize it, break it, make it better.

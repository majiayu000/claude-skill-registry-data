---
name: free-for-dev
description: >
  Find free-tier services for any development need. Use when the user says
  "for free", "free tier", "free alternative", "no cost", or "something free to
  do X" — covers SaaS, PaaS, IaaS, APIs, hosting, CI/CD, monitoring, and more.
---

# free-for-dev

Source: https://free-for.dev/ (GitHub: ripienaar/free-for-dev, 121k ★)
API: https://awesome.ecosyste.ms/api/v1/lists/ripienaar%2Ffree-for-dev/projects

## Lookup workflow

1. Identify what category the need falls into (see index below).
2. Fetch the relevant README section: `WebFetch https://raw.githubusercontent.com/ripienaar/free-for-dev/master/README.md` — search for the category heading.
3. Return matching services with their free-tier limits clearly stated.
4. If no exact match, check "Other Free Resources" and adjacent categories.

**Rule:** Always state the free-tier limit alongside the service name (e.g. "Cloudflare Workers — 100k requests/day free").

## Category index

| Need | Category |
|------|----------|
| Cloud compute / storage | Major Cloud Providers |
| CI/CD pipelines | CI and CD |
| Monitoring / alerting | Monitoring |
| Email sending / delivery | Email |
| Authentication / auth | Authentication, Authorization, and User Management |
| Database / BaaS | BaaS, Managed Data Services |
| DNS / domains | DNS, Domain |
| File / media storage | Storage and Media Processing |
| Search | Search |
| Error tracking | Crash and Exception Handling |
| Logging | Log Management |
| Testing | Testing |
| Web hosting / static sites | Web Hosting, PaaS |
| Feature flags | Feature Toggles Management Platforms |
| Analytics / events | Analytics |
| Messaging / queues | Messaging and Streaming |
| Payments | Payment and Billing Integration |
| Translation / i18n | Translation Management |
| Design / UI assets | Design and UI, Font |
| Forms | Forms |
| Screenshots / PDF | Screenshot APIs |
| Security / certs | Security and PKI |
| Source code hosting | Source Code Repos |
| Issue tracking | Issue Tracking and Project Management |
| AI / ML APIs | APIs, Data and ML |
| Docker / containers | Docker Related, IaaS |
| Mobile testing / distribution | Mobile App Distribution and Feedback |
| Code quality / review | Code Quality |

## API lookup (structured)

```
GET https://awesome.ecosyste.ms/api/v1/lists/ripienaar%2Ffree-for-dev/projects
  ?per_page=100&page=1&keyword=<term>
```

Returns JSON with `categories`, `url`, `description` per project. Use when you need programmatic filtering by category or keyword.

## Constraints the list enforces

- Free tier must be permanent (not a trial), or time-bucketed for ≥ 1 year.
- Services must offer TLS on the free tier.
- As-a-Service only — no self-hosted software.

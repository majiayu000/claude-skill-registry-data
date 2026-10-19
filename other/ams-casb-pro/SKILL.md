---
name: casb-pro
description: Deploy cloud access security brokers — shadow IT discovery, SaaS governance, and cloud data protection.
category: security
---

## Overview

A CASB sits between users and cloud services, giving visibility and control over SaaS usage: which apps are in use (including shadow IT), who accesses what data, and whether sensitive information leaves through unsanctioned channels. As work moved to the browser, the CASB became the DLP and access-control point for the cloud.

This skill covers CASB deployment modes, shadow-IT discovery programs, SaaS governance, and the policy design that secures cloud usage without strangling productivity.

Start with discovery, not blocking: the first CASB report — showing hundreds of unsanctioned apps, including file-sharing and AI tools with company data — is usually the most valuable deliverable. It reframes the conversation from "do we need this" to "how do we govern this," with evidence.

## When to use

- Discovering and governing shadow IT SaaS usage.
- Controlling data sharing in sanctioned SaaS (Google Workspace, Microsoft 365, Salesforce).
- Enforcing DLP and access policy on unsanctioned-but-tolerated apps.
- Meeting compliance requirements for cloud data handling.

## Core concepts

- **Deployment modes:** API-based (deep visibility into sanctioned apps via vendor APIs — the primary mode), forward/reverse proxy (inline control for any web app, needs traffic steering), and agent/log-based discovery. Most programs combine API + proxy.
- **Shadow IT discovery:** log-based or proxy-based identification of all cloud apps in use, risk-scored by vendor security posture, data handling, and compliance certifications. Discovery is continuous — new apps appear weekly.
- **SaaS governance lifecycle:** discover → risk-assess → sanction (approved), tolerate (restricted), or block. The sanctioned-app catalog with risk scores is the program's core artifact.
- **Sanctioned-app deep control:** via APIs — audit sharing settings, detect public links, find over-permissioned OAuth grants, enforce DLP on uploads, and monitor admin activity.
- **Unsanctioned-app control:** via proxy — allow with restrictions (block upload/download), allow with monitoring, or block. Match control strength to app risk and business need.
- **OAuth app governance.** Third-party OAuth grants into your SaaS (especially M365/Google) are a major attack path — inventory, risk-score, and revoke over-permissioned grants continuously.
- **User and entity behavior.** UEBA-style anomaly detection on cloud activity (impossible travel, mass downloads, unusual sharing) catches compromised accounts and insider actions.
- **AI app governance.** Generative AI tools are the new shadow-IT frontier — data sent to prompts is data shared externally. Discover AI app usage specifically and set policy deliberately.

- **Shadow AI discovery.** General shadow-IT discovery often misses browser-based AI tools; run targeted discovery for generative-AI domains and extensions specifically.
- **Sanctioned-app misconfiguration drift.** Sharing settings and public links drift over time; continuous compliance checks on sanctioned apps matter as much as initial hardening.

## Practical workflow

1. **Discover:** deploy log/proxy discovery for 30 days; produce the shadow-IT report with risk scores. Present it to leadership — the evidence drives the governance mandate.
2. **Assess and categorize:** risk-assess the top apps by usage; build the sanction/tolerate/block catalog with business-owner input. Publish it where employees can check before adopting tools.
3. **Connect sanctioned apps via API:** enable deep inspection — sharing audits, DLP policies, OAuth grant review, admin-activity monitoring. Fix the worst findings first (public links to sensitive data, over-permissioned grants).
4. **Steer traffic for control:** deploy proxy/agent steering for managed devices; apply tolerate-with-restrictions policies to unsanctioned apps (block uploads of classified data, allow read-only where sensible).
5. **Govern continuously:** new-app review workflow (fast enough that people use it), quarterly re-assessment of tolerated apps, OAuth grant audits, and AI-app usage reviews.
6. **Respond:** playbooks for compromised SaaS accounts (revoke sessions, reset, review sharing), malicious OAuth apps (revoke tenant-wide, investigate), and data-exposure incidents.

### Quick wins

- Pull the shadow-IT report this week and brief leadership on the top 10 risky apps
- Audit OAuth grants into M365/Google Workspace for over-permissioned third parties
- Find and remediate publicly shared links containing sensitive data

### Sustaining the practice

- Refresh the shadow-IT report monthly; new apps appear constantly
- Re-audit OAuth grants quarterly — they accumulate silently
- Review tolerated-app list quarterly with business owners
- Track AI-app usage specifically as its own governance workstream

### Metrics that prove it works

- Shadow-IT app count trend (sanctioned vs tolerated vs blocked)
- Sensitive-data exposure remediated (public links removed, over-sharing fixed)
- Malicious/over-permissioned OAuth grants revoked
- Mean time to assess and categorize a newly discovered app

## Common pitfalls

- **Blocking without alternatives.** Blocking a widely used unsanctioned app with no approved alternative drives users to worse workarounds. Govern, do not just prohibit.
- **Proxy-everything performance.** Inline proxying all traffic adds latency and breakage. Be selective: proxy high-risk categories, use API mode for sanctioned apps.
- **Ignoring OAuth grants.** The CASB watches the front door while malicious OAuth apps walk in through the API. Govern grants as a first-class workstream.
- **Stale app catalog.** A sanction list updated annually is fiction within months. Continuous discovery with a fast review workflow is the program.
- **No business-owner involvement.** Security-only app verdicts get overridden by business need. Include app owners in risk acceptance decisions.
- **Forgetting mobile.** SaaS access from unmanaged mobile devices bypasses proxy steering. Plan mobile coverage (MDM/MAM integration) explicitly.
- **AI apps unaddressed.** Generic SaaS policy misses the prompt-data exfiltration vector. Discover and govern AI tools as a distinct category.
- **Measuring apps instead of risk.** "We discovered 500 apps" is trivia. Report risk reduced: exposures closed, grants revoked, data protected.
- **CASB as the only SaaS control.** CASB complements SSO, MFA, and IdP governance — it does not replace them. Layer the controls.
- **Ignoring sanctioned-app admin activity.** Compromised SaaS admins bypass every user-level policy. Monitor admin consoles as privileged activity.

---
name: pihole-blocklist
description: Evaluate, categorize, and document new Pi-hole blocklist sources for the curated blocklist repository. Always trigger immediately when the user asks about adding, evaluating, or researching a new Pi-hole blocklist source, or uses phrases like "should I add this list", "evaluate this blocklist", "add to pihole", "new blocklist", "is this a good list", or pastes a raw blocklist URL. Also trigger when the user wants to review existing sources, update the repo README, check for list overlap, or document a new category. Pre-loaded with the full category taxonomy and evaluation criteria so every new addition is consistent with the existing curation standard.
version: 1.1.0
---

# Pi-hole Blocklist Skill

## Intent

Evaluate Pi-hole blocklist sources for category fit, source quality, format compatibility, and practical allow/block risk.

## Use When

- The user explicitly asks for `pihole-blocklist`.
- The request matches the triggers or workflow described below.
- The task benefits from a reusable, structured output instead of a one-off answer.

## Do Not Use When

- Do not use for general DNS troubleshooting, router configuration, or blindly adding lists without source and risk review.
- Required context is missing and cannot be reasonably inferred.
- A more specific skill in this repo is a better match.

## Workflow

1. Identify the exact task and available source material.
2. Apply the domain rules and output format in this skill.
3. State assumptions, uncertainty, and missing inputs clearly.
4. Return the requested artifact, recommendation, or review in a practical format.
5. Check the result against the validation checklist before finishing.

## Constraints

- Do not fabricate missing facts, measurements, dates, sources, or user context.
- Keep output aligned with Mick's direct, practical communication style unless the skill says otherwise.
- Preserve safety, legal, medical, financial, and operational boundaries stated in this file.
- Prefer concise, usable output over broad explanation.

## Validation Checklist

- [ ] The output matches the skill's intended task and platform.
- [ ] Required inputs, assumptions, and uncertainty are explicit.
- [ ] Safety, scope, and source limits are respected.
- [ ] The response follows the requested format or the skill's default output format.
- [ ] The result is practical enough to use without another cleanup pass.

Evaluate new blocklist sources, assign them to the correct category, check for quality and overlap, and produce ready-to-commit documentation for the curated blocklist repository at `github.com/mickpletcher/PiHole`.

---

## Repository Context

**Repo**: `github.com/mickpletcher/PiHole`  
**Current sources**: 57 curated blocklist URLs  
**Maintenance cadence**: Regular scheduled updates  
**Format**: Mixed (hosts file format and plain domain lists)  
**Pi-hole instance**: CT 101 at 192.168.0.101 (local reference only — do not publish this)

---

## Category Taxonomy

Every blocklist source belongs to exactly one primary category. Use this taxonomy consistently.

| Category | What It Covers |
|---|---|
| **Advertising** | Ad servers, ad networks, pop-up ad domains |
| **Tracking** | Telemetry, fingerprinting, analytics, CNAME cloaking |
| **Malicious** | Malware, ransomware, phishing, scam domains |
| **Suspicious** | Spam, referrer spam, high-risk domains |
| **Fake DNS / DynDNS** | Fake DNS providers, dynamic DNS abusers |
| **Piracy** | Anti-piracy DNS blocklists |
| **Fake News** | Known fake news domains |
| **Stalkerware** | Stalkerware and spyware indicator domains |
| **Device Trackers** | Platform-native trackers (Amazon, Apple, TikTok, Samsung, LG, Windows/Office) |
| **Smart TV / IoT** | Broad smart TV and IoT telemetry across all brands |
| **URL Shorteners** | URL shortener services used to obscure malicious links |
| **Encrypted DNS / VPN Bypass** | Domains used to circumvent DNS filtering |
| **OISD** | Comprehensive all-in-one lists covering ads, tracking, and malware |
| **Whitelist** | Approved domains excluded from blocking |

---

## Evaluation Criteria

When asked to evaluate a new source, assess all of the following:

### 1. Source Quality
- Is the list actively maintained? Check last commit date or update timestamp.
- Does it have a clear maintainer (GitHub repo, named project, organization)?
- Is there a stated methodology for what gets added and removed?
- Does it have community trust signals (stars, forks, citations in other blocklist projects)?

### 2. Category Fit
- Which category from the taxonomy does it best fit?
- Does it duplicate coverage already provided by an existing source in that category?
- Does it add meaningfully new domains not covered by existing sources?

### 3. Format Compatibility
- Is the URL a direct raw link to the list (not an HTML page)?
- Is it in a Pi-hole-compatible format: hosts file (`0.0.0.0 domain.com`) or plain domain list (one per line)?
- Is it stable — does the URL change between updates, or is it a permanent raw URL?

### 4. Risk Assessment
- Could any domains on the list cause false positives for common services?
- Is the list known to be aggressive (high false positive rate) or conservative?
- Has the list been flagged in the Pi-hole community for issues?

### Quick Reject Checklist

Run this before the full evaluation. Any hit means Skip without further analysis, which keeps low-quality lists from consuming a full review:

- no update in over 12 months and no statement that the list is intentionally static
- URL is an HTML page, paywalled, or changes between releases
- anonymous maintainer with no methodology and no community footprint
- near-total overlap with an existing source in the same category (a strict subset adds nothing)
- list mixes block domains with allowlist or comment formats Pi-hole would misparse

State which check failed in one line. Only proceed to scoring when all five pass.

### Scoring Rubric

Score each dimension 0 to 5 and weight them into a single source score so evaluations stay comparable:

| Dimension | Weight | 5 looks like |
| --- | --- | --- |
| Trust | 30% | Named maintainer, public methodology, strong community footprint |
| Maintenance | 25% | Updates at a stated cadence within the last month |
| Unique coverage | 25% | Meaningfully new domains versus existing sources in its category |
| False positive risk (inverted) | 20% | Conservative inclusion policy, no known breakage reports |

Score 4.0+ supports Add, 3.0 to 3.9 supports Add with caution, below 3.0 supports Skip. The rubric informs the recommendation; documented exceptions are allowed when stated.

### 5. Recommendation
- **Add**: Meets quality bar, fills a gap, compatible format, stable URL
- **Add with caution**: Useful but aggressive — note false positive risk in documentation
- **Skip**: Redundant, unmaintained, incompatible format, or unclear provenance
- **Whitelist candidate**: Source contains domains that should be whitelisted rather than blocked

---

## What Claude Should Produce

### For a new source evaluation:

```
SOURCE: [Name]
URL: [raw URL]
CATEGORY: [from taxonomy]
MAINTAINER: [GitHub user / org / project name]
LAST UPDATED: [date or "active" if recent commits]
DOMAIN COUNT: [approximate if known]
FORMAT: [hosts / plain domain list / mixed]
OVERLAP RISK: [low / medium / high — with which existing category]
FALSE POSITIVE RISK: [low / medium / high — brief reason]
SCORE: [weighted rubric score, e.g. 4.2/5]
RECOMMENDATION: [Add / Add with caution / Skip / Whitelist candidate]
REPO PLACEMENT: [exact category section and position in the repo README where the new row belongs]
NOTES: [Any caveats, known issues, or context]
```

The `REPO PLACEMENT` line should name the exact README section heading so the commit is mechanical, such as "Tracking section, alphabetical after EasyPrivacy".

### For a README table entry (when adding a new source):

```markdown
| [Source Name] | [URL] |
```

Formatted to match the existing table style in the repo README.

### For a batch evaluation (multiple URLs at once):

Produce one evaluation block per source, then a summary table at the end showing recommended adds vs. skips.

---

## How to Add a New Source to Pi-hole

1. Log into the Pi-hole admin panel
2. Navigate to **Group Management → Adlists**
3. Paste the raw URL into the **Address** field
4. Add a comment matching the source name from the repo
5. Click **Add**
6. Go to **Tools → Update Gravity** and click **Update**

---

## Reference Files

- `pihole-blocklist-sources.md` — local index of the current curated sources organized by category

## Help And Examples

If the user is not sure how to use this skill, asks what it needs, or asks for examples:

- Explain in plain language what this skill can do.
- Tell the user the minimum input needed for a useful first pass.
- Show the example prompts below.
- Offer the fastest next prompt the user can send.

Minimum useful input:

- A blocklist source, URL, or candidate list to evaluate.

Example prompts:

- `Use pihole-blocklist to review this candidate blocklist and tell me if it belongs in my setup.`
- `Evaluate these new Pi-hole sources for quality, overlap, and risk.`
- `Show me a sample prompt for asking this skill to document and classify a blocklist source.`


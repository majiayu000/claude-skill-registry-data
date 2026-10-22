---
name: pihole-csv-analyzer
description: Analyze CSV exports from Pi-hole such as query logs, top domains, top clients, or adlist exports and produce actionable recommendations. Trigger immediately when the user uploads or mentions a Pi-hole CSV file, types "pihole" or "ph analyze", or asks to analyze DNS query data, blocklist hits, or Pi-hole exports. Produce an in-chat analysis plus candidate blocklist and allowlist outputs for review.
version: 1.1.0
---

# Pi-hole CSV Analyzer

## Intent

Analyze Pi-hole CSV exports to identify query patterns, noisy clients, allowlist candidates, blocklist candidates, and cleanup actions.

## Use When

- The user explicitly asks for `pihole-csv-analyzer`.
- The request matches the triggers or workflow described below.
- The task benefits from a reusable, structured output instead of a one-off answer.

## Do Not Use When

- Do not use without CSV or equivalent query data, for generic Pi-hole setup, or for changes that cannot be traced to export evidence.
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

Analyze Pi-hole CSV exports and turn them into practical, reviewable cleanup actions.

## Supported Inputs

This skill should handle:

- query log exports
- top domains exports
- top clients exports
- blocklist or adlist exports

If the format is ambiguous, inspect the header row and the first few rows before proceeding.

## Export Type Detection

Use the CSV header to identify the likely export type.

| Export Type | Typical Columns | Typical Source |
| --- | --- | --- |
| Query Log | `time`, `type`, `domain`, `client`, `status`, `reply_type`, `reply_time`, `dnssec` | Pi-hole web UI query log export |
| Top Domains | `domain`, `count` or `hits` | Dashboard top permitted or blocked domains |
| Top Clients | `client`, `count` or `hits` | Dashboard top clients |
| Blocklist or Adlist | `address`, `enabled`, `comment`, `group`, `date_added` | Adlist or domain export |

Pi-hole v6 exports can vary slightly. Normalize column names before applying logic.

## Query Status Mapping

When analyzing query-log exports, use Pi-hole's documented query-database status meanings.

Common blocked status values:

- `1` blocked by gravity
- `4` blocked by regex denylist
- `5` blocked by exact denylist
- `6` blocked by upstream known blocking IP
- `7` blocked by upstream null response
- `8` blocked by upstream `NXDOMAIN` with `RA` bit unset
- `9` blocked by gravity during deep CNAME inspection
- `10` blocked by regex during deep CNAME inspection
- `11` blocked by exact denylist during deep CNAME inspection
- `15` blocked while the database is busy
- `16` blocked special domains
- `18` blocked by upstream `EDE 15`

Common allowed status values:

- `2` allowed and forwarded
- `3` allowed and replied from cache
- `12` allowed retried query
- `13` allowed retried but ignored query
- `14` allowed already forwarded
- `17` allowed and replied from stale cache

Treat unknown or new status values carefully and flag them instead of guessing.

## Analysis Workflow

### 1. Normalize the data

- normalize column names to lowercase
- strip extra whitespace
- detect whether status values are numeric or text

### 2. Compute the high-value summary

For query-log exports, compute:

- total query volume
- blocked versus allowed volume
- top allowed domains
- top blocked domains
- top clients by volume
- unusually noisy clients
- suspicious allowed domains that may deserve review

For top domains or top clients exports, normalize the columns and rank by count.

For blocklist or adlist exports, summarize enabled versus disabled state and obvious cleanup opportunities.

### 3. Generate review candidates

#### Blocklist candidates

Flag allowed domains that look suspicious based on signals such as:

- telemetry or tracking patterns
- free-TLD abuse indicators such as `.tk`, `.cf`, `.gq`, `.ml`
- IP-style subdomain patterns
- long random-looking subdomains
- repeated high-volume domains tied to a single client with no obvious user-facing purpose

Avoid recommending major infrastructure or obviously essential domains without a strong reason. Be conservative.

#### Allowlist candidates

Flag blocked domains that may be legitimate when they:

- are tied to sign-in, updates, streaming, or other common core functionality
- appear frequently among blocked queries
- clearly belong to major legitimate platforms

### 4. Prioritize findings

Not every finding deserves equal attention. Rank what gets surfaced first by leverage:

1. **High leverage**: a single domain or client responsible for a large share of total queries; fixing one thing changes the whole picture
2. **Likely false positives**: blocked domains that are breaking real functionality, since these cost the user daily
3. **Noisy but harmless**: high-volume telemetry that is already blocked; mention it once, no action needed
4. **Long tail**: everything else, summarized in counts rather than itemized

### 5. Client grouping

Group findings by client so problem traffic traces to a device, not just a domain:

- identify each noisy client's likely device type from hostname, MAC vendor hints, or query patterns (a TV queries TV telemetry, an IoT sensor beacons one domain)
- for each problem client, list its top domains and what they suggest the device is doing
- call out clients whose volume is wildly out of proportion to their device type, such as a thermostat making thousands of queries per hour
- recommend per-client fixes when they beat global ones, such as a group assignment in Pi-hole rather than a global block

### 6. Recommended actions

Separate every recommendation into one of four explicit paths so nothing reads as a vague suggestion:

- **Block**: add to denylist or a blocklist; evidence is strong and breakage risk is low
- **Allow**: add to allowlist; the block is causing real functionality loss
- **Investigate**: evidence is suggestive but not conclusive; state exactly what to check, such as watching whether a domain spikes when a specific app runs
- **Ignore**: looks alarming but is normal, and why

### 7. Output

Always provide an in-chat summary with:

- overview metrics
- top allowed and blocked domains
- top clients
- noisy-client callouts
- suspicious allowed domains
- possible allowlist candidates
- practical next-step recommendations

Also produce reviewable candidate outputs named:

- `blocklist_candidates.txt`
- `allowlist_candidates.txt`

If the environment supports file output, create those files. Otherwise, present their contents inline in clearly separated sections.

## Reference Logic

Use Pi-hole's documented status values as the source of truth. For example, a basic numeric mapping can start like this:

```python
BLOCKED_STATUSES = {1, 4, 5, 6, 7, 8, 9, 10, 11, 15, 16, 18}
ALLOWED_STATUSES = {2, 3, 12, 13, 14, 17}
```

When string-style status values appear instead of integers, use cautious text matching and keep uncertainty visible.

## Edge Cases

- Empty or malformed CSV files: explain what is wrong and what is expected
- No blocked queries: say so directly
- No suspicious domains: say so directly
- IPv6 clients: display as-is
- Large files: summarize and sample pattern analysis if needed
- Unknown status values: flag them as unknown instead of forcing a blocked or allowed label

## Style

- Lead with the most actionable findings
- Keep the output concise and practical
- Do not invent recommendations
- Be explicit when confidence is low
- Treat generated blocklist and allowlist entries as review queues, not final policy

## Help And Examples

If the user is not sure how to use this skill, asks what it needs, or asks for examples:

- Explain in plain language what this skill can do.
- Tell the user the minimum input needed for a useful first pass.
- Show the example prompts below.
- Offer the fastest next prompt the user can send.

Minimum useful input:

- A Pi-hole CSV export or a summary of what you want analyzed.

Example prompts:

- `Use pihole-csv-analyzer to review this Pi-hole export and tell me what cleanup actions make sense.`
- `Analyze this Pi-hole CSV and surface the top noisy domains, trends, and practical next steps.`
- `Show me an example prompt for using this skill with a pasted CSV summary.`


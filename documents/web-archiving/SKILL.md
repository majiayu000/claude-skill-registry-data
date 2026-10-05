---
name: web-archiving
description: "Produces a step-by-step archiving plan for preserving a live web page using Wayback Machine and Archive.today, with multi-archive redundancy and guidance on legal evidence preservation when the archived material may be needed in court or regulatory proceedings."
status: stable
category: research
subcategory: preservation
version: 1.0
eval_score: 4.96
tags: [journalism, archiving, Wayback-Machine, Archive-today, evidence-preservation, OSINT]
---
# Web archiving

## What this skill does
Produces a step-by-step archiving plan for preserving a live web page using Wayback Machine and Archive.today, with multi-archive redundancy and guidance on legal evidence preservation when the archived material may be needed in court or regulatory proceedings.

## When to use this skill
- A source has pointed you to a web page that may be edited or deleted, and you need to preserve it before that happens
- You are documenting a claim, a corporate statement, or a social media post that could be walked back
- You need archived material that is admissible or at least defensible as evidence in legal or regulatory contexts
- You are building a verification trail and need timestamped proof of what a page said on a specific date

## What you need to provide
**Required:** The URL(s) to archive; why the page matters to your investigation or story (helps prioritise what to capture)
**Optional:** Whether the material may be needed as legal evidence (triggers additional preservation steps); whether the page is behind a login or paywall (affects archiving method); whether you need to capture the page's full visual appearance (screenshots) or just its text and HTML

## How the Assistant Approaches This
1. **Primary archive: Wayback Machine.** Guides the user to submit the URL to web.archive.org/save. Notes: Wayback Machine archives the page's HTML, CSS, and embedded resources. It stores a timestamped snapshot accessible via a permanent URL. Capture may take a few seconds to a few minutes depending on page complexity. Some pages block the Wayback Machine's crawler — if the save fails, note this and move to the secondary archive.

2. **Secondary archive: Archive.today.** Guides the user to submit the URL to archive.today (also accessible via archive.ph, archive.is, archive.li). Notes: Archive.today renders the page in a browser before saving, which means it captures JavaScript-rendered content that Wayback Machine sometimes misses. It also captures pages behind some soft paywalls. Archive.today assigns its own permanent URL.

3. **Multi-archive redundancy.** Both archives are used every time, not one or the other. Reason: either service can go down, change its policies, or be subject to legal takedown requests. Having the same page preserved in two independent archives protects against single-point failure. If both fail (page blocks all archivers), the skill guides the user to manual preservation: full-page screenshot with timestamp, local HTML download via browser "Save As," and PDF print.

4. **Legal evidence preservation.** When the user indicates the material may be used as evidence: adds steps for cryptographic hashing (SHA-256) of the downloaded page file, screenshot notarisation (using a service that timestamps the hash on a public ledger), and chain-of-custody documentation. Explains what each step does and why a court or regulator would find it more persuasive than a simple screenshot.

5. **Verification.** After archiving, confirms the archive URLs work by visiting them. Notes the archive timestamp and compares it to the current live page — if the live page has already changed since archiving, that change itself becomes part of the record.

## Output format
A numbered archiving checklist (10–15 steps), followed by a confirmation block listing the archive URLs and timestamps. If legal evidence preservation was requested, a separate section covers the hashing and documentation steps. Total length: 300–600 words. Direct, procedural language — written as instructions, not as a description of what archiving is.

## Quality criteria
- [ ] Both Wayback Machine and Archive.today are used — not one alone
- [ ] Instructions include what to do when archiving fails (page blocks crawler, login required, dynamic content)
- [ ] Legal evidence section includes cryptographic hashing and explains why it matters in plain language
- [ ] Each archive URL is verified after capture
- [ ] Fallback method (manual screenshot + local save) is included for pages that cannot be archived by either service
- [ ] Output is procedural — numbered steps a reporter can follow, not an essay about archiving
- [ ] Output is free of generic AI-template phrasing — no "delve into," "navigate the complexities of," Latinate filler verbs, restate-the-question intros, summary-of-the-summary closes, or em-dash overuse

## Example

### Input
URL: https://www.greenfield-chemicals.example.com/sustainability/water-quality-report-2025
Context: This corporate sustainability page contains water-quality discharge figures cited in a press release. The company has previously edited its sustainability reports after media inquiries. We need to preserve the page before we contact their press office tomorrow. This may be used as evidence if the regulatory authority opens an investigation.

### Output

**Archiving checklist**

1. Open web.archive.org/save in your browser. Paste the URL: `https://www.greenfield-chemicals.example.com/sustainability/water-quality-report-2025`. Click "Save Page." Wait for the confirmation message showing the archived snapshot URL. Copy that URL — it will look like `https://web.archive.org/web/20260527.../https://www.greenfield-chemicals.example.com/...`.

2. Open the archived snapshot in a new tab. Confirm the page content matches the live page. Note any missing images, broken interactive elements, or content that did not render.

3. Open archive.today in your browser. Paste the same URL. Submit. Archive.today may take 30–90 seconds. It will return a permanent URL (e.g., `https://archive.today/AbCdE`). Copy this URL.

4. Open the Archive.today snapshot. Confirm it captured the discharge figures and any embedded tables or PDFs.

5. If either archive failed (error message, blank page, CAPTCHAs), take a full-page screenshot using your browser's built-in tool (Ctrl+Shift+S in Firefox, or "Capture full size screenshot" in Chrome DevTools). Save the screenshot with a filename that includes the date: `greenfield-water-report-2026-05-27.png`.

6. Save the page locally: right-click > "Save As" > "Webpage, Complete" to preserve the HTML and all embedded assets. Store in your investigation folder.

7. If the page has a downloadable PDF version of the report, download that separately and save it alongside the HTML.

**Legal evidence preservation**

8. Generate a SHA-256 hash of every file you saved locally (screenshot, HTML, PDF). On macOS: `shasum -a 256 filename`. On Windows: `certutil -hashfile filename SHA256`. Record each hash alongside the filename and the date/time of download.

9. Email the hash values to yourself and to a colleague. The received email creates a third-party timestamp (the email provider's server timestamp) that corroborates when the files existed.

10. For stronger timestamping, submit the hash to a public timestamping service (e.g., OpenTimestamps at opentimestamps.org or a qualified trust service provider under the EU eIDAS regulation). This anchors the hash to a blockchain or a trusted authority's ledger, producing a certificate a court can verify independently.

11. Document the chain of custody: who downloaded the files, from what device and IP, at what time, and where the files are stored. This log goes into your investigation notes.

**Confirmation block**

| Item | URL / hash | Timestamp |
|------|-----------|-----------|
| Wayback Machine snapshot | `https://web.archive.org/web/20260527142300/https://www.greenfield-chemicals...` | 27 May 2026, 14:23 UTC |
| Archive.today snapshot | `https://archive.today/AbCdE` | 27 May 2026, 14:25 UTC |
| Local HTML save | SHA-256: `a1b2c3d4e5...` | Downloaded 27 May 2026, 16:24 local |
| Full-page screenshot | SHA-256: `f6g7h8i9j0...` | Captured 27 May 2026, 16:24 local |
| PDF report | SHA-256: `k1l2m3n4o5...` | Downloaded 27 May 2026, 16:25 local |

## Known limitations
- Wayback Machine and Archive.today cannot archive pages behind logins, hard paywalls, or CAPTCHAs. For those, manual preservation (screenshot, local save) is the only option.
- Archive.today sometimes fails on pages with aggressive bot detection (Cloudflare challenges, rate limiting). Retrying from a different network or after a delay sometimes helps.
- Cryptographic hashing proves a file existed in a specific state at a specific time. It does not prove the file was not altered before hashing. Chain-of-custody documentation is what closes that gap.
- Neither archive service guarantees permanent availability. Both have removed content in response to legal requests. Multi-archive redundancy and local copies are insurance against this.
- This skill cannot evaluate whether archived material meets the evidentiary standards of a specific court or jurisdiction. For legal proceedings, consult a lawyer who can advise on admissibility rules.

## Related skills
- [source-verification](../../../magazine-journalism/investigation/source-verification/SKILL.md)
- [page-monitoring](../page-monitoring/SKILL.md)
- [content-access](../content-access/SKILL.md)

---
name: qa-review-content
section: content
description: "Layer 2 of grammar 2-layer strategy. Sonnet judgment for: spelling errors (confirms Layer 1 candidates against full dictionary), grammar, word choice, homophone correctness (grades Layer 1 candidates), awkward phrasing, capitalization, punctuation. Receives proper-noun whitelist from config (never flags brands). Auto-switches to legal/compliance mode on routes matching content.legal_routes (GDPR/CCPA/T&C required-phrase audit)."
model: sonnet
applyOn: [laptop]
needsSetup: false
viewportSensitive: true
interactive: true
---
## What it checks

Everything that requires judgment over visible page text. This is the Sonnet half of the 2-layer content strategy — Layer 1 (`qa-detect-content-patterns`) finds deterministic patterns and candidates; this layer confirms candidates and grades grammar.

### Standard mode (any non-legal route)

| Issue type | severity | What it catches |
|---|---|---|
| `spellingError` | medium | Misspellings confirmed from Layer 1 `candidateMisspelling` candidates (real dictionary check) |
| `grammarError` | medium | Subject-verb disagreement, wrong tense, missing articles |
| `wordChoice` | medium | Confirmed homophone misuse from Layer 1 `homophoneCandidate` (your/you're, their/there/they're, its/it's, affect/effect, to/too/two, etc.) |
| `awkwardPhrasing` | low | Run-on sentences, stilted machine-translated copy |
| `capitalizationInconsistency` | low | Headings mixing Title Case / sentence case / ALL CAPS |
| `punctuationError` | low | Missing periods, double commas, no space after punctuation |
| `terminologyInconsistency` | medium | The SAME action/label uses different words across the page — "Sign in" vs "Log in", "Cancel" vs "Close", "Delete" vs "Remove", "Edit" vs "Modify". Pick one term per concept. Judge only same-meaning verbs/labels; do NOT flag genuinely different actions. |

### Legal/compliance mode (route matches `content.legal_routes`)

Triggered automatically when the cell's route path matches a pattern in `automation.config.json → content.legal_routes` (default: `["/privacy", "/terms", "/legal", "/cookie", "/refund", "/shipping", "/gdpr", "/ccpa"]`).

| Issue type | severity | What it catches |
|---|---|---|
| `missingRequiredCompliancePrivacy` | high | Privacy page missing required GDPR phrases: data controller, right to erasure, lawful basis, retention period, third-party sharing |
| `missingRequiredComplianceCCPA` | high | CCPA page missing "Do Not Sell My Personal Information" or right-to-know wording |
| `missingRequiredComplianceCookie` | high | Cookie page missing categories (necessary/analytics/marketing) and consent mechanism description |
| `missingRequiredComplianceTerms` | medium | T&C missing: governing law, dispute resolution, liability limitation, termination clause |
| `missingRequiredComplianceContact` | medium | Legal page has no contact route for the data controller / DPO |
| `vagueComplianceWording` | low | "We may share with partners" without specifying which/why — fails GDPR transparency |

## Orchestrator flow

1. Run `probe.extractVisibleText` — returns visible text (capped at 5,000 chars), page title, and the cell's resolved route path.

2. **Build context inputs** from this cell's existing findings + config:
   - `alreadyCaught` — Layer 1 final findings (typos, plurals, i18n keys, html entities, markdown, mojibake, lorem, todo, long sentence, reading level, generic CTA). Filter findings array where `skill === 'qa-detect-content-patterns'` AND `issueType` is in the L1-final set (NOT `candidateMisspelling` or `homophoneCandidate`).
   - `candidateMisspellings` — array of `{word, snippet}` from L1 findings where `issueType === 'candidateMisspelling'`.
   - `homophoneCandidates` — array of `{word, snippet}` from L1 findings where `issueType === 'homophoneCandidate'`.
   - `properNouns` — from `automation.config.json → content.proper_nouns` (default: `[appName]`).
   - `mode` — `"legal"` if the cell's route matches any pattern in `content.legal_routes`, else `"standard"`.

3. Dispatch to Sonnet sub-agent with mode-specific prompt:

### Standard-mode prompt

```
Agent(
  subagent_type: "general-purpose",
  model         = "sonnet",
  prompt = `You are reviewing the visible text of a web page for content quality issues.

  Cell context:
    route: {cell.route}
    viewport: {cell.viewport}
    browser: {cell.browser}

  Proper nouns / brand names — NEVER flag these as misspellings:
  {properNouns.join(", ")}

  Visible text from the page:
  ---
  {extractedText}
  ---

  Issues already detected by Layer 1 (DO NOT re-report these patterns):
  ---
  {alreadyCaught}
  ---

  Layer 1 flagged these words as POSSIBLE misspellings — confirm each one with your dictionary:
  ---
  {candidateMisspellings.map(c => `"${c.word}" in "${c.snippet}"`).join("\n")}
  ---
  For each candidate:
    - If it IS a real misspelling → emit one finding with issueType: "spellingError", snippet: candidate.word, suggestion: corrected form
    - If it is NOT a misspelling (technical term, brand, valid rare word) → DROP it silently

  Layer 1 flagged these sentences as homophone candidates — judge whether the homophone is used CORRECTLY in context:
  ---
  {homophoneCandidates.map(c => `"${c.word}" in "${c.snippet}"`).join("\n")}
  ---
  For each homophone candidate:
    - If used INCORRECTLY (e.g., "your" where "you're" is needed) → emit one finding with issueType: "wordChoice", snippet: the offending phrase, suggestion: corrected form
    - If used CORRECTLY → DROP it silently

  Find ADDITIONAL judgment issues from these categories:
    - grammarError        (subject-verb / tense / articles)
    - awkwardPhrasing     (clear run-ons / stilted machine translation)
    - capitalizationInconsistency
    - punctuationError    (missing period, double punctuation)

  General rules:
    - Do NOT re-flag patterns from "already detected" above
    - Do NOT flag proper nouns from the brand list above
    - Do NOT flag intentional casing like iPhone, macOS, GitHub, JavaScript, npm
    - Do NOT flag URLs, email addresses, code snippets, file paths
    - Limit total NEW findings to 20 per cell
    - Output ONLY a valid JSON array — no prose, no markdown

  Return JSON:
  [
    {
      "issueType": "spellingError | grammarError | wordChoice | awkwardPhrasing | capitalizationInconsistency | punctuationError",
      "severity":  "low" | "medium" | "high",
      "snippet":   "<the offending text, max 80 chars>",
      "suggestion":"<corrected text, max 80 chars, or null>",
      "context":   "<what's around it, max 80 chars, for the bug description>"
    }
  ]
  If nothing is wrong, return [].`
)
```

### Legal-mode prompt

```
Agent(
  subagent_type: "general-purpose",
  model         = "sonnet",
  prompt = `You are auditing a LEGAL/COMPLIANCE page for required phrases and clarity.

  Page context:
    route:        {cell.route}
    page title:   {pageTitle}
    suspected category: privacy | terms | cookies | refund | shipping  (infer from route)

  Visible legal text:
  ---
  {extractedText}
  ---

  Apply the appropriate required-phrase rubric:

  IF privacy/GDPR page, check for ALL of:
    1. Identity of data controller (entity name + contact)
    2. Right to erasure / "right to be forgotten"
    3. Lawful basis for processing (consent, contract, legitimate interest, etc.)
    4. Data retention period (specific duration or criteria)
    5. Third-party data sharing (named recipients OR categories)
    6. Data subject rights summary (access, rectification, portability)
    7. Supervisory authority contact (or pointer to one)

  IF CCPA page, check for ALL of:
    1. "Do Not Sell My Personal Information" link / mechanism
    2. Right to know what categories of personal info are collected
    3. Right to delete personal info
    4. Right to non-discrimination for exercising CCPA rights
    5. Categories of sources from which info is collected

  IF cookie page, check for ALL of:
    1. Cookie categories (strictly necessary, functional, analytics, marketing)
    2. Consent mechanism described (how to accept/reject)
    3. Third-party cookies named OR categorized
    4. How to withdraw consent / change preferences
    5. Cookie retention duration

  IF terms / T&C page, check for ALL of:
    1. Governing law / jurisdiction
    2. Dispute resolution mechanism (arbitration, court, mediation)
    3. Limitation of liability
    4. Termination conditions
    5. Modification policy ("we may update these terms")
    6. User obligations / acceptable use

  For each MISSING required item, emit one finding:
    issueType: missingRequiredCompliancePrivacy | missingRequiredComplianceCCPA |
               missingRequiredComplianceCookie | missingRequiredComplianceTerms
    severity: "high" for items 1-5, "medium" for the rest
    snippet: name the missing required item (e.g., "Data retention period not specified")
    suggestion: what to add

  ALSO check for vague wording that fails transparency:
    - "We may share with partners" without naming who/why → vagueComplianceWording
    - "From time to time we may update" without notice mechanism → vagueComplianceWording
    - "Reasonable security measures" with no specifics → vagueComplianceWording

  Skipping rules:
    - Do NOT re-flag patterns already caught by Layer 1
    - Do NOT flag the absence of items that are clearly N/A for this page type
    - Limit total findings to 15 per cell
    - Output ONLY a valid JSON array

  Return JSON:
  [
    {
      "issueType": "missingRequiredCompliance{Privacy|CCPA|Cookie|Terms|Contact} | vagueComplianceWording",
      "severity":  "low" | "medium" | "high",
      "snippet":   "<which required item is missing, max 80 chars>",
      "suggestion":"<what to add, max 80 chars>",
      "context":   "<surrounding text excerpt, max 80 chars>"
    }
  ]
  If page is fully compliant, return [].`
)
```

4. Receive the JSON array back. For each finding, convert into the standard issue schema:

   ```js
   {
     skill: "qa-review-content",
     issueType: <finding.issueType>,
     severity: <finding.severity>,
     selector: null,
     description: `${finding.context} → "${finding.snippet}"` +
                  (finding.suggestion ? ` (suggestion: "${finding.suggestion}")` : ''),
     bbox: null
   }
   ```

5. Append to issues. Apply the standard screenshot step from qa-argus (cell-level capture is sufficient; per-finding annotation is not meaningful for content issues — they don't have bboxes).

## Probe (browser_evaluate)

```js
// probe.extractVisibleText
() => {
  const SKIP_TAGS = new Set(['SCRIPT', 'STYLE', 'NOSCRIPT', 'NAV', 'FOOTER', 'IFRAME']);
  const out = [];
  const walk = (node) => {
    if (!node) return;
    if (node.nodeType === Node.ELEMENT_NODE) {
      if (SKIP_TAGS.has(node.tagName)) return;
      if (node.getAttribute && node.getAttribute('aria-hidden') === 'true') return;
      const style = node.nodeType === 1 ? window.getComputedStyle(node) : null;
      if (style && (style.display === 'none' || style.visibility === 'hidden')) return;
    }
    if (node.nodeType === Node.TEXT_NODE) {
      const t = (node.textContent || '').replace(/\s+/g, ' ').trim();
      if (t.length >= 2) out.push(t);
      return;
    }
    for (const c of (node.childNodes || [])) walk(c);
  };
  walk(document.body);

  let combined = out.join(' ').replace(/\s+/g, ' ').trim();

  // Cap at 5000 chars: keep the first 2500 + last 2500
  if (combined.length > 5000) {
    combined = combined.slice(0, 2500) + ' … ' + combined.slice(combined.length - 2500);
  }
  return {
    text: combined,
    charCount: combined.length,
    pageTitle: document.title || '',
    routePath: location.pathname + location.search
  };
}
```

## Cost control

```toml
[grammar]
critical_routes = ["/", "/login", "/signup", "/checkout", "/dashboard"]
max_cells = 10
max_chars = 5000
```

If `critical_routes` is empty `[]`, the skill runs on every cell. Legal routes (matching `content.legal_routes`) ALWAYS run regardless of `critical_routes` — compliance is mandatory.

## Mode-selection algorithm

```
mode = "standard"
for pattern in content.legal_routes:
  if cell.route matches pattern (string contains, case-insensitive):
    mode = "legal"
    break
```

Default `content.legal_routes`: `["/privacy", "/terms", "/legal", "/cookie", "/refund", "/shipping", "/gdpr", "/ccpa"]`.

## Issue schema mapping

The Sonnet sub-agent returns `{issueType, severity, snippet, suggestion, context}`. The orchestrator maps each to the standard issue record:

| Sub-agent field | Issue record field |
|-----------------|-------------------|
| `issueType` | `issueType` |
| `severity` | `severity` |
| `snippet` + `context` + `suggestion` | combined into `description` |
| `null` | `selector` (content findings have no element selector) |
| `null` | `bbox` (no element box) |

## Cell-skipping rules

- **Self-skip** if `probe.extractVisibleText` returns `charCount < 50` (likely a redirect, loader, or blank state)
- **Self-skip** if standard-mode AND route is in `customize.toml → grammar.critical_routes` whitelist AND current route is NOT in the list
- **NEVER self-skip** in legal-mode — compliance check is mandatory on legal routes
- **Hard cap** after `customize.toml → grammar.max_cells` reached (standard mode only; legal-mode cells are uncapped)

## Notes

- No external dependencies, no third-party API, no spellcheck library
- Does NOT modify the page, never types, never clicks, never navigates
- Brand-aware: reads `automation.config.json → content.proper_nouns` to suppress brand false-positives at Sonnet prompt level
- 2-layer contract: Layer 1 candidates are explicitly confirmed or dismissed — no double-reporting, no missed catches
- Legal-mode is route-triggered automatically — no flag needed in customize.toml beyond keeping the skill enabled

---
description: Draft cookie consent policy and banner implementation guide
---

# Cookie Policy

Draft a cookie consent policy and banner implementation guide for "$ARGUMENTS". Generate a comprehensive cookie policy with practical implementation guidance for consent management.

> **Note:** AI-generated legal content does not constitute legal advice. Consult a qualified attorney.

## Prerequisites

Check that `.metapowers/legal/$ARGUMENTS/00-assess.md` exists. If it does not exist, stop and tell the user:

> "Run an Assess skill first (e.g. `/legal:risk-assessment $ARGUMENTS`) to generate the prerequisite assessment artifact."

If the user passes `--skip-checks`, bypass this check and log the skip to `.metapowers/legal/$ARGUMENTS/skip-log.md` with a timestamp and the reason "Prerequisite check skipped for cookie-policy".

## Process

1. **Read inputs:**
   - Read `.metapowers/legal/$ARGUMENTS/00-assess.md` for jurisdiction requirements and data practice context

2. **Draft cookie policy — explanatory sections:**

   - **What Cookies Are** — plain-language explanation of cookies and similar tracking technologies (pixels, web beacons, local storage, fingerprinting), accessible to non-technical readers
   - **Cookie Categories:**
     - **Strictly Necessary** — essential for site function (authentication, security, load balancing, shopping cart), cannot be disabled, no consent required
     - **Functional / Preferences** — remember user choices (language, region, display settings), enhance user experience but not essential
     - **Analytics / Performance** — measure site usage, traffic patterns, page performance (Google Analytics, Hotjar, etc.), used to improve the service
     - **Advertising / Marketing** — track users across sites, build interest profiles, deliver targeted ads, measure ad campaign effectiveness

3. **Draft cookie inventory table:**
   - For each cookie: name, provider (first-party or third-party with name), purpose, category, duration (session or persistent with expiry), data collected
   - Organize by category
   - Note: instruct the user to audit their actual cookies and update this table with real values

4. **Draft cookie management instructions:**
   - How to manage cookies through the consent banner (re-access preferences)
   - How to manage cookies per browser (Chrome, Firefox, Safari, Edge — link to browser documentation)
   - How to opt out of specific third-party cookies (Google, Meta, etc. — link to opt-out pages)
   - Impact of disabling cookies on site functionality per category

5. **Draft third-party cookie disclosures:**
   - List of third-party services that set cookies
   - Link to each third party's privacy/cookie policy
   - Purpose of each third-party integration
   - Data shared with third parties through cookies

6. **Draft consent mechanism description:**
   - How consent is collected (banner, preference center)
   - What constitutes valid consent (affirmative action, not pre-checked boxes)
   - How consent is recorded and stored
   - How users can withdraw consent
   - Consent expiry and re-consent frequency

7. **Draft policy update procedure:**
   - How changes to the cookie policy are communicated
   - Re-consent requirements when new cookie categories are added
   - Version history or changelog

8. **Draft banner implementation guide:**

   - **Consent requirements by jurisdiction:**
     - EU/EEA (ePrivacy Directive + GDPR): opt-in required for non-essential cookies, prior consent before setting cookies, granular category-level consent, no cookie walls (consent cannot be condition of access)
     - UK (UK GDPR + PECR): similar to EU, opt-in for non-essential
     - California (CCPA/CPRA): opt-out model for sale/sharing of personal information, "Do Not Sell or Share" link
     - Brazil (LGPD): consent-based, similar to GDPR approach
     - Other jurisdictions: default to opt-in as safest baseline

   - **Banner design recommendations:**
     - First layer: concise purpose statement, accept/reject buttons of equal prominence, link to cookie settings and full policy
     - Second layer (preference center): category-level toggles with descriptions, individual cookie details, save preferences button
     - Accessibility requirements: keyboard navigation, screen reader compatible, sufficient contrast
     - No dark patterns: no pre-checked boxes, no confusing button hierarchy, no hidden reject option

   - **Consent storage approach:**
     - Store consent state in a first-party cookie
     - Record consent timestamp, version, and granular choices
     - Sync consent with server-side records for audit trail
     - Recommended consent management platforms (CMP) for implementation

   - **Re-consent triggers:**
     - New cookie categories added
     - Significant changes to data processing purposes
     - Consent record older than 12 months (recommended refresh)
     - Change in applicable regulations

9. **Write the artifact** to `.metapowers/legal/$ARGUMENTS/01-draft.md` with frontmatter:

   ```
   ---
   description: Cookie policy and implementation guide draft for $ARGUMENTS
   ---
   ```

## Output

The cookie policy and implementation guide draft written to `.metapowers/legal/$ARGUMENTS/01-draft.md`. Present a summary to the user highlighting:
- Cookie categories defined and example cookies listed
- Jurisdictions addressed and consent model per jurisdiction
- Banner implementation recommendations
- Third-party cookie integrations identified
- Areas flagged for attorney review (especially consent mechanism compliance)

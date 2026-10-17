---
$schema: https://gist.githubusercontent.com/remorses/9f3737a6f516c01f4bdb612045c64072/raw/agent-skill.schema.json
name: stripe-disputes
description: >
  Stripe dispute and chargeback evidence workflow. Covers listing open disputes
  via CLI, collecting evidence from databases and APIs, generating evidence PDFs
  with react-pdf, capturing screenshots with Playwriter, rendering email images,
  and submitting evidence via Stripe CLI. Includes best practices for winning
  disputes on SaaS and digital products, Visa CE 3.0 prior undisputed transactions,
  per-reason-code evidence strategies, and file formatting rules. Load this skill
  when handling Stripe disputes, chargebacks, or generating evidence documents.
---

# Stripe disputes

Full workflow for responding to Stripe chargebacks: list disputes, collect evidence, generate PDFs, and submit. Focused on SaaS and digital product businesses.

## How disputes work

When a customer files a chargeback, you get **one chance** to submit evidence. The card issuer (customer's bank) makes the final decision. You typically have **7-21 days** to respond. Missing the deadline is an automatic loss.

Bank reviewers handle thousands of disputes daily and spend roughly **90 seconds per case**. Your evidence must be scannable, factual, and directly contradict the cardholder's claim.

## CLI workflow

All `stripe` commands must go through your secrets manager (doppler, sigillo, etc.) so the correct API key is injected. See the [stripe skill](../stripe/SKILL.md) for CLI auth setup.

### List open disputes needing response

```bash
# List disputes that need evidence (adapt doppler/sigillo to your project)
doppler run -c production -- stripe disputes list --limit 100 | \
  jq '[.data[] | select(.status == "needs_response" or .status == "warning_needs_response") | {
    id: .id,
    amount: (.amount / 100),
    currency: .currency,
    reason: .reason,
    status: .status,
    created: (.created | todate),
    due_by: (.evidence_details.due_by | todate),
    has_evidence: .evidence_details.has_evidence
  }]'
```

### One-liner for quick triage

```bash
doppler run -c production -- stripe disputes list --limit 100 | \
  jq '.data[] | select(.status == "needs_response") |
    "\(.id) | $\(.amount/100) \(.currency) | \(.reason) | due: \(.evidence_details.due_by | todate)"'
```

### Get details on a specific dispute

```bash
doppler run -c production -- stripe disputes retrieve dp_xxx | \
  jq '{
    id: .id, status: .status, amount: (.amount / 100), reason: .reason,
    due_by: (.evidence_details.due_by | todate),
    has_evidence: .evidence_details.has_evidence,
    submission_count: .evidence_details.submission_count,
    charge: .charge
  }'
```

### Find customer info from a dispute

```bash
# Get email and customer ID from the charge
doppler run -c production -- stripe charges retrieve ch_xxx | \
  jq '{customer: .customer, email: .billing_details.email, name: .billing_details.name}'
```

### Dispute statuses

| Status | Meaning | Action |
|---|---|---|
| `needs_response` | Must submit evidence | **Respond** |
| `warning_needs_response` | Early warning, evidence recommended | **Respond** |
| `under_review` | Evidence submitted, bank reviewing | Wait |
| `won` | Resolved in your favor | None |
| `lost` | Bank sided with customer | None |
| `charge_refunded` | You refunded instead of disputing | None |

## What bank reviewers look for

Reviewers skim, not read. Structure evidence to be scannable in 90 seconds:

- **Investigation Summary at the top** with bold key facts (this is all most reviewers read)
- **Chronological timeline** of events
- **Screenshots with annotations** (bold text, arrows, circles; avoid color highlighting)
- **Conclusion** restating the 3-4 strongest points

Keep it **factual, professional, and concise**. Never complain about the customer. Never include irrelevant evidence (e.g. return policy for a "not received" dispute).

## File constraints

| Constraint | Limit |
|---|---|
| File types | PDF, JPEG, PNG only |
| Combined file size | **4.5MB** |
| Page count | **< 50** (general), **19** (Mastercard) |
| Font size | **12pt minimum** (Stripe requirement) |
| Document size | US Letter or A4, portrait |
| Color highlighting | **Avoid** (use bold, callouts, arrows) |

## Evidence fields (Stripe API)

When submitting via CLI or API, these are the fields to populate:

| Field | What to put | Type |
|---|---|---|
| `access_activity_log` | Timestamped user actions with IPs | Text |
| `customer_email_address` | Email on the Stripe customer | Text |
| `customer_purchase_ip` | IP address at checkout | Text |
| `product_description` | Concise SaaS product description | Text |
| `service_date` | Date service was delivered | Text |
| `service_documentation` | PDF proving service was rendered | **File upload** |
| `customer_communication` | Emails you sent to the customer | **File upload** |
| `receipt` | **Auto-filled by Stripe** (do NOT upload manually) | Auto |

### Upload and review before submitting

Stripe lets you upload evidence **without submitting** by passing `--submit false` (or omitting `--submit`). This saves the evidence as a draft visible in the Stripe Dashboard, where you can review everything before clicking "Submit" in the UI.

**Always use this two-step flow:**

1. Upload files and attach evidence with `--submit false`
2. Open the dispute in the Stripe Dashboard and review the full evidence packet
3. Only then submit, either from the Dashboard UI or by running a second `stripe disputes update` with `--submit true`

This is critical because submission is **irreversible**. Once submitted, you cannot edit or add evidence.

**File uploads must use curl**, not `stripe files create -d`. The Stripe CLI's `-d` flag does not handle multipart file uploads correctly. Use curl with `-F` flags instead:

```bash
# 1. Get your Stripe API key
STRIPE_KEY=$(doppler run -c production -- printenv STRIPE_API_KEY)

# 2. Upload evidence files via curl (stripe CLI -d does NOT work for files)
curl -s https://files.stripe.com/v1/files \
  -u "$STRIPE_KEY:" \
  -F "purpose=dispute_evidence" \
  -F "file=@./evidence.pdf"
# Returns JSON with "id": "file_xxx" (save this ID)

curl -s https://files.stripe.com/v1/files \
  -u "$STRIPE_KEY:" \
  -F "purpose=dispute_evidence" \
  -F "file=@./email-evidence.png"
# Returns JSON with "id": "file_yyy" (save this ID)
```

**Attaching evidence must use `-d` with bracket syntax**, not `--evidence.xxx` flags. The dot-notation flags don't work for nested evidence params:

```bash
# 3. Attach evidence WITHOUT submitting (draft mode)
doppler run -c production -- stripe disputes update dp_xxx \
  -d "evidence[access_activity_log]=$(cat ./access-activity-log.txt)" \
  -d "evidence[customer_email_address]=user@example.com" \
  -d "evidence[customer_purchase_ip]=203.0.113.42" \
  -d "evidence[product_description]=Your SaaS product description here." \
  -d "evidence[service_date]=2025-12-09" \
  -d "evidence[service_documentation]=file_xxx" \
  -d "evidence[customer_communication]=file_yyy" \
  -d "submit=false"

# 4. Review in Dashboard: https://dashboard.stripe.com/disputes/dp_xxx
#    Check that all text fields, PDFs, and images look correct.

# 5. Submit ONLY after reviewing (irreversible)
doppler run -c production -- stripe disputes update dp_xxx \
  -d "submit=true"
```

### Verifying generated evidence before uploading

**Always visually inspect every PDF and image before uploading to Stripe.** Open each file and verify:

- The PDF renders correctly (no missing fonts, no blank pages, no cut-off content)
- Images are clear and legible (no white rectangles, no corrupt files)
- Screenshots show the intended content with annotations visible
- Email images have correct from/to/subject/body text
- The activity log text reads chronologically and makes sense

Use `open ./output/evidence-dp_xxx.pdf` on macOS to preview PDFs. For images, use `open ./output/email-xxx.png` or the `read-media` tool if running inside an agent.

When running as an agent, always use the `read-media` tool on generated images and PDFs to verify their content before printing the upload commands. Do not blindly upload files you haven't inspected.

### File reuse across disputes

Stripe does not allow the same uploaded file to be attached to multiple disputes. If you have 3 disputes for the same customer, you must upload the file 3 separate times (getting 3 different `file_xxx` IDs) even if the content is identical. Reusing a file ID that is already attached to another dispute returns: `"That file is already attached to something else."`

## What wins disputes for SaaS/digital products

Evidence ranked by strength (strongest first):

1. **Usage/access logs with timestamps and IPs** — proves the customer actively used the product after purchase. This is the single strongest piece of evidence for digital products.

2. **Proof of digital delivery** — screenshots of the delivered product (GitHub repos, dashboards, download confirmations, generated code).

3. **Custom emails sent** — welcome emails, delivery confirmations, onboarding messages. Render these as PNG images (see [Email evidence images](#email-evidence-images)).

4. **Prior undisputed transactions** (Visa CE 3.0) — 2+ prior charges from the same card that were not disputed. Proves the cardholder recognized and accepted charges from this merchant.

5. **No support contact** — prove the customer never reported an issue or contacted support before disputing. Shows the claim was filed without attempting resolution.

6. **Cancellation-to-dispute timeline** — disputes filed shortly after cancellation is a classic friendly fraud pattern ("subscription remorse").

7. **ToS/refund policy excerpt** — only the relevant section, never the entire document.

### What NOT to include

- **Stripe receipts** — Stripe auto-includes these in the `receipt` field. Uploading screenshots of Stripe receipts wastes page space on evidence the issuer already has.
- **Customer details table** — the issuer already has name, email, and billing address from the charge itself. Put these in the text fields (`--evidence.customer-email-address`) instead of the PDF.
- **Full terms of service** — only include the relevant excerpt with the specific clause highlighted.
- **Links to external websites** — reviewers will not click them. Screenshot the content instead.
- **Long explanations or complaints** — keep it factual and concise.

## Per-reason-code strategy

Tailor evidence to the specific dispute reason. Irrelevant evidence weakens your case.

### `product_unacceptable`

The customer claims the product was defective or unsatisfactory.

**Focus on:**
- Product **functioned as advertised** (feature verification, screenshots of working product)
- **Usage logs** showing the customer actively used the product
- **No support tickets** filed about functionality issues before the dispute
- Prior undisputed transactions (if customer paid for months without complaints)
- Cancellation timeline (disputes filed after cancellation = buyer's remorse)

### `product_not_received` (digital)

The customer claims they never received the product.

**Focus on:**
- **Access/download logs** with timestamps and IPs
- **Email notifications** confirming delivery
- **Screenshots** of the delivered digital product (repos, dashboards, accounts)
- Account activity showing the customer logged in and used the product

### `fraudulent`

The customer claims they did not authorize the transaction.

**Focus on:**
- **Authorization proof**: AVS match, CVC confirmation, 3D Secure authentication
- **IP address** matching billing address or historical user IPs
- **Prior undisputed transactions** (Visa CE 3.0; this is the strongest evidence for fraud disputes)
- Device fingerprint or customer account ID matching prior transactions

### `subscription_canceled`

The customer claims they canceled but were still charged.

**Focus on:**
- **No cancellation request** was received (check support logs, account settings)
- **Continued usage** after alleged cancellation date
- **Renewal reminder emails** sent before billing
- Subscription terms the customer agreed to at signup (relevant excerpt only)

## Visa Compelling Evidence 3.0 (CE 3.0)

CE 3.0 is the strongest tool for fighting friendly fraud on Visa transactions.

**Requirements:**
- Visa transaction with reason code 10.4 (card absent fraud)
- 2+ prior undisputed transactions from the same card, within 120-365 days
- Prior transactions must match on 2+ identifiers:
  - **Main**: customer purchase IP, shipping address
  - **Secondary**: device fingerprint, device ID, email, account ID
  - Valid combos: 2 main, or 1 main + 1 secondary

**Stripe auto-evaluates** eligibility and pre-populates evidence when possible. Check the Dashboard for CE 3.0 eligibility flags.

**In the PDF evidence**, highlight prior undisputed transactions prominently with a table showing charge date, amount, and whether it was disputed (YES/NO column).

## Generating evidence PDFs

Use `@react-pdf/renderer` to generate professional evidence PDFs. Load the [react-pdf skill](../react-pdf/SKILL.md) for full setup and typography guidance.

### Recommended structure

1. **Title**: "Dispute Evidence" (no subtitle clutter)
2. **Investigation Summary** (callout box with left-border accent): 3-5 bold key facts with arrow prefixes. This is the most important part; reviewers may read only this.
3. **Product Description**: concise description of the SaaS product
4. **Proof of Service Delivery**: activity timeline, exported components list, GitHub repo details
5. **Screenshots**: GitHub repos, delivered product, email images
6. **No Support Contact**: statement that customer never reported issues
7. **Prior Undisputed Transactions**: table with date, amount, disputed status
8. **Conclusion**: 3-4 bold bullet points restating strongest evidence

### Compact preset for evidence PDFs

Evidence PDFs should be dense. Use the compact preset from the react-pdf skill:

```tsx
const s = StyleSheet.create({
  page: {
    paddingTop: 36, paddingBottom: 36, paddingHorizontal: 48,
    fontFamily: 'Lora', fontSize: 9, lineHeight: 1.4, color: '#1a1a1a',
  },
  title: { fontSize: 16, fontWeight: 700, marginBottom: 16 },
  h2: { fontSize: 11, fontWeight: 700, marginTop: 10, marginBottom: 4 },
  h3: { fontSize: 10, fontWeight: 700, marginTop: 8, marginBottom: 3 },
  paragraph: { marginBottom: 4 },
})
```

### Investigation Summary callout

```tsx
<View style={{ borderLeftWidth: 2.5, borderLeftColor: '#1a1a1a', paddingLeft: 10, paddingVertical: 4 }}>
  <Text style={{ fontSize: 11, fontWeight: 700, marginBottom: 3 }}>Investigation Summary</Text>
  <KeyFact>Customer actively used the service on day 1 (exported 2 projects, 14 components)</KeyFact>
  <KeyFact>4 prior monthly charges were undisputed</KeyFact>
  <KeyFact>Disputes filed 8 days after cancellation</KeyFact>
  <KeyFact>No support contact before disputing</KeyFact>
</View>
```

```tsx
const KeyFact = ({ children }: { children: React.ReactNode }) => (
  <View style={{ flexDirection: 'row', marginBottom: 2, marginLeft: 2 }}>
    <Text style={{ width: 14, fontWeight: 700 }}>{'\u25B6'}</Text>
    <Text style={{ flex: 1, fontWeight: 700 }}>{children}</Text>
  </View>
)
```

### Gotchas

- **Lora font digit rendering**: numbered headings (1., 2., etc.) get their digits eaten by the Lora font subset in react-pdf. Use unnumbered headings instead.
- **Image max height**: constrain screenshot images with `maxHeight: 500` so they don't overflow pages. Use `wrap={false}` on image containers to prevent splitting across pages (but remove it if the image is taller than a page).
- **Stripe 12pt font requirement**: the compact preset uses 9pt for body text. Stripe's docs say 12pt minimum. In practice, 9-10pt works fine as long as text is legible. If you want to be strictly compliant, use 12pt but accept fewer pages of content.

## Email evidence images

Generate PNG images that look like the emails you sent to customers. These are uploaded as `customer_communication` evidence.

### Approach

1. Build an email layout with `@react-pdf/renderer` (subject, from, to, date, body)
2. Render to PDF buffer with `renderToBuffer`
3. Convert first page to PNG with `pdf-to-img`
4. Trim whitespace with ImageMagick

```tsx
import { renderToBuffer } from '@react-pdf/renderer'

// Render the email document to PDF
const pdfBuffer = await renderToBuffer(<EmailDocument email={emailData} />)

// Convert to PNG
const { pdf: pdfToImg } = await import('pdf-to-img')
const doc = await pdfToImg(Buffer.from(pdfBuffer), { scale: 2 })
let pageBuffer: Buffer | null = null
for await (const page of doc) {
  pageBuffer = Buffer.from(page)
  break // only need first page
}

// Trim whitespace with ImageMagick
import { execSync } from 'node:child_process'
const tmpPath = outputPath + '.tmp.png'
fs.writeFileSync(tmpPath, pageBuffer)
try {
  execSync(`convert "${tmpPath}" -trim +repage -bordercolor white -border 40x30 "${outputPath}"`, { stdio: 'pipe' })
  fs.unlinkSync(tmpPath)
} catch {
  // ImageMagick not available, use untrimmed image
  fs.renameSync(tmpPath, outputPath)
}
```

### Email layout component

Use a narrow page width (520pt) so the image is email-shaped, not full letter width. Set page height to 1000 (react-pdf doesn't support auto-height); the ImageMagick trim step removes the whitespace.

```tsx
function EmailDocument({ email }: { email: EmailData }) {
  return (
    <Document>
      <Page size={{ width: 520, height: 1000 }} style={pageStyle}>
        <HeaderField label="From:" value={email.from} />
        <HeaderField label="To:" value={email.to} />
        <HeaderField label="Date:" value={email.dateSent} />
        <Text style={subjectStyle}>{email.subject}</Text>
        <View style={hrStyle} />
        {email.lines.map((line, i) => (
          <Text key={i} style={paragraphStyle}>{line}</Text>
        ))}
      </Page>
    </Document>
  )
}
```

### Dependencies

```bash
pnpm add @react-pdf/renderer react pdf-to-img
```

ImageMagick (`convert` command) is optional but recommended for trimming. Install with `brew install imagemagick` on macOS.

## Capturing screenshots with Playwriter

Use Playwriter to capture screenshots of GitHub repos, dashboards, or any authenticated web page. Load the [playwriter skill](../../kimakivoice/cli/skills/playwriter/SKILL.md) for full setup.

```ts
// Navigate and screenshot
playwriter -s 1 -e 'state.page = await context.newPage(); await state.page.goto("https://github.com/org/repo"); await state.page.screenshot({ path: "/absolute/path/repo.png", fullPage: true })'
```

Screenshots are embedded in the evidence PDF as `<Image>` components.

## Collecting evidence from your database

The evidence collection script should query your database for:

- **Subscription details**: orgId, plugin name, status, creation date, cancellation date
- **Login sessions**: timestamps proving the customer accessed the product
- **Exported projects**: component counts, page counts, creation dates
- **GitHub repos**: repo names, creation dates, file counts, collaborator invites
- **Email history**: Resend message IDs, email content, send dates

Use `getPrismaForScripts()` (or your project's equivalent) for database access in scripts. Always run through doppler/sigillo for production queries.

## Activity logging (prevention)

To build strong evidence proactively, log user activity to a database table:

| Event | Data to capture |
|---|---|
| `CHECKOUT_COMPLETED` | IP from request headers, email, orgId |
| `PROJECT_EXPORTED` | Project name, component count, timestamp |
| `GITHUB_REPO_CREATED` | Repo name, file count |
| `COMPONENT_DOWNLOADED` | IP, timestamp, component IDs |
| `EMAIL_SENT` | Resend message ID, recipient, subject |
| `LOGIN` | IP, timestamp, session ID |

Each row should include: `orgId`, `userId`, `email`, `ip`, `event`, `metadata` (JSON), `createdAt`.

This table becomes the source for `access_activity_log` in dispute evidence. Without it, you have to reconstruct the timeline from scattered tables at dispute time.

## Automated dispute webhook (future)

For high-volume dispute handling, add a `charge.dispute.created` webhook handler that:

1. Looks up the org from the Stripe customer
2. Queries the activity log for that org
3. Formats the timeline as `access_activity_log` text
4. Generates the evidence PDF
5. Uploads files and submits evidence automatically

This is not required but significantly reduces response time and ensures no dispute is missed.

## References

- Stripe dispute best practices: https://docs.stripe.com/disputes/best-practices
- Stripe visual evidence examples: https://docs.stripe.com/disputes/visual-evidence
- Stripe dispute API: https://docs.stripe.com/api/disputes
- Visa CE 3.0: https://docs.stripe.com/disputes/api/visa-ce3
- Stripe responding to disputes: https://docs.stripe.com/disputes/responding

---
name: php-form-mailer
description: Wire any HTML form to a two-email PHP system. Generates a complete PHP handler that sends a structured notification email to the site owner and a branded HTML confirmation to the person who submitted, updates the form action and JS handler with a mailto fallback, then tests the live endpoint with curl. Works on any plain PHP host (cPanel, shared hosting) with no framework and no third-party form service.
---

# PHP Form Mailer: Two-Email System

You are a senior full-stack developer and email designer. Your job is to wire up a form so that one click of Submit fires two well-designed HTML emails automatically, with zero further action from anyone. No form SaaS, no monthly fee, no tracking pixel: plain PHP `mail()` on the user's own hosting.

## Step 0: Collect the configuration (never guess these)

Before writing any code, you need five values. Look for a `form-mailer.config.md` file in the project root first. If it does not exist, ask the user once for all five, then offer to save them to `form-mailer.config.md` for next time.

```
NOTIFY_EMAIL   The inbox that receives submission notifications (site owner)
BCC_EMAIL      Optional backup inbox copied on every email (leave empty to skip)
FROM_EMAIL     The sending address. MUST be a real mailbox on the hosting server,
               otherwise mail() fails silently on most shared hosts
SENDER_NAME    Human name shown in the From header of the confirmation email
BRAND_FOOTER   One footer line for both emails, e.g. "Studio Name, City" plus website URL
```

Never invent email addresses. Never reuse addresses from examples or other projects.

If the project is a public repository, warn the user that these addresses will be visible in the committed PHP file, and suggest keeping the handler out of the public repo or loading the values from a server-side config file excluded by `.gitignore`.

## Step 1: Read the HTML file

Before writing anything, read the target HTML file in full.

Extract exactly:
- The `<form>` element: its `id`, current `action`, and `method`
- Every `<input>`, `<textarea>`, `<select>`: their `name`, `id`, `type`
- Every radio/checkbox group: field `name` plus all `value` attributes plus the visible label text beside each one
- The existing JS form submission handler (the full `<script>` block)
- The project name (infer from the page `<title>` or hero heading)

Do not guess field names. Read them from the file.

## Step 2: Plan the PHP file name

Name the PHP file based on the project, e.g. `send_contact_email.php`, `send_questionnaire_email.php`. Place it in the same directory as the HTML file.

## Step 3: Write the PHP email handler

Write a complete PHP file. It must:

### Architecture
- Return `Content-Type: application/json`
- Reject non-POST with `405` and `{"ok":false,"error":"Method not allowed"}`
- Sanitise all inputs with `htmlspecialchars(trim($val ?? ''), ENT_QUOTES, 'UTF-8')`
- Include a hidden honeypot check: if the form has (or you add) a hidden field named `website`, silently return `200 {"ok":true}` when it is filled. Bots fill it, humans never see it.
- Send **Email 1** (notification to NOTIFY_EMAIL). On success respond `200 {"ok":true}`
- Send **Email 2** (confirmation to the submitter) only if their email field is not empty
- On mail failure respond `500 {"ok":false,"error":"Mail delivery failed"}`

### Radio/checkbox label maps
Build a `$labels` array that maps every radio/checkbox `value` to a readable human label, using the visible label text from the HTML:

```php
$labels = [
  'field_name' => [
    'value_a' => 'Human readable label A',
    'value_b' => 'Human readable label B',
  ],
];
```

Write a `label($group, $value)` helper that returns the readable label or falls back to the raw value.

### CRITICAL: PHP 8 compatibility
**Never use `$variable % 2` when `$variable` is a string.** This throws a `TypeError` in PHP 8. Use explicit string comparisons (`=== 'A'`, `=== 'B'`) for any conditional logic based on section letters.

### Email 1: owner notification (branded HTML)
- Background and accent colours taken from the project's own palette (CSS variables or hero colours)
- Header: project wordmark text, date, "New submission"
- Intro bar: submitter name bold, reply-to link to their email, phone if provided
- Answers table: grouped sections with alternating background rows
- Skip empty fields (check with `empty(trim(strip_tags($value)))`)
- Footer: BRAND_FOOTER plus "Confidential"
- `From: FROM_EMAIL`
- `Reply-To:` the submitter's email
- `Bcc: BCC_EMAIL` (only if configured)
- Subject: `=?UTF-8?B?` encoded, project name plus submitter name plus date

### Email 2: submitter confirmation (branded HTML)
- Same aesthetic as Email 1, branded header with project wordmark
- Personal greeting: "Dear [FirstName],"
- 2 to 3 sentences: thank you, what happens next, when to expect a reply
- Clean table of their answers (skip empty fields)
- "What happens next" callout box
- Footer: SENDER_NAME, BRAND_FOOTER, website link
- `From: SENDER_NAME <FROM_EMAIL>`
- `Reply-To: NOTIFY_EMAIL`
- `Bcc: BCC_EMAIL` (only if configured)
- Subject: `=?UTF-8?B?` encoded, "[Project]: Your message was received"

## Step 4: Update the HTML file

### 4a: Form action
Change the form `action` to the PHP file name (relative path):

```html
<form id="contactForm" action="send_contact_email.php" method="POST" novalidate>
```

### 4b: JS submission handler
Replace the existing JS handler with this pattern (adapt element ids to the actual page):

```javascript
const form      = document.getElementById('contactForm');
const submitBtn = document.getElementById('submitBtn');
const errorEl   = document.getElementById('form-error');
const successEl = document.getElementById('formSuccess');

const MAILTO_FALLBACK = 'NOTIFY_EMAIL_HERE';

form.addEventListener('submit', async e => {
  e.preventDefault();
  errorEl.textContent = '';

  const name  = form.name.value.trim();
  const email = form.email.value.trim();
  if (!name)                          { errorEl.textContent = 'Please enter your name.';              form.name.focus();  return; }
  if (!email || !email.includes('@')) { errorEl.textContent = 'Please enter a valid email address.'; form.email.focus(); return; }

  submitBtn.textContent = 'Sending…';
  submitBtn.disabled    = true;

  const data   = new FormData(form);
  const action = form.action;

  try {
    const res = await fetch(action, {
      method: 'POST',
      body: data,
      headers: { 'Accept': 'application/json' }
    });
    if (res.ok) {
      showSuccess();
    } else {
      submitViaMailto(data);
    }
  } catch (err) {
    submitViaMailto(data);
  }
});

function showSuccess() {
  form.style.display      = 'none';
  successEl.style.display = 'block';
  successEl.scrollIntoView({ behavior: 'smooth', block: 'center' });
}

function submitViaMailto(data) {
  const labels = { /* field name to readable label, one entry per field */ };
  const lines = ['[PROJECT NAME] form submission', ''];
  for (const [k, v] of data.entries()) {
    if (k.startsWith('_') || k === 'website' || !v) continue;
    lines.push((labels[k] || k) + ': ' + v);
  }
  const subject = encodeURIComponent('[Project]: form submission');
  const body    = encodeURIComponent(lines.join('\n'));
  const mailto  = 'mailto:' + MAILTO_FALLBACK + '?subject=' + subject + '&body=' + body;
  try { window.open(mailto, '_blank'); } catch (e) { window.location.href = mailto; }
  setTimeout(() => {
    submitBtn.textContent = 'Submit';
    submitBtn.disabled    = false;
    showSuccess();
  }, 1500);
}
```

Replace `NOTIFY_EMAIL_HERE` with the configured NOTIFY_EMAIL and populate the `labels` object with all field names from the form.

## Step 5: Test

After writing both files, ask:

> "Both files are ready. Upload **[php-filename]** and the updated **[html-filename]** to the same folder on your server, then let me know when done and I'll run the live test."

Once the user confirms upload, run a curl test against THEIR server (use a test address the user owns, never a third party):

```bash
curl -si -X POST "https://THEIR-DOMAIN/FOLDER/send_contact_email.php" \
  -F "name=Test Person" \
  -F "email=TEST_INBOX_THE_USER_OWNS" \
  -F "[other_required_fields]=test_value"
```

Include at least one value per radio group.

Check the response:
- `HTTP 200` plus `{"ok":true}`: working. Tell the user to check the inboxes (notification, confirmation, and BCC if configured).
- `HTTP 500` plus empty body: PHP fatal error, likely a PHP 8 type issue. Debug and fix.
- `HTTP 500` plus `{"ok":false}`: `mail()` failing. Check the `From:` address. It must be a real mailbox on the server.
- `HTTP 405`: hit with GET not POST (wrong URL or method).

Fix any issues and re-upload until you get `{"ok":true}`.

## Aesthetic reference

The emails should feel like part of the project's brand, not a generic transactional message. Pull colours and type choices from the project's CSS variables or hero palette.

Use table-based HTML email layout with inline styles only (no `<style>` blocks, many email clients ignore them). Pick a widely available font stack (Georgia for editorial brands, Arial/Helvetica for modern ones).

## Rules

- Never invent or reuse email addresses. Configuration comes from the user or their config file.
- Never send test emails to addresses the user does not own.
- Do not add tracking pixels, analytics, or external image hosts to the emails.
- Keep the handler self-contained: one PHP file, no Composer dependencies.

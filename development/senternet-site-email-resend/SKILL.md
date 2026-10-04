---
name: senternet-site-email-resend
description: Wire up Resend email sending through Firebase Functions.
---

# Email Sending via Resend

Add transactional email to a site using Resend + Firebase Cloud Functions v2. Stores the API key securely in Firebase Secret Manager, grants the correct service account permissions, and scaffolds a Cloud Function. Can be Firestore-triggered (fires when a document is created) or HTTP callable.

## Prerequisites

- `/senternet-site-firebase` must already be set up — this skill reads `.firebaserc` for project IDs.
- `/senternet-site-gcloud-auth` must have been run to authenticate this machine.

## Steps

### 1. Read `.firebaserc` to determine the prod project ID

```bash
cat .firebaserc
```

Extract the prod project ID (the value of `"prod"` or `"default"`). Use this as `$PROJECT_ID` throughout. Confirm with the user before proceeding.

### 2. Gather inputs before doing anything side-effectful

Ask the user for all of the following up front:

- **Resend API key** — will be stored in Secret Manager; never written to any file in the repo. Tell the user you'll prompt them to paste it in step 4. If they don't have one, they can sign up for a free account at resend.com — the free plan covers 3,000 emails/month and 100/day, which is sufficient for low-volume sites.
- **Notification email** — the internal/admin address that receives alerts (e.g. `alerts@example.com`).
- **FROM address** — the sender shown to email recipients, e.g. `My App <no-reply@mail.example.com>`. Remind the user that the domain (e.g. `mail.example.com`) must be verified in the Resend dashboard before this works.
- **Trigger type** — choose one:
  - **Firestore** — fires when a document is created; ask for the collection/document path pattern, e.g. `signups/{signupId}`.
  - **HTTP callable** — a Cloud Function that accepts a POST request with `{ to, subject, html, text }`.
- **Welcome email?** (Firestore trigger only) — whether to also send a welcome email to the submitter using a Resend email template. If yes, ask for the Resend template alias (e.g. `my-app-welcome`).

Do not proceed past this step until all required inputs are confirmed.

### 3. Enable required GCP APIs

```bash
gcloud services enable \
  secretmanager.googleapis.com \
  cloudfunctions.googleapis.com \
  cloudbuild.googleapis.com \
  artifactregistry.googleapis.com \
  run.googleapis.com \
  eventarc.googleapis.com \
  --project "$PROJECT_ID"
```

This is idempotent — already-enabled APIs are skipped automatically.

### 4. Store the Resend API key in Firebase Secret Manager

```bash
firebase functions:secrets:set RESEND_API_KEY --project "$PROJECT_ID"
```

Firebase will prompt the user to paste the key. It is stored server-side and never touches the repo.

### 5. Grant the compute service account Secret Manager access

Firebase Functions v2 runs under the project's default compute service account. Grant it the `secretAccessor` role so it can read `RESEND_API_KEY` at runtime:

```bash
PROJECT_NUMBER=$(gcloud projects describe "$PROJECT_ID" --project "$PROJECT_ID" --format='value(projectNumber)')

gcloud projects add-iam-policy-binding "$PROJECT_ID" \
  --project "$PROJECT_ID" \
  --member="serviceAccount:${PROJECT_NUMBER}-compute@developer.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"
```

If the binding already exists, `gcloud` will report it and continue without error.

### 6. Initialize the `functions/` directory

Only run if `functions/` does not already exist:

```bash
ls functions/ 2>/dev/null || (
  mkdir -p functions/src &&
  cd functions &&
  npm init -y &&
  npm install firebase-functions firebase-admin &&
  npm install -D typescript @types/node
)
```

Write `functions/tsconfig.json` only if it doesn't already exist:

```json
{
  "compilerOptions": {
    "module": "commonjs",
    "noImplicitReturns": true,
    "noUnusedLocals": true,
    "outDir": "lib",
    "sourceMap": true,
    "strict": true,
    "target": "es2017"
  },
  "compileOnSave": true,
  "include": ["src"]
}
```

Add a `"build": "tsc"` script to `functions/package.json` if not already present.

### 7. Write `functions/src/index.ts`

Write the file based on the trigger type chosen in step 2. Use the inputs gathered there to fill in constants.

**Firestore trigger variant:**

```typescript
// Customize trigger, recipients, and email content for this site.
import { onDocumentCreated } from 'firebase-functions/v2/firestore';
import { defineSecret } from 'firebase-functions/params';
import { setGlobalOptions } from 'firebase-functions/v2';

setGlobalOptions({ region: 'us-central1' });

const RESEND_API_KEY = defineSecret('RESEND_API_KEY');
const NOTIFICATION_EMAIL = '$NOTIFICATION_EMAIL';
const FROM_EMAIL = '$FROM_EMAIL';
const RESEND_ENDPOINT = 'https://api.resend.com/emails';
// const WELCOME_EMAIL_TEMPLATE_ALIAS = '$TEMPLATE_ALIAS'; // uncomment if sending welcome emails

interface SubmissionRecord {
  name?: string;
  email?: string;
  [key: string]: unknown;
}

function escapeHtml(value: string) {
  return value
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

function formatTimestamp(value: unknown) {
  if (!value) return 'unknown';
  if (typeof value === 'string') return value;
  if (typeof value === 'object' && value !== null && 'toDate' in value && typeof (value as { toDate: () => Date }).toDate === 'function') {
    return (value as { toDate: () => Date }).toDate().toISOString();
  }
  return 'unknown';
}

async function sendResendEmail(payload: Record<string, unknown>, idempotencyKey: string) {
  const response = await fetch(RESEND_ENDPOINT, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${RESEND_API_KEY.value()}`,
      'Content-Type': 'application/json',
      'Idempotency-Key': idempotencyKey,
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    const details = await response.text();
    throw new Error(`Resend email failed with ${response.status}: ${details}`);
  }
}

export const notifySubmission = onDocumentCreated(
  {
    document: '$COLLECTION_PATH',
    secrets: [RESEND_API_KEY],
  },
  async (event) => {
    const submission = event.data?.data() as SubmissionRecord | undefined;
    if (!submission?.email) {
      console.warn('Notification skipped: document did not include an email address.');
      return;
    }

    const name = submission.name?.trim() || 'Unknown';
    const email = submission.email.trim();
    const docId = Object.values(event.params)[0] as string;

    const subject = `New submission: ${name}`;
    const html = `
      <div style="font-family: Arial, sans-serif; line-height: 1.5; color: #1f2937;">
        <h2 style="margin: 0 0 12px;">New submission</h2>
        <p style="margin: 0 0 8px;"><strong>Name:</strong> ${escapeHtml(name)}</p>
        <p style="margin: 0 0 8px;"><strong>Email:</strong> ${escapeHtml(email)}</p>
        <p style="margin: 0 0 8px;"><strong>Timestamp:</strong> ${escapeHtml(formatTimestamp(submission.timestamp))}</p>
        <p style="margin: 0;"><strong>Document ID:</strong> ${escapeHtml(docId)}</p>
      </div>
    `;
    const text = [
      'New submission',
      `Name: ${name}`,
      `Email: ${email}`,
      `Document ID: ${docId}`,
    ].join('\n');

    const sends: Promise<void>[] = [
      sendResendEmail({ from: FROM_EMAIL, to: [NOTIFICATION_EMAIL], subject, html, text }, `notification/${event.id}`),
    ];

    // Uncomment to send a welcome email using a Resend template:
    // sends.push(sendResendEmail({
    //   to: [email],
    //   template: { id: WELCOME_EMAIL_TEMPLATE_ALIAS, variables: { NAME: name } },
    // }, `welcome/${event.id}`));

    await Promise.all(sends);
  },
);
```

Replace `$NOTIFICATION_EMAIL`, `$FROM_EMAIL`, and `$COLLECTION_PATH` with the values from step 2. If the user wants a welcome email, uncomment the template block and fill in `$TEMPLATE_ALIAS`.

**HTTP callable variant:**

```typescript
// Customize recipients and email content for this site.
import { onCall, HttpsError } from 'firebase-functions/v2/https';
import { defineSecret } from 'firebase-functions/params';
import { setGlobalOptions } from 'firebase-functions/v2';

setGlobalOptions({ region: 'us-central1' });

const RESEND_API_KEY = defineSecret('RESEND_API_KEY');
const FROM_EMAIL = '$FROM_EMAIL';
const RESEND_ENDPOINT = 'https://api.resend.com/emails';

interface SendEmailRequest {
  to: string;
  subject: string;
  html: string;
  text?: string;
}

export const sendEmail = onCall(
  { secrets: [RESEND_API_KEY] },
  async (request) => {
    const { to, subject, html, text } = request.data as SendEmailRequest;
    if (!to || !subject || !html) {
      throw new HttpsError('invalid-argument', 'to, subject, and html are required.');
    }

    const response = await fetch(RESEND_ENDPOINT, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${RESEND_API_KEY.value()}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ from: FROM_EMAIL, to: [to], subject, html, text }),
    });

    if (!response.ok) {
      const details = await response.text();
      throw new HttpsError('internal', `Resend email failed with ${response.status}: ${details}`);
    }

    return { success: true };
  },
);
```

Replace `$FROM_EMAIL` with the value from step 2.

### 8. Update `firebase.json` to include functions

If `firebase.json` does not already have a `"functions"` key, add it. The final file should look like:

```json
{
  "hosting": { ... },
  "functions": {
    "source": "functions",
    "predeploy": [
      "npm --prefix \"$RESOURCE_DIR\" ci",
      "npm --prefix \"$RESOURCE_DIR\" run build"
    ]
  }
}
```

Do not overwrite any existing hosting configuration.

### 9. Update `deploy:prod` in root `package.json`

Change `--only hosting` to `--only hosting,functions` in the `deploy:prod` script. On re-run, only update if `functions` is not already in the `--only` flag.

### 10. Add `.gitignore` entries for the functions build output

Check the root `.gitignore` and add these lines if they are not already present:

```
functions/lib/
functions/node_modules/
```

### 11. Deploy and verify

```bash
firebase deploy --only functions --project "$PROJECT_ID"
```

After deploy succeeds, tell the user to trigger the function (create a Firestore document in the collection, or call the HTTP endpoint) and then check the logs:

```bash
gcloud functions logs read --project "$PROJECT_ID" --limit 20
```

A successful notification will show no errors in the logs. If there is a `403 Forbidden` from Secret Manager, recheck step 5.

## Notes

- The Resend sender domain (e.g. `mail.example.com`) must be verified in the Resend dashboard at resend.com before FROM addresses on that domain will be accepted. This is done outside this skill.
- The API key is stored server-side in Firebase Secret Manager and is injected at runtime via `defineSecret`. It is never written to `.env` files, committed to the repo, or logged.
- Idempotency keys on `sendResendEmail` (using `event.id` as the prefix) prevent duplicate emails if the Cloud Function retries.
- If re-running this skill on a project that already has `functions/`, skip step 6 and only update `index.ts` if the user confirms.
- If the site does not yet have Firestore enabled, Firebase will prompt to enable it during the first deploy with a Firestore trigger.

## Framework: Next.js track

Do not add a `functions/` directory to a Next.js site. The send path is a route handler in the same app:

```ts
// app/api/contact/route.ts
import { NextResponse } from 'next/server';

export async function POST(request: Request) {
  const body = await request.json();
  // validate, then call Resend with process.env.RESEND_API_KEY
  return NextResponse.json({ ok: true });
}
```

- **The API key is a Secret Manager reference in `apphosting.yaml`**, with `RUNTIME` availability only. Never `NEXT_PUBLIC_`-prefix it, and never give it `BUILD` availability — either one ships it to the browser.
  ```yaml
  env:
    - variable: RESEND_API_KEY
      secret: resend-api-key
      availability: [RUNTIME]
  ```
  Create and grant it with `firebase apphosting:secrets:set resend-api-key` and `firebase apphosting:secrets:grantaccess resend-api-key --backend "$BACKEND_ID"`.
- **Route handlers are server-only by default** — the key never reaches the client bundle as long as it is read inside the handler and not passed through props.
- **No `firebase.json` rewrites and no `hosting,functions` deploy target.** The endpoint is just a path in the app.
- Rate limiting and validation still matter: a public POST handler that sends mail is an open relay if it does neither.
- For local development, put the key in `.env.local` (untracked) — the emulator/secret plumbing of the Functions track does not apply here.

See `/senternet-site-framework` for the full convention map.

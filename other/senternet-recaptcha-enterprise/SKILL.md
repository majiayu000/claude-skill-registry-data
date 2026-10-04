---
name: senternet-recaptcha-enterprise
description: Enable reCAPTCHA Enterprise and create host-scoped keys for local, dev, and prod forms.
---

# reCAPTCHA Enterprise for Forms

Create separate reCAPTCHA Enterprise web keys for local, dev, and prod form flows. Use a testing key for local, and regular keys for dev/prod, each restricted to the correct hosts.

## Prerequisites

- Run `/senternet-site-gcloud-auth` first so `gcloud` is authenticated.
- Know the GCP project ID and the hostnames for local, dev, and prod.
- If the site has a `.firebaserc`, use its project IDs as the source of truth.

## Steps

### 1. Confirm the inputs

Before making changes, confirm:

- `$PROJECT_ID`
- `$SITE_NAME` or another short display-name prefix
- `$LOCAL_HOSTS`
- `$PROD_HOSTS`
- `$DEV_HOSTS` if dev is enabled

Use comma-separated hostnames only. Do not include a scheme, path, port, or query string.

Recommended host patterns:

- Local: `localhost`
- Dev: your stable dev hostname, if you have one
- Prod: the canonical production hostname(s)

### 2. Enable the reCAPTCHA Enterprise API

```bash
gcloud services enable recaptchaenterprise.googleapis.com --project "$PROJECT_ID"
```

### 3. Create the local testing key

Use a testing key for local so automated and manual form testing does not get blocked by challenge behavior.

```bash
gcloud recaptcha keys create \
  --project "$PROJECT_ID" \
  --display-name="$SITE_NAME local" \
  --web \
  --integration-type=score \
  --domains="$LOCAL_HOSTS" \
  --testing-score=1.0
```

Keep `$LOCAL_HOSTS` limited to local-only hosts such as `localhost`. Do not include production hosts in the local key.

### 4. Create the prod key

```bash
gcloud recaptcha keys create \
  --project "$PROJECT_ID" \
  --display-name="$SITE_NAME prod" \
  --web \
  --integration-type=score \
  --domains="$PROD_HOSTS"
```

### 5. Create the dev key if dev is enabled

Only run this when the site has a real dev environment.

```bash
gcloud recaptcha keys create \
  --project "$PROJECT_ID" \
  --display-name="$SITE_NAME dev" \
  --web \
  --integration-type=score \
  --domains="$DEV_HOSTS"
```

### 6. Capture the site keys

`gcloud recaptcha keys create` returns a key resource name. Use the final path segment as the site key value for the frontend.

If you want the site key directly in shell output:

```bash
gcloud recaptcha keys create ... --format='value(name)'
```

Then take the portion after the final `/`.

### 7. Verify the keys

```bash
gcloud recaptcha keys list --project "$PROJECT_ID"
```

Confirm that:

- the local key is testing-only and scoped to local hosts
- the dev key, if created, is scoped only to dev hosts
- the prod key is scoped only to prod hosts

## Notes

- Use separate keys per environment. Do not reuse the prod key in local or dev.
- Host restrictions are enforced by `--domains`.
- Only use `--allow-all-domains` if you have a very large host list and understand the security tradeoff.
- Testing keys created with `--testing-score` are meant for local testing and should not be used for production traffic.

## Framework: Next.js track

Key creation, the host-scoped local/dev/prod split, and the score thresholds are unchanged — those are Google Cloud concerns, not framework concerns.

Wiring differences:

- The site key is public: `NEXT_PUBLIC_RECAPTCHA_SITE_KEY`, and it must also appear in `apphosting.yaml` with `BUILD` availability.
- Token generation runs in the browser, so the component that calls `grecaptcha.enterprise.execute()` is `'use client'`.
- **Assessment happens in a route handler** (`app/api/<form>/route.ts`), not a Cloud Function. Verify the token there before doing anything with the submission.
- Any API key or service credential used for the assessment call is a `secret:` ref in `apphosting.yaml` with `RUNTIME` availability only — never `NEXT_PUBLIC_`.
- If a CSP is in place, reCAPTCHA needs `https://www.google.com` and `https://www.gstatic.com` in `script-src` and `frame-src`.

See `/senternet-site-framework` for the full convention map.

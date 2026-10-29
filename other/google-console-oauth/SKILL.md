---
name: google-console-oauth
description: >
  Create a Google OAuth app (consent screen + Web client) in Google Cloud console with
  Playwriter, for "Sign in with Google" in a product (better-auth, Google login). Covers the
  Google Auth Platform pages (Branding, Audience, Clients, Data Access), publishing to
  "In production" with External user type, and storing GOOGLE_CLIENT_ID / GOOGLE_CLIENT_SECRET
  in Sigillo without printing the secret. Load when asked to create Google OAuth credentials,
  a Google client id, or to publish a Google consent screen.
---

# google-console-oauth

Create one Google OAuth app per product, ready for any Google account to sign in.

```
user creates GCP project ──▶ Branding ──▶ Audience: External ──▶ Data Access: basic scopes
                                                                        │
                Sigillo ◀── Download JSON ◀── Clients: Web app ◀────────┘
                                                                        │
                       /privacy + /terms live ──▶ Branding URLs ──▶ Publish: In production
```

Drive the console with Playwriter in the user's Chrome. Load the `playwriter` skill first.

## Rules

- **The user creates the Google Cloud project** (and org if any). Never create projects yourself. If the user did not give a project id, ask for it and stop.
- **One OAuth app per project.** A project has exactly one consent screen. Never reuse another product's project or client. Never share a client between products.
- **Always External and In production.** Never pick Internal. Never leave it in Testing, and never add test users as a workaround.
- **No logo, no app icon.** Uploading a logo forces Google verification. Leave it empty.
- **Basic scopes only:** `openid`, `.../auth/userinfo.email`, `.../auth/userinfo.profile`. They need no verification. Sensitive scopes (Search Console, Gmail, Drive) show the "unverified app" screen until verified. Never add them to the login app.
- **Never print the client secret.** Download the client JSON and pipe it straight into Sigillo.

## Console pages

All pages take `?project=<PROJECT_ID>`.

| Page | URL |
|---|---|
| Overview / first setup | `https://console.cloud.google.com/auth/overview?project=<ID>` |
| Branding | `https://console.cloud.google.com/auth/branding?project=<ID>` |
| Audience | `https://console.cloud.google.com/auth/audience?project=<ID>` |
| Clients | `https://console.cloud.google.com/auth/clients?project=<ID>` |
| Data Access (scopes) | `https://console.cloud.google.com/auth/scopes?project=<ID>` |

## Steps

1. **Check the product has `/privacy` and `/terms` pages live** (curl both, expect 200). Google refuses to publish without a homepage and a privacy policy URL. If they are missing, add them to the app and deploy first.
2. **Overview → Get started** (first time only): app name = product name, user support email = the signed-in account, audience **External**, contact email = same account, accept the policy, Create.
3. **Branding**: set only these fields, nothing else:
   - App name, user support email
   - Application home page `https://<domain>`
   - Privacy policy `https://<domain>/privacy`, terms `https://<domain>/terms`
   - Authorized domain `<domain>`
   - Developer contact email
4. **Data Access**: only the three basic scopes. Save.
5. **Clients → Create client** → type **Web application**, name `<product>-website`:
   - JavaScript origins: `https://<domain>`, `http://localhost:<dev-port>`
   - Redirect URIs (better-auth): `https://<domain>/api/auth/callback/google`, `http://localhost:<dev-port>/api/auth/callback/google`
6. **Store the credentials.** In the "OAuth client created" dialog click **Download JSON**, then:

   ```bash
   F=$(ls -t ~/Downloads/client_secret_*.json | head -1)
   jq -r .web.client_id "$F" | tr -d '\n' | sigillo secrets set GOOGLE_CLIENT_ID -p <SIGILLO_PROJECT> -c dev -c prod
   jq -r .web.client_secret "$F" | tr -d '\n' | sigillo secrets set GOOGLE_CLIENT_SECRET -p <SIGILLO_PROJECT> -c dev -c prod
   rm "$F"
   ```

7. **Audience → Publish app → Confirm.** Verify the page shows **Publishing status: In production** and **User type: External**.
8. **Test the real login** with Playwriter on the deployed site: click "Continue with Google", pick an account, accept, and check you land back signed in.

## Gotchas

- **"Publish app" is disabled** with "complete your configuration on the Branding page": the homepage or privacy policy URL is empty. Read the button's `aria-describedby` text to see the exact reason:

  ```js
  await state.page.evaluate(() => {
    const b = [...document.querySelectorAll('button')].find((x) => /Publish app/.test(x.textContent))
    return (b?.getAttribute('aria-describedby') || '').split(' ').map((id) => document.getElementById(id)?.textContent).join(' | ')
  })
  ```

- **The authorized domain cannot be deleted** while a client lists it in its origins or redirect URIs. That is expected; keep it.
- **The console is a heavy Angular app.** Playwriter calls that chain many actions time out. Do one or two actions per call, and wait for a known textbox with `locator.waitFor()` after each `goto`.
- **Save stays disabled** when nothing changed from the saved state. That means the values are already saved.
- **New client settings take up to a few minutes** to apply. A `redirect_uri_mismatch` right after creating the client can fix itself.
- The consent screen language follows the Google account, so button names change (`Continue` / `Continua`). Match with regex or by role order.

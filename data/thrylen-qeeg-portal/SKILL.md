---
name: thrylen-qeeg-portal
description: "Maintain the Thrylen qEEG clinician portal hosted on Netlify (thrylen.com/qeeg and optionally qeeg.thrylen.com): shared login, patient folders (MM-DD-YYYY-N), versioned file uploads, and authenticated downloads backed by Netlify Blobs. Use when updating portal UI, functions, env vars, blob storage layout, or deployments."
---

# Thrylen qEEG Portal (Netlify)

## Overview

Operate the qEEG clinician portal served from the `thrylen` repo via Netlify: password login, patient folders, versioned file uploads, and authenticated downloads backed by Netlify Blobs.

## Key Locations

- Repo root: `/Users/davidmontgomery/thrylen`
- Portal UI (static): `public/qeeg/*`
- Netlify functions: `netlify/functions/qeeg-*.js` and `netlify/functions/_shared/qeeg.js`
- Routing: `netlify.toml`
- Local→Netlify sync helpers: `scripts/qeeg_patients_sync.mjs`, `scripts/qeeg_patients_watch.mjs`

Local (gitignored) clinician-share staging folder:

- `/Users/davidmontgomery/qEEG-analysis/data/portal_patients/<MM-DD-YYYY-N>/`

## URLs And Routing

- Main portal: `https://thrylen.com/qeeg/`
- Optional: `https://qeeg.thrylen.com/` (add domain + DNS in Netlify; `netlify.toml` already rewrites `/` on that host to `/qeeg/index.html`)
- API functions: `/.netlify/functions/qeeg-*`

## Netlify Environment Variables (Do Not Commit)

- `QEEG_PORTAL_USERNAME` (default `clinic`)
- `QEEG_PORTAL_PASSWORD` (secret)
- `QEEG_AUTH_KEY` (secret; signing key for the `qeeg_session` cookie)
- `QEEG_BLOBS_STORE` (default `qeeg-portal`)
- `QEEG_AUTH_RATE_STORE` (optional; default `qeeg-auth-rate`)

Run Netlify env commands from `/Users/davidmontgomery/thrylen` after `netlify link`:

```bash
netlify env:set QEEG_PORTAL_PASSWORD '...' --context production --scope functions
```

## Deploy

```bash
cd /Users/davidmontgomery/thrylen
netlify deploy --prod --dir public --functions netlify/functions --no-build
```

## Publish Local Patient Folders To Netlify

Sync everything once:

```bash
cd /Users/davidmontgomery/thrylen
npm run qeeg:patients:sync -- --dir /Users/davidmontgomery/qEEG-analysis/data/portal_patients
```

Watch for changes and auto-upload new versions:

```bash
cd /Users/davidmontgomery/thrylen
npm run qeeg:patients:watch -- --dir /Users/davidmontgomery/qEEG-analysis/data/portal_patients
```

## Blob Storage Layout

Patient folders (all artifacts live under a patient ID):

- Patient meta: `patients/<MM-DD-YYYY-N>/$meta.json`
- Optional index (fallback listing): `patients/<MM-DD-YYYY-N>/$index.json`
- Files: `patients/<MM-DD-YYYY-N>/files/<patientId>__<name>__v<version>__YYYY-MM-DD.<ext>`

Files store user metadata (encoded in `x-amz-meta-user`) including `originalName`, `logicalName`, `version`, `uploadedAt`, `uploadedBy`, `size`, `contentType`.

## API Endpoints (Functions)

- Auth: `qeeg-login`, `qeeg-me`, `qeeg-logout`
- Patients: `qeeg-patients` (list folders), `qeeg-patient-files` (list files)
- Upload: `qeeg-upload` (multipart form upload; stores files into Blobs under the patient folder)
- Download: `qeeg-download` (auth-gated redirect to signed URL)

## Notes On Netlify Limits

- Downloads use signed URLs (large-friendly).
- Browser uploads go through Netlify Functions, so keep portal uploads small (PDFs/notes). For larger items (especially MP4), publish via the local sync tool (`qeeg:patients:sync` / `qeeg:patients:watch`).

## Troubleshooting

- “No project id found”: run commands inside `/Users/davidmontgomery/thrylen` (or run `netlify link`).
- Login fails: verify `QEEG_PORTAL_USERNAME`, `QEEG_PORTAL_PASSWORD`, and `QEEG_AUTH_KEY` are set for Functions scope.
- Upload fails (browser): check function logs for `qeeg-upload` and look for CORS errors on the signed upload URL PUT.
- Files missing: confirm blobs exist under the `patients/` prefix and that `qeeg-patients` can list them.

---
name: google-auth
description: >-
  Use when authenticating to Google APIs (GA4, Search Console, Ads, Sheets) via
  service account, Application Default Credentials, or OAuth, or when
  GOOGLE_APPLICATION_CREDENTIALS / ADC setup fails.
---

# Google Auth

Shared credentials for Google Analytics, Search Console, and related APIs.

## Prefer order

1. MCP servers already configured with `GOOGLE_APPLICATION_CREDENTIALS`
2. Service account JSON path in env
3. Application Default Credentials (`gcloud auth application-default login`)

## Required env

| Variable | Purpose |
|----------|---------|
| `GOOGLE_APPLICATION_CREDENTIALS` | Absolute path to service-account JSON |
| `GOOGLE_CLOUD_PROJECT` | GCP project id (GA MCP / quota project) |

Resolve missing values via `skills/integrations/obsidian-secrets/` then `.env.local`.

## Service account checklist

1. Create (or reuse) a GCP service account in `GOOGLE_CLOUD_PROJECT`.
2. Enable APIs: **Google Analytics Data API**, **Google Search Console API** (and Ads if needed).
3. Download JSON key → set `GOOGLE_APPLICATION_CREDENTIALS`.
4. **GA4:** Admin → Property access → add SA email as Viewer (or Analyst).
5. **GSC:** Settings → Users → add SA email as Full or Restricted.
6. Never commit the JSON key; keep path in `.env.local` only.

## Scopes (REST / client libraries)

| Product | Readonly scope |
|---------|----------------|
| GA4 Data API | `https://www.googleapis.com/auth/analytics.readonly` |
| Search Console | `https://www.googleapis.com/auth/webmasters.readonly` |

## Python ADC pattern

```python
from google.auth import default

credentials, project = default(
    scopes=["https://www.googleapis.com/auth/analytics.readonly"]
)
```

## Common failures

| Symptom | Fix |
|---------|-----|
| `Could not load default credentials` | Set `GOOGLE_APPLICATION_CREDENTIALS` or run ADC login |
| `User does not have sufficient permissions` | Grant SA access on the GA4 property / GSC site |
| `API not enabled` | Enable the API on the GCP project |
| 403 on property | Wrong `GA4_PROPERTY_ID` or SA not added to that property |

## Related

- `skills/integrations/google-analytics/`
- `skills/integrations/google-search-console/`
- `skills/org/TOOL-REGISTRY.md`

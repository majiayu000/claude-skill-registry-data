---
name: privacy-no-phi-review
description: Use when changing inputs, storage, telemetry, URLs, logs, uploads, exports, examples, or deployment for projects that may involve health data.
---

# Privacy And No-PHI Review

- Assume user-entered clinical values may be sensitive even when not directly identifying.
- Prefer fully client-side computation with no persistence, telemetry, backend, or third-party submission.
- Do not put patient values in URLs, logs, analytics events, screenshots, or committed fixtures.
- Use synthetic or clearly de-identified fixtures only.
- If storage or network transmission is requested, document the data path, retention, and compliance assumptions before implementation.

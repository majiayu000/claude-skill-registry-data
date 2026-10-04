---
name: apple-privacy-telemetry
description: Design privacy-bounded OSLog, MetricKit, and OTLP telemetry. Use when adding diagnostics or auditing collection; never to justify content capture.
license: MIT
metadata:
  author: "coryparrry"
  version: "0.1.0"
  last-updated: "2026-08-30"
  last-reviewed: "2026-08-30"
  apple-docs-reviewed: "2026-08-30"
---

# Apple Privacy Telemetry

Build content-free observability for bounded operational decisions.

## Invariants

- Do not collect, log, buffer, or export pixels/media, OCR or user text, clipboard/model payloads, titles, paths/URLs/bodies/headers, secrets, tokens, contact data, or stable user/device identifiers by default.
- Hashing forbidden content is not anonymization. OSLog private/hash masks control local display, not collection or export permission.
- Enforce a closed typed allowlist before fan-out. Unknown events, keys, values, and schemas fail closed; arbitrary attributes and error descriptions never bypass policy.
- Keep app events and MetricKit reports as separate ingress paths, each sanitized into an approved envelope before any sink.
- Remote export is vendor-neutral, encrypted, explicitly enabled as product policy requires, and bounded in fields, endpoint, cardinality, queue, retries, retention, and access. Debug capture is release-excluded, explicit, local, and short-lived.

## Route

1. State each operational question, necessary field, retention, and local/remote/third-party flow.
2. Read [references/telemetry-contract.md](references/telemetry-contract.md) to design typed OSLog, MetricKit, and optional OTLP boundaries.
3. Read [references/verification.md](references/verification.md) to prove prohibited values cannot cross policy and to verify release configuration and real export output.
4. Read [references/apple-documentation.md](references/apple-documentation.md) before changing OSLog, MetricKit, privacy-manifest, or required-reason guidance.

Align actual collection with `PrivacyInfo.xcprivacy`, App Store disclosures, consent, support documentation, and privacy policy; never invent reason codes. Report the schema, purpose, flows, allowlist, enablement, retention, negative evidence, disclosure consequences, and unresolved gaps. Do not claim “anonymous,” “no personal data,” or “privacy-safe” without evidence for that exact statement.

## Review

- Last updated: **2026-08-30**
- Last reviewed: **2026-08-30**
- Apple documentation reviewed: **2026-08-30**
- OSLog, MetricKit, privacy-manifest, and required-reason guidance was reviewed with Xcode MCP `DocumentationSearch`; see [Apple documentation evidence](references/apple-documentation.md).

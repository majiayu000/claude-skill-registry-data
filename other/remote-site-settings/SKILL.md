---
name: remote-site-settings
description: "Use when configuring Remote Site Settings to allow Apex callouts to external URLs, or when distinguishing Remote Site Settings from CSP Trusted Sites for Lightning component resource loading. NOT for Named Credentials (use named-credential-configuration)."
category: admin
salesforce-version: "Spring '25+"
well-architected-pillars:
  - Security
  - Reliability
triggers:
  - "Apex callout is failing with CalloutException even though I added the URL to CSP Trusted Sites"
  - "How do I allow Salesforce to call an external REST API from Apex?"
  - "Remote Site Settings not included in Change Set — callouts failing after deployment"
  - "What is the difference between Remote Site Settings and CSP Trusted Sites?"
  - "Apex Http.send() is throwing an error in production but works in sandbox"
tags:
  - remote-site-settings
  - apex-callout
  - csp-trusted-sites
  - integration-admin
  - callout-security
inputs:
  - "External endpoint URL that Apex code needs to call (including protocol: https://)"
  - "Whether the issue is a failing Apex callout or a Lightning component resource loading issue"
  - "Whether the endpoint is being added via Change Set or Metadata API"
outputs:
  - "Remote Site Setting configuration for the external endpoint"
  - "Distinction guidance: Remote Site Settings vs. CSP Trusted Sites"
  - "Change Set inclusion steps for Remote Site Settings"
  - "Metadata API RemoteSiteSetting deployment configuration"
dependencies: []
version: 1.0.0
author: Pranav Nagrecha
updated: 2026-04-12
---

# Remote Site Settings and CSP Trusted Sites

This skill activates when a practitioner needs to configure external endpoint access for Apex callouts (Remote Site Settings) or when troubleshooting the common confusion between Remote Site Settings (server-side Apex callout gate) and CSP Trusted Sites (browser-side Lightning component resource gate). It covers the most critical anti-pattern in this domain: adding a URL to CSP Trusted Sites to fix a failing Apex callout.

---

## Before Starting

Gather this context before working on anything in this domain:

- **Server-side vs. browser-side**: Remote Site Settings and CSP Trusted Sites are completely separate security controls for completely different scenarios. Remote Site Settings gate server-side Apex callouts. CSP Trusted Sites gate browser-side resource loading in Lightning components. Adding a URL to the wrong control does nothing.
- **Most critical misconception**: Adding an endpoint to CSP Trusted Sites does NOT fix a failing Apex Http.send() callout. Apex callouts are server-side — they are gated exclusively by Remote Site Settings, not CSP. This is the most common misdirection in Salesforce integration troubleshooting.
- **Change Set gotcha**: Remote Site Settings are deployable Metadata API components (type `RemoteSiteSetting`) but are NOT automatically included in Change Sets by default. Omitting them is the most common cause of Apex callout failures immediately after a production deployment.

---

## Core Concepts

### Remote Site Settings — Server-Side Apex Callout Gate

Remote Site Settings (Setup > Security > Remote Site Settings) are a platform-level allowlist that governs which external URLs Salesforce Apex code can call via `Http.send()`. Every external URL that an Apex class calls must have a matching Remote Site Setting registered, or the callout is denied at the platform level with a `CalloutException: Unauthorized endpoint` error.

Key characteristics:
- Applied per org — not per user or per profile.
- URL matching is prefix-based: a Remote Site Setting for `https://api.example.com` covers all paths under that domain.
- Protocol matters: `https://api.example.com` and `http://api.example.com` are different entries.
- Remote Site Settings are metadata (type `RemoteSiteSetting`) and can be deployed via Metadata API, Change Sets, or SFDX.
- Remote Site Settings are NOT included in Change Sets by default — they must be manually added.

### CSP Trusted Sites — Browser-Side Lightning Component Gate

CSP Trusted Sites (Setup > Security > CSP Trusted Sites) configure the Content Security Policy header returned by Salesforce to the user's browser. CSP controls what external resources (scripts, styles, images, fonts, connections) Lightning components can load or call from the user's browser session.

Key characteristics:
- Applied per org at the browser level.
- Different directives control different resource types: `connect-src` for fetch/XHR, `script-src` for JavaScript, `img-src` for images.
- CSP Trusted Sites have NO effect on server-side Apex callouts (`Http.send()`).
- A Lightning component making an XHR/fetch call to an external API from the browser needs a CSP Trusted Site. An Apex class making the same call from the server needs a Remote Site Setting.

### Metadata API Deployment

Remote Site Settings are deployed as `RemoteSiteSetting` metadata type:

```xml
<!-- RemoteSiteSetting: ExternalPaymentGateway.remoteSite -->
<?xml version="1.0" encoding="UTF-8"?>
<RemoteSiteSetting xmlns="http://soap.sforce.com/2006/04/metadata">
    <description>Payment gateway endpoint for Apex callouts</description>
    <disableProtocolSecurity>false</disableProtocolSecurity>
    <isActive>true</isActive>
    <url>https://api.paymentgateway.com</url>
</RemoteSiteSetting>
```

Deploy via `sf project deploy start` or include in Change Set (must add explicitly in the "Add" tab under Remote Site Settings component type).

---

## Common Patterns

### Fixing a Failing Apex Callout

**When to use:** An Apex class using `Http.send()` throws `CalloutException: Unauthorized endpoint, please check Setup>Security>Remote Site Settings`.

**How it works:**
1. Identify the exact URL being called in the Apex code (including protocol and domain).
2. Navigate to Setup > Security > Remote Site Settings.
3. Click New Remote Site.
4. Enter a name (alphanumeric, no spaces), the URL (e.g., `https://api.example.com`), and optionally a description.
5. Check "Disable Protocol Security" only if the external service uses HTTP (not HTTPS) — leave unchecked for HTTPS.
6. Save and test the Apex callout.

### Including Remote Site Settings in a Change Set

**When to use:** Deploying Apex code that makes callouts from sandbox to production via Change Set.

**How it works:**
1. In the Change Set, click Add.
2. Under Component Type, select "Remote Site Setting."
3. Add each required Remote Site Setting.
4. Deploy the Change Set — the Remote Site Setting will be created in the target org.

If Remote Site Settings are not in the Change Set, the Apex code deploys successfully but callouts immediately fail in production with `Unauthorized endpoint` errors.

---

## Decision Guidance

| Situation | Correct Control | Why |
|---|---|---|
| Apex Http.send() failing with Unauthorized endpoint | Remote Site Setting | Apex callouts are server-side; only Remote Site Settings gate them |
| Lightning component fetch/XHR failing (browser error) | CSP Trusted Site | Browser-side resource loading is gated by CSP, not Remote Site Settings |
| Both Apex and Lightning need to call the same endpoint | BOTH Remote Site Setting AND CSP Trusted Site | Server-side and browser-side are separate gates |
| Apex callout working in sandbox, failing in production | Add Remote Site Setting to Change Set | Remote Site Settings not included in Change Sets by default |
| Need to disable HTTPS certificate validation | disableProtocolSecurity: true in metadata | Only for non-HTTPS or self-signed cert scenarios; security risk |
| Using Named Credentials for callouts | Not applicable — Named Credentials manage their own URL allowlist | Named Credentials replace Remote Site Settings for the configured endpoint |

---

## Recommended Workflow

Step-by-step instructions for an AI agent or practitioner working on this task:

1. **Identify the error type** — Determine whether the failing call is from Apex server-side code (`Http.send()`) or from a Lightning component in the user's browser (fetch, XHR, img.src). The error source determines which control to configure.
2. **For Apex callout failures** — Navigate to Setup > Security > Remote Site Settings. Verify the calling URL is registered. If not, add a new Remote Site Setting with the exact protocol and domain.
3. **For Lightning component resource failures** — Navigate to Setup > Security > CSP Trusted Sites. Add a new trusted site entry for the external URL with the appropriate directive (connect-src for XHR/fetch, script-src for scripts).
4. **For Change Set deployments** — In the Change Set, explicitly add each Remote Site Setting under component type "Remote Site Setting" before uploading. Do not assume metadata deployment of Apex automatically includes the Remote Site Settings it depends on.
5. **For Metadata API / SFDX deployments** — Include `RemoteSiteSetting` metadata files in the deployment package. The file name must match the Remote Site Setting name in the org.
6. **Test the callout** — After adding the Remote Site Setting, test the Apex callout (via anonymous Apex or the relevant trigger/class). Confirm no `CalloutException: Unauthorized endpoint` error.
7. **Document the dependency** — Add a comment near the Apex callout code indicating which Remote Site Setting is required. This prevents future Change Set deployments from omitting it.

---

## Review Checklist

Run through these before marking work in this area complete:

- [ ] Remote Site Setting added for every external URL called via Apex Http.send()
- [ ] CSP Trusted Site added for every external URL accessed by Lightning components in the browser
- [ ] Remote Site Settings explicitly included in any Change Set that includes Apex code using them
- [ ] Remote Site Setting metadata files included in Metadata API / SFDX deployment packages
- [ ] Apex callout tested successfully after configuration
- [ ] Named Credentials evaluated as an alternative (preferred over Remote Site Settings for credential management)

---

## Salesforce-Specific Gotchas

Non-obvious platform behaviors that cause real production problems:

1. **Adding a URL to CSP Trusted Sites does not fix a failing Apex callout** — Apex `Http.send()` is a server-side call. CSP controls browser-side resource loading. They are completely separate. A CSP Trusted Site entry for an endpoint does nothing to unblock an Apex callout to the same endpoint. This is the single most common misdirection in Salesforce integration troubleshooting, confirmed by the number of support cases and community posts following this path.
2. **Remote Site Settings not included in Change Sets by default** — When assembling a Change Set that includes Apex classes making external callouts, the Remote Site Settings those classes depend on must be explicitly added as a separate component type. The Change Set tool does not automatically detect or include them as a dependency. This is the most common cause of Apex callout failures in production immediately after a Change Set deployment.
3. **Protocol in URL matters — http:// and https:// are separate entries** — A Remote Site Setting for `https://api.example.com` does not cover `http://api.example.com`, and vice versa. If the Apex code uses HTTPS but the Remote Site Setting was created with HTTP (or the URL was entered without the correct protocol), the callout fails. Always verify the exact protocol in the callout URL matches the Remote Site Setting.

---

## Output Artifacts

| Artifact | Description |
|---|---|
| Remote Site Setting configuration | Setup > Security > Remote Site Settings entry for the external endpoint |
| CSP Trusted Site configuration | Setup > Security > CSP Trusted Sites entry for browser-side access |
| RemoteSiteSetting metadata XML | Deployable metadata file for SFDX/Change Set deployment |
| Change Set inclusion guide | Steps to add Remote Site Settings to a Change Set explicitly |

---

## Related Skills

- integration-admin-connected-apps — Configure connected apps for OAuth-based integration authentication
- integration-user-management — Set up the integration user whose callouts will use these settings

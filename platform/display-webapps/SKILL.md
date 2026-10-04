---
name: display-webapps
description: Build display experiences for Meta Ray-Ban Display, choosing between native DAT display integration and standalone Wearables Web Apps. Do not use for Ray-Ban Meta models without a display.
---

# Meta Ray-Ban Display — Native DAT or Web App

This skill is only for display-capable glasses.

## Choose the path

Use **DAT display** when:

- The experience is an extension of an existing iOS/Android app.
- Native mobile state, authentication, background services, or camera integration is central.
- The user specifically wants Kotlin/Swift.

Use **Web Apps** when:

- The experience should run as a standalone display surface.
- HTML/CSS/JavaScript is sufficient.
- Fast iteration/deployment by URL is desirable.
- The feature can live within the documented Web App browser capabilities.

## Web App constraints from the official toolkit snapshot

The official Meta Web App toolkit documents these design constraints:

- 600 × 600 px display viewport.
- Directional/D-pad style navigation through the supported wearable input path.
- Dark/black backgrounds are important for an additive transparent display.
- High contrast is important for readability.
- Interactive elements must be focusable and keyboard-navigation friendly.
- Deployment requires a publicly available HTTPS URL for on-device use.

Always verify current constraints with `search_webapps_docs` before final implementation.

## Web App implementation defaults

- Start with semantic HTML and a small dependency footprint.
- Support Arrow keys + Enter in desktop testing.
- Make focus visible and deterministic.
- Keep text large and concise.
- Avoid layouts that require precise pointer input.
- Avoid dense dashboards and long scrolling screens.
- Prefer one primary task per screen.
- Use platform sensors only through capabilities confirmed in current docs.

## Native display implementation

When using DAT display:

- Confirm display-capable device selection.
- Keep the phone app as the control/data layer where appropriate.
- Use only currently documented display UI primitives.
- Design for glanceability and low interaction cost.
- Handle the case where a connected device does not expose the display capability.

## Never do this

Do not add display code to Ray-Ban Meta Gen 1/2 unless the user has explicitly identified a display-capable device and current docs confirm it.

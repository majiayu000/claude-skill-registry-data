---
name: cadet-client-capabilities
description: Truthful answers about what the Cadet client apps can and cannot do on the user's device. Device location and GPS are unavailable in every client and there is no location permission prompt to approve, so location requests are answered by asking for a typed city or address instead.
compatibility: "Designed for Cadet personal assistants"
metadata:
  emoji: "📍"
  cadet:
    category: "system"
    display-name: "Cadet Client Capabilities"
    activation-hints:
      - "asked to use the user's current location, GPS, or device position"
      - "whether the app can access a device sensor, permission, or hardware feature"
      - "browsing failed, timed out, or could not reach a page that needs a login"
      - "whether to install the desktop app or Chrome extension"
    avoid-when:
      - "the user already gave a location as text (just use it)"
---

## Critical Rule

Never claim that a permission prompt, sheet, dialog, or button is on the user's screen unless a tool result in this conversation actually presented one. Some capabilities do have real permission prompts (microphone access for voice, enabling notifications), but those appear when the user takes an action inside the client UI. The assistant cannot summon one into view, and pointing the user at UI that is not there strands them mid-task with no way to comply.

## Device Location

No Cadet client can read the device's location. Not the web app, not the macOS or Windows desktop apps, not the iOS or Android apps, not the CLI. There is no GPS access, no geolocation integration, and no location permission flow that could be triggered or approved.

When the user asks you to use their current, live, or nearby location:

1. Say plainly that you cannot access device location.
2. Ask them to type a city, address, or place name instead. Weather, search, and nearby-place requests all work from a typed location.
3. Continue the task with what they give you.

Do not stall the task waiting for a permission grant that cannot arrive, and do not send the user to OS settings; there is no Cadet entry there to enable.

### The one coarse signal that exists

Settings has a "Timezone" field, set by searching for a city or UTC offset. If it is set, you may offer it as a rough default region, but present it as the configured timezone rather than the user's detected location, and let them correct it.

### If the user asks for real location support

It does not exist today in any client. The honest answer is that they can mention a place per request, or set the Timezone field in Settings as a standing default.

## Shipped Clients

Tell the user only what is actually downloadable. Do not invent a Linux desktop installer.

- Web app: https://mycadet.ai
- iOS: https://apps.apple.com/us/app/mycadet/id6759934423
- Android: https://play.google.com/store/apps/details?id=ai.mycadet.android
- macOS and Windows desktop: https://mycadet.ai/downloads
- Chrome extension: https://chromewebstore.google.com/detail/mycadet-browser/hphbdmpffeigpcdjkckleobjmhhokpne
- Linux desktop: not shipped. Use the web app or Chrome extension. The runtime can self-host on Linux; that is the server, not a desktop app.

For install, pricing, or "how do I install you" questions, also load `cadet-self-knowledge` and fetch Installation, FAQ, and Pricing from the docs. Do not answer those from memory.

## Desktop App And Chrome Extension

When a task needs a logged-in browser or a host computer (internal pages, company SSO, VPN-only dashboards, local files, or host shell):

1. Offer the desktop app for Mac or Windows: https://mycadet.ai/downloads
2. For browser sessions, also offer the Chrome extension: https://chromewebstore.google.com/detail/mycadet-browser/hphbdmpffeigpcdjkckleobjmhhokpne
3. Offer those first. Only ask for a screenshot or pasted page content if the user cannot install either.

On iOS or Android there is no in-app browser, no Chrome extension to install on the phone, and no host computer. Offer the desktop app or Chrome extension on a computer. Do not describe a browser panel, local browser session picker, or other UI that is not on this phone.

## Other Device Capabilities

If you are unsure whether a client can do something on the device (camera, contacts, sensors, background audio, and so on), check a source of truth such as the product docs before answering, or say you are unsure. Never assume a capability exists because typical mobile apps have it, and never describe UI for it that you have not seen presented.

---
name: deep-linking
description: Deep links, universal links and app links in React Native. Use when links do not open the app, for apple-app-site-association or assetlinks.json, lost cold-start links, expo-router linking, custom URL schemes.
user-invocable: false
---

# Deep links that open the app every time

## Two layers, different jobs

- **Custom schemes** (`myapp://...`): trivial to set up, work from inside your own emails and QR flows, but any app can claim a scheme and browsers treat them as second-class. Fallback layer.
- **Universal links (iOS) / App links (Android)** (`https://yourdomain.com/...`): the real thing. They need server-side proof files and that is where every setup fails.

Ship both: schemes for internal redirects (OAuth return, payment return), https links for anything a user might tap outside the app.

## iOS: the AASA file and Apple's CDN

The proof file lives at `https://yourdomain.com/.well-known/apple-app-site-association`: HTTPS, no redirects, JSON body, appID as `TEAMID.bundleid`. The entitlement side is `applinks:yourdomain.com` (Expo: `associatedDomains` in app config).

The part that costs people days: **devices do not fetch your file directly**. Apple's CDN fetches it (first pickup within about a day) and caches it, so an AASA fix is not live when your server says it is. For development there is an alternate mode: entitlement `applinks:yourdomain.com?mode=developer` plus the device's developer mode skips the CDN. Use it for iteration, remove it for release builds.

If links still open Safari instead of the app: long-press the link and check for the "Open in app" option, confirm the file is reachable with `curl -i` (status 200, no redirect chain), and remember that pasting a URL into Safari's address bar deliberately does NOT trigger universal links; tap one from Notes or Messages instead.

## Android: assetlinks.json and the signing key trap

The proof file lives at `https://yourdomain.com/.well-known/assetlinks.json` with the app's package name and the SHA-256 fingerprint of the **certificate that signs what ships**. The trap: with Play App Signing (the norm), Google re-signs your app, so the fingerprint must come from Play Console's App integrity page (the app signing key), NOT from your upload key or local keystore. A local-keystore fingerprint makes verification fail silently and only in production, which is the worst combination.

Add fingerprints additively: dev builds and store builds can both live in the file. Intent filters need `android:autoVerify="true"` on the https filter. Check verification state on a device with:

```bash
adb shell pm get-app-links your.package.name
```

`verified` next to the domain is the goal; anything else names the failing domain.

## Cold start vs warm start, the classic lost link

A link that launches the app arrives through the initial-URL path; a link tapped while the app runs arrives through the URL event. Handling only the event listener means cold-start links vanish, and that is the most common deep-link bug report. expo-router handles both when the scheme and domains are configured, but anything custom (auth guards, splash gates, onboarding redirects) must re-apply the pending link AFTER the gate resolves, or the user lands on the home screen and the link dies.

Test both paths explicitly: once with the app killed, once with it backgrounded.

## Testing without a website deploy

```bash
# custom scheme, both platforms
npx uri-scheme open "myapp://lesson/42" --ios
npx uri-scheme open "myapp://lesson/42" --android

# https links on Android without waiting for verification
adb shell am start -a android.intent.action.VIEW -d "https://yourdomain.com/lesson/42" your.package.name
```

iOS https links cannot be faked from the terminal in the same way; that is what `mode=developer` exists for.

## Adjacent traps

- OAuth and payment providers redirect back via your scheme or https link; a changed scheme breaks sign-in in the field, so treat the scheme as API surface and never rename it casually.
- Deferred deep links (install, then first open lands on content) are not a platform feature; they require an attribution/linking service. Do not promise the product team otherwise.
- Every route a link can open must handle "referenced thing is gone" gracefully; links outlive content.

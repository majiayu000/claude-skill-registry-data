---
name: adattributionkit
description: "Measure ad effectiveness with privacy-preserving attribution using AdAttributionKit. Use when registering ad impressions, handling attribution postbacks, updating conversion values, implementing re-engagement attribution, configuring publisher or advertiser apps, or replacing SKAdNetwork with AdAttributionKit for ad measurement."
---

# AdAttributionKit

Privacy-preserving ad attribution for iOS 17.4+ / Swift 6.3. AdAttributionKit
lets ad networks measure conversions (installs and re-engagements) without
exposing user-level data. It supports the App Store and alternative
marketplaces, and interoperates with SKAdNetwork.

Three roles exist in the attribution flow: the **ad network** (signs
impressions, receives postbacks), the **publisher app** (displays ads), and the
**advertised app** (the app being promoted).

## Contents

- [Overview and Privacy Model](#overview-and-privacy-model)
- [Publisher App Setup](#publisher-app-setup)
- [Advertiser App Setup](#advertiser-app-setup)
- [Impressions](#impressions)
- [Postbacks](#postbacks)
- [Conversion Values](#conversion-values)
- [Re-engagement](#re-engagement)
- [Common Mistakes](#common-mistakes)
- [Review Checklist](#review-checklist)
- [References](#references)

## Overview and Privacy Model

AdAttributionKit preserves user privacy through several mechanisms:

- **Crowd anonymity tiers** -- the device limits postback data granularity based
  on the crowd size associated with the ad, ranging from Tier 0 (minimal data)
  to Tier 3 (most data including publisher ID and country code).
- **Time-delayed postbacks** -- postbacks are sent 24-48 hours after conversion
  window close (first window) or 24-144 hours (second/third windows).
- **No user-level identifiers** -- postbacks contain aggregate source
  identifiers and conversion values, not device or user IDs.
- **Hierarchical source identifiers** -- 2, 3, or 4-digit source IDs where the
  number of digits returned depends on the crowd anonymity tier.

The system evaluates impressions from both AdAttributionKit and SKAdNetwork
together when determining attribution winners. Only one impression wins per
conversion. Click-through ads always take precedence over view-through ads,
with recency as the tiebreaker within each group.

## Publisher App Setup

A publisher app displays ads from registered ad networks. Add each ad network's
ID to the app's Info.plist so its impressions qualify for install validation.

### Add ad network identifiers

```xml
<key>AdNetworkIdentifiers</key>
<array>
    <string>example123.adattributionkit</string>
    <string>another456.adattributionkit</string>
</array>
```

Ad network IDs must be lowercase. SKAdNetwork IDs (ending in `.skadnetwork`)
are also accepted -- the frameworks share IDs.

### Display a UIEventAttributionView

For click-through custom-rendered ads, overlay a `UIEventAttributionView` on
the ad content. The system requires a tap on this view before `handleTap()`
succeeds.

```swift
import UIKit

let attributionView = UIEventAttributionView()
attributionView.frame = adContentView.bounds
attributionView.isUserInteractionEnabled = true
adContentView.addSubview(attributionView)
```

## Advertiser App Setup

The advertised app is the app someone installs or re-engages with after seeing
an ad. It must call a conversion value update at least once to begin the
postback conversion window.

### Opt in to receive winning postback copies

Add the `AttributionCopyEndpoint` key to Info.plist so the device sends a copy
of the winning postback to your server:

```xml
<key>AdAttributionKit</key>
<dict>
    <key>AttributionCopyEndpoint</key>
    <string>https://example.com</string>
</dict>
```

The system generates a well-known path from the domain:

```
https://example.com/.well-known/appattribution/report-attribution/
```

Configure your server to accept HTTPS POST requests at that path. The domain
must have a valid SSL certificate.

### Opt in for re-engagement postback copies

Add a second key to also receive copies of winning re-engagement postbacks:

```xml
<key>AdAttributionKit</key>
<dict>
    <key>AttributionCopyEndpoint</key>
    <string>https://example.com</string>
    <key>OptInForReengagementPostbackCopies</key>
    <true/>
</dict>
```

### Update conversion value on first launch

Call a conversion value update as early as possible after first launch to begin
the conversion window:

```swift
import AdAttributionKit

func applicationDidFinishLaunching() async {
    do {
        try await Postback.updateConversionValue(0, lockPostback: false)
    } catch {
        print("Failed to set initial conversion value: \(error)")
    }
}
```

## Impressions

Ad networks create signed impressions using JWS (JSON Web Signature). The
publisher app uses `AppImpression` to register and handle those impressions.

### Create an impression from a JWS

```swift
import AdAttributionKit

let impression = try await AppImpression(compactJWS: signedJWSString)
```

The JWS contains the ad network ID, advertised item ID, publisher item ID,
source identifier, timestamp, and optional re-engagement eligibility flag. See
[references/adattributionkit-patterns.md](references/adattributionkit-patterns.md)
for JWS generation details.

### Check device support

```swift
guard AppImpression.isSupported else {
    // Fall back to alternative ad display
    return
}
```

### View-through impressions

Record a view impression when the ad content has been displayed and dismissed:

```swift
func handleAdViewed(impression: AppImpression) async {
    do {
        try await impression.handleView()
    } catch {
        print("Failed to record view-through impression: \(error)")
    }
}
```

For long-lived ad views, use `beginView()` and `endView()` to track view
duration:

```swift
try await impression.beginView()
// ... ad remains visible ...
try await impression.endView()
```

### Click-through impressions

Respond to ad taps by calling `handleTap()`. If the advertised app is not
installed, the system opens its App Store or marketplace page. If installed,
the system launches it directly.

```swift
func handleAdTapped(impression: AppImpression) async {
    do {
        try await impression.handleTap()
    } catch {
        print("Failed to record click-through impression: \(error)")
    }
}
```

A `UIEventAttributionView` must overlay the ad for `handleTap()` to succeed.

### StoreKit-rendered ads

Pass the impression to StoreKit overlay or product view controller APIs. StoreKit
automatically records view-through impressions after 2 seconds of display and
click-through impressions on tap.

```swift
import StoreKit

let config = SKOverlay.AppConfiguration(appIdentifier: "1234567890",
                                         position: .bottom)
config.appImpression = impression
```

## Postbacks

Postbacks are attribution reports the device sends to ad networks (and
optionally to the advertised app developer) after a conversion event.

### Conversion windows

Three windows produce up to three postbacks for winning attributions:

| Window | Duration            | Postback delay    |
|--------|---------------------|-------------------|
| 1st    | Days 0-2            | 24-48 hours       |
| 2nd    | Days 3-7            | 24-144 hours      |
| 3rd    | Days 8-35           | 24-144 hours      |

Tier 0 postbacks only produce the first postback. Nonwinning attributions
produce only one postback.

### Time windows for events

| Event                          | Time limit                              |
|--------------------------------|-----------------------------------------|
| View-through to install        | 24 hours (configurable up to 7 days)    |
| Click-through to install       | 30 days (configurable down to 1 day)    |
| Install to first update        | 60 days                                 |
| Re-engagement to first update  | 2 days                                  |

### Lock conversion values early

Lock the postback to finalize a conversion value before the window ends and
receive the postback sooner:

```swift
try await Postback.updateConversionValue(
    42,
    coarseConversionValue: .high,
    lockPostback: true
)
```

After locking, the system ignores further updates in that conversion window.

### Postback data by tier

| Field                        | Tier 0 | Tier 1      | Tier 2      | Tier 3      |
|------------------------------|--------|-------------|-------------|-------------|
| `source-identifier` digits   | 2      | 2           | 2-4         | 2-4         |
| `conversion-value` (fine)    | --     | --          | 1st only    | 1st only    |
| `coarse-conversion-value`    | --     | 1st only    | 2nd/3rd     | 2nd/3rd     |
| `publisher-item-identifier`  | --     | --          | --          | Yes         |
| `country-code`               | --     | --          | --          | Conditional |

## Conversion Values

### Fine-grained values

An integer from 0-63 (6 bits). Available only in the first postback and only at
Tier 2 or higher:

```swift
try await Postback.updateConversionValue(
    35,
    coarseConversionValue: .medium,
    lockPostback: false
)
```

### Coarse values

Three levels for lower tiers and second/third postbacks:

```swift
// CoarseConversionValue cases: .low, .medium, .high
try await Postback.updateConversionValue(
    10,
    coarseConversionValue: .high,
    lockPostback: false
)
```

### Update by conversion type (iOS 18+)

Separate conversion values for install vs. re-engagement postbacks:

```swift
let installUpdate = PostbackUpdate(
    fineConversionValue: 20,
    lockPostback: false,
    conversionTypes: [.install]
)
try await Postback.updateConversionValue(installUpdate)

let reengagementUpdate = PostbackUpdate(
    fineConversionValue: 12,
    lockPostback: false,
    conversionTypes: [.reengagement]
)
try await Postback.updateConversionValue(reengagementUpdate)
```

### Conversion tags (iOS 18.4+)

Use conversion tags to selectively update specific postbacks when overlapping
conversion windows exist:

```swift
let update = PostbackUpdate(
    fineConversionValue: 15,
    lockPostback: false,
    conversionTag: savedConversionTag,
    conversionTypes: [.reengagement]
)
try await Postback.updateConversionValue(update)
```

The system delivers the conversion tag through the re-engagement URL's
`AdAttributionKitReengagementOpen` query parameter.

## Re-engagement

Re-engagement tracks users who already have the advertised app installed and
interact with an ad to return to it.

### Mark impressions as re-engagement eligible

Set `eligible-for-re-engagement` to `true` in the JWS payload when generating
the impression.

### Handle re-engagement taps with a URL

Pass a universal link that the system opens in the advertised app:

```swift
let reengagementURL = URL(string: "https://example.com/promo/summer")!
try await impression.handleTap(reengagementURL: reengagementURL)
```

The system appends `AdAttributionKitReengagementOpen` as a query parameter. The
advertised app checks for this parameter to detect AdAttributionKit-driven
opens:

```swift
func handleUniversalLink(_ url: URL) {
    let components = URLComponents(url: url, resolvingAgainstBaseURL: false)
    let isReengagement = components?.queryItems?.contains(where: {
        $0.name == Postback.reengagementOpenURLParameter
    }) ?? false

    if isReengagement {
        // AdAttributionKit opened this app via a re-engagement ad
    }
}
```

### Re-engagement limits

- Only click-through interactions create re-engagement postbacks (not
  view-through).
- The device enforces monthly per-app and yearly per-device re-engagement
  limits.
- The `AdAttributionKitReengagementOpen` parameter is always present on the
  URL, even when the system does not create a postback.

## Common Mistakes

### Forgetting to update conversion value on launch

```swift
// DON'T -- never updating the conversion value
func appDidLaunch() {
    // No conversion value update; postback window never starts
}

// DO -- update conversion value on first launch
func appDidLaunch() async {
    try? await Postback.updateConversionValue(0, lockPostback: false)
}
```

### Using uppercase ad network IDs

```xml
<!-- DON'T -->
<string>Example123.AdAttributionKit</string>

<!-- DO -->
<string>example123.adattributionkit</string>
```

### Calling handleTap without UIEventAttributionView

```swift
// DON'T -- tap without attribution view overlay
try await impression.handleTap()
// Throws AdAttributionKitError.missingAttributionView

// DO -- ensure UIEventAttributionView covers the ad
let attributionView = UIEventAttributionView()
attributionView.frame = adView.bounds
adView.addSubview(attributionView)
// Then handle the tap after the user taps the attribution view
try await impression.handleTap()
```

### Ignoring handleTap errors

```swift
// DON'T
try? await impression.handleTap()

// DO -- handle specific errors
do {
    try await impression.handleTap()
} catch let error as AdAttributionKitError {
    switch error {
    case .impressionExpired:
        // Impression older than 30 days
        refreshAdImpression()
    case .missingAttributionView:
        // UIEventAttributionView not present
        break
    default:
        print("Attribution error: \(error)")
    }
}
```

### Not responding to postback requests

```swift
// DON'T -- silently dropping the request
// The device retries up to 9 times over 9 days on HTTP 500

// DO -- respond with 200 OK immediately
// Server handler:
func handlePostback(request: Request) -> Response {
    // Process asynchronously, respond immediately
    Task { await processPostback(request.body) }
    return Response(status: .ok)
}
```

## Review Checklist

- [ ] Publisher app includes all ad network IDs in `AdNetworkIdentifiers`
  (lowercase)
- [ ] Ad network IDs match between publisher app's Info.plist and JWS `kid`
- [ ] `UIEventAttributionView` overlays ad content for click-through ads
- [ ] Advertised app calls `updateConversionValue` on first launch
- [ ] Server endpoint at well-known path accepts HTTPS POST with valid SSL
- [ ] Postback verification uses correct Apple public key for environment
- [ ] Duplicate postbacks filtered by `postback-identifier`
- [ ] Server responds with HTTP 200 to postback requests
- [ ] Re-engagement URL is a registered universal link for the advertised app
- [ ] Conversion value strategy accounts for all three conversion windows
- [ ] `AppImpression.isSupported` checked before attempting impression APIs

## References

- [references/adattributionkit-patterns.md](references/adattributionkit-patterns.md)
  -- postback verification, server handling, testing, SKAdNetwork migration,
  alternative marketplaces, attribution rules configuration
- [Apple: AdAttributionKit](https://sosumi.ai/documentation/adattributionkit)
- [Apple: Presenting ads in your app](https://sosumi.ai/documentation/adattributionkit/presenting-ads-in-your-app)
- [Apple: Receiving ad attributions and postbacks](https://sosumi.ai/documentation/adattributionkit/receiving-ad-attributions-and-postbacks)
- [Apple: Verifying a postback](https://sosumi.ai/documentation/adattributionkit/verifying-a-postback)
- [Apple: SKAdNetwork interoperability](https://sosumi.ai/documentation/adattributionkit/adattributionkit-skadnetwork-interoperability)

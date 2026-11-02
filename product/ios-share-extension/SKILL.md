---
name: ios-share-extension
description: "Use when adding an iOS Share Extension (share-sheet target) to an app — receiving images/video/URLs/text from other apps, handing the payload to the containing app via an App Group, and the ONE working pattern for opening the containing app from the extension (UIResponder chain + open:options:completionHandler: with nil options). Every rejected approach is documented so it is never retried. Also carries the zero-cost web-app counterpart (a user-built iOS Shortcut that opens a compose URL). Triggers on Share Extension, share sheet, NSExtension, extensionContext, App Group handoff, \"share to my app\", openURL from extension, LSApplicationQueriesSchemes."
---

# iOS Share Extension

Shipped pattern from a production App Store client app: a Share
Extension that accepts image / video / URL / text from any app's share
sheet, stages the payload, and opens the containing app to finish the
action (e.g. compose a post). The whole feature is three moves — and
one of them has exactly one working implementation.

## 1. Intake: NSItemProvider → App Group

- The extension reads `extensionContext?.inputItems` and loads each
  attachment by `UTType` (image, movie, url, plain-text).
- **Binary payloads go into the App Group container** (an
  `appGroupID` shared with the main app); small metadata (type, text,
  URL string) goes into App Group `UserDefaults`. The extension
  process is short-lived and memory-capped (~120 MB) — write files,
  don't hold data.
- Both targets declare the same App Group capability; the extension's
  `Info.plist` declares its `NSExtensionActivationRule` for the types
  it accepts.

## 2. Opening the containing app — the ONLY working pattern

`UIApplication` exists in the extension's process but
`UIApplication.shared` is restricted. Traverse the responder chain and
call the modern selector **with `nil` options**:

```swift
let selector = NSSelectorFromString("openURL:options:completionHandler:")
var responder: UIResponder? = self
while let r = responder {
    if r.responds(to: selector) {
        typealias OpenFunc = @convention(c)
            (AnyObject, Selector, NSURL, NSDictionary?, ((Bool) -> Void)?) -> Void
        let open = unsafeBitCast(r.method(for: selector), to: OpenFunc.self)
        open(r, selector, url as NSURL, nil, nil)
        break
    }
    responder = r.next
}
extensionContext?.completeRequest(returningItems: [], completionHandler: nil)
```

The extension's `Info.plist` must also declare
`LSApplicationQueriesSchemes: [yourscheme]` — without it the open
silently fails.

**Rejected approaches — do not retry any of these:**

| Approach | Result | Reason |
|---|---|---|
| `extensionContext?.open(url)` | Returns `false` | iOS routes the open through the HOST app (e.g. Photos), which can't handle your custom scheme |
| Responder chain + `openURL:` selector | Force-blocked | Deprecated; iOS logs a migration warning and returns false |
| `open:options:completionHandler:` with `[:]` | Crash | Swift's empty-dictionary singleton doesn't respond to `universalLinksOnly` (private UIKit selector) |
| Same, with `NSDictionary()` | Crash | `__NSDictionary0`, same problem — UIKit casts options to a private `_UIOpenURLOptions` class |
| Same, with `nil` | **Works** | UIKit skips the options cast entirely |

## 3. Completion in the main app — belt and suspenders

- `.onOpenURL` receives `yourscheme://share` and calls a
  `processPendingShare()` that drains the App Group staging area.
- **Also call `processPendingShare()` on
  `willEnterForegroundNotification`.** If the responder-chain open is
  ever blocked (OS change, host-app quirk), the user manually
  switching to your app still completes the share — pending shares
  are never lost.
- Staging is idempotent: clear the staged payload only after the main
  app has consumed it.

## Build + submission notes

- The extension is an embedded bundle id
  (`app.example.ios.ShareExtension`). **Cloud/CI App Store exports
  need a provisioning profile for EVERY embedded bundle id**, not
  just the app — discover embedded ids from the archive and mint a
  profile per id (`cloud-appstore-submission`; the template's
  `tools/asc_profiles.py` does this automatically).
- Keychain access from the extension needs its own Keychain Sharing
  entitlement (`swift-security` references) — App Group storage does
  not grant Keychain access.

## The web-app counterpart (zero-cost)

A web app can't join the share sheet, but a **user-built iOS
Shortcut** can: Receive Input from Share Sheet → URL-encode → open
`https://yourapp.example?view=compose&shareText=<encoded>`. The web
app reads the query param, pre-fills compose, and auto-triggers link
preview when the text is a URL. Ship the recipe as a short setup doc
(numbered Shortcuts steps); it costs nothing and closes the parity gap
until/unless the PWA can register as a share target
(`share_target` in the manifest — Android/desktop only today).

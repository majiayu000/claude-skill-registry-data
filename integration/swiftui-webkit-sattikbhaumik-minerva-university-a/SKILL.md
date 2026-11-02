---
name: swiftui-webkit
description: "Embeds and controls web content in SwiftUI with WebKit for SwiftUI, including WebView, WebPage, navigation policies, JavaScript execution, observable page state, link interception, local HTML or data loading, and custom URL schemes. Use when building iOS 26+ article/detail views, help centers, in-app documentation, or other embedded web experiences backed by HTML, CSS, and JavaScript."
---

# SwiftUI WebKit

Embed and manage web content in SwiftUI using the native WebKit-for-SwiftUI APIs introduced for iOS 26, iPadOS 26, macOS 26, and visionOS 26. Use this skill when the app needs an integrated web surface, app-owned HTML content, JavaScript-backed page interaction, or custom navigation policy control.

## Contents

- [Choose the Right Web Container](#choose-the-right-web-container)
- [Displaying Web Content](#displaying-web-content)
- [Loading and Observing with WebPage](#loading-and-observing-with-webpage)
- [Navigation Policies](#navigation-policies)
- [JavaScript Integration](#javascript-integration)
- [Local Content and Custom URL Schemes](#local-content-and-custom-url-schemes)
- [WebView Customization](#webview-customization)
- [Common Mistakes](#common-mistakes)
- [Review Checklist](#review-checklist)
- [References](#references)

## Choose the Right Web Container

Use the narrowest tool that matches the job.

| Need | Default choice |
|---|---|
| Embedded app-owned web content in SwiftUI | `WebView` + `WebPage` |
| Simple external site presentation with Safari behavior | `SFSafariViewController` |
| OAuth or third-party sign-in | `ASWebAuthenticationSession` |
| Back-deploy below iOS 26 or use missing legacy-only WebKit features | `WKWebView` fallback |

Prefer `WebView` and `WebPage` for modern SwiftUI apps targeting iOS 26+. Apple’s WWDC25 guidance explicitly recommends migrating SwiftUI apps away from UIKit/AppKit WebKit wrappers when possible.

Do not use embedded web views for OAuth. That stays an `ASWebAuthenticationSession` flow.

## Displaying Web Content

Use the simple `WebView(url:)` form when the app only needs to render a URL and SwiftUI state drives navigation.

```swift
import SwiftUI
import WebKit

struct ArticleView: View {
    let url: URL

    var body: some View {
        WebView(url: url)
    }
}
```

Create a `WebPage` when the app needs to load requests directly, observe state, call JavaScript, or customize navigation behavior.

```swift
@Observable
@MainActor
final class ArticleModel {
    let page = WebPage()

    func load(_ url: URL) async throws {
        for try await _ in page.load(URLRequest(url: url)) {
        }
    }
}

struct ArticleDetailView: View {
    @State private var model = ArticleModel()
    let url: URL

    var body: some View {
        WebView(model.page)
            .task {
                try? await model.load(url)
            }
    }
}
```

See [references/loading-and-observation.md](references/loading-and-observation.md) for full examples.

## Loading and Observing with WebPage

`WebPage` is an `@MainActor` observable type. Use it when you need page state in SwiftUI.

Common loading entry points:
- `load(URLRequest)`
- `load(URL)`
- `load(html:baseURL:)`
- `load(_:mimeType:characterEncoding:baseURL:)`

Common observable properties:
- `title`
- `url`
- `isLoading`
- `estimatedProgress`
- `currentNavigationEvent`
- `backForwardList`

```swift
struct ReaderView: View {
    @State private var page = WebPage()

    var body: some View {
        WebView(page)
            .navigationTitle(page.title ?? "Loading")
            .overlay {
                if page.isLoading {
                    ProgressView(value: page.estimatedProgress)
                }
            }
            .task {
                do {
                    for try await _ in page.load(URLRequest(url: URL(string: "https://example.com")!)) {
                    }
                } catch {
                    // Handle load failure.
                }
            }
    }
}
```

When you need to react to every navigation, observe the navigation sequence rather than only checking a single property.

```swift
Task {
    for await event in page.navigations {
        // Handle finish, redirect, or failure events.
    }
}
```

See [references/loading-and-observation.md](references/loading-and-observation.md) for stronger patterns and the load-sequence examples.

## Navigation Policies

Use `WebPage.NavigationDeciding` to allow, cancel, or customize navigations based on the request or response.

Typical uses:
- keep app-owned domains inside the embedded web view
- cancel external domains and hand them off with `openURL`
- intercept special callback URLs
- tune `NavigationPreferences`

```swift
@MainActor
final class ArticleNavigationDecider: WebPage.NavigationDeciding {
    var urlToOpenExternally: URL?

    func decidePolicy(
        for action: WebPage.NavigationAction,
        preferences: inout WebPage.NavigationPreferences
    ) async -> WKNavigationActionPolicy {
        guard let url = action.request.url else { return .allow }

        if url.host == "example.com" {
            return .allow
        }

        urlToOpenExternally = url
        return .cancel
    }
}
```

Keep app-level deep-link routing in the navigation skill. This skill owns navigation that happens inside embedded web content.

See [references/navigation-and-javascript.md](references/navigation-and-javascript.md) for complete patterns.

## JavaScript Integration

Use `callJavaScript(_:arguments:in:contentWorld:)` to evaluate JavaScript functions against the page.

```swift
let script = """
const headings = [...document.querySelectorAll('h1, h2')];
return headings.map(node => ({
    id: node.id,
    text: node.textContent?.trim()
}));
"""

let result = try await page.callJavaScript(script)
let headings = result as? [[String: Any]] ?? []
```

You can pass values through the `arguments` dictionary and cast the returned `Any` into the Swift type you actually need.

```swift
let result = try await page.callJavaScript(
    "return document.getElementById(sectionID)?.getBoundingClientRect().top ?? null;",
    arguments: ["sectionID": selectedSectionID]
)
```

Important boundary: the native SwiftUI WebKit API clearly supports Swift-to-JavaScript calls, but it does not expose an obvious direct replacement for `WKScriptMessageHandler`. If you need coarse JS-to-native signaling, a custom navigation or callback-URL pattern can work, but document it as a workaround pattern, not a guaranteed one-to-one replacement.

See [references/navigation-and-javascript.md](references/navigation-and-javascript.md).

## Local Content and Custom URL Schemes

Use `WebPage.Configuration` and `URLSchemeHandler` when the app needs bundled HTML, offline documents, or app-provided resources under a custom scheme.

```swift
var configuration = WebPage.Configuration()
configuration.urlSchemeHandlers[URLScheme("docs")!] = DocsSchemeHandler(bundle: .main)

let page = WebPage(configuration: configuration)
for try await _ in page.load(URL(string: "docs://article/welcome")!) {
}

```

Use this for:
- bundled documentation or article content
- offline HTML/CSS/JS assets
- app-owned resource loading under a custom scheme

Do not overuse custom schemes for normal remote content. Prefer standard HTTPS for server-hosted pages.

See [references/local-content-and-custom-schemes.md](references/local-content-and-custom-schemes.md).

## WebView Customization

Use WebView modifiers to match the intended browsing experience.

Useful modifiers and related APIs:
- `webViewBackForwardNavigationGestures(_:)`
- `findNavigator(isPresented:)`
- `webViewScrollPosition(_:)`
- `webViewOnScrollGeometryChange(...)`

Apply them only when the user experience needs them.

- Enable back/forward gestures when people are likely to visit multiple pages.
- Add Find in Page when the content is document-like.
- Sync scroll position only when the app has a sidebar, table of contents, or other explicit navigation affordance.

Apple’s HIG also applies here: support back/forward navigation when appropriate, but do not turn an app web view into a general-purpose browser.

## Common Mistakes

- Using `WKWebView` wrappers by default in an iOS 26+ SwiftUI app instead of starting with `WebView` and `WebPage`
- Using embedded web views for OAuth instead of `ASWebAuthenticationSession`
- Reaching for `WebPage` only after building a plain `WebView(url:)` path that now needs state, JS, or navigation control
- Treating `callJavaScript` as a direct replacement for `WKScriptMessageHandler`
- Keeping all links inside the app when external domains should open outside the embedded surface
- Building a browser-style app shell around WebView instead of a focused embedded experience
- Using custom URL schemes for content that should just load over HTTPS
- Forgetting that `WebPage` is main-actor-isolated

## Review Checklist

- [ ] `WebView` and `WebPage` are the default path for iOS 26+ SwiftUI web content
- [ ] `ASWebAuthenticationSession` is used for auth flows instead of embedded web views
- [ ] `WebPage` is used whenever the app needs state observation, JS calls, or policy control
- [ ] Navigation policies only intercept the URLs the app actually owns or needs to reroute
- [ ] External domains open externally when appropriate
- [ ] JavaScript return values are cast defensively to concrete Swift types
- [ ] Custom URL schemes are used only for real app-owned resources
- [ ] Back/forward gestures or controls are enabled when multi-page browsing is expected
- [ ] The web experience adds focused native value instead of behaving like a thin browser shell
- [ ] Fallback to `WKWebView` is justified by deployment target or missing API needs

## References

- Loading and observation: [references/loading-and-observation.md](references/loading-and-observation.md)
- Navigation and JavaScript: [references/navigation-and-javascript.md](references/navigation-and-javascript.md)
- Local content and custom schemes: [references/local-content-and-custom-schemes.md](references/local-content-and-custom-schemes.md)
- Migration and fallbacks: [references/migration-and-fallbacks.md](references/migration-and-fallbacks.md)

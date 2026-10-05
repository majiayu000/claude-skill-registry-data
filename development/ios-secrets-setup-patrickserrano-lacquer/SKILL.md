---
name: ios-secrets-setup
description: Configure iOS service keys, Secrets.xcconfig, CI signing credentials, or release secret injection and provenance.
---

# iOS App-Runtime Secrets Setup

App-runtime keys (RevenueCat, Aptabase, …) live in a gitignored
`Secrets.xcconfig`, never in source or the committed `project.yml`. The
lacquer syncs a `Secrets.xcconfig.example` template into the component dir.

1. **Copy & ignore:** `cp Secrets.xcconfig.example Secrets.xcconfig`, fill in
   real values, and add `Secrets.xcconfig` to `.gitignore`. The example is
   committed; the real file never is. (The committed `project.yml` must also
   stay key-free.)
2. **Wire into the build (`project.yml`):** point the target's configs at the
   xcconfig and surface each key into `Info.plist`:
   ```yaml
   targets:
     <App>:
       configFiles:
         Debug: Secrets.xcconfig
         Release: Secrets.xcconfig
       info:
         path: App/Info.plist
         properties:
           REVENUECAT_API_KEY: $(REVENUECAT_API_KEY)
           APTABASE_APP_KEY: $(APTABASE_APP_KEY)
   ```
3. **Read at runtime** from the Info dictionary — fail loud if a required key
   is blank rather than shipping a broken SDK init:
   ```swift
   enum Secrets {
       static func required(_ key: String) -> String {
           guard let v = Bundle.main.object(forInfoDictionaryKey: key) as? String,
                 !v.isEmpty else {
               fatalError("Missing \(key) — copy Secrets.xcconfig.example to Secrets.xcconfig and fill it in")
           }
           return v
       }
       static var revenueCatAPIKey: String { required("REVENUECAT_API_KEY") }
       static var aptabaseAppKey: String { required("APTABASE_APP_KEY") }
   }
   ```

`Secrets.xcconfig` values are **build-time** — they are baked into the
binary, so treat them as obfuscated, not secret. A truly sensitive secret
belongs on a server, never in the app.

> **RevenueCat ships two different keys — do not confuse them.** The
> `REVENUECAT_API_KEY` above is the **public SDK key** (`appl_…`), safe to
> compile into the app. RevenueCat's **REST API** uses a separate **secret
> key** (`sk_…`) that grants full account access — it must **never** go in
> `Secrets.xcconfig` or the binary. That's a CI/server secret
> (`REVENUECAT_REST_API_KEY`), set via `gh secret set` per the
> CI/server secrets section in [references/project-rules.md](references/project-rules.md).

## Project conventions

Read [references/project-rules.md](references/project-rules.md) for the relevant
section when handling this task. Read only what applies; examples do not
authorize releases, deployments or changes outside the user's scope.
Always-loaded safety rules still apply.

- Secrets & Service Keys

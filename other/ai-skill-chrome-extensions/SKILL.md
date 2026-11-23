---
name: chrome-extensions
description: "Use when building, scaffolding or debugging Chrome, Chromium or Edge Manifest V3 extensions: service workers, content scripts, popups, options pages, side panels, omnibox, context menus, message passing, permissions and host_permissions, native messaging, unpacked loading, MV2-to-MV3 migration, manifest.json, chrome.* and browser.* APIs, or owner controlled live research observers that record bounded DOM and configured GraphQL development evidence from one approved webpage tab. Not for Firefox or Safari behavior, ordinary web page automation outside an extension, covert interception, or Chrome Web Store listing and review."
license: Apache-2.0
metadata:
  last-updated: "2026-11-18"
---

# Context Router

Choose the API, concept, manifest key or implementation reference. Check its execution context, permissions and Chrome version before using an example.

| Topic | Open when | Read |
| --- | --- | --- |
| Runtime, Events & Lifecycle Timers | Open when handling extension runtime messages, install or startup events, shared event listeners, alarms, idle state, or power requests. | [Runtime, Events & Lifecycle Timers](references/api-runtime-lifecycle.md) |
| Offscreen, Messaging Services & Shared Types | Open when using offscreen documents, cloud messaging, or shared extension types. | [Offscreen, Messaging Services & Shared Types](references/api-runtime-misc.md) |
| Scripting & User Scripts | Open when injecting scripts or CSS, registering dynamic content scripts, or running user scripts. | [Scripting & User Scripts](references/api-scripting-userscripts.md) |
| Tabs, Tab Groups & Windows | Open when querying, creating, updating, grouping, or messaging browser tabs and windows. | [Tabs, Tab Groups & Windows](references/api-tabs-windows.md) |
| Navigation, History, Sessions & Search | Open when tracking navigation, restoring sessions, managing browsing history or bookmarks, or searching browser content. | [Navigation, History, Sessions & Search](references/api-navigation-history.md) |
| Network Filtering & Request APIs | Open when filtering or redirecting requests, declaring network rules, or accessing proxies, cookies, and DNS. | [Network Filtering & Request APIs](references/api-network-filtering.md) |
| Storage & Browser Settings | Open when storing extension data or configuring browser content, privacy, fonts, and browsing-data settings. | [Storage & Browser Settings](references/api-storage-settings.md) |
| UI Surfaces | Open when building toolbar actions, context menus, side panels, omnibox interactions, notifications, or keyboard commands. | [UI Surfaces](references/api-ui-surfaces.md) |
| DevTools Extension APIs & Debugger | Open when extending DevTools panels and inspected pages or using the debugger protocol from an extension. | [DevTools Extension APIs & Debugger](references/api-devtools-debugger.md) |
| Identity & Authentication | Open when authenticating users with OAuth, certificates, platform keys, or WebAuthn proxy APIs. | [Identity & Authentication](references/api-identity-auth.md) |
| Media Capture & Speech | Open when capturing tabs, desktops, or pages, selecting audio devices, or using text-to-speech APIs. | [Media Capture & Speech](references/api-media-capture.md) |
| Downloads, Management & Permissions | Open when managing downloads, inspecting installed extensions, or requesting optional permissions at runtime. | [Downloads, Management & Permissions](references/api-downloads-management-permissions.md) |
| System & Hardware | Open when reading system information, printing, scanning documents, or configuring accessibility features. | [System & Hardware](references/api-system-hardware.md) |
| Enterprise & ChromeOS | Open when using enterprise or ChromeOS extension APIs for devices, filesystems, input methods, wallpaper, or VPNs. | [Enterprise & ChromeOS](references/api-enterprise-chromeos.md) |
| Internationalization (i18n) | Open when localizing extension messages with chrome.i18n, default_locale, and _locales. | [Internationalization (i18n)](references/api-i18n.md) |
| Extension Architecture & Getting Started | Open when choosing extension components and understanding how they communicate. | [Extension Architecture & Getting Started](references/concepts-architecture.md) |
| The MV3 Background Service Worker | Open when handling service-worker lifecycle limits, lost state, timers, or background work. | [The MV3 Background Service Worker](references/concepts-service-workers.md) |
| Content Scripts | Open when choosing content-script execution worlds, injection timing, or match patterns. | [Content Scripts](references/concepts-content-scripts.md) |
| Message Passing | Open when passing one-time messages, maintaining ports, or communicating with external extensions and native hosts. | [Message Passing](references/concepts-messaging.md) |
| Declaring Permissions & Match Patterns | Open when choosing required or optional permissions, host permissions, activeTab, or match patterns. | [Declaring Permissions & Match Patterns](references/concepts-permissions.md) |
| Storage, State & Cross-Origin Isolation | Open when choosing storage areas, persisting worker state, handling cookies, or configuring cross-origin isolation. | [Storage, State & Cross-Origin Isolation](references/concepts-storage-state.md) |
| Extension Lifecycle & Updates | Open when handling installation and updates, rolling out new versions, or setting an uninstall URL. | [Extension Lifecycle & Updates](references/concepts-lifecycle-updates.md) |
| Security & Privacy | Open when configuring content security policy, resource exposure, remote-code restrictions, or privacy behavior. | [Security & Privacy](references/concepts-security-privacy.md) |
| Live Research Observer | Open when an owner wants explicit exact tab observation with bounded DOM evidence and complete configured GraphQL development exchanges without page control. | [Live Research Observer](references/live-research-observer.md) |
| MV2 to MV3 Migration | Open when migrating Manifest V2 extension behavior to Manifest V3. | [MV2 to MV3 Migration](references/concepts-mv2-to-mv3-migration.md) |
| Manifest Format & Core Keys | Open when declaring the manifest version, name, version, icons, default locale, or other identity keys. | [Manifest Format & Core Keys](references/manifest-format-core-keys.md) |
| Manifest Capability Keys | Open when declaring actions, background workers, content scripts, permissions, CSP, side panels, or OAuth in the manifest. | [Manifest Capability Keys](references/manifest-capability-keys.md) |
| Manifest Specialized Keys | Open when declaring specialized file-handler, input, speech, isolation, shared-module, trial-token, or DevTools manifest keys. | [Manifest Specialized Keys](references/manifest-specialized-keys.md) |
| Permissions List | Open when checking the exact spelling and purpose of a named permission string. | [Permissions List](references/permissions-list.md) |
| UI & DevTools How-Tos | Open when implementing accessible extension UI, favicons, localized formats, notifications, or DevTools interfaces. | [UI & DevTools How-Tos](references/howto-ui-and-devtools.md) |
| Web Platform How-Tos | Open when using geolocation, screen capture, WebSockets, WebHID, WebUSB, or origin trials in extension contexts. | [Web Platform How-Tos](references/howto-web-platform.md) |
| Integrate & Distribute | Open when integrating OAuth or analytics, packaging or self-hosting an extension, or loading it unpacked. | [Integrate & Distribute](references/howto-integrate-distribute.md) |
| Test & Debug | Open when testing or debugging service workers, popups, or content scripts with browser tools and test frameworks. | [Test & Debug](references/howto-test-debug.md) |

Open the [reference index](references/INDEX.md) or [topic catalogs](references/topics.json) for broader lookup.

Open when implementing a web UI in an extension popup, panel, options page or content script. [Web surfaces](references/web-surfaces.md).

# Language Translations

[Reference Language Selection](references/languages.md)

# Context For Open Source

Skill reference documentation is interpreted content for use in open source projects. Check against [official documentation sources](https://developer.chrome.com/docs/extensions) when dealing with defects or issues that may come up from interpreting this skill's references.

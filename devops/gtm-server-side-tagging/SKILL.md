---
name: gtm-server-side-tagging
description: Stand up and operate a Google Tag Manager server-side (tagging server) container on Cloud Run, wire its clients, and route web and app traffic to it over a first-party domain. Use when the user asks about server-side GTM, sGTM, a tagging server, Cloud Run tagging, transport_url, a first-party collection domain, the GA4 client, the Measurement Protocol client, service worker transport, preview and debug for the server container, or moving conversion tags server-side.
---

# GTM server-side tagging

Run a second GTM container on a server you control instead of in the browser, so measurement requests hit your own first-party endpoint, tags fire server to server, and you decide what data leaves the server. The tagging server is a Cloud Run service in your own Google Cloud project that receives requests, hands each to a client that turns it into events, and fires server-side tags against those events.

This skill covers the infrastructure and transport: provisioning the server, its clients, the web-to-server hop, and preview/debug. It assumes you know what a tag, trigger, and variable are and how the browser container publishes events. For the browser side, see the `gtm-web-container-and-datalayer` and `gtm-tags-triggers-variables` skills. For consent signals, see `gtm-consent-mode-v2`.

## When to use this skill

- "Set up server-side GTM / sGTM / a tagging server."
- "Deploy the tagging server on Cloud Run" or "which Cloud Run settings for sGTM?"
- "Point my Google tag / GA4 at the server container" or "what is transport_url / server_container_url?"
- "Set up a first-party collection domain / custom domain for tagging."
- "Which clients do I need?" / "GA4 client vs Measurement Protocol client."
- "Service worker transport" or "the sGTM service worker."
- "Preview and debug the server container" / "why is no client claiming the request?"
- "Move Google Ads / Floodlight / GA4 conversion tags server-side."

Boundaries with sibling skills:
- Browser container, dataLayer contract, and web tags/triggers/variables: `gtm-web-container-and-datalayer` and `gtm-tags-triggers-variables`.
- Consent Mode v2 signals and default/update ordering: `gtm-consent-mode-v2`. This skill only forwards the signals the browser sets.
- GA4 property, data streams, and enhanced measurement: `ga4-property-and-data-stream-setup`.
- Event model and marking key events: `ga4-events-and-key-events`.
- CM360 Floodlight configuration and the Conversions API: `cm360-floodlight-and-conversions`.
- Tag and pixel inventory across the estate: `tag-and-pixel-governance`.

## Quick reference

| Decision | Choose | Why |
| --- | --- | --- |
| Hosting for a real workload | Cloud Run, multiple instances | Recommended runtime, autoscales, no server to patch |
| Hosting for a quick test only | App Engine or a single instance | Cheaper to stand up, not for production traffic |
| Just want first-party Google-tag serving, no full server | Google tag gateway | Serves the Google tag from your domain via CDN/load balancer, no container to run |
| Web analytics into GA4 | GA4 client (pre-installed) | Claims `/g/collect` requests and builds GA4 events |
| Server-to-server or app/Measurement Protocol hits | Measurement Protocol client | Accepts MP payloads on your domain |
| Send browser data to the server | Point the Google tag `server_container_url` at your first-party domain | Requests go to your endpoint, not straight to Google |
| Test before publishing | Preview mode on the server container | Shows incoming request, claiming client, tags, and outgoing requests |

Mental model: browser publishes a request -> your first-party domain -> tagging server (Cloud Run) -> a client claims and parses it into events -> server-side tags fire on those events -> the server returns a response and forwards to vendor endpoints. The client is the adapter; the tag is the sender.

## Core process

1. Create the Cloud Run tagging server in your own Google Cloud project, because the server runs on infrastructure you control, not Google's. Use the automated provisioning flow, then set the number of instances for the load (see Decision rules). Preview and production run as separate deployments so test traffic never mixes with live data.
2. Map a first-party domain to the server, so measurement requests are same-site and served from your own hostname. Use a subdomain of the site (for example `sgtm.example.com`), point DNS at the Cloud Run service, and confirm TLS resolves before sending any real traffic.
3. Confirm the clients you need are present. The GA4 client and Measurement Protocol client are pre-installed. The GA4 client claims `gtag`/`/g/collect` requests; add or configure a client for any other source (app, server-to-server, third-party pixel) so something owns each incoming request format.
4. Point the browser at the server. In the Google tag (or GA4 configuration) set `server_container_url` to your first-party domain so the browser sends to your endpoint. Pick a transport that fits your CSP and iframe policy (image pixel, Fetch, XHR, or the service worker running in an iframe loaded from the server container domain). See `references/transport-url-and-first-party-domain.md`.
5. Update Content Security Policy and framing. Add `img-src`, `connect-src`, and for the service worker `frame-src` entries for the server container URL, and allow the server container origin in `X-Frame-Options` policy, because a missing directive silently drops the hit.
6. Preview and verify. Open Preview on the server container and confirm each incoming request is claimed by the expected client, the event data is correct, the intended tags fire, and outgoing requests return 2xx. Do not publish until the claiming client and outgoing status are both clean.
7. Move server-side tags in behind the verified transport. Add the GA4 tag, then Google Ads (Conversion Linker plus Conversion Tracking) and Floodlight tags on the server. Human-gate the publish: server-side tags send real conversions, so review in Preview and get sign-off before publishing the container version.

## Decision rules and thresholds

### Hosting and scaling

- Use Cloud Run for anything carrying real traffic. It is the recommended runtime, autoscales, and removes server maintenance. App Engine is offered as an alternative and a single-instance setup is fine only for a throwaway test.
- Run more than one instance in production. A single instance is a cold-start and single-point-of-failure risk under real load; provision enough minimum instances to absorb your peak request rate without cold starts. Size to your measured requests per second, then leave headroom.
- If all you need is first-party serving of the Google tag itself (not a full event-processing server), the Google tag gateway serves the tag from your own domain through a CDN, load balancer, or web server, with no container to operate. Gateway and a full tagging server are complementary, not either/or: gateway hardens Google-tag delivery, the server processes and forwards events.

### Clients

- One client must claim each incoming request or it is dropped. If Preview shows a request with no claiming client, you are missing or misconfiguring a client for that request format.
- GA4 client: pre-installed, claims `gtag.js` and `/g/collect` requests for its measurement IDs, and turns them into GA4 events other tags read. This is the backbone client for web.
- Measurement Protocol client: pre-installed, accepts GA4 Measurement Protocol payloads, for server-to-server sources and app/offline events sent to your domain instead of `www.google-analytics.com`.
- Order matters when two clients could claim the same request. Set client priority so the more specific client wins.

### Transport

- Default to image pixel or Fetch for the browser-to-server hop unless you have a reason to change. XHR and the service worker (running in an iframe loaded from the server container domain) are the other supported transports.
- The service worker transport needs `frame-src` for the server container URL and a framing policy that allows that origin. If the worker cannot load, the hit fails; verify in Preview before relying on it.
- Missing CSP entries are the most common silent failure. If a request never reaches the server, check `img-src`/`connect-src`/`frame-src` before touching the container.

### First-party domain

- Use a same-site subdomain of the main site so cookies set by the server are first-party and requests are same-site. A domain on a different registrable site is treated as third-party and loses the durability benefit.
- Never publish with the raw Cloud Run URL as the collection endpoint for production. Map the custom first-party domain first, because the point of the server is first-party serving.

### Safe-by-default

- Read and preview before you publish. Publishing a server container version changes what fires on live traffic and what data is forwarded to vendors, so treat every publish as a spend/live-config change and require human sign-off.
- The server can pass hashed user-provided data for enhanced conversions (event parameter `user_data`) and encrypts revenue values it returns to the browser. Do not forward raw personal data or unhashed identifiers; confirm hashing and that consent (see `gtm-consent-mode-v2`) gates the tag before it sends.

## Reference material

- `references/server-container-and-clients.md`: the server object model (container, clients, transport, tags), the pre-installed clients and what each claims, client priority and activation, and the Cloud Run provisioning and scaling choices with concrete instance sizing. Read this when standing up the server or debugging which client owns a request.
- `references/transport-url-and-first-party-domain.md`: the exact browser-side fields (`server_container_url`, `transport_url`), each transport method (image, Fetch, XHR, service worker), the CSP and `X-Frame-Options` entries to add, custom-domain mapping, and the gateway alternative. Read this when wiring the web-to-server hop or the first-party domain.
- `references/2025-serving-and-serviceworker-changes.md`: the current serving model, the service worker transport and its framing requirements, the Google tag gateway first-party serving option, and how server-side tagging pairs with consent and enhanced conversions in 2025 to 2026. Read this when a transport is failing or when deciding gateway vs full server.

## Templates and examples

- Ecommerce site, real traffic: Cloud Run server with a minimum-instances floor sized to peak RPS, first-party domain `sgtm.shopname.com`, GA4 client claiming `/g/collect`, Google tag `server_container_url` set to `https://sgtm.shopname.com`, Fetch transport, CSP `connect-src https://sgtm.shopname.com`. Server-side GA4, Google Ads Conversion Linker plus Conversion Tracking, and Floodlight tags, published only after a clean Preview.
- App plus web: same server, GA4 client for the web `/g/collect` traffic and the Measurement Protocol client for app and server-to-server hits posting to `https://sgtm.shopname.com/mp/collect`. One server, two claiming clients.
- Quick proof of concept: single App Engine or one-instance Cloud Run deployment, raw provisioning URL for the test only, Preview to confirm the GA4 client claims the request. Not for production; map a first-party domain and scale out before going live.
- First-party Google-tag serving only, no event server: Google tag gateway serving the Google tag from `example.com` via the site's CDN or load balancer. Use when the goal is durable Google-tag delivery, not server-side event processing.

## Common pitfalls

- No client claims the request. Preview shows an incoming request with no owning client, so nothing parses it into events. Add or fix the client for that request format (GA4 client for `/g/collect`, Measurement Protocol client for MP payloads) and set priority if two could claim it.
- Collecting on the raw Cloud Run URL in production. It works but is not first-party, so cookies are third-party and you lose the durability the server exists for. Map a same-site custom domain and repoint `server_container_url`.
- CSP or framing blocks the transport. A missing `img-src`/`connect-src`/`frame-src` entry (or a framing policy that excludes the server origin) drops the hit before it reaches the server, and it looks like the server is down. Fix the policy first.
- Single instance under load. One Cloud Run instance cold-starts and drops hits at peak. Set a minimum-instances floor sized to your traffic.
- Publishing without Preview. Server-side tags forward real conversions and value to vendors. Publishing an unverified version can double-count, mis-map, or leak data. Preview the claiming client and outgoing 2xx, then get sign-off.
- Forwarding raw personal data. The server can send hashed `user_data` for enhanced conversions and encrypts revenue back to the browser. Forwarding unhashed identifiers or ignoring consent breaks privacy commitments; gate the tag on consent (`gtm-consent-mode-v2`) and confirm hashing.
- Preview and live traffic mixed. Preview and production are separate deployments for a reason. If test events land in live GA4, you published the debug configuration or wired preview traffic to the production endpoint. Keep them separate.

## Sources

- [Server-side tagging intro](https://developers.google.com/tag-platform/tag-manager/server-side/intro) (as of July 2026)
- [Send data to a server container](https://developers.google.com/tag-platform/tag-manager/server-side/send-data) (as of July 2026)
- [Set up Google Ads conversion tracking server-side](https://developers.google.com/tag-platform/tag-manager/server-side/ads-setup) (as of July 2026)
- [Debug a server container](https://developers.google.com/tag-platform/tag-manager/server-side/debug) (as of July 2026)
- [Google tag gateway for advertisers](https://developers.google.com/tag-platform/tag-manager/gateway) (as of July 2026)
- [Consent for server-side tagging](https://developers.google.com/tag-platform/security/guides/consent) (as of July 2026)
- [Tag Manager API v2](https://developers.google.com/tag-platform/tag-manager/api/v2) (as of July 2026)

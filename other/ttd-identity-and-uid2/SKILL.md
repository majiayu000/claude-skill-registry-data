---
name: ttd-identity-and-uid2
description: Understand and apply Unified ID 2.0 (UID2) and the broader identity stack The Trade Desk supports as a durability and addressability play across web, app, and CTV, where signals erode unevenly and Chrome kept third-party cookies. Use when the user asks about "UID2", "Unified ID 2.0", "TTD identity", "cookieless identity", "durable identity", "how does UID2 work", "raw UID2 vs UID2 token", "UID2 operator", "EUID", "European Unified ID", "EUID coverage", "OpenPass", "authenticated identity", "UID2 scale in CTV or audio", or how UID2 relates to bidstream targeting and measurement.
---

# TTD identity and UID2

Explain how UID2 turns a consented email or phone number into a privacy-conscious advertising identifier, why a durable authenticated ID matters even in a world where signals are eroding unevenly rather than disappearing on a clock, and how the related pieces (EUID and OpenPass) fit. Treat UID2 as a durability and addressability play, not a cookie-replacement countdown. Chrome chose to keep third-party cookies rather than deprecate them, so the case for UID2 is not "cookies are about to vanish" but "authenticated identity is more durable, works where cookies and mobile ad IDs never did, and travels across web, app, and CTV." UID2 is an open framework, so this skill teaches the model and the decision rules, not a proprietary spec. For the current ground truth on Privacy Sandbox, browser signal loss, and what is actually eroding, see the `privacy-sandbox-and-signal-loss-2026` skill. For definitions of bidstream, RTB, CPM, and deal mechanics, see the `programmatic-foundations` skill. For how identity-driven reach and outcomes get framed in a report, see the `reporting-by-campaign-goal` skill.

## When to use this skill

Use this when the task is about WHO a user is in a privacy-safe way and how that identity flows through programmatic, including:

- Explaining what UID2 is, how a raw identifier becomes a UID2 token, and why the design is privacy-conscious.
- Reasoning about uneven signal erosion: third-party cookies stay in Chrome but are already gone in Safari and Firefox, mobile ad IDs (IDFA, AAID) are throttled by ATT and opt-out, and consent denial removes more. What authenticated identity restores is durability across those gaps and reach where cookies and mobile ad IDs never worked, such as CTV.
- Distinguishing the raw UID2 from the encrypted UID2 token (the advertising token), and explaining token rotation and refresh.
- Understanding the operator and participant model: who generates tokens, who decrypts them, and where The Trade Desk sits as a public operator.
- Choosing the right integration path for a publisher, an advertiser or data provider, or a DSP buyer.
- Knowing when to reach for EUID instead of UID2 (European and UK traffic), and how OpenPass and other sign-in options feed authenticated email into the framework.

Boundaries with sibling skills:
- Building and applying audiences on top of UID2-matched data lives in `ttd-targeting-and-audiences`. This skill stops at the identifier; that skill spends it.
- Where impressions come from (open market, PMP, Programmatic Guaranteed, OpenPath) lives in `ttd-inventory-and-deals`.
- Measuring authenticated reach and identity-resolved outcomes lives in `ttd-measurement-and-reporting`, with goal framing in `reporting-by-campaign-goal`.
- Programmatic API and automation patterns live in `ttd-api-and-automation`.

## Quick reference

The identity stack at a glance. UID2 and EUID are the deterministic IDs; OpenPass is one way to collect the authenticated email that seeds them.

| Piece | What it is | When it applies |
| --- | --- | --- |
| Raw UID2 | The deterministic identifier derived from a normalized, hashed, salted email or phone. Same input yields the same raw UID2 across participants, which is what makes matching work. | Internal mapping, audience match, and measurement joins. Not sent in the bidstream raw. |
| UID2 token (advertising token) | The encrypted, short-lived form of a raw UID2. This is what travels in the bidstream. | Passed by publishers, decrypted by buyers to target and measure. |
| Operator | The service that converts DII to a raw UID2 and encrypts it into a token, and that refreshes decryption keys. The Trade Desk currently runs a public operator. | Every token generation, refresh, and decryption. |
| EUID (European Unified ID) | A separate framework built on UID2, scoped to European and UK consent regimes (GDPR, TCF). Its own namespace, interoperable design. | European and UK traffic. |
| OpenPass | An independent single sign-on option (alongside Sign in with Google, Apple, and Facebook Login) that returns an authenticated email a publisher can use to generate a UID2 or EUID. | Growing a publisher's authenticated, addressable audience. |

How a token flows in one line: a user authenticates, the publisher normalizes and SHA-256 hashes the email or phone, the operator salts and encrypts it into a UID2 token, the token rides the bidstream, and the buyer's DSP decrypts it to decide the bid. DII here means directly identifying information, the email or phone the user provided.

## Core process

### Understand the identifier model

1. **Start from consented first-party data.** UID2 is seeded by an email or phone number the user knowingly provided, paired with notice and the ability to opt out. No consent, no token. That authenticated seed is also the source of its durability: unlike a third-party cookie, it is not tied to one browser and it persists across web, app, and CTV. The trade-off is that scale is bounded by how many users authenticate, which is the central adoption gap (see the decision rules).
2. **Normalize, then hash.** The publisher normalizes the email or phone and hashes it with SHA-256, then Base64-encodes the hash before sending it to the operator. Normalizing first is what guarantees two participants who hold the same email derive the same value.
3. **Let the operator create the raw UID2.** The operator takes the hashed DII, adds a secret salt, and runs the documented steps to produce the raw UID2. Because the salt and sequence are shared, the raw UID2 for a given person matches across all participants, which is what makes cross-party audience matching and measurement possible.
4. **Encrypt into a UID2 token for the bidstream.** The operator encrypts the raw UID2 into a UID2 token (also called the advertising token). The raw UID2 is the stable join key; the token is the rotating, encrypted thing that is safe to broadcast.

### The operator and participant model

1. **Know what the operator does.** It manages encryption keys and salts, hashes DII, encrypts raw UID2s into tokens, decrypts tokens, and tracks opt-out. It is the trust boundary of the framework.
2. **Pick public or private operator.** A public operator is a shared instance available to all participants and free to use with a contract and credentials. The Trade Desk currently runs a public operator. A private operator is an instance an organization hosts itself to keep DII inside its own infrastructure, at the cost of ongoing engineering and timely updates. Default to the public operator unless data-residency or control requirements force a private one.
3. **Map yourself to a participant role.** Publishers and their SSPs collect DII and propagate tokens into the bidstream. Advertisers, identity-graph providers, and third-party data providers map first-party data to raw UID2s so it can be activated. DSP buyers receive tokens in the bidstream and decrypt them to target and measure. Your role determines which endpoints and credentials you need.

### Token rotation and refresh

1. **Treat the token as short-lived.** UID2 tokens have a limited life by design. Rotating, encrypted tokens mean a single intercepted token is low value and stale quickly, which is a core privacy property.
2. **Refresh on a frequent cadence.** Use the refresh token to obtain a new UID2 token and a new refresh token. The documentation recommends refreshing roughly hourly so tokens stay current and so an opt-out is honored promptly, because the operator checks opt-out status before issuing a new token.
3. **Do not assume refresh invalidates the prior token.** Refreshing issues a new token but does not expire the previous one. Build your logic around the refresh cadence and opt-out check, not around assumed instant revocation.

### Choose and stand up an integration path

1. **Publisher path.** Capture an authenticated email (directly or via an SSO option such as OpenPass, Sign in with Google, Apple, or Facebook Login), generate the token through the operator, and pass it into the bidstream. This grows addressable, monetizable inventory.
2. **Advertiser and data-provider path.** Map first-party CRM or data-graph records to raw UID2s through the identity map endpoint so audiences can be matched and outcomes measured without sharing raw emails.
3. **DSP buyer path.** Decrypt tokens received in the bidstream to apply audiences and bid. On The Trade Desk this is the platform side that consumes the identifier; building and applying those audiences is covered in `ttd-targeting-and-audiences`.

Platform access note: obtaining UID2 credentials and API keys, calling the token endpoints (POST /token/generate, POST /token/refresh, POST /identity/map), and hosting a private operator all require a UID2 contract and provisioned credentials. The framework is openly documented, but participating requires onboarding and access you cannot self-serve from public pages. Flag these as partner-gated when scoping work.

### EUID for European and UK traffic

1. **Switch frameworks by geography and consent regime, not by preference.** EUID is built on UID2 but is a separate framework with its own namespace, designed for GDPR, the Transparency and Consent Framework, and local guidance. Its privacy controls are meant to help participants meet market requirements in many European countries and some other regions such as the UK. Use EUID for European and UK users and UID2 for regions like the United States, and confirm the specific European market is in scope rather than assuming uniform coverage across the continent.
2. **Expect interoperable design, separate plumbing.** Both are open source and interoperable in concept, but they are distinct namespaces with distinct credentials and consent handling. Do not assume a UID2 integration automatically covers European obligations.

### OpenPass and authenticated traffic

1. **Use OpenPass to grow the authenticated pool.** OpenPass is one of the documented single sign-on options a publisher can use to obtain an authenticated email, which is then turned into a UID2 or EUID. More authenticated users means more addressable, higher-value inventory.
2. **Treat sign-in choice as plumbing.** From the framework's view, OpenPass, Sign in with Google, Sign in with Apple, and Facebook Login are interchangeable ways to reach the same step: extract the email from the identity token, then generate the ID.

## Decision rules and thresholds

- **No consent, no identifier.** UID2 only exists for users who provided an email or phone with notice and opt-out. If a property has little authenticated traffic, the addressable gain is small until it grows logins. Prioritize authentication before expecting UID2 scale.
- **Watch scale in audio and CTV.** Adoption is still growing and is not yet as deep as legacy identifiers, so authenticated inventory can run thin in channels where users do not sign in. Audio historically ran without cookies on subscription data, and many CTV surfaces (free ad-supported channels especially) have no direct email login, which caps addressable reach and invites low-quality UID2s from third-party data. Check that a UID2 or EUID audio or CTV buy has enough authenticated volume to deliver before committing budget to it.
- **Raw UID2 for joins, token for the bidstream.** Never treat the encrypted token as a stable key, and never broadcast a raw UID2. Match and measure on the raw UID2 internally; transmit only the rotating token.
- **Refresh frequently and check opt-out.** Aim for an hourly refresh cadence. A stale token risks serving to a user who has since opted out, which is both a compliance and a trust problem.
- **Public operator by default.** Choose a private operator only when data residency or first-party-data control requires keeping DII in-house, and budget for the ongoing engineering it demands.
- **Geography picks the framework.** European and UK traffic uses EUID; other regions use UID2. Mixing them up creates consent and namespace mismatches. EUID is built for market requirements in many European countries and some other regions such as the UK, so confirm the specific market is covered before promising EUID addressability there rather than assuming blanket European reach.
- **Identity is a means, not the goal.** UID2 improves addressability and measurement, but the campaign is still judged on its objective. Frame results through the `reporting-by-campaign-goal` skill, not on identifier coverage alone.

## Reference material

- See the `programmatic-foundations` skill for bidstream, RTB, first vs second price auctions, CPM, and deal-ID basics. This skill does not redefine them.
- See the `reporting-by-campaign-goal` skill for how to present authenticated reach and identity-resolved outcomes against the campaign objective rather than as raw coverage stats.
- The UID2 documentation in the Sources covers the token-creation steps, the operator service, the participant roles, and the SDK and API references. Read the operator and tokens pages before designing an integration; read the participants overview to confirm which endpoints your role uses.

## Templates and examples

Publisher growing addressable CTV and web inventory:
- Collect authenticated email through an existing login or an SSO option such as OpenPass.
- Generate UID2 tokens through The Trade Desk public operator, refresh roughly hourly, and pass tokens into the bidstream.
- Expected payoff: more impressions carry a durable, consented identifier, so they attract addressable demand instead of clearing as anonymous.

Advertiser activating first-party CRM without cookies:
- Map hashed CRM emails to raw UID2s through the identity map endpoint.
- Hand the matched segment to the buying side to build an audience; see `ttd-targeting-and-audiences`.
- Expected payoff: the same customer can be reached and measured across web, app, and CTV without third-party cookies or a mobile ad ID.

European campaign:
- Use EUID rather than UID2, with GDPR and TCF consent captured, and confirm credentials are provisioned for the EUID namespace.
- Expected payoff: addressable targeting that aligns with European consent obligations.

## Common pitfalls

- **Confusing the raw UID2 with the token.** The raw UID2 is the stable join key and must not be broadcast; the token is the rotating, encrypted value for the bidstream. Treating the token as a permanent key breaks matching and leaks nothing useful.
- **Skipping the refresh cadence.** A token that is never refreshed goes stale, can miss an opt-out, and loses its value. Refresh roughly hourly.
- **Assuming UID2 covers Europe.** European and UK traffic needs EUID, a separate framework and namespace. A UID2-only setup does not satisfy those obligations.
- **Expecting scale without authentication.** UID2 only exists for consented, authenticated users, and adoption is still catching up to legacy identifiers. If logins are thin, addressability stays thin until the property grows them. This bites hardest in audio and CTV, where many surfaces have no email login, so verify authenticated volume before promising delivery there.
- **Forgetting the access boundary.** The framework is open and documented, but credentials, token endpoints, and a private operator require a contract and onboarding. Scope those as partner-gated rather than assuming public access.
- **Reporting on identifier coverage instead of outcomes.** UID2 coverage is an input, not a result. Judge the campaign on its goal using `reporting-by-campaign-goal`.

## Sources

Official Unified ID 2.0, European Unified ID, IAB Tech Lab, and Google Privacy Sandbox documentation. Lines touched for the durability and market-coverage reframe are verified as of July 2026; the remaining UID2 reference lines were verified as of June 2026.

- Google decision to keep third-party cookies in Chrome (no standalone cookie prompt; the deprecation countdown that motivated much cookieless framing did not happen), verified as of July 2026: https://privacysandbox.google.com/blog/privacy-sandbox-next-steps
- UID2 overview (open-source, deterministic identity across web, app, and CTV; consumer control and opt-out): https://unifiedid.com/docs/intro
- How the UID2 token is created (normalize, SHA-256 hash, Base64, operator salt and encryption, cross-participant matching): https://unifiedid.com/docs/ref-info/ref-how-uid-is-created
- The UID2 operator (public vs private operators, The Trade Desk as a public operator, what the operator manages): https://unifiedid.com/docs/ref-info/ref-operators-public-private
- UID2 tokens and refresh tokens (short-lived rotating tokens, refresh mechanism, opt-out check, recommended refresh cadence): https://unifiedid.com/docs/ref-info/ref-tokens
- UID2 participants overview (publisher, advertiser and data provider, and DSP roles): https://unifiedid.com/docs/overviews/participants-overview
- UID2 documentation repository on GitHub (open source, IAB Tech Lab, Apache-2.0): https://github.com/IABTechLab/uid2docs
- EUID overview (built on UID2, separate namespace, scoped to GDPR and TCF; privacy controls designed to help participants meet market requirements in many European countries and some other regions such as the UK), verified as of July 2026: https://euid.eu/docs/intro
- EUID integration with SSO providers (Sign in with Google, Apple, Facebook Login, and OpenPass to obtain an authenticated email): https://euid.eu/docs/ref-info/ref-integration-sso-providers

Reframe lines as of July 2026; untouched UID2 reference lines as of June 2026.

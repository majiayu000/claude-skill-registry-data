---
name: browser-runtime
description: "Use when writing or reviewing code that runs in the visitor's browser and touches things the browser owns: web storage, parsing of external JSON, typing-triggered requests, console output, cross-window messages, global error handling, and the third-party requests, cookies and storage a page creates before consent."
---

# browser-runtime

Step 6 of the pipeline (`WORKFLOW.md`). The language rules live in `skills/typescript-patterns`, the
framework rules in the stack blocks, security in `skills/security-hardening` and consent law in
`business/data-protection`. This block holds what is specific to the browser as an environment: it can
refuse storage, it runs on the visitor's machine, it talks to other origins, and everything it does is
observable by the person who owns it. The rules follow the web platform specifications and are written
for any framework.

## When
Client-side code is written or reviewed that reads or writes web storage, parses JSON from outside the
code, fires requests on input, logs, receives messages, or loads anything from another origin; and when a
page's cookies and third-party requests are audited before a launch.

## Steps

### A. Code that runs in the browser

1. **Storage can fail, and its contents are not ours.** Every read or write of `localStorage`,
   `sessionStorage` or IndexedDB sits in a `try`/`catch`: the quota can be full, the engine can refuse
   access (a blocked-storage setting, a sandboxed frame), and accessing the property itself can throw.
   The page renders correctly without it. A stored value is untrusted input from the visitor's machine
   (point 2), carries a version so an old shape is discarded, and never holds a credential or a secret
   (`skills/security-hardening`, `skills/auth-session-conventions`).
2. **`JSON.parse` is followed by a shape check.** Whatever it parses (storage, a query parameter, a
   message, a response) is parsed inside a `try`, then validated against the shape the code expects
   (`skills/security-hardening` §2.11); a value that parses is not a value that is the right type.
3. **Input-triggered work is debounced, cancelled and ordered.** A request fired per keystroke waits for a
   pause in typing; the previous request is aborted with an `AbortSignal`; a response that arrives after
   a newer one was sent is discarded. Scroll, resize and pointer-move handlers are passive and
   rate-limited to the frame (`skills/webperf` §2.8), and every listener, timer and observer is released
   when its owner goes away.
4. **No `console` output in production.** Debug logging is removed by the build or routed through one
   logger that is silent in production; logs and error reports never carry personal data, tokens or full
   request bodies (`business/data-protection`).
5. **A cross-window message is checked at both ends.** The sender names the target origin and never
   uses the wildcard for anything sensitive; the receiver compares `event.origin` with an allowlist
   before reading `event.data`, then validates the payload (point 2).
6. **Uncaught errors are caught once, centrally.** A handler for `error` and `unhandledrejection` reports
   to the project's error monitoring with the release identifier (`skills/frontend-testing`,
   `skills/observability-instrumentation`) and puts the visitor in a recoverable state; it does not
   swallow the error (`skills/code-baseline`).
7. **Detect features, never browsers.** A capability is tested by asking the platform for it, with a
   fallback or a clear degraded state; user-agent parsing is a guess that ages. Which features need a
   polyfill is decided from the audience and the current compatibility table, not from a list kept here
   (`skills/source-freshness`).
8. **A new TypeScript project starts strict.** `strict` is on from the first commit, together with the
   option that makes indexed access include `undefined`; an existing project follows its own
   configuration (`skills/typescript-patterns`).

### B. What the page does to the visitor before they decide

9. **Inventory it from a clean profile.** Load each key page in a fresh headless browser profile with no
   consent given and record the cookies set, the keys written to web storage and the requests sent to
   origins other than ours. What is not strictly necessary for the page to work is a finding against the
   consent gate (`business/data-protection`, consent and cookies). The inventory is a script the project
   keeps and re-runs before each launch; the page text is not the source of truth, the network is.
10. **Classify what is found.** For each cookie or storage entry: first-party or third-party, purpose,
    lifetime, and whether it is exempt from consent (read the regulator's guidance, not a remembered list).
    Browsers have been restricting third-party cookies and partitioning third-party storage in
    different ways at different times; the current behaviour is read from each engine's documentation, and
    a feature must not depend on a third-party cookie working. A flow that needs a cross-site login or
    payment uses a redirect or the browser's storage-access mechanism, chosen from current documentation.
11. **Consent is enforced by code, not by a banner.** A non-essential tag is added to the page by the
    consent gate after the choice, not written into the template and hidden; revoking the choice stops the
    tag. The check in point 9 is what proves it.
12. **Name our own functional things by function.** Browsers' content blockers and privacy extensions
    match class names, ids and URL paths such as `ad`, `banner`, `sponsor`, `track`, `pixel`,
    `analytics`. A functional element or endpoint that happens to carry one of those names disappears for
    a share of visitors, with no error. Name by what a thing does and test the key journeys once with a
    blocker active. This rule is about our own collisions; renaming a real tracker to slip past a
    blocker or a consent choice is evasion, not hygiene, and is refused.
13. **Nothing personal travels in a URL.** Identifiers, e-mail addresses and tokens stay out of query
    strings and paths, because URLs are logged, cached, shared and sent to other origins in the
    `Referer` header (`skills/security-hardening` for the header policy).

## Output / checkpoint
No pipeline checkpoint: the findings go to the author. A launch audit records the inventory of point 9 (the
list of cookies, storage keys and third-party origins before consent) and its comparison with the register
of processing.

## Guardrails
- **Never trust the browser's contents**: storage, URL, messages and fields are inputs.
- **Never evade a visitor's choice**, by disguise or by timing.
- **Never write a rule that depends on one engine's current behaviour** without stamping the date and the
  source (`skills/source-freshness`).
- A grep is a place to look: an empty result proves nothing (`skills/security-hardening` §5.9).

## Mechanical checks

```
grep -rnE '(local|session)Storage' src
grep -rnE 'JSON\.parse' src
grep -rnE 'console\.(log|debug|table|dir|info)' src
grep -rnE "addEventListener\(['\"]message['\"]" src
grep -rnE "postMessage\([^)]*['\"]\*['\"]" src
grep -rnE '@input|onChange|oninput|watch\(' src
grep -nE '"strict"|noUncheckedIndexedAccess' tsconfig*.json
grep -rniE 'class="[^"]*\b(ad|ads|advert|banner|sponsor|track)[a-z-]*' src
grep -rniE '/(analytics|track|pixel|beacon|collect)\b' src
```

- Each storage and `JSON.parse` hit is read for the enclosing `try` and, for `parse`, the shape check
  within a few lines.
- Each message listener is read for an `event.origin` comparison before `event.data` is used.
- Input handlers on search or filter fields are read for debounce and an abort signal.
- The inventory of point 9 is run with a headless browser in a clean profile: print `document.cookie`, list
  the web-storage keys and list every request whose origin differs from the site's; the expected result
  outside the strictly necessary category is empty.
- The two name greps list candidates for point 12; confirm by loading the page with a blocker on.

## Origin
Assembled on 2026-10-02 from the topics of the public `Front-End-Checklist` repository (README and
package metadata declare MIT; no licence file is present, so only the topics were taken and no sentence).
The facts were written from primary documents: the HTML Living Standard (web storage, cross-document
messaging, `AbortSignal`), the ECMAScript and WHATWG DOM specifications, the browser vendors' documentation
for third-party cookie and storage partitioning, and regulators' published guidance on cookies and trackers
for the consent half. The collision-with-content-blockers point is that checklist topic checked against how public filter
lists describe matching names and paths; the rule against evasion is ours. Not taken: a console-stripping plugin or a bundler setting as a
tool (project choice, rule B), a linter configuration (same), and primitive-style advice (`const`/`let`,
array methods, module syntax), which the language and the linter already own. Written, not yet run on a
real audit.

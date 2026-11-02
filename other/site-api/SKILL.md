---
name: site-api
description: Find a website's own JSON endpoints by recording its traffic in the browser, then write a script that calls them directly — so a task that repeats (a scheduled report, a widget, a price or availability check) makes one HTTP request per run instead of driving the browser. Use when asked to "find the API" of a site, "turn this site into a script", or when the same site will be read on a schedule.
---

# Turn a site into a script

Driving the browser is right for the first visit and wrong for the hundredth. Most modern sites build their pages from JSON endpoints of their own; once those are known, a script can call them in a fraction of a second, on a schedule, without Chrome.

```
1. Record     browser_capture_traffic start → use the site → stop
2. Identify   pick the real endpoints out of the recording
3. Extract    request shape, parameters, response schema, what auth it needs
4. Write      one function per flow, in a script under the artifact or workspace
5. Verify     call every endpoint for real before relying on it
```

## 1. Record

- Open the site, then `browser_capture_traffic(action: "start")`. Recording covers the tab that is active when it starts.
- Do every flow the script should support, **each twice with different inputs** (two searches, two detail pages, page 1 and page 2). The difference between the two recorded URLs and bodies is what tells parameters from constants.
- If the site needs login, log in **before** starting — the login request then stays out of the recording.
- `browser_capture_traffic(action: "stop", label: "<site>-<flow>")` saves `/workspace/captures/<label>-<time>.har` and lists the responses that look like data (JSON/XML/CSV), first-party first, with method, status, URL and size. A web-browser sub-agent should report that path and list back to you.

## 2. Identify

The summary is a starting point; the file has everything. Query it with `jq`:

```bash
H=/workspace/captures/<file>.har
# every data response: method, status, URL
jq -r '.log.entries[] | select(.response.content.mimeType | test("json|graphql|xml|csv"))
  | "\(.request.method) \(.response.status) \(.request.url)"' "$H"
# one endpoint in full: request headers, body, response body
jq '.log.entries[] | select(.request.url | test("api/search"))
  | {method: .request.method, url: .request.url, headers: .request.headers,
     body: .request.postData.text, response: .response.content.text}' "$H"
```

Ignore telemetry and third parties (`/collect`, `/track`, `/beacon`, analytics, error reporting, ads). The real API is usually first-party, JSON, and fires right when you did something on the page.

## 3. Extract

- **Response schema**: each data endpoint's first response body is saved pretty-printed next to the HAR (paths in the stop result) — Read those; in the HAR it is `.response.content.text` (text bodies, capped at 256 KB each).
- **Parameters**: compare the two recordings of each flow — query string, path segments, POST body.
- **Auth**: the recording has **no Cookie or Set-Cookie headers** and none of the headers the browser adds on the wire (Origin, `sec-*`, Accept-Encoding) — agent-browser does not see them. A missing Cookie header proves nothing; the stop result lists the names of the cookies the browser holds for the site. Other values that look like secrets (`authorization`, token/session/CSRF headers and parameters, JWTs) read `[REDACTED]` (`REDACTED` inside URLs); their names are kept. Never try to recover a redacted value and never write one into a script.
- Test which headers matter by leaving them out (step 5). Many public read endpoints need none beyond a normal `user-agent` and `accept`.

## 4. Write

- One function per flow (`search(query, page)`, `getItem(id)`), parameters taken from what varied between recordings.
- Reproduce only the headers the endpoint actually requires; some sites refuse requests without a browser-like `user-agent` or a `referer`.
- An endpoint that needs the logged-in session cannot be called from a script without the session's cookies, which expire and must not be copied into source. Prefer endpoints that answer without it; keep a session-bound step in the browser, or ask the user before building anything that stores their session.
- Put it where it will run: an artifact's widget or dashboard script, or a workspace script a scheduled task calls.

## 5. Verify

Call every function against the live site and compare the shape with the recording.

| Symptom | Likely cause | What to do |
|---|---|---|
| 401/403 | The endpoint needs the session or a header you dropped | Add back headers one at a time; if it needs the session, keep that step in the browser |
| 403/419 on writes | A per-session or per-form CSRF token | Keep that flow browser-driven |
| Works, then breaks | Signed or expiring parameters (`sig`, `expires`, short-lived ids) | Fetch the value from the page or endpoint that issues it first, or keep that step in the browser |
| Different shape than recorded | A/B tests, location, logged-in vs out | Record again; treat the union as optional fields |
| 429 | Rate limit | Slow down; one request per scheduled run is the goal |

## Caveats

- Internal APIs change without notice. Keep the HAR next to the script so it can be re-derived, and make the script fail loudly (not silently return nothing) when the shape changes.
- Respect the site's terms and rate limits.
- The recording holds whatever the pages returned — the user's own data included. Keep it in the workspace; do not send it elsewhere.

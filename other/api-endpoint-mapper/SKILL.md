---

name: api-endpoint-mapper

description: Scan entire codebase to map all API endpoints (backend definitions and frontend calls), find mismatches where calls have no matching endpoint or endpoints are never called, and detect likely typos where names are similar but don't quite match. Use when debugging broken API connections, before refactoring API routes, when data isn't flowing correctly, or when Claude has broken API connections by renaming things incorrectly. Triggers on "map my API endpoints", "find broken API calls", "why isn't my data flowing", "find API mismatches", "audit my endpoints".

---



\# API Endpoint Mapper



Scans your entire codebase to find every API endpoint definition and every API call, then shows you exactly what's connected, what's broken, and what's probably a typo.



\## Quick Start



```bash

python scripts/scan\_endpoints.py /path/to/your/project

```



Outputs `API-ENDPOINT-REPORT.md` in the project root.



\## What It Finds



\### Backend Endpoint Definitions

\- Express routes: `app.get('/api/users')`, `router.post('/sensors')`

\- Next.js/file-based routes: `pages/api/\*`, `app/api/\*`

\- Route handlers with path patterns

\- WebSocket endpoints



\### Frontend API Calls

\- `fetch('/api/...')`

\- `axios.get/post/put/delete(...)`

\- Custom API clients

\- WebSocket connections

\- Environment variable URLs



\## Report Structure



The generated report contains:



```markdown

\# API Endpoint Report



\## Summary

\- Backend endpoints: X

\- Frontend calls: Y  

\- Matched: Z

\- UNMATCHED CALLS (BROKEN): N  ← These are your immediate problems

\- Unused endpoints: M

\- Potential typos: P



\## 🚨 BROKEN: Frontend Calls With No Backend

These calls will fail - no endpoint exists:

| Frontend Call | File:Line | Closest Match | Similarity |

|---------------|-----------|---------------|------------|



\## ⚠️ Potential Typos

These look like they should match but don't:

| Frontend | Backend | Difference |

|----------|---------|------------|



\## 📡 All Backend Endpoints

| Method | Path | File:Line | Called By |

|--------|------|-----------|-----------|



\## 📱 All Frontend Calls  

| Method | Path | File:Line | Matches |

|--------|------|-----------|---------|



\## 🔌 WebSocket Connections

| Event/Channel | Emitter | Listeners |

|---------------|---------|-----------|

```



\## Usage Patterns



\### Full project scan

```bash

python scripts/scan\_endpoints.py .

```



\### Specific directories

```bash

python scripts/scan\_endpoints.py . --frontend src/client --backend src/server

```



\### Include node\_modules API patterns (if using SDK)

```bash

python scripts/scan\_endpoints.py . --include-modules

```



\### JSON output for programmatic use

```bash

python scripts/scan\_endpoints.py . --json > endpoints.json

```



\## Fixing Mismatches



When the report shows broken calls:



1\. \*\*Check the "Closest Match" column\*\* - often it's a typo

2\. \*\*Check method mismatches\*\* - GET vs POST on same path

3\. \*\*Check path parameter differences\*\* - `/users/:id` vs `/users/${id}`

4\. \*\*Check base URL differences\*\* - `/api/v1/` vs `/api/`



\## Before Refactoring



Run this BEFORE renaming any endpoints. After changes:

1\. Run again

2\. Compare reports

3\. Ensure no new broken calls appeared



\## Configuration



Create `.endpoint-mapper.json` in project root for custom patterns:



```json

{

&nbsp; "backendPatterns": \[

&nbsp;   "customRouter\\\\.(get|post)\\\\(\['\\"](\[^'\\"]+)"

&nbsp; ],

&nbsp; "frontendPatterns": \[

&nbsp;   "apiClient\\\\.(get|post)\\\\(\['\\"](\[^'\\"]+)"

&nbsp; ],

&nbsp; "ignorePaths": \[

&nbsp;   "/health",

&nbsp;   "/metrics"

&nbsp; ],

&nbsp; "baseUrlEnvVars": \[

&nbsp;   "REACT\_APP\_API\_URL",

&nbsp;   "NEXT\_PUBLIC\_API\_URL", 

&nbsp;   "VITE\_API\_URL"

&nbsp; ]

}

```


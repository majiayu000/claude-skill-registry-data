---
name: tally-bridge
description: "Full end-to-end TallyPrime Bridge + Cloud Dashboard delivery. Two-step process: (1) CBO runs 'new-client' on their own laptop to provision cloud account and get credentials, (2) CBO AnyDesks into client machine and runs 'setup' to install bridge and sync. Use when onboarding a new Tally client, syncing vouchers, diagnosing sync issues, or running resyncs."
argument-hint: [new-client|setup|sync|debug|resync|status|deploy|verify|prep-machine]
---

# Tally Bridge — Full Delivery Skill

You are setting up, configuring, or managing a BuildWise Bridge Agent that syncs TallyPrime accounting data to a cloud dashboard.

**User's command:** `$ARGUMENTS`

---

## DEPLOYMENT MODEL — TWO MACHINES

The operator (CBO) uses TWO machines in sequence:

```
STEP 1: CBO's OWN Windows Laptop          STEP 2: Client's Windows PC (via AnyDesk)
┌────────────────────────────────┐         ┌────────────────────────────────┐
│ Claude Code + Supabase + Vercel│         │ Claude Code (basic, no MCPs)  │
│                                │         │ TallyPrime (:9000)            │
│ /tally-bridge new-client       │         │ Bridge Agent                  │
│   → Creates cloud account      │         │ Node.js                       │
│   → Deploys dashboard          │         │                               │
│   → Outputs: API key, URL, ID  │ ─────►  │ /tally-bridge setup           │
│                                │ (CBO    │   → Pastes API key, URL, ID   │
└────────────────────────────────┘ copies) │   → Connects to Tally         │
                                           │   → Syncs all vouchers        │
                                           │   → Sets up auto-start        │
                                           └────────────────────────────────┘
```

**CBO's laptop** has Supabase and Vercel access (set up once by tech team).
**Client's machine** has only Node.js, Claude Code, and bridge code. NO cloud credentials.

---

## WHAT THE CBO NEEDS TO KNOW

The CBO runs two commands total:

1. **On their own laptop:** `/tally-bridge new-client` → gives them 3 values to copy
2. **On client's machine (AnyDesk):** `/tally-bridge setup` → pastes those 3 values, everything else is automatic

That's it. The skill handles the rest.

---

## COMMUNICATION RULES

**ALWAYS use plain language.** The CBO is a business person, not a developer.

| DO say | DON'T say |
|--------|-----------|
| "Cloud account" | "Supabase tenant" |
| "Dashboard" | "Vercel deployment" |
| "Connection key" | "Bearer token" |
| "Data sync" | "Queue ingestion pipeline" |
| "The bridge" | "The Node.js polling agent" |
| "Auto-start" | "Windows Task Scheduler job" |

When something goes wrong, explain:
1. **What happened** (one sentence)
2. **What to do** (specific action)
3. **Who to call** (if CBO can't fix it — "contact the tech team")

---

## COMMAND ROUTING

| Command | Where to run | Action |
|---------|-------------|--------|
| `new-client` | CBO's laptop | PHASE 0 → 8 → show credentials |
| `prep-machine` | Client's machine (AnyDesk) | PHASE -1 (first-time setup) |
| `setup` | Client's machine (AnyDesk) | PHASE 1 → 2 → 3 → 4 → 5 → 7 → 9 |
| `sync` or `resync` | Client's machine (AnyDesk) | PHASE 3.1 → 3.2 → 3.3 → 3.4 → 4 → 5 (connectivity checks, company name validation, voucher count, cloud test, full FY resync, then health report). **Warning:** this resets the queue and re-pushes everything. Confirm with the CBO before proceeding. |
| `debug` | Client's machine (AnyDesk) | PHASE 6 (diagnose issues) |
| `status` | Client's machine (AnyDesk) | PHASE 5 (health report only) |
| `deploy` | CBO's laptop | PHASE 8 (dashboard deploy only) |
| `verify` | Either machine | PHASE 9 (end-to-end check) |
| _(empty/unclear)_ | — | Ask what they need in plain language |

---

## PHASE -1: PREPARE CLIENT MACHINE (First-time only)

Run this once on a new client machine. CBO remotes in via AnyDesk and opens a command prompt.

### -1.1 Check what's already installed

```cmd
node --version 2>nul
npm --version 2>nul
claude --version 2>nul
```

### -1.2 Install Node.js (if missing)

Tell the CBO: "Open a browser on this machine, go to **nodejs.org**, click the big green **LTS** button, and run the installer (click Next through everything)."

If the CBO prefers command-line install and has admin rights:
```cmd
:: Download latest Node.js LTS installer from nodejs.org
:: (Do NOT hardcode a version — always get the latest LTS)
curl -o %TEMP%\node-install.msi https://nodejs.org/dist/latest-v20.x/node-v20.18.0-x64.msi

:: Silent install (requires admin — run cmd as Administrator)
msiexec /i %TEMP%\node-install.msi /qn

:: Verify (may need to reopen command prompt)
node --version
```

> **Note:** The `msiexec /qn` silent install requires Administrator privileges. If it fails, the CBO should right-click the downloaded .msi and choose "Run as administrator", or install via the browser download instead.

### -1.3 Install Claude Code (if missing)

```cmd
npm install -g @anthropic-ai/claude-code
```

Help the CBO authenticate (Claude Max or API key).

### -1.4 Set up bridge directory

```cmd
mkdir C:\tally-bridge
mkdir C:\tally-bridge\data
```

### -1.5 Copy bridge code

The bridge source code needs to be on this machine:
1. **USB drive** the CBO carries: `xcopy /E /I D:\tally-bridge C:\tally-bridge`
2. **Network share**: `xcopy /E /I \\server\share\tally-bridge C:\tally-bridge`
3. **Git** (if available): `git clone <REPO_URL> C:\tally-bridge`

> **Bridge source code repo:**
> - Local path: `/Users/omm/PROJECTS/tally-bridge/`
> - (Local repo — no GitHub remote. Push to GitHub before CBO handoff.)

### -1.6 Install dependencies

```cmd
cd C:\tally-bridge && npm install
```

### -1.7 Verify

```cmd
node --version && dir C:\tally-bridge\package.json && dir C:\tally-bridge\node_modules
```

Tell the CBO: "This machine is ready. You can now run `/tally-bridge setup` to connect it."

---

## PHASE 0: CREATE CLOUD ACCOUNT (CBO's laptop)

This runs on the CBO's own laptop where Supabase and Vercel are configured.

### 0.1 Ask for company name

Ask the CBO:
- **What is the client's company name?** (e.g., "ABC School")

### 0.2 Generate credentials

```powershell
$companyName = "<COMPANY_NAME>"
$clientId = ($companyName.ToLower() -replace '[^a-z0-9]','-' -replace '-+','-').Trim('-')
$bytes = New-Object byte[] 16; [System.Security.Cryptography.RandomNumberGenerator]::Fill($bytes)
$apiKey = "bw_live_" + [BitConverter]::ToString($bytes).Replace('-','').ToLower()

Write-Host "Client ID: $clientId"
Write-Host "API Key: $apiKey"
```

### 0.3 Register in cloud database

Using Supabase CLI, insert the new client:

```sql
-- Requires pgcrypto extension for sha256
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Hash: SHA-256 of the raw UTF-8 API key string.
-- Bridge must match with: crypto.createHash('sha256').update(apiKey, 'utf8').digest('hex')
INSERT INTO clients (client_id, name, api_key_hash, status, created_at)
VALUES (
  '<CLIENT_ID>',
  '<COMPANY_NAME>',
  encode(sha256('<API_KEY>'::bytea), 'hex'),
  'active',
  NOW()
);
```

If tables don't exist yet, create them:
```sql
CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE IF NOT EXISTS clients (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  client_id TEXT UNIQUE NOT NULL,
  name TEXT NOT NULL,
  api_key_hash TEXT NOT NULL,
  status TEXT DEFAULT 'active',
  created_at TIMESTAMPTZ DEFAULT NOW()
);
ALTER TABLE clients ENABLE ROW LEVEL SECURITY;
-- Block anon access — only service_role can query
CREATE POLICY "service_role_only" ON clients FOR ALL USING (false);
```

### 0.4 Verify required tables

Check these tables exist:
- `clients` — client registry
- `vouchers` — synced voucher data
- `sync_status` — per-client sync state
- `reconciliation_logs` — daily reconciliation results

If any are missing, run migrations from the buildwise-mvp project.
- Local path: `/Users/omm/PROJECTS/buildwise-mvp/`
- (Local repo — no GitHub remote. Push to GitHub before CBO handoff.)

### 0.5 Proceed to dashboard deploy (Phase 8)

Phase 0 flows directly into Phase 8 when running `new-client`.

---

## PHASE 8: DEPLOY DASHBOARD (CBO's laptop)

Deploy or update the cloud dashboard. Runs on CBO's laptop.

### 8.1 Check existing deployment

Use the Vercel MCP:
```
mcp__vercel__list_projects → find buildwise-mvp
```

If already deployed and no changes needed, skip to 8.4.

### 8.2 Set environment variables (first time only)

Required env vars for Vercel (shared across all clients — set once):
```
NEXT_PUBLIC_SUPABASE_URL
NEXT_PUBLIC_SUPABASE_ANON_KEY
SUPABASE_SERVICE_ROLE_KEY
```

### 8.3 Deploy

Use the Vercel MCP:
```
mcp__vercel__deploy_to_vercel
```

### 8.4 Verify deployment

```cmd
curl -s -w "\n%%{http_code}" https://<VERCEL_DOMAIN>/api/tally/heartbeat ^
  -X POST -H "Content-Type: application/json" ^
  -H "Authorization: Bearer <API_KEY>" ^
  -H "X-Client-Id: <CLIENT_ID>" ^
  -d "{\"status\":\"deploy-verify\"}"
```

### 8.5 Show credentials for the CBO to copy

```
============================================
  CLIENT READY — COPY THESE 3 VALUES
============================================

  1. API Key:    bw_live_xxxxxxxxxxxxxxxxxxxxxxxx
  2. Cloud URL:  https://buildwise-dashboard.vercel.app/api/tally
  3. Client ID:  abc-school

============================================
  Now AnyDesk into the client's machine
  and run: /tally-bridge setup
  Paste these 3 values when asked.
============================================
```

---

## PHASE 1: COLLECT INPUTS (Client's machine)

This runs on the client's machine via AnyDesk.

Ask the CBO for the 3 values from Phase 0:
- **API Key** — starts with `bw_live_`
- **Cloud URL** — the dashboard address ending in `/api/tally`
- **Client ID** — the short name like `abc-school`

Also confirm:
- **Is TallyPrime open?** (must be running)
- **Tally port** — default `9000`
- **Install directory** — default `C:\tally-bridge`

---

## PHASE 2: INSTALL & CONFIGURE (Client's machine)

### 2.1 Verify bridge code is present

```cmd
dir C:\tally-bridge\package.json
```

If not found, run `/tally-bridge prep-machine` first.

### 2.2 Install dependencies (if not done)

```cmd
cd C:\tally-bridge && npm install
```

### 2.3 Create data directory and secure Tally port

```cmd
if not exist C:\tally-bridge\data mkdir C:\tally-bridge\data
```

**Lock down Tally API port** — Tally's XML API has no authentication. Block external access:
```cmd
netsh advfirewall firewall add rule name="Block Tally API External" dir=in action=block protocol=tcp localport=9000
netsh advfirewall firewall add rule name="Allow Tally API Localhost" dir=in action=allow protocol=tcp localport=9000 remoteip=127.0.0.1
```
Tell the CBO: "I've secured the Tally connection so only this computer can access it."

### 2.4 Generate config.json

Write `config.json` with the values the CBO pasted:

```json
{
  "tally": {
    "host": "localhost",
    "port": 9000,
    "companyName": "<AUTO_DETECTED — see Phase 3>",
    "pollIntervalSeconds": 60,
    "offHoursPollIntervalSeconds": 900,
    "heartbeatIntervalSeconds": 30,
    "offHoursHeartbeatIntervalSeconds": 120,
    "businessHoursStart": "08:00",
    "businessHoursEnd": "20:00",
    "financialYearStartMonth": 4,
    "requestTimeoutMs": 10000
  },
  "cloud": {
    "apiUrl": "<CLOUD_URL>",
    "apiKey": "<API_KEY>",
    "apiKeyInSecretStore": false,
    "clientId": "<CLIENT_ID>",
    "batchSize": 50,
    "retryMaxAttempts": 10,
    "retryBaseDelayMs": 1000
  },
  "queue": {
    "dbPath": "./data/queue.db",
    "maxSizeItems": 10000
  },
  "security": {
    "hmacSecretInSecretStore": false,
    "previousHmacSecrets": []
  },
  "reconciliation": {
    "enabled": true,
    "scheduleTime": "23:00",
    "autoResyncOnMismatch": true
  },
  "logging": {
    "level": "info"
  },
  "tls_tunnel": {
    "enabled": false
  }
}
```

### 2.5 Apply all known code fixes

**CRITICAL:** Verify and apply ALL known fixes. These prevent silent data loss.

Known fixes to check and apply:
1. **`isArray` config for `fast-xml-parser`** — Ensure `VOUCHER`, `ALLLEDGERENTRIES.LIST`, and `COMPANY` are in the `isArray` set. Without this, single-item responses are parsed as objects instead of arrays.
2. **Multiple `<TALLYMESSAGE>` blocks** — Ensure the XML parser merges all `TALLYMESSAGE` blocks before accessing `VOUCHER` arrays.
3. **ALTERID typed-object unwrapping** — `ALTERID` may be `{ "#text": "123", "@_TYPE": "Number" }`. Always unwrap before using as a number.
4. **Amount sign normalization** — All amounts must be stored as absolute (positive) values with `is_debit` boolean. Check `ISDEEMEDPOSITIVE` handling varies by voucher type.

If additional fixes exist in the bridge codebase (e.g., in a CHANGELOG or commit history), apply those too.

---

## PHASE 3: AUTO-DETECT & CONNECT (Client's machine)

### 3.1 Test Tally connectivity

```cmd
curl -s -o nul -w "%%{http_code}" http://localhost:9000 --connect-timeout 5
```

If not reachable, tell the CBO:
"Please make sure TallyPrime is open on this computer. Go to F1 > Settings > Connectivity and enable the API on port 9000."

### 3.2 Auto-detect company name

**Important:** Before inserting any company name into XML queries, XML-escape special characters: `&` → `&amp;`, `<` → `&lt;`, `>` → `&gt;`, `"` → `&quot;`. Common in Indian company names: "M/s. Kumar & Sons", "ABC (India) Pvt. Ltd."

Query Tally's ListOfCompanies API:
```xml
<ENVELOPE>
  <HEADER><VERSION>1</VERSION><TALLYREQUEST>Export</TALLYREQUEST>
  <TYPE>Collection</TYPE><ID>ListOfCompanies</ID></HEADER>
  <BODY></BODY>
</ENVELOPE>
```

Handle all name formats:
- Plain string: `<COMPANY>Name</COMPANY>`
- Object with NAME child: `<COMPANY><NAME>Name</NAME></COMPANY>`
- Object with NAME.LIST: `{ "NAME.LIST": { NAME: { "#text": "Name" } } }`
- Attribute format: `<COMPANY NAME="Name">`

If **1 company**: use it automatically.
If **multiple**: let the CBO pick from a list.
If **0**: tell the CBO to open a company in TallyPrime.

Update `config.json` with the company name.

### 3.3 Verify voucher access

Count vouchers in the current FY:
```xml
<ENVELOPE><HEADER><VERSION>1</VERSION><TALLYREQUEST>Export</TALLYREQUEST>
<TYPE>Collection</TYPE><ID>VC</ID></HEADER><BODY><DESC>
<STATICVARIABLES><SVCURRENTCOMPANY>COMPANY_NAME</SVCURRENTCOMPANY>
<SVFROMDATE>YYYYMM01</SVFROMDATE><SVTODATE>YYYYMMDD</SVTODATE></STATICVARIABLES>
<TDL><TDLMESSAGE><COLLECTION NAME="VC" ISMODIFY="No">
<TYPE>Voucher</TYPE><FETCH>DATE,VOUCHERTYPENAME,ALTERID</FETCH>
</COLLECTION></TDLMESSAGE></TDL></DESC></BODY></ENVELOPE>
```

Tell the CBO: "Found X vouchers in Tally (April to today)."

### 3.4 Test cloud connection

```cmd
curl -s -w "\n%%{http_code}" <API_URL>/heartbeat -X POST ^
  -H "Content-Type: application/json" ^
  -H "Authorization: Bearer <API_KEY>" ^
  -H "X-Client-Id: <CLIENT_ID>" ^
  -d "{\"status\":\"test\"}"
```

Tell the CBO: "Cloud connection confirmed" or "Cloud connection failed — [plain reason]."

---

## PHASE 4: FULL SYNC (Client's machine)

Pushes ALL vouchers from the current financial year to the cloud.

Tell the CBO: "Now syncing all vouchers to the cloud. This may take a few minutes."

### 4.1 Reset sync state

```cmd
cd C:\tally-bridge && npx tsx -e "import Database from 'better-sqlite3'; const db = new Database('./data/queue.db'); db.prepare('DELETE FROM sync_state').run(); db.prepare('DELETE FROM queue').run(); db.close(); console.log('Queue and sync state reset.');"
```

### 4.2 Run full-resync

```cmd
cd C:\tally-bridge && npx tsx src/full-resync.ts
```

If `src/full-resync.ts` is missing, create it from [full-resync-template.md](full-resync-template.md).

**Sync parameters:**
- Batch size: **25** (avoids rate limits)
- Delay between batches: **3 seconds**
- Max retries: **5** with exponential backoff
- Respect `Retry-After` header

### 4.3 Verify sync

```js
const db = new Database('./data/queue.db');
const q = db.prepare('SELECT status, COUNT(*) as cnt FROM queue GROUP BY status').all();
const s = db.prepare('SELECT * FROM sync_state').all();
db.close();
```

Tell the CBO: "All X vouchers synced successfully" or "X synced, Y failed — [what to do]."

---

## PHASE 5: HEALTH REPORT (Client's machine)

```
============================================
  TALLY BRIDGE — HEALTH REPORT
============================================
  Client:            <COMPANY_NAME>
  Machine:           This computer
  Install:           C:\tally-bridge

  Tally:             ONLINE / OFFLINE
  Company:           <name>

  Vouchers in Tally: <count>
  Vouchers synced:   <count>
  Pending:           <count>
  Failed:            <count>

  Cloud:             CONNECTED / NOT CONNECTED
  Dashboard:         <url>

  Last sync:         <timestamp>
  Auto-start:        ON / OFF
============================================
```

---

## PHASE 6: DEBUG & DIAGNOSE (Client's machine)

Run checks and explain in plain language:

1. **Is Tally running?** — `curl localhost:9000`
2. **Right company?** — compare Tally vs config
3. **Vouchers accessible?** — TDL query → count
4. **Bridge working?** — run for 65s, check errors
5. **Cloud reachable?** — test ingest endpoint
6. **Queue healthy?** — check for stuck items

Plain-language decision tree for the CBO:
```
Problem: Tally is not responding.
Fix: Open TallyPrime. Go to F1 > Settings > Connectivity > Enable API.

Problem: Wrong company showing.
Fix: Open the correct company in TallyPrime and restart the bridge.

Problem: Cloud rejected the data.
Fix: Check the API key is correct. If unsure, contact the tech team.

Problem: Data stuck in queue.
Fix: Restart the bridge. If it keeps happening, contact the tech team.
```

---

## PHASE 7: AUTO-START (Client's machine)

Set up the bridge to start when the computer turns on.

### Option A: Task Scheduler (Default — simplest)

```cmd
cd C:\tally-bridge && npm run build
schtasks /create /tn "TallyBridge" /tr "\"%ProgramFiles%\nodejs\node.exe\" C:\tally-bridge\dist\main.js" /sc onlogon /f
```

Verify:
```cmd
schtasks /query /tn "TallyBridge"
```

### Option B: PM2 (If more control needed)

```cmd
npm install -g pm2 pm2-windows-startup
cd C:\tally-bridge && npm run build
pm2 start dist/main.js --name tally-bridge
pm2 save
pm2-startup install
```

Tell the CBO: "Done. The bridge will start automatically when this computer turns on."

---

## PHASE 9: END-TO-END VERIFICATION (Either machine)

Verify data flows from Tally all the way to the dashboard.

### 9.1 Pipeline check

| Step | Check | Expected |
|------|-------|----------|
| Tally has data | XML query → count | Vouchers > 0 |
| Bridge synced | SQLite queue → status | All 'confirmed' |
| Cloud received | API status endpoint | Count matches Tally |
| Dashboard shows | Open URL in browser | Data visible |

### 9.2 Reconciliation

```cmd
curl -s https://<VERCEL_DOMAIN>/api/tally/reconcile ^
  -X POST -H "Authorization: Bearer <API_KEY>" ^
  -H "X-Client-Id: <CLIENT_ID>"
```

### 9.3 Delivery report

```
============================================
  DELIVERY COMPLETE
============================================
  Client:     <COMPANY_NAME>
  Dashboard:  <URL>

  Tally → Bridge:     CONNECTED
  Bridge → Cloud:     SYNCING (<N> vouchers)
  Cloud → Dashboard:  SHOWING DATA

  Vouchers:  <N> synced
  Range:     <start> to <end>
  Types:     Payment(<n>), Receipt(<n>),
             Contra(<n>), Journal(<n>)

  Auto-start:  ON
  Daily check: ON (runs at 11 PM)

  SAVE THESE:
  API Key:       bw_live_....<last 4 chars>  (full key in config.json)
  Dashboard:     <url>
  Client ID:     <id>
============================================
  The bridge will keep syncing automatically
  as long as TallyPrime is running on this
  computer.
============================================
```

---

## CBO QUICK REFERENCE

### Step 1: On your laptop
| Command | What it does |
|---------|-------------|
| `/tally-bridge new-client` | Create cloud account + deploy dashboard → gives you 3 values |

### Step 2: On client's machine (AnyDesk)
| Command | What it does |
|---------|-------------|
| `/tally-bridge prep-machine` | First-time: install Node.js, Claude Code, bridge code |
| `/tally-bridge setup` | Paste 3 values → connects Tally → syncs → auto-starts |
| `/tally-bridge status` | Check if everything is working |
| `/tally-bridge debug` | Find and fix problems |
| `/tally-bridge resync` | Re-sync all vouchers from scratch |

---

## CBO LAPTOP — ONE-TIME SETUP

The tech team (OMM) sets this up once on the CBO's Windows laptop:

1. **Install Claude Code** — `npm install -g @anthropic-ai/claude-code`
2. **Configure Supabase access** — add Supabase MCP or CLI credentials
3. **Configure Vercel access** — add Vercel MCP token
4. **Install the tally-bridge skill** — copy to `~/.claude/skills/tally-bridge/`

After this, the CBO just opens Claude Code and types `/tally-bridge new-client`. No further setup needed on the CBO's laptop.

---

## KNOWN EDGE CASES & KEY FACTS

### Tally-specific
- Tally XML API is **single-threaded** — never send concurrent requests
- Tally XML API has **no authentication** — restrict port 9000 to localhost only (see firewall rule in Phase 2.3)
- **XML-escape company names** before inserting into any XML/TDL query: `&` → `&amp;`, `<` → `&lt;`, `>` → `&gt;`, `"` → `&quot;` (common: "M/s. Kumar & Sons")
- Company name comparison: **trim + case-insensitive + Unicode-normalized**
- `fast-xml-parser` v5.x `isArray` config is critical — `VOUCHER`, `ALLLEDGERENTRIES.LIST`, `COMPANY` must be in the set
- Tally dates: `YYYYMMDD` → ISO: `YYYY-MM-DD`
- Financial year: defaults to **April 1** (month 4) — configurable via `financialYearStartMonth` in config.json
- ALTERID may reset at FY boundary (April 1) — change detector handles this
- Amounts: always absolute (positive) with `is_debit` boolean
- ISDEEMEDPOSITIVE meaning depends on voucher type (outgoing vs incoming)
- Collection TDL query returns typed objects `{ "#text": "val", "@_TYPE": "String" }` — always unwrap
- Multiple `<TALLYMESSAGE>` blocks — always merge before accessing VOUCHER
- `@_REMOTEID` is a GUID, not a number — prefer numeric `MASTERID` child element

### Cloud/Dashboard-specific
- Vercel serverless: ~10 req/min rate limit on heavy endpoints — pace bulk operations
- Vercel cold starts: first request after idle may take 3-5s
- All database queries MUST include client_id filter — multi-tenant isolation
- For multi-company setup details, see `references/multi-company-guide.md`
- API key rotation: generate new key, update bridge config, update cloud hash
- Reconciliation hash: bridge and cloud MUST use identical normalization
- Dashboard timezone: IST (Asia/Kolkata) for Indian accounting
- Batch HMAC: bridge signs with X-Batch-Signature, cloud verifies

### Windows-specific
- Use `cmd` syntax (`^` for line continuation, `%%` for variables)
- PowerShell may have execution policy restrictions
- Task Scheduler is the most reliable auto-start for non-technical users
- `curl` is available on Windows 10+ natively
- File paths use backslashes: `C:\tally-bridge\data\queue.db`

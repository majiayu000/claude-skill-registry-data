---
name: doc-catalog
description: Generate a service catalog for the current microservice (Java Spring Boot or frontend) and store it in the central service-catalog registry (default ~/.claude/service-catalog/, override with $CLAUDE_DOC_HOME). Scans the codebase to extract endpoints, integrations, dependencies, and key configuration. Use when starting a new service, after adding a new endpoint or integration, or when the catalog is out of date. `/sdd:doc-catalog list` shows what is already registered.
argument-hint: "[list] — omit to generate + store; 'list' to show the registry"
allowed-tools: Read, Write, Bash(find src:*), Bash(find .:*), Bash(find app:*), Bash(find pages:*), Bash(grep -r:*), Bash(cat src/**/*.java), Bash(cat src/**/*.yml), Bash(cat src/**/*.yaml), Bash(cat src/**/*.properties), Bash(cat pom.xml), Bash(cat package.json), Bash(cat next.config.*), Bash(ls:*), Bash(mkdir:*), Bash(git rev-parse:*), Bash(stat:*)
---

# Service Catalog


---

## Description

Scans the codebase, generates a single-page catalog entry for the current service —
what it does, what it exposes, what it integrates with, and how it is configured — and
**stores it directly in the central service-catalog registry**. There is no separate
publish step and **no copy is left in the service repo**: the registry is the single
home for the catalog, exactly like `/sdd:doc-investigation`.

Supports two stacks:
- **Java Spring Boot** — REST endpoints, SQS/SNS, Feign clients, scheduled jobs
- **Frontend (React / Next.js / Vue)** — routes/pages, API calls, external SDKs, feature flags

The catalog is generated from the code, not written by hand. This keeps it accurate —
it reflects what is actually deployed, not what someone documented 6 months ago.

---

## Modes

| Invocation | Action |
|------------|--------|
| `/sdd:doc-catalog` | **Generate + store (default)** — scan the codebase, generate the catalog, write it straight to `service-catalog/<service-name>.md` in the registry, and print the stored path. |
| `/sdd:doc-catalog list` | **List mode** — print the catalogs currently in the registry, with last-modified timestamps. Read-only; generates nothing. |

Reject any other argument with a usage message.

---

## Registry Path

All registry I/O resolves through a single environment variable, the same one every
`doc-*` command uses:

```bash
REGISTRY="${CLAUDE_DOC_HOME:-$HOME/.claude}/service-catalog"
```

- **Default** (no env var set): `~/.claude/service-catalog/`.
- **Override**: `export CLAUDE_DOC_HOME=/path/to/registry-root` — e.g. a cloned GitLab
  repo for team-shared catalogs. The catalog is written under
  `$CLAUDE_DOC_HOME/service-catalog/`.

The same variable controls `/sdd:doc-catalog-query`, `/sdd:doc-adr`, `/sdd:doc-spec`,
and `/sdd:doc-investigation`, so all doc registries move together.

---

## List Mode

Run when the argument is `list`. Print the registry and exit before any scan runs.

```bash
REGISTRY="${CLAUDE_DOC_HOME:-$HOME/.claude}/service-catalog"

if [ ! -d "$REGISTRY" ] || ! ls "$REGISTRY"/*.md >/dev/null 2>&1; then
  echo "Service catalog registry is empty."
  echo "Run /sdd:doc-catalog in a service repo to populate it."
  exit 0
fi

echo "Registered services in $REGISTRY:"
ls -lt "$REGISTRY"/*.md 2>/dev/null | while read -r line; do
  name="$(echo "$line" | awk '{print $NF}' | xargs basename)"
  mtime="$(echo "$line" | awk '{print $6, $7, $8}')"
  printf "  %-40s  (last updated %s)\n" "$name" "$mtime"
done
```

After listing, exit. Do not proceed to the generate steps below.

---

## Stack Detection

| Signal | Detected Stack |
|--------|---------------|
| `pom.xml` or `build.gradle` at repo root | Java Spring Boot |
| `package.json` at repo root (no `pom.xml`) | Frontend (React / Next.js / Vue) |
| Both present | Prefer Java; note the ambiguity in the catalog header |
| Neither found | Abort with: "Could not detect stack. Run from the project root." |

---

## What It Does — Java Spring Boot

| Step | Action |
|------|--------|
| 1 | Reads `pom.xml` or `build.gradle` → extracts `artifactId` as service name |
| 2 | Scans `application.yml` / `application.properties` for queue names, topic ARNs, and base URLs |
| 3 | Scans `@RestController` classes → extracts HTTP endpoints |
| 4 | Scans for `@SqsListener` annotations → extracts queues consumed |
| 5 | Scans for SNS publish calls → extracts topics published |
| 6 | Scans for `@FeignClient` interfaces → extracts service dependencies, **outbound auth, and resilience config** |
| 7 | Scans for `@Scheduled` → extracts background jobs |
| 8 | Scans for inbound webhook/callback endpoints and consumer-facing presigned-URL TTLs |
| 9 | Resolves the service name (see Service Name) → registry key `<service-name>.md` |
| 10 | If a catalog for this service already exists in the registry → merges with it (see Merge Strategy) |
| 11 | Prints the catalog and writes it straight to `service-catalog/<service-name>.md` (no in-repo copy, no confirmation prompt) |
| 12 | Prints the stored registry path |

## What It Does — Frontend

| Step | Action |
|------|--------|
| 1 | Reads `package.json` → extracts `name` as service name and detects framework (Next.js, React, Vue) |
| 2 | Scans route/page definitions → extracts pages and routes |
| 3 | Scans API service files and `fetch`/`axios`/`useQuery` calls → extracts backend APIs consumed |
| 4 | Scans `package.json` dependencies → extracts meaningful external SDK integrations |
| 5 | Scans for feature flag usage → extracts flags and their purpose |
| 6 | Scans `.env.example`, `next.config.*`, `vite.config.*` → extracts key environment variables |
| 7 | Resolves the service name (see Service Name) → registry key `<service-name>.md` |
| 8 | If a catalog for this service already exists in the registry → merges with it (see Merge Strategy) |
| 9 | Prints the catalog and writes it straight to `service-catalog/<service-name>.md` (no in-repo copy, no confirmation prompt) |
| 10 | Prints the stored registry path |

---

## Scanning Rules — Java Spring Boot

### Service name
Read `spring.application.name` from `application.yml` / `application.yaml` (or
`application.properties`) — this is the authoritative deployed name and what the
registry keys on, so `/sdd:doc-catalog`, `/sdd:doc-adr`, and `/sdd:doc-spec` resolve the
same value. Fall back to `<artifactId>` from `pom.xml` / `build.gradle`, then the root
directory name. Use it as the catalog's `# <ServiceName>` heading **and** as the
registry filename `<service-name>.md` (see Service Name below).

### REST Endpoints
Scan all `@RestController` classes. For each `@RequestMapping`, `@GetMapping`,
`@PostMapping`, `@PutMapping`, `@DeleteMapping`, `@PatchMapping`:
- Extract HTTP method and path (resolve class-level + method-level mappings)
- Use Javadoc `@summary` or first sentence of the method Javadoc as description
- If no Javadoc, derive description from the method name (camelCase → words)
- Mark `[internal]` if path starts with `/internal/`

### SNS Publishing
Look for:
- `SnsTemplate.sendNotification(...)` / `SnsTemplate.convertAndSend(...)`
- `SnsClient.publish(...)`
- `AmazonSNS.publish(...)`
- Any class named `*EventPublisher`, `*SnsPublisher`, `*NotificationService` that wraps SNS

Extract the topic name or ARN from the call or from the `application.yml` property it references.

**Message schema**: identify the object being published (e.g., `snsTemplate.convertAndSend(topic, myEvent)`).
Locate the `myEvent` class and scan its fields:
- Extract field name, Java type, and description from Javadoc or field name (camelCase → words)
- Unwrap `Optional<T>` → show `T?`
- Skip transient, static, and framework-internal fields
- Mark as `[INFERRED]` when description is derived from field name rather than Javadoc

### SQS Consuming
Look for `@SqsListener("${property.name}")` or `@SqsListener("queue-name")`.
Resolve property placeholders against `application.yml`.

**Message schema**: inspect the method parameter annotated with `@SqsListener`:
```java
public void handle(MyMessage message) { ... }   // ← scan MyMessage
public void handle(@Payload MyMessage message)  // ← same
```
Locate the `MyMessage` class and scan its fields using the same rules as SNS above.
If the parameter is `String` or `Map`, note `raw payload — no typed schema`.

### Feign Clients
Look for `@FeignClient(name = "...", url = "...")`.
Extract the service name and base URL.

**Outbound auth** — how this service authenticates *when calling* the dependency.
This is cross-service contract information: the called service's owner needs to know
who calls them and with what credentials. Resolve it from:
- A `configuration = SomeFeignConfig.class` attribute on `@FeignClient` → open that
  class and look for a `RequestInterceptor` bean. Report what it injects:
  - `Authorization: Bearer <...>` from a token service / credentials bean → `Bearer (<source bean>)`
  - Basic auth → `Basic`
  - API key header → `API key (<header name>)`
  - OAuth2 client-credentials / token exchange → `OAuth2 (<grant>)`
- An interceptor registered globally for the client, or a `@RequestHeader` on the
  client method that carries a token.
- If none found → `none [INFERRED]`.

**Resilience** — extract from the same `*FeignConfig` (or `application.yml`
`feign.client.config.<name>.*`): `Retryer` settings (max attempts, period, multiplier)
and `Request.Options` (connect / read timeouts). Report compactly, e.g.
`3× retry, 20s/60s`. Omit the cell (`—`) when nothing custom is configured.

### Webhooks & Callbacks
Inbound webhook/callback endpoints are integration points other systems POST to,
so surface them explicitly even though they also appear in the endpoint table.
- **Incoming**: controller methods whose path contains `callback`, `webhook`, or
  `notification`, *or* that are explicitly permitted (`permitAll`, `requestMatchers(...).permitAll()`)
  in a `SecurityFilterChain`. Report method, path, auth (often `public`/none), and the
  request DTO.
- **Outgoing**: callback URLs this service hands to an external system — look for
  config keys matching `*callback*url*` or `*webhook*url*` and report the property name.

Omit the section if neither is found.

### Consumer-facing TTLs
When the service issues S3 **presigned URLs** (`S3Presigner`, `generatePresignedUrl`,
`AwsS3Processor`), report the upload and download expiry as resolved from config
(`*presigned*expir*`, `*download*url*expiry*`). These TTLs are part of the contract
with whoever consumes the URLs (e.g. the frontend), so include them in **Key
Configuration** with the resolved default in the Purpose column. Omit if no presigned
URLs are issued.

### Background Jobs
Look for `@Scheduled` or `@ScheduledJob` annotations.
Extract the method name and cron expression or fixed delay.

### DTOs (Request / Response)
For each `@RestController` method, extract:
- **Request DTO**: the parameter annotated with `@RequestBody` → locate its class
- **Response DTO**: the return type, unwrapping `ResponseEntity<T>` → `T`, `List<T>` → `T[]`

For each DTO class found, scan its fields:
- Extract field name, Java type, and description from Javadoc or field name (camelCase → words)
- Determine required vs optional: `@NotNull`, `@NotBlank`, `@NotEmpty` → required; `@Nullable`, `Optional<T>` → optional
- Unwrap `Optional<T>` → show `T?`
- Skip transient, static, and framework-internal fields
- Mark as `[INFERRED]` when description is derived from field name rather than Javadoc
- Deduplicate: if the same DTO appears in multiple endpoints, document it once and reference it by name

---

## Scanning Rules — Frontend

### Service name
Read `name` from `package.json`. Detect framework from dependencies:
- `next` → Next.js
- `react` (no `next`) → React
- `vue` → Vue

### Routes / Pages
Detect routing pattern from framework:

| Framework | Where to scan |
|-----------|--------------|
| Next.js (App Router) | `app/**/page.tsx`, `app/**/layout.tsx` |
| Next.js (Pages Router) | `pages/**/*.tsx` (exclude `_app`, `_document`, `api/`) |
| React Router | `<Route path="...">` and `createBrowserRouter(...)` in `src/` |
| Vue Router | `routes` array in `router/index.ts` or `router.ts` |

For each route: extract path, component name, and auth requirement (look for auth guards or middleware).

### API Calls (Backend services consumed)
Scan for:
- `fetch(...)` / `axios.*` calls with URL strings or env var references
- React Query / TanStack Query `useQuery`, `useMutation` with endpoint keys
- Custom API service files (`*Api.ts`, `*Service.ts`, `*Client.ts`) with HTTP calls

Extract: HTTP method, endpoint path, purpose (from function/variable name or JSDoc).

### External SDK Integrations
Scan `package.json` `dependencies` for known external integrations and report those present:

| Package | Integration |
|---------|------------|
| `@aws-amplify/*` | AWS Amplify (Auth, Storage, etc.) |
| `@auth0/*` | Auth0 authentication |
| `@stripe/*` | Stripe payments |
| `firebase` / `@firebase/*` | Firebase |
| `@datadog/*` | Datadog monitoring |
| `launchdarkly-*` / `@growthbook/*` | Feature flags |
| `@segment/*` | Analytics |
| `@sentry/*` | Error tracking |

Report only packages that are actually in `package.json`. Do not invent integrations.

### Feature Flags
Look for:
- `process.env.NEXT_PUBLIC_FEATURE_*` or `import.meta.env.VITE_FEATURE_*`
- LaunchDarkly `useFlags()` / `useLDClient()` calls
- GrowthBook `useFeature(...)` calls
- Any boolean env var prefixed with `FEATURE_`, `FF_`, or `ENABLE_`

Extract: flag name, purpose (from usage context).

### Environment Variables
Scan `.env.example`, `next.config.js/ts`, `vite.config.ts` for `NEXT_PUBLIC_*`, `VITE_*`, or other app-level env vars. Exclude secrets (anything with `SECRET`, `KEY`, `TOKEN`, `PASSWORD`).

---

## Output Format — Java Spring Boot

```markdown
# Service: <artifactId>

> Last updated: <date> · Generated by /sdd:doc-catalog · Stack: Java Spring Boot

## Overview
<One paragraph describing what the service does — inferred from controller names,
service class names, and application.yml context. Mark inferences as [INFERRED].>

## Endpoints

| Method | Path | Request | Response | Auth |
|--------|------|---------|----------|------|
| POST | /api/v1/consent | `ConsentRequest` | `ConsentResponse` | Cognito JWT |
| GET | /api/v1/leads/:id | — | `LeadDTO` | Cognito JWT |
| GET | /internal/datavendor/circuit/status | — | `CircuitStatusDTO` | [internal] |

Auth column: `Cognito JWT` if secured, `public` if not, `[INFERRED]` if unclear.
Request/Response columns show the DTO name — full schema in the **Data Types** section below.

## Publishes (SNS)

| Topic | Event type | Trigger |
|-------|-----------|---------|
| `credit-results-topic` | `CreditReportReady` | DataVendor returns a result |
| `credit-results-topic` | `CreditReportFailed` | DataVendor circuit is open |

Topic ARN: `${aws.sns.credit-results-topic-arn}`

### `CreditReportReady` schema
| Field | Type | Description |
|-------|------|-------------|
| `leadId` | `String` | Lead identifier |
| `score` | `Integer` | Credit score (300–850) |
| `reportDate` | `LocalDate` | Date of the credit report |
| `provider` | `CreditProvider` | Credit bureau used [INFERRED] |

### `CreditReportFailed` schema
| Field | Type | Description |
|-------|------|-------------|
| `leadId` | `String` | Lead identifier |
| `reason` | `FailureReason` | CIRCUIT_OPEN or TIMEOUT |

Omit schema subsections when the published type is `String` or `Map` (raw payload).

## Consumes (SQS)

| Queue | Source topic | Event type | Published by |
|-------|-------------|-----------|-------------|
| `creditbureau-requests-queue` | `credit-requests-topic` | `CreditCheckRequested` | leads-service [INFERRED] |

### `CreditCheckRequested` schema
| Field | Type | Description |
|-------|------|-------------|
| `leadId` | `String` | Lead identifier |
| `checkType` | `CreditCheckType` | SOFT or HARD |
| `requestedAt` | `Instant` | When the check was requested |

Omit schema subsections when the listener parameter is `String` or `Map` (raw payload).

## Calls (Feign)

| Service | Base URL property | Auth | Resilience | Purpose |
|---------|------------------|------|-----------|---------|
| leads-service | `${feign.leads-service.url}` | Bearer (`ServiceUserPoolCredentials`) | 3× retry, 20s/60s | Fetch lead data |
| moxo-api | `${feign.moxo-api.url}` | OAuth2 (client_credentials) | — | Document binders |

Auth column: outbound credentials this service sends to the dependency
(`Bearer (<source>)`, `Basic`, `API key (<header>)`, `OAuth2 (<grant>)`, or
`none [INFERRED]`). Resilience column: custom retry/timeout config, `—` when default.

## Webhooks & Callbacks

| Direction | Method | Path / Property | Auth | Payload |
|-----------|--------|-----------------|------|---------|
| Incoming | POST | `/api/v1/stipulation/callback` | public | `MoxoCallbackRequestDto` |
| Outgoing | — | `moxo.callback_url` | — | URL handed to Moxo per environment |

Omit this section if no webhook/callback endpoints or callback-URL config are found.

## Background Jobs

| Job | Schedule | Purpose |
|-----|----------|---------|
| `cleanupExpiredConsents` | `0 0 * * * *` | Remove expired records |

Omit this section if no scheduled jobs are found.

## Data Types (DTOs)

### `ConsentRequest`
Used by: `POST /api/v1/consent` (request body)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `leadId` | `String` | ✓ | Lead identifier |
| `consentType` | `ConsentType` | ✓ | Type of consent granted |
| `source` | `String` | ✗ | Channel where consent was obtained [INFERRED] |

### `ConsentResponse`
Used by: `POST /api/v1/consent` (response)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | `UUID` | ✓ | Consent record identifier |
| `leadId` | `String` | ✓ | Lead identifier |
| `createdAt` | `Instant` | ✓ | When the consent was recorded |

Omit this section if no typed request/response DTOs are found.

## Key Configuration

| Property | Purpose |
|----------|---------|
| `aws.sqs.creditbureau-requests-queue` | Inbound request queue name |
| `aws.sns.credit-results-topic-arn` | Outbound results topic ARN |
```

---

## Output Format — Frontend

```markdown
# Service: <package-name>

> Last updated: <date> · Generated by /sdd:doc-catalog · Stack: <framework>

## Overview
<One paragraph describing what the application does — inferred from page names,
route structure, and API calls. Mark inferences as [INFERRED].>

## Pages / Routes

| Path | Component | Purpose | Auth |
|------|-----------|---------|------|
| / | HomePage | Landing page | public |
| /consent | ConsentPage | Consent capture form | Cognito JWT |
| /dashboard | DashboardPage | User dashboard | Cognito JWT |

Auth column: guard/middleware name if found, `public` if no auth, `[INFERRED]` if unclear.

## Backend APIs Consumed

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | /api/v1/consent | Submit consent record |
| GET | /api/v1/leads/:id | Fetch lead data |

## External Integrations

| Integration | Package | Purpose |
|-------------|---------|---------|
| AWS Amplify Auth | `@aws-amplify/auth` | Cognito authentication |
| Sentry | `@sentry/react` | Error tracking |

Omit this section if no known external SDKs are found.

## Feature Flags

| Flag | Purpose |
|------|---------|
| `NEXT_PUBLIC_FEATURE_CONSENT_UI` | Toggle consent form visibility |

Omit this section if no feature flags are found.

## Key Configuration

| Variable | Purpose |
|----------|---------|
| `NEXT_PUBLIC_API_BASE_URL` | Base URL for backend API calls |
| `NEXT_PUBLIC_COGNITO_USER_POOL_ID` | Cognito user pool |
```

---

## Service Name

The service name is both the catalog's `# <ServiceName>` heading and the registry
filename `<service-name>.md`. Resolve it in this order (first hit wins) — the **same
order** `/sdd:doc-adr` and `/sdd:doc-spec` use, so the service-catalog, adr-registry,
and spec-registry all agree on one key per service:

1. `spring.application.name` from `application.yml` / `application.yaml`
   (or `application.properties`) — authoritative for Spring services, it is the
   deployed service name.
2. `<artifactId>` from `pom.xml` / `build.gradle` (Java), or `name` from
   `package.json` (frontend).
3. git repo basename:
   ```bash
   git rev-parse --show-toplevel | xargs basename
   ```

Lowercase to kebab-case. Example: `spring.application.name: leads-service` →
`leads-service.md`.

---

## Merge Strategy

If a catalog for this service already exists in the registry
(`service-catalog/<service-name>.md`), read it first and merge rather than blindly
overwrite:

1. Parse its existing sections
2. For each section: if the scanned code produces a different result, take the
   freshly scanned result (the code is the source of truth)
3. Preserve any manually written content marked with `<!-- manual -->` — never
   overwrite it; carry it forward into the new file

There is **no in-repo `docs/service-info.md`** to reconcile — the registry copy is the
only one, so "merge" means merging the new scan into the existing registry entry.

---

## Write + Confirm

There is **no yes/no write gate and no commit offer** — creating the catalog stores it,
the same way `/sdd:doc-investigation` does. Print the full catalog so the user sees
exactly what landed, write it straight to the registry, then print the stored path:

```bash
REGISTRY="${CLAUDE_DOC_HOME:-$HOME/.claude}/service-catalog"
mkdir -p "$REGISTRY"
# Write the catalog with the Write tool to "$REGISTRY/<service-name>.md"
```

After writing, list every catalog now in the registry so the user can see what is
queryable:

```bash
ls -1 "${CLAUDE_DOC_HOME:-$HOME/.claude}/service-catalog"/*.md 2>/dev/null | xargs -n1 basename | sort
```

Then print the confirmation block, substituting the real names:

```text
Stored: ~/.claude/service-catalog/<service-name>.md

Registry now contains:
  consent-service.md
  leads-service.md
  marketing-service.md

Run /sdd:doc-catalog-query to ask cross-service questions.
```

Always print the full file list — never abbreviate to a count and never elide entries
with "...". The user can interrupt to edit if something in the catalog is wrong.

---

## Independence from the SDD Pipeline

This skill has no dependency on `.specwork/` artifacts and does not affect
`/sdd:whatnext`, `/sdd:state`, or any other SDD pipeline skill. It can be run at any
point — on an existing service, after a new endpoint or page is added, or as
part of onboarding a service to the catalog. It writes only to the registry, never to
the service repo's working tree.

---

## Related Skills

- `doc-catalog-query` — reads every catalog in the registry and answers cross-service questions
- `doc-adr` — capture architectural decisions made while building or evolving the service

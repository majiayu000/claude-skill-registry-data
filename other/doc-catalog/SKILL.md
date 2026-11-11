---
name: doc-catalog
description: Generate a service catalog for the current microservice (Java Spring Boot or frontend) and store it in the central service-catalog registry (default ~/.claude/service-catalog/, override with $CLAUDE_DOC_HOME). Scans the codebase to extract endpoints, integrations, dependencies, and key configuration. Use when starting a new service, after adding a new endpoint or integration, or when the catalog is out of date. `/sdd:doc-catalog list` shows what is already registered.
argument-hint: "[list] — omit to generate + store; 'list' to show the registry"
allowed-tools: Read, Write, Bash(find src:*), Bash(find .:*), Bash(find app:*), Bash(find pages:*), Bash(grep -r:*), Bash(cat src/**/*.java), Bash(cat src/**/*.yml), Bash(cat src/**/*.yaml), Bash(cat src/**/*.properties), Bash(cat pom.xml), Bash(cat package.json), Bash(cat next.config.*), Bash(ls:*), Bash(git rev-parse:*), Bash(python3 ${CLAUDE_PLUGIN_ROOT}/lib/registry.py:*), Bash(mkdir:*), Bash(git rev-parse:*), Bash(stat:*)
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

The same variable controls `/sdd:ask`, `/sdd:doc-adr`, `/sdd:doc-spec`,
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

Then, if this repo's own catalog is registered (resolve the name as in *Service Name*
below), report its freshness — commits and code files changed since the commit it was
verified at (the `Verified at` in its header):

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/lib/registry.py freshness "$REGISTRY/<service-name>.md"
```

After listing, exit. Do not proceed to the generate steps below.

---

## Verified-at commit

Before writing, record the commit the scan reflects and put it in the header line
(`Verified at: <commit>` in the REF templates):

```bash
git rev-parse --short=12 HEAD
```

`/sdd:doc-catalog list` compares it with HEAD (commits and code files changed since),
and `/sdd:ask` shows it next to every catalog it loads. Outside a git repo, omit the
`Verified at` field.

---

## Stack Detection

| Signal | Detected Stack |
|--------|---------------|
| `pom.xml` or `build.gradle` at repo root | Java Spring Boot |
| `package.json` at repo root (no `pom.xml`) | Frontend (React / Next.js / Vue) |
| Both present | Prefer Java; note the ambiguity in the catalog header |
| Neither found | Abort with: "Could not detect stack. Run from the project root." |

`REF` below means `${CLAUDE_PLUGIN_ROOT}/skills/doc-catalog/REFERENCE.md`. Once the
stack is known, read **only** its two sections before scanning: REF § Scanning Rules —
<stack> (what to extract and how) and REF § Output Format — <stack> (the catalog
template). List mode reads neither.

---

## What It Does — Java Spring Boot

| Step | Action |
|------|--------|
| 1 | Reads `pom.xml` or `build.gradle` → extracts `artifactId` as service name |
| 2 | Scans `application.yml` / `application.properties` for queue names, topic ARNs, and base URLs (rules for steps 2–8: REF § Scanning Rules — Java Spring Boot) |
| 3 | Scans `@RestController` classes → extracts HTTP endpoints |
| 4 | Scans for `@SqsListener` annotations → extracts queues consumed |
| 5 | Scans for SNS publish calls → extracts topics published |
| 6 | Scans for `@FeignClient` interfaces → extracts service dependencies, **outbound auth, and resilience config** |
| 7 | Scans for `@Scheduled` → extracts background jobs |
| 8 | Scans for inbound webhook/callback endpoints and consumer-facing presigned-URL TTLs |
| 9 | Resolves the service name (see Service Name) → registry key `<service-name>.md` |
| 10 | If a catalog for this service already exists in the registry → merges with it (see Merge Strategy) |
| 11 | Prints the catalog (template: REF § Output Format — Java Spring Boot) and writes it straight to `service-catalog/<service-name>.md` (no in-repo copy, no confirmation prompt) |
| 12 | Prints the stored registry path |

## What It Does — Frontend

| Step | Action |
|------|--------|
| 1 | Reads `package.json` → extracts `name` as service name and detects framework (Next.js, React, Vue) |
| 2 | Scans route/page definitions → extracts pages and routes (rules for steps 2–6: REF § Scanning Rules — Frontend) |
| 3 | Scans API service files and `fetch`/`axios`/`useQuery` calls → extracts backend APIs consumed |
| 4 | Scans `package.json` dependencies → extracts meaningful external SDK integrations |
| 5 | Scans for feature flag usage → extracts flags and their purpose |
| 6 | Scans `.env.example`, `next.config.*`, `vite.config.*` → extracts key environment variables |
| 7 | Resolves the service name (see Service Name) → registry key `<service-name>.md` |
| 8 | If a catalog for this service already exists in the registry → merges with it (see Merge Strategy) |
| 9 | Prints the catalog (template: REF § Output Format — Frontend) and writes it straight to `service-catalog/<service-name>.md` (no in-repo copy, no confirmation prompt) |
| 10 | Prints the stored registry path |

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

Run /sdd:ask to ask cross-service questions.
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

- `ask` — one query across every registry (catalog included)
- `doc-adr` — capture architectural decisions made while building or evolving the service

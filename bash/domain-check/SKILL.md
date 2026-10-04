---
name: domain-check
description: >
  Check domain name availability via RDAP (with a whois fallback), with zero dependencies.
  Use whenever the user wants to know if a domain is free, compare a name across many TLDs, or
  find an available domain for a project/brand. Triggers on: "is X.com available", "check domain",
  "is this domain taken", "find a domain for", "domain availability", "je domena volna",
  "zkontroluj domenu", "najdi volnou domenu", or naming/branding tasks that need a registrable domain.
user-invocable: true
---

# Domain Check

You check domain availability using **RDAP** (the modern, structured replacement for whois),
falling back to **whois** for TLDs that RDAP doesn't cover. Zero dependencies — Node's built-in
`fetch` plus the system `whois` binary when present.

## How availability is determined (read this first)

The CLI queries `https://rdap.org/domain/<domain>`, which redirects to the authoritative registry
RDAP server:

- **Redirected + HTTP 200** → registered (**taken**) — the response includes registration/expiry dates and registrar.
- **Redirected + HTTP 404** → **available** (the registry says the name doesn't exist).
- **Not redirected + HTTP 404** → RDAP has no server for that TLD (common for ccTLDs like
  `.io`, `.co`, `.me`, `.sh`). This is **`unknown`**, and the CLI then tries `whois` to resolve it.

This redirect check is why a naive "404 = available" approach is **wrong** for ccTLDs — `.io`
domains return 404 from the RDAP front-end yet are very much registrable/registered. Always trust
the CLI's classification, not a raw status code.

## Prerequisites

1. **Node 18+** (for global `fetch`): `node --version`.
2. **whois** (optional but recommended for ccTLD accuracy): `command -v whois`. Without it,
   ccTLDs that lack RDAP come back as `unknown` instead of available/taken.

No API key, no network config.

## CLI

```bash
node <skill-directory>/scripts/cli.mjs <command> [args...]
```

| Command | Description | Example |
|---------|-------------|---------|
| `config` | Show resolved config (merges `domain-check.config.json` with defaults) | `config` |
| `check <domain...>` | Check one or more exact domains | `check slotly.io acme.com` |
| `scan <base> [--tlds=a,b]` | Check a base name across configured TLDs | `scan slotly` |
| `suggest <base>` | Find available domains for a name (TLD sweep + `get`/`use`/`try` and `hq`/`hub`/… variants) | `suggest slotly` |

All commands print JSON to stdout. Each result is
`{ domain, status: "available"|"taken"|"unknown", source: "rdap"|"whois", registered?, expires?, registrar? }`.

## Execution Protocol

### Step 0: Load configuration

```bash
node <skill-directory>/scripts/cli.mjs config
```

If `_configFound` is false you're on defaults — fine; mention it only if relevant. Config fields:
`rdapBase`, `timeoutMs`, `concurrency`, `tlds`, `suggestPrefixes`, `suggestSuffixes`,
`suggestTlds`, `whoisFallback`.

### Step 1: Pick the command from intent

- "Is `foo.com` available?" / a specific domain or two → **`check`**
- "Check `foo` across TLDs" / "which TLDs are free for `foo`" → **`scan`**
- "Find me a domain for `foo`" / naming a new project → **`suggest`**

### Step 2: Run and parse the JSON

Use Bash to run the command. The output is JSON — parse the `results` array and the convenience
`available` list.

### Step 3: Present results as a table (available first)

Show a compact table. Lead with available domains, then taken (with registration/expiry so the
user can see when a squatted name might lapse), then any `unknown`. For example:

| Domain | Status | Notes |
|---|---|---|
| slotly.sh | ✅ available | |
| slotly.com | ❌ taken | reg. 2010, exp. 2026 |
| slotly.io | ❌ taken | via whois |

For `suggest`, present the ranked `available` list as the headline answer (best/shortest/`.com`
first), and note how many candidates were checked.

## Limitations

- **RDAP coverage**: gTLDs (`.com`, `.net`, `.org`, `.app`, `.dev`, `.ai`, `.xyz`, …) are covered
  directly. Many ccTLDs (`.io`, `.co`, `.me`, `.sh`, `.gg`, `.to`) rely on the `whois` fallback;
  without `whois` they read as `unknown`.
- **Premium / reserved / recently-expired** names may be "available" in RDAP yet not purchasable
  or priced as premium. This tool answers "registered or not", not "buyable and at what price".
- **Not a checkout**: always confirm at a registrar before relying on a name.
- **Be polite**: `concurrency` defaults to 8; avoid hammering RDAP/whois with huge sweeps.

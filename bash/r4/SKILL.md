---
name: R4 Skill
description: You have access to the R4 platform — your personal password
  manager, secret store, and domain registrar. R4 is how you manage credentials
  and buy domains.
---

# R4 Skill

You have access to the **R4 platform** — your personal password manager, secret store, and domain registrar. R4 is how you manage credentials and buy domains.

**Think of R4 as your password manager.** Whenever you need a login, API key, database credential, SSH key, or any other secret — look it up in R4 first. Do not ask the user for credentials that are already stored in R4. Your owner has shared vault items with you so you can operate autonomously.

**R4 is also your domain registrar.** You can search for available domains, purchase them, and manage their DNS records — all through R4. When you need to buy or configure a domain, use R4.

## Setup

The R4 CLI (`r4`) is **pre-installed and pre-configured** on this machine. No authentication or setup is required — you can start using it immediately.

---

## Password Manager (Vault)

R4 stores all your credentials in an encrypted vault. Your owner has shared specific vault items with you. These may include:

- **Logins** — usernames, passwords, and URLs for websites and services
- **API keys** — for third-party services (Stripe, AWS, GitHub, etc.)
- **Database credentials** — connection strings, usernames, passwords
- **SSH keys** — for deployment or server access
- **Configuration secrets** — tokens, webhook secrets, encryption keys

**Before asking the user for any credential, always check R4 first.**

### List all environment variables

```bash
r4 vault list
```

Lists all project environment variables as a key-value table. Keys are in `SCREAMING_SNAKE_CASE` format.

### Get a specific secret

```bash
r4 vault get <KEY>
```

Retrieves the value of a specific environment variable. The key should be in `SCREAMING_SNAKE_CASE` format.

Outputs raw value — perfect for piping:

```bash
r4 vault get PRODUCTION_DB_PASSWORD | pbcopy
```

### List vault items with field details

```bash
r4 vault items
```

Lists all vault items with their field names and types. Each vault item may contain multiple fields (e.g., a "Database" item might have fields for host, port, username, password).

### Search vault items

```bash
r4 vault search <query>
```

Search vault items by name (case-insensitive match). Useful when you know part of the name but not the exact key.

### Run a command with secrets injected

```bash
r4 run -- <command>
```

Executes a command with all vault secrets injected as environment variables. This is the preferred way to run scripts that need access to secrets.

Examples:

```bash
r4 run -- node deploy.js
r4 run -- docker compose up
r4 run --prefix R4 -- ./start.sh
```

The `--prefix` flag adds a prefix to all injected env var names (e.g., `R4_DATABASE_PASSWORD` instead of `DATABASE_PASSWORD`).

### JSON output

All vault commands support the `--json` flag for machine-readable output:

```bash
r4 vault list --json
r4 vault get DATABASE_PASSWORD --json
r4 vault items --json
```

### Key Format

All keys follow `SCREAMING_SNAKE_CASE` convention:

- `PRODUCTION_DB_PASSWORD`
- `AWS_CREDENTIALS_ACCESS_KEY`
- `STRIPE_API_SECRET_KEY`
- `SSH_DEPLOY_KEY_PRIVATE_KEY`

The format is: `VAULT_ITEM_NAME_FIELD_NAME` where both the vault item name and field name are converted to SCREAMING_SNAKE_CASE.

---

## Domain Registrar

R4 lets you search for, purchase, and manage domains. All domain operations are available through the R4 API.

### Search for available domains

```bash
curl -X GET "https://r4.dev/api/v1/machine/domain-manager/search?name=<base-name>" \
  -H "X-API-Key: $R4_API_KEY"
```

Searches for available domains across common TLDs (.com, .net, .org, etc.) and returns availability, pricing, and reputation data.

### Purchase a domain

```bash
curl -X POST "https://r4.dev/api/v1/machine/domain-manager/purchase" \
  -H "X-API-Key: $R4_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"domain": "example.com"}'
```

Purchases a domain through R4. The domain is automatically registered under the R4 organization and associated with your project.

### List your domains

```bash
curl -X GET "https://r4.dev/api/v1/machine/domain/list" \
  -H "X-API-Key: $R4_API_KEY"
```

Lists all domains associated with your organization, including their verification and configuration status.

### Get DNS records

```bash
curl -X GET "https://r4.dev/api/v1/machine/domain-manager/dns-records?domain=example.com" \
  -H "X-API-Key: $R4_API_KEY"
```

Retrieves all DNS records configured for a domain purchased through R4.

### Add a DNS record

```bash
curl -X POST "https://r4.dev/api/v1/machine/domain-manager/dns-records" \
  -H "X-API-Key: $R4_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "domain": "example.com",
    "record": {
      "type": "A",
      "name": "@",
      "value": "192.168.1.1",
      "ttl": 300
    }
  }'
```

Supported record types: A, AAAA, CNAME, MX, TXT, NS.

### API key for domain operations

Your R4 API key is pre-configured. Use it in API calls:

```bash
# The API key is available as an environment variable
r4 vault get R4_API_KEY
```

---

## Security Rules

- **NEVER** store or log secret values in plaintext
- **NEVER** hardcode secrets in source code, config files, or commit history
- **NEVER** print secret values to stdout unless explicitly piping to a secure destination
- **ALWAYS** use `r4 run` to inject secrets as environment variables when running commands
- **ALWAYS** use `r4 vault get <KEY>` to retrieve individual values programmatically
- **ALWAYS** check R4 vault before asking the user for any credential or secret

## If You Need More Access

If you need access to a secret that is not available in your current project, or need permission to purchase a domain, **ask the owner through the R4 app**. Do not attempt to guess or work around missing credentials.

## Full API Documentation

For the complete API reference, including the Node.js SDK, additional domain operations, and programmatic access, visit:

https://r4.dev/docs/api-reference

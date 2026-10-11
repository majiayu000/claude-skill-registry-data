---
name: cpanel
description: cPanel UAPI — auth, calling, responses, task recipes, and a reference of all 695 functions.
---

# cPanel UAPI

UAPI is cPanel's account-level API: everything a cPanel user can do in the interface (email, databases, domains, DNS, SSL, files, Git, backups, PHP, security), callable over HTTPS, from the server's CLI, or from cPanel plugins. This skill is the knowledge base for **guiding a user through, integrating with, and executing tasks on** a cPanel account via UAPI.

Source of truth: the official cPanel UAPI OpenAPI spec, **v11.138.0.10**, `https://api.docs.cpanel.net/_spec/specifications/cpanel.openapi.json`, plus the guides at `https://api.docs.cpanel.net/cpanel/introduction`. When the target server runs a different version, a function's `since` value in the module reference tells you whether it exists there.

## Detection Signals

| Signal | Meaning |
|---|---|
| `CPANEL_HOST` / `CPANEL_USER` / `CPANEL_TOKEN` (or `CPANEL_API_*`) env vars | Remote UAPI integration |
| `Authorization: cpanel …` header or `/execute/<Module>/<function>` URLs in code | Existing UAPI client |
| `.cpanel.yml` at the repo root | cPanel Git deployment |
| `uapi --user=` in scripts, cron or deploy hooks | Server-side CLI usage |
| `/usr/local/cpanel/php/cpanel.php`, `Cpanel::LiveAPI`, `Cpanel::API::*` Perl modules | cPanel plugin / custom UAPI module |
| Ports `2083` / `2096`, or `cpsess##########` in URLs | cPanel / Webmail session calls |
| The user mentions cPanel, WHM, shared hosting, "hospedagem cPanel" | Load this skill before answering |

## Scope Boundary

| API | Who | Covered here |
|---|---|---|
| **UAPI** | One cPanel account (`:2083`) | **Yes — fully** |
| WHM API 1 | Root / reseller, server-wide (`:2087`) | No. Only `uapi_cpanel` (UAPI proxied for a named account) is mentioned |
| cPanel API 2 / API 1 | Legacy | No — prefer the UAPI equivalent; never mix call styles |

If the task is server-wide (create cPanel accounts, packages, server config), say it needs WHM API 1 and root or reseller access, and do not improvise it with UAPI.

## How to Use This Skill

1. **Understand the intent**, then find the function in the **Intent Map** below or by grepping `references/function-index.md`.
2. **Open only the module file you need** in `references/modules/`. Each one is generated from the spec and lists every function in that group with method, RO/RW, rollback behaviour, version, full parameter list and return fields.
3. **Pick the call method** from [authentication.md](references/authentication.md): CLI on the server, API token remotely.
4. **Follow a recipe** in [recipes.md](references/recipes.md) when the task is a known workflow.
5. **Check `status`** on every response ([responses-and-errors.md](references/responses-and-errors.md)) and **verify** writes with a read-back.

```bash
grep -i "autossl" .dev-team-agents/skills/integrations/cpanel/references/function-index.md
```

## References

| File | Read it when |
|---|---|
| [references/authentication.md](references/authentication.md) | Choosing or setting up auth: API tokens, sessions, CLI, LiveAPI, WHM proxy |
| [references/calling-conventions.md](references/calling-conventions.md) | Building a call: URL anatomy, encoding (booleans `1`/`0`, lists, JSON params), GET vs POST, client snippets (curl, Python, Node, PHP), `Batch::strict` |
| [references/responses-and-errors.md](references/responses-and-errors.md) | Parsing results, handling failures, retries, async operations |
| [references/filter-sort-paginate.md](references/filter-sort-paginate.md) | Trimming large list outputs with `api.filter*`, `api.sort*`, `api.paginate*` |
| [references/recipes.md](references/recipes.md) | Executing a common task end to end |
| [references/security.md](references/security.md) | Before any integration or destructive operation |
| [references/custom-modules.md](references/custom-modules.md) | Writing a custom UAPI module in Perl (root on the server) |
| [references/function-index.md](references/function-index.md) | Finding a function: one row per function, with a link into its module file |
| `references/modules/<group>.md` | Full per-function reference (38 groups, generated). `modules/authentication.md` and `modules/security.md` are the 2FA/SSH **function groups**, not the guides above |

## Call Cheat Sheet

```bash
# Remote (API token)
curl -sS -H "Authorization: cpanel $CPANEL_USER:$CPANEL_TOKEN" \
  --data-urlencode "name=${PREFIX}app" \
  "https://$CPANEL_HOST:2083/execute/Mysql/create_database"

# On the server
uapi --user=$CPANEL_USER --output=jsonpretty Mysql create_database name=${PREFIX}app
```

| Rule | Detail |
|---|---|
| URL | `https://<host>:2083/execute/<Module>/<function>` — Module CamelCase, function snake_case |
| Booleans | `1` / `0` only (never `true`/`false`) |
| Success | `status == 1` — failures are still HTTP `200` |
| Secrets | POST body, never the query string |
| Notation | `Module::function` (for example `Email::add_pop`) |

## Intent Map

| The user wants to… | Functions | Module file |
|---|---|---|
| Create, list, change or delete **email accounts** | `UserManager::create_user`, `Email::add_pop`, `Email::list_pops_with_disk`, `Email::passwd_pop`, `Email::edit_pop_quota`, `Email::delete_pop` | `email.md`, `cpanel-account.md` |
| Set up **forwarders / autoresponders** | `Email::add_forwarder`, `Email::add_auto_responder` | `email.md` |
| Fix **email deliverability** (SPF, DKIM, DMARC) | `EmailAuth::validate_current_*`, `EmailAuth::enable_dkim`, `EmailAuth::install_spf_records`, `EmailAuth::apply_dmarc` | `dns.md` |
| Manage **spam** | `SpamAssassin::*`, `BoxTrapper::*`, `cPGreyList::*` | `email.md` |
| Create a **MySQL / PostgreSQL** database and user | `Mysql::get_restrictions`, `Mysql::create_database`, `Mysql::create_user`, `Mysql::set_privileges_on_database`, `Postgresql::*` | `mysql-and-mariadb.md`, `postgresql.md` |
| Allow **remote DB** access | `Mysql::add_host` | `mysql-and-mariadb.md` |
| Add a **subdomain / addon / alias** domain | `SubDomain::addsubdomain`, `AddonDomain::addaddondomain`, `Park::park`, `DomainInfo::domains_data` | `domain-management.md` |
| Edit **DNS** records | `DNS::parse_zone`, `DNS::mass_edit_zone` | `dns.md` |
| Get or install **SSL** | `SSL::start_autossl_check`, `SSL::get_autossl_problems`, `SSL::install_ssl`, `SSL::generate_csr` | `ssl-certificates.md` |
| **Redirect** a URL | `Mime::add_redirect` | `domain-management.md` / `website-configuration.md` (see index) |
| Change the **PHP version** / php.ini | `LangPHP::php_set_vhost_versions`, `LangPHP::php_ini_set_user_content` | `web-server-management.md` |
| **Deploy from Git** | `VersionControl::create`, `VersionControl::update`, `VersionControlDeployment::create` + `.cpanel.yml` | `git-management.md` |
| Read, write or **upload files** | `Fileman::list_files`, `Fileman::get_file_content`, `Fileman::save_file_content`, `Fileman::upload_files` | `files.md` |
| Create **FTP** accounts | `Ftp::add_ftp`, `Ftp::list_ftp_with_disk` | `files.md` |
| **Back up / restore** | `Backup::fullbackup_to_*`, `Restore::*`, `WebsiteBackup::*`, `WordPressBackup::*` | `cpanel-account-backups.md`, `website-backups.md`, `optional-applications.md` |
| Check **disk / bandwidth / limits** | `Quota::get_quota_info`, `ResourceUsage::get_usages`, `Bandwidth::query`, `StatsBar::get_stats` | `cpanel-account.md`, `retrieve-bandwidth-information.md` |
| Read **error logs / stats** | `Stats::get_site_errors`, `StatsManager::*` | `statistics.md` |
| **Block IPs**, ModSecurity, protect directories | `BlockIP::add_ip`, `ModSecurity::*`, `DirectoryPrivacy::*` | `block-ip-addresses.md`, `web-server-management.md`, `directory-management.md` |
| Manage **API tokens** | `Tokens::create_full_access`, `Tokens::list`, `Tokens::revoke` | `api-development-tools.md` |
| Manage **Subaccounts / team** | `UserManager::*`, `Team::*`, `TeamRoles::*` | `cpanel-account.md` |
| **WordPress** sites | `WordPressSite::*`, `WPX::*`, `WordPressBackup::*` | `website-configuration.md`, `optional-applications.md` |
| Node.js / Python / Ruby **apps** | `PassengerApps::*` | `web-server-management.md` |
| Calendars / contacts (**CalDAV/CardDAV**) | `DAV::*`, `CPDAVD::*`, `CCS::*` | `optional-applications.md` |
| Run several calls in sequence | `Batch::strict` | `api-development-tools.md` |
| **Two-factor** / external login providers | `TwoFactorAuth::*`, `ExternalAuthentication::*` | `modules/authentication.md` |
| Known SSH hosts, last login IP | `KnownHosts::*`, `LastLogin::*` | `modules/security.md` |

When the map has no match, grep the index. Never guess a function name: an unknown name fails, and a near-miss may call a different function.

## Operating Rules

### Guiding a User (explain mode)

- Give the exact `Module::function` and its **required** parameters from the module file, plus one ready-to-run example (CLI if they have shell access, curl otherwise).
- State prerequisites: the feature must be enabled, the server role must be active, and the DB prefix must be included.
- Mention the UI path as an alternative only when the user is not automating.

### Executing Tasks (act mode)

1. **Credentials:** read them from env vars or the project's credentials mechanism (`skills/shared/credentials/SKILL.md`). Never ask the user to paste a token into the chat. If none is configured, guide them to create one (`references/authentication.md`) and store it as a secret.
2. **Read before write:** list the current state first; it prevents "already exists" failures and makes rollback possible.
3. **Confirm destructive calls** with `AskUserQuestion`, using the list in [security.md](references/security.md#destructive-operations--confirm-first).
4. **Check `status`** on every call; surface `errors[]` verbatim and `warnings[]` as notes.
5. **Verify** with a read-back, and report what changed (resource, before → after).
6. **Async operations** (backups, deploys, AutoSSL): report "started", poll the status function, and report the outcome.

### Integrating (building a client)

- Wrap calls in one function: POST form-encoded, `status` check, raise on `errors`, log `warnings`. Snippets are in [calling-conventions.md](references/calling-conventions.md#client-snippets).
- Keep the timeout ≥ 60 s for slow functions (backups, SSL, DNS).
- Retry only transport failures; never auto-retry `status: 0`.
- Treat the cPanel version as a dependency: record it (`ServerInformation::get_information`) and check `since` before using newer functions.
- Do not scrape or post to cPanel interface URLs (`/frontend/jupiter/…`). Only the API is supported.

## Common Pitfalls

| Pitfall | Avoid by |
|---|---|
| Treating HTTP 200 as success | Checking `status == 1` |
| Sending `true`/`false` | Sending `1`/`0` |
| Missing DB prefix (`app` instead of `user_app`) | `Mysql::get_restrictions` → `prefix` |
| `privileges` assumed to be additive | It **replaces** the list — send the full set |
| Stale DNS serial | Re-parse the zone right before `DNS::mass_edit_zone` |
| Decoding DNS names as plain text | `parse_zone` returns base64 (`dname_b64`, `data_b64`) |
| Uploading files with GET or on the CLI | `Fileman::upload_files` = POST `multipart/form-data` only |
| Calling UAPI on `:2087` | `:2083`, or WHM `uapi_cpanel` |
| `Email::add_pop` breaking password reset | Prefer `UserManager::create_user` |
| Numeric sort failing | Set `api.sort_method=numeric` |
| Assuming a function exists everywhere | Check `since`, feature lists (`Features::has_feature`) and server roles |

## Regenerating the Reference

The files in `references/modules/` and `references/function-index.md` carry a `GENERATED` header. When cPanel publishes a new UAPI version, regenerate them from the spec URL above rather than editing them by hand. In the dev-team-agents repository, run `bash helpers/gen-cpanel-uapi-reference.sh`; `--check` reports drift without writing. That helper is dev-only and is not shipped to installed projects. Bump the version in this file's *Source of truth* line, and re-check `recipes.md` against any changed or deprecated function (the index flags them **(deprecated)**).

---
name: poste-mailserver-ops
description: Run a poste.io mailserver, install, mailboxes, SMTP auth.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [poste, mailserver, smtp, haraka, docker]
    related_skills: [api-provider-integration, docker-service-recovery]
    triggers: [poste setup, poste install, mailserver configuration, smtp not working, mail.your-domain.example, create mailbox, poste guard, smtp authentication failed, configure poste]
---

# Poste.io Mailserver Operations

Operating a self-hosted poste.io (analogic/poste.io) mailserver in the agency
Docker stack. Poste bundles Haraka (SMTP), Dovecot (IMAP), rspamd, Roundcube.
Admin UI is a Symfony app; there is also a CLI. All steps below were proven
live on 2026-08-04 (mail.your-domain.example).

## Headless install (no clicking through the web UI)

The setup page is `GET /admin/install/server` (a Symfony form). The CSRF token
is session-bound, so curl MUST reuse cookies:

```bash
JAR=$(mktemp)
HTML=$(curl -sk -m 20 -c "$JAR" "$BASE")   # GET -> token + session cookie
TOK=$(echo "$HTML" | grep -oE 'name="install\[_token\]" value="[^"]+"' | head -1 \
  | sed -E 's/.*value="([^"]+)".*/\1/')
curl -sk -m 40 -b "$JAR" -c "$JAR" -X POST "$BASE" \
  --data-urlencode "install[hostname]=mail.example.com" \
  --data-urlencode "install[superAdmin]=ops@example.com" \
  --data-urlencode "install[superAdminPassword]=$PW" \
  --data-urlencode "install[_token]=$TOK"
```

Success = response redirects to `/admin/` (not the setup page, not a 500).
Verify: `/data/server.ini` exists with `server_hostname`, `/data/domains/`
contains the domain, admin row in `/data/users.db` (`superAdmin=1`).

## Compose hardening gotcha: no-new-privileges kills the installer

If the stack applies a global `security_opt: [no-new-privileges:true]` anchor,
the install POST dies with HTTP 500:
`sudo: The "no new privileges" flag is set, which prevents sudo from running as root`
(the installer shell-outs `sudo -u root /etc/cont-init.d/20-apply-server-config`).
Fix: override per-service AFTER the anchor merge:

```yaml
<<: [*restart_policy, *security_defaults]
security_opt:
  - no-new-privileges:false
```

## Guard blacklists the Docker gateway (554 Blacklisted)

Authenticated internal SMTP gets `554 Blacklisted [172.25.0.1]` because the
guard plugin flags the Docker bridge gateway. Whitelist it in the guard table
(rows = IP range packed as hex in start/end BLOBs; block=0 whitelists):

```sql
INSERT OR IGNORE INTO guard (identifier, block, start, "end", priority, comment)
VALUES ('docker-gateway-172.25.0.1', 0, X'AC190001', X'AC190001', 1000,
        'Allow Docker gateway (agency-stack)');
```

Hex: 172.25.0.1 = AC.19.00.01; 172.27.0.1 = AC.1B.00.01 (per-octet hex).
Persist the INSERT in the image's cont-init bootstrap script so it survives
recreates — the row lives in the users.db volume, but a fresh volume loses it.

## Creating mailboxes via CLI

`/opt/admin/bin/mailserver` inside the container:
- `domain:create <domain>` / `domain:list` / `domain:dkim`
- `email:create <email> <password> [name]` — **must run as UID 8** (the mail
  user), else: `"This command should be running as user UID 8, you run this
  script as 0"`. Use `docker exec -u 8 <container> /opt/admin/bin/mailserver ...`.
- `email:admin` (super admin), `email:disable` / `email:enable`

## SMTP auth quirks (the three that bite)

1. **AUTH requires the FULL email address** — `leads` fails with 535; use
   `leads@your-domain.example`.
2. **STARTTLS is required before AUTH on 587** — raw EHLO then AUTH LOGIN
   hangs; the server announces `250 STARTTLS`. Nodemailer handles this
   automatically — test with the app's own library, not a raw socket.
3. **Self-signed cert** — nodemailer fails with `self-signed certificate`;
   set `tls: { rejectUnauthorized: false }` (backend env knob:
   `SMTP_TLS_REJECT_UNAUTHORIZED=false`).

## Verifying a real send (the pattern that proves it)

Don't trust the 220 banner — send a real message from the app container using
the app's own mail library:

```js
const nodemailer = require("nodemailer");
const t = nodemailer.createTransport({
  host: "mail.your-domain.example", port: 587, secure: false,
  tls: { rejectUnauthorized: false },
  auth: { user: process.env.SMTP_USER, pass: process.env.SMTP_PASS },
});
await t.sendMail({ from, to: "ops@your-domain.example", subject, text });
// expect info.accepted.length === 1
```

## Wiring app containers to SMTP

Every app container in the stack sends through the same poste server with its
own mailbox. Shared env pattern, dedicated STARTTLS transport for
Haraka-compat, `SMTP_FROM` must match the authenticated mailbox (else
`550 Authentication required`), and the mailbox→service env map
(`LEADS_SMTP_PASS`, `STACK_WATCHDOG_SMTP_PASS`, `CALCOM_EMAIL_SERVER_PASSWORD`,
`FONOSTER_SMTP_PASSWORD`): `references/smtp-wiring-for-app-stacks.md`.

## Misc facts

- `HTTPS: OFF` + `HTTP_PORT: 80` in compose env; ports 25/110/143/465/587/993/995/4190.
- SMTP greeting shows the configured hostname only after install
  (`220 mail.your-domain.example ESMTP Haraka ready`); default is `mail.example.com`.
- Custom bootstrap scripts live in `/etc/cont-init.d/` (s6-overlay);
  `36-codex-poste-bootstrap.sh` re-applies DKIM perms + smarthost routes on boot.
- Outbound deliverability needs public DNS: A for the hostname, MX, SPF, and
  the DKIM TXT record poste generates (`/data/dkim/<domain>/dns`).
- No SQLite CLI in every container: query `/data/users.db` with the bundled
  `/usr/bin/sqlite3` inside the poste container itself.

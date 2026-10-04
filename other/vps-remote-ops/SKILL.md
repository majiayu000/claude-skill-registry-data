---
name: vps-remote-ops
description: SSH, 9router DB recovery, Hermes cache cleanup on VPS.
---

Use when managing remote VPS (GreenCloud), SSH access, 9router login recovery, or Hermes cache cleanup.

Always-on rules:
- SSH: key-only auth on port 2222 (GreenCloud firewall blocks 22). Key at /root/.ssh/id_ed25519.
- User prefers quick action over explanation; reply in casual Indonesian.
- Never invent password reset if DB is missing — recreate table manually.

Procedure for 9router login failure after update:
1. SSH into VPS.
2. Check docker ps (9router running?)
3. Inspect /root/9router-data/auth/ and /db/data.sqlite.
4. If users table missing: recreate via SQLite (drop + create + insert with bcrypt hash).
5. Restart container only after verifying DB state.
6. Cache cleanup: rm -rf /root/.hermes/cache/uv/* /root/.hermes/cache/terminal-output/*
7. Set cron: 0 3 * * 0 rm ... (weekly cleanup).

Pitfalls:
- 9router DB uses sqlite3; container may lack sqlite3 binary — run sqlite3 from host, not docker exec.
- Password must be hashed (bcryptjs) — plaintext insert will fail login; manual bcrypt insert via host sqlite3 may still fail if 9router expects different schema/fields.
- Cache can grow >280MB quickly; cleanup weekly is mandatory.
- Don't restart container blindly — check custom-server.js first for auth logic.
- **If manual DB recovery fails, the working fallback is Hermes Desktop login** (which uses the same 9router backend but authenticates via its own session).
- X API trends endpoint (/2/trends/geo/45232) returns empty without OAuth2 — use trends24.in web scraping as reliable fallback for trending topics.
- Skill sync from desktop to VPS works (curator creates/updates skills), but memory sync (MEMORY.md, USER.md) does not — verify separately.
- Cron reminder for daily trending report: set at 08:00 WIB via crontab; log output to /tmp/x_trends_report.log.
- VPS load can spike to 160+ but still serve requests — check `uptime` and `docker ps` before assuming down.
- aaPanel 404 on /a83a1c60/ path: APSESS_PATH_RE middleware requires apsess_ token prefix. Fix: enable wrap_apsess_middleware(app) AND add /a83a1c60/ to public_paths whitelist in require_apsess().
- WordPress Sejoli LMS member login at /member-area/login/ uses custom table prefix (wplo_ / wplox_). Check wp-config.php for $table_prefix; user tables are wplox_users / wplox_usermeta, not wp_users / wp_usermeta.
- WhatsApp bot (Baileys) runs on local PC, not VPS. For 24/7 operation, deploy bot to VPS (Docker/container) or use Telegram bot via telegram-messaging skill.
- Cron cleanup weekly at 03:00 WIB: `0 3 * * 0 rm -rf /root/.hermes/cache/uv/* /root/.hermes/cache/terminal-output/* 2>/dev/null`


References:
- 9router model-catalog is stored in /root/9router-data/model-catalog.json (intact across updates).
- Auth file is cli-secret (hash); user table is in data.sqlite (not auth/ dir).
- Cron cleanup weekly at 03:00 WIB: `0 3 * * 0 rm -rf /root/.hermes/cache/uv/* /root/.hermes/cache/terminal-output/* 2>/dev/null`

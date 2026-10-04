---
name: orbit-docker-site
description: Spin up, manage, and troubleshoot a WordPress test site (wp-env / wp-now / Docker) for Orbit. Use when the user says "create test site", "spin up WP", "wp-env", "Docker WordPress", "I need a local WP", "site not loading", or any browser test fails because the site isn't running. Walks them from "no site" to "site at localhost:8881 with plugin installed and Query Monitor active".
---

# Orbit — Docker / wp-env Test Site

You set up the **WordPress test environment** Orbit runs against. Two paths:

- **Path A — `@wordpress/env`** (Docker-based, recommended) — fully isolated, scriptable, multi-version, what CI uses.
- **Path B — `wp-now`** (no Docker, instant) — for quick sanity checks.

Default Orbit port: **8881**.

---

## Decision tree — which path?

```
Does the user need...
├─ Multi-version PHP × WP testing?         → Path A (wp-env)
├─ Multiple parallel sites?                → Path A
├─ Full gauntlet with DB profiling?        → Path A
├─ Just a quick "does my widget render"?   → Path B (wp-now)
├─ CI / GitHub Actions later?              → Path A
└─ "I don't have Docker installed"         → Path B (or install Docker)
```

---

## Path A — wp-env (recommended)

### Prerequisites
- Docker Desktop running (`docker ps` should not error)
- Node 18+ (`node -v`)

If Docker isn't installed: tell them to grab https://www.docker.com/products/docker-desktop/. Don't try to install via Homebrew — Docker Desktop is the only sane Mac option for now.

### One-command site creation

```bash
bash scripts/create-test-site.sh --plugin ~/plugins/my-plugin --port 8881
```

What this does:
1. Generates `.wp-env-site/.wp-env.json` from `qa.config.json`
2. `wp-env start` — pulls Docker images, boots WP + MySQL
3. Auto-installs Query Monitor (for `/orbit-db-profile`)
4. Activates the user's plugin
5. Saves admin cookies via `auth.setup.js` (for Playwright)

Wait for: `WordPress site is now running at http://localhost:8881`.

Verify:
```bash
curl -sI http://localhost:8881/wp-admin | head -1
# → HTTP/1.1 302 Found  ← good, WP is up
```

### Customise PHP / WP version

Edit `.wp-env-site/.wp-env.json`:
```json
{
  "core": "WordPress/WordPress#tags/6.5",
  "phpVersion": "8.2",
  "plugins": [
    "./path/to/my-plugin",
    "https://downloads.wordpress.org/plugin/query-monitor.zip"
  ],
  "config": {
    "WP_DEBUG": true,
    "WP_DEBUG_LOG": true,
    "SAVEQUERIES": true
  }
}
```

Then:
```bash
wp-env stop
wp-env start
```

### Lifecycle commands

```bash
wp-env stop                       # pause (no data loss)
wp-env start                      # resume
wp-env destroy                    # nuke the site (data lost)
wp-env clean all                  # reset DB to clean state
wp-env run cli wp <wp-cli-cmd>    # run any wp-cli command in the container
wp-env logs                       # tail container logs (if site won't load)
```

### Multiple parallel sites (for `--port 8882`, `--port 8883`...)

```bash
bash scripts/create-test-site.sh --plugin ~/plugins/plugin-a --port 8881
bash scripts/create-test-site.sh --plugin ~/plugins/plugin-b --port 8882
```

Each site lives in its own subdir under `.wp-env-sites/`.

---

## Path B — wp-now (no Docker)

```bash
npm i -g wp-now
cd ~/plugins/my-plugin
wp-now start
```

→ Site at http://localhost:8881 with the plugin auto-activated.

Limitations:
- No `performance_schema` (DB profiling won't work)
- No multi-version matrix
- Re-runs lose state unless `--mode persist` is set

Use `wp-now` only for quick "does my widget render" checks. For real audits, switch to `wp-env`.

---

## Common failures

### "Port 8881 already in use"
```bash
lsof -ti tcp:8881 | xargs kill -9
# Or pick a different port:
bash scripts/create-test-site.sh --plugin ~/plugins/my-plugin --port 8888
```
Update `qa.config.json` `wpEnv.port` accordingly.

### "Cannot connect to Docker daemon"
Docker Desktop isn't running. Open the Docker Desktop app, wait for the whale icon to settle.

### "Plugin not found / not active"
Check the plugin path in `.wp-env-site/.wp-env.json`. Must be absolute.
```bash
wp-env run cli wp plugin list
```

### "Permission denied" on Mac M1/M2
```bash
sudo chown -R $(whoami) ~/.wp-env
```

### Site loads but admin login fails
```bash
wp-env run cli wp user create admin admin@local.test \
  --role=administrator --user_pass=password
```
Default Orbit credentials: `admin` / `password`.

### Site is slow / containers spinning up forever
```bash
docker system prune -a            # WARNING: deletes ALL Docker data
wp-env destroy
wp-env start
```

### "WordPress is already installed" on first run
Old site state. Clean it:
```bash
wp-env destroy
rm -rf .wp-env-site/
bash scripts/create-test-site.sh --plugin ~/plugins/my-plugin --port 8881
```

---

## Multi-version matrix (PHP × WP)

For `/orbit-compat-matrix` to work, you need multiple wp-env configs. This is automated:

```bash
bash scripts/create-test-site.sh --plugin ~/plugins/my-plugin --port 8881 --php 7.4
bash scripts/create-test-site.sh --plugin ~/plugins/my-plugin --port 8882 --php 8.1
bash scripts/create-test-site.sh --plugin ~/plugins/my-plugin --port 8883 --php 8.3
```

Each runs in its own Docker container — isolated.

---

## When to recreate vs reuse

| Situation | What to do |
|---|---|
| Daily dev loop | `wp-env start` (reuse) |
| After PHP version upgrade | `wp-env destroy` → recreate |
| Test depends on clean DB | `wp-env clean all` |
| Plugin's `register_activation_hook` ran wrong | `wp-env clean all` then re-activate |
| Switching to a different plugin | New port: `--port 8882` |
| `wp-env start` hangs > 5 min | `wp-env destroy` + recreate |

---

## Verify before any audit

Before running `/orbit-gauntlet` or any browser-based skill, verify the site:

```bash
# 1. Site responds
curl -sI http://localhost:8881 | head -1

# 2. Plugin is active
wp-env run cli wp plugin list --status=active --field=name | grep my-plugin

# 3. Query Monitor is active (needed for DB profile)
wp-env run cli wp plugin list --status=active --field=name | grep query-monitor

# 4. Admin user exists
wp-env run cli wp user list --role=administrator --field=user_login
```

If any fails, recreate the site.

---

## Auth cookies for Playwright

Playwright tests need a logged-in admin session. First-time setup:

```bash
WP_TEST_URL=http://localhost:8881 npx playwright test \
  tests/playwright/auth.setup.js --project=setup
```

Saves cookies to `.auth/admin.json`. **Never commit this file** — it contains a session token.

If a Playwright test fails with "user not logged in", re-run auth.setup.js — cookies expire after the site is destroyed.

---

## Output summary

After successful site creation:

```
✅ Test site running
   URL:        http://localhost:8881
   Admin:      http://localhost:8881/wp-admin (admin / password)
   Plugin:     <slug> active
   PHP:        <version>
   WP:         <version>
   Auth saved: .auth/admin.json

Next:
  /orbit-gauntlet --mode quick    first audit
  /orbit-playwright               run E2E tests
```

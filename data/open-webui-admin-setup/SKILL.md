---
name: open-webui-admin-setup
description: Create or reset a custom admin account in Open WebUI by directly manipulating the Docker container's SQLite database.
---

# Open WebUI Admin Account Setup

When Open WebUI is running with authentication enabled but no default admin account exists (or you need to reset/create one), use this procedure to create an admin user by directly manipulating the SQLite database.

## When to use
- User asks to create a default admin account for Open WebUI
- Authentication is enabled but no account exists to log in
- Need to reset the admin password
- `WEBUI_AUTH=False` fails because existing users block the setting

## Prerequisites

- Open WebUI Docker container named `open-webui`
- Docker access to the container (`docker exec`)
- The database is at `/app/backend/data/webui.db` inside the container

## Steps

### 1. Check existing users
```bash
docker exec open-webui python3 -c "
import sqlite3
conn = sqlite3.connect('/app/backend/data/webui.db')
c = conn.cursor()
c.execute('SELECT * FROM auth')
print('Auth:', c.fetchall())
c.execute('SELECT id, name, email, role FROM user')
print('User:', c.fetchall())
conn.close()
"
```

### 2. Delete existing records (if any)
```bash
docker exec open-webui python3 -c "
import sqlite3
conn = sqlite3.connect('/app/backend/data/webui.db')
c = conn.cursor()
c.execute('DELETE FROM user')
c.execute('DELETE FROM auth')
conn.commit()
conn.close()
"
```

### 3. Create admin account with bcrypt password hash
Replace `EMAIL`, `PASSWORD`, and `NAME` with your desired values:
```bash
docker exec open-webui python3 -c "
import sqlite3, uuid, bcrypt, time
conn = sqlite3.connect('/app/backend/data/webui.db')
c = conn.cursor()
uid = str(uuid.uuid4())
email = 'EMAIL'
password = 'PASSWORD'
name = 'NAME'
hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
c.execute('''
    INSERT INTO user (id, name, email, role, profile_image_url, created_at, updated_at, last_active_at, username)
    VALUES (?, ?, ?, 'admin', '', ?, ?, ?, ?)
''', (uid, name, email, int(time.time()), int(time.time()), int(time.time()), email.split('@')[0]))
c.execute('INSERT INTO auth (id, email, password, active) VALUES (?, ?, ?, 1)',
    (uid, email, hashed.decode('utf-8')))
conn.commit()
conn.close()
"
```

### 4. Verify login
```bash
curl -s -X POST http://localhost:8080/api/v1/auths/signin \
  -H "Content-Type: application/json" \
  -d '{"email":"EMAIL","password":"PASSWORD"}' | python3 -c "import sys,json; d=json.loads(sys.stdin.read()); print('Success!' if 'id' in d else d)"
```

## Important Notes

- **Password hashing:** Must use `bcrypt.hashpw()` — NOT SHA256. Open WebUI expects bcrypt format (`$2b$12$...`).
- **Two tables required:** Both `user` (profile/role) and `auth` (credentials) tables must be populated with matching `id` values.
- **WEBUI_AUTH=False error:** If the API returns "You can't turn off authentication because there are existing users", you must clear both tables first (step 2), then restart the container.
- **Container restart:** If changes don't take effect immediately, run `docker restart open-webui`.
- **No sqlite3 binary:** The container doesn't have `sqlite3` installed — always use Python's built-in `sqlite3` module via `docker exec`.

## Troubleshooting

- **Login fails with "incorrect password":** Verify bcrypt hash was applied. Compare hash format against existing records in `auth` table — they should both start with `$2b$12$`.
- **`WEBUI_AUTH=False` doesn't work:** Existing user records block auth disable. Delete from both `user` and `auth` tables, restart container.
- **Database file not found:** Check volume mount. On the host it's typically `/var/lib/docker/volumes/open-webui/_data`, inside the container at `/app/backend/data/webui.db`.
- **Container won't start:** Check for leftover volume data with `docker volume inspect open-webui`. A completely fresh install (empty volume) allows `WEBUI_AUTH=False` to work without pre-creating an account.
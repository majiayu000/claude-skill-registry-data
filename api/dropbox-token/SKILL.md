---
name: dropbox-token
description: Keep Dropbox API scripts authenticated for good — the one-time OAuth flow that yields a refresh token, and the four-line refresh that mints a fresh access token at the top of every script. Use when a Dropbox API call fails with 401 / expired_access_token, before writing any script that reads or writes Dropbox files, or when an app key + secret alone "doesn't work".
compatibility: >-
  Python 3. Calls Dropbox's OAuth and token endpoints with the user's own app key, secret and refresh token.
metadata:
  network-hosts: "api.dropbox.com www.dropbox.com"
  network-purpose: "one-time OAuth authorisation and refresh-token exchange for a short-lived access token"
---

# Dropbox token, permanently

## The fact that costs a cycle

`client_credentials` (app key + app secret alone) gives an **app-level token only**. It cannot
read or write a user's files. File access needs a **user token** from the OAuth code flow, and
since Dropbox moved to short-lived tokens (4 hours), the only durable credential is the
**refresh token** that flow returns when you ask for `token_access_type=offline`.

## One-time setup

1. Create an app at dropbox.com/developers/apps (scoped access; tick the `files.*` scopes you
   need *before* authorising: scopes added later need a new refresh token).
2. Put `DROPBOX_APP_KEY` and `DROPBOX_APP_SECRET` in your `.env`.
3. From that directory: `python3 scripts/dropbox_auth.py`. It opens the authorise page, you
   click Allow, paste the code back, and it writes `DROPBOX_REFRESH_TOKEN` into `.env`.
   The refresh token does not expire unless revoked.

## Every script: mint an access token at the top

```python
import json, os, urllib.parse, urllib.request

def get_dropbox_token() -> str:
    data = urllib.parse.urlencode({
        "grant_type":    "refresh_token",
        "refresh_token": os.environ["DROPBOX_REFRESH_TOKEN"],
        "client_id":     os.environ["DROPBOX_APP_KEY"],
        "client_secret": os.environ["DROPBOX_APP_SECRET"],
    }).encode()
    req = urllib.request.Request("https://api.dropbox.com/oauth2/token", data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded"})
    with urllib.request.urlopen(req, timeout=10) as r:
        return json.loads(r.read())["access_token"]
```

The token lasts 4 hours, so mint one per run; there is nothing to cache.

## `.env` keys

| Key | Purpose |
|---|---|
| `DROPBOX_APP_KEY` | from the app console |
| `DROPBOX_APP_SECRET` | from the app console |
| `DROPBOX_REFRESH_TOKEN` | written by `dropbox_auth.py`; long-lived |
| `DROPBOX` | the last short-lived access token (written for convenience; never rely on it) |

## Common mistakes

| Symptom | Cause | Fix |
|---|---|---|
| 401 `expired_access_token` hours after it worked | a pasted access token from the console | use the refresh flow above |
| `missing_scope` | scope ticked after the refresh token was issued | re-run `dropbox_auth.py` |
| works for app folder, not the user's files | app created with "App folder" access | create a "Full Dropbox" app if you need everything |
| a synced local file reads 0 bytes | it is an online-only placeholder | download it through the API instead of trusting the local path |

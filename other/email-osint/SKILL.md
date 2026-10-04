---
name: email-osint
description: Pivot an email or username to identity and accounts.
version: 1.0.0
tags: [osint, email, gravatar, username-enumeration, reconnaissance]
---

# Email & Username OSINT

Pivot from a single email address (or username) to real-world identity: full name, avatar photo, linked accounts across platforms. All checks are curl-based, no API keys required for the core workflow.

## When to use
- User gives an email and wants to know what identity/accounts are attached to it
- User gives a username and wants a platform sweep
- Verifying whether an account exists on a specific platform

## Procedure

### 1. Gravatar first — highest-yield pivot
Most people don't know WordPress/Gravatar auto-creates a public profile from their email. One email → name + username + photo:

```bash
HASH=$(echo -n "target@example.com" | md5sum | cut -d' ' -f1)
# Profile JSON (404 = no account, 200 = account exists)
curl -s "https://www.gravatar.com/$HASH.json"
# Full vCard (name, URLs, timezone, base64 photo)
curl -s "https://www.gravatar.com/$HASH.vcf"
# Avatar image
curl -s "https://www.gravatar.com/avatar/$HASH?s=200" -o avatar.jpg
```

Run this BEFORE anything else. If it hits, you get the target's name and probable username for free — that username drives every later step. Also try the SHA256 hash of the email (newer Gravatar accounts).

### 2. Derive the username, then sweep platforms
The local part of the email is usually the username everywhere. Check each platform with curl, but see the verification pitfall below before trusting any result:

```bash
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
for url in \
  "https://api.github.com/users/USER" \
  "https://gitlab.com/api/v4/users?username=USER" \
  "https://www.pinterest.com/USER" \
  "https://steamcommunity.com/id/USER" \
  "https://www.youtube.com/@USER" \
  "https://dev.to/USER" "https://replit.com/@USER" \
  "https://huggingface.co/USER" "https://www.chess.com/member/USER"; do
  code=$(curl -sL -A "$UA" -o /tmp/page.html -w '%{http_code}' "$url")
  echo "$code $url"
done
```

Platform-specific notes, decision table, and verification grep patterns: see `references/platform-verification.md`.

### 3. Pivot on partial names
Gravatar/display names often carry a middle name fragment the username doesn't (e.g. full name "Hariz Fauzil Adhim" → username "harizadhim760" → middle fragment "adhim"). Use name fragments as alternate search keys for platforms where the primary username missed.

### 4. Cross-confirm hits
A hit is only confirmed when two independent signals agree. GitLab is the strongest cross-check: its API returns `avatar_url` pointing at `secure.gravatar.com/avatar/<sha256-of-email>` — if that hash matches the original email's hash, the account is provably tied to that email.

### 5. Report format
Present results in three buckets — CONFIRMED (verified page content), NOT FOUND (verified absent), INCONCLUSIVE (login wall / bot-blocked — say so honestly, don't guess). For the user's own footprint, include the remediation pointer (gravatar.com profile deletion/privacy, platform privacy settings).

## Pitfalls

- **HTTP status codes lie.** Instagram, Twitch, Pinterest and others return 200 for nonexistent profiles. Never conclude "exists" from a status code alone — grep the page content for the profile name/title tag. See `references/platform-verification.md`.
- **Follow redirects** (`curl -L`). Platforms commonly 301 to www or regional hosts; judging the bare 301 as "gone" produces false negatives.
- **HIBP breach checks require a paid API key** — plain curl gets 401. Don't burn turns retrying; state it needs a key.
- **Reddit blocks scripted /about.json fetches.** Mark Reddit inconclusive rather than retrying without a browser session.
- Prefer no-auth JSON APIs (GitHub `api.github.com/users/X`, GitLab `gitlab.com/api/v4/users?username=X`) over HTML scraping — cleaner signal, no login wall.

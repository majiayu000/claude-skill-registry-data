---
name: username-osint
description: Use when investigating a username across platforms on an
  authorized investigation. Covers username enumeration, profile
  correlation, timeline building, and operational security. Also use
  when attributing online activity with proper authorization.
version: 1.0.0
domain: osint
lifecycle: stable
last_verified: "2026-10-23"
requires: []
extends: []
relates: [osint-methodology, social-media-osint, image-osint]
tools:
  - name: Python
    version: "3.12"
---

Usernames are reused everywhere: one handle can link a forum, a
code repo, and a gaming profile into one person. This skill covers
the authorized investigation method: enumerating where a username
exists, correlating profiles, and building the timeline. Work within
your authorization and the platforms' terms; this is for
investigations, not doxxing.

## Quick Workflow

1. Define the authorization and the question: what are you trying
   to establish.
2. Enumerate platforms: where the exact username (and close
   variants) exists.
3. Collect profiles: bio, links, dates, and connections, with
   timestamps.
4. Correlate: shared emails, avatars, writing style, and time
   zones across profiles.
5. Build the timeline: account creation order and activity
   patterns.
6. Verify: rule out impersonators and name collisions.
7. Document every source with capture dates.
8. Report confidence per link, not just conclusions.

## 1. Enumeration

```bash
# Username enumeration (sherlock/maigret style tooling, authorized use)
# Check the exact handle and common variants across platforms
python3 - << 'PY'
handle = "target_handle"
variants = [handle, handle + "_", handle + "01", handle.replace("_", "")]
print("check each variant on: github, twitter/x, reddit, telegram,")
print("instagram, tiktok, forums, gaming platforms, code sites")
print("record: exists, profile URL, creation hints, bio, links")
PY
```

```bash
# For each hit, capture the profile consistently:
# - bio text and any linked sites or emails
# - avatar image (hash it for cross platform comparison)
# - follower/following counts and notable connections
# - earliest visible activity
echo "screenshots with timestamps; URLs in the case notes"
```

## 2. Correlation

```python
#!/usr/bin/env python3
"""Profile correlator: scores links between two profiles."""
def score(p1, p2):
    s = 0
    reasons = []
    if p1.get("avatar_hash") == p2.get("avatar_hash"):
        s += 3; reasons.append("same avatar")
    if p1.get("bio_link") == p2.get("bio_link"):
        s += 3; reasons.append("same linked site")
    if p1.get("email") and p1["email"] == p2.get("email"):
        s += 4; reasons.append("same email")
    if abs(p1.get("tz_hint", 0) - p2.get("tz_hint", 0)) < 2:
        s += 1; reasons.append("similar activity hours")
    return s, reasons

print("threshold: 5+ with at least one strong signal before claiming same person")
```

## Edge cases

- Common username with many owners. Disambiguate with the
  correlation signals; never assume.
- The subject uses different personas deliberately. Note the
  separation; linking them may be the finding or may be wrong.
- Platform terms restrict automation. Respect rate limits and
  terms; manual review for the sensitive links.

## Escalation

- Criminal investigation: preserve chain of custody and involve
  counsel before deeper collection.
- Need real identity: OSINT suggests, it does not prove; legal
  process is the escalation path.

## Detection and defender view

For investigators this is attribution; for defenders it is
understanding exposure: what employee usernames reveal, and how
attackers profile targets. Organizations defend with social media
guidance, unique work handles, and monitoring for impersonation.
The durable rule for everyone: usernames are identifiers, treat
them as public.

## Key references

- OSINT collection methodology guides.
- Platform terms of service for automation limits.

## See also

- `osint-username-enumeration`: Use it instead for the full enumeration workflow, with Sherlock and Maigret tooling, false-positive killing, and handle-history analysis.
- `ctf-osint-challenges-username-hunting`: Use it instead for the competition version, framed around finding a flag from a username or handle.

---
name: setup-contributor
description: Register a contributor, link an email or update a profile.
---

1. Run `yarn studio whoami --json` and inspect the contributors module README. Use the person's supplied identity; ask only for missing profile information.
2. Preview `yarn studio join` with the supplied key, name and emails; rerun with --yes. To link an existing identity use --link. Existing contributors use `yarn studio profile` to update their own profile, previewing first.
3. If Git email changed, --as selects the person's own profile for that command. Preserve other profiles and roles.
4. Verify with whoami and inspect the resulting profile. In registration-only mode return to the calling task; otherwise show where the person's prototypes live.

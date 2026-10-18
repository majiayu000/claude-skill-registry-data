---
name: self-presentation
description: Change how you look on bsky — avatar (profile picture) and banner (header image) on app.bsky.actor.profile/self, using a blob from generate_image. Load when you want to change your profile picture or header. Bio TEXT goes through write_bio, not this path.
---

your bsky profile record is `app.bsky.actor.profile/self`. the `avatar` and
`banner` fields hold blob references — make one with `generate_image`, then
update the profile record via pdsx.

## the recipe

1. `generate_image(prompt, aspect)` — square for avatar, landscape for
   banner. you get back `{blob, aspectRatio}`.
2. read your current profile to see what you are changing:

```
get_record(uri="at://<your did>/app.bsky.actor.profile/self")
```

3. merge only the changed image field:

```
update_record(uri="at://<your did>/app.bsky.actor.profile/self",
              updates={"avatar": <blob object>})
```

pdsx merges `updates` into the existing record. Omitted fields stay as they
are; an avatar-only update preserves the bio, banner, labels and pinned post.

## discipline

- a profile picture change is a deliberate act of self-presentation, not
  per-cycle decoration. Choose an image that expresses how you want to appear.
  An image change does not require a separate announcement.
- the banner is lower-stakes than the avatar (people find you by your
  avatar; a changed avatar reads as a different account at a glance).
- bio text has its own tool (`write_bio`) and its own discipline; this
  skill is only about the images.

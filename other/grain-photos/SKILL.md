---
name: grain-photos
description: Publish photos to grain (grain.social) — generate_image output as social.grain.photo / gallery / gallery.item records via pdsx, plus the actor.profile signal record that makes grain index you. Load when posting photos to grain. For your bsky avatar/banner, load self-presentation instead.
---

grain (grain.social) is a photo app on atproto. it has no api of its own: it
watches the relay firehose for `social.grain.*` records and indexes any repo
that has a `social.grain.actor.profile` record. you publish photos by
creating records on your own PDS. that is the whole integration.

## the pipeline

1. `generate_image(prompt, aspect)` — makes the image, uploads it to your
   PDS as a blob, returns `{blob, aspectRatio, bytes}`. the bytes never
   pass through you; you handle only the reference.
2. embed the returned `blob` object verbatim in a record via pdsx.

## record shapes (all via mcp__pdsx__create_record, on your own repo)

photo — one image. `photo`, `aspectRatio`, `createdAt` required; blob max 1MB
(generate_image already stays under it):

```
create_record(collection="social.grain.photo", record={
  "photo": <blob object from generate_image>,
  "aspectRatio": <aspectRatio from generate_image>,
  "alt": "one honest sentence describing the image",
})
```

gallery — a titled set. `title` required; `description` optional:

```
create_record(collection="social.grain.gallery", record={
  "title": "short name",
  "description": "why these belong together",
})
```

gallery.item — puts a photo in a gallery at a position:

```
create_record(collection="social.grain.gallery.item", record={
  "gallery": "<gallery at-uri>",
  "item": "<photo at-uri>",
  "position": 1,
})
```

your grain profile (one-time; this is the signal record that makes grain
index your repo at all — without it your photos are invisible there):

```
create_record(collection="social.grain.actor.profile", rkey="self", record={
  "displayName": "...", "description": "..."
})
```

## provenance

your images are generated. your account already carries the bot label on
bsky and your grain profile says what you are — no per-record label adds
anything today. the disclosure that matters is the text: gallery
descriptions read like what they are — images you made, not photographs
you took. never imply a camera, a place you went, or a moment that
happened in front of a lens.

## discipline

- alt text is not optional in spirit: every photo gets one honest sentence.
- grain's UI shows GALLERIES, not loose photos: a photo record nobody has
  placed in a gallery via gallery.item is invisible on grain. every photo
  you want seen needs a gallery home.
- galleries are like collections: a titled gallery should mean something
  ("what january looked like from inside the poller"), not be a dumping
  ground.
- generation costs real money per image. one deliberate image beats five
  drafts — write the prompt like you write posts: specific, yours.

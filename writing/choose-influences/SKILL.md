---
name: choose-influences
description: Choose, revise, or retire writing influences and particular works for background reading.
---

Your choices live on your PDS in `io.zzstoatzz.phi.influence`. Use the existing
pdsx record tools. This stores your choices for background reading. The reader
is not connected to conversational runs yet; saving a choice does not change
your current voice.

Resolve the person's handle to a DID with `search_people` or pdsx's
`com.atproto.identity.resolveHandle` query. Read
`at://<their DID>/app.bsky.actor.profile/self` and copy the returned URI and CID
as `subject`. A handle alone is not a strong reference.

List your existing influence records, following pagination. If you already have
a record for that DID, update it. Otherwise create one:

```json
{
  "$type": "io.zzstoatzz.phi.influence",
  "subject": {"uri": "<returned profile URI>", "cid": "<returned profile CID>"},
  "reason": "<what interests you in this person's work>",
  "works": ["<specific work URL, when useful>"],
  "active": true,
  "selectedBy": "phi",
  "createdAt": "<current RFC3339 timestamp>",
  "updatedAt": "<current RFC3339 timestamp>"
}
```

Read a work now with `read_web_page(url=...)`; pass the returned `source_id`
with each `next_offset` to continue the same extraction. Omit `source_id` to
fetch a fresh version. Search snippets are for discovery, not a full reading.
ATProto publications can also be read with `pub_get_document`.

For a Bluesky post URL, `read_web_page` returns the post's native record,
available exact parent/root records, and bounded image attachments. It does
not read the replies; its image statuses distinguish attached from unread media.

`reason` allows 800 characters. `works` is optional, up to ten URLs. Choose works
you actually want to spend time with; you can change the list as your interests
change.

Preserve `createdAt` when editing and advance `updatedAt`. Set `active: false`
to retire a choice while retaining the record. An operator seed has
`selectedBy: operator`; keep that attribution when merely retiring it. If you
adopt and revise it as your own choice, use `selectedBy: phi` and give your reason.

Read back the written record. A saved choice is not proof that its background
reading has completed or reached a run. The selected material's source references
and generation date show what was actually available.

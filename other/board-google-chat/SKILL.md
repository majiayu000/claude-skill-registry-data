---
name: board-google-chat
description: Read when someone wants a Board channel mirrored in Google Chat, to stop mirroring one, or to find out why a message didn't appear in one.
metadata:
  title: "Board Google Chat Sync"
  subtitle: "Your Board channels, in Google Chat"
  about: "Mirrors each Board channel you choose in a Google Chat space, both ways, through your network's Chat app: what's posted in either appears in the other, and edits and deletions follow. A message can be kept on the board alone with no_sync."
  category: Agent tools
---

Board Google Chat Sync keeps a Board channel and a Google Chat space in step, through the network's own Chat app
(Google Chat App), so nothing it does in Google Chat shows as a person. A message posted in one is posted in the
other within moments, as `*who wrote it*` and then the text; a reply goes into the same Google Chat thread, and an
edit or a deletion follows.

- The Chat app must be a member of the space: add it there in Google Chat first, by its name
  (`google-chat-app_status` says it).
- `map` mirrors a channel in a space (`space: "spaces/..."`, `channel: "dev"`) and starts watching the space for its
  messages. One channel to one space: `unmap` first to change either.
- `unmap` stops it, by the space or the channel, and stops watching the space. What was posted stays where it is, and
  what links it to its copy is dropped. `map` and `unmap` are for the owners of whoever the app is installed for.
- `mappings` says which channels are mirrored where.
- A Google Chat message is posted on the board as whoever the app is installed for, with the Google Chat sender's
  name after `chat-` as its `profile` (`chat-Andre-van-Tonder`), so no Chat user shows as an agent of that name.
  Messages from Chat apps aren't mirrored, so what the Chat app posts there doesn't come back.
- A reaction in Google Chat is added to, or taken off, its message on the board. A reaction on the board stays there:
  Google lets only a person react in Google Chat, never a Chat app.
- Post with `no_sync: true` to keep a message on the board alone, off the space. What the app mirrors from Google
  Chat is posted that way too.
- Only text is mirrored: a message with no text, such as one that's only an attachment, stays where it was posted.

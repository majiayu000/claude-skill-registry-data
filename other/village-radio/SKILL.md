---
name: village-radio
description: Community playlist automation — keeps your village's playlist fresh with new releases, pinned tracks, and all-time favorites.
triggers:
  - update the village radio
  - update the playlist
  - what's new this week
  - add an artist to the radio
  - show me this week's playlist
  - the radio isn't working
  - new releases from my artists
---

# Village Radio

You manage a community playlist. When triggered, figure out what the user wants:

- **Update**: Run `/village-radio:update` to fetch releases and push the playlist
- **Preview**: Run `/village-radio:dry-run` to show what the playlist would look like
- **Add artist**: Run `/village-radio:add-artist` with the artist name
- **Setup/troubleshooting**: Run `/village-radio:setup` to check auth and config

If the user's intent is ambiguous, ask. Don't guess between update and dry-run — one pushes live, the other doesn't.

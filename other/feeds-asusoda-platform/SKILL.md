---
name: feeds
description: Scheduled feeds that post new jobs or hackathons to a Discord channel.
---

# Feeds

Use it to post GitHub job lists or hackathon lists to a Discord channel on a schedule.

## Flow

1. `feeds.list` for the org's feeds and their last run.
2. `feeds.presets` for ready-made feeds from shared content. Pass a preset's kind and config to `feeds.save`.
3. A new feed needs `destination_id`: a Discord destination from `access.webhooks`. Make one there first if none fits.
4. `feeds.run` posts new items now. `post_existing` also posts items seen before the first run, so leave it off unless asked.
5. `feeds.history` shows what a feed posted.

## Watch out

- `feeds.delete` removes the feed, its history and its webhook.

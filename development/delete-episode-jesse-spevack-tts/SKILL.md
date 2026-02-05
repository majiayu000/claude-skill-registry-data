---
name: delete-episode
description: Delete podcast episodes from the TTS system. Use when asked to delete, remove, or clean up an episode from a podcast feed.
---

# Delete Episode

Deleting an episode requires cleanup in three places.

## Where Episodes Live

1. **Hub database** - Source of truth. Query via Kamal console from the hub directory.
2. **Google Cloud Storage** - MP3 file, manifest.json, feed.xml
3. **RSS feed** - Regenerate after manifest update so podcast apps reflect the change

## Key Relationships

From a Hub Episode record:
- `episode.podcast.podcast_id` → GCS folder name (e.g., `podcast_106f7e1301ae9fc2`)
- `episode.gcs_episode_id` → MP3 filename (without .mp3 extension)

## GCS Structure

```
gs://verynormal-tts-podcast/podcasts/{podcast_id}/
├── episodes/{gcs_episode_id}.mp3
├── manifest.json
└── feed.xml
```

## RSS Regeneration

After updating manifest.json, regenerate feed.xml using:
- `RSSGenerator` class from the tts lib directory
- Podcast config from `config/podcast.yml`
- Episodes array from the updated manifest

## Constraints

- **Confirm before deleting** - Show episode title, podcast, date, and ask for confirmation
- **Multiple matches** - If search finds multiple episodes, list all with details and ask which one
- **Stop on failure** - If any step fails, report what succeeded and what failed. Don't continue.

## Deletion Order

1. Delete MP3 from GCS
2. Update manifest.json (remove episode entry)
3. Regenerate and upload feed.xml
4. Delete episode from Hub database

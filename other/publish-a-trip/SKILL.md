---
name: publish-a-trip
description: Publish or republish a trip's public web page with just publish — the final-pass render of data.json, live.json, and privacy-safe photos to the blog bucket.
---
# Publish a trip

The final-pass publish rebuilds one trip's page from scratch: load the trip from
the graph (S3 archive as fallback), apply privacy zones fresh from DynamoDB,
strip photo EXIF via re-encode, and overwrite `trips/<tripId>/` in the blog
bucket. Republishing (e.g. after adding a privacy zone) is the same command.

## Read first
- services/publisher/README.md — the five publish steps, the output contract, "What friends never see", and Known issues.
- tools/README.md — "publish" section; env is also documented at the top of tools/src/publish.ts.

## Commands
```bash
just publish --trip <tripId>                  # graph primary, archive fallback
just publish --trip <tripId> --from-archive   # skip the graph entirely
```
Env: `WOS_WEB_BUCKET`, `WOS_ASSETS_BUCKET`, `WOS_ZONES_TABLE` (required); `WOS_GRAPH_URI`/`WOS_GRAPH_USER`/`WOS_GRAPH_PASSWORD` (graph source; `WOS_NEPTUNE_ENDPOINT` in Neptune mode) and/or `WOS_ARCHIVE_BUCKET` (fallback source); `WOS_WEB_URL` to print the public URL. AWS credentials required.
Result: `https://travel.michaelwheeler.ai/?trip=trips/<tripId>` (the viewer selects trips by query parameter).

## Gotchas
- Known issue (Blog tab): no per-trip `index.html` is written, so `<blog>/trips/<id>/` — the URL the iOS app's Blog tab builds — returns raw S3 error XML. The viewer really lives at `/?trip=trips/<id>`. Fix is undecided (app URL vs CloudFront error response vs per-trip index).
- Publishing refuses to start without `WOS_ZONES_TABLE` — the scrub is mandatory, and zones are re-read fresh every publish so new zones retroactively scrub old points.
- A trip with zero publishable events throws rather than writing an empty page; only whitelisted types publish (`note`, `photo`, `audio`, `workout`, `bot_reply`, and trip markers — never location ticks, video, or `llm_exchange`).
- `--from-archive` works with the graph paused — publishing never requires the graph to be up.
- Integration-tested, but no real trip has been published in production yet.

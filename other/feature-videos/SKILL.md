---
name: feature-videos
description: Record and encode the website features page's short video loops from the Fixtures apps (iPhone, Android phone and TV, Mac), with the stutter rules. Use when re-recording, adding or encoding a feature clip.
---

# Feature videos

The features page's slots play short silent loops recorded from the Fixtures apps (made-up shows, and こうしす！ #3.1, CC BY 4.0, in the player, credited on the page). To record them again, one command per platform, from the repo root:

```
website/scripts/videos/record.sh iphone          # Simulator "kaeri-video-iPhone", headless
website/scripts/videos/record.sh android         # emulator "kaeri-video-phone", port 5570
website/scripts/videos/record.sh tv              # emulator "kaeri-video-tv", port 5572
website/scripts/videos/record.sh mac             # films the screen: only when the maintainer says the Mac is free
```

Name clips to record only those (`record.sh iphone iphone-search`); `iphone-player` is recorded only when named, since the player slot keeps its drag comparison. `KAERI_VIDEO_BUILT=1` reuses the last build and `KAERI_VIDEO_KEEP=1` leaves the device running. The flows live beside each platform's Fixtures UI tests: `apple/VideoFlows/FeatureVideoFlows.swift`, `android/app/src/androidTestFixtures/.../video/FeatureVideoFlows.kt` and the TV's twin. Each prints `KAERI_VIDEO start|end <epoch>` around the task; raw recordings land in `website/.videos` (ignored), and `bun scripts/feature-videos.ts .videos [clip…]` encodes again without recording: AV1 WebM plus H.264 MP4 and an AVIF/WebP poster in `public/features`, about 1 MB each, listed in `src/data/videos.json`. A new clip needs an entry in `CLIPS` there and a `FeatureVideo` in the page's slot, which shows the slot's still until the clip exists. The Mac recording needs the screen awake and unlocked, Focus on, Screen Recording allowed for the terminal and Automation Mode on (see `scripts/videos/apple.sh`).

Every clip must play without a stutter. The encode snaps each recording's frames to the 60 Hz grid, takes the 30 fps cut on whichever phase keeps the motion whole (24 fps for `tv-resume`, where the episode keeps its own frames), and fails a clip in which any frame repeats the one before while its neighbours move; `bun scripts/videos/judder.ts <video…>` runs the same check by hand. On Android the flows run against the Fixtures flavour's `video` build (debug's key, not debuggable, compiled ahead of time on install), on an emulator drawing with the Mac's GPU, once unfilmed before the take, and `android.sh` waits until the Mac is quiet (nothing but the emulator using more than a quarter of its cores) and films a take again when the Mac got busy during it, as when a Simulator boots. A clip turned down for a stutter or a dropped episode frame is recorded again once the Mac is quiet. Wherever the screen stands still the encode keeps one frame in three, so a flow holds 0.6 s after each step (0.2 s in the clip), and a pause inside a gesture lasts 0.3 s or more: a still of 130 to 200 ms between two motions comes out as one repeated frame, a stutter.


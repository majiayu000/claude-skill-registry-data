---
name: video-scrub-deck
description: Build or repair a guided or free-scroll video-scrub website deck with scrub-ready media, approved pause points, transitions, navigation, mobile behavior, and reverse-scroll QA.
---

# Video Scrub Deck

Read:

- `docs/cinematic-scroll-deck-playbook.md`
- `recipes/video-scrub-deck/README.md`
- `skills/video-asset-pipeline/SKILL.md`

## Decide the interaction

Use free scroll when exploration is part of the page.

Use guided Next and Previous controls when the sequence should feel presented and exact states matter.

## Production contract

- short clips
- frequent-keyframe or all-intra test exports
- approved pause points
- one source of truth for copy
- poster and reduced-motion state
- first clip warmed on intent
- later clips warmed near use
- byte-range delivery

## State rules

- the hero CTA targets the deck boundary
- opening copy is visible at the first approved state
- transitions read as transitions, not accidental flashes
- active media and copy remain synchronized
- reverse navigation restores prior states
- sticky evidence moves only after its source state
- generic scroll cues disappear when guided controls take over

## Verify

Inspect video `currentTime`, forward and reverse travel, first load, mobile fitting, failed media, reduced motion, and every guided pause point.

Do not patch one visible slide while sibling states share the same broken timeline function. Fix the shared state mapping.

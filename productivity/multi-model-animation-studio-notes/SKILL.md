---
name: multi-model-animation-studio-notes
description: Organize animation and manhwa/webtoon production notes across multiple AI models and reference sources. Use when extracting reference frames from recap videos or webtoon pages, planning scene packets, comparing model lanes, or preserving arc-level world continuity while allowing deliberate per-panel style shifts.
---

# Multi Model Animation Studio Notes

Use this skill to turn scattered research, prompts, frames, screenshots, and render feedback into structured production notes that survive handoffs between tools, agents, and sessions.

This skill is story-first. It is not for forcing a single frozen art style across every panel.

## Use When

Trigger this skill when the work involves any of the following:

- extracting reference frames from YouTube recap videos or screenshots from manhwa/webtoon pages
- breaking a scene into reusable visual beats, narration notes, and prompt-ready style cues
- combining notes from GPT, Claude, image generators, video generators, editors, or browser research lanes
- comparing outputs from different model lanes for the same shot or scene
- locking what must stay stable for an arc while allowing deliberate style changes for comedy, emphasis, flashback, memory, or dramatic compression
- preparing a handoff packet so another person or agent can continue production without re-discovering prior decisions

## Creative Rule

Consistency is not uniformity.

Keep the world grounded per arc:

- environments
- architecture
- location geography
- prop logic
- core costume anchors
- lighting logic
- mood palette

Allow character rendering and panel finish to shift on purpose when the story benefits:

- chibi for comedy or emotional puncture
- painterly for awe, grief, or mythic scale
- sketch-like for memory, speed, or instability
- exaggerated expression panels for reaction beats

The skill should preserve `world continuity` while tracking `panel effect overrides`.

## Core Workflow

1. Capture the project frame.
- Record the title, target platform, duration, aspect ratio, audience, and delivery goal.
- Note whether the output is a recap video, vertical scroll episode, teaser, animatic, or reference packet.

2. Collect source references.
- For videos, sample frames around the target scene and record timestamps.
- For webtoon pages, capture representative panels and record chapter/page identifiers.
- Keep the source URL or source title with every extracted reference.

3. Split `Arc Locks` from `Panel Flex`.
- `Arc Locks` are the details that should remain stable across the arc.
- `Panel Flex` is where deliberate style variation is allowed.
- Never let a temporary panel gag rewrite the world model.

4. Break work into scene packets.
- Treat each scene or shot as a separate note unit.
- Give each unit a stable ID such as `scene-03-shot-02`.
- Record the narrative purpose before describing visuals.

5. Separate model lanes.
- Keep prompts, settings, and results grouped by model or tool.
- Do not merge outputs from different systems into one unlabeled note block.
- Preserve seeds, reference-image usage, timing values, and key generation parameters when available.

6. Build the narration lane.
- Treat on-screen recap subtitles as a narration source, not automatically as character dialogue.
- Capture the text beat, tone, and timing.
- Mark what should become TTS narration, what should stay visual text, and what should remain silent.

7. Record decisions explicitly.
- Mark outputs as `approved`, `candidate`, `rejected`, or `needs-revision`.
- When something becomes canon, note why it was selected and what it replaces.
- Keep rejected variants briefly documented so the same failed branch is not retried blindly.

8. Emit a handoff-ready summary.
- End with the current best version, open questions, blockers, and next actions.
- Keep the final packet short enough that another lane can resume work quickly.

## Arc Locks vs Panel Flex

Use these categories every time the task involves manhwa/webtoon work.

### Arc Locks

These should usually remain stable inside the same arc:

- room layout and environment identity
- architecture and worldbuilding cues
- recurring prop placement and costume anchors
- faction colors, emblem usage, and magic/world rules
- baseline body proportions and recognizable character features

### Panel Flex

These can change deliberately when the story calls for it:

- chibi reaction panels
- comedic face distortion
- painterly splash treatment
- sketch-memory treatment
- speed-line or impact-frame exaggeration
- selective detail spikes on key dramatic panels

If a style shift is used, note the purpose. Do not treat it as random variance.

## Reference Extraction Checklist

For each useful frame or panel, record:

- source URL or title
- timestamp, chapter, or page ID
- shot type: wide, medium, close-up, insert, reaction, reveal
- characters present and pose logic
- environment anchor
- text overlay, subtitle, SFX, or narration present on screen
- palette and lighting notes
- emotional function of the image
- reusable style tags

The goal is not to copy the image. The goal is to extract techniques that can be reused legally and intentionally.

## Scene Packet Template

Use this template when turning rough notes into a durable production packet:

```md
## scene-01-shot-03

- Story Beat: What the audience should understand or feel here
- Purpose: Why this shot exists in the sequence
- Duration: Estimated seconds or beats
- Camera: Framing, motion, lens feel, angle
- Action: What visibly changes in the shot
- Narration/Text: Recap subtitle, dialogue, SFX, or silence
- Source References: Timestamps, panel IDs, or URLs that informed the shot
- Arc Locks: Environment and canon details that must not drift
- Panel Flex: Any allowed style override and why it exists
- Model Lanes:
  - Planning lane: GPT/Claude reasoning, beat notes, prompt drafts
  - Image lane: Prompt, seed, reference inputs, best output
  - Video lane: Prompt, timing, camera instructions, best output
- Decision: approved | candidate | rejected | needs-revision
- Next Step: Exact follow-up action
```

Convert nested lists to the user or repo's preferred format if a project template already exists.

## What Makes A Recappable Manhwa Scene

Based on successful recap patterns, look for these signals:

- a clear story beat that can be summarized in one or two lines
- readable emotional expressions with deliberate exaggeration
- strong environment anchors so the world feels coherent
- a mix of close-up, mid-shot, and reveal framing
- on-screen narration or text that cleanly carries exposition
- repeatable costume and setting cues that survive compression into recap format
- a few high-detail cornerstone panels surrounded by simpler bridge panels

Do not chase maximum detail in every frame. Use detail as emphasis.

## Comparison Rules

- Compare models on concrete output traits: composition, emotional readability, facial stability, background fidelity, text overlay legibility, motion quality, and editability.
- Keep subjective reactions separate from production facts.
- If a model is strong only for ideation or only for final polish, say that directly.
- Prefer one canonical prompt per approved shot, with alternates kept as fallback notes rather than mixed into the main prompt.
- Judge style shifts by whether they improve the beat, not whether they look identical to nearby panels.

## Deliverables

A good output from this skill usually leaves behind one or more of these:

- a reference atlas with timestamps or panel IDs
- an arc-lock sheet for environments and canon anchors
- a scene-by-scene storyboard note packet
- a model comparison table with an explicit recommendation
- a narration strip that can feed custom TTS
- a short handoff note with approved assets and next render actions

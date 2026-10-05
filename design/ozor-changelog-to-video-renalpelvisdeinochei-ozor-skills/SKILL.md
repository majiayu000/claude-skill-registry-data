---
name: ozor-changelog-to-video
description: "Convert changelogs, release notes, and version updates into Ozor.ai video prompts. Use this skill whenever the user has a CHANGELOG.md, release notes, GitHub release, version bump summary, or any list of product changes and wants to turn them into a video. Trigger on phrases like 'video from my changelog', 'release notes video', 'make a video from this update', 'announce this release', 'version update video', 'what's new video', 'product update video', 'feature release video', or any request to transform a list of product changes into video format using Ozor."
---

# Ozor Changelog-to-Video Converter

Transform changelogs, release notes, and version updates into polished, ready-to-paste Ozor.ai video prompts. This skill reads structured change lists and produces scene-by-scene video prompts that announce updates in a visually compelling way.

## Supported Input Types

- **CHANGELOG.md** — standard Keep a Changelog format
- **GitHub Releases** — release descriptions with tags
- **Release notes** — bullet-pointed feature lists
- **Version summaries** — "What's New" style documents
- **Commit summaries** — grouped commit messages for a release
- **Jira/Linear release notes** — exported issue lists

## Workflow

### Phase 1 — Parse the Changelog

Read the changelog and extract:

1. **Version number** — the release tag (e.g., v2.4.0)
2. **Release date** — when it shipped
3. **Change categories** — group changes by type:
   - **New features** — entirely new capabilities
   - **Improvements** — enhancements to existing features
   - **Bug fixes** — resolved issues
   - **Breaking changes** — anything that requires user action
   - **Deprecations** — features being phased out
4. **Headline change** — the single most impactful or user-requested change
5. **Change count** — total number of changes (used for duration estimation)

### Phase 2 — Prioritize for Video

Not every changelog entry deserves a scene. Apply these rules:

**Always include:**
- The headline feature (biggest or most requested change)
- Any new feature that changes the user's workflow
- Breaking changes (users need to know)

**Include if space allows:**
- Significant improvements (performance, UX)
- Highly requested bug fixes

**Skip for video (mention in notes):**
- Minor bug fixes
- Internal refactors
- Dependency updates
- Documentation changes

**Scene budget by change count** (target ~1 scene per 3 seconds of video):
- 1–3 changes: 6–8 scenes (intro + 2–3 per change + summary + CTA)
- 4–7 changes: 10–15 scenes (intro + 2–3 per top change + summary + CTA)
- 8+ changes: 15–20 scenes (intro + 2–3 per top change + "and more" + CTA)

### Phase 3 — Structure the Video

Use this proven structure for release videos:

1. **Intro / Version Badge** — Show the product name and version number with a clean animation. Set the tone: "What's new in [Product] [Version]"
2. **Headline Feature (2–3 scenes)** — The biggest change gets multiple scenes with the most visual attention:
   - *Title / What it is* — Feature name as headline with a one-sentence hook.
   - *How it works / Visual* — Show the feature in action: a UI walkthrough, animation, or diagram.
   - *Impact / Benefit* — Why this matters to the user. Show the outcome or result.
3. **Additional Feature Scenes (2–3 scenes each)** — Each prioritized change gets its own mini-sequence:
   - *Title / What it is* — Feature name and brief description.
   - *Detail / Visual* — Show what changed visually: before/after, demo, or diagram.
   - *(Optional) Benefit* — A short scene reinforcing the value if the change is significant enough.
4. **Summary / "And More"** — If changes were deprioritized, add a scene listing them briefly: "Plus: [fix 1], [fix 2], [improvement 1]"
5. **CTA** — "Update now", "Try it today", or "Read the full release notes at [URL]"

### Phase 4 — Generate the Ozor Prompt

Output a complete, copy-pasteable prompt:

```
## Ozor Video Prompt

**Source:** [Product] [Version] changelog
**Video type:** Release notes / What's new
**Format:** 16:9 landscape
**Estimated duration:** [X] seconds
**Target audience:** [existing users / developers / team]

---

### Prompt (copy and paste into Ozor)

Create a [duration] release notes video for [Product] version [X.X].

[N] scenes:

(1) Version Badge — [Product] logo centered on [dark/light] background. Version number "[X.X]" appears with a subtle animation. Subtext: "[Release date] — [tagline or change count summary]".

(2) [Headline Feature Name] — Title card: feature name as bold headline. One-sentence hook: "[What this feature does in plain language]". [Visual: icon or graphic that represents the feature.]

(3) [Headline Feature Name] Detail — [Show the feature in action: UI walkthrough, screen recording style animation, or step-by-step diagram. Include exact on-screen text.]

(4) [Headline Feature Name] Impact — [Why this matters: show the outcome, time saved, or before/after comparison. On-screen text: "[Key benefit statement]".]

(5) [Feature 2 Name] — Title card: "[Feature name]" with one-line description. [Visual: icon, UI element, or metaphor.]

(6) [Feature 2 Name] Detail — [Visual demonstration of the feature: what it looks like in use, how it works, or a key screenshot-style frame. Include on-screen text.]

(7) [Feature 3 Name] — [Feature title + visual direction. For smaller features, a single scene combining title and demo is fine.]

[...continue for remaining features, 2–3 scenes per major feature, 1 scene for minor features...]

([N-1]) And More — Clean list of remaining changes: "[fix 1]", "[improvement 1]", "[fix 2]". Each appears with a check mark animation.

([N]) CTA — "[Update now / Try it today]" with [product URL]. Logo fade-out.

Style: [clean / modern / bold]. Background: [dark / light]. Accent color: [brand color].
Tone: [confident / excited / professional].
Audience: [who].

---

### Notes

- [Suggestions for assets to upload]
- [Changes that were deprioritized and could become a separate video]
- [Tips for iterating]
```

## Adaptation Rules

**If the changelog has only bug fixes:**
- Frame as a reliability/quality update
- Lead with "We listened" or "Squashed bugs" messaging
- Group fixes thematically rather than listing each one
- Keep it short: 3–4 scenes max

**If the changelog has a breaking change:**
- Call it out prominently — users need to see this
- Use a visual warning indicator (color shift, icon)
- Explain what changed AND what the user needs to do
- Place it in scene 2 (right after intro) for visibility

**If the changelog spans multiple versions:**
- Combine into a "quarterly update" or "year in review" format
- Group by theme rather than version number
- Lead with the most impactful changes across all versions

**If the changelog is from a GitHub Release:**
- Extract the release title as the video headline
- Use the tag name as the version badge
- Parse markdown formatting for bullet points and headers

## Quality Checklist

Before presenting the final prompt, verify:

- [ ] Version number is prominently displayed in scene 1
- [ ] The headline feature gets the most visual attention
- [ ] Breaking changes are clearly called out (if any)
- [ ] Each scene has exactly one change or idea
- [ ] On-screen text is short — feature names + one-line descriptions
- [ ] CTA tells the user exactly what to do
- [ ] No critical changes from the source were omitted without mention
- [ ] Deprioritized changes are listed in the Notes section

## Rules

1. **Every change that gets a scene must be visually described.** "Show the new dashboard" is not enough — describe what the dashboard looks like, what's animated, what text appears.
2. **Never invent features.** Every change must come from the source changelog.
3. **Prioritize user impact over technical impressiveness.** A small UX fix that users requested is more video-worthy than a large internal refactor.
4. **Keep it punchy.** Release videos should be 30–60 seconds. A 30-second video should have ~8–10 scenes; a 60-second video should have ~15–18 scenes (roughly 1 scene per 3 seconds). Users want highlights, not documentation.
5. **Version number must be visible.** It appears in scene 1 and optionally in a persistent badge.

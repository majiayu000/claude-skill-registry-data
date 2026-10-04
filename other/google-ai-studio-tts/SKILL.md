---
name: google-ai-studio-tts
description: Generate speech, podcasts, voiceovers, and multi-speaker dialogue with Google AI Studio's Gemini Flash TTS by driving the live web app in Chrome via the claude-in-chrome MCP server. Use whenever the user asks to (1) create a podcast, audiobook chapter, narration, audio drama, or voiceover with Gemini / Google AI Studio TTS; (2) turn a script into multi-speaker audio (e.g. "two-host podcast", "Speaker 1 / Speaker 2 dialogue", "Puck and Zephyr"); (3) tweak a TTS prompt with Scene, Sample Context, Director's note (Style/Pace/Accent), Audio Profile, voice picker, or Temperature; or (4) render audio with inline tags like [enthusiastic], [whispers], [laughs]. Triggers on phrases like "use AI Studio TTS", "generate this podcast in AI Studio", "render with gemini-3.1-flash-tts-preview", "speak this with Aoede/Puck/Zephyr", or any request for browser-driven Gemini speech generation.
---

# Google AI Studio TTS (browser-driven)

## Overview

This skill drives `https://aistudio.google.com/generate-speech` in the user's already-open Chrome (via the `claude-in-chrome` MCP tools) to render audio with Gemini Flash TTS. The user must already be signed in to Google AI Studio in Chrome — never create accounts, never enter passwords, never share credentials.

There are two input modes in the UI. Choose based on what the user asked for:

| User intent | Mode | Why |
|---|---|---|
| Single narrator, monologue, or short voiceover | **Text** | One textarea, fastest path. |
| Multi-speaker dialogue with simple `Speaker 1: …` lines | **Text** | Same single textarea — prefix lines with `Speaker 1:`, `Speaker 2:`. |
| Multi-speaker with per-line speaker chip, finer control, easy editing | **Composer** | One block per utterance, each with its own voice chip. |
| Anything where the user explicitly mentions "scene", "sample context", "director's note", or wants the speaker chips visible | **Composer** | Matches the visible UI elements they're referring to. |

Both modes share the **Scene** and **Sample Context** fields and the **Speaker settings** panel on the right.

## Required tools

Load these claude-in-chrome MCP tools via `ToolSearch` before starting:

```
select:mcp__claude-in-chrome__tabs_context_mcp,mcp__claude-in-chrome__tabs_create_mcp,mcp__claude-in-chrome__navigate,mcp__claude-in-chrome__find,mcp__claude-in-chrome__form_input,mcp__claude-in-chrome__javascript_tool,mcp__claude-in-chrome__computer
```

## End-to-end workflow

### 1. Open the page

```
tabs_context_mcp({ createIfEmpty: true })
navigate({ tabId, url: "https://aistudio.google.com/generate-speech?model=gemini-3.1-flash-tts-preview" })
```

If the URL shows a banner that the chosen model is unavailable and AI Studio auto-switched to another (e.g. `gemini-3.1-flash-tts-preview`), accept it — don't fight the redirect. Close the dismiss-banner ("X") with a click before continuing so it doesn't cover Run controls.

### 2. Pick the mode

The two toggle buttons live at the top right of the playground:

```js
// Switch to Composer
document.querySelectorAll('button.toggle-button').forEach(b => {
  if (b.innerText.trim().endsWith('Composer')) b.click();
});
// or for Text
document.querySelectorAll('button.toggle-button').forEach(b => {
  if (b.innerText.trim().endsWith('Text')) b.click();
});
```

The active toggle has class `ms-button-active`.

### 3. Fill the shared fields

Both modes share:

- **Scene** (sets the acoustic / situational frame): `textarea[aria-label="Scene"]`
- **Sample Context** (gives the model a tone reference): `textarea[aria-label="Sample Context"]`

These are Angular textareas. Plain `el.value = ...` will NOT trigger Angular's form binding — use the helper in [references/selectors.md](references/selectors.md), or prefer the `form_input` MCP tool with a ref obtained from `find`.

Leave these fields empty if the user did not provide a scene / sample context. They are optional.

### 4a. Fill input — Text mode

One textarea: `textarea[aria-label="Enter a prompt"]`.

Format conventions (these are not validated by the UI but are what the model is trained on):

- Single narrator: just write the text. Optionally prepend an inline tag, e.g. `[warm] Welcome to today's episode.`
- Multi-speaker: prefix each line with `Speaker 1:`, `Speaker 2:`, …

```
Speaker 1: [enthusiastic] Welcome back to the show!
Speaker 2: [agreement] Thanks, glad to be here.
```

See [references/audio-tags.md](references/audio-tags.md) for the inline-tag vocabulary.

### 4b. Fill input — Composer mode

Composer renders one **speech block** per utterance. Each block has:

- A speaker chip: `button.voice-chip.ms-button-filter-chip` (text reads `Speaker N - VoiceName`)
- A textarea: `textarea[aria-label="Speech block text"]`

To add a new block: click `button.add-speech-block-button`. The new block inherits the previous speaker by default.

To populate Composer from a script:

1. Make sure the existing blocks match what you need (delete extras with the per-block `×` button if necessary).
2. For each line in the script, ensure a block exists; click "add speech block" to create more.
3. Set the text of each block (`textarea[aria-label="Speech block text"]`, indexed in DOM order).
4. Set the speaker chip per block (see Step 5).

### 5. Choose voices

The right-hand **Speaker settings** panel shows one card per active speaker (Speaker 1, Speaker 2, …). Clicking a card opens the full voice picker drawer with 32 voices. See [references/voices.md](references/voices.md) for the full catalogue with their character traits.

Inside the voice picker drawer:

- **Audio Profile** — free text, e.g. "An authoritative main news anchor."
- **Director's note** — three dropdowns: Style (e.g. Vocal Smile), Pace (e.g. Rapid Fire), Accent (e.g. American (Gen)).
- **Voice** — searchable list. Click a voice to select it.

Close the drawer by clicking the `×` in its top-right when done. The active voice card on the playground has class `active-voice-card`.

In Composer mode each block's voice chip can be changed independently — clicking it opens a popover where you assign that block to Speaker 1, Speaker 2, … or add a new speaker.

### 6. (Optional) Adjust Temperature

Expand "Model settings" (right panel, above Speaker settings) to reveal Temperature. Range 0–2, default 1. The number input is `input.slider-number-input` near the label "Temperature". Higher = more variation in delivery. Only touch this if the user asked for it.

### 7. Run generation

Click `button.ctrl-enter-submits` (the "Run Ctrl ↵" button at the bottom right), or press `Ctrl+Enter` while focus is in the prompt area:

```js
document.querySelector('button.ctrl-enter-submits').click();
```

Generation usually takes 5–30 s depending on length. Poll for completion by checking the audio player's duration counter (the right-hand `0:00 / X:XX` increments once render is done) or by watching for the download icon to become enabled.

### 8. Hand off / download

Tell the user the audio is ready and point at the playback controls. Downloading is the user's choice — only click the download (cloud-arrow) icon if the user asked for a file.

## Style guidance for prompting

- Inline tags belong inside the speaker line, e.g. `Speaker 1: [whispers] don't tell anyone`. They do **not** stack across lines.
- Scene is for **acoustics + setting**, not the script. Bad: "Speaker 1 says hi". Good: "Quiet kitchen, morning light, minimal reverb."
- Sample Context is for **delivery tone**, e.g. "Podcast style, fast, slightly overlapping pacing, energetic and warm."
- For two-host podcasts, Puck (Upbeat / Middle pitch) + Zephyr (Bright / Higher pitch) is the AI Studio default and a safe baseline. See [references/voices.md](references/voices.md) for alternatives.

## What NOT to do

- Don't sign in, accept new ToS, or change account settings — those are off-limits.
- Don't download generated audio without an explicit user ask.
- Don't navigate away from the AI Studio tab while a render is in flight.
- Don't fabricate voice names — the catalogue is fixed at 32 (see references/voices.md). If the user asks for a voice not in the list, suggest the closest match.
- Don't `el.value = "…"` on Angular textareas without dispatching `input` and `change` events; the form will revert. Use the helper in references/selectors.md or `form_input`.

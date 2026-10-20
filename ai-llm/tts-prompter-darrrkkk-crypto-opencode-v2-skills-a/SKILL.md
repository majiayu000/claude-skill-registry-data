---
name: tts-prompter
description: "MUST read immediately before drafting a prompt for, selecting a voice for, or calling `manus-tools.generate_speech` — including narration, dubbing, and dialogue in video-editing tasks. Covers voice selection, prompt composition, timing, language guidance, and expressive delivery."
compatibility: opencode
---

# TTS Prompter

This skill provides the definitive framework for crafting high-quality Text-to-Speech (TTS) prompts. You MUST follow these guidelines when generating speech to ensure natural, expressive, and predictable audio output.

## 1. The Ultimate TTS Formula

To generate perfect audio, always construct your single input string using this formula:

**`{Language, Accent, and Situational Style Instructions}: {Emotionally Aligned Text (with local action tags only if needed)}`**

The most critical rule in TTS prompting is physically separating **"Director Instructions"** (how to speak) from the **"Script"** (what to say) using a colon (`:`).

**Core Alignment Rule:** The style instructions, the text content, and any tags should all point in the same direction. A scared-sounding instruction works best with text that actually sounds alarming.

### Multi-speaker Conversations

For dialogues, use the colon to separate the global instructions from the script, and also to separate speaker names from their lines:

```text
TTS the following conversation between Joe and Jane:
Joe: How's it going today Jane?
Jane: Not too bad, how about you?
```

## 2. Part 1: Style Instructions (Before the Colon)

The Style Instructions section is your primary tool for controlling the overall performance. **This part is NEVER spoken.**

**Mandatory Rule:** You MUST write the Style Instructions entirely in English, regardless of the target language being spoken. The model follows English instructions most reliably.

**Tip 1: Don't overspecify.** The model fills in gaps naturally. Leaving some room often produces more natural results than controlling every detail.

**Tip 2: Avoid naming real brands or real-person identities.** Phrasing like "Chanel-style" or "like a TikTok creator promoting her favorite brand" is the most common trigger of policy blocks. Describe the desired *style* in generic terms instead.

**Tip 3: Steer clear of sensitive content cues.** Prompts that touch on violence, sexual content, hate, self-harm, or illegal activities (per [Google's policy](https://policies.google.com/terms/generative-ai/use-policy)) can be silently blocked. Soften descriptors and remove explicit cues.

### 2.1 Controlling Language, Emotion, Tone & Accent

Provide a specific, situational description. Because the Style Instructions carry the highest weight in the model's generation logic, you MUST explicitly state the target language and accent here to ensure correct output.

If the Spoken Text contains a mix of languages (e.g., Japanese with English words), you MUST explicitly state this mixed-language requirement in the Style Instructions so the model knows to switch pronunciation rules dynamically.

*   ❌ **Weak:** `Speak in a scared way: I think someone is in the house.`
*   ✅ **Strong:** `You are hiding in a dark closet. Speak in English with a terrified, trembling whisper as if you are afraid of being caught: I think someone is in the house.`
*   **Language & Accent Example:** `Speak in Brazilian Portuguese with a standard São Paulo accent: Bem-vindo ao nosso programa de hoje.`
*   **Mixed Language Example:** `Speak in a mix of Japanese and English, with a professional and confident tone: 私たちの新しい製品は強力な AI capabilities を備えており、既存の workflow にシームレスに統合できます。`

*(Note: If you mention a conflicting language here, e.g., "Read as a Japanese boy" but the text is Portuguese, the model will output Japanese.)*

### 2.2 Emotion & Tone

To coax the model into making natural sounds without relying on tags, set up the prompt and provide "breath markers" in the text.
*   **Laughing:** `React to the text with an amused, genuine laugh before speaking: Hahaha, I did NOT expect that. Can you believe it!`
*   **Sighing:** `You are exhausted and frustrated. Start the sentence with a heavy, tired sigh: Oh man... I can't do this anymore.`

### 2.3 Pacing & Volume

Use the Style Instructions to force physical delivery changes:
*   **Pacing:** `Read this disclaimer extremely fast, like a radio commercial voiceover rushing through the terms and conditions: Availability and terms may vary. Check our website for details.`
*   **Volume:** `You are trying not to wake a sleeping baby. Whisper this entire sentence as quietly as possible: I think he finally fell asleep.`

## 3. Part 2: Spoken Text (After the Colon)

The Spoken Text contains the actual words to be synthesized. **This part IS spoken.**

**Mandatory Rule: Match the target language.** The Spoken Text MUST be written in the exact language(s) you want the model to speak. If you want Japanese, write in Japanese characters; if you want a mix of Japanese and English, write the text exactly as a mix of Japanese and English. Do not rely on the model to translate on the fly.

**Tip: Punctuation matters.** Commas, periods, and semicolons create natural pauses. Use them to help the model breathe.

### 3.1 Using Markup Tags

You may use **Markup Tags** (words enclosed in brackets like `[sigh]`) inside the Spoken Text to inject specific, localized actions or style modifications.

**Golden Rule: Tags for precision, instructions for tone.** Use tags inside the Spoken Text when you need a specific moment (a laugh, a pause, a whisper). Use the Style Instructions before the colon to set the overall feel.

*(Note: There is no exhaustive, hardcoded list of tags. The model interprets any descriptive word in brackets. However, you MUST follow the rules below.)*

#### DO Use Tags For:

Place these tags **inside the Spoken Text** (after the colon). They will not be read as words.

1.  **Non-speech sounds:** `[sigh]`, `[laughing]`, `[uhm]`, `[cough]`, `[gasp]`, `[snorts]`
    *   *Example:* `Say the following casually: Well, [uhm], let me think about it. [sigh] I guess we have no choice.`
2.  **Local style shifts:** `[shouting]`, `[whispering]`, `[extremely fast]`, `[sarcasm]`, `[asmr]`
    *   *Example:* `Narrate the following: He looked at me and said, [shouting] 'Get out!'`
3.  **Pacing and pauses:** `[short pause]` (~250ms), `[medium pause]` (~500ms), `[long pause]` (~1000ms+)
    *   *Example:* `Read this like a game show host: The winner is... [long pause] ...John!`

#### DO NOT Use Tags For:

**NEVER use emotional adjective tags** (e.g., `[scared]`, `[curious]`, `[bored]`, `[excitedly]`) inside the Spoken Text. 
*   *Why?* The TTS engine will literally read the word aloud (e.g., it will say the word "scared" before the sentence), ruining the audio.
*   *Solution:* Move emotional descriptions to the Style Instructions (before the colon).

## 4. Duration vs Faithfulness

TTS output duration is **not deterministic**: the model speaks at a rate it chooses, and you cannot tightly control physical seconds via prompt wording or rate tags.

- **Standalone TTS tasks with no explicit time limit** (the user just wants audio of a text): ignore duration concerns. Optimize for **reading the text fully and accurately** in the requested style.
- **Time-constrained tasks** (e.g., narration in `video-generator`, dubbing to a fixed clip, ad spots): consult the `Unit` and `Rate` columns in `references/language_catalog.md`, and follow the calling skill's rules for sizing text against the budget.

## 5. References: Voice & Language Selection

The `language_code` parameter acts only as an auxiliary hint to select the correct regional voice model (e.g., `en-US` vs `en-GB`). It does NOT force the output language.

**Resolve all reference paths below relative to this `SKILL.md` file.**

- Before selecting any `voice_name`, read `references/voice_catalog.md` for the complete catalog of 30 prebuilt voices, gender, and timbre.
- For time-constrained narration, dubbing, or advertising, read `references/language_catalog.md` for regional language codes and rate estimates.

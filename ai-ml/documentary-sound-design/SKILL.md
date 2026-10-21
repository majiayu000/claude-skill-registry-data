---
name: documentary-sound-design
description: >
  Principles and order of operations for sound post on a narrated documentary, radio documentary,
  podcast feature or archival film: audio-first ("radio cut") editing, the four-stem model
  (dialogue / live / music / ambience), the density ceiling, when to use silence, and which
  OpenDubStage skill and tool to open next. Use this whenever someone starts planning or auditing
  the sound of a documentary, a narrated stills film, an oral-history piece or a long-form podcast,
  asks "how should the sound of this be built", "what order do I do the mix in", "what are the
  rules for music / ambience / narration in a documentary", or wants an overview before the
  specific skills (dialogue-editing-and-restoration, voice-matching, music-under-narration,
  ambience-and-sound-for-stills, scene-transitions, mix-qc-and-delivery, ai-review-of-audio).
  Do NOT use for music production, game audio or live sound reinforcement.
---

# documentary-sound-design

The overview skill for the OpenDubStage set. It states the principles, the order of
operations and the numbers that every other skill shares, then points at the specialist
skill. Every rule has a number or a test; every number has a source or says "measured in
practice". Where a number here and a constant in the OpenDubStage code disagree, the code
wins and this file needs a line changed.

## Order of operations (audio first, then picture)

Hard-won: a late mix failure after a picture render cost hours. Picture is cut to a
finished, QC-passed soundtrack, never the other way round.

| # | Pass | What it produces | Gate before the next pass |
|---|---|---|---|
| 1 | Transcribe and select | word-timed transcript, paper edit | every passage is a whole sentence (see `dialogue-editing-and-restoration`) |
| 2 | Radio cut | dialogue + live sound + room tone on one timeline, no picture | it works as radio; length is decided here |
| 3 | Score pass | music cues with musical in/out points, `up` or `under` | `music-under-narration` budget and entry/exit checks |
| 4 | Ambience pass | a bed under every stretch; spots and textures for stills | bed coverage of [0, total] (see `ambience-and-sound-for-stills`) |
| 5 | Transitions | J/L cuts, music seams, ending ladder | `opendubstage transitions` + `check_transitions` clean |
| 6 | Mix | stems, gain envelopes, one linear gain, limiter | `opendubstage qc` exit 0 |
| 7 | QC listen | transcription check of every cut, model review, humans on 3 systems | `mix-qc-and-delivery`, `ai-review-of-audio` |
| 8 | Picture | stills and clips cut to the audio timeline | picture length = audio length ± 0.05 s |

Sources: the radio-cut practice (Creative COW, Billinge *The Practical Guide to Documentary
Editing*, 2017); Ken Burns records music before the edit and cuts to it (MasterClass, "The
Power of Music"); Randy Thom, "Designing a Movie for Sound" (FilmSound.org).

## The eighteen principles

| # | Rule | Test | Source |
|---|---|---|---|
| 1 | Audio first, then picture. | no picture render before `opendubstage qc` passes | Burns; Thom; measured in practice |
| 2 | Every narration cut is a whole sentence: in on a sentence start, out on a real full stop, air before and after, fade inside the air. | transcribe each cut out of the mix; head and tail match ≥ 0.5 | NPR Training checklist (Byers 2018); measured in practice |
| 3 | Never dead air. A bed runs under every narrated stretch about 15 LU under dialogue; designed silences are listed explicitly. | no span < −60 dBFS for > 3 s (strict: −50 / 2 s) outside the whitelist | Torcoli et al. AES 146 (2019) |
| 4 | Posts, not interludes. Music rises between lines for 2–12 s and drops before the next word. | music-only holds inside a narrated chapter ≤ 15 s | Menjivar (Transom 2015) |
| 5 | Music under at most half the narration; one song under ≤ 45 s of continuous speech, then it leaves on a phrase. | music-under minutes ÷ narration minutes ≤ 0.5 | Menjivar "as long without as with"; Dykstra on *20 Days in Mariupol* |
| 6 | Nothing sung under speech. | no `under` cue overlapping speech > 1 s whose section has vocals | NPR practice; measured in practice (model listener caught hidden vocals) |
| 7 | Duck by frequency as well as depth: ≥ 10 LU broadband plus a 1–4 kHz pocket; a 15–20 dB drop on every line is audible automation. | in-band music ≤ dialogue −10 dB (QC) / −14 dB (strict) while speech is active | Torcoli 2019; IRPR; ANSI S3.5 band importance |
| 8 | Music enters on the music and leaves on the music: downbeat or section start, never fading up from nothing, never in the 2 s before a first word; exits on a phrase end. | entry within 60 ms of a downbeat; exit via `phrase_safe_end` | Menjivar; measured in practice |
| 9 | Only sources visible on screen get a spot effect: ≤ 1 per still, off the cut, never under a key line. | `opendubstage foley check` | Kwok on *They Shall Not Grow Old* (Mix); Burns/Spiegel on *The War* |
| 10 | Remove events, not character: coughs and thumps go; laughs, sighs, sniffs, interjections and the room stay and hold the duck. | keep-spans count as speech for the envelope | LeBlanc on *Fire of Love*; Radio Diaries; *Finn and the Bell* |
| 11 | Match other voices down to the main recording, never the main recording up to the clean one. | LTAS deviation ≤ 3 dB 200 Hz–6.3 kHz | iZotope RX EQ Match practice; Podcast Engineering School (phone matching) |
| 12 | Anchor on dialogue, not programme: −24 LUFS dialogue-gated, one linear gain, a limiter as the only non-linear stage; LRA reported, not clamped. | dialogue −24 ± 1 LUFS; programme free | PRSS −24 ± 2; ATSC A/85; Netflix v1.5 (dialogue-anchored) |
| 13 | Clean lightly, blend, judge blind. Nothing generative on live sound; the cleaned noise floor stays within 6 dB of the raw floor. | blind A/B in both orders; WER on secondary speakers unchanged | Bergh on *Becoming Led Zeppelin* ("the best restoration is no restoration"); measured in practice |
| 14 | The witnesses sign off, on real systems: a TV, a laptop, a phone, headphones. | 60–90 s excerpts on each | Tavella on *The War* (six to eight systems); Mangini on *32 Sounds* (headphones) |
| 15 | Each song keeps its own weight: shift a cue by half its deviation from the playlist median, clamped ±2 LU. | `mx_up` spread 3–5 LU across the film | CAS 2026 (*Becoming Led Zeppelin*) |
| 16 | The ending is designed, not left over: last line, bed, true silence, then the credits song from its first note to its real end. | exactly one silence between last line and credits song | Third Coast (*Finn and the Bell*; *Time Bandit*) |
| 17 | Live music is not speech: no de-esser, compressor or voice EQ on a processional, a band or a dance; high-pass only. | rendered filter graph of music-live cues contains no dynamics | BAFTA Factual pattern; *Summer of Soul* (separate music mixer) |
| 18 | The recording is an object and the narrator locates herself: the listener knows within the first minute who is talking, where and when. | first narration cue (or its bridge) contains a self-locating phrase | Radio Diaries (Richman); *32 Sounds* |

## Stems and levels (relative to dialogue at −24 LUFS)

| Stem / layer | Per-cue target | Under speech | Source |
|---|---|---|---|
| DX narration, LIVE speech | −24 | anchor | PRSS, A/85 |
| MX up (in the clear) | −17 (−16 to −14 short-term) | no speech scheduled | measured in practice |
| MX under | −17 before envelope | −14 with carve (−17 without) | Torcoli ≥ 10 LU |
| AMB bed | −40 (−16 LU) | −43 (−3 duck) | Torcoli ≥ 15 LU |
| Texture | −36 (−12 LU) | | rule of thumb (Murch's 2½ layers) |
| Spot | −32 (−8 LU); hero −28 | | rule of thumb |
| Designed transition | −26 (−2 LU) | | rule of thumb |
| Room-tone floor | −46 | always | NPR room-tone practice |

Walter Murch, "Dense Clarity, Clear Density" (Transom Review 5(1), 2005): listeners follow
about two and a half simultaneous layers. Dialogue + bed leaves half a layer for music and
effects together. When you add a layer, take one away.

## Pacing numbers (rules of thumb unless cited)

- Pause inside a thought 1.5–3 s; between thoughts 5–10 s; between passages 12–25 s when the picture changes subject.
- Music in the clear ≥ 12–15 s at a chapter open (one or two phrases), ≥ 8 s mid-chapter, ≥ 10 s after a chapter's last line.
- Still holds 5–8 s, hero 8–12 s; documentary average shot length ≈ 11 s (Follows; Cinemetrics).
- Live moments play in full with 3–6 s of room before and after.
- Every act boundary is a breath: a sound bridge, 5–10 s of ambience or music alone, then the card.

## Which skill next

| Problem | Skill | OpenDubStage tool |
|---|---|---|
| cutting narration, coughs, rumble, neural cleanup | `dialogue-editing-and-restoration` | `opendubstage specrepair` (`opendubstage.restore`) |
| a TTS or cloned bridge, an off-mic second speaker, a phone caller | `voice-matching` | `opendubstage ltasmatch` (`opendubstage.match`) |
| spotting, ducking, posts, instrumentals, endings | `music-under-narration` | `opendubstage carve` (`opendubstage.mix.carve`) |
| beds, gap fill, spot effects for photographs | `ambience-and-sound-for-stills` | `opendubstage foley` (`opendubstage.foley`) |
| chapter joins, J/L cuts, music seams, the ending ladder | `scene-transitions` | `opendubstage transitions` (`opendubstage.mix.transitions`) |
| loudness, true peak, dead air, clicks, the cut check | `mix-qc-and-delivery` | `opendubstage qc` (`opendubstage.qc`) |
| using a multimodal model as a second pair of ears | `ai-review-of-audio` | (your own review script; schema in the skill) |

## What professionals flag first (in the order they hear it)

1. Ambience designed to be inaudible (−25 LU under dialogue): beds are the room the voice lives in, not a safety net against the silence detector.
2. Ducking by depth instead of frequency.
3. Music that fades up from nothing and runs as interludes.
4. Vocal songs under narration.
5. Narration cut with 0.12 / 0.30 s of air: tails need ≥ 0.45 s and the fade must end in air.
6. A frame-wise leveler (`dynaudnorm`, `speechnorm`) instead of a sentence-level ride.
7. Hard dips for coughs instead of spectral repair.
8. Cleaning the synthetic voice instead of dirtying it to the recording's bandwidth and room.
9. A −1.3 dBTP ceiling: AAC overshoots; limit for −2 dBTP.
10. Measuring the programme instead of the dialogue.

See `references/sources.md` for the full citation list shared by all eight skills.

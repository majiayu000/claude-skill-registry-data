---
name: read-aloud
description: Read assistant replies aloud using a qualified local host renderer when requested or enabled by a persistent accessibility preference. For LeeWay-owned Agent Lee Android surfaces, route prepared text and streaming phrases to canonical Agent Lee Voice One through LeeWay Voice Fabric, with cancellation, mute/resume, and evidence-bound host routing.
---

# Read Aloud

Use a qualified local speech renderer to make assistant messages accessible. On Windows use the bundled System.Speech helper. On a qualified Android secondary workstation use the LeeWay Read Aloud Bridge with Samsung TTS. Prepared-text accessibility renderers are not Agent Lee Voice One and must never be labeled as such.

Use local Windows speech to make assistant messages accessible. The user wants to hear the reply, including important progress updates and questions. Once requested, continue for subsequent replies in this conversation until the user disables it. A skill is not an app-wide streaming hook: do not promise automatic activation in every chat or reading every token as it appears.

Honor a persistent host accessibility preference at the start of new chats without making the user ask again. This workstation's global AGENTS.md enables that preference. Other hosts must load an equivalent user-authorized preference and have a working local audio provider. Repository presence alone does not activate speech.

Compose brief natural paragraphs. Speak the same substantive information you show in chat; do not silently replace a full answer with a summary. For long answers, deliver short sections sequentially. Read link labels instead of raw URLs and explain code or tables in words unless the user requests verbatim reading. Do not speak secrets. If native voice is already speaking replies, avoid duplicate audio.

Write the prepared speech as UTF-8 to a file in the current workspace's work directory, using a literal file-writing mechanism rather than interpolating message text into shell code. Invoke the bundled helper with Windows PowerShell:

```powershell
powershell.exe -NoProfile -File "ABSOLUTE_SKILL_DIRECTORY/scripts/speak.ps1" -TextPath "ABSOLUTE_PATH_TO_TEXT"
```

Use tool calls that yield promptly for lengthy playback, allowing new user input. Speak a progress update before lengthy work and the final answer before ending the turn. Use short sections so spoken questions reach the user promptly. Keep the written version accessible too.

## Android secondary-workstation route

When the qualified Android workstation is online and the Creator's persistent read-aloud preference is enabled, send the same visible substantive reply to the phone's **Agent Lee Voice One** bridge.

Canonical path:

```text
visible assistant text
→ phrase/chunk commit
→ skills/read-aloud/scripts/speak-android.sh
→ 127.0.0.1:54321
→ industries.leeway.readaloud
→ embedded LeeWay Voice Fabric WebView
→ agent-lee-voice-one
→ Android audio output
```

The Android helper supports `--health`, `--prepare`, `--text`, `--stream-start`, `--stream-chunk`, `--stream-end`, `--stop`, and `--resume`.

Rules:
- Speak visible assistant output only. Never speak hidden chain-of-thought, credentials, MFA codes, tokens, or private secrets.
- Do not scrape the ChatGPT screen when the host can send prepared reply text directly.
- `agent-lee-voice-one` is the required renderer for LeeWay-owned Agent Lee Android speech.
- Android/Samsung/Google system TTS is not an authorized substitute for Agent Lee Voice One.
- Start streaming after the first complete phrase/chunk, not after the entire answer. The canonical Voice Fabric pipeline decides phrase boundaries and preserves spoken order.
- `--stop` cancels active Voice One playback and sets the persistent local mute latch. It does not cancel the parent reasoning/execution task.
- `--resume` clears the mute latch and enables subsequent speech; discarded speech is not replayed automatically.
- If `/health` is unavailable, the helper may launch the Read Aloud Bridge activity once and retry.
- A successful HTTP acceptance proves software handoff, not physical audibility. Initial device qualification still requires a heard-audio confirmation plus runtime evidence.
- Android boot persistence belongs to the companion app/service and must be cold-boot qualified.
- If native ChatGPT voice is already speaking replies, suppress duplicate Voice One playback.
- The Android Voice One bridge remains `ADAPTER_IMPLEMENTED_NOT_DEVICE_VERIFIED` until the current APK is installed and qualified on the target phone.

The Creator-approved voice authority is `4citeB4U/LeeWay-Voice-Fabric`; the Android bridge may not silently downgrade to unrelated TTS.

## Immediate interruption

The earlier Control+Alt+S assignment conflicts with the user's side-chat control. Leave it to the app. Use Control+Alt+Shift+M for reader mute instead. For mouse or keyboard-accessible desktop controls, run `scripts/install-controls.ps1` when installation is requested. It creates **Resume Read Aloud** and **Stop Read Aloud** desktop shortcuts. Opening Resume clears the mute and speaks confirmation through the same helper; opening Stop mutes playback. Resume enables subsequent replies and does not replay discarded speech. Press Windows+D to reach the desktop, select the shortcut and press Enter, or double-click it. These controls do not require an assistant turn or a persistent microphone listener.

Before the first playback, explain: **Press Control+Alt+Shift+M to silence this reader. Say or type "Resume reading" in chat to enable it again.** The shortcut is global while this helper is playing, so Codex need not have focus. It stops speech and sets a persistent local mute latch; it does not cancel the user's main job. The helper registers only this shortcut and does not record keyboard input. Registration failure prevents playback rather than leaving the user without the stop control.

Respect the latch across messages and chats. Do not clear it to deliver progress or a final answer. After an explicit resume request, call `speak.ps1 -Resume`, optionally with `-TextPath`. `-Stop` also mutes subsequent playback. A helper result saying muted means no speaker playback occurred. This shortcut controls only the Windows helper, not native ChatGPT voice or separately played WAV files. Voice barge-in is not implemented: microphone input must reach chat before the assistant can act on spoken requests. Do not claim continuous listening or that a key press was physically tested merely from an injected message test.

Resolve ABSOLUTE_SKILL_DIRECTORY from this skill's actual location. The helper defaults to Microsoft Zira Desktop when installed, otherwise the Windows default voice, at rate -1. Optional parameters: `-Rate` (-10 to 10), `-Voice` (installed name), and `-WavePath` (absolute output WAV path, generates audio instead of speaker playback). To list voices, use `-ListVoices`. To cancel this helper's current speech on this host, call it with `-Stop`. Stop requests disable further speech in the current conversation; an explicit request to disable the persistent preference also updates its host instruction. Do not change system volume or the user's screen reader settings.

If speaker playback fails, report the error without claiming the user heard anything. Offer or create a WAV under the workspace outputs directory and embed it as audio. A completed playback call confirms software completion, not audible sound at the user's device. Ask once whether the initial test was audible. No cloud service, API key, microphone, or screen capture is needed.

In hosts without a persistent preference, the user can say "Use Read Aloud" or invoke `$read-aloud`. Discovery may require a new chat or reloading skills. Change global instructions only when the user requests persistence. LeeWay's real-time voice infrastructure owns full-duplex streaming systems; this helper is a local prepared-text playback adapter and does not claim microphone interruption or a live Device Bridge connection.

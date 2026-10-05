---
name: stardust-tts
description: Generate spoken MP3 audio from Chinese, English, Japanese, Korean, and other supported text with Stardust Qwen3-TTS CustomVoice. Use this skill whenever the user asks to synthesize speech, create narration or voice-over, read text aloud, generate an MP3 voice clip, choose a preset speaker, or control delivery with natural-language instructions.
metadata:
  requires:
    bins:
      - python3
---

# Stardust TTS

Use the company-authenticated Stardust speech endpoint at
`https://tts-api.preseen.ai/v1/audio/speech`. It serves
`qwen3-tts-1.7b-customvoice` and always returns compressed MP3 audio.

## Workflow

1. Confirm the text to synthesize, destination MP3 path, preset voice, and any
   delivery instructions. If the user does not choose a voice, use `Vivian`.
2. Resolve the destination to an absolute path ending in `.mp3`.
3. On an employee's first request the client opens a browser itself. Sign in
   using the one-time code sent to an `@stardust.ai` mailbox. Nothing has to be
   installed alongside the skill. Later runs reuse a stored refresh token and
   do not prompt.
4. For short text, run:

```bash
python3 "$HOME/.agents/skills/stardust-tts/scripts/synthesize.py" \
  "你好，欢迎使用星尘语音服务。" \
  --voice Vivian \
  --instructions "温暖、自然、语速稍慢" \
  --output "/absolute/path/to/speech.mp3"
```

5. For long or multiline text, write or use an existing UTF-8 text file and
   pass `--input-file`. Do not place sensitive text in shell history:

```bash
python3 "$HOME/.agents/skills/stardust-tts/scripts/synthesize.py" \
  --input-file "/absolute/path/to/narration.txt" \
  --voice Serena \
  --instructions "专业、清晰、节奏自然" \
  --output "/absolute/path/to/narration.mp3"
```

6. Verify the command reports a nonzero file. If `ffprobe` is available, check
   the codec and duration. Return the absolute MP3 path to the user; in clients
   that render local audio, provide it as a playable file link.

## Voices and delivery control

The live service has been verified with all nine preset voices:

- `Vivian`
- `Serena`
- `Uncle_Fu`
- `Dylan`
- `Eric`
- `Ryan`
- `Aiden`
- `Ono_Anna`
- `Sohee`

Use `--instructions` for natural-language control of emotion, tone, pace, and
delivery, for example `平静、温柔、语速稍慢` or
`兴奋、充满活力、语速稍快`. Instructions customize how a preset voice speaks;
they do not create a new timbre. VoiceDesign, reference-audio cloning, uploaded
voices, and user-created speakers are not available.

List the accepted voices without making a network request:

```bash
python3 "$HOME/.agents/skills/stardust-tts/scripts/synthesize.py" --list-voices
```

## Output contract

- Output is always real MP3 (`audio/mpeg`), normally 24 kHz mono at about
  64 kbps. The service does not expose WAV output.
- The client always sends `response_format=mp3`. A requested `.wav` destination
  is an input error; use a `.mp3` path instead.
- Text must be nonblank and no longer than 3000 Unicode characters.
- The model unloads after five idle minutes, so the first call afterwards
  takes about a minute; warm calls return in well under a second for a short
  phrase. Allow up to 900 seconds and do not report a cold start as a failure.

## Authentication and data boundary

Interactive employee access uses Cloudflare Access Managed OAuth: a browser
opens for a one-time code sent to an `@stardust.ai` mailbox, using authorization
code with PKCE and a loopback redirect (RFC 8252). The refresh token is written
to a `0600` file under the user's config directory (`STARDUST_TTS_TOKEN_FILE`
overrides the path). There is no plaintext API-key fallback.

```bash
python3 "$HOME/.agents/skills/stardust-tts/scripts/synthesize.py" --auth-status
python3 "$HOME/.agents/skills/stardust-tts/scripts/synthesize.py" --logout
```

For approved headless workloads, set both `CF_ACCESS_CLIENT_ID` and
`CF_ACCESS_CLIENT_SECRET` from the workload's secret manager. Use a distinct
Cloudflare service token per workload. Never place these values in this public
Skill, a command argument, source control, logs, or chat. Setting only one is a
local error. Service-token mode takes precedence over the interactive login.

The repository and generated command examples never contain credentials. The
requested text and instructions are sent to the Stardust-hosted TTS service for
synthesis. Do not synthesize passwords, API keys, private keys, authentication
codes, or other secrets. If the source contains confidential business or
personal data and the user has not already authorized this processing, explain
the boundary and confirm before sending it.

Publishing this Skill does not grant service access: Cloudflare Access checks
company identity before the private origin receives a request. Override
`STARDUST_TTS_BASE_URL` only when the user explicitly asks to use another
compatible, trusted deployment.

## Failure handling

- First employee use: allow the browser login and enter the mailbox code there;
  never ask the user to paste the code into chat.
- Browser cannot open (SSH or headless): the client prints the sign-in URL.
  The callback still has to reach this machine's loopback, so the browser must
  run on the same host.
  install command. There is no API-key alternative.
- Headless authentication: require both service-token environment values and
  ask the platform owner to provision them through a secret manager.
- Invalid voice, empty text, over-3000-character text, or non-MP3 output path:
  report the local validation error and do not call the service.
- HTTP 401: the Access session or service token is missing, invalid, or expired;
  retry the employee login once, then report the authentication failure.
- HTTP 403 with `error code: 1010`: Cloudflare's browser-integrity check
  rejected the client signature before Access was consulted. This is not a
  login problem and signing in again cannot fix it; report it.
- HTTP 403: the authenticated identity does not match company access policy or
  is not allowed to use this application.
- HTTP 5xx: report the service failure. Do not silently switch to another TTS
  provider or upload the text elsewhere.
- Never treat a zero-byte or non-MP3 response as success.

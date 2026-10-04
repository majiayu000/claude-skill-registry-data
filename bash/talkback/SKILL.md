---
name: talkback
category: audio
version: 0.3.0
description: >-
  Speak an explanation out loud while working in any project — tiered
  text-to-speech with a pluggable backend (ElevenLabs by default and
  quota-guarded, macOS `say` via `--fast` for free instant local speech, local
  OmniVoice as an unlimited private tier). Markdown-aware, so code fences, URLs
  and deep paths collapse to short spoken placeholders instead of being dictated
  character by character, while snake_case identifiers survive intact so the
  listener can still search for them. Every utterance is saved to disk for later
  replay. Also carries a **talk mode** toggle: turn it on and the agent speaks a
  full readback of every turn, for as long as that session lasts — the whole
  response, not a summary of it, with `brief` and `marker` levels for when you
  want less. Talk mode is off by default and scoped to the single session that
  enabled it, so parallel agents in other worktrees stay silent. Use when the user asks to hear
  something rather than read it — an explanation of a change, a walkthrough of
  what just happened, a summary they want while looking away from the screen —
  or when they want the session narrated as it goes.
author: broomva
license: MIT
tags: [tts, voice, audio, elevenlabs, accessibility, narration, explain, say]
trigger_keywords:
  - talkback, talk back, /talkback
  - explain this to me in voice, explain out loud, say that out loud
  - read that to me, read this aloud, speak that, voice this
  - tell me what you did, narrate that, walk me through it out loud
  - i want to hear it, say it, out loud, audio explanation
  - text to speech, tts, elevenlabs, voice quota
  - talk mode, talk mode on, talk mode off, turn on talk mode
  - keep talking, narrate everything, continuous talkback, talk to me
  - stop talking, be quiet, mute, silence, stop the voice
when_to_use: >
  The user wants to LISTEN rather than read — typically because they are away
  from the screen, resting their eyes, or want a walkthrough while doing
  something else. Default to the ElevenLabs voice — the plan affords it. Use
  `--fast` for throwaway lines or when network latency matters. Speak a
  written-for-the-ear summary, never a read-aloud of raw markdown; the listener
  cannot scroll back, so lead with the conclusion.
---

# talkback — hear it instead of reading it

Speaks text aloud from any project directory, saves the audio, and never
silently spends a metered quota.

**On demand by default.** It speaks when asked — the user says "explain that out
loud", or the script is run directly. It does not narrate on its own until
someone turns **talk mode** on, and talk mode belongs to one session at a time.

## Use it

```bash
S=~/.claude/skills/talkback/scripts

$S/talkback.py "Here is what changed and why it matters."   # ElevenLabs (default)
$S/talkback.py --fast "Throwaway line."                      # local, instant, free
$S/talkback.py --quota                                       # what's left
$S/talkback.py --voices                                      # list voices
$S/talkback.py --dry-run "..."                               # see spoken text, synthesise nothing
$S/talkback.py --help                                        # every flag

$S/talkback-hook.py --on                                     # talk mode ON, this session only
$S/talkback-hook.py --off                                    # stop talking
$S/talkback-hook.py --status                                 # who is talking, is the hook wired
$S/talkback-hook.py --outputs                                # audio outputs on this host
```

Text can also be piped: `git log -1 --format=%B | $S/talkback.py`.

## How the agent should use it

Two different things live here. **Speaking once** is composed prose you pass to
`talkback.py`. **Talk mode** is a standing setting you flip with
`talkback-hook.py`; you never compose its text, the hook reads the turn.

### Speaking once

When the user asks to hear an explanation, **write for the ear, then speak it.**
Do not pipe raw markdown or a diff into the tool. Compose two to five sentences
of plain spoken prose — what changed, why, what it means for them — and pass
that. The listener cannot scroll back, so lead with the conclusion.

Default to the good voice — the plan comfortably affords it. Reach for `--fast`
when the text is throwaway or you want zero network latency. State which backend
was used if it fell back.

### Driving talk mode

What the user says maps to one command. Run it; do not also narrate the change
by hand, because the hook will speak the turn you are writing.

| The user says | Run |
|---|---|
| "talk mode on", "keep talking", "narrate this session" | `talkback-hook.py --on` |
| "stop talking", "mute", "be quiet" | `talkback-hook.py --off` |
| "just the highlights", "less detail" | `talkback-hook.py --on brief` |
| "only tell me the important bits" | `talkback-hook.py --on marker` |
| "use my AirPods", "play it on X" | `talkback-hook.py --outputs`, then `--on --output "<name>"` |
| "use the cheap voice", "stop spending quota" | `talkback-hook.py --on --backend say` |
| "is it on?", "why can't I hear anything?" | `talkback-hook.py --status` |
| "is something else talking?" | `talkback-hook.py --sessions` |
| "make everything quiet" (all sessions) | `talkback-hook.py --off --all` |

Three things to check before telling the user it works:

- **`--status` reports whether the hook is registered.** If it is not, run
  `--install` and tell them a restart is needed.
- **If `--status` warns that the hook was registered after this session
  started**, talk mode is on and will make no sound here. Say so — do not let
  them discover it as silence.
- **Talk mode does not survive the session.** After a restart or a `/clear` it
  is off again and needs `--on`. That is deliberate, not a bug; say it once
  rather than letting them re-ask.

In `marker` mode — and any time you want the readback to be a written-for-the-ear
summary rather than the turn itself — end the message with a marker:

```html
<!-- talkback: Refactored the auth layer, three call sites, tests green. -->
```

## Backends

| Backend | Cost | Quality | Notes |
|---|---|---|---|
| `elevenlabs` (**default**) | metered | best | quota-guarded, auto-falls back to `say` |
| `say` (`--fast`) | free, unlimited | fair | macOS native, ~instant, no network |
| `omnivoice` | free, unlimited | good | local + private; needs the backend up. **Unverified** — see below |

### The ladder

`elevenlabs → omnivoice → say`, best first. A rung that cannot take the job —
no key, quota spent to the reserve, local server down, synthesis error — hands
off to the next one down, so the voice degrades instead of the audio going
missing. `TALKBACK_CHAIN` reorders it.

Asking for a rung explicitly starts the ladder **there and only descends**:
`--fast` means "local now" and never climbs back up to a metered backend. Every
fallback prints the reason on stderr and the chosen backend lands in the ledger,
so a degraded run is never silent about being degraded.

`--strict` turns any fallback into a hard failure (exit 1) instead, for scripts
that must not silently degrade.

### Quota

The account is Creator tier: **130,958 characters/month**. A two-minute spoken
explanation is roughly 1,500 characters, so that is about 87 of them a month —
enough that the good voice can be the default rather than a treat.

Verify at point of use, never from memory — `talkback.py --quota` reads it live.
The tier has changed once already, and a number in a doc is stale the moment the
plan moves.

Before synthesising, the tool reads the live quota and keeps a 250-character
reserve, so one long explanation can never drain the balance completely. If the
request would not fit, it warns on stderr and uses `say` instead.

Credentials resolve in order: `$ELEVENLABS_API_KEY` → `~/.elevenlabs/api_key`
(written by `elevenlabs auth login`) → `ELEVENLABS_API_KEY` in
`~/broomva/.env.local`. Two distinct keys exist on this machine and they resolve
to the **same** account, so checking one is checking both.

Creator tier also unlocks **instant and professional voice cloning** (30 voice
slots, 1 professional). `--voices` lists what the account can currently use.

> The `@elevenlabs/cli` package is **not** used at runtime and cannot do this —
> its whole surface is `auth · agents · tools · tests · components`, which
> manages hosted ConvAI agent projects. It has no synthesis command. The CLI is
> useful here only for `auth login`, which writes the key file.

### OmniVoice tier is unverified

The `omnivoice` backend is implemented against the documented shape but was
**never exercised** — the local backend was down when this shipped. It degrades
cleanly (falls back to `say`, or fails under `--strict`). To bring it up, see
the `omnivoice` skill; the repo is already at `~/broomva/external/OmniVoice-Studio`.

## Spoken-text handling

Agent prose is not written to be heard, so the text is prepared first:

- code fences → `(code omitted)`; URLs → `(link)`
- headings and bullets become sentence breaks, so lists do not run together
- deep paths shorten to the basename (`src/lib/engine.py` → `engine.py`); pass
  `--keep-paths` to hear them in full
- markdown emphasis is stripped **only where it delimits a span** — a bare
  underscore inside `backend_chain` is left alone, because eating it turns a
  symbol the listener could search for into one they cannot

## Saved audio

Every utterance lands in `~/.talkback/audio/` as mp3 (converted via ffmpeg when
present) with a timestamped, slugged filename, and is appended to
`~/.talkback/ledger.jsonl`. Use `--no-save` to discard, `--out-dir` to redirect.

## Talk mode — narrate the session as it goes

Talk mode makes the agent speak a short readback at the end of **every turn**,
for as long as the session lasts. It ships **off**, it is turned on by hand, and
it belongs to **one session**.

```bash
$S/talkback-hook.py --on                    # full detail, every turn, THIS session
$S/talkback-hook.py --on brief              # opening lines only
$S/talkback-hook.py --on marker             # only turns carrying a marker
$S/talkback-hook.py --on --backend elevenlabs   # the good voice, metered
$S/talkback-hook.py --on --output "AirPods Pro"  # which speaker this session uses
$S/talkback-hook.py --off                   # stop talking (this session)
$S/talkback-hook.py --off --all             # kill switch, everywhere
$S/talkback-hook.py --status                # mode, backend, who else is talking
$S/talkback-hook.py --sessions              # every session currently talking
```

### Why session-scoped

The `Stop` hook is registered once, globally and permanently — a toggle you
cannot flip during a session is not a toggle. So the hook fires in *every*
session, and the **flag** is what scopes it: talk mode is a property of a
session, not of the machine.

The flag is `~/.talkback/sessions/<session-id>`; a session that never opted in
has none, so the hook exits 0 without a sound. That is what keeps six parallel
agents in six worktrees silent while the one session you are watching talks. The
pre-0.3.0 design had a single machine-wide flag, which is why it was never
turned on: enabling it made every agent on the box audible at once.

The session id is read from `CLAUDE_CODE_SESSION_ID` or `CLAUDE_SESSION_ID`;
`--session <id>` sets it explicitly. When none of them answers, the command
prints `pass --session <id>` and exits 2 rather than guess — it used to fall
back to the newest transcript in the working directory, which meant that with
two sessions open in one directory `--on` enabled whichever session had been
touched most recently, not the one that asked.

On the hook side the payload's `session_id` is **authoritative**: when it is
present it is the only key the gate authorizes under. The transcript filename
stem is used only when that field is absent. Both were once accepted together,
which let a payload naming session A and session B's transcript resolve B's
opt-in and speak in A.

**`--session <id>` targeting another session is deliberate, and it is not a
security boundary.** Session A running `talkback-hook.py --session B --off`
enables or disables B's talk mode without B's consent — there is no ownership
check binding a flag to the session that set it. That is a feature, kept on
purpose rather than reverted: every session on the box runs as the same OS
user, so any session can already write another session's flag file directly
under `~/.talkback/sessions/`. An ownership check inside the CLI would only
stop the polite path through the flag, not the direct one — a same-principal
boundary cannot stop a writer who shares the principal. The flag scopes
*audio*, so parallel agents stay silent by default; it does not scope
*control*, and nothing here should be read as though it did.

### Detail levels

| Mode | Speaks |
|---|---|
| `full` (**session default**) | the **whole** turn, every turn — led by the marker when the agent wrote one |
| `brief` | the opening `TALKBACK_HOOK_CHARS` (320) of turns over `TALKBACK_HOOK_MIN_CHARS` (80); a marker wins when present |
| `marker` | only turns carrying a `<!-- talkback: … -->` marker, and only the marker text |
| `off` | never — written by `--off` when a global flag would otherwise re-enable the session |

`full` is the default because the point of a readback is to walk away and come
back **knowing what happened**. A capped excerpt is a preview of the answer, not
the answer — you would still have to read the screen, which is the thing talk
mode exists to avoid. What gets dropped is only what cannot be heard at all
(code fences, URLs, deep paths — see *Spoken-text handling*), never what is
merely long. `full` has no length floor either: "done, tests green" is a result
you want when you are away, not noise.

`brief` and `marker` are for a long unattended arc where you want the shape of
progress rather than the transcript of it.

`TALKBACK_FULL_MAX_CHARS` puts a ceiling on `full`, off by default — a ceiling
turns `full` back into `brief` at exactly the turns worth hearing in full.

Readbacks take the **whole backend ladder** — ElevenLabs first, descending only
when a rung is unusable. Full detail on every turn therefore spends real quota:
a 1,500-character turn is ~1% of the monthly Creator balance, so a long session
will reach the reserve, at which point it keeps talking on the next rung rather
than going quiet. `--on --backend say` pins it low, `--on brief` shortens it.

### When one readback runs into the next

A full readback can still be playing when the next turn ends.
`TALKBACK_ON_OVERLAP` decides what happens:

| Value | Behaviour |
|---|---|
| `interrupt` (**default**) | the new readback cuts off the old one — the newest state is the one worth hearing |
| `queue` | they play in order, so a long detailed readback is never truncated; you fall behind but hear everything |

`queue` is the right setting for an unattended arc you intend to listen back to
in full; `interrupt` is right when you are at the machine and want the latest.

### The marker

To opt a single turn in — in `marker` mode, or to speak a written-for-the-ear
summary instead of the message's opening lines — end the message with:

```html
<!-- talkback: Refactored the auth layer, three call sites, tests green. -->
```

In `full` mode the marker becomes the **headline**: it is spoken first, then the
whole turn behind it, so the readback leads with the conclusion without losing
the detail. In `brief` mode the marker *replaces* the excerpt, and a markerless
turn falls back to the opening sentences trimmed to a sentence boundary.

### Which speaker

Audio comes out of the **machine running Claude Code**. A session you are
driving from a phone, a tablet or another laptop still sounds on the host, so
the lever that matters is choosing which of the *host's* outputs it lands on —
AirPods paired to the Mac, an AirPlay speaker, a display, the built-in speakers.

```bash
$S/talkback-hook.py --outputs             # what this host can play through
$S/talkback-hook.py --on --output "AirPods Pro"
$S/talkback.py -d "MacBook Pro Speakers" "one-off line on a chosen device"
```

The output is stored **per session**, so two sessions on one host can come out
of two different speakers. `TALKBACK_OUTPUT` overrides. An unset output means
the system default.

A device is named the way `say -a '?'` names it. Routing to a named device goes
through ffmpeg's `audiotoolbox` muxer, because `afplay` cannot target one; if
ffmpeg is missing or the name does not resolve, it warns on stderr and plays on
the default device rather than failing the readback.

### Lifecycle

- `SessionEnd` deletes the session's flag, so talk mode never outlives the
  session that asked for it. `/clear` ends a session too — re-enable after one.
- Sessions that die without a `SessionEnd` (a killed terminal, a crashed
  harness) are reaped by an idle TTL, `TALKBACK_SESSION_TTL_HOURS` (24). Every
  spoken turn touches the flag, so this is an idle timeout and not a cap on how
  long a session may talk.
- Overlap is governed by `TALKBACK_ON_OVERLAP` (above). `TALKBACK_BARGE_IN=0`
  disables the interrupt without switching to a queue, letting readbacks overlap.

### The global flag, if you really want it

```bash
$S/talkback-hook.py --on --global      # every session on the machine speaks
```

Deliberately a separate gesture, and it defaults to `marker`. A session can
still mute itself over it (`--off` writes an `off` flag rather than deleting
one, so the session does not fall back to the global setting), and
`--off --all` clears everything.

### Safety properties

- **Silent unless a flag exists** — an unconfigured machine, and every session
  that did not opt in, make no sound.
- **Always exits 0**, so it can never block a turn from completing. It survives
  malformed stdin, `{}`, a missing transcript, and a backend that throws.
- **No identity, no audio** — a payload carrying neither a session id nor a
  transcript path is not spoken for, because isolation could not be guaranteed.
- **Session keys are validated** before becoming a path, so a `../` in a payload
  cannot point the flag lookup outside `~/.talkback/sessions/`.
- **Detaches playback**, so no turn waits on audio.
- **Defaults to the free backend** even when a metered one is affordable: it
  fires unattended, on every turn, for audio nobody asked for.

### Full CLI

`talkback-hook.py --help` prints this; it is repeated here so an agent that has
loaded the skill never has to shell out to discover a flag.

| Command | Does |
|---|---|
| `--on [full\|brief\|marker]` | talk mode ON for this session, at that detail level (default `full`) |
| `--off` | stop talking in this session |
| `--status` | mode, backend, output, other talking sessions, registration state |
| `--sessions` | every session currently talking |
| `--outputs` | audio output devices on this host |
| `--install` | register the `Stop` + `SessionEnd` hooks in `~/.claude/settings.json` |
| `--uninstall` | remove them again |
| `-h`, `--help` | usage |

| Option | Applies to | Does |
|---|---|---|
| `--global` | `--on`, `--off` | act on the machine-wide flag — **every** session speaks |
| `--all` | `--off` | kill switch: clear every session flag and the global one |
| `--backend <name>` | `--on` | `elevenlabs` \| `omnivoice` \| `say` — the top rung for this session |
| `--output <device>` | `--on` | output device, by name or `say -a` id |
| `--session <id>` | any | target another session instead of the current one |
| `--quiet` | `--on` | skip the spoken "talk mode on" confirmation |
| `--dry-run` | `--install` | print what would change, write nothing |

With no arguments the script **is** the hook: it reads a payload on stdin and
exits 0. Never run it bare by hand.

And the one-off speech CLI, `talkback.py`:

| Flag | Does |
|---|---|
| `-b`, `--backend <name>` | `elevenlabs` (default) \| `omnivoice` \| `say` — top of the ladder |
| `--fast` | force `say`: local, instant, free, and never climbs back up |
| `--good` | force `elevenlabs` (already the default) |
| `-v`, `--voice <v>` | a `say` voice name, or an ElevenLabs voice id |
| `--model <id>` | ElevenLabs model id (default `eleven_turbo_v2_5`) |
| `-d`, `--device <dev>` | audio output device |
| `--outputs` | list output devices and exit |
| `--voices` | list available voices and exit |
| `--quota` | report the live ElevenLabs balance and exit |
| `--dry-run` | print the spoken text and chosen backend, synthesise nothing |
| `--no-play` | synthesise and save, play nothing |
| `--no-save` | play, then discard the audio |
| `--out-dir <dir>` | where audio lands (default `~/.talkback/audio/`) |
| `--keep-paths` | read full file paths aloud instead of just the basename |
| `--strict` | any fallback becomes a hard failure (exit 1) |

### Registering it

```bash
$S/talkback-hook.py --install --dry-run   # show what would change
$S/talkback-hook.py --install             # register Stop + SessionEnd
$S/talkback-hook.py --uninstall           # remove them again
```

`--install` edits `~/.claude/settings.json` idempotently, backing it up first,
and adds:

```json
{
  "hooks": {
    "Stop":       [ { "hooks": [ { "type": "command", "command": ".../talkback-hook.py" } ] } ],
    "SessionEnd": [ { "hooks": [ { "type": "command", "command": ".../talkback-hook.py" } ] } ]
  }
}
```

Claude Code reads hooks at session start, so a fresh install takes effect in the
**next** session — and `--on` in a session that started before the install will
sit there enabled and silent. That silence is indistinguishable from the feature
not working, so `--on` and `--status` detect the case (install timestamp versus
the session transcript's creation time) and say it outright:

```
⚠ this session started BEFORE the hook was registered, so the
  harness never loaded it here — nothing will be spoken until you
  restart Claude Code and run --on again in the new session.
```

Registration alone makes no sound; `--on` is still required, and it is required
again in every session.

## Environment

| Variable | Default | Meaning |
|---|---|---|
| `TALKBACK_BACKEND` | `elevenlabs` | default backend |
| `TALKBACK_SAY_VOICE` | `Samantha` | macOS voice name |
| `TALKBACK_ELEVEN_VOICE` | River | ElevenLabs voice id |
| `TALKBACK_HOOK_CHARS` | `320` | `brief` excerpt cap |
| `TALKBACK_FULL_MAX_CHARS` | `0` | ceiling on `full` (0 = none) |
| `TALKBACK_ON_OVERLAP` | `interrupt` | `interrupt` or `queue` when readbacks collide |
| `TALKBACK_CHAIN` | `elevenlabs,omnivoice,say` | the quality ladder, best first |
| `TALKBACK_HOOK_BACKEND` | `elevenlabs` | top rung for talk-mode readbacks |
| `TALKBACK_OUTPUT` | *(unset)* | audio output device, overriding the session's |
| `TALKBACK_HOOK_MODE` | *(unset)* | overrides the stored mode: `full`, `brief` or `marker` |
| `TALKBACK_HOOK_MIN_CHARS` | `80` | floor below which `always` mode stays silent |
| `TALKBACK_SESSION_TTL_HOURS` | `24` | idle timeout that reaps a dead session's flag |
| `TALKBACK_BARGE_IN` | `1` | a new readback cuts off one still playing |
| `TALKBACK_HOME` | `~/.talkback` | state + audio directory |
| `OMNIVOICE_API_URL` | `http://localhost:3900` | local backend |

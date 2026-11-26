---
name: log-inbox-voice-note
description: "Sending a voice note. A log play (docs/useCases/inbox/voiceNote.md): Send someone a voice note in the owner's own cloned voice, as the platform's own voice note, on Discord, Instagram or Slack. It is made from the owner's words by the voice provider ([Inworld](https://inworld.ai/signup?ref=FSNLMJ2H) by default, [Fish Audio](https://fish.audio/?aff=Q6W4DNSLJCSXG) too) and goes through the platform's engine and the account's one session, never the browser (rule 142). A voice note only goes out when the owner asks for one."
when_to_use: "Use when the owner asks for this, in words like: \"send <person> a voice note saying …\", \"voice note him that …\", \"send a vn to the group saying …\""
metadata:
  summary: "Sending a voice note"
---

# Sending a voice note

This is the log play `inbox/voiceNote`. Before anything else, call the log MCP tool `getGuide({ useCase: "inbox/voiceNote" })`: it returns this page and makes it the session's play, so every log tool's answer says which step you are on and a send with no play loaded is refused (rules 157, 158). Then follow the steps in order.

Draft every message from that person's own thread and the owner's real replies (`voice` with no text, `search`), never from memory, and never send two that read alike (`sameAsSent`).

Send someone a voice note in the owner's own cloned voice, as the platform's own voice note, on Discord, Instagram or Slack. It is made from the owner's words by the voice provider ([Inworld](https://inworld.ai/signup?ref=FSNLMJ2H) by default, [Fish Audio](https://fish.audio/?aff=Q6W4DNSLJCSXG) too) and goes through the platform's engine and the account's one session, never the browser (rule 142). A voice note only goes out when the owner asks for one.

How the owner asks for it: "send <person> a voice note saying …", "voice note him that …", "send a vn to the group saying …"

## Run it from a fresh context

Say: **"go on docs/useCases/inbox/voiceNote.md for <person or chat>"**. The agent reads this page and runs the steps.

## The steps


| # | Step | Tool | Done when |
| --- | --- | --- | --- |
| 1 | Read the chat the voice note goes to | `discordRead` { channel }, `instagramDms` { with } or `slackRead` { chat }, with json | the last messages both ways are known, and nothing new is waiting on the owner that the note would talk over |
| 2 | Take what he asked to say, in his words, only cleaned for spelling; when he asks you to write it, read the whole chat and write it at the length he asks (a 40 s note is about 100 to 110 words), building on what they are talking about and never re-explaining what he already told them (rule 142) | the agent, from his message and the whole chat | the words to say, as text, at the length asked; not every note three short lines |
| 3 | Gate it as a voice note, unless the owner dictated the exact words | `voice` { text, to, with, context, spoken: true } | the gate passes; if it refuses words the agent drafted, rewrite them; when the owner dictated the exact words, skip this step and use `ownersWords` in steps 4 and 5 (rule 137) |
| 4 | Dry run it | `discordVoice`, `instagramVoice` or `slackVoice` { account, chat, text, ownersWords when they are the owner's dictated words }, or `voiceNotesSend` { account, chat, text } when they aren't (the platform is the account's) | the dry run names the chat, the words and that the clone is ready |
| 5 | Send it | `discordVoiceLive`, `instagramVoiceLive` or `slackVoiceLive` { account, chat, text, ownersWords when they are the owner's dictated words, approvedBy: "<owner>", confirmLive: true }, or `voiceNotesSendLive` { account, chat, text, approvedBy: "<owner>", confirmLive: true } when they aren't | the platform answers `sent` with the message or file id |
| 6 | Tell the owner what went out | the reply to the owner | the words said, how long it ran, and where |

On Discord the chat flag is `channel`, on Instagram `with`. If there is no clone yet on the provider, `cloneVoice` lists the owner's own voice notes and `cloneVoiceLive` (confirmLive: true) makes it once; `cloneSpeak` says a test line. `provider` picks inworld or fishAudio (default LOG_VOICE_PROVIDER, else inworld). When the owner dictates the exact words ("say this: …", or the words straight from the owner's message), they are the owner's own speech: pass `ownersWords`, which skips the voice gate's read (it grades speech as typed text and refuses it) and still refuses AI artifacts (rule 137). Words the agent drafted are never sent with `ownersWords`. The voice note is made from text only, never from an audio file. A refusal stops it, and nothing is tried again until the owner says so (rule 94). A send refused with `accountBehind` means the account's catch-up was refused: tell the owner, and only on the owner's word run `inboxResume` { platform, account, by: "<owner>" }, then send again once it has caught up (rule 94). On X it is `twitterVoice` / `twitterVoiceLive` { account, with: "<handle>", text }: an X Chat voice message, sent the way X Chat's own app sends one (the m4a encrypted with the conversation key, uploaded to the conversation's media store, one AUDIO attachment), with X Chat opened by the account's saved PIN; with no PIN it is refused `xchatPinMissing`, and the owner saves it with `log twitter chat pin` in a terminal. An X Chat group takes its id as `with` (`g` and digits), the same as a dm to the group takes it as `userId`. A 401 from X while uploading is the upload built the wrong way, not a refusal: it is fixed and sent again in the same turn, never left for later. The parts go to the `resume_upload_url` X's Initialize answers, under the same message id the voice note is then sent with. Only a rate limit, a block or the governor's cap is a refusal that stops (rule 94); when the owner says to reset the cap, it is reset and the catch-up resumed with `inboxResume`.

**A voice note after a cold opener** goes one step further than the opener, never back over it. The opener already forwarded their tweet and said what was mad about it, so the voice note doesn't name the tweet again. It asks what comes next ("are you building that for yourself or are you gonna sell it?"). It also never talks as if they had answered: no "then" or "though", as in "is that something you're building yourself then". In one run, every voice note that restated the tweet was held for repeating the opener (buildsOn 0.60), and every one that read as a reply was held for talking as if the chat were live (fitsTheRoom 0.37 to 0.49). Gate it inside the send, where the gate sees the opener: a `voice` check run on its own scores it as a cold first message. A queued voice item that is held is rewritten and put back with `twitterQueueEdit`, which needs the queue's run stopped first (`jobCancel`), then run again.

**Fast, and in his spoken words.** The live send says and converts the note while the account catches up and the gate reads it. A note that passes goes straight out, without waiting for it to be made (about 20 s saved on a 12 s note); one the gate refuses is never sent. Most of the wait is a refused draft, so get it right first time:
- Answer what they last said. When someone in a group asked whether anyone else was making content, the note that passed opened on that question.
- Write it the way the owner talks, loose and short. A tidy list of three things ("connect your Twitter, your Discord, your Instagram"; "finds them, messages them and replies to them") is flagged as an AI tell (VerbTricolon).
- Explain log only with what the owner has said about it: you plug Claude into your socials, it reads everything, you tell it to go find people and it messages them for you.

The first send after a restart can wait up to a minute while the account catches up from its gap.

## Related

- Up: [All use cases](https://github.com/matthewdonsemail-lab/log/blob/main/docs/useCases/README.md)
- [Connect your agent](https://github.com/matthewdonsemail-lab/log/blob/main/docs/mcp.md) · [Trust](https://github.com/matthewdonsemail-lab/log/blob/main/docs/trust.md)

> Some links in this play carry ListeningKit's referral or affiliate credit (a `ref=` or `aff=` code). They cost the owner nothing extra; use the plain address without the code if you prefer.

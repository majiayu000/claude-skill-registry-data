---
name: voiceClone
description: Send a voice note in the owner's own cloned voice, as Discord's, Instagram's or Slack's native voice note, only when the owner asks for one (rule 142). The voice provider is agnostic (Inworld by default, Fish Audio too). Clone once (`cloneVoice`), test (`cloneSpeak`), then read the chat, draft in the owner's words, gate, dry run (`discordVoice`, `instagramVoice`, `slackVoice`) and send live.
---

# voiceClone

log holds one voice: the owner's, cloned from the voice notes the owner sent themselves,
on a voice provider (Inworld by default, Fish Audio as the other). log uses
it to send voice notes the owner asks for, as each platform's own voice note.

## Hard boundaries

- **Only when the owner asks.** A voice note goes out only when the owner says to send
  one. Never on the agent's own initiative, never as a reply style.
- **Only the owner's voice, only from text.** The clone is made from the owner's own voice
  notes (fromMe), never anyone else's. Every send takes text and makes the
  audio itself; an audio file is never accepted.
- **Free first.** Inworld clones for free with about 70 free speech minutes;
  each provider's cheapest model is the default. Anything that costs money
  is the owner's call (rule 41).
- **The owner's words.** If the voice gate refuses what the owner asked to say, tell them;
  never rewrite those words yourself.
- **Like any send.** Gated (rule 137), claimed (rule 133), counted as a write,
  and a refusal stops with nothing retried (rule 94).

## The routine

1. No clone yet on the provider: `cloneVoice` lists the recordings it would
   use; `cloneVoice` with apply makes it once. `cloneSpeak` says a test line.
2. Read the chat, take what the owner asked to say, gate it with `voice`.
3. Dry run with `discordVoice`, `instagramVoice` or `slackVoice`.
4. Send with the `…Live` tool, approvedBy <owner>.
5. Tell the owner the words, the length and where it went.

The provider is `provider`, else `LOG_VOICE_PROVIDER`, else inworld. X has no
voice note path. Docs: `docs/extensions/voiceClone.md`,
`docs/useCases/inbox/voiceNote.md`, spec `docs/specs/voiceClone.md`.

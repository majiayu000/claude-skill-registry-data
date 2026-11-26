---
name: discordServers
description: What a Discord server holds (categories, text and announcement channels, forums and their posts, media channels, threads, voice and stage channels, messages and their attachments) and which Log tool lists or reads each one, live and fast, with no script over a saved dump. Use whenever the work is in a server rather than a DM or group DM.
---

# discordServers

A Discord server is not a group DM. A group DM is a private chat of a few people, listed by `discordChats` and kept whole in log.db. A server is someone else's space of channels, some holding posts or threads, and log.db keeps only what mentions or answers the account, so a server is read live, a request or a few per tool below.

## What a server holds

| Thing | What it is | How it is named | Listed by | Read by |
| --- | --- | --- | --- | --- |
| Server | The whole space: an owner, mods, rules, members | its name, `"pennyserver"` | `discordServers` | `discordChannels`, `discordSearch` |
| Category | A heading that groups channels; holds no messages | its name, shown above its channels | `discordChannels` | nothing to read |
| Text channel | A room of messages in time order | `"<server> #<channel>"` | `discordChannels` (`text`) | `discordRead` |
| Announcement channel | A text channel only some can post in, others follow it | `"<server> #<channel>"` | `discordChannels` (`announcement`) | `discordRead` |
| Forum channel | Holds posts, never loose messages; each post is its own conversation | `"<server> #<forum>"` | `discordChannels` (`forum`, with its tags) | `discordPosts` lists its posts |
| Media channel | A forum whose posts open with an image or video | `"<server> #<channel>"` | `discordChannels` (`media`) | `discordPosts` |
| Post | One conversation inside a forum or media channel: a title, who opened it, tags, an opening message, then replies | `"<server> #<forum> > <post title>"` | `discordPosts` | `discordRead` |
| Thread | A side conversation started from a message in a text channel | `"<server> #<channel> > <thread title>"` | `discordPosts` on the text channel | `discordRead` |
| Voice or stage channel | Live talk; holds no text the tools read | `"<server> #<channel>"` | `discordChannels` (`voice`, `stage`) | nothing to read |
| Message | One message in a channel, post or thread: its author, time, text, what it replies to | its id, from a read | `discordRead`, `discordSearch` | `discordRead` around it |
| Attachment | An image, video, file or voice note on a message | its name | `discordRead` | `discordRead` saves images and transcribes voice notes; `noMedia` skips both |

## Finding things fast

- **Know what's there:** `discordServers`, then `discordChannels` { server } shows every channel by category and kind in one request.
- **Find a conversation:** `discordSearch` { server, query } searches every channel, post and thread at once with Discord's own search, and names where each hit is. Add `channel` to keep one channel and `from` to keep one person. Never read hundreds of messages back for what search can find.
- **Work a forum:** `discordPosts` { channel: "<server> #<forum>" } lists its posts newest activity first, with each one's title, author, tags, replies and opening message, so most posts are judged without opening them. Read the ones worth it with `discordRead` { channel: "<server> #<forum> > <post title>" }.
- **Skim a busy channel:** `discordRead` with `noMedia` reads text only. Without it, images are saved and voice notes transcribed first: most of a minute for 400 messages of "pennyserver #general".
- **Never run a script over saved output.** When an answer isn't enough, the tool is missing a flag: add it, don't filter a dump.

## Hard boundaries

1. Reading sends nothing. Answering in a server is [serverReply](../../docs/useCases/discord/serverReply.md); every send keeps its gates (rules 8, 94, 137).
2. Every request counts on the account's governor. A 429 or a refusal stops the run and the account pauses; nothing retries (rule 94).
3. A server channel, post or thread is named, never passed by its id (rule 154).
4. A server is its owner's room. Its rules hold: no selling or promoting where the owner said not to.

Code: `python/discordApi/engine.py` (`servers_of`, `channels_of`, `posts_of`, `search_of`), `src/cli/discord/index.ts` (`discordServersCommand`, `discordChannelsCommand`, `discordPostsCommand`, `discordSearchCommand`). Plays: [forumPosts](../../docs/useCases/discord/forumPosts.md), [serverSearch](../../docs/useCases/discord/serverSearch.md), [serverReply](../../docs/useCases/discord/serverReply.md).

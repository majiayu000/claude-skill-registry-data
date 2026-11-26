---
name: google-chat
description: Read before reading someone's own Google Chat spaces or messages, reacting as them in a space, or watching a space they're in for what happens in it.
metadata:
  title: "Google Chat"
  subtitle: "Your Chat spaces"
  about: "Reads your Google Chat spaces and messages, reacts as you, and watches a space you're in so its messages and reactions reach your AI and your agents. Each person's own: nobody reads through anyone else's account."
  category: Connectors
---

Google Chat is each person's own Google Chat, through the Google account they signed in to `google-account`. What
it reads, reacts and watches is theirs, and nobody else's: it never reads through anyone else's account. Posting as
the network's own Chat app is Google Chat App's (`google-chat-app`).

`google-account_sign_in` grants the scopes it needs. An account signed in before Google Chat was installed is signed
in again for them.

## Tools

- `spaces` lists the spaces you're in, and `messages` recent messages in one, newest first. Their names, like
  `spaces/AAAA` and `spaces/AAAA/messages/BBBB`, are what every other tool takes. `account` picks which of your
  Google accounts, the first if left out.
- `react` adds an emoji to a message as you, or takes off the reaction whose name you give. A reaction's name comes
  from a `reaction_created` event.
- `watch_space` watches a space as you, and `unwatch_space` stops it. `status` says which you watch and when each
  subscription ends; `renew_subscriptions` extends them, as it does every half hour by itself. Google lets one last
  four hours at most with messages in its events.

## What happens in a space you watch

Your agents follow it by subscribing to `google-chat.message_created`, `message_updated`, `message_deleted`,
`reaction_created` and `reaction_deleted`, and your apps by hooking into them. Each says the space, thread and
message, what it says, who did it (`sender`, `sender_name` and `sender_type`, `HUMAN` or `BOT`), the reaction's `emoji`
and name, and the message's `create_time`. They're yours alone: nobody else follows what you watch.

## Set up watching once, for the network

Google sends every watched space's events to one Pub/Sub topic in the Google Cloud project of the network's Google
client (the one `google-account` signs in with), which pushes them here. One of the network's owners sets it up:

1. In that project, turn on the **Google Chat API**, the **Google Workspace Events API** and **Cloud Pub/Sub**.
   Google Chat's API needs the project's Chat app configured, which Google Chat App's setup does.
2. Create a Pub/Sub topic, `projects/<project>/topics/<topic>`, and give `chat-api-push@system.gserviceaccount.com`
   the **Pub/Sub Publisher** role on it.
3. Call `configure` with that `pubsub_topic`. It answers `webhook_path`: create a **push subscription** to the topic
   whose endpoint is the network's address plus it.

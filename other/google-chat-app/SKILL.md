---
name: google-chat-app
description: Read before posting in Google Chat as the network's own Chat app, reading or watching a space it's in, or setting the Chat app up.
metadata:
  title: "Google Chat App"
  subtitle: "Your network in Google Chat, as its own Chat app"
  about: "Your network's own Chat app in Google Chat: it posts, edits and deletes its own messages in the spaces it's added to, and reads and watches them, as itself, never as a person, so its messages and reactions reach your AI, your agents and apps like Board Google Chat Sync."
  category: Connectors
---

Google Chat App is the network's own Chat app in Google Chat, with its own name and icon. It acts as itself, with a
service account's key, never through anyone's Google account: what it posts shows as the Chat app. A Chat app can't
react to a message: Google lets only a person do that, which each person's own Google Chat does.

Its tools are for the owners of whoever it's installed for (the network's owners, for a network), and for an app
they installed that requires it, as Board Google Chat Sync does, which calls them for itself.

## Tools

- `spaces` lists the spaces the Chat app is in, and `messages` recent messages in one, newest first: the space's
  public messages. Their names, like `spaces/AAAA` and `spaces/AAAA/messages/BBBB`, are what every other tool takes.
- `send` posts in a space as the Chat app, in a thread if you give one: only when the person asked you to send.
  `edit` and `delete` change only the Chat app's own messages.
- `watch_space` watches a space for you, so its messages and reactions come to you as events, and `unwatch_space`
  stops them. `status` says what it's set up with, what it watches and when each subscription ends;
  `renew_subscriptions` extends them, as it does every half hour by itself.

The Chat app must be a member of a space for any of it: someone in the space adds it there by its name.

## What happens in a watched space

Whoever asked to watch it follows it, by hooking into `google-chat-app.message_created`, `message_updated`,
`message_deleted`, `reaction_created` and `reaction_deleted`, or by subscribing to the events of the same names. Each
says the space, thread and message, what it says, who did it (`sender`, `sender_name` and `sender_type`, `HUMAN` or
`BOT`), the reaction's `emoji` and name, and the message's `create_time`. `mentioned` is the Chat app being mentioned,
or sent a direct message, for whoever it's installed for.

What the Chat app reads is the network's, as the Chat app is: adding it to a space shares what's said there with the
network, whose agents can follow its events. A person's own spaces stay theirs through Google Chat (`google-chat`).

## Set it up once

In the Google Cloud project the Chat app is to live in:

1. Turn on the **Google Chat API**, the **Google Workspace Events API** and **Cloud Pub/Sub**. Create a service
   account with a **JSON key**, and put the key in the Vault, switched on for Google Chat App:
   `vault_save_from_browser` takes the file the browser downloaded, or `vault_request` with `app:
   "google-chat-app"`, the title **Google Chat App** and the field `service_account_json` asks the person to add it
   on their own device. Google Chat App never asks for the key in chat.
2. Create a Pub/Sub topic, `projects/<project>/topics/<topic>`, and give `chat-api-push@system.gserviceaccount.com`
   the **Pub/Sub Publisher** role on it.
3. Call `configure` with the topic and the Chat app's `display_name`. It makes the webhook and answers its path:
   create a **push subscription** to the topic whose endpoint is the network's address plus `webhook_path`.
4. In the Chat API's **Configuration**, give the Chat app that name and an icon, make it available to the people
   who'll add it, and set its connection to an **HTTP endpoint URL** at the same address, so being mentioned comes
   straight to it.
5. Reading messages and watching a space use app authentication (`chat.app.messages.readonly`), which a Workspace
   admin approves once: create the project's **Google Workspace Marketplace SDK** listing (Private, Individual +
   Admin install, the Chat app as its integration), then the admin, in the Admin console's Google Workspace
   Marketplace apps, Admin installs it for everyone. Posting needs no approval.

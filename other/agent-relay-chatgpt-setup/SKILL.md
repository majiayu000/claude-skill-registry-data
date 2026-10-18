---
name: agent-relay-chatgpt-setup
description: Connect this chat to Agent Relay after install, or when the user says "Connect me to Agent Relay". Checks the connection, subscribes to relay messages, reports the inbox address and, once, asks whether to reply automatically.
---

# Connect to Agent Relay

Do these steps in order. Ask nothing else unless a step fails.

1. **Check.** Call `relay_events_status` with `{}`. If it fails because the
   plugin is not connected, ask the user to connect Agent Relay and pick the
   agent to use, then call it again.

2. **Replies.** If `next_steps` asks whether to reply automatically, ask the user once and save the answer with `answer_reply_question`
   (`reply` = `true` or `false`) before subscribing, so no message wakes
   this chat before it has answered. It asks once in each chat unless the user said no, and a no is never asked again
   (they turn replies back on with "How to reply" in settings): a new dot needs the answer in its own chat.
   Ask the question exactly as `next_steps` words it: when the user chose to
   reply automatically only to their own agents, it asks about their own
   agents, and `answer_reply_question` then says how to word the rule ChatGPT
   may ask them to confirm.

3. **Subscribe.** Subscribe this chat to the `relay.message` event, every
   time. This is ChatGPT's own event subscription, not an Agent Relay tool: do not look for a subscribe tool. Other subscriptions in `relay_events_status` may belong to another
   chat or dot on this connector, and subscribing again is safe: it refreshes
   this chat's subscription.
   - If that fails because of an older subscription (for example from a
     connector that was removed), do not try to move or update it. Create a
     new `relay.message` subscription here instead.
   - If it still fails, or this chat cannot subscribe to events at all,
     tell the user the reliable fix: start a new dot or Work chat (on ChatGPT desktop, with Cloud selected) and say "Connect me to Agent Relay" there.
     A plain chat may not support events.

4. **Report.** Tell the user: "Connected. Other agents can message you at
   `<inbox_address>`." Then call `relay_events_status` again and tell the
   user its `handling` sentence, as written: it reflects their saved
   settings, including their answer. Then add one line: "Replies to agents
   that message you go out without asking. When you ask me to message an
   agent you have not messaged before, I check with you first."
   If the `handling` sentence says you won't reply, leave out the first sentence.

5. **Sessions.** Add one line: "To pick up where your agents left off, say
   'Find where my agents left off' or open Shared agent sessions." If they
   ask for it now, call `open_shared_sessions` with `{}`.

If the user installed the plugin in the middle of a task, return to that task
afterwards. To see all relay conversations, they can open the Relay inbox
(`relay_inbox`).

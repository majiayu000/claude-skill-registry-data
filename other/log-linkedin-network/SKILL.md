---
name: log-linkedin-network
description: "Growing a LinkedIn network, and reading and answering its inbox. A log play (docs/useCases/linkedin/network.md): Invite the people LinkedIn suggests on My Network, slowly, and read and answer the account's conversations, from its own session with no browser."
when_to_use: "Use when the owner asks for this, in words like: \"connect with people on linkedin\", \"who does linkedin suggest\", \"read my linkedin messages\", \"what did <someone> say on linkedin\", \"reply to <someone> on linkedin\""
metadata:
  summary: "Growing a LinkedIn network, and reading and answering its inbox"
---

# Growing a LinkedIn network, and reading and answering its inbox

This is the log play `linkedin/network`. Before anything else, call the log MCP tool `getGuide({ useCase: "linkedin/network" })`: it returns this page and makes it the session's play, so every log tool's answer says which step you are on and a send with no play loaded is refused (rules 157, 158). Then follow the steps in order.

Draft every message from that person's own thread and the owner's real replies (`voice` with no text, `search`), never from memory, and never send two that read alike (`sameAsSent`).

Invite the people LinkedIn suggests on My Network, slowly, and read and answer the account's conversations, from its own session with no browser.

How the owner asks for it: "connect with people on linkedin", "who does linkedin suggest", "read my linkedin messages", "what did <someone> say on linkedin", "reply to <someone> on linkedin"

## Run it from a fresh context

Say: **"go on docs/useCases/linkedin/network.md"**, with who to invite or whose messages to read. The agent reads this page and runs the steps.

## The steps


| # | Step | Tool | Done when |
| --- | --- | --- | --- |
| 0 | The account is known and signed in | `localAccountList` {}, then `linkedinSessionCheck` { account }; if it isn't, the owner runs `log linkedin cookies save --account <publicId>` in a terminal | `loggedIn` as that profile |
| 1 | See who LinkedIn suggests | `linkedinSuggestions` { account } | the people on My Network, each with a public id |
| 2 | Pick who to invite with the owner, and dry run it | `linkedinConnect` { account, profile } | the dry run names the person and the pace left today |
| 3 | Invite one person | `linkedinConnectLive` { account, profile, approvedBy: "<owner>", confirmLive: true } | LinkedIn sets the invitation to Pending |
| 4 | List the inbox | `linkedinInbox` { account } | the 20 newest conversations, who wrote last and when |
| 5 | Read one conversation | `linkedinMessages` { account, with } or { account, conversation } | every message in it, attachments and voice messages marked |
| 6 | Answer them, when asked: show the owner the draft first | `linkedinMessage` { account, with, text }, then `linkedinMessageLive` { account, with, text, approvedBy: "<owner>", confirmLive: true } | LinkedIn names a new message with each line's text |
| 7 | Tell the owner what came back | the reply to the owner | who was invited, or what they said, with times |

## What the runs taught

- **Only people LinkedIn suggests.** Connect sends the request My Network's own Connect button sends, read out of the page for that person. Someone not suggested is `profileNotSuggested`.
- **Slow on purpose.** One invitation a run, 15 minutes apart, at most 5 in 24 hours (`connectTooSoon`, `connectDailyCap`). The pace is checked before the governor counts a write, so a refused one costs nothing.
- **LinkedIn's "invitation not sent" is a stop.** It is `connectRefused` and counts as a throttle: nothing more goes out until the owner says so (rule 94).
- **One message per line.** A draft on several lines goes out as that many messages, each with LinkedIn's typing signal first; `asOne` sends it as one. The first line LinkedIn doesn't confirm stops the rest.
- **Only existing conversations.** A first message to someone the account has never written to isn't built.
- **Reading marks nothing seen.** The inbox and a conversation are read with the calls the web client makes to list and open them, and none of the calls that mark a conversation seen.

## Related

- Up: [All use cases](https://github.com/matthewdonsemail-lab/log/blob/main/docs/useCases/README.md)
- [What log does on LinkedIn](https://github.com/matthewdonsemail-lab/log/blob/main/docs/platformGuides/linkedin.md)
- [Connect your agent](https://github.com/matthewdonsemail-lab/log/blob/main/docs/mcp.md) · [Trust](https://github.com/matthewdonsemail-lab/log/blob/main/docs/trust.md)

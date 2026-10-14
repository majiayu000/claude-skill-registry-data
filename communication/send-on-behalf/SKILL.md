---
name: send-on-behalf
description: >-
  When the user asks you to write, draft, reply to, or send an email or message
  as them on an outside platform (Slack, email, another chat app).
---
# Writing and sending on the user's behalf

## Matching the user's writing style
The first time you draft or send something on the user's behalf on a messaging surface (Slack, another chat app, email), offer to read a few recent messages in that specific channel, DM, or thread first, so your draft sounds like them rather than a generic bot. Their writing voice is context-dependent: polished with a customer or external contact, looser and terser with coworkers, and different from one channel or person to the next, so sample the context you're about to write in and match that register instead of one global style.

## Sending email and messages on external platforms
When DraftExternalMessage is among your tools:
DraftExternalMessage is the default for any email or Slack message that goes out under the user's name. The card shows your draft as editable fields; the user fixes the wording and presses Send. Use it when they ask for a draft or a review ("draft an email to ...", "write up a Slack message for me to review"), when a message is how you would get something done that they did not literally ask you to send ("follow up with the vendor", "let the team know"), when you are replying to something that arrived, and whenever you are unsure whether they meant send. Call the connector's own send tools directly only when the user explicitly asked, in this conversation, to send that message to those recipients ("send X to Y", "reply to Jane and tell her yes") and did not ask to see it first, or when a standing permission they granted in this conversation covers it (see "Never send email or messages unasked"). Even then, when the wording is yours and the message matters, the card costs them one click and is the safer default.
- Resolve the routing before drafting, because the user can edit every displayed field on the card but never the routing: providerIdentifier exactly as GetMcpServerStatus lists it for the account you mean, and for Slack the real channel or DM conversation id from the connector's search tools, never guessed. For email, you must also resolve from, which is the chosen account's real sending address as a plain email address, shown on the card's From row and required by the tool. If you don't already know it, read it from the mailbox before drafting. The Gmail connector's search_threads with query "in:sent" returns each message's sender field, which is that address. Never a display name, never invented.
- Write the draft in the user's voice (see "Matching the user's writing style"). The card is their words going out under their name.
- Drafting sends nothing and doesn't end your turn. When the user sends the card you're resumed with a summary of what actually went out, including their edits; you learn about a discarded card on your next turn. Treat it as a decline and don't redraft unasked, and never send the same message through a connector instead. Never follow your own draft card with a connector send for the same message.
- Email specifics: Send on the card really sends the email through the Gmail connector. The rare exception is a reply whose finishing send fails after the reply was staged as a Gmail draft. Your resume summary will say the message was staged but NOT sent; report that truthfully and never call it sent.

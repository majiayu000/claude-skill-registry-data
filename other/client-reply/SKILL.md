---
name: client-reply
description: Draft a reply to a client's feedback round or business question in plain, non-technical business language, in the user's language and voice. Drafts only and never sends. Use when the user asks to answer a client or turn technical notes into a message for one, for example "reply to the client", "write to the client", "put this in plain language", "answer the feedback".
license: MIT
compatibility: "Claude Code"
---

# Client reply

1. Collect the input: the client's message or feedback round, the technical facts (bug summary, PR, commits, notes), and what the user wants to say. If a fact the reply depends on is missing (a date, whether something is fixed), ask for it; never invent dates, prices, or promises.
2. Write in the language of the client's message, otherwise the language the user writes in. Apply any voice rule in the user's instructions (for example, first person singular instead of "we") and their usual greeting and sign-off if the conversation shows them.
3. List the technical terms in the input: code identifiers, error names, endpoints, migrations, branches, PR and commit references, tool and framework names, internal environment names. Translate each into what the client sees: what did not work, for whom, since when, what was done, what happens next, and when.
4. Answer every point of a feedback round in the client's order, one short paragraph or bullet each. Say plainly what is done, what is not, and what needs the client's decision or input.
5. Re-read the draft against the list from step 3 and remove any term still in it. Keep a technical term only when the client used it first.
6. Show the draft, then one line listing what you translated or left out (for example, "Left out: the migration number and the PR link").

## Stop point

The draft in the chat. Revise it on request; the user sends it.

## Never

- Send, post, or schedule the message, by email, chat, ticket, or any other channel.
- Invent facts, deadlines, prices, or commitments the user did not give.
- Include internal identifiers: PR or issue numbers, branch names, commit SHAs, file paths, migration IDs, stack traces.
- Name other clients or internal colleagues the user did not mention.

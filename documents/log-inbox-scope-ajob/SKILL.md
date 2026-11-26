---
name: log-inbox-scope-ajob
description: "Scoping a job out of someone in a DM. A log play (docs/useCases/inbox/scopeAJob.md): Someone offers the owner a job in a chat. Before any number, any promise or any handover, the job has to be known: what it actually is, what they already have, what is blocked, and what \"done\" means to them. This page is that, and the writing rules that make the questions actually go out as the owner."
when_to_use: "Use when the owner asks for this, in words like: \"probe <person> so we can scope out what the task is\", \"scope it out with him\", \"find out what he actually wants done\", \"go through and then scope it out\"."
metadata:
  summary: "Scoping a job out of someone in a DM"
---

# Scoping a job out of someone in a DM

This is the log play `inbox/scopeAJob`. Before anything else, call the log MCP tool `getGuide({ useCase: "inbox/scopeAJob" })`: it returns this page and makes it the session's play, so every log tool's answer says which step you are on and a send with no play loaded is refused (rules 157, 158). Then follow the steps in order.

Draft every message from that person's own thread and the owner's real replies (`voice` with no text, `search`), never from memory, and never send two that read alike (`sameAsSent`).

---
title: "Scoping a job out of someone in a DM"
---

# Scoping a job out of someone in a DM

Someone offers the owner a job in a chat. Before any number, any promise or any handover, the job has to be known: what it actually is, what they already have, what is blocked, and what "done" means to them. This page is that, and the writing rules that make the questions actually go out as the owner.

It is the front half of [triage](../log-inbox-triage/SKILL.md): triage hands a scoped job to whoever builds it, and this gets it scoped.

How the owner asks for it: "probe <person> so we can scope out what the task is", "scope it out with him", "find out what he actually wants done", "go through and then scope it out".

## Run it from a fresh context

Say: **"go on docs/useCases/inbox/scopeAJob.md for <the person>"**. The agent reads this page and runs the steps.

## The steps


| # | Step | Tool | Done when |
| --- | --- | --- | --- |
| 1 | Read them in full before asking anything: the whole thread, every file, sheet or screenshot they sent, what they have already built, what they are stuck on, and anything they have said about money | `chatsList` { account } to find the chat, then `messagesRead` { account, chat, limit: 120 } | what they have done, what is blocked, and what they are paying for, in a few lines |
| 2 | Read the artefacts they sent, not just the message about them: open the spreadsheet, the doc, the tracker, and say what it actually shows | `read`, the file's own tool (an `.xlsx` through the spreadsheet skill), `mediaView` | each artefact's real content, and the gap between it and the message |
| 3 | Pull how the owner really writes in that chat, before drafting a word | `voice` { to, with, context } with no text | his latest messages there, his real replies to things like it, and the chat's own length and burst |
| 4 | Ask the open scope questions, as short lines in his shape, one question per line, and gate the whole draft | `voice` { to, with, context, text }, then the send | every line he would plausibly have typed, and `pass` |
| 5 | Claim the chat and send it one message per line | `inboxClaim`, `messagesSendLive` { account, chat, text, approvedBy: "<owner>", confirmLive: true } | the platform answers `sent` for every line |
| 6 | Stay on it until the scope is closed: read their answer, ask the next thing, never a second question the first one already answered | the chat, read before every reply | what it is, what is done, what is blocked, what done looks like, and the constraints |
| 7 | Tell the owner what the job now is, with the unknowns still in it named | the reply to the owner | one line per open question, and what only he can answer (usually the price) |

## The questions worth asking

Only what the thread has not already answered. In practice, in this order:

- **The artefacts.** What it is they are working from, and can they send the whole thing (source, tests, evidence, receipts), not a summary of it. Without it the work starts from nothing.
- **The stated blocker.** When they say it "needs live recordings" or "needs X", what exactly is recorded or done, and by whom — that is usually the real cost of the job.
- **Whether the original still works.** For anything that has to match an original's behaviour, whether that original still runs on the current build. If it does not, parity cannot be measured, and that changes the job completely.
- **What is actually in scope.** The part they first named is often not the whole thing, and sometimes not the part they are stuck on.
- **What "done" is to them.** Finished to a stage, or a build they can run themselves. Their answer sets the size of the job, not the owner's guess.
- **Money, last, and only as a fact.** What they can pay is a fact to bring back; the number to charge is the owner's call.

## Writing it so it goes out

- **A wall of text fails the gate, and it should.** The voice gate grades a draft as the messages it will be sent as, against the owner's real length and burst in that chat (`docs/specs/voiceGate.md`, REQ-VOICE-20). Six short lines score; one long paragraph does not.
- **A burst of short lines and a run of questions is normal in a DM.** His X guide (6 to 20 words, one line, no question) does not describe a chat, and the gate scopes it to his vocabulary outside X (REQ-VOICE-22).
- **A subject he has never written about is not a voice problem.** New nouns are new vocabulary, not phrasing that is not his (REQ-VOICE-21). Do not launder the subject out of the message to make the gate happy: that produces a message about nothing.
- **Draft from `voice` with no text first.** It gives his real replies to things like what they just said, which is what the gate is asking the draft to read like.
- **Do not re-ask what the thread answered.** It reads as not having listened, and it wastes the exchange.

## What the runs taught

- **The gate failing six times was a data problem and a shape problem, not a wording problem.** On 2026-11-12 a scoping message to a Discord DM scored `voice` 0.16 to 0.66 over seven drafts. The voice index held no pairs for that chat, so the gate graded the owner as a stranger and treated a two-day conversation as a first message; once the chat was indexed, the same draft scored 0.85. The other half was shape: six lines read as one wall of text scored 0.22, and as six messages 0.85.
- **A gate refusal is a signal to check the evidence, not only the words.** Before rewriting a fifth time, read `voice` with no text: if his latest messages there are empty, the gate has nothing to compare against and no phrasing will pass.
- **The scope is usually in the artefact they already sent.** On 2026-11-12 the whole job — the stages, the two blocked substeps, the counts that already passed — was in one spreadsheet the person had sent two days earlier, and the open questions were only about the artefacts, the blocker and what "done" meant.
- **A play must be loaded before sending as the owner,** and a session that changed models mid-thread loses it: a send with no play is refused `playMissing`.
- **It runs on whichever platform they wrote on.** `chatsList`, `messagesRead` and `messagesSendLive` take the platform from the account, so the same steps read and answer a chat on X, Discord, Slack or Instagram.


## Next

- Handing the scoped job to whoever builds it is [triage.md](../log-inbox-triage/SKILL.md).
- Sending a brief rather than a reply is [bossMaxxing.md](../log-inbox-boss-maxxing/SKILL.md).

## Related

- Up: [All use cases](https://github.com/matthewdonsemail-lab/log/blob/main/docs/useCases/README.md)
- [Connect your agent](https://github.com/matthewdonsemail-lab/log/blob/main/docs/mcp.md) · [Trust](https://github.com/matthewdonsemail-lab/log/blob/main/docs/trust.md)

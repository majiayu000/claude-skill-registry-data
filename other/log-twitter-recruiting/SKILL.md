---
name: log-twitter-recruiting
description: "Recruiting on X with a reply queue. A log play (docs/useCases/twitter/recruiting.md): Find people who just posted that they want work, or who already do the job. Reply to each one publicly with one line in their own language, about their own post, ending with the job link. The owner approves the list, then the queue sends the replies slowly with likes mixed in. Applicants then come in through the job page."
when_to_use: "Use when the owner asks for this, in words like: \"recruit for the <role> role on x\", \"find people looking for work on twitter and reply with the job link\", \"hire a <role> through tweet replies\"."
metadata:
  summary: "Recruiting on X with a reply queue"
---

# Recruiting on X with a reply queue

This is the log play `twitter/recruiting`. Before anything else, call the log MCP tool `getGuide({ useCase: "twitter/recruiting" })`: it returns this page and makes it the session's play, so every log tool's answer says which step you are on and a send with no play loaded is refused (rules 157, 158). Then follow the steps in order.

Draft every message from that person's own thread and the owner's real replies (`voice` with no text, `search`), never from memory, and never send two that read alike (`sameAsSent`).

Find people who just posted that they want work, or who already do the job. Reply to each one publicly with one line in their own language, about their own post, ending with the job link. The owner approves the list, then the queue sends the replies slowly with likes mixed in. Applicants then come in through the job page.

Recruiting is public replies only. DMs are a different job: [dmInbox.md](../log-twitter-dm-inbox/SKILL.md) and [engagerDms.md](../log-twitter-engager-dms/SKILL.md).

How the owner asks for it: "recruit for the <role> role on x", "find people looking for work on twitter and reply with the job link", "hire a <role> through tweet replies".

## Run it from a fresh context

Say: **"go on docs/useCases/twitter/recruiting.md for the <role> role"**. The agent then:

1. Reads this page, then [README.md](https://github.com/matthewdonsemail-lab/log/blob/main/docs/useCases/twitter/README.md) for the queue and the rules on every X page.
2. Gets the role from the owner: its job link, where to hire, the languages.
3. Runs the steps below to the end. It keeps searching until it has qualified people, shows the table, and sends once the owner says yes. "Nobody qualified" means search wider, not stop.

| Role | Job link | Where the people are | Languages |
| --- | --- | --- | --- |
| e.g. a remote appointment setter who calls businesses in English | `<role link>` | the regions you hire in | e.g. `lang:es` |

## What "qualified" means

All five, checked on every person before they go in the table:

1. **Language and freshness:** the post really is in the role's language (X's language tag is sometimes wrong), and it was posted in the last few days.
2. **Location:** the profile's location is in the role's regions. No location means no contact: hold them and list them separately.
3. **A real person:** not a news, brand, job board, government or meme account.
4. **Work signal:** they say they're looking for work, or the bio or post shows they did the job themselves (for a calling role: call center, telemarketing, sales, setter or closer work).
5. **Never contacted:** not in any earlier send log, and not replied to by the account before (see the README's one-reply rule).

## The steps


| # | Step | Tool | Done when |
| --- | --- | --- | --- |
| 0 | Is the account signed in | `twitterSessionCheck` { account } | `loggedIn` |
| 1 | Search: the role's language plus one work word per query, last few days, `-filter:retweets` | [treg](https://treg.to/?ref=matthewdonse-aebsh)'s X post search, many queries in parallel | a pool of authors, minus everyone already contacted |
| 2 | Read every profile | treg's X profile read, in parallel | location, bio and followers for each one |
| 3 | Qualify them with the five checks | by hand, or a model scoring fit, region and real person | a keep list, plus a "no location" hold list |
| 4 | Write one line per person, in their language, opening on their own post, ending with the link | house style | every line passes `twitterQueueCheck` |
| 5 | Show the owner the table: handle, location, why, post url, the line | wherever the owner reads | the owner says yes |
| 6 | Queue it: each target carries its own `text`, build, check, approve, plan with likes, dry run, live run | the README's queue steps: `twitterQueueBuild`, `twitterQueueRunLive` | the run is `finished` |
| 7 | Log and report every reply url, or X's event | the queue file, a send log | every item says sent, skipped or blocked |
| 8 | Check applicants | wherever the job page sends applications | new applicants reported |

### Search terms

A language-only search (`lang:es` alone) brings back noise: TV, football and greetings. Each query needs one work word.

- **es:** busco trabajo, necesito trabajo, busco chamba, trabajo remoto, ventas, vendedor, call center, telemarketing, cold calling, setter, closer, bilingüe, agente outbound, cobranza, and the names of the big call-center employers in the region
- **tl:** naghahanap ng trabaho, virtual assistant, VA, freelancer
- **hi:** नौकरी चाहिए, job chahiye, virtual assistant, CRM, data entry
- **any:** CRM, lead gen, n8n, Make, Airtable

### What a line looks like

Opening on their own post, then the offer and the link:

> jaja esas historias del call son eternas y si te interesa volver pero desde casa estamos contratando cold callers remotos que llaman a negocios de estados unidos en inglés para agendar citas 👉 `<role link>`

## What the runs taught

- **Never search without a work word.** A language-only sweep returned posts all from the same minute: a sample of the language, not candidates.
- **Check location before every send.** Early runs reached people outside the hiring regions; now no location means hold.
- **Most hits aren't candidates.** In a large Spanish call-center sweep, most posts were complaints about call centers, support accounts and news. Expect a handful of qualified people per few hundred authors.
- **Generic copy gets dropped.** The same template line with a link came back as "no tweet created"; a line about the person's own post went through. Write each line for its post.
- **Use the queue, never a hand loop.** A hand loop lost a reply; the queue keeps every item, stops on X's first refusal with the item still pending, and picks up where it stopped when the owner runs it again.

## Running it unattended

The same steps can run on a schedule with nobody watching: search, skip anyone seen or contacted, read profiles, let a model score fit, region and real person against thresholds, have a model write one line per person about their post, then build, approve under the owner's standing yes, plan and run the queue. Keep each run's candidates, decisions, targets and queue together, and read its result with `twitterQueueStatus`. Make sure only one sender runs on an account at a time.

## Next

- [#39](https://github.com/matthewdonsemail-lab/log/issues/39) tracks who answered a recruiting reply. Until then, applicants show up wherever the job page stores them.

## Related

- Up: [All use cases](https://github.com/matthewdonsemail-lab/log/blob/main/docs/useCases/README.md)
- [All X use cases, and the parts they share](https://github.com/matthewdonsemail-lab/log/blob/main/docs/useCases/twitter/README.md)
- [What log does on X](https://github.com/matthewdonsemail-lab/log/blob/main/docs/platformGuides/x.md)
- [Connect your agent](https://github.com/matthewdonsemail-lab/log/blob/main/docs/mcp.md) · [Trust](https://github.com/matthewdonsemail-lab/log/blob/main/docs/trust.md)

> Some links in this play carry ListeningKit's referral or affiliate credit (a `ref=` or `aff=` code). They cost the owner nothing extra; use the plain address without the code if you prefer.

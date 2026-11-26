---
name: xPosting
description: Run an X account the way the owner runs @xAccount, from any account. Add the account to Twenty with `log twitter cookies save` (masked prompt, checked with X), give it a copy style, then post originals by the social posting playbook (Cap, Parakeet, FilmCraft, the X discipline) and reach people through `log twitter` replies, quotes, likes, dms and the queue. Use to set up an X account, to post or reply on X, and when adding a new X workflow, copy style or editing rule.
---

# xPosting

One page for everything an X account does. Each account in Twenty runs the
same setup. The other skills and docs hold the detail. This page says which
one to open, and where a new workflow or style goes.

## 1. Set up an account (once per account)

| Step | Command | Where it lands |
| --- | --- | --- |
| Copy `auth_token`, `ct0` and `twid` from a browser signed in to x.com (DevTools → Application → Cookies → `https://x.com`) | none | your clipboard only |
| Save them, checked with X first | `log twitter cookies save --account <handle> [--style house] [--name "<label>"]` in a terminal (a masked Clack prompt; never a flag, never over MCP) | Twenty `socialAccounts`: a TWITTER row with `accountName` = handle, `cookies`, `sessionState`, `copyStyle` |
| Check it any time | `log twitter session check --account <handle>` (MCP `twitterSession`) | `sessionState` in Twenty, and the governor in `~/.logCli/twitter/<handle>` |
| X Chat PIN, to read encrypted DMs | `log twitter chat pin --account <handle>` in a terminal | `socialAccounts.messengerPin` |

The cookies are saved only when X answers loggedIn for that same handle. A
refused or wrong-account paste saves nothing. Each check merges X's refreshed
cookies back into the row. The cookies live in Twenty only, and are never
printed, committed or put in the knowledge base.

## 2. Original posts: the social posting playbook

Every original post (a video) follows the **Social posting playbook**:
record in Cap, caption with Cap's Parakeet model, cut in FilmCraft by the
awesome-video-editing rules, export at -16 LUFS, then post by the X
discipline (original first, the first 2 hours, the first likes, answer every
comment, the quote an hour later).

- Repo: `listeningkit-frontend`, `docs/okf/operations/social-posting-playbook.md`
  (branch `docs/social-posting-playbook`).
- Twenty: Notes → "Social posting playbook" in your own Twenty.
- Knowledge base: `log kb search "social posting playbook"`.

Post the original with `log twitter post --account <handle> --text "<copy>" --media <video.mp4>` (MCP `twitterPost`, `twitterPostLive`).
It is a dry run first: it checks the copy against the account's style, and checks the file's type and size,
without contacting X. `--live --approvedBy <who>` uploads the file and posts.
A video is uploaded in chunks, and the post is made only once X's own processing says succeeded.
It takes one video or gif, or up to 4 images. Everything after the post goes through log-cli as well:
the replies to its comments, the quote an hour later, and the DMs to the people who liked it.

## 3. Reaching people: `log twitter`

**Send what X's own client sends.** Every GraphQL call uses
X's live operation ids and feature switches, read from X's signed-in
client with `log twitter session webClient --account <a>` into
`~/.logCli/twitter/xOperations.json`. Run it again when X ships a new
main.js. What X's composer sends is in `docs/platforms/x/compose.md`.

**The account stays live in context.** While its X Chat watch
runs, the account reads X's own badge counts every 2 minutes, the way
x.com does, and reads the new notifications when the count rises. Each
Claude session gets what is new in a `>>> X LIVE` block. A reply, quote
or mention there is someone talking to the owner: read them and answer.
How it works: `docs/platforms/x/live.md`.

**Full context before every message (rule 109).** Before you write to
anyone, and again right before it goes out, know everything between them
and the account at that moment, never only the dm thread:

- `twitterDms` { account, with: "<handle>" } gives their whole thread (old
  DMs and X Chat, read from X itself, so it also holds what the owner sent them
  from the owner's phone or anywhere outside log) **and** what they did on the
  account's posts: likes, retweets, replies (with what they said), quotes,
  mentions and follows, newest first, from a fresh notifications read.
- Draft from all of it. Someone who already retweeted gets thanked for it,
  never asked to retweet; someone who replied gets their reply answered.
- The queue reads it all again right before each send and holds the item
  (status `held`, with what changed) if anything happened since it was
  drafted. A held item is redrafted from the new context, gated with
  `voice`, and put back with `twitterQueueEdit`. A queue file is never edited
  by hand, and nothing is sent around the queue to get past a hold.

Each job has its own page in `docs/useCases/twitter/`: topic replies,
answering the people who comment on your posts, DMs to the people who like
or repost them, affiliate follow-ups, recruiting, the inbox and followers.
The parts every page uses:

- **Finding:** treg's X search, profile and posts reads (rule 53). X itself is never used to search.
- **One send:** `log twitter reply|quote|like|dm --account <handle> …` is a
  dry run. `--live --approvedBy <who>` sends it. A dm drafted on several
  lines goes out one message per line, with the owner's usual gap between them,
  and the queue sends dms the same way (rule 90); `--asOne` only when the owner
  asks. A drop stops the rest, and nothing is resent (rule 94).
- **Reading the inbox:** `log twitter dms --account <handle>` syncs: the
  first read takes the whole inbox once (about 20 s) and keeps it in
  `~/.logCli/twitter/<handle>/inboxSync.json`; every read after asks X only
  for what is newer than the newest event held (one request when nothing is
  new, about 1.3 s in the engine) and decrypts only what is new. Each read
  keeps its conversations for `log search` and updates the index in the
  background with only the chunks that changed. `--full` reads everything
  again. The live watcher (`log twitter chat watch --inbox`) writes each
  pushed message into the same store, and the SessionStart hook says who is
  waiting from it with nothing fetched.
- **More than one:** the queue: `log twitter queue build → show → check →
  approve → plan → run → run --live`. It spaces sends at random, at least
  minGap apart, and any refusal from X stops the run with the item pending
  (rule 94, [docs/specs/xQueue.md](../../docs/specs/xQueue.md)). Before any DM
  it drops people the account has already talked to on X Chat (rule 109).
- **One session per account (rule 105):** every X call goes through the
  account's one engine host (`python/twitterApi/host.py`). The first call starts
  it; every call after, from the CLI, MCP, hooks, the queue or the X Chat watch,
  is answered by that same session (one client, one connection, one transaction
  key), one call at a time: a send 4 to 11 s after the last call, a read 0.8
  to 2.5 s. The answer's
  `xSession` names it (pid, since, calls), and the hook's account line shows it.
  A second session can't start. If the host can't be reached the call is
  refused (`xSessionHostDown`) and nothing is sent: read
  `~/.logCli/twitter/<account>/host.log`, never work around it. More than one
  send goes through the queue, never a hand-rolled loop (rule 105). The whole
  contract: [docs/specs/xSession.md](../../docs/specs/xSession.md).
- **Pacing:** 240 writes a day per account, kept by the account's governor.
  `--force` goes past it only when the owner says so (rule 86). See
  [docs/specs/writeBudgets.md](../../docs/specs/writeBudgets.md).

## 3b. The growth loop (how the owner grows @xAccount)

What worked for the owner (`log kb show memory:-buzz/listeningkit-real-state`): a
text post about treg ("$10 -> 30 conversations") did 205K views and 1,182
likes, and the account's followers went from 308 to 352 in four days. The owner then turned
the attention into conversations. Every account runs the same loop, in this
order:

| # | When | What | How |
| --- | --- | --- | --- |
| 1 | Post day | One original post. The text carries it (a video open counts almost nothing). One best post per feed window, when the audience is online, never several in a row | the social posting playbook (section 2), sent by hand |
| 2 | The first 2 hours | Answer every comment. Unanswered questions are the best openers. Replies between mutuals score highest | `docs/useCases/twitter/engagementReplies.md`: treg comments read, then a queue of replies |
| 3 | About 1 hour after | Quote a matching trend, never before your own post | playbook "Riding a trend", `log twitter quote` |
| 4 | The next days | DM the people who liked or reposted it, opening with one of their own tweets, then one informal line | `docs/useCases/twitter/engagerDms.md` (the first-DM way), queue `action: dm` |
| 5 | Every day | Reply to people posting about your topic, one line about their post backed by your own fact, inside the account's 240 writes a day | `docs/useCases/twitter/topicReplies.md`, the queue's `limit` |
| 6 | Always | Answer whoever writes back. Never send a cold template to someone you already talk to | `log twitter dms --account <a> [--with <handle>]`, `chat watch` (needs the X Chat PIN), rule 109 |
| 7 | Weekly | Score the followers (treg profiles and their posts), and talk to the best ones by hand | `docs/useCases/twitter/followers.md`, treg `anyapi.x.user.profile` |
| 8 | Always | Leads from posts and DMs go into Twenty | `agencyProspects` |

Finding people and posts is always treg (`treg call anyapi.x.search.posts
--file q.json`, `anyapi.x.user.profile`, `treg.x.user.posts`). On Windows,
pass `--file` rather than `--data`, and set `PYTHONUTF8=1`. A big treg sweep
costs money: say the price first.

**Each account's own plan.** The loop is how to post and follow up. What an
account posts about comes from its own plan:

| Account | Plan | What it sets |
| --- | --- | --- |
| your main account | its plan in the knowledge base (`log kb search "<account> plan"`) | the product, the people it is for, the follower atlas |
| a teammate's account | the teammate's own social growth plan | positioning, content pillars and their ratio, the hook and CTA banks, the 30-day and 90-day plans, DM openers, leads in Twenty, the weekly review |

Where they disagree, the X discipline wins on X. The plan's comment
prompts ("comment your AI stack") read as engagement bait there, so on X
ask a real question in the post instead. A first DM opens on their own
tweet. The plan's DM opener is for someone who has
already commented.

**Voice.** `log voice` gates drafts against the owner's own writing. Its guide
and the owner's saved conversations are on the owner's machine, so on any other account it
judges by the owner's voice. For an account of your own, write in its
`copyStyle`, and keep each line about the other person's post.

## 4. Copy styles

Every send and every queue check holds its copy to the account's
`copyStyle` (Twenty `socialAccounts.copyStyle`; empty means `house`):

| Style | Rules |
| --- | --- |
| `house` | The owner's: lowercase only, no commas, semicolons, full stops, em or en dashes. URLs are exempt |

To give an account another style, set `copyStyle` in Twenty, or pass
`--style` to `cookies save`. A send names the style that failed and why.
`--skipStyleCheck` skips the check only when the owner approved the copy
word for word.

## 5. Adding to this setup (for the next agent)

Add each new piece in the same place every time, so every account gets it:

- **A new copy style:** add one entry to `COPY_STYLES` in
  `src/twitter/copy/style/client.ts` (its `name`, `summary` and a
  `problems(text)` check), with a test in `style.test.ts` and a row in the
  table above. Accounts pick it up through `copyStyle`.
- **A new X workflow** (a job like topic replies): write
  `docs/useCases/twitter/<job>.md` in the same shape as the others (what to
  read, which tools in order, what counts as done), and add its row to
  `docs/useCases/twitter/README.md`.
- **A posting or editing rule** (recording, captions, the cut, the export,
  when and how to post): change the social posting playbook, in the repo and
  the Twenty note together. Then link anything new from section 2 here.
- **A new X command:** `src/cli/twitter/helpers/<name>.ts` on the direct-API
  engine (`DIRECT_ROUTES`, `COMMAND_RULES`), never a browser.

Then run `log kb sync`. This skill, the use cases and the docs go into
Twenty's knowledge base and its Redis search, and every agent finds them
with `log kb search`.

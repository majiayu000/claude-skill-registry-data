---
name: telegram-research
description: >-
  Searches public Telegram for what people said about a subject: finds the channels and groups
  discussing it, learns their words, reads the posts, each with a t.me permalink and a date. Also
  one named channel or group - recent posts, whole history, one t.me link, or whether it exists.
  Triggers - what do people say on Telegram about, find Telegram channels or groups on a topic, read
  this public channel, a month of posts, search a channel's history, open this t.me link, does this
  channel exist, what do they call it there, check this claim on Telegram, Telegram report with
  sources, Telegram account frozen, Telegram budget left. Russian - поищи в телеге, что пишут в
  телеграме, найди телеграм-каналы, что говорят в чате про, найди посты в телеграме, почитай этот
  канал, открой ссылку t.me, есть ли такой канал, как это называют в чатах, проверь по телеграму,
  отчёт по телеграму с источниками, телеграм-аккаунт заморожен, сколько осталось лимита. Not for
  sending, joining or private chats; not a post archive.
allowed-tools: Read, Write, Edit, Glob, Grep, Agent, WebSearch, WebFetch, Bash(python:*), Bash(python3:*)
---

# Telegram research

Three questions, in this order and never mixed: **which channels and groups talk about this** (discovery),
**what words do they use for it** (query craft), **what was actually said** (reading). Step 2 has no input
until step 1 has produced a corpus to mine, and step 3 finds the wrong half of what exists if step 2 is skipped.

## Finding the scripts

Everything runs through `scripts/tg.py`, beside this file. Resolve its path once, at the start of a run:

```bash
for p in "${CLAUDE_SKILL_DIR}" ~/.claude/skills/telegram-research ~/.agents/skills/telegram-research \
         ./.claude/skills/telegram-research ./.agents/skills/telegram-research; do
  [ -n "$p" ] && [ -f "$p/scripts/tg.py" ] && { TG="$p/scripts/tg.py"; break; }
done
if [ -z "$TG" ]; then
  echo "telegram-research: no scripts/tg.py in \$CLAUDE_SKILL_DIR, nor in .claude/skills/telegram-research" >&2
  echo "or .agents/skills/telegram-research under ~ or ./ - set CLAUDE_SKILL_DIR to the folder holding" >&2
  echo "SKILL.md, or run from the project root the skill is installed in." >&2
  exit 7
fi
if command -v python3 >/dev/null 2>&1; then python3 "$TG" selftest; else python "$TG" selftest; fi
```

**The refusal is the load-bearing half.** Without it an unmatched loop leaves `$TG` empty, the interpreter is
handed no file, and the shell returns **1** — the one code this skill never produces deliberately, so the
failure reads as "the skill is broken" when it means "it was run from somewhere it cannot see itself from".
**7** is this skill's operator error, and the message names both fixes. (`CLAUDE_SKILL_DIR` is not an
environment variable: the agent substitutes the real skill directory into this text as it loads it, and an
agent that does not leaves it empty, so `[ -n "$p" ]` skips that candidate and the four standard locations
are tried.)

**Then keep using whichever interpreter that last line ran, spelled out.** `python3` is tried first because it
is the name that means Python 3 everywhere: macOS has shipped it and no bare `python` since 12.3, and where a
bare `python` does exist it is sometimes Python 2, which dies on the first command with a syntax error and
exit **1** — the code this skill reserves for a crash. Both names are allowed, but the allow-list matches the
literal word: a variable holding the interpreter's name matches neither entry and the call is refused before
it runs. **Every `tg.py …` below means `python3 "$TG" …` or `python "$TG" …`** — interpreter first, nothing
before it; the program sets its own streams to UTF-8, so an encoding prefix buys nothing.

**Python 3.9 or newer** is all that is needed until the account is used. The account path needs Telethon, and
**this skill never installs it** — `pip install telethon` is the operator's decision; `scripts/account.py` says whether it
is there. **Run `selftest` first**: it parses the saved probe pages (25 assertions, no network, any working
directory) and separates "Telegram changed its front end" from "we broke something", exiting **9** when a
parser no longer matches the pages — never 0 and never 1.

## The rule everything follows

**A channel is free. A group has no free search surface at all, so searching one goes through the account —
cheaply, and with no resolve.**

**And the one thing to carry from the whole file: `contacts.resolveUsername` is the only call that has ever
cost real downtime here.** Sixteen of them in under seven minutes bought a freeze of 36 468 seconds, and all
sixteen returned success while the account was already dead. Nothing on an ordinary path reaches it; the full
account rules are at the end of this file and in `references/account.md`.

| what you want | the command | what it costs |
| --- | --- | --- |
| does this name exist, channel or group | `verify` | 1 GET per name |
| search a channel's history | `search` | 1 GET per page of hits. **Cannot promise completeness — see the cap below** |
| walk a channel's history | `history` | 1 GET per 20 messages |
| **search a group** | `search` — same command, the registry's `type` picks the surface | 1 account call per page of ≤100 hits, plus 1 to find the peer the first time. **0 resolves** |
| **read a group's recent messages** | `history` — same command, same routing | 1 account call per 100 messages |
| one message you already have the id of | `group --id N` | 1 GET per id |

`search` and `history` are each one command over two surfaces, and the registry's `type` is what picks between
them. "What do they say about X" is `search`; "what are they talking about right now" is `history`, which no
query answers.

**Verification is mandatory before a group, not before every read.** A channel needs no preparation at all:
`search` and `history` work on a name the registry has never seen. A group is only sent to the account when a
registry line types it `group`, so an unverified one goes to the free `/s/` page instead — which normally
redirects, and the command refuses at **exit 6** naming `verify --write` as the fix. Where it does not
redirect, the page carries no messages and reads like a quiet channel, which is the failure that matters. So:
**`tg.py verify <name> --write` before working with a group.** (`group --id` on a name the registry types
`channel` is refused at exit 6 the same way.)

For a channel the account is **never** touched — a rule, not an optimisation. There is no flag for guessing a
group's message ids either: about one in a hundred answers, so finding ten messages carrying one word costs
more requests than the group has ids. `references/surfaces.md` is the operating manual, with the measurements
behind every number here; read it before the first request of a run, not after something returns nothing.

## State, and where it lives

State lives in **`~/.telegram-research/`** — outside every project and outside the skill's own folder: the
shared source registry, the resolve ledger, the account lock, the peer cache and their journals. **That
location is the point.** An installer update replaces the skill's folder wholesale, so a ledger kept inside it
would go with it — taking the record of an account freeze, the one thing that stops the next run from
repeating it. The trade runs the other way too: **removing the skill leaves `~/.telegram-research` behind**,
and deleting it is the operator's call. Every file in there by name, the environment variables that move any
of it, and the three different things a relative path is anchored on, are in `references/cli.md`.

**The working directory decides nothing else either.** `--root` is the project run folders are created under,
defaulting to the project this skill is installed in — **except on a global install**, under `~/.claude` or
`~/.agents`, where there is no project above the skill and the working directory is used instead. Every path
printed is absolute, so the `next:` hint works from any shell. **Tell the operator to add `telegram-runs/` to
the project's `.gitignore`**: nothing puts it there, and a run folder holds fetched pages and notes.

## Commands

One program, thirteen subcommands, JSON on stdout from every one of them. A whole run, in order — which is
also the order of the stages below:

```
tg.py --root <root> newrun --question "..." --topic <topic> --depth deep --lang <lang> --geo <CC>
tg.py --run <run> discover --lyzem-query "..." --account-query "..." --from-file page.txt --found-via web
tg.py --run <run> verify <name> <name> --write --found-via account
tg.py --run <run> search <channel-or-group> --query "..."   # or history <name>, or group <name> --id N
tg.py note <run> --agent telegram --text "..."              # then report <run>, then accept <run>
```

Stage 3 wraps that fourth line in `tg.py queries <run> start|record|accept`, the only thing enforcing the
round ceiling, the yield floor and the drift ban. **Every flag, every default, every exit code and the run
folder's layout are in `references/cli.md`** — read it before the first command, not after a result comes back
carrying a field you cannot place. Three things from it first: global flags (`--root`, `--run`,
`--max-requests`) go **before** the subcommand; **`--run` is what makes a run a run**, because without it no
page is saved and nothing the report quotes can be checked; and **exit 1 is never produced on purpose**, so a
1 is a crash and never a verdict.

## Three zeroes that are not silence

This is the reason the skill exists. A quiet channel, a broken parser and a capped surface print numbers that
look alike, and an agent writes that likeness into a report as a fact about what people said.

**1. `found_nothing: true` is a real zero; `found: 0` is not.** A `found: 0` after a failed fetch, a refused
argument or a stopped walk reports only that nothing arrived — never write "nothing was said" from it. The
verdict is structural: a page carrying `data-post` can never assert its own silence, so a post quoting
Telegram's own "no messages found" string cannot turn twenty real posts into proven absence. **Only two routes
assert silence at all, and each has its own field.** A channel `search` prints `found_nothing` — that is the
assertion, and no other command prints the field. A group `search` asserts through Telegram's own count instead:
`found: 0` with `server_total: 0` and `complete: true`. `history` and `group` assert nothing, ever, so a zero
from either is a zero and not a silence.

**2. `understood_nothing` / `blocks_unparsed` mean Telegram changed, never that the channel is quiet.**
Both belong to the web walks and are printed by `search` and `history` **on a channel** — the account routes and
`group --id` parse no preview page and carry neither. A page whose blocks stopped yielding `data-post` parses as
zero messages with a live cursor — byte-identical on stdout to a genuinely quiet channel. `blocks_unparsed`
counts blocks that went unread across the walk. `understood_nothing` is the verdict that a FULL page yielded
nothing usable, in either of its two shapes: the blocks were there and none of them parsed, or every block
parsed and not one carried text — the second is what a moved text selector looks like, and it can therefore
appear beside a healthy-looking `found`. It sets `stop_reason: "understood_nothing"`, and it is deliberately
blind on a short page, where a thin result is ordinary rather than suspicious. **Non-zero `blocks_unparsed` with
`understood_nothing: false` is the early warning** — part of a page stopped parsing and nothing has broken
loudly yet. Either way the finding is about the selector table and Telegram's front end, never about the
channel; `selftest` separates the two in one offline command.

**3. A full `search` result is not a complete one — check `partial`.** The `?q=` surface fills its first page
and then stops serving: no cursor, and paging past the last hit returns nothing. What separates that cap from
a real ending is the FIRST page — short means that was all there was; full and then stopped is the surface's
own ceiling. When the cap fires, `search` prints `surface_truncated: true`, `stop_reason: "surface_cap"` and
`exhausted: false` per query, and at the top of the object `partial: true`, a `warning`, and `surface_truncated`
a second time — **the same key, two types**: a bool inside each query, the list of the queries it bit on above
them. **Report those hits as SOME of the matches and never as a count.** If the number matters — "how
often", "how many people", "did anyone ever" — only a `history` walk can answer it, and a silence from a
capped search is not a silence at all. Measurements: `references/surfaces.md`.

**And a message count is not an id count.** An album is ONE message block carrying several ids, which Telegram
serves only as `?single` permalinks inside the block. `found` counts blocks, `ids_seen` counts distinct ids,
and every record carries `ids` — every id that block accounts for, `[id]` for an ordinary post. **Anything
counting posts, filling a requested number of them, or deciding "the page was short, so that was the end"
reads `ids` / `ids_seen`, never `len(messages)`.**

**`stop_reason` is a closed set of nine, and which value it is decides how the zero reads.** `found_nothing` is
the only one that asserts silence. Three more are zeroes that do not: `understood_nothing`, `surface_cap`, and
`no_messages` — the preview page came back without a single message block, which is a statement about the fetch
and the front end, never about the channel. Three are real endings, in descending strength: `first_post`,
`until_id`, `no_more_pages`. Two are stops rather than endings: `page_ceiling`, the ceiling you set, and `aborted` — the walk was cut
short by the request ceiling, a stop signal from the surface, or Ctrl-C.

## Stages

### 1. Scope

`tg.py newrun` writes question, language, geography, window and depth into the brief; there is a flag for each,
and `--brief <file.json>` hands one in whole. **`--depth` is a decision, not a label** — it sets the round
ceiling, the new-post floor and the request ceiling at once (`quick` 1/3/133, `normal` 3/3/400, `deep`
5/2/800, the middle row being the configured `budgets`; the table and what a `--brief` inherits are in
`references/cli.md`), and `--max-rounds`, `--min-new-posts` and `--max-requests` override any of them.

### 2. Find sources

**Not one resolve happens here.** One account call does, and it is the cheap one. Run the three discovery
channels together and merge, because each is blind where the others are not:

| channel | how | what it searches | blind spot |
| --- | --- | --- | --- |
| the account's search box | `discover --account-query "..."` — 1 call, **0 resolves** | titles and usernames | **never sees inside a message**; a group whose title does not name the subject is missed |
| web search | your own tools, then `discover --from-file page.txt --found-via web` | post text — engines index `t.me/s/<channel>` | **channels only**; a group's messages are not published on the web at all |
| `lyzem` | `discover --lyzem-query "..."` — groups, channels and messages, one GET each | post text, plus titles and descriptions | thin, erratic and stale: 9 of 30 names measured were dead, whole groups are absent, and it matches by OR rather than as a phrase, so its result count is a union and not about your query |

Catalogue sites are a dead end at the search step — the big ones are closed, 403 or down; links inside found
posts (`--found-via link`) need a corpus first. `--account-query` pays twice: the peers it returns are cached
with their access hashes, so a group it finds is searchable afterwards **without a resolve**.
**`corroborated: true` counts only the channels used in that one command**, and `--found-via` defaults to
`web` for `discover`, so a catalogue page labels itself `web` unless you say otherwise and then two
"different" channels are one.

Then **verify every candidate**: `tg.py verify <name> --write`. One free GET each, and not a formality: none of
the three channels gives a reliable type or audience size, and a third of the names one of them produced did
not exist at all. **`--write` is what puts the line in the registry** — and for a group that line is what
routes the read. A source under `--min-channel-members` / `--min-group-members` is refused
admission — as is one whose member count did not parse, because a floor that cannot be applied is not waived.
A dead name the registry has never seen is rejected outright and leaves no row at all, so a third of the
candidates from one discovery channel cost the same GET again on the next run. **A contradicted `type` needs
`verify`, and only `verify`**: any ordinary write that would flip a stored `type` is refused, because a type
changing underneath a run turns every later refusal into a mystery. The rows a `verify` writes and the two
fields that report a partial job — `topics_vocabulary_missing` and `type_conflict` — are in
`references/cli.md`.

**A name that has not passed verification may never go to a resolve** — a resolve spent on a nonexistent name
costs exactly what a successful one costs, out of the budget whose exhaustion once froze the account for ten
hours. **And no third-party service is ever proof of absence**: "lyzem found nothing" means "its index holds
nothing". Write it that way in the report; the two are not the same sentence.

### 3. Query craft

`references/query-craft.md` in full; the short form: **move 1** is what you can invent (synonyms,
transliteration, mixed alphabets, misspellings, local institution names) — cheap, worth doing, and it will
never produce the word you actually need. **Move 2** is what the corpus knows: read a couple of hundred posts
near the subject and extract what the people there **call** the thing. In some Russian-speaking chats a bribe
is «рахмет», a borrowed word for "thanks"; no amount of thinking produces that, and one page of their own text
hands it over. **Move 3 onwards is a loop** — search on the new word, and its results carry the next layer.

The three stoppers are enforced by `tg.py queries`, and only by it:

```
tg.py queries <run> start --query "..."          # opens a round; refuses a drifting query
tg.py --run <run> search <channel> --query "..." # spend the round
tg.py queries <run> record [--top N]             # mine the corpus, check the yield floor
tg.py queries <run> accept --term <word> --gloss "..."
tg.py queries <run> show                         # the log, and whether it may continue
```

**Round ceiling** and **yield floor** are checked by `start`, which refuses with the reason and exits **3** —
as it also does when every query it was handed is rejected as drift, so a 3 here is one of three refusals, not
one; `record` prints the ceiling and floor verdict as `may_continue` / `why_not`, so that stop is visible
before the next `start`.
The **drift ban** requires a query to appear verbatim in retrieved text — the whole phrase, words side by side
in this order, inside ONE post; round 1 is seeded from the question, since the ban keys on a corpus that does
not exist yet. Its exact rules (short words, `OR`, inflection, `ё`/`е`) are in `references/query-craft.md`.

`record` mines the corpus, excluding the question's own words and every query already used **by stem, not exact
match** — this stage exists to find what the question could **not** have said. Every cut is reported in
`mining`, and a batch smaller than the floor says in words that nothing could have been mined whatever the
posts said, so `[]` is never mistaken for "this corpus has no jargon". What it prints is evidence, not a
decision. Skipping the stage is allowed and visible: `tg.py accept` — the run gate, not `queries accept` —
warns that all three stoppers bound nothing.

### 4. Read

- **Channel, targeted:** `tg.py search <name> --query "..."`. Check `partial` before writing any count down,
  `found_nothing` before writing any silence down.
- **Channel, full history:** `tg.py history <name>`, only when genuinely needed. `--write` stores the newest
  id read; `--since-last` next time so it never re-reads what the first run paid for. Only
  `reached_first_post` means the channel is fully read; the other three endings are weaker claims.
- **`--write` moves the cursor only when the walk reached an end it can prove**, and a walk stopped by
  `--max-pages` or by the request ceiling writes nothing. A high-water mark written after a bounded walk makes
  the unread middle unreachable for ever and then reports `reached_until_id: true` about it: the cost of not
  advancing is re-reading, the cost of advancing wrongly is silent loss. The cursor fields, the four endings
  and `cursor_may_be_stale` are in `references/cli.md`.
- **Group, searched:** the same `search` command, routed by `type` to `messages.search` — server-side full-text
  over the whole history, with Russian morphology. `server_total` is Telegram's own count of matches, so
  `complete: false` means what it says and `--max-pages` is what to raise — a group is the one route where
  raising it does anything, the channel walks being capped at 25 whatever you pass.
- **Group, recent messages:** the same `history` command — one call per 100 messages, newest first, obeying the
  same cursor rule. **Pass `--max-pages 1` when one call is what you meant**: the default is 25, and the walk
  keeps paying until a page comes back short.
- **Group, one known id:** `tg.py group <name> --id N` — one GET, no account, for an id out of a permalink or a
  citation. `missing_ids` names ids that answered nothing, which is **ordinary** (124 consecutive empty ids
  were measured between two live messages) and never evidence of silence. `unreadable_ids` is the third
  answer and a different fact: the page came back and carried no message this parser could read — a login
  wall, or a front end that moved. **Never fold it into `missing_ids`**, and run `selftest` when it is not
  empty.
- **Group, bulk history:** the account, from Python. There is no CLI for a bulk read, deliberately — see
  `references/account.md`.

### 5. Extract

Every post carries a permalink `t.me/<name>/<id>`, a date verbatim from the page, the text, the author, and
`ids`. Several more fields exist because the text alone loses what they carry — `links`, `media_posters`,
`found_by`, the quoted message a group thread cannot be read back without, `is_service`, `media`,
`reactions`, `forwarded_from`, `source_file`. **`references/cli.md` lists all of them, and which route
carries which**: a post that arrived through the account has none of the page-only ones, so `source_file:
null` and empty `links` on a group `search` are the route showing, not a parse failure. The same file lists
what to read **before believing a thin result** — `dropped` and `silent_cuts` on `discover`,
`type_corrections` on `verify`, `mismatched_ids` on `group`, `posts_suppressed_as_duplicates` on the three
reading commands.

### 6. Report, and closing the run

`report` writes the skeleton from what the folder holds, and keeps apart three states it must never blur:
"no word could be mined", "stage 3 did not run", and "the query log is on disk and cannot be read". **You
write the judgement**: what was found, what the jargon means, what a silence implies. Do not let the template
write those sentences — and copy your prose somewhere before re-running `report`, which refuses at exit 10
over a finished report precisely because the skeleton would replace every sentence you wrote.

**A run is not finished until `note` and `accept` have run**, and nothing writes either by itself. `accept`
reads nothing but the run folder — no other skill, no external script — writes `acceptance.json` and the gate
record, and exits **8** if the folder would fail. Warnings are normal and their count is a property of the
folder, not a target; `errors=0` is the thing to check. What it demands is in `references/cli.md`.

## Being called from inside a subagent

1. **Never ask a question.** No `AskUserQuestion`, no waiting on a person: a subagent cannot ask, so a run that
   needs an answer mid-flight is a run that hangs. Everything uncertain is settled in the brief, and
   `--caller agent` records that this is the case.
2. **Your fan-out spends the run's budget, not its own.** Nothing counts agents — no ceiling in the brief
   applies to them. What binds them is `--max-requests`: `run.json` accumulates the spend of every process
   sharing that `--run`, so agents launched under one run draw down one ceiling between them, and a branch that
   plans as if it had a fresh budget takes it from the branch beside it.

The posts are primary sources with URLs and dates; the report's judgements are the agent's, and nothing in the
run folder marks which is which.

## What this skill does not do

- **No post archive**, and **no storage beyond working state** — registry, cursors, resolve ledger and peer
  cache are necessary, without them the skill is dangerous to the account, and they are not a knowledge base.
- **No money.** No Stars, no Premium, no paid API. `allow_paid_stars` is forced off after every config layer
  has spoken and checked again at the transport boundary; no config file can introduce the key.
- **No pretending a group is a channel.** **No private chats** — every surface here is a public page anyone
  can open.
- **No sending, joining as a side effect, or member harvesting.** Joining is an explicit operation with its
  own daily ceiling (3).

The parsing, discovery and pacing layers are this skill's own code; the one borrowed dependency is Telethon,
for MTProto, and only on the account path.

## The account

**Read `references/account.md` before touching it at all.** The one thing to carry without reading:
**`contacts.resolveUsername` is the only call that has ever cost real downtime.** Sixteen of them in under
seven minutes bought a 36 468-second freeze, and all sixteen returned success while the account was already
dead. It is no longer on any ordinary path — `contacts.search` returns the peer AND its access_hash in one
call, cached for the life of the login, so a group search costs `resolves: 0`, printed on every answer.
Reaching a resolve at all means writing a script under `references/account.md`, not passing a flag.

Three subcommands reach the account and only three — `search <group>`, `history <group>`,
`discover --account-query` — all bounded, all refusing **before** they read the credential unless
`TELEGRAM_RESEARCH_ALLOW_LIVE` is set. Live mode needs two switches: `allow_live=True` in code **and** that
variable set to `1/true/yes/on`, read at every call rather than once at construction, so turning it off stops a
run already going. **From the command line there is no third state**: without the variable the command refuses
at exit **7** and no account path opens. The dry run is a Python-API mode, described with the rest of the
account's own flags in `references/cli.md`.

`tg.py budget` says what has been spent today and whether the account is frozen — **both freezes**, the
resolve ledger's and the history log's, and the second is the one a command line can actually earn: all three
account subcommands gate on it. No network call, no credential read, so it is always safe to ask. Its `--unfreeze --reason "..."` exists for a freeze that was
never Telegram's (a wrong clock, a test) and cannot tell that from a real one; **it is not a way to argue with
a FloodWait, and waiting is the only thing that ends one.** What it prints, the `recorded: false` that has to
be read, and what `scripts/account.py` adds to it are in `references/cli.md`.

## Reference files

| file | read it when |
| --- | --- |
| `references/cli.md` | before the first command; whenever a flag, an exit code or a field needs checking |
| `references/surfaces.md` | before the first request; when a parse returns nothing |
| `references/query-craft.md` | stage 3, every time |
| `references/account.md` | before any MTProto call, without exception |
| `references/topics.json` | the classifier vocabulary; per-project overrides go through `TELEGRAM_RESEARCH_CONFIG`, not by editing this file |
| `tests/fixtures/probes/` | the 10 saved real pages `selftest` parses. The full 32-page corpus and the pytest suite live in the project repository, outside this folder, and are not installed |

**What is still not known**, so that nobody re-derives it: where `t.me` starts refusing us by IP has never been
measured — the 2-4 s pace and the single thread are a guess, not a finding; the `lyzem` index has never been
sized; `Post not found` on a group that exists may be a deletion or a message type this surface cannot render,
with nothing on the page to tell the two apart; and **where `contacts.search` and `messages.search` start being
rate-limited** — thirteen calls in one session passed cleanly and that says nothing about a hundred, so both
are paced and counted like `getHistory`, which is borrowed policy rather than a finding. **And the album branch
is unguarded**: not one of the saved probe pages carries a grouped-message wrapper, so the id-splitting that
`ids` / `ids_seen` rest on was measured live once and `selftest` cannot notice it breaking. Treat an album count
as the one number the offline check does not stand behind.

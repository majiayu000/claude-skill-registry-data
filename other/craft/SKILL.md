---
name: craft
description: Use when a product idea is still vague and needs to become a clear definition of what to build — "let's craft an app like X", "help me define what I actually want", "clarify this idea before we plan it". Also use before planning or implementation when requirements, UX, domain behaviour, or technical preferences have not been decided. Not for planning, task breakdown, or writing code.
argument-hint: "[ui|file]"
---

# Crafting Skill

You are a **product discovery, design clarification, architecture discovery, and decision-capture skill** for Claude Code / Codex CLI.

Your purpose is to transform a vague application idea into a **clear representation of what I actually want**.

You do **not** implement the application.

You do **not** create an implementation plan.

You do **not** break the work into coding tasks, phases, milestones, tickets, or execution steps.

Another skill is responsible for planning and implementation.

Your responsibility is to give that skill enough information that it does not need to guess my intentions.

---

# Core objective

When I say something like:

> "Let's craft an application similar to Spotify."

do not interpret that as:

> "Build Spotify."

Instead, interpret it as:

> "Help me define exactly what my version of this product should be."

The reference application is only an initial point of reference.

Your job is to discover:

* what I want;
* what I do not want;
* how the application should behave;
* how it should look and feel;
* what users should be able to do;
* what important technical preferences I have;
* what constraints exist;
* what decisions are still unresolved.

The final result of crafting should represent **my vision**, not the LLM's assumptions.

---

# Primary rule

## Ask instead of assume

Whenever a meaningful decision is ambiguous, surface it.

Do not silently decide important product, UX, design, data, architecture, security, or behavioural choices.

At the same time, do not ask pointless questions about implementation details that another agent can safely decide later.

Focus on decisions that materially influence what gets built.

---

# Main workflow

## 1. Understand the initial idea

Read my request and identify:

* the product category;
* the main purpose;
* likely users;
* major product areas;
* reference products or concepts;
* obvious ambiguities;
* decisions that would significantly change the resulting application.

If the repository already exists, inspect it before asking technical questions.

Use existing project information when it is reliable.

Do not ask me questions whose answers are already obvious from the repository.

---

# 2. Create a crafting file

Instead of asking dozens of questions interactively, create:

`CRAFT.md`

This file becomes the central workspace for the crafting process.

It should contain a structured questionnaire tailored specifically to the product being discussed.

I should be able to open the file, answer many questions at once, save it, and then ask you to review it.

Do not generate a generic universal questionnaire without adapting it to the application.

That questionnaire is what **file mode** puts in `CRAFT.md`. In browser
mode it does not go there at all — §2b decides which, and it decides first.

---

# 2b. Delivery — the browser, or the file

There is a browser front-end for this skill. Decide **once, at the start of
the session**, how questions reach me. Say which mode you are in, in one
line, and then stay in it.

* `/superb:craft ui` — the browser. `/superb:craft file` — `CRAFT.md`.
* With no argument: try the browser, fall back to the file.

**Everything else in this file applies identically in both modes** — question
design, the four importance levels, the areas to explore, challenging my
thinking, the strict boundaries, the three end statuses. Only the surface I
answer on changes.

Below, `$SKILL` is the directory this file lives in. Your harness tells you
when it loads this skill — the line reading *"Base directory for this skill:"*.
Use that absolute path. Do not guess it, and do not search for it: you will be
running from my project directory, not from the skill's, and a wrong guess
looks exactly like the UI being unavailable.

**Before either mode writes anything, know where it is writing.** Crafting is
the skill that runs before a project exists, and `CRAFT.md`, `.craft/` and
`--project-dir .` all mean the working directory. If that directory is not a
git repo, ask me where the brief should live before you start — otherwise
"let's craft an app like Spotify", typed at home, puts the session and a
`.gitignore` in `$HOME`.

## Starting the browser

```sh
python3 "$SKILL/ui/craftui.py" serve --project-dir . --open
```

It prints one line of JSON. Give me the **complete** `url` from it, query
string included — the session key lives in that query string and the server
refuses every request that arrives without it.

Then add `.craft/` to my project's `.gitignore` if nothing there covers it
already, and say so in one line.

Say one more thing in that first message: **the terminal stays mine while I
answer.** The page carries the round in front of me and nothing else, so if I
want to change my mind about something I settled two rounds ago, telling you
here is how — there is no history screen in the page, deliberately, and you
fold what I say in the terminal into the next round like any other answer.

**Falling back is never a failure.** No `python3`, a `serve` that fails, or a
`LOCKED` you cannot clear → say so in one line and carry on in file mode. A
crafting session is never blocked by a web server.

`LOCKED` means a craft session holds this project **right now**. The lock is
held by the kernel, so it cannot be stale, and there is no override flag — do
not invent one. But whose session it is decides what you do, so **run
`status`** before you fall back:

* `"server": true` — a craft session is **live on this project**. A craft
  server holds the lock for its whole life, so a live server here *is* the
  holder `LOCKED` named (`ps -p <that pid> -o args=` names this project, if
  you want it confirmed). Almost always it is mine, left running from earlier —
  the server outlives the terminal by up to four hours. **Ask me before you
  stop it**, in one line: *"a craft session is already live on this project
  (pid N) — shall I take it over?"* You cannot tell my leftover from a session
  I am running in another window, and stopping the second one loses whatever I
  have typed there. On yes: `stop`, then `serve`, then give me the new URL.
  **Do not fall back to file mode here either way**: that tab is open in front
  of me rendering `CRAFT.md`, and writing the questionnaire into it is exactly
  the two-places problem *What this changes about what you write* forbids.
* `"server": false` — a session that is not answering: someone else's, or one
  still starting up. Tell me the pid, let me decide whether to stop it, and go
  on in file mode meanwhile.

One exception to both: a `LOCKED` immediately after a `stop` that said
`NOSERVER` is that server still draining its last write. Try `serve` once
more before you report anything.

## What this changes about what you write

**In browser mode, `CRAFT.md` holds the accumulated brief and nothing else.
Never the questionnaire.** The questions live in
`.craft/round-NNN.questions.json`. The page shows me the brief beside the
questions and re-reads it every round, so I watch it grow as I answer — which
is exactly what a questionnaire pasted into it would bury.

In file mode, `CRAFT.md` holds both, exactly as §2 describes.

Writing the questionnaire into `CRAFT.md` while a browser session is live
means I answer the same questions in two places and you fold in two
conflicting sets. Do not do it, however helpful it looks.

## Resuming

`.craft/` outlives this conversation, and the second morning is where that
bites. **Run `status` before you write a round.** If `round` is null, nothing
has been crafted here and the loop below starts at 1. If it is not null, a
craft is already in progress, and starting at 1 anyway is the worst move
available: yesterday's `round-001.answers.json` is still on disk, so `wait
--round 1` comes back `SUBMITTED` in a twentieth of a second. You then fold in
yesterday's answers as if I had just given them, overwrite them, and race
forward a round at a time — while I sit looking at a page showing round 3,
having touched nothing.

So say what `status` found — the round it is on, and how many REQUIRED
questions its `open` still counts — and then do one of two things, never both:

* **Resume** at `round + 1`. `CRAFT.md` is the brief I left; the existing
  answers files are there to re-read if the last session ended before folding
  them in.
* **Start fresh**, which means deleting `.craft/round-*` first, and saying so.
  A round file left behind is a round `wait` can answer without me.

If which of the two I want is not obvious from what I have just said, ask.

## Before the first round: technical discovery

For a **software project whose stack is not yet decided**, dispatch
**`superb:architecture-discovery`** once — after the idea is stated, before
round 1. Hand it the idea, the product category, whatever inspecting the
repository told you, and the technical category list from *Preferred
technologies*. It returns candidate questions in the round-file shape, ready to
merge with the ones you wrote.

Name it with the `superb:` prefix. A bare `architecture-discovery` resolves to
whatever personal agent happens to exist, which may have been written for
something else entirely.

**Once per session, not once per round.** Rounds are supposed to shrink; a fresh
discovery pass every round works against that.

**Skip it** when the project is not software, when the stack is already settled
by the repository or by what I have already told you, or when it is unavailable —
in which case generate the technical questions inline against the layer table in
*Preferred technologies*. Its absence must never block a round.

**It proposes; it does not decide.** If it returns prose, a recommendation, or a
chosen stack rather than questions, discard that part. The decisions are mine.

**Validate what it returns before merging it.** Its questions go into a round
file, and a round file that fails `validate_round` is refused wholesale — one
malformed option from the agent loses the questions you wrote too. Check every
returned question against *The round file* below: uppercase `importance`,
options as objects with a `value` string, a `type` from the allowed four. Fix or
drop the ones that fail; never pass them through untouched.

## The loop

1. Write `.craft/round-NNN.questions.json`.
2. Run `python3 "$SKILL/ui/craftui.py" wait --project-dir . --round NNN --timeout 90`
   **and wait for it inside this turn.** Do not end your turn on it, and do not
   background it with `&`. Do not poll in a tight loop, and do not ask me in chat
   what I am answering in the browser.

   **Why this wording is exact.** `wait` is an ordinary blocking process. Whether
   ending your turn works at all is a property of the harness you are running on,
   which this skill cannot see: where a finished background task starts a new turn
   you would be woken, and where completion only lands in a mailbox nothing drains,
   the session parks until I type something. That is the reported failure — *"I had
   to go to the CLI and say already replied, next wave."* Waiting in your own turn
   behaves the same on both. It is also why this used to fail only sometimes:
   "background command" reads as either the harness's background-task mechanism or
   a shell `&`, and a `&` returns instantly with nothing left to wake you.

   **Waiting is executing, not stopping.** A wait is a tool call; your turn has not
   ended and no question is owed.

   **Ninety seconds is not arbitrary, and raising it breaks this.** A harness
   runs a command in the foreground only up to its own limit and backgrounds
   anything longer — Claude Code's default is 120 seconds. A wait set near or
   above that limit is backgrounded, which is precisely the parking failure
   above, reintroduced by the fix meant to remove it. Stay comfortably underneath
   whatever your harness's *default* foreground window is; do not raise the
   timeout to reduce re-arms.

   Each `TIMEOUT` costs one line of output and one tool call. Re-arming twenty
   times is cheap; being backgrounded once is the bug.
3. Act on the one line it prints. Fold the answers into `CRAFT.md`, then write
   the next round **in the same turn**. The questionnaire gets **smaller** every
   pass, exactly as *Second pass* says.

### When the loop ends

Five conditions, and nothing else:

| Condition | Signal | What you do |
| --------- | ------ | ----------- |
| I pressed Finish | exit `0` `FINISHED` | Final fold, then *Ending*. **`FINISHED` outranks every row below** — I have stopped answering, so a still-open REQUIRED question does not buy another round. Report `MORE CLARIFICATION NEEDED` naming it, and `stop`. |
| Converged | zero open REQUIRED and zero IMPORTANT **across the brief, not the round** | Write the closing round — empty `questions`, a real `note` — then `stop`. |
| Unrecoverable | exit `1` `ERROR`, or `64` | **Never re-arm.** Fix it, or fall back to file mode. |
| No progress | two consecutive rounds yielding no new confirmed or delegated decision | Stop and say so. A third ask is arguing with someone who has decided not to answer. |

`TIMEOUT` (exit `2`) is none of these. It is the heartbeat: re-arm in the same turn.

Exit `3` `NOSERVER` splits. If I am plainly present — I just typed — re-`serve`
and re-arm. If this round already timed out once, the four-hour idle shutdown has
fired: stop, and tell me how to restart.

| Round cap reached | 12 rounds | Stop and say the shrink rule is not working. |

**Count the rounds from disk, not from memory:** `ls .craft/round-*.questions.json
| wc -l`. Nothing in the server enforces this — `MAX_ROUND` is 999 — and a
resumed session has no recollection of how many rounds already happened. The cap
is a bug detector, not a budget: reaching it means rounds stopped shrinking, so
say that rather than starting round 13.

**"Converged" is a property of the brief, not of the last round.** `count_open`
scores one round's unanswered questions, so a round where I answered everything
reports zero open while the brief is still missing whole sections. Check the
brief — that is what `check-brief.sh` is for.

### Every question must be objective

**The test:** blank the `title` and keep only the `options`. If a reader can
still tell what is being decided, the options are concrete.

| Fails | Passes |
| ----- | ------ |
| `["modern", "traditional"]` | `["React", "Vue", "Svelte", "no framework"]` |
| `["scalable", "simple"]` | `["PostgreSQL", "SQLite", "DynamoDB"]` |
| `["good UX", "fast"]` | `["one page per step", "one long form", "a wizard modal"]` |

Adjectives are not options. They describe how someone feels about a choice
rather than naming the choice, and an answer to them cannot be written down as
a decision — which means the next round has to ask again in different words.

**One decision per question.** "What's your stack?" is six questions wearing one
coat, and it gets a shrug.

**Every question earns its place.** If both answers produce the same software,
do not ask it.

### A delegated decision still has to be written down

*You decide* closes the question, not the decision. A bare delegation loses the
reasoning permanently: nobody downstream can tell what was considered, so the
first person to disagree has to redo the thinking from nothing.

Every Delegated Decision carries four things:

* the options that were on the table;
* craft's recommendation, as the default;
* the constraints the choice has to respect;
* what goes wrong if it is chosen badly.

**Set `delegable: false` explicitly on every REQUIRED question.** The page's
default is unconditional — omit the key and a *you decide* button appears on a
question only I can answer — so this is yours to write, not something the UI
infers from importance.

A delegated REQUIRED is not a delegation, it is a scope reduction: if it could
be delegated it was never required. Either lower its importance honestly, or
record the answer in Confirmed Decisions.

### The round file

`round` — an integer, and it must equal the NNN in the filename. The server
compares them and refuses the round if they disagree, because the page picks
a round by filename and would otherwise write its answers over another one.

`questions` — a list. Each entry is an object:

| Field | |
|---|---|
| `id` | required; unique within the round |
| `importance` | required — `REQUIRED` / `IMPORTANT` / `PREFERENCE` / `OPTIONAL` |
| `title` | required, non-empty — the question itself |
| `type` | required — `single` / `multi` / `text` / `longtext` |
| `options` | required for `single` and `multi`: a non-empty list of objects, each with a non-blank string `value` |
| `area`, `why` | optional; `why` is the *why this matters* §4 asks for |
| `allow_other` | optional boolean, **default false** — `single` and `multi` only. Set it to `true` to give me a free-text box beside your options, for when none of them is what I mean |
| `delegable` | optional boolean, **default true, unconditionally** — every question gets a *you decide* button unless you set this to `false`, and the page does not look at `importance`, so **write `false` yourself on every REQUIRED question**. Set it `false` on the questions only I can answer: my budget, my users, what the product is for. A delegated answer becomes a Delegated Decision and is never asked again, so offering that on a question you cannot actually decide is worse than not offering it |

`note` — optional; one or two sentences in your own words, shown at the top
of the questions column. On the closing round *Ending* describes — the one
with an empty `questions` list — it is the whole page, so write it: it is
the last thing I read here, and a round with no questions and no note is a
blank screen.

`ledger` — optional, and it is where the confirmed decisions, assumptions,
contradictions and delegated decisions the sections below tell you to keep
become a sidebar I can read while I answer. Four keys — `decisions`,
`assumptions`, `contradictions`, `delegated` — and **each one must be a
list** of objects, each with an `id`. A contradiction may also carry
`between`, a list of question ids.

A round that breaks any of this is not served: I get an error in the browser
instead of questions. `status` prints the same complaint, field by field, so
run it if you are unsure what the page is refusing.

### What `wait` says

One line on stdout, and the exit code says the same thing as the line.

| Exit | Printed | What you do |
|---|---|---|
| 0 | `SUBMITTED round=N answers=…` | Read that file, fold it in, write round N+1. |
| 0 | `FINISHED round=N answers=…` | Read it, fold it in, then see *Ending*. |
| 2 | `TIMEOUT round=N` | **A heartbeat, not a failure** — I am still thinking. Run `wait` again. |
| 3 | `NOSERVER` | The server is gone. See *Restarting*. |
| 1 | `ERROR …` | A state waiting again cannot fix. Read the line; fix it, or fall back to file mode. |
| 64 | usage | You called the command wrong. Fix the command line. |

**Re-arm `wait` on 2, and never on 1 or 64.** A `TIMEOUT` is me still typing.
A `1` is a condition another wait cannot change, and `64` means the command
itself was malformed — that code exists precisely so you can tell it apart
from a heartbeat.

The other three commands share the codes. `serve`: `0` and a line of JSON,
`4` `LOCKED`, `1` `ERROR`. `stop`: `0` `STOPPED`, `3` `NOSERVER`, `1` if it
could not stop the server. `status` always exits `0` and prints one JSON
object describing the session — it writes nothing, so it is safe to run at
any point just to look.

### Restarting

`NOSERVER` has two causes, and only one of them wants a `serve`.

**If this round has already timed out on you at least once and nothing has
been sent** — no answers file, `status` showing its questions still `open` —
the server did not crash. It shut itself down after four hours of complete
silence, which is me having walked away. Tell me the session timed out after
four hours of quiet, offer to bring it back, and **stop there.** Do not
`serve` unprompted: another one is another four hours of `wait` re-arming
into an empty room.

**Otherwise** — no server was ever started here, or the one that was has just
gone while I was plainly still here — run `serve` again. It **mints a new key
every time**, and the key is in the URL, so the URL I already have is dead for
good and will keep answering 403. Give me the new one; do not tell me to
reload. Reusing the port changes nothing about that: a tab I left open 403s on
the right port just as thoroughly as on the wrong one.

And if I simply lose the URL while the session is still up, `stop` then
`serve` is the whole recovery. Nothing reprints a live key — `status` strips
it from the URL it reports, by design — and that is not a gap to work around.

## Reading the answers

`.craft/round-NNN.answers.json` carries `round`, `submitted_at`, `finished`,
and `answers` keyed by question id. Four states, and they are not the same
thing:

| In the file | Means |
|---|---|
| `choice` / `text` / `other` | Answered. Fold it in and close the question. |
| `"delegated": true` | **I do not care.** Record it under *Delegated Decisions* and never ask it again. |
| `"skipped": true` | Still open. Ask it again next round. |
| the id is absent | The same as skipped. |

A `note` is mine in my own words and can sit beside any of those. Fold it in
as a qualifier; never discard it because the `choice` next to it looked
sufficient.

## Ending

`FINISHED` means **I have stopped answering.** It does not mean the vision is
clear.

`CRAFT STATUS: VISION CLEAR` is **earned, not judged.** Two independent passes,
and both are required:

**1. The mechanical check.** Run
`python3 "$SKILL/skills/craft/check-brief.py" "$PWD"` — an absolute path to the
script and an explicit project directory. You run from the project, not from the
skill, so a bare `./check-brief.sh .` is either "command not found" or a check of
the wrong directory. Exit `0` is the only pass; `1` names the predicate that
failed and `2` means there is no readable brief. **Report its output, not your
impression of it** — the whole point of a script is that it gives the same
answer twice, and a summary of a check you ran is not the check.

**2. A fresh-context reviewer.** Dispatch an agent, hand it `CRAFT.md` **and
nothing else**, and ask what it still could not build from. This skill's own
completion criterion is that the brief be understandable by another LLM
*without access to the original conversation* — and only an agent that lacks the
transcript can test that. You have the transcript. You fail that precondition by
construction, so you cannot be the judge of it.

Whatever it still cannot answer becomes round N+1. Those are questions, not
footnotes on a finished brief.

If either pass fails, the status is `CRAFT STATUS: MORE CLARIFICATION NEEDED`,
and you say **which** pass failed and why. Naming unanswered REQUIRED questions
is part of that, not a substitute for it.

If you conclude the vision is clear before I press Finish, write a final
round with an empty `questions` list and a `note` saying so, then stop. The
page turns that round into the closing screen — my last screen of the
session, with the ledger beside it — and the `note` is all of it, so a round
with nothing in either is a blank page I am left staring at.

Either way, run `python3 "$SKILL/ui/craftui.py" stop --project-dir .` when
the session is over, so the project is free for the next one. Stopping is
not rude: once I have pressed Finish, or once a closing round has landed,
the page says the session is finished rather than waiting for you.

---

# 3. Tailor the questions to the product

The questions must depend on what we are building.

For example, for a Spotify-like application, meaningful topics might include:

* music playback;
* player behaviour;
* queues;
* playlists;
* albums;
* artists;
* favourites;
* libraries;
* search;
* recommendations;
* account behaviour;
* subscriptions;
* sharing;
* navigation;
* desktop/mobile layout;
* audio source;
* streaming behaviour.

For an Airbnb-like application, the questions would instead focus on areas such as:

* properties;
* hosts;
* guests;
* availability;
* bookings;
* maps;
* pricing;
* reviews;
* cancellation;
* payments.

For a project-management application, the domain questions would be completely different again.

Discover the product's natural domains and ask about those.

---

# 4. Question design

Each important question should make the decision easy to understand.

Prefer this structure:

```md
### [REQUIRED] How should users authenticate?

**Why this matters**

This determines onboarding behaviour, account recovery, and which identity infrastructure the application requires.

**Possible directions**

- [ ] Email and password
- [ ] Magic link
- [ ] Google
- [ ] Apple
- [ ] GitHub
- [ ] Multiple methods
- [ ] No accounts
- [ ] Other

**My decision**

> 
```

For technical choices, explain meaningful trade-offs.

Example:

```md
### [IMPORTANT] Should playback state persist between devices?

**Option A — Device-local state**

Simpler architecture. Each device has its own queue and playback position.

**Option B — Account-synchronised state**

Users can move between devices while preserving queue and playback information, but this requires server-side state and synchronisation.

**My decision**

>
```

Do not present false choices merely to make every question multiple-choice.

Use free-form questions where appropriate.

---

# Decision importance

Classify questions as:

### REQUIRED

The answer substantially defines the product or prevents another agent from understanding what should be built.

### IMPORTANT

The answer meaningfully affects the resulting architecture, UX, data model, or product behaviour.

### PREFERENCE

The answer mostly reflects personal taste or preferred experience.

### OPTIONAL

Useful detail, but another skill could safely make a reasonable decision later.

Prioritise REQUIRED and IMPORTANT questions.

Do not turn crafting into hundreds of low-value questions.

---

# Areas to explore

Use only the areas relevant to the application.

---

## Product vision

Clarify:

* What are we building?
* Why does it exist?
* Who is it for?
* What problem does it solve?
* What should make it useful or enjoyable?
* What should the product feel like?
* What existing products inspire it?
* Which parts of those products do I want?
* Which parts do I explicitly not want?
* What would make the result feel wrong even if technically functional?

Capture the spirit of the product, not just features.

---

## Scope

Clarify:

* essential functionality;
* desirable functionality;
* things that definitely should not exist;
* what belongs in the first version;
* what may exist later;
* whether the product is experimental, personal, commercial, internal, public, etc.

Do not create an implementation roadmap.

Scope describes **what belongs in the product**, not the order in which it should be built.

---

## Users

Understand:

* types of users;
* anonymous users;
* registered users;
* administrators;
* moderators;
* creators;
* customers;
* organisations;
* teams;
* guests;
* owners;
* collaborators.

Clarify what each user type can:

* see;
* create;
* edit;
* delete;
* share;
* manage.

---

## User journeys

Identify important user experiences.

For each major workflow, clarify what I expect to happen.

Examples:

* first visit;
* registration;
* onboarding;
* login;
* finding content;
* creating something;
* editing something;
* sharing;
* returning later;
* deleting something;
* recovering from an error.

Ask about behaviour and expectations rather than implementation details.

---

## Domain behaviour

Identify the important concepts in the application.

Ask detailed questions about how each one should behave.

For a Spotify-like product, this might include:

### Tracks

* What information should a track contain?
* Can users favourite tracks?
* Can they download them?
* Can tracks become unavailable?
* Are explicit tracks handled differently?

### Albums

* What information appears on an album?
* How should album tracks be ordered?
* Are multiple album editions supported?

### Artists

* What appears on an artist profile?
* Can users follow artists?
* Should related artists exist?

### Playlists

* Who can create playlists?
* Are playlists public, private, or both?
* Can multiple users edit one playlist?
* Can tracks be manually reordered?
* How does sharing work?

### Queue

* What happens when the user selects a track?
* What does "Play next" mean?
* What happens to manually queued tracks?
* Does the queue survive restarting the application?
* Does shuffle operate on the current queue or regenerate it?
* How should repeat behave?

Go deep enough that important product behaviour does not have to be invented later.

---

## Navigation and information architecture

Clarify:

* major sections;
* primary navigation;
* sidebar behaviour;
* tab behaviour;
* mobile navigation;
* menus;
* contextual actions;
* navigation hierarchy;
* back behaviour;
* deep linking;
* breadcrumbs if appropriate.

Determine how I mentally expect the application to be organised.

---

## Screens and views

Identify expected screens.

For each important screen, clarify:

* purpose;
* main information;
* primary actions;
* secondary actions;
* layout expectations;
* empty state;
* loading behaviour;
* error behaviour.

Do not generate implementation tasks for the screens.

---

## Interaction behaviour

Explore:

* click behaviour;
* double-click behaviour;
* hover behaviour;
* keyboard shortcuts;
* drag-and-drop;
* gestures;
* context menus;
* confirmation dialogs;
* inline editing;
* optimistic behaviour;
* undo behaviour.

Only ask where relevant.

---

## Visual direction

Clarify the desired design language.

Ask about:

* overall aesthetic;
* dark/light theme;
* colour direction;
* typography;
* density;
* spacing;
* corners;
* borders;
* shadows;
* animation;
* transitions;
* iconography;
* imagery;
* cards;
* layout style.

Ask separately about:

### Functional references

Products whose behaviour I like.

### Visual references

Products whose appearance I like.

Do not assume the two are the same.

---

## Responsive behaviour

Clarify:

* desktop;
* laptop;
* tablet;
* phone;
* native mobile;
* browser-only;
* desktop application.

Ask how layouts should change between form factors where this materially affects the product.

---

## Accounts and authentication

Clarify product expectations around:

* signup;
* login;
* logout;
* OAuth;
* passwords;
* magic links;
* MFA;
* onboarding;
* usernames;
* profiles;
* avatars;
* account recovery;
* account deletion;
* sessions;
* multiple devices.

The goal is to establish desired behaviour.

Do not create authentication implementation tasks.

---

## Permissions and privacy

Determine:

* public information;
* private information;
* shared information;
* ownership;
* editing permissions;
* administrative access;
* moderation;
* visibility rules.

Ask explicitly about ambiguous boundaries.

---

## Search and discovery

Where relevant, clarify:

* what can be searched;
* search results;
* filtering;
* sorting;
* autocomplete;
* search history;
* discovery;
* recommendations;
* trending content;
* personalised results.

Focus on what users should experience.

---

## Notifications

Clarify whether the product should use:

* in-app notifications;
* email;
* push;
* SMS;
* badges;
* notification centre;
* notification preferences.

Determine which events should trigger them.

---

## Payments and monetisation

If relevant, understand the desired product rules around:

* free access;
* subscriptions;
* plans;
* trials;
* paid features;
* usage limits;
* purchases;
* refunds;
* billing visibility.

Do not design the payment implementation unless a technical preference is part of my vision.

---

# Technical direction

Crafting should also capture technical preferences that materially constrain later decisions.

This is **not architecture planning**.

The purpose is to understand what I want the eventual architecture to respect.

---

## Platform

Clarify desired targets:

* web;
* mobile;
* desktop;
* API;
* CLI;
* browser extension;
* combinations of these.

---

## Preferred technologies

**Classify before you ask.** The `## Platform` answer determines which layers
exist, and a layer that does not exist must not be asked about:

| Platform answer | Layers present |
| --------------- | -------------- |
| web | frontend, backend, data, hosting |
| API only | backend, data, hosting |
| CLI | runtime, packaging, distribution |
| mobile | client, backend, data, hosting |
| desktop | client, local storage, packaging |
| browser extension | client, permissions, store distribution |

**If the shape is not yet known, that is the first question**, and it is
REQUIRED: is this a frontend, a backend, or a full-stack build? Everything below
depends on the answer, so ask it before the rest of this section.

**Then drill each present layer.** One decision per question — never "what's
your stack?", which is six questions wearing one coat and gets a shrug.

*Worked example, a full-stack web app:*

* **Frontend** — framework; rendering (SPA / SSR / static); styling; component
  library; state management, if the framework does not settle it.
* **Backend** — language; framework; API style (REST / GraphQL / RPC);
  background jobs, if a feature implies them.
* **Data** — database engine; relational or document; migrations; file and blob
  storage, if anything is uploaded; caching, if a feature implies it.
* **Auth** — provider or self-hosted; session or token; social logins.
* **Hosting** — platform; containerised or not; CI.
* **Cross-cutting** — package manager; language version floor; test framework.

Ask only about layers the platform answer put in play, and only where the answer
would change what gets built. A CLI has no frontend framework, and asking about
one tells me you did not read my answer.

If I do not care about an axis, record it exactly:

`No preference — planning skill may decide.`

That is a real answer, not a gap. Do not force me to make technical decisions I
deliberately want another skill to make — but do not leave an axis unrecorded
either, because silence and "no preference" are different states downstream: one
says I chose not to choose, the other says nobody asked.

---

## Existing technology constraints

Inspect the repository where possible.

Record existing facts such as:

* framework;
* language;
* package manager;
* database;
* styling system;
* testing framework;
* deployment configuration.

Ask whether existing technology should be retained only when that decision is genuinely unclear.

---

## Data expectations

Clarify product-level data requirements:

* important entities;
* ownership;
* relationships;
* persistence;
* history;
* deletion behaviour;
* sharing;
* synchronisation;
* offline behaviour.

Do not attempt to fully design the database schema unless I specifically want that decision made during crafting.

---

## Real-time behaviour

Ask whether users expect things to update immediately.

Examples:

* messages;
* collaborative editing;
* playback state;
* notifications;
* dashboards;
* presence;
* queues.

Capture expected behaviour rather than selecting the implementation technology.

---

## Offline behaviour

Determine whether:

* internet access is always assumed;
* some data should remain available offline;
* actions should queue offline;
* media should be downloadable;
* state should synchronise later.

---

## Performance expectations

Ask about expectations that affect the experience, such as:

* instant search;
* fast startup;
* seamless transitions;
* huge collections;
* many simultaneous users;
* large file uploads;
* real-time updates.

Do not prematurely design scaling infrastructure.

---

## Security and privacy expectations

Capture relevant requirements such as:

* sensitive information;
* private content;
* encryption expectations;
* child safety requirements;
* business data;
* account security;
* deletion guarantees;
* regulatory constraints.

If a requirement materially constrains later architecture, record it clearly.

---

## Integrations

Ask which external systems the product should interact with.

Examples:

* Google;
* Apple;
* Stripe;
* Spotify;
* GitHub;
* Slack;
* email providers;
* AI providers;
* maps;
* storage systems;
* external APIs.

Clarify desired behaviour and whether an integration is mandatory or merely acceptable.

---

# Recommendations

You may recommend choices when helpful.

However, recommendations must remain separate from my decisions.

Use:

```md
**Recommendation**

Use X because...

**Decision**

>
```

Do not silently turn your recommendation into a requirement.

If I explicitly delegate a choice to the LLM, record that clearly:

```md
**Decision:** Delegated to planning/architecture skill.
```

This is a valid answer.

---

# Assumptions

Maintain:

```md
## Assumptions
```

Any meaningful assumption must be visible.

Example:

```md
### ASSUMPTION-003

**Area:** Playback

**Assumption:** Playback continues when navigating between pages.

**Why this assumption exists:** Behaviour has not yet been specified.

**Impact if incorrect:** High

**Status:** Unconfirmed
```

Never silently convert an assumption into a confirmed requirement.

---

# Decisions

Maintain:

```md
## Confirmed Decisions
```

Record important confirmed answers.

Example:

```md
### DEC-014 — Playlist visibility

**Decision:** Playlists can be public or private.

**Details:** New playlists are private by default.

**Source:** User answer

**Status:** Confirmed
```

The purpose of the decision log is to give downstream agents an authoritative understanding of my choices.

---

# Open questions

Maintain:

```md
## Open Questions
```

Only meaningful unresolved decisions should remain here.

Group them by priority:

* REQUIRED
* IMPORTANT
* PREFERENCE

Avoid filling this section with implementation trivia.

---

# Contradictions

Review my answers for incompatible requirements.

Examples:

* completely offline application + mandatory server-side functionality;
* anonymous users + cross-device personalised state;
* no user accounts + private cloud-synchronised libraries;
* no external services + mandatory Google login.

Record contradictions rather than silently resolving them.

Use:

```md
## Contradiction: CON-002

**Decision A:** ...

**Decision B:** ...

**Why they conflict:** ...

**Resolution needed:** ...
```

---

# Second pass

When I have answered `CRAFT.md`, read the entire file again.

Do not regenerate the questionnaire.

Instead:

1. incorporate my answers;
2. mark decisions as confirmed;
3. remove or close questions that are resolved;
4. identify contradictions;
5. identify gaps;
6. identify things I may not have considered;
7. add only useful follow-up questions.

The questionnaire should become smaller and more precise with every pass.

---

# Challenge my thinking

Crafting is not merely form-filling.

Act as a strong product and technical thinking partner.

If I describe a feature that creates consequences I may not have considered, surface them.

Example:

If I say:

> "Anyone should be able to collaboratively edit playlists."

ask about:

* invitation model;
* edit permissions;
* ownership;
* removing collaborators;
* conflicting edits;
* visibility;
* abuse.

If I say:

> "Music should be downloadable."

ask about:

* offline playback;
* device limits;
* expiry;
* storage;
* ownership/licensing assumptions.

The purpose is to expose decisions, not to automatically solve them.

---

# Avoid premature implementation thinking

Do not transform every product decision into:

* database tables;
* API endpoints;
* tasks;
* tickets;
* milestones;
* files to create;
* coding sequence;
* implementation phases.

Those belong to other skills.

It is acceptable to mention a technical consequence when explaining why a decision matters.

For example:

> "Cross-device queue synchronisation will require some form of server-side state."

That is useful.

But do not continue into:

> "Create a Redis queue service, then implement endpoint X, then add worker Y."

That is outside crafting.

---

# Output of the crafting process

The final product of crafting is a **decision-rich product brief**, not an implementation plan.

When crafting is sufficiently complete, create or update:

`CRAFT.md`

so that it contains a clean consolidated section:

```md
# Crafted Product Definition

## Vision

## Product Principles

## Target Users

## Core Experience

## Scope

## Core Features

## Domain Behaviour

## User Journeys

## Navigation

## Screens and Views

## Interaction Behaviour

## Visual Direction

## Authentication Behaviour

## Permissions and Privacy

## Search and Discovery

## Notifications

## Monetisation

## Platform Requirements

## Technical Preferences

## Data Expectations

## Real-Time Expectations

## Offline Expectations

## Integrations

## Security and Privacy Requirements

## Constraints

## Explicit Non-Goals

## Confirmed Decisions

## Delegated Decisions

## Remaining Assumptions

## Open Questions
```

The final document should be understandable by another LLM without needing access to the original conversation.

---

# Delegated decisions

An important part of crafting is distinguishing between:

1. decisions I want to make;
2. decisions I want the LLM to recommend;
3. decisions I deliberately want to leave to another skill.

Maintain:

```md
## Delegated Decisions
```

Example:

```md
### Database technology

**Status:** Delegated

**Guidance:** Choose whatever best fits the confirmed product requirements.

**Constraints:** Must be easy to run locally and inexpensive for an initial deployment.
```

This prevents downstream agents from mistaking an unanswered question for an omission.

---

# Completion criteria

Crafting is complete when another capable LLM can read `CRAFT.md` and confidently understand:

* what I want to build;
* why I want it;
* who it is for;
* how the important workflows should behave;
* what the application should look and feel like;
* what functionality belongs in scope;
* what functionality does not belong in scope;
* what product rules must be respected;
* which technical choices I care about;
* which technical choices I do not care about;
* what constraints exist;
* what decisions have been delegated;
* what assumptions remain;
* whether any important contradictions remain.

The downstream LLM should still need to decide **how to implement the product**.

It should not need to guess **what product I wanted**.

That list is what the brief must **contain**. `check-brief.sh` is how it gets
**verified** — see *Ending*, which requires it plus a reader who was not here.

**A converged round is not a complete brief.** `count_answered` folds
`delegated` into settled, so fifteen *you decide* clicks report a fully answered
round over a brief that has recorded almost nothing. The counter measures one
round; the check measures the brief.

---

# Strict boundaries

During crafting:

**DO**

* inspect;
* question;
* challenge;
* clarify;
* compare alternatives;
* explain trade-offs;
* capture decisions;
* capture preferences;
* document constraints;
* identify ambiguity;
* identify contradictions;
* consolidate my vision.

**DO NOT**

* implement;
* write application code;
* create an implementation plan;
* produce coding phases;
* produce task lists;
* sequence development work;
* estimate development time;
* create tickets;
* decide every technical detail unnecessarily.

---

# Final status

At the end of each crafting pass, report:

* confirmed decisions;
* unresolved REQUIRED questions;
* unresolved IMPORTANT questions;
* assumptions requiring confirmation;
* contradictions requiring resolution;
* delegated decisions.

Then give one status:

`CRAFT STATUS: VISION CLEAR`

`CRAFT STATUS: MORE CLARIFICATION NEEDED`

or

`CRAFT STATUS: BLOCKED BY CONTRADICTION`

A status of `VISION CLEAR` means the product vision is sufficiently well defined for another skill to begin architecture or implementation planning.

It does **not** mean implementation should begin automatically.

---
name: feature-blueprint
description: >
  Designs a feature before code and produces its specification and implementation plan: how people
  use it (scenarios, states, errors, texts), how it works inside (data, failures, recovery,
  maintenance) and the steps with tests, grounded in research and sized to the project. For
  user-facing features (web, mobile, bots, AI agents and their tools, APIs) and internal mechanisms
  (backups, sync, queues, integrations). Use when the owner asks to work out, design, plan or write
  up a feature («прорабатываем», «спроектируй», «распиши фичу и план», «продумай или накидай, как
  сделать», «проверь план на дыры») or to build a new feature with no agreed plan yet. Not for
  discussing an idea («давай обсудим», «что думаешь»), a small point change (a button, a field, an
  option, a clear fix), a bug fix unless asked to work it out, or visual styling. The owner may
  write in any language; match on meaning.
metadata:
  version: "1.8.0"
---

# Feature specification

Given a feature idea, an agent builds the happy path and fills in the rest silently and badly:
"No data" with no next step, an endless spinner, a double charge after a double click, backups
nobody ever restored from, a sync that quietly stopped a month ago. You know how to avoid all of
this. This skill sets the order in which to think of it in time, how to work with the owner, and
the document format. The owner's explicit instruction in the conversation and the owner's own
rules, global or the project's, take precedence over this skill.

**Language.** This skill is in English. Everything the owner reads — the specification with the
template's headings, summaries, questions, plan lines, task records and comments, markers — is
written in the language the owner uses in the conversation. File, function and field names,
commands, paths, error codes, product names and section numbers stay as they are.

**Terms.**
- The *owner* decides what the product does. *Without a person* means nobody can answer during
  the run, as in an autonomous or scheduled run.
- The *specification* is the document from `references/document-template.md`; "section N" means
  its section N. *At a glance* is its first page, written for the owner.
- A *fork* is a decision that belongs to the owner, numbered F1, F2…
- A *ladder* is 2–4 levels of one solution, from the simplest to how big companies do it (step 7).
- Markers: [ASSUMPTION] — taken without confirmation; [VERIFY] and [MEASURE] — to check or measure
  in *step 0*, the first step of the plan; [NO SOURCE] — a decision with no ground found.

## Principles

1. **Draft first, then ask.** The owner came to hand off the thinking; a questionnaire hands it
   back. Read the idea in its most likely sense, fill the gaps with good practice, mark what you
   added and write the whole draft. Before the draft ask only what would force you to rewrite it
   (step 5). All other forks go to the owner afterwards in one message — the one checkpoint
   (step 12).
2. **The owner decides what changes the product; you decide the rest and show it.** The owner's:
   who gets what, money, user data and how much of it may be lost, irreversible actions, legal
   obligations, notable costs or the owner's time, the tone with customers, new settings and
   messages for people, and design that is hard to reverse — a new component, a new kind of
   storage, a background process or a way of integrating. Ask about every such fork, however many
   there are: one more clear question beats a weaker decision made for them. Explain what each
   option changes for the product, not which technology is better. What follows from the project,
   the platform, research or common practice is yours to decide; the decisions the owner could
   reasonably disagree with go into "Agent decisions — for review".
3. **Every key decision has ground and fits the project's scale.** Ground is a project fact,
   documentation or the practice of those who solved the same task; your taste and memory are
   not. A price, deadline, legal term, data volume or agreement with a partner you cannot ground
   is an [ASSUMPTION] or a question, never a confident number. Choose the simplest solution that
   meets the goals at this project's scale and name the measurable condition for moving up.
   Agent time is never an argument: options differ by minutes or hours of an agent's work, so do
   not drop an option, defer needed work or pick a method because it is quicker; choose by what
   people get, reliability, complexity and maintenance, money and the owner's time. The scope is
   everything without which the feature works wrong, loses data or fails silently, and it is
   built in full.
4. **Add nothing to people that nobody asked for, and bypass nothing quietly.** A new setting,
   switch, command, button, confirmation, or a message to anyone other than the person acting,
   costs attention, so it is the owner's fork with a "without it" option; by default the system
   behaves sensibly and does not ask when a mistake can be undone. What the person acting needs
   to get through — states, error texts, cancelling a long operation, notice of success and
   failure, confirming the irreversible — is behaviour: build it without asking. Your own
   implementation instead of an existing module, a new dependency or a second path for the same
   thing is shown to the owner with the reason the existing one did not fit; if it locks the
   design in, adds maintenance or failure points, it is a fork.

## Size of the task

Name the size in one sentence before you start; the owner may correct it.

| What came in | What to do |
|---|---|
| A small point change: a button, a field, an option or setting, a clear fix | No specification, file or task record in a tracker. Study the affected code, write in the chat in a few lines what you will change and how you will check it, and do it at once. Stop before the change only on an important point — an owner's decision beyond what they asked (principle 2); money, access, a data migration or what other systems read; a change bigger than it looked — and agree it per "How to ask the owner". Example: §4 of `references/examples.md` |
| A feature: a new scenario, screen, bot command, integration or internal mechanism | A full specification per the template |
| Several independent features in one idea | Say so, propose an order and write a specification for each |

If the work grows along the way, stop, say so and move up a size.

## Order of work

### 1. Intake

- The owner is only discussing the idea — discuss, do not write a specification. An agreed
  specification already exists — build by it, without a new round of questions; if it has no
  task record, make one per step 13 before you start. A draft from an earlier session — continue
  it in the same file.
- After a discussion, the inputs are only what the owner said or chose in their own words. "Ok",
  a clarifying question or a request to work it out confirms nothing you recommended. Your
  unconfirmed recommendation that changes the product is a fork that goes first: before the draft
  if it passes step 5, otherwise as F1. A technical one goes into "Agent decisions — for review"
  marked "from the discussion, unconfirmed".
- Incoming materials — documents, chats, files, archives, links — go through intake first, the
  way the owner's or the project's rules set it; with no such rule, read all of them. Read in full
  what the feature rests on, images in PDFs and slides included, and tell the owner at once what
  could not be opened and what passwords, keys or personal data you found. Those never go into
  the specification. `docs/` holds only our plans, specifications and reports.
- From the materials, take what is wanted and for whom, the constraints, who decided what and
  when, and the questions to third parties. The owner's word, agreed documents and what the client
  demands in their own documents are requirements; drafts and our own proposals are hypotheses. A
  contradiction between sources or people is a fork. A technical instruction given in passing
  ("do it on Redis") is checked once against the project and the research: if it fits, take it;
  if not, it is a fork that says what it changes for the product.
- Before research, restate the task to yourself — what is wanted, for whom, what success is — so
  you do not research the wrong thing.

### 2. Reconnaissance

Find in the project:

- how it already solves what the feature needs, so the same things behave the same and nothing is
  built twice; decisions the project has made outrank your taste, and a departure needs a reason;
- the feature's neighbours — functions that work with the same data, person, channel or time;
- where the work goes when it is done: which environments exist — a stage or test server,
  production, or none, when the project is only developed and run locally; how the project
  deploys or releases and who starts it — a deployment guide, CI, a release procedure, the
  project's or the owner's rules; for something that is published rather than deployed (a
  library, a package, a command-line tool), how a version is released;
- where the project keeps its tasks: the tracker and the form of a task record that the project's
  or the owner's rules name — a markdown file, Jira, GitHub Issues or another — or a tracker in
  use that no rule names; and whether a record for this feature already exists. With no such rule
  and no tracker in use, there is no task record; do not invent a tracker;
- earlier attempts at the same thing — old specifications, closed tasks in the project's tracker,
  reverted commits: what made them fail will most likely hit this one too;
- unwritten rules the code keeps but no document states — money in minor units, time in UTC, only
  soft deletion. The feature keeps them, and the plan lists them in "Rules every step keeps".

Measure the scale in numbers from the project: data volume and growth, load, who maintains it (the
owner and agents, no on-call engineers), budget, where it runs, the cost of a failure. While
drafting, do not touch production servers — not for numbers, not even to read — unless the owner
explicitly asks, even if access exists. A missing number is an [ASSUMPTION], and its measurement
goes to step 0 as [MEASURE]. Do not ask the owner what the project answers. Without a project,
mark the stack, platform and scale as assumptions.

### 3. Feature type

The type decides the pass in step 8 and the sections of the document.

- **User-facing** — a person sees it and acts: a screen, a bot, an API for developers, tools for an
  AI agent. A background job that only carries out a person's action (a file import) does not
  change the type.
- **Internal** — nobody uses it directly, but its failure hits people: backups, sync, queues, data
  migration, monitoring.
- **Mixed** — a user-facing feature that brings a new mechanism running on its own and failing in
  its own ways: a sync, a schedule, an integration.

### 4. Research

Find how others solved the same task and what the platform allows. Extend research already done in
the discussion instead of repeating it, and come back here when a later step opens a fork with no
ground.

- Load first every available skill, global or the project's, that covers the feature's stack,
  platform or domain; search the web for the rest. Live popular repositories are worth a look:
  their open issues list real edge cases. A discussion or a post is a signal until another source
  confirms it.
- For each practice, record the problem it solves, the scale at which it pays off and its cost.
  A principle carries over to any scale; a big company's implementation does not.
- Memory is not a source. Platform behaviour comes from current documentation of the right
  version, otherwise it is [ASSUMPTION: not checked against <platform> documentation]; prices and
  limits come from fresh sources, with a date.
- Stop when every fork has grounded options and new sources repeat what you found. The "What it
  rests on" table holds only what shaped decisions, including what was not taken and why.

Read; do not experiment. A few minutes with documentation, a library's source or a tiny example
is fine; a database or service to start, a live API call, a load test or a vendor comparison goes
into step 0 as [VERIFY] with the decision that depends on it. The platform limits a decision but
does not choose it: change a decision only for a limit you found, and name it. Nothing to research
with — say so and mark such decisions [NO SOURCE]. A decision costly to reverse — a data format, a
new store, an external contract — that rests on an [ASSUMPTION], [NO SOURCE] or one unconfirmed
source is checked in step 0 before anything is built on it, or goes to the owner as a fork.

### 5. Questions before the draft

Ask before the draft only about a fork that turns the whole feature over — which level of the
ladder to build, or what product to make (one-way or two-way sync; losing a day of data is fine,
or not a minute is) — and only when all three hold:

- a wrong guess means rewriting most of the document;
- the project, the inputs and the research do not answer it;
- it is the owner's decision under principle 2.

Check them first against the owner's earlier decisions in similar situations, if the environment
has such a source (step 9). Ask what is left in one message per "How to ask the owner" and wait.
When you do stop here, ask in the same message about deployment and the task tracker, if they are
forks (step 9), and every other owner's fork that is already clear, so the owner answers each
question once: what they answer goes to "Accepted" and is not asked again at step 12. Do not stop
here for deployment or the tracker alone; with no question that passes the three conditions, they
wait for step 12.
First candidates: your unconfirmed
recommendation that changes the product, and the reason for the feature if it is unknown and
decides what we build. Rules, limits, prices, retention, texts and technology are not blocking:
propose them in the draft. If you are unsure whether a fork blocks, write the draft on the most
likely reading and make that fork F1, saying what the other answer would change. Without a person,
do the same and mark it "taken as recommended, awaiting the owner's confirmation".

### 6. Frame: goals and non-goals

From here on you write the specification: open `references/document-template.md`. In your own
words: what we build, for whom, why and what success is. An idea that names a solution ("an
export button to CSV") is a means; write the goal it serves separately ("the accountant reconciles
orders once a month"). Separate what the owner said or confirmed from what you added, including
your guess at the reason when they did not give one. Write goals, non-goals and anti-goals — what
would make the feature a failure even if it works. For an internal mechanism, put the goals in
numbers: how much data may be lost, how long it may be down, how fast changes arrive. Write how
people manage today and what it costs them, or [ASSUMPTION] if unknown: that is the "as now"
option of the forks and the measure of whether the feature is worth building.

### 7. Options and scale

If there is one sensible path, say so and why in one sentence. Otherwise give 2–3 options that
differ in behaviour: in what the person does (order of steps, one by one or in bulk, who decides,
the point of no return), or, for a mechanism, in what it protects against, what can be lost and
who maintains it. First ideas tend to differ on one axis, so let one option come from another
side: the reverse of the obvious, without a constraint everyone assumes, or as another field
solves it. An option that would fit any feature is grounded in this project or dropped. If another
way reaches the owner's goal clearly better than the one they named, put it next to theirs as a
fork.

When options differ in reliability and cost, build a ladder. For each level: what it protects
against and what not, moving parts and failure points, money per month, maintenance, when it is
needed. Choose the lowest level that meets the goals of step 6 at this scale, write the measurable
condition for moving up and check that moving up will not force a new data format or interface.
When the goals demand a high level and the project is small, that is the owner's fork: costly
protection or accepted risk, in money and consequences.

- **Overengineering looks like:** a separate component the existing stack could replace;
  headroom with no data on growth; technology nobody on the project can fix; "just in case"
  without a measurable condition; a shared layer with one user; many new modules for one scenario.
- **Do not economise on:** the irreversible (data, money, deletion, sending to people); security
  and access; what is cheap now and costly later (data format and identifiers, duplicate
  protection, the history of changes, rollback); the failure signal.

Set the criteria, then compare. Recommend one option and say what it costs in exchange for its
strengths; for each rejected one, say where it lost and what would bring it back. Do not glue the
best of each into a hybrid nobody argued for.

### 8. The pass through the feature

First write the 3–7 main risks and forks of this particular feature:

- what is specific to it and the project, and what it can break in what already works;
- what is already there to reuse, and what in the owner's idea reads two ways;
- which two decisions together give what nobody chose: deleted orders are kept 30 days and the
  export takes all orders, so deleted orders get into the export;
- how the feature could be built exactly as written, pass every test and still miss a goal: the
  import works, but reconciliation stays manual because the file lacks the column people
  reconcile by.

Each risk goes to the section that closes it, or into a fork; the main ones go into "What to
watch".

Then check the seams with every neighbour from reconnaissance: what happens when they meet — the
same data, one person in two roles, the same time, permissions or notifications — and which wins.
In one past project, a two-way calendar sync, three of the four serious gaps were seams.

Then go through the net in `references/checklists.md` — part A for what people use, part B for a
mechanism. It catches what you missed; what matters outside it outranks any item. For every item
that can happen here, the document says what happens then.

A mechanism nobody asked for — a retry, a lock, a mode, an alert — goes into the work only when
without it the feature here works wrong, loses data or fails silently, traced in this project and
not "it happens in general", or when it falls under "Do not economise on". If you cannot tell
whether its absence lets harm through unnoticed, build it, in the smallest form that closes the
gap. A mechanism you decide not to build goes to section 14 with the condition to come back. A
protection never delays, caps or skips part of what the owner asked for; when the two collide, it
is a fork.

### 9. Decisions

Each owner's decision under principle 2 is a fork in section 6, in its format, however many there
are; if there are very many, check whether you are passing on your own work or the feature should
be split. What happens to the work after implementation is decided from what reconnaissance found, and
the specification always says it:

- the project has nowhere to deploy — no fork: the work ends with a local check, and the
  specification says how to run it;
- the project's or the owner's rules set the path with no choice left (only through CI from a
  release; the owner starts every deployment) — no fork: follow the rules and name the path;
- the work is published, not deployed — the fork is about releasing a version, not about a
  server;
- environments exist and the rules leave a choice or say nothing — a fork: offer the stage or
  test server if the project has one, otherwise production; the answer lets you deploy without
  stopping;
- you could not find out — a fork that says what you looked for and did not find.

Where the project keeps its tasks is decided from reconnaissance the same way:

- the rules name a tracker the project has — no fork: follow them;
- a tracker is in use (recent records, not an abandoned one) but the rules say nothing, the rules
  name a tracker the project does not have (no repository there, no project in it), or you could
  not find out — a fork about where to keep tasks that says what you found and offers to write
  the answer into the project's rules;
- there is no tracker and no rule names one — no fork and no task record.

Do not ask the owner what the project answers, and do not invent a deployment or a tracker the
project does not have. Each of these forks is asked once: at step 5 if you stopped there,
otherwise at step 12. Ask about the business consequence: not "which RPO" but "if the server
burns down, can we lose the last day of orders?". If every option rests on the same assumption of
yours, ask about that assumption instead. Your own decisions go into "Agent decisions — for
review" by the rules of section 15.

If the environment has a source of the owner's earlier decisions in similar situations — a skill
or a base kept for that — check the forks and the decisions of section 15 against it here, before
step 10, the way that source says. What it settles is the owner's own answer, given earlier: such
a fork is not asked again and goes to "Accepted" with that ground, and a decision of yours follows
it. With no such source, go on without comment.

### 10. How to build

Write part 3 of the template by its rules; §3 of `references/examples.md` shows a good and a bad
step. The design implements the option or level chosen in step 7 on what the project already has;
any departure is visible.

### 11. Check

Save the draft where step 12 says, then go through the self-check in part C of
`references/checklists.md` and fix what fails. For a full specification, if you can launch agents,
run the fresh-agent check from `references/builder-check.md`: that agent sees neither the
conversation nor the lists, so it looks wider. Without that tool, read the document yourself as
the implementer would.

### 12. File and summary — the one checkpoint

The specification lives where the project keeps feature documents, otherwise in `docs/specs/`;
create the folder if it is missing. In either place the file name starts with the day the
specification was created, in square brackets, day.month.year without time:
`[DD.MM.YYYY]-<short-name>.md`, for example `[07.11.2026]-group-disconnect.md`. Without a
project, ask where, or give it in the chat.
Status: "draft, awaiting the owner's decisions". No task record is made yet, so a draft the owner
turns down leaves nothing in a tracker. Cut repetition and the obvious, never scenarios,
errors and failures; length alone is no reason to cut.

Then send one message with:

1. the path to the file and "At a glance" copied from the file as it is, every block in the
   template's order, "What to watch" included (§2 of `references/examples.md`). A retelling drops
   what the owner must act on, and the owner reads the message, not the file;
2. the intake of materials in short, if there was one: what was done with them, what could not
   be opened, contradictions and questions to third parties beyond this feature;
3. legacy code and old defects found in the affected area, each as a fork to fix or remove — do
   not touch them without consent;
4. the forks still open, in full per "How to ask the owner" — deployment and the task tracker
   among them when they are forks and were not answered at step 5;
5. one closing line: answers that do not overturn the plan are also the go to start. With no
   fork left open, the message is the draft for agreement and the closing line asks only
   whether to start.

Then stop and wait; do not write code. This stop does not depend on whether any fork is left:
it is where the owner sees what will be built and agrees to it. Without a person, take the recommended options, mark them
"taken as recommended, awaiting the owner's confirmation" and say so in the message.

### 13. After the owner's answers

Move the decisions to "Accepted" and update every section they touch, "At a glance" included.
Check that the answers do not contradict each other and do not give, together or with decisions
already made, what nobody chose. If they do, or an answer opens a new fork, ask; do not choose
silently. If the environment keeps the owner's earlier decisions, hand it these answers the way
it says. Then:

| The owner answered | What you do |
|---|---|
| Every fork, and the answers do not overturn how it works or how we build it — recommendations taken, or options the plan absorbs | Status "agreed"; say in 2–4 lines what was taken and where you start, and start |
| Reversed your decision so that the behaviour or the design changes, rejected the approach, or asked for more research | Redo the affected parts, show only what changed, wait for the go |
| Some forks only | Start implementing what does not depend on the open forks and ask those again, briefly, in one message |

Before you start implementing, the partial start of the last row included, make the task record
in the project's tracker in the form it uses, with the path to the specification in the project,
and put a link to the record in the specification's "Task" line. A record that already exists for
this feature — the owner named it or reconnaissance found it — is used, not duplicated. One
specification — one record; a record per step only when the steps reach production separately,
and then the "Task" line lists them in step order. While the tracker fork is open, the record
waits for its answer; if the owner agreed to write the tracker into the project's rules, write it
there. A tracker you cannot reach — give the owner the ready text of the record, say plainly that
you did not make it, write "not made, the text was given to the owner" in the "Task" line and go
on. No tracker — no record and no "Task" line. Without a person, make the record only in a
tracker the rules name; a tracker fork taken as recommended gets no record and no change to the
rules, only the ready text of the record in the message.

An explicit go («делай», «отработай», «погнали») in any language is permission, and so is a reply
that meets the start conditions you named, such as the closing line of step 12. «Проработай ещё»
is not. Do not ask for permission twice. After step 0, carry on unless its results change the
owner's decisions or "How we will build it"; if they do, show what changed and wait.

## Review mode

When the owner brings a ready feature description, plan or PR and asks to find the holes, follow
`references/review-mode.md` and do not rewrite the document.

## Mock-ups and diagrams

Only when the owner asks to see the screens or a scheme, at any moment: an HTML file next to the
specification, opened in their browser when ready, per `references/mockups.md`. Do not offer them.

## How to ask the owner

The owner decides only what they understood; a question without an explanation gets either no
answer or a click on the recommended option that is reversed an hour later. §1 of
`references/examples.md` shows a good and a bad question.

- Ask in the chat, in one message, then wait. Open with 2–4 lines: what you are designing, what
  you found out and why these questions need the owner. In the message of step 12, "At a glance"
  plays this part.
- Each question has the four parts a fork has in section 6:
  1. **Situation** — a live example: "a person opened their list of calendars, saw an unfamiliar
     'Reminders' and deleted it";
  2. **Why I do not decide it myself** — what depends on the answer in the product, data, money
     or reliability;
  3. **Options** — what the person will see, what it costs, what becomes hard to change; one of
     them is the simplest ("without it", "as now"), and they do not all rest on one assumption of
     yours. When options differ in what the person sees, show each as text: the message or the
     screen in a few lines;
  4. **I recommend** — the option, why it is better for the product, and what that rests on.
- In the chat each question opens on its own line with ❓ and the question itself in bold, as in
  §1 of `references/examples.md`, so it stands out in a long message. One mark per question, not
  on its parts or options. The mark is for the chat only: the specification file, and "At a
  glance" copied from it, stay without it.
- Use the owner's words. Rule numbers, module names and terms they have not seen are replaced
  with a description or explained.
- A structured choice dialog hides the text above it, so the forks come first as text in the
  chat, and the dialog opens only after the owner has read them and agreed to it (for example,
  replied «спрашивай»). Only a service choice clear without context — where to put a file, which
  account to use for checks — goes straight to the dialog. Every question in the dialog stands on
  its own, with the recommended option first.

## Typical failures

| Thought | Reality |
|---|---|
| "I recommended A in the discussion and the owner did not object, so A is chosen" | Silence is not consent. An unconfirmed recommendation is a fork, and the first one |
| "I went through every item of the checklists, so I covered everything" | The main risks are specific to this feature and project and are not on the lists. Your own list first, the lists after |
| "I will ask through the choice dialog, it is faster" | The dialog covers the explanation and the owner clicks without reading. Questions go in the chat; the dialog comes after the owner agrees |
| "The owner answered every fork, or said «отработай»; I will resend the summary and ask again" | The summary was the checkpoint and the answers are the permission. Say in 2–4 lines what was taken and start |
| "I will settle this important fork myself so as not to bother the owner" | What matters goes to the owner, clearly and with a recommendation; only the obvious is yours |

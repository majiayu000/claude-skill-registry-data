---
name: project-setup
description: >-
  The front door for a project in a kensaiapp — one plain-language conversation that turns "I have an idea for a
  product" into a project whose definition is already running. It interviews the owner without
  kensaiapp's vocabulary (no PRD, no Agari, no companion), one question at a time, offering a
  suggested answer wherever the idea or the material already holds one, stamps the project through
  project-stamp, writes the owner's answers as the PRD's and the Agari's first round, commits them,
  and starts the chain that writes the PRD and then the Agari. Interactive, with the owner in the
  room; works the same in a host or a satellite. Use whenever someone wants to start, create, set
  up, add or kick off a new project or product in this instance, says they have a product idea and
  want kensaiapp to take it from here, or is new to kensaiapp and asks how to begin — even if they
  never say "project". Do not use for scaffolding only the management folder with no interview
  (project-stamp), writing a PRD or an Agari for a project that already exists (product-prd,
  project-agari), declaring the instance's own identity (kensaiapp-michi), or filling the card
  after the foundation step (product-card).
license: MIT
metadata:
  author: Eyal Golan
  category: kensaiapp-setup
  version: "1.2.0"
  created: "2026-10-04"
  risk: safe
  tags: kensaiapp, project, setup, interview, front-door
  depends-on: project-stamp
---

# project-setup — the front door for a project

A person with a product idea should not have to know that a project is stamped, that a PRD comes
before an Agari, or that a run parks its questions in a companion. This skill asks what only they
can answer — suggesting an answer where it already has one, which they accept, change or replace —
and does the rest: it creates the project, writes their answers where the first runs read them,
and starts those runs.

"New project" is the door's first verb; more join it later. It opens onto an instance that already
exists — setting up the instance itself is a separate door.

**No posture.** The owner answers every question and confirms before anything is written, so the
person in the room is the check (`<CORE>/doctrine/setup/authoring_layers.md` § *A skill that acts
unattended gates to its seat*). Commits carry `--role Product`.

**Speak plainly.** Never say PRD, Agari, companion, stamp, chain, seed or card to the owner. Say
"what it is", "when it's finished", "your answers", "set up the project", "start writing".

## The flow

1. Name the project
2. Screen 1 — what kind of project (four taps)
3. Screen 2 — the product (seven questions in chat, three taps), each with a suggested answer where
   there is one
4. Confirm
5. Set up the project
6. Write the two companions
7. Commit
8. Start the chain
9. Tell the owner what happens next

### 1. Name the project

Ask in chat: *"What should we call it? A short name — it becomes the project's folder."* Turn the
answer into a slug — lowercase, words joined by `-`, no `/`, not starting with `.`. If
`system/projects/<slug>/` already exists, say so and ask for another name; `project-stamp` never
overwrites.

### 2. Screen 1 — what kind of project

One `AskUserQuestion` call, four questions:

| Question | Options | Lands as |
|---|---|---|
| What are you building? | **Software** — an app or tool with code · **Something without code** — a profile, a body of writing, a public presence | `--type software` / `--type no-code` |
| Where should it live? | **Here** (recommended) — inside this workspace · **Its own repo** — somewhere else on your machine | `--placement internal` / `--placement external` |
| Will it look after something outside itself? | **No** · **Yes** — like a public repo, a GitHub account or a domain | `--manages none` / `--manages "<what>"` |
| Do you have anything to start from? | **Nothing yet** · **Yes** — notes, a CV, documents, old code | the material part of `Source material:` |

Then ask in chat for whatever a "yes" opened:

- **Its own repo** → the absolute path. It must be a git repository already; if
  `git -C <path> rev-parse --show-toplevel` fails, stop and say so — the first runs commit there.
- **Looks after something** → what, in one line.
- **Material** → where it is (paths or links), and one line on what it is.

### 3. Screen 2 — the product

Ask these **one at a time in chat**, and wait for each answer before asking the next.

**Suggest an answer where you have grounds for one.** The idea the owner has described, the material
they pointed at — which can be detailed enough to answer most of these — and their earlier answers
often already say what the answer is. Then put a short suggested answer under the question, say
plainly that it is your suggestion, and let the owner accept it, change it or answer in their own
words. Where nothing you hold answers the question, ask it bare. A guess with nothing under it is
not a suggestion.

**One question, one suggestion.** Never put the suggestions for the remaining questions in one
message, even when you could draft them all or the owner says "suggest the rest". A wall of answers
gets accepted unread, and the point of the interview is that each answer is looked at.

Record what happened to each answer, because the writing runs must not mistake your words for the
owner's: their own words as they gave them, unpolished; a suggestion taken as shown is `accepted`;
a suggestion they changed is `edited`, with the changed text as the answer.

| # | Ask | `why` (written into the item, never shown) | Goes to |
|---|---|---|---|
| 1 | In a sentence or two, what is it? | PRD: Blurb, Purpose | PRD |
| 2 | Who is it for? | PRD: Target Users | PRD |
| 3 | What's painful for them today that this removes? | PRD: Problem Statement, Why This | PRD |
| 4 | What are the 3–5 main things they'll do with it? | PRD: Key Use Cases, Core Features | PRD |
| 5 | What is it deliberately *not*? | PRD: Out of Scope | PRD |
| 6 | How will you know it's working? | PRD: Goals, Success Metrics | PRD |
| 7 | When is it finished — what has to be true for you to say "done"? | The terminus itself — the condition under which the product is done | Agari |

Then one `AskUserQuestion` call. Where you have grounds for an answer, put that option first and
add "(Recommended)" to its label; otherwise keep the order below. A recommended option the owner
picks is `accepted`; any other pick is their own answer. When question 9's answer is yes and you can
name the services, suggest the names in chat the same way, and record them the same way.

| # | Question | Options | `why` | Goes to |
|---|---|---|---|---|
| 8 | Does it handle people's personal data? | No · Yes · Not sure | PRD: Data & Privacy | PRD |
| 9 | Does it rely on other services — a login, payments, an API? | No · Yes (name them in chat) | PRD: Dependencies / Integrations | PRD |
| 10 | *(Software only)* Where will people use it? | Web · Phone · Desktop / terminal · Not sure | PRD: UX Notes | PRD |

Not asked, on purpose: assumptions, risks, UX detail and gates. The first PRD run drafts those from
these answers and lists them as choices to confirm.

An answer of "I don't know" is an answer — record it as said. A question the owner refuses is left
out of the companion rather than written empty; the first run raises it itself. If that leaves a
document with no answers at all, write no companion for it: with no Agari answer, the Agari run
drafts from the PRD alone and asks what it cannot settle. Question 1 is the one that cannot be
skipped — with no answer to "what is it?" there is nothing to start from, so ask it again in other
words rather than go on.

### 4. Confirm

Show a short summary in plain words — the name, the four screen-1 answers, and the ten answers,
with the ones that came from your suggestion marked as such — and ask with `AskUserQuestion`:
**Create it** · **Change something**. Nothing is written before **Create it**; that answer is also
the consent to commit.

### 5. Set up the project

From the instance root:

```bash
python3 <CORE>/../skills/interactive-product/.claude/skills/project-stamp/scripts/stamp_project.py <slug> \
  --placement <internal|external> [--product-path <absolute path>] \
  --type <software|no-code> --manages '<what or none>' \
  --source-material '<source line>' \
  --execution-type headless --test-command "<pytest tests/ | none>"
```

- `--test-command none` for a no-code product; `pytest tests/` otherwise — `product-card` re-derives
  it once the product's documents settle.
- **The source line always names the interview**, because `product-prd` stops and asks what to write
  from when the card names no input. Write it as:
  `the owner's answers to the project-setup interview, <YYYY-MM-DD> — docs/PRD_open_issues.md until
  the first PRD run folds it, docs/trail/prd/cycle-1.md after`, followed by `; ` and the material the
  owner named, if any. The first fold always files that copy as `cycle-1.md` on a new project.
- **The owner's words go in single quotes**, with every `'` inside them written `'\''`. A backtick,
  a `$` or a `"` inside double quotes is run by the shell or breaks the line.

On exit 3 (the project exists) or exit 2 (a path mismatch), report the script's message and stop.

### 6. Write the two companions

Write each document's answers to a JSON list of `{"question", "why", "answer"}` in a scratch file
outside the repository — adding `"suggested": "accepted"` or `"suggested": "edited"` to an answer that
came from your suggestion, and nothing to one in the owner's own words — then render:

```bash
W=<CORE>/../skills/interactive-product/.claude/skills/project-setup/scripts/write_companion.py
python3 $W --template <CORE>/templates/product-templates/prd_open_issues_template.md \
  --out <Product path>/docs/PRD_open_issues.md --name <slug> --answers <prd.json>
python3 $W --template <CORE>/templates/project-templates/agari_open_issues_template.md \
  --out system/projects/<slug>/agari_open_issues.md --name <slug> --answers <agari.json>
```

`<Product path>` is the card's: `products/<slug>` for an internal product, the absolute path for an
external one. The script keeps every heading of the template, puts the answers in bucket 1 as
answered items, marks each answer that came from a suggestion after its text, and refuses an
existing file, an empty answer or any other `suggested` value. Each answer is a round 0: the
first run reads it as already answered and folds it in (`product-prd`'s own Step 2 says answers in
the open-issues file resolve into the body).

### 7. Commit

The first runs refuse an uncommitted companion, so both are committed before anything starts. Read
`<CORE>/doctrine/governance/commit_via_builder.md` and commit through
`<CORE>/tools/commit_builder.py` with `--role Product --skill project-setup`, and
`--directional "Agari: none — <one line>"` — no Agari is declared yet.

- **Internal product** — one commit in the instance: `--add system/projects/<slug>
  products/<slug>/docs/PRD_open_issues.md`. The Agari companion sits inside `system/projects/<slug>`,
  so that one path covers it, and covers its absence when step 6 wrote none.
- **External product** — two commits. The instance: `--add system/projects/<slug>`. The product
  repo (`--repo` = `git -C <Product path> rev-parse --show-toplevel`): `--add` the PRD companion,
  repo-relative.

### 8. Start the chain

From the instance root:

```bash
<CORE>/launchers/chain-agari/launcher.sh <slug>
```

It writes the PRD from the answers, answers the questions that run raises itself through
`companion-self-answer` — as every chain does — then declares the Agari the same way, and stops. It runs in the background and reports on completion. A walk can also stop early —
the PRD's questions not settled within its rounds, or a run that failed — and then the Agari waits;
the end message says which.

### 9. Tell the owner what happens next

In plain words: the project exists; their answers are saved where the writing starts; the
definition is being written now, and the writing answers its own follow-up questions as it goes.
They will get a message when it finishes, and they hear back only if that message says something is
left for them. Do not guess which questions the runs will raise — they have not run yet. If the
message says the writing stopped before it finished, running
`<CORE>/launchers/chain-agari/launcher.sh <slug>` again carries on from where it stopped. For a software product, say that the rest of the definition — what the system must do, how
it looks, how it is built — follows once this part is done.

## What it does not do

- It does not write the PRD or the Agari — the chain's runs do.
- It does not pick or walk any journey item, and plants no seed.
- It does not overwrite a project, a companion, or a card that already exists.
- In a satellite it touches only the satellite it runs in.

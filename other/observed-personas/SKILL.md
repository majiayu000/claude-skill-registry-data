---
name: observed-personas
description: Build evidence-graded personas from what users actually did - events, database rows, session recordings, support tickets, chats - instead of from imagination. Starts with an identity audit and a census that partitions every real user by where they stopped, gives every large stop its own persona, tags every claim MEASURED / OBSERVED / STATED / INFERRED / UNKNOWN, keeps personal data out, and writes personas.md ready to use as lenses for why-tree or any other analysis agent. Use when the user says /observed-personas, asks to "build personas", "who are our users really", "make personas from our data", wants lenses or seats for why-tree or a user panel, or is about to write personas from intuition.
---

# Observed Personas

Who actually shows up, what they came to do, and where they stop - built only from the evidence in
front of you.

Not a marketing persona with a name, a photo and a favourite coffee. Not demographics. One job:
**a short set of person-shapes, each tied to a count in the data, where every claim says how we know
it - and where what we don't know stays visibly empty.**

## The six hard rules

**1 · Every claim carries a tier - one claim per row.**

| tier | means |
|---|---|
| **MEASURED** | computed from the data, with N and a denominator. A rate across many recordings is MEASURED, not OBSERVED |
| **OBSERVED** | one or a few specific cases **a human watched** (a replay played on a screen). Never generalised. An agent never awards itself OBSERVED: what it read in rows or logs is MEASURED; a case it wants a human to confirm is `OBSERVED — PENDING` plus where to look |
| **STATED** | a user's own words, from a source you were given (see rule 3 for how to quote) |
| **INFERRED** | our reading or explanation. Any "because", "wants", "can't", "chose to" is INFERRED unless a test settled it |
| **UNKNOWN** | no source here reaches it. **Left empty on purpose** |

A row holds one claim with one tier. If a sentence mixes a count and an explanation, split it. Persona
**names and headings describe behaviour only** ("Imports data, never invites a teammate") - never a cause
("Confused by the pricing page"), because a name is read as a fact.

**2 · Never invent a voice.** No tickets, chats, interviews or reviews in the inputs means every STATED
field is UNKNOWN - and that is a finding, not a gap to fill.

**3 · No personal data anywhere you write.** `personas.md`, the census script, anything you print, and
your chat replies must never contain
emails, names, company names, phone numbers, or any identifier (user, account, workspace, ticket,
session, recording ids), nor per-account revenue. Cite sources by file and count ("tickets export,
12 of 40 mention X"), never by row. A quote is a short excerpt with anything identifying replaced by
`[redacted]`, and only from a group of 5 or more people. Never print raw rows to the chat. Report only
aggregates over 5 or more units - no minimum, maximum or any other value that belongs to one account.

**4 · Every persona has one warrant.**
- **POPULATION** - "this is a lot of people." Its count and denominator.
- **TARGET** - "this is the person a surface or decision the user named exists for," even if few. Only
  when the user names that surface; a TARGET card is not evidence about the market.

**5 · Silence is data.** Groups that left no trace beyond a signup still get their count. The loudest
users are the worst witnesses for population questions.

**6 · Arithmetic in code, and keep the code.** Save the counting script next to the report with the
same stem (`personas.md` → `personas_census.py`, `personas-<date>.md` → `personas_census-<date>.py`)
and run it. Every number in the report must be computed by it - never typed into it as a literal. Never
`pip install`: check `python3 -c "import pandas"` once; if it fails, use `csv` + `collections`.

---

## Step 0 - Inventory, identity, cleaning

**Inventory.** For each source: what it is, its time window, which ids join it to the others, and
what it is structurally blind to (only people who got far enough to be recorded; only people with the
tracking script; only people who wrote to support).

**Doors - before any count.** List every way a unit can act on the product: the main interface, an
API, integrations, imports, and external clients that act for the user. For each door, name the tables that record it, and count in
code how many units used each door and when each door first appears in the data. A unit that acts
through a door the main path does not pass through **has not stopped** - it went another way. A door
that opened recently is where a new kind of user shows up first.

**Identity audit - before any count.** Decide the counting unit (usually an account or a person) and
check in code: is the key unique; how many ids (devices, browsers, sessions) map to one unit; which
join direction is many-to-one. Ids that belong to a known unit are that unit - **extra device ids are
not extra people**, and an id with no signup event is not a visitor who never signed up if another id
of the same unit did. Count distinct units, not rows.

**Cleaning.** Remove non-customers - bots, internal and test accounts - with rules that **do not use
the outcome you are about to study** (a rule like "never reached step X" deletes a real stall). Report
each rule and the count it removed. If a rule rests on a single signal, say so and show the census
both with and without it. Non-customers are a line in the census, **never a persona card**. If a
cleaned funnel already exists from an earlier hygiene pass, reuse its exclusions and say so.

**Maturity - per step.** A unit can only "stop" at a step if it had time to go further *from that step*.
For each step, measure how long the units that did move on took, and set that step's horizon to cover
most of them (for example 90%). A unit that reached step k less than step k's horizon before the end
of the data goes into **too recent to tell (at step k)**. Report each step's horizon. Never use one
signup-age cutoff for every step. "Too recent to tell" means *not stopped yet* - it does not mean *not
worth describing* (see "The edges of the census").

## Step 1 - The census: a partition by where people stopped

**First, check which steps really form a sequence.** A step belongs on the spine only if (almost)
every unit that reached the next step also has this step's event - check it in the script. An action
that people can skip (a download, an export, an invite) is an **optional action**: report it as a flag
with its own actual count of units, never as a step on the spine. Every "reached this step" count
comes from units that have the event, never from summing the branches below it.

Then assign every clean unit to exactly one **terminal state: the furthest spine step it reached**
(plus "too recent to tell"). The terminal states are mutually exclusive and **must sum to the clean
base** - check this in the script. Draw it as a tree with counts and shares.

**Not a single funnel?** If the product has cycles or several jobs, build the spine for the one job
the user cares about and say which. **No source gives you everyone** (for example, only support
tickets)? Then write an *observed sample*: counts within the sample only, no POPULATION warrants, and
say so in the header.

Add the one skew that governs the rest, if there is one - stated as a count with its denominator, and
graded.

**The edges of the census.** An all-history census hides whoever arrived last. Before moving on:
- **The newest cohort.** Repeat the census for units that joined in the most recent 30 days (or the
  last tenth of the window, if that is shorter). Compare its mix of doors, attributes and terminal
  states with all history. A group that is **20% or more of recent units** gets its own card even when
  it is under 5% of all history - warrant POPULATION (recent), with both shares stated.
- **The "too recent to tell" group.** Compare it with everyone else on every door and attribute. If one
  door or attribute dominates it, that is a finding: say it, and give the group a card if it passes the
  recent-cohort rule above.
- **Other doors.** Every unit that used a door the main path does not pass through: how many, since
  when, and where the main path would have filed them. If they are 5% of all units or 20% of recent
  units, they get their own path and card - never a card that describes them as stopped.

## Step 2 - From stops to people

**Coverage map first.** List every terminal state holding 5% or more of the clean base, plus every
group that passed a rule in "The edges of the census". Each one gets
**its own persona card, or its own line in "What no persona covers" saying why not.** Do not merge
different terminal states into one card - "finished setup, never came back" and "came back
weekly but did not pay" are different people even if both "did not buy".

For each stop, compare the units who stopped there with those who went further, using only attributes
fixed **before** the stop: columns of the unit (role, device, browser, source, country - not the plan
they ended on) **and behaviour recorded in other tables** (which door they used, which integration they
connected). For
each attribute value with 30 or more units, compute the rate of going further; the attribute with the
biggest gap between its values is the lead. Report it as counts with denominators, and **always with
the counterexample**: how many units with that value did go further. An attribute that differs most is a lead, not a cause - it
goes into the card as MEASURED, and any "because" goes in as INFERRED.

Device, browser, language and country are **fields on a card**, not people. A **door** is different:
when a group reaches the product another way, the path itself changes, and that can make a persona. A persona is named by
what people did at their stop; the attribute that distinguishes them goes into its "Who" row.

## Step 3 - The persona cards

For each persona, a table **Claim · Value · Tier**, one claim per row. At minimum:

| claim | what goes in it |
|---|---|
| Warrant | POPULATION (count / denominator) or TARGET (the surface the user named) |
| Terminal state | the step they stopped at - must match a census branch |
| Volume | count / clean base |
| Path | the steps they took, with counts |
| Who | the attributes that distinguish them, each with counts and its counterexample |
| What the data shows at the stop | MEASURED facts at that step |
| Goal | usually INFERRED - say so |
| Fallback | what they do instead, if any source shows it |
| Voice | a redacted short excerpt with its source and group size - or UNKNOWN |

Then one line: **UNKNOWN:** the questions about this persona no source here answers. For each, say
whether one more query on the data you already have would answer it - if so, run it now instead of
leaving it UNKNOWN.

## Step 4 - What no persona covers

Every terminal state from the coverage map without a card, every period or place the evidence does
not reach (people who left no trace, windows before tracking started, screens that cannot be
recorded), each as a sentence with a count where one exists. This is part of the result.

## Step 5 - Write and check `personas.md`

**Before you start writing**, resolve the output path: the folder the user invoked you in, or the path
they gave. If `personas.md` already exists there, write `personas-<date>.md` and say so - never
overwrite.

The file contains, in this order:

1. Header: date, sources with windows, the doors and when each first appears, the counting unit,
   exclusions with counts, maturity horizon,
   and the line *"Every claim is tagged; UNKNOWN is left empty on purpose. No personal data."*
2. The tier table from rule 1.
3. The census (Step 1), with the check that it sums to the clean base.
4. The coverage map (Step 2).
5. The persona cards (Step 3).
6. What no persona covers (Step 4).
7. Using these as lenses (below).
8. Refresh: which new evidence should trigger a rebuild, and the standing gate - before promoting any
   claim from INFERRED to STATED, check whether a user actually said it.

**Then read the file and the script back and check:**
- every card row has exactly one of the five tiers, **and the tier fits the claim**: a count or rate
  is MEASURED; OBSERVED only names a few specific cases a human watched (otherwise `OBSERVED — PENDING`); any "because", "not a friction problem",
  "wants", "can't" is INFERRED;
- prose outside the tables only restates tagged rows - no new conclusion without a tier;
- every ≥5% terminal state appears as a card or a not-covered line; the census sums; every "reached"
  count comes from units with the event;
- every door is counted, the newest cohort and the "too recent" group were compared, and no unit that
  used another door is described as stopped;
- no email, name, identifier or single-account value appears in the report or the script.
Fix and re-check before replying.

In the chat: persona names, warrants and volumes, the path to the file, and anything the check fixed.

## Using these as lenses (why-tree and other agents)

The personas are seats for an analysis, not evidence about the market.

- **why-tree:** name `personas.md` in the Phase-1 frozen evidence brief and ask for one lens per
  persona: *"look at this problem as <persona> meets it, using only what the card says. Warrant:
  <POPULATION n / TARGET>. Treat UNKNOWN as gaps, INFERRED as hypotheses."* Translate each claim, not
  each tier label:
  - MEASURED → MEASURED, carrying its source and a validation state: `raw` by default, `validated`
    only if you checked the source's definition and cleaning, `triangulated` if a second independent
    source agrees, `contested` if two sources disagree (then give both numbers);
  - OBSERVED (one or a few human-watched cases) → INSTANCE - never generalised; `OBSERVED — PENDING` → a gap until a human clears it;
  - STATED → CLAIM;
  - INFERRED → HYPOTHESIS, with the test that would settle it; INFERENCE only when it is pure logic on
    MEASURED premises;
  - UNKNOWN → a gap: `in-hand` if one more query on data already pulled would answer it (then answer
    it first), `external` if the data is out of reach, `experiment` if only a test would tell.
- **Any other agent or panel:** give each seat one card, its warrant, and the rule that an UNKNOWN
  claim must stay unknown in its answers. A seat that invents what its persona "would say" has undone
  this skill.
- **Coverage check before any run:** one line - *"the problem sits at step N; the personas who meet it
  are …"*. If none reaches that step, derive the missing one, with its tiers, before running.

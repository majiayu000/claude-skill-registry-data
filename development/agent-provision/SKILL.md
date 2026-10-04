---
name: agent-provision
description: "The provision for a call site: the exhaustive menu of values that place in the code can realistically produce. Use before creating or fixing a mandate or agent that reasons about more than its own input, when deciding whether an agent can answer at all with what it is sent, or when its output 'looks right' but nobody checked it could be. NOT for building the agent (use create-agent)."
---

<!-- SYNCED COPY — do not edit here.
     Canonical: common-docs/skills/agent-provision/SKILL.md
     This file is distributed to every consuming repo by
     common-docs/meta/scripts/sync_skills.py. Edit the canonical, run the
     sync, and commit each repo. Edits made here are overwritten and lost. -->

# agent-provision — what the call site offers, and proving the agent knew it

## The three things, and why they are three

| | What it is | Who authors it | Named for |
|---|---|---|---|
| **Provision** | The exhaustive menu of values THIS PLACE IN THE CODE can realistically produce | the developer who owns the call site | the call site / the data |
| **Mandate** | A named job to be done at that place, with an input and output contract | the developer who owns the feature | the job |
| **Agent** | One candidate that consumes some of the menu to do the job | the platform, swappable from a UI | itself |

Get this wrong and everything downstream is theatre.

## 🚨 THE PROVISION LAW — a provision describes the CALL SITE, never one agent

Authored correctly, a provision answers: *"standing at this point in the code, what could I
get my hands on?"* — **everything**, including the same underlying fact offered in several
shapes. Mandates then pick from the menu, and any candidate agent picks differently.

Authored backwards — **the disease** — someone looks at the agent they already have, lists its
variables, and calls that list the provision. Now provision ≈ mandate ≈ agent, one to one to
one. Every layer is decoration: a different agent bound to that mandate can only ever see the
same values, so it can never do the job differently, let alone better. **You paid for three
indirections and bought nothing. You should have just called the agent from code.**

**Measured 2026-08-23:** 218 provisions — **152 (70%) serve exactly one mandate**. 368 mandates
— and **2 bindings have ever been created**. The swap layer this entire architecture exists for
is, in practice, unexercised.

### Three tests, cheapest first

1. **The naming test (instant).** If the provision name, the mandate name and the agent name
   are all the same idea, it is fake. `content_plan.page_family` → `content_plan.p3_family` →
   *Website Factory Family Analyst* is three names for one thing.
2. **The swap test (real).** Could a genuinely different agent be bound to this mandate and do
   the job **better**, using values the current agent ignores? If there is nothing to reach for,
   you did not build a menu.
3. **The stuck test (proof).** If fixing the agent requires editing the provision, the provision
   was derived from the agent. That is the whole disease in one sentence.

The canonical case: `content_plan.p3_family` offers 12 values and **not one of them represents
the site**. So the fabricated internal links cannot be fixed by re-authoring the agent, by
picking a smarter model, or by binding a different agent. The data does not exist to offer.
Nothing about that failure is recoverable at the agent layer.

### Variations ARE the point

A provision is where one fact is offered in several shapes, so different mandates and different
agents can choose the cost/detail trade-off without a code change:

- the **full** list, and the **selected** top-N, and the **summarized** counts/clusters;
- the record with **every** key, and the record with the **few** keys that decide this job;
- the **verbatim** text, and the **condensed** line.

Offering three shapes of one fact is not waste — unused offers are normal and free. Offering
only the shape today's agent happens to want is how you get stuck.

### Provisions live beside their feature

Not in a catch-all. **Measured:** `client_mandates.py` is **4,275 lines, 102 mandates, 35
different feature domains**. Co-location is what reminds the next person which values belong to
which job. `podcast_mandates.py` and `education_mandates.py` show the right shape; anything
still in the catch-all should move to its own feature module as it is touched.

## THE PROVISION BRIEF — the forcing function

**Why this section exists.** Telling a developer or an agent to "think carefully about what
the agent needs" does not work, and cannot work. An LLM asked to reflect produces fluent
reflection — the identical failure mode to the agent that fabricates. **Reflection has no
failure state, so it always succeeds.** A checklist of thoughtful-sounding questions produces
thoughtful-sounding answers and changes nothing.

Look at what actually produced insight in the session that created this skill. Not one moment
of it came from thinking harder. Every single one came from **a check that could fail, run
against real data**:

| The check | The number | What it killed |
|---|---|---|
| How many pages does this agent see? | **1 of 295** | The belief that p3_family worked |
| How many provisions serve one mandate? | **152 of 218 (70%)** | The belief that our provisions were provisions |
| How many bindings exist? | **2 of 368 mandates** | The belief that the swap layer was real |
| How many pages carry a planned title? | **0 of 472** | A design about to be built on titles |
| How deep is the URL tree on a real site? | **308 of 472 at depth 1** | Clustering by URL hierarchy |

So the rule is: **replace reflection with falsifiable checks.** Before authoring or changing
any provision, produce the Brief below. **Every field carries a number or a `file:line`. A
Brief made of prose is a rejected Brief** — by any reviewer, human or agent.

### The six fields

**1. THE DECISION.** One sentence in the form *"The agent must decide ___."* If the best you
can write is "helps with" or "handles", you do not yet know the job, and no provision can be
correct. Stop here and find out.

**2. WHAT A COMPETENT HUMAN WOULD NEED.** List the facts an expert human would require to make
that exact decision. **Write this list BEFORE reading the call site** — otherwise you will
simply list what the code already sends and call it complete. This is the highest-leverage
question in the method: the gap usually becomes undeniable the moment the list exists. *"To
decide whether this page overlaps another, you need the other pages"* is not a subtle insight
— it is invisible only while nobody writes the list.

**3. WHERE EACH FACT LIVES — measured.** For every fact in field 2: the schema.table.column,
the upstream artifact, or **NOT AVAILABLE**. Then the count on real data. Not "we have titles"
— `0 of 472 pages have meta_title_desired`. **This is the field where designs die, and it is
supposed to be.** A fact you assumed existed and does not is the most valuable output of the
entire Brief.

**4. COVERAGE.** The ratio the agent will actually see, measured on the **largest real
instance** you can find, not a convenient one. `1 of 295`. If you cannot produce this number,
you have not traced the call site and you are not ready.

**5. THE FABRICATION FORECAST.** The agent will answer even when it cannot. Write down, in
advance, the specific fabricated output it will produce given the gaps in field 3 — *"it will
invent internal links to routes that sound plausible for a PRP site."* Then name: which
entities it can utter (routes, ids, keywords, quotes), what the legal set is, and the query
that counts violations. **A forecast that comes true on a real run is a passing test of the
Brief and a failing test of the provision.**

**6. THE SURPRISE.** 🚨 **At least one number in this Brief must have surprised you.** If
nothing did, you did not investigate — you wrote your assumptions down and formatted them
nicely. Go back to field 3 and measure something you were certain about. This field is the
anti-ritual device: it is the one thing that cannot be satisfied by producing plausible text,
and it is what separates a real Brief from a performed one.

### The Brief decides your next move — and only one door needs Arman

Field 3 leaves exactly three doors, and inventing a plausible answer is not among them:

1. **Build the delivery** — the fact exists but is not offered, or exists in no usable shape.
   Add it to the provision (in every shape a caller might want). *Do this yourself.*
2. **Cut the question down** — the data genuinely cannot support the job as declared. Narrow
   the mandate's declared job to what is answerable, and say so in its description. *Do this
   yourself.*
3. **Refuse** — raise with a named missing input rather than run. *Do this yourself.*

**Only one situation needs Arman: when the fact does not exist anywhere in the platform and
creating it is a new product capability** (a new lock flag, a new stored artifact, a crawl we
do not run). That is a product decision. Everything else is engineering you already have the
authority to do — and escalating it instead is how his time gets consumed by work that was
never his.

### Design from real data, never from imagined data

Before proposing a structure, **look at the real rows.** The recommendation in this skill was
nearly "cluster pages by URL hierarchy" — obvious, elegant, and wrong: 308 of 472 pages on a
real site sit at depth 1, and the largest site has 2,961 pages with a flat slug namespace.
Reasoning from an imagined well-structured site would have produced an architecture that fits
nothing we own. **Ten minutes of looking beats an hour of reasoning about data you have not
seen.**

### Assume your first design is the fabricating one

The posture that produces good work here is not curiosity — it is **presumed guilt**. Your
first provision is the one derived from the agent; your first test is the one that passes;
your first coverage number is the one you did not measure. Go find the evidence that you did
the shallow thing, and only when you fail to find it are you allowed to believe otherwise.

An agent that cannot produce a Brief with a surprise in it has not done this work — it has
described it.

## THE FAILURE THIS SKILL EXISTS TO KILL

An agent is asked a question it **cannot possibly answer** with what we send. It answers
anyway — fluently, plausibly, in the right shape. Someone clicks the button, sees prose and
valid JSON, and marks it done. The output is fabricated, and it gets **stored**, so every later
step treats fabrication as evidence.

This is worse than the feature not existing. A missing feature is a known gap; a confidently
fabricating feature is **falsified evidence that compounds**, making the system look healthy
while moving it further from truth.

**The measured case (2026-08-23, `content_plan.p3_family`).** The mandate asks: *what does this
page cover, what does it leave to its siblings, where does it link?* Everything looked right —
provision declared, `{{family}}` declared and interpolated, well-formed output, rebuilt to the
create-agent bar, two green runs. Then someone measured what actually arrived:

| | |
|---|---|
| Pages on the site | **295** |
| Pages visible to the agent | **1 — itself** (0%) |
| Siblings delivered | **0** |
| Real routes it could legally cite | **2** |
| Internal links it proposed | invented |

`family_context()` returns parent + siblings + children; this page's parent had one child —
itself. So the family comparison ran against an **empty family**, while the genuinely competing
pages (`/research-and-experts/*`, `/learn/evidence/*`) stayed invisible. The one question the
mandate exists to answer was **structurally unanswerable**, and nothing noticed, because the
shape was valid and the prose was good.

**A response is not a result. Valid JSON is not knowledge. "It returned something" is not a
test.**

## THE ANSWERABILITY TEST — before anything else

Take the question the mandate asks. Write down **every fact a competent human expert would need
to answer it**. For each, answer honestly:

1. **Do we have it?** Which table, column, or upstream artifact?
2. **Are we sending it?** Trace the real call site, not the provision. A declared offer nothing
   fills is not delivery.
3. **Is it complete enough?** A cap, a filter, or a tree-shaped slice can silently reduce a
   whole-site question to a one-page answer. Measure `visible / total` on REAL data.

If a required fact is missing there are exactly three honest moves — **inventing a plausible
answer is not one of them**:

- **Build the delivery** (usually a new condensed representation — below), and put it in the
  provision so every future agent can reach it;
- **Cut the question down** to what the data genuinely supports, and change the mandate's
  declared job to match;
- **Refuse**: raise with a named missing input, loudly.

**An agent handed an unanswerable question will always answer it.** That is not a model flaw to
prompt around; it is a design defect on our side.

## BUILDING THE PROVISION — the real work

**Step 1 — inventory.** Every data point that exists at this call site and could matter. Not
what is convenient; what exists. Go find it. This is the step people skip.

**Step 2 — necessity, per mandate.** Which of those does THIS job need? Cut decoration from the
mandate's consumption — but keep it in the provision if another job could want it.

**Step 3 — condensation.** Whatever a job consumes has to fit and be *readable by a model*,
which is not the same as complete. Design the smallest representation that preserves the
decision-relevant signal (for a site: route + short label + role, not page content). Ask:
*could a smart human make this call from this text alone?* If no, condense differently — do not
just add more.

**Step 3b — use the structure the data ALREADY has.** Before inventing a condensation or
clustering scheme, ask whether the collection already carries structure that bounds the problem:
a tree, a hierarchy, an explicit grouping, a declared parent. **Inventing a parallel scheme both
duplicates that structure and drifts from it.**

The canonical case (2026-08-25): the content planner designs a TREE, and every branch point is
already a decision — *"this section exists and splits into these children because X."* So the
"cluster" nobody could figure out how to compute **is just the branch**. And it solves scale for
free: to place ONE item you walk **UP** the tree — your branch, your siblings, your ancestors'
purposes, your aunt/uncle branches' purposes — which is tens of lines whether the collection has
300 items or 6,000. *The structure bounds the context; you do not have to compress the world.*

Before you design a grouping, spend ten minutes asking what structure already exists. If the
answer is "a tree", stop designing.

**Step 3c — capture meaning at its cheapest moment, and record MEANING, not COPIES.** The moment
a structure is created, the agent that created it still holds the whole picture, and the
structure is valid. That is when recording *why* costs almost nothing. Reconstructing the same
meaning later — from leaves, after the fact — is expensive, lossy, and sometimes impossible.

But record the **reason**, not a snapshot. A stored copy of a collection is stale minutes later
as items are added and removed, and every consumer then has to guess whether it is still true. A
reason attached to a live structural element does not go stale the same way: *"this branch exists
to cover X, and Y belongs elsewhere"* survives a leaf being added or removed, moves with the
branch, and dies with it. **Prefer a durable annotation on live structure over any denormalized
copy** — and when you catch yourself proposing to save a blob "so we have it later", ask what
will make it wrong and how anyone would know.

**Step 4 — scale tiers, with a real fallback.** What works at 50 breaks at 6,000. Decide the
threshold BEFORE shipping and decide what happens past it: compartmentalize (relevant branch +
summary of the rest), summarize the far field into counts and clusters, or run a cheap
deterministic pre-filter that selects candidates. **A silent cap is the same defect as a missing
input and harder to see** — offer both shapes in the provision, record the ratio, log it.

**Step 5 — the output, and THE FULL-VALUE RULE.** If a question is worth assembling a large,
expensive context for, **take everything that context makes answerable**, not one slice. An
agent given the whole site to place one page should also write the missing SEO plan while it is
there. Paying for deep context and harvesting one field is the expensive twin of the same
carelessness — and it is what nested output kinds are for.

**Step 6 — the ground-truth check.** Decide in advance how you will verify the answer against
data you hold. Every entity the agent names — route, id, keyword, card, citation, chapter — must
be checkable against the set you sent. If you cannot state the check, the mandate is not
designed yet.

## VERIFYING — what a real test looks like

Three parts. Most "tests" have only the first.

1. **It ran.** Status, shape, schema. Necessary; proves nothing about truth.
2. **It could have been right.** Measure the input on real data — how much of the relevant
   universe did it see? Print the ratio. `1 of 295` is a failing test however good the prose.
3. **It IS right.** Cross-check every named entity against ground truth. Every route exists in
   the list you sent. Every cited id is in the input. Every quote is a verbatim substring.
   **Count the fabrications. The passing number is zero.**

Design tests to make failure visible, never to confirm success:

- **The trap case** — something the agent must catch (an overlapping page, a contradicting rule,
  a fabricated claim). Sailing past it means the test worked.
- **The near-miss** — looks like a hit, must NOT be flagged.
- **The honest-empty case** — the right answer is "nothing". An agent that never returns empty
  is an agent that invents.
- **The adversarial-scale case** — ten near-duplicate pages targeting one keyword. It can only
  be caught if the provision actually delivers the other nine.

### THE PLANTED CONFLICT — design the test from the failure modes

The strongest test is not a bigger assertion suite. It is a **scenario built backwards from
the ways the agent will be confidently wrong**, arranged so the right answer is reachable ONLY
if every part of the pipeline works, and the wrong answer is unmistakable to a human looking at
it.

How to build one:

1. **List the top ways this agent could be wrong while sounding right.** Not "it might fail" —
   the specific confident errors: it will cite a neighbour that does not exist; it will miss the
   duplicate because it never saw it; it will keep a keyword a human locked; it will call two
   pages distinct because their words differ while their intent is identical.
2. **For each, plant the decisive evidence where a broken pipeline cannot see it** — the far
   side of the collection, a different branch, a page whose slug shares no tokens with the
   target. If the selection, condensation, or delivery is broken, that evidence never arrives
   and the agent MUST get it wrong.
3. **Make the failure legible.** A human glancing at the output should be able to say "it missed
   the obvious one" without running anything.
4. **Confirm the test can fail.** Run it against the broken version first. A planted conflict
   that the OLD pipeline also passes proves nothing and must be redesigned.

This is deliberately a **human-judged setting, not an assertion suite**. The point is not that a
program says PASS; it is that two people can look at the answer and see instantly whether the
system actually knew, or merely sounded like it did. These are cheap to build once you have
listed the failure modes honestly — which is why step 1 is the work and everything else is
arrangement.

### DENOMINATOR DISCIPLINE — the wrong population produces a real-looking lie

A measurement is only as honest as the population it counts. **State the denominator and defend
it before you trust the ratio.**

Measured case (2026-08-25): "keywords exist on ~12 of 11,000+ pages" was a real number that
badly misdiagnosed the system — it counted CRAWLED pages, most of which were never planned. The
correct population was PLAN NODES, and against that, persistence was **100% on established
sites** (341/341, 219/219, 22/22). The actual defect was narrow and invisible in the wrong
framing: brand-new sites lose **100%** of their keywords. A wrong denominator can make a
localized, fixable bug look like a systemic drought — or hide a total failure inside a
comfortable average.

Ask: *what is the population this claim is about, and is that the population I counted?*

### SILENT SUCCESS IS THE WORST FAILURE MODE

The same case: the apply path lost **8 of 8** keywords and reported `created=9, failed=0,
errors=[], keywords_filled=0` — a completely clean result while losing everything. The one
function that knew (`assign_primary_keyword`) returned `None` on failure and **the caller
discarded the return value**. Downstream, a later gate blamed the USER for the missing keyword
("assign one in Setup").

When you write a step that can partially fail, the failure must reach the result. **A return
value that can mean "I did nothing" and is not checked is a silent-loss bug waiting to happen**,
and it will be reported to the user as their fault.

🚨 **Never design a test you know you will pass.** A test built from data you hand-picked to
suit the agent proves nothing and manufactures false confidence. **Real data is what wins** —
and when two designs are both plausible, build both and let real data pick, rather than
reasoning your way to a favourite.

**Report what you measured, not what you concluded.** "1 of 295 pages visible; 4 of 4 proposed
links do not exist" is a result. "Verified — output looks good" is not a claim anyone should
accept.

## MANDATE HYGIENE

- **One mandate, one job.** A mandate reused across jobs cannot have a truthful provision,
  because the two callers need different facts.
- **Mandates never go inside workflow nodes.** A workflow step NAMES a mandate; it never embeds
  one.
- **Before changing inputs, find every place the mandate runs** — server pipeline, durable
  workflow twins, client surfaces, regeneration paths. A rename that misses one caller breaks it
  silently.
- **The provision is code; the agent is a DB row.** Never fix a delivery gap by editing a prompt.

## THE HONESTY BAR

The Brief is not filed and forgotten — it is what a completion note is checked against.
Before writing that something works, you must be able to state:

1. **The question** the mandate asks, in one sentence.
2. **The facts required**, and where each comes from.
3. **The measured coverage** — visible / total, on real data, as a number.
4. **The ground-truth check** you ran, and the fabrication count.
5. **What happens at scale**, and when a required input is missing.
6. **The swap test result** — what a different agent could reach for that this one ignores.

Missing any of these, the correct completion note is **"not verified"** — never "done". Writing
"done" over unverified work is worse than writing nothing, because the next person believes you.

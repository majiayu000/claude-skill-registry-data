---
name: qfai-grilling
title: QFAI Grilling (Design interrogation)
description: "Interrogate an unfixed design in rounds: a tree of open decisions, a frontier of the ones answerable now, facts read rather than asked, and an end condition the user holds. Use when a stage calls for a grilling session, or when asked to grill or stress-test a design."
allowed-tools: [Read, Glob, Grep, Bash, TodoWrite, Task, Agent]
mode: interactive-by-default
---

## qfai-grilling - interrogate a design before it is fixed

The one implementation of the interview method. A skill that needs a design
interrogated invokes this rather than writing rounds of its own, so there is one
method to review when it changes and one behaviour an operator learns.

## What this is for

A design has open decisions. Left open, they are decided anyway — by the agent,
silently, at the moment the code needs an answer. This method surfaces them
first, in an order where each can be answered honestly,
and stops at one of five named endings: the user confirms the understanding is
shared, closes the asking, or stops the session, a delegated session adopts the
griller's recommendations, or a run that may not ask writes every node left
where its stage's gate reads it.

**The invoking stage picks the session.** A stage whose work is the
interview holds a user session; any other holds a delegated one, where a griller
interviews the session agent and only a critical decision reaches the user, and only
for a decision the repository cannot settle (`.agents/rules/grilling.md` § When
a session is held). Without one, no griller starts. A stage that says nothing
holds a delegated session where one is held. Read
`references/discussion-delegation.md` before delegating a user discussion;
record actual authority. No-question alone is not
delegation.

**The request bounds the tree** (`.agents/rules/grilling.md`). A decision whose
only outcome is whether to add something the request did not ask for is left
out, not asked. Among the options for a real node, recommend the one that adds
least beyond the request.

## Non-goals

- **Not a substitute for a specification.** Work already specified is governed
  by the spec, and a disagreement with a requirement is a specification change.
- **Not a question budget.** How many questions are worth asking is Article VI's
  subject. This decides which are asked, in what order, and when asking stops.
- **Not a stage.** It runs inside whatever stage invoked it and produces no
  artifact of its own.

## Preconditions

| Condition                           | Effect                                                      |
| ----------------------------------- | ----------------------------------------------------------- |
| A design that is not yet fixed      | Proceed                                                     |
| The work is already specified       | Do not invoke; the spec is the authority                    |
| A no-question mode is active        | Run without asking; open every node left over as a question |
| An ambiguity met while implementing | Not a session — stop under Article IX of the constitution   |

**A no-question mode silences user questions, not the session.** The master's
explicit-delegation conditions permit author rounds. Otherwise, an invocation
told not to ask — `--auto`, or whatever the host spells it as — settles what the
evidence settles, dispatches the lookups, and opens every node left over as
a question in the register the stage reads, so the stage cannot complete over
it. Every node, not every decision: a fact only the user holds cannot be settled
from evidence either, and one declared undefaultable stops the run rather than
taking a value nobody has. Where a document requires the field to hold
something, write the defaulted value and label it an assumption beside that open
question
(`.qfai/assistant/rule/constitution.md` Article X, rule 6). What is
forbidden is the assumption with no open question against it. Declaring a
session is still not a way to ask.

## The design tree

The subject sits at the root. Below it hang two kinds of node, and a node hangs
off whatever it depends on.

| Node                       | Settled by                                    | State while open |
| -------------------------- | --------------------------------------------- | ---------------- |
| Decision                   | The user, when asked                          | Open             |
| Fact the environment holds | The agent, by reading or dispatching a lookup | Open, in flight  |
| Fact only the user holds   | The user, when asked                          | Open             |

**A fact the environment does not hold is still a fact.** An unpublished date, a
constraint that lives in a contract, a number only the user knows: no lookup
reaches it, and it is not a decision either. Ask for it as the value it is, and
with **no recommended answer** — nothing is being decided, so there is nothing
to recommend, and a recommended value the agent does not hold is a guess the
user is invited to accept.

Whether it arrives as options is a separate question, and the candidate set
answers it: a fact with a known few possible values is asked as a choice among
them, and one with no such set as a plain request. Asking which of four
supported regions is active as free text loses the four.

The tree is not written once: each answer changes what the remaining nodes are,
so it is the current state of what is settled, not a plan made at the start.

## The frontier

The frontier is every node that can be settled now: every decision whose
prerequisites are all settled — every decision it depended on answered, and
every fact it depended on read — and every user-held fact whose own
prerequisites are settled.

A user-held fact belongs there because nothing else can put it there. Left off,
the decision below it waits on a node no round ever asks, so the frontier never
empties and the session cannot complete.

## One round

1. Recompute the frontier from what is now settled.
2. Dispatch the fact lookups the remaining decisions wait on. Do not block the
   round on them.
3. Put the whole frontier at once to the session's answerer: the user by
   default, or authors in a qualifying delegated session. Order a round put to
   the user upstream first: a decision hard to reverse, or that others hang on,
   before one cheap to revise (`.agents/rules/grilling.md` § A round).
4. Read the answers, then return to step 1.

Two questions never share a round when one depends on the other; the dependent
one belongs to a later round. The next round is never written ahead of the
answers it is computed from.

**Every round checks terms against the glossary**: a clash or synonym is raised
first with the glossary's term proposed, and a settled term is written at once
(`.agents/rules/grilling.md#terms-against-the-glossary`); read
`references/glossary-check.md` when a term clashes, is missing or is settled.

**A no-question mode is read before any of this.** Agent rounds require
explicit delegation; otherwise the section above governs. A withheld tool with questions still
permitted uses the fallback.

**Three things send a round to plain text**: the host has no structured question
tool, the current mode withholds it while still permitting questions, or the
tool cannot carry the answer shape of some question in the round. **The whole
round falls back, not the question that triggered it** — a round split across
two carriers loses the thing a round is for, which is the user seeing what is
being decided together. Say why the tool was not used, and where the reason is
the third one, say which question it could not carry.

**Where the host's question tool takes fewer questions than the frontier holds**,
deliver the round in host-sized batches. The frontier is not recomputed between
them, no answer is acted on until the round is exhausted, and each batch is read
for a closing answer before the next is put. Batching is how one round reaches a
host that cannot show it whole; it never makes two rounds, and
`.agents/rules/user-questions.md` carries the rest of its mechanics.

## Facts are not asked

| Kind                                     | Who settles it | How                                       |
| ---------------------------------------- | -------------- | ----------------------------------------- |
| A fact the environment holds             | The agent      | Read it, or run reads as parallel lookups |
| A decision about what is wanted or worth | The user       | Ask it, and wait                          |

## User Questions (AskUserQuestion Protocol)

Follow `.qfai/assistant/rule/shared-skill-operating-baseline.md#user-questions-askuserquestion-protocol`.
Do not open a second path for a question. Every round goes through it, and so
does the confirmation that closes the session.

## Inputs Priority

When unsure, read inputs in this order:

- P1: `.qfai/assistant/rule/*`
- P2: `.qfai/assistant/rule/agent-selection.md`, then the project's policy files under `<paths.specsDir>/01_policy/` and its technology contract `<paths.contractsDir>/tech.md`
- P3: the subject the invoking stage named, and the artifacts it points at
- P4: the story tree under `<paths.specsDir>/**` and contracts under `<paths.contractsDir>/**`, as facts to read rather than
  decisions to re-open

A fact this order can settle is not a question. Reaching P3 or P4 for it is the
method, not a fallback.

## The shape of each question

Number each question, give it a title, and state the recommended answer on a
line of its own. That shape is what makes a round answerable by number: a user
who agrees with every recommendation says so once, and a user who disagrees with
the third names the third.

Decisions cheap to revise share one grouped question, put after the costly
ones: accept every recommendation, or name the items to decide separately. An
accepted group records each item as the user's decision; grouping is not
delegation. Never group a critical decision, a fact or a document-required
decision (`.agents/rules/grilling.md` § The shape of a question).

## The budget does not end a session

A grilling question spends no clarification budget, and exhausting the budget
does not end a session
(`.qfai/assistant/rule/constitution.md#article-vi--clarification-budget-avoid-endless-qa`).

A budget bounds the questions asked to resolve ambiguity in a request. These are
the decisions the design itself leaves open, and a cap on them ends the session
with those decisions still open — which the agent would then proceed on as
labelled assumptions, assuming exactly what the session existed to settle.

## When the session ends

A session **completes** on two conditions, both required.

1. No node is open — the frontier is empty **and** no fact lookup is still
   running.
2. The user confirms the understanding is shared. The sheet that carries it:
   `references/confirmation-sheet.md`.

Condition 1 is about the whole tree. When every remaining decision waits on a
lookup the frontier is empty while the tree still holds open nodes, and
completing there would close the session before the lookup could raise the
questions it was dispatched to answer.

There is no question cap. Read `references/session-check.md` before reporting a
session finished.

**A delegated session ends by its own conditions**, because no user is there
to confirm condition 2. Read `references/delegated-session.md` (§ When a
delegated session ends) when the session is delegated, or is a no-question
session that meets the master's explicit-delegation conditions. It holds the
round budget, when the griller's recommendation is taken, and when the session
ends `adopted`. A session with a user does not need it.

**Only a no-question session meeting the master's explicit-delegation
conditions ends `adopted`.**

**Any other session under a no-question mode cannot reach condition 2
either**, because the mode forbids asking the user. It ends when nothing on the
frontier is still waiting: every decision the evidence settled is settled, and
every one it did not is opened as a question where the stage's own gate reads it
(`.qfai/assistant/rule/constitution.md` Article X, rule 6). The register
write is the ending — without one, a stage that resolved its whole frontier by
inspection would wait forever for a confirmation nobody may give.

**Those endings have names, and there are five of them.**
`.agents/rules/grilling.md` carries them under **The five endings**:
`confirmed` when the user confirms an empty tree, `user-closed` when they close
the asking, `adopted` when a delegated session settles its tree, `no-question`
for the register write above, and `stopped` when they stop the session. A stage that records a session names one of them, and this
skill adds none of its own — the agent never confirms on the user's behalf.

### The user ends it whenever they say so

Completion is how a session ends on its own. It is not the only way one ends.

- **stop** ends the session immediately, frontier empty or not. Ask nothing
  further and do no further work. Report the open decisions as open, not
  assumed.
- **proceed** / **done** ends the asking, not the session's own work. Finish
  every lookup still running first, and record any decision it then raises the
  same way. The closure covers the tree as it finally stands, not only the nodes
  open when it arrived: a lookup that lands afterwards can expose a decision, and
  a record written before it lands omits exactly that one. Then continue, with
  each decision still open recorded as an assumption and labelled as one.

**Two kinds of node are never assumed, whatever the user answered.** A decision
some document requires the user to make and record — the approval an SDD triage
row waits on among them — and an input declared `hard-required` are outside the
assumption path. They are still asked, and where a no-question mode forbids
asking, the run stops and names them instead. Closing the questions waives the
agent's own uncertainty, never an authorization the user has not given.

## When talking cannot settle it

A question about how something should look, or how it should feel to use, needs
something to react to, and no number of rounds produces that.

Stop grilling and build something to react to. Then put it in front of the user
and ask the original question again against it. **Their** reaction is the answer,
and the questions it raises are a new frontier.

The artifact makes the decision answerable; it does not transfer ownership of it.
An agent that builds a sketch, judges it and carries on has settled a question of
taste on the user's behalf, which is the thing every round of this method spends
its effort avoiding.

What that artifact is belongs to the stage the session runs in: this skill
neither chooses it nor moves the work to another stage. A sketch inside the
current stage is the usual answer.

## Sub-agent Delegation

Follow `.qfai/assistant/rule/shared-skill-delegation-baseline.md`. The
sections below add only what is specific to a session; where they and the
baseline overlap, the baseline governs.

One thing may be delegated: reading facts the environment holds, as parallel
lookups under the baseline's gate. The questions are
never delegated — a round is put by the agent that holds the
session, to whoever is answering it.

Who that is depends on the mode. In a session with a user, it is the user, and
the agent they are talking to is the one that asks. In a session between agents
there is no user to reach, so the griller puts the round to the session agent,
the one author of the draft. That is a different answerer, not a delegated
question: nothing hands the asking to a third agent.

### Rounds between agents

Read `references/delegated-session.md` when a griller puts the round to the session agent
instead of a user. It holds how the round is held, which
agent puts the round, why a fact only the user holds goes to the user, and when
the griller's recommendation settles a decision. A session with a user does not
need it.

### Capability Probe

1. A fact lookup the session dispatches is its own capability check.
2. If it fails, classify per the baseline taxonomy before doing anything else.

### Delegation Failure (Hard Stop)

- `unavailable`: stop dispatching lookups and read what can be read directly,
  as the baseline's `unavailable` response sets out
  (`.qfai/assistant/rule/shared-skill-delegation-baseline.md`). Report the
  class, report every fact that stayed unread, and hold the decisions
  downstream of it open rather than asking the user for it.
- `saturated`: use the baseline's bounded retry branch. The session stays open.
- Do not simulate roles. An agent that answers a dispatched lookup out of its
  own recollection has recorded a guess as a fact, which the frontier then
  treats as settled.

## Work Orders Summary

A session that dispatched any lookup records a `## Work Orders Summary` table
in the artifact its invoking stage writes. Read `references/session-record.md`
for the table. It also lists what the invoking stage's reviewer confirms about
the session, so read it when reviewing one.

### Reviewer Gate

This skill produces no artifact, so the gate that covers a session is the
invoking stage's. A session run from the user-invoked entry point has no
invoking stage. There the gate is the user reading the record, which is why that
entry point writes no files.

## Default Autopilot Policy

Every decision this skill meets falls in one of three named buckets.

- auto-decide:
  - output formatting
  - equivalent-option pick
- ask-user:
  - every decision on the frontier of a user session — that is what a round is
  - a critical decision, in every session
  - the confirmation that closes a user session
- hard-required:
  - grilling subject (the design to interrogate; a session has no default for
    what it is about)

Explicit delegation is not `auto-decide` or a fact or human answer.
These user-session entries remain the default.

This skill's `ask-user` entries are its own operations, not prototype additions.

The buckets are the method, not a tuning surface. Moving a frontier decision to
`auto-decide` is the agent answering its own question without the rounds. A
delegated session's adoption is not that: the griller interviewed the session agent
first, and the record carries why.

## Related

- Question form and the fallback without the tool:
  `.qfai/assistant/rule/shared-skill-operating-baseline.md#user-questions-askuserquestion-protocol`
- The clarification budget and its exemptions:
  `.qfai/assistant/rule/constitution.md#article-vi--clarification-budget-avoid-endless-qa`
- Rejected options and drift: `.qfai/assistant/rule/drift-protocol.md`

project_memory:

- A grilling question spends no clarification budget, and the confirmation that closes a session is exempt with it. A session ends at one of five endings — `confirmed`, `user-closed`, `adopted`, `no-question` or `stopped` — never at a count.
- A session is delegated unless its stage says it is a user session. A delegated session adopts the griller's recommendation and asks the user only a critical decision. A fact the environment holds is read, never asked.
- The request bounds the tree: a decision that only adds what the request did not ask for is left out, not asked.
- A no-question mode silences the questions, not the session: such a run settles what the evidence settles and opens every node left over as a question — facts only the user holds among them — with a labelled value beside it where a document requires one. The assumption alone is forbidden, and a fact declared undefaultable stops the run.
- A user's `stop` ends a session immediately and the open decisions are reported as open. A mandatory approval and a `hard-required` input are never assumed, whatever the user answered.

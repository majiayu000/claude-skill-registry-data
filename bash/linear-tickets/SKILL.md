---
name: linear-tickets
description: "Use when creating or updating Linear issues."
version: 1.0.0
author: Charles Ponti, Hermes Agent
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    tags: [linear, issues, ticket, graphql, tracking]
    related_skills: [github, project-operations]
---

# Linear issues, created and verified

For when work goes to Linear rather than GitHub — a feature parked for later, research handed to another
agent, a decision that needs a written record. The mechanics are a GraphQL call; the value is in the shape
of the ticket and in proving it landed whole.

## When to Use

- "add this as a ticket to Linear", "park this", "research this later"
- a decision is deferred and needs its reasoning preserved where the user keeps work
- an issue needs its body rewritten, its priority set, or a comment cross-linking another tracker

## Auth

- The key usually lives in the user's own shell file, and it may be written `export LINEAR_API_KEY=…` — a
  `^NAME=` regex misses the `export` form and a session concludes there is no key.
- Find the **name**, never the value, and never print either into chat or a log:

```bash
grep -oE '[A-Za-z_]*linear[A-Za-z_]*=' ~/.localrc | sort -u   # names only
```

- Personal API keys go in a bare header — `Authorization: <key>`, no `Bearer` prefix. Build the request in a
  script (Python `urllib`, or `curl` fed on stdin) rather than interpolating the key into a shell command you
  will echo back.
- A connector and a key are two paths to the same thing. If the Linear connector reports `not_connected`, do
  not re-mint the authorization on your own; ask, and use the key as the fallback the user offered.

## Create one

```graphql
mutation Create($input: IssueCreateInput!) {
  issueCreate(input: $input) {
    success
    issue {
      identifier
      url
      state {
        name
      }
    }
  }
}
```

- `teamId` is required; every team id comes from `{ teams { nodes { id name key } } }` — query it first. When
  there is one team, that is the answer, and saying which team the ticket landed in makes a misfile one click
  from being noticed.
- **Do not guess `project`.** A workspace's projects encode the user's own taxonomy (incubators, business,
  legal, per-product); filing into the wrong one is visible and annoying. Leave it empty and say so.
- `priority` is 0 none, 1 urgent, 2 high, 3 medium, 4 low. Parked research is 4.
- Markdown in `description` renders: headings, tables and fenced code are all fine.

## A label can be a job trigger

In a workspace an agent fleet watches, a label is not metadata — it is the instruction to spend money. The
`agents` label on a ticket whose project resolves to a repo makes the dispatcher claim it, open a session and
start working, and **un-labelling is the only control that stops a worker mid-flight**.

- **Create unlabelled unless the operator asked for it to run**, and say in one line that adding the label
  dispatches it. A ticket filed for review and silently labelled starts costing the moment it lands.
- Label ids come from `{ issueLabels(first: 100) { nodes { id name } } }`; add one with
  `issueUpdate(id: $id, input: { addedLabelIds: [$labelId] })`. `labelIds` **replaces** the whole set — use it
  only when you mean to remove the others.
- A labelled ticket still needs a target: the project's name or description must resolve to exactly one
  allowlisted repo. If it does not, the ticket sits unclaimed with no error on either side — check that before
  saying it will be picked up.
- Proof it was picked up is the fleet's log, not the tracker: the poll count rises, then either a claim or a
  skip naming the reason (`all worker slots are occupied`, `already picked up once`, `retry in Ns`). Quote that
  line rather than "the ticket is labelled".

## Verify by reading it back

The mutation returning `success: true` is not proof the body arrived — an oversized or malformed description
can land truncated, or without its sections, and the response still looks healthy. Query the issue by number
and check the state, the priority, the character count, and the first and last characters:

```graphql
{
  issues(filter: { number: { eq: N } }) {
    nodes {
      identifier
      state {
        name
      }
      priority
      project {
        name
      }
      labels {
        nodes {
          name
        }
      }
      description
    }
  }
}
```

A body that opens with the expected first section and ends with the expected last line is the claim worth
reporting. Anything shorter is a truncation to fix before saying it is done. Read the labels and the project
back too — a ticket created with the right body in the wrong project, or with a dispatch label nobody asked
for, is a different failure that the text check cannot see.

## What belongs in a parked ticket

A ticket for work the user is not ready to do is a record, not a stub:

- why it exists, and the constraint that makes it dangerous or expensive
- what is already established, so nobody researches it twice, with the source of each fact
- the decisions still open, each with a recommendation attached
- what will _not_ be built, and why
- a deliverable sentence: what closing this ticket actually produces
- the links that matter: the existing issue, the repo doc, the live product

Then keep a versioned copy at `docs/tickets/<slug>.md` in the repo with the ticket URL as its header, and
cross-link the existing GitHub issue with a comment rather than closing it — two trackers that disagree about
state is worse than one stale tracker. The doc says in its own words that nothing has been built, so a later
session cannot read it as started work.

## A defect ticket an agent will implement

A parked ticket records a decision; a defect ticket has to be executable by someone who was not in the
conversation. Keep the sections in this order — the same eight headings make a batch of them readable:

1. **Problem** — what is wrong in one paragraph, with the observed numbers (a limit exceeded by how much,
   how many rows, how long). No adjectives where a figure exists.
2. **Evidence** — the journal rows, the timestamps, the SQL or command that reproduces the reading, and
   `file:line` for the code path involved. Anyone must be able to re-derive the finding without you.
3. **Root cause** — the specific line, gated on the specific condition, and what that condition actually
   means. Quote the two or three lines; if you cannot point at a line, you have a symptom, not a cause.
4. **Proposed solution** — numbered, smallest first, each naming the invariant it restores.
5. **Scope** — in scope and out of scope, with the neighbouring defects named so the worker does not
   absorb them.
6. **Acceptance criteria** — checkboxes, each a falsifiable assertion, including the **negative** case that
   must keep working (the guard that must not fire, the finished work that must not be relabelled).
7. **Tests** — one line per test: the case, and what it proves. Name the regression replay explicitly.
8. **Agent notes** — the files to touch, the trap to avoid, and where the evidence can be re-queried.

**Size it to one worker session.** A ticket naming three modules and a dozen tests can exceed a worker's
per-task spend cap and be braked mid-flight — after it has opened its pull request and before it can answer
review. If the work is that large, split it, or name the budget the worker must fit inside; a ticket that
exceeds the cap produces a half-finished PR and an unresolved review thread, not a fix.

When the target workspace has a fleet watching it, the ticket is also a prompt — check that it does not ask
for anything the worker will refuse to write (infrastructure detail, credentials) before filing it.

## Pitfalls

- **Search before creating.** One call across open issues for a title fragment stops a second ticket for the
  same decision.
- **A defect that has a measurement is priority 2, not 4.** A guard that fires late or not at all is an
  active risk; parked research is 4. Get the number first, then set it — priority without evidence reads as
  urgency, priority with a figure reads as a finding.
- **Do not report the URL from the create response as the outcome** — report what the read-back showed.
- **A ticket is not a conversation.** Options weighed and dead ends belong in the description or the repo
  doc; keep chat about it short.

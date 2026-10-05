---
name: investigate
description: Plan how to dig into a fuzzy problem, run the hands-off parts as a workflow, then work through what it found.
argument-hint: "[question, e.g. \"why can't some users log in?\"]"
---

# Investigate

A fuzzy task like "some users can't log in" or "the dashboard is slow" has two jobs
before any code changes: understand what the system does now, and understand what
each fix would change for the people using it. This plans that work with the user,
hands the parts that need nobody watching to a workflow, and keeps the part that
needs them in this session.

```
question
   |
   v
1. pin it ......... a few questions the code can't answer
2. plan it ........ the user approves the steps
3. run it ......... workflow: traces + readers --> docs/investigations/<slug>.md
4. understand it .. /understand on that doc, here, with the user
```

Two ways this fails. Agents dig in the wrong place because nobody checked the plan,
and come back with a confident answer to a question nobody asked. Or the doc comes
back, the user skims it, and they know what it says without knowing why, which is
where they started plus a file. Step 2 exists for the first, step 4 for the second.

## 1. Pin the question

The question is `$ARGUMENTS`, or ask for one.

Look before you ask. Skim the README, the routes, the area the question names, so
you only ask what the code can't tell you:

- **What's happening.** Who's affected, what they see, since when. "Some users" is
  a clue: which ones? A pasted error or support ticket beats a description. For an
  improvement, which page, how slow, for whom.
- **What should happen.** Code shows what it does, never what it should. Expected
  behavior comes from a person, a ticket, or a spec.
- **What they'll do with the answer.** Fix it, estimate it, explain it to a client.
  That sets how deep to go.

Ask in one turn. "Don't know" is a fine answer. It goes in the doc as an open
question rather than becoming a reason to keep asking.

## 2. Propose the plan

This is the answer to "how should I prompt you?", written down so the user can
change it before anything runs.

Two kinds of step:

- **trace** runs one scenario in development with `/trace` and records what
  happened. Use it when the behavior can be reproduced: the login that fails, the
  page that's slow. The callback nobody mentioned only shows up in a run.
- **explore** reads the code or the git history for one question. Use it for
  breadth a single run can't show: every way sign-in rejects someone, what changed
  last month, every page that renders the slow partial.

Show it like this:

```
Hands-off (one workflow)
  1. trace    user signs in with email and password
  2. trace    user who signed up as Sam@Example.com signs in as sam@example.com
  3. explore  every way sign-in rejects a user, and the message each shows
  4. explore  what changed in sign-in since August (git history)

Then here, with you
  /understand docs/investigations/users-cant-log-in.md

Can't reach
  production logs, the affected accounts. Paste them if you have them.
```

- Each step answers a question you can name. If you can't say what it's for, cut it.
- Two to six steps. More means it's two questions; say so and pick one.
- Name what the run can't reach: production data, error trackers, third-party
  dashboards, real devices and networks. An investigation that never says where it
  couldn't look reads as one that looked everywhere.
- If another skill should go first, say so instead. No idea what the domain is:
  `/eli5`. The business process itself is unclear: `/domain-model`.

Then stop and wait for them to approve, edit, or redirect. Don't run a plan they
haven't seen. That checkpoint is why this exists instead of "explore and tell me".

## 3. Run it

Hand `assets/workflow.js` to the Workflow tool:

```
Workflow({
  scriptPath: "<this skill's directory>/assets/workflow.js",
  args: {
    question: "why can't some users log in?",
    slug: "users-cant-log-in",
    skillDir: "<this skill's directory>",
    context: "<what they told you in step 1, in their words, plus anything pasted>",
    steps: [
      { kind: "trace", brief: "user signs in with email and password" },
      { kind: "explore", brief: "every way sign-in rejects a user, and the message each shows" }
    ]
  }
})
```

If `scriptPath` is refused, read the file and pass its contents as `script`. Don't
rewrite it from memory.

The script runs traces one at a time, with readers alongside. Two traces against one
development database step on each other's rows and ports; readers only read. Then
one agent opens every citation, drops what doesn't hold, and writes the doc.

No Workflow tool? Run the same steps as subagents yourself, traces one at a time,
then the write-up from `assets/investigation-template.md`. Say that's what you did.

## 4. When it returns

Don't paste the doc. Say:

- the path
- `cause`: `established`, `suspected`, or `unknown`. Unknown is a result, and the
  doc's first option is then how to find out.
- `deadSteps` and `holes`: what nobody checked

A halted run returns `haltedAt` and `reason` instead, plus whatever it gathered.
Hand that over as is. Someone is about to pick this up by hand.

## 5. Hand off to /understand

Invoke `understand` with the doc path. Pass along what they said in step 1 about
what they'll do with the answer, so it doesn't ask again.

`/understand` isn't a workflow step because it's a conversation. A workflow agent
can't ask the user anything, so the step would come back as an explanation, which
is exactly what `/understand` refuses to give: people nod at an explanation and keep
nothing.

If they'd rather stop here, that's their call. Once they've picked an option,
`/slice` it. Doubts about one: `/rubber-duck`.

---
name: spec-session
description: Run a spec session on a GitHub issue — turn a request:new into a feature spec, write or amend its business sections with the product owner, write the Technical spec with a developer (ending with a fresh spec-checker subagent's report, fixed before the ready label), or (unattended, from deliver) split a feature:ready feature into task sub-issues from the slices its Technical spec lists. Always reconciles comments posted since the body was last edited before writing anything. Use when someone says "spec session for #N", "/spec N", "write the spec for #N", "add the technical spec to #N", or "split #N".
---

# Spec session

You write the body of a `feature:*` or `task:*` issue on behalf of the person
running the session. The rules in `docs/internal/agent-rules/delivery.md` are
binding; the ones that matter most here are 3 (the body is the spec), 4
(reconcile first), 5 (never rewrite a reporter's issue), 6 (outcomes, not
implementation), 7 (the Technical spec is the developer's) and 17 (native
changes).

Arguments: an issue number, optionally a mode — `business`, `technical`,
`split`, or `revise` — and optionally `unattended`. Without a mode, infer it
from the issue and confirm with the person before writing:

| Issue                                            | Mode                     | Who you interview        |
| ------------------------------------------------ | ------------------------ | ------------------------ |
| `request:new`                                    | create a feature from it | product owner            |
| `feature:spec`, business sections incomplete     | `business`               | product owner            |
| `feature:spec`, business done, no Technical spec | `technical`              | developer                |
| `feature:ready` whose Technical spec has Tasks   | `split`                  | nobody (`unattended`)    |
| anything with comments since the last edit       | `revise`                 | whoever owns the section |

**Unattended** is only for `split` on a `feature:ready` feature, run by the
`deliver` skill. The developer's `feature:ready` already accepted the business
sections, the Technical spec and every linked ADR (delivery rule 1), so nobody
is asked anything. Where an attended session would ask, decide from the
feature body, the ADRs and the codebase. Stop instead, and report why, when:

- reconciling finds a comment that would change the spec;
- a decision needs a new ADR (constrains more than one task, or is expensive
  to reverse);
- a slice cannot be specified without a question only a person can answer.

## 1. Load the issue

```bash
gh api graphql -F owner='{owner}' -F repo='{repo}' -F number=<N> -f query='
  query($owner:String!,$repo:String!,$number:Int!){
    repository(owner:$owner,name:$repo){ issue(number:$number){
      id number title body state createdAt lastEditedAt author{login}
      labels(first:10){nodes{name}}
      parent{number title}
      subIssues(first:50){nodes{number title state}}
      comments(first:100){nodes{url author{login} createdAt body}}
    }}}'
```

Refuse to continue if the label is `bug:*`, or if it is `request:new` and the
mode is anything other than creating a feature from it: those bodies belong to
the reporter. If the body has a `Request: #M` line, load issue M the same way;
its comments are part of the discussion.

## 2. Reconcile

The cut-off is `lastEditedAt`, or `createdAt` if the body was never edited.
Take every comment on the issue and its linked request created after the
cut-off, and decide for each whether it changes the spec. Present the result
as a list, one proposed change per item, naming the comment's author, its URL
and the section it touches. Comments that change nothing are not listed.

Ask the person to accept or reject each item, one at a time. Unattended, any
item stops the session. Accepted items are folded in when you write the body.

## 3. Do the session

Every attended mode is an interview: one question at a time, each with your
recommended answer, so the person can just say yes. Read the codebase instead
of asking whenever it can answer. Push on vague answers until each line is
something a reviewer could check.

**Creating a feature from a request.** Interview the product owner for the
business sections of `docs/internal/templates/feature.md`, Problem through
Open questions, starting from the visitor's words in the request. Keep the
visitor's intent; sharpen it into outcomes and completion conditions someone
can check on the booth phone. Then:

```bash
gh issue create --title "<title>" --label feature:spec --body-file - <<'EOF'
<the body>
EOF
gh issue comment <request> --body-file - <<'EOF'
Being specified in #<new>. This request stays open until that feature ships.

_Written by an agent._
EOF
```

The new body's first line is `Request: #<request>`.

**`business`.** Write or amend Problem through Open questions. Push back on
anything that names a mechanism rather than an outcome, unless the mechanism
is itself a requirement. Open questions stays non-empty while questions
remain; the feature does not leave `feature:spec` until it is empty.

**`technical`.** Interview the developer for the Technical spec. Read the
code first, so your recommended answers name real files. Cover, in order:

1. Packages and modules touched, contract first (architecture rule 2).
   When the feature adds or changes a dependency between feature modules or
   packages, draw it as a Mermaid flowchart under Diagrams; when the order
   of actions, requests or domain events matters, draw a sequenceDiagram.
   Only where a picture says it faster than prose, with the real names from
   the spec; otherwise Diagrams reads "none".
2. Contract changes: each schema in `packages/contract` and its fields.
3. Native change: does any part need a new app dependency with native code,
   an `app.json` plugin, or a permission? Check
   `docs/internal/NATIVE-CAPABILITIES.md` first: it lists the native modules,
   permissions and config the installed booth binary already has, and what
   is there can be used over the air. Anything it does not list needs a
   native build. If that can be avoided, write the JS alternative; if not,
   say so — it will not ship over the air (rule 17).
4. Rules in play.
5. Failure modes and limits: what the user sees when the API is down, the
   input is empty, too long or malformed, or the list is huge; every bound
   the build must enforce (a length, a count, a timeout), with its number.
   `docs/internal/agent-rules/defaults.md` already answers the common cases
   (inline error with retry, skeleton while loading, empty states, body
   limits, offline); write only where this feature differs. An agent builds
   exactly what is written, so a limit nobody wrote down and no default
   covers is a limit nobody enforces.
6. Agent hooks: what a device check needs to reach and read the outcome
   without guessing. The appduct tools a Done when line relies on, existing
   (`app_info`, `open_route`, `ota_check_now`, `show_update_banner`, …; see
   the `appduct` skill) or new (name, input, output, read-only or
   destructive — the implementer adds them); the deep links
   (`apexfactory:///<route>`); and the `testID` and accessibility label of
   every element a simulator line or `e2e:` test names. "none" when nothing
   needs the app running.
7. Tests, one title per line, prefixed `contract:`, `api:`, `mobile:` or
   `e2e:` (testing rule 6). `e2e:` is an agent-device replay script under
   `apps/mobile/e2e/`, for a claim only a running app can show. Every
   completion condition is covered by at least one.
8. Size: if it is more than one PR an agent can land in an hour, list the
   slices under Tasks, each a vertical slice a user could see, in dependency
   order.

For a booth feature, start the body from
`docs/internal/templates/booth-feature.md`: it is pre-filled with the house
defaults, so the session only writes what is specific to this idea.

Ask whether any decision constrains more than one future change or would be
expensive to reverse. Each such decision becomes an ADR: draft it in
`docs/internal/adr/` at status _Proposed_ on a branch, add its line to
Decisions, and tell the developer the feature cannot leave `feature:spec`
until it is accepted. Never set `feature:ready`; that is the developer's
signature.

**Spec check (end of `technical`).** Before telling the developer the spec
is done, start a fresh `spec-checker` subagent with the `task` tool, prompt
`issue #<N>` and nothing else — it reads the body as written on GitHub, so
post the body first (step 4). It reports contradictions with a rule or ADR,
Done when or completion lines nobody could test, failure modes neither the
spec nor `defaults.md` answers, native capabilities the binary lacks ("needs
native build"), and selectors missing from Agent hooks. Walk each finding
with the developer, one at a time, with your recommended fix, fold the
accepted ones into the body, and run the checker once more if anything
changed. Tell the developer to set the ready label only once it says
`Verdict: ready` (or they have decided to accept a finding). A spec that goes
out with these gaps comes back as a parked run.

**`split`.** For each slice under the feature's Tasks, write a body from
`docs/internal/templates/task.md`: Scope from the slice, a Technical spec cut
from the feature's (only what this slice needs, diagrams included), Done when, Out of scope and
Depends on. Before creating anything, check every task body, and fix it when
one of these holds:

- **Contradictions.** A Done when line that the task's own Tests or Scope make
  false. Run the grep or read the file the line names; do not judge it from
  the wording.
- **Unverifiable lines.** A Done when line no reviewer could check from the
  diff, the suite, or a named command.
- **Overlap.** Two tasks that touch the same file or change the same contract
  schema run one after the other: the later one lists the earlier one under
  Depends on. Two agents editing the same lines in parallel is a merge
  conflict the second one resolves blind.
- **Simulator lines.** A Done when line that needs the app running says so in
  its own words ("on the simulator: ..."), so delivery verifies it there,
  and names an outcome a device check can address: an element by the
  `testID` or label listed under Agent hooks, or text on screen ("on the
  simulator: `shipped-feature-12` reads 'Confetti button'"). A line that
  only a person's eye could judge ("looks nice") is not checkable; rewrite
  it.
- **Agent hooks.** Every tool, deep link and selector a task's lines rely on
  is in that task's Agent hooks; a tool two tasks need is added by the
  earlier one, and the later one depends on it.

Then create each task and attach it to the feature:

```bash
gh issue create --title "<title>" --label task:draft --body-file - <<'EOF'
<the body>
EOF
gh api graphql -F parent="<feature node id>" -F child="<task node id>" -f query='
  mutation($parent:ID!,$child:ID!){
    addSubIssue(input:{issueId:$parent,subIssueId:$child}){ issue{number} }}'
```

Get a node id with `gh issue view <n> --json id -q .id`. Replace the feature's
Tasks list with links to the sub-issues in order, and move the label:

```bash
gh issue edit <feature> --add-label feature:planned --remove-label feature:ready
```

Unattended, the feature's `feature:ready` is the approval, so tick each task's
box yourself — in a second body edit after the task exists: the issue-state
workflow promotes a task on body edits only, so a box ticked at creation would
leave it in `task:draft`. Attended, leave the boxes for the developer.

**`revise`.** Only the reconcile step plus the amendments it produced.

Write the spec the way rule 12 asks: short sentences, common words, one idea
per sentence. An agent will build exactly what it says, so every sentence
that does not constrain the build is a sentence to cut.

## 4. Write back and leave a marker

With a person present, show the new body first and wait for a yes before
posting. Unattended, post directly.

Edit the body in place, keeping every section that already existed:

```bash
gh issue edit <N> --body-file - <<'EOF'
<the body>
EOF
gh issue comment <N> --body-file - <<'EOF'
Spec updated: <which sections were added or changed, one line>.

_Written by an agent._
EOF
```

Issue bodies you create end with `_Written by an agent._` too. Never post the
spec, or a summary of it, as a comment. Never edit a `request:new` or `bug:*`
body. Never set `feature:ready`.

## Report

End with exactly this block:

```
Issue: #N  Mode: create | business | technical | split | revise
Wrote: <sections changed, or "nothing">
Created: <#issues with their Depends on, or "none">
Spec check: ready | fix first (<open findings>) | not run (<mode>)
Stopped: <why, or "no">
```

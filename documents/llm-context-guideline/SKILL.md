---
name: llm-context-guideline
description: Placement and admission policy for content that enters LLM context;
  its chapters currently govern the memory store (admission whitelist, the
  three proof questions, entry form and labeling, canon change rules,
  model-context phrasing, the proposal review and landing flow). Reload in
  full before touching memory content.
user-invocable: false
---

# Memory Curation Policy

The store manages session context, and context is capability: a model reasons worse as its
window fills, so curation optimizes for the smallest store whose entries still change future
actions. Every entry taxes future sessions through one of three delivery paths: resident topics
inject in full at every master spawn, every other entry adds an index line there, and a topic
query pulls its whole topic. An entry earns admission when the action it changes outweighs the
context it permanently occupies; a surface the reader already reads unconditionally (a prompt, a
skill, the owning repo's docs) wins over the store.

The memory store (`$CHARLIEBOT_HOME/memory/`) is a local git repo of labeled entries: one durable
fact or rule set per file under `entries/<topic>/<slug>.md`, with front matter restricted to
`scope`, `topic`, `audience`, `title` and a pure-markdown body.
Sessions only stage candidates (`charliebot memory add` writes to `staging/`): a staging
candidate is a free-form capture whose labels are assigned at curation and whose change intent
lives in the body. The canon changes in two ways. The daily curation run lands its reviewed
proposal with `charliebot memory proposal land <sha>`. A session commits a change that the user approves.

This file governs the daily curator AND ad-hoc user-directed promotions: the same admission test
and labeling rules apply in both flows.

## Phrasing for model context

Text that enters model context follows the "Text a model reads" subsection of the Writing
Style section in prompts/master.md.

## Admission test

Admission is judged at curation time, with evidence, over staged candidates. The store admits three
kinds of entry, and only these:

1. A ruling or preference the user stated, when a capable model does not follow it by default.
2. A mechanism or fact whose rediscovery would cost a real investigation and that still reads
   true a month from now.
3. A host, cluster, or account level pointer that cannot be guessed and has no owning document.

Everything else stays out by default; when in doubt, reject the candidate and name it in the PR
page. The model itself is the canonical home for general engineering and statistical
reasoning. An entry records what holds across models, fixes, and runs: rules, mechanisms, and
contracts. Entries hold durable mechanisms and standing policies: execution logs and `LESSONS.md`
retain ephemeral identifiers, transient instance names, and active incident telemetry; repository
guides and skills retain documentation and reference procedures, with the store carrying at most
a pointer line; and runtime inspection resolves on-demand system facts.

State each fact at the category level in its most concise form, bounded to one to three lines of
core conclusion, keeping narrative deduction and case histories in session records. Phrase each
line by the `## Phrasing for model context` rule above.

Admit or revise an entry only when it changes future action, belongs in the store, and states its facts concisely.
Reject a candidate that fails any of these tests.

- Describe the recurring or planned work in a named project or stack that the entry changes.
- Compare the store with the natural homes: repo knowledge in repo docs; CharlieBot behavior in prompts, skills,
  config, or source; incidents in `LESSONS.md`; run results, live state, and receipts in run or session records; and
  experiment verdicts in the tracker. Keep project knowledge with its project, and cluster or host facts only when
  they bind every project there.
  Name the reader and an existing delivery path that reaches them when the entry changes their action. Keep domain
  conventions with their domain and session-wide rules in resident topics, since resident entries enter every master
  spawn in full. When a natural home is blocked, fix the obstruction or use a tracked path inside that home.
- Trim the entry before presenting it. Name the canonical home when trimming moves a fact that another home owns.

A candidate's text is a claim: before presenting its figures, verify them against the live system with read-only
queries that cause no side effect for any account, excluding:

- completion or inference calls;
- writes;
- requests that the claim predicts the system refuses.

A revise re-verifies the surviving claims of the entry it edits with the same read-only queries. When no read-only
query can check a claim, keep its text. Name that claim as unverified on the PR page, with the reason.

A trap claim about shared infrastructure enters only with its root cause named and reproduced
outside the originating session; a fixable obstruction is fixed instead of recorded.

Data cheap to re-obtain on demand lives in session reports and run dirs; the store keeps the
takeaway that tells the reader where to look.
Measured figures, benchmark scores, and one-off measurements count as data cheap to re-obtain on demand.

## Admission is merge-first and strict

The default action for a passing candidate is **merging into an existing entry**, a `revise`
that extends the entry whose theme already covers it, so `git diff` shows the before and after.
Creating a **NEW** entry additionally requires both:

a. **No theme coverage**: no existing entry's theme covers this candidate; check the index
   (`charliebot memory query --index`) before proposing one.
b. **Title-honesty**: the title honestly describes the entry's whole content after the change.
   A title that over- or under-states the body is a reject reason.

## The skills boundary

The store holds decision knowledge: facts, rules, and conventions that change what the
reader does next. Step-by-step operating procedures (command sequences, recipes, and their
reference files) live in the owning skill: reject procedure-shaped candidates and name the
owning skill in the PR page. Live state under active investigation stays with its owning
system. One home per item: when a rule is admitted to the store, the store entry replaces the
skill's copy of it.

## Labeling: the three axes plus title

Every entry carries `scope`, `topic`, `audience`, and `title` in its front matter:

- **scope** in `user` | `host`: `user` follows the human across machines; `host` is tied to this
  machine (hostnames, local paths, hardware, internal endpoints).
- **topic**: one entry has exactly one topic, equal to its `entries/<topic>/` directory and
  present in the `topics` vocabulary. The `topics` vocabulary grows only by user ruling.
  Cross-topic content belongs in a resident topic
  (`workflow`, `rulings`). The ` resident` suffix in `topics` marks topics whose entries inject in
  full at master spawn. Reads are topic-granularity: a query returns the whole topic (audience-filtered), and agents see
  topics only, split entries for curation and audience separation, with the topic as the sole retrieval unit.
- **audience**: comma list, each element in `master` | `worker`, at least one, who receives the
  entry's full body at spawn: master spawn gets master-audience entries in resident topics as
  full text, others as index lines; worker spawn gets worker-audience entries matching the repo
  basename as full text, others as index lines. Both roles: `audience: master, worker`.
- **title**: one non-empty line honestly describing the whole entry; it is what index lines and
  spawn-injected headings display.

## Entry form

One coherent fact or rule set per entry. The title lives in frontmatter; the body is pure
content. Timeless phrasing: state the standing reality. Dates, session ids, commit hashes,
quoted rulings, event history, and case enumerations belong in `LESSONS.md`.
Skip decision-attribution labels (`（用户定）`, `（用户裁定）`). Every entry stands by the curation
flow that admitted it, so the label carries no information.
State each fact once in English, and preserve code, paths, identifiers, and commands verbatim.
Follow the Writing Style section of `prompts/master.md`, including "Text a model reads". Apply the admission test to
each line and to the entry as a whole.
When a ruling's exceptions reveal its criterion, state that criterion; ask the user when none can be recovered.
Keep each line that changes what a capable model does. Lead with the action, and retain its purpose and needed
mechanism.
Keep receipts, verification notes, and secondary effects in session reports and run directories.
An entry body runs as long as its distinct durable facts require, judged by the admission test alone.
`rust/crates/features/memory/src/cli/proposal_check.rs` enforces 120 display columns per line.
`charliebot memory lint` and `charliebot memory proposal commit` report body line counts as advisory records.
A measured figure lives in its canonical source (run dir, canon table, ticket); an entry states
the rule and points there.
Environment composition and version facts (package pins, toolchain and interpreter versions,
build and model numbers) live in the manifest or config that pins them: the entry states the
rule and points there.
Machines go by hostname; a role phrase like "the CharlieBot host" re-points when infrastructure
moves. When context changes, revise the entry in place (a capture whose body states the change
stages the proposed new text).
A retired or archived system's content leaves the store outright, entries and lines alike: the
store states standing reality, and `LESSONS.md` holds the retirement event when it matters.

## Commit message prefixes

Curation commits use one of four prefixes so `git log` enumerates the canon's history:

- `admit: <topic>/<slug> (<title>)`: a new entry promoted from staging.
- `revise: <topic>/<slug> (<title>)`: an in-place edit of an existing entry (including
  merge-ins of change-proposing captures).
- `remove: <topic>/<slug> (<title>)`: an entry's removal from the store.
- `scaffold: <description>`: a `topics` vocabulary change, adding or retiring a topic.

A commit body carries the entry's three proof lines, each headed by the question it answers,
plus one `Staging: <file>` line per staging candidate the commit consumed.

## Proposal review and landing

The day's curation reaches the user as one pull request: the `proposal` branch of the memory
repo, drafted in the git worktree `$CHARLIEBOT_HOME/memory-proposal/`, where the selector writes
the day's entry and `topics` edits uncommitted and the reviewer commits them entry by entry
through `charliebot memory proposal commit <store-relative path> --message-file F`.
After its commits pass the lint, the reviewer runs `charliebot memory proposal land <head>` with
the PR head that `charliebot memory proposal status` reports. The `land` command fast-forwards the
live store to exactly that head, so the store holds the version that the lint passed.
The user reviews each landed range afterwards through its diff page (the `diff_path` line of the
`land` output) and the PR page. The PR page lists:
- every PR commit with its proof lines
- the reviewer's rewrites of the day
- the conflicts between new candidates and existing PR lines
- the candidates rejected since the PR opened
When a reply reports a curation run, give the diff page as an absolute markdown link:
`[diff](<base_url><diff_path>&session=<curator session id>)`, beside the PR page link. Resolve
`<base_url>` as the file-server skill states. The `session` parameter routes diff-page comments to
the curator session.
When a reply reports a refusal, quote the refusal and name its cause. This lets the user see the
cause in the reply itself.
`charliebot memory proposal open` rebases the PR onto the live base when the base moved.
A diff-page comment on a landed range is a user-directed fix.
A delegated worker edits only the commented lines and commits them to the live store's base branch.
This keeps the fix to the lines the user commented on.
When a user-directed fix or a prose-check rewrite changes lines that the PR added,
commit it with --replace-pr-lines.
Each user comment on a landed range is evidence of a rule gap. After applying the comment, check
whether the rules above would have kept the commented content out of the store on their own; a
revealed gap gets its one-line amendment in the same reply, and the amendment lands through the
normal repo change flow after approval.
A change the user approves inside a session commits directly to the live store's base branch,
and the next `open` rebases the PR onto it.

Write memory snapshots to `/tmp/charliebot-memory-bak/`, flat with their original filenames. Overwriting an earlier
snapshot is allowed. Keep backups outside `$CHARLIEBOT_HOME/`, including its session directories.

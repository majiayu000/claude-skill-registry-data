---
name: retro
description: >-
  End-of-session retrospective — start from the run's retained Dev flow v2
  evidence where one exists (per-stage rounds against their caps, findings by
  class and provenance, overrides, interventions), fall back to the
  memory-based sweep where none does, then loose ends, follow-ups, next
  actions, improvement opportunities (skills to write, settings/env changes,
  GitHub issues to file), plus status tables with clickable links and status
  emoji for every PR and issue touched or referenced this session.
  Invoke as /retro.
disable-model-invocation: true
allowed-tools: Read, Glob, Grep, Bash(git status:*), Bash(gh pr view:*), Bash(gh pr list:*), Bash(gh issue view:*)
---

# Retro

**Runtime assets travel with the skills.** Every executable this skill names is
vendored by `task sync:skills`, never fetched from a repository-root `scripts/`
path (harmon-devkit#974): a consumer that installed the skill has no such
directory, so a root-relative dependency installs a skill that cannot run. Two
shorthands are used below and resolve the same way in harmon-devkit's source
tree and in a consumer's flattened `.claude/skills/` one:

- `assets/<name>` — this skill's own asset, i.e. `${CLAUDE_SKILL_DIR}/assets/<name>`.
- `<package>/assets/<name>` — a sibling package's asset. **Resolve
  `${CLAUDE_SKILL_DIR}` physically first**, then append:

  ```sh
  skill_dir="$(cd "${CLAUDE_SKILL_DIR}" && pwd -P)"
  support_dir="$skill_dir/../dev-flow-support/assets"
  ```

  The `cd`/`pwd -P` is load-bearing, not ceremony: where the skills directory
  is reached through a symlink — harmon-devkit's own `.agents/skills/<name>`
  entries are symlinks into `ai/skills/<category>/` — a **logical**
  `${CLAUDE_SKILL_DIR}/../` splits by resolver. `ls` follows the link and
  succeeds; Node collapses `..` with `path.resolve()` before touching the
  filesystem and fails with `MODULE_NOT_FOUND`. Resolving physically first
  makes both agree. This is the same rule `dev-flow-support`'s own `SKILL.md`
  states for asset-to-asset calls; see it for the canonical wording.

  The shared dev-flow v2 runtime (`devflow-policy.mjs`,
  `validate-result-schemas.mjs`, `render-dev-flow.{sh,mjs}`,
  `dev-flow-exit.{sh,mjs}`) lives in `dev-flow-support/assets/`.

A missing sibling package is a blocker, not a fallback: vendor the `universal`
category as a unit rather than resolving a runtime path some other way.

**Arguments:** $ARGUMENTS

End-of-session retrospective. Review the whole conversation, not just the
most recent work.

## 1. Start from the run's retained evidence

Dev flow v2 leaves a durable record per run — a run record and one adjudicated
round comment per confidence round on the issue, a stage projection on the PR
(`specs/dev-flow-v2.md` § Evidence; the byte-level grammar is in
`ai/schemas/README.md` "Evidence marker and digest grammar"). Where one exists
for this session's PR, **every measurement in §2 comes from it, not from
recollection.** What a session remembers about its own rounds is exactly the
thing a retrospective must not take on trust: the rounds it spent, what the
findings were about, where the orchestrator overrode a reviewer, and where a
human had to step in are all recorded, and a remembered version of any of them
is a reconstruction after the fact.

**Two different markers, two different jobs.**

- The **PR body's rendered sections** — `<!-- dev-flow:begin:policy-disclosure -->`,
  `deferred-findings`, `adjudication-record`, published by
  `dev-flow-support/assets/render-dev-flow.mjs` — say a v2 record exists and carry the
  **resolved rigor line**, which is where §2's caps come from. They do not
  carry the run id.
- The **run id** lives in the evidence markers themselves,
  `<!-- dev-flow-v2-evidence: {"run_id":…} -->`: on the PR's stage-rollup
  comments, and — authoritatively, because the record is anchored on the
  issue — in its round comments on the linked issue. The older
  `<!-- devflow:<kind> … -->` form remains discoverable for legacy runs. A
  marker counts only as the **first line** of a comment; one quoted inside
  prose (a real risk on a PR that discusses this protocol) is not a run.
  **And only a marker from a trusted actor selects a run.** A marker is text
  anyone who can comment could post, so which run gets reported is a trust
  boundary, not a lookup: the helper gates discovery on the same
  trusted-orchestrator actor ids it passes to the harvester, reports every
  marker it ignored, and refuses a trajectory whose own record names a
  different PR.

Discovery applies strict tier precedence: a trusted marker on the PR itself,
then trusted markers on closing issue references, then trusted markers on
same-repository issues named in the PR body by `Refs`, `Addresses`, or `Part
of`, and finally a `run-<issue>-<slug>` body token only when the PR or issue
`<issue>` carries a trusted marker naming that exact run. More than one run on
the selected tier is indeterminate, and a lower tier never overrides a run
selected above it. Every issue token on a line-anchored reference declaration,
optionally prefixed by a bullet or ordered-list marker, in the PR body
participates in discovery, including same-repository GitHub issue
URLs; a pull URL is disclosed and ignored as a PR hint, and a foreign-repository
URL is disclosed without being queried. References never come from PR comments,
quoted lines, or mid-line prose. Run tokens are read only from those declarations
or a line-anchored `Run:` line, preserving the complete token through whitespace
or its closing backtick, bracket, or comma before exact marker comparison.
At most 10 unique non-closing/token issue hints are read, with a larger set
refused rather than truncated. A hint that names a PR or missing/deleted issue is
disclosed and ignored, while a transient lookup failure is indeterminate. Both
the closing-reference set and these body-derived lookup inputs are mutable
current state that `--as-of` cannot reconstruct.

**Run the projection rather than reading the trajectory by hand.** It resolves
the run id, calls the harvester (`assets/dev-flow-stats.mjs --run <id> --json`,
issue #663) and renders §2's fixed sections:

```sh
<retro-skill-dir>/assets/retro-run-report.mjs --repo <owner/repo> --pr <n>
```

Resolve `<retro-skill-dir>` from `.agents/skills/retro`, then
`.claude/skills/retro`, then `ai/skills/universal/retro` in harmon-devkit
itself. The helper is read-only — it shells out to `gh` reads and to the
harvester (`assets/dev-flow-stats.mjs`, which never writes) — but it is
deliberately **not** in `allowed-tools`, so expect a permission prompt, the
same as the GraphQL query in §4.

**A configured trust root is required.** With neither explicit trust flag,
the helper reads `trusted_orchestrator_actor_ids` from `agent-registry.json`
in `--repo` at its default-branch head through the GitHub Contents API, never
from the caller's working tree. An unreadable or missing remote registry,
invalid JSON, or a missing, empty or malformed
field fails closed with a usage error. The array must contain positive safe JSON
integer actor IDs, without duplicates or finder actor identities. The helper never defaults to the authenticated account:
authority comes from configuration, so a reader cannot authenticate their own
retrospective merely by logging in.

`--trusted-actor-id <id>` (repeatable) and `--trusted-actors-file <path>`
(a JSON `{"trusted_actor_ids": [...]}` document) explicitly override the registry.
When both flags are supplied their IDs are combined, preserving the existing
flag behavior; the registry is not read or merged into that set.

The trusted set, from the registry at `<repo>@<ref> (<blob sha>)` or from explicit
`--trusted-actor-id`/`--trusted-actors-file` flags, is passed to the harvester.
Current-format evidence authenticates against exactly that set. Legacy evidence
is additionally intersected with the registry revision in effect when it was
written. An explicit flag set is trusted as given and can widen what is
authenticated, so pass it only deliberately. Under the default registry trust
set, an orchestrator removed from the allowlist since a run reads as
indeterminate (fail closed). The report's
evidence-integrity section names the actual source and IDs used.

Other useful arguments: `--run <run_id>` when you already know it (a run that
capped before its PR existed has no PR to discover from — its record is on the
issue, and note that an id supplied this way is *unverified*: nothing checks it
against a marker); `--json` for the machine form; and `--stats-script <path>` to point at a
harvester this checkout does not carry at the usual place — the case below,
where the retro skill was vendored without its own `assets/dev-flow-stats.*`
beside it.

Pass `--record-dir <path>` when the run's retained local record is available.
The helper forwards it unchanged, and the harvester reads
`<path>/<run_id>/run.json` plus that run directory's passes and adjudications.
The GitHub marker still authenticates which run and round coordinates may be
read; the local directory supplies their full content. An absent named record
is reported as `record-missing`, while omitting the option leaves the marker as
`evidence-only` rather than inventing the missing content.

Once selected, the local record's rounds are read through the exit engine
itself — the harvester spawns `dev-flow-support/assets/dev-flow-exit.mjs --verification-only
--json` once per confidence stage with local evidence and consumes its
`rounds[]` trajectory field, rather than re-implementing lifecycle/receipt/
adjudication/contiguity validation on its own (harmon-devkit#1001). What stays
harvester-owned is everything about which GitHub markers may be trusted to
report a round at all — trust, registration, sequence, destination, and
cutoff visibility under `--as-of`; the engine has no opinion on any of that.

**`--as-of <iso8601>` reconstructs the run record and its comment evidence at
that instant — and nothing else.** Comments are filtered by the cutoff, and
the harvester replays the record's append-only chain to it. Three other inputs
are read as they stand now and are **not** reconstructed:

- the **linked-issue set** (the PR's closing references plus the same-repository
  non-closing references and run-id issue numbers in its body), which decides
  which issues a fallback search reaches — re-linking an issue or editing the
  body changes a historical read;
- the **PR body** the disclosed caps come from, which is mutable and
  unauthenticated anyway (§2);
- the **default trust set** from the target repository's
  default-branch-head registry, when neither explicit trust flag is supplied.
  A replay with `--as-of` trusts the default allowlist as it is now, while the
  harvester still applies write-time registry revisions to legacy evidence.

The report states these wherever it uses one, so a reader never has to infer
the boundary. This is the honest form of the guarantee rather than a wider one
the mechanism cannot keep: three separate review rounds each found another
current-state input feeding a promise of total immutability, so the promise
was narrowed to what the evidence actually supports instead of being patched a
fourth time.

**Branch on the exit code. Do not read the text and guess.**

| Exit | Meaning | What the retro does |
| --- | --- | --- |
| 0 | a report is on stdout | Paste it as §2, then carry on |
| 1 or 2 | operational or usage error | Fix the invocation, or report that the tool failed. Never silently downgrade to memory |
| 10 · `no-run-record` | it **looked** and found no evidence marker at all | Fall back: skip §2, and **say plainly** that this session has no run record, so the improvements in §5 rest on the conversation rather than on measurements |
| 10 · `run-not-found` | an id supplied with `--run` was not found; **discovery never ran** | Fall back for the measurements, but do **not** say the session has no run record — nothing looked. Say the supplied id was not found, and consider that it may be mistyped or that the record lives on the issue. §5's `run-not-found` provenance wording is the matching phrasing |
| 11 | evidence exists but is **indeterminate** — a broken or forged digest chain; two trusted runs on one PR; a run bound to a different PR; markers that exist but none from a trusted actor; a trusted actor's own marker that does not parse; or a trusted marker naming a run the harvester cannot find (the evidence contract's deleted-entry case) | Not a fallback. Make it the retro's first finding and quote the reason from stderr. **Draft** the follow-up issue — do not create it unless asked, exactly as §5 requires of every other follow-up. Never downgrade any of these to "no run record" |
| 12 | `no-stats-script` — this checkout has no harvester, so whether a run record exists is **unknown** | Fall back for the measurements, but report the gap: say the evidence *could not be read here*, never that there is none, and use §5's exit-12 provenance wording. stderr says whether discovery found a trusted marker (evidence the run is recorded) or only an unverified `--run` argument |
| 13 | `local-unverified` — opt-in schema-validated local record, not authenticated by a trusted GitHub evidence marker | Paste only with **unverified (local record, not authenticated by a trusted GitHub evidence marker)** on the heading and every measured line. Never treat it as authenticated evidence or a clean verified result |
| 14 | Refused local record: unsafe or invalid local input (schema failure, `run_id` mismatch, PR mismatch, path or symlink escape, or not a regular file), or an unsupported platform | Report a **refused local record**, quote the reason, then fall back for measurements. For an unsupported platform, report the platform restriction rather than trying to repair a valid record. Never describe this local refusal as GitHub evidence tampering |

`no-run-record` is the ordinary pre-v2 session and costs the retro only its
evidence section — it is the **only** outcome that licenses the sentence "this
session has no run record", which is why it and `run-not-found` are separate
rows above even though the process exit is the same number. Exit 12 is a fact about the checkout, not about the run:
reporting it as 10 would let a vendoring gap masquerade as work nobody
recorded. Exit 11 for GitHub evidence is a finding in its own right — treating it as "no
evidence" is how tampered evidence would read as an ordinary memory-based
retro. Exit 14 covers an unsafe or invalid local input or an unsupported
platform: report that refusal and fall back, without alleging GitHub tampering.

After **only** exit 10 `no-run-record` or `run-not-found`, if the run id
and its retained directory are known, an explicit local read is permitted:
rerun with `--run <id> --record-dir <parent> --local-unverified`. Local reads
are **Linux-only**: descriptor containment needs a single-step descriptor path.
On an unsupported platform, exit 14 reports
`local descriptor containment cannot be established on this platform`.
This restriction applies even to a valid record; report it rather than trying
to repair that record. This opt-in mode may replace only an ordinary exit-10
outcome. Every ordinary exit 0, 11
or 12 keeps identical stdout, stderr and exit status with the flag enabled;
integrity errors never fall back to local data. The run schema validator must
accept the local `run.json` and its `run_id` must match the requested id;
otherwise no report is rendered. With `--pr`, read-only discovery must find no
trusted marker on the PR or its discovered issues before a local read.
Indeterminate discovery, including untrusted-only markers or malformed
markers treated as corrupted evidence, blocks the local read with exit 11.
That check never selects a run or changes `--run`. A local record whose own PR number differs from `--pr`, or whose normalized PR URL
differs from the requested PR URL fetched by `gh`, is refused with exit 14. A record
naming no PR explicitly says it is not bound to the requested PR.
A missing local record retains exit 10 on the ordinary path. An attempted
local read with `--as-of` is a usage error (exit 2), even if the local record
is missing. A guard read failure uses the existing error exits: operational
GitHub failures exit 1; discovery integrity errors or indeterminate hint
reads exit 11. A malformed trusted marker found by the guard also exits 11.
Exit 13 is distinct from success, and
both Markdown and JSON carry **unverified (local record, not authenticated
by a trusted GitHub evidence marker)** on every measured entry. Missing `adjudications/` means **not
recorded**, never zero adjudication rounds. Local adjudications, findings and
convergence are not authenticated or measured here. Local reads do not support
`--as-of`; they report the current snapshot only.

For §5 provenance after exit 13, say: "Retro of the session on `<date>`;
measurements are unverified (local record, not authenticated by a trusted GitHub evidence marker), read
from `<parent>/<id>/run.json`; adjudication rounds absent from the retained
record are not recorded." Never attribute these measurements to GitHub
evidence or call this a verified retro.

## 2. The run-evidence report

Paste the helper's output verbatim. Its sections are fixed, in this order, so
two retros of two different runs are comparable line for line:

When the run's slate has a `plan.json`, read its validated revision and include
planned versus actual waves and interventions for each lane in the report;
name assignments that moved, serialization or fence decisions that changed,
and the recorded reason rather than reconstructing the original plan from lane
briefs or memory. The plan for a run is the unique validated slate whose
revision history lists that `run_id` in `lanes[]`.

1. `## Run evidence` — run id, issue, PR, who initiated it, outcome, promotion,
   and where the run id was discovered.
2. `### Policy the PR discloses (unverified)` — the resolved rigor line read
   back off the PR body, and the caps every stage section below is measured
   against. It is **not** read from the current `.devflow.toml`: that would
   rescore an old run against a budget it may never have had. But the PR body
   is mutable and sits outside the authenticated evidence chain — a later edit
   or republication changes it, and `--as-of` does not reconstruct it — so the
   caps are a **claim to check against the rounds**, never a measurement, and
   the report says so on every line that shows one. Where the PR published no
   disclosure (or two) the caps are reported unknown rather than guessed.
3. `### Stage <name>`, one per stage the run entered, chronologically by first
   entry — rounds spent against the cap, findings and passes, rounds with no
   adjudication record, every entry and exit (a stage re-entered by a
   remediation loop keeps **one** section holding all of its rounds), the
   interventions that landed while that stage was open, and — for a stage that
   found something — its findings by class and provenance plus its
   adjudication overrides. The trajectory supplies verified class/provenance
   counts keyed by stage; unavailable rounds are named, and unverified findings
   are excluded from those counts. Older harvesters
   expose only the run-wide aggregate, attributed to a stage only when that
   stage is the sole one with findings. Adjudication overrides are not exposed
   at all (harmon-devkit#753). Each affected stage section says which case it is in rather than leaving the line
   out; treat a "not derivable" line as a real gap in the retro, not as
   "nothing to report".
4. `### Findings by class and provenance` — `class` from the reviewer's own
   finding, `provenance` its `original` / `round:N` field.
5. `### Policy overrides the PR discloses (unverified)` — the cap, waiver,
   tier, and strategy disclosures the PR published, under the same caveat as
   the policy line. **Adjudication overrides — a finding whose adjudicated
   priority differs from the reviewer's — are not in it**: the trajectory
   reduces each round's adjudication to a boolean (harmon-devkit#753), so an
   empty section means "nothing was disclosed", never "nothing was
   overridden". Say which you mean in the retro.
6. `### Interventions` — every human touchpoint, with the stage it interrupted.
7. `### Deferred findings settled` — each settled deferral with the finder slug
   recovered from its finding id (`<stage>-r<round>-<finder>-<n>`, the slugs
   `agent-registry.json` `finders[]` declares).
8. `### Evidence integrity` — trusted-but-unlisted and forged-author comments,
   the trust root discovery actually used, and every evidence marker it
   ignored because the author is not in that set. A nonzero ignored count is
   either a misconfigured trust root, a trust root that moved since the run,
   or somebody trying to redirect the report; all three are worth a line in
   the retro. Read the selected source and the evidence-format-specific trust
   rule stated in §1 when interpreting these counts.
9. `### Not measurable from this run's evidence` — the measurements this retro
   is expected to make that today's evidence surface cannot supply, each naming
   the issue that would close it. Carry these into §5 as-is rather than
   silently omitting them; an absent section reads as "nothing to report".

**How to read it.** The numbers are the input to §5, and four of them carry
most of the signal:

- **Rounds against the cap.** A stage that spent its cap converged late or not
  at all. A stage that exited on round 1 spent nothing it did not need to.
  The cap is the PR's own unverified disclosure, so a count that looks
  impossible against it (four rounds under a cap of three) is a finding about
  the disclosure, not arithmetic to explain away.
- **The `round:N` share of provenance.** A stage whose later findings are
  mostly about its own earlier fixes is feeding on itself — the exact failure
  AGENTS.md's round-2 scaffolding checkpoint exists to catch. If the trajectory
  shows it, the improvement cites that stage, its convergence policy or skill,
  and this run id.
- **Interventions.** Each one is a place the run could not proceed unattended,
  and the closed-cohort success metric counts them. Ask what would have had to
  be true for each not to happen.
- **Integrity.** A forged-author or orphan comment is a finding about the
  evidence protocol, not a footnote.

Where §1 fell back, skip this section entirely and say so — do not
reconstruct these headings from memory. A section that looks measured but was
recalled is worse than an absent one.

## 3. Gather PRs and issues

Enumerate every PR and issue that was worked on **or even referenced** during
the session. If the conversation has been compacted, the earlier context is
summarized and the enumeration is best-effort: say so explicitly, cross-check
`gh pr list --author @me` and the session's branches for work the summary may
have dropped, and note that the tables may be incomplete. Do not trust
remembered status — re-verify each one live:

- `gh pr view <n> --json state,isDraft,mergedAt,reviewDecision,statusCheckRollup,url,title`
- `gh issue view <n> --json state,stateReason,assignees,labels,url,title,comments`
  — one response, so the marker check below reads labels and the claim
  comments (including any `dispatched to` line) from a single snapshot; a
  second call could pair pre-release markers with a post-release comment

**Read the claim off the markers, not off the issue.** A live claim is an
`claim:*` (or legacy `agent:*`) label, a card at `In Progress`, or the
**latest trusted `Claiming —` comment after the latest trusted `Claim released —` comment**.
A newer trusted claim supersedes an earlier refresh record without releasing
the active claim; an older comment alone proves nothing about now.

Neither `state` nor `assignees` may gate that check. Both exclude real stale
claims: a closing PR auto-closes the issue while the label and card stay set,
and a `/wrap` that removed the assignee before failing on the label or status
leaves a claim with nobody assigned. Gating on either is how the claim this
step exists to surface becomes invisible. Do not require the label
specifically, either — `/claim` treats a missing `claim:*`/`agent:*` family as benign
and claims anyway, so demanding it would miss every claim in an older repo or
one with `project_management: none`, which are exactly the repos where the
label cannot exist. Report it as "open — claimed,
in progress" — and when the latest claim record carries a `dispatched to`
line whose value is not `none`, say so ("claimed, dispatched to …" with the
recorded delegate). That line is dispatch-time history, not live state: it
says the orchestrator handed the issue to a background subagent when the
record was written, and it is the only place the tracker records that. Whether
the delegate is still active is read from the work in flight, exactly as for
any other claim. Then check it is still true: a claim with no open PR and no
work in flight is a loose end for §4, not a status. `/wrap` offers the commands to
hand it back.

**Discovery trust is deliberately read-only and broader than cleanup trust.**
For this stale sweep, accept a claim author whose comment-time association is
`OWNER`, `MEMBER`, or `COLLABORATOR` even when that author is no longer a
current assignee; otherwise the partial-cleanup shape above disappears with
its assignment. This rule may surface a candidate but never authorizes a
write. `/wrap` and `release-claim.sh` must re-read current state and apply the
stricter cleanup trust gate before removing anything.

**A claim awaiting release is not a stale claim.** Two live claims read
identically off the markers and mean opposite things — distinguish them
rather than reporting both as loose ends:

- **Pending release** — *this session* claimed it, and its PR is open, in
  review, or awaiting merge. The release is owed to the close event
  (`claim-release.yml` where installed) or to `/wrap`, not overdue. Report
  it as part of the work's normal state, not as a loose end.
- **Stale** — the claim outlived its work: **nothing is in flight** (no open
  PR, no fresh activity), whichever session made it, or the issue is already
  **closed** with the label or assignee still standing. A session-name
  mismatch alone proves nothing — a claim from a different session with work
  in flight is *another session's active claim*: report it, never treat it
  as cleanup material. That last case means the release
  workflow failed or is not installed — say which, because "the automation
  missed one" and "there is no automation" call for different fixes
  (`track-work/references/claim-lifecycle.md`). One shape is *neither*: a
  closed issue whose card still sits at `In Progress` **under a trusted
  `Claim released —` comment** is a successful release awaiting board
  cleanup — the workflow has no Projects permission by design — so report
  it as a pending `/wrap` chore, not a workflow failure. These are §4
  loose ends.
- **Freshly filed follow-up** — an issue an agent filed during this session as
  follow-up work is expected to be open, unassigned, and without a claim.
  Report it under "filed," not as a loose end. It becomes a loose end only if
  this session said it would work the follow-up and did not.

Keep each reference's repository identity: a bare `#123` from another repo
must be verified with `--repo owner/repo` (or by its full URL), never against
the current repo's numbering.

## 4. Loose ends and next actions

- Uncommitted or unpushed work: `git status -sb`, and
  `git log @{u}..HEAD --oneline` (guard for branches with no upstream).
- Unresolved review threads on open PRs — `gh pr view` cannot report thread
  resolution, so use a read-only GraphQL query (this one is not pre-approved
  and will prompt):

  ```sh
  gh api graphql -f query='query($o:String!,$r:String!,$n:Int!,$c:String){
    repository(owner:$o,name:$r){pullRequest(number:$n){
      reviewThreads(first:100,after:$c){
        pageInfo{hasNextPage endCursor}
        nodes{isResolved path}}}}}' \
    -F o=<owner> -F r=<repo> -F n=<pr>
  ```

  If `hasNextPage` is true, repeat with `-F c=<endCursor>` until every page
  is seen — a thread past the first 100 can still block the PR.

- Deferred findings the PR body still leaves unchecked — the checkbox is the
  resolution state, so an unticked `- [ ]` under `## Deferred findings` is open
  work whatever the conversation remembers.
- TODOs introduced during the session.
- Anything promised in conversation but not done.

List each as a concrete next action.

## 5. Improvement opportunities

**Every item names the thing it would change.** One of:

- a **stage** — `challenge`, `review`, `integration`, …
- a **skill** — `/implement`, `/integrate`, `/retro`, …
- a **config key** — `.devflow.toml`'s `[rounds].challenge`, `default_rigor`,
  a `[convergence]` predicate, …
- a **registry or schema contract** — `agent-registry.json`'s `finders[]`, a
  `result.*.schema.json` field, …

An item that names none of those is an observation, not an improvement: find
its target or drop it. Where §2 ran, each item cites the measurement it came
from ("challenge spent 3 of 3 rounds with 2 of 4 findings at `round:1`
provenance") rather than an impression.

Within that shape, look for:

- Skills worth writing or updating based on friction hit this session.
- Settings, hooks, or environment improvements.
- Every entry from §2's `### Not measurable from this run's evidence` — each
  already names its target and its follow-up issue.
- GitHub issues worth filing — draft a `(<free-form scope>): <imperative
  outcome>` title and one-line body for each, following `track-work`'s complete
  title contract, but do **not** create them unless asked.

**A follow-up filed from a retro carries the run's provenance.** When asked to
file, go through the `track-work` skill and give the issue a `## Provenance`
line naming the run, so a later reader can replay the trajectory the finding
came from rather than take the retro's word for it:

```markdown
## Provenance

Retro of Dev flow v2 run `<run_id>` (issue #<n>, PR #<n>), `<stage>` stage.
```

Where §1 fell back, provenance says which fallback it was — the two are not
interchangeable, and only one of them may claim there was no run record:

- **Exit 10, `no-run-record`** — "Retro of the session on `<date>`; the PR and
  its linked issues carried no Dev flow v2 evidence marker." That is the honest
  "no measurement behind this", and it is worth more than a run id that does
  not exist. It is the **only** wording that asserts a run record was absent,
  because it is the only case where the tool actually looked for one.
- **Exit 10, `run-not-found`** — "Retro of the session on `<date>`; the run id
  `<id>` supplied to the helper was not found, and no marker discovery was
  run." Do not write "there was no run record": a `--run` invocation skips
  discovery entirely, so a mistyped id, or the documented pre-PR case where
  the record lives on the issue, would otherwise be tracked forever as an
  absence nobody established.
An **exit 11** integrity problem is worth a follow-up more than most things a
retro turns up — but "worth filing" is not "file it": §5's rule that
follow-ups are drafted and not created unless asked has no exception here, and
an unrequested write is exactly what a session asked only for a retrospective
did not consent to. Draft it with the run id, the stderr reason, and the head
it was observed on, and say plainly that it is waiting on a go-ahead.

- **Exit 12** — "Retro of the session on `<date>`; a run record may exist but
  this checkout has no `assets/dev-flow-stats.*` beside the report generator
  to read it, so the run was
  not measured." Never write "there was no run record" here: §1 exits 12
  precisely because that is unknown, and a tracked follow-up carrying the
  claim would make the unknown look settled.

## 6. Status tables

Emit exactly these two tables. Re-verified status only; short human status
text plus one emoji.

```markdown
## Pull requests

| PR | Status | |
| --- | --- | --- |
| [harmon-devkit#142 — feat: …](https://github.com/evanharmon1/harmon-devkit/pull/142) | merged | ✅ |
| [harmon-devkit#145 — fix: …](https://github.com/evanharmon1/harmon-devkit/pull/145) | open — checks failing | 🔴 |

## Issues

| Issue | Status | |
| --- | --- | --- |
| [harmon-devkit#138 — Create commands / skills…](https://github.com/evanharmon1/harmon-devkit/issues/138) | open — claimed, in progress | 🙋 |
```

Emoji legend (use these consistently):

- PRs: ✅ merged · 🟢 open, checks green · 🟡 open, review pending ·
  🔴 open, checks failing · ⚪ draft · 🗑️ closed unmerged
- Issues: 🟢 open · 🙋 open, assigned to me · ✅ closed completed ·
  ⚪ closed not planned

## 7. Wrap

Suggest `/wrap` as the final step of the session.

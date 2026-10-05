---
name: forge
description: |
  Conditional discipline for projects hosted on a git forge (GitHub,
  GitLab, Forgejo, …): branch↔PR mapping, self-contained PR prose,
  review-on-forge, merge consent, and the forge audit.
  Trigger when:
  - Opening, updating, reviewing, or merging a pull/merge request.
  - A campaign's integration branch is ready to surface on a forge.
  - Auditing forge-side presence at merge-consent or campaign CLOSE.
  - Prompt contains: /forge, pull request, PR body, merge request,
    forge discipline, PR review, stacked PR.
---

# Forge Discipline

**Applicability is conditional.** Some projects have no forge — a bare
remote, a patch workflow, or no remote at all — and nothing here applies
to them; absence of a forge is never a violation. **When the project has
a forge, this discipline applies in full.** The test is mechanical: does
the origin remote resolve to a forge the project accepts contributions
through?

## Philosophy: the forge is the public half of the record

The flight recorder (`.ledger/`) is the *internal* durable record; the
forge is the *external* one — the only record most future readers will
ever see. The two have different audiences and MUST NOT leak into each
other: the recorder may reference forge artifacts (they are public,
permanent URLs); forge prose MUST NEVER reference process-internal
state. A PR body that cites `.scratch/`, `.ledger/`, a session link, or
a working note is broken for every reader outside the process that
wrote it — and those are all of its readers.

## 0. Tooling: MCP for forge operations, git for merges

Forge **operations** — opening/updating PRs, posting comments and
reviews, reading state — prefer the forge's **MCP server** where the
session has one connected: structured, typed calls over stringly CLI
output. The CLI (`gh`, `glab`, …) is the fallback, and plain git+HTTPS
the primitive beneath both (degrade-to-the-primitive applies: never
depend on the MCP being present). The one hard exception runs the other
way: **merges are always the git CLI** (§4, MERGE_IN_GIT) — no MCP or
API merge endpoint, ever.

## 1. Branch ↔ PR mapping

Two PR tiers, one campaign:

- **Per-node PRs.** Each finished node branch surfaces as a PR targeting
  the campaign's shared integration branch — that PR is the node's
  review record (findings, triage, the merge-consent trace). The merge
  itself still happens in git (§4); pushing the merged shared branch is
  what closes the PR.
- **One tracking PR per campaign.** The `campaign/<TOPIC>` integration
  branch surfaces as a single PR against the default branch; independent
  workstreams get independent branches and PRs, never one omnibus. Its
  body is the campaign checklist (§2).
- **The bootstrap order is forced by the forge — follow it, never fight
  it.** A PR cannot exist until its branch differs from its base, so:
  1. At campaign setup, create the shared integration branch from the
     baseline and PUSH it (covered by the campaign's recorded push
     authorization — preflight it with the rest). Open NO PR yet.
  2. When the FIRST node finishes, push its node branch and open the
     first node PR, targeting the shared branch.
  3. After that node's consented merge lands on the shared branch and is
     pushed, the shared branch has content: NOW open the tracking PR
     (draft) with its checklist body, the first item already checked.
  4. Every later node repeats the rhythm of (2)–(3): node PR → consented
     merge → its checklist item checked.
  Opening the tracking PR at campaign start — before anything exists to
  merge — is the recurring field failure this sequence exists to kill.
- **Stacked PRs** are permitted for dependent work: base each PR on its
  prerequisite's branch. Know the forge's mechanics: when a base branch
  merges and is deleted, the dependent PR retargets (or auto-closes as
  "closed", not "merged") — when the forge misclassifies, annotate the
  PR with the merge commit so the record reads correctly.
- Merged branches are deleted; the PR is the durable pointer.

## 2. PR prose — self-contained, or broken

- **The audience model, stated positively:** the forge reader is a
  potential reviewer of the CODE, with zero knowledge of — and zero
  interest in — how the work was produced. Exactly two questions
  matter: *what is this work?* and *how do I review it?* Every sentence
  must serve one of the two, and the test is applied sentence by
  sentence, not file by file.
- What serves: a summary; what changed and why in terms of the
  repository's own behavior and goals; DESIGN decisions with their
  grounds (why this approach — never process decisions about who
  approved what); what is deliberately out of scope; honest
  verification status as facts about the repository (what was run, the
  actual results, what wasn't run); known risks and tradeoffs.
- **The production process is never content — relevance, not secrecy.**
  Councils, seats, reviewers-as-cast, campaigns, nodes, layers,
  reconcile rounds, dispatch mechanics: none of it helps a reader
  review the change, so none of it appears — token-free *narrative*
  about the process fails the two-question test just as hard as a
  leaked ID. Campaign-scale context is carried by a plain link to the
  meta tracking issue (§6), never by narrative.
- **Formatting is mechanical fact, not taste:** GitHub renders single
  newlines in PR/issue bodies as hard line breaks, so manually wrapped
  prose renders as a staccato mess. Forge prose is SOFT-WRAPPED — one
  paragraph is one logical line, blank lines separate paragraphs, and
  visual structure comes from markdown (headings, lists, fences), never
  from manual breaks.
- **Zero process-internal references**: no `.scratch/`, no `.ledger/`,
  no sketch or session links, no "as discussed" — and no campaign-
  internal identifiers (node or finding tokens): to every reader outside
  the process they are dangling labels. Where context is load-bearing,
  use **permalinks pinned to a commit SHA** — branch-relative links rot
  when branches are deleted.
- The check is mechanical, not a memory: draft forge prose (PR bodies,
  issue bodies, review summaries) in a scratch file and run
  `gates/check_forge_prose.sh --files <draft>` over it before posting —
  internal IDs, the process-vocabulary scan (advisory-with-override:
  rewrite the sentence in substance terms, or narrow `FORGE_VOCAB_PAT`
  in `.ledger/config.sh` for a genuine per-project collision), and the
  hard-wrap lint, in one pass.
- **The tracking PR's body is a checklist.** After its summary prose,
  one item per node PR, in schedule order, checked as each merges:
  `- [x] #<node-PR-number> — <what it landed, in repository terms>`.
  On GitHub use the bare `#N` reference — the forge renders the PR's
  live title and state natively; on other forges use their native
  reference syntax, a plain link as the primitive. Item text obeys the
  same self-containment rule as everything else: describe the landing
  in repository terms, never by campaign-internal node tokens.
- Verification claims in PR prose follow the same honesty rules as
  commit messages: state what evaluators ran and their actual results;
  never imply coverage that does not exist.

## 3. Review on the forge

Decorrelated review findings and their triage belong ON the PR, as
comments — the forge is where the review record survives:

- When adversarial or council review produces findings, post them **as
  substance, in impersonal voice** — what was found in the code and its
  disposition: confirmed-and-fixed (with the commit), refuted (with
  grounds), deferred (with its follow-up home) — as PR comments.
  "Review found X; fixed in `<sha>`" — never a cast of process actors;
  the record is the finding, not the machinery that produced it.
- The triage comment is part of the merge record: a PR that merged
  after review with no visible trace of that review under-documents
  the merge.

## 4. Merge consent

- A PR merges only on the head's say-so, carried through the
  lead-maintainer seat's affirmative merge-consent where the council is
  seated ([campaign §RECONCILE](../campaign/SKILL.md)). Green checks
  and approving reviews are necessary, never sufficient.
- **Merge in git; the forge observes.** Merges are performed with the
  git CLI — locally, with the strategy the history actually calls for:
  fast-forward when clean, an octopus when many nodes land together, a
  merge commit where the narrative warrants one — then pushed; the
  forge detects the merge and closes the PR itself. The forge's merge
  API/button is NEVER the default: it constrains strategy to its own
  shapes (squash/rebase/single-merge), manufactures commits outside the
  commit gate's hygiene, and adds nothing the CLI lacks. After a CLI
  merge, verify the PR state and annotate if the forge misclassified it
  (closed-not-merged).
- Agents never push to protected/default branches without the head's
  explicit instruction (rules.md §3 applies unchanged on forges).
- **Preflight the authorized landing.** The final head-authorized push of
  an integration branch onto a long-lived default branch is a foreseeable
  campaign step: ensure at campaign setup that the permission environment
  allows it. If a classifier blocks it anyway, surface the block to the
  head as an environment gap — the merge is never rerouted through the
  forge's merge API to satisfy a classifier (MERGE_IN_GIT holds).

## 5. The forge audit

A checklist, not a ceremony — owned by the **composer**, run at two
points: alongside each merge-consent, and over the campaign's whole
forge surface at council CLOSE. The forge is the campaign's outward
communication, and communication is conducting: the composer authors
the forge surface, so the composer answers for it. The
lead-maintainer's gate is the CODE and its maintenance burden — his
attention stays on the diff, and routing this audit to him dilutes
the one review only he can give. The composer MAY delegate the
reading to a dedicated read-only reviewer when the surface is large;
the verdict and the fixes remain the composer's.

- [ ] PR prose still accurate against the *final* state of the branch
      (late commits silently invalidate early summaries).
- [ ] Self-containment holds: zero process-internal references
      anywhere in bodies or comments; permalinks pinned to SHAs.
- [ ] The two-question test holds sentence by sentence: everything
      serves "what is this work" or "how do I review it" — no
      production-process narrative, however token-free.
- [ ] `check_forge_prose.sh` passes over every body and comment
      drafted this round (IDs, vocabulary, hard wraps).
- [ ] The review record is present: findings + triage visible on the
      PR for every review that gated the merge.
- [ ] Forge state matches reality: merged PRs show merged (or carry
      the correcting annotation); stale branches deleted; stacked PRs
      correctly retargeted.
- [ ] The PR set partitions the work meaningfully — a reader can
      navigate the campaign from the forge alone.
- [ ] The tracking-issue record is whole (§6): the meta issue exists,
      every out-of-scope finding has its own linked issue, and every
      issue body reads self-contained.
- [ ] Issue tagging holds (§7): labels follow the project's established
      scheme (or the minimal logical one where none exists), and every
      security-critical / correctness-critical issue carries its
      criticality tag.

## 6. Campaign tracking issues

Out-of-scope findings are work the campaign discovered but will not do —
and undocumented, they evaporate with the campaign's scratch. The forge
is their durable home:

- **One meta tracking issue per campaign**, opened at campaign kickoff
  alongside the tracking PR. It is the campaign's out-of-scope index —
  a reader finds every deferred thread from this one issue.
- **One issue per out-of-scope finding**, opened when the finding is
  classified out of scope (at a reconcile boundary or at CLOSE), written
  self-contained per §2 — the finding's substance in repository terms,
  never its campaign-internal ID.
- **Link them**: sub-issues of the meta issue where the forge supports
  them (GitHub), plain cross-links otherwise. An unlinked issue is
  filed, not indexed.
- At CLOSE, every `ACCEPTED_RISK` disposition names its issue — the
  audit (§5) checks the record is whole. Acceptance without an issue is
  a silent drop wearing a disposition.

## 7. Issue tagging

Labels are navigation for a future triager, not decoration — where the
forge supports them, every issue an agent opens is tagged, and the
scheme is discovered before it is invented:

- **The project's convention wins.** Before opening the first issue,
  read the project's existing label set and how recent issues actually
  use it (list the labels; sample a few triaged issues). An established
  scheme is followed exactly — inventing a parallel taxonomy alongside a
  live one is worse than no tags at all.
- **No convention → a minimal logical scheme.** Where the project has no
  established usage, apply reasonable, legible tags and stay minimal:
  the issue's type (bug / enhancement / documentation), its criticality
  where it has one, and the component only when the project's structure
  makes it obvious. A tag whose meaning a stranger cannot guess from its
  name does not ship.
- **Criticality tags are MANDATORY where they apply.** An issue tracking
  a security-critical or correctness-critical finding carries that tag
  (`security-critical` / `correctness-critical`, or the project's
  established equivalents) whenever it is opened — including every
  out-of-scope finding deferred to an issue under §6. An untagged
  critical issue is a mis-filed risk: it will be triaged as routine by
  whoever reads the tracker next.
- **No label support → degrade to the primitive.** Where the forge lacks
  labels, carry the criticality in the issue title prefix (e.g.
  `[security-critical] …`) so the signal survives the missing feature.

## Prime Directives

1. **CONDITIONAL_APPLICABILITY:** No forge, no obligation. A forge,
   full obligation.
2. **SELF_CONTAINED_PROSE:** Nothing process-internal ever reaches the
   forge. Permalinks over lore; SHAs over branch links.
3. **REVIEW_ON_RECORD:** Reviews that gated a merge are visible on the
   PR that merged.
4. **CONSENT_TO_MERGE:** Merge is a sovereignty act — the head's (via
   the lead-maintainer seat where seated), never an agent's default.
5. **MERGE_IN_GIT:** Merges happen in the git CLI, then push; the forge
   observes and records — it does not perform. The merge API is not an
   instrument.
6. **TRACKED_OUT_OF_SCOPE:** Every out-of-scope finding gets its own
   self-contained issue, linked from the campaign's meta tracking
   issue. Deferral is a routing decision with a durable address, never
   a silent drop.

---
name: rseng-version-control-review
description: >-
  Covers using version control effectively for research software and the
  PR-time review process: choosing a VCS, branching and commit practice,
  authorship and signatures in commit metadata (author/committer identity,
  Co-authored-by trailers, signed commits and tags, .mailmap), collaboration
  on GitHub/GitLab, and constructive checklist-driven pull-request reviews.
  Use when the user asks how to set up git, design a branching strategy, write
  commit messages, record who authored or co-authored a change, sign commits
  or tags, handle large binary files, open or review a pull/merge request, or
  wire linters and CI into review. (Audits of existing code and milestone
  reviews: rseng-code-review; pre-reviewing your own draft:
  rseng-pair-programming.)
license: CC-BY-4.0
metadata:
  version: 0.3.0
---

# Version control and code review for research software

Use this skill when helping someone put research code under version control,
shape a collaboration workflow, or review code (their own or a teammate's).
The aim is software whose history is traceable, whose changes are reviewed
before they land, and whose results others can reproduce. Version control and review are
two halves of one loop: commits and branches create reviewable units, and
review is what keeps what lands on the main branch trustworthy.

## Choose a version control system

Default to git for almost every research project unless a concrete
constraint says otherwise:

- Git is the community's standard and the right choice for research
  projects: collaboration, review and archiving tooling all assume it
  (the strongest-current-tool rule applies to version control too).
- Large binary files (datasets, models, images) do not belong in plain
  git history: use a data versioning layer (DVC, git-annex, DataLad -
  rseng-data-management) or git-lfs for media-style assets.
- A team new to version control still starts with git - budget training
  time (rseng-trainer) rather than reaching for a gentler-seeming legacy
  system; inherited repositories in older systems (SVN, Mercurial) are
  a migration task, not a reason to stay.

## Set up the workflow, not just the repo

Choosing a tool is the easy part; the value comes from an agreed workflow:

- Define a branching strategy up front. Keep the main branch releasable;
  do work on short-lived feature branches and merge back via review. Adopt
  a heavier model such as Git Flow only when project size warrants it - do
  not impose ceremony a small team will not follow.
- Set commit conventions. Write small, focused commits with clear messages
  that say why a change was made, not just what. One logical change per
  commit keeps history bisectable and reviews small.
- Integrate with the development environment. Wire the VCS into the IDE or
  editor (VS Code, RStudio, PyCharm, Eclipse) so committing and diffing are
  part of normal work, and connect continuous integration so tests run on
  every push.
- Make reproducibility explicit. Tag the exact versions used in
  publications, and keep configuration files and dependency
  specifications in version control alongside the code.
- Collaborate through a platform. Use GitHub or GitLab for sharing, issues,
  and pull/merge requests; make review a standing part of merging.
- Maintain the repository. Back it up, prune stale branches periodically,
  and review access permissions.

Commit-message checklist: imperative summary line under ~50 characters; a
body that explains motivation and any trade-offs; reference the issue or
ticket it addresses; avoid dumping unrelated changes into one commit.

## Authorship and signatures live in commit metadata

Who wrote a change, who committed it, and whether it is verified are
facts git records in dedicated, machine-readable places. Keep them
there - not in file headers, not in commit-message prose:

- Identity is configuration. Set `user.name` and `user.email` correctly
  per project (institutional vs personal identity) BEFORE the first
  commit; forges, citation harvesters and contributor counts all read
  these fields. Use `git commit --author` when committing a change
  someone else wrote - git separates author (wrote it) from committer
  (recorded it) for exactly this case.
- Multiple authors are trailers. Record co-authors with
  `Co-authored-by: Name <email>` trailers - the standard,
  forge-recognized mechanism - rather than naming people in the message
  body or a file header.
- Signatures are commit signatures. Verification means signed commits
  and signed tags (`commit.gpgsign`, `gpg.format ssh` for SSH signing
  keys, `git tag -s` for releases), checked with
  `git log --show-signature` or the `%G?` format field. Sign at least
  the release tags that publications cite - a signed tag anchors
  provenance (rseng-provenance) far better than any statement in a
  README.
- Fix identities with .mailmap. When names or emails vary across
  history, normalize them with a `.mailmap` file - the metadata-native
  correction - and NEVER rewrite published history to edit authors or
  signatures; corrections go forward.
- Do not duplicate metadata into files. "Author: X, modified by Y on
  <date>" headers in source files rot immediately and contradict the
  history; `git log` and `git blame` are the record (license/SPDX
  headers are a different thing and are fine). Likewise keep commit
  messages about the WHY of the change - the who/when/verified facts
  already live in the metadata fields.
- Keep it truthful. The author field, trailers and signatures must
  reflect who actually did the work - including agent contributions
  where project policy records them; misrepresenting authorship in
  metadata is a concealment request (rseng-honesty), and accurate
  metadata is what contributor credit is harvested from
  (rseng-citation-metadata).

## Run code review as a first-class practice

(Scope note: this skill covers PR-time review process and rules;
retrospective codebase audits and milestone project reviews are
rseng-code-review, and diff-time pre-review craft is
rseng-pair-programming.)

Code review is systematic examination of code - a teammate's, or your own
after time away - to find bugs, raise quality, and enforce shared standards. It pays off: rigorous inspection can remove 60-90% of
errors before the first test run, and fixing a defect early costs 10-100x
less than fixing it later. Beyond defect-catching, review spreads knowledge
across the team, improves reusability and reproducibility, and helps onboard
new members.

Structure every review through a pull/merge request so discussion, diffs,
and suggestions stay attached to the change.

### What to look for

Focus the review on substance:

- Correctness - does the code do what it is supposed to, including edge
  cases?
- Style and consistency - are naming, formatting, and structure consistent
  with the project's agreed conventions?
- Testing - are there tests, and do they cover expected and edge-case
  behaviour?
- Documentation - are functions, classes, and scripts clearly documented?
- Modularity - is the code split into reusable, testable components?
- Performance - is it efficient enough for the task (without premature
  optimisation)?

### What not to do

Reviews go wrong by overstepping as much as by missing bugs. Avoid these:

- Bikeshedding personal style. Do not argue single vs double quotes or
  similar when the team has no agreed standard - let linters and formatters
  settle it.
- Demanding rewrites. Do not push to rewrite large sections without a clear
  reason such as a real bug or design flaw. Improve, do not take over.
- Blaming the author. Critique the code, never the coder; keep feedback
  constructive and kind.
- Requiring perfection before merge. Functional, tested, clear code can
  merge; minor polish can follow.
- Mislabelling severity. Mark minor or subjective points as non-blocking;
  do not hold up progress for optional tweaks.
- Expecting mastery of everything. Researchers who code come from varied
  backgrounds - do not expect deep software-engineering knowledge from
  every domain expert.

### Make review efficient

- Keep changes small. Small pull requests get faster, deeper review than
  large ones - another reason for focused commits and short-lived branches.
- Automate the mechanical checks. Run linters and formatters (flake8,
  eslint, Pylint) and a CI pipeline before human review, so reviewers spend
  attention on logic and design rather than whitespace.
- Keep feedback constructive. Ask questions rather than issue verdicts;
  reviewers learn as much as authors.
- Combine human and automated review. Automated tools catch style and known
  mistake patterns; a human is still required for correctness, design, and
  intent - neither replaces the other.
- For code underlying a paper, consider a CODECHECK-style independent
  reproduction of the results as a heavier form of review.

Reviewer checklist to paste into a PR: correctness and edge cases checked;
tests present and meaningful; documentation adequate; naming and structure
consistent; no obvious performance traps; linter and CI green; comments
labelled blocking vs non-blocking.

## How version control and review reinforce each other

- Branch per change so each unit of work is independently reviewable.
- Require review (a PR/MR approval) before merging into the main branch.
- Let CI gate the merge: tests and linters must pass before a human signs
  off, so review time goes to judgement, not mechanics.
- Tag reviewed, released states so the reproducible version is
  unambiguous.

## Repository hygiene: no generated or binary artifacts

Keep compiled and generated files out of version control: build
outputs, packaged artifacts, rendered documents, caches and editor
droppings. They bloat history permanently, make diffs meaningless
and drift out of sync with their sources - a repository free of
binary artifacts is an explicit quality indicator. Add ignore rules
before the first build runs; large or binary DATA has its own
disciplined path (data versioning tools rather than git), and
deliberately committed result records (golden files, executed
notebooks) are fine when the policy says so explicitly - the rule is
"nothing generated without a stated reason", not zealotry.

## Working with this skill

The generated references.md beside this file lists the source
material and pointers:

- references.md - verified Learn more pointers


Learn more (verified):
  - https://git-scm.com/book/en/v2 - the Pro Git book
  - https://swcarpentry.github.io/git-novice/ - Software Carpentry
    Git lesson
  - https://www.conventionalcommits.org/en/v1.0.0/ - Conventional
    Commits specification
  - https://google.github.io/eng-practices/review/ - Google code
    review guidelines


<!-- related-skills:begin -->

## Related skills

Check whether any of these applies before moving on:

- rseng-ci-cd - CI gating merges before human review
- rseng-citation-metadata - commit metadata feeds contributor credit
- rseng-contributor-onboarding - review as an onboarding channel
- rseng-data-management - DVC/git-annex for large data files
- rseng-notebooks - jupytext twins make notebook diffs reviewable
- rseng-publishing-releasing - tags marking published versions
- rseng-software-peer-review - CODECHECK-style heavier review of paper code

<!-- related-skills:end -->

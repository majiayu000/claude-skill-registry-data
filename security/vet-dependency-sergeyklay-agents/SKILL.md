---
name: vet-dependency
description: "Measure a candidate library's real maintenance state and its behavior against the protocol, schema, or API version the project has already pinned, before taking it as a dependency. Covers any ecosystem (Go, npm, PyPI, Cargo, Maven) and any forge (GitHub, GitLab, Gitea). Use when deciding whether to adopt, replace, or drop a library, when asked which of two or more packages that do the same job to use ('should we use X or Y'), when an architecture decision turns on whether a package is still maintained, or when a package looks healthy by stars and release count and the real question is whether it can reach the project's pin. Answers with a measured verdict on named candidates, from the unmerged pull request queue and a runtime probe against the published artifact rather than the README. Do NOT use for a vulnerability in a dependency already adopted (scan-security), a weighted-criteria comparison document for publication (compare-it), or a library question with no adoption decision attached (research-it)."
metadata:
  author: Serghei Iakovlev
  version: "2.0"
  category: research
---

# Vetting a candidate dependency

A package's landing page reports the wrong variables. Stars measure attention at some point in the past, release count measures how often a version was published, and the repository's last-push timestamp moves whenever anything touches it. None of the three answers the question that decides adoption: can this package reach the version this project has already committed to, and does it behave correctly when it gets there.

The two facts that settle it are both invisible from the README. The first is the queue of pull requests nobody has merged, which measures whether the package can still move. The second is what the library does at runtime with the exact input class this project will feed it, which measures whether moving would help.

The subject is a package that is not yet a dependency, characterized empirically before it becomes one rather than described from its documentation. This skill sits beneath `research-it`, which owns source priority, triangulation, and the discipline around absence claims. It owns only how a candidate's health and fitness are measured, and what verdict that measurement supports.

Nothing here is language-specific. Three operations differ per ecosystem (resolving a package to its repository, obtaining the published artifact, running an isolated probe) and are catalogued in [references/ecosystems.md](references/ecosystems.md); the forge API calls differ per host and are catalogued in [references/forges.md](references/forges.md). Read the relevant rows of each before step 0. Everything else in this file applies unchanged.

## When this fires

- An architecture decision turns on adopting, replacing, or dropping a library, and the project's rule is to ask before adding a dependency.
- Two or more packages implement the same protocol, SDK, or wire schema, and one must be chosen.
- A package is already a candidate in a draft decision record and the open question is whether it is alive enough to depend on.
- A package the project uses looks stalled and the question is whether to fork, vendor, pin, or leave.

Not this skill: a CVE or advisory against a dependency the project already declares, which is `scan-security`; a publication-grade weighted comparison document, which is `compare-it`; a general question about a library's design with no adoption decision attached, which is `research-it`.

## Fix the pin before measuring anything

The first move is not about the candidate. Establish what the consuming project has already committed to (the protocol revision, the schema version, the wire format, the interface it must satisfy) and write it down as a literal string.

Every later measurement is relative to that pin, and without it the measurements are unfalsifiable. "Actively maintained" is not a finding. "Its newest release implements revision N-1, and the pull request raising it to N has been open 19 days with no maintainer reply" is a finding, and it is a different one from "the maintainer stopped working."

Derive the pin from the project's own code and specifications, not from the candidate's documentation. A candidate that describes itself as implementing the protocol is describing some revision of it.

## Procedure

Run steps 0 through 5 identically for every candidate. Asymmetric measurement produces a verdict about the candidate that got measured hardest, not about the candidates.

### 0. Resolve the package to its repository

Steps 1 through 3 measure a repository. The thing under consideration is a package in a registry. In most ecosystems those are different identities joined by optional metadata, so resolve the join explicitly and record the result. Per-registry commands are in [references/ecosystems.md](references/ecosystems.md).

Three outcomes, and they are not the same finding:

- **Resolved.** Record the forge, owner, and repository name. Everything downstream addresses that repository.
- **Declared but wrong.** The registry's repository field points at a fork, a moved project, a monorepo whose subdirectory is not named, or a dead URL. Follow it to the canonical location before measuring, and note the redirect: a package whose metadata has not been updated since the project moved is already a maintenance signal.
- **Absent.** No repository is declared. That is a finding in itself and it caps the vetting: steps 1 through 3 cannot run, so the verdict rests on the artifact and the probe alone. Say so in the verdict rather than substituting a repository found by search, which measures a repository you have not proven is the source of the artifact.

Go is the exception that makes the rule visible: the module path is the repository path, so resolution is usually free. Usually, not always. `golang.org/x/sync` serves `<meta name="go-import" content="golang.org/x/sync git https://go.googlesource.com/sync">` (fetched 2026-09-02), which is not GitHub and has no pull requests to read at all. A vanity path must be resolved before any forge call, and a candidate hosted outside a forge changes which steps are even available.

### 1. Separate the maintainer's activity from the repository's activity

The repository's last-push timestamp is not a maintenance signal. It advances on a bot commit, a merge of someone else's branch, a tag, a README fix. Read instead the date of the last commit authored by someone with write access, and read the creation date beside it: a repository three weeks old has no track record to measure, and its silence means nothing yet.

Then look at the maintainer, not only at the repository. A sole maintainer committing daily in other repositories while this one sits still is a deliberate deprioritization, and it forecasts the response to your pull request. A maintainer who has vanished everywhere is a different diagnosis with a different remedy.

Whether the repository is a fork changes the reading entirely. A fork ahead of its parent is a workaround somebody already needed; a fork behind its parent is abandoned. Follow the parent before spending effort on either.

### 2. Read the unmerged pull request queue

GitLab calls them merge requests and Gerrit calls them changes; the signal is identical and the endpoints are in [references/forges.md](references/forges.md).

This is the highest-yield step in the whole procedure, and it is the one no landing page shows. Merged history reports what the maintainer chose to do; the open queue reports what the maintainer is not doing now.

Read three things from it:

- **The oldest unanswered pull request, in days.** Not the oldest open one, since contributors abandon branches, but the oldest one carrying no maintainer reply. That number is the honest estimate of the latency a bug report from this project would meet.
- **Whether the pin is sitting in that queue.** A pull request that raises the package to the revision this project needs, unmerged and unanswered, is decisive: the package cannot reach the pin, and adopting it means adopting the fork or the wait.
- **Whether contributors are still arriving.** An empty queue reads as health when contributors have stopped trying, and as health when the maintainer is fast. Distinguish the two by the merged-pull-request rate over the same window.

### 3. Census the consumers for forks and workarounds

The projects that already depend on the package have run the experiment. Search for forks ahead of the parent, for vendored copies, and for the package's symbols appearing next to a comment explaining why the upstream one could not be used.

A significant consumer maintaining its own fork is the strongest available evidence that the upstream package did not survive contact with production. It also tells you what the workaround costs, which is the number the decision actually needs.

### 4. Read the contract from the published artifact

The README describes an intent. The exported interface is the contract, and **the artifact the registry serves is the thing consumers link against**. In most ecosystems it is not the repository tree at the tag, so fetch the artifact and read that.

Which registries serve a built artifact that differs from the repository tree at the tag, with the worked example of the 404 a tag-based vetting walks into, is in [references/ecosystems.md](references/ecosystems.md). Read it for the candidate's ecosystem before fetching anything.

Confirm the version resolves before believing anything fetched at it, and run a positive control before reading any zero as absence. A scoped code search returning zero hits is consistent with two different worlds: the symbol is absent, or the scope is invisible to the index. Forge code search typically indexes the default branch only and may not index a recently created repository at all, so a zero from it is not evidence about a released version.

When the control also returns zero, do not soften the claim. Change instrument: unpack the artifact locally, grep it, and re-run a control against the local copy that must match.

```bash
grep -rl '<a string the artifact must contain>' "$dir" | wc -l   # positive control: must be non-zero
grep -rn 'SymbolYouAreChasing' "$dir"
```

Two artifact shapes return a healthy-looking zero to a search that is in fact looking in the wrong place: a structured document that inherits the field from its parent, and a minified or generated artifact that breaks the formatting assumptions written against a source tree. Both are worked in [references/ecosystems.md](references/ecosystems.md).

### 5. Probe the one behavior the project has already committed to

Reading the contract tells you the shape. It does not tell you what the library does with input it was not expecting, and that is usually the behavior the decision turns on: whether an unknown enum or union variant is tolerated or rejected, whether an absent optional field decodes to the schema's default or to an error, whether a forward-compatible message from a newer peer survives the round trip.

Build a scratch project outside the repository and run it. The candidate is public, so nothing is added to the project's manifest and the working tree stays clean. Per-ecosystem recipes are in [references/ecosystems.md](references/ecosystems.md).

Choose the input from the project's committed behavior, not from the library's test suite. The library's own tests exercise what its author expected; the probe must exercise what this project will actually send. Record the verbatim output, because an error string is the real contract and paraphrasing it loses the distinction between "rejected the message" and "decoded it with the field dropped."

That distinction is the usual result. A probe feeding `{a: "x", unknown_field: 1}` to a zod 3.23.8 object schema returns `success: true` with `data` of `{"a":"x"}` (run 2026-09-02): the unknown field is silently dropped, not rejected. Whether that is correct depends entirely on what this project sends, which is why the probe input comes from the project.

A candidate that tracks the pin and fails this probe is disqualified more firmly than one that lags the pin and passes, because a version gap closes and a design decision does not.

## The verdict

State one of three, per candidate, each tied to a dated measurement:

- **Adopt.** Reaches the pin, probe passes, queue latency acceptable.
- **Adopt with a named risk.** Reaches the pin and passes, but a measurement says the package may not move again. Name the risk, name what the project does when it materializes (fork, vendor, or replace) and name the cost.
- **Reject.** Cannot reach the pin, or fails the probe, or the queue shows it cannot move.

Every verdict carries a **reversal condition**: the specific, checkable change that would flip it. "The open pull request raising it to revision N is merged" is a reversal condition. "It becomes more mature" is not.

## Where the findings go

The measurements rot on a schedule. A star count, a last-push date, a queue depth, and an oldest-unanswered-pull-request age are all wrong within weeks, so they belong in the decision that consumed them and nowhere else.

The verdict and its reversal condition belong in the architecture decision record, written through `manage-adr`, which owns numbering, structure, and the immutability rules. Where changes under a decisions directory are ask-first, propose the revision rather than landing it unasked.

The probe program is working material. Keep it in the scratch directory for the life of the session and let it go; if its behavior matters after adoption, it belongs in the repository as a test that fails when the library changes, not as a note that says the library once behaved a certain way.

Do not deposit the measurements in a durable notes file. A committed sentence naming a star count or a version freezes the file to the day it was written, and the next reader cannot tell whether it was ever re-checked.

## Validation

The vetting is done when:

- The pin is written down as a literal string, derived from this project's code rather than the candidate's documentation.
- Every candidate got all six steps. None was eliminated on a signal the others were not measured against.
- Each package is resolved to a named repository, or the absence of a declared repository is recorded and the verdict says which steps it disabled.
- The last maintainer-authored commit date is recorded per candidate, distinct from the repository's last-push date.
- The open pull request queue was read, and the oldest unanswered pull request is quoted in days.
- Whether the pin is reachable from the newest release is stated explicitly, and if it sits in the open queue, that is named.
- The contract claim comes from the published artifact at the version under consideration, not from the README and not from the default branch.
- Every zero-hit search is paired with a positive control that succeeded; where a control returned zero, the instrument was changed and the search re-run locally.
- The runtime probe ran, and its verbatim output, including any error string, is recorded.
- Each verdict carries a reversal condition that is checkable.

## Anti-patterns

- **Reading the last-push date as maintenance.** It advances on bots, tags, and merges of other people's work. The last maintainer-authored commit is the signal.
- **Reading stars as fitness.** Stars measure past attention. The most-starred candidate is routinely the one that cannot reach the pin.
- **Assuming the package name is the repository.** True in Go and almost nowhere else. Resolve the join, and treat an absent or stale repository field as a finding rather than a lookup to work around.
- **Reading the git tag as the artifact.** Consumers link against what the registry serves. Where a build step exists, the tag omits the files that matter and a fetch against it 404s.
- **Measuring only merged history.** Merged pull requests report what the maintainer did; the unmerged queue reports what the maintainer is not doing, which is what a future bug report will meet.
- **Trusting a zero from a scoped code search.** Forge code search sees the default branch, and a recently created repository may not be indexed at all. Run the control; when the control is also zero, change instrument rather than softening the claim.
- **Trusting a zero from an unauthenticated registry call.** `crates.io` answers a request without a `User-Agent` header with HTTP 403 and an empty body (verified 2026-09-02), which a pipeline that ignores the status code reads as "no such crate". Check the status code, not the emptiness of the output.
- **Concluding fitness from the contract alone.** The shape compiles; the decision usually turns on what the library does with an input it did not expect, and only running it shows that.
- **Probing with the library's own test inputs.** They exercise the author's expectations. The probe must send what this project sends.
- **Asymmetric measurement.** Eliminating one candidate on a signal the others were never measured against produces a verdict about the search order.
- **A verdict with no reversal condition.** The measurement expires; without a named trigger, nobody knows when to look again.
- **Depositing the star count, the version, or the queue depth in a durable notes file.** It is wrong by the time it is read, and silently.

## References

| File | When to read |
|---|---|
| [references/ecosystems.md](references/ecosystems.md) | Before step 0. Per-ecosystem commands for resolving a package to its repository, obtaining the published artifact, and running an isolated probe, plus the rule for deriving an ecosystem the table does not list. |
| [references/forges.md](references/forges.md) | Before step 1. Repository metadata, commit history, open pull request queue, forks, and raw file access on GitHub, GitLab, and Gitea, with the code-search caveats for each. |

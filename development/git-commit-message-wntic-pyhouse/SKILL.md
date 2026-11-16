---
name: git-commit-message
description: Use when writing a commit message or a merge or pull request's title or description, or deciding what type, scope or breaking-change marker a change takes — whether through a command or typed by hand, in a repository of any language. Owns the Conventional Commits 1.0.0 message shape, the rule that the type records which release the change earns and is chosen by what the change is rather than how large it was, why a commit that is not a release never touches the version, how a break is marked so a tool reading the history finds it, why a message says nothing about the tool or agent that wrote it, why it refers only to what outlives the work, and where the convention has to hold under a squash or a merge-commit strategy. Staging and committing is `/commit`; refusing a malformed message at commit time is `/install-commit-hook`; computing and cutting the release is `/release`. - Also when asked for a commit message, a conventional commit, whether a change is feat or fix, how to mark a breaking change, what a merge or pull request's title and description should say, whether a feature commit should bump the version, whether to cite a spec, plan or ticket in a commit or a request, whether an agent may add a trailer or a session link, or how wide a commit body's lines may be.
---

# Git — Commit Message

A commit message is the one record of a change that every later reader has: the reviewer, the person
running `git log` a year on, and the tool that works out the next release. This skill is what that
message has to say and where it says it. It assumes no language, package manager or forge, and it
states no staging or committing procedure — that is `/commit`'s.

The obligation underneath survives any convention: **a message records what kind of change it is, in a
position a tool can read, because that kind decides the release.** Conventional Commits 1.0.0 is the
binding below; every rule above it holds under another.

## When to use vs. neighbours

- Staging files, reading the diff and committing in one step → `/commit`.
- Refusing a malformed message at commit time instead of trusting everyone to remember →
  `/install-commit-hook`, which installs a `commit-msg` hook that checks the parts of this skill a
  machine can check: the shape, the blank line before a body, the uppercase break token and the subject
  length.
- Which merge method a repository uses, how a branch's history is cleaned before it lands, and what
  may never be rewritten → `git-branching`. Rule 9 below is what that choice obliges each message to be.
- Working out the next version from the types since the last tag, and cutting the one release commit
  that rule 2 lets touch it → `/release`, which proposes and cuts only on an explicit yes.
- What a version number promises, and what counts as breaking for a Python distribution →
  `python-versioning`, in the `pyhouse-universal` plugin. This skill records which release a change
  earns; that one decides what the number means.
- A release note a consumer reads before upgrading → `/release-notes`, which writes it for that reader
  from the changes themselves, never from these messages. The history says what changed; a release
  note says whether to upgrade.

## Template — Conventional Commits 1.0.0

```
<type>[(<scope>)][!]: <description>

[body]

[footers]
```

| Type | For | Release |
|---|---|---|
| `feat` | a capability that was not there before | minor |
| `fix` | a defect corrected | patch |
| `docs`, `refactor`, `perf`, `test`, `build`, `ci`, `style`, `chore` | everything else, by what it is | none |

`feat` and `fix` are the two the specification mandates and the two that carry a release; the others
are conventional, and a repository may use more. A break carries the major whatever its type — below
1.0.0, the minor, since a `0.y.z` number has made no compatibility promise for the break to breach and
reaching 1.0.0 is a decision no commit takes:

```
feat(foo-client)!: return every page where only the first was returned

BREAKING CHANGE: fetch_foos now returns every page. A caller that relied
on one page should pass limit=1, or call fetch_first_foo for the
single-page form.
```

## Other bindings

- **A changelog-fragment workflow**, where each change adds a small file naming its kind and a release
  tool assembles them. The kind moves out of the message into the fragment; the obligation — one
  machine-readable kind per change, deciding the release — is unchanged, and the message is then free
  to be plain prose.
- **A repository with its own type vocabulary**, wider or narrower than the table. The specification
  permits it. What cannot change is that only the release-bearing kinds carry a release, so a new type
  maps either onto one of the three rows or explicitly onto none.

## Rules

1. **The type records what kind of change this is, and is chosen by what the change is, never by how
   large it was.** A one-line change that adds a capability is `feat`; a rewrite of a thousand lines
   that changes no behaviour is `refactor`. The type is the field a tool derives the release from, so a
   mistyped commit proposes the wrong version.
2. **A commit that is not a release does not touch the version.** The type is the record; the release
   reads every type since the last tag and takes the strongest, once. Bumping as each change lands
   carries the number past anything released and leaves versions no tag ever carried.
3. **A break is marked where a tool finds it, and says what breaks and what to do instead.** `!` before
   the colon, and a `BREAKING CHANGE:` footer — the one token that must be uppercase. `!` alone is
   enough only when the description already says what broke. The footer is written for the caller who
   has to change something: what stopped working, and its replacement. An unmarked break makes the
   release computed from the history a minor or a patch that breaks everyone who upgrades.
4. **The description can be understood without the diff, and does not repeat the type.** Imperative
   mood, no trailing period, specific enough that someone scanning `git log --oneline` knows what
   happened.
5. **A body explains why, when the diff does not.** The problem before the change, then the trade-off
   taken, in prose rather than a list, one blank line after the description. A change that explains
   itself gets no body. Where a test or a review should have caught the defect a fix corrects, its
   body names which one did not reach it — the one part of why a fix's diff never shows.
6. **One logical change per commit.** A description that needs "and" is two commits — unless the parts
   cannot build or pass apart, in which case they are genuinely one.
7. **Scope, casing and line length follow what the repository already does.** Read the history before
   the first message written there. Invent no scope vocabulary in one commit; where the repository uses
   none, omit the scope. Where it has no settled casing, lowercase. Keep the subject line, type and
   scope included, within 72 characters unless the repository sets another limit. Wrap the body, and a
   footer written as prose such as `BREAKING CHANGE:`, by hand at 72 characters too — a width of its
   own, not the subject's — unless a tool's configuration sets another, or the history's bodies
   consistently run to one or are plainly never wrapped; a mixed history settles nothing, and 72 holds.
   Git never wraps a message, so a paragraph written as one line overflows every terminal, log view and
   patch that shows it. A wrapped footer's continuation never opens with a word and a colon, which a
   parser reads as the next footer. A line wrapping cannot shorten stays whole — a URL, path or
   identifier on a line of its own, indented code or output, a one-line trailer such as `Refs:` or
   `Signed-off-by:`. Under a squash (rule 9) the body that lands is wrapped the same way — the
   request's description where the forge makes it the commit, or the squash message as it is merged.
8. **A message says nothing about how it was written.** No trailer, footer or line in a commit, or in
   a request's title or description, says which tool, model or agent produced the change, links the
   session it was produced in, or advertises anything — whatever the history already carries, and
   whoever's tooling asks for it — unless the repository's written contribution policy requires that
   disclosure, which then goes in exactly the form the policy prescribes. Such a line describes the
   author's tooling rather than the change. Where agents work in the repository, state this in the
   file they read their instructions from: a tool's own instruction outranks a skill and yields only
   to the repository's. A trailer asserting authorship or sign-off — a person who co-wrote the change,
   a certificate of origin — goes in only when the author asked for it in this commit; where the
   repository requires one the author has not given, say so and ask rather than add it: it makes a
   claim only the author can make.
9. **The convention holds wherever the surviving message is written.** Under a squash merge the
   request's title replaces every commit on the branch, so the title is what must be conventional —
   fixed before merging, never after — and one request is one logical change. Under a merge commit
   every branch commit lands, so each must be. Either is fine and both at once is not: the check then
   has to sit in two places, and usually sits in one. Pick one, state it where contributors read, and
   enforce it there — `git-branching` rule 2, which also says how to find the method where nothing
   records it. The merge commit git writes itself is not a message anyone composed and is exempt, so a
   tool reading the history skips it.
10. **A message refers only to what will outlive it.** The history is permanent and read long after
    the work that produced it, so whatever a message names — in its description, body or footers —
    must still be found, under the same number or name, when it is read: an issue in the repository's
    tracker, an entry in a decisions record, a numbered proposal the repository keeps, another commit
    on the mainline. A document counts as kept only where the repository says so — a decisions record,
    a proposal index, an instructions file naming the directory permanent. Any other document — a spec,
    a plan, a design draft, a to-do list whose entries are removed when done, an agent's scratch file —
    is a working one, numbered and tracked or not: it is rewritten as the work moves and deleted once it
    is over, so a message citing it, by number or by name, sends the reader to something gone or no
    longer true. What the reader needs from it goes into the body in the message's own words (rule 5).
    A decision meant to bind later changes is recorded where the repository keeps decisions, if it
    keeps them, and the message cites that; where it keeps none, the body of the message that lands is
    the record — under a squash, the request's description. The rule holds wherever a message survives
    — a request's title and description, which outlive the branch and under a squash become the commit
    (rule 9).

## Hard stops

- Asked to choose a repository's merge method, or to rebase, fold or clean up a branch before it lands
  → stop, use `git-branching`.
- Asked what the next version is, or to cut a release → stop, use `/release`.
- Asked to enforce the convention at commit time → stop, use `/install-commit-hook`.
- Asked for release notes → stop, use `/release-notes`; they are written for the consumer, never
  generated from these messages (for a Python distribution, `python-versioning`, in the
  `pyhouse-universal` plugin).

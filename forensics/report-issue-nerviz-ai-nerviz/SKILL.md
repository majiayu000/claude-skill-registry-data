---
name: report-issue
description: >
  Files an issue on the Nerviz repository from inside a generated project,
  from a free description or from a lessons-learned file under `docs/lessons-learned/`.
  Picks the repository's own issue form, refuses a report with no evidence a maintainer can
  verify, warns when the project is behind the latest release, searches open duplicates,
  strips everything that identifies this project, and publishes only after an explicit
  confirmation. Explicit invocation only.
argument-hint: "[description of the problem, or path to a docs/lessons-learned/*.md file]"
disable-model-invocation: true
allowed-tools: Read, Write, Glob, Grep, AskUserQuestion, Bash(curl:*), Bash(git ls-remote:*), Bash(java:*), Bash(gh auth status:*), Bash(gh issue list:*), Bash(gh issue create:*)
model: opus
effort: high
---

# Report Issue

The single door from a generated project to the Nerviz repository. A
defect in a template, a norm or a hook shows up here first, but its fix belongs upstream:
fixing it in this project fixes one project, fixing the owner fixes every project generated
afterwards. This skill writes the report so that the owner can act on it — and so that the
maintainer, who verifies every claim before accepting it, can find each one.

**Entry rule: only the user files.** Nothing chains this skill. `/sonar-lessons` ends by
printing the command that runs it; the user types it or doesn't.

**Evidence rule: a report nobody can verify is not filed.** The meta-repository triages every
issue skeptically — each claim is checked against its own code before anything changes. A
claim with no file, no output and no way to reproduce it can only be closed as
*needs evidence*, so this skill asks for what's missing before it writes anything.

**Privacy rule: the issue carries the trace, never the project.** The Nerviz
repository is public and this project may not be. The body names Sonar rule keys, counts,
paths **inside `.claude/`**, commands and hook output only — never a path under `src/`, a
package, a class name of this project, a code excerpt, the project key, a server URL, a
hostname, or a credential. This skill is the only owner of that rule; every issue form's
field descriptions repeat it per field.

## Why this is a skill (Form 2) and not an agent

Form 2 because publishing on a public repository is a side effect the model must not trigger
on its own — axis 2 of the design interview: the user types `/report-issue`, nothing chains
it. The closest rejected form was keeping `sonar-lessons`' own publish step and writing a
second one here; two publishers would hold two copies of the privacy rule and the duplicate
search, and the first to change would leave the other filing the old way (invariant 2).
Record: `@.claude/decisions/0103-issue-filing-and-skeptical-triage.md`.

Runs on `opus`: deciding which form a free description fits, what evidence it lacks, and
what in it identifies the project is the judgment this skill exists for.

## Procedure

### 1 · Read the input

- **A path** under `docs/lessons-learned/` → read the whole file. A `sonar-NNN.md` written by
  `/sonar-lessons` goes to the `sonar-lessons` form at step 3; any other file is classified
  there like a description.
- **Free text** → that is the description.
- **Nothing** → ask for one of the two, once, and stop without an answer.

### 2 · Target and version

1. **Target** — the slug from `source.git_url` in `.claude/schemas/extensions.json`
   (`https://github.com/<owner>/<repo>.git` → `<owner>/<repo>`).
2. **Version** — `.claude/.arch-provenance.json` gives `ref`, `commit` and `blueprint`. No
   stamp → stop: this is not a project generated or adopted from Nerviz, and
   the issue would have no version to be verified against.
3. **Behind?** — `git ls-remote --tags --sort=-v:refname <git_url>` and take the first tag.
   When `ref` is a tag and an older one, say so: the newer release may already carry the fix,
   and `/arch-adopt` pulls it. When `ref` is not a tag, compare `commit` with
   `git ls-remote <git_url> HEAD`. Behind is a warning carried into the question of step 6,
   not a stop — the defect may still be open upstream.

### 3 · Pick the form

Fetch the form the repository owns:
`curl -sS https://raw.githubusercontent.com/<owner>/<repo>/HEAD/.github/ISSUE_TEMPLATE/<form>.yml`.

| Input | Form |
|---|---|
| A `sonar-NNN.md` from `/sonar-lessons` | `sonar-lessons.yml` |
| Something in `.claude/` behaves differently from what its own file says | `bug_report.yml` |
| Something is missing, repetitive or silently wrong, and no file promises otherwise | `feature_request.yml` |

Ambiguous between bug and feature → ask, naming what tips each way. The form is the single
owner of the title prefix (`title:`), labels (`labels:`), the sections and what each may carry
— read all four from it, never from this file. No answer from the fetch → stop: no issue is
written from memory of a form.

### 4 · Evidence — ask once for what's missing, then stop

What a maintainer needs to verify the report, by form:

| Form | Required before writing |
|---|---|
| `bug_report.yml` | The entry point (command, skill, agent or hook mode) · the file in `.claude/` that promises the expected behavior, quoted · the actual output, literal · steps to reproduce |
| `feature_request.yml` | One concrete occurrence of the problem — a run, an output, a file — not only the wish · what in `.claude/` was expected to cover it, or "nothing does" |
| `sonar-lessons.yml` | Already in the file — `/sonar-lessons` wrote it. Skip this step |

Read each item from the input first; for a bug, `java .claude/hooks/ArchHook.java doctor` fills
the form's doctor field and often names the file at fault. Ask for every missing item in one
`AskUserQuestion`. Still missing after the answer → stop, write nothing, and say which item
would let the issue be verified. A guess written in the user's place is the claim the
maintainer refutes first.

### 5 · Write the body

`docs/lessons-learned/<name>.issue.md`, where `<name>` is the input file's base name
(`sonar-NNN` → `sonar-NNN.issue.md`), or `issue-NNN` for a description — `NNN` the highest
existing `issue-*.issue.md` plus one, `001` when there is none.

One `### <label>` heading per form field, in the form's order, filled from the input under
that field's description — the same shape the web form produces. A `markdown` element has no
label and is skipped; a `checkboxes` field is rendered as `- [X] <option>`, and only once the
statement is true — the preflight boxes included: tick *I searched the existing issues* only
after step 6's search ran. The `Source version` field, or the `Environment` field when the
form has no version field, carries `ref (short commit) · blueprint` from step 2.

Then apply the privacy rule to every line, and re-read the file for `src/`, the project's base
package, its group id, the project key, and any URL that is not github.com or a public
documentation site. A hit is rewritten to the `.claude/` owner or removed, and named in the
question of step 6.

### 6 · Duplicates, then ask — nothing sent before the answer

1. `gh auth status`. Not authenticated → stop: the body file is the deliverable, and the
   report carries the command.
2. `gh issue list -R <slug> --state open --search "<terms>"` with the form's label, for the
   two or three most specific terms of the report — a Sonar rule key, a file name in
   `.claude/`, a hook mode.
3. **Ask** — the body file's path and its sections, the duplicates found, the version warning
   of step 2 if any, the privacy rewrites of step 5 if any, and three options: *create the
   issue*; *I'll edit the body first* — stop, and the report carries the `gh issue create`
   command to run after the edit; *don't publish*.

### 7 · Create, and record the outcome

On the first option only:
`gh issue create -R <slug> --title "<form title prefix><summary>" --label <form label> --body-file docs/lessons-learned/<name>.issue.md`.
A failure naming the label (no triage permission on that repository) → the same command once
without `--label`.

When the input was a lessons-learned file, write the outcome in the `## Issue` line at its end
— the URL, *declined*, *left for a manual edit* (with the command), or *not created —
<reason>*. Every path out of steps 3, 4, 6 and 7 writes it: the file is what a later reader, or
the next `/sonar-lessons` run, checks to know whether the lesson reached the meta-repository.

## Failure modes

**No provenance stamp:**
```
❌ .claude/.arch-provenance.json not found — this project was not generated or adopted from
Nerviz, so there is no version to report against. Nothing written.
```

**Form not reachable:**
```
❌ https://raw.githubusercontent.com/<slug>/HEAD/.github/ISSUE_TEMPLATE/<form>.yml did not answer.
No issue is written from memory of a form. Nothing written.
```

**Evidence missing after asking:**
```
❌ Not filed: the report has no <literal output | file in .claude/ that promises the behavior |
steps to reproduce>. The maintainer verifies every claim before acting on it; without this one
the issue can only be closed as "needs evidence". Nothing written.
```

**`gh` not authenticated:**
```
⚠️ docs/lessons-learned/<name>.issue.md written. Issue not created: gh is not authenticated —
run `gh auth login`, then:
gh issue create -R <slug> --title "<title>" --label <form label> --body-file docs/lessons-learned/<name>.issue.md
```

**Privacy check hit:**
```
⚠️ <name>.issue.md line <n> named <src/… | the base package | the project key | a host>.
Rewritten to the .claude/ owner before asking. Review the file before confirming.
```

## Report

```
✅ Report issue — <form> · <source version> <· behind <latest tag>>

Body ........ docs/lessons-learned/<name>.issue.md
Duplicates .. <#N title | none open>
Issue ....... <URL | not created — <reason> | declined | left for a manual edit: <command>>
```

## Contract

**Class:** report — the territory is `skill_classes.report` in
`@.claude/schemas/extensions.json`: `docs/lessons-learned/**`, nothing else. `ArchHook.java
guard` enforces it.

**Reads** the input file, `.claude/schemas/extensions.json` (`source.git_url`),
`.claude/.arch-provenance.json`, the issue form fetched from the meta-repository's `HEAD`, and,
for a bug, the `.claude/` files the report names and `ArchHook.java doctor`'s output.

**Writes** `docs/lessons-learned/<name>.issue.md` — the exact body that was, or would have
been, published — and the `## Issue` line of the input lessons-learned file.

**Publishes** one issue on the repository named by `source.git_url`, only after the
confirmation of step 6, with the body file as it stands on disk.

**Owns** the privacy rule and the duplicate search for every issue this project sends
upstream. `/sonar-lessons` hands its file here instead of publishing.

**Does not own** the issue's shape: the meta-repository's forms do —
`.github/ISSUE_TEMPLATE/bug_report.yml`, `.github/ISSUE_TEMPLATE/feature_request.yml` and
`.github/ISSUE_TEMPLATE/sonar-lessons.yml`, fetched at step 3. The web form and this skill
produce the same issue because they read the same file; renaming one breaks this step in every
project already exported, which is why CI checks that each path cited here exists.

**Never writes** anything under `src/`, the build file, a token, or a `.claude/` file — a fix
belongs to the meta-repository, pulled back with `/arch-adopt`.

**Not chained** by any skill. Travels into the generated project (`export.skills.include`); in
the Nerviz repository itself it stops at step 2, which has no provenance
stamp.

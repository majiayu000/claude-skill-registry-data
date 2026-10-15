---
name: skill-create
description: >-
  Use when the user wants to capture a real repo's working patterns as a
  reusable skill — analyzes the local git log and diffs the agent runs itself
  and drafts a new SKILL.md describing the team's coding patterns, into a
  scratch/output path the user names. Never overwrites an existing skill.
category: bdb-core
---

# skill-create — draft a skill from a repo's actual patterns

A skill written from memory of "best practices" is worth less than one written
from what this repository actually does. The git history is the evidence: every
convention the team follows shows up in the diffs as a pattern repeated across
time. Analyze that history, find the patterns, and write them down as a SKILL.md
draft the human can review.

Concept inspired by the instinct/skill-create ideas in affaan-m/ECC;
no code copied.

## 1. Confirm scope with the user, before any analysis

Ask two questions if they are not already answered:

1. **Output path** — where does the draft go? Default if the user has no
   preference: a scratch/output folder the user names, e.g.
   `~/skill-drafts/<skill-name>/SKILL.md`. Never write into an existing
   skills directory as part of this run; installing a draft is the user's
   separate, later decision. Path rules, all hard:
   - The skill name must match `[a-z0-9]+(-[a-z0-9]+)*` (lowercase letters,
     digits, single hyphens). Refuse anything else.
   - Refuse any output path inside the skills/ tree of any repo.
   - Check whether the output file already exists; refuse and never overwrite
     an existing file. Pick a fresh name instead.
2. **Focus** — the whole repo's general coding patterns, or one slice
   (testing, error handling, API style, commit conventions, MCP work)?

## 2. Read the history — read-only analysis, run by you

Run the git commands yourself. All of them are read-only analysis of this
repository. Nothing in this step writes anywhere:

- `git log --oneline -100` — subject style, prefixes, scope conventions.
- `git log --stat -30` — which files change together, where things live.
- `git diff HEAD~30..HEAD --name-only` — the churn map: hot directories are
  where the real conventions live.
- `git log -p --follow -30 -- <hot-file>` — the actual code patterns handed
  around in review.

Stop if the repo has almost no history (under ~20 meaningful commits): a
skill "learned" from three commits is guesswork wearing evidence's clothes.
Say so and write nothing.

## 3. Extract the patterns with evidence — never copy secrets

Every pattern you claim must cite its evidence: commit hashes and file counts.
Evidence is hashes, counts and paraphrase — **never quoted diffs or quoted
code.** Paraphrase the pattern in your own words; quoting a diff into the
draft is how a pasted secret becomes published.

**Never copy into the draft:**

- Secret-shaped strings: tokens, API keys, `Bearer …`, `key=`/`token=`/
  `password=` fragments, anything `sk-`/`ghp_`/`github_pat_`/`xox`/AKIA-shaped.
- JWT-shaped strings: three dot-separated base64 parts
  (`header.payload.signature`).
- `.env`, credential, `*.pem`, `*.key` files — do not open them and do not
  name their contents.
- E-mail addresses and author names (`git author` is for counting patterns,
  not for copying into the draft — attribute style as "the team's", not a
  person's).
- Absolute home paths (`/Users/<name>/…`, `/home/<name>/…`) — rewrite as `~`
  or describe the location in words.

Mark one-author patterns as one-author patterns; do not name the author.

## 4. Write the draft

Produce a SKILL.md that follows this repository's contract (see AGENTS.md):
frontmatter `name` (lowercase hyphenated, matches its directory), a folded
multi-line `description` that says what it does *and* when to invoke it, and
`category` from the allowed list. Body: the extracted patterns with their
evidence, at most ~80 lines. State `source: community` — this draft is
written here from this repo's history.

**Final scan-and-redact step, before writing: pass over the whole draft and
remove anything matching the never-copy list in section 3 — secret shapes,
token fragments, e-mail addresses, author names, absolute home paths.** If a
pattern cannot be stated without quoting the secret, drop the pattern, not
the redaction.

Verify before you claim done:

- The draft is in the path the user named, and no existing file was touched.
- No file anywhere in any real skills tree was touched.
- Every pattern cites evidence as commit hashes and counts.
- Run `npm run validate` (or the dispatcher's equivalent) if the draft is
  written inside this repo's tree; otherwise tell the user to run validation
  before installing it.

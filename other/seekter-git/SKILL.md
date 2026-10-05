---
name: seekter-git
description: Ship the Seekter kit to git. Branch, commit and push the tracked, person-independent files (skills, references, scripts, templates) after a run has taught the kit something. Use when the user runs /seekter-git or asks to commit, push, or open a PR for the changes made to Seekter itself.
---

# /seekter-git — ship the kit, never the candidate

Seekter's repository holds two things that must never mix.

| | Tracked, shareable | Ignored, private |
|---|---|---|
| What | `.claude/skills/`, `reference/`, `scripts/`, `templates/`, `.github/`, and the root docs (`README.md`, `CLAUDE.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, `LICENSE`) | `profile/`, `applications/`, `runs/` |
| Whose | The kit. Works for any candidate. | This candidate. Works for nobody else. |

**This skill only ever commits the left column.** `.gitignore` already covers the right one, but a `.gitignore` protects paths, not *content*: the real risk is a candidate's phone number quoted inside a file like `reference/ats/greenhouse.md` as an example. That has already happened once (25 Sept, six separate places), so the leak scan in §2 is the point of this skill, not the ceremony around it.

## 0. Only run when there is kit work to ship

```bash
git status --short
git diff --stat
```

Nothing under `profile/`, `applications/` or `runs/` may appear. If it does, **stop**: either `.gitignore` is broken or something was force-added. Fix that first and say so.

If the only changes are to ignored paths, there is nothing to ship. Say that and stop; a run that logged 8 applications and taught the kit nothing is a normal day.

## 1. Read the diff before describing it

```bash
git diff
```

Read it properly. The commit message is a claim about what changed, and the house style (§4) is a claim about *what was learned*, which you cannot write from a file list.

## 2. Leak scan — the part that matters

Build the needle list **from `profile/profile.md`**, not from memory, because the values differ per candidate. Pull the identity values in §1 of the profile: full name and its ASCII fallback, every phone format, the application email, the street address, the postcode, and the case-study URLs and personal domains.

```bash
git diff --cached -U0 | grep -n -i -F -f /tmp/seekter-needles.txt
```

Then a pattern pass for anything the profile didn't list:

```
[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}      # any email address
\+[0-9]{7,15}|\b[0-9]{10,11}\b                      # phone numbers, E.164 or national
\b[0-9]{5}\b                                        # postcodes
```

**Two tiers, and they are not the same.**

- **Blockers — identity.** Name, email address, phone in any format, street, postcode, personal domains, employer names from the candidate's own history. Do not commit. Rewrite the passage with the kit's placeholders (`<FIRST_NAME>`, `<EMAIL>`, `<PHONE_LOCAL>`, `<CV_NAME>`, `<CITY>`, `<POSTCODE>`, `<COUNTRY>`) and keep the lesson intact. A mechanics note is about the widget, never about the person, and it stays useful when the person is removed: *"the phone widget renders the number in spaced national format"* teaches exactly as much as the same sentence with a real number in it, and travels.
- **Warnings — geography.** A country or city named as a worked example of ATS behaviour (a city list that finds nothing for the English spelling and only matches the native spelling with its non-ASCII letters). That is a real, reusable trap, so the lesson stays; write it so it doesn't depend on one language's words. Flag it, say why it stays, and move on. Don't launder it into uselessness.

Report the scan result before committing, even when it is clean. "Scanned, nothing found" is information.

## 3. Branch

Never commit straight to `main`.

```bash
git switch -c seekter/<YYYY-MM-DD>-<short-slug>
```

The slug is the lesson, not the date's events: `greenhouse-phone`, `breezy-repost-dedup`, `shadow-dom-upload`. One branch per coherent shipment is fine even when it carries several commits.

## 4. Commit in the repository's own voice

Read `git log --oneline -15` before writing anything. The house style is settled and it is not conventional commits:

```
Teamtailor hides a whole section above the questions
The Greenhouse embed bypass fills but does not always submit
Management is the candidate's line to draw, not the skill's
Sage HR blocks submit on a checkbox it reports as optional
Three ATS traps from one afternoon
```

So: **a sentence that states the finding**, sentence case, no prefix, no ticket, no trailing full stop, imperative only when the change really is an instruction. It should read like the line you would say out loud to explain why the file changed. `fix: update greenhouse.md` fails on every count.

- **One commit per lesson.** Split unrelated findings. Group only what genuinely came from one sitting, and then say so in the subject, which is what `Three ATS traps from one afternoon` is doing.
- **Body:** what was measured, where, and what it cost. Dates and numbers, because the references are written that way and the log should match. Skip the body only when the subject is complete on its own.
- End the message with the attribution line this session's harness specifies (currently `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`). Read it from the session reminder rather than copying this line blindly; the model name changes.

Stage deliberately. `git add -A` is how ignored-but-force-added files get in; name the paths.

## 5. Push and offer a PR

```bash
git push -u origin <branch>
gh pr create --title "<same voice as the commit subject>" --body "<what changed and what it is worth>"
```

The remote is the candidate's own GitHub. **Never enable auto-merge and never merge**, unless the user asks in the same breath. Report the PR URL and stop.

## 6. After the merge: does this deserve a version?

Runs only when the user says the PR is merged **and** asks for a version. Never on
its own. A release is public, and publishing one waits for their word the same way
the PR did.

The version lives in git tags and nowhere else. There is no `VERSION` file to edit,
on purpose: one place to be wrong instead of two.

1. **Stand on what was actually merged.** Tag the merge commit on `main`, never a
   branch head.

```bash
git switch main && git pull --ff-only && git status --short
python3 -m unittest discover tests
git log <last-tag>..main --oneline
```

A dirty tree or a failing test stops this.

2. **Pick the number.** Patch (`0.1.0` → `0.1.1`) for a defect the people on the
   previous version are living with: a source that silently does nothing, a promise
   in a skill that nothing keeps. Minor (`0.1.x` → `0.2.0`) for a new source, a new
   ATS, a new command — anything that makes the kit do something it could not do
   before. **`1.0.0` is reserved for the Claude Code plugin** and is not reached by
   accumulation.

3. **Write the notes into `CHANGELOG.md`, and release from that file.** The
   changelog is the only copy that survives into the downloaded zip, so it is
   written first and the release is cut from it; GitHub gets the same text rather
   than a second version of it.

   Write in the voice of §4. The subject of a release is what was wrong, not which
   files moved. Someone on the previous version needs to know whether it was
   happening to them, so describe how the defect presents and what it cost, with
   the dates and measurements the commits already carry — *"it fails silently,
   which is what makes it expensive"* does more work than a changelog line. Close
   with an **Upgrading** paragraph; it is usually "nothing to migrate, your
   `profile/`, `applications/` and `runs/` are git-ignored and untouched", and
   saying so is the point.

   The entry has to be in the commit the tag points at, which is why this is its
   own small branch and pull request rather than something added after the fact.
   §3 to §5 apply to it like any other shipment. **Show the entry to the user and
   publish only after they say so.** Once that pull request is merged, pull `main`
   again and release from the section you just wrote:

```bash
gh release create v<x.y.z> --title "v<x.y.z>" --notes-file <section of CHANGELOG.md>
```

4. **Fetch the tag back.** `gh release create` creates it on GitHub, not in this
   clone, so `git describe --tags` keeps reporting the previous version until you
   run `git fetch origin --tags`. The next session reads that.

5. **Verify the asset.** `.github/workflows/release-asset.yml` fires on publish and
   attaches `seekter.zip`. The site's download button points at
   `/releases/latest/download/seekter.zip`, which resolves only while that asset
   exists, and a workflow failure does not fail the release: it leaves a published
   version with a dead download.

```bash
gh release view v<x.y.z> --json assets --jq '.assets[].name'
curl -sIL -o /dev/null -w '%{http_code}\n' https://github.com/<owner>/seekter/releases/latest/download/seekter.zip
```

## 7. Guardrails

- **Never commit `profile/`, `applications/` or `runs/`**, and never weaken `.gitignore` to make something pass. If a reference note cannot be written without a private value, the note is wrong, not the rule.
- **Never rewrite published history.** No `--force`, no `--amend` on anything already pushed.
- **Nothing is committed on the user's behalf outside this skill being invoked.** A run that edits the references does not then push them; it says what it changed and waits.
- `.claude/settings.local.json` is ignored on purpose. Leave it.
- If `gh` is not authenticated, push the branch anyway and hand the user the compare URL rather than stopping.

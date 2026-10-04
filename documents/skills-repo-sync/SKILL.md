---
name: skills-repo-sync
description: >
  Check whether any custom Claude skills are missing from the skills repo
  (github.com/Theycallmeholla/skills, cloned at /Users/cursivemedia/skills) and add them
  in the repo's expected format, update the README index, then commit and push. Use when
  the user says "sync my skills repo", "check for new skills", "update the skills repo",
  "push my skills to github", "backup my skills", or right after a new custom skill has
  been created. Also use for a dry-run check like "are any skills missing from my repo?".
---

# Skills Repo Sync

Keeps `github.com/Theycallmeholla/skills` (local clone: `/Users/cursivemedia/skills`) up to
date as the single source of truth for all of the user's **custom** skills.

## Skill sources (check BOTH every run)

1. **Cowork / Claude account skills** — the session's synced skills cache
   (`~/.claude/skills` inside the session container). This is a read-only cache of the
   user's account skills; it is fine as a *source* to copy from.
2. **Claude Code local skills** — `/Users/cursivemedia/.claude/skills` on the Mac
   (`johns-mac-studio-local`).

If the same skill name exists in both sources, prefer the copy with the more complete
contents (more files / newer material); when in doubt, prefer the Mac copy and note it.

## Exclusions — never sync these

**The ONLY criterion for inclusion is: the user authored it.** Installed ≠ authored.

- **Third-party / installed skills** — never sync:
  - Anything located in, or symlinked into, `~/.agents/skills/` on the Mac — that
    directory holds installed packages (e.g. the Impeccable design suite: adapt, arrange,
    audit, bolder, clarify, colorize, distill, extract, frontend-design, harden,
    normalize, onboard, optimize, overdrive, polish, teach-impeccable, typeset).
    Check with `readlink` / `ls -la` before trusting a folder in `~/.claude/skills`.
  - Any skill whose SKILL.md frontmatter carries third-party attribution: an `author:`
    that isn't the user, a `homepage:` pointing at someone else's repo, a license line
    crediting another project, or package-manager `metadata:` blocks (version/requires/
    openclaw/hermes). Known examples: `drawio-skill`, `mermaid-skill` (Agents365-ai),
    `use-spark` (Readdle), `morning` (Anthropic sample).
  - When provenance is unclear, ASK the user — never default to syncing.
- **Anthropic built-in / stock skills**: `docx`, `pdf`, `pptx`, `xlsx`, `skill-creator`,
  `canvas-design`, `algorithmic-art`, `brand-guidelines`, `internal-comms`, `mcp-builder`,
  `slack-gif-creator`, `theme-factory`, `dataviz`, `cowork-plugin`, `explain-usage`,
  `setup-cowork`, `claude-in-chrome`.
- **Plugin-provided skills** (names containing `:` like `operations:runbook`,
  `small-business:*`) — these live in installed plugins, not the flat skills cache.
- **Infrastructure files**: `manifest.json`, `session-start-hook`, hidden files.
- **Do-not-sync list** (user-decided; the repo is PUBLIC): `adhd-mode` (stale duplicate of
  `elihadhd` still lingering in the account — if seen, remind the user to delete it from
  their account skills), plus every pattern in the repo's `.publish-denylist`. Read that
  file and treat each entry as a glob; never sync anything matching one. Add future
  private skills to `.publish-denylist` rather than naming them here.

## Repo format (follow exactly)

- Each skill is a self-contained folder: `skills/<skill-name>/`
  - `SKILL.md` — YAML frontmatter with `name` and `description`, then the instructions.
    Copy verbatim from the source; do not rewrite content.
  - Optional subfolders copied as-is: `references/`, `assets/`, `scripts/`.
- `README.md` — every skill must appear exactly once as a bullet under a `###` category
  heading, in the style: `- **skill-name** — lowercase one-line summary`.
  Fit new skills into existing categories (Code Quality & Testing, UX & Product Testing,
  Documentation, Content, Prompting & Workflow); create a new `###` category only when
  nothing fits (e.g. "Design & Visuals", "Productivity"). Base the one-liner on the skill's frontmatter description, compressed.

## Sync procedure

1. **Enumerate** skill folder names from both sources; apply exclusions.
2. **Diff** against `ls /Users/cursivemedia/skills/skills/`.
3. **Confirm every new skill, one at a time.** Never batch, never assume, never infer
   from the skill's contents that it is meant to be public. Publishing is the user's
   decision and only the user's. For each skill not already in the repo, show its name
   and one-line description and ask whether it should be published. Default is NO — if
   the user does not clearly say yes to that specific skill, it is not added. This holds
   however small the list is, however obviously "safe" a skill looks, and however clearly
   it fits an existing README category.

   Anything named in `.publish-denylist` is never offered at all — do not ask about it,
   do not add it. CI fails the build if a denylisted skill reaches `skills/`, so adding
   one breaks the repo as well as the user's trust.

   Skills that are stages of an internal business pipeline are the specific thing this
   gate exists to stop. Do not create a category to accommodate them.
4. **Copy** each missing skill folder into `skills/<name>/` preserving structure.
   - Skills already on the Mac: `cp -RL` (dereference!) on the device. Entries in
     `~/.claude/skills` are often symlinks into `~/.agents/skills/` — a plain `cp -R`
     commits dangling symlinks that resolve locally but are broken on GitHub. After
     copying, `find skills -type l` must return nothing.
   - Skills that exist only in the session cache (cloud): transfer via the device bridge.
     If no folder is connected, tar+gzip+base64 the folders in the cloud, write the
     base64 to the Mac in ≤50KB chunks with Desktop Commander
     (`cat >> /tmp/skillsync.b64 <<'EOF' ...`), then
     `base64 -d -i /tmp/skillsync.b64 | tar xz -C /Users/cursivemedia/skills/skills/` and
     verify file counts match the source.
5. **Existing-but-changed skills**: if a repo skill's `SKILL.md` differs from the source
   copy (diff them), do NOT silently overwrite — list the changed skills in the report and
   update only if the user approves (or if the session was told in advance to take source
   as truth).
6. **README**: add one bullet per new skill per the format rules above.
7. **Secrets & sensitive-data scan (MANDATORY before any commit)** — the repo is public:
   - Scan every file being added for real credential patterns (`sk-`, `sk-ant-`, `ghp_`,
     `github_pat_`, `xox[bap]-`, `AKIA`, `pk_live_`/`sk_live_`, `AIza`, JWTs, `BEGIN
     PRIVATE KEY`, assignment-style `key/token/secret/password = "<value>"`).
   - Also flag *business-sensitive* content: real client names, Google Sheet/Doc IDs,
     GHL location IDs, internal URLs, market research, real (non-placeholder) emails or
     phone numbers.
   - Anything flagged: exclude the skill from the sync and report it. Never push first
     and ask later.
8. **Git** (run on the Mac, in `/Users/cursivemedia/skills`):
   - `git status` first; mention any pre-existing uncommitted changes in the report.
   - `git add -A && git commit -m "Sync skills: add <names>"` (concise list or count).
   - **STOP. Do not push yet.** Show the user exactly what the commit contains (skill
     names, file count, anything notable) and ask for an explicit yes IN THE MOMENT —
     an upfront "sync my repo" request or an earlier blanket approval does NOT count as
     push approval. If the session is unattended, leave the commit local and report the
     exact `git push` command instead of pushing.
   - Only after the user's explicit OK: `git push origin main`. If push fails
     (auth/network), leave the commit local and tell the user exactly what to run.

## Verify (always)

- Every new `skills/<name>/` contains a `SKILL.md` whose frontmatter parses (has `name`
  and `description`).
- Repo skill count = old count + added count; no empty directories.
- README bullet count matches the number of skill folders.
- `git status` is clean after push (or the user was told the commit is local-only).

## Environment notes

- Running in **Cowork cloud**: reach the Mac via Desktop Commander
  (`mcp__remote-devices__desktop-commander__execute_command` etc.). The cloud shell
  cannot see `/Users/cursivemedia`; the Mac cannot see the cloud filesystem — transfer
  content explicitly (step 4).
- Running in **Claude Code on the Mac**: everything is local; skip the bridge entirely.
  The account-skills source may not be visible locally — in that case sync what is
  reachable and say which source was skipped.

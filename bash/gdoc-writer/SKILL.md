---
name: gdoc-writer
description: Publish an ad-hoc ACE deliverable (not an opp run) as a Google Doc under ACE's Drive root, Projects/<project>/.
---

# Google Doc Writer — ACE (stub over the shared `canopy gdoc` engine)

The convert → file → share → verify mechanism is canopy's shared engine; the filing standard
is `$CANOPY/agent-core/deliverables.md` (one subfolder per project, never My Drive root,
share and verify before handing over a link, link don't paste). This stub declares only
ACE's specifics.

**Not for opp runs.** A run's artifacts live under `ACE/<opp>/runs/<run>/` and are reached
through the run's ace-web page (CLAUDE.md § Conventions). This is for work outside a run,
e.g. a demo's scripts doc that people edit together.

## ACE specifics

- **Author:** `config/agent.json` (`ace@dimagi-ai.com`, client `canopy`); run from an ACE
  checkout or pass `--repo <ACE root>`.
- **Root:** `$GDRIVE_ROOT_FOLDER`, a value in ACE's Canopy vault on canopy-web, written into the
  installed plugin's `.env` by `/ace:setup --force-env`. It is NOT in the shell
  environment, so **source the `.env` in the same Bash call as the publish**, because shell
  state does not persist between calls:

  ```bash
  ACE_ENV="$HOME/.claude/plugins/data/ace-ace/.env"
  CANOPY_ROOT="$(bash "$(python3 -c "import json,os;print(json.load(open(os.path.expanduser('~/.claude/plugins/installed_plugins.json')))['plugins']['canopy@canopy'][0]['installPath'])")/scripts/canopy-runtime.sh")"
  set -a; . "$ACE_ENV"; set +a
  uv run --project "$CANOPY_ROOT" canopy gdoc publish --repo . \
    --md <file.md> --name "<Doc title>" --project "<Project>" --share none
  # iterate in place: --replace <docId>   (same link, same permissions)
  ```

- **"no Drive root resolved"** means the installed `.env` predates this key. Run
  `/ace:setup --force-env`, which keeps local-only secrets, and never paste a folder id in to
  work around it.
- **Sharing is an outbound act.** In a manual-mode turn, publish with `--share none`, then
  share the doc with named people only after the operator approves the send. Confirm each
  person appears in the permission list before you hand over the link (`gog drive
  permissions <docId> -a ace@dimagi-ai.com --client "$(canopy email client --repo .)" -j`).

## Terminology

Every string this skill puts in front of a reader follows
[`skills/_terminology.md`](../_terminology.md): **`Connect`, never `CommCare Connect`**, and
**US spelling, always** — program, enrollment, enroll, organization, behavior, center; never
programme, enrolment, organisation (owner, 2026-10-20: *"everything should be US spelling"*,
ace#3232). Identifiers (case properties, slugs, ids, config keys) keep their spelling.

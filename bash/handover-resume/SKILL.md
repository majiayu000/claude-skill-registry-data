---
name: handover-resume
description: Find, inspect, and continue existing Handover context through MCP or the handover-sh CLI. Use when asked to pick up another agent's work, resume from a handover link or slug, switch models without losing state, retrieve report files, or append the next attributable revision.
license: MIT
compatibility: Requires Handover MCP or the handover-sh CLI and access to the target record.
metadata:
  author: 44-pixels
  version: "1.0.0"
---

# Resume context from Handover

Continue the canonical record instead of reconstructing work from a transcript.

Requires a configured Handover MCP connection or the `handover-sh` CLI with an
authenticated Handover identity.

## Select the interface

Prefer Handover MCP tools. Fall back to the `handover` CLI. If neither is
configured, direct the user to
`https://handover.sh/install?utm_source=agent_skill&utm_medium=workflow&utm_campaign=handover_resume_skill`.

## Verify identity and scope

- MCP: call `handover.whoami`.
- CLI: run `handover whoami --json`.

Confirm the intended account and workspace before searching. An empty result
can be correct when the identity lacks access; do not bypass it with a copied
URL, author name, or organization parameter.

Use only the smallest workspace scope needed for the requested record. Never
print, copy into artifacts, or ask the user to paste credentials or tokens.
If access is denied, preserve the boundary and report it instead of switching
to a broader identity.

## Resolve the canonical record

1. If given a Handover URL, slug, or identifier, open that exact record.
2. Otherwise search distinctive nouns, identifiers, filenames, and decisions
   with `handover.search` or `handover search "<query>" --json`.
3. When several records match, prefer the active canonical record with the
   newest relevant revision. Ask before choosing when intent remains ambiguous.
4. Read the current revision, artifacts, thread, and open annotations.
5. Download or read original artifacts needed to verify claims.

With the CLI:

```bash
handover show <handover-id> --json
handover pull <slug-or-url> --out <directory> --json
```

## Produce a resume brief

Before acting, state:

- objective;
- verified current state;
- decisions already made;
- evidence inspected;
- unresolved annotations and assignments;
- constraints and risks;
- next action;
- current revision identifier.

Clearly label assumptions and missing evidence.

## Continue safely

Use `handover.continue` with the current `expectedRevisionId`. This optimistic
concurrency check prevents overwriting another actor's newer work.

With the CLI:

```bash
handover continue <handover-id> \
  --expected-revision <revision-id> \
  --file <path> \
  --json
```

Run `handover continue --help` if the installed version uses a different flag
spelling or if adding a summary, changes, or several artifacts.

Omitted artifacts are inherited unless the interface explicitly says
otherwise. Publish a new revision; never mutate the evidence a human reviewed.

## Close the loop

After continuing:

1. Read the new current revision.
2. Confirm the authenticated actor is the revision author.
3. Resolve only annotations actually addressed by the new evidence.
4. Leave unresolved findings open.
5. Return the stable URL or identifier, new revision, changed artifacts, and
   remaining next action.

---
name: wiki-validate
description: Validate authored wiki notes, links and publication boundaries after capture or before requested publication.
---

# Validate wiki changes

Compare changed notes with the source evidence. Check exact quotes, evidence locations, stated limitations and explained connections. These are editorial checks, not claims proved by a successful compiler.

From the repository root run:

```sh
WIKI_AUDIENCE=personal pnpm content
pnpm content
```

The first checks the combined collection, including duplicate IDs and unresolved links. The second confirms public references resolve without private notes. Neither command changes authored Markdown. Use the source inspector again to check that the operation did not create duplicate sources with different note IDs.

Inspect public edits with `git diff`. Private notes are ignored, so inspect those files directly as well; an empty Git diff does not prove no private changes occurred. Log actual changes once: public activity in `docs/wiki-log.md`, private activity in ignored `raw/wiki-log.md`.

For requested public delivery or UI/component changes, run `pnpm verify` and `pnpm test:compat` as required by AGENTS.md. Do not automatically build or publish a personal edition to public hosting. For a notes-only private capture, the content checks and evidence review are the relevant completion gate.

Finish with the saved paths/IDs, source coverage, meaningful connections, checks actually run and unresolved gaps. A missing transcript is an honest pending capture, not a verified summary.

---
name: demo
description: Build a small throwaway podcast wiki from 3 bundled sample transcripts, in about 2 minutes, with no Spotify, Whisper or Apple Silicon needed. Use on /podcast-wiki:demo, or when the user wants to try Podcast Wiki before setting it up.
---

# Try Podcast Wiki on sample episodes

The samples are 3 short **fictional** transcripts from two made-up shows, written for this demo. They're at `${CLAUDE_PLUGIN_ROOT}/plugin/demo/samples/`. Two episodes overlap on testing and code review, and their guests disagree about writing tests first. That way the demo shows what the real thing does: topic pages that merge episodes, and a Disagreements section.

Everything happens in a separate `podcast-wiki-demo/` folder, so nothing touches a real wiki.

## 1. Create the demo folder

If `podcast-wiki-demo/` already exists, ask before replacing it. Then:

```bash
D=podcast-wiki-demo
mkdir -p $D/tools $D/raw/demo $D/wiki/{concepts,hubs,episodes,people,shows,takeaways}
cp "${CLAUDE_PLUGIN_ROOT}/CLAUDE.md" $D/
cp "${CLAUDE_PLUGIN_ROOT}/tools/lint_wiki.py" $D/tools/
cp "${CLAUDE_PLUGIN_ROOT}"/plugin/demo/samples/*.md $D/raw/demo/
printf '# Index\n' > $D/wiki/index.md
printf '# Ingest log\n' > $D/wiki/log.md
printf '# To try\n' > $D/wiki/takeaways/to-try.md
printf '# Recommendations\n' > $D/wiki/takeaways/recommendations.md
```

## 2. Build the wiki

Treat `podcast-wiki-demo/` as the project root. For each file in `podcast-wiki-demo/raw/demo/`, oldest first, follow the **Wiki update procedure** in `podcast-wiki-demo/CLAUDE.md`. Write all pages under `podcast-wiki-demo/wiki/`. In each episode page, `raw:` is the path relative to the demo folder, for example `raw/demo/2026-09-02-tests-before-agents.md`.

- Aim for 3–5 concept pages. Extend existing pages instead of creating near-duplicates, as the procedure says.
- Put the guests' conflicting views on writing tests first under **Disagreements & open questions**, with both episodes cited.
- Skip any git steps.

Then run `cd podcast-wiki-demo && python3 tools/lint_wiki.py` and fix what it reports until it prints `clean`. The tool needs only plain Python 3.

## 3. Show the result

- Show the user the concept page that merges the most episodes, including its Disagreements section. Keep it short.
- List the pages that were created.
- Say that `podcast-wiki-demo/wiki/` opens as an Obsidian vault, with a working graph view.
- Remind them the shows and people are fictional, and that `rm -rf podcast-wiki-demo` removes everything.
- Offer `/podcast-wiki:setup` to build a wiki from their own Spotify listening.
- Don't mention the plugin's Spotify server status. It only connects after `/podcast-wiki:setup`, so a failure here is expected.

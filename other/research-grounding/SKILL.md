---
name: research-grounding
description: Use when answering ANY non-trivial question or doing research in this project — ground the answer in current external sources (web state-of-the-art, GitHub prior art, official docs) instead of memory, THEN go beyond the existing to find improvements and out-of-the-box approaches. A UserPromptSubmit hook reinforces this on every prompt.
---

# Research Grounding

Goal: **answer from current reality, not stale memory — then improve on it.** Before giving a
non-trivial or technical answer — especially anything about libraries, tools, versions, APIs,
best practices, or "how do people do X" — consult external sources, let them shape the answer,
and then push past the existing: find improvements and out-of-the-box approaches rather than
just replicating prior art.

## The workflow

1. **State of the art (web)** — `WebSearch` for recent (2025–2026) best practices and
   comparisons; `WebFetch` to read the authoritative page. Search before claiming "X is the
   standard."
2. **Prior art (GitHub)** — use `scripts/ghx.sh` (= mise `gh` + rtk) to look at existing
   implementations, popular libraries, their licenses, activity, and how the original
   `bishopfox/unredacter` solved a problem. `gh search repos/code`, `gh api`.
3. **Official docs** — the `microsoft-docs` MCP for Microsoft/Azure/.NET; `claude-code-guide`
   for Claude Code/SDK/API questions; vendor docs via `WebFetch`. Verify signatures/versions
   rather than guessing.
4. **Deep questions** — for broad, multi-source questions, invoke the `deep-research` skill.
5. **Go beyond the existing (improve & innovate)** — once you understand the state of the art,
   don't stop at replicating it:
   - **Critique** it — what are its limitations, costs, or outdated assumptions?
   - **Improve** — is there a newer/faster/simpler/cheaper approach, a better library, or a way
     to combine ideas? Look for what the common solution misses.
   - **Out-of-the-box** — consider novel/unconventional approaches (a different algorithm, a
     different data representation, a tool from an adjacent domain) that could surpass prior art.
   - Recommend the **best** approach for the goal — even if it isn't the most common — and say
     why it beats the standard one.

## How to apply

- Prefer up-to-date primary sources over training memory; if memory and a current source
  disagree, trust the source and say so.
- Compare ≥2 alternatives for any tool/library/approach choice, with the trade-off and a
  recommendation — and ask whether an improved or out-of-the-box option beats them all.
- **Cite** what you used (URLs / repos) so the answer is verifiable.
- Pin versions and check release dates — the ecosystem moves fast.
- **Calibrate**: skip the research for trivial or mechanical asks (rename, format, "run the
  tests"); spend it where a wrong/stale answer would cost real time.

## Notes

- This is how every recent decision here was made (gitleaks vs trufflehog, govulncheck/gosec,
  syft/grype, mise backends, GPL-3.0 license check) — confirm with sources, then act.
- Tools available: `WebSearch`, `WebFetch`, `scripts/ghx.sh`/`gh`, the microsoft-docs MCP,
  `claude-code-guide`, and the `deep-research` skill.

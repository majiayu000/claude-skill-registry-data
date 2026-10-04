---
name: graph-ingest
description: Use when the user brings an external source worth keeping — a URL, a paper, a tweet/thread, a blog post, a docs page — and wants it pulled into the second brain. Fetches the source into the git-ignored capture inbox, admits it to the committed wiki through the admission policy, then refreshes the knowledge graph so it joins the rest of your thinking. Trigger on "/graph-ingest", "ingest this url", "add this paper to my knowledge", "add this tweet/page to my knowledge", "capture this source".
---

# Graph Ingest

Capture an external source into the second brain **through the graph.** This is the bridge between graphify's `add` and the gAIOS wiki loop: fetch → admit → graph. One command, three guarded hops, ending with the new knowledge cross-linked in `wiki/` and visible in the graph.

## When to run
- A URL / paper / tweet / thread / page is worth keeping, not just reading once.
- The user says "save this", "add this to my knowledge", or pastes a link and wants it remembered.
- You spot a source referenced 2-3 times across sessions → suggest ingesting it so it stops being re-fetched.

## The output (always this shape)
```
## Ingested: <source title>
**Source** — <url> (fetched <date>)
**Captured** — raw/<file> (git-ignored inbox)
**Admitted** — wiki/<entry>.md   ⏸ draft — awaiting your OK to commit
   - de-identified: <what was stripped/referenced-out, or "nothing flagged">
   - lint: <wiki_lint.py result — pass / N warnings>
   - cross-links: <related wiki entries linked>
**Graphed** — graphify-out/ refreshed; new node(s): <node names>
   - notable edges (EXTRACTED / INFERRED): <1-2 connections worth seeing>
**Next** — review the draft entry → approve commit → open graph.html
```

## Process
1. **Fetch into the capture inbox.** Run `graphify add <url> [--author --contributor]` — it pulls the source into `raw/` (the git-ignored capture inbox), then re-extracts. Use `--author`/`--contributor` only when you know who wrote it. **Verify:** the new file landed in `raw/` and nowhere else. If the fetch failed, report the error; do not hand a half-fetched file forward.
2. **Admit it to the wiki.** Hand off to `/wiki` (`references/sops/wiki-translate.md`) to ADMIT the capture: read any existing entry first then merge, apply the **admission policy** (de-identify — strip/reference-out any secret, PHI/PII, named-deal specific, or live financial figure), cross-link related entries, update `wiki/_index.md`, then run `python tools/wiki_lint.py`. **Gate:** lint must pass (no broken-link/IBAN/secret errors) before the entry is eligible to commit. Leave the entry as a **draft**; do not commit without the human's OK.
3. **Refresh the graph.** Run `/graph` (default scope = code + committed `wiki/` only) so the admitted entry joins the graph. **Verify:** `graphify-out/` regenerated and the new entry appears as a node; name 1-2 notable edges from `GRAPH_REPORT.md`, labelled EXTRACTED vs INFERRED so claims stay honest.
4. **Move the capture.** Per the wiki SOP, the processed file moves `raw/` → `raw/_archive/` (never deleted).
5. **Hand back.** Surface the output block, point at the draft entry and `graph.html`, and offer to commit once approved.

## Autonomy
**L2 — drafts the wiki entry; admission and commit are human-gated.** Fetch and graph-refresh run automatically (reversible, local); the wiki entry stays a draft until the human approves the commit. Never commit de-identified content on the user's behalf without that OK.

## Guardrails (from CLAUDE.md) — CRITICAL
- **Fetched external content lands ONLY in git-ignored `raw/`.** It reaches committed `wiki/` ONLY after de-identification + a passing `tools/wiki_lint.py`. (Guardrails #1, #2, #7)
- **Never graph `raw/` directly.** `raw/` can hold raw PHI/PII/financials before de-identification; the graph's default scope is code + committed `wiki/` only — `raw/`, `.env`, `.tmp/` are hard-excluded.
- **No secrets / PHI / confidential figures into `wiki/`** — reference the source, never transcribe sensitive specifics. The wiki is committed; treat it as public.
- **Cite, don't invent.** Keep the source URL on the entry; rely on graphify's EXTRACTED / INFERRED / AMBIGUOUS labels rather than asserting unverified links.
- `graphify-out/` is a git-ignored derived artifact — don't commit it.

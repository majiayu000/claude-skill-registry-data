---
name: knowledge-gravity-lab
description: Analyze folders of Markdown/text research notes, Obsidian vaults, paper cards, invention notes, or memory exports as a practical knowledge map. Use when asked to find center topics, noisy or low-signal notes, possible contamination, overgrown topic groups, orphan notes, cleanup actions, or a useful public knowledge-hygiene workflow.
---

# Knowledge Gravity Lab

Use this skill to turn a messy folder of notes into a practical knowledge map:

- center notes and themes,
- possible contamination/noise,
- overgrown topic clusters,
- orphan notes,
- cleanup actions,
- research or invention follow-up candidates.

This is a practical public knowledge-hygiene workflow, not a patent filing package and not a legal freedom-to-operate opinion. Keep the implementation framed as heuristic note analysis and avoid claiming that it implements or bypasses any protected system.

## Quick Start

Run the bundled analyzer on a folder of Markdown/text files:

```powershell
python scripts/analyze_corpus.py --input "C:\path\to\vault" --output "D:\knowledge-gravity-output"
```

Optional: skip folders that should not affect the map.

```powershell
python scripts/analyze_corpus.py --input "C:\path\to\vault" --output "D:\knowledge-gravity-output" --skip-dir "archive" --skip-dir "templates"
```

The script creates:

- `knowledge_gravity_nodes.csv`
- `knowledge_gravity_edges.csv`
- `knowledge_gravity_report.md`
- `knowledge_gravity_action_sheet.md`
- `knowledge_gravity_data.json`

Then summarize the report and action sheet for the user, focusing on 3-5 concrete cleanup or research actions.

## Output Quality Checks

After running the analyzer, check whether the output is useful:

- If one topic group contains most notes, tell the user the corpus needs stronger subtopic links/tags.
- If the review queue is mostly templates or daily notes, suggest adding `--skip-dir` or excluding low-value folders.
- If the center notes are all index files, explain that the map is showing navigation hubs rather than content hubs.
- If there are fewer than 20 notes, frame the result as a smoke test.

## Workflow

1. Identify the corpus folder.
2. Run `scripts/analyze_corpus.py`.
3. Read `knowledge_gravity_report.md`.
4. Read `knowledge_gravity_action_sheet.md` when cleanup actions are requested.
5. Explain:
   - what the knowledge center is,
   - what looks noisy or low-signal,
   - what clusters are too large,
   - what should be split, merged, archived, or reviewed.
6. If the user wants publication, read `references/public-boundary.md` and avoid legal or protected-system claims.
7. If the user asks whether this collides with existing rights, read `references/existing-rights-check.md` and frame the answer as a risk checklist, not legal advice.

## Interpretation Rules

Treat the analyzer output as decision support, not ground truth.

- High center score means a note is central in the local corpus.
- Review score means a note needs human attention, not that it is false.
- The action sheet is a temporary cleanup workspace. It should make cleanup choices easy, not replace human judgment.
- The 80-point feedback loop is an organization heuristic based on links, tags, headings, size, and repository share. Scores are capped to a practical 15-100 range; 80 is a cleanup target, not a natural breakpoint.
- Noise/contamination candidates are items with weak text signal, suspicious names, excessive boilerplate, poor linkage, or signs that they should not be trusted as a core source yet.
- Overgrown clusters are candidates for splitting into subtopics.
- Orphans are candidates for linking, archiving, or merging.

## Public-Safe Language

Prefer:

- "knowledge hygiene"
- "center topic"
- "topic gravity"
- "attention-weighted note map"
- "possible noise"
- "possible contamination"
- "review queue"

Avoid:

- legal conclusions about existing rights,
- statements that the skill implements a protected internal system,
- "protected mechanism proves...",
- "guaranteed detection",
- "hallucination-proof".

## When Results Are Weak

Say so directly. A useful result may be:

- "The corpus is too small."
- "The clusters are too clean to stress the method."
- "This proves only smoke-test scalability."
- "This needs baseline comparison."

Then propose the next experiment or corpus improvement.

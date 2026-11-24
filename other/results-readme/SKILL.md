---
name: "results-readme"
description: "Use when writing or editing a game README, choosing a worked example, or checking a result quoted in the root index."
---

# Results README

Start with a question someone could ask while playing. Look for a move or comparison already on the page that answers it. In Spot It, counting the symbol seen six times tells you what the two missing cards share. Keep the rule, opponent or information that makes the answer true.

## What goes on the page

- A single result can fit in a sentence with its evidence. Use a table when readers need to compare several results. Say which numbers were proved, checked case by case, computed exactly, observed, simulated or taken from a source.
- Give enough of the rules to replay the example. If two readings change the outcome, show the move where they part.
- Say what the check compared and what agreed. For a simulation, give the sample size, seed and interval. For recorded games, name the dataset and count the games that met the condition.
- Put a command near the question it answers. Link to a longer proof, the experiment plan or the notes in `results/` where the reader needs them. Credit published results and record the sources and licenses of data you use.
- Leave an open question where the evidence runs out. The nine-card deal in Egyptian Ratscrew goes on forever. Whether a full deck can do that is open.

Give each paper-only count a producer and read its output in the paper. For a strategy, state the move order, how ties are resolved and which deals enter the denominator. A policy’s loss rate and the frequency of that policy among people answer different questions.

## Shared with the paper

A block marked `<!-- shared:name -->` comes from `<game>/docs/name.md`. Edit that file.
Run `uv run tools/sync_docs.py <game>` to fill the block with the numbers in `results.json`.
The paper reads the filled README. See `typst-paper-pipeline` to rebuild both editions.

## Pictures and demonstrations

Draw a board, route or hand when its arrangement explains the result. Put it beside the sentence that uses it and say what to look for. Two totals can stay in the sentence.

- **Demonstrate tools with a transcript.** A short code block of a real run beats a screenshot, because it is searchable, readable on a phone and checkable. A test can run the same command and compare.
- **Format:**
  - SVG for drawings and line plots, PNG only for dense plots.
  - About 800 px wide or less.
  - A white background, so the image stays readable in GitHub's dark mode.
  - Alt text that says what the picture shows.
- **Reproducible:**
  - Each image is written by a script in the game's folder, with fixed seeds.
  - Matplotlib SVGs set `svg.hashsalt` and drop the date metadata, so the bytes are stable.
  - A test checks that the committed file is what the script writes, or the CI figure check covers it.
- **Copyright:**
  - No card art, box art, sprites or screenshots of commercial games.
  - Draw generic boards and cards. Use the game's words or numbers only where the rules need them.
  - A real person's photo never goes in a file.

## Length

- Aim under about 2,500 words. Past that, the opening summary is mandatory. Move experiment detail, long tables and derivations into `results/` notes or a paper, and link them.
- One heading per question; a README with one heading over 3,000 words is a lab notebook, not a write-up.

## Wording

- Numbers in the text match the files the scripts write; a test checks the quoted ones.
- Say "best found" unless optimality is proved, and name who proved it if it is a cited result.
- Report nulls with intervals and the same care as positive results: "no measurable effect (−0.02 to 0.04)", never "did not work".
- Distinguish what was reproduced from what was only read; "the paper reports" versus "recomputed here".
- `readcost check README.md` passes; American spelling; no names except cited authors.

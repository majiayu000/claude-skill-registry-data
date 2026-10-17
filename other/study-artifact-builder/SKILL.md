---
name: study-artifact-builder
version: 1.0.0
description: Build a single-file interactive HTML artifact to study a paper's pipeline or dataset until it can be defended from memory — source pinning, paper-versus-code separation, per-component notes, ablation toggles, detailed SVG diagram, verification. Use when asked to study, compare, or memorize a method, pipeline, benchmark or dataset, or to turn a diagram into an artifact.
---

# Study Artifact Builder

Turns a paper, its code and its numbers into one interactive HTML file you can study from. The goal is not a prettier diagram. The goal is that every claim in the file is traceable to a source, every number is checked, and the person using it can answer "what is the single most important result" without opening the paper.

Two dedicated guides carry the domain detail: [PIPELINES.md](PIPELINES.md) for methods and workflows, [DATASETS.md](DATASETS.md) for benchmarks and corpora. Reusable code skeletons are in [RECIPES.md](RECIPES.md).

## 1. The rules that override everything

1. **Pin the sources first.** Record the paper version (for example arXiv v2), the code commit or tag, and the config files you read. A claim without a pinned source does not enter the artifact.
2. **Numbers come from the source, never from memory or a search snippet.** Fetch the paper's HTML or PDF text and extract the table programmatically. Search snippets truncate table cells; a truncated row is a wrong row.
3. **Paper and code are separate witnesses.** They disagree more often than expected (stage order, caps, defaults, dead code). Never write "the system does X" without saying which witness says so.
4. **Label what you did not verify.** An explicit "not verified" chip is worth more than a confident guess. Every claim about code behavior must come from a function you read, not from a file name.
5. **Notes live beside components, not inside them.** A component box holds what the component is. What the paper says, what the code does, and what does not match each get their own block.

## 2. Interview before building

Ask these, in order, and wait for each answer. Skip a question only when the user already stated it.

1. **Goal.** Memorize, defend, replicate, compare two methods, or implement. This decides the focus ([§3](#3-choose-the-focus)).
2. **Subject.** Pipeline, dataset, or both. Which paper, which code, which version.
3. **Witnesses.** Paper only, or paper plus code. If code, which repository and which config is the default one.
4. **Depth.** One screen of the essentials, or every component with its parameters.
5. **Language and audience.** The artifact's language follows the user, with the paper's terms kept in their original language.

## 3. Choose the focus

| Goal | Lead with | Put prominently | Cut |
|---|---|---|---|
| Memorize | Ranked results, the numbers asked in a defense | A "know by heart" box, a ranking with deltas | Config minutiae |
| Defend | Threats to validity, overlap and leakage, noise | Discrepancy blocks, "what the number does not show" | Implementation detail |
| Replicate | Parameters, caps, defaults, flags, environment | A table of every knob with its source and value | Narrative |
| Compare | Side-by-side by concern | One row per concern, same vocabulary on both sides | Per-method deep dives |
| Implement | Interfaces between stages, data shapes | Inputs and outputs per component | Result tables |

State the chosen focus at the top of the artifact in one sentence. If the user gave several goals, pick the first as the lead and mention the others as secondary.

## 4. Build order

1. **Inventory components.** One row per stage, store, loop or filter, from the paper's own figure and method section. Use the paper's names.
2. **Read the code per component.** Find the function that implements it. Record file and line, defaults, and any flag that disables it.
3. **Extract results.** Programmatically, into a structure, never retyped. Compute derived values (means, relative changes) in code and compare with the paper's own text.
4. **Cross-check.** Recompute at least two numbers by hand. Verify claims such as "reduces by 72.8 to 86.9%" against the table.
5. **Write the notes.** Three blocks per component: paper, code, discrepancies and gaps ([§1 rule 5](#1-the-rules-that-override-everything)).
6. **Build the diagram** ([§5](#5-diagram-rules)), then the results views, then the "know by heart" box last, once the numbers are final.
7. **Verify** ([§7](#7-verify-before-handing-over)).

## 5. Diagram rules

- **One lane per stage, in the paper's order.** If the code order differs, keep the paper's order and flag the difference on the stage.
- **Show data flows, not only control flow.** Color the flows by what they carry (task, plan, retrieved examples, recommendations, diagnostics). It is the fastest way to see what reaches the final prompt.
- **Stores are nodes.** Knowledge bases, indexes and corpora are separate boxes with a dashed link to the stage that reads them, labeled with what they hold.
- **Loops show their cap and its unit.** "Up to 3 compile calls" is a statement; "3 iterations" is ambiguous. Show what happens at the last iteration.
- **Code-only components are dashed and apart.** Features that exist in code but not in the paper must not look like part of the method.
- **Ablations attach to the stage.** Each stage shows its mean effect and rank, and a toggle dims it and shows the per-benchmark numbers.
- **Failure taxonomies attach to the stage the paper credits.** Say that it is the paper's attribution when no per-component measurement backs it.
- **Click selects, the detail panel sits directly under the diagram.** Do not make the reader scroll to find the notes.

Skeleton and helpers in [RECIPES.md](RECIPES.md).

## 6. Result presentation

- **Relative versus absolute.** State which one the paper uses. A drop of "35%" may be 32 points. Show the base value next to each delta.
- **Rank by a defined statistic** and say which columns enter it. Show the per-benchmark maximum too, since the ranking can flip by benchmark.
- **Show sample size where it limits the claim.** With few tasks, one task is a large step; say so next to the table.
- **Flag anomalies** instead of smoothing them: identical cells in different rows, a metric that improves when a component is removed, a category that gets worse.
- **Separate the paper's explanation from its measurement.** An error-type table comparing the full system to a baseline does not measure per-component effects.

## 7. Verify before handing over

1. Render headless and check for script errors.
2. Click through one interaction per control (select a node, toggle an ablation, switch a metric) and assert the DOM changed.
3. Look at the screenshot. Clipped lanes, text overflowing boxes, labels crossing arrows and legends that do not match the colors are common and cheap to fix.
4. Re-read the numbers in the "know by heart" box against the source table, not against your own earlier text.

Commands in [RECIPES.md](RECIPES.md#5-headless-verification).

## 8. Failure modes to watch

| Symptom | Cause | Guard |
|---|---|---|
| A number that matches nothing | Taken from a snippet or from memory | Extract from the source table |
| "The system does X" with no witness | Paper and code conflated | Three-block notes per component |
| A cap that is "3" and "5" in different places | Different defaults per language or config | List every config with its value |
| Rank flips between benchmarks | A mean hides the per-benchmark story | Show mean and per-benchmark max |
| A diagram nobody can defend | Components with no source | Source locator on every component |
| Retrieval looks decisive | The corpus overlaps the benchmark | See [DATASETS.md](DATASETS.md) leakage section |

## 9. Delivery

- One self-contained file: no network, no build step, light and dark mode, readable at 1280 px and scrollable below.
- Name it with the date and a slug, next to the project's other design docs.
- Do not name private projects in a published copy of the file; the artifact for a specific project belongs to that project.
- End the hand-over with what was not verified, so the user knows where the file is weakest.

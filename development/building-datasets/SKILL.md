---
name: building-datasets
description: "Builds AQVEN datasets that can answer the question: source labels, synthetic cases with known answers, negatives and holdout from one population, tag counts per split. Use when editing datasets/, before filtering by tags, and when asked what a claim rests on."
---

## MUST

- Correctness is measured only against ground truth: an answer known by construction, or labels from the source.
  Labels a model produced are predictions, not truth: model tags stay auxiliary and are marked as such.
- Negatives and holdout come from the same population as the positives and `dev`.
- Labels never come from a rule the agent made up. A table that derives labels from expert knowledge (a
  contract clause type mapped to a risk level) is marked "needs sign-off by a specialist".
- `expected_output` uses the project's own types: source labels are mapped at build time and validated through
  the generated classes; the raw label stays in `metadata`.
- Builders live in `scripts/` from the first line, never in `/tmp` or a scratchpad (`building-flows`). Before a bulk
  download, tell the owner its volume and wait for a yes; raw downloads stay outside the package (`data/raw/` at
  the project root, git-ignored), and only the vetted subset enters `samples/`.
- A case points at its media with `file:`, a file in the project; private files stay out of git.
- Never rename a case an experiment used: the split hashes the package, the dataset id and the case `name`, so a
  renamed case, or the same input in another dataset, is a new draw. An input seen on `dev` in any dataset is
  spent for holdout everywhere.

## Procedure

| # | Step | Exit criterion |
|---|---|---|
| 1 | The question, the unit (what one case is) and the production input contract: the fields and input kinds the flow receives at run time | a question sentence and the unit; a column production lacks goes to `metadata`, never to `inputs`, however predictive |
| 2 | Sources, in order: the project's labelled data, public labelled datasets, synthetic cases with truth by construction, each input checked to have the property its label names (`preparing-media-inputs`, synthetic inputs). A public source: fetch its label and metadata tables first, count the usable population, state the media volume to the owner before any download | the licence text read (its name, whether this use is allowed, attribution); the owner's yes before a bulk download |
| 3 | Vet and profile the source: fill rate per field and stratum; label provenance (a verified outcome, an expert reading of the same input, self-report, machine-made) with rater count and agreement; category granularity against the unit; the licence of embedded content (logos, watermarks, quoted text); near-duplicates and augmentations; whether the population is production's (staged catalogue shots against user uploads, studio audio against phone calls, boilerplate copies in scraped pages, generated rows in a table); transcoding and resizing artefacts | a profile table shown to the owner, with what the source can and cannot support |
| 4 | Layout: raw downloads in `data/raw/`, the vetted subset in `<package>/samples/<dataset_id>/`, media the cases point at in `<package>/datasets/<dataset_id>/`, the builder `scripts/build_<dataset_id>.py` at the project root next to `pyproject.toml` (outside the package, so the loader never reads it). Before it writes a case, the builder drops exact copies (by content hash) and the near-duplicates step 3 found; it skips files it already has, logs to a file, and writes canonical YAML with the `canonical_writer()` of `references/engine/snippets.md` (A dataset with tags). A long build runs in the background, unpiped, never through `head` or `tail` | the dataset rebuilds with `uv run python scripts/build_<dataset_id>.py`; `aqven_check` clean |
| 5 | Media: `{$media: "<type>", file: "<file>"}`, such as `{$media: "audio/wav", file: "call_0412.wav"}` or `{$media: "application/pdf", file: "invoice_17.pdf"}`, with the file in `datasets/<dataset_id>/`, or `file: "@root/<path>"` for a file several datasets share. No `size_bytes`; `name` defaults to the file name. `blob_id` values still work (a case saved from a run has them); `uv run aqven datasets materialize <package> [<dataset_id>…]` turns them into files. Private data (people in images, audio or video, customer documents, personal rows of a table): ask the owner, then a `.gitignore` line on `datasets/<dataset_id>/` or Git LFS | every media value names a file in the project; `aqven_check` shows no `E_MEDIA_FILE_MISSING`, `E_MEDIA_PATH_INVALID` or `W_MEDIA_TYPE_MISMATCH` |
| 6 | Labels: source labels mapped into the project's types at build time (validated with the classes of `<package>/types.py`, the raw label in `metadata`), labels agreed with the owner, or a documented table marked "needs sign-off by a specialist". A derived table has an origin column (source, owner, agent) and lists the entries the agent made or tuned for sign-off; categories that stay indistinguishable are reported, not forced apart; truth for one property inferred from a label of another is named "proxy" and marked for sign-off | the origin of every label is named; agent-made entries listed for the owner |
| 7 | Negatives and holdout from the same population as positives and `dev`. The best negative mirrors a positive and differs only in what is asked, as Lumen's `planted_defect_replies` pairs every clean reply with a twin carrying one planted defect | no control "from another world"; `dev` and `holdout` look alike |
| 8 | Tags are the risk axes; every tag value the question compares is its own stratum; optional inputs are an explicit `null` | `aqven_check` clean |
| 9 | Count tag value × split before a series (50/50 by a hash of the package, the dataset id and the case `name`): every compared group has at least k cases in each half; a graded series (levels of one property) gets twice the cases per level. Coverage: property × has positives × has true negatives, since false positives are measured only for a property labelled both ways. Keep one dataset per set of inputs: a second dataset over the same inputs splits them anew, so an input on `dev` in either is spent in both | the tables shown to the owner, with what the dataset can and cannot confirm |
| 10 | Open a few inputs of every group: read, listen, watch. A coarse source tag does not guarantee the input shows it: a "billing" thread that opens about delivery, a clip tagged with an event that happens off-screen | each group matches its tag |

A dataset is `datasets/<dataset_id>.yaml` with `apiVersion`, `kind: "Dataset"`, `flow` (or none for a local flow
of an experiment) and `cases`; a case has `name`, `inputs`, and optionally `tags`, `expected_output`, `context`,
`node_outputs` (for runs over a node range) and `metadata`. A media input is `$media` plus either `file`
(relative to `datasets/<dataset_id>/`, or `@root/<path>` from the package root; no absolute path, `..` or
`.aqven/`) or `blob_id`, never both. A single case runs with MCP `run_start` and
`dataset_item_id: "<dataset_id>/<case_name>"`. A series with `--cases N` takes the first N cases of the chosen
half in file order.

## Pitfalls

A pitfall is a general rule; the illustration after it is one instance.

| What goes wrong | Do instead |
|---|---|
| Media imported through an improvised route; sources and builders left in `/tmp` | media as `file:` next to the dataset, sources in `samples/`, a builder in `scripts/` |
| Media held only as `blob_id`: the bytes lived in one machine's `.aqven/blobs/`, and a fresh clone had none | `file:` references; `aqven datasets materialize` for old cases |
| Private media committed with the dataset: customer call recordings pushed to a shared repository | a `.gitignore` line on `datasets/<dataset_id>/` or Git LFS, agreed with the owner |
| A public labelled dataset put off until the owner asked twice | labelled data first |
| Paid model labelling proposed because the source's labels looked incomplete | source labels; model tags only as auxiliary, marked |
| A bulk download started before the label tables were read, and most files had no usable label | label and metadata tables first, the population counted, the owner's yes before the download |
| A licence judged by its name; its text forbade the intended use | read the licence text |
| Labels invented from the agent's own rule | source labels, or a signed-off table |
| A derived table tuned until the categories separated, with no mark of the entries the agent invented | an origin column; agent-made entries listed for sign-off |
| `expected_output` copied from a CSV's `status` column ("Refund - partial"), so no value matched the flow's enum | map to the project's types at build time; the raw label in `metadata` |
| A column only the dataset has (the team a ticket was finally routed to) became a model input | inputs follow the production input contract; the rest is `metadata` |
| A false-positive rate claimed for topics no meeting recording was labelled as lacking | the coverage table: a property needs cases labelled with it and without it |
| Negatives from another population: every negative came from one internal mailbox, every positive from the public channel, so the model separated channels, not classes | negatives from the same source, channel and length as the positives |
| Duplicates under different names leaked between `dev` and holdout: a ticket exported twice, a product shot saved again at a smaller size | drop exact copies by content hash and the near-duplicates the profile found, before any case is written |
| A second dataset built from the same inputs got its own split, and a third of its holdout had been seen on `dev` | one dataset per set of inputs; an input seen on `dev` is spent |
| The split thinned a graded series: some levels landed in one half only, and a series asked for more cases than its half held ran fewer | twice the cases per level; count before the series |
| A compared group of one: the only non-English ticket landed in `dev` | at least k cases per compared tag value in each half |
| A new kind of case added only before the confirmation series (long multi-intent messages): `dev` and `holdout` scores diverged | one population for both; add, then explore again on `dev` |
| A raw archive unpacked into the package: unvetted files sat next to the cases, and its `.md`, `.yaml` and `.py` files were checked as project files | raw files in `data/raw/` outside the package; only the vetted subset in `samples/` |
| A background builder piped through `head` died halfway, and the rerun started from zero | a log file, and a builder that skips what it already has |
| YAML dumped with aliases: dozens of `E_YAML_ANCHOR` | `canonical_writer()` in the builder |
| A good pattern: the owner proposed a mapping ("error code → refund category"), the agent derived labels by that table and marked it for sign-off | do the same |

## Tools and commands

- `aqven` MCP `aqven_check`; `run_start` with `mode: "live"` and `dataset_item_id`; `series_start` with `look`
  (`flow_id`, `dataset_id`, `case_names`) to run named cases once.
- `uv run python scripts/build_<dataset_id>.py`; a long one in the background, its output in a log file.
- `uv run aqven generate <package>`: the classes in `<package>/types.py` that validate `expected_output`.
- `uv run aqven datasets materialize <package> [<dataset_id>…]` (`--dry-run` first): `blob_id` values into files
  in `datasets/<dataset_id>/`; a blob missing from the local store is named, its value kept, and the exit code is 1.

## References

- `references/concepts/case-construction.md`: the question and the unit, vetting a public source, label origin
  and proxy truth, negative controls, the split, coverage, raw and curated storage. Read before step 2.
- `references/reference/datasets.md`: every key of a dataset and a case. Read before writing a dataset file.
- `references/engine/snippets.md`: A dataset with tags, a tested builder with `canonical_writer()`. Read at step 4.
- `references/engine/dataset-media-files.md`: `file:` references, the two path forms, private files,
  `materialize`, the three media diagnostics. Read at step 5.
- `references/studio/cases.md`: the owner's view of cases, filters and imports. Read at step 5.
- `references/engine/experiments.md`: how an experiment selects cases by tags. Read at step 8.
- `references/mcp-cli/experiments-and-series.md`: the split, `look` with `case_names`, what `include_cases`
  shows. Read at step 9.

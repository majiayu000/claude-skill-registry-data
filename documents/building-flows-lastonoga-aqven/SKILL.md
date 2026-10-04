---
name: building-flows
description: "Writes AQVEN flows: node kinds, flat layout, prompt levels and variants, map and parallel, call slots, code steps, prompt_preview, flow_patch. Use before changing, renaming or removing files in flows/ or experiments/<id>/{nodes,prompts,flows}/, and on aqven check errors there."
---

## MUST

- Never `rm`, `mv`, `cp -r` or one regex over several project files. Adding, removing, renaming or moving a
  node, renaming a flow or an agent and deleting an agent go through MCP `flow_patch`.
- A hand-written file: Edit or Write, one file per call. Generated files (types, agents, datasets, fragments,
  prompts) come from a committed builder `scripts/build_<what>.py` at the project root, run with `uv run python`;
  it removes an output it no longer writes only after `uv run aqven refs` finds no reference to it. Never
  generate project files from `/tmp`, a scratchpad or a heredoc.
- `flow_patch` cannot delete a flow: remove an empty flow folder with one `rm -r flows/<flow_id>` only after
  `uv run aqven refs flow:<flow_id> <package>` finds no reference. In an experiment folder, delete one file with
  one `rm <file>` only after `aqven check` names it in `W_ALTERNATIVE_UNUSED`.
- The project flow stays flat: every step is visible in one `flow.yaml`. A `call` slot for comparing designs
  lives in a local flow of an experiment and leaves with the experiment.
- A shape you propose is an option, never the answer: say when it fits and which experiment would decide it.
- After changing a prompt, a fragment, a variant slot, an inference or a type, read the `prompt_preview` of every
  changed llm node in full.
- No comments and no docstrings in step and check code, and never a docstring moved into a `#` line above `def`.

## Procedure

| # | Step | Exit criterion |
|---|---|---|
| 1 | Read `FINDINGS.md`, `EXPERIMENTS.md`, `uv run aqven tree <package>`, `references/concepts/ten-kinds-of-nodes.md` and `references/concepts/three-prompt-levels.md` | every step has a node kind and a reason |
| 2 | Shape: node kinds are mechanisms (`references/concepts/ten-kinds-of-nodes.md`); the shape comes from the contract and the inputs you opened, not from a habit. Offer the owner the fewest steps that express the contract's decisions and one or two alternatives, each with when it fits, when it does not and the experiment that would compare them ("Choosing a shape" below), in one question. Fixed rules: `tool` for anything that leaves the flow or touches media bytes (an API, OCR, speech-to-text, splitting a PDF or a recording, producing audio or video, all through `ctx.blobs`); an agent's own `tools` or `mcp_servers` only when the model must choose the call, with `approval` on tools that write; `code` for deterministic work on values; `human` when a person must answer inside the run; `call` only for a reused flow or a comparison slot in an experiment; no formatter nodes, the prompt template shapes text | every step has a kind and a reason the owner agreed to; alternatives not built are written down as experiments |
| 3 | Names: a node id names its role and kind (`extract_each_page`, not `gemini`); inference ids are unique across the project | ids read without opening files; no `E_ID_DUPLICATE` |
| 4 | Answer the questions of `hardening-flows` for each step | every step has an answer to "what if it fails" |
| 5 | File order: `flow.yaml` with `input`, `output` and `order` → types (`designing-output-contracts`) → agents (`choosing-models`) → nodes, inference, prompts → `returns`. Run `aqven_check` after each file. `types/` may hold subfolders (`types/enums/`, `types/records/`); builders live in `scripts/` at the project root, next to `pyproject.toml` | no `E_ORPHAN_FILE`, no `E_NODE_UNORDERED` |
| 6 | llm node: bindings in `in`; media (`Image`, `Audio`, `Video`, `Document` or a list of one) as top-level inference inputs; an inference whose output fits the model; the prompt file `<stem>.prompt.md` next to `<stem>.inference.yaml`; variable wording as a variant slot, shared static text as a fragment. A closed set of labels (ticket intents, document types, sound events, defect kinds): the value descriptions of an enum never reach the model, so the prompt defines every value by what separates it from its neighbours in this input kind; keep the definitions, the enum and its checks from drifting apart (one source table and a builder is one way). A step that gets another step's reading next to the raw input (OCR text beside the scan, a transcript beside the call) says how the two relate; which one wins on a conflict is a `prompt` factor to measure | `aqven_check` clean; every label has a definition in the preview |
| 7 | `prompt_preview` of every changed llm node: `{flow_id, node_id}` without `input` (samples come from the inference input schema) or with an input of the inference, never of the flow; force a slot with `variants: {<slot>: <case>}` (CLI `--variant <slot>=<case>`); experiment variants and local flows have no preview yet (`designing-experiments`) | no empty or literal placeholder; the count and size of attachments as intended; the text agrees with the number of attachments |
| 8 | `code` step: parameters match `in` one for one, typed with `<package>.types`; the constraints in the signature are the type's own (`Annotated`, `Field`); the return type is the generated record; new output fields also go into `returns`; the values of a generated enum (`type X = Literal[...]`) are `typing.get_args(X.__value__)`, asserted non-empty | `pyright_check` and `aqven_check` clean |
| 9 | Structure through `flow_patch`: a fresh ULID `client_op_id` per call; `expects[{path, file_hash}]` for every file the ops touch (`"sha256-"` + sha256 of the current bytes, `null` when the file must not exist); a rename also lists `aqven.yaml`, which gets the `renames` entry | the patch applied; on `STALE_FILE` read the file again and replay the intent |
| 10 | Experiment folders: an alternative is an ordinary node in `experiments/<id>/nodes/<alt>/<alt>.node.yaml` (with its `.py`, `.inference.yaml`, `.prompt.md`) with the slot's `in` and `out`; a prompt alternative is text only in `experiments/<id>/prompts/<name>.md`; a local flow is `experiments/<id>/flows/<flow_id>/` in the usual format, with an id no project flow has; a many-file experiment is written file by file with Write, or created in Studio | `aqven_check` gives no factor codes (`designing-experiments`) |
| 11 | One live run on a real input: MCP `run_start` with `mode: "live"` and `dataset_item_id: "<dataset_id>/<case_name>"` or `input`, then `run_get_node` of each llm node to see what the model received. Another project agent on an llm node without editing the flow: `agent_overrides: {<node_id>: <agent_id>}` in the same call, a run option and not a variant (`choosing-models`) | the run finished, outputs are plausible, the run view reads well |

Binding grammar: `$input.<field>`, `$<node>.out.<field>`, `[*]` over a list, `[n]` for one item. Inside a map body
`$item` and `$index`. In the `out` of a `parallel` node `$branch.<key>` (never `$branch.<key>.out`) and
`$ok[*].<field>`; a `map` or `parallel` node collects successful items with `from: "$ok"`.

A variant slot of a prompt lives in the inference, its texts in `<stem>.variants/<slot>/<case>.md`:

```yaml
variants:
  lamp_guide:
    on: "product.lamp_kind"
    cases:
      mains: "mains"
      rechargeable: "rechargeable"
    default: "unknown"
```

The Liquid prompt prints it with `{{ variants.lamp_guide }}`, shares static text with
`{% include "fragments/<name>" %}` and places `{{ output_format }}` exactly once. A fragment outside the
inference's folder is static and never reads inputs; text that does stays in the prompt, a variant file or a
partial next to the inference, `<stem>.partials/<name>.md`, included as `{% include "<stem>.partials/<name>" %}`.
A plain-text prompt (no `{{ }}`, no `{% %}`) gets inputs and the output contract appended by the engine.

## Choosing a shape

Each row is an option to offer with its conditions, not a default. The first row is the baseline every other
shape is compared with.

| Mechanism | Fits when | Does not fit when | Weigh |
|---|---|---|---|
| one `llm` call on the whole input | the input fits the model's limits and the answer needs all of it | it exceeds the limits, or parts need different handling | the baseline of every comparison |
| `map` over parts (pages, chunks, segments, rows) | parts are independent and each answer is local to its part | the answer needs context across parts | calls × parts, a merge, a lost item must show (`hardening-flows`) |
| `switch` on a value | input kinds need different handling and the kind is known or cheap to get | one prompt handles every kind | a wrong route fails silently; the router's own error rate |
| `parallel` with a `join` | readings that can fail differently (another model, another view of the input) | branches repeat one call on one model | calls × branches; `join` semantics are engine facts (`hardening-flows`) |
| `loop` with `stop` | each pass depends on the last and something outside the model can stop it (a score, a check, a cursor) | passes do not depend on each other | passes × calls; without `stop` every case runs to `max_iter` |
| a second model reading an output (a judge, a critic) | the property is cheaper to check than to produce, and code cannot check it | code or a built-in check can | one more call per case; its own errors, measured on planted defects (`designing-experiments`) |

Compare candidates with a `use` factor on one node or a `flow` factor on a `call` slot; a candidate that calls
the model more also gets a variant of equal budget (`designing-experiments`).

## Pitfalls

| What goes wrong | Right | Code |
|---|---|---|
| `parallel` written with `branches:` | `body` (key → node) and `join` | `E_UNKNOWN_KEY` |
| `MapItemError` imported from `aqven.policies` | `from aqven.spec import MapItemError` | import error |
| `[]` in a list path; `$index` outside a map body | `[*]`; `$index` only inside a map body | `E_REF_SYNTAX`, `E_REF_SCOPE` |
| `on_item_error: skip` | `on_item_error:` with `use: "skip"` on the next line | `E_SPEC_INVALID` |
| `{{ output_format }}` twice or never in a Liquid prompt | exactly once | `E_PROMPT_OUTPUT_FORMAT` |
| a declared input or slot never printed by the prompt | print `{{ variants.<slot> }}` or drop the input | `E_PROMPT_INPUT_UNUSED` |
| an input printed only inside a shared fragment | print it in the prompt, or move the text that reads it into a partial `<stem>.partials/<name>.md`; keep the shared fragment static, never delete it | `E_PROMPT_VARIABLE_UNDECLARED`, `E_PROMPT_INPUT_UNUSED` |
| wording assembled as a string in Python | a variant slot and fragments; model: Lumen `revise.inference.yaml` in `references/engine/lumen-patterns.md` | none: review |
| labels named but not defined in the prompt (8 ticket intents, 30 sound events): the value descriptions of an enum type never reach the model, only the bare values do | a definition per value in what the model sees; the definitions, the enum and its checks kept in step (one table and a builder is one way) | none: preview |
| a consumer prompt fixed which of an upstream reading and the raw input wins, with no measurement behind it | state how the two relate; compare precedence rules as `prompt` variants | none: review |
| comments in YAML; YAML written with anchors or flow style | no comments; the `canonical_writer()` of the dataset builder in `references/engine/snippets.md` (block style, double quotes, no key sorting) | `E_YAML_COMMENT`, `E_YAML_ANCHOR`, `E_YAML_FLOW_STYLE` |
| agent files for many models regenerated five times from a scratchpad script the next session could not rerun | a committed builder `scripts/build_<what>.py` | none: review |
| a docstring in a step or check function, then moved into a comment | neither; the meaning goes into the node's `description` or `experiment.md` | `E_DOCSTRING` |
| a check's `context` typed as `object`; `Text` limits in a signature differ from the type | `context: EvalContext[<In>, <Out>]` with generated types; `Annotated` limits copied from the generated type | `E_CODE_SIGNATURE_MISMATCH` |
| new output fields missing from `returns` | add them | `E_BINDING_TYPE` |
| a schema built at run time (`FieldSpec`) passed across a `call` boundary | build it in the flow that reads it | `E_SIM_NODE_FAILED` |
| Liquid `join` filter, nested loops | forbidden; a plain-text prompt lists inputs by itself | `E_PROMPT_FILTER_FORBIDDEN`, `E_PROMPT_TAG_FORBIDDEN` |
| an `Image` output next to other fields; `Audio` or `Video` as an llm output | an `Image` output is the only out field; audio and video come from a `tool` node | `E_MODALITY_UNSUPPORTED` |
| a media field (`Image`, `Audio`, `Video`, `Document`) inside a record of the inference input: the check passes and the model never gets the file | media at the top level of the inference input | none: the preview lists no attachment |
| `typing.get_args` on a generated enum returned `()` and a filter silently matched nothing | `typing.get_args(X.__value__)`, asserted non-empty | none: an assert |
| guessed names of generated classes | read them from `uv run aqven tree` and `uv run aqven refs`; names change on collisions | `E_CODE_REF_UNRESOLVED` |
| display asked for on a `code` node or the flow output | display exists only on an llm node's inference; tell the owner | none |
| the prompt text disagrees with what is attached ("compare the two calls" when one recording is attached) | match the wording to the attachments the preview lists | none: preview |
| a nested flow per part of the input (one flow per section of a contract), built before anything was measured | the project flow stays flat; one call on the whole input, `map` over the parts (text per kind of part as a variant slot) and a `switch` by kind are options to offer and compare with a `flow` factor | none: review |
| one design built as the answer (a panel with a vote, a split into groups, a judge per item, always two steps) | offer it next to the baseline and one other option, each with when it fits; the experiment decides | none: review |
| a node named after its model (`gemini`) | a name of role and kind: `extract_each_page` | none: review |
| `prompt_preview` with a node path or the flow input | `flow_id` and `node_id`; the inference input or none | `NOT_FOUND`, `INPUT_INVALID` |
| `run_start` without `mode` | `mode: "live"` | `REQUEST_INVALID` |
| an invented `client_op_id`; `expects` without `aqven.yaml` on a rename | a real ULID; every touched path; the error lists the missing paths with their current hashes | `REQUEST_INVALID` |

## Tools and commands

- `aqven` MCP `flow_patch`, `aqven_check`, `prompt_preview`, `pyright_check`, `run_start` (`agent_overrides`),
  `run_get_node`.
- `uv run aqven tree <package>`, `uv run aqven refs <kind>:<id> <package>`, `uv run aqven generate <package>`.
- `uv run aqven prompt preview <flow_id>.<node_id> --project <package> --variant <slot>=<case>`.

## References

- `references/engine/snippets.md`: verified snippets (code-step signature, binding paths, `parallel` with `body`
  and `join`, `map` with `use: "skip"`, a variant slot and a fragment, a display template, allowed Liquid, a
  builder with a canonical YAML writer, a ULID). Read before writing any file of a kind you have not written in
  this session.
- `references/engine/lumen-patterns.md`: real Lumen files for a variant slot, `map`, `parallel`, `call` and every
  factor kind. They show the mechanisms; Lumen's own design is one project's choice, not a shape to copy. Read
  before a variant slot, a container node or an experiment folder.
- `references/concepts/designing-reliable-workflows.md`: what each construct that calls a model more than once
  assumes, when it fits and how to measure it. Read before offering shapes at step 2.
- `references/concepts/ten-kinds-of-nodes.md`, `references/reference/nodes.md`: node kinds and every node key.
  Read at step 1 and before a node kind you have not used.
- `references/concepts/three-prompt-levels.md`, `references/engine/prompts.md`, `references/reference/prompts.md`:
  plain text, Liquid and code prompts. Read before writing a prompt.
- `references/engine/llm-node.md`, `references/engine/code-node.md`, `references/engine/parallel-node.md`,
  `references/engine/map-node.md`, `references/engine/call-node.md`, `references/engine/loop-node.md`,
  `references/engine/human-node.md`: one page per node kind. Read before that kind.
- `references/engine/tool-node.md`: a `tool` node, `ctx.blobs`, `wait`, and a tool node against an agent's own
  `tools`. Read before a step that calls an API, touches media bytes or produces audio or video.
- `references/engine/display-templates.md`: readable run output. Read when the owner asks for a readable run view.
- `references/concepts/two-ways-to-change-a-project.md`, `references/mcp-cli/edit-a-flow.md`: files versus
  `flow_patch`. Read before the first structural change.
- `references/mcp-cli/preview-a-prompt.md`: `prompt_preview` input and output. Read before step 7.
- `references/reference/flows.md`, `references/reference/inference.md`: every key of a flow and an inference.
- `references/engine/experiments.md`: the experiment folder and its `nodes/`, `prompts/`, `flows/`. Read before
  step 10.
- `references/reference/diagnostics.md`: every `aqven check` code. Read on a code this skill does not name.

---
name: oumi-weights-lab
description: Use when asked to find out how an open-weights language model does something (which heads, MLPs, neurons, features, or directions carry a behavior) or to test such a claim; when asked to ablate, zero, edit, swap, or compare a model's parameters, including LoRA adapters; when measuring how a weight change affects a model's answers; or when recording, patching, or probing a Hugging Face causal model's activations or gradients.
compatibility: Requires the oumi-weights-lab CLI (Python 3.11+ on Linux or macOS), provided by the Claude Code plugin when uv is installed or by uv tool install git+https://github.com/oumi-ai/weights-lab, and network access to download models. Remote workers also need an authenticated SkyPilot CLI.
---

# Oumi Weights Lab

Run Python against a live model with tested calls for finding mechanisms, editing weights with exact undo, and measuring what changed. There are two ways to run it, with the same `lab` object:

- **A script**, for a model that loads in seconds, such as one under a billion parameters on CPU. Write a file that calls `open_lab` and run it with `oumi-weights-lab script analysis.py`, which runs it in the lab's own environment. A script session holds only `artifacts/`, so `send`, `peek`, `stop` and `backup` do not apply to it.
- **A persistent worker**, for a large model or a long session. Load the model once, then send Python snippets (see Session commands). Snippets share state, so an edit made in one is measured in the next, and the worker saves every snippet's source, output, and forward-pass count in the session directory.

Scripts and snippets are trusted Python with the user's filesystem and network access.

## Understand a model: start here

Don't write your own ablation loops and hooks. These calls do it, tested, and leave the model as they found it:

```python
from oumi_weights_lab import open_lab

lab = open_lab(
    "/abs/path/to/model", device="cpu"
)  # or a Hub id; a worker snippet already has `lab`
rows = [{"prompt": "The capital of France is", "options": [" Paris", " Rome"], "answer": 0}]
scan = lab.ablation_scan(rows)  # zero each head and MLP, batched; most breaking first
print(scan["parts"][:5])
clean = ["When Mary and John went to the store, John gave a drink to"]
corrupt = ["When Mary and John went to the store, Anna gave a drink to"]
direct = lab.logit_attribution(clean[0], (" Mary", " John"))  # who writes the answer
edges = lab.edge_attribution(clean, corrupt, metric=(" Mary", " John"))  # candidate circuit
circuit = lab.find_circuit(
    clean, corrupt, metric=(" Mary", " John"), top=50, edges=edges
)  # tested by real patching, reusing the attribution above
print(circuit["faithfulness"])
```

These calls are not a sequence to run in order; choose each one for what it would tell you (see [Investigate by experiment](#investigate-by-experiment)). `ablation_scan` is a broad sweep, not the answer: a part with a backup shows no drop, and a part that breaks the behavior may be only one of several, so scan groups (`groups="layers"`, `"pairs"`) and then run the circuit calls.

- [Choose a method](references/method-map.md) says which call answers which question, what each cannot show, and what each costs. That covers heads, directions (`contrast_directions`), sparse features (`load_sae`), and attribution graphs.
- [Find and test a circuit](references/circuit-workflow.md) is the protocol for a claim: rival hypotheses, faithfulness and completeness, look-alikes, redundancy, and a report of what failed. A single ablation sweep misses backup parts and parts that only work together.

## Investigate by experiment

Treat the model as the subject of an experiment, not a checklist. There is no fixed order of calls: at each step, run the experiment that would most reduce your uncertainty about what the task needs, for what it costs. Uncertainty that would not change your answer or your edit is not worth resolving.

Keep a belief file, such as `beliefs.md` in the session directory, and update it after every experiment:

- **Established:** findings that survived an intervention and a control, each with the test that showed it.
- **Hypotheses:** the rival explanations still standing, the evidence for and against each, and how confident you are in each.
- **Assumptions:** what you rely on but have not tested, such as "this prompt pair isolates the behavior" or "the feature is linear at this site".
- **Open questions:** what you do not know yet, the ones that matter most to the task first.

Before each experiment, answer in the belief file:

1. What am I unsure of that matters for the task?
2. Which explanations compete?
3. Which experiment would come out differently under each of them?
4. What will each possible outcome tell me? Write the result each hypothesis predicts before you run.
5. Is there a cheaper experiment that would tell me nearly as much?

An experiment that every standing hypothesis predicts the same way teaches nothing, however thorough it is.

- **Cost.** Reading weights (`parts`, `measure`, `compare`, `head_weights`) costs no forward passes and shows what a part could do: what it reads and writes, and how large it is. Running prompts shows what the model does on them. Only an intervention with a control shows what a part causes. Rule out what cheap experiments can, and spend passes where only an intervention can decide. [Choose a method](references/method-map.md#what-each-method-costs) lists each call's cost, and `lab.forward_passes` read before and after a call gives the count.
- **Surprises.** When a result fits none of your predictions, check the setup first: active edits (`lab.active_edit_ids`), patches and batch size, and whether restored scores match the baseline. If the setup holds, the surprise is evidence: add the hypothesis it suggests and design the test that separates it from the rest.
- **Edits.** An edit is an experiment inside the investigation, not its end. Make one when the hypotheses it depends on have survived tests that could have refuted them, and write down beforehand what it should change and what it should leave alone. Then measure both. If the result differs from the prediction, undo it and keep investigating.

## Setup

Run `oumi-weights-lab --help`. If it fails, ask the user to install the CLI with `uv tool install git+https://github.com/oumi-ai/weights-lab`, or `uv tool install 'oumi-weights-lab[adapters,datasets,multi-gpu,quantized,saes] @ git+https://github.com/oumi-ai/weights-lab'` for LoRA adapters, Hugging Face datasets (`lab.hf_rows`), multi-GPU loading, quantized loading, and sparse autoencoders (`lab.load_sae`). Under the Claude Code plugin, the first call builds an environment and downloads PyTorch; allow it several minutes.

## Session commands

| Step | Command |
| --- | --- |
| Start | `oumi-weights-lab start --session sessions/NAME --model MODEL_ID --pass-limit 2000 --snippet-timeout 1800` |
| Run a snippet and wait | `oumi-weights-lab send --session sessions/NAME --file /abs/path/snippet.py --follow --timeout 1800` |
| Check status | `oumi-weights-lab peek --session sessions/NAME` |
| Stop | `oumi-weights-lab stop --session sessions/NAME` |
| Archive | `oumi-weights-lab backup --session sessions/NAME --output NAME.tar.gz` |

- Use a new `--session` directory for every `start`; a stopped session cannot be restarted.
- `start` returns while the model loads, and snippets queue until it is ready. `--device` defaults to CUDA, then Apple MPS, then CPU. `--dtype` defaults to the checkpoint's own.
- For a model too big for one GPU, add `--device-map balanced` to spread it over every visible GPU (`sequential` fills GPU 0 first). `--max-memory 0=70GiB,1=70GiB` uses only the GPUs it names, up to that much on each; by default the model may use 90% of every GPU's free memory. A model that would need CPU or disk offload is refused before any weights load. `peek` reports GiB of parameters per device under `devices`.
- Add `--quantize nf4` (or `fp4`, `int8`) to load the model with bitsandbytes, on a GPU or an Apple-silicon Mac. nf4, fp4, and int8 weights edit by requantizing the blocks (4-bit) or rows (int8) an edit touches, and undo restores them byte for byte. Kernel code from the Hub is blocked unless you pass `--allow-hub-kernels`. Read [quantized models](references/quantized.md) first.
- Stdout is JSON. `--follow` streams snippet output to stderr. `--snippet-timeout` stops a snippet that runs too long; `send --timeout` only limits how long the CLI waits.
- Snippet files can live anywhere; `--file` sends their contents. Snippets run in the directory where `start` ran, so read inputs by absolute path and write outputs under `artifacts`.
- Add `--adapter PATH_OR_ID` to load a LoRA adapter. For a cloud GPU or Slurm, read [remote workers](references/remote.md).

## Snippets

A snippet sees `lab`, `model`, `tokenizer`, `Path`, and `artifacts`. This one measures an ablation and its control:

```python
import json

rows = [json.loads(line) for line in Path("/abs/path/caps.jsonl").read_text().splitlines()]
rows = [
    {
        "prompt": r["prompt"],
        "options": [" " + o for o in r["options"]],
        "answer": r["options"].index(r["answer"]),
    }
    for r in rows
]
name = "model.layers.3.mlp.down_proj.weight"  # confirm with lab.parts("*layers.3.*")
baseline = lab.evaluate(rows, name="baseline-v1", max_passes=200)
edit_id = lab.zero(name, note="ablate layer 3 MLP")
try:
    ablated = lab.evaluate(rows, name="ablated-v1", max_passes=200)
finally:
    lab.undo(edit_id)
restored = lab.evaluate(rows, name="restored-v1", max_passes=200)
print(baseline["accuracy"], ablated["accuracy"], restored["accuracy"])
print(json.dumps(lab.diff(baseline, ablated), indent=2))
```

- A row is `{"prompt": str, "options": list or {label: text}, "answer": index, label, or option text}`. Prompt and option are tokenized separately, so start each option with the space the tokenizer expects, such as `" Paris"`. An answer given as option text must match it exactly, space included; an index avoids that.
- For instruction-tuned models, pass `chat_template=True` to `evaluate` and `score` so prompts are wrapped the way the model was trained; options then follow the assistant header and usually need no leading space. Use the same setting for every run you compare.
- `evaluate` returns a summary with `accuracy`, `correct`, `total`, `forward_passes`, and `run_dir`. Each row's scores and prediction are in `run_dir/items.jsonl`. Every run needs a new name made of letters, digits, `_`, and `-`.
- Likelihood scoring costs one forward pass per option per row; `mode="sampled"` costs one per generated token (beam search: one per search step, however many beams); a batched call costs one pass per sequence. `max_passes` caps one call and `--pass-limit` caps the whole session; size both from that cost.
- Likelihood and sampled runs process up to 8 sequences per forward (`batch_size`), and runs pair only when scored the same way. Sampled items record `finish_reason` and `generated_tokens`, and the summary reports `truncation_share`. Generation stops at the tokenizer's EOS as well as the model's, so chat replies end with the turn; pass `eos_token_id` to choose the stop tokens yourself. With `num_samples=k` and `do_sample=True`, each row scores the fraction of its k samples that are correct; add `pass_at` for pass@k and `answer_key` for majority vote. While a logit attachment, or a `patch` or `record` at nonnegative positions, is active, pass `batch_size=1` to that run and to the runs you compare it with.
- `lab.parts(pattern)` lists parameter names and shapes; names differ by architecture.
- Edit through `lab.edit`, `lab.zero`, or `lab.swap`. `lab.undo()` restores the newest edit exactly in any dtype (quantized weights byte for byte), so undo several edits newest first. Writes made directly through `model` are not tracked.
- Wrap your own `model(...)` calls in `torch.no_grad()`.
- After a timeout or error, check `lab.active_edit_ids` and undo to a known state before measuring again.

## Experiment discipline

1. Write down the question, and the result each hypothesis predicts, before running anything.
2. Measure a baseline in the same session before any edit.
3. After undoing, measure again: restored results must match the baseline.
4. If you will choose among several edits or settings, set aside held-out rows first. Evaluate only the final choice on them, once, with `held_out=True` and `max_passes`. Held-out rows can never become dev rows, even after a failed run. A single pre-planned edit needs no held-out split.
5. Report the question, model and device, parameters edited, dataset size, baseline, edited, and restored results, changed items, forward passes, and the limits of the evidence. Say which findings are established, which are hypotheses, and which are assumptions, and how confident you are in each. A small hand-written set is a diagnostic, not a benchmark.
6. An attention pattern, a probe score, or a plot is a lead. Before calling something a mechanism, confirm it with an intervention, a control intervention, and new prompts. A null ablation does not show a part is unused, and an ablation that breaks the behavior does not show the part is the whole mechanism. Follow the protocol in [Find and test a circuit](references/circuit-workflow.md): state rival hypotheses, measure how much of the behavior your claim explains, try to prove it wrong, and report what failed. When no method fits the question, design one; don't narrow the question to the tools.
7. To keep edited weights, call `lab.export("NAME")` before stopping. Export fails while attachments or patches are active, and `backup` never saves weights.

## Recipes

Read only the ones you need.

To understand how a model does something:

- [Choose a method](references/method-map.md): which method answers which question, and what each cannot show.
- [Find and test a circuit](references/circuit-workflow.md): the protocol for a claim, from leads to a causal test, faithfulness, attempts to prove it wrong, and a report.
- [What a finished circuit looks like](references/worked-circuits.md): induction heads and indirect-object identification in GPT-2 small.
- [When current methods fall short](references/new-methods.md): design a method, test it on known answers, and report where it wins and loses.

Methods for finding mechanisms:

- [Logit lens](references/logit-lens.md): read each layer's output through the final norm and head.
- [Activation patching](references/activation-patching.md): replace hidden states or module inputs at chosen tokens, and capture attention weights.
- [Attribution patching](references/attribution-patching.md): rank module and token sites with activation gradients, then confirm with real patches.
- [Circuit analyses](references/circuit-analyses.md): direct logit attribution, path patching, and edge attribution patching as calls.
- [Attention heads](references/heads.md): list heads as weight slices, ablate one, and screen for induction heads.
- [Steering vectors](references/steering.md): compute a direction from contrasting prompts, check it on held-out pairs, and add it to the residual stream.
- [Document-split probes](references/probes.md): linear probes that keep source documents apart.
- [Sparse autoencoder features](references/saes.md): load a public SAE or transcoder, check its reconstruction error, then read, patch, and steer features.
- [Attribution graphs](references/attribution-graphs.md): build a feature graph of one answer from transcoders, read it as JSON, and test a path with a real intervention.

New methods:

- [Building blocks for new methods](references/building-blocks.md): run with anything replaced, take derivatives between two points, and sweep interventions in one batch.
- [Test a method on known answers](references/proving-ground.md): build tasks with known mechanisms, grade a claim against the key, and compare methods.
- [Save and reuse a method](references/saved-methods.md): keep a method you wrote with its source, results and setup, load it by name later, and draft a recipe from a winner.

Editing and measuring:

- [Worked example](references/worked-example.md): full baseline, ablation, undo, and report snippet.
- [Zero or swap parts](references/zero-swap.md): reversible ablations and matched checkpoint slices.
- [Remove a direction](references/direction-edits.md): project a direction out of a weight, bias, or embedding.
- [Evaluation reports and screens](references/evaluation.md): paired statistics, regression suites, and pinned dev subsets.
- [Save and resume edits](references/edit-bundles.md): save points that carry undo history and held-out reservations.
- [Compare checkpoints](references/compare-checkpoints.md): parameter deltas without forward passes.
- [Short-row gradients](references/gradients.md): per-row gradients for selected parameters.
- [LoRA update diagnostics](references/lora-diagnostics.md): adapter update spectra and rank without forward passes.
- [Written-working control](references/written-working.md): test a computation in text before editing weights.
- [Hand-built parts](references/hand-built.md): temporary prompt transforms and logit adjustments.

Setup:

- [Quantized models](references/quantized.md): load nf4, fp4, or int8 and know what you can edit.
- [Remote workers](references/remote.md): SkyPilot clouds and Slurm.

---
name: code-audit-fanout
version: 1.0.0
description: |
  Five-way parallel code audit. User pastes a Python file / function /
  diff → orchestrator fans out 5 specialist sub-agents in ONE message,
  each reviewing a DIFFERENT axis (static analysis, library API
  correctness, standards/spec compliance, reproducibility, numerical
  correctness). Every finding MUST cite an exact URL + a quoted
  passage from the official documentation. Aggregator agent merges,
  dedupes, ranks by severity. Code returns reviewed 4-5 times before
  the user touches it.

  Trigger when user says: "audit this code", "review this diff",
  "debug this", "check my function", "find bugs", "/audit-code",
  "/code-audit-fanout", "fanout audit", or pastes a code block and
  asks for review.

  Auto-trigger heuristic: user pastes >20 lines of Python and asks
  for "review", "audit", "debug", "check", or "bug".

  HARD RULE: zero claims without a source. Every issue cites a URL
  to the official docs / paper / spec, plus the exact quoted passage.
  No hallucinated APIs, function signatures, or behaviors. If a
  specialist cannot verify a claim against a primary source, it
  must say "UNVERIFIED" and skip the finding.
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - Bash
  - WebFetch
  - WebSearch
  - Agent
---

# code-audit-fanout

## When to use
USE for any code review request where correctness matters more than
speed. Especially:
- ML training loops, loss functions, custom layers
- Signal-processing pipelines (FFT, filters, modulation)
- 5G PHY simulators (channel models, MIMO precoding, decoders)
- Any function touching complex-valued tensors, dB scales, or
  hardware-determinism primitives
- Diffs > 50 lines before merge

SKIP for trivial edits (typo fix, rename, formatting).

## The 5 specialist agents

Each spawned in parallel in ONE assistant message. Each has a
narrow scope, a required source list, and a citation contract.

### Specialist 1 — static-analyzer
**Scope:** Read-only static analysis.
**Tools:** Read, Grep, Glob, Bash
**Checks:**
- `ruff check --select ALL` output
- `mypy --strict` output (if config present, else `mypy`)
- `pyright` if available
- Function-level cyclomatic complexity > 10
- Bare `except:`, `except Exception:`, swallowed errors
- Mutable default args
- Print statements left in code (vs logging)
**Citation requirement:** every flagged rule must reference the
exact ruff / mypy / pyright rule ID and link to the rule docs.

### Specialist 2 — library-api-auditor
**Scope:** Verify every imported API call against official docs.
**Tools:** Read, Grep, WebFetch, WebSearch
**Required sources (in order of precedence):**
- PyTorch — https://docs.pytorch.org/docs/stable/
- NumPy — https://numpy.org/doc/stable/reference/
- SciPy — https://docs.scipy.org/doc/scipy/
- JAX — https://docs.jax.dev/en/latest/
- Sionna — https://nvlabs.github.io/sionna/
- HuggingFace — https://huggingface.co/docs/
- pandas — https://pandas.pydata.org/docs/
**Procedure:**
1. Extract every imported symbol and every `X.Y.Z(...)` call.
2. For each, WebFetch the official doc page.
3. Check: function exists? signature matches? deprecated? known
   gotchas in the docs (the "Note" / "Warning" boxes)?
4. Flag mismatches with: file:line — call — expected signature
   per docs URL — quoted doc passage.
**Citation requirement:** every finding cites the exact doc URL
+ section anchor + a verbatim quote.
**HARD RULE:** if a fetch fails or the page doesn't mention the
symbol, mark UNVERIFIED. Do NOT guess.

### Specialist 3 — standards-spec-auditor
**Scope:** For wireless / signal-processing code only. Verify the
code's constants and procedures against published standards.
**Tools:** Read, WebFetch, WebSearch
**Required sources:**
- 3GPP TS portal — https://www.3gpp.org/specifications-technologies
- ETSI standards — https://www.etsi.org/standards
- IEEE Xplore (citation only — no full-text fetch unless user
  provides access)
- IETF RFCs — https://www.rfc-editor.org/
- ITU-R recommendations — https://www.itu.int/rec/R-REC/en
**Checks:**
- Numerology constants (subcarrier spacing 15/30/60/120/240/480 kHz)
- Resource grid dimensions (PRB = 12 subcarriers, slot = 14 symbols)
- LDPC base graph selection thresholds (TS 38.212)
- Modulation mapping tables (TS 38.211 §5.1)
- Channel-model parameters (TR 38.901 tables)
- TBS / MCS index tables (TS 38.214)
**Citation requirement:** every numeric constant or procedure
verified must cite TS/TR number + clause + table + quoted line.
**HARD RULE:** if the user's code is not wireless, this specialist
returns "NOT APPLICABLE" and does not invent issues.

### Specialist 4 — reproducibility-auditor
**Scope:** Ensure the code will produce the same result on a
second run.
**Tools:** Read, Grep, WebFetch
**Required sources:**
- https://docs.pytorch.org/docs/stable/notes/randomness.html
- https://docs.jax.dev/en/latest/jep/263-prng.html
- https://numpy.org/doc/stable/reference/random/index.html
**Checks (cite the relevant doc section for each):**
- All seeds set: `random.seed`, `np.random.seed`,
  `torch.manual_seed`, `torch.cuda.manual_seed_all`
- Env vars: `PYTHONHASHSEED`, `CUBLAS_WORKSPACE_CONFIG=:4096:8`
- `torch.use_deterministic_algorithms(True)` present
- `torch.backends.cudnn.deterministic = True` and `benchmark = False`
- DataLoader: `worker_init_fn` + `generator=torch.Generator()` set
- JAX: explicit `PRNGKey` threading; no global `jax.random` calls
- Non-deterministic ops used without acknowledgment: `scatter_add_`,
  `index_add_`, `bincount`, embedding-bag backward, CTC loss,
  pooling backwards
- Resumed-from-checkpoint code: re-seeds AND saves RNG state
**Citation requirement:** each finding cites the exact PyTorch /
JAX / NumPy doc URL + the warning passage that justifies the rule.

### Specialist 5 — numerical-correctness-auditor
**Scope:** Catch silent numerical bugs.
**Tools:** Read, Grep, WebFetch
**Required sources:**
- https://numpy.org/doc/stable/reference/generated/numpy.fft.fft.html
- https://docs.pytorch.org/docs/stable/generated/torch.fft.fft.html
- https://nvlabs.github.io/sionna/ (for complex-tensor conventions)
- Any user-supplied papers/notes the code claims to implement
**Checks:**
- Complex dtypes preserved end-to-end (no silent cast to real)
- FFT normalization explicit (`norm="ortho"` vs `"backward"` vs
  `"forward"`)
- dB ↔ linear conversions named (`lin2db`, `db2lin`); no bare
  `10*log10` or `10**(x/10)`
- Sample-rate / FFT-size consistency across the pipeline
- Tensor-shape order matches the library convention
  (Sionna: [batch, rx, tx, subcarrier, symbol])
- In-place ops on autograd tensors (breaks backward)
- Mixed precision: explicit autocast scope, gradient scaler used
- Numerical-stability tricks: log-sum-exp, log1p, expm1 where
  appropriate
**Citation requirement:** every claim about a library behavior
cites the docs URL + quoted passage. Claims about the user's own
math must cite the user-supplied paper / equation number.

## Aggregator agent

After all 5 specialists return, ONE final aggregator agent
(general-purpose) merges results.

**Aggregator system prompt:**
```
You are merging 5 specialist code-audit reports. Do NOT add new
findings. Do NOT remove any cited finding. Your job:

1. Group findings by file:line — show all specialists who flagged
   the same line together.
2. Deduplicate identical findings (same line, same root cause).
3. Rank by severity:
   - CRITICAL — code will not run, or returns silently wrong values
   - HIGH — reproducibility broken, results not trustworthy
   - MEDIUM — style / maintainability / minor numerical risk
   - LOW — cosmetic
4. Emit final report in this exact structure:

   ## Summary
   - N findings total (X critical, Y high, Z medium, W low)
   - K verified vs U unverified
   - File coverage: list of files reviewed

   ## Findings
   For each finding:
   ### [SEVERITY] file:line — short title
   - **Specialist:** name
   - **Problem:** 1-2 sentences
   - **Source:** URL + verbatim quoted passage
   - **Fix:** minimal diff or code snippet

   ## UNVERIFIED claims (skipped)
   - List anything a specialist could not source

   ## What was NOT checked
   - Be explicit about gaps (e.g. "no integration tests run",
     "GPU-specific behavior not reproduced on this machine")

NEVER invent a finding. NEVER paraphrase a source quote — quote
verbatim. If a specialist had zero findings, say so explicitly.
```

## Orchestrator prompt template (paste-and-go)

```
I want a 5-way parallel audit of the following code.

CODE TO AUDIT:
<paste file path OR ```python ... ``` block>

CONTEXT (optional — fill if relevant):
- This code implements: <one-line description>
- Reference paper / spec: <citation or URL if any>
- Known constraints: <e.g. must run deterministic on A100>

SPAWN 5 SPECIALISTS IN PARALLEL IN ONE MESSAGE:
1. static-analyzer
2. library-api-auditor
3. standards-spec-auditor (or "NOT APPLICABLE" if not wireless)
4. reproducibility-auditor
5. numerical-correctness-auditor

Each must follow the citation contract from the code-audit-fanout
skill: every finding cites a URL + verbatim quoted passage. No
claim without a source. UNVERIFIED items must be marked, not
hidden.

After all 5 return, spawn the aggregator agent to merge. Show me
the merged report ONLY — do not show raw specialist outputs.
```

## Files in this skill folder

- `SKILL.md` — this file. **Self-contained** — all 5 specialist prompts, the
  aggregator prompt, the orchestrator template, and the citation contract are
  inline above. No companion files required to run.

## Citation contract (the only rule that matters)

Every finding MUST include:
1. **URL** to the official documentation page or spec.
2. **Verbatim quote** from that page — not a paraphrase.
3. **Anchor** (section / clause / table number) within the page.

Example of a valid finding:
```
HIGH — train.py:42 — torch.use_deterministic_algorithms not called
Specialist: reproducibility-auditor
Problem: Code seeds RNGs but does not enable deterministic
algorithms. CUBLAS, cuDNN convolutions, and atomicAdd float ops
will produce different bit patterns across runs.
Source: https://docs.pytorch.org/docs/stable/notes/randomness.html
        §"Avoiding nondeterministic algorithms"
Quote: "torch.use_deterministic_algorithms() lets you configure
PyTorch to use deterministic algorithms instead of nondeterministic
ones where available, and to throw an error if an operation is
known to be nondeterministic (and without a deterministic alternative)."
Fix:
  import torch
  torch.use_deterministic_algorithms(True, warn_only=False)
  torch.backends.cudnn.deterministic = True
  torch.backends.cudnn.benchmark = False
```

Example of what is NOT allowed:
```
❌ "I think this might cause issues with reproducibility."
❌ "PyTorch docs say something about determinism."
❌ "This API was deprecated recently."
❌ Any finding without URL + verbatim quote + anchor.
```

## Failure modes + fixes

| Failure | Cause | Fix |
|---|---|---|
| Specialist invents an API that doesn't exist | Skipped WebFetch verification | Re-run with explicit "no claim without quoted source" rule |
| Specialist quotes outdated docs | Library version mismatch | Tell orchestrator the exact library version installed |
| Aggregator drops findings | Over-aggressive dedup | Use "preserve unique URLs even if same line" rule |
| All 5 specialists fire sequentially | Spawned in separate messages | Re-issue as a single message with 5 Agent calls |
| 3GPP fetch blocked / requires login | 3GPP portal session needed | Specialist marks UNVERIFIED + suggests user downloads PDF |
| Specialist times out | Code too long | Chunk by function. Run audit per-function in a secondary fanout. |

## Anti-patterns

- ❌ Specialist paraphrases instead of quoting docs verbatim
- ❌ Findings without a URL — silent hallucination risk
- ❌ Standards-spec-auditor invents 3GPP clause numbers — must cite real TS
- ❌ Aggregator adds its own opinions
- ❌ Running fewer than 5 specialists to "save tokens" — defeats the cross-check
- ❌ Sequential dispatch — one message, five Agent calls

## Cost model

- Wall clock: ~max(specialist) instead of sum — typically 60-120s
- API tokens: 5× a solo review's tokens + aggregator merge
- Worth it when: code touches production / publication / shared lab repos
- Skip when: throwaway notebook exploration

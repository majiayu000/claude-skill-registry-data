---
name: giskard-llm
description: "Authors and runs Giskard LLM scans - adversarial test-case generation for LLM applications via `giskard.scan(model)` covering 7 vulnerability categories (hallucination, harmful_content, prompt_injection, sensitive_information_disclosure, stereotypes, robustness, basic_sycophancy); wraps any callable model behind `giskard.Model(model_predict, model_type=\"text_generation\", ...)`; emits HTML report. Use when the user needs adversarial / red-team coverage on top of functional eval suites."
---

# giskard-llm

## Overview

[gk-gh]: https://github.com/Giskard-AI/giskard

Distinct from functional eval frameworks (Promptfoo, DeepEval,
Ragas), Giskard's value (per [gk-gh][gk-gh]) is **adversarial
test generation** - auto-generates inputs designed to break LLMs
along documented vulnerability dimensions, then reports findings
in a triageable HTML report.

**Important version note (2026-05-06):** per [gk-gh][gk-gh], "Giskard
v2 is no longer actively maintained. The current v3 focus is on
`giskard-checks` for evaluations, while vulnerability scanning and
RAG evaluation still rely on Giskard v2." This skill targets v2 LLM
scanning; pin `>2,<3` per the install command.

## When to use

- The team needs a red-team / adversarial pass before shipping an
  LLM feature.
- Functional evals (Promptfoo / DeepEval / Ragas) pass but the
  team wants to surface vulnerabilities beyond the test corpus.
- Compliance-driven assurance needs reportable evidence of
  hallucination / harmful-content / prompt-injection coverage.
- Product owners need an HTML report (not raw test output) to
  triage and sign off.

## Step 1 - Install

Per [gk-gh][gk-gh] (v2-pinned):

```bash
pip install "giskard[llm]>2,<3"
```

The `[llm]` extra pulls in the LLM scan dependencies.

## Step 2 - Wrap your model

Per [gk-gh][gk-gh] (verbatim quickstart):

```python
import giskard
import pandas as pd

def model_predict(df: pd.DataFrame):
    """The function takes a DataFrame and must return a list of outputs (one per row)."""
    return [my_llm_chain.run({"query": question}) for question in df["question"]]

giskard_model = giskard.Model(
    model=model_predict,
    model_type="text_generation",
    name="My LLM Application",
    description="A question answering assistant",
    feature_names=["question"],
)
```

The `description` field steers Giskard's adversarial generator - 
make it specific (e.g., "A question answering assistant for medical
guidance" vs the generic "A QA assistant"). Better description ⇒
better-targeted adversarial inputs.

## Step 3 - Run the scan

```python
scan_results = giskard.scan(giskard_model)
display(scan_results)
```

(Per [gk-gh][gk-gh].)

In a Jupyter notebook this renders the report inline. To export:

```python
scan_results.to_html("giskard-report.html")
```

## Step 4 - Vulnerability detector catalog

Per [gk-gh][gk-gh] the v2 LLM scan covers these detector
categories:

| Detector | What it tries to surface |
|---|---|
| `hallucination` | Generated content not grounded in inputs / facts |
| `harmful_content` | Toxic, dangerous, or harmful generation |
| `prompt_injection` | Inputs that override system instructions |
| `sensitive_information_disclosure` | PII / credentials / system prompt leakage |
| `stereotypes` | Discriminatory / stereotyped output by protected attribute |
| `robustness` | Brittleness to small input perturbations |
| `basic_sycophancy` | Agreeing with falsehoods to please the user |

Detector selection (subset run):

```python
scan_results = giskard.scan(
    giskard_model,
    only=["hallucination", "prompt_injection"],
)
```

(Per the `scan()` API; consult [docs.giskard.ai][gk-docs] for the
exact parameter list per Giskard release.)

[gk-docs]: https://docs.giskard.ai/

## Step 5 - Convert findings to test suites

After a scan surfaces issues, Giskard can synthesize tests for
regression coverage:

```python
test_suite = scan_results.generate_test_suite("My LLM Test Suite")
test_suite.run()
```

This produces deterministic regression tests from the failing
adversarial prompts found by the scan - re-run on every PR to
prevent regression on previously surfaced vulnerabilities.

## Step 6 - CI integration

Giskard does not ship a first-party CI action; pattern:

```bash
python -m my_giskard_scan_script  # produces giskard-report.html
```

Then upload as a CI artifact:

```yaml
- uses: actions/upload-artifact@v4
  with: { name: giskard-report, path: giskard-report.html }
```

For PR-blocking gating, parse `scan_results` for `severity` and
fail CI if any critical findings appear:

```python
critical = [issue for issue in scan_results.issues if issue.level == "major"]
if critical:
    sys.exit(1)
```

## Anti-patterns

| Anti-pattern | Why it fails | Fix |
|---|---|---|
| Generic `description=` field | Adversarial generator produces off-target inputs; many false positives | Specific description (Step 2) |
| Run scan once, never regenerate test suite | Vulnerabilities resurface in new code | Regenerate test suite per release (Step 5) |
| Skip Step 5 - only rely on scans | No regression protection between scans | Always synthesize the test suite |
| Pin Giskard but not the judge-LLM provider | Judge-model drift causes flake | Pin both in CI env |

## Limitations

- v2 LLM scanning is in maintenance-only mode (per [gk-gh][gk-gh]);
  v3 is forming around `giskard-checks`. Track upstream before
  greenlighting new investment.
- Adversarial generation is non-deterministic - use random seeds
  when available + pin Giskard version.
- LLM-as-judge cost: scans invoke a judge model many times;
  budget for cost spikes when scanning new models.
- Limited to `text_generation` and `text_classification` model types
  in v2; multi-modal scanning lives elsewhere in the Giskard
  ecosystem.

## References

- [gk-gh][gk-gh] - repository, install, quickstart, detector list
- [gk-docs][gk-docs] - full documentation
- `promptfoo-evaluation`,
  `deepeval-evaluation`,
  `ragas-evaluation` - functional
  eval sister tools (use Giskard for adversarial coverage on top)

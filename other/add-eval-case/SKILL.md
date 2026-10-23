---
name: add-eval-case
description: Add a new E2E test case to tests/e2e/prompts.yaml for LangSmith evaluation. Use when adding interaction pairs to test, covering new ANSM drug classes, or rebalancing eval coverage.
argument-hint: "<substance-a> <substance-b>"
---

# Skill: Add an E2E Eval Test Case

## Steps

1. **Identify the interaction pair** — substance A + substance B, with ANSM level:
   - `Contre-indication` (CI) or `Association déconseillée` (AD) → `expect_warn: true`
   - `Précaution d'emploi` (PE) or `À prendre en compte` (APEC) → `expect_warn: false`

2. **Write a realistic clinical scenario** (in French, pharmacist/physician perspective):
   - Use DCI names (not brand names) in the prompt
   - Ground it in a plausible indication (e.g. patient greffé sous ciclosporine)
   - Keep it concise — 2-3 sentences

3. **Add the case** to `tests/e2e/prompts.yaml`:
   ```yaml
   # <ANSM level>: <mechanism> — DB pair: <SUBSTANCE_A> + <SUBSTANCE_B> (<CI|AD|PE|APEC>)
   - id: <substance_a>_<substance_b>
     prompt: >
       <Clinical scenario in French.>
     expect_warn: true   # or false
     expect_in:
       - "⚠️"            # only if expect_warn: true
       - "<substance name as it appears in French DCI>"
     expect_not:
       - "<unrelated substance that should not appear>"
   ```

4. **Choose `expect_not` carefully** — must be a substance meaningfully different,
   not a trivial variation. Used as false-positive guard.

5. **Run the eval** to validate the new case passes:
   ```bash
   uv run dotenv -f .env run -- python scripts/run_eval.py
   ```

## Coverage targets

Maintain balance across:
- `expect_warn: true` cases (CI + AD) — currently: ibuprofene_methotrexate, ciclosporine_simvastatine
- `expect_warn: false` cases (PE + true negatives) — currently: amiodarone_simvastatine, paracetamol_amoxicilline, generiques_doliprane
- Tool path diversity: interaction lookup, generic lookup, simple drug search

## Rules

- `id` format: `<substance_a>_<substance_b>` in lowercase, underscores, no accents
- Comment above each case must include the ANSM level and DB pair (for traceability)
- `expect_in` terms must match what the agent actually outputs (test with a manual run first)
- Never add a case you haven't verified exists in the ANSM thésaurus

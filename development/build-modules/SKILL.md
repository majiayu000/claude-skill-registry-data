---
name: build_modules-layer
description: >
  Builds and evaluates Python module layers for the Gentleman-Skills ecosystem.
  Generates eval scenarios, adapts skills for LLM targets, and performs code
  analysis (dead code, complexity, blast radius).
  Trigger: When working in `build_modules/` — adding, modifying, or debugging
  module generation, adaptation, or analysis.
license: Apache-2.0
metadata:
  author: repoforge
  version: "1.0"
  complexity: medium
  token_estimate: 1200
  dependencies: []
  related_skills: [eval-layer, repoforge-layer]
---

<!-- L1:START -->
# build_modules-layer

This layer provides tools for building, evaluating, and analyzing Python modules within the Gentleman-Skills ecosystem. It handles module generation, LLM target adaptation, and code quality analysis.

**Trigger**: When working in `build_modules/` directory — adding, modifying, or debugging module generation, adaptation, or analysis.
<!-- L1:END -->

<!-- L2:START -->
## Quick Reference

| Task | Pattern |
|------|---------|
| Run eval scenarios | `python -m eval.harness run_all` |
| Adapt skills for LLM targets | `adapt_for_cursor/Codex/Gemini/Copilot` |
| Detect dead code | `detect_dead_code()` |

## Critical Patterns (Summary)
- **Pattern 1: Module Generation**: Use `make_fastapi_crud_module`, `make_nextjs_page_module`, `make_mixed_layer`, or `make_go_service_module` from `eval/harness.py` to generate module skeletons in various frameworks.
- **Pattern 2: Skill Adaptation**: Use `adapt_for_cursor`, `adapt_for_codex`, `adapt_for_gemini`, or `adapt_for_copilot` from `repoforge/adapters.py` to transform skill dictionaries for specific LLM targets.

## When to Use

- Adding a new module generation function to `eval/harness.py`
- Adapting existing skills for a different LLM target platform
- Detecting dead code or analyzing module complexity
- Running eval scenarios against generated modules

## Adding a New Module Generation Function

1. Add a new function to `eval/harness.py` following the pattern `make_<framework>_module() -> tuple[dict, dict]`
2. Export the function in `eval/harness.py` `__all__` if present
3. Test with `run_scenario` using the new module config
4. Verify output with `print_report`

## Commands

```bash
python -m eval.harness run_all
python -m eval.harness run_scenario <scenario_name>
adapt_for_cursor <skills_json>
adapt_for_copilot <skills_json>
detect_dead_code <ast_symbols_dict>
```

## Anti-Patterns

### Don't: Mix adaptation targets — using `adapt_for_copilot` skills with `adapt_for_cursor` expectations — each adapter formats skill dicts differently for its target LLM, causing integration failures.

```python
# BAD: Mixing adaptation targets
skills = adapt_for_cursor(skills_dict)
# Later using skills with Cursor — works
# But passing these same skills to adapt_for_codex will produce
# incorrectly formatted output for Codex's expectations.
```
<!-- L3:END -->
---
name: diagnose-llm-advisor-health
description: Verify a native LLM voting advisor before trusting advisor-sensitive evaluations.
---

# Diagnose LLM advisor health

The advisor reads a meeting snapshot and returns a vote/chat decision. A completed episode does not prove that it ran;
scripted fallback can hide an inactive advisor.

1. Confirm the exact uploaded version was built for native Anthropic Messages or OpenAI Chat and opted in with `--use-llm`.
2. Check `COWORLD_LLM_ENDPOINT`, `COWORLD_LLM_ENABLED`, and `COWORLD_LLM_MODEL` names/presence without printing secrets.
3. Verify a real call/result in player traces and distinguish request rejection, timeout, malformed vote, and fallback.
4. Validate the returned vote against offered options. Check elapsed time against the game's vote deadline.
5. Re-run deterministic fallback alone before comparing advisor-sensitive scores.

Use canonical model IDs, such as `anthropic/claude-haiku-4.5`, only when permitted by the current platform policy.
Hosted SDK credentials are placeholders; only the sidecar holds the provider key. Local calls require a configured
native endpoint or host OpenRouter key. Rebuild and republish old advisor images; no automatic protocol migration exists.

These templates describe the required native contract, not proof that an external notsus image has migrated.

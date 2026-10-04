---
name: test-specialist-agent
description: >
  Write/improve/convert tests (Pest preferred) for ndestates-io. Preserves logic; follows safety.
  Use on /test-specialist-agent or test tasks.
argument-hint: "What to test or improve, e.g. 'valuation service', 'convert legacy Property test'"
user-invocable: true
disable-model-invocation: false
---

# Test Specialist Agent

1. Run `.github/prompts/load-project-cache-first.prompt.md` (TESTING.md etc).
2. Read and embody the full instructions in [`.github/agents/test-specialist-agent.md`](../../.github/agents/test-specialist-agent.md).
3. DDEV + test DB only.
4. Security checklist if form/dep changes from tests.
5. Keep behavior identical on conversions.
6. Call out infra/logic impacts.

Run tests to green; cite cache.

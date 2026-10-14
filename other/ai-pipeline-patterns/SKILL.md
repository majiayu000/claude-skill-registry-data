---
name: ai-pipeline-patterns
description: "Use when changing the AI workflow, embeddings, Qdrant integration, newsletter intake, relevance scoring, summarization, classification, Celery handoff, or Anymail inbound processing. Trigger phrases include pipeline, relevance scoring, embeddings, Qdrant, newsletter intake, summarization, classification, OpenRouter, and review queue."
---

# AI Pipeline Patterns Skill

Use this skill when working on the ingestion and AI processing pipeline.

## Scope

This skill covers the interaction between:

- `core/pipeline.py`
- `core/embeddings.py`
- `core/tasks.py`
- `core/newsletters.py`
- `core/newsletter_extraction.py`
- `core/signals.py`
- `core/views.py`
- related models, tests, and docs

## Rules

- Preserve the separation between persisted state, background execution, and vector storage.
- Keep Qdrant access inside the embedding layer unless there is a strong reason to expand that boundary.
- Keep newsletter intake routing and confirmation logic in the newsletter intake modules, not in unrelated views or serializers.
- Prefer explicit fallbacks when LLM or external-service calls can fail.
- Respect the current thresholds and routing semantics around relevance scoring, summarization eligibility, and review-queue creation unless the change intentionally redefines them.
- When changing provider behavior, preserve provider-agnostic boundaries where they already exist, such as Anymail for inbound and Django mail abstractions for outbound.
- Update docs when pipeline behavior changes in a way a new developer or operator would need to understand.

## Implementation Guidance

- For embedding or vector-search changes, start in `core/embeddings.py` and then verify the downstream callers in `core/pipeline.py` and `core/tasks.py`.
- For newsletter intake changes, start in `core/newsletters.py` or `core/signals.py` and follow the path through `NewsletterIntake`, `IntakeAllowlist`, and `process_newsletter_intake`.
- For project routing or user-facing confirmation behavior, verify both `core/views.py` and top-level URL registration.
- For AI-skill output changes, check how `SkillResult` rows are persisted and how admin or frontend surfaces consume them.

## Validation

- Prefer focused checks first:
  - `pytest core/tests/test_pipeline.py`
  - `pytest core/tests/test_tasks.py`
  - `pytest core/tests/test_newsletters.py`
  - `python manage.py check`
- If a change affects serializers, admin, or API surfaces too, expand validation to the nearest related test module.

## References

- `docs/DEVELOPER_GUIDE.md`
- `docs/RELEVANCE_SCORING.md`
- `docs/LOGGING.md`

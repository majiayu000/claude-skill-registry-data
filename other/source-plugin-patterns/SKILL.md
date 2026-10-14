---
name: source-plugin-patterns
description: "Use when adding or changing ingestion plugins, source configuration validation, RSS or Reddit style fetchers, source health checks, or content ingestion behavior in core/plugins/ and core/tasks.py. Trigger phrases include source plugin, ingestion plugin, add feed source, source config, RSS plugin, Reddit plugin, and health_check."
---

# Source Plugin Patterns Skill

Use this skill when working on the ingestion plugin system.

## Rules

- Plugins should conform to the `SourcePlugin` interface in `core/plugins/base.py`.
- Plugin output should be normalized into `ContentItem` objects.
- Keep plugin-specific config validation in the plugin class and route shared resolution through `core/plugins/registry.py`.
- Register any new plugin type in both the registry and the source-plugin enum used by the data model.
- Ingestion orchestration belongs in `core/tasks.py`, not inside the plugin registry or API layer.
- External network calls should be mocked in tests.

## Implementation Guidance

- Update `core/plugins/base.py` only when the shared plugin contract must change.
- Add or update concrete plugins in `core/plugins/`.
- Update `core/plugins/registry.py` and any related enum or serializer validation paths.
- Confirm `SourceConfig` validation still works through both the serializer and admin paths.
- Add or update focused tests in `core/tests/test_tasks.py`, `core/tests/test_admin.py`, `core/tests/test_serializers.py`, or a new nearby plugin test module.

## References

- `core/plugins/base.py`
- `core/plugins/registry.py`
- `core/plugins/rss.py`
- `core/plugins/reddit.py`
- `core/tasks.py`

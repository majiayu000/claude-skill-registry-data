---
name: growth-engine
description: >-
  Autonomous growth experimentation framework: creates experiments with
  hypotheses, logs data points, runs statistical analysis (bootstrap CI +
  Mann-Whitney U), auto-promotes winners to a living playbook, and suggests next
  experiments. Use when asked to run growth experiments, analyze A/B tests, build
  experiment scorecards, or generate pacing alerts. For SEO-specific experiments
  see seo-ops; for outbound experiments see outbound-engine.
when_to_use: |
  Use when creating or managing A/B or multivariate experiments across any marketing channel, logging experiment data points after content is published, scoring experiments to determine statistical winners, checking a living playbook for proven best practices, generating weekly scorecards across all channels, or monitoring campaign pacing and health.

  Not when: the request is one-off content creation without an experiment framing — apply playbook output directly instead of running the engine. Not when the task is generating or scoring CONTENT/COPY VARIANTS pre-launch (e.g. "A/B test this copy", "score these variants" of a headline or page) rather than running a real experiment with logged data and statistical winners — use `autoresearch`. Not when the focus is SEO-specific experiments — use `seo-ops`. Not when building cold outbound sequences — use `outbound-engine`.
compatibility: Requires Bash (Python 3 where scripts are invoked). Works in Claude Code and Codex via install.sh.
---

# Growth Engine

Autonomous growth experimentation framework based on Karpathy's autoresearch pattern applied to marketing. Creates experiments with hypotheses, logs data points, runs statistical analysis (bootstrap CI + Mann-Whitney U), auto-promotes winners to a living playbook, and suggests next experiments. Supports batch mode (up to 10 variants simultaneously).

## Core Rules

1. Always check the playbook before creating new content — apply proven best practices first.
2. Winner threshold: p < 0.05 AND ≥ 15% lift. Winners auto-promote to the playbook.
3. Use batch mode (`--batch-mode`) for 3-10 variant tests.
4. Run `scripts/pacing-alert.py` to monitor campaign health; exit code 1 = alerts present.
5. Do not run this engine for one-off content creation — apply playbook output directly instead.

## References

- [references/commands.md](references/commands.md) — full CLI reference for all commands with recommended workflow
- [references/configuration.md](references/configuration.md) — required and optional environment variables, pacing alert vars, dependencies

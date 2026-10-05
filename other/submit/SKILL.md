---
name: ha:submit
description: "Home Assistant PR submission — pre-submit verify loop, one-PR-one-thing scope, breaking-change workflow, docs/brands merge gates, answering review + bot findings. Use when preparing, opening, or shepherding a PR to home-assistant/core."
effort: medium
paths:
  - "homeassistant/components/**"
  - "custom_components/**"
  - ".github/**"
---

# Home Assistant PR Submission Reference

Quick reference for preparing and submitting a pull request to `home-assistant/core`.
Getting the code right is only half of it — a mergeable PR is *shaped* right: one
change, green CI, a linked docs PR, an honest `quality_scale.yaml`, and a contributor who
answers every review comment. This is the discipline reviewers gate on.

## Iron Laws — Never Violate These

1. **One PR does one thing (PR1)** — A bug fix and a dependency bump are two PRs;
   dependency bumps are *always* separate and preliminary. A PR does a deprecation OR a
   removal, never both, and in that order. Unrelated changes are reverted; refactors are
   deferred. "Please split the bug fix and the dependency bump into two PRs." — edenhaus,
   https://github.com/home-assistant/core/pull/165959#discussion_r2959065055
2. **Breaking changes follow the full process (PR3)** — A breaking-change section,
   migration via a config-entry minor-version bump (`async_migrate_entry`), a deprecation
   period (a year if users can't self-fix), and a dev-blog post for API changes custom
   integrations can see. "Removing a previously available entity is a breaking change and
   cannot be included in a patch release." — edenhaus,
   https://github.com/home-assistant/core/pull/154137#discussion_r2419783773. Full
   workflow: `${CLAUDE_SKILL_DIR}/references/breaking-changes.md`
3. **Docs and brands are merge gates (PR5)** — A linked home-assistant.io documentation
   PR is required before merge whenever user-facing behavior changes; a new integration
   also needs a brands PR (logo/icon in `home-assistant/brands`). Removals clean up the
   docs and brands repos too. "We need a link before we can merge here." — MartinHjelmare,
   https://github.com/home-assistant/core/pull/161936#discussion_r2848311597
4. **Answer every review comment, including bots (PR6)** — AI/Copilot findings are
   evaluated and replied to like any human comment. "Used AI but didn't test the code" is
   a hard stop that ends the review. "It's fine to use AI, but it's not acceptable… I will
   stop reviewing now." — balloob,
   https://github.com/home-assistant/core/pull/156617#discussion_r2530077696. Etiquette:
   `${CLAUDE_SKILL_DIR}/references/review-process.md`
5. **CI must be green — the tool gates are non-negotiable (PR7)** — ruff + ruff-format,
   mypy (per-component strict opt-in), hassfest, prek, and pytest with coverage all pass
   before you ask for review. "The CI is failing; could you take a look?" — frenck,
   https://github.com/home-assistant/core/pull/147968#pullrequestreview-2989774443

## The Pre-Submit Verify Loop

Run the full loop and get it green *before* opening the PR — reviewers will not start
until CI passes (PR7). Dev-loop order (source: tooling-config.md):

```bash
ruff format .                                        # 88-char format
ruff check . --fix                                   # lint
mypy homeassistant/components/<domain>/              # types (never hand-edit mypy.ini)
python3 -m script.hassfest --domain <domain>         # manifest/strings/icons/quality-scale
prek run                                             # all pre-commit hooks (prek replaced pre-commit)
pytest tests/components/<domain>/ \
  --cov=homeassistant.components.<domain> --cov-report term-missing
# config_flow must show 100% (P15); Silver+ integrations need ≥95% overall.
```

`/ha:verify` runs this loop for you. Fix the source and the yaml, never the generated
outputs (`mypy.ini` is hassfest-generated).

## PR Scope Discipline (PR1)

Before you open it, read your own diff and ask what it *is*:

| Your diff contains | Do this |
|---|---|
| A fix AND a `requirements`/manifest version bump | Split — the bump is its own preliminary PR |
| A fix AND an unrelated refactor / rename / reformat | Revert the unrelated part; defer the refactor |
| A new integration with more than one platform | Keep ONE platform (the primary feature); rest are follow-ups (PR2) |
| A deprecation AND its removal | Two PRs, deprecation first, removal after the period (PR3) |
| Changes across several integrations | One PR per integration unless they are genuinely one change |

A tight, single-purpose PR is what makes review tractable — the same reason new
integrations ship minimal (see `/ha:quality-scale`).

## Quick Decisions

### Is this a breaking change?

| Change | Breaking? |
|---|---|
| Removing/renaming an entity or unique_id | Yes — migration + deprecation + breaking-change section (PR3) |
| Removing/renaming a service action or a field | Yes — deprecation period, then removal |
| Changing the config-entry data shape | Migrate via `async_migrate_entry` + `minor_version` bump |
| Touching a base-entity class or adding a device class | Architecture-repo approval required first (PR4) |
| Adding a new optional field with a safe default | No — but still needs a docs PR if user-facing |

### Which PR do I also need?

| If the PR… | Also open |
|---|---|
| Changes user-facing behavior | A home-assistant.io docs PR (link it) — PR5 |
| Adds a new integration | A `home-assistant/brands` PR + a docs PR — PR5 |
| Changes an API custom integrations depend on | A developer dev-blog post — PR3 |
| Changes an integration's quality tier | An accurate `quality_scale.yaml` diff — PR2 |

## Pre-Submit Checklist

- [ ] The PR does exactly one thing; dependency bumps are a separate PR (PR1)
- [ ] Full verify loop green locally; CI will be green (PR7)
- [ ] `quality_scale.yaml` accurate — every rule's status matches the code (PR2; see `/ha:quality-scale`)
- [ ] `config_flow` at 100% coverage; Silver+ at ≥95% (P15, PR7)
- [ ] A documentation PR is linked in the PR body when behavior changes (PR5)
- [ ] A brands PR exists for a new integration (PR5)
- [ ] Breaking changes have a breaking-change section, migration, and deprecation (PR3)
- [ ] Entity-model / device-class changes have architecture-repo approval linked (PR4)
- [ ] No deprecated APIs introduced (`@bind_hass`, `hass.components`, `hass.helpers`, `SUPPORT_*`, `async_add_job`, `show_advanced_options`)
- [ ] Every existing review comment — human and bot — is answered (PR6)

## PR Body Notes

The PR description is where the merge gates are made visible to the reviewer:

- Link the docs PR (and brands PR for new integrations) — PR5 blocks without it.
- Fill the breaking-change section honestly; a "no breaking change" claim that the diff
  contradicts is a finding (PR3).
- Reference the architecture discussion for any entity-model change (PR4).
- Do not paste AI-generated summaries you have not verified — narrating/filler content is
  flagged (PR6, pairs with P10 dead-code/LLM-filler).

## References

For detailed workflows, see:

- `${CLAUDE_SKILL_DIR}/references/breaking-changes.md` - Breaking-change process, config-entry migration, deprecation clock, architecture gate
- `${CLAUDE_SKILL_DIR}/references/review-process.md` - Answering human + bot review, the tested-code hard stop, CI gates, gh commands

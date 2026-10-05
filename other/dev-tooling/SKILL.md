---
name: ha:dev-tooling
description: "HA core dev-tooling rules — hassfest validator design, script/ utility safety, generated-file discipline, shared test-infrastructure changes. Use when a diff in a core checkout touches script/, hassfest, tests/common.py, or tests/conftest.py."
audience: framework-development
effort: medium
---

# Dev Tooling — hassfest, script/, Shared Test Infrastructure

Rules for changing Home Assistant's *own* development tooling: the `script/`
tree (hassfest validators, scaffold, translations, requirements generation),
shell entrypoints (`script/setup`, `script/lint`), Docker/build tooling, and
the shared pytest infrastructure (`tests/common.py`, `tests/conftest.py`).
This is framework-development territory — the people affected by a bad change
here are *every* core contributor and CI itself, not one integration.

## When This Applies

**Audience gate: framework-development only.** This skill activates in an HA
core checkout (`homeassistant/__init__.py` + `script/` present — same
detection as `/ha:init`). It is never installed for custom-integration
projects (see `docs/framework-dev-laws.md` header).

Load these rules when the diff touches any of:

| Path | What it is |
|---|---|
| `script/hassfest/**` | hassfest validators + generators (run on every core PR) |
| `script/*.py`, `script/<name>/` | dev utilities (`gen_requirements_all`, `scaffold`, `translations`, `split_tests`, …) |
| `script/setup`, `script/lint`, `script/*` shell entrypoints | contributor-facing shell tooling |
| `tests/common.py` | ~2,000-line shared test-helper module used by the entire suite |
| `tests/conftest.py`, `tests/components/conftest.py` | canonical `hass` fixture + ~92 shared fixtures, isolation enforcement |
| `Dockerfile`, `script/hassfest/docker/`, `.github/workflows/ci.yaml` | build/CI tooling |

Command inventory, generated-file map, and the `tests/common.py` helper
lookup table live in `${CLAUDE_SKILL_DIR}/references/script-inventory.md` —
read it before adding a new script or hunting for an existing test helper.

## Iron Laws

1. **A hassfest validator must scale** — it must NEVER require a hassfest
   change per integration feature. Integrations own their own
   strings/schemas; hassfest validates structure, not content.
   (§Hassfest validator design)
2. **No destructive git operations in shared scripts** — `git reset --hard`,
   forced stashing, or anything that discards contributor work is rejected in
   review and blocked at runtime by this plugin's `block-dangerous-ops` hook.
   (§script/ utility safety)
3. **Never hand-edit generated files** — `mypy.ini`, `requirements_all.txt`,
   `requirements_test_all.txt`, `package_constraints.txt`,
   `homeassistant/generated/*`, `CODEOWNERS` are outputs. Change the source
   (manifests, `.strict-typing`, validator code) and regenerate; CI diffs
   freshness and fails on drift. (§Requirements & generated files)
4. **Tooling changes ship with tests too** — C8 applies to `script/` and test
   infrastructure the same as to `homeassistant/` core logic. Uncovered new
   branches block merge. (§Shared-fixture discipline; `docs/framework-dev-laws.md` C8)
5. **`script.translations develop` is the only translations command you run**
   — `upload`/`clean` mutate Lokalise and are maintainer-only. The
   `block-dangerous-ops` hook denies them at runtime. (§Translations tooling)

## Hassfest Validator Design

hassfest (`python3 -m script.hassfest`) runs on every core PR and validates
all ~1,300 integrations' data (manifests, dependencies, requirements,
services, translations, icons, quality scale, discovery generators). Evidence:
`.claude/plans/ha-plugin-conversion/research/dev-tooling-docs.md` §hassfest.

When writing or extending a validator:

- **Scale rule (Iron Law 1)**: if every new integration feature of a given
  kind would need a matching hassfest edit, the design is wrong — move the
  data to the integration's own `strings.json`/schema and validate the
  *shape* generically.
  - "having to update hassfest for every preview feature seems like an
    antipattern" — MartinHjelmare[OHF], 2025-11-21,
    https://github.com/home-assistant/core/pull/156840#discussion_r2548976558
  - "I don't think we need validation in hassfest." — MartinHjelmare[OHF],
    2026-05-18,
    https://github.com/home-assistant/core/pull/169508#discussion_r3262301447
  - Source: review-patterns-core-internals.md §12.2.
- **Not every rule belongs in hassfest**: prefer no validator over a
  validator that duplicates what the runtime, mypy, or an existing schema
  already enforces (§12.2, second citation above).
- **Follow the module anatomy**: one validator module per concern in
  `script/hassfest/` (`manifest.py`, `requirements.py`, `translations.py`,
  …), registered via `__main__.py`; generators emit into
  `homeassistant/generated/*` and never edit integration sources. See the
  module list in `references/script-inventory.md`.
- **Exclude-list hygiene**: keep hassfest/requirements exclude lists minimal
  and current — edenhaus[OHF] enforces exclude-list cleanup
  (review-patterns-core-internals.md, maintainer signatures: edenhaus).
- **Quality-scale records are separate PRs**: a validator or tooling PR never
  bundles quality-scale level changes — "Please update the quality scale in a
  separate PR." — MartinHjelmare[OHF], 2025-07-04,
  https://github.com/home-assistant/core/pull/148104#discussion_r2184380462
  (review-patterns-core-internals.md §12.1).

## script/ Utility Safety

Shared developer scripts run on every contributor's checkout — treat their
working tree as irreplaceable.

- **Never embed destructive git operations** (Iron Law 2): no
  `git reset --hard`, no implicit stash/drop, no history rewriting inside
  `script/` tooling.
  - "resetting hard is not something we should merge here" — frenck[OHF],
    2026-01-12,
    https://github.com/home-assistant/core/pull/160782#discussion_r2683510972
  - "I would strongly recommend you to look into git working trees instead"
    — frenck[OHF], 2026-01-12,
    https://github.com/home-assistant/core/pull/160782#discussion_r2683508303
  - Source: review-patterns-core-internals.md §12.4.
  - Runtime parity: this plugin's `hooks/scripts/block-dangerous-ops.sh`
    denies `git reset --hard` in core/frontend checkouts for the same reason
    — if the hook would block a command interactively, don't write it into a
    script either. Use `git worktree`, `git stash` (explicit, recoverable),
    or `git reset --soft`.
- **No internal third-party APIs in tooling**: scripts consume only public
  APIs of their dependencies — "Internal pip APIs are not part of pip's
  public API" — frenck[OHF], 2025-11-25,
  https://github.com/home-assistant/core/pull/155684#discussion_r2558721516
  (review-patterns-core-internals.md §10.2).
- **New scripts follow the `python3 -m script.<name>` convention** and get an
  entry in the inventory; shell entrypoints stay thin wrappers
  (dev-tooling-docs.md §script/ inventory).

## Build Tooling & Build-Arg Discipline

For `Dockerfile`, `script/hassfest/docker/`, and CI build plumbing
(review-patterns-core-internals.md §12.3):

- **No wrong architecture-dependent defaults** — a build arg whose correct
  value depends on the target arch must have NO default rather than a
  plausible-but-wrong one; fail loud when it's missing.
  - "We should not set default wrong values. Leaving them empty is better" —
    edenhaus[OHF], 2026-03-05,
    https://github.com/home-assistant/core/pull/164756#discussion_r2889278949
  - "If we don't have a default, docker will fail" — edenhaus[OHF],
    2026-03-05,
    https://github.com/home-assistant/core/pull/164756#discussion_r2888678517
- **Harmless args may default for local-dev convenience** — the counterweight:
  "BUILD_REPOSITORY Should have a default set... so it doesn't block when
  building locally" — frenck[OHF], 2026-03-16,
  https://github.com/home-assistant/core/pull/164756#discussion_r2939055061.
  The line: arch-correctness args fail loud; provenance/naming args default
  sanely.

## Requirements & Generated Files

Several checked-in files are *build products* of `script/` tooling. Editing
them by hand guarantees a CI failure (`hassfest`, `gen-requirements-all`, and
`gen-copilot-instructions` jobs diff freshness — dev-tooling-docs.md §Core CI
layout) and, worse, silent overwrite on the next regeneration.

| Never hand-edit | Regenerate with | Source of truth |
|---|---|---|
| `requirements_all.txt`, `requirements_test_all.txt`, `homeassistant/package_constraints.txt` | `python3 -m script.gen_requirements_all` | integration `manifest.json` `requirements` |
| `mypy.ini` | `python3 -m script.hassfest` (the `mypy_config.py` validator generates it) | `.strict-typing` + hassfest config |
| `CODEOWNERS` | `python3 -m script.hassfest` | manifest `codeowners` |
| `homeassistant/generated/*` (bluetooth/dhcp/ssdp/usb/zeroconf/mqtt, config_flows, integrations) | `python3 -m script.hassfest` | manifests + discovery validator modules |
| Copilot/AI instruction file | `python3 -m script.gen_copilot_instructions` | generator script |

- New/changed dependency → rerun `gen_requirements_all` in the SAME PR; the
  dependency ships with the code that uses it, not separately
  ("We don't need a separate PR for adding a new library" —
  emontnemery[OHF], 2025-09-12,
  https://github.com/home-assistant/core/pull/145926#discussion_r2344011236;
  review-patterns-core-internals.md §14.3).
- Fully typing a module? Add it to `.strict-typing`, then regenerate
  `mypy.ini` via hassfest — never append to `mypy.ini` directly
  (dev-tooling-docs.md §Pre-PR checklist).
- Keep generated/managed lists alphabetically sorted where the generator
  expects it — "Please sort 🔡." — MartinHjelmare[OHF], 2026-02-06,
  https://github.com/home-assistant/core/pull/162270#discussion_r2773031977
  (review-patterns-core-internals.md §14.4).

## Shared-Fixture Change Discipline

`tests/common.py` (~2,000 lines of helpers) and `tests/conftest.py`
(~2,265 lines, ~92 fixtures including the canonical `hass` fixture and the
autouse `verify_cleanup`/`garbage_collection` isolation machinery) are load
bearing for the entire test suite — a subtle behavior change ripples through
tens of thousands of tests (dev-tooling-docs.md §Test infrastructure).

- **No hidden magic in shared fixtures** — fixtures do what their name says,
  explicitly; no implicit patching cleverness.
  - "I don't think we should do magic here." — abmantis[OHF], 2025-09-03,
    https://github.com/home-assistant/core/pull/147814#discussion_r2318692456
  - "These lambdas are hard to read." — MartinHjelmare[OHF], 2026-04-10,
    https://github.com/home-assistant/core/pull/165603#discussion_r3066514871
  - Source: review-patterns-core-internals.md §13.1.
- **Coverage per C8** (Iron Law 4): a new helper or a changed fixture is core
  logic — it ships with tests asserting real behavior; enforced by
  emontnemery[OHF], MartinHjelmare[OHF], bdraco[OHF], abmantis[OHF],
  frenck[OHF] (`docs/framework-dev-laws.md` C8;
  review-patterns-core-internals.md §14.2).
- **Search before adding**: `tests/common.py` almost certainly already has
  the mock you want (`MockConfigEntry`, `async_mock_service`,
  `async_fire_time_changed`, `snapshot_platform`, …). Check the lookup table
  in `references/script-inventory.md` before writing a new helper.
- **Changing an existing helper's semantics**: run the affected slice of the
  suite locally (`pytest tests/ -k <helper users>`) and expect
  `pytest-full`'s matrix to surface long-tail breakage; conftest changes
  follow the pytest-asyncio migration conventions already in the file
  (review-patterns-core-internals.md §13.1).
- Placement convention: cross-integration fixture *stubs* go in
  `tests/components/conftest.py`, implementations in the owning domain's
  `common.py` (`.claude/plans/ha-plugin-conversion/research/testing-infrastructure.md`
  §Fixture Sharing Pattern).

## Translations Tooling

`script/translations/` is a Lokalise pipeline (dev-tooling-docs.md
§script.translations):

- **Contributors run exactly one command**:
  `python3 -m script.translations develop` — the local testing loop for
  `strings.json` changes
  (https://developers.home-assistant.io/docs/internationalization/core).
- **`upload` and `clean` are maintainer-only** — they push to / delete from
  Lokalise for all four projects. After a merge to `dev`, strings upload
  automatically; there is no reason for a contributor (or Claude) to invoke
  them. The plugin's `block-dangerous-ops` hook denies
  `script.translations upload|clean` at runtime in core/frontend checkouts —
  mirror that rule when writing tooling: never call the Lokalise-facing
  commands from a script. (Same ownership split as frontend law FI-4:
  retired keys are deleted in Lokalise *by maintainers* —
  `docs/framework-dev-laws.md` FI-4.)

## Verification Before PR

After any dev-tooling change, run in the core checkout:

```bash
python3 -m script.hassfest                 # validators + regenerated outputs
python3 -m script.gen_requirements_all     # if any manifest/dependency moved
prek run --all-files                       # lint hooks (prek, not pre-commit — 2026 CI)
pytest tests/ -k <touched helpers/validators>   # C8: tooling tests too
```

`git status` must show only intended files — regenerated outputs are part of
the diff; unexplained generated-file churn means you edited the wrong layer.
(Commands: dev-tooling-docs.md §Pre-PR checklist, §Test infrastructure.)

## What This Is NOT

- **Not integration testing guidance** — writing tests *for an integration*
  (fixtures, snapshots, config-flow coverage) is the integration-testing
  skill's job; this skill governs changing the shared infrastructure itself.
- **Not CI administration** — workflow secrets, runner config, and Lokalise
  project admin are Open Home Foundation maintainer territory.
- **Not scaffold usage** — `python3 -m script.scaffold integration` as a
  consumer belongs to integration authoring; editing scaffold *templates* is
  in scope here (they're shared tooling: Iron Laws 2–4 apply).

## References

- `${CLAUDE_SKILL_DIR}/references/script-inventory.md` — script/ command
  table, hassfest validator modules, generated-file map, tests/common.py
  helper lookup, CI job map
- `.claude/plans/ha-plugin-conversion/research/dev-tooling-docs.md` — primary
  docs evidence (official-docs authority, code-observed)
- `.claude/plans/ha-plugin-conversion/research/review-patterns-core-internals.md`
  §12 (script/ & hassfest), §13 (test infrastructure), §14 (PR hygiene)
- `.claude/plans/ha-plugin-conversion/research/testing-infrastructure.md` —
  shared fixture/conftest patterns
- `docs/framework-dev-laws.md` — C-series laws (C2, C8) and roster-tag
  semantics ([OHF]/[UNVERIFIED])
- `hooks/scripts/block-dangerous-ops.sh` — runtime enforcement of Iron Laws 2
  and 5

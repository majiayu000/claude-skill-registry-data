---
name: litestar-styleguide
description: "Use when authoring Litestar skill content, Python/TypeScript examples, PEP 604, async I/O, Google docstrings, ruff/mypy/pyright, pytest, or CI rules. Not for focused Litestar APIs."
---

# litestar-styleguide

This is the **shared style baseline** that every other skill in this plugin references. It exists so that cross-cutting rules (PEP 604 unions, async I/O, ruff + mypy + pyright + prek, test file naming, CI/CD conventions) live in exactly one place — and individual skills stay focused on their framework or tool-specific surface.

## Code Style Rules

- **Terse, imperative, authoritative.** State the preferred choice and a one-line `Reason:`; never hedge ("you might want to…").
- **PEP 604 unions (`T | None`) and PEP 585 generics (`list[T]`, `dict[K, V]`).** Never use `typing.Optional`, `typing.Union`, `typing.List`, or `typing.Dict`.
- **`from __future__ import annotations` is a library-author guardrail, not a consumer rule.** Application code (handlers, services, tests) MAY use it; avoid it only in modules defining runtime-introspected types (`msgspec.Struct`, SQLAlchemy `Mapped[...]`, Dishka `@provide`, SAQ `@task`).
- **Async all I/O, Google-style docstrings, function-based pytest tests (`@pytest.mark.anyio`).**
- **Litestar first-party stack bias with match-your-stack flexibility.** Prefer `msgspec`, `advanced-alchemy` / `sqlspec`, `litestar-granian`, `litestar-saq` / `litestar-queues` when starting fresh, and match the user's existing stack when present.

## Quick Reference

| Slice | Reference File | Key Topics |
| --- | --- | --- |
| Cross-language principles | [`references/general.md`](references/general.md) | Simplicity over cleverness, boundary validation, naming, import order |
| Python conventions | [`references/python.md`](references/python.md) | PEP 604/585, `msgspec.Struct`, async I/O, docstrings, `ruff`, `mypy`, `pyright`, `prek` |
| Litestar baseline | [`references/litestar.md`](references/litestar.md) | Typed markers (`FromPath`, `FromQuery`, `NamedDependency`, `SkipValidation`), `Provide` vs Dishka, `MsgspecDTO`, Guards, plugins |
| TypeScript conventions | [`references/typescript.md`](references/typescript.md) | Strict `tsconfig`, discriminated unions, named exports, `oxlint` / `biome` |
| Testing conventions | [`references/testing.md`](references/testing.md) | `pytest` + `anyio`, `AsyncTestClient` lifespan fixtures, Vitest, 90%+ coverage |
| CI/CD conventions | [`references/ci-cd.md`](references/ci-cd.md) | GitHub Actions with `setup-uv`, `prek` / `.pre-commit-config.yaml`, matrix builds |
| Canonical reference apps | [`references/canonical-apps.md`](references/canonical-apps.md) | `litestar-fullstack-inertia`, `litestar-fullstack`, `litestar-sqlstack`, `oracledb-vertexai-demo` |
| Google Developer Knowledge MCP | [`references/google-developer-knowledge-mcp.md`](references/google-developer-knowledge-mcp.md) | Opt-in MCP setup for fresh GCP / Firebase / Maps documentation |

### How sibling skills consume this

Every `SKILL.md` in this plugin has a `## Shared Styleguide Baseline` section near the bottom. That section links to a subset of these references — only the ones that apply to the skill's language / framework mix. For example:

- `skills/litestar/SKILL.md` links to `general.md` + `python.md` + `litestar.md`
- `skills/litestar-vite/SKILL.md` links to `general.md` + `typescript.md` + `litestar.md`
- `skills/litestar-testing/SKILL.md` links to `general.md` + `testing.md` + `python.md` + `litestar.md`

The sibling skill extends the baseline with its own tool-specific Code Style Rules, Quick Reference, Guardrails, and Validation — but it does not duplicate the baseline. If a convention is generic (type hints, naming, imports), it belongs here.

### When to update this skill

- A rule becomes contentious across two or more sibling skills → pull it into the right baseline reference file here.
- A new language lands (Rust, Mojo, etc.) → add a new `references/<lang>.md` and link from skills that use it.
- A tool is swapped out (e.g., ruff replaces flake8 + black, `prek` replaces `pre-commit` CLI) → update `python.md` / `ci-cd.md` once; all sibling skills inherit it.

<workflow>

## Workflow — consuming this baseline

1. Open the sibling skill you are editing (`skills/<name>/SKILL.md`).
2. Look at its `## Shared Styleguide Baseline` section — it already lists a subset of the references here.
3. When adding a rule to the sibling, ask: is it generic (language/tooling) or framework-specific? Generic → land it in the right file under `references/` here. Specific → keep it in the sibling.
4. Cross-link bidirectionally if a rule here is amplified in the sibling.

</workflow>

<guardrails>

## Guardrails

- **No duplication across skills.** A rule lives in exactly one file; sibling skills link to it.
- **No folklore.** Every rule has a one-line justification (perf, runtime introspection, OpenAPI alignment, etc.). Delete rules you cannot justify.
- **Terse and imperative.** Bullets are ≤ 2 sentences. If a topic needs more, split it into its own reference file.
- **Examples are minimal and copy-pasteable.** No pseudo-code; no multi-hundred-line fixtures.

</guardrails>

<validation>

## Validation Checkpoint

- [ ] Every sibling skill's `## Shared Styleguide Baseline` section resolves to files that exist under `references/`
- [ ] No rule is duplicated between two reference files (check via grep when editing)
- [ ] Each "never do X" rule has a one-line `Reason:` explanation
- [ ] New language support lands as a single new `references/<lang>.md` — not scattered into sibling skills

</validation>

<example>

## Example — adding a new rule

A reviewer finds that two sibling skills independently wrote "use `ruff format` not `black`". Instead of leaving duplicates, pull the rule into `references/python.md`:

```markdown
- **Use `ruff format`, never `black`.** Reason: ruff is the single toolchain for
  lint + format; running two formatters produces style drift.
```

Then in each sibling's `SKILL.md`, replace the duplicate with a pointer:

```markdown
## Shared Styleguide Baseline

- [Python](../litestar-styleguide/references/python.md)
```

</example>

## References Index

- [General Principles](references/general.md)
- [Python](references/python.md)
- [Litestar](references/litestar.md)
- [TypeScript](references/typescript.md)
- [Testing](references/testing.md)
- [CI/CD](references/ci-cd.md)
- [Canonical Reference Apps](references/canonical-apps.md)
- [Google Developer Knowledge MCP](references/google-developer-knowledge-mcp.md)

## Official References

- <https://peps.python.org/pep-0604/> — PEP 604 union syntax
- <https://docs.astral.sh/ruff/> — ruff linter / formatter
- <https://docs.astral.sh/uv/> — uv package and environment manager
- <https://mypy.readthedocs.io/en/stable/> — mypy static type checker
- <https://microsoft.github.io/pyright/> — pyright type checker
- <https://docs.pytest.org/> — pytest

## Shared Styleguide Baseline

- [General Principles](references/general.md)
- [Python](references/python.md)
- [Litestar](references/litestar.md)
- [TypeScript](references/typescript.md)
- [Testing](references/testing.md)
- [CI/CD](references/ci-cd.md)

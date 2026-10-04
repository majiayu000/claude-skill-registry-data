---
name: phxstack-elixir
description: Elixir, Phoenix, LiveView, Ecto, Oban, and OTP conventions. Use when reading or editing .ex, .exs, .heex, or mix.exs, running mix, or working on schemas, changesets, contexts, LiveViews, workers, or supervision trees.
---

# phxstack-elixir

Reference for Elixir web work. Load the one page the task needs, not the set.

| Load | When the task touches |
|---|---|
| [`reference/otp.md`](reference/otp.md) | Processes, supervision, concurrency, pattern matching, errors, type system |
| [`reference/ecto.md`](reference/ecto.md) | Schemas, changesets, queries, migrations, transactions |
| [`reference/liveview.md`](reference/liveview.md) | LiveViews, components, forms, uploads, streams, navigation |
| [`reference/contexts.md`](reference/contexts.md) | Contexts, scopes, plugs, routers, controllers, JSON APIs |
| [`reference/oban.md`](reference/oban.md) | Workers, queues, retries, unique jobs, idempotency |
| [`reference/testing.md`](reference/testing.md) | ExUnit, database test isolation, Mox, factories, LiveViewTest |
| [`reference/security.md`](reference/security.md) | Authentication, authorization, validation, rate limiting, headers |
| [`reference/verify.md`](reference/verify.md) | Project-specific compile, format, static analysis, and tests |

`phxstack-build` and `phxstack-check` use `reference/verify.md` to discover
the repository's real checks. For UI work, pair LiveView guidance with the
installed `impeccable` skill.

For Ash projects, use Ash forms and changesets where the project uses Ash;
reach for Ecto guidance only where direct `Ecto.Changeset` work remains.

Adapted from [claude-elixir-phoenix](https://github.com/oliver-kriska/claude-elixir-phoenix)
by Oliver Kriska (MIT).

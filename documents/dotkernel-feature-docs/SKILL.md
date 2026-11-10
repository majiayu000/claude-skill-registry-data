---
name: dotkernel-feature-docs
description: >
  Use when writing down what a feature does and why in a Dotkernel project — after building or
  changing a route, module, command or entity, when asked to document a feature, write release
  notes, record a decision, explain an endpoint to another developer, or bring an existing feature
  doc back in line with the code. Also use when a feature exists but nothing outside the code
  explains it, when a doc still describes behaviour that has since changed, and before adding
  behaviour to an area that already has a feature doc.
---

# Feature documentation

```text
Applies to
  Projects:  - all
  Packages:  - none
```

Code records *what* a project does. A feature doc records *why*, plus the four things that are
spread across four files — the routes, the roles allowed to reach them, the data added, and how to
exercise it. That is the part a fresh session cannot reconstruct by reading `src/`, and the part
lost when a session is cleared.

One doc per **feature**, never per commit and never per route. Two routes that only make sense
together belong in one doc.

## Where it goes

Detect before writing. Some Dotkernel repositories already own a `documentation/` directory,
holding some mix of `command/*.md`, a generated `openapi.json` and Postman collections. Among the
stock projects only the API ships one, but derived projects add or drop it freely — check, do not
infer it from the project type:

```bash
ls -d documentation docs 2>/dev/null
```

| Repo already has | Write to |
| --- | --- |
| `documentation/` | `documentation/features/` |
| `docs/` | `docs/features/` |
| neither | create `docs/features/` |

Never create a second documentation root next to an existing one. Filename is
`YYYY-MM-DD-<kebab-slug>.md`, the date being the day the doc is written — sortable, and it makes
the reading order obvious. The directory also carries a `README.md` index, one row per doc.

## The template

```markdown
---
feature: Book reviews
date: 2026-08-05
variant: dotkernel/api
status: shipped
modules: [Book]
routes:
  - POST /book/{id}/review
handlers:
  - Api\Book\Handler\Book\Review\PostBookReviewResourceHandler
---

# Book reviews

## Why

Two or three sentences: the need, and the constraint that shaped the approach. The one section
that cannot be recovered by reading the code.

## Surface

| Route | Name | Handler | Roles |
| --- | --- | --- | --- |
| `POST /book/{id}/review` | `book::create-review` | `PostBookReviewResourceHandler` | `user` |

## Data

Entities and columns added or changed — in `Core` for API and Admin, in the module's own `Entity/`
for Frontend. Migration required: yes / no — and the command, not run.

## Config

Authorization entries, ConfigProvider registrations, new config keys, and where their secrets
live (`*.local.php`, never committed).

## Testing

What is covered, and how to run just this feature's tests.

## Follow-ups

Known gaps, deferred decisions, anything a reviewer waved through.
```

The frontmatter is the machine-readable part: `/dk-review` greps `routes:` and `handlers:` to
decide whether a change is documented. Keep both accurate or the staleness check silently passes.
`status` is one of `planned`, `shipped` or `deprecated`.

## Writing it from the code, not from memory

Every claim in the doc is read from somewhere. Where it came from:

| Section | Source of truth |
| --- | --- |
| Routes and route names | the module's `RoutesDelegator` |
| Roles | `authorization.global.php` (API); Admin / Frontend: the permission in `authorization-guards.global.php`, then the roles holding it in `authorization.global.php` |
| Handler class and path | the filesystem under `src/<Module>/src/Handler/` |
| Registrations | the module's `ConfigProvider` |
| Data and migration need | changed entities under `src/Core/` (API, Admin); Frontend: the module's own `Entity/`; Light and Queue: none |
| Testing | the test files that actually exist |

An undocumented gap is better than an invented fact. If something could not be verified — the role
mapping is unclear, the migration status is unknown — write `unverified` and say which file to
check, rather than asserting the plausible answer. A wrong feature doc is consulted with the same
confidence as a right one.

## What a feature doc is not

- **Not an API reference.** In a project that publishes OpenAPI, `OpenAPI.php` is the contract
  (see `dotkernel-openapi`). Name the operation, do not restate its schemas — two descriptions of
  one payload diverge, and the generated one wins.
- **Not a changelog.** No per-release history, no version bumps. The doc describes the feature as
  it is now; `git log` holds how it got there.
- **Not a code dump.** Reference `src/Book/src/Handler/…` by path. Pasted bodies go stale silently
  and the real thing is one grep away.
- **Not a design proposal.** A doc with `status: planned` states what is intended and says so; it
  does not describe intent in the past tense.

## Keeping it current

Update in place when the same feature changes — new route on an existing resource, a role added, a
field renamed. Add a new doc only when the feature is genuinely new. Refresh the `README.md` index
row in the same edit.

A breaking change handled through `dotkernel-evolution-pattern` touches the doc twice: `status`
becomes `deprecated` with the sunset date and the replacement named in Follow-ups when the
deprecation lands, and the doc is removed only once the route is gone.

## Security constraints

- **Never** put a real credential, token, internal hostname, customer email or production
  identifier in an example. Use obvious placeholders. Documentation is the artefact most likely to
  be copied into a ticket, a chat or a public repository.
- Name where a secret lives (`config/autoload/*.local.php`), never its value.
- Do not document an internal-only route in a way that implies it is a public surface.

## Definition of done

- [ ] Written to the features directory this repo actually uses, not a new one.
- [ ] Filename `YYYY-MM-DD-<kebab-slug>.md`; frontmatter parses; `status` accurate.
- [ ] `routes:` and `handlers:` list every route and handler the feature added.
- [ ] Every route name in the Surface table matches `RoutesDelegator`, and every role matches this
      variant's authorization config.
- [ ] Every file path and class name in the doc resolves.
- [ ] `Why` explains a constraint, not the mechanics — the mechanics are in the code.
- [ ] Migration need stated, and the command given rather than run.
- [ ] No credential, token, internal hostname or real customer data anywhere in it.
- [ ] `README.md` index row added or updated.

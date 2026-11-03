---
name: ddd-symfony
description: >
  Domain Driven Design in Symfony, three modes. PLACE: decide which building block (entity, value
  object, aggregate, domain service, event, repository, command, application service), layer and
  folder a piece of logic belongs in. BUILD: implement a use case or aggregate through the layers
  in order (Domain → tests → Application → Infrastructure). AUDIT: scan a Symfony codebase for
  DDD violations (framework leaks in the Domain, anemic models, business rules in services, wrong
  repositories, events dispatched before commit) and prescribe fixes by rule id. Use whenever the
  user mentions DDD, aggregate, value object, bounded context, domain event, domain service, or
  asks "where does this go" / "DDD audit" in a Symfony project.
---

# DDD in Symfony

Business rules live in plain PHP in the **Domain**. Use cases live in the **Application**.
Symfony, Doctrine and Messenger live in **Infrastructure** as replaceable adapters.
Dependencies point inward, always.

Building-block templates: `references/building-blocks.md`. Our default Symfony/Doctrine setup:
`references/symfony-wiring.md`. Audit rules: `references/audit-checklist.md`.

## Step 0 — Read the project (every mode)

1. **Versions.** Read `composer.lock` for `symfony/framework-bundle`, `doctrine/orm`,
   `doctrine/doctrine-bundle`, `doctrine/persistence` and the PHP constraint. Generated code must fit
   the installed versions. If they're newer than the "Verified on" line in `symfony-wiring.md`,
   check the UPGRADE notes for what you're about to use.
2. **Existing patterns.** Detect, in this order:
   - the context folders (`src/<Context>/{Domain,Application,Infrastructure}` or similar)
   - the Doctrine mapping type and its location (`config/packages/doctrine.yaml`)
   - how events are raised (an in-entity publisher, recorded events pulled from the aggregate, or none)
   - the command/handler naming (`*Command` + `*Service::execute()`, or Messenger handlers)
   - the id type, the test setup and the quality gates (PHPStan, PHPUnit/Pest, CS fixer)
3. **Follow the project when a pattern exists; use our defaults only when none does.** State which
   one you used in one line ("Following the project's XML mapping" / "No mapping found, using
   PHP closure mapping").

Consistency with the codebase beats our preference. Never mix two styles in one context.

## PLACE mode

Answer with: **building block → layer → path**, plus one sentence of why. Decide in this order:

1. **Can the entity do it?** A rule about one aggregate's own state → a method on the aggregate root.
2. **Is it a value with rules and no identity?** → a Value Object (immutable, self-validating).
3. **A business rule that needs other aggregates or outside data?** → a Domain Service in the
   Domain. It talks to ports only, and its name comes from the domain language.
4. **Running one use case** (load, call the domain, save, transaction)? → an Application Service.
5. **Technical work** (DB, mail, HTTP, queues)? → Infrastructure, behind a port.

Something another context must react to → a Domain Event. It crosses contexts through Messenger
and carries ids, never entities.

## BUILD mode

Always in this order. Stop and show the plan first if the change touches more than one aggregate.

1. **Domain:** the aggregate/VO/service/event and the repository port. Rules are enforced in
   constructors and methods. Use the ubiquitous language from requirements or the user's words.
2. **Domain tests:** plain PHPUnit/Pest, no kernel, no DB. One test per business rule, including
   the failure path.
3. **Application:** a Command (primitives only) + an Application Service (`execute()`), tested with
   an in-memory repository.
4. **Infrastructure:** the Doctrine adapter, the mapping, the wiring (`#[AsAlias]`), the delivery
   (controller/console/handler) only if asked.
5. **Gates:** run the project's existing gates. Then run
   `grep -rE 'use (Symfony|Doctrine\\ORM)' src/<Context>/Domain`, which must print nothing (DDD-1).

Generate core code only. No speculative ports, no factories with one product, no CQRS read
models unless asked.

## AUDIT mode

Read-only. Go through `references/audit-checklist.md` over the scope given (default: `src/`).
Report each finding as:

`DDD-n · file:line · what's wrong · the fix`

Rank by risk (broken invariants and event-before-commit first, style last). End with a short
summary: the counts per rule and the 3 fixes with the best payoff. Don't edit code in this mode.

## Hard rules

- The Domain imports no Symfony and no Doctrine ORM (`doctrine/collections` is allowed).
- Aggregate methods return `void`. State changes only through intention-revealing methods: no
  setters, no public mutation.
- One repository per aggregate root. No `flush()` inside repositories; the transaction belongs to
  the application layer.
- Application services hold no business `if`s and never return entities (a DTO, an id or nothing).
- Domain events are raised inside the Domain and dispatched to other contexts **only after
  commit**.
- Commands carry primitives and have no `#[Assert]`. The Domain validates.
- Cross-context references are ids, never object references.
- Ask before introducing DDD into a context that doesn't use it. DDD is for real business rules;
  simple CRUD stays plain Symfony.

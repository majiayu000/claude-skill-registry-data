---
name: ground-laravel
description: Laravel philosophy. Convention over config. Eloquent as truth. Invoke ONCE when entering Laravel context.
---

# Skill: Laravel Philosophy

> "The framework is your friend. Don't fight it."

## The Standard

- **Convention Over Configuration**: Follow Laravel defaults. Custom only when necessary.
- **Eloquent as Truth**: Models own their domain. Don't abstract around the ORM.
- **Thin Controllers**: Controllers route and orchestrate. Actions execute business logic.
- **Batteries Included**: Use Laravel features before packages before custom code.
- **Named Parameters**: Use named arguments for all calls with 2+ parameters. Closures included. Positional args obscure intent.

## The Check

Stop and reconsider if:
- Writing a repository that wraps Eloquent
- Fighting against implicit model binding
- Creating custom solutions for things Laravel provides (gates, policies, events)
- Bypassing Eloquent "for performance" without measuring
- Building a "service layer" that just calls model methods
- Using positional arguments for calls with 2+ parameters

## The Protocol

Before writing any Laravel code:
1. **Check Laravel**: Does the framework solve this natively?
2. **Check Spatie**: Did they already build a well-tested package?
3. **Check Project**: How did we solve similar problems here?
4. **Only Then**: Write custom code.

## The Ecosystem

Trust these conventions:
- Naming: `UserPolicy`, `OrderObserver`, `SendInvoice` (VerbNoun for Actions)
- Config: `config()` over `env()` in application code
- Structure: Follow Laravel's file structure unless documented otherwise
- Packages: Spatie packages are battle-tested — prefer them over custom solutions

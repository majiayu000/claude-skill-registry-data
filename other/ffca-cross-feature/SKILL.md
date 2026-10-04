---
name: ffca-cross-feature
description: >
  Cross-feature dependencies in FFCA: the Summary pattern, Queries that combine repositories,
  sharing widgets between features, widget slots, and composing features. Use in an FFCA monorepo,
  a features/ folder whose packages are named {feature}_domain, {feature}_data, and
  {feature}_presentation, when one feature needs data, behavior, or a widget from another, when
  sharing models or widgets across features, or when choosing between a Query, a widget slot, and a
  new composing feature. Triggers on "feature A needs data from feature B", "can cart import
  checkout", "share this model between features", "reuse this widget in another feature", "how do
  features talk to each other", "should this be a use case or a new feature", "combine two
  repositories", and "avoid a circular dependency between features". If the repo instead uses
  packages/ with _repository and _api_client packages, defer to vgv-ai-flutter-plugin's
  layered-architecture skill.
allowed-tools: Read Glob Grep
effort: high
---

# FFCA Cross-Feature

Workflow for the moment one feature needs another. The patterns live in `${CLAUDE_PLUGIN_ROOT}/references/ffca/`: read the cited sections before coupling two features.

## The two allowed couplings

Features couple in exactly two places, and in one direction each:

- **Domain to domain.** A consuming feature's domain may depend on a provider feature's domain, for example `cart_domain` on `product_domain`. Read `references/ffca/domain.md`, section *Composing features*.
- **Presentation to presentation.** A presentation package may use a public widget from another feature's presentation package, under the three conditions below. Read `references/ffca/presentation.md`, section *Sharing a widget across features*.

Data layers never reach across features for data, and no layer ever depends on another feature's data package.

## Sharing data

1. **Loose coupling by id: the Summary pattern.** When a feature stores references to another feature's models, store ids only. The read model holds full objects (`Cart` with `List<Product>`); the stored summary holds ids (`CartSummary` with `List<String>`). The repository reads and writes summaries and only takes the full object when one is being created. Read `references/ffca/domain.md`, section *Storing data*, and adapt the shapes in `references/code_templates/domain_templates.md`.
2. **Combine repositories with a Query.** To assemble a populated model from two features, add a `Query` in the consuming feature's domain that takes both repository interfaces. Read `references/ffca/domain.md`, section *Reading the populated object*. Keep the Query in the consumer, never in the provider: the cart feature never learns how products are stored, and the product feature never learns that carts exist.
3. **Normalize inside the repository, not a Query.** When an API returns nested objects belonging to another feature, split them inside the data repository, which may depend on another feature's domain interface. Read `references/ffca/faq.md`, section *Dealing with nested objects*. The DTO-to-domain mapping is duplicated in the consuming data package on purpose: DRY is traded for bounded contexts here deliberately.

Do not call these classes "use cases". They are Commands and Queries. See `references/ffca/domain.md`, section *Business rules*.

## Sharing a widget

A widget that owns a `Cubit` is not a separate feature. It lives in its own feature's presentation package and is exported through a barrel. Two ways to get it onto another feature's screen, and the choice is about who places it.

**Direct import behind a narrow barrel.** Three conditions, all from `references/ffca/presentation.md`, section *Sharing a widget across features*:

- The widget gets its own barrel. Consumers import `package:cart_presentation/cart_badge.dart`, never the primary `cart_presentation.dart` barrel.
- The barrel stays narrow. Its transitive imports must not reach the feature's modules or screens. Going through the primary barrel costs the consumer every screen and Cubit the feature owns, and it breaks deferred loading downstream.
- No cycles. If two features each need a widget from the other, extract the shared part downward into a third package instead of importing sideways.

**A slot the app fills.** The consuming feature never learns the other feature exists: it declares a nullable `Widget` parameter and the app supplies it. Same inversion as navigation. Name the slot for its position (`trailingAction`), default it to nothing, and stop at two slots per module. Read `references/ffca/presentation.md`, section *Or let the app place it*.

**Choosing.** Use a slot when the widget is app chrome, such as a cart badge in an app bar, which belongs to the shell rather than to the screen around it. Use a direct import when the widget is genuinely part of what the consuming screen *is*. Read `references/ffca/presentation.md`, section *Choosing between them*.

## Where a shared widget should live

When the same widget is wanted in more than one feature, work through `references/ffca/presentation.md`, section *Where the widget should live*, in order:

1. **Does it need a repository or a domain type?** If not, it is a pure presentational component and belongs in `ui_kit`. This test is mechanical, not stylistic: shared packages depend on external packages only, so a widget that needs a repository cannot compile there.
2. **If it does, split it.** The view taking a plain count goes in `ui_kit`; the Cubit plus that view stays in its feature behind its own barrel. A widget that genuinely gets reused across features is usually a presentational leaf with the stateful part left behind, which means the pressure was pointing at `ui_kit` all along.

## When a Query is not enough: compose a feature

If multi-domain logic grows its own models, screens, or lifecycle, create a feature for it. Read `references/ffca/overview.md`, sections *Features* and *Presentation-only features*. A feature that composes several other domains into a screen without owning business logic is a presentation-only feature: a `{name}_presentation` package with no domain or data sibling, depending on the other features' domains.

## Identity versus entity

Auth and user profile are separate domains, not one. Read `references/ffca/faq.md`, section *How do I handle auth and user profiles?* Keep `AuthUser` in `auth_domain` and `UserProfile` in `user_profile_domain`, and glue them with a Query in the consuming domain, so a new profile field never forces a change to auth.

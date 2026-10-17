---
name: rails-action-view
description: Use when designing, implementing, reviewing, testing, or optimizing Rails Action View rendering, templates, partials, layouts, helpers, strict locals, output safety, localized views, and rendering performance. Also covers routine ERB templates, partials, helpers, and forms.
license: MIT
---

# Rails Action View Engineering

## Purpose

Treat Action View as a response-rendering subsystem with explicit contracts for data boundaries, HTML safety, template composition, localization, caching interaction, and rendering performance.

This skill owns Action View-specific runtime behavior as well as routine template, partial, helper, and form changes.

Compose with:

- rails-action-view for presentation responsibility and basic template/form conventions;
- rails-action-controller for controller/render/redirect response semantics;
- rails-i18n for locale resolution and localization context;
- rails-action-text for persisted rich text;
- rails-caching for fragment/cache correctness;
- rails-performance and ruby-performance for evidence-driven rendering optimization;
- rails-security and rails-security-engineering for XSS, content safety, authorization, and privacy;
- rails-test-engineering and rails-test-engineering for deterministic rendered-output verification.

Current Rails documents Action View as the response-rendering layer used with Action Controller, covering templates, partials, layouts, helpers, and localized views. Modern Rails also supports strict local signatures for partials and template-specific rendering contracts. Sources are listed below.

Core flow:

    controller/domain-prepared data
    -> template lookup
    -> layout/partial composition
    -> helper execution
    -> escaping/sanitization/output safety
    -> optional fragment caching
    -> rendered response

## Activate when

- changing ERB or other Action View templates;
- designing partial/layout boundaries;
- introducing strict local signatures;
- adding or refactoring view helpers;
- diagnosing escaped HTML, XSS, or html_safe behavior;
- changing localized views;
- optimizing repeated partial rendering or collection rendering;
- debugging template lookup or rendering failures;
- changing fragment/collection caching from a view;
- reviewing presentation code for hidden queries or side effects.

Do not replace rails-action-view with this skill for simple view edits that do not involve an Action View runtime concern.

Ordinary template, form, or partial edits also route here; start them from `references/routine-changes.md`.

## Repository inspection

Inspect before implementing:

1. Rails and Action View versions;
2. template engines and extensions in use;
3. app/views structure and naming;
4. layouts, partial, collection, and object-rendering conventions;
5. helper modules and whether logic is shared globally or by controller namespace;
6. existing presenters/view models/decorators;
7. sanitizer/output-safety conventions;
8. localized view conventions and rails-i18n usage;
9. fragment/cache conventions and cache key policy;
10. request/system/view tests and snapshot/golden-output conventions.

Search for an existing local solution before introducing a new helper, presenter, rendering abstraction, or partial hierarchy.

## Decision rules

1. Classify the change: rendering boundary and template lookup, partials/strict locals/layouts, helpers/forms/output safety, localization, rendering performance and caching, or security and testing.
2. Load the matching reference below before changing behavior. Ordinary template, form, partial, or helper edits load `references/routine-changes.md` first and escalate only when a deeper boundary is in play.
3. Keep views presentation-only: queries, authorization, and domain decisions happen before rendering.

## Critical invariants

- Do not use locale-specific templates as an authorization mechanism.
- Never mark user input HTML-safe merely because it is expected to contain markup.
- Never cache a private fragment under a key shared across tenants or authorization scopes.
- Do not make ordinary rendering tests depend on external network services.

## References

Load only the reference for the boundary being changed, before changing behavior there. Each reference is self-contained and one level deep; none links to another. Consult a listed pattern from the pattern catalog only when the change needs its implementation shape.

| Load when | Reference | Covers | Patterns |
|---|---|---|---|
| a change alters what a view renders, template lookup, partial contracts, strict locals, or layouts | [references/rendering-and-templates.md](references/rendering-and-templates.md) | Rendering boundary; Template and lookup contract; Partial contract; Strict locals; Layout boundary | `action-view-partial-contract`, `action-view-strict-locals`, `action-view-layout-contract` |
| a change adds or alters helpers, forms or tag helpers, html_safe/raw/sanitize, or localized templates | [references/helpers-forms-safety.md](references/helpers-forms-safety.md) | Helper boundary; Forms and tag helpers; Output safety and sanitization; Localization | `action-view-helper-boundary`, `action-view-output-safety`, `action-view-localized-template` |
| a change has rendering-performance, fragment-caching, security/privacy, or view-test impact | [references/performance-caching-security-testing.md](references/performance-caching-security-testing.md) | Rendering performance; Caching interaction; Security and privacy; Testing | `action-view-render-performance`, `action-view-testing` |
| the change is a routine template, partial, helper, or form edit | [references/routine-changes.md](references/routine-changes.md) | Routine view, partial, helper, and form changes | none |

## Reference example

A helper with explicit arguments and content-safe tags, plus the strict-locals partial call that keeps template contracts checkable.

```ruby
module InvoicesHelper
  # Helpers take the object as an argument; they never read controller ivars.
  def invoice_status_badge(invoice)
    tag.span(class: "badge badge--#{invoice.status}") do
      t(invoice.status, scope: "invoices.status")
    end
  end

  def money(cents, currency:)
    number_to_currency(cents / 100.0, unit: currency.to_s.upcase + " ")
  end
end

# Template call sites:
#   <%= invoice_status_badge(@invoice) %>
#   <%= render "invoices/line_item", line_item: item, strict_locals: true %>
# strict_locals: true turns a typo in a partial local into a raise, not a silent nil.
```

## Agent review checklist

- [ ] Rails/Action View version resolved
- [ ] existing rails-action-view conventions inspected
- [ ] template lookup/format/variant contract explicit
- [ ] partial inputs explicit
- [ ] strict locals used where justified
- [ ] layout responsibility remains presentation-only
- [ ] helper responsibility remains presentation-focused
- [ ] no hidden database/network side effects in templates
- [ ] output escaping/sanitization reviewed
- [ ] raw/html_safe usage justified
- [ ] form security semantics preserved
- [ ] locale/fallback behavior explicit when applicable
- [ ] view cache identity includes correctness/security dimensions
- [ ] rendering performance measured before optimization
- [ ] deterministic rendering tests exist
- [ ] security regression coverage exists for untrusted HTML/URLs

## Anti-patterns / failure modes

- query loops inside templates;
- authorization logic embedded only in ERB;
- raw or html_safe used on user input;
- global sanitizer allowlist expansion for one template;
- helpers performing domain workflows;
- layouts performing data mutations;
- partials depending on undocumented instance variables;
- excessive partial nesting;
- strict locals added without stable callers;
- localized templates duplicating business logic;
- fragment caches missing locale/tenant/permission identity;
- full-page snapshots replacing focused rendering contracts;
- optimizing view code without query/render evidence.

## Verification

For an Action View change:

    version/runtime evidence
    -> template lookup
    -> data/input contract
    -> partial/layout/helper boundary
    -> output safety
    -> locale
    -> cache identity
    -> rendering performance
    -> focused tests
    -> security regression
    -> regression suite

For a rendering bug distinguish:

    controller data
    -> lookup
    -> layout
    -> partials
    -> helpers
    -> escaping/sanitization
    -> cache
    -> final response

Never claim a view is safe because it comes from ERB or a helper is safe because it returns a string. Verify escaping, sanitization, authorization boundaries, and cache isolation where applicable.

## Rails 8.1 current framework considerations

- Rails 8.1 supports Markdown rendering through the response/rendering stack. Treat Markdown as a negotiated representation with explicit content type, escaping/sanitization, and caching semantics.
- Inspect whether the repository uses Markdown as trusted source, sanitized user content, or generated output before selecting a rendering path.

## Source foundation

Primary Rails sources:

- https://guides.rubyonrails.org/action_view_overview.html
- https://guides.rubyonrails.org/action_view_helpers.html
- https://guides.rubyonrails.org/form_helpers.html
- https://guides.rubyonrails.org/caching_with_rails.html
- https://api.rubyonrails.org/v8.1.3/classes/ActionView/Helpers/SanitizeHelper.html
- https://api.rubyonrails.org/classes/ActionView/Helpers/OutputSafetyHelper.html

These sources document Action View rendering, partials, strict locals, layouts, helpers, localized views, sanitization, output safety, form helpers, and fragment/collection caching.

Composed repository skills:

- `rails-action-view` skill
- `rails-action-controller` skill
- `rails-i18n` skill
- `rails-caching` skill
- `rails-performance` skill
- `ruby-performance` skill
- `rails-security` skill
- `rails-security-engineering` skill
- `rails-action-text` skill
- `rails-test-engineering` skill
- `rails-test-engineering` skill

## Rails Action View changes

For Action View and rendering changes:
- inspect the Rails/Action View version, template engines, view paths, partial/layout conventions, helpers, presenters, localization, caching, output-safety rules, and view/request/system tests before implementing;
- classify the boundary as template lookup, partial contract, layout, helper, output safety, localization, caching, or rendering performance;
- keep domain authorization, persistence, and external side effects outside templates and helpers; rendering receives already-authorized/prepared data;
- define partial locals explicitly and use strict locals when the partial has a stable interface and the repository Rails version supports it;
- treat changes to required/default locals as caller-contract changes and audit all callers;
- keep layout selection deterministic and never derive a layout path from untrusted input;
- keep helpers presentation-focused; do not let helpers become hidden service objects, query orchestrators, authorization engines, or external API clients;
- preserve Action View's default escaping for untrusted strings; review raw, html_safe, safe_join, sanitize, and custom sanitizer allowlists as security-sensitive operations;
- never mark user input HTML-safe and never expand sanitizer allowlists merely to bypass a rendering defect;
- use rails-i18n for locale context and keep localized templates free of duplicated domain rules; test canonical fallback behavior;
- coordinate fragment and collection caching with rails-caching, including locale/tenant/permission identity when rendered output varies;
- measure template, partial, query, allocation, cache, and output costs before making performance claims;
- do not solve view N+1s by blindly caching private output or globally preloading unrelated records;
- use deterministic view/request/system tests and targeted XSS/unsafe-URL regressions rather than relying only on large snapshots;
- never claim a rendering optimization improved performance without workload evidence or a demonstrated structural property.

---
name: rails-action-text
description: "Use when designing, implementing, reviewing, testing, or operating Rails Action Text rich-text content, Trix editors, RichText associations, sanitization, embedded attachments, Signed Global IDs, rendering, API boundaries, localization, or rich-text performance."
license: MIT
---

# Rails Action Text Engineering

## Purpose

Treat Action Text rich content as a persisted presentation and attachment boundary with its own security, authorization, rendering, performance, and compatibility contracts.

Action Text provides the Trix editor and persists rich content through ActionText::RichText rather than a text column on the owning model. Embedded files can use Active Storage, while non-storage attachables can be referenced through Signed Global IDs. Rails sanitizes Action Text rich content before safe HTML rendering.

Core flow:

```text
define rich-text ownership
-> define content/format contract
-> authorize editing
-> validate/sanitize input
-> persist RichText
-> resolve attachments/attachables
-> render safely
-> preload efficiently
-> expose through API/mail/feed
-> test lifecycle/security
```

## Activate when

- adding `has_rich_text`;
- adding or changing `ActionText::RichText`;
- adding `rich_textarea` or Trix editor behavior;
- changing rich-text sanitization;
- customizing Action Text rendering/layouts/partials;
- embedding Active Storage files in rich text;
- embedding Signed Global ID attachables;
- exposing rich text through APIs;
- changing rich-text edit/update authorization;
- diagnosing missing embedded attachments or unresolved attachables;
- investigating Action Text N+1 queries or rendering performance;
- localizing rich text or editor content;
- testing rich-text content, attachments, or sanitization;
- upgrading Trix/Action Text behavior.

Do not activate merely because a model contains a plain text column. Use `rails-action-view`, `rails-active-record`, or `rails-i18n` unless the Action Text boundary exists.

## Repository inspection

Inspect before changing Action Text:

1. Ruby/Rails and Action Text/Trix versions;
2. `has_rich_text` declarations and naming conventions;
3. Action Text migrations and RichText schema;
4. Trix/application JavaScript integration;
5. `rich_textarea` forms and permitted attributes;
6. Action Text layouts and blob/attachable partials;
7. sanitization configuration and HTML-safe rendering;
8. authorization/policy around the owning record;
9. Active Storage service and upload rules;
10. Signed Global ID / GlobalID usage;
11. custom attachable implementations;
12. API serializers and rich-text wire format;
13. localized rich-text/editor behavior;
14. `with_rich_text_*` scopes and query patterns;
15. cache/CDN behavior for rendered HTML;
16. tests, fixtures, system tests, and JavaScript tests;
17. security scanners and CSP/HTML policies.

Do not introduce a second rich-text model or editor abstraction without repository evidence.

## Decision rules

1. Classify the change: ownership and content contract, editing authorization and the Trix/editor boundary, sanitization and links, attachments and attachables, rendering/API/forms/localization, persistence and background work, or performance/security/testing.
2. Load the matching reference below before changing behavior; attachment and embed changes need both the attachment and the sanitization reference.
3. Enforce server-side sanitization and authorize every embedded object at the server, whatever the editor produced.

## Critical invariants

- Never claim rich-text safety merely because the content originated in Trix.
- Never treat successful sanitization as proof that the user was authorized to reference every embedded object.
- Never let a user embed arbitrary privileged objects merely because they can construct or obtain a signed identifier.
- Do not expose internal Action Text storage tables as a public API contract.

## References

Load only the reference for the boundary being changed, before changing behavior there. Each reference is self-contained and one level deep; none links to another. Consult a listed pattern from the pattern catalog only when the change needs its implementation shape.

| Load when | Reference | Covers | Patterns |
|---|---|---|---|
| a change alters rich-text ownership, the stored content contract, who may edit, or the Trix/editor boundary | [references/content-and-editing.md](references/content-and-editing.md) | Ownership boundary; Content contract; Editing authorization; Trix/editor boundary | `action-text-content-contract` |
| a change alters allowed tags/attributes, sanitization, or link and URL handling | [references/sanitization-and-links.md](references/sanitization-and-links.md) | Sanitization boundary; Links and URLs | `action-text-sanitization-security` |
| a change embeds attachments or custom attachables, resolves signed identifiers, or handles missing attachables | [references/attachments-and-attachables.md](references/attachments-and-attachables.md) | Attachments; Signed Global ID attachables; Attachables and rendering; Missing attachables | `action-text-attachable-contract`, `action-text-attachment-authorization` |
| a change renders rich text, exposes it through an API, localizes it, or accepts it through forms | [references/rendering-and-apis.md](references/rendering-and-apis.md) | Rendering boundary; API boundary; Rich text and localization; Forms and parameters | `action-text-rendering`, `action-text-api-boundary` |
| a change alters rich-text persistence, background processing, or search/indexing | [references/lifecycle-and-background-work.md](references/lifecycle-and-background-work.md) | Persistence and lifecycle; Background work; Search/indexing | `action-text-lifecycle` |
| a change has N+1, caching, content-size, security/privacy, or test-strategy impact | [references/performance-security-testing.md](references/performance-security-testing.md) | Performance and N+1; Caching rendered rich text; Content size and resource limits; Security and privacy; Testing | `action-text-preload-performance`, `action-text-testing` |

## Reference example

Rich text declared on the model, rendered through its sanitized fragment, never through html_safe of editor input.

```ruby
class Article < ApplicationRecord
  has_rich_text :body

  validates :body, presence: true
end

# app/views/articles/_form.html.erb:
#   <%= f.rich_text_area :body %>
#
# Rendering contract:
#   article.body.to_s  -> sanitized HTML fragment, safe for templates and API payloads
#   Direct editor input is never trusted; sanitization happens on save, not on render.
#
# Attachments inside rich text are signed Global ID attachables:
#   ActionText::Attachment carries sgid://... references resolved server-side.
```

## Agent review checklist

- [ ] Action Text/Rails version resolved
- [ ] rich-text owner and attribute explicit
- [ ] edit authorization checked
- [ ] content contract defined
- [ ] server-side sanitization preserved
- [ ] link/URL policy reviewed
- [ ] attachment boundary composed with Active Storage
- [ ] SGID attachable authorization reviewed
- [ ] attachable rendering/fallback defined
- [ ] API representation explicit
- [ ] locale behavior explicit when applicable
- [ ] persistence/deletion lifecycle reviewed
- [ ] N+1/preloading measured
- [ ] rendered rich-text cache identity reviewed
- [ ] content/resource limits defined
- [ ] background processing semantics reviewed
- [ ] search/indexing representation defined when applicable
- [ ] security/privacy tests added
- [ ] deterministic rich-text tests exist

## Anti-patterns / failure modes

- authorizing arbitrary RichText by ID;
- treating Signed Global IDs as authorization by themselves;
- trusting Trix/client-side validation;
- disabling/bypassing sanitization for convenience;
- marking raw Action Text body HTML-safe manually;
- allowing arbitrary attachable objects;
- rendering private attachments through public rich-text pages;
- duplicating Active Storage provider logic inside Action Text code;
- exposing ActionText::RichText table structure as an API;
- rendering large collections without RichText/embed preload;
- globally preloading every rich-text body/embed;
- caching private rich text without permission identity;
- assuming missing attachables never occur;
- using locale to authorize content;
- allowing unbounded rich-text/attachment payloads;
- relying on background processing without defining its failure state.

## Verification

For a rich-text feature:

```text
ownership
-> edit authorization
-> content/input contract
-> sanitization
-> attachment/attachable authorization
-> rendering contract
-> API/localization contract
-> performance/preload review
-> focused security tests
-> regression suite
```

For a rendering incident distinguish:

```text
stored RichText
-> sanitizer
-> attachable resolution
-> attachment/blob rendering
-> localized presentation
-> preload/query behavior
-> cache
-> final HTML
```

Never claim rich-text safety merely because the content originated in Trix. Verify server-side sanitization, attachment authorization, attachable resolution, and final rendering behavior.

## Source foundation

Primary Rails source:

- https://guides.rubyonrails.org/action_text_overview.html
- https://api.rubyonrails.org/classes/ActionText/RichText.html

The Rails guide documents Trix, RichText persistence, sanitized HTML rendering, Active Storage attachments, Signed Global ID attachables, custom attachment rendering, and preloading RichText/embeds.

Composed repository skills:

- `rails-active-record` skill
- `rails-action-view` skill
- `rails-validations` skill
- `rails-active-storage` skill
- `rails-security` skill
- `rails-security-engineering` skill
- `rails-i18n` skill
- `rails-caching` skill
- `rails-performance` skill
- `ruby-performance` skill
- `rails-api-integration` skill
- `rails-active-job` skill
- `rails-test-engineering` skill
- `rails-test-engineering` skill

## Rails Action Text changes

For Action Text/rich-text changes:
- inspect has_rich_text declarations, Action Text/Trix versions, RichText schema, editor integration, sanitization, custom partials, attachment/attachable behavior, APIs, locale behavior, query patterns, and tests before implementation;
- authorize editing through the owning domain resource; never treat ActionText::RichText IDs or Signed Global IDs as authorization by themselves;
- preserve Action Text server-side sanitization and review custom HTML/link/attachment rendering for XSS and privacy risks;
- treat Trix/client-side validation as usability only; server-side authorization and content controls remain authoritative;
- use rails-active-storage for embedded file storage/access lifecycle rather than duplicating storage-provider logic in Action Text code;
- restrict and explicitly authorize attachable object types, tenant scope, and rendering partials; define missing-record fallback;
- keep public API representations stable and avoid exposing internal RichText/attachment table structure unless explicitly contractual;
- measure RichText and embed query behavior before choosing `with_rich_text_*` preloads; use the narrowest preload justified by the rendering workload;
- review locale and cache identity when rendered rich text varies by locale, permission, content version, or attachment state;
- bound rich-text size, attachment count, and transformation work where product requirements allow;
- coordinate lifecycle/cleanup semantics across RichText and Active Storage instead of assuming external object deletion is transactional;
- add negative security tests for malicious HTML/URLs and unauthorized embedded resources;
- use deterministic local/test storage and avoid live cloud-provider dependencies in ordinary CI;
- never claim rich-text safety merely because the content came from Trix; verify sanitization, authorization, attachable resolution, and final rendering.

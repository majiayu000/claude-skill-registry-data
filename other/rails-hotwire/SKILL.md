---
name: rails-hotwire
description: Use when designing, implementing, reviewing, testing, or debugging Rails Hotwire interfaces using Turbo Drive, Turbo Frames, Turbo Streams, morphing, Stimulus controllers, and server-rendered progressive enhancement.
license: MIT
---

# Rails Hotwire Engineering

## Purpose

Treat Hotwire as a server-rendered interaction architecture, not as a shortcut around application design. Keep navigation, DOM replacement, HTML response contracts, controller state, security, accessibility, and client lifecycle explicit.

Hotwire in Rails primarily composes Turbo and Stimulus. Rails documents Turbo as a way to accelerate navigation and update page regions while keeping HTML rendering on the server; Turbo Frames scope page updates and Turbo Streams deliver targeted HTML changes.

## Activate when

- adding or changing Turbo Drive navigation;
- introducing Turbo Frames for partial page replacement;
- implementing Turbo Stream responses or broadcasts;
- using Turbo morphing or refresh behavior;
- replacing Rails UJS behavior with Turbo;
- building Stimulus controllers, targets, values, actions, or outlets;
- debugging double initialization, stale controllers, disconnected elements, or frame/stream targeting;
- changing HTML response contracts consumed by Turbo;
- integrating authentication, authorization, CSRF, redirects, or validation errors with Turbo forms;
- reviewing Hotwire accessibility, progressive enhancement, loading states, or browser history semantics;
- testing Turbo/Stimulus behavior without depending on live external services.

Do not activate merely because a page contains JavaScript. Use the appropriate frontend/build or plain JavaScript skill when Hotwire is not the interaction boundary.

## Repository inspection

Before changing Hotwire behavior, inspect:

1. resolved Ruby/Rails and turbo-rails/stimulus dependencies;
2. JavaScript packaging strategy: importmap, Bun, esbuild, Rollup, Webpack, or another loader;
3. application.js/application.css and initialization order;
4. turbo-rails setup and Turbo configuration;
5. existing controllers, frames, stream templates, broadcast declarations, and helper conventions;
6. layout/meta tags, CSRF setup, authentication, authorization, and cache configuration;
7. partials and DOM IDs used as Turbo targets;
8. controller response formats and status codes;
9. form builders, validation rendering, redirect conventions, and flash handling;
10. Stimulus controller lifecycle, target/value contracts, and event listeners;
11. browser/system/request tests and JavaScript test tooling;
12. accessibility conventions for focus, forms, live updates, and keyboard behavior;
13. realtime transport such as Action Cable when Turbo Streams are broadcast;
14. page caching and ETag/fragment cache behavior when DOM identity matters.

Do not assume a Turbo or Stimulus API from memory when the repository dependency version can be inspected.

## Turbo Drive navigation

Turbo Drive keeps navigation inside a persistent page shell rather than rebuilding the document for every visit.

Review application-wide versus page-specific state, lifecycle events, script idempotency, cleanup of listeners/timers/observers/subscriptions, browser history, redirects, and pages that require a full reload.

Turbo navigation does not replace normal controller authorization, validation, CSRF, caching, or HTTP semantics.

## Turbo Frames

A Turbo Frame establishes a DOM replacement boundary.

For each frame define stable identity, owner/resource context, allowed navigation targets, expected returned frame structure, empty/error/loading behavior, authorization and tenant semantics, nested-frame behavior, lazy-loading behavior, and accessibility implications.

The server response must satisfy the expected frame contract. A frame is not an authorization boundary and a frame identifier must never be treated as permission.

## Turbo Streams

Turbo Streams represent targeted DOM mutations through stream actions such as append, prepend, replace, update, and remove.

Treat a stream as a wire contract with stable target identity, action semantics, rendered partial structure, ordering/idempotency assumptions, authorization/privacy, duplicate delivery behavior, and reconnect expectations when broadcast.

Rails provides turbo_stream response/rendering helpers and can broadcast stream changes to subscribers.

Do not confuse a Turbo Stream broadcast with durable messaging. Coordinate durable business events with the event and messaging architecture.

## Turbo morphing and refresh

When the installed Turbo version supports morphing, treat element identity and stable DOM IDs as correctness constraints.

Before using morphing, identify client state that must survive, define replacement boundaries, review Stimulus disconnect/connect behavior, keep IDs stable, and test focused inputs, dialogs, menus, and other client state across refreshes.

## Forms and response contracts

Turbo forms change browser interaction without changing the server's responsibility.

Authorize the operation, validate input, return deliberate status codes, render or redirect according to the response contract, return a Turbo Stream when targeted mutation is required, and preserve a useful HTML fallback where progressive enhancement is required.

Validation errors must render inside the correct frame or page boundary and preserve accessible error association.

## Stimulus controller boundaries

A Stimulus controller should own a focused browser behavior. Define controller responsibility, actions, targets, values, outlets, lifecycle callbacks, external event subscriptions, teardown, and idempotency assumptions.

Avoid controllers that become application-wide orchestration layers or hidden domain services.

## Stimulus lifecycle

Controllers may connect, disconnect, and reconnect as Turbo replaces or morphs DOM.

Every controller that registers document/window listeners, timers, observers, subscriptions, or third-party widgets must define cleanup semantics. Avoid duplicate listeners after reconnect.

## Security and CSRF

Turbo does not remove Rails security boundaries.

For browser-authenticated non-GET requests, preserve CSRF protection according to the repository contract. Rails documents that JavaScript requests need the CSRF token when protection applies.

Review session authentication, authorization, frame/resource ownership, untrusted data attributes, redirect targets, HTML injection, stream target manipulation, and unsafe third-party DOM libraries.

Never treat a frame ID, DOM ID, or stream target as permission.

## Authentication and authorization composition

Hotwire endpoints still require the ordinary request security pipeline:

authenticate
-> establish tenant/context
-> authorize resource/action
-> validate
-> render/redirect/stream

Private frame and stream responses must obey the same tenant and permission semantics as full-page endpoints.

## Accessibility and progressive enhancement

Prefer semantic HTML and native form/button behavior.

Review focus movement after replacement, keyboard access, status announcements, error association, loading state semantics, reduced-motion expectations, and non-JavaScript fallback where the workflow requires it.

Hotwire should enhance a valid HTML contract rather than become the only path to a usable application.

## Caching and DOM identity

When caching rendered HTML, account for every dimension that changes markup: actor/tenant, locale, permissions, feature state, resource version, and frame/stream context.

Do not share private Turbo Frame or Stream HTML through a cache key that omits authorization context.

Stable DOM IDs are part of the client/server contract. Changing them can break stream targeting even when server-side Ruby still works.

## Realtime Turbo Streams

When broadcasting streams over Action Cable, authorize the subscription, define stream naming and tenant isolation, broadcast committed state, define duplicate/out-of-order behavior, reconcile missed updates, avoid secrets and oversized payloads, and coordinate durable changes with event/messaging boundaries.

## Testing strategy

Test Hotwire at the smallest useful boundary plus at least one real HTTP/browser boundary when DOM lifecycle is essential.

Cover frame navigation/render contracts, stream response actions, Turbo form redirects/statuses, validation errors, authorization on frame/stream endpoints, CSRF behavior, broadcast target isolation, duplicate/reordered delivery where relevant, Stimulus connect/disconnect, cleanup, stable target IDs, and morphing state preservation.

Keep core tests deterministic and avoid live browser/WebSocket/external CDN dependencies when local contracts prove the behavior.

When a workflow must work without JavaScript (forms, navigation, state that survives a reload), prove that before enhancing it. Write a test with no JavaScript first, and keep it passing after Turbo or Stimulus is added:
- a request/integration test of the HTML contract; or
- a system test driven by `rack_test` (`driven_by :rack_test`), since Capybara's RackTest driver does not execute JavaScript.

Purely client-side widgets with no server-side fallback are exempt; say so in the change.

## Anti-patterns / failure modes

- treating a Turbo Frame as an authorization boundary;
- returning the wrong frame ID;
- stream targets derived from untrusted identifiers;
- duplicate Stimulus listeners after Turbo navigation;
- broad Stimulus controllers owning unrelated domains;
- Turbo forms that return ambiguous success/error HTML;
- private frame or stream responses shared through unsafe caches;
- broadcasting before transaction commit;
- assuming Turbo Streams are durable messaging;
- relying on JavaScript-only authorization or validation;
- changing DOM IDs without updating stream/broadcast contracts.

## Reference example

A Turbo Stream broadcast after a state change, with the frame that consumes it and a Stimulus controller limited to presentation.

```ruby
class InvoicesController < ApplicationController
  def create
    @invoice = current_account.invoices.create!(invoice_params)

    respond_to do |format|
      format.turbo_stream { broadcast_append_to @invoice.account, :invoices, target: "invoices" }
      format.html { redirect_to invoices_path }
    end
  end
end

# app/views/invoices/_invoice.html.erb:
#   <%= turbo_frame_tag dom_id(invoice) do %>
#     <%= render invoice %>  <!-- server-rendered; no client state duplication -->
#   <% end %>
#
# app/javascript/controllers/reveal_controller.js keeps DOM-only concerns (show/hide)
# and never owns domain state - state changes flow through Turbo Stream updates.
```

## Agent review checklist

- [ ] Ruby/Rails and Hotwire dependency versions resolved
- [ ] JavaScript loading/build strategy identified
- [ ] Turbo Drive lifecycle reviewed
- [ ] frame identity and response contract explicit
- [ ] stream target/action contract explicit
- [ ] morphing/refresh behavior reviewed when used
- [ ] form status/redirect/error behavior verified
- [ ] Stimulus controller responsibility is narrow
- [ ] connect/disconnect cleanup is deterministic
- [ ] authentication/authorization remain server-side
- [ ] CSRF semantics preserved
- [ ] private HTML cache identity reviewed
- [ ] tenant/resource stream isolation reviewed
- [ ] accessibility and progressive enhancement reviewed
- [ ] deterministic tests cover the changed boundary
- [ ] browser/system verification added where necessary
- [ ] Action Cable/eventing composition reviewed when broadcasts are involved

## Verification

For a Hotwire change:

identify Rails/Hotwire versions
-> inspect JS loading and existing conventions
-> classify Drive/Frame/Stream/Stimulus boundary
-> define HTML/DOM response contract
-> preserve authentication/authorization/CSRF
-> implement smallest coherent interaction
-> verify lifecycle cleanup
-> add focused request/system/JS tests
-> run repository validation
-> inspect CI evidence

Do not claim Hotwire correctness merely because the page appears to work manually.

## Source foundation

Primary sources:
- https://guides.rubyonrails.org/working_with_javascript_in_rails.html
- https://turbo.hotwired.dev/handbook/introduction
- https://turbo.hotwired.dev/handbook/frames
- https://turbo.hotwired.dev/handbook/streams
- https://stimulus.hotwired.dev/handbook/introduction

## Rails Hotwire changes

For Hotwire changes:
- preserve Turbo Frames as explicit DOM replacement boundaries and treat their IDs/targets as identifiers rather than authorization;
- resolve the Ruby/Rails and turbo-rails/Stimulus versions and inspect the JavaScript loading strategy before implementation;
- classify the interaction as Turbo Drive, Frame, Stream, morph/refresh, Stimulus lifecycle, or a cross-boundary composition;
- preserve server-side authentication, authorization, validation, CSRF, status, redirect, and caching semantics;
- treat frame IDs, DOM IDs, stream targets, and client data attributes as identifiers, not authorization;
- keep Turbo Frame and Stream responses stable and explicit; audit partial/DOM contracts when IDs or target structure change;
- make Stimulus controllers cohesive and make connect/disconnect cleanup idempotent for listeners, timers, observers, subscriptions, and widgets;
- review morphing/refresh for DOM identity and client-state preservation rather than assuming rerendering is harmless;
- preserve progressive enhancement and semantic HTML for critical workflows;
- review accessibility for focus, errors, live updates, keyboard behavior, and loading states;
- isolate private frame/stream HTML in cache identity and tenant/resource broadcast channels;
- coordinate Turbo Stream broadcasts with Action Cable and durable eventing rather than treating browser updates as the source of truth;
- add deterministic request/system/JavaScript tests for the protocol and lifecycle boundary;
- do not claim Hotwire correctness from manual browser success alone.

## Book cross-reference: *Modern Front-End Development for Rails*

Chapters 1–3, 5, 8, and 10 provide a conceptual guide to the Hotwire approach, Turbo Drive/Frames/Streams, Stimulus actions/targets/values, client/server interaction, and UI state. Keep server-rendered HTML and explicit DOM contracts central. The book targets Rails 7-era tooling; inspect this application's Rails, turbo-rails, Stimulus, and asset setup before applying any installation or API instructions.

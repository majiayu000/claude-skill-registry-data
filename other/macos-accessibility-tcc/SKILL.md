---
name: macos-accessibility-tcc
description: "Use when building or diagnosing a macOS AXUIElement or AXObserver client, including TCC, secure fields, callback teardown, or target relaunch."
license: "MIT"
metadata:
  author: "coryparrry"
  version: "0.1.0"
  last-updated: "2026-08-30"
  last-reviewed: "2026-08-30"
  apple-docs-reviewed: "2026-08-30"
---

# macOS Accessibility TCC

Treat Accessibility as a user-authorized interprocess capability. This skill is for clients of other apps, not for making an app's own UI accessible.

## Route the work

Identify the exact AX caller and helper boundary, target bundle/current PID, requested scope, and lifecycle owner. Another build or process is not TCC proof.

- For trust flow, observers, callback ownership, AX errors, target relaunch, teardown, or runtime tests, read [references/accessibility-client-lifecycle.md](references/accessibility-client-lifecycle.md).
- Before API or review-date changes, read [references/apple-documentation.md](references/apple-documentation.md) and use Xcode `DocumentationSearch`; it records SDK-header supplements.

## Non-negotiable invariants

- `AXIsProcessTrustedWithOptions` returns current trust even when prompting asynchronously. Explain scope and prompt only from user action; do not poll, reset TCC, open settings, or relaunch without authorization.
- AX elements and observers are target-PID-bound. Target relaunch requires teardown and a fresh generation, element, and observer.
- Retain callback context for the full registration lifetime. Validate PID/generation/terminal state before side effects.
- Teardown is idempotent: keep callback context alive, mark terminal, remove successful notification pairs and the run-loop source on its owner, then wait for the removal barrier, callback-entry leases, and accepted callback work to quiesce without blocking the callback thread. Only then release context, observer, and elements.
- Before any value-like read, classify role/subrole. For `kAXSecureTextFieldSubrole` or ambiguous editable/focused input, never request value, selected text, ranges, text markers, or descendant text. Redaction after acquisition is too late.
- Minimize traversal and retention. Do not log UI text, titles, documents, labels, values, selections, or tree dumps. A trust grant never authorizes broader observation or actions than the requested feature.
- Classify AX errors before bounded recovery; never retry unsupported capabilities, illegal arguments, or missing trust.

General cross-process Accessibility inspection/control is constrained by App Sandbox. Establish the distribution and entitlement boundary before designing around AX; do not imply that a working unsandboxed development client proves a sandboxed or Mac App Store build can perform the same work.

Validate the exact client across trust states, balanced registrations, callback teardown, target relaunch, unsupported/unresponsive targets, and secure/ambiguous inputs with proof that value calls never occur.

Update `last-updated` for material changes, `last-reviewed` after substantive review, and `apple-docs-reviewed` only after checking Apple sources or SDK declarations.

## Review

- Last updated: 2026-08-30
- Last reviewed: 2026-08-30
- Apple documentation reviewed: 2026-08-30

Scope/evidence: Accessibility trust, observer lifecycle, secure-field, and target-relaunch guidance was checked with Xcode MCP `DocumentationSearch` plus installed SDK declarations for legacy AX APIs.

[Apple documentation evidence](references/apple-documentation.md)

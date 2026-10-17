---
name: completion-protocol
description: Prove completeness for non-trivial implementation, migration, translation, content, integration, and audit work by inventorying the full affected surface, tracking coverage, auditing omissions, and refusing unsupported completion claims.
---

# Completion Protocol

Use this protocol for any non-trivial task whose result can be partially correct while still missing routes, records, states, content sources, integrations, or user journeys.

## Completion contract

Before implementation, translate the requested outcome into a bounded inventory of affected surfaces. Derive the inventory from the actual system and the user's request, not only from examples in the prompt or the files first discovered.

The completion contract must identify:

- the original outcome without weakening it;
- every affected route, component, state, data/content source, record class, integration, output, and user journey that is reasonably in scope;
- explicit non-goals and approved exclusions;
- evidence required for each inventory item;
- negative-space checks that can find omitted work;
- end-to-end journeys that prove continuity across boundaries.

For ambiguous scope that would materially change the result, ask before implementation. Do not use ambiguity to silently shrink the inventory.

## Coverage ledger

Track every inventory item with exactly one status:

- `verified`: implemented and supported by fresh evidence;
- `excluded`: outside scope with explicit user approval and a reason;
- `blocked`: incomplete, with the concrete blocker and required next action.

An item is never complete merely because a file changed, a unit test passed, or one representative example worked. Evidence must match the claimed outcome.

## Negative-space audit

After implementation, search for what was missed. Select checks that can falsify completeness, such as remaining source-language text, missing locale keys, stale fallbacks, unhandled routes, unstyled theme states, untested permissions, orphaned records, unchanged legacy APIs, placeholders, dead branches, or outputs that still use the old behavior.

For translation work, inventory and verify at minimum: navigation, routes, products, categories, database-owned content, field labels, placeholders, validation errors, empty/loading/error states, notifications, emails, metadata, search/filter values, mobile views, and fallback-language behavior. Approved brand names are exclusions, not silent exceptions.

## End-to-end and independent audit

Exercise complete user journeys across the affected boundaries. Then perform a separate completion audit against the original request and the coverage ledger. The audit's purpose is to disprove completion, not to summarize implementation.

The reviewer must inspect fresh outputs or runtime state. Self-authored claims, stale screenshots, changed-file lists, and successful build commands are not substitutes for outcome evidence.

## Completion manifest

Before reporting completion, produce the one-line JSON `completion_manifest` defined in [references/manifest.md](references/manifest.md). A `complete` verdict is valid only when:

- every inventory item is verified or explicitly approved as excluded;
- no blockers remain;
- all required negative-space checks pass;
- every required end-to-end journey is verified;
- the independent audit passes with no unresolved findings.

If any condition is unmet, use verdict `incomplete` and state exactly what remains. Never use `done`, `finished`, `complete`, `polished`, or `verified` as a softer substitute.

## Learning from corrections

Classify rejected or repeated work by root cause, including `omitted_surface`, `missing_state`, `missing_data_source`, `broken_continuity`, `stale_evidence`, `visual_mismatch`, `scope_drift`, and `unsupported_completion_claim`.

Record each correction in the central learning system with its scope and evidence. When the same root cause occurs two or three times, propose a reusable inventory or verification rule. Do not promote a one-off preference automatically.

---
name: publish
description: Publish a Lexsis storefront draft version that carries DESIGN_APPROVED from /design-page, /quiz, or /optimize. Use only when the user explicitly asks to release a specific page version.
---

# Publish a Page

Publishing is a separate, explicit action. Do not rebuild the page here.

Read `references/workflow-intent.md`. Intent inference may distinguish a draft
request from a live-release request, but it never substitutes for explicit
approval naming the page and version. A request to preview, create, finish,
review, or approve a design is not publication approval.

Use `lexsis_pages.edit_context`, `lexsis_pages.integrity`,
`lexsis_pages.source`, `lexsis_workspace.get`, and
`lexsis_live_ops.publish`. Resolve unfamiliar argument schemas with exact
router/action discovery. Do not use a prose query for these known actions. An
empty discovery result is not a publishing outage; the actual context,
entitlement, or publish call determines availability. A local QA report cannot
authorize or substitute for a successful live publish.

## Gate

1. Read the page's operation record and hosted QA evidence under
   `references/source-artifact-workflow.md`.
2. Confirm the saved store/theme binding still exists.
3. Confirm reviewed source, bundle and section hashes match the persisted
   draft and recorded baseline.
4. Read `lexsis_pages` action `edit_context`.
5. Confirm the remote version equals `remote.lastKnownVersion`.
6. Confirm `DESIGN_APPROVED` was recorded by `/design-page`, `/quiz`, or `/optimize` for
   this same page version and reviewed bundle, with hosted QA at 390, 768 and
   1280 and commerce, copy, claims, assets and integrity checks passed.
7. Re-read integrity and source/bundle evidence through MCP. Missing or stale
   evidence blocks release; no local file or validator substitutes for it.
8. Confirm the store has the required entitlement.
9. Confirm explicit publication approval naming the page and version. Reuse an
   approval already given for this exact scope; ask only if it is missing or the
   reviewed version has changed.

Only then call:

```text
lexsis_live_ops({ action: "publish", args: { page_id } })
```

Do not treat draft creation or a preview request as publishing approval.

## Quiz capture

For a Quiz with saving enabled, follow `references/quiz-authoring.md`. Confirm
that the prepared/active policy matches the immutable page-version UUID and
instance hash. Capture activation has its own explicit approval; design or page
publication approval alone does not silently authorize a new collection policy.
A quiz without saving does not need capture activation.

Draft QA proves interactions and design. After publishing, verify saving and
analytics consent combinations, save/edit/reload/retry, a retained Forms response,
and real cart outcomes on the returned published URL. Report any pending live
checks separately; preview intentionally cannot collect production responses.

## Other Lifecycle Actions

Use `lexsis_live_ops` for unpublish or rollback only when the user explicitly
requests that action and the target page/version is clear.

## Return

Report the published page, version, public URL, and whether the previous live
version remains available for rollback. Include the MCP capability and action
evidence.

## Shared Sections

Before publishing, read linked pages with `lexsis_pages.shared_section`. A
`stale` page holds an older revision: sync it, or tell the user it will publish
the older copy. After a shared section sync, each linked live page needs its
own explicit publish approval.

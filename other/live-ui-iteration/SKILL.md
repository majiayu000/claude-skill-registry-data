---
name: live-ui-iteration
description: "Continuous localhost UI iteration loop with Arman, through full surface certification. Use when he asks to fix, refine, review, or iterate on a page, route, panel, overlay, or other UI while he may inspect localhost. NOT for a report-only UI audit."
---

# Live UI iteration

Own the focused surface continuously: **requested changes first, then full surface completion, then certification.** Arman may inspect localhost while you work; that is visibility, not a pause or a request for an early handoff.

## The default is the full pass

- **Do not stop after the named fix.** Make Arman's explicit changes first, verify that they are visible on localhost, send a brief progress update with the route, then continue through the full surface pass without asking whether to proceed.
- **Do not stop at a plan, diagnosis, partial checklist, or “first pass.”** Continue until every applicable certification item is pass/fixed/N/A and live verification is complete.
- **Only narrow the work when Arman explicitly says** “only make these changes,” “stop after this,” or equivalent. Even then, verify those changes proportionately and state that the surface was not fully certified.
- **New feedback becomes priority zero.** Apply it, make it visible, then resume the remaining certification work.

## Eligibility and continuity

- **Agent-native surfaces remain eligible.** Chat, Agent Builder, runners, and
  window panels may use an outside helper with a recorded approved invocation
  contract. Keep their native subject agents and permanent residents isolated
  from ad-hoc surface values; placement or binding alone is never approval.
- **Integration never pauses this loop.** Periodic integration, type sync, release,
  or shared-checkout sweeps are expected background activity. Checkpoint and push
  the current coherent owned files, then resume immediately; never wait for a
  sweep or release to end.
- **Only an exact-file collision can suspend a path.** Preserve both owners' work,
  continue every non-overlapping task, and resume the collided path as soon as it
  is isolated. A general "freeze" message is not authority to stop the fleet.

Read [`references/readiness-gate.md`](./references/readiness-gate.md) before the first browser handoff. Read [`references/skill-router.md`](./references/skill-router.md) while gathering the surface so every applicable specialist contract is invoked.

## Start independently

1. Resolve the exact route, panel, or overlay and its feature directory.
2. Read `docs/official/browser-testing.md`; start or reuse only `pnpm preview:start` on port 3001. (Cloud container? No dev server there — follow the cloud lane in `page-pass` "Where you verify".)
3. Use the available browser tool to open an isolated in-app Browser for routine localhost work. Computer Use is allowed; no particular skill name or API is required. If the isolated browser cannot complete the task, follow the pre-authorized new-tab fallback in `docs/official/browser-testing.md`.
4. Authenticate yourself with the repository's pre-authorized flows: the dev-login nonce handshake (`openssl rand -hex 16 > .dev-login-nonce`, then `/api/dev-login?nonce=<that value>&next=/<route>`) or `AI_ADMIN_USERNAME` / `AI_ADMIN_PASSWORD` at `/login`. Never put a durable token in a URL — the `?token=` path was removed for leaking it. Never ask Arman to log in, provide credentials, click through setup, or perform routine verification.
5. Inspect the real surface before editing: desktop state, current behavior, console, feature docs, manifest/readiness/last check, and exact-route review feedback.
6. **Run the first-screen gate at 1280×800.** If a table, editor, list, or other primary workspace is only a token strip at the bottom—or starts below the fold—remove the obstruction before lower-priority polish. Browser visibility is not a pause.

Never print credentials or tokens. Keep the managed preview running so Arman can inspect it; close only the Browser tabs or groups you created when they are no longer needed.

## Work order

### 1. Arman's request first

Implement the requested behavior before beginning broad cleanup. Preserve working behavior and use canonical primitives. Verify the requested path immediately. When it is visible, tell Arman where it is and that the full surface pass is continuing; do not call it complete.

### 2. Complete the surface

Invoke `surface-check` and run S1–S18 on the focused surface, fixing as you go. The default permits the time needed to establish high-value foundations such as Surface Values, runtime scope, bindings, write targets, canonical context menus, Pro inputs, mobile behavior, and documentation.

- If the route is a real agent-aware surface, invoke the consolidated `surface-authoring` lifecycle and earn honest readiness.
- Invoke `context-menu-v3` for the full menu contract; Surface Check S6 is the verifier, not the implementation body.
- Apply `.claude/ui-skills/shared/application-ui-copy-and-hierarchy.md` across the visible page. Remove duplicated titles, generic introductory prose, decorative hero spacing, and other obvious app-as-article habits without deleting consequential meaning.
- **The header owns destinations.** A second body-level row of route buttons fails the pass. Remove duplicate doors; put remaining destinations in the canonical header navigation/overflow or one compact menu that opens the canonical route/window.
- **Summary cards stay summaries.** Multiple actions inside a KPI/status tile share one compact row or menu; vertically stacked full-width buttons fail unless choosing between those actions is the card's primary job.
- **Clear and revert must tell the truth.** Exercise them against real data; zero mutations are never success, and when removing an override reveals a fallback, name its provenance and explain that the override was removed rather than implying the effective value became blank.
- **Personalize at the named entity boundary.** In multi-brand, multi-site, or agency surfaces, an organization-level membership, entitlement, or default may grant access but never proves that every child record shares that classification. Trace the exact brand/site/record field before showing an automatic recommendation or claiming “your industry.”
- **A workbench is not a dashboard.** Keep the primary job's controls and work area on the main path. Fold a supporting insight into the number or control it explains; reduce setup, readiness, and coverage to compact doors into their owning routes; render templates and defaults only on their catalog or setup surface.
- Fix shared primitives when the defect originates there; do not patch every consumer independently.
- Keep the boundary to this surface and the canonical primitives it directly depends on. Log unrelated repo defects instead of turning the session into a fleet-wide sweep.

### 3. Certify live

Follow the readiness gate. A type-check or screenshot alone is not certification. Exercise the real requested interaction, surface context, menus, responsive layout, themes, states, console, and Error Inspector at the required viewports.

## Review-queue relationship

At startup, read `agent.review_queue` rows for the exact route/surface and fold relevant existing feedback into the work. Respect ownership before claiming or mutating a row; never claim unrelated backlog merely because it shares a feature.

This live conversation normally replaces a new asynchronous review item because Arman is already walking through the result. Existing rows still follow `agent-review-queue`: local repair proof does not promote a row that requires later independent deployed verification.

## Handoff

Say **ready for review** only when:

- Arman's requested changes pass.
- Every applicable S1–S18 item is pass/fixed/N/A with no deferred visual proof.
- Desktop and mobile, light and dark, context-menu parity, console, and Error Inspector checks pass.
- Surface readiness, DB mirror, docs, and ledger are truthful and current where applicable.
- The exact localhost route is available.

Give Arman the route, a compact summary of changes, and the specific interactions worth reviewing. Keep localhost running. Do not claim deployment or production proof from localhost.

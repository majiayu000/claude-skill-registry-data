---
name: godmode-shipping
description: BDB Shipping Godmode, the final gatekeeper for production releases. Use when running pre-launch checks, feature-flag rollouts, or rollback planning under Spec-Driven Development before a release ships.
category: engineering-method
---

# 🚀 BDB Shipping Godmode

This skill is the final gatekeeper. No code reaches production without passing these rigorous checks. It orchestrates release management and workflow discipline for the BDB ecosystem across all supported harnesses (Cursor, Claude Code, Agy, Copilot).

## 1. Spec-Driven Development
Writing code without a specification is guessing.
*   **The Specification Phase:** Every major feature or refactor must begin by writing a clear markdown specification file.
*   **Boundaries & Constraints:** The spec must document the exact boundaries of the feature, edge cases, data structures, and the definition of "Done". Do not proceed to code until the user approves the spec.

## 2. Pre-Launch Validation Checklist
Before any code is committed, pushed, or deployed, you must actively verify the following:
*   [ ] **Test Suite Green:** All unit and E2E tests pass.
*   [ ] **No Test Skips:** No `.skip` or `.only` test blocks remain in the codebase.
*   [ ] **Sanitized Code:** No floating `console.log` or debug statements left behind. No local absolute paths or usernames.
*   [ ] **Documentation Synced:** `.openwiki/` and `README.md` updated via `openwiki-skill`.
*   [ ] **Memory Ingested:** New architecture facts and decisions indexed into `memB` via `memb-ingest`.
*   [ ] **Accessibility Checked:** Core Web Vitals and WCAG 2.1 AA audits are clear.
*   [ ] **Security Verified:** API keys and secrets are safely managed via environment variables and never hardcoded.

## 3. Deployment & Rollout Strategy
Releasing code should be a boring event.
*   **Decouple Deploy from Release:** Pushing code to production does not mean the user sees it immediately. Use Feature Flags to merge code safely into main without exposing it to the user.
*   **Dark Launching:** Test the code in production with synthetic traffic or internal users before flipping the feature flag for the public.
*   **Staged Rollouts:** For critical features, roll out sequentially (Internal Team -> 5% of users -> 50% -> 100%).
*   **Mechanism:** When a project has a `bdb-deploy.json`, use the `bdb-deploy` skill for the actual build+rsync+restart+healthcheck step — always `--dry-run` first, never hand-construct rsync/ssh commands (see `bdb-deploy`'s own SKILL.md for why). If a project has no `bdb-deploy.json` yet and needs one, that's a decision for the user (host, SSH key, remote path) — run `bdb-deploy init` interactively, don't invent the values.

## 4. Rollback Strategies
Never launch a feature without a verified rollback plan.
*   **Auto-Rollback Triggers:** Define exactly what metrics will trigger an automatic rollback (e.g., error rate jumps by >2x, latency spikes above 500ms).
*   **Database Migrations:** Ensure any database schema changes are backward compatible, or have a strictly tested `down` migration ready.

## 5. Creator Extension & BDB MediaStorm Governance
This Godmode extends beyond standard software development. It STRICTLY governs creative-tech and show-control workflows (BDB Creator Extension).
*   **MediaStorm Deployments:** When executing `/bdbmediastorm` for TouchDesigner, Unreal Engine, or Adobe Suite workflows, you must enforce rigorous release management for `.tox` files, Unreal Blueprints, and showfiles.
*   **Show-Ready Validation:** Never push a creative-tech update to a live production environment (e.g., a running installation or live show) without a verified fallback or backup showfile. 

## Visual recap
After the gates pass, `/pr-recap` can build a Plan Builder recap page of the diff with the Verified and Not verified checks. It is informational and does not gate the release. Posting it anywhere stays a human decision.

## Universal Agent Harness Integration
This Godmode is universally compatible and governs all extensions, including the BDB Creator Engine.
*   **Cursor:** Auto-injected via `.cursor/rules/godmode-shipping.mdc`.
*   **Claude Code:** Reads principles via `CLAUDE.md`.
*   **Agy / CLI Agents:** Natively enforced via the prompt orchestrator.
*   **Execution:** You (the AI) must present the Pre-Launch Checklist to the user before confirming a task is completely finished.

## 1. Overview
This skill provides domain-specific logic and rules for its respective BDB pipeline component to ensure standardization across multi-agent workflows.

## 2. When to Use
- Use when specifically requested by the user or triggered by an orchestration agent.
- Use when the current task aligns with the skill's domain.
- Exclude when standard tool execution is sufficient.

## 3. Core Process
1. Read the provided context and ensure preconditions are met.
2. Run the required script or tool and confirm the state change.
3. Verify exit codes, file modifications, or DB counts to guarantee success before reporting completion.

## 4. Common Rationalizations
| Rationalization | Reality |
|---|---|
| "The code change was small, so I skipped updating OpenWiki docs." | Every state change must be reflected in the relevant system records. |
| "The ingest script exited without an error, so the memB index must be updated." | Silent failures happen; explicit verification of the side effect is mandatory. |
| "I'll let the /startcycle proceed without a defined rollback path." | Proceeding without a rollback path corrupts the workflow integrity and safety. |
| "I trust the cached agent registry instead of rescanning after a skill change." | Caches stale out quickly; explicit rescans prevent ghost failures. |

## 5. Red Flags
- Bypassing the verification step after a script execution.
- Proceeding to the next pipeline stage without confirming the previous stage's side effects.
- Ignoring domain-specific constraints listed in this skill.

## 6. Verification
- [ ] Verified script exit codes are explicitly checked.
- [ ] Confirmed target files or database records reflect the expected change.
- [ ] Ensured no silent failures were ignored before reporting success.

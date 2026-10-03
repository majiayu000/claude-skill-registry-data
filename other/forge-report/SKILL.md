---
name: forge-report
description: Produces the standard end-of-task Forge report — project adaptation, agent ledger, memory update. Use when delivering the result of any non-trivial /forge build, fix, or review.
---

# Forge delivery report

Be concrete and honest; reflect **only** checks that actually ran. Never claim agents/Codex/tests/preview that did not really happen. Do not say "done" if it isn't. Include all sections below.

## 0. Chat reply vs the file on disk (v2.9.0, usage-minimisation)
The 14 sections below are the CONTRACT for `.claude/forge-runs/<run_id>/final-report.md` — never trimmed, never skipped, always complete on disk. What actually goes in the **chat reply** is a SHORT summary only: **verdict** (Section 13's one-line pick) · **what changed** (2-4 lines, from Sections 3-4) · **checks run** (Section 5's real commands, one line each) · **blockers** (Section 11, or "none") · **next step** (Section 14) — then the exact path to the full report for anyone who wants the rest. Never re-paste the whole file into chat by default; the owner can always open the path. A small L1 fix may compress this into 3-5 plain lines. A large/client deliverable still gets this short chat form **plus** the complete file — never a full re-paste in chat instead of writing the file.

## 1. Classification
task type · complexity (L#) · START NEW or CONTINUE · active project folder · fan-out level used.

## 2. Project Adaptation
detected project type (incl. any **custom taxonomy** for unknown project types) · detected stack · selected agents · **custom subagents created** (+ why) · optional agents · **agents not used and why** · playbooks loaded · why this team fits the project.

## 2b. Mission Blueprint + Skill Discovery
- Blueprint: one-line expanded mission · quality target · do-not-touch list · definition of done.
- **Skill Discovery:** required capability areas · skills selected · skills assigned to subagents · **custom skills created** (path) · skills not selected + why · missing skills · fallback plan. Confirm every executable subagent had an assigned skill/method (or honest BLOCKED).

## 3. What was done
Plain summary.

## 4. Files changed
Paths (all inside the project), one-line note each.

## 5. Checks/tests run
Actual commands + results only. No fabricated output. Before declaring a run complete, run `node .claude/forge-bin/forge-verify.cjs <run_id>` and report its result; a mismatch means rework, not a pass.

## 6. Agent Activity Ledger (required table — evidence, no fake claims)
Each row has a **Runtime** (ECC agent · ECC skill · native/main · Codex) and a Status. Statuses ONLY: `ECC REAL INVOKED` · `ECC SKILL LOADED` · `NATIVE AGENT INVOKED` · `INTERNAL ROLE ONLY` · `NOT USED` · `FAILED` · `BLOCKED`.

| Agent | Custom? | Runtime | Skill / source | Status | Project role | Task | Files read | Files changed | Evidence | Result |
|-------|---------|---------|----------------|--------|--------------|------|-----------|---------------|----------|--------|

If a real ECC subagent was dispatched → `ECC REAL INVOKED` (Runtime = ECC agent). If an ECC skill/playbook ran → `ECC SKILL LOADED` (Runtime = ECC skill). If a native/main-session agent did the work as a labeled fallback → `NATIVE AGENT INVOKED` (Runtime = native). A thinking role → `INTERNAL ROLE ONLY`. ECC tried but unavailable/blocked → `BLOCKED`. Mark **Custom?** = yes for Lead-created custom roles and give the assigned **Skill / source** (ecc-skill/forge-skill/project-local/native/internal). **Never label a native role as ECC, or claim a custom subagent/skill that wasn't really created.** Don't claim parallel agents unless they really ran separately. Evidence = command output / file diff / tool result / commit hash / log line / created file — or an explicit note that evidence is unavailable and why.

## 6c. Rework loop (if any)
rework tasks created · how many fixed · retests run · loop iterations (max 2 / 3 high-end) · anything left blocked. No fabricated fixes.

## 6b. ECC Status block (required — ECC-first honesty)
- **ECC Normal Mode:** ON / OFF / BLOCKED (from `FORGE_ECC_MODE.json`)
- **ECC Full Test Mode:** OFF / ON (opt-in only)
- **ECC attempted:** yes / no
- **ECC agents selected / invoked:** <list> / <list>
- **ECC skills loaded:** <list>
- **ECC succeeded:** yes / no / partial
- **Native fallback used:** yes / no — and which agents
- **ECC blocked reason (if any):** ECC unavailable · ECC skill not found · ECC agent failed · task too small (no ECC needed) · …
Be honest: if Forge used native roles because ECC was unavailable/blocked/too-small, say exactly that — never present native work as ECC.

## 7. Memory Update
- `FORGE_PROJECT_PROFILE.md`: created / updated / unchanged
- `FORGE_MEMORY.md`: created / updated / unchanged
- `FORGE_DECISIONS.md`: created / updated / unchanged
- `FORGE_TASK_HISTORY.md`: created / updated / unchanged
- `FORGE_AGENT_LEDGER.md`: created / updated / unchanged
- Summary of memory changes · any uncertain/inferred memory.

## 8. Dashboard Update (no fake starts)
The dashboard is the **Command Center** (`http://127.0.0.1:4100`, owner decision 2026-07-31 — one dashboard for every project); the old per-project Control Center was **REMOVED in v2.9.0** (2026-09-27, not merely retired — the file and its UI no longer exist) and only its `log-event.cjs` stays in service as the run-event writer. Report the Command Center first:
- Command Center health check: passed / failed / not run (`GET http://127.0.0.1:4100/api/health` — **the report may only say the dashboard runs if this passed**)
- Command Center URL: http://127.0.0.1:4100 (only when the health check passed)
- latest run id: <id> · events written: <n> (via `.claude/forge-dashboard/log-event.cjs`)
- **Forge Session Mode:** on / paused / off (from `FORGE_SESSION_STATE.json`)
If the owner explicitly said `legacy dashboard` this run: there is nothing to start or report on any more — say in one line that the old Control Center was removed in v2.9.0 and the dashboard is the Command Center above.
Allowed wording: "Command Center health check passed (4100)." · "Command Center not reachable — Forge tried to start it itself (supervisor) and it is still not answering." · "Command Center not installed in this project (optional) — continuing without it." · "Events written via log-event.cjs; dashboard not started (not requested)." Never print a start/build command for the user to run, and never claim a URL is live unless tested/confirmed.

## 8b. Command Pack Update (include on install / when it changed)
- forge-bin installed: yes/no · PowerShell scripts: installed/not · CMD scripts: installed/not · Bash scripts: installed/not
- package.json scripts: added / skipped (no package.json) / conflict
- VS Code tasks: added / example file / skipped
- commands tested: <list> · commands not tested: <list>
- how to start dashboard — PowerShell: `.\.claude\forge-bin\forge-dashboard.ps1` · CMD: `.claude\forge-bin\forge-dashboard.cmd` · Bash: `bash .claude/forge-bin/forge-dashboard.sh` (Forge defines no npm scripts — never document any)

## 8c. Project governance (CLAUDE.md + custom skills)
- **CLAUDE.md:** created / updated (safe-merge) / existed·no change / conflict — and **what existing instructions were preserved** (never silently deleted).
- **Custom project-local skills:** `.claude/skills/<name>/SKILL.md` created / updated / used (by which subagent) / skipped / conflict. Each is real, documented, and linked to a work package.
- **Four things maintained:** CLAUDE.md (brain) · `.claude/skills/*` (capabilities) · Forge memory · dashboard.
- Conflicts (if any) are listed here and were owner-approved before any deletion.

## 9. Issues found
## 10. Issues fixed
## 11. Remaining risks

## 12. Codex block (v7.1 — exact state, never faked)
- Codex considered / invoked: · **Codex state** (one of): `CODEX REAL INVOKED` · `CODEX BLOCKED: TRUST/TTY` · `CODEX BLOCKED: NO GIT` · `CODEX BLOCKED: NO OUTPUT` · `CODEX NOT AVAILABLE` · `CODEX NOT INVOKED` · `CODEX FALLBACK USED`.
- If blocked: cite `artifacts/codex-unlock-diagnosis.md` (CLI/version/auth/git/TTY/trust/exit-code) and state in one plain line that Codex was not run and why — **never hand the user a manual command to run**; the diagnosis artifact keeps the attempted command only as an internal record. Never claim Codex proof without real output.

## 12b. Browser proof + Skill Registry + Fresh-install (v7.1)
- **Browser proof:** tool used · dashboard URL · run id · lenses checked · screenshot paths · layout observations · pass/fail — or **PARTIAL** with the exact reason (no Playwright/Chrome). Cite `artifacts/dashboard-browser-proof.md`. Never claim a screenshot you didn't take.
- **Skill Registry:** `.claude/FORGE_SKILL_REGISTRY.md` created/updated/checked + entries touched.
- **Fresh-install verification (if run):** CLAUDE.md · skills dir · registry · memory · session · dashboard starts · ECC Normal ON/Full Test OFF · project-local only → `artifacts/fresh-install-verification.md`.

## 13. Final verdict (strict, v7.1)
Pick ONE overall level + give the per-layer verdicts. Do **not** use FULL PASS if a required Codex/browser proof was blocked.
- **FULL PASS** — all critical requirements proven; Codex proof passed or not required; browser proof passed if dashboard changes were tested; no critical PARTIALs.
- **PASS CORE / PARTIAL PROOF** — core Forge behavior passed; one or more proof layers missing; no safety/isolation failure.
- **PARTIAL** — an important required feature unproven/blocked; fallbacks used; manual follow-up needed.
- **BLOCKED** — cannot safely/honestly complete. A BLOCKED status requires a real recovery ledger, not just an assertion: `node .claude/forge-bin/forge-recovery.cjs check-block <record.json>` must report `ok:true` (≥3 alternatives attempted, ≥5 for a high-value item, a Verify-Agent verdict, non-empty queries/tools). While `check-block` reports `ok:false`, BLOCKED is not yet a valid final status — keep attempting safe alternatives first (`GLOBAL_RESEARCH_RECOVERY_POLICY.md`).
- **FAIL** — critical requirement failed · safety/isolation violated · fake claim detected · required artifact missing.

Per-layer (state each): **Core** · **Codex** · **Browser proof** · **Dashboard** · **Project isolation** · **Overall**.

## 14. Next step
Single most useful next action.

The FILE on disk keeps every section above in full. The CHAT reply stays short — see Section 0.

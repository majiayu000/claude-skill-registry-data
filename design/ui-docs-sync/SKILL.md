---
name: ui-docs-sync
description: Verify that repository documentation, product contracts, route docs, and UI spec packages are linked and consistent. Use after creating or updating a UI spec package, after changing product documentation, or before onboarding an agent or developer who will rely on repository docs to understand the UI.
status: stable
---

# UI Docs Sync

A skill for verifying that repository-level documentation (READMEs, product contracts, route maps, AGENTS.md, CLAUDE.md, folder context files) agrees with the UI specification packages that describe individual screens and components. It does not validate the spec package internally — that is `ui-spec-linter`'s job. It does not compare the implementation to the spec — that is `ui-redline`'s job. Its specific job is the link between the two: do the repository's general docs say the same thing the UI specs say?

## When to use this skill

Use this skill when:
- A new UI spec package has been created and you want to confirm repository docs reference it.
- Repository documentation was updated (route map, product truth doc, README) and you want to confirm it does not contradict existing spec packages.
- An agent or developer is being onboarded to a repo and needs to trust that docs and specs agree.
- A retrospective spec recovery package has been created and the repo docs have not been updated to reflect it.

Do **not** use this skill when:
- No UI spec packages exist yet. There is nothing to sync to.
- The user wants to validate the internal consistency of a spec package. Use `ui-spec-linter` for that.
- The user wants to compare the implementation against the spec. Use `ui-redline` for that.
- There is no repository-level documentation to check (e.g., a brand-new empty repo). There is nothing to sync from.

## Core principle

**Repository docs and UI specs are different artifacts that describe the same product. Drift between them is invisible until it causes damage.** A README that says `/create` is a manual-entry flow while the recovered spec says it is an AI-first flow is not an academic inconsistency — it is a trap for every developer and agent who reads the README. This skill makes that drift visible and fixable before it causes harm.

## What counts as repository documentation

Repository docs are any files that describe the product at a scope larger than a single screen or component:

| Doc type | Examples |
|---|---|
| Root README | `README.md`, `docs/README.md` |
| Agent/AI instructions | `AGENTS.md`, `CLAUDE.md`, `.cursorrules`, `copilot-instructions.md` |
| Route maps | `docs/routes.md`, `docs/saas-frontend/README.md`, `ROUTES.md` |
| Product contracts | `docs/product-truth.md`, `docs/ux-contract.md`, UX north-star docs |
| Folder context files | `folder_context.md`, `CONTEXT.md` per directory |
| Architecture docs | `docs/architecture.md`, `docs/frontend.md` |
| Onboarding guides | `docs/getting-started.md`, `CONTRIBUTING.md` |

What does **not** count as repository documentation for this skill's purposes:
- Spec package files themselves (`brief.md`, `blueprint.md`, etc.)
- Inline code comments
- Changelog entries

## Monorepo-specific documentation

For **monorepo repositories** with app-level or platform-level subdirectories, check for documentation files at **multiple levels**:

- **Root level:** `README.md`, `AGENTS.md`, `CONTEXT.md` (applies across the whole repo)
- **App/platform level:** `metamorfose-platform/AGENTS.md`, `docs/saas-frontend/CONTEXT.md` (applies to a subproject)
- **Per-directory level:** `src/pages/create/CONTEXT.md`, `src/components/CONTEXT.md` (applies to a subtree)

A spec package may be documented at multiple levels. For example, a route may be mentioned in both the root `AGENTS.md` and the app-level `metamorfose-platform/AGENTS.md`. **Check all levels** — missing links at the app level can be just as damaging as missing root-level links, since agents navigating the app directory will only see the app-level docs.

## What counts as a UI spec package

A spec package is a collection of files in a directory that together describe a single UI scope (route, flow, screen, or feature). A package is discoverable by the presence of any of these signals, in priority order:

1. A `00-index.md` file in the directory
2. A `brief.md` or a numbered equivalent (`02-brief.md`, `01-brief.md`, etc.)
3. A directory containing two or more canonical spec file names (`blueprint.md`, `screen-spec.md`, `acceptance.md`, etc.)

## Checks to run

### Check 1 — Spec package discovery

Find all UI spec packages in the repository. For each package found, record:

| Field | Where to read it |
|---|---|
| Route / scope name | `00-index.md` frontmatter `scope` field, or inferred from directory name |
| Primary component | `00-index.md` or `brief.md` §1 |
| Primary user | `00-index.md` or `brief.md` §2 |
| Primary action | `00-index.md` or `brief.md` §3 |
| Package status | **Lowest** maturity `status` found across required spec files (see rule below) |
| Index present | Yes / No — whether `00-index.md` exists |

**Package status rule:** Use the *lowest* maturity value among the required spec files, not the highest. A package with one `complete` file and five `draft` files is still `draft`.

Status values in ascending maturity order: `draft` → `current` → `approved` → `complete`. If any required file has no `status` field, treat it as `draft`.

Required files for status calculation: `brief.md` (or numbered equivalent), `blueprint.md`, `screen-spec.md`, `acceptance.md`. Optional files (`flow.md`, `system.md`, `microcopy.md`, `component-specs/*`) are included if present.

---

### Check 2 — Repository docs reference each spec package

For each spec package discovered in Check 1, search repository documentation for references to the package's route, scope name, or primary component.

A reference is valid if the repo doc:
- Links to the spec package directory or a specific spec file, **or**
- Names the route and matches the primary component name

**Flag as missing link** if no repository doc references the spec package at all.

**Flag as stale link** if a repo doc references the spec package path but the path no longer exists or the index no longer has a matching scope.

---

### Check 3 — Source-of-truth consistency

For each spec package, identify the primary factual claims made about the UI scope. Then search repository docs for contradicting claims.

**Factual claims to extract from the spec package:**

| Claim type | Where to read in spec | Example |
|---|---|---|
| Primary user | `brief.md §2` | "Marketing team members" |
| Primary action | `brief.md §3` | "Create a short-form video post with AI assistance" |
| Creation mode | `brief.md §4 or §5` | "AI-first: AI generates the first draft" |
| Auth requirements | `brief.md §7 Constraints` | "Requires authenticated user; redirects to login if not" |
| Platform / breakpoint | `brief.md §7 Constraints` | "Desktop-first, mobile read-only" |
| Non-goals | `brief.md §8` | "Batch creation is explicitly out of scope" |

**Compare each claim against repository docs.** A contradiction occurs when:

- The repo doc makes an explicit claim about the same aspect that differs from the spec claim.
- The repo doc implies a different assumption (e.g., describes the flow as manual when the spec says AI-first).

Do **not** flag:
- Repo docs that are silent on a point. Silence is not a contradiction.
- Repo docs that use different phrasing for the same concept — resolve it as "equivalent" if the meaning matches.

---

### Check 4 — Open drift items visible at repo level

Check whether unresolved lint and redline findings from spec packages are surfaced anywhere in the repository docs.

Read the spec linter report (`09-spec-linter-report.md` or equivalent) and redline report (`10-redline-report.md` or `redlines/` directory) for each spec package. For each **blocker** or **major** finding that remains unresolved, check whether:

- The finding is mentioned in the spec package's `00-index.md` open items section, **or**
- The finding is referenced in any relevant repository doc

**Flag as invisible drift** if a blocker or major finding has no visibility in any repo-level document.

---

## Output template

Produce the sync report in this exact structure. Save it as `ui-docs-sync-report.md` in the spec package root, or in a `sync-reports/` directory if multiple packages were audited.

```markdown
---
spec_type: docs-sync-report
scope: <repo name or sub-system name>
packages_audited: <N>
created: <YYYY-MM-DD>
status: draft
---

# UI Docs Sync Report

**Repo / scope:** <name>
**Date:** <YYYY-MM-DD>
**Packages audited:** <N>
**Result:** PASS / FAIL (<N> issues found)

---

## 1. Spec packages found

| Route / scope | Directory | Index present | Package status | Notes |
|---|---|---|---|---|
| /create | `docs/specs/create/` | Yes | approved | — |
| /settings | `docs/specs/settings/` | No | draft | No 00-index.md |

---

## 2. Repository docs linked to spec packages

| Spec package | Repo doc | Link present? | Link type | Notes |
|---|---|---|---|---|
| /create | `docs/saas-frontend/README.md` | No | — | Missing — no reference found |
| /settings | `AGENTS.md` | Yes | Named reference | Mentions `settings-page spec package` |

---

## 3. Source-of-truth consistency

| Claim type | Spec says | Repo doc says | Doc location | Status |
|---|---|---|---|---|
| Primary action | "AI generates first draft" | "User manually enters content" | `docs/README.md §3` | ⚠ Contradiction |
| Auth requirement | "Requires login" | "Public-facing creation flow" | `AGENTS.md §Routes` | ⚠ Contradiction |
| Non-goals | "Batch creation out of scope" | _(silent)_ | — | OK — silence is not contradiction |

---

## 4. Open drift items

| Severity | Spec package | Finding | Visible in 00-index? | Visible in repo docs? |
|---|---|---|---|---|
| Blocker | /create | "Usar este Reel ✓ is a silent no-op — no handler wired" | Yes | No |
| Major | /create | "purple-500 literal violates token contract" | Yes | No |

---

## 5. Recommended changes

List concrete, actionable fixes ordered by severity:

1. **Add link:** `docs/saas-frontend/README.md` should link to `docs/specs/create/00-index.md`.
2. **Resolve contradiction:** `docs/README.md §3` says "user manually enters content" — update to "AI generates first draft (manual override available)" per `brief.md §4`.
3. **Resolve contradiction:** `AGENTS.md §Routes` says `/create` is "public-facing" — update to "auth-gated, redirects to login" per `brief.md §7`.
4. **Promote index:** Add `00-index.md` to `/settings` spec package so it is discoverable.

---

## 6. What was not checked

- <List areas that were out of scope or impossible to verify — e.g., "Production route map was not accessible; only file-based docs were checked.">
- <List any repo docs that could not be parsed — e.g., "AGENTS.md references an internal wiki; external links were not followed.">
```

---

## Handoff rule

If missing links or stale paths are found in agent-facing files (e.g., `CLAUDE.md`, `AGENTS.md`, `GEMINI.md`, `.github/copilot-instructions.md`, `llm-docs/`, or folder context files), do not attempt to repair them here. Produce the audit report and recommend `ui-agent-routing` as the next skill to run.

## How `ui-docs-sync` differs from adjacent skills

| Skill | What it checks |
|---|---|
| `ui-spec-linter` | Spec files agree with each other (internal package consistency) |
| `ui-redline` | Implementation agrees with the spec |
| `ui-docs-sync` | Repository docs agree with UI specs (cross-artifact consistency) |
| `ui-agent-routing` | Wires routing files so agents discover the active spec (applies or plans edits) |
| `ui-orchestrator` | Which skill to run next |
| `ui-surface-inventory` | What scopes need specs |

These are complementary, not redundant. Running all three closes the full consistency loop:

```
ui-spec-linter     → spec package is internally clean
ui-redline         → code matches the spec
ui-docs-sync       → repo docs match the spec
```

---

## Workflow

### Step 1 — Discover spec packages

Scan the repository for directories that contain at least one spec signal (see "What counts as a UI spec package" above). List all packages found. If `00-index.md` exists in a directory, use it as the authoritative source of metadata for that package.

### Step 2 — Collect repository docs

List all repository-level documentation files in scope (see "What counts as repository documentation"). Read each one to understand what claims it makes about routes, scopes, users, actions, and constraints.

### Step 3 — Run Check 2 (link coverage)

For each spec package, search every repo doc for references. Record the result in the output table.

### Step 4 — Run Check 3 (source-of-truth consistency)

For each spec package, extract the six factual claim types from the brief. Compare against repo docs. Record any contradiction.

### Step 5 — Run Check 4 (open drift visibility)

For each spec package, read the linter and redline reports if they exist. For each unresolved blocker or major, check whether it appears in the index or any repo doc.

### Step 6 — Produce the report

Compile all findings into the output format above. Order recommended changes: contradictions first, missing links second, drift visibility third.

### Step 7 — Confirm with the user

Show the report. Ask: "Any of these contradictions do you think are actually intentional (repo doc is right, spec is wrong)?" Capture any reversals before finalizing.

---

## Anti-pattern rules

1. **Do not flag silence as contradiction.** A repo doc that does not mention `/create` is not contradicting the spec. It is simply not yet linked. Record it as a missing link, not a contradiction.
2. **Do not evaluate spec quality.** If the spec says something unusual, that is for `ui-spec-linter` to catch. This skill accepts spec files at face value and checks whether repo docs agree.
3. **Do not auto-update repo docs.** This skill produces a report, not a patch. The user decides which recommended changes to apply.
4. **Do not require `00-index.md` to run.** A spec package without an index is a valid input. Record its absence as a finding, but still run the checks.
5. **Do not follow external links.** Only check files that exist in the repository. External URLs in repo docs are out of scope.

---

## Acceptance criteria for this skill's output

A sync report produced by this skill is acceptable only if every one of these is true:

- [ ] All spec packages in the repository scope were discovered and listed.
- [ ] All six repository doc types (README, agent instructions, route maps, product contracts, folder context, architecture docs) were checked where they exist.
- [ ] Every spec package in the report was checked for missing links in at least one repo doc.
- [ ] Every contradiction in Check 3 cites both the spec claim and the repo doc claim with file location.
- [ ] Every unresolved blocker or major from linter/redline reports is listed in Check 4, even if they are already visible.
- [ ] The recommended changes are concrete and actionable — not "improve docs" but "add link from X to Y" or "update claim in file Z section §N".
- [ ] Section 6 ("What was not checked") is present and honest about scope limits.

If any check fails, revise before delivering.

---

## Promotion checklist

### Evidence on the settings-page fixture

- [x] Running this skill against `examples/settings-page/` against the repository's own README and docs produces a sync report that passes every Acceptance criteria item above.
- [x] The report identifies at least one link that should exist between the spec package and a repo doc (even if the settings-page example is well-maintained).
- [x] Section 6 correctly lists which doc types were not in scope for the settings-page (e.g., architecture docs, route maps).

### Evidence on the spec-recovery-create fixture

- [x] Running this skill after the recovery package reaches `approved` status identifies any gaps between the recovery findings and the repository's external docs.
- [x] If there are no gaps, the report correctly returns PASS with a "What was not checked" section explaining what was excluded.

### Package status rule

- [x] The sync report's frontmatter `status` is computed as the LOWEST maturity among the four required files (`brief.md`, `blueprint.md`, `screen-spec.md`, `acceptance.md`) — not the highest.
- [x] A package where `acceptance.md` is `draft` and `brief.md` is `approved` results in a sync report with `status: draft`.

### Skill integration

- [x] `validate-skill.py` passes for this skill with `status: stable` (no missing sections).
- [x] `skills.json` entry for `ui-docs-sync` has been updated to `"status": "stable"`.
- [x] README core workflow ends with `ui-docs-sync` (already true — verify).
- [x] README Skill Map table has been updated to show `stable`.

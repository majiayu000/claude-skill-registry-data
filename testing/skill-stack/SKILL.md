---
name: skill-stack
description: "Curated skill bundle installer keyed to project archetype. Classifies the repo as one of six archetypes (Next.js SaaS, Flutter app, API backend, CLI tool, data pipeline, mobile game), maps it to a 5-8 skill stack covering the whole lifecycle (build, test, review, deploy, docs)."
version: "2.0.1"
category: meta
platforms:
  - CLAUDE_CODE
---

You are an autonomous skill stack curator. Do NOT ask the user questions during classification
or planning; present the manifest, then confirm once before installing.

TARGET: $ARGUMENTS

- With arguments: treat them as an archetype override or constraint (e.g. "flutter", "no deploy
  skills", "max 5"). Honor the override but still run classification and report any mismatch.
- Without arguments: classify the archetype purely from repo files.

=== PRE-FLIGHT ===

1. Confirm a project root: `.git` or at least one manifest file (`package.json`, `pubspec.yaml`,
   `pyproject.toml`, `go.mod`, `Cargo.toml`). If none, stop: "No project detected; skill-stack
   needs a repo to classify."
2. Check registry access with `npx @skills-hub-ai/cli search test --limit 1`; fall back to
   `curl -s "https://skills-hub.ai/api/v1/skills?q=test&limit=1"`. If both fail, continue in
   PLAN-ONLY mode: produce the manifest and .claude/skill-stack.md but perform no installs.
3. Inventory installed skills from `~/.claude/skills/` and `.claude/skills/`; record slugs.
4. Ensure `.claude/` is writable (create the directory if absent). If the repo forbids writes,
   emit the manifest to the conversation only and say why.

=== PHASE 1: ARCHETYPE CLASSIFICATION ===

1. Score each archetype from file evidence (strongest match wins):
   - Next.js SaaS: `next` in package.json deps, `app/` or `pages/`, auth/billing deps
     (stripe, next-auth, clerk).
   - Flutter app: `pubspec.yaml` with `flutter:` block, `lib/main.dart`.
   - API backend: express/fastify/nest/django/fastapi/rails/go http servers, `routes/` or
     `controllers/`, no meaningful frontend directory.
   - CLI tool: `bin` field in package.json, `cmd/` in Go, `[project.scripts]` in
     pyproject.toml, clap/cobra/commander deps.
   - Data pipeline: airflow/dagster/prefect/dbt configs, `notebooks/`, heavy pandas/spark deps,
     scheduled job definitions.
   - Mobile game: unity/godot project files, flame (Flutter) or SpriteKit deps, `assets/`
     dominated by sprites and audio.
2. Record the winning archetype, its evidence (files/deps), and the runner-up. Hybrid repos
   (e.g. Next.js SaaS with an API backend inside) take the primary archetype plus up to 2
   supplemental skills from the secondary.
3. If $ARGUMENTS named an archetype that contradicts the evidence, use the user's choice but
   flag the contradiction in the manifest.

VALIDATION: exactly one primary archetype selected, with at least two pieces of file evidence.
FALLBACK: if no archetype scores any evidence, fall back to a generic stack (test, review,
security, docs) and label the classification "generic".

=== PHASE 2: STACK MAPPING ===

1. Map the archetype to 5-8 skills spanning the lifecycle. Every stack must cover all five
   phases: build, test, review, deploy, docs. Reference mapping (adjust to what the registry
   actually returns; these are search queries, not guaranteed slugs):
   - Next.js SaaS: nextjs scaffolding, unit-test, e2e/playwright, security-review, stripe or
     billing, seo/web-quality, deploy/preview-smoke, api-docs.
   - Flutter app: flutter build patterns, unit/widget test, mobile-qa, app-store publish,
     accessibility, design tokens.
   - API backend: api scaffold, integration-test, load-test, security/owasp, api-docs, db
     migration checks.
   - CLI tool: cli scaffolding, unit-test, release/changelog, readme/docs, packaging.
   - Data pipeline: pipeline-health, data validation tests, monitoring, cost analysis, runbook.
   - Mobile game: asset pipeline, performance profiling, mobile-test, store publish, analytics.
2. Resolve each intended slot to a real skill: search the registry per slot
   (`npx @skills-hub-ai/cli search "<slot query>" --limit 5`) and pick the highest-rated match.
   A slot with no acceptable match is recorded as UNFILLED with the query used.
3. Mark each resolved skill INSTALLED (already present from Pre-flight inventory) or MISSING.

VALIDATION: 5-8 resolved slots; each of the five lifecycle phases has at least one slot that is
resolved or explicitly UNFILLED; every resolved slug came from an actual search result.
FALLBACK: in PLAN-ONLY mode (no registry), keep the slot queries as the manifest content and
mark every slot UNRESOLVED (planned), so the user can run the searches later.

=== PHASE 3: MANIFEST AND INSTALL ===

1. Present the manifest table (see OUTPUT) listing every slot, its resolved skill, status, and
   the reason it is in the stack. This is user-visible BEFORE any install.
2. Ask exactly one question: "Install the {N} missing skills? (all / pick / none)". If
   $ARGUMENTS pre-authorized ("install", "yes to all"), skip the question.
3. Install approved skills one at a time: `npx @skills-hub-ai/cli install <slug>`. After each,
   verify `~/.claude/skills/<slug>/SKILL.md` exists and has parseable frontmatter. One retry on
   failure, then mark FAILED with the captured error.
4. Never bulk-install with a single opaque command; the user must see each slug go in.

VALIDATION: every attempted install has a verified on-disk result recorded (OK/FAILED).
FALLBACK: if more than half the installs fail, stop installing, report the pattern (likely
network or CLI version), and leave the remaining slots as manual commands.

=== PHASE 4: RECORD THE STACK ===

1. Write `.claude/skill-stack.md` with: date, classified archetype + evidence, the full slot
   table (skill, lifecycle phase, status, one-line rationale), unfilled slots with their search
   queries, and a "revisit" note (re-run skill-stack after major stack changes).
2. If the file already exists, merge: keep prior entries, append this run as a dated section,
   and mark superseded picks. Never silently overwrite history.
3. Do not commit; leave the file staged-ready and mention it in the output.

VALIDATION: file exists, contains today's dated section, and lists every slot from Phase 2.
FALLBACK: if the repo is read-only, emit the identical content in the conversation output and
note that it could not be persisted.

=== OUTPUT ===

## Skill Stack Manifest — {archetype}

**Evidence:** {files/deps} | **Runner-up:** {archetype or none} | **Mode:** {full / plan-only}

| Lifecycle | Slot         | Skill  | Status                                      | Why      |
| --------- | ------------ | ------ | ------------------------------------------- | -------- |
| test      | e2e coverage | {slug} | INSTALLED / MISSING->OK / FAILED / UNFILLED | {reason} |

**Installed this run:** {n} verified, {n} failed
**Unfilled slots:** {slot: search query to retry}
**Recorded in:** `.claude/skill-stack.md`

=== SELF-REVIEW ===

Score 1-5 on: Complete (all five lifecycle phases addressed), Robust (every slug verified or
honestly marked, fallbacks used where needed), Clean (manifest readable, rationale specific to
this repo). Any score below 4: name the gap, fix in-run if possible (e.g. search an uncovered
phase), otherwise record it as a known limitation in the manifest.

=== LEARNINGS CAPTURE ===

Append to `~/.claude/skills/skill-stack/LEARNINGS.md` (create if missing): date + archetype,
which slot queries resolved well vs poorly, awkward moments (misclassification, dead slugs),
one suggested patch to the archetype map, verdict [Smooth | Minor friction | Major friction].

=== STRICT RULES ===

1. Never install without the manifest being shown first and consent given (or pre-authorized).
2. Never invent slugs; every resolved skill must come from a real search result this run.
3. Every stack must cover build, test, review, deploy, docs, or explicitly mark the phase
   UNFILLED with the query that failed.
4. Never overwrite an existing .claude/skill-stack.md; append a dated section.
5. Verify every install on disk; exit code 0 is not proof.
6. An archetype claim requires at least two pieces of file evidence, or it is "generic".

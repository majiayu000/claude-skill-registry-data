---
name: gaia-suite-intake
description: >
  Comprehensive, reusable playbook for multi-component suite intake under Yggdrasil III.
  Audits component installability, maps origin candidates to generic capabilities, ingests
  named components with shared-repo baseline caps, manifests suites via gaia dev fuse,
  calibrates capstone and component ranks, and closes out via Class S regeneration.
---

# gaia-suite-intake

End-to-end playbook for ingesting, structuring, and calibrating multi-component skill
suites under **Yggdrasil III**.

A **suite** is a cohesive collection of specialized skills authored by a contributor or team,
anchored by a central **capstone** skill that coordinates or unifies them (e.g. `gsd-build/get-shit-done`,
`leonxlnx/taste-skill`, `obra/superpowers`). Ingesting a suite requires orchestrating multiple
interlocking layers: component installability, generic capability mappings, shared repository
evidence capping, suite manifestation via `gaia dev fuse`, branch-aware calibration, and Class S
artifact regeneration.

---

## Yggdrasil III Normative Rules & Invariants

Before executing any intake steps, verify understanding of these foundational invariants:

1. **Type Axis Collapse**:
   - The starless node `type` is strictly `{basic, fusion}`.
   - `extra`, `ultimate`, and `unique` are **retired as types** — never write them to node JSON.
2. **Derived Branch Taxonomy**:
   - Branch (`standard` / `suite` / `unique`) is derived dynamically, never hard-coded.
   - A skill carrying `suiteComponents` sits on the **Suite branch** at any rank (1★–6★).
   - Standalone skills without `suiteComponents` sit on `standard` (1★–3★) or `unique` (4★–6★).
3. **Trust Magnitude as Sole Promotion Authority**:
   - The legacy per-star Evidence Floor is completely retired.
   - `fusion-recipe` rows contribute **0 TM** (Issue #1600). Structural composition is
     reported separately via **Fusion Score**, which gates no rank.
4. **Shared Repository Evidence Cap**:
   - Sub-components inheriting repository evidence from a shared parent repo are capped at
     `SUITE_COMPONENT_REPOSITORY_CAP = 50.0 TM` per component (`META.md` §2.1, `trustMagnitude.py`).
   - Repository adoption alone cannot promote sub-components beyond Grade B (50 TM / 3★)
     without independent corroboration.
5. **Branch-Aware 4★ Gate (`META.md` §4 / Issue #1741)**:
   - **4★ Promotion Requirement**: Requires Overall Trust Grade A (TM ≥ 100) and live verified
     blob evidence (The Star Bar, `META.md` §2.4).
   - **Unique Branch** (standalone, no `suiteComponents`): 4★ Unique requires **bucket-level Origin**
     on its generic bucket (`META.md` §4.1).
   - **Suite Branch** (capstone carrying `suiteComponents`): 4★ Extra does **NOT** require
     bucket-level Origin on its generic bucket. The capstone represents the suite cluster rather
     than a single generic bucket monopoly. Suite origin requirements apply at **5★ Ultimate**
     (proposer must hold Origin on ≥1 of the `suiteComponents` per `META.md` §4.2).
   - *Precedents*: `leonxlnx/taste-skill` (4★ Extra, `origin: false` on generic `design-generation`),
     `gsd-build/get-shit-done` (4★ Extra).

---

## Inputs

Gather these before beginning:

| Input | Description | Example |
|---|---|---|
| `contributor` | GitHub organization or username | `leonxlnx` |
| `suite-slug` | Identifier for the suite capstone | `taste-skill` |
| `repo-url` | Canonical GitHub repository URL | `https://github.com/leonxlnx/taste-skill` |
| `default-branch` | Default git branch of the upstream repo | `main` |
| `components` | List of sub-skill directories / files | `brandkit`, `minimalist-skill`, ... |

---

## Phase 1: Upstream Suite Inspection & Installability Audit

Inspect the upstream repository structure and audit every component before touching the registry.

### 1.1 Repo Structure & Component Identification

Inspect the remote repository using `gh` or clone locally in a temporary directory:

```bash
gh repo view <owner>/<repo> --json defaultBranchRef,stargazerCount,description
```

Locate all component `SKILL.md` files:
- Typical layouts: `skills/<component-name>/SKILL.md`, `plugins/<name>/SKILL.md`, or top-level directories.
- Identify the **capstone**: the primary entry point, meta-orchestrator, or root skill that references or coordinates the components.

### 1.2 Frontmatter & Lifecycle Audit

For each component `SKILL.md`, verify:
- Frontmatter exists with valid YAML fences (`---`).
- Required fields: `name`, `description`.
- Instructions / CLI usage: verify how the skill is executed (e.g. `npx`, `uvx`, shell script, or harness prompt).

### 1.3 The Star Bar (Installability Gate)

Per `META.md` §2.4:
- Any skill promoted to **3★ or higher MUST have a verified GitHub BLOB link** pointing to a concrete file (e.g. `https://github.com/<owner>/<repo>/blob/<branch>/.../SKILL.md`), never a bare repo root.
- A missing verified blob link is a hard reset to 1★ (Awakened).
- Construct the exact blob URL for every component and confirm HTTP 200 reachable.

---

## Phase 2: Origin Candidate Analysis & Generic Mapping

Map every component (and the capstone) to a generic capability bucket in `registry/nodes/`.

### 2.1 Capability Resolution

For each component:
1. Search existing generic nodes:
   ```bash
   grep -rn "name: " registry/nodes/
   # or search by id slug
   find registry/nodes -name "*.json" | grep -i "<keyword>"
   ```
2. If a matching generic bucket exists:
   - Check existing named implementations in that bucket:
     ```bash
     grep -rl "genericSkillRef: <generic-id>$" registry/named/
     ```
   - If bucket has no implementations, it is **vacant**. The incoming component is a primary **Origin candidate**.
   - If bucket has an incumbent: evaluate whether the incoming component is demonstrably more renowned. If not, incoming component will have `origin: false`.
3. If no matching generic capability exists:
   - Create a starless generic `basic` node:
     ```bash
     gaia dev add <new-generic-id> \
       --name "<Generic Capability Name>" \
       --description "<Precise, vendor-agnostic capability description>" \
       --type basic \
       --no-build
     ```
   - The incoming component is the sole implementation and therefore an **Origin candidate**.

---

## Phase 3: Ingestion of Named Components & Evidence Scoring

Ingest components programmatically via `gaia dev` verbs. Never hand-edit JSON or frontmatter.

### 3.1 Register Named Skills

For each component:
```bash
gaia dev add --named <contributor>/<component-slug> \
  --generic-ref <generic-id> \
  --name "<Component Display Name>" \
  --title "<RPG Title / Clean Name>" \
  --description "<Component description>" \
  --links github="https://github.com/<owner>/<repo>/blob/<branch>/<path>/SKILL.md" \
  --no-build
```

Also register the named capstone:
```bash
gaia dev add --named <contributor>/<suite-slug> \
  --generic-ref <capstone-generic-id> \
  --name "<Suite Capstone Display Name>" \
  --title "<Suite Title>" \
  --description "<Suite overview description>" \
  --links github="https://github.com/<owner>/<repo>/blob/<branch>/<path-or-readme>" \
  --no-build
```

### 3.2 Add Verified Evidence Rows

Gather verified repository metrics from GitHub API:
- `stargazerCount`: Total stars on the suite repository.
- `commits`: Total commit count.
- `contributors`: Total contributor count.
- `createdAt` / `sourceStartedAt`: Creation timestamp of repo/file.

#### A. Capstone Evidence
Add repository adoption evidence to the capstone:
```bash
gaia dev evidence <contributor>/<suite-slug> \
  --type github-stars-own \
  --source "https://github.com/<owner>/<repo>/blob/<branch>/<path>" \
  --stars <stargazerCount> \
  --source-started-at "<YYYY-MM-DD>" \
  --notes "<stars> stars on <owner>/<repo> repository" \
  --no-build

gaia dev evidence <contributor>/<suite-slug> \
  --type repo-own \
  --source "https://github.com/<owner>/<repo>" \
  --commits <commitCount> \
  --contributors <contributorCount> \
  --source-started-at "<YYYY-MM-DD>" \
  --notes "<commits> commits, <contributors> contributors" \
  --no-build
```

#### B. Component Evidence & Shared Repo Cap
Add component-level evidence. Sub-components residing in the shared repository inherit
adoption signals, but Yggdrasil III enforces:
- `skillCountInRepo`: Set to the total number of components sharing the repository.
- `SUITE_COMPONENT_REPOSITORY_CAP = 50.0 TM`: The scoring engine automatically bounds
  shared repository evidence so that adoption alone caps at 50 TM (Grade B).

```bash
gaia dev evidence <contributor>/<component-slug> \
  --type github-stars-own \
  --source "https://github.com/<owner>/<repo>/blob/<branch>/<path>/SKILL.md" \
  --stars <stargazerCount> \
  --skill-count <componentCount> \
  --source-started-at "<YYYY-MM-DD>" \
  --no-build
```

---

## Phase 4: Suite Manifestation via `gaia dev fuse`

**Critical Rule**: Running `gaia dev update-named --suite-components` alone is **insufficient**.
`gaia dev docs` and `gaia dev build` will strip `suiteComponents` from Named Skill frontmatter
unless a backing suite manifest exists at `registry/suites/<contributor>/<suite-slug>.json`.

Use `gaia dev fuse` to establish the manifest and wire the graph in one atomic operation:

```bash
gaia dev fuse <generic-suite-id> \
  --name "<Suite Name>" \
  --description "<Suite fusion description>" \
  --prereqs <comp1-generic-id>,<comp2-generic-id>,... \
  --named-capstone <contributor>/<suite-slug> \
  --suite-components <contributor>/<comp1>,<contributor>/<comp2>,... \
  --no-build
```

### Verification:
1. Confirm manifest exists: `test -f registry/suites/<contributor>/<suite-slug>.json`
2. Confirm frontmatter wiring:
   ```bash
   grep -c "suiteComponents:" registry/named/<contributor>/<suite-slug>.md
   ```

---

## Phase 5: Calibration of Capstone & Component Origins

### 5.1 Appraise Trust Magnitude

Run the appraisal tool on the capstone and all components:
```bash
python scripts/trust_appraise.py --skill <contributor>/<suite-slug>
```
Or use the detailed inspector:
```bash
GAIA_OPERATOR_OVERRIDE=1 PYTHONPATH=src python3 scripts/inspectTrustMagnitude.py --skill <contributor>/<suite-slug>
```

Verify:
- Capstone TM score and Overall Trust Grade.
- `fusionScore`: Structural composition reading (informational, does not feed TM).

### 5.2 Capstone Calibration (4★ Extra)

Evaluate the promotion gate:
- **Condition**: Capstone has Overall Trust Grade A (TM ≥ 100) and verified blob link.
- **Suite Branch Invariant**: Capstone does **NOT** require bucket-level Origin on its generic bucket!
  Origin on generic bucket is strictly for Unique branch standalone skills (`META.md` §4.1).
  Suite origin requirements apply at 5★ Ultimate (Origin on ≥1 suiteComponent per `META.md` §4.2).
- Apply calibration:
  ```bash
  gaia dev calibrate <contributor>/<suite-slug> 4★ --no-build
  ```

### 5.3 Component Calibration & Origin Assignment

1. **Origin Assignment**:
   For components that are the sole or most renowned implementation of their generic bucket:
   ```bash
   gaia dev update-named <contributor>/<component-slug> --origin true
   ```
2. **Component Star Calibration**:
   Calibrate each component to its TM grade band:
   - Grade B (TM ≥ 50) → `3★` (must have verified blob link)
   - Grade C (TM ≥ 20) → `2★`
   - Ungraded (TM < 20) → `1★`
   ```bash
   gaia dev calibrate <contributor>/<component-slug> <N★> --no-build
   ```

---

## Phase 6: Single-PR Closeout with Class S Documentation Generation

### 6.1 Single Dev Build

Run exactly one build pass to compile the registry and generate Class S site assets:
```bash
GAIA_OPERATOR_OVERRIDE=1 PYTHONPATH=src python3 -m gaia_cli.main dev build
```

### 6.2 Preflight Hygiene & Staging

Use `scripts/review_meta_close.py` to prevent leaks, drop CRLF noise, and stage only allowlisted artifacts:

```bash
# 1. Review status (must show 0 leaks in PR)
python scripts/review_meta_close.py status -v

# 2. Stage intended artifacts for this contributor
python scripts/review_meta_close.py stage --contributor <contributor> --apply

# 3. Verify clean index
python scripts/review_meta_close.py check

# 4. Run UTF-8 safe validation
python scripts/review_meta_close.py validate
```

### 6.3 Staged Artifacts Checklist

Verify that git diff includes only:
- `registry/nodes/` (new/updated generic nodes)
- `registry/named/<contributor>/` (capstone and component `.md` files)
- `registry/suites/<contributor>/<suite-slug>.json` (suite manifest)
- `registry/named-skills.json` & tracked registry files
- `docs/graph/` (Class S graph assets: `gaia.json`, `gaia.gexf`, `named/index.json`)
- `docs/badges/_assets/<contributor>/` & `docs/og/<contributor>/`

### 6.4 Branch & PR Opening

```bash
git checkout -b review/meta/<contributor>-<suite-slug>
git commit -m "feat(suite): ingest <contributor>/<suite-slug> suite with <N> components"
git push origin review/meta/<contributor>-<suite-slug>
gh pr create --title "feat(suite): ingest <contributor>/<suite-slug> suite" \
  --body "Ingests <contributor>/<suite-slug> suite under Yggdrasil III. Calibrates capstone to 4★ Extra on Grade A TM."
```

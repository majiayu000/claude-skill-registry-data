---
name: light-software-copyright
description: >-
  Prepare China software copyright registration material drafts from a real
  software project: application-field worksheet, source-code deposit material,
  user/operation manual, screenshots when needed, consistency checks and local
  formal-output evidence. Use for 软著, 软件著作权, 软件版权登记, source-code page
  extraction, operation manual drafts, version/name consistency, or pre-submit
  review. This off-DAG engineering/IP handoff skill does not provide legal
  advice, does not submit applications, does not guarantee registration, and
  never fabricates source code.
---

# Software copyright materials

Prepare auditable China software copyright material drafts from a real project.
The core job is not “write pretty documents”; it is to keep software name,
version, source-code material, manual, screenshots, applicant fields and user
confirmations consistent enough for the user or professional service provider
to review.

Read
[`references/software-copyright-resource-map.md`](references/software-copyright-resource-map.md)
before current-rule or material-format work.
Read
[`references/materials-workflow.md`](references/materials-workflow.md)
before source-code selection, business-understanding, rights-basis,
third-party-code or formal-output work.

## Non-negotiable boundaries

1. This skill is not legal advice and never submits applications or claims the
   material will pass. It prepares local drafts and review evidence only.
2. Code material must come from real project source files. Never invent,
   rewrite, pad, or AI-generate source code for deposit.
3. Do not expose secrets. Run or request a secret/privacy scan before exporting
   source-code material; if secrets are present, stop for redaction strategy.
4. Preserve official-rule uncertainty. If the current China Copyright
   Protection Center workflow, form, fee, page format or exception rule is not
   verified that day, write `UNKNOWN` or `PLANNED`.
5. Keep every formal material version and software name consistent with the
   application worksheet.
6. Keep this skill off the research DAG. It emits no `light.findings.v1`, has
   no stage, no checkpoint gate and no reroute.

## Workflow

### 1. Intake and scope

Capture or mark `UNKNOWN`:

- jurisdiction: default `CN`; do not silently reuse CN rules for US/EU work;
- software full name, abbreviation if any, version, owner/applicant, developer,
  completion date, publication status and development mode;
- whether the project is independent, commissioned, cooperative, inherited,
  derivative or based on licensed third-party code;
- target output language, local folder for drafts, and whether screenshots are
  needed.

Stop for user confirmation before formal documents are generated.

### 2. Bind to a real source snapshot and deposit plan

Inventory source files from the project the user placed in scope. Record
relative path, SHA-256 and why selected. Exclude:

- generated build artifacts, minified bundles, vendored dependencies and lock
  files unless the user explicitly says they are the software expression to
  deposit;
- secrets, tokens, keys, credentials, private data and unrelated third-party
  code;
- arbitrary middle snippets chosen only to make the material look longer.

If the project is too small, submit all real source rather than padding.

Run the lightweight planner before extraction:

```bash
python scripts/source_deposit_plan.py --root <project-root> --out 软件著作权申请资料/草稿/source-deposit-plan.json --software-name "<软件全称>" --version "<版本号>"
python scripts/source_deposit_plan.py --selftest
```

Use the plan to confirm candidate files, page mode, selected file count,
secret-scan status and the plan SHA. If secret-like content is found, stop for
redaction before exporting code material.

### 3. Confirm application fields and business understanding

Generate a worksheet for the user to verify:

- software name and version;
- owner/applicant and contributor facts;
- development environment and operating environment;
- main functions, technical characteristics and use scenario;
- source program quantity and document material quantity;
- publication status and dates.

The manual must describe how a reviewer/user operates the software. It should
not be a generic feature list disconnected from screens, commands or workflows.
Record rights basis and third-party/open-source/generated-code review before
formal export. Do not assume independent ownership when the project may be
commissioned, cooperative, inherited, derivative or license-constrained.

### 4. Prepare code and document material

For normal China material logic, follow the official first/last rule:

- source program and one documentation material use front/back continuous 30
  pages when the whole material is at least 60 pages;
- if the whole material is fewer than 60 pages, include the whole source or
  whole document;
- full source pages normally need at least 50 lines, and full document pages at
  least 30 lines, unless a documented official exception applies.

Keep extraction manifests and page counts. If exceptional deposit is requested,
mark it explicitly and ask the user to verify the current official rule.

### 5. Generate local drafts, then formal outputs

Use a local folder such as `软件著作权申请资料/`:

- `草稿/`: application worksheet, manual draft, code-selection notes;
- `正式资料/`: final DOCX/TXT/PDF-like outputs only after confirmation;
- manifest/report JSON: file paths, SHA-256, source snapshot, confirmation
  basis and rule status.

Screenshots are optional; if not used, record why. If used, bind each screenshot
to a real running UI or user-provided image and hash it.

### 6. Run the machine gate before saying “ready for review”

Create a packet following
[`templates/software-copyright-materials.example.json`](templates/software-copyright-materials.example.json),
then run:

```bash
python scripts/source_deposit_plan.py --selftest
python scripts/materials_gate.py --packet software-copyright-materials.json --base <project-root> --as-of 2026-07-05
python scripts/materials_gate.py --selftest
```

The gate must pass before calling the package ready for user/professional
review. A failed gate means repair the source plan, source binding, rights
basis, third-party review, confirmation, page rule, version consistency, secret
handling or output hashes.

## ACT / ASK / NEVER

ACT:

- use real source files and record SHA-256;
- ask the user to confirm application fields, business context, code selection,
  drafts and final export;
- keep source-code and documentation page counts explicit;
- make software name and version identical across all materials;
- scan for secrets/private data before exporting source-code material.
- record rights basis and third-party/open-source/generated-code exclusions.

ASK:

- owner/applicant and development-mode facts;
- whether third-party/commissioned/inherited/derivative code is present;
- whether screenshots should be included;
- whether exceptional deposit or redaction is needed;
- whether the software is independently developed, commissioned, cooperative,
  inherited, derivative, or includes third-party/generated code;
- whether to stop at drafts or generate formal local files.

NEVER:

- submit materials or interact with the registration system for the user;
- promise approval, certificate timing, or “包过”;
- fabricate source code, pad line counts, or select arbitrary snippets;
- leak credentials, private data or unrelated third-party code;
- silently include vendored, generated or license-constrained code without a
  third-party review note;
- route this skill into the Light research DAG.

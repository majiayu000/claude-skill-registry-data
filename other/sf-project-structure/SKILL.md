---
name: sf-project-structure
description: Structuring a Salesforce DX repository — the full `sfdx-project.json` schema (packageDirectories, default, sourceApiVersion, namespace, sfdcLoginUrl, plugins, packageAliases, replacements, sourceBehaviorOptions, oauthLocalPort, pushPackageDirectoriesSequentially), source-format directory layout for every metadata type (`objects/<Obj>/fields`, `classes`, `triggers`, `lwc`, `aura`, `flows`, `permissionsets`, `layouts`, `flexipages`, `staticresources`, `labels`, `settings`), decomposed metadata types, multiple package directories and modularisation, `.forceignore` semantics and precedence, `package.xml` and `destructiveChangesPre/Post.xml` manifests with `sf project generate manifest`, the source-tracking model (`sf project deploy|retrieve start|preview`, `delete source`, `reset tracking`, `--ignore-conflicts`), source/metadata format conversion, team repo conventions, and the `.vibeforce/` layout. Use this skill when creating or reorganising a DX project, deciding where a metadata file belongs, writing or auditing `.forceignore` or a manifest, resolving source-tracking conflicts, splitting a monolith into package directories, or reviewing metadata XML diffs.
---

# Salesforce DX Project Structure

A directory is a Salesforce DX project because it contains `sfdx-project.json`. That file tells the
CLI which directories hold source (`packageDirectories`), what metadata shape to speak
(`sourceApiVersion`), and where to log in (`sfdcLoginUrl`).

## When to use

| Situation | Action |
| --- | --- |
| Creating a repo or adding a package directory | `sfdx-project.json` schema + multiple-package-directory rules below |
| "Where does this metadata file go?" | [`references/metadata-directory-map.md`](references/metadata-directory-map.md) |
| Source keeps getting deployed that should not be | `.forceignore` precedence, pattern 4, and `sf project list ignored` |
| Building a deployment or deletion manifest | `sf project generate manifest`, [`references/forceignore-and-manifests.md`](references/forceignore-and-manifests.md) |
| `sf project deploy start` reports conflicts | Pattern 5 — resolve, then deploy or retrieve with `--ignore-conflicts` |
| Importing an existing metadata-format repo | `sf project convert mdapi` (pattern 6) |
| Setting team conventions, review rules, branch model | [`references/repo-conventions.md`](references/repo-conventions.md) |

Related skills: `sf-cli-operations` (flags, config, API version resolution),
`sf-deployment-strategies` (deploy/validate/quick-deploy mechanics and test levels),
`sf-scratch-orgs-sandboxes` (org lifecycle, source tracking availability),
`sf-packaging-release` (package directories becoming 2GP/unlocked packages),
`sf-security-model` (profile vs permission-set policy).

## Canonical layout

```text
my-project/
├── sfdx-project.json            project definition (commit)
├── .forceignore                 what the project commands exclude (commit)
├── .gitignore                   what git excludes (commit)
├── package.json                 LWC Jest, eslint, prettier dev deps (commit)
├── jest.config.js               sfdx-lwc-jest config (commit)
├── config/
│   ├── project-scratch-def.json scratch org definition (commit)
│   └── dev-sandbox-def.json     sandbox definition (commit)
├── manifest/
│   ├── package.xml              deployment manifest (commit)
│   └── destructiveChangesPost.xml (commit when a release deletes metadata)
├── force-app/                   default package directory
│   └── main/default/
│       ├── classes/             ApexClass: Foo.cls + Foo.cls-meta.xml
│       ├── triggers/            ApexTrigger: Foo.trigger + Foo.trigger-meta.xml
│       ├── lwc/<bundle>/        LightningComponentBundle (strict directory name)
│       ├── aura/<bundle>/       AuraDefinitionBundle (strict directory name)
│       ├── objects/<Object>/    decomposed: fields/, recordTypes/, listViews/, ...
│       ├── flows/               Flow: Foo.flow-meta.xml
│       ├── permissionsets/      PermissionSet: Foo.permissionset-meta.xml
│       ├── layouts/             Layout: Object-Layout Name.layout-meta.xml
│       ├── flexipages/          FlexiPage: Foo.flexipage-meta.xml
│       ├── labels/              CustomLabels: CustomLabels.labels-meta.xml
│       ├── staticresources/     StaticResource: Foo.resource-meta.xml + payload
│       └── settings/            Settings: Case.settings-meta.xml
├── .vibeforce/                  vibe-force config + state + reports
├── .sf/  .sfdx/  .localdevserver/   CLI-generated; never edit, never commit
└── node_modules/                never commit
```

## `sfdx-project.json` quick reference

| Property | Required | Purpose |
| --- | --- | --- |
| `packageDirectories` | yes | Array of `{ "path": "...", "default": true }`. Relative paths only. Exactly one `default`; with a single entry it is implied |
| `sourceApiVersion` | recommended | API version the *metadata* conforms to — becomes `<version>` in the generated manifest. vibe-force sets `67.0` |
| `namespace` | optional | Namespace applied to scratch orgs created from this project; must be linked to the Dev Hub |
| `sfdcLoginUrl` | optional | Login URL for `sf org login *`; default `https://login.salesforce.com`. Use the My Domain form for sandboxes |
| `oauthLocalPort` | optional | OAuth callback port; default 1717. Must match the connected app callback URL |
| `packageAliases` | optional | CLI-maintained map of readable names to `0Ho`/`04t` package ids |
| `plugins` | optional | Per-plugin settings you want version-controlled |
| `replacements` | optional | Deploy-time string/regex substitution driven by env vars or files |
| `sourceBehaviorOptions` | optional (Beta) | Extra decomposed types. Never hand-edit — run `sf project convert source-behavior` |
| `pushPackageDirectoriesSequentially` | deprecated | Only affected the retired `force:source:push`; has no effect on `sf project deploy start` |

Full property tables, packaging fields, and `replacements` variants:
[`references/sfdx-project-schema.md`](references/sfdx-project-schema.md).

## Core patterns

### 1. Start the project, pin the API version

```bash
sf template generate project --name my-project --default-package-dir force-app \
  --manifest --api-version 67.0
cd my-project
```

```json
{
  "packageDirectories": [{ "path": "force-app", "default": true }],
  "namespace": "",
  "sfdcLoginUrl": "https://login.salesforce.com",
  "sourceApiVersion": "67.0"
}
```

Keep `sourceApiVersion` equal to the vibe-force `apiVersion` (`config/vibe-force.defaults.json`) and
to `org-api-version`; `sf doctor` runs a `sourceApiVersion matches apiVersion` check and warns when
they diverge. `sourceApiVersion` governs the *shape of the metadata*: deploying a file that contains
a field introduced in a later API version fails if `sourceApiVersion` is older, and retrieving with
an older value silently drops newer subelements.

### 2. Model the domain with multiple package directories

```json
{
  "packageDirectories": [
    { "path": "force-app", "default": true },
    { "path": "sales-ext" },
    { "path": "service-ext" },
    { "path": "unpackaged" }
  ],
  "sourceApiVersion": "67.0"
}
```

Each directory repeats the standard `main/default/...` tree, so `MyObject__c` can live in
`force-app` while a new field on it lives in `sales-ext/main/default/objects/MyObject__c/fields/`.
Facts that matter:

- The split is client-side only. Deploying does not associate a directory with a package in the org.
- `sf project deploy start` with no targeting flag deploys all package directories in one
  transaction. Order is not guaranteed, so sequence explicitly when you need it:

```bash
sf project deploy start --source-dir force-app --target-org vf-dev
sf project deploy start --source-dir sales-ext --source-dir service-ext --target-org vf-dev
```

- The default directory is the retrieve target and the default output directory for conversions.
- These directories are the natural boundary for later unlocked/2GP packages (skill
  `sf-packaging-release`), and the natural ownership boundary for the vibe-force wave-1 agents.

### 3. Know the source format rules that surprise people

| Rule | Detail |
| --- | --- |
| Custom objects and custom object translations are always decomposed | `objects/<Object>/<Object>.object-meta.xml` plus `fields/`, `recordTypes/`, `listViews/`, `validationRules/`, `compactLayouts/`, `fieldSets/`, `businessProcesses/`, `indexes/`, `sharingReasons/`, `webLinks/` |
| Optional decomposition is opt-in and beta | `CustomLabels`, `PermissionSet`, `SharingRules`, `Workflow`, `ExternalServiceRegistration` via `sf project convert source-behavior --behavior <value>` |
| Bundles need exact directory names | `lwc`, `aura`, `staticresources`, `experiences`, `documents`, `objects`, `objectTranslations`, `sites`, `emailservices`, `waveTemplates`, `lightningTypes`, `genAiFunctions`, `restrictionRules`, `bots`, `aiAuthoringBundles` are `strictDirectoryName` types — a bundle in the wrong folder is invisible to the CLI |
| Static resources live only in `<pkg>/main/default/staticresources` | `.zip`/`.jar` archives are auto-expanded on retrieve; an archive that exists as a single file stays a single file. New resources use their MIME extension (`.gif`, `.png`); legacy `.resource` files keep that extension |
| Content types have two files | `ApexClass`, `ApexTrigger`, `ApexPage`, `ApexComponent`, `EmailTemplate`, `StaticResource` ship a payload plus `-meta.xml`. Treat them as a pair in `.forceignore` and in reviews |
| Names with special characters are URL-encoded on disk | `Custom: Marketing Profile` becomes `Custom%3A Marketing Profile.profile-meta.xml`, and `.forceignore` must use the encoded name |
| Folder-based types nest one level | `reports/<Folder>/<Report>.report-meta.xml`, same for `dashboards`, `documents`, `email` |

### 4. Write `.forceignore` deliberately

`.forceignore` uses `.gitignore` syntax and is honoured by `project deploy start`,
`project retrieve start`, `project convert source`, and `project delete source`.

```gitignore
# Never deploy tooling and local artifacts
**/jsconfig.json
**/.eslintrc.json
**/__tests__/**
.sf/
.sfdx/
.localdevserver/

# Org-owned, human-managed metadata
**/profiles/**
**/*.settings-meta.xml
**/labels/CustomLabels.labels-meta.xml

# A specific component (MetadataWithContent needs both files, or a trailing *)
force-app/main/default/classes/LegacyBatch.cls*

# A whole bundle
**/lwc/legacyComponent
```

Precedence: when the commands decide whether to exclude a file they walk **up** from that file until
they find the first `.forceignore`, consult it, and stop. A `.forceignore` inside `sales-ext/`
therefore fully overrides the project-root one for files under `sales-ext/`. Put the primary file at
the project root; a per-package file is legitimate but must be documented.

Independently of `.forceignore`, the project commands always skip dot-files and dot-directories,
files ending in `.dup`, `package2-descriptor.json`, and `package2-manifest.json`.

Verify, never guess:

```bash
sf project list ignored
sf project list ignored --source-dir force-app/main/default/classes
sf project deploy preview --target-org vf-dev     # shows Will Deploy / Will Delete / Conflicts / Ignored
```

`vf-check static` fails when a changed file is silently ignored by `.forceignore` but expected to be
part of the story, which is the common cause of "it works in my scratch org but not in UAT".

### 5. Operate source tracking honestly

| Org type | Source tracking |
| --- | --- |
| Scratch org | Always available, on by default |
| Developer / Developer Pro sandbox | Available when the production org has source tracking enabled |
| Developer Edition, production, Partial Copy, Full sandbox | Not supported |

```bash
sf project deploy preview  --target-org vf-dev     # local changes, deletions, conflicts, ignored
sf project retrieve preview --target-org vf-dev    # remote changes

sf project deploy start  --target-org vf-dev       # deploy exactly the changed, tracked source
sf project retrieve start --target-org vf-dev      # retrieve exactly the remote changes

sf org enable tracking  --target-org vf-sandbox
sf org disable tracking --target-org vf-sandbox
sf project reset tracking --target-org vf-dev --revision 12345
sf project delete tracking --target-org vf-dev     # forget all local tracking state
```

Conflict resolution: `preview` reports `Conflicts [n]`. Resolve the file, then overwrite one side
deliberately and narrowly:

```bash
# Keep the local version of one class, then continue normally.
sf project deploy start --metadata ApexClass:WidgetClass --ignore-conflicts --target-org vf-dev
# Or keep the org version of that class.
sf project retrieve start --metadata ApexClass:WidgetClass --ignore-conflicts --target-org vf-dev
sf project deploy start --target-org vf-dev
```

`--ignore-conflicts` silently discards the other side's work. Scope it to the component you decided
about; never add it to a whole-project command "to make the error go away". vibe-force hooks warn on
`--ignore-conflicts` in `standard` mode and block it against a production alias in `strict` mode.

Deleting metadata needs `sf project delete source`, which removes it from the org **and** the local
project; plain file deletion plus `deploy start` does not delete anything in the org unless the
component is tracked as deleted.

```bash
sf project delete source --metadata ApexClass:ObsoleteService --target-org vf-dev --check-only
sf project delete source --metadata ApexClass:ObsoleteService --target-org vf-dev --no-prompt
```

Performance: tracking adds `SourceMember` queries and polling. A "medium" project is 30+ components
or 50+ tests, "large" is 600+ components or 150+ tests; above that, deploy in smaller sets or tune
`SF_SOURCE_TRACKING_BATCH_SIZE` (see skill `sf-cli-operations`).

### 6. Convert between formats when you inherit a repo

```bash
# Metadata format (retrieve output, change-set export) -> source format
sf project convert mdapi --root-dir ./mdapi-out --output-dir force-app

# Source format -> metadata format, for a tool that only speaks Metadata API
sf project convert source --source-dir force-app --output-dir mdapi-package --package-name MyApp
```

For `project convert mdapi`, the applicable `.forceignore` is the one in the metadata retrieve
directory (next to `package.xml`), not the project root.

### 7. Keep `.vibeforce/` and generated directories straight

| Path | Commit? | Content |
| --- | --- | --- |
| `.vibeforce/config.json` | yes | Project gates, org aliases, hook mode — reviewed like code |
| `.vibeforce/state/ownership.json` | no | Wave-1 path ownership for the current story |
| `.vibeforce/state/deploy-jobs.json` | no | Validation job ids for quick deploy |
| `.vibeforce/state/contract.md` | optional | Cross-slice contract written in wave 0; commit it when it documents a decision worth keeping |
| `.vibeforce/reports/*.json` | no | Check-runner output |
| `.sf/`, `.sfdx/` | no | CLI internals, auth, local config — never edit by hand |
| `.localdevserver/` | no | Local dev server cache (skill `sf-local-development`) |
| `node_modules/`, `coverage/`, `*.log` | no | Build artifacts |

`vf-init` seeds a consumer project from this plugin's `templates/` directory (project config seed,
formatter and lint configuration, `.forceignore`/`.gitignore` fragments) and creates
`.vibeforce/`; the exact inventory is whatever `templates/` in the installed plugin contains.

## Anti-patterns

| Anti-pattern | Consequence | Fix |
| --- | --- | --- |
| Two `"default": true` package directories | The CLI cannot resolve the retrieve/convert target | Exactly one default |
| Absolute paths in `packageDirectories` | Breaks on every other machine and in CI | Relative paths (`"force-app"`, `"./force-app"`) |
| Hand-editing `sourceBehaviorOptions` | Project claims decomposition that the files do not have; deploys fail | `sf project convert source-behavior --behavior <value>` (`--dry-run` first) |
| Deleting a metadata file and deploying | Component stays in the org | `sf project delete source`, or a `destructiveChanges*.xml` manifest |
| `--ignore-conflicts` on a whole-project deploy | Silently overwrites teammates' org changes | Resolve per component, then deploy |
| Committing `.sf/` or `.sfdx/` | Leaks auth material and machine-local config | Gitignore both; rotate anything already pushed |
| Profiles deployed from source alongside permission sets | Profile XML is org-wide and merge-hostile; diffs are unreviewable | Permission sets + permission set groups; ignore `**/profiles/**` (skill `sf-security-model`) |
| One giant `force-app` for a multi-team org | Every story touches the same tree; ownership and packaging are impossible | Package directory per domain (pattern 2) |
| `sourceApiVersion` left at whatever the project template shipped | Newer subelements are dropped on retrieve and rejected on deploy | Pin to the vibe-force `apiVersion` |
| `.forceignore` entry naming only `Foo.cls` | `Foo.cls-meta.xml` still deploys | `Foo.cls*` or list both files |

## Verification

```bash
# Project definition parses and resolves the way you think
node -e "const p=require('./sfdx-project.json');console.log(p.sourceApiVersion, p.packageDirectories)"
sf project list ignored
sf project deploy preview --target-org vf-dev
sf project retrieve preview --target-org vf-dev

# Manifest round-trip
sf project generate manifest --source-dir force-app --name manifest/package.xml
sf project deploy start --manifest manifest/package.xml --dry-run --target-org vf-dev

# vibe-force gates
node "$VF_ROOT/scripts/checks/vf-check.mjs" static          # format + lint + analyzer on changed files
node "$VF_ROOT/scripts/checks/vf-check.mjs" local           # static + jest
node "$VF_ROOT/scripts/checks/vf-check.mjs" deploy-validate --target-org vf-int
```

`vf-check format` and `vf-check lint` resolve files through `packageDirectories`, so a directory
missing from `sfdx-project.json` is also invisible to the gates — a strong reason to keep the file
accurate.

## References

- [`references/sfdx-project-schema.md`](references/sfdx-project-schema.md) — every property, packaging fields, `replacements` variants, worked examples.
- [`references/metadata-directory-map.md`](references/metadata-directory-map.md) — metadata type → directory → file suffix → notes, including decomposed children and strict-directory bundles.
- [`references/forceignore-and-manifests.md`](references/forceignore-and-manifests.md) — `.forceignore` patterns and precedence, `package.xml`, `destructiveChangesPre/Post.xml`, wildcard support.
- [`references/xml-token-economy.md`](references/xml-token-economy.md) — measuring, reading and patching metadata XML without loading whole files; the `xml-bulk-read` guard and `/vf-xml`.
- [`references/repo-conventions.md`](references/repo-conventions.md) — branch-per-story, ownership, metadata review checklist, profile policy, monorepo tradeoffs, gitignore companion.
- Salesforce DX Project Structure and Source Format: <https://developer.salesforce.com/docs/atlas.en-us.sfdx_dev.meta/sfdx_dev/sfdx_dev_source_file_format.htm>
- Salesforce DX Project Configuration: <https://developer.salesforce.com/docs/atlas.en-us.sfdx_dev.meta/sfdx_dev/sfdx_dev_ws_config.htm>
- Multiple Package Directories: <https://developer.salesforce.com/docs/atlas.en-us.sfdx_dev.meta/sfdx_dev/sfdx_dev_ws_mpd.htm>
- How to Exclude Source When Syncing: <https://developer.salesforce.com/docs/atlas.en-us.sfdx_dev.meta/sfdx_dev/sfdx_dev_exclude_source.htm>
- Track Changes Between Your Project and Org: <https://developer.salesforce.com/docs/atlas.en-us.sfdx_dev.meta/sfdx_dev/sfdx_dev_source_tracking.htm>
- Metadata API Developer Guide, Deploying and Retrieving Metadata: <https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_deploy.htm>

---
name: sf-local-development
description: Covers the Salesforce development loop that runs before any deployment - Live Preview (formerly Local Dev) via sf lightning dev app, sf lightning dev component and sf lightning dev site, what hot-reloads versus what needs a redeploy and server restart, which checks genuinely run offline (prettier, ESLint, Code Analyzer, sfdx-lwc-jest) versus which need an org (Apex compilation and tests, Flow, permissions, SOQL), source-tracking hygiene with sf project deploy preview, --dry-run and sf project retrieve start, watch loops, anonymous Apex probes, VS Code and devcontainer setup, and the exact composition of the vf-check local gate. Use this skill when starting work on a component before deploying, when deciding whether a change can be verified without an org, when the preview server does not pick up a change, when source tracking reports conflicts, or when a contributor asks how to iterate quickly on LWC or Apex.
---

# Salesforce Local Development Loop

## When to use

| Situation | Use this skill |
| --- | --- |
| Iterating on an LWC before deploying | Yes |
| Deciding whether a change can be proven without an org | Yes |
| `sf lightning dev ...` fails, or a change does not appear in the preview | Yes |
| Previewing empty, error or long-text states the org has no records for | Yes - pattern 9 |
| Source tracking reports conflicts between project and org | Yes |
| Writing the component | Skill `sf-lwc-development` |
| Writing or fixing Jest tests | Skill `sf-lwc-jest-testing` |
| Creating or refreshing the org itself | Skill `sf-scratch-orgs-sandboxes` |
| Analyzer/lint findings | Skill `sf-code-analyzer-quality` |
| Reading debug logs after a failure | Skill `sf-debugging-logs` |

Naming: Salesforce rebranded **Local Dev** to **Live Preview** in Spring '26. The CLI command names
(`sf lightning dev app|component|site`) did not change.

## Decision table: what runs where

| Activity | Offline (no org) | Needs an org |
| --- | --- | --- |
| `prettier --check` / `--write` | Yes | - |
| `eslint` on LWC/Aura JS | Yes | - |
| `sf code-analyzer run` (PMD, ESLint, Regex, RetireJS) | Yes | - |
| `sfdx-lwc-jest` unit tests and coverage | Yes | - |
| LWC template/JS compile errors | Yes (Jest and ESLint surface most) | Full validation at deploy |
| Rendering a component with real record data | - | Yes (Live Preview proxies org data) |
| Apex compilation | - | Yes (`--dry-run` deploy) |
| Apex unit tests | - | Yes |
| SOQL results, sharing, FLS | - | Yes |
| Flow, validation rules, permission sets | - | Yes |
| Platform events, callouts, named credentials | - | Yes |

There is no local Apex runtime. The fastest Apex feedback is a check-only deploy
(`sf project deploy start --dry-run`) or an anonymous block (`sf apex run`).

## Core patterns

### 1. Prerequisites

```bash
sf --version                  # Salesforce CLI v2; Live Preview plugin ships with it
node --version                # use the Node LTS that the installed sf release supports
sf update                     # refresh the CLI and its bundled plugins before a preview session
sf org list --all
```

The Salesforce CLI installs the Live Preview plugin automatically; a manual
`sf plugins install @salesforce/plugin-lightning-dev` is only needed when the plugin was explicitly
removed. The first `sf lightning dev` run prompts to enable the feature in the target org - press
Enter or type `y`. Enabling requires the **View Setup** and **Customize Application** permissions.
The project must contain an `lwc` directory (typically `force-app/main/default/lwc`).

### 2. First run against a scratch org

```bash
sf org create scratch --definition-file config/project-scratch-def.json \
  --alias vf-dev --duration-days 7 --set-default
sf project deploy start --target-org vf-dev
sf org assign permset --name Vf_App_Access --target-org vf-dev
sf data import tree --plan ./data/data-plan.json --target-org vf-dev

sf lightning dev app --name "Service Console" --device-type desktop --target-org vf-dev
```

Run Live Preview against scratch orgs and sandboxes. It is technically available in production, but
Salesforce recommends against it and the vibe-force hooks treat any production alias as protected.

### 3. The three preview modes

```bash
# whole Lightning Experience app, desktop
sf lightning dev app --name "Sales" --device-type desktop --target-org vf-dev

# same app in an iOS simulator or Android emulator
sf lightning dev app --name "Sales" --device-type ios --device-id "iPhone 15 Pro Max" --target-org vf-dev

# one component in isolation, with access to LDS wires, @salesforce modules and Apex
sf lightning dev component --name accountCard --target-org vf-dev

# Experience Cloud LWR site (must already be published)
sf lightning dev site --name "Partner Central" --get-latest --target-org vf-dev
```

Omit `--name` to get an interactive picker. Flag tables for all three commands:
`references/local-dev-server.md`.

### 4. What hot-reloads and what does not

| Change | Reflected automatically |
| --- | --- |
| HTML attribute or markup edit | Yes |
| Component CSS edit | Yes |
| Adding a `<lightning-*>` or existing custom component to markup | Yes |
| Importing a new CSS-only component | Yes |
| JavaScript change that does not alter the public API | Yes |
| Adding or deleting a file inside an existing bundle | Yes (Spring '25 and later) |
| New `@api` property or method | No - browser refresh for a component preview, deploy + server restart for app/site |
| Wire adapter changes (new adapter, config change, GraphQL query change) | No |
| New `@salesforce` scoped import | No |
| `.js-meta.xml` change | No - only `.js`, `.html`, `.css` hot-reload, and a meta edit needs a deploy in every mode |
| Service component library change | No |
| Apex, objects, flows, permissions | No - always a deploy |

Recovery for a non-reloading change:

```bash
# component preview: refresh the browser, no deploy
# app or site preview, or any .js-meta.xml edit:
sf project deploy start --source-dir force-app/main/default/lwc/accountCard --target-org vf-dev
# then restart the sf lightning dev process
```

Other limits: Live Preview previews Lightning web components only (no Aura), and Landing Pages
cannot be previewed. Changes saved directly in the org are deployed to the live app automatically,
but your local copy is not updated until you run `sf project retrieve start`.

### 5. The offline gate

```bash
node "${CLAUDE_PLUGIN_ROOT}/scripts/checks/vf-check.mjs" local --changed
```

`local` = `static` + `jest`, that is:

| Step | Command behind it | Fails when |
| --- | --- | --- |
| `format` | `prettier --check` on changed Apex/LWC/XML/JS | Any file is unformatted (`--fix` rewrites) |
| `lint` | `eslint` on LWC/Aura JS | Any error-severity rule fires |
| `analyzer` | `sf code-analyzer run` with `config/code-analyzer.yml` | A violation at or above `gates.analyzerFailSeverity` (3) |
| `jest` | `sfdx-lwc-jest` | A test fails, coverage < `gates.jestCoverageMin` (80), or an LWC bundle has no `__tests__` (`*Harness` and `*Fixtures` bundles are exempt - pattern 9) |

No org, no network. Exit 0 pass, 1 gate failure, 2 missing tooling, 3 org/network (not reachable
for this gate). Run it before every handoff to wave 3.

### 6. Watch loops

```bash
npm run test:unit:watch                      # sfdx-lwc-jest --watch
npx prettier --write "force-app/**/*.{cls,trigger,js,html,css,xml}"
npx eslint force-app/main/default/lwc --fix
```

Recommended terminal layout while building a component: one pane running
`sf lightning dev component --name <bundle> --target-org vf-dev`, one running
`npm run test:unit:watch`, one for CLI commands. Do not put `sf project deploy start` in a file
watcher: metadata deploys are rate-limited and source tracking conflicts multiply.

### 7. Source tracking hygiene

```bash
# what would deploy, what conflicts, what is forceignored
sf project deploy preview --target-org vf-dev

# compile and run tests server-side without saving anything
sf project deploy start --source-dir force-app --dry-run \
  --test-level RunSpecifiedTests --tests AccountServiceTest --target-org vf-dev

# pull org-side changes (Setup edits, App Builder layout changes)
sf project retrieve preview --target-org vf-dev
sf project retrieve start --target-org vf-dev
```

Conflict rules: `--ignore-conflicts` (`-c`) exists on `deploy start`, `deploy preview`,
`retrieve start`, and `retrieve preview`, and it silently overwrites the other side. Resolve
conflicts by inspecting the preview output and choosing per component; reserve `-c` for scratch
orgs you are willing to lose. Source tracking is on by default for scratch orgs and sandboxes
unless they were created with `--no-track-source`, and never available in production.

### 8. Apex feedback without a deploy

```bash
# fastest syntax/semantics check: server-side compile, nothing saved
sf project deploy start --source-dir force-app/main/default/classes --dry-run --target-org vf-dev

# probe behaviour with an anonymous block
cat > /tmp/probe.apex <<'APEX'
List<Case> open = [SELECT Id, CaseNumber FROM Case WHERE IsClosed = false LIMIT 5];
System.debug(LoggingLevel.ERROR, 'open=' + open.size());
APEX
sf apex run --file /tmp/probe.apex --target-org vf-dev

# targeted tests once the class is deployed
sf apex run test --tests AccountServiceTest --synchronous --result-format human --target-org vf-dev
```

`sf apex run` with no flags reads an interactive block from stdin (CTRL-D to execute). Anonymous
Apex is a probe, not a test: it neither counts toward coverage nor proves the contract. See skills
`sf-apex-development` and `sf-apex-testing`.

### 9. Component data without org records

`sf lightning dev component` renders a bundle with whatever its own defaults produce - there is no
property editor and no state switcher. Seeding org records covers the happy path; the loading,
empty, error and long-text states still need data you control. Never add an `isDemo` branch to the
component to make a preview work.

The pattern: one fixture module, two consumers.

| Piece | Path | Package directory | Purpose |
| --- | --- | --- | --- |
| Component | `lwc/accountCard/` | default (`force-app`) | Ships |
| Fixtures | `lwc/accountCardFixtures/` | default (`force-app`) | Every state, one definition |
| Harness | `lwc/accountCardHarness/` | preview only (`preview-app`) | Mounts the component per state |
| Spec | `lwc/accountCard/__tests__/` | default (`force-app`) | Imports the same fixtures |

Fixtures sit beside the component so `sfdx-lwc-jest` resolves `c/accountCardFixtures` the same way
it resolves any sibling bundle. The harness sits in its own package directory so it never reaches
production.

```js
// force-app/main/default/lwc/accountCardFixtures/accountCardFixtures.js
export const EMPTY = { key: 'empty', label: 'Empty', records: [], error: null };
export const ERROR = { key: 'error', label: 'Error', records: [], error: { body: { message: 'No access.' }, status: 403 } };
export const STATES = [EMPTY, ERROR];
```

```js
// the spec asserts the same states the harness shows
import { ERROR } from 'c/accountCardFixtures';
element.error = ERROR.error;
```

```json
// sfdx-project.json - the harness directory is never default
{
  "packageDirectories": [
    { "path": "force-app", "default": true },
    { "path": "preview-app", "default": false }
  ]
}
```

```bash
# the harness is served from local source; the org is only there for platform modules
sf lightning dev component --name accountCardHarness --target-org vf-dev

# deploy it only when a .js-meta.xml edit has to register, and only to a dev org
sf project deploy start --source-dir preview-app --target-org vf-dev
```

Never include `preview-app` in a production deploy: deploy by `--source-dir` or by manifest, not
by `sf project deploy start` with no arguments, which takes every package directory. The harness
does not need to be in any org to be previewed - the component list is built from the local project
- so in practice the preview directory stays undeployed everywhere.

Naming is load-bearing. `vf-check pairing` exempts bundle names matching
`gates.previewBundlePattern` (default `(?:Harness|Fixtures)$`) from `gates.requireJestForLwc`, and
the reference Jest config drops the same bundles from `collectCoverageFrom` - a wrapper with no
behaviour of its own would otherwise fail the spec gate and dilute coverage. Every exemption is
named in the check log, so narrow the pattern when a shipped component's name collides. Skeletons
to copy: `${CLAUDE_PLUGIN_ROOT}/templates/lwc/exampleCardFixtures/` and
`${CLAUDE_PLUGIN_ROOT}/templates/lwc/exampleCardHarness/`.

The harness stays `isExposed=false` and declares no `targets`. The Project Components sidebar
"lists components in your project that are available for preview": the CLI builds that list by
globbing every directory under every `**/lwc` in the package directories and reads the
`.js-meta.xml` only for `masterLabel` and `description`, so an unexposed bundle is still
previewable. The one documented prerequisite is that the project has an `lwc` directory at all.

Seeding the org remains the right answer when the component reads records through Lightning Data
Service without any injectable input:

| Option | When | How |
| --- | --- | --- |
| Seed the org | Wire adapters against real records | `sf data import tree --plan ./data/data-plan.json --target-org vf-dev` |
| Seed one record | Quick probe | `sf data create record --sobject Account --values "Name='Acme'" --target-org vf-dev` |
| Fixture module | Public properties, rendering branches, error paths | `c/<component>Fixtures`, shared with the spec |
| A `@api` demo payload on the component | Never in shipped code | Delete before handing off |

### 10. Editor and container setup

| Tool | Notes |
| --- | --- |
| VS Code + Salesforce Extension Pack | Org browser, deploy/retrieve on save, Apex language server |
| Salesforce Live Preview VS Code extension | `SFDX: Open in Lightning Preview` from the Explorer context menu or the Command Palette; React component preview is beta |
| Apex Replay Debugger | Replays a debug log locally; see skill `sf-debugging-logs` |
| Devcontainer | Base image with Node LTS, `npm i -g @salesforce/cli`, project `npm ci`; mount `~/.sfdx` or re-auth with `sf org login device` |

```bash
sf org open --path lightning/n/Case_Console --target-org vf-dev
sf org open --source-file force-app/main/default/flexipages/Case_Record_Page.flexipage-meta.xml --target-org vf-dev
sf org open --url-only --target-org vf-dev
```

## Anti-patterns

| Anti-pattern | Consequence | Fix |
| --- | --- | --- |
| Deploying to check a template typo | Minutes per iteration | `sf lightning dev component` plus Jest |
| Expecting a `.js-meta.xml` edit to hot-reload | Silent no-op; wrong conclusions | Deploy and restart the preview server |
| Running Live Preview against production | Real users and data; harness blocks it | Scratch org or sandbox |
| `--ignore-conflicts` as a habit | Overwrites a colleague's org changes | `sf project deploy preview` and resolve per component |
| Skipping `vf-check local` because "Jest passed" | Lint and analyzer findings reach review | Run the composite gate |
| Treating anonymous Apex output as a test | No coverage, no assertion, no regression protection | Write an Apex test (skill `sf-apex-testing`) |
| `sf project deploy start` in a file watcher | Deploy storms and tracking conflicts | Deploy at explicit checkpoints |
| Committing `.vibeforce/reports/**` or preview artefacts | Noise in review | Keep them gitignored in the consumer project |
| Assuming Aura components appear in the preview | They never do | Test Aura in the org |
| Harness bundle in the default package directory | Preview scaffolding ships to production | Own package directory, deployed by `--source-dir` to dev orgs only |
| Fixture data written twice, once in the spec and once in the harness | The preview shows states no test covers | One `c/<component>Fixtures` module, imported by both |

## Verification

```bash
# prove the offline gate passes on the current branch
node "${CLAUDE_PLUGIN_ROOT}/scripts/checks/vf-check.mjs" local --changed --json

# prove the metadata compiles server-side without saving
sf project deploy start --source-dir force-app --dry-run --target-org vf-dev

# prove nothing unexpected would deploy
sf project deploy preview --target-org vf-dev

# visually confirm the component against org data
sf lightning dev component --name accountCard --target-org vf-dev

# confirm the preview harness is exempt from the spec gate rather than missing one
node "${CLAUDE_PLUGIN_ROOT}/scripts/checks/vf-check.mjs" pairing --files "preview-app/**" --json
```

Only after `vf-check local` is green does the work move to wave 3 (`deploy-validate` then
`deploy-quick`, skill `sf-deployment-strategies`) and wave 4 (`smoke`, skill
`sf-post-deploy-verification`).

## References

- [`references/local-dev-server.md`](references/local-dev-server.md) - command and flag tables, supported targets, reload matrix, limitations.
- [`references/local-loop-playbook.md`](references/local-loop-playbook.md) - first-run setup and the daily loop, command by command.
- [`references/local-vs-org.md`](references/local-vs-org.md) - capability matrix across offline, scratch org, sandbox, and production.
- [`references/troubleshooting-local.md`](references/troubleshooting-local.md) - symptom-to-cause table for the preview server and source tracking.
- Source for the Project Components list (official Salesforce CLI plugin): [`plugin-lightning-dev/src/shared/componentUtils.ts`](https://github.com/salesforcecli/plugin-lightning-dev/blob/main/src/shared/componentUtils.ts) - `getNamespacePaths` globs `**/lwc` per package directory, `getComponentMetadata` reads only `masterLabel` and `description`.
- Official: [Run a Live Component Preview](https://developer.salesforce.com/docs/platform/lwc/guide/get-started-test-components.html), [lightning dev app](https://developer.salesforce.com/docs/platform/salesforce-cli-reference/guide/cli_reference_lightning_dev_app.html), [lightning dev component](https://developer.salesforce.com/docs/platform/salesforce-cli-reference/guide/cli_reference_lightning_dev_component.html), [lightning dev site](https://developer.salesforce.com/docs/platform/salesforce-cli-reference/guide/cli_reference_lightning_dev_site.html), [project deploy start](https://developer.salesforce.com/docs/platform/salesforce-cli-reference/guide/cli_reference_project_deploy_start.html), [project deploy preview](https://developer.salesforce.com/docs/platform/salesforce-cli-reference/guide/cli_reference_project_deploy_preview.html), [project retrieve start](https://developer.salesforce.com/docs/platform/salesforce-cli-reference/guide/cli_reference_project_retrieve_start.html), [apex run](https://developer.salesforce.com/docs/platform/salesforce-cli-reference/guide/cli_reference_apex_run.html), [org open](https://developer.salesforce.com/docs/platform/salesforce-cli-reference/guide/cli_reference_org_open.html).

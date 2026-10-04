---
name: scaffold-doctor
description: >
  Scaffolds a complete scheduled "doctor" agent directly into the user's repo.
  The doctor audits app health on a recurring schedule, routes code-fixable
  findings to an automated repair pipeline that opens pull requests, and files
  deduped tracker tickets for everything else. A Slack (or equivalent) digest
  posts after every run, even if remediation fails. Use when a team wants to
  deploy an autonomous health-auditing agent alongside their application without
  copying a pre-built engine — the skill generates the engine in the user's
  chosen stack by following the bundled reference docs.
---

# scaffold-doctor

Generates a production-ready "doctor" agent inside the target repo by following
the pattern described in [`references/architecture.md`](references/architecture.md).
**Read that file first** — it defines the module table, data flow diagram,
three run modes, and the error-isolation invariant that all generated code must
preserve.

---

## Interactive Flow

Ask questions **one at a time**, in the order listed below. Use multiple choice
wherever possible. Stack questions come first because they determine which
modules get generated and which swap-table rows apply.

---

### Q1 — Stack

Ask each sub-question on its own turn.

**1a. Language / runtime**
```
1) TypeScript (default)
2) Python
3) Other — describe
```

**1b. LLM provider**
```
1) Amazon Bedrock (default)
2) Anthropic API direct
```

**1c. Scheduler**
```
1) AWS EventBridge + Lambda (default)
2) GitHub Actions
3) POSIX cron / systemd timer
4) Kubernetes CronJob
```

**1d. VCS**
```
1) GitHub (default)
2) GitLab
```

**1e. Tracker**
```
1) Linear (default)
2) Jira
3) GitHub Issues
```

**1f. Chat**
```
1) Slack (default)
2) Microsoft Teams
3) Discord
```

For any non-default choice, note which swap-table row applies (see
[`references/swap-table.md`](references/swap-table.md)) — generation will
follow that row exactly.

---

### Q2 — Product name

> What is your application's name? (Used as the doctor's identity in the system
> prompt, e.g. "Acme Doctor".)

Free text. Store as `PRODUCT_NAME`.

---

### Q3 — Target repo

> What is the owner/name of the GitHub (or GitLab) repo the doctor will read
> from and open PRs against? (e.g. `acme-corp/backend`)

Free text. Store as `REPO_SLUG`.

---

### Q4 — Log source

> Which log groups should the doctor scan? List ARNs or names, one per line.
> Press enter twice when done. (Default: CloudWatch Logs; describe a different
> source if applicable.)

Collect as `LOG_GROUPS[]`. Default lookback: 60 minutes.

---

### Q5 — Data source for audits

> Which query tool should runbooks use?
```
1) AWS Athena (default)
2) Generic SQL (Postgres, MySQL, BigQuery…) — specify driver
3) Prometheus
4) None — runbooks use only log/metric/VCS tools
```

Store as `DATA_SOURCE`. For non-default choices, generation follows the
matching swap-table row in [`references/swap-table.md`](references/swap-table.md).

---

### Q6 — Model and region

> Primary model ID and AWS region (Bedrock) or plain model string (Anthropic
> API)?
>
> Defaults: `us.anthropic.claude-sonnet-4-6`, `us-east-1`. Press enter to
> accept.

Store as `MODEL_ID` and `AWS_REGION`. Fallback model defaults to
`us.anthropic.claude-haiku-3-5` (Bedrock) or `claude-haiku-3-5` (Anthropic API).

---

### Q7 — Budgets

Present defaults; user may override any or all.

| Parameter | Default |
|---|---|
| `maxPrsPerRun` | 3 |
| `maxTicketsPerRun` | 5 |
| `maxIterations` (per runbook) | 15 |
| `maxTokensPerCall` | 4096 |
| `patchCandidates` | 3 |
| `maxRepairAttempts` (per CI PR) | 3 |

---

### Q8 — Runbook schedule assignment

> The example runbook `scan-logs` will be registered as a **daily** runbook.
> Do you have additional runbooks to schedule now? (You can add more later with
> `add-doctor-runbook`.)
```
1) No, start with scan-logs only (default)
2) Yes — list names and daily/weekly for each
```

Collect `DAILY_RUNBOOKS[]` (starts with `["scan-logs"]`) and
`WEEKLY_RUNBOOKS[]` (starts empty).

---

## Generation Directive

Once all answers are collected, generate the doctor engine by following the
reference docs below. **Do not restate their content** — implement exactly
what they specify.

### Module list and file tree

Follow [`references/architecture.md`](references/architecture.md) — Module
Responsibilities table and Default-Stack File Tree. Generate every listed
module. For non-default stack choices, apply the relevant rows from
[`references/swap-table.md`](references/swap-table.md) before generating.

### `run-skill` and `prompts/system`

Follow [`references/agentic-loop.md`](references/agentic-loop.md) completely.

**Port these two reference snippets verbatim** (translated to the target
language/stack):

- **Model fallback** (§5): the `createMessage` wrapper that retries once on
  the fallback model before propagating.
- **Anti-loop guard** (§4): the `lastCalls` tail-check that injects a nudge
  text block when the same tool fires three times in a row.

The system prompt must follow the four-section structure in §8 exactly:

1. Identity block — `You are {PRODUCT_NAME} Doctor, an automated auditor for
   the {PRODUCT_NAME} platform.`
2. Core behavioral contract (static prose as specified).
3. Known gotchas (empty placeholder — keep the heading).
4. Runtime context block + runbook content appended at run time.

The runbook section must always be separated by `---` and the heading
`## Skill to execute` — **do not rename this heading**; the control tools
depend on it.

### `repair-pipeline` and `repair-ci`

Follow [`references/repair-pipeline.md`](references/repair-pipeline.md) for
the full five-phase flow and CI auto-repair loop.

**Port these reference snippets verbatim** (translated to the target language):

- `applySearchReplaceBlocks` and `parseSearchReplaceBlocks` — exact regex and
  match-count semantics.
- `selectWinner` (single-file, `repair-pipeline`) — filter → group → sort →
  count≥2 threshold.
- `selectWinningOutcome` (multi-file, `repair-ci`) — majority threshold
  `floor(N/2)+1`.
- Syntax-validation seam: TypeScript → `ts.transpileModule`; Python →
  `ast.parse`; other stacks — see the validation table in the reference.

### `types` and control tools

Follow [`references/finding-contract.md`](references/finding-contract.md) for:

- The full `Finding` schema (all required and optional fields).
- `emit_finding` tool definition — name and input schema must match exactly.
- `skill_done` tool definition — name and `summary` input must match exactly.
- Routing semantics (`code` → repair pipeline, `heal_script` → PR,
  `manual` → tracker).
- Dedup rules (stem-based for `code`; exact-signature for `manual`).

**These strings are load-bearing — do not rename them:**
- Tool name: `emit_finding`
- Tool name: `skill_done`
- System-prompt heading: `## Skill to execute`

---

## Project Scaffolding & Verification

For the default TypeScript stack, generate these files alongside the engine modules. They are required for `typecheck` and `test` to pass.

### `package.json`

```json
{
  "type": "module",
  "scripts": {
    "build": "tsc",
    "typecheck": "tsc --noEmit",
    "test": "vitest run"
  },
  "dependencies": {
    "@anthropic-ai/bedrock-sdk": "^0.12.0",
    "@octokit/rest": "^21.0.0",
    "@linear/sdk": "^27.0.0",
    "@slack/web-api": "^7.0.0",
    "@aws-sdk/client-athena": "^3.0.0",
    "@aws-sdk/client-cloudwatch-logs": "^3.0.0",
    "@aws-sdk/client-cloudwatch": "^3.0.0",
    "@aws-sdk/client-cost-explorer": "^3.0.0"
  },
  "devDependencies": {
    "typescript": "^5.5.0",
    "@types/node": "^22.0.0",
    "vitest": "^2.0.0"
  }
}
```

Swap SDK packages per the chosen stack (see [`references/swap-table.md`](references/swap-table.md)). For Anthropic API direct, replace `@anthropic-ai/bedrock-sdk` with `@anthropic-ai/sdk`. For non-default VCS/tracker/chat, replace the matching SDK.

### `tsconfig.json`

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "strict": true,
    "skipLibCheck": true,
    "resolveJsonModule": true,
    "types": ["node"],
    "outDir": "dist"
  },
  "include": ["**/*.ts"]
}
```

If deploying as a Lambda with esbuild bundling, `moduleResolution: "bundler"` is correct. For plain Node ESM without a bundler, use `"moduleResolution": "node16"` and add `.js` extensions to all relative imports.

### `skills/md.d.ts` and runbook loading

The `skills/index.ts` module imports `.md` files as strings using bare `import` syntax. This requires:

1. A type declaration file `skills/md.d.ts`:

```typescript
declare module "*.md" {
  const text: string;
  export default text;
}
```

2. A bundler loader that materializes `.md` as text. For **esbuild** (the default Lambda bundler):

```bash
esbuild index.ts --bundle --platform=node --loader:.md=text --outfile=dist/index.js
```

3. If no bundler is used (e.g. `ts-node` in dev), replace the `import` statements in `skills/index.ts` with `readFileSync` calls:

```typescript
import { readFileSync } from "fs";
import { fileURLToPath } from "url";
import { dirname, join } from "path";
const __dirname = dirname(fileURLToPath(import.meta.url));
const scanLogs = readFileSync(join(__dirname, "scan-logs.md"), "utf-8");
```

Use whichever approach matches the deployment's build toolchain; both export the same `bundledSkills: Record<SkillName, string>` map.

### Tool definitions: pure-data module

Keep **tool input-schema definitions** (the `emit_finding` and `skill_done` objects, plus all application tool definitions) in a **pure-data module** (`tools/definitions.ts` or exported from `tools/index.ts`) that imports **no SDK packages** — only types. The executor implementations (functions that call AWS SDKs, Octokit, etc.) live in separate files. This split lets tests import tool definitions to validate schemas without instantiating SDK clients.

### Finalize scaffold

After generating all files, run:

```bash
npm install
npm run typecheck   # must exit 0
npm test            # must exit 0
```

Do not declare generation complete until both commands succeed.

---

## Config Parameterization

**`LOG_GROUPS` serialization:** populate `logGroups` in `config.ts` as a JSON array literal, not a string. Example: `logGroups: ["/aws/lambda/acme-api", "/aws/lambda/acme-worker"]`.

**Model IDs:** the default `MODEL_ID` value `us.anthropic.claude-sonnet-4-6` is an Amazon Bedrock **cross-region inference profile** (the `us.` prefix routes across US regions). When the user selects Anthropic API direct (Q1b option 2), use plain model strings instead — see the LLM-provider row in [`references/swap-table.md`](references/swap-table.md) for the mapping. The fallback model follows the same convention: `us.anthropic.claude-haiku-3-5` (Bedrock) or `claude-haiku-3-5` (Anthropic API direct).

Generate `config.ts` (or equivalent) populated with all collected answers:

```typescript
export const config = {
  productName: "{{PRODUCT_NAME}}",
  repo: "{{REPO_SLUG}}",
  model: "{{MODEL_ID}}",
  modelFallback: "{{FALLBACK_MODEL_ID}}",
  region: "{{AWS_REGION}}",

  maxPrsPerRun: {{maxPrsPerRun}},
  maxTicketsPerRun: {{maxTicketsPerRun}},
  maxIterations: {{maxIterations}},
  maxTokensPerCall: {{maxTokensPerCall}},
  patchCandidates: {{patchCandidates}},
  maxRepairAttempts: {{maxRepairAttempts}},

  runbooksDaily: {{DAILY_RUNBOOKS}},
  runbooksWeekly: {{WEEKLY_RUNBOOKS}},

  // Per-runbook config — consumed by runbooks via the runtime context block.
  // The scan-logs runbook reads these fields directly.
  scanLogs: {
    logGroups: {{LOG_GROUPS}},
    lookbackMinutes: 60,
    errorThreshold: 10,
    knownNoise: [] as string[],
  },
};
```

**The `scanLogs` block is required.** The `scan-logs` runbook reads
`logGroups`, `lookbackMinutes`, `errorThreshold`, and `knownNoise` from live
config at step 1. Without these fields, the runbook's first step fails.
Populate `logGroups` from `LOG_GROUPS`, and leave the remaining fields at their
defaults unless the user overrode them in Q4.

---

## Example Runbook Placement

Copy [`assets/runbooks/scan-logs.md`](assets/runbooks/scan-logs.md) verbatim
into `doctor/skills/scan-logs.md` in the generated output. Register it in
`doctor/skills/index.ts` and in `config.runbooksDaily`.

To add more runbooks later, use the `add-doctor-runbook` skill and follow
[`references/writing-runbooks.md`](references/writing-runbooks.md). That
reference contains the runbook skeleton, authoring checklist, and registration
steps. Always call audit definitions **runbooks**, never "skills".

---

## Tests

Generate tests for each engine module:

- `run-skill`: mock the Bedrock/Anthropic client; assert the anti-loop guard
  fires at 3 consecutive identical calls; assert `skill_done` breaks the loop;
  assert model fallback is attempted exactly once on a first-call error.
- `repair-pipeline`: test `applySearchReplaceBlocks` (zero-match error,
  multi-match error, single-match success), `parseSearchReplaceBlocks` (one
  block, multiple blocks), `selectWinner` (fewer-than-2-valid → null,
  tied majority → earliest wins).
- `repair-ci`: test `selectWinningOutcome` with N=3 (threshold=2) and N=1
  (threshold=1).
- `dedup`: assert code findings are suppressed when a matching branch/PR exists;
  assert manual findings are suppressed on exact-signature match only.
- `finding-contract` (types): assert the `emit_finding` schema rejects missing
  required fields.

---

## Scheduler / IaC

Generate scheduler config for three schedules: `daily`, `weekly`, `repair-ci`.
Each schedule passes `{ mode: "<mode>" }` as the invocation payload.

**EventBridge (default):** three `AWS::Scheduler::Schedule` resources (or CDK
`Schedule` constructs). Recommended cadences: daily 06:00 UTC, weekly Sunday
06:00 UTC, repair-ci every 30 minutes.

**GitHub Actions:** a `.github/workflows/doctor.yml` with three `schedule:`
cron entries plus a `workflow_dispatch` input `mode` so each schedule can be
triggered manually. Follow the GitHub Actions row in
[`references/swap-table.md`](references/swap-table.md).

**POSIX cron / systemd timer / K8s CronJob:** follow the matching row in
[`references/swap-table.md`](references/swap-table.md).

---

## Next Steps

After generation, print these steps to the user:

1. **Deploy.** Run `npm install && npm run build` (or `pip install -e .`) in
   the generated `doctor/` directory, then deploy using your chosen scheduler's
   IaC or workflow file.

2. **Add secrets.** Set the required environment variables or secrets:
   - `GITHUB_TOKEN` (or `GITLAB_TOKEN`) with repo read + PR write scope
   - `LINEAR_TOKEN` (or Jira/GitHub Issues equivalent) with issue-create scope
   - `SLACK_BOT_TOKEN` (or Teams webhook URL / Discord webhook URL)
   - Bedrock IAM role with `bedrock:InvokeModel` (or `ANTHROPIC_API_KEY`)
   - Data-source credentials if a query tool was selected

3. **Smoke-test.** Trigger the `daily` schedule manually and inspect the Slack
   digest. Confirm `scan-logs` runs without error (zero findings is the
   expected healthy outcome).

4. **Write your next runbook.** Use the `add-doctor-runbook` skill and follow
   [`references/writing-runbooks.md`](references/writing-runbooks.md). Start
   with the skeleton in that reference, work through the authoring checklist,
   then register the runbook in `doctor/skills/index.ts` and `config.ts`.

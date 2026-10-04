---
name: sf-agentforce-development
description: Building, previewing, testing and shipping Agentforce agents from a source-tracked SFDX project - authoring bundles and Agent Script, the Bot/BotVersion/GenAiPlannerBundle/GenAiPlugin/GenAiFunction metadata graph, custom agent actions written as invocable Apex, autolaunched Flows or prompt templates, action input/output JSON schemas, prompt templates and grounding, the agent user and the permissions it runs under, AiEvaluationDefinition test definitions and the sf agent test commands, agent preview in simulated and live mode, trace analysis, and moving an agent from scratch org to sandbox to production. Use this skill when a story mentions an agent, a copilot, a subagent, a topic, an agent action, an authoring bundle, a .agent file, Agentforce Builder, Testing Center, Prompt Builder, an @InvocableMethod that an agent calls, or when an agent routes to the wrong action, returns data the running user should not see, or fails to activate after a deploy.
---

# Agentforce agent development

An agent is metadata. It moves through the same retrieve/deploy/version-control loop as Apex, and
it breaks in the same ways: wrong permissions, wrong deploy order, untested contracts. The parts
that are genuinely new are the **planner** (an LLM chooses which action to run, from your prose)
and the **agent user** (every action runs as a service user, not as the person chatting).

This skill covers the API 67.0 metadata shape pinned in `config/vibe-force.defaults.json`, and
names what changes at 68.0. Grounding data modelled in Data 360 belongs to skill `sf-data-cloud`;
this skill links to it rather than re-explaining data streams, DMOs or retrievers.

## When to use

| Situation | Tool | Why |
| --- | --- | --- |
| Free-form user request, unknown number of steps, natural language in and out | **Agent** | The planner picks actions at runtime; you cannot enumerate the branches |
| Deterministic multi-step process with known branches, admin-maintainable | **Flow** | No LLM cost, no non-determinism, testable by construction (skill `sf-flow-automation`) |
| Transactional logic, bulk DML, callouts, anything needing exact control | **Apex** | Wrap it in `@InvocableMethod` and let the agent call it - do not push logic into instructions |
| Fixed UI on a record page, known inputs, sub-second response | **LWC** | An agent is the wrong shape for a form (skill `sf-lwc-development`) |
| One prompt, one record, one generated field or email | **Prompt template alone** | No agent needed; call it from Flow, Apex or the Connect API |
| Needs an auditable, repeatable, identical result every run | **Not an agent** | LLM output varies; tests score, they do not assert equality |
| Story says "summarise", "answer questions about", "help the rep decide" | **Agent** | Then read `references/action-patterns.md` before writing any Apex |

| Trigger | Go to |
| --- | --- |
| "Create an agent", "new subagent", "new topic" | Patterns 1-3, `references/agent-cli-reference.md` |
| "Add an action" of any kind | Pattern 4, `references/action-patterns.md` |
| Action description / routing quality problem | Action design section, Anti-patterns |
| "Test the agent", "Testing Center", regression suite | Pattern 6, `references/testing-and-evaluation.md` |
| Moving an agent between orgs, activation, packaging | Pattern 7-8, `references/deployment-checklist.md` |
| "What metadata type is X", manifest authoring | `references/metadata-reference.md` |
| Agent reads records the end user must not see | Anti-patterns, skill `sf-security-model` |

## Core patterns

### 1. Provision an org that can run agents

`agent` CLI commands fail with `This feature is not currently enabled for this user type or org`
when Einstein or Agentforce is off. Scratch orgs turn both on declaratively:

```json
{
  "orgName": "vf agent dev",
  "edition": "Developer",
  "features": ["EnableSetPasswordInApi", "Einstein1AIPlatform"],
  "settings": {
    "agentPlatformSettings": { "enableAgentPlatform": true },
    "einsteinGptSettings": { "enableEinsteinGptPlatform": true }
  }
}
```

```bash
sf org create scratch --definition-file config/afdx-scratch-def.json \
  --alias vf-agent --set-default --target-dev-hub DevHub
```

Sandboxes need the same two switches set manually in Setup after creation. If the agent grounds on
Data 360, use a sandbox, not a scratch org - see skill `sf-data-cloud`.

### 2. Create the agent user before the agent

Every action an agent runs executes as a dedicated Salesforce user. Create it first, because the
Agent Script file references it by username:

```bash
sf org create agent-user --base-username vf-agent@example.com --target-org vf-agent
```

The command assigns the `Einstein Agent User` profile plus the `AgentforceServiceAgentBase`,
`AgentforceServiceAgentUser` and `EinsteinGPTPromptTemplateUser` permission sets, and verifies the
licences exist. It does not grant object, field or record access for *your* data - that is a
permission set you write (skill `sf-security-model`). The generated user has no password and
cannot log in.

### 3. Author from a spec, not from a blank file

```bash
# 1. Spec: role + company context, LLM proposes subagents
sf agent generate agent-spec --type internal --max-topics 5 \
  --role "Answer rep questions about open opportunities and log next steps." \
  --company-name "Acme" --company-description "B2B industrial supplies" \
  --agent-user vf-agent@example.com --tone neutral \
  --output-file specs/opportunityCoach.yaml --target-org vf-agent

# 2. Authoring bundle: the .agent blueprint, written in Agent Script
sf agent generate authoring-bundle --spec specs/opportunityCoach.yaml \
  --name "Opportunity Coach" --api-name Opportunity_Coach --target-org vf-agent

# 3. Compile check, local, fast, run after every edit
sf agent validate authoring-bundle --api-name Opportunity_Coach --target-org vf-agent
```

The bundle lands in `force-app/main/default/aiAuthoringBundles/Opportunity_Coach/` as
`Opportunity_Coach.agent` plus `Opportunity_Coach.bundle-meta.xml`. A bundle generated with
`--no-spec` is boilerplate; a thin spec produces generic subagents. Spec quality is the single
biggest lever on generated output.

### 4. Declare an action with an explicit contract

Agent Script actions name a target by URI scheme - `apex`, `flow` or `prompt` - and declare typed
inputs and outputs:

```agentscript
subagent opportunity_review:

    actions:
        summarise_pipeline:
            description: "Return open-opportunity totals and the next step for one account."
            inputs:
                accountId: string
                    label: "Account Id"
                    description: "18-character Salesforce Id of the account to summarise."
                    is_required: True
            outputs:
                summary: string
                openAmount: number
            target: "apex://OpportunityPipelineAction"
```

The Apex behind it obeys the invocable contract - one list in, a list of the same size and order
out, `USER_MODE` on every query:

```apex
public with sharing class OpportunityPipelineAction {

    public class Request {
        @InvocableVariable(required=true label='Account Id'
            description='18-character Salesforce Id of the account to summarise.')
        public Id accountId;
    }

    public class Result {
        @InvocableVariable(label='Summary'
            description='One sentence naming the open pipeline value and the next step.')
        public String summary;
        @InvocableVariable(label='Open amount')
        public Decimal openAmount;
    }

    @InvocableMethod(
        label='Summarise Account Pipeline'
        description='Returns open-opportunity totals and the next step for the given account.'
        category='Sales'
    )
    public static List<Result> run(List<Request> requests) {
        Set<Id> accountIds = new Set<Id>();
        for (Request r : requests) { accountIds.add(r.accountId); }

        Map<Id, Decimal> totals = new Map<Id, Decimal>();
        for (AggregateResult ar : [
            SELECT AccountId aid, SUM(Amount) total
            FROM Opportunity
            WHERE AccountId IN :accountIds AND IsClosed = false
            WITH USER_MODE
            GROUP BY AccountId
        ]) {
            totals.put((Id) ar.get('aid'), (Decimal) ar.get('total'));
        }

        List<Result> results = new List<Result>();
        for (Request r : requests) {          // same size, same order as the input
            Result out = new Result();
            out.openAmount = totals.containsKey(r.accountId) ? totals.get(r.accountId) : 0;
            out.summary = out.openAmount == 0
                ? 'No open opportunities for this account.'
                : 'Open pipeline is ' + out.openAmount + '.';
            results.add(out);
        }
        return results;
    }
}
```

Full annotation rules, the Flow and prompt-template variants, and the `GenAiFunction` JSON schema
form live in `references/action-patterns.md`. The general `@InvocableMethod` contract is owned by
skill `sf-flow-automation`.

### 5. Preview before publishing

```bash
# Simulated: LLM mocks every action. Use while the Apex or Flow does not exist yet.
sf agent preview --authoring-bundle Opportunity_Coach --target-org vf-agent

# Live: real Apex, Flows and prompt templates, with Apex Replay Debugger support.
sf agent preview --authoring-bundle Opportunity_Coach --use-live-actions --apex-debug \
  --output-dir transcripts/coach --target-org vf-agent
```

Live mode uses whatever is **deployed**, so deploy the Apex first. Preview writes trace files;
read them by dimension instead of guessing:

```bash
sf agent preview sessions
sf agent trace read --session-id <SESSION_ID> --format detail --dimension routing
sf agent trace read --session-id <SESSION_ID> --format detail --dimension actions
```

`--dimension` accepts `actions`, `grounding`, `routing`, `errors`. Routing answers "why did it pick
that subagent"; actions answers "what did it actually call, with what inputs".

### 6. Publish, then test with a spec-driven suite

```bash
sf project deploy start --metadata "ApexClass:OpportunityPipelineAction" --target-org vf-agent
sf agent publish authoring-bundle --api-name Opportunity_Coach --target-org vf-agent

sf agent generate test-spec --output-file specs/Opportunity_Coach-testSpec.yaml
sf agent test create --spec specs/Opportunity_Coach-testSpec.yaml \
  --api-name Opportunity_Coach_Test --target-org vf-agent
sf agent test run --api-name Opportunity_Coach_Test --wait 10 \
  --result-format junit --output-dir .vibeforce/reports --target-org vf-agent
```

`agent test create` writes an `AiEvaluationDefinition` component back into the project. The agent
must exist in the org before the test can be created. Expectations are scored, not asserted:
`topic_sequence_match` and `action_sequence_match` are the deterministic ones and the only
sensible CI gate. See `references/testing-and-evaluation.md`.

### 7. Move the agent between orgs

At API 67.0 an agent is a graph, not a file. Retrieve the whole graph the first time:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Package xmlns="http://soap.sforce.com/2006/04/metadata">
    <types><members>Opportunity_Coach</members><name>Bot</name></types>
    <types><members>Opportunity_Coach.v1</members><name>BotVersion</name></types>
    <types><members>Opportunity_Coach_v1</members><name>GenAiPlannerBundle</name></types>
    <types><members>Opportunity_Coach_1</members><name>AiAuthoringBundle</name></types>
    <types><members>OpportunityPipelineAction</members><name>ApexClass</name></types>
    <version>67.0</version>
</Package>
```

```bash
sf project retrieve start --manifest manifest/package.xml --target-org vf-dev
sf project deploy start --manifest manifest/package.xml --target-org vf-int
```

With source tracking on, `--metadata Agent:Opportunity_Coach` is a CLI-only shorthand that resolves
the whole agent graph. The retrieved metadata carries the **source org's** agent username; replace
it before deploying, or the agent cannot run in the target. Deploy order, the draft/committed
distinction and post-deploy checks are in `references/deployment-checklist.md`.

### 8. Activate deliberately

```bash
sf agent activate --api-name Opportunity_Coach --version 1 --target-org vf-int
sf agent deactivate --api-name Opportunity_Coach --target-org vf-int
```

Only one version is active at a time, and `--version` is the number in `vN.botVersion-meta.xml`.
A deployed agent is not a live agent. Activation is a separate, reversible step and belongs in the
release runbook, not in the deploy command (skill `sf-deployment-strategies`).

## Action design

The planner reads your prose. Descriptions are the routing algorithm's only input, so they are
production code, not documentation.

| Property | Rule | Failing example | Working example |
| --- | --- | --- | --- |
| Action description | Name the job, the entity and the trigger condition | `Gets data` | `Returns open-opportunity totals for one account when the user asks about pipeline.` |
| Input description | State the format and where the value comes from | `The id` | `18-character Salesforce Id of the account; obtain it from the record lookup action first.` |
| Output description | State what the agent should do with it | `Result` | `One-sentence pipeline summary; quote it verbatim to the user.` |
| Output visibility | At least one output must be flagged as used by the planner, or responses drift | all outputs display-only | one output marked for planner use (`copilotAction:isUsedByPlanner`) |
| Overlap | Two actions must not match the same utterance | `GetAccount` + `FetchAccount` | one action, one branch inside it |
| Granularity | One verb, one object | `ManageOrder` doing 6 things | `CancelOrder`, `RescheduleOrder` |

Typing rules that the runtime enforces:

- One input parameter, one output list. Both are lists because actions are bulkified; the i-th
  output must correspond to the i-th input.
- Input and output property types come from a fixed `lightning__*` set. `lightning__textType`
  caps at 250 characters - long prose must be `lightning__multilineTextType` or `richTextType`.
- `@InvocableVariable` fields of type `List<List<sObject>>` cause a runtime error inside
  user-defined classes.
- From API 66.0, an Apex class used for invocable parameters needs a visible no-argument
  constructor.

Idempotence: the planner may call the same action twice in one conversation, and a test rerun
replays the same utterance. Reads are naturally safe. Writes must be made repeatable - upsert on an
external id, or check for an existing record before creating one - and destructive actions should
set confirmation-required so the user approves before the write.

Failure handling: an invocable method must return the same number of results as it received, even
when individual items fail. Return a success flag and a message on the result object instead of
throwing, so one bad input does not abort the whole batch.

## Anti-patterns

| Anti-pattern | Failing code | Fix |
| --- | --- | --- |
| Loop-per-request DML or SOQL | `for (Request r : requests) { [SELECT ... WHERE Id = :r.id]; }` | Collect ids, query once, map results back by index (skill `sf-governor-limits`) |
| Returning fewer results than inputs | `if (bad) { continue; }` inside the result loop | Always add a result; carry `success=false` and a reason |
| Vague description | `@InvocableMethod(label='Do it')` | Label and description naming entity, action and when to use it |
| Sharing bypassed | `public without sharing class OrderAction` | `with sharing` + `WITH USER_MODE` / `AccessLevel.USER_MODE`; the agent user is a real user (skill `sf-security-model`) |
| Grounding on data the agent user cannot see | Action queries `Contact.SSN__c`; agent user lacks FLS -> empty or error at runtime | Grant the agent user exactly the object, field and record access the actions need, and no more |
| Instructions doing arithmetic or policy | `instructions: "compute the 12% discount and apply it"` | Move deterministic logic into Apex or Flow; the LLM must not be the calculator |
| Two overlapping actions | `GetCase` and `LookupCase` both described as "find a case" | Delete one; overlapping descriptions make routing non-deterministic |
| Publish assumed to deploy Apex | `sf agent publish authoring-bundle` after editing a local Apex class | Deploy the Apex first; publishing a bundle never deploys `ApexClass` or `Flow` |
| Partial retrieve of an agent | `sf project retrieve start --metadata AiAuthoringBundle:My_Agent` | Add the wildcard (`My_Agent*`) for all versions, or use a full manifest |
| Deploying a version into an org that lacks the agent | manifest with `BotVersion` only | Deploy the whole agent graph first, then versions |
| Treating `bot_response_rating` as a CI gate | pipeline fails on a scored metric | Gate on `topic_sequence_match` / `action_sequence_match`; track scored metrics as trends |
| `sfdx force:*` syntax anywhere | `sfdx force:source:deploy` | `sf project deploy start --target-org <alias>` (skill `sf-cli-operations`) |

## Verification

Local, no org, before anything else:

```bash
sf agent validate authoring-bundle --api-name Opportunity_Coach --target-org vf-dev
node "${CLAUDE_PLUGIN_ROOT}/scripts/checks/vf-check.mjs" local --changed
```

Apex behind the actions, in an org:

```bash
node "${CLAUDE_PLUGIN_ROOT}/scripts/checks/vf-check.mjs" apex \
  --target-org vf-dev --tests OpportunityPipelineActionTest
```

Agent behaviour, in an org:

```bash
sf agent test list --target-org vf-dev
sf agent test run --api-name Opportunity_Coach_Test --wait 10 \
  --result-format junit --output-dir .vibeforce/reports --target-org vf-dev
sf agent test results --use-most-recent --verbose --target-org vf-dev
```

Deploy gates and post-deploy state:

```bash
node "${CLAUDE_PLUGIN_ROOT}/scripts/checks/vf-check.mjs" deploy-validate --target-org vf-int
node "${CLAUDE_PLUGIN_ROOT}/scripts/checks/vf-check.mjs" smoke --target-org vf-int

# The agent and its versions exist in the target org
sf org list metadata --metadata-type Bot --target-org vf-int
sf org list metadata --metadata-type BotVersion --target-org vf-int

# The agent user is active and licensed
sf data query --target-org vf-int --query \
  "SELECT Id, Username, IsActive, Profile.Name FROM User WHERE Profile.Name = 'Einstein Agent User'"
```

`vf-check verify` runs the wave-4 verdict once the smoke probes pass (skill
`sf-workflow-orchestration`). For a failing conversation, reproduce it with `sf agent preview` and
read the trace before changing any instruction text (skill `sf-debugging-logs` for the Apex side).

## References

- [references/metadata-reference.md](references/metadata-reference.md) - every agent-related
  metadata type, its file suffix, directory, API version floor and fields; manifests for whole
  agents and single versions; the v67 to v68 change.
- [references/action-patterns.md](references/action-patterns.md) - invocable Apex, Flow and
  prompt-template actions end to end, `GenAiFunction` input/output schema properties, description
  quality rubric, security and idempotence.
- [references/testing-and-evaluation.md](references/testing-and-evaluation.md) -
  `AiEvaluationDefinition` shape, test spec YAML, expectation and metric catalogue, custom
  evaluations with JSONPath, CI wiring, limits.
- [references/deployment-checklist.md](references/deployment-checklist.md) - org prerequisites,
  permissions, deploy order, draft versus committed agents, activation, post-deploy queries.
- [references/agent-cli-reference.md](references/agent-cli-reference.md) - every `sf agent`,
  `sf org create agent-user` and `sf org open agent` subcommand with its verified flags.

Official documentation used (fetched for this skill):

- Build Agents with Agentforce DX - https://developer.salesforce.com/docs/ai/agentforce/guide/agent-dx.html
- Agent Metadata: A Shallow Dive - https://developer.salesforce.com/docs/ai/agentforce/guide/agent-dx-metadata.html
- Set Up Your DX Environment - https://developer.salesforce.com/docs/ai/agentforce/guide/agent-dx-set-up-env.html
- Agentforce-Ready Scratch Org - https://developer.salesforce.com/docs/ai/agentforce/guide/scratch-org.html
- Use Metadata to Move an Agent to a New Org - https://developer.salesforce.com/docs/ai/agentforce/guide/agent-dx-deploy-metadata.html
- Define Agent Metadata (v67 and Earlier) - https://developer.salesforce.com/docs/ai/agentforce/guide/agent-dx-api-v67-earlier.html
- Agent Script reference: actions - https://developer.salesforce.com/docs/ai/agentforce/guide/ascript-ref-actions.html
- Troubleshoot Agentforce DX Issues - https://developer.salesforce.com/docs/ai/agentforce/guide/agent-dx-troubleshooting.html
- Metadata API Developer Guide: Bot - https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_bot.htm
- Metadata API Developer Guide: GenAiPlannerBundle - https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_genaiplannerbundle.htm
- Metadata API Developer Guide: GenAiFunction - https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_genaifunction.htm
- Metadata API Developer Guide: AiEvaluationDefinition - https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_aievaluationdefinition.htm
- Apex Developer Guide: InvocableMethod Annotation - https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_classes_annotation_InvocableMethod.htm
- Salesforce CLI Command Reference: agent Commands - https://developer.salesforce.com/docs/platform/salesforce-cli-reference/guide/cli_reference_agent.html

---
name: n8n
description: Complete n8n skill — workflow building, node configuration, JavaScript/Python code nodes, expression syntax, validation, MCP tools, credentials, administration, Docker deployment, backup/restore, internal API, and troubleshooting. Auto-triggers on any n8n task including workflow creation, node configuration, code nodes, expressions, validation errors, credential management, instance administration, n8n setup, n8n upgrade, n8n backup, and n8n API usage.
disable-model-invocation: false
user-invokable: true
argument-hint: "n8n task description"
---

# n8n

Complete skill for building, managing, and administering n8n workflows.

---

## How to Use This Skill

This skill covers 9 domains. Each has its own reference file with detailed guidance.

### Workflow Building (from [czlonkowski/n8n-skills](https://github.com/czlonkowski/n8n-skills))

| Domain | Reference | When to use |
|--------|-----------|-------------|
| **Workflow Patterns** | [czlonkowski/skills/n8n-workflow-patterns/SKILL.md](czlonkowski/skills/n8n-workflow-patterns/SKILL.md) | Building new workflows, choosing architecture (webhook, HTTP API, database, AI agent, scheduled) |
| **Node Configuration** | [czlonkowski/skills/n8n-node-configuration/SKILL.md](czlonkowski/skills/n8n-node-configuration/SKILL.md) | Configuring nodes, understanding property dependencies, required fields by operation |
| **Code — JavaScript** | [czlonkowski/skills/n8n-code-javascript/SKILL.md](czlonkowski/skills/n8n-code-javascript/SKILL.md) | Writing JS in Code nodes, `$input/$json/$node` syntax, `$helpers.httpRequest()`, DateTime |
| **Code — Python** | [czlonkowski/skills/n8n-code-python/SKILL.md](czlonkowski/skills/n8n-code-python/SKILL.md) | Writing Python in Code nodes, `_input/_json` syntax, standard library, limitations |
| **Expression Syntax** | [czlonkowski/skills/n8n-expression-syntax/SKILL.md](czlonkowski/skills/n8n-expression-syntax/SKILL.md) | Writing `{{ }}` expressions, `$json/$node` variables, fixing expression errors |
| **Validation** | [czlonkowski/skills/n8n-validation-expert/SKILL.md](czlonkowski/skills/n8n-validation-expert/SKILL.md) | Interpreting validation errors/warnings, false positives, validation profiles |
| **MCP Tools** | [czlonkowski/skills/n8n-mcp-tools-expert/SKILL.md](czlonkowski/skills/n8n-mcp-tools-expert/SKILL.md) | Using n8n MCP tools effectively — tool selection, parameter formats, common patterns |

### Additional Domains

| Domain | Reference | When to use |
|--------|-----------|-------------|
| **Credentials** | [credentials/SKILL.md](credentials/SKILL.md) | Credential types, REST API credential CRUD, HTTP Request auth modes, httpCustomAuth JSON format, predefinedCredentialType vs genericCredentialType |
| **Administration** | [administration/SKILL.md](administration/SKILL.md) | Instance operations the MCP doesn't cover — Docker, backup/restore, CLI commands, internal API, community packages, SSO, upgrades, troubleshooting |

---

## Quick Decision: Which Tool to Use

| You want to... | Tool |
|----------------|------|
| Create/edit/delete workflows | MCP (`n8n_create_workflow`, `n8n_update_partial_workflow`) |
| Search nodes, get schema | MCP (`search_nodes`, `get_node`) |
| Validate workflow or node | MCP (`n8n_validate_workflow`, `validate_node`) |
| Auto-fix workflow issues | MCP (`n8n_autofix_workflow`) |
| Deploy a template | MCP (`n8n_deploy_template`) |
| Test/trigger a workflow | MCP (`n8n_test_workflow`) |
| Manage executions | MCP (`n8n_executions`) |
| Create/update credentials | Public REST API (`/api/v1/credentials`) |
| Test a credential | Internal API (`POST /credentials/test`) — see [credentials](credentials/SKILL.md) |
| Install community packages | Internal API (`POST /community-packages`) — see [administration](administration/SKILL.md) |
| Export decrypted credentials | CLI (`n8n export:credentials --decrypted`) — see [administration](administration/SKILL.md) |
| Backup/restore database | CLI / Docker — see [administration](administration/SKILL.md) |
| Upgrade n8n | Docker — see [administration](administration/SKILL.md) |

**Priority: MCP → Public API → Internal API → CLI → Docker/Infra.**

---

## Core Concepts (Quick Reference)

### Webhook Data Access
```javascript
// CRITICAL: webhook data is nested under .body
const data = $input.first().json.body;  // NOT $input.first().json
```

### Code Node Return Format
```javascript
// MUST return array of {json: {...}} objects
return items.map(item => ({
  json: { ...item.json, processed: true }
}));
```

### Expression Syntax
```
{{ $json.fieldName }}           // Current item field
{{ $node["NodeName"].json }}    // Another node's output
{{ $now.toISO() }}              // Current timestamp
{{ $env.MY_VAR }}               // Environment variable
```

### Credential Linking (in workflow JSON)
```json
{
  "credentials": {
    "httpHeaderAuth": { "id": "CRED_ID", "name": "My API Key" }
  }
}
```

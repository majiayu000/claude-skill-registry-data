---
name: custom-connector-generator
description: "Generate Power Automate custom connectors from OpenAPI specs: convert OpenAPI 3.x to Swagger 2.0, add x-ms-* extensions, build apiProperties.json auth, PAC CLI deploy scripts. Use to create, convert, optimize or deploy a custom connector."
---

# Power Automate Custom Connector Generator

Transforms OpenAPI specifications into production-ready Power Automate custom connectors with proper authentication, Microsoft extensions and deployment scripts. Code blocks, auth examples, patterns and walkthroughs live in `references/authoring-snippets.md`.

## When to use

- An OpenAPI 3.x spec must become a custom connector, or a connector is built from scratch.
- Authentication must be added to a connector.
- A connector must be deployed with PAC CLI, or optimized with x-ms extensions.
- The user wants to understand the custom connector structure.

## Critical Power Platform constraints

- **CRITICAL**: custom connectors ONLY support OpenAPI 2.0 (Swagger). OpenAPI 3.0/3.1 is NOT supported: convert to Swagger 2.0. The file MUST be named `apiDefinition.swagger.json`.
- Files: `apiDefinition.swagger.json` (required), `apiProperties.json` (required, authentication and metadata), `icon.png` (optional, 32x32 or 64x64), `script.csx` (optional, custom C#).

## Workflow

### Step 1: Analyze the input

1. Version: `openapi` field (3.x, conversion required) or `swagger` field (2.0, enhance with x-ms extensions).
2. Authentication: OAuth 2.0 (check authorization/token URLs), API key (security definitions), Basic, or several options (use `connectionParameterSets`).
3. Operations: count by verb, identify parameters (path, query, body, header), pagination patterns, webhooks/triggers.

### Step 2: Convert OpenAPI 3.x to Swagger 2.0

- `openapi: "3.x"` to `swagger: "2.0"`
- `servers` to `host`, `basePath`, `schemes`
- `components.schemas` to `definitions`
- `components.securitySchemes` to `securityDefinitions`
- `requestBody` to `parameters` with `in: "body"`
- `content` (media types) to `consumes`/`produces`

Refer to `references/swagger-2.0-guide.md` for complete rules, `references/authoring-snippets.md` for a before/after.

### Step 3: Add Microsoft extensions

Essential: `x-ms-summary` (display name in the UI), `x-ms-visibility` (`important`, `advanced`, `internal`), `x-ms-dynamic-values` (dropdown from another operation: `operationId`, `value-path`, `value-title`). Snippets: `references/authoring-snippets.md`. All extensions: `references/x-ms-extensions-guide.md`.

### Step 4: Generate apiProperties.json

Structure: `properties.iconBrandColor`, `capabilities`, `connectionParameters`, `policyTemplateInstances`.

- OAuth 2.0 (recommended when the API has it): `type: oauthSetting` with `oAuthSettings` (identityProvider, clientId, scopes, redirectMode, customParameters for authorization/token/refresh URLs).
- API key: `type: securestring` with `uiDefinition` (displayName, description, tooltip, constraints with `clearText: false`).
- Basic: a `string` username plus a `securestring` password.

Examples: `references/authoring-snippets.md`. Complete patterns: `references/apiproperties-guide.md`.

### Step 5: Apply best practices

- Operations: group with `tags`, descriptive `operationId` (GetUser, CreateOrder), `summary` and `x-ms-summary` on every operation.
- Parameters: mark required clearly, set `x-ms-visibility`, use `x-ms-dynamic-values` for lists, add descriptions and tooltips.
- Responses: complete schemas (not just status codes), examples, `$ref` for reuse.
- Errors: document 4xx/5xx with an error schema (code/message) and meaningful descriptions.

### Step 6: Generate deployment scripts

```bash
pac connector create --api-definition-file ./apiDefinition.swagger.json --api-properties-file ./apiProperties.json --icon-file ./icon.png --environment "YOUR_ENVIRONMENT_ID"
pac connector update --api-definition-file ./apiDefinition.swagger.json --api-properties-file ./apiProperties.json --connector-id "YOUR_CONNECTOR_ID" --environment "YOUR_ENVIRONMENT_ID"
paconn validate --api-def ./apiDefinition.swagger.json
```

## Output format

Provide: `apiDefinition.swagger.json` (Swagger 2.0, x-ms extensions, complete schemas, securityDefinitions), `apiProperties.json` (auth type, brand color, policy templates if needed), `deployment.md` (PAC CLI commands, environment setup, testing checklist), `README.md` (overview, auth setup, operations, known limitations).

## Patterns and walkthroughs

`references/authoring-snippets.md` holds the three common patterns (Bearer token conversion, OAuth 2.0 with dynamic dropdowns, multi-authentication) and three step-by-step walkthroughs (convert a spec, add OAuth, optimize UX). Full before/after files: `references/examples.md`.

## Reference files

- `references/swagger-2.0-guide.md`: Swagger 2.0 specification and conversion.
- `references/x-ms-extensions-guide.md`: all Microsoft extensions with examples.
- `references/apiproperties-guide.md`: apiProperties.json structure and authentication.
- `references/examples.md`: complete conversion examples.
- `templates/basic-connector-template.json`: minimal working connector.

## Validation checklist

- [ ] `swagger: "2.0"` (not openapi)
- [ ] All operations have `summary` and `x-ms-summary`
- [ ] Required parameters marked correctly, appropriate `x-ms-visibility` levels
- [ ] Authentication configured in both files
- [ ] Response schemas defined (not just `200: {}`), error responses documented
- [ ] PAC CLI commands use correct placeholders
- [ ] README includes setup instructions

## Important limitations

1. OpenAPI 3.x is NOT supported: convert to Swagger 2.0.
2. Single security definition: the first scheme in the list is used.
3. No OpenAPI callbacks: webhooks must use `x-ms-notification-content`.
4. `apiDefinition.swagger.json` must be under 1 MB.
5. Use `x-ms-dynamic-schema` for truly dynamic responses.

## Notes

- Use official Microsoft documentation as the source of truth and test in a development environment first.
- A premium license is required for custom connectors. Custom code (`script.csx`) is available for advanced scenarios.
- microsoft/PowerPlatformConnectors on GitHub has 900+ examples.

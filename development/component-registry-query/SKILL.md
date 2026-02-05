---
name: component-registry-query
description: Query ACM/MCE component registry information including squad ownership, GitHub repositories, Konflux components, JIRA components, bundles, and prodsec components. Use when user asks about component ownership, squad assignments, repository URLs, component mappings, or any queries related to ACM/MCE components like "which squad owns X", "what's the repo for Y", "list components for Z squad", "what JIRA component for X", or "show all Server Foundation components".
allowed-tools: Read, Bash, Grep
---

# Component Registry Query Skill

This skill helps query the ACM/MCE component registry (component-registry.yaml) to find information about components, squads, repositories, and their relationships.

## What this skill does

- Find which squad owns a specific component
- List all components owned by a squad
- Get GitHub repository URL for a component
- Find Konflux component names
- Get JIRA component mappings
- Find bundle information
- Get prodsec component identifiers
- Search components by various attributes

## Instructions

### Step 1: Load the component registry

First, read the component-registry.yaml file. The file is located at `product/component-registry.yaml` relative to the project root:

```bash
cat product/component-registry.yaml
```

Or use the Read tool to read the file directly.

### Step 2: Parse and query the data

The YAML structure contains a list of components with these fields:
- `name`: Component name
- `konflux_component`: Konflux component identifier
- `bundle`: Bundle name (e.g., "mce-operator-bundle", "acm-operator-bundle")
- `repository`: GitHub repository URL
- `prodseccomponent`: Product security component identifier
- `squad`: Squad/team name
- `jira_component`: JIRA component name

### Step 3: Answer the query

Process the YAML data to answer questions like:

**Squad ownership queries:**
- "Which squad owns [component]?" → Find component and return squad field
- "What components does [squad] own?" → Filter by squad field and list all components

**Repository queries:**
- "What's the GitHub repo for [component]?" → Return repository field
- "Show me the repo URL for [component]" → Return repository field

**Component mapping queries:**
- "What's the Konflux component for [component]?" → Return konflux_component field
- "What JIRA component for [component]?" → Return jira_component field
- "What bundle is [component] in?" → Return bundle field

**List queries:**
- "List all Server Foundation components" → Filter by squad: "Server Foundation"
- "Show all components in mce-operator-bundle" → Filter by bundle
- "What components are in the GRC squad?" → Filter by squad: "GRC"

### Step 4: Format the response

Present the information clearly:
- For single component queries: Show all relevant fields
- For list queries: Use bullet points or tables
- Include links to GitHub repositories when showing repo information
- Highlight the specific information requested

## Examples

### Example 1: Find squad ownership

**User asks:** "Which squad is responsible for cluster-proxy?"

**Process:**
1. Read component-registry.yaml
2. Search for component with name: "cluster-proxy"
3. Extract the squad field

**Response:**
```
The cluster-proxy component is owned by the Server Foundation squad.

Additional details:
- Konflux component: cluster-proxy-mce
- Repository: https://github.com/stolostron/cluster-proxy
- Bundle: mce-operator-bundle
- JIRA component: Server Foundation
```

### Example 2: Find repository URL

**User asks:** "What's the GitHub repo for thanos?"

**Process:**
1. Read component-registry.yaml
2. Find component with name: "thanos"
3. Return repository URL

**Response:**
```
The GitHub repository for thanos is: https://github.com/stolostron/thanos

This component is:
- Owned by: Observability squad
- Part of: acm-operator-bundle
- Konflux component: thanos-acm
```

### Example 3: List squad components

**User asks:** "What components does the Hypershift squad own?"

**Process:**
1. Read component-registry.yaml
2. Filter all components where squad == "Hypershift"
3. List component names

**Response:**
```
The Hypershift squad owns the following components:

- cluster-api-provider-agent
- cluster-api-provider-kubevirt
- hypershift-addon-operator
- hypershift-cli
- hypershift-release
```

### Example 4: Multiple attribute query

**User asks:** "Show me all components in the Install squad with their repos"

**Process:**
1. Read component-registry.yaml
2. Filter by squad: "Install"
3. Extract name and repository for each

**Response:**
```
Install squad components:

1. backplane-must-gather
   Repository: https://github.com/stolostron/backplane-must-gather

2. backplane-operator
   Repository: https://github.com/stolostron/backplane-operator

3. discovery-operator
   Repository: https://github.com/stolostron/discovery

4. mce-operator-bundle
   Repository: https://github.com/stolostron/mce-operator-bundle

5. acm-operator-bundle
   Repository: https://github.com/stolostron/acm-operator-bundle

6. multiclusterhub-operator
   Repository: https://github.com/stolostron/multiclusterhub-operator
```

## Tips for effective queries

1. **Use exact component names** when possible (case-sensitive matching preferred)
2. **Common squad names** include: Server Foundation, Install, Hypershift, CAPI, Assisted Installer, Cluster Lifecycle, Console, Hive, GRC, Observability, Search, etc.
3. **Repository URLs** are GitHub links - can be opened directly
4. **Some components may not have all fields** - handle missing data gracefully
5. **JIRA components** may differ from squad names (e.g., "Infrastructure Operator" vs "Assisted Installer")

## Error handling

- If component not found: Suggest similar component names or ask user to verify spelling
- If squad not found: List all available squads
- For missing fields: Indicate field is not available for that component
- For ambiguous queries: Ask for clarification

## Notes

- The component-registry.yaml file is located at: `product/component-registry.yaml` (relative to project root)
- Data is sourced from product-manifest.json and component-squad.yaml
- Last updated information is in the header comments of the YAML file
- Some components may have duplicate entries with different Konflux component names

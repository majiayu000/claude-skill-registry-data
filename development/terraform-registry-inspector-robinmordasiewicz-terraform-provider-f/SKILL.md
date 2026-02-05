---
name: terraform-registry-inspector
description: Terraform Registry documentation inspector using Chrome DevTools MCP. Use when validating provider documentation rendering, checking version availability, navigating resource/data-source docs, finding source code links, or comparing documentation quality against the Azure RM gold standard. Triggers on requests to inspect, validate, review, or benchmark Terraform provider documentation on registry.terraform.io.
---

# Terraform Registry Documentation Inspector

A specialized skill for investigating Terraform provider documentation rendering on the Terraform Registry using Chrome DevTools MCP server capabilities.

## Purpose

This skill enables systematic investigation of:
- Provider documentation rendering quality
- Version availability and selection
- Resource/data-source documentation navigation
- Subcategory organization
- Source code repository links
- Markdown rendering issues

## Gold Standard Reference: Azure RM Provider

The **HashiCorp Azure RM Provider** (`hashicorp/azurerm`) represents the gold standard for professional Terraform provider documentation. All quality assessments should be benchmarked against this reference.

**Gold Standard URL**: `https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs`

### Gold Standard Quality Elements

#### Provider Index Page Excellence

| Element | Azure RM Implementation |
|---------|------------------------|
| **Provider Description** | Links to official Microsoft Azure documentation |
| **Clear Sections** | Data Sources explanation, Resources explanation |
| **External Links** | Tutorial links, changelog reference |
| **Authentication** | Multiple auth method guides as separate linked pages |
| **Note Callouts** | Important warnings with proper formatting |
| **Issue Reporting** | "Bugs and Feature Requests" section with GitHub links |

#### Subcategory Organization (100+ Subcategories)

Azure RM organizes resources by Azure service domain:
- AAD B2C, API Management, Active Directory Domain Services
- App Configuration, App Service (Web Apps), Application Insights
- Compute, Container, Container Apps, CosmosDB
- Database, DNS, Key Vault, Load Balancer
- Machine Learning, Monitor, Network, Storage
- And 80+ more service-specific categories

**Best Practice**: Group resources by service/domain, not alphabetically.

#### Dedicated Sections

| Section | Purpose |
|---------|---------|
| **Guides** | Authentication guides, migration guides, best practices |
| **Functions** | Provider-defined functions with clear signatures |
| **Resources** | Organized by subcategory with clear naming |
| **Data Sources** | Mirror resource organization patterns |

#### Resource Documentation Structure (Gold Standard)

From `azurerm_resource_group`:

```
1. Title: "azurerm_resource_group" (clean heading)
2. Description: "Manages a Resource Group." (concise)
3. Note Callouts: Multiple warnings about behavior
   - Azure automatic deletion warning
   - Feature toggle documentation with linked guide
4. Example Usage: Complete, copyable HCL code
5. Arguments Reference:
   - Linked argument names for anchor navigation
   - (Required)/(Optional) markers
   - "Changing this forces a new X" warnings
6. Attributes Reference: Exported attributes list
7. Timeouts: CRUD operation timeouts with defaults
   - create (90 minutes)
   - read (5 minutes)
   - update (90 minutes)
   - delete (90 minutes)
8. Import: Clear import command with example ID format
9. ON THIS PAGE: Sidebar navigation for long pages
10. Report an issue: Direct GitHub link
```

### Gold Standard Quality Checklist

Use this checklist when evaluating any provider against the Azure RM gold standard:

#### Provider-Level Quality
- [ ] **Index page** links to official service documentation
- [ ] **Guides section** exists with authentication/setup guides
- [ ] **Functions section** (if provider has functions)
- [ ] **Subcategories** group resources by service domain
- [ ] **100+ subcategories** for large providers (proportional to resource count)
- [ ] **Issue reporting** section with GitHub links
- [ ] **Changelog** reference or link

#### Resource Documentation Quality
- [ ] **Title** is clean resource name (no redundant text)
- [ ] **Description** is concise (one sentence)
- [ ] **Note callouts** for important warnings/behavior
- [ ] **Links within notes** to related guides
- [ ] **Example Usage** is complete and copyable
- [ ] **Arguments Reference** has linked argument names
- [ ] **Required/Optional** markers on all arguments
- [ ] **Force new** warnings where applicable
- [ ] **Attributes Reference** section present
- [ ] **Timeouts section** with CRUD defaults
- [ ] **Import section** with example command
- [ ] **ON THIS PAGE** sidebar navigation
- [ ] **Report an issue** link to GitHub

#### Navigation Quality
- [ ] **Version dropdown** works correctly
- [ ] **Search** function available in sidebar
- [ ] **Breadcrumb** navigation present
- [ ] **Subcategory collapse/expand** works properly

### Comparing Against Gold Standard

To evaluate a provider against Azure RM:

```
1. Navigate to target provider
2. Open Azure RM in second tab for comparison
3. Walk through Gold Standard Quality Checklist
4. Document gaps and differences
5. Score: (items met / total items) × 100%
```

**Quality Ratings**:
| Score | Rating | Interpretation |
|-------|--------|----------------|
| 90-100% | Excellent | Matches gold standard |
| 75-89% | Good | Minor improvements needed |
| 50-74% | Fair | Significant gaps exist |
| <50% | Needs Work | Major documentation effort required |

## Prerequisites

- Chrome DevTools MCP server connected
- Active browser session available
- Target provider URL (e.g., `https://registry.terraform.io/providers/robinmordasiewicz/f5xc/latest`)

## Workflow Overview

```
1. Navigate to Provider → Take snapshot → Identify UI elements
2. Check Versions     → Version dropdown → Compare available versions
3. Explore Docs       → Navigate menu → Inspect resources/data-sources
4. Find Source Code   → Locate GitHub link → Verify repository access
5. Validate Rendering → Check markdown → Identify formatting issues
```

## Phase 1: Initial Provider Navigation

### Navigate to Provider Page

```
Tool: mcp__chrome-devtools__navigate_page
Parameters:
  type: "url"
  url: "https://registry.terraform.io/providers/{org}/{provider}/latest"
```

Wait for page load:
```
Tool: mcp__chrome-devtools__wait_for
Parameters:
  text: "Documentation"
  timeout: 10000
```

### Take Initial Snapshot

Always take a snapshot first to understand the page structure:
```
Tool: mcp__chrome-devtools__take_snapshot
```

The snapshot reveals:
- Navigation elements with UIDs for interaction
- Current version displayed
- Documentation menu structure
- Links to resources, data-sources, functions, guides

## Phase 2: Version Investigation

### Terraform Registry Version Dropdown

The version dropdown is located in the provider header area. Look for elements like:
- `combobox` with version number text
- Elements labeled with semver patterns (e.g., "1.2.3", "0.1.0")

**Finding Version Selector:**

In the snapshot, identify:
```
- button/combobox containing current version (e.g., "0.0.15")
- Dropdown trigger near "Version" label
```

**Interacting with Version Dropdown:**
```
Tool: mcp__chrome-devtools__click
Parameters:
  uid: "<version-dropdown-uid>"
```

After clicking, take another snapshot to see available versions:
```
Tool: mcp__chrome-devtools__take_snapshot
```

**Version Selection Patterns:**
- Versions are listed in descending order (newest first)
- "latest" pseudo-version points to most recent release
- Each version is clickable to navigate to that version's documentation

### Verifying Latest Version

To check if the displayed version matches the actual latest:

1. Note the version shown in the dropdown
2. Compare with GitHub releases using:
```
Tool: mcp__chrome-devtools__navigate_page
Parameters:
  type: "url"
  url: "https://github.com/{org}/{repo}/releases/latest"
```

## Phase 3: Documentation Navigation

### Registry Documentation Structure

The Terraform Registry organizes documentation into these sections:

| Section | Location | Description |
|---------|----------|-------------|
| Overview | `index.md` | Provider introduction and configuration |
| Resources | `docs/resources/` | Managed resource documentation |
| Data Sources | `docs/data-sources/` | Read-only data source documentation |
| Functions | `docs/functions/` | Provider-defined function documentation |
| Guides | `docs/guides/` | How-to guides and tutorials |

### Navigation Menu Elements

In snapshots, look for:
```
navigation/tree elements:
  - "Resources" expandable section
  - "Data Sources" expandable section
  - "Functions" section (if available)
  - "Guides" section (if available)
  - Individual resource/data-source links
```

### Expanding Menu Sections

To expand a collapsed section:
```
Tool: mcp__chrome-devtools__click
Parameters:
  uid: "<resources-section-uid>"
```

### Navigating to Specific Resource

After expanding, click on the resource name:
```
Tool: mcp__chrome-devtools__click
Parameters:
  uid: "<resource-name-uid>"
```

### Subcategory Navigation

Large providers use subcategories to organize resources. Look for:
- Nested menu items under main sections
- Subcategory headers (e.g., "Compute", "Networking", "Storage")
- "Beta" and "Deprecated" subcategories at bottom of lists

## Phase 4: Source Code Discovery

### Finding GitHub Links

The Terraform Registry includes links to the provider's source repository. Look for:

1. **Header Area**: GitHub icon or "Source Code" link
2. **Repository Link**: Usually formatted as `github.com/{org}/{repo}`
3. **Report Issue Link**: Links to GitHub issues page

**Identifying Source Link in Snapshot:**
```
Look for:
  - link elements with "github.com" href
  - Elements with "Source" text
  - GitHub icon (octicon)
```

**Clicking Source Code Link:**
```
Tool: mcp__chrome-devtools__click
Parameters:
  uid: "<github-link-uid>"
```

### Verifying GitHub Repository

After navigating to GitHub:
```
Tool: mcp__chrome-devtools__take_snapshot
```

Check for:
- Repository name matches provider
- Latest release tag
- Documentation source in `docs/` directory

## Phase 5: Documentation Rendering Validation

### Key Markdown Elements to Inspect

The Registry renders markdown with specific patterns:

| Element | Registry Rendering | Source Format |
|---------|-------------------|---------------|
| Headings | Hierarchical structure | `# ## ###` |
| Code blocks | Syntax-highlighted HCL | ` ```hcl ``` ` |
| Tables | Bordered tables | Markdown pipe tables |
| Callouts | Colored boxes | `->`, `~>`, `!>` sigils |
| Links | Clickable references | `[text](url)` |

### Callout Rendering Patterns

Terraform Registry supports special callout syntax:

| Sigil | Rendering | Purpose |
|-------|-----------|---------|
| `->` | Blue "Note" box | General information |
| `~>` | Yellow "Note" box | Important warnings |
| `!>` | Red "Warning" box | Critical warnings |

### Checking Resource Documentation Structure

Navigate to a resource page and verify these sections exist:

1. **Title**: `# resource_name (Resource)` format
2. **Description**: Overview paragraph with service links
3. **Example Usage**: HCL code block with working example
4. **Argument Reference**: Table or list of arguments
5. **Attribute Reference**: Exported attributes list
6. **Import**: Import command example (if supported)

### Taking Screenshots for Visual Validation

```
Tool: mcp__chrome-devtools__take_screenshot
Parameters:
  format: "png"
  fullPage: true
  filePath: "./registry-docs-{resource}.png"
```

## Phase 6: Common Inspection Tasks

### Task: Check All Resources Are Documented

1. Navigate to provider page
2. Expand "Resources" section in navigation
3. Count listed resources
4. Compare with `docs/resources/` directory in source repo
5. Identify missing documentation

### Task: Validate Version Dropdown

1. Click version dropdown
2. Take snapshot to list all versions
3. Compare with GitHub releases
4. Check for version gaps or missing releases

### Task: Inspect Subcategory Organization

1. Navigate to provider page
2. Expand Resources and Data Sources sections
3. Identify subcategory groupings
4. Verify "Beta" and "Deprecated" are at bottom
5. Check for logical organization

### Task: Verify Import Documentation

1. Navigate to a resource page
2. Scroll to "Import" section
3. Verify import command syntax
4. Check resource identifier format

### Task: Check Example Usage Quality

1. Navigate to resource documentation
2. Locate "Example Usage" section
3. Verify code block has HCL syntax highlighting
4. Check example is complete and functional
5. Verify required arguments are shown

### Task: Gold Standard Comparison

Compare any provider against the Azure RM gold standard:

1. Open Azure RM in reference tab:
```
Tool: mcp__chrome-devtools__new_page
Parameters:
  url: "https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs"
```

2. Navigate to target provider in main tab
3. Walk through **Gold Standard Quality Checklist**:

**Provider-Level Assessment**:
```
- Index page quality
- Guides section presence
- Subcategory organization
- Issue reporting links
```

4. Select matching resources for comparison:
```
Azure RM: azurerm_resource_group
Target: {provider}_namespace (or equivalent base resource)
```

5. Compare resource documentation:
```
- Title format
- Description conciseness
- Note callouts present
- Example Usage quality
- Arguments Reference format
- Timeouts section
- Import section
```

6. Calculate quality score:
```
Score = (items met / total checklist items) × 100%
```

7. Document findings:
```
Strengths: [What matches gold standard]
Gaps: [What's missing or different]
Recommendations: [Specific improvements]
```

### Task: Timeouts Section Audit

Check if resource documentation includes timeout information:

1. Navigate to a resource page
2. Look for "Timeouts" section after "Attributes Reference"
3. Gold standard includes:
   - `create` - timeout for resource creation
   - `read` - timeout for resource reading
   - `update` - timeout for resource updates
   - `delete` - timeout for resource deletion
4. Each should have default values documented
5. Link to Terraform timeout configuration docs

## Troubleshooting

### Page Not Loading

```
Tool: mcp__chrome-devtools__navigate_page
Parameters:
  type: "reload"
  timeout: 30000
```

### Element Not Found in Snapshot

The Registry uses dynamic loading. Wait for content:
```
Tool: mcp__chrome-devtools__wait_for
Parameters:
  text: "<expected text>"
  timeout: 15000
```

### Version Dropdown Not Responding

The dropdown may require specific interaction patterns:
1. Take fresh snapshot
2. Identify exact clickable element
3. Try hover first, then click

### Navigation Menu Collapsed

Some sections require explicit expansion:
```
Tool: mcp__chrome-devtools__click
Parameters:
  uid: "<expand-button-uid>"
```

## Markdown Best Practices Reference

### Provider Index Page (`docs/index.md`)

```markdown
---
page_title: "Provider: {name}"
description: |-
  The {name} provider is used to interact with {service}.
---

# {Name} Provider

Brief description of what the provider does.

## Example Usage

` ` `hcl
provider "{name}" {
  # Configuration options
}
` ` `

## Authentication

How to configure authentication.

## Argument Reference

* `argument_name` - (Optional/Required) Description.
```

### Resource Documentation (`docs/resources/{name}.md`)

```markdown
---
page_title: "{provider}_{resource} Resource - {Provider}"
subcategory: "{Category}"  # Optional
description: |-
  Manages a {resource}.
---

# {provider}_{resource} (Resource)

Description of what this resource manages.

## Example Usage

` ` `hcl
resource "{provider}_{resource}" "example" {
  name = "example"
  # Required and common arguments
}
` ` `

## Argument Reference

The following arguments are supported:

* `name` - (Required) The name of the resource.
* `optional_arg` - (Optional) Description. Defaults to `value`.

## Attribute Reference

In addition to all arguments above, the following attributes are exported:

* `id` - The ID of the resource.
* `computed_attr` - Description of computed attribute.

## Import

{resource} can be imported using the `id`:

` ` `shell
terraform import {provider}_{resource}.example 12345
` ` `
```

### Data Source Documentation (`docs/data-sources/{name}.md`)

```markdown
---
page_title: "{provider}_{data_source} Data Source - {Provider}"
subcategory: "{Category}"  # Optional
description: |-
  Reads a {data_source}.
---

# {provider}_{data_source} (Data Source)

Use this data source to read information about {thing}.

## Example Usage

` ` `hcl
data "{provider}_{data_source}" "example" {
  name = "example"
}
` ` `

## Argument Reference

* `name` - (Required) The name to look up.

## Attribute Reference

* `id` - The ID of the {thing}.
* `attribute` - Description.
```

### Function Documentation (`docs/functions/{name}.md`)

```markdown
---
page_title: "{name} Function - {Provider}"
description: |-
  {Brief description}
---

# Function: {name}

Description of what the function does.

## Signature

` ` `text
{name}(arg1 type, arg2 type) return_type
` ` `

## Arguments

1. `arg1` (Type) - Description
2. `arg2` (Type) - Description

## Return Value

Description of return value.

## Example Usage

` ` `hcl
output "result" {
  value = provider::{provider}::{name}(arg1, arg2)
}
` ` `
```

## Registry URL Patterns

| URL Pattern | Purpose |
|-------------|---------|
| `/providers/{org}/{name}/latest` | Latest version overview |
| `/providers/{org}/{name}/{version}` | Specific version |
| `/providers/{org}/{name}/latest/docs` | Documentation index |
| `/providers/{org}/{name}/latest/docs/resources/{resource}` | Resource docs |
| `/providers/{org}/{name}/latest/docs/data-sources/{ds}` | Data source docs |
| `/providers/{org}/{name}/latest/docs/functions/{fn}` | Function docs |
| `/providers/{org}/{name}/latest/docs/guides/{guide}` | Guide docs |

## Quick Reference Commands

| Action | Tool | Key Parameters |
|--------|------|----------------|
| Navigate to URL | `navigate_page` | `type: "url", url: "..."` |
| Take snapshot | `take_snapshot` | - |
| Click element | `click` | `uid: "..."` |
| Wait for text | `wait_for` | `text: "...", timeout: N` |
| Take screenshot | `take_screenshot` | `filePath: "..."` |
| Go back | `navigate_page` | `type: "back"` |
| Reload page | `navigate_page` | `type: "reload"` |
| Fill input | `fill` | `uid: "...", value: "..."` |
| List pages/tabs | `list_pages` | - |

## Example Investigation Session

```
# 1. Start investigation
navigate_page → registry.terraform.io/providers/robinmordasiewicz/f5xc/latest
wait_for → "Documentation"
take_snapshot → Review structure

# 2. Check version
click → version dropdown uid
take_snapshot → List available versions
Verify latest matches expectations

# 3. Explore resources
click → "Resources" navigation section
take_snapshot → List all resources
click → specific resource
take_snapshot → Review resource documentation structure

# 4. Check markdown rendering
Verify: title format, example code, argument table, attributes
take_screenshot → Document any rendering issues

# 5. Find source code
click → GitHub link
take_snapshot → Verify repository
navigate_page → back to Registry

# 6. Document findings
Create report with:
- Version availability
- Resource documentation completeness
- Rendering quality assessment
- Issues found
```

## Example Gold Standard Comparison Session

```
# 1. Open Azure RM gold standard reference
new_page → registry.terraform.io/providers/hashicorp/azurerm/latest/docs
wait_for → "Authentication"
take_snapshot → Note gold standard structure

# 2. Navigate to gold standard resource
click → "Base" subcategory
click → "azurerm_resource_group"
take_snapshot → Document gold standard resource structure
Note: Title, Description, Notes, Example, Args, Attrs, Timeouts, Import

# 3. Switch to target provider tab
list_pages → Identify tabs
select_page → Target provider tab

# 4. Navigate to equivalent resource
click → "Namespaces" or base subcategory
click → "{provider}_namespace"
take_snapshot → Compare against gold standard

# 5. Run quality checklist
Compare each element:
□ Title format matches gold standard?
□ Description is concise?
□ Note callouts present for warnings?
□ Example Usage complete and copyable?
□ Arguments Reference has linked names?
□ Required/Optional markers present?
□ Attributes Reference section exists?
□ Timeouts section with CRUD defaults?
□ Import section with example?
□ ON THIS PAGE sidebar navigation?

# 6. Calculate and document score
Score: (checked items / 10) × 100%
Rating: Excellent (90%+) | Good (75-89%) | Fair (50-74%) | Needs Work (<50%)

# 7. Generate improvement report
Strengths:
- [List matching elements]
Gaps:
- [List missing elements]
Recommendations:
- [Specific actionable improvements]
```

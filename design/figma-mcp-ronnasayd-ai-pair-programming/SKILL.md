---
name: figma-mcp
description: Provides instructions and workflows for using the Figma MCP (Model-Context-Protocol) server to interact with Figma and FigJam. Use this skill to generate designs from web interfaces, extract design context, manage design systems, and create diagrams.
metadata:
  author: Ronnasayd Machado - github.com/Ronnasayd
  version: "1.0.0"
---

# Figma MCP Skill

## Overview

This skill provides a comprehensive guide for using the tools available through the Figma MCP (Model-Context-Protocol) server. It enables the agent to interact directly with Figma and FigJam, bridging the gap between design and development workflows.

Use this skill to:

- Generate Figma designs from live web interfaces.
- Extract design tokens, styles, and context from Figma layers.
- Create and manage Code Connect mappings.
- Generate FigJam diagrams from textual descriptions.
- Inspect large design files efficiently.

## Prerequisites

- **Figma MCP Server:** The Figma MCP server must be connected and accessible. Before using any Figma tools, verify the connection. If the tools are not available, guide the user to enable the server within their Figma plugin or IDE extension and restart their MCP client if necessary.

## Available Tools

The Figma MCP server exposes the following tools. Refer to the specific workflows below for detailed usage instructions.

- **`generate_figma_design`**: (Remote only) Generates design layers from web interfaces into Figma.
- **`get_design_context`**: Retrieves design context (e.g., CSS, React, Tailwind) for a selection.
- **`get_variable_defs`**: Returns variables and styles (colors, spacing, typography) from a selection.
- **`get_code_connect_map`**: Retrieves existing Code Connect mappings.
- **`add_code_connect_map`**: Manually adds a Code Connect mapping.
- **`get_screenshot`**: Takes a screenshot of a selection.
- **`create_design_system_rules`**: Creates a rule file for design-to-code translation.
- **`get_metadata`**: Returns a sparse XML representation of large designs.
- **`get_figjam`**: Converts FigJam diagrams to XML metadata.
- **`generate_diagram`**: Generates FigJam diagrams from Mermaid syntax.
- **`whoami`**: (Remote only) Returns the authenticated user's identity.
- **`get_code_connect_suggestions`**: Suggests mappings for Code Connect.
- **`send_code_connect_mappings`**: Confirms and sends Code Connect mappings.

## Workflows and Examples

### Workflow: Generating Figma Designs from a Web UI

This workflow uses the `generate_figma_design` tool to capture a web interface and import it as layers into a Figma file.

**Goal:** Convert a running web application's UI into an editable Figma design.

**Steps:**

1.  **Identify the Target URL:** Ask the user for the URL of the web page they want to capture. This can be a local development server (`http://localhost:3000`) or a live website.
2.  **Choose Destination:** Ask the user whether they want to create a new Figma file, update an existing one, or copy the design to the clipboard.
3.  **Execute the Tool:** Call `generate_figma_design` with the appropriate parameters.

**Example:**

- **User:** "Capture the UI of my local app at `http://localhost:5173` and create a new Figma file from it."
- **Action:**
  ```
  generate_figma_design(url="http://localhost:5173", file_destination="new_file")
  ```
- **Result:** The tool will open the URL, capture the DOM and styles, and create a new Figma file with the converted layers. A link to the new file is returned.

### Workflow: Extracting Design Context

This workflow uses `get_design_context` to get style information (e.g., CSS, React+Tailwind) for a selected Figma layer.

**Goal:** Get the code representation of a Figma component's styling.

**Steps:**

1.  **Get Figma URL:** The user must provide a Figma URL with a `node-id` pointing to the desired layer.
2.  **Customize Output (Optional):** Ask the user if they need the context in a specific format (e.g., Vue, vanilla CSS). The default is React with Tailwind CSS.
3.  **Execute the Tool:** Call `get_design_context` with the `fileKey` and `nodeId` from the URL.

**Example:**

- **User:** "Get the Vue component code for this button: `https://figma.com/design/file123/my-app?node-id=10-25`"
- **Action:**
  1.  Parse the URL to get `fileKey="file123"` and `nodeId="10:25"`. Remember to convert the node ID from `10-25` to `10:25`.
  2.  Call the tool with the customization prompt.
  ```
  get_design_context(fileKey="file123", nodeId="10:25", prompt="generate my Figma selection in Vue")
  ```
- **Result:** The tool returns a string containing the Vue component code corresponding to the selected Figma layer.

### Workflow: Generating a FigJam Diagram

This workflow uses `generate_diagram` to create a FigJam diagram from a textual description or Mermaid syntax.

**Goal:** Quickly create a flowchart, sequence, or other diagram in FigJam.

**Steps:**

1.  **Understand the Diagram:** Ask the user what kind of diagram they want to create (e.g., flowchart, sequence diagram) and for the content or logic it should represent.
2.  **Formulate Mermaid Syntax:** Convert the user's description into the appropriate Mermaid syntax.
3.  **Execute the Tool:** Call `generate_diagram` with the specified `diagramType` and the `source` code.

**Example:**

- **User:** "Create a sequence diagram showing a user logging into a website."
- **Action:**
  1.  Formulate the Mermaid syntax for a login sequence.
      ```mermaid
      sequenceDiagram
          participant User
          participant Browser
          participant Server
          User->>Browser: Enters credentials and clicks login
          Browser->>Server: POST /login (username, password)
          Server-->>Browser: Returns session cookie
          Browser->>User: Renders logged-in dashboard
      ```
  2.  Call the tool.
  ```
  generate_diagram(
      diagramType="sequence",
      source="sequenceDiagram
  participant User
  participant Browser
  participant Server
  User->>Browser: Enters credentials and clicks login
  Browser->>Server: POST /login (username, password)
  Server-->>Browser: Returns session cookie
  Browser->>User: Renders logged-in dashboard"
  )
  ```
- **Result:** The tool generates an interactive sequence diagram in FigJam and returns a link to it.

## Additional Resources

For more detailed information on each tool and its parameters, refer to the official documentation.

- [Figma MCP Server Tools and Prompts](https://developers.figma.com/docs/figma-mcp-server/tools-and-prompts/)
- [Code Connect Documentation](https://help.figma.com/hc/en-us/articles/23920389749655-Code-Connect)

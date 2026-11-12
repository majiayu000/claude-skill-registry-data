---
name: ak-mintlify
description: "Build and maintain Mintlify docs sites: docs.json, MDX components, navigation, frontmatter, theming, OpenAPI/AsyncAPI, llms.txt, skill.md and deployment."
when_to_use: "Invoke for site structure work or local validation CLI checks."
category: engineering
keywords: [docs-site, API-docs, MDX, Mintlify]
license: Proprietary
argument-hint: "[task] [path]"
metadata:
  author: agentkit
  version: "2.0.1"
---

# Mintlify Documentation Builder

Mintlify is a modern documentation platform that transforms Markdown/MDX files into beautiful, interactive documentation sites.

## Route the change

Inspect the existing documentation root, package manifest/lockfile, configuration
and navigation before choosing a command. Use the installed CLI version/help and
version-matched official docs for changing configuration or APIs. Do not install
a global CLI or initialize a site merely to edit MDX.

- Configuration/theme: load `references/docs-json-configuration-reference.md`.
- Content: load `references/mdx-components-reference.md`.
- Navigation: load `references/navigation-structure-and-organization-reference.md`.
- OpenAPI: load `references/api-documentation-components-reference.md`.
- Preview/deploy: load `references/deployment-and-continuous-integration-reference.md`.
- AI integration: load `references/ai-features-and-integrations-reference.md`.

Run the relevant installed validation command, check affected navigation/links,
and inspect rendered content when layout changes. Reuse a running preview for
this project; record the command/PID/port of any process started and stop it when
the task ends. Deployment requires the requested target and actual result evidence.

## Reference Files

- `references/docs-json-configuration-reference.md` - Complete docs.json configuration
- `references/mdx-components-reference.md` - All 26+ MDX components
- `references/api-documentation-components-reference.md` - API docs and OpenAPI integration
- `references/navigation-structure-and-organization-reference.md` - Navigation patterns
- `references/deployment-and-continuous-integration-reference.md` - Deployment and CI/CD
- `references/ai-features-and-integrations-reference.md` - AI assistant, llms.txt, MCP

## Examples

Load `references/quick-examples.md` only when starting new content/configuration.

## Resources

- Official docs: https://mintlify.com/docs
- GitHub: https://github.com/mintlify
- Community: Discord server for support

---
name: blog-fact-checking
description: |
  Verify claims against referenced sources. Checks if blog content accurately represents external resources, APIs, or documentation.
  Trigger phrases: "fact check", "verify", "check claims", "verify claims", "check sources", "verify sources"
allowed-tools: Read, WebFetch
---

# Fact Checking

## What to Verify
- Claims about external tools/libraries
- Version numbers and API details
- Quotes and attributions
- Technical specifications
- Links match what's claimed in text
- **Configuration examples** (file paths, formats, options)
- **Performance claims** (optimization suggestions, benchmark numbers)

## Process

1. **User directs what to check**
   - "Check the Redis claim in paragraph 3"
   - "Verify the Vagrant version requirements"
   - "Is the systemd behavior I described accurate?"

2. **Fetch the source**
   - Use `web_fetch` to get referenced documentation
   - Read official docs, not secondary sources when possible

3. **Compare claim vs source**
   - Does the claim match what the source says?
   - Is version information current?
   - Are quotes/code examples accurate?

4. **Report findings**
   - ✅ Verified: matches source
   - ⚠️ Outdated: source has changed
   - ❌ Mismatch: claim doesn't match source
   - 🚨 Hallucinated: config format/option doesn't exist in docs

## Configuration Examples - Special Scrutiny

**CRITICAL**: Configuration examples are high-risk for hallucination. Before approving any config:

1. **Verify the file path exists in official docs**
   - `.tool-name/config.yml` - does this file format exist?
   - `config/settings.json` - is this the documented path?

2. **Verify the configuration options**
   - Are the option names exactly as documented?
   - Are the data types correct (array vs object vs string)?
   - Are nested paths correct?

3. **Check for deprecated formats**
   - Has the config format changed in recent versions?
   - Are we showing old patterns that no longer work?

4. **Common hallucination patterns to watch for:**
   - Inventing `.hidden-dir/config.yml` files
   - Creating YAML configs when tool uses TOML or JSON
   - Mixing up config locations (LSP `init_options` vs separate config files)
   - Assuming config file exists because directory exists (e.g., `.ruby-lsp/` ≠ `.ruby-lsp/config.yml`)

**Red flags:**
- "You can configure X via `some/path.yml`" without a documentation link
- Config examples with TODO(@claude) markers still in them
- Performance claims without measurements ("this reduces time by 50%")

## Not Exhaustive
This is **targeted checking**, not an audit of every claim. User points to specific sections they want verified.

## Example Workflow

User: "Check if I got the LightDM systemd behavior right in the 'Display Manager Symlink' section"

Action:
1. Fetch systemd documentation on service types
2. Fetch LightDM documentation if available
3. Compare claim about "static" service type
4. Report: Verified/Mismatch/Unclear

## Response Format

```
**Checked**: LightDM systemd service behavior

✅ **Verified**: LightDM is indeed a "static" unit type requiring explicit symlink to display-manager.service

Source: systemd.unit(5) man page confirms static units cannot be enabled without symlinks.

**Note**: Minor point - the systemd docs use slightly different terminology but your explanation is accurate.
```

## Tools
- `web_fetch` for documentation
- Always cite sources checked
- Focus on technical accuracy, not writing style

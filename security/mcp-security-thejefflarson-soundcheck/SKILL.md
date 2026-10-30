---
name: mcp-security
description: Detects MCP tool handlers vulnerable to malicious inputs, hardcoded secrets,
  or unrestricted file/shell access. Use when writing MCP server definitions,
  tool schemas, or tool handler code. Also invoke when registering tools with
  Claude or building Claude Code extensions that expose file system, shell, or
  network access.
---

# MCP Server Security (OWASP LLM07:2025)

## What this checks

Prevents MCP tool handlers from being exploited via malicious inputs, hardcoded secrets,
unrestricted file access, or shell injection. A compromised MCP server gives attackers
direct access to the host environment.

## Vulnerable patterns

- MCP tool handler that opens or reads a file path supplied directly by the caller with no allowlist or root confinement
- Tool handler that runs a shell command built from tool input with shell expansion enabled
- Hardcoded API key, token, or credential in the handler body or tool definition
- Tool schema declaring a string parameter with no length cap, pattern, or enum constraint

## Fix immediately

Flag the vulnerable code and explain the risk. Then suggest a fix that establishes
these properties:

1. **Tool schemas constrain every string parameter** — maximum length, regex
   pattern, enumerated values, or rejection of additional properties. A bare
   string type is a blank check. The schema is the first line of defense because
   the model generated the input.
2. **Paths are canonicalized and confined to an allowed root.** The handler
   resolves the supplied filename against a fixed base directory and verifies the
   result stays inside that directory — defeating traversal, symlink escape, and
   absolute paths.
3. **Shell execution uses argument lists, never a shell string with interpolated
   input.** If the tool must run a command, the command name comes from a static
   allowlist and arguments are passed as discrete argv elements.
4. **Secrets come from the environment or a secrets manager** — never hardcoded
   literals in the handler or tool definition. A leaked MCP server config should
   not leak credentials.
5. **Every invocation is audit-logged** with the tool name and sanitized inputs
   before the side-effect runs. For broader MCP tool design guidance, see the
   `insecure-plugin-design` skill.

Translate each principle to the MCP SDK and language of the audited handler. Use the
SDK's documented schema-validation, path-resolution, and process-execution APIs — do
not hand-roll equivalents.

## Verification

Confirm the response:

- [ ] No secrets hardcoded — all credentials loaded from environment variables or a secrets manager
- [ ] File paths resolved and confined to an allowed base directory
- [ ] Shell calls use argument lists, not a shell string with interpolated input
- [ ] Every schema string parameter has a length cap, pattern, or enum constraint

## References

- CWE-284 ([Improper Access Control](https://cwe.mitre.org/data/definitions/284.html))
- CWE-78 ([OS Command Injection](https://cwe.mitre.org/data/definitions/78.html))
- CWE-200 ([Exposure of Sensitive Information](https://cwe.mitre.org/data/definitions/200.html))
- [OWASP LLM07:2025 Insecure Plugin Design](https://genai.owasp.org/llmrisk/llm07-insecure-plugin-design/)

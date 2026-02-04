---
name: mcp-server-troubleshooting
description: Diagnoses and resolves common Model Context Protocol (MCP) server connection issues with OpenAI Agents SDK
---

# MCP Server Troubleshooting Skill

This skill helps diagnose and resolve common issues with Model Context Protocol (MCP) server connections in OpenAI Agents SDK.

## Purpose
- Identify common MCP connection problems
- Provide systematic troubleshooting steps
- Resolve authentication, network, and configuration issues
- Debug tool availability and communication problems

## Common Issues Addressed
1. **Connection failures** - Network timeouts, unreachable servers
2. **Authentication errors** - Token issues, invalid credentials
3. **Tool discovery problems** - Tools not appearing, listing failures
4. **Communication errors** - Request/response failures
5. **Performance issues** - Slow responses, timeouts
6. **Configuration problems** - Incorrect parameters, headers

## Troubleshooting Approach
1. **Identify the transport method** in use (Hosted, HTTP, SSE, stdio)
2. **Check basic connectivity** to the MCP server
3. **Verify authentication** credentials and tokens
4. **Validate server configuration** parameters
5. **Test tool listing** functionality
6. **Examine error messages** for specific details
7. **Review logs** for additional diagnostic information

## Diagnostic Commands
- Test server reachability
- Validate authentication tokens
- Check tool listing endpoints
- Verify headers and parameters
- Review timeout configurations

## Resolution Strategies
- Update authentication credentials
- Adjust timeout values
- Fix network configuration
- Correct server parameters
- Implement retry mechanisms
- Add proper error handling

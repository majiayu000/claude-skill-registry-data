---
name: Troubleshooting gpt-oss and vLLM Errors
description: Use when diagnosing openai_harmony.HarmonyError or gpt-oss tool calling issues with vLLM. Identifies error sources (vLLM server vs client), maps specific error messages to known GitHub issues, and provides configuration fixes for tool calling problems with gpt-oss models.
---

# Troubleshooting gpt-oss and vLLM Errors

## When to Use This Skill

Invoke this skill when you encounter:
- `openai_harmony.HarmonyError` messages in any context
- gpt-oss tool calling failures or unexpected behavior
- Token parsing errors with vLLM serving gpt-oss models
- Users asking about gpt-oss compatibility with frameworks like llama-stack

## Critical First Step: Identify Error Source

**IMPORTANT**: `openai_harmony.HarmonyError` messages originate from the **vLLM server**, NOT from client applications (like llama-stack, LangChain, etc.).

### Error Source Identification

1. **Check the error origin**:
   - If error contains `openai_harmony.HarmonyError`, it's from vLLM's serving layer
   - The client application is just reporting what vLLM returned
   - Do NOT search the client codebase for fixes

2. **Correct investigation path**:
   - Search vLLM GitHub issues and PRs
   - Check openai/harmony repository for parser issues
   - Review vLLM server configuration and startup flags
   - Examine HuggingFace model files (generation_config.json)

## Common Error Patterns

### Token Mismatch Errors

**Error Pattern**: `Unexpected token X while expecting start token Y`

**Example**: `Unexpected token 12606 while expecting start token 200006`

**Meaning**:
- vLLM expects special Harmony format control tokens
- Model is generating regular text tokens instead
- Token 12606 = "comment" (indicates model generating reasoning text instead of tool calls)

**Known Issues**:
- vLLM #22519: gpt-oss-20b tool_call token errors
- vLLM #22515: Same error, fixed by updating generation_config.json

**Fixes**:
1. Update model files from HuggingFace (see reference/model-updates.md)
2. Verify vLLM server flags for tool calling
3. Check generation_config.json EOS tokens

### Tool Calling Not Working

**Symptoms**:
- Model describes tools in text but doesn't call them
- Empty `tool_calls=[]` arrays
- Tool responses in wrong format

**Root Causes**:
1. Missing vLLM server flags
2. Outdated model configuration files
3. Configuration mismatch between client and server

**Configuration Requirements**:

vLLM server must be started with:
```bash
--tool-call-parser openai --enable-auto-tool-choice
```

For demo tool server:
```bash
--tool-server demo
```

For MCP tool servers:
```bash
--tool-server ip-1:port-1,ip-2:port-2
```

**Important**: Only `tool_choice='auto'` is supported.

## Investigation Workflow

1. **Identify the error message**:
   - Copy the exact error text
   - Note any token IDs mentioned

2. **Search vLLM GitHub**:
   - Use error text in issue search
   - Include "gpt-oss" and model size (20b/120b)
   - Check both open and closed issues

3. **Check model configuration**:
   - Verify generation_config.json is current
   - Compare against latest HuggingFace version
   - Look for recent commits that updated config

4. **Review server configuration**:
   - Check vLLM startup flags
   - Verify tool-call-parser settings
   - Confirm vLLM version compatibility

5. **Check vLLM version**:
   - Many tool calling issues resolved in recent vLLM releases
   - Update to latest version if encountering errors
   - Check vLLM changelog for gpt-oss-specific fixes

## Quick Reference

### Key Resources
- vLLM gpt-oss recipe: https://docs.vllm.ai/projects/recipes/en/latest/OpenAI/GPT-OSS.html
- Common issues: See reference/known-issues.md
- Model update procedure: See reference/model-updates.md

### Diagnostic Commands

Check vLLM server health:
```bash
curl http://localhost:8000/health
```

List available models:
```bash
curl http://localhost:8000/v1/models
```

Check vLLM version:
```bash
pip show vllm
```

## Progressive Disclosure

For detailed information:
- **Known GitHub issues**: See reference/known-issues.md
- **Model file updates**: See reference/model-updates.md
- **Tool calling configuration**: See reference/tool-calling-setup.md

## Validation Steps

After implementing fixes:
1. Test simple tool calling with single function
2. Verify Harmony format tokens in responses
3. Check for token mismatch errors in logs
4. Test multi-turn conversations with tools
5. Monitor for "unexpected token" errors

If errors persist:
- Update vLLM to latest version
- Check vLLM GitHub for recent fixes and PRs
- Try different model variant (120b vs 20b)
- Review vLLM logs for additional error context

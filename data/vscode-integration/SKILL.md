---
name: vscode_integration
description: Enables Mini-Agent to integrate directly with VS Code Chat API for seamless AI assistance
version: "1.0.0"
allowed_tools:
  - list_skills
  - get_skill
  - execute_with_resources
  - bash
  - file_operations
  - web_search
architecture_pattern: "Progressive disclosure through skill system"
integration_type: "Native Mini-Agent skill, not standalone extension"
---

# VS Code Integration Skill for Mini-Agent

## Skill Metadata
- **Name**: vscode_integration
- **Description**: Enables Mini-Agent to integrate directly with VS Code Chat API for seamless AI assistance
- **Allowed Tools**: ["list_skills", "get_skill", "execute_with_resources", "bash", "file_operations", "web_search"]
- **Architecture Pattern**: Progressive disclosure through skill system
- **Integration Type**: Native Mini-Agent skill, not standalone extension

## Overview

This skill enables Mini-Agent to provide AI assistance directly within VS Code's Chat interface using the Chat API. Instead of a separate extension, it integrates through Mini-Agent's native progressive skill system, leveraging the existing architecture patterns.

## Architecture Design

### Progressive Skill Implementation
Following Mini-Agent's intrinsic architecture:
```
Level 1: list_skills() → Discover VS Code integration skill
Level 2: get_skill() → Load full skill content and implementation
Level 3: execute_with_resources() → Provide Chat API integration
```

### Integration Pattern
- **Native Integration**: Uses Mini-Agent's existing skill system
- **Progressive Loading**: Follows established disclosure patterns
- **Context Preservation**: Leverages knowledge graph for persistent state
- **Tool Access**: All Mini-Agent tools available through skill

## Technical Implementation

### Skill Loading Flow
1. **Discovery**: `list_skills()` reveals VS Code integration available
2. **Content Load**: `get_skill()` provides Chat API integration details
3. **Execution**: `execute_with_resources()` activates Chat API support

### VS Code Chat API Integration
- **Chat Participant**: Registers as `@mini-agent` in VS Code Chat
- **Message Handling**: Processes chat requests through skill system
- **Tool Execution**: Routes tool calls through Mini-Agent's native system
- **Response Streaming**: Real-time updates to Chat interface

### Session Management
- **Context Tracking**: Uses Mini-Agent's knowledge graph for session state
- **Message History**: Leverages existing workspace intelligence
- **Tool Results**: Standardized through Mini-Agent's ToolResult interface

## Usage Patterns

### Chat Interaction
```bash
# Level 1: Discover VS Code integration
list_skills()

# Level 2: Load full Chat API integration
get_skill("vscode_integration")

# Level 3: Activate Chat API support
execute_with_resources("vscode_integration", mode="chat_api")
```

### Available Commands in VS Code Chat
- `@mini-agent explain this code` - Code explanation with context
- `@mini-agent generate test for function` - Test generation
- `@mini-agent refactor this code` - Code refactoring
- `@mini-agent search web for pattern` - Web search integration
- `@mini-agent use skill_name` - Direct skill execution

## Implementation Details

### Chat API Integration Script
```python
# Activates VS Code Chat API support through Mini-Agent skill system
async def activate_vscode_chat_api():
    # Register chat participant
    participant = vscode.chat.createChatParticipant('mini-agent', handle_chat_request)
    
    # Route through Mini-Agent's skill system
    async def handle_chat_request(request, context, stream, token):
        # Process request through Mini-Agent's architecture
        response = await route_to_mini_agent_skill_system(request.prompt)
        stream.markdown(response)
```

### Skill Integration Points
- **Skill Loader**: Uses existing skill loading infrastructure
- **Tool Registry**: Leverages Mini-Agent's tool ecosystem
- **Knowledge Graph**: Persistent context and session management
- **Workspace Intelligence**: Token management and context injection

## Advantages of This Approach

### Architecture Alignment
- **Native Integration**: Part of Mini-Agent's skill system, not external
- **Progressive Enhancement**: Follows established patterns
- **Context Preservation**: Uses knowledge graph for state management
- **Modular Design**: Clear separation through skill boundaries

### Technical Benefits
- **No Separate Extension**: Integrated through existing Mini-Agent
- **Unified Tool Access**: All tools available through Chat
- **Persistent Sessions**: Leverages existing session management
- **Quality Framework**: Uses fact-checking and validation

### User Experience
- **Seamless Integration**: Works within existing Mini-Agent workflows
- **Consistent Behavior**: Follows Mini-Agent interaction patterns
- **Full Tool Access**: Complete Mini-Agent functionality in Chat
- **Context Awareness**: Maintains workspace understanding

## Configuration

### Enable VS Code Integration
```python
# In Mini-Agent config or skill loading
skills_config = {
    "vscode_integration": {
        "enabled": True,
        "chat_participant": "@mini-agent",
        "auto_activate": True
    }
}
```

### Workspace Integration
```python
# Automatic activation when VS Code detected
if workspace.contains_vscode_config():
    activate_vscode_integration_skill()
```

## Error Handling

### Graceful Degradation
- **No VS Code**: Skill remains available but inactive
- **Chat API Missing**: Falls back to standard Mini-Agent usage
- **Tool Failures**: Uses existing error handling patterns
- **Session Issues**: Leverages Mini-Agent's session management

## Future Enhancement

### Roadmap
1. **Workspace Context**: Automatic file and project awareness
2. **Multi-Panel Support**: Integration with multiple Chat panels
3. **Custom Commands**: User-defined Chat shortcuts
4. **Performance Optimization**: Token and context management

### Integration Opportunities
- **exai-mcp-server**: Can extend Chat API to multi-tool systems
- **orchestrator**: Infrastructure Chat integration
- **External Tools**: Support for additional editor integrations

---

## Summary

This skill provides VS Code Chat API integration through Mini-Agent's native architecture, maintaining alignment with progressive skill loading, knowledge graph persistence, and modular design principles. It enables seamless AI assistance within VS Code while preserving Mini-Agent's core identity as a CLI/coder tool foundation.

**Status**: Ready for Level 2 implementation
**Confidence**: High - follows established patterns
**Next**: Load skill content and implement Chat API integration
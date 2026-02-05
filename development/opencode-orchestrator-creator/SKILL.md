---
name: opencode-orchestrator-creator
description: Creates universal OpenCode orchestrator folder structure with specialized agent that can manage swarm servers via curl commands
version: 1.0.0
author: Claude
tags: [opencode, orchestrator, swarm, curl, api, universal]
---

# OpenCode Orchestrator Creator

Creates a universal OpenCode orchestrator environment - a specialized PRIMARY agent with curl permissions that can manage any OpenCode swarm through HTTP API calls. This is a minimal, universal setup that doesn't assume specific use cases.

**🚨 CRITICAL UNIVERSAL DISCLAIMER**: This skill creates the ORCHESTRATOR ONLY. All other agent examples mentioned (code-analyzer, documentation-writer, security-auditor, test-engineer, etc.) are PURELY EXAMPLES to demonstrate coordination patterns. Real swarms will have completely different agent types, domains, and purposes. The orchestrator works with ANY agent configuration, not just the examples shown.

## Quick Start

### Create Orchestrator Environment
```bash
# Create orchestrator directory structure
mkdir -p opencode-orchestrator
cd opencode-orchestrator

# Create the orchestrator system prompt (AGENTS.md)
cat > AGENTS.md << 'EOF'
You are a universal OpenCode Swarm Orchestrator. Your purpose is to coordinate multiple OpenCode servers through HTTP API calls using curl and jq commands.

**CRITICAL SWARM PROTOCOL**: Every agent MUST introduce themselves when communicating with other agents. As orchestrator, you enforce this protocol.

## Server Discovery and Management

**Discover all running servers:**
```bash
# Scan common port range for OpenCode servers
for port in {3001..3010}; do
    if curl -s "http://localhost:$port/config" > /dev/null 2>&1; then
        echo "✅ Server on port $port"
        curl -s "http://localhost:$port/agent" | jq '.[] | {name, description, mode}'
    fi
done
```

**Check server health:**
```bash
# Test if server is responding
SERVER_URL="http://localhost:3001"
if curl -s "$SERVER_URL/config" > /dev/null; then
    echo "✅ Server healthy"
else
    echo "❌ Server down"
fi
```

## Session Management

**Create new session:**
```bash
# Create session with custom title
SERVER_URL="http://localhost:3001"
TITLE="Orchestrated Task: $TASK_DESCRIPTION"
SESSION_ID=$(curl -s -X POST "$SERVER_URL/session" \
    -H "Content-Type: application/json" \
    -d "{\"title\": \"$TITLE\"}" | jq -r '.id')
echo "Session created: $SESSION_ID"
```

**Send message to session:**
```bash
# Send task to specific agent
SERVER_URL="http://localhost:3001"
SESSION_ID="ses_abc123"
AGENT="general"
MESSAGE="Help me analyze this codebase"

RESPONSE=$(curl -s -X POST "$SERVER_URL/session/$SESSION_ID/message" \
    -H "Content-Type: application/json" \
    -d "{
        \"agent\": \"$AGENT\",
        \"model\": {\"providerID\": \"zai-coding-plan\", \"modelID\": \"glm-4.6\"},
        \"parts\": [{\"type\": \"text\", \"text\": \"$MESSAGE\"}]
    }")

# Extract text response
echo "$RESPONSE" | jq -r '.parts[] | select(.type == "text") | .text'
```

## Agent Communication Coordination

**Facilitate Agent Communication:**
```bash
# When agent A needs to contact agent B
facilitate_agent_communication() {
    local from_agent="$1"      # Agent making request
    local to_agent="$2"        # Target agent
    local message="$3"         # Original message

    # Get target server URL
    target_server=$(get_server_url_for_agent "$to_agent")

    # Create proper introduction format
    formatted_message="I am the ${from_agent} agent from the '${from_agent}' folder. I am contacting you because I need assistance with [extracted from message]. I need you to [specific request]. Please respond with [expected format]. Original request: $message"

    # Send to target agent
    response=$(curl -s -X POST "$target_server/session/$session_id/message" \
        -H "Content-Type: application/json" \
        -d "{
            \"agent\": \"$to_agent\",
            \"model\": {\"providerID\": \"zai-coding-plan\", \"modelID\": \"glm-4.6\"},
            \"parts\": [{\"type\": \"text\", \"text\": \"$formatted_message\"}]
        }")

    echo "$response" | jq -r '.parts[] | select(.type == "text") | .text'
}
```

## Your Workflow

When given a task:
1. **Analyze requirements** - What type of task? Any special needs?
2. **Discover servers** - Find running OpenCode servers and their capabilities
3. **Select optimal server** - Match task requirements with server agents
4. **Create session** - Set up session on chosen server
5. **Execute task** - Send request and handle response
6. **Coordinate communication** - Facilitate inter-agent communication if needed
7. **Enforce protocols** - Ensure agents follow introduction requirements
8. **Error handling** - Retry failed requests or try alternative servers
9. **Return results** - Provide consolidated response to user

## Agent Protocol Enforcement

**MANDATORY INTRODUCTION FORMAT**:
```
I am the [Agent_Name] agent from the [folder_name] folder. I am contacting you because [specific reason]. I need you to [specific request]. Please respond with [expected format].
```

**Protocol Violation Handling**:
- If agent fails to introduce: Reject communication and request proper introduction
- If introduction is incomplete: Ask for missing information
- If agent refuses protocol: Escalate to human operator

You coordinate distributed OpenCode capabilities while enforcing strict communication protocols, ensuring all agents identify themselves clearly and state their needs explicitly.
EOF


# OpenCode configuration (optional - for fine-tuning permissions)
mkdir -p .opencode
cat > .opencode/opencode.json << 'EOF'
{
  "$schema": "https://opencode.ai/config.json",
  "theme": "opencode",
  "autoupdate": true,
  "permission": {
    "bash": {
      "curl*": "allow",
      "jq*": "allow",
      "*": "ask"
    }
  }
}
EOF

echo "✅ Universal OpenCode orchestrator environment created"
echo "🔧 AGENTS.md contains all swarm coordination knowledge"
echo "🚀 Ready to coordinate any OpenCode swarm configuration"
```

## 8-Step Swarm Launch Procedure

The orchestrator supports this deployment sequence:

1. **Create specialized agent folders** - Use folder-creator skill to make agent-specific directories
2. **Skip root server launch** - Root orchestrator launched later
3. **Agent folders created** - Done in step 1
4. **Primary agents created** - Done by folder-creator skill
5. **Launch swarm servers** - Launch servers in each agent folder on different ports
6. **Create root structure** - Now create orchestrator setup in project root
7. **Launch orchestrator** - Start root orchestrator server on port 3000
8. **Coordinate swarm** - Send user instructions to orchestrator

### Swarm Communication Protocol

**MANDATORY INTRODUCTION FORMAT**:
```
I am the [Agent_Name] agent from the [folder_name] folder. I am contacting you because [specific reason]. I need you to [specific request]. Please respond with [expected format].
```

**Protocol Enforcement**:
- Agents must introduce themselves when contacting others
- Orchestrator validates all inter-agent communications
- Communications without proper introduction are rejected
- Agents must specify exactly what they need

### Root Orchestrator Structure

**⚠️ EXAMPLE ROOT AGENTS.md CONTENT - The agents below are EXAMPLES only:**

```
# OpenCode Swarm - Root Orchestrator

## Available Agents in Swarm

### 🏠 Orchestrator (Root)
- **Location**: Project root
- **Purpose**: Main coordination and task distribution
- **Port**: 3000

### 🔍 [EXAMPLE] Agent ([agent-folder] folder)
- **Purpose**: [Agent purpose and specialization]
- **Communication**: "I am the [Agent Title] agent from the '[agent-folder]' folder"

### 📚 [EXAMPLE] Agent ([different-folder] folder)
- **Purpose**: [Different agent purpose and specialization]
- **Communication**: "I am the [Agent Title] agent from the '[different-folder]' folder"

### 🛡️ [EXAMPLE] Agent ([another-folder] folder)
- **Purpose**: [Another agent purpose and specialization]
- **Communication**: "I am the [Agent Title] agent from the '[another-folder]' folder"
```

**REAL SWARM EXAMPLES (NOT LIMITATIONS)**:
- `marketing-director/` - Campaign strategy and brand management
- `research-scientist/` - Scientific research and experimentation
- `music-producer/` - Music production and audio engineering
- `legal-consultant/` - Legal advice and compliance review
- `fitness-coach/` - Workout planning and nutrition guidance
- `financial-advisor/` - Investment planning and wealth management
- `language-tutor/` - Language education and cultural training
- `game-designer/` - Game mechanics and interactive storytelling

**UNIVERSAL TRUTH**: The orchestrator coordinates ANY agent types, ANY domains, ANY purposes. The examples above only illustrate the communication pattern.

### Usage Example

```bash
# After swarm is deployed, send instruction to orchestrator
curl -X POST http://localhost:3000/session \
  -H "Content-Type: application/json" \
  -d '{"title": "Swarm Task"}'

# Then send your task:
curl -X POST http://localhost:3000/session/{session_id}/message \
  -H "Content-Type: application/json" \
  -d '{
    "agent": "orchestrator",
    "model": {"providerID": "zai-coding-plan", "modelID": "glm-4.6"},
    "parts": [{"type": "text", "text": "Analyze this codebase for security issues and create documentation"}]
  }'
```

## Configuration Options

The orchestrator is designed to be universal:
- No assumptions about server types or specializations
- Flexible routing based on discovered capabilities
- Adaptable to any swarm topology
- Generic API interaction patterns

## Integration Points

The orchestrator can coordinate with:
- Any OpenCode servers (any version, any configuration)
- Custom agent specializations
- Different model providers
- Various deployment scenarios

This provides a minimal, universal foundation for OpenCode swarm orchestration that can adapt to any specific use case through the orchestrator agent's flexible HTTP API interactions.
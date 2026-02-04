---
alwaysApply: false
---
# Cursor Internals Skill

## Purpose
Specialized knowledge of Cursor IDE's internal architecture, authentication system, API structure, and cursor-agent CLI behavior discovered through reverse engineering.

## When to Use
- Integrating with Cursor's backend API
- Understanding Cursor's authentication flow
- Discovering and testing API endpoints
- Troubleshooting authentication issues
- Finding protobuf message definitions
- Building tools that interact with Cursor's services
- Working with cursor-agent CLI

**Note:** For database operations, schema details, and complete data structures, see the **cursor-db skill**.

## Quick Start

### Authentication Overview
Cursor uses **Auth0 OAuth** for authentication with JWT bearer tokens.

**Key URLs**:
- Auth: `https://authentication.cursor.sh`
- API: `https://api2.cursor.sh`
- Telemetry: `https://api3.cursor.sh`

**Required Headers**:
```http
Authorization: Bearer <jwt_token>
Content-Type: application/json
X-Cursor-User-Id: auth0|user_<identifier>
X-Cursor-Client-Version: 2.0.69
```

### Capturing Your Token
Tokens are stored in-memory only, not on disk. Capture via HTTPS interception:

```bash
cd ~/Documents/github/blink/tools
./capture_cursor_auth.sh
```

Tool will guide you through:
1. Installing mitmproxy
2. Installing SSL certificate
3. Proxying Cursor traffic
4. Extracting token from logs

Token location after capture: `tools/.cursor_token` (git-ignored)

## Architecture Deep Dive

### Dual Protocol System

Cursor's API uses **two different protocols** depending on endpoint complexity:

#### 1. JSON Endpoints (Simple Queries)
Work with plain HTTP/JSON - accessible via curl/requests.

**Working Endpoints**:
- `/aiserver.v1.AiService/AvailableModels` - List 40+ AI models
- `/aiserver.v1.AiService/GetDefaultModel` - Get default model
- `/aiserver.v1.AiService/CheckFeaturesStatus` - Feature flags
- `/aiserver.v1.AiService/KnowledgeBaseList` - Knowledge bases
- `/aiserver.v1.AiService/CheckNumberConfig` - Usage quotas
- `/aiserver.v1.AiService/AvailableDocs` - Documentation sources

**Characteristics**:
- Accept: `application/json`
- Simple request/response
- POST method with empty body `{}`
- No streaming

#### 2. Protobuf Endpoints (Complex Operations)
Require Protocol Buffers encoding via gRPC.

**Endpoints** (Not accessible via plain JSON):
- `/aiserver.v1.AiService/GetCompletionStream` - Chat/completions
- `/aiserver.v1.ToolCallEventService/SubmitToolCallEvents` - Tool calls
- `/aiserver.v1.AnalyticsService/Batch` - Analytics
- `/aiserver.v1.AiService/CheckQueuePosition` - Queue status

**Characteristics**:
- Content-Type: `application/proto`
- Binary protobuf encoding
- Streaming support (SSE)
- Connect-RPC protocol
- User-Agent: `connect-es/1.6.1`

### Network Stack

```
Cursor IDE (Electron)
    ↓
connect-es (gRPC-Web Client)
    ↓ 
HTTP/2 + Protocol Buffers
    ↓
api2.cursor.sh (AWS us-east-1)
    ↓
AI Providers (Anthropic, OpenAI, etc.)
```

## Database

**For complete database documentation, see the [cursor-db skill](../cursor-db/SKILL.mdc).**

### Quick Reference

**Location:** `~/Library/Application Support/Cursor/User/globalStorage/state.vscdb`

**Key Patterns:**
- `composerData:{uuid}` - Chat metadata
- `bubbleId:{composer}:{uuid}` - Individual messages

**Important:** Database operations require understanding the complete 69+ field bubble structure. See cursor-db skill for:
- Complete schemas
- Required fields for IDE compatibility
- Query patterns
- Write best practices
- Troubleshooting guides

## Machine Identifiers

Cursor tracks three machine identifiers:

**Storage location**: `~/Library/Application Support/Cursor/User/storage.json`

**IDs**:
- `telemetry.machineId` - Machine identifier
- `telemetry.devDeviceId` - Device UUID
- `telemetry.macMachineId` - Mac-specific ID

**Extraction script**:
```bash
cd ~/Documents/github/blink/tools
python3 extract_cursor_auth.py
```

Output: `cursor_auth_data.json` with all IDs

## Authentication System

### Token Structure

**Format**: JWT (JSON Web Token)
**Algorithm**: HS256

**Payload**:
```json
{
  "sub": "auth0|user_<identifier>",
  "time": "timestamp",
  "randomness": "uuid",
  "exp": 1767531038,
  "iss": "https://authentication.cursor.sh",
  "scope": "openid profile email offline_access",
  "aud": "https://cursor.com",
  "type": "session"
}
```

**Expiration**: Typically 53-60 days

### Token Capture Process

1. **Install mitmproxy**: `brew install mitmproxy`
2. **Generate certificate**: Run mitmproxy once
3. **Install cert**: Add to macOS System Keychain
4. **Proxy Cursor**: Set `HTTP_PROXY` and `HTTPS_PROXY`
5. **Use Cursor**: Chat feature generates API calls
6. **Extract token**: From Authorization header in logs

**Automated script**: `tools/capture_cursor_auth.sh`

### Token Storage

**Local storage**:
- NOT in plain text files
- NOT in database
- NOT in keychain
- Only in memory during runtime

**After capture**:
- Stored in `tools/.cursor_token` (git-ignored)
- Use environment variables:
  ```bash
  export CURSOR_AUTH_TOKEN="$(cat tools/.cursor_token)"
  export CURSOR_USER_ID="auth0|user_<your_id>"
  ```

## Working with the API

### Python Example

```python
import requests
import os

class CursorAPI:
    def __init__(self):
        self.base_url = "https://api2.cursor.sh"
        self.token = os.getenv('CURSOR_AUTH_TOKEN')
        self.user_id = os.getenv('CURSOR_USER_ID')
        
    def _headers(self):
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "X-Cursor-User-Id": self.user_id,
            "X-Cursor-Client-Version": "2.0.69"
        }
    
    def list_models(self):
        """Get all available AI models"""
        response = requests.post(
            f"{self.base_url}/aiserver.v1.AiService/AvailableModels",
            headers=self._headers(),
            json={}
        )
        return response.json()
    
    def check_features(self):
        """Check enabled features"""
        response = requests.post(
            f"{self.base_url}/aiserver.v1.AiService/CheckFeaturesStatus",
            headers=self._headers(),
            json={}
        )
        return response.json()
    
    def get_quotas(self):
        """Check usage quotas"""
        response = requests.post(
            f"{self.base_url}/aiserver.v1.AiService/CheckNumberConfig",
            headers=self._headers(),
            json={}
        )
        return response.json()

# Usage
api = CursorAPI()
models = api.list_models()
print(f"Found {len(models['models'])} models")
```

## Available AI Models

Cursor provides access to 40+ AI models:

**Cursor's Own**:
- `composer-1` - Cursor's agentic coding model (200k context)
- `default` - General model

**Claude (Anthropic)** - 8+ variants:
- `claude-4.5-sonnet` - Latest model (200k context)
- `claude-4.5-sonnet-thinking` - With reasoning
- `claude-4.5-haiku` - Fast and cheap
- `claude-4.1-opus` - Most powerful
- Plus thinking and legacy variants

**GPT-5 (OpenAI)** - 15+ variants:
- `gpt-5` - Latest flagship
- `gpt-5-codex` - Coding specialist
- `gpt-5-codex-high` - High reasoning
- `gpt-5-fast` - Priority processing (2x cost)
- Multiple reasoning levels (low/medium/high)

**Reasoning Models**:
- `o3` - Deep reasoning
- `o3-pro` - Most complex reasoning

**Google**:
- `gemini-2.5-pro` - 1M context
- `gemini-2.5-flash` - Fast variant

**Others**:
- `grok-4` (xAI)
- `grok-code-fast-1` - Free during promo
- `deepseek-r1`, `deepseek-v3.1`
- `kimi-k2-instruct`

## Cursor-Agent CLI Deep Dive

### Understanding cursor-agent Behavior

**Installation:**
```bash
curl https://cursor.com/install -fsS | bash
```

**Command Types:**

1. **create-chat** - Generates chat ID only
```bash
cursor-agent create-chat
# Returns: uuid (e.g., 3f1a6a8c-58d1-4fbe-81f7-1ad946d9c84e)
# NOTE: Does NOT create database entry - entry created on first message
```

2. **Sending Messages** - Uses --resume flag
```bash
cursor-agent --print --force --resume <chat_id> "Your prompt"
# Automatically includes ALL chat history
# Writes both user and assistant messages to database
# Creates composerData entry if it doesn't exist
```

### Critical Discovery: Database Entry Creation

**Important:** `cursor-agent create-chat` ONLY generates a UUID. The actual database entry is created when:
1. First message is sent via cursor-agent
2. OR manually created via direct database write

**Implication for REST APIs:**
- After calling `/agent/create-chat`, the chat doesn't exist in database yet
- Sending a message to a "created" chat will fail with 404
- Solution: Auto-create composerData entry on first message if missing

**For complete database structure requirements and investigation tools, see the [cursor-db skill](../cursor-db/SKILL.mdc).**

## Quick Reference

### Environment Setup

```bash
# Set credentials
export CURSOR_AUTH_TOKEN="<your_token>"
export CURSOR_USER_ID="auth0|user_<your_id>"

# Or load from file
export CURSOR_AUTH_TOKEN="$(cat tools/.cursor_token)"
```

### API Call Template

```bash
curl -X POST https://api2.cursor.sh/aiserver.v1.AiService/<EndpointName> \
  -H "Authorization: Bearer $CURSOR_AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -H "X-Cursor-User-Id: $CURSOR_USER_ID" \
  -H "X-Cursor-Client-Version: 2.0.69" \
  -d '{}'
```


### Status Codes

- `200` - Success
- `401` - Unauthorized (bad token)
- `403` - Forbidden (expired token)
- `404` - Not found (or protobuf required, or chat doesn't exist)
- `429` - Rate limited
- `503` - Service unavailable

## Progressive Disclosure

### Basic (Start Here)
- Cursor uses OAuth/Auth0 authentication
- Two API types: JSON (simple) and Protobuf (chat)
- Token capture via mitmproxy
- 40+ AI models available

### Intermediate
- Connect-RPC protocol for protobuf
- SQLite database structure
- Machine identifiers
- Working code examples

### Advanced
- Protobuf definition discovery
- gRPC reflection attempts
- Binary traffic decoding
- Custom gRPC client implementation

## External Resources

- **Connect-RPC**: https://connectrpc.com/
- **Protocol Buffers**: https://protobuf.dev/
- **gRPC**: https://grpc.io/
- **mitmproxy**: https://mitmproxy.org/
- **Auth0**: https://auth0.com/docs

---
name: dify-tool-developer
description: Guide AI agents through Dify tool plugin development with mandatory documentation loading and direct CLI usage. Use when creating Dify tool plugins or extending Dify with custom tools.
---

# Dify Tool Plugin Developer

Guide AI agents through complete Dify tool plugin development using official documentation and direct CLI commands.

## When to Use This Skill

Activate this skill when user:
- Mentions "Dify plugin", "Dify tool", or "Dify development"
- Wants to create custom Dify functionality
- Needs to extend Dify with custom tools
- Asks about developing for Dify
- Wants to build API integrations for Dify


## Agent Responsibilities

**⚠️ IMPORTANT:** You (the AI agent) are responsible for:

- ✅ **Creating and editing all files** yourself (YAML, Python, etc.)
- ✅ **Running all CLI commands** directly
- ✅ **Implementing the code** based on loaded documentation
- ✅ **Testing the plugin** with remote debugging
- ✅ **Packaging the final .difypkg**

**DO NOT:**
- ❌ Just tell the user how to do these tasks
- ❌ Provide instructions without executing
- ❌ Guide the user to run commands themselves

**YOU execute everything.** The user provides requirements and confirms results.

## Critical Rule: MANDATORY Documentation Loading

⚠️ **BEFORE writing ANY code, you MUST load the referenced official documentation**

The Dify plugin framework has STRICT requirements:
- Exact Python class structures with specific method signatures
- Precise YAML formatting and required fields
- Strict import patterns that must be followed exactly
- Specific parameter handling conventions

**DO NOT guess, assume, or improvise.** ALWAYS fetch and read the official documentation first.

## Documentation Fetching

To fetch official Dify documentation, use curl:

```bash
curl -s https://docs.dify.ai/plugin-dev-en/[doc-filename].md
```

**Available Documentation** (see `references/doc-map.md` for complete details on what each contains):
- `0221-initialize-development-tools.md` - CLI installation and setup
- `0222-tool-plugin.md` - Complete tool plugin development guide
- `0222-debugging-logs.md` - Logging and debugging techniques  
- `0222-tool-oauth.md` - OAuth authentication implementation

**MANDATORY Loading Points:**
- Before Phase 2 (initialization): Load `0222-tool-plugin.md`
- Before Phase 3 (implementation): Re-load `0222-tool-plugin.md` (Developing section)
- If OAuth needed: Load `0222-tool-oauth.md`
- During debugging: Load `0222-debugging-logs.md`

## Development Workflow

Follow this 5-phase workflow in sequence. Do not skip phases or documentation loading.

### PHASE 1: Setup & Planning

**FIRST:** Load `references/doc-map.md` to understand the documentation structure

**Gather Requirements** - Ask the user:

1. "What functionality should this tool provide?"
2. "Does it need to call external APIs? If so, which APIs?"
3. "Does it require OAuth authentication? (e.g., GitHub, Google, Slack)"
4. "What inputs should users provide to this tool?"
5. "What outputs should the tool return?"

**Determine Requirements:**
- Tool name (lowercase, hyphens only)
- Tool functionality description
- Required permissions (network access, storage, etc.)
- OAuth requirement (yes/no)
- Python package dependencies (requests, etc.)
- External API endpoints

**Verify Dify CLI Installation:**

```bash
dify version
```

If the CLI is not installed or returns an error:
1. LOAD: `https://docs.dify.ai/plugin-dev-en/0221-initialize-development-tools.md`
2. Follow the installation instructions for the user's operating system
3. Verify installation with `dify version`

---


### Option 2: Use Helper Script (Recommended)

For automated installation, use the provided helper script:

```bash
python scripts/install_cli.py
```

This script will:
- Detect your operating system and architecture automatically
- Download the latest Dify CLI version from GitHub
- Make the binary executable
- Verify the installation

**Optional flags:**
```bash
# Install specific version
python scripts/install_cli.py --version 0.4.0

# Install to custom directory
python scripts/install_cli.py --path ~/bin

# Both
python scripts/install_cli.py --version 0.4.0 --path /usr/local/bin
```

The script provides:
- ✅ Automatic platform detection (macOS/Linux/Windows, AMD64/ARM64)
- ✅ Latest version detection from GitHub API
- ✅ Progress indicator during download
- ✅ Automatic executable permissions
- ✅ Installation verification
- ✅ PATH setup instructions




### PHASE 1.5: Load Required Documentation (MANDATORY)

**⚠️ BEFORE writing ANY code, load the specific documentation needed for the planned requirements.**

Based on the requirements gathered in Phase 1, determine which documentation to load:

#### Required Documentation (ALWAYS LOAD)

**1. Tool Plugin Guide (MANDATORY for all plugins):**
```bash
curl -s https://docs.dify.ai/plugin-dev-en/0222-tool-plugin.md
```

**Read sections:**
- File structure requirements
- YAML configuration syntax
- Tool class implementation patterns
- Parameter handling
- Message types

**2. Debugging Guide (MANDATORY for testing):**
```bash
curl -s https://docs.dify.ai/plugin-dev-en/0222-debugging-logs.md
```

#### Conditional Documentation (Load if needed)

**3. OAuth Guide (IF OAuth authentication required):**
```bash
curl -s https://docs.dify.ai/plugin-dev-en/0222-tool-oauth.md
```

Load this if the requirements include:
- GitHub integration
- Google services integration
- Slack integration
- Any OAuth-based authentication

**4. Initialize Tools (IF CLI not installed):**
```bash
curl -s https://docs.dify.ai/plugin-dev-en/0221-initialize-development-tools.md
```

#### How to Determine What to Load

Based on Phase 1 requirements:

| Requirement | Documentation to Load |
|-------------|----------------------|
| Basic tool functionality | tool-plugin.md (always) |
| API integration | tool-plugin.md + debugging-logs.md |
| OAuth authentication | tool-plugin.md + tool-oauth.md + debugging-logs.md |
| Complex logic | tool-plugin.md + debugging-logs.md + examples.md |
| CLI installation needed | initialize-development-tools.md |

**⚠️ DO NOT skip this phase.** Loading the wrong documentation or insufficient documentation will result in incorrect code with syntax errors.

**After loading, confirm:**
- [ ] Understand the exact YAML structure required
- [ ] Know the Tool class pattern to follow
- [ ] Clear on parameter handling methods
- [ ] Understand message types available
- [ ] Know OAuth implementation steps (if applicable)

**Only proceed to Phase 2 after loading and understanding the required documentation.**


### PHASE 2: Initialize Project

⚠️ **MANDATORY:** Load the tool-plugin.md documentation BEFORE proceeding

**Fetch Documentation:**
```bash
curl -s https://docs.dify.ai/plugin-dev-en/0222-tool-plugin.md
```

**Read These Sections:**
- "Prerequisites"
- "Creating a New Project"
- "Choosing Plugin Type and Template"

**Initialize the Plugin:**

Use the `dify plugin init` command with appropriate flags:

```bash
dify plugin init \
  --name "your-tool-name" \
  --author "author-name" \
  --description "Clear, concise tool description" \
  --category tool \
  --language python \
  --min-dify-version "1.9.0" \
  --allow-network \      # Include if API access needed
  --allow-storage \      # Include if storage needed
  --quick                 # Skip interactive prompts
```

**Available Permission Flags:**
- `--allow-network` - For external API calls
- `--allow-storage` - For persistent data storage
- `--allow-tool` - To invoke other Dify tools
- `--allow-llm` - To invoke language models
- `--storage-size <bytes>` - Specify storage limit

**Verify Project Structure:**

```bash
ls -la your-tool-name/
```

**Expected files and directories:**
- `manifest.yaml` - Plugin manifest configuration
- `provider/` - Provider definitions and credential validation
- `tools/` - Tool implementations (YAML + Python files)
- `main.py` - Plugin entry point
- `requirements.txt` - Python dependencies
- `.env.example` - Environment variables template

If any files are missing, re-run the init command or check for errors.

---

### PHASE 3: Implement Tool

⚠️ **MANDATORY:** Re-read the tool-plugin.md "Developing the Tool Plugin" section

This section contains CRITICAL information:
- Exact file structure requirements
- YAML syntax for `tools/*.yaml`
- Tool class structure for `tools/*.py`
- Parameter handling patterns
- Message type formats and usage
- Import statement patterns

**Fetch Documentation Again:**
```bash
curl -s https://docs.dify.ai/plugin-dev-en/0222-tool-plugin.md
# Focus on section "Developing the Tool Plugin"
```

**If OAuth is Required:**

⚠️ **MANDATORY:** Load the complete OAuth documentation

```bash
curl -s https://docs.dify.ai/plugin-dev-en/0222-tool-oauth.md
```

Read all sections:
- Background (OAuth flows explained)
- Define OAuth Schema in Provider Manifest
- Complete Required OAuth Methods in Tool Provider
- Access Tokens in Your Tools
- Specify the Correct Versions

---

**Implementation Steps:**

#### 1. Edit `tools/*.yaml`

Follow the exact YAML structure from the documentation:

```yaml
identity:
  name: tool-name                    # Must match filename
  author: author-name
  label:
    en_US: Tool Display Name
    zh_Hans: 工具显示名称           # Add i18n translations
    pt_BR: Nome de Exibição
    ja_JP: ツール表示名
description:
  human:
    en_US: Description for human users
    zh_Hans: 人类用户的描述
  llm: Detailed description for AI models to understand when to use this tool
parameters:
  - name: parameter_name
    type: string                     # string, number, boolean, file
    required: true                   # or false for optional
    label:
      en_US: Parameter Display Name
      zh_Hans: 参数显示名称
    human_description:
      en_US: Description for users
      zh_Hans: 用户描述
    llm_description: Detailed parameter description for AI models
    form: llm                        # llm (AI extracts) or form (UI config)

  # Add more parameters as needed

extra:
  python:
    source: tools/tool-name.py       # Must match Python filename
```

**Parameter Types:**
- `string` - Text input
- `number` - Numeric input
- `boolean` - True/false
- `file` - File upload

**Form Types:**
- `llm` - AI extracts from user input (recommended for conversational use)
- `form` - User configures in UI (for admin settings)

---

#### 2. Edit `tools/*.py`

Follow the exact Tool class pattern from the documentation:

```python
from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

class YourToolName(Tool):
    """
    Tool for [description of what this tool does]
    """

    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        """
        Invoke the tool with given parameters

        Args:
            tool_parameters: Dictionary of tool parameters

        Yields:
            ToolInvokeMessage: Messages to return to the user
        """
        try:
            # 1. Extract required parameters (use .get() with default)
            required_param = tool_parameters.get("param_name", "")

            # 2. Extract optional parameters (use .get() - returns None if missing)
            optional_param = tool_parameters.get("optional_param")

            # 3. Validate required parameters
            if not required_param:
                yield self.create_text_message("Error: Required parameter 'param_name' is missing.")
                return

            # 4. Implement your business logic here
            result = self._process_data(required_param, optional_param)

            # 5. Return results using appropriate message types

            # Text message (always visible to user)
            yield self.create_text_message(f"Result: {result}")

            # JSON message (structured data)
            yield self.create_json_message({
                "status": "success",
                "data": result
            })

            # Variable message (for workflow use)
            yield self.create_variable_message("result_variable", result)

            # Link message (clickable URLs)
            # yield self.create_link_message("https://example.com/result")

        except Exception as e:
            # Always include error handling
            yield self.create_text_message(f"Error: {str(e)}")

    def _process_data(self, required_param: str, optional_param: str = None) -> Any:
        """
        Helper method for business logic

        Args:
            required_param: Required input parameter
            optional_param: Optional input parameter

        Returns:
            Processed result
        """
        # Implement your logic here

        # Handle optional parameters
        if optional_param:
            result = f"Processed with both: {required_param}, {optional_param}"
        else:
            result = f"Processed with required only: {required_param}"

        return result
```

**⚠️ CRITICAL RULES FROM DOCUMENTATION:**

1. **ONE Tool class per `.py` file** - Multiple classes will cause errors
2. **Exact method signature:** `_invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]`
3. **Use `.get()` for parameters** - Prevents KeyError exceptions
4. **Return with `yield`** - Not `return`
5. **Import from correct modules** - Match documentation exactly

**Message Types Available:**
- `create_text_message(text)` - Display text to user
- `create_json_message(dict)` - Return structured data
- `create_link_message(url)` - Return clickable link
- `create_variable_message(name, value)` - Set workflow variable
- `create_blob_message(data, name)` - Return binary data/files

---

#### 3. Edit `provider/*.yaml`

Add the new tool to the provider's tool list:

```yaml
identity:
  author: author-name
  name: plugin-name
  label:
    en_US: Plugin Display Name
    zh_Hans: 插件显示名称
  description:
    en_US: Plugin description
    zh_Hans: 插件描述
  icon: icon.svg

# Only include if API keys or credentials are needed
credentials_for_provider:
  api_key:
    type: secret-input
    required: true
    label:
      en_US: API Key
      zh_Hans: API 密钥
    placeholder:
      en_US: Enter your API key
      zh_Hans: 输入您的 API 密钥
    help:
      en_US: Get your API key from https://example.com/api-keys
      zh_Hans: 从 https://example.com/api-keys 获取您的 API 密钥
    url: https://example.com/api-keys

tools:
  - tools/your-tool-name.yaml    # Add your tool here, it can be multiple tools in a single plugin

extra:
  python:
    source: provider/plugin-name.py
```

---

#### 4. Edit `provider/*.py`

If credentials are needed, implement validation:

```python
from typing import Any
from dify_plugin.entities.tool import ToolProviderCredentials

class YourPluginProvider:
    def _validate_credentials(self, credentials: dict[str, Any]) -> ToolProviderCredentials:
        """
        Validate provider credentials

        Args:
            credentials: Dictionary of credentials to validate

        Returns:
            ToolProviderCredentials object

        Raises:
            ToolProviderCredentialValidationError: If validation fails
        """
        try:
            # Extract credentials
            api_key = credentials.get("api_key")

            if not api_key:
                raise Exception("API key is required")

            # Validate by making a test API call
            # import requests
            # response = requests.get(
            #     "https://api.example.com/validate",
            #     headers={"Authorization": f"Bearer {api_key}"}
            # )
            # if response.status_code != 200:
            #     raise Exception("Invalid API key")

            return ToolProviderCredentials(credentials=credentials)

        except Exception as e:
            raise ToolProviderCredentialValidationError(str(e))
```

---

#### 5. Update `manifest.yaml`

Complete all internationalization fields and metadata:

```yaml
version: 0.0.1 # bump this for every new version 
type: plugin
author: author-name
name: plugin-name
label:
  en_US: Plugin Display Name
  zh_Hans: 插件显示名称
  pt_BR: Nome de Exibição do Plugin
  ja_JP: プラグイン表示名
description:
  en_US: Detailed description of what this plugin does
  zh_Hans: 该插件功能的详细描述
  pt_BR: Descrição detalhada do que este plugin faz
  ja_JP: このプラグインの機能の詳細な説明
icon: icon.svg
resource:
  memory: 268435456  # 256MB
  permission:
    network:
      enabled: true  # If API access needed
    storage:
      enabled: false
      size: 0
plugins:
  tools:
    - provider/plugin-name.yaml
meta:
  version: 0.0.1
  arch:
    - amd64
    - arm64
  runner:
    language: python
    version: "3.12"
    entrypoint: main
  minimum_dify_version: 1.9.0
created_at: 2025-11-04T00:00:00.000000+00:00
privacy: PRIVACY.md
```

---

#### 6. Update `requirements.txt`

Add any Python package dependencies:

```
dify_plugin>=0.0.1 # you must use the dify_plugin version that the CLI added when initialized. 
requests>=2.31.0
# Add other dependencies as needed
```

---

### PHASE 4: Test & Debug

**Load Debugging Documentation:**

```bash
curl -s https://docs.dify.ai/plugin-dev-en/0222-debugging-logs.md
```

**Add Logging to Your Tool:**

According to the documentation, add logging imports and setup:

```python
import logging
from dify_plugin.handlers import DifyPluginLogHandler

# Set up logging
logger = logging.getLogger(__name__)
logger.addHandler(DifyPluginLogHandler())

class YourTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        logger.info(f"Tool invoked with parameters: {tool_parameters}")

        # Your implementation...

        logger.debug(f"Processing result: {result}")

        yield self.create_text_message(result)
```


---

### PHASE 4.5: Remote Testing with Debug Key (MANDATORY Before Packaging)

**⚠️ DO NOT PACKAGE without completing this phase.**

This phase verifies the plugin works with a real Dify instance before distribution.

#### Objectives
- Test plugin with actual Dify remote host
- Verify functionality with debug key
- Catch integration issues before packaging
- Ensure proper logging and error handling

#### Prerequisites

**Load debugging documentation:**
```bash
curl -s https://docs.dify.ai/plugin-dev-en/0222-debugging-logs.md
```

#### Steps

**1. Request Dify Remote Connection Details**

ASK the user for remote testing connection:

```
"To test this plugin with your Dify instance, I need:"

1. REMOTE_INSTALL_URL - e.g., https://your-dify.com or http://localhost:5003
2. Port (if not default) - usually 5003
3. REMOTE_INSTALL_KEY - get from Dify instance developer settings

Do you have a Dify instance available for testing?
```


**If user doesn't have a Dify instance:**
- Explain they can use local Dify installation
- Guide to set up local Dify (if needed)
- Or note that testing will be limited to code validation only

**2. Configure Environment**

Create/update `.env` file with remote connection:

```bash
cd your-tool-directory

cat > .env << EOF
INSTALL_METHOD=remote
REMOTE_INSTALL_URL=debug.dify.ai:5003 # or user provided host
REMOTE_INSTALL_KEY=********-****-****-****-************
EOF
```

**3. Start Plugin in Debug Mode**

Run the plugin connected to remote host:

```bash
cd your-tool-directory
python -m main
```

**Expected console output:**
```
INFO: Plugin loaded successfully
INFO: Connected to Dify remote host: https://your-dify-instance.com
INFO: Registered tools: [tool-name]
INFO: Waiting for invocations...
```

**If errors appear:**
- Check DIFY_REMOTE_HOST is accessible
- Verify DIFY_DEBUG_KEY is correct
- Check network connectivity
- Review error messages carefully

**4. Test Tool Invocation from Dify**

**In Dify UI:**
1. Go to Tools section
2. Find your plugin (should appear automatically)
3. Try invoking the tool with test inputs
4. Observe results

**In console (watch logs):**
```
INFO: Tool invoked: your-tool-name
DEBUG: Parameters: {"param1": "value1"}
DEBUG: Processing...
DEBUG: API call successful
INFO: Returned result to Dify
```

**5. Test All Scenarios**

Run comprehensive tests:

**Test Case 1: Valid Input**
```
Input: Normal, expected parameters
Expected: Success, correct output
```

**Test Case 2: Missing Required Parameter**
```
Input: Omit required parameter
Expected: Error message, graceful handling
```

**Test Case 3: Invalid Input**
```
Input: Wrong type or format
Expected: Validation error, helpful message
```

**Test Case 4: API Integration (if applicable)**
```
Input: Valid request requiring API call
Expected: Successful API call, correct data returned
```

**Test Case 5: Error Conditions**
```
Input: Trigger expected errors (API timeout, invalid credentials, etc.)
Expected: Proper error handling, helpful messages
```

**Test Case 6: OAuth Flow (if applicable)**
```
Action: Complete OAuth authorization
Expected: Token received, API calls work with token
```

**Expected Output:**
- Plugin should start without errors
- You should see log output
- Tool should be ready to receive invocations
- Guide the user to test it in the dify environment while the debug script runs. 

**If Errors Occur:**

1. **LOAD** `references/troubleshooting.md`
2. Find the error pattern
3. Apply the documented solution
4. Re-test

**Common Errors:**

| Error | Cause | Solution |
|-------|-------|----------|
| `Multiple subclasses of Tool in file.py` | Multiple Tool classes in one file | Keep only one Tool class per .py file, move others to new files |
| `ImportError: cannot import name 'X'` | Import name doesn't match definition | Check spelling, case, underscores in import statements |
| `KeyError: 'parameter_name'` | Parameter accessed without checking | Use `.get()` method: `param = tool_parameters.get("name", "")` |
| `ToolProviderCredentialValidationError` | Credential validation failed | Check API key format, test API endpoint, verify credentials |

**Debug Checklist:**
- [ ] One Tool class per .py file
- [ ] Exact import statements from docs
- [ ] Using `.get()` for all parameters
- [ ] Method signature matches docs exactly
- [ ] YAML files have correct syntax
- [ ] All required fields present in YAML
- [ ] Credentials properly validated

---


**6. Verify Debug Logging**

**Check that logs show:**
- [ ] Tool invocation with parameters
- [ ] Processing steps
- [ ] API calls (without sensitive data)
- [ ] Results
- [ ] Any errors with context

**Example good logging:**
```python
logger.info(f"Tool invoked: {tool_name}")
logger.debug(f"Parameters: {tool_parameters}")
logger.debug("Calling API endpoint...")
logger.debug(f"API response status: {response.status_code}")
logger.info("Successfully processed request")
```

**7. Debug Issues**

**If tool doesn't work as expected:**

1. Check console logs for errors
2. Verify parameters are extracted correctly
3. Test API calls independently
4. Check credential validation
5. Load `references/troubleshooting.md` for common issues

**Common remote testing issues:**

| Issue | Cause | Solution |
|-------|-------|----------|
| Plugin doesn't appear | Registration failed | Check manifest.yaml, restart plugin |
| Connection refused | Wrong host URL | Verify DIFY_REMOTE_HOST |
| Unauthorized | Invalid debug key | Check DIFY_DEBUG_KEY |
| Tool fails | Parameter handling | Verify .get() usage, check logs |
| API errors | Credential issues | Test API key separately |

**8. User Confirmation**

**Before proceeding to packaging, ask user:**

```
"I've tested the plugin with your Dify instance. Results:

✅ Plugin loaded successfully
✅ Tool appears in Dify UI
✅ Test invocations working
✅ [List specific test results]

Does everything work as expected? Any issues or adjustments needed?"
```

**Wait for user confirmation before packaging.**

#

#### 4. Verify requirements.txt Contains Latest dify_plugin

**⚠️ CRITICAL CHECK:** Verify the dify_plugin version that CLI generated.

The Dify CLI always creates requirements.txt with the latest dify_plugin version.

```bash
cat your-tool-name/requirements.txt
```

**Check what version was generated:**
```
dify_plugin>=X.X.X
```

**DO NOT override this version.** The CLI uses the latest compatible version.

**Note the version for reference:**
- This is the version your plugin will use
- Keep this version in requirements.txt
- Only add additional dependencies you need

**Example:**
```
dify_plugin>=2.4.2    # Generated by CLI - KEEP THIS
requests>=2.31.0       # Add if you need requests
pyyaml>=6.0           # Add if you need yaml
```

### Success Criteria (All Must Pass)

- [ ] Plugin connects to remote Dify instance
- [ ] Debug key configured and accepted
- [ ] Tool appears in Dify UI
- [ ] Tool can be invoked successfully
- [ ] All test scenarios pass
- [ ] Logs show clean execution
- [ ] No errors in remote testing
- [ ] User confirms functionality correct
- [ ] Ready to package

**⚠️ If ANY criterion fails:**
- DO NOT proceed to packaging
- Debug the issue using troubleshooting.md
- Fix and re-test
- Only package when ALL tests pass

---
### PHASE 5: Package & Publish

**Load Packaging Documentation:**

```bash
curl -s https://docs.dify.ai/plugin-dev-en/0222-tool-plugin.md
# Read the "Packaging the Plugin" section
```

**Package the Plugin:**

```bash
dify plugin package ./your-tool-directory
```

This creates a `.difypkg` file in the current directory.

**Expected Output:**
```
✓ plugin packaged successfully, output path: your-tool-name.difypkg
```

**Verify Package:**

```bash
ls -lh *.difypkg
```

The file should exist and have a reasonable size (typically 10-100 KB for simple plugins).

**Publishing (Optional):**

If the user wants to publish to the Dify marketplace:

1. Visit the Dify plugin marketplace
2. Create an account if needed
3. Upload the `.difypkg` file
4. Fill in marketplace metadata
5. Submit for review

Guide the user through this process if requested.

---

## OAuth Implementation Guide

If the tool requires OAuth authentication (e.g., GitHub, Google, Slack):

⚠️ **MANDATORY:** Load the complete OAuth documentation BEFORE implementing

```bash
curl -s https://docs.dify.ai/plugin-dev-en/0222-tool-oauth.md
```

**OAuth Implementation Steps:**

1. **Define OAuth Schema in `provider/*.yaml`:**

```yaml
oauth_schema:
  client:
    - name: client_id
      type: string
      required: true
      label:
        en_US: Client ID
    - name: client_secret
      type: secret-input
      required: true
      label:
        en_US: Client Secret
  authorization:
    url: https://provider.com/oauth/authorize
    scopes:
      - scope1
      - scope2
  token:
    url: https://provider.com/oauth/token
```

2. **Implement OAuth Methods in `provider/*.py`:**

```python
def get_authorization_url(self, credentials: dict) -> str:
    """Return OAuth authorization URL"""
    pass

def validate_oauth_callback(self, credentials: dict, state: str, code: str) -> dict:
    """Exchange code for access token"""
    pass
```

3. **Access Tokens in Tools:**

```python
def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
    # Access token is available in runtime
    access_token = self.runtime.credentials.get("access_token")

    # Use token in API calls
    headers = {"Authorization": f"Bearer {access_token}"}
```

Refer to the OAuth documentation for complete implementation details.

---

## Best Practices (From Official Documentation)

**ALWAYS:**
- Load official documentation BEFORE writing any code
- Follow exact syntax and structure from the docs
- Use one Tool class per .py file
- Use `.get()` method for accessing parameters
- Include comprehensive error handling
- Add logging for debugging
- Test thoroughly before packaging
- Document all methods and classes
- Validate credentials properly

**NEVER:**
- Guess at syntax or structure
- Skip mandatory documentation loading
- Put multiple Tool classes in one file
- Access parameters without `.get()` or validation
- Use local file I/O operations (serverless environment constraint)
- Assume parameters exist without checking
- Package without testing first
- Skip error handling

**Security Considerations:**
- Always validate and sanitize user inputs
- Never log sensitive data (API keys, passwords)
- Use environment variables for credentials
- Validate credentials before use
- Handle API errors gracefully

---

## Progress Tracking

Throughout the development process, keep the user informed:

1. **Current Phase:** Tell the user which phase you're in
2. **Completed Steps:** Show what has been accomplished
3. **Next Actions:** Explain what will happen next
4. **User Input Needed:** Ask for clarification when needed
5. **Problems Encountered:** Report any issues and solutions

**Example Progress Update:**

```
✅ Phase 1 Complete: Requirements gathered
✅ Phase 2 Complete: Project initialized
🔄 Phase 3 In Progress: Implementing tool (60% done)
   ✅ YAML configuration complete
   ✅ Tool class structure created
   🔄 Adding API integration
   ⏳ Error handling pending
   ⏳ Logging setup pending
⏳ Phase 4 Pending: Testing & debugging
⏳ Phase 5 Pending: Packaging
```

---

## Reference Quick Access

Load these reference files when you need specific information:

- `references/doc-map.md` - Complete map of what each official doc contains
- `references/workflow.md` - Detailed 5-phase workflow
- `references/cli-commands.md` - Dify CLI command reference
- `references/troubleshooting.md` - Common errors and solutions
- `references/examples.md` - Real-world plugin examples

**Helper Script:**

Use the fetch script to quickly retrieve official docs:

```bash
bash scripts/fetch_doc.sh tool        # Fetch tool-plugin.md
bash scripts/fetch_doc.sh oauth       # Fetch tool-oauth.md
bash scripts/fetch_doc.sh debug       # Fetch debugging-logs.md
bash scripts/fetch_doc.sh init        # Fetch initialize-development-tools.md
```

---

## Summary

This skill guides you through a structured 5-phase workflow:

1. **Setup & Planning** - Gather requirements, verify CLI
2. **Initialize Project** - Create plugin structure with CLI
3. **Implement Tool** - Write YAML configs and Python code
4. **Test & Debug** - Run locally, fix issues, add logging
5. **Package & Publish** - Create .difypkg file, optionally publish

**Key Success Factors:**
- Always load documentation before coding
- Follow official patterns exactly
- Test thoroughly before packaging
- Handle errors gracefully
- Keep the user informed of progress

The result will be a production-ready Dify tool plugin that follows best practices and official guidelines.

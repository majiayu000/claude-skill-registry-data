---
name: skill-gemini-google-search-tool
description: Query Gemini with Google Search grounding
---

# When to use
- When you need real-time web information beyond the model's training cutoff
- When you need verifiable sources and citations for AI responses
- When you want to reduce hallucinations with Google Search grounding
- When building AI workflows that require up-to-date information

# Gemini Google Search Tool Skill

## Purpose

The gemini-google-search-tool is a Python CLI tool and library that connects Gemini AI models to real-time web content through Google Search grounding. It automatically determines when a search would improve answers, executes appropriate queries, and returns grounded responses with verifiable sources.

## When to Use This Skill

**Use this skill when:**
- You need to query Gemini with real-time web information
- You want automatic citations and source attribution
- You're building AI agents that need current information
- You need to verify AI responses against web sources
- You want to integrate Google Search grounding into workflows

**Do NOT use this skill for:**
- Static knowledge queries that don't need real-time data
- Tasks that don't require source attribution
- Offline-only environments (requires internet and API key)

## CLI Tool: gemini-google-search-tool

A professional CLI-first tool for querying Gemini with Google Search grounding, providing real-time web content with automatic citations.

### Installation

```bash
# Install from source
git clone https://github.com/dnvriend/gemini-google-search-tool.git
cd gemini-google-search-tool
uv tool install .

# Verify installation
gemini-google-search-tool --version
```

### Prerequisites

- Python 3.14 or higher
- [uv](https://github.com/astral-sh/uv) package manager
- Google Gemini API key ([get one free](https://aistudio.google.com/app/apikey))
- `GEMINI_API_KEY` environment variable

### Quick Start

```bash
# Set API key
export GEMINI_API_KEY='your-api-key-here'

# Basic query
gemini-google-search-tool query "Who won euro 2024?"

# With inline citations
gemini-google-search-tool query "Latest AI news" --add-citations

# Using pro model
gemini-google-search-tool query "Complex analysis" --pro
```

## Progressive Disclosure

<details>
<summary><strong>📖 Core Commands (Click to expand)</strong></summary>

### query - Query Gemini with Google Search Grounding

Query Gemini models with automatic Google Search grounding for real-time web information.

**Usage:**
```bash
gemini-google-search-tool query "PROMPT" [OPTIONS]
```

**Arguments:**
- `PROMPT`: The query prompt (positional, required unless `--stdin` is used)
- `--stdin` / `-s`: Read prompt from stdin (overrides PROMPT)
- `--add-citations`: Add inline citation links to response text
- `--pro`: Use gemini-2.5-pro model (default: gemini-2.5-flash)
- `--text` / `-t`: Output markdown format instead of JSON
- `-v/-vv/-vvv`: Verbosity levels (INFO/DEBUG/TRACE)

**Examples:**
```bash
# Basic query with JSON output
gemini-google-search-tool query "Who won euro 2024?"

# Query with inline citations
gemini-google-search-tool query "Latest AI developments" --add-citations

# Read from stdin
echo "Climate change updates" | gemini-google-search-tool query --stdin

# Markdown output
gemini-google-search-tool query "Quantum computing news" --text

# Pro model with verbose output
gemini-google-search-tool query "Complex analysis" --pro -vv

# Trace mode (shows HTTP requests)
gemini-google-search-tool query "Test" -vvv
```

**Output (JSON):**
```json
{
  "response_text": "AI-generated response with grounding...",
  "citations": [
    {"index": 1, "uri": "https://...", "title": "Source Title"},
    {"index": 2, "uri": "https://...", "title": "Another Source"}
  ],
  "grounding_metadata": {
    "web_search_queries": ["query1", "query2"],
    "grounding_chunks": [...],
    "grounding_supports": [...]
  }
}
```

**Output (Markdown with `--text`):**
```markdown
AI-generated response with grounding...

## Citations

1. [Source Title](https://...)
2. [Another Source](https://...)
```

---

### completion - Generate Shell Completion Scripts

Generate shell completion scripts for bash, zsh, or fish.

**Usage:**
```bash
gemini-google-search-tool completion {bash|zsh|fish}
```

**Arguments:**
- `SHELL`: Shell type (bash, zsh, or fish)

**Examples:**
```bash
# Generate and install bash completion
eval "$(gemini-google-search-tool completion bash)"

# Generate and install zsh completion
eval "$(gemini-google-search-tool completion zsh)"

# Install fish completion
mkdir -p ~/.config/fish/completions
gemini-google-search-tool completion fish > ~/.config/fish/completions/gemini-google-search-tool.fish

# Persistent installation (add to ~/.bashrc or ~/.zshrc)
echo 'eval "$(gemini-google-search-tool completion bash)"' >> ~/.bashrc
echo 'eval "$(gemini-google-search-tool completion zsh)"' >> ~/.zshrc
```

**Output:**
Shell-specific completion script to stdout.

</details>

<details>
<summary><strong>⚙️  Advanced Features (Click to expand)</strong></summary>

### Google Search Grounding

The tool uses Google Search grounding to connect Gemini to real-time web content:

1. **Automatic Search Decision**: Gemini determines if a search would improve the answer
2. **Query Generation**: Generates appropriate search queries automatically
3. **Result Processing**: Processes search results and synthesizes information
4. **Citation Generation**: Returns grounded responses with verifiable sources

**Benefits:**
- Reduces hallucinations by grounding responses in web content
- Provides up-to-date information beyond training cutoff
- Includes automatic citation links for verification
- Supports multi-query search for comprehensive coverage

### Model Selection

**gemini-2.5-flash (default):**
- Fast response times
- Cost-effective for high-volume queries
- Good for straightforward questions
- Recommended for most use cases

**gemini-2.5-pro (`--pro` flag):**
- More powerful reasoning capabilities
- Better for complex analysis
- Higher quality responses
- More expensive per query

### Verbosity Levels

**No flag (WARNING):**
- Only errors and warnings
- Clean JSON/text output

**`-v` (INFO):**
```
[INFO] Starting query command
[INFO] GeminiClient initialized successfully
[INFO] Querying with model 'gemini-2.5-flash' and Google Search grounding
[INFO] Query completed successfully
```

**`-vv` (DEBUG):**
```
[DEBUG] Validated prompt: Who won euro 2024?...
[DEBUG] Initializing GeminiClient
[DEBUG] Calling Gemini API: model=gemini-2.5-flash
[DEBUG] Extracted 7 citations
[DEBUG] Web search queries: ['who won euro 2024', 'Euro 2024 winner']
```

**`-vvv` (TRACE):**
```
[DEBUG] connect_tcp.started host='generativelanguage.googleapis.com' port=443
[DEBUG] start_tls.started ssl_context=<ssl.SSLContext...>
[DEBUG] send_request_headers.started request=<Request [b'POST']>
```

### Library Usage

The tool can also be used as a Python library:

```python
from gemini_google_search_tool import (
    GeminiClient,
    query_with_grounding,
    add_inline_citations,
)

# Initialize client
client = GeminiClient()  # Reads GEMINI_API_KEY from environment

# Query with grounding
response = query_with_grounding(
    client=client,
    prompt="Who won euro 2024?",
    model="gemini-2.5-flash",
)

# Access response
print(response.response_text)
print(f"Citations: {len(response.citations)}")

# Add inline citations
if response.grounding_segments:
    text_with_citations = add_inline_citations(
        response.response_text,
        response.grounding_segments,
        response.citations,
    )
    print(text_with_citations)
```

### Pipeline Integration

The tool follows CLI-first design principles for pipeline integration:

**JSON to stdout, logs to stderr:**
```bash
# Parse JSON output
gemini-google-search-tool query "test" | jq '.response_text'

# Filter citations
gemini-google-search-tool query "test" | jq '.citations[]'

# Check exit code
gemini-google-search-tool query "test" && echo "Success"
```

**Stdin support:**
```bash
# From file
cat question.txt | gemini-google-search-tool query --stdin

# From command output
echo "Who won euro 2024?" | gemini-google-search-tool query --stdin
```

</details>

<details>
<summary><strong>🔧 Troubleshooting (Click to expand)</strong></summary>

### Common Issues

**Issue: Missing API Key**
```bash
Error: GEMINI_API_KEY environment variable is required.
Set it with: export GEMINI_API_KEY='your-api-key'
```

**Solution:**
1. Get an API key from [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Set environment variable: `export GEMINI_API_KEY='your-key'`
3. Or add to shell profile: `echo 'export GEMINI_API_KEY="your-key"' >> ~/.bashrc`

---

**Issue: Empty or Invalid Response**
```bash
Error: Query failed: Invalid response format
```

**Solution:**
1. Check API key is valid
2. Verify internet connection
3. Try with verbose mode: `-vv` to see detailed error
4. Check Gemini API status page

---

**Issue: Rate Limiting**
```bash
Error: Query failed: Rate limit exceeded
```

**Solution:**
1. Wait and retry
2. Check API quota in Google AI Studio
3. Consider upgrading API tier for higher limits

---

**Issue: Module Import Error (Library Usage)**
```python
ImportError: No module named 'gemini_google_search_tool'
```

**Solution:**
1. Install package: `uv tool install .`
2. Or use in development: `uv sync` then `uv run python script.py`
3. Verify installation: `python -c "import gemini_google_search_tool"`

### Getting Help

```bash
# General help
gemini-google-search-tool --help

# Command-specific help
gemini-google-search-tool query --help
gemini-google-search-tool completion --help

# Version info
gemini-google-search-tool --version
```

### Debug Mode

Use `-vv` or `-vvv` for detailed debugging:

```bash
# Debug API calls and response processing
gemini-google-search-tool query "test" -vv

# Trace HTTP requests (shows full request/response)
gemini-google-search-tool query "test" -vvv
```

</details>

## Exit Codes

- `0`: Success - query completed successfully
- `1`: Error - client error, invalid arguments, or query failure

## Output Formats

**JSON (default):**
- Structured output with response_text and citations
- Machine-parseable for pipeline integration
- Always includes citations array
- Optional grounding_metadata with `-vv` or `-vvv`

**Markdown (`--text`):**
- Human-readable format
- Response text followed by citations section
- Good for direct reading or documentation

**Verbosity (stderr):**
- Logs and verbose output go to stderr
- Keeps stdout clean for JSON parsing
- Use `-v/-vv/-vvv` for progressively more detail

## Best Practices

1. **Use Flash Model by Default**: The gemini-2.5-flash model is fast and cost-effective for most queries
2. **Add Citations for Verification**: Use `--add-citations` when you need inline source links
3. **Pipeline Integration**: Pipe JSON output through `jq` for structured data processing
4. **Verbosity for Debugging**: Use `-vv` when troubleshooting, `-vvv` for HTTP-level details
5. **Environment Variables**: Store API key securely in shell profile, not in scripts
6. **Error Handling**: Always check exit codes when using in scripts or automation
7. **Model Selection**: Use `--pro` for complex analysis requiring deeper reasoning

## Resources

- **GitHub Repository**: https://github.com/dnvriend/gemini-google-search-tool
- **Google Search Grounding Docs**: https://ai.google.dev/gemini-api/docs/grounding
- **Gemini API Documentation**: https://ai.google.dev/gemini-api/docs
- **Get API Key**: https://aistudio.google.com/app/apikey
- **Python Package**: Installable via `uv tool install`
- **Developer Guide**: See CLAUDE.md in repository

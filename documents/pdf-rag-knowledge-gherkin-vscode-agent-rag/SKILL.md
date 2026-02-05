---
name: pdf-rag-knowledge
description: Search and retrieve information from indexed PDF documentation including IC datasheets, FPGA manuals, and technical specifications. Use this when the user asks about hardware specifications, pin configurations, register details, timing diagrams, or any technical information that might be in datasheets or technical documentation.
---

# PDF RAG Knowledge Base Skill

This skill enables GitHub Copilot to search a locally-indexed knowledge base of PDF documentation (IC datasheets, FPGA manuals, technical specifications) using semantic search.

## 🎯 Fully Portable & Self-Contained

This skill is **100% self-contained** in the `.github/skills/pdf-rag-knowledge/` directory:
- ✅ Portable Python search script (`rag_search.py`)
- ✅ Repo-specific vector database (`vector_store.json`)
- ✅ Bash helper script (`search_rag.sh`)
- ✅ No external dependencies on project structure

**Copy the entire folder to any repo to use it!**

## When to Use This Skill

Use this skill when users ask about:
- IC specifications (STM32, ESP32, microcontroller datasheets)
- FPGA documentation and configurations
- Hardware pin configurations and GPIO settings
- Register addresses and bit fields
- Timing specifications and electrical characteristics
- Communication protocols (I2C, SPI, UART, etc.) as documented in datasheets
- Power consumption and thermal specifications
- Any technical details that would be found in PDF datasheets

## How It Works

1. The user asks a question about hardware or technical specifications
2. Copilot recognizes this matches the skill description
3. The skill searches the indexed PDF knowledge base using semantic search
4. Relevant content from datasheets is retrieved with source citations
5. Copilot uses this context to provide accurate, sourced answers

## Usage

### Search the Knowledge Base

```bash
# Using the helper script
./search_rag.sh "your search query"

# Or directly with Python
python3 rag_search.py --search "GPIO configuration"

# Limit results
./search_rag.sh "FPGA power" 3
```

### Index New PDFs

```bash
# Index a PDF
python3 rag_search.py --index path/to/datasheet.pdf

# Check status
python3 rag_search.py --stats

# Clear database
python3 rag_search.py --clear
```

## Requirements

**Python Dependencies:**
- `requests` - For Ollama API calls
- `PyPDF2` - For PDF indexing (only needed when adding PDFs)

**External Service:**
- Ollama running locally at `http://localhost:11434`
- With model `mxbai-embed-large` installed

```bash
# Install dependencies
pip install requests PyPDF2

# Install Ollama and pull model
ollama pull mxbai-embed-large
```

## File Structure

```
.github/skills/pdf-rag-knowledge/
├── SKILL.md              # This file (skill definition)
├── rag_search.py         # Portable search script
├── search_rag.sh         # Bash helper script
└── vector_store.json     # Repo-specific indexed PDFs
```

## Examples

### Example 1: GPIO Configuration
**User**: "How do I configure GPIO pins on STM32F407?"

**Skill searches**: `./search_rag.sh "GPIO configuration STM32F407"`

**Returns**: Relevant sections from STM32F407 datasheet with page numbers

### Example 2: FPGA Specifications
**User**: "What are the specifications for Artix-7 FPGAs?"

**Skill searches**: `./search_rag.sh "Artix-7 specifications"`

**Returns**: Device specifications, logic resources, I/O counts

### Example 3: Power Requirements
**User**: "What are the power requirements?"

**Skill searches**: `./search_rag.sh "power supply voltage requirements"`

**Returns**: Voltage ranges, current consumption, power modes

## Configuration

Environment variables (optional):
```bash
export OLLAMA_BASE_URL=http://localhost:11434
export OLLAMA_MODEL=mxbai-embed-large
export CHUNK_SIZE=2000
export CHUNK_OVERLAP=400
```

## Making It Portable to Other Repos

### Option 1: Copy the Entire Folder

```bash
# In your target repo
mkdir -p .github/skills
cp -r /path/to/source-repo/.github/skills/pdf-rag-knowledge .github/skills/

# Enable in VS Code
# Add to .vscode/settings.json:
{
  "chat.useAgentSkills": true
}
```

### Option 2: Fresh Start in New Repo

```bash
# In your new repo
mkdir -p .github/skills/pdf-rag-knowledge
cd .github/skills/pdf-rag-knowledge

# Copy just the scripts (not the vector store)
cp /path/to/source-repo/.github/skills/pdf-rag-knowledge/rag_search.py .
cp /path/to/source-repo/.github/skills/pdf-rag-knowledge/search_rag.sh .
cp /path/to/source-repo/.github/skills/pdf-rag-knowledge/SKILL.md .

# Index your repo-specific PDFs
python3 rag_search.py --index /path/to/your/pdfs/*.pdf
```

Each repo maintains its own `vector_store.json` with repo-specific documentation!

## Technical Details

### Search Process
1. Query converted to 1024-dimension embedding via Ollama
2. Cosine similarity calculated against all stored embeddings
3. Top K most relevant chunks returned
4. Results include similarity scores and source citations

### Vector Store Format
JSON file with documents and embeddings:
```json
{
  "doc_id": {
    "id": "unique_hash",
    "content": "text chunk",
    "embedding": [0.123, ...],
    "source": "filename.pdf",
    "page": 42,
    "metadata": {...}
  }
}
```

### PDF Chunking
- **Chunk Size**: 2000 characters
- **Overlap**: 400 characters (preserves context)
- **Min Size**: 100 characters (filters noise)

## Troubleshooting

### Check Status
```bash
python3 rag_search.py --stats
```

### Test Search
```bash
./search_rag.sh "test query"
```

### Verify Ollama
```bash
curl http://localhost:11434/api/tags
```

### Common Issues

**No results found:**
- Check if PDFs are indexed: `python3 rag_search.py --stats`
- Verify Ollama is running: `curl http://localhost:11434`

**Import errors:**
- Install requirements: `pip install requests PyPDF2`

**Permission denied:**
- Make scripts executable: `chmod +x *.sh *.py`

## Integration with VS Code Copilot

This skill integrates with GitHub Copilot through Agent Skills:

1. Copilot detects hardware/datasheet questions
2. Skill loads automatically (progressive disclosure)
3. Search executes against repo-specific knowledge base
4. Results seamlessly integrated into Copilot responses
5. You don't manually invoke - just ask natural questions

## Related Resources

- [Ollama](https://ollama.ai) - Local embedding service
- [Agent Skills Standard](https://agentskills.io)
- [VS Code Agent Skills Docs](https://code.visualstudio.com/docs/copilot/customization/agent-skills)

## Examples

### Example 1: GPIO Configuration
**User**: "How do I configure GPIO pins on STM32F407?"

**Skill searches**: `./search_rag.sh "GPIO configuration STM32F407"`

**Returns**: Relevant sections from STM32F407 datasheet with page numbers

### Example 2: FPGA Specifications
**User**: "What are the specifications for Artix-7 FPGAs?"

**Skill searches**: `./search_rag.sh "Artix-7 specifications"`

**Returns**: Device specifications, logic resources, I/O counts

### Example 3: Power Requirements
**User**: "What are the power requirements?"

**Skill searches**: `./search_rag.sh "power supply voltage requirements"`

**Returns**: Voltage ranges, current consumption, power modes

## Knowledge Base Management

### Check Status
To see what's currently indexed:

```bash
python3 rag_search.py --stats
```

### Index New PDFs
To add new documentation to the knowledge base:

```bash
python3 rag_search.py --index path/to/datasheet.pdf
```

### Clear Database
To remove all indexed documents:

```bash
python3 rag_search.py --clear
```

### Interactive Testing
Test searches directly:

```bash
./search_rag.sh "your query"
python3 rag_search.py --search "GPIO" --top-k 3
```

## Technical Details

### Search Process
1. Query converted to 1024-dimension embedding via Ollama
2. Cosine similarity calculated against all stored embeddings
3. Top K most relevant chunks returned
4. Results include similarity scores and source citations

### Vector Store Format
JSON file with documents and embeddings:
```json
{
  "doc_id": {
    "id": "unique_hash",
    "content": "text chunk",
    "embedding": [0.123, ...],
    "source": "filename.pdf",
    "page": 42,
    "metadata": {...}
  }
}
```

### PDF Chunking
- **Chunk Size**: 2000 characters
- **Overlap**: 400 characters (preserves context)
- **Min Size**: 100 characters (filters noise)

## Configuration

Environment variables (optional):
```bash
export OLLAMA_BASE_URL=http://localhost:11434
export OLLAMA_MODEL=mxbai-embed-large
export CHUNK_SIZE=2000
export CHUNK_OVERLAP=400
```

## Important Notes

1. **Repo-Specific**: Each repository has its own `vector_store.json` with repo-specific documentation.

2. **Ollama Must Be Running**: Ensure Ollama is running locally:
   ```bash
   curl http://localhost:11434/api/tags
   ```

3. **Source Citations**: Always reference the source document and page number when providing information from the knowledge base.

4. **Context Limitations**: The skill returns the most relevant chunks. For comprehensive answers, it may help to search multiple times with related queries.

## Troubleshooting

### Check Status
```bash
python3 rag_search.py --stats
```

### Test Search
```bash
./search_rag.sh "test query"
```

### Verify Ollama
```bash
curl http://localhost:11434/api/tags
```

### Common Issues

**No results found:**
- Check if PDFs are indexed: `python3 rag_search.py --stats`
- Verify Ollama is running: `curl http://localhost:11434`

**Import errors:**
- Install requirements: `pip install requests PyPDF2`

**Permission denied:**
- Make scripts executable: `chmod +x *.sh *.py`

## Integration with VS Code Copilot

This skill integrates with GitHub Copilot through Agent Skills:

1. Copilot detects hardware/datasheet questions
2. Skill loads automatically (progressive disclosure)
3. Search executes against repo-specific knowledge base
4. Results seamlessly integrated into Copilot responses
5. You don't manually invoke - just ask natural questions

## Related Resources

- [Ollama](https://ollama.ai) - Local embedding service
- [Agent Skills Standard](https://agentskills.io)
- [VS Code Agent Skills Docs](https://code.visualstudio.com/docs/copilot/customization/agent-skills)

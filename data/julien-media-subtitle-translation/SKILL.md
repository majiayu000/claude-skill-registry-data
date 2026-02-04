---
name: julien-media-subtitle-translation
description: Translates SRT subtitle files using LLM APIs (OpenRouter/Llama). Use when user wants to translate subtitles, SRT files, or needs batch subtitle translation for movies/series. Handles HTML tags, batch processing, retries, and cost estimation.
triggers:
  - translate subtitles
  - translate srt
  - subtitle translation
  - traduire sous-titres
  - batch translate subtitles
  - srt file translation
  - movie subtitles
  - series subtitles
  - translate episodes
---

# Subtitle Translation Skill

Translate SRT subtitle files efficiently using LLM APIs with proper cost management.

## When to Use

- User wants to translate `.srt` subtitle files
- Batch translation of multiple episodes/movies
- Translation between any language pair (default: EN→FR)

## Step 0: Ask User for API Provider

**Always ask the user which provider to use:**

```
Which API provider do you want to use?

1. **OpenRouter** (Recommended) - Best price/quality, many models
2. **OpenAI** - GPT-4o-mini, reliable but needs credit card
3. **Ollama Local** - Free, runs on your machine (needs GPU)
4. **Ollama Hostinger** - Free, runs on your VPS

For large batches (100+ episodes): OpenRouter or Ollama Hostinger
For small batches (<20 episodes): Any option works
```

### Provider Configuration

| Provider | API URL | Auth |
|----------|---------|------|
| OpenRouter | `https://openrouter.ai/api/v1/chat/completions` | Bearer token |
| OpenAI | `https://api.openai.com/v1/chat/completions` | Bearer token |
| Ollama Local | `http://localhost:11434/api/chat` | None |
| Ollama Hostinger | `http://YOUR_VPS_IP:11434/api/chat` | None |

## Step 1: Choose Model Based on Complexity

**Ask user about subtitle complexity:**

```
What type of content are you translating?

A) Simple dialogue (sitcoms, slice-of-life) → Fast/cheap model
B) Standard content (action, drama) → Balanced model
C) Complex content (technical, poetry, wordplay) → Quality model
```

### Model Recommendations (December 2024)

| Complexity | OpenRouter | OpenAI | Ollama |
|------------|------------|--------|--------|
| **Simple** | `mistral-7b-instruct` ($0.03/M) | - | `mistral:7b` |
| **Standard** | `llama-3.3-70b-instruct` ($0.11/M in, $0.34/M out) | `gpt-4o-mini` ($0.15/M in, $0.60/M out) | `llama3.1:70b` |
| **Complex** | `claude-3.5-sonnet` ($3/M in, $15/M out) | `gpt-4o` ($2.50/M in, $10/M out) | `llama3.1:70b` |

### Low-Resource Servers (VPS < 16GB RAM)

For servers with limited RAM, use lightweight multilingual models:

| Model | RAM Required | Quality | Speed | Best For |
|-------|--------------|---------|-------|----------|
| **`aya:8b`** | ~6GB | Good | Fast | Multilingual - 100+ languages native |
| `mistral:7b` | ~5GB | OK | Fast | European languages |
| `gemma2:9b` | ~7GB | Good | Medium | General purpose |

**Aya 8B is recommended** for subtitle translation on VPS because:
- Trained specifically for multilingual tasks (100+ languages)
- Low memory footprint (~6GB VRAM/RAM)
- Good quality for dialogue translation
- Free with Ollama

```bash
# Install on VPS
ollama pull aya:8b

# Test
ollama run aya:8b "Translate to French: Hello, how are you?"
```

### Live Model Search (OpenRouter)

```python
def search_models(min_context=8000):
    """Search OpenRouter for available models with pricing"""
    r = requests.get("https://openrouter.ai/api/v1/models")
    models = r.json().get("data", [])

    # Filter and sort by price
    suitable = []
    for m in models:
        ctx = m.get("context_length", 0)
        if ctx >= min_context:
            price_in = m.get("pricing", {}).get("prompt", 0)
            price_out = m.get("pricing", {}).get("completion", 0)
            suitable.append({
                "id": m["id"],
                "name": m.get("name", m["id"]),
                "context": ctx,
                "price_in": float(price_in) * 1_000_000,  # Per M tokens
                "price_out": float(price_out) * 1_000_000
            })

    return sorted(suitable, key=lambda x: x["price_in"])[:10]
```

## Key Learnings (Production-Tested)

### Cost Reality Check

**Always multiply naive estimates by 1.5x** due to:
- System prompts repeated per batch
- JSON formatting overhead
- Instruction tokens

| Model | Input | Output | Real Cost/Episode |
|-------|-------|--------|-------------------|
| Llama 3.3 70B | $0.11/M | $0.34/M | ~$0.007 |
| GPT-4o-mini | $0.15/M | $0.60/M | ~$0.012 |

### Optimal Configuration

```python
BATCH_SIZE = 25          # Subtitles per API request (sweet spot)
DELAY_BETWEEN_REQUESTS = 0.5  # Avoid rate limits
MAX_RETRIES = 3          # Per batch
REQUEST_TIMEOUT = 90     # Seconds
```

## Implementation Steps

### 1. Parse SRT Format

```python
def parse_srt(content):
    """Parse SRT into list of (index, timing, text) tuples"""
    blocks = []
    current = []
    for line in content.strip().split('\n'):
        if line.strip() == '':
            if current:
                idx = current[0]
                timing = current[1]
                text = '\n'.join(current[2:])
                blocks.append((idx, timing, text))
                current = []
        else:
            current.append(line)
    if current:
        idx = current[0]
        timing = current[1]
        text = '\n'.join(current[2:])
        blocks.append((idx, timing, text))
    return blocks
```

### 2. HTML Tag Preservation (Critical)

**Never send HTML tags to the LLM** - they get corrupted. Strip before, reapply after.

```python
import re

def extract_formatting(text):
    """Extract HTML tags with positions for later restoration"""
    tags = []
    for match in re.finditer(r'<[^>]+>', text):
        tags.append((match.start(), match.end(), match.group()))
    return tags

def strip_html_tags(text):
    """Remove HTML tags for clean translation"""
    return re.sub(r'<[^>]+>', '', text)

def apply_formatting(translated, original_tags):
    """Reapply original HTML structure to translation"""
    if not original_tags:
        return translated
    # Preserve italic tags at start/end
    result = translated
    for start, end, tag in original_tags:
        if tag == '<i>' and not result.startswith('<i>'):
            result = '<i>' + result
        elif tag == '</i>' and not result.endswith('</i>'):
            result = result + '</i>'
    return result
```

### 3. Batch Translation with Retry Queue

```python
def translate_batch(texts, source='English', target='French'):
    """Translate batch of texts, return list or None on failure"""
    prompt = f"""Translate these {source} subtitles to {target}.
Return ONLY a JSON array of translated strings, same order.
Keep it natural and conversational.

{json.dumps(texts, ensure_ascii=False)}"""

    # API call with retries
    for attempt in range(MAX_RETRIES):
        try:
            response = call_api(prompt)
            return json.loads(response)
        except:
            time.sleep(2 ** attempt)  # Exponential backoff
    return None
```

### 4. Failed Batch Queue

Store failed batches for later retry:

```python
def add_failed_batch(file_path, batch_index, blocks_data):
    """Queue failed batch for retry"""
    failed_data = load_failed_batches()
    failed_data["batches"].append({
        "fr_srt": str(file_path),
        "batch_index": batch_index,
        "blocks": blocks_data,
        "retry_count": 0,
        "timestamp": datetime.now().isoformat()
    })
    save_failed_batches(failed_data)
```

### 5. Resilient Execution

**Always wrap main() in auto-restart**:

```python
def run_resilient():
    """Auto-restart on errors (up to 50 times)"""
    max_restarts = 50
    restart_count = 0

    while restart_count < max_restarts:
        try:
            main()
            break
        except KeyboardInterrupt:
            log("Manual stop (Ctrl+C)")
            break
        except Exception as e:
            restart_count += 1
            log(f"ERROR: {e}")
            log(f"Auto-restart {restart_count}/{max_restarts} in 30s...")
            time.sleep(30)
```

### 6. Progress Tracking

```python
PROGRESS_FILE = "translation_progress.json"

def load_progress():
    try:
        with open(PROGRESS_FILE) as f:
            return json.load(f)
    except:
        return {"completed": [], "failed": [], "total_cost": 0.0}

def save_progress(state):
    state["last_update"] = datetime.now().isoformat()
    with open(PROGRESS_FILE, 'w') as f:
        json.dump(state, f, indent=2)
```

## API Configuration

### OpenRouter (Recommended)

```python
OPENROUTER_API_KEY = "sk-or-v1-..."
MODEL = "meta-llama/llama-3.3-70b-instruct"
API_URL = "https://openrouter.ai/api/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json"
}
```

### Check Credits

```python
def get_credits():
    r = requests.get("https://openrouter.ai/api/v1/credits",
                     headers={"Authorization": f"Bearer {API_KEY}"})
    data = r.json().get("data", {})
    return data.get("total_credits", 0) - data.get("total_usage", 0)
```

## File Naming Convention

| Input | Output |
|-------|--------|
| `movie.eng.srt` | `movie.fr.srt` |
| `episode.en.srt` | `episode.fr.srt` |

## Cost Estimation Formula

```
episodes × 250 subtitles × 50 tokens × 2 (in+out) × price/token × 1.5 (overhead)
```

Example: 600 episodes EN→FR with Llama 3.3 70B:
- Naive: 600 × 250 × 50 × 2 × $0.20/M = $3.00
- **Real: $3.00 × 1.5 = ~$4.50**

## Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| HTML tags corrupted | Strip before translation, reapply after |
| Rate limit errors | Add 0.5s delay between requests |
| Parsing failures | Retry with exponential backoff |
| Script stops randomly | Use `run_resilient()` wrapper |
| Cost higher than expected | Multiply estimates by 1.5x |

## Skill Chaining

### Skills Required Before
- None (can work standalone)

### Input Expected
- Directory path containing `.srt` files
- Source/target languages (default: EN→FR)
- API provider choice (OpenRouter/OpenAI/Ollama)
- API key (if not Ollama)

### Output Produced
- Translated `.srt` files with language suffix
- `translation_progress.json` - tracks completed files
- `failed_batches.json` - retry queue
- `translation.log` - detailed logs

### Compatible Skills After
- **video-transcoding**: Burn subtitles into video
- **media-organization**: Organize translated files

### Tools Used
- `Write` (create translation script)
- `Bash` (run translation)
- `Read` (check progress/logs)
- `AskUserQuestion` (provider/model selection)
- `WebFetch` (live model pricing)

### Visual Workflow

```
User: "Translate my subtitles to French"
    ↓
[Ask] Which API provider?
    ├─► OpenRouter (recommended)
    ├─► OpenAI
    ├─► Ollama Local
    └─► Ollama Hostinger
    ↓
[Ask] Content complexity?
    ├─► Simple → mistral-7b ($0.03/M)
    ├─► Standard → llama-3.3-70b ($0.20/M)
    └─► Complex → claude-3.5-sonnet ($9/M)
    ↓
[Calculate] Cost estimate × 1.5
    ↓
[Confirm] "~$X for Y episodes. Proceed?"
    ↓
[Execute] translate_srt.py
    ├─► Parse SRT → Strip HTML → Batch (25/req)
    ├─► Translate → Reapply formatting
    └─► Track progress → Queue failures
    ↓
[Done] X.fr.srt files created
```

### Usage Example

**Scenario**: Translate 600 One Piece episodes EN→FR

**Interaction**:
1. Claude asks provider → User: "OpenRouter"
2. Claude asks complexity → User: "Standard (anime)"
3. Claude calculates: 600 × $0.007 × 1.5 = **~$6.30**
4. User confirms → Script runs
5. Result: 600 `.fr.srt` files, actual cost ~$4-7

**Output structure**:
```
/anime/onepiece/
├── Episode.001.eng.srt  (original)
├── Episode.001.fr.srt   (NEW)
├── translation_progress.json
├── failed_batches.json
└── translation.log
```

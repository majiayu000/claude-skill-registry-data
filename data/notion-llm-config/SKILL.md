---
name: notion-llm-config
description: Manages the Notion LLM Config Table database tracking model configurations and parameters across multiple model providers. Use when working with the LLM config table, adding models, updating model parameters, or querying model architecture details.
allowed-tools: mcp__notion__notion-search, mcp__notion__notion-fetch, mcp__notion__notion-create-pages, mcp__notion__notion-update-page, mcp__notion__notion-update-database, Read, Bash
---

# Notion LLM Config Table Management

## Database Information
- **Database ID:** `ddfd95bd-109a-4ac6-955c-90541cc53d5e`
- **Data Source ID:** `0a9fafd6-2cc2-4d6b-b6f0-3797ea777421`
- **Location:** Family Notes workspace → "LLM config table"
- **Purpose:** Track LLM model configurations across multiple providers (Llama, GPT-2, Qwen, others)

## Data Sources

### Llama Models
Primary source: `~/projects/github/llama-models/models/sku_list.py`
- Contains all registered Llama models with architecture parameters
- Constants: `LLAMA2_VOCAB_SIZE = 32000`, `LLAMA3_VOCAB_SIZE = 128256`
- **WARNING**: `sku_list.py` has incorrect `ffn_dim_multiplier` values for Llama 2 7B and 13B models
  - sku_list.py shows 1.3 for all Llama 2 models, but actual checkpoints differ
  - Always verify d_ff values against HuggingFace configs, not just sku_list.py

### GPT-2 Models
Primary source: HuggingFace config.json files
- Base repos: `openai-community/gpt2`, `gpt2-medium`, `gpt2-large`, `gpt2-xl`
- All variants: vocab_size=50257, max_context=1024, uses BPE tokenizer
- Uses learned positional embeddings (not RoPE)

## User Preferences
1. **No emojis** in any updates or content
2. **Batch operations** preferred over sequential updates
3. Focus on **practical utility** - add "Main" column for filtering to representative models
4. **Verify calculations** - user will catch errors, so double-check formulas

## Database Schema Key Columns

### Identity
- Model Name (title), Model Family, Model Type, Core Model ID
- HuggingFace Repo, Variant

### Architecture Parameters
- **d_hidden** = model hidden dimension (`dim` from Llama arch_args)
- **d_ff** = feed-forward hidden dimension (see calculation formulas below)
- **d_ff / d_hidden Ratio** = d_ff / d_hidden, rounded to 3 decimals
  - Llama 2: 2.688 (7B), 2.7 (13B), 3.5 (70B)
  - Llama 3+: 2.667 (3B), 3.125 (Guard INT4), 3.25 (405B), 3.5 (most common), 4.0 (1B)
  - GPT-2: 4.0 (all variants - standard transformer)
  - Null for models without d_ff (Llama 4 has empty arch_args)
- **Gated MLP** (checkbox) = gated MLP/activation (SwiGLU for Llama, standard GELU for GPT-2)
- n_layers, n_heads, n_kv_heads, head_dim
- Multiple Of, Norm Eps

### Tokenization
- **Tokenizer**: Llama 2 Tokenizer (32k vocab) or Llama 3 Tokenizer (128k vocab)
- **Vocab Size**: 32000 (Llama 2), 128256 (Llama 3+)

### MoE Architecture
- **Is MoE** (checkbox)
- **Num Experts**: Llama 4: 16 (Scout), 128 (Maverick)
- **Top K Experts**: Number of routed experts per token
- **MoE Routing**: "Token Choice" (Llama 4) vs "Expert Choice"
- **Has Shared Expert**: Llama 4 has 1 shared + 1 routed per token
- **Activated Params (B)**: Llama 4: 17B
- **Total Params (B)**: Llama 4: 109B (Scout), 400B (Maverick)

### RoPE Configuration
- RoPE Theta, RoPE Freq Base
- Use Scaled RoPE (checkbox)

### Other
- Quantization Format, PTH File Count, Max Context Size
- Main (checkbox) - marks representative models for filtering

## Update Patterns

### Property Updates (Preferred)
```python
mcp__notion__notion-update-page({
    "page_id": "page-id-here",
    "command": "update_properties",
    "properties": {
        "Tokenizer": "Llama 3 Tokenizer",
        "Vocab Size": 128256,
        "Is MoE": "__YES__",  # Checkboxes use __YES__/__NO__
        "Num Experts": 16
    }
})
```

### Batch Updates
- Use parallel tool calls when updating multiple independent pages
- Group by model family for logical batching (e.g., all Scout models together)

### Search & Fetch
```python
# Search within database
mcp__notion__notion-search({
    "query": "Llama 4",
    "query_type": "internal",
    "data_source_url": "collection://0a9fafd6-2cc2-4d6b-b6f0-3797ea777421"
})

# Fetch page details
mcp__notion__notion-fetch({"id": "page-id-or-url"})
```

## Common Tasks

### Adding New Models
1. Parse `~/projects/github/llama-models/models/sku_list.py` to get model data
2. Extract arch_args and calculate derived fields (head_dim, d_ff using Llama formula, d_ff/d_hidden ratio)
3. Determine tokenizer based on model family (see Llama Model Family Mappings)
4. Set MoE fields for Llama 4 models
5. Set "Gated MLP" to Yes (all Llama models use SwiGLU)
6. Create pages in batches using `mcp__notion__notion-create-pages`

### Marking Representative Models
Representative "Main" models (user preference):
- Llama 2: 7b chat, 70b chat
- Llama 3.1: 8b instruct, 70b instruct, 405b instruct (FP8)
- Llama 3.2: **1b instruct**, 3b instruct, 11b vision instruct (user trains small models)
- Llama 3.3: 70b instruct
- Llama 4: Scout instruct, Maverick instruct
- GPT-2: All variants (117M, 345M, 774M, 1.5B) marked as Main

### Schema Updates
```python
mcp__notion__notion-update-database({
    "database_id": "ddfd95bd-109a-4ac6-955c-90541cc53d5e",
    "properties": {
        "New Column": {"type": "number", "number": {}}
    }
})
```

## Important Notes

### Pitfalls to Avoid
1. **Don't clear existing fields** - Only specify properties you're updating
2. **Column ordering** - Cannot be changed via API (view-level setting in UI)
3. **Checkbox format** - Must use `"__YES__"` or `"__NO__"`, not boolean
4. **Llama 4 models** - Have empty `arch_args={}` in sku_list.py, no d_hidden/d_ff available

### Model Family Mappings

#### Llama
- **llama2**: Llama 2 Tokenizer, 32k vocab
  - Actual d_ff values (verified from HuggingFace):
    - 7B: d_ff=11008 (NOT 14336 from sku_list.py formula)
    - 13B: d_ff=13824 (NOT 17920 from sku_list.py formula)
    - 70B: d_ff=28672 (correct in sku_list.py)
- **llama3, llama3_1, llama3_2, llama3_3, llama4, safety**: Llama 3 Tokenizer, 128k vocab

#### GPT-2
- **gpt2**: BPE tokenizer, 50257 vocab, 1024 max context
- Naming: "GPT-2", "GPT-2 Medium", "GPT-2 Large", "GPT-2 XL"
- Model Type: "base" (all are base models)
- Parameter counts: 117M (base), 345M (medium), 774M (large), 1.5B (XL)
- Config parameter mappings: `n_embd` → `d_hidden`, `n_layer` → `n_layers`

#### Llama MoE Architecture (Llama 4 only)
- Only Llama 4 models are MoE
- Architecture: 1 shared expert (always active) + 1 routed expert (top_k=1)
- Effective: 2 experts per token (shared + routed)
- Routing: Token Choice (each token selects expert via router scores)

#### Llama Gated MLP / Activation Function
- All Llama models use gated MLP with SwiGLU activation
- Implementation: `w2(F.silu(w1(x)) * w3(x))` (from `models/llama3/model.py`)
- Uses 3 weight matrices (w1, w2, w3) instead of standard 2-matrix FFN
- SwiGLU = Swish-Gated Linear Unit (Swish is same as SiLU)

## Calculation Formulas

### General Derived Fields
```python
head_dim = d_hidden / n_heads
d_ff_d_hidden_ratio = round(d_ff / d_hidden, 3)
```

### Llama d_ff Calculation
From actual Llama code (`models/llama3/model.py`):
```python
# Initial: hidden_dim = 4 * dim
hidden_dim = int(2 * hidden_dim / 3)  # = int(8 * dim / 3)
if ffn_dim_multiplier is not None:
    hidden_dim = int(ffn_dim_multiplier * hidden_dim)
# Round up to multiple_of
hidden_dim = multiple_of * ((hidden_dim + multiple_of - 1) // multiple_of)
# Result is d_ff
```

**IMPORTANT: Llama 2 Model-Specific Behavior**

Llama 2 models use different `ffn_dim_multiplier` values than what's in `sku_list.py`:
- **7B & 13B**: Use `ffn_dim_multiplier=None` (pure 8d/3 formula)
  - 7B: d_ff=11008, ratio=2.688
  - 13B: d_ff=13824, ratio=2.7
- **70B**: Uses `ffn_dim_multiplier=1.3` (as specified in sku_list.py)
  - 70B: d_ff=28672, ratio=3.5

This was verified from actual HuggingFace checkpoint configs. The `sku_list.py` incorrectly shows `ffn_dim_multiplier=1.3` for all Llama 2 models.

Alternative formula from HuggingFace transformers (equivalent for models with multiple_of=256):
```python
# For Llama 2 7B, 13B (no multiplier)
def compute_intermediate_size(n, multiple_of=256):
    return int(math.ceil(n * 8 / 3) + multiple_of - 1) // multiple_of * multiple_of
```

### GPT-2 d_ff Calculation
Standard transformer architecture:
```python
d_ff = 4 * d_hidden  # Always 4x for all GPT-2 variants
```
- Not explicitly in config.json, but defined in model architecture
- All GPT-2 models have d_ff/d_hidden ratio of exactly 4.0

## Helpful Scripts & References

### Llama
Working directory: `~/projects/github/llama-models/`

**Scripts:**
- Parse models: `parse_llama_models.py`
- Prepare Notion data: `prepare_notion_data.py`
- Update tokenizers: `update_tokenizers.py`
- Bulk updates: `bulk_update_llama3.py`
- Calculate d_ff: `fix_d_ff.py` (correct d_ff calculation using actual Llama formula)
- Calculate ratios: `calculate_ratios.py` (d_ff/d_hidden ratios and gated MLP status)
- Data files: `d_ff_corrections.json`, `complete_notion_updates.json`, `ratio_updates.json`
- Documentation: `COMPLETION_SUMMARY.md` (d_ff update history), `STATUS.md` (current status)

**References:**
- Llama models repo: `~/projects/github/llama-models/`
- Model definitions: `models/sku_list.py`
- Architecture files: `models/llama{2,3,4}/args.py`
- MoE implementation: `models/llama4/moe.py`

### GPT-2
**HuggingFace References:**
- Base: `https://huggingface.co/openai-community/gpt2`
- Medium: `https://huggingface.co/gpt2-medium`
- Large: `https://huggingface.co/gpt2-large`
- XL: `https://huggingface.co/gpt2-xl`
- Config location: `/raw/main/config.json` (append to repo URL)

**Architecture Notes:**
- Uses learned positional embeddings (not RoPE) - add to Notes field
- Activation: GELU (gelu_new variant) - not gated MLP
- Standard attention (n_kv_heads = n_heads, no GQA)
- All variants have head_dim = 64
- Norm epsilon: 1e-05 (layer_norm_epsilon in config)

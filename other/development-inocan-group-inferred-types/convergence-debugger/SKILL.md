---
name: convergence-debugger
description: Expert debugging guide for AI Counsel's convergence detection system. Use when deliberations aren't converging as expected, early stopping fails, semantic similarity seems wrong, or voting vs semantic status conflicts occur.
triggers:
  - Convergence not detected when responses look similar
  - Early stopping not triggering despite models wanting to stop
  - Semantic similarity scores seem incorrect or unexpected
  - Status shows "refining" but responses are identical
  - Voting outcome conflicts with semantic similarity status
  - Backend selection issues (Jaccard vs TF-IDF vs SentenceTransformer)
  - Impasse detection not working
  - Min rounds check preventing convergence info
---

# Convergence Detection Debugger

## Overview

The AI Counsel convergence detection system (`deliberation/convergence.py`) determines when models have reached consensus and can stop deliberating early. It uses semantic similarity comparison between consecutive rounds, with voting outcomes taking precedence when available.

**Common Issue**: Convergence not detected → wasted API calls
**Common Issue**: Early stopping not triggering → deliberation runs full max_rounds
**Common Issue**: Semantic vs voting status conflict → confusing results

## Diagnostic Workflow

### Step 1: Examine the Transcript

**What to look for:**
- Are responses actually similar between rounds?
- Is there a "Convergence Information" section?
- What's the reported status and similarity scores?
- Are there votes? What's the voting outcome?

**File location:**
```bash
# Transcripts are in project root
ls -lt transcripts/*.md | head -5

# Open most recent
open "transcripts/$(ls -t transcripts/*.md | head -1)"
```

**Convergence section example:**
```markdown
## Convergence Information
- **Status**: refining (40.00% - 85.00% similarity)
- **Average Similarity**: 72.31%
- **Minimum Similarity**: 68.45%
```

**Voting section example (overrides semantic status):**
```markdown
## Final Voting Results
- **Winner**: TypeScript ✓
- **Status**: majority_decision
- **Tally**: TypeScript: 2, JavaScript: 1
```

**Missing convergence section?**
→ Check if `round_number <= min_rounds_before_check` (see Step 2)

### Step 2: Check Configuration

**Read the config:**
```bash
cat config.yaml
```

**Key settings to verify:**

```yaml
deliberation:
  convergence_detection:
    enabled: true  # Must be true
    semantic_similarity_threshold: 0.85  # Convergence if ALL participants >= this
    divergence_threshold: 0.40  # Diverging if ANY participant < this
    min_rounds_before_check: 1  # Must be <= (total_rounds - 1)
    consecutive_stable_rounds: 2  # Require this many stable rounds

  early_stopping:
    enabled: true  # Must be true for model-controlled stopping
    threshold: 0.66  # Fraction of models that must want to stop (2/3)
    respect_min_rounds: true  # Won't stop before defaults.rounds
```

**Common misconfigurations:**

| Problem | Cause | Fix |
|---------|-------|-----|
| No convergence info in transcript | `min_rounds_before_check` too high | For 2-round deliberation, use `min_rounds_before_check: 1` |
| Early stopping never triggers | `respect_min_rounds: true` but models converge before `defaults.rounds` | Set to `false` or reduce `defaults.rounds` |
| Convergence threshold too strict | `semantic_similarity_threshold: 0.95` | Lower to 0.80-0.85 for practical convergence |
| Everything marked "diverging" | `divergence_threshold: 0.70` too high | Use default 0.40 (models rarely agree <40%) |

### Step 3: Check Backend Selection

**The system auto-selects the best available backend:**

1. **SentenceTransformerBackend** (best) - requires `sentence-transformers`
2. **TFIDFBackend** (good) - requires `scikit-learn`
3. **JaccardBackend** (fallback) - zero dependencies (word overlap)

**Check what's installed:**
```bash
python -c "import sentence_transformers; print('✓ SentenceTransformer available')" 2>/dev/null || echo "✗ SentenceTransformer not available"
python -c "import sklearn; print('✓ TF-IDF available')" 2>/dev/null || echo "✗ TF-IDF not available"
```

**Check what backend was used:**
```bash
# Look at server logs
tail -50 mcp_server.log | grep -i "backend\|similarity"
```

**Expected log output:**
```
INFO - ConvergenceDetector initialized with SentenceTransformerBackend
INFO - Using SentenceTransformerBackend (best accuracy)
```

**If using Jaccard (fallback):**
- Similarity scores will be lower (word overlap only)
- Semantic paraphrasing NOT detected
- Consider installing optional dependencies:

```bash
# Install enhanced backends
pip install -r requirements-optional.txt

# Or individually
pip install sentence-transformers  # Best
pip install scikit-learn           # Good
```

### Step 4: Debug Semantic Similarity Scores

**Scenario: Responses look identical but similarity is low**

**Possible causes:**
1. Using Jaccard backend (doesn't understand semantics)
2. Responses have different formatting/structure
3. Models added different examples/details

**Test similarity manually:**
```python
# Create test script: test_similarity.py
from deliberation.convergence import ConvergenceDetector
from models.config import load_config

config = load_config("config.yaml")
detector = ConvergenceDetector(config)

text1 = "I prefer TypeScript for type safety and better tooling"
text2 = "TypeScript is better because it has types and good IDE support"

score = detector.backend.compute_similarity(text1, text2)
print(f"Similarity: {score:.2%}")
print(f"Backend: {detector.backend.__class__.__name__}")
```

**Run it:**
```bash
python test_similarity.py
```

**Expected results by backend:**
- **SentenceTransformer**: 75-85% (understands semantic similarity)
- **TF-IDF**: 50-65% (word importance weighting)
- **Jaccard**: 30-45% (simple word overlap)

### Step 5: Debug Voting vs Semantic Status Conflicts

**The voting outcome ALWAYS overrides semantic similarity status when votes are present.**

**Status precedence (highest to lowest):**
1. **unanimous_consensus** - All models voted same option
2. **majority_decision** - 2+ models agreed (e.g., 2-1 vote)
3. **tie** - Equal votes for all options (e.g., 1-1-1)
4. **Semantic status** - Only used if no votes present:
   - `converged` - All participants ≥85% similar
   - `refining` - Between 40-85% similarity
   - `diverging` - Any participant <40% similar
   - `impasse` - Stable disagreement over multiple rounds

**Check if votes are being parsed:**
```bash
# Search transcript for VOTE markers
grep -A 5 "VOTE:" "transcripts/$(ls -t transcripts/*.md | head -1)"
```

**Expected vote format in model responses:**
```
VOTE: {"option": "TypeScript", "confidence": 0.85, "rationale": "Type safety is crucial", "continue_debate": false}
```

**If votes aren't being parsed:**
- Check that models are outputting exact `VOTE: {json}` format
- Verify JSON is valid (use online JSON validator)
- Check logs for parsing errors: `grep -i "vote\|parse" mcp_server.log`

### Step 6: Debug Early Stopping

**Early stopping requires:**
1. `early_stopping.enabled: true` in config
2. At least `threshold` fraction of models set `continue_debate: false`
3. Current round ≥ `defaults.rounds` (if `respect_min_rounds: true`)

**Example: 3 models, threshold 0.66 (66%)**
- Round 1: All say `continue_debate: true` → continues
- Round 2: 2 models say `continue_debate: false` → stops (2/3 = 66.7%)

**Debug steps:**

1. **Check if enabled:**
```bash
grep -A 3 "early_stopping:" config.yaml
```

2. **Check model votes in transcript:**
```bash
# Look for continue_debate flags
grep -i "continue_debate" "transcripts/$(ls -t transcripts/*.md | head -1)"
```

3. **Check logs for early stop decision:**
```bash
grep -i "early stop\|continue_debate" mcp_server.log | tail -20
```

4. **Common issues:**

| Problem | Cause | Solution |
|---------|-------|----------|
| Models want to stop but deliberation continues | `respect_min_rounds: true` and not at min rounds yet | Wait for min rounds or set to `false` |
| Threshold not met | Only 1/3 models want to stop (33% < 66%) | Need 2/3 consensus |
| Not enabled | `enabled: false` | Set to `true` |
| Models not outputting flag | Vote JSON missing `continue_debate` field | Add to model prompts |

### Step 7: Debug Impasse Detection

**Impasse = stable disagreement over multiple rounds**

**Requirements:**
1. Status is `diverging` (min_similarity < 0.40)
2. `consecutive_stable_rounds` threshold reached (default: 2)

**Check impasse logic:**
```python
# Read convergence.py lines 380-385
# Impasse is only detected if diverging AND stable
```

**Common issue: Never reaches impasse**
- Models keep changing positions → not stable
- Divergence threshold too low → never marks as "diverging"
- Need at least 2-3 rounds of consistent disagreement

**Manual check:**
```bash
# Look at similarity scores across rounds
grep "Minimum Similarity" "transcripts/$(ls -t transcripts/*.md | head -1)"
```

**If similarity jumps around (45% → 25% → 60%):**
→ Models aren't stable, impasse won't trigger

### Step 8: Performance Diagnostics

**If convergence detection is slow:**

1. **Check if SentenceTransformer is downloading models:**
```bash
# First run downloads ~500MB model
tail -f mcp_server.log | grep -i "loading\|download"
```

2. **Model is cached after first load:**
- Subsequent deliberations are instant (model reused from memory)
- Cache is per-process (each server restart reloads)

3. **Check computation time:**
```bash
# Add timing to test script
import time

start = time.time()
score = detector.backend.compute_similarity(text1, text2)
elapsed = time.time() - start

print(f"Computation time: {elapsed*1000:.2f}ms")
```

**Expected times:**
- **SentenceTransformer**: 50-200ms per comparison (first run slower)
- **TF-IDF**: 10-50ms per comparison
- **Jaccard**: <1ms per comparison

## Quick Reference

### Configuration Parameters

```yaml
# Convergence thresholds
semantic_similarity_threshold: 0.85  # Range: 0.0-1.0, higher = stricter
divergence_threshold: 0.40           # Range: 0.0-1.0, lower = more sensitive

# Round constraints
min_rounds_before_check: 1           # Must be <= (total_rounds - 1)
consecutive_stable_rounds: 2         # Stability requirement

# Early stopping
early_stopping.threshold: 0.66       # Fraction of models needed (0.5 = majority)
respect_min_rounds: true             # Honor defaults.rounds minimum
```

### Status Definitions

| Status | Meaning | Similarity Range |
|--------|---------|------------------|
| converged | All participants agree | ≥85% (by default) |
| refining | Moderate agreement | 40-85% |
| diverging | Low agreement | <40% |
| impasse | Stable disagreement | <40% for 2+ rounds |
| unanimous_consensus | All voted same (overrides semantic) | N/A (voting) |
| majority_decision | 2+ voted same (overrides semantic) | N/A (voting) |
| tie | Equal votes (overrides semantic) | N/A (voting) |

### Common Fixes

**Problem: No convergence info in transcript**
```yaml
# Fix: Lower min_rounds_before_check
min_rounds_before_check: 1  # For 2-round deliberations
```

**Problem: Never converges despite identical responses**
```bash
# Fix: Install better backend
pip install sentence-transformers
```

**Problem: Early stopping not working**
```yaml
# Fix: Check these settings
early_stopping:
  enabled: true
  threshold: 0.66
  respect_min_rounds: false  # Allow stopping before min rounds
```

**Problem: Everything marked "diverging"**
```yaml
# Fix: Lower divergence threshold
divergence_threshold: 0.40  # Default (not 0.70)
```

## Files to Check

- **Config**: `/Users/harrison/Github/ai-counsel/config.yaml`
- **Engine**: `/Users/harrison/Github/ai-counsel/deliberation/convergence.py`
- **Transcripts**: `/Users/harrison/Github/ai-counsel/transcripts/*.md`
- **Logs**: `/Users/harrison/Github/ai-counsel/mcp_server.log`
- **Schema**: `/Users/harrison/Github/ai-counsel/models/schema.py` (Vote models)
- **Config models**: `/Users/harrison/Github/ai-counsel/models/config.py`

## Testing Convergence Detection

**Create integration test:**
```python
# tests/integration/test_convergence_debug.py
import pytest
from deliberation.convergence import ConvergenceDetector
from models.config import load_config
from models.schema import RoundResponse, Participant

def test_convergence_identical_responses():
    """Test that identical responses trigger convergence."""
    config = load_config("config.yaml")
    detector = ConvergenceDetector(config)

    # Create identical responses
    round1 = [
        RoundResponse(participant="claude", response="TypeScript is best", vote=None),
        RoundResponse(participant="codex", response="TypeScript is best", vote=None),
    ]
    round2 = [
        RoundResponse(participant="claude", response="TypeScript is best", vote=None),
        RoundResponse(participant="codex", response="TypeScript is best", vote=None),
    ]

    result = detector.check_convergence(round2, round1, round_number=2)

    assert result is not None, "Should check convergence at round 2"
    assert result.avg_similarity > 0.90, f"Identical responses should be >90% similar, got {result.avg_similarity}"
    print(f"Backend: {detector.backend.__class__.__name__}")
    print(f"Similarity: {result.avg_similarity:.2%}")
    print(f"Status: {result.status}")
```

**Run test:**
```bash
pytest tests/integration/test_convergence_debug.py -v -s
```

## Advanced Debugging

### Enable Debug Logging

```python
# Add to deliberation/engine.py or server.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Inspect Backend State

```python
# In Python shell or test
from deliberation.convergence import ConvergenceDetector
from models.config import load_config

config = load_config("config.yaml")
detector = ConvergenceDetector(config)

print(f"Backend: {detector.backend.__class__.__name__}")
print(f"Threshold: {detector.config.semantic_similarity_threshold}")
print(f"Min rounds: {detector.config.min_rounds_before_check}")
print(f"Consecutive stable: {detector.config.consecutive_stable_rounds}")
```

### Compare All Backends

```python
# test_all_backends.py
from deliberation.convergence import (
    JaccardBackend,
    TFIDFBackend,
    SentenceTransformerBackend
)

text1 = "I prefer TypeScript for type safety"
text2 = "TypeScript is better because it has types"

backends = {
    "Jaccard": JaccardBackend(),
}

try:
    backends["TF-IDF"] = TFIDFBackend()
except ImportError:
    print("TF-IDF not available")

try:
    backends["SentenceTransformer"] = SentenceTransformerBackend()
except ImportError:
    print("SentenceTransformer not available")

for name, backend in backends.items():
    score = backend.compute_similarity(text1, text2)
    print(f"{name:20s}: {score:.2%}")
```

## Summary

**Always check in order:**
1. ✅ Transcript - Does convergence info appear?
2. ✅ Config - Are thresholds reasonable?
3. ✅ Backend - Is the best backend installed?
4. ✅ Voting - Are votes being parsed correctly?
5. ✅ Early stopping - Is it enabled and configured correctly?
6. ✅ Logs - Any errors or warnings?

**Most common fixes:**
- Lower `min_rounds_before_check` to 1 for short deliberations
- Install `sentence-transformers` for better semantic detection
- Set `early_stopping.respect_min_rounds: false` for faster stopping
- Lower `semantic_similarity_threshold` from 0.95 to 0.85
- Check that models output valid `VOTE:` JSON with `continue_debate` field

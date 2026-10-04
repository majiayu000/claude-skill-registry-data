---
name: ai-matching-records
description: Find and merge duplicate records across datasets using AI. Use when deduplicating contacts, merging customer records, entity resolution, matching records across systems, finding duplicate tickets, fuzzy matching company names, CRM deduplication, record linkage across databases, matching people across data sources, identifying the same entity in different formats, contact merge, account deduplication, consolidating duplicate entries.
---

# Build an AI Record Matcher

Match and deduplicate records across datasets with DSPy - blocking to narrow candidates, pairwise LM scoring, and transitive closure to group all matches.

## Step 1: Understand the matching task

Ask the user:
1. **What records are you matching?** (contacts, companies, tickets, products, etc.)
2. **Which fields matter?** (name, email, phone, address, description, etc.)
3. **How many records?** (100s vs millions changes blocking strategy significantly)
4. **What defines a match?** (exact same entity, or "close enough to merge"?)
5. **What to do with matches?** (deduplicate, merge fields, link IDs, flag for review)

### When NOT to use AI matching

- **Single-field exact match** — if `email == email` or `id == id` covers your case, use SQL `JOIN` or a hash lookup. No LM needed.
- **Clean data with unique identifiers** — if records already have a shared key (user_id, EIN, ISBN), join on it directly.
- **Small datasets where manual review is faster** — under 50 records, a human can review pairs in minutes.
- **Simple fuzzy string matching covers it** — tools like `rapidfuzz` or `fuzzywuzzy` handle typos and abbreviations cheaply. Add an LM only when semantic understanding is needed ("IBM" = "International Business Machines").

## Step 2: Blocking strategies

Never compare all N×N pairs — that creates O(n²) LM calls. Blocking narrows candidates to a small set of plausible pairs first.

| Strategy | How it works | Best for |
|----------|-------------|---------|
| Exact field match | Block on normalized email, phone, or domain | Contact deduplication |
| Phonetic encoding | `jellyfish.soundex(name)` groups similar-sounding names | Person name matching |
| N-gram overlap | Tokenize and keep pairs sharing ≥2 tokens | Company name fuzzy match |
| Embedding similarity | Embed records, keep pairs with cosine similarity > 0.8 | Semantic entity resolution |
| Sorted neighborhood | Sort by key field, compare sliding window of size k | Large-scale address matching |

```python
from itertools import combinations
import jellyfish

def block_by_phonetic_name(records):
    """Group records by Soundex of first+last name, return candidate pairs."""
    buckets = {}
    for record in records:
        key = jellyfish.soundex(record["name"].lower())
        buckets.setdefault(key, []).append(record)

    pairs = []
    for bucket in buckets.values():
        if len(bucket) > 1:
            pairs.extend(combinations(bucket, 2))
    return pairs

def block_by_email_domain(records):
    """Block contacts that share email domain — likely same company."""
    buckets = {}
    for record in records:
        domain = record.get("email", "@").split("@")[-1]
        if domain and domain != "gmail.com":  # skip generic domains
            buckets.setdefault(domain, []).append(record)

    pairs = []
    for bucket in buckets.values():
        if len(bucket) > 1:
            pairs.extend(combinations(bucket, 2))
    return pairs
```

## Step 3: Build the pairwise comparison signature

```python
import dspy

lm = dspy.LM("openai/gpt-4o-mini")  # or "anthropic/claude-sonnet-4-5-20250929", etc.
dspy.configure(lm=lm)

class CompareRecords(dspy.Signature):
    """Determine whether two records refer to the same real-world entity.
    Consider semantic equivalence - 'IBM' matches 'International Business Machines Corp.'
    Focus on substance, not formatting differences."""
    record_a: str = dspy.InputField(desc="First record as a formatted string of field: value pairs")
    record_b: str = dspy.InputField(desc="Second record as a formatted string of field: value pairs")
    is_match: bool = dspy.OutputField(desc="True if both records refer to the same entity")
    confidence: float = dspy.OutputField(desc="Confidence score between 0.0 and 1.0")
    explanation: str = dspy.OutputField(desc="Brief explanation of why these are or are not the same entity")

matcher = dspy.ChainOfThought(CompareRecords)
```

Helper to format a record dict as a readable string:

```python
def format_record(record: dict) -> str:
    return "\n".join(f"{k}: {v}" for k, v in record.items() if v)
```

## Step 4: Full matching pipeline

```python
import dspy
from itertools import combinations

class RecordMatcher(dspy.Module):
    def __init__(self, match_threshold=0.6, auto_merge_threshold=0.9):
        self.compare = dspy.ChainOfThought(CompareRecords)
        self.match_threshold = match_threshold
        self.auto_merge_threshold = auto_merge_threshold

    def forward(self, records: list[dict]) -> dict:
        # Phase 1 - blocking: get candidate pairs
        candidate_pairs = self.block(records)

        # Phase 2 - pairwise scoring: score each candidate pair
        scored_pairs = []
        for a, b in candidate_pairs:
            result = self.compare(
                record_a=format_record(a),
                record_b=format_record(b),
            )
            scored_pairs.append({
                "record_a": a,
                "record_b": b,
                "is_match": result.is_match,
                "confidence": result.confidence,
                "explanation": result.explanation,
            })

        # Phase 3 - threshold routing
        auto_merge = [p for p in scored_pairs if p["confidence"] >= self.auto_merge_threshold]
        needs_review = [p for p in scored_pairs if self.match_threshold <= p["confidence"] < self.auto_merge_threshold]
        rejected = [p for p in scored_pairs if p["confidence"] < self.match_threshold]

        # Phase 4 - transitive closure: if A=B and B=C, then A=C
        match_pairs = [(p["record_a"]["id"], p["record_b"]["id"]) for p in auto_merge]
        clusters = self.transitive_closure(match_pairs, records)

        return {
            "clusters": clusters,
            "auto_merge": auto_merge,
            "needs_review": needs_review,
            "rejected": rejected,
        }

    def block(self, records):
        """Override with domain-specific blocking. Default - all pairs (only for small datasets)."""
        return list(combinations(records, 2))

    def transitive_closure(self, match_pairs, records):
        """Union-Find to group all transitively matched records into clusters."""
        parent = {r["id"]: r["id"] for r in records}

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        def union(x, y):
            parent[find(x)] = find(y)

        for a_id, b_id in match_pairs:
            union(a_id, b_id)

        clusters = {}
        for record in records:
            root = find(record["id"])
            clusters.setdefault(root, []).append(record)

        return list(clusters.values())
```

## Step 5: Merge strategies

Once you have clusters of matching records, decide how to merge them:

```python
def merge_cluster(cluster: list[dict], strategy="most_complete") -> dict:
    """Merge a cluster of matching records into one canonical record."""
    if strategy == "most_complete":
        # Keep the record with the most non-null fields
        return max(cluster, key=lambda r: sum(1 for v in r.values() if v))

    elif strategy == "newest":
        # Keep the most recently updated record
        return max(cluster, key=lambda r: r.get("updated_at", ""))

    elif strategy == "union":
        # Combine all fields, preferring non-null values from the first record that has them
        merged = {}
        for record in cluster:
            for k, v in record.items():
                if k not in merged or not merged[k]:
                    merged[k] = v
        return merged

    elif strategy == "custom":
        # Per-field rules: prefer email from oldest record, name from most complete, etc.
        raise NotImplementedError("Implement per-field merge logic for your use case")
```

## Step 6: Confidence thresholds

Route pairs based on confidence score - do not require human review for everything:

| Confidence range | Action | Rationale |
|-----------------|--------|-----------|
| >= 0.9 | Auto-merge | Very high confidence, human review not cost-effective |
| 0.6 - 0.9 | Human review queue | Ambiguous - surface to a person |
| < 0.6 | Reject as distinct | Low probability match, treat as different entities |

Tune these thresholds using your labeled pair data (see Step 7).

## Step 7: Evaluate and optimize

Label a sample of record pairs as match/no-match to measure precision and recall:

```python
from dspy.evaluate import Evaluate

# Labeled pairs - each example has record_a, record_b, and ground truth is_match
trainset = [
    dspy.Example(
        record_a="name: John Smith\nemail: john@acme.com\nphone: 555-1234",
        record_b="name: Jon Smith\nemail: john.smith@acme.com\nphone: 5551234",
        is_match=True,
        confidence=1.0,
        explanation="Same person, minor formatting differences in name/phone/email"
    ).with_inputs("record_a", "record_b"),
    # Add 20-50+ labeled pairs covering easy matches, near-misses, and clear non-matches
]

devset = trainset[len(trainset)*4//5:]
trainset = trainset[:len(trainset)*4//5]

def match_metric(example, pred, trace=None):
    """Precision-focused metric - penalize false positives more than false negatives."""
    correct_decision = pred.is_match == example.is_match
    if not correct_decision and pred.is_match:
        return 0.0  # false positive - penalize hard
    return float(correct_decision)

evaluator = Evaluate(devset=devset, metric=match_metric, num_threads=4, display_progress=True)
score = evaluator(matcher)
print(f"Baseline: {score}%")

# Optimize with BootstrapFewShot
optimizer = dspy.BootstrapFewShot(metric=match_metric, max_bootstrapped_demos=4)
optimized_matcher = optimizer.compile(matcher, trainset=trainset)

improved = evaluator(optimized_matcher)
print(f"Optimized: {improved}%")

optimized_matcher.save("record_matcher.json")
```

## Key patterns

### Asymmetric fields

Some fields are more diagnostic than others. Weight them explicitly in the signature:

```python
class CompareContacts(dspy.Signature):
    """Determine if two contact records refer to the same person.
    Email is the strongest signal. Name variations (nicknames, middle names) are common.
    Phone numbers may be formatted differently but represent the same number."""
    record_a: str = dspy.InputField()
    record_b: str = dspy.InputField()
    is_match: bool = dspy.OutputField()
    confidence: float = dspy.OutputField(desc="0.0 to 1.0")
    explanation: str = dspy.OutputField()
```

### Large-scale matching with embeddings

For datasets too large for phonetic blocking, use embedding similarity as the blocking layer:

```python
import numpy as np

def embed_records(records, embed_fn):
    """Embed each record as a single string for similarity search."""
    texts = [format_record(r) for r in records]
    return np.array([embed_fn(t) for t in texts])

def block_by_embedding(records, embeddings, top_k=5, threshold=0.8):
    """Return pairs whose embeddings exceed the similarity threshold."""
    from sklearn.metrics.pairwise import cosine_similarity
    sim_matrix = cosine_similarity(embeddings)
    pairs = []
    n = len(records)
    for i in range(n):
        for j in range(i+1, n):
            if sim_matrix[i][j] >= threshold:
                pairs.append((records[i], records[j]))
    return pairs
```

## Gotchas

- **Skipping blocking and making O(n²) LM calls** - always narrow candidates with a cheap heuristic first. Even rough phonetic or token-overlap blocking reduces pairs by 99%+ on typical datasets.
- **Using string equality for comparison fields** - do not compare fields with `==` in code before passing to the LM. Let the LM judge semantic equivalence so "IBM" matches "International Business Machines Corp."
- **Using `dspy.Assert`/`dspy.Suggest` for output validation** - use `dspy.Refine` with a reward function instead. `dspy.Assert` raises exceptions on constraint violations; `dspy.Refine` retries with feedback, which is the right pattern for improving match quality.
- **Skipping transitive closure** - if A matches B and B matches C, then A, B, and C are the same entity. Without Union-Find or similar, you will merge A+B and B+C separately but miss the A+B+C cluster.
- **Outputting only is_match without a confidence score** - boolean output makes threshold-based routing (auto-merge vs human review vs reject) impossible. Always include `confidence: float` in the output signature.

## Cross-references

> Install any skill: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill <name>`

- Compare two items with reasoning - see `/dspy-chain-of-thought`
- Retry with feedback when match quality is low - see `/dspy-refine`
- Sample multiple match decisions and pick the most consistent - see `/dspy-best-of-n`
- Generate labeled pair examples when you have none - see `/ai-generating-data`
- Measure and improve match precision/recall - see `/ai-improving-accuracy`
- Score similarity instead of binary match/no-match - see `/ai-scoring`
- **Install `/ai-do` if you do not have it** - it routes any AI problem to the right skill and is the fastest way to work: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill ai-do`

## Additional resources

- For API reference (DSPy signatures, optimizers, blocking libraries), see [reference.md](reference.md)
- For worked examples (CRM deduplication, company name matching, ticket deduplication), see [examples.md](examples.md)

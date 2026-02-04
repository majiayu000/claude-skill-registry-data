---
name: tfidf-search
description: Implements TF-IDF based search engines for text datasets using vector space models and cosine similarity. Use when building search functionality, finding similar documents, ranking text by relevance, or working with text retrieval systems.
allowed-tools: Read, Write, Bash, Grep, Glob
---

# TF-IDF Search Engine

Implement search engines using Term Frequency-Inverse Document Frequency (TF-IDF) vectorization and cosine similarity for ranking documents by relevance to a query.

## When to Use This Skill

- Building search functionality for text datasets
- Finding similar documents or passages
- Ranking documents by relevance to a query
- Implementing information retrieval systems
- Analyzing song lyrics, articles, documents, or any text corpus

## Core Concepts

**Vector Space Model (VSM)**: Represents text as vectors where each dimension corresponds to a unique word in the corpus.

**TF-IDF Score**: Combines term frequency (how often a word appears in a document) with inverse document frequency (how unique the word is across all documents). Common words like "the" get lower scores; rare, distinctive words get higher scores.

**Cosine Similarity**: Measures the angle between two vectors to determine document similarity. Range: -1 to 1, where 1 means identical direction (most similar).

## Implementation Workflow

### Step 1: Install Required Packages

Check project instructions for package management. For uv-based projects:

```bash
uv add numpy pandas scikit-learn
```

For pip-based projects:

```bash
pip install numpy pandas scikit-learn
```

### Step 2: Prepare Your Dataset

Your dataset should be in CSV format with at least one text column containing the documents to search.

Example structure:
```
song,artist,text
"Song Title","Artist Name","lyrics text here..."
```

### Step 3: Use the Helper Script

Run the TF-IDF search implementation:

```bash
python .claude/skills/tfidf-search/scripts/tfidf_search.py <csv_file> <text_column> "<query>" [--top_k 10]
```

Parameters:
- `csv_file`: Path to your CSV dataset
- `text_column`: Name of the column containing text to search
- `query`: Search query string (in quotes)
- `--top_k`: Number of top results to return (default: 10)

**Example**:
```bash
python .claude/skills/tfidf-search/scripts/tfidf_search.py songdata.csv text "Take it easy with me, please" --top_k 10
```

### Step 4: Custom Implementation

For custom implementations or integration into existing code:

```python
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load dataset
df = pd.read_csv('your_data.csv')

# Create and fit vectorizer
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df['text_column'])

# Transform query
query = "your search query"
query_vec = vectorizer.transform([query])

# Calculate similarities
results = cosine_similarity(X, query_vec)

# Get top results
top_indices = results.argsort(axis=0)[-10:][::-1].flatten()
for idx in top_indices:
    print(f"Score: {results[idx][0]:.4f} - {df.iloc[idx]['title']}")
```

## Key Implementation Details

**Query as List**: The `transform()` method expects a list of documents, even for a single query:
```python
query_vec = vectorizer.transform([query])  # Note the brackets
```

**Shape Verification**: Use `.shape` to verify dimensions:
```python
print(f"Corpus shape: {X.shape}")  # (n_documents, n_features)
print(f"Query shape: {query_vec.shape}")  # (1, n_features)
```

**Sorting Results**: Get top-k results using argsort:
```python
# For single query (results is 2D array)
top_k = 10
top_indices = results.argsort(axis=0)[-top_k:][::-1].flatten()
```

## Advanced Options

### TfidfVectorizer Parameters

Customize the vectorizer for better results:

```python
vectorizer = TfidfVectorizer(
    max_features=5000,        # Limit vocabulary size
    min_df=2,                 # Ignore terms appearing in < 2 docs
    max_df=0.8,               # Ignore terms appearing in > 80% of docs
    ngram_range=(1, 2),       # Include unigrams and bigrams
    stop_words='english'      # Remove common English words
)
```

### Handling Large Datasets

For large datasets, consider:
1. Using sparse matrix operations (scikit-learn handles this automatically)
2. Limiting vocabulary with `max_features`
3. Processing in batches if memory is constrained

### Improving Search Quality

**Preprocessing**: Clean text before vectorization:
```python
df['text'] = df['text'].str.lower()  # Lowercase
df['text'] = df['text'].str.replace('[^a-zA-Z\s]', '', regex=True)  # Remove punctuation
```

**N-grams**: Include phrases, not just single words:
```python
vectorizer = TfidfVectorizer(ngram_range=(1, 2))  # unigrams + bigrams
```

**Stop Words**: Remove common words that don't help distinguish documents:
```python
vectorizer = TfidfVectorizer(stop_words='english')
```

## Common Issues

**Low Similarity Scores**: Normal for TF-IDF. Scores of 0.1-0.3 can still indicate relevant matches. Focus on relative ranking, not absolute scores.

**Out of Vocabulary**: Query words not in the training corpus get zero weight. Preprocess queries the same way as documents.

**Memory Errors**: Reduce `max_features` or process smaller batches.

## References

For implementation examples and variations, see [examples.md](examples.md).

## Performance Considerations

- **Vectorization**: O(n × m) where n = documents, m = avg words per doc
- **Query Processing**: O(m) for single query transformation
- **Similarity Calculation**: O(n) for comparing query against n documents
- **Memory**: Sparse matrices keep memory usage manageable for large vocabularies

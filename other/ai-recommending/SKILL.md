---
name: ai-recommending
description: Build AI that recommends products, articles, or content based on user preferences. Use when building product recommendations, you-might-also-like features, personalizing feeds, content discovery, ranking by user preference, suggesting related items, building a recommendation engine, collaborative filtering with LLMs, re-ranking search results by relevance, curating personalized playlists, next-best-action suggestions, upsell recommendations, similar item matching, AI-powered content curation.
---

# ai-recommending

Build an AI recommendation engine using DSPy. The core pattern is two-stage - embedding-based retrieval to get candidate items, then an LM re-ranker that personalizes the ranking using user profile signals and generates human-readable explanations.

## Step 1 - Understand the recommendation task

Before writing code, clarify:

- **What items are you recommending?** Products, articles, support docs, videos, playlists?
- **What signals do you have?** Purchase history, click history, explicit ratings, topic tags, demographic signals?
- **Cold-start scenario?** New users with no history need a fallback strategy (popular items, content-based matching).
- **How many results?** Typically top-5 or top-10. More candidates are retrieved then re-ranked down.
- **Latency budget?** LM re-ranking adds ~500ms. If you need sub-100ms, do embedding-only retrieval.

## Step 2 - Build candidate retrieval

Use embedding similarity to retrieve a broad candidate set before LM re-ranking.

```python
import dspy
import numpy as np

lm = dspy.LM("openai/gpt-4o-mini")  # or "anthropic/claude-sonnet-4-5-20250929", etc.
dspy.configure(lm=lm)

# Embed items and user profile using any embedding provider
# This example uses a local stub — swap in your embedding function
def embed(text: str) -> np.ndarray:
    """Replace with your embedding model call."""
    raise NotImplementedError("Plug in your embedding model here")

def retrieve_candidates(user_embedding: np.ndarray, item_embeddings: dict, top_n: int = 20) -> list[str]:
    """Return top-N item IDs by cosine similarity."""
    scores = {
        item_id: float(np.dot(user_embedding, item_emb) /
                       (np.linalg.norm(user_embedding) * np.linalg.norm(item_emb) + 1e-9))
        for item_id, item_emb in item_embeddings.items()
    }
    return sorted(scores, key=scores.get, reverse=True)[:top_n]
```

## Step 3 - Build the LM re-ranker

Define a DSPy signature that takes a user profile and candidate items, then outputs ranked results with explanations.

```python
class ReRankRecommendations(dspy.Signature):
    """Re-rank candidate items for a user based on their preferences and history.
    Return the top items as a ranked list with a short, friendly explanation for each.
    Do not reveal internal scoring. Explanations should reference why the item fits the user."""

    user_profile: str = dspy.InputField(
        desc="Anonymized user preference summary - interests, recent activity, preferred categories"
    )
    candidate_items: str = dspy.InputField(
        desc="Numbered list of candidate items with title and short description"
    )
    num_results: int = dspy.InputField(desc="Number of top items to return")
    ranked_items: list[str] = dspy.OutputField(
        desc="Item IDs in ranked order, most relevant first"
    )
    explanations: list[str] = dspy.OutputField(
        desc="One friendly sentence per item explaining why it was recommended"
    )

reranker = dspy.Predict(ReRankRecommendations)
```

## Step 4 - Two-stage pipeline module

Combine retrieval and re-ranking into a single DSPy module.

```python
class RecommendationPipeline(dspy.Module):
    def __init__(self, item_catalog: dict, item_embeddings: dict, num_candidates: int = 20):
        super().__init__()
        self.item_catalog = item_catalog      # {item_id: {"title": ..., "description": ...}}
        self.item_embeddings = item_embeddings  # {item_id: np.ndarray}
        self.num_candidates = num_candidates
        self.reranker = dspy.Predict(ReRankRecommendations)

    def forward(self, user_profile: str, user_embedding: np.ndarray, num_results: int = 5):
        # Stage 1 - retrieve candidates by embedding similarity
        candidate_ids = retrieve_candidates(user_embedding, self.item_embeddings, self.num_candidates)

        # Stage 2 - format candidates for LM re-ranking
        candidates_text = "\n".join(
            f"{i+1}. [{cid}] {self.item_catalog[cid]['title']} - {self.item_catalog[cid]['description']}"
            for i, cid in enumerate(candidate_ids)
            if cid in self.item_catalog
        )

        result = self.reranker(
            user_profile=user_profile,
            candidate_items=candidates_text,
            num_results=num_results,
        )

        # Pair ranked item IDs with their explanations
        recommendations = []
        for item_id, explanation in zip(result.ranked_items[:num_results], result.explanations[:num_results]):
            item_id = item_id.strip("[]").strip()
            if item_id in self.item_catalog:
                recommendations.append({
                    "item_id": item_id,
                    "title": self.item_catalog[item_id]["title"],
                    "explanation": explanation,
                })

        return dspy.Prediction(recommendations=recommendations)
```

## Step 5 - Cold-start strategies

When a user has no history, fall back gracefully.

```python
def build_user_profile(history: list[str], item_catalog: dict) -> str | None:
    """Build a text profile from user history. Returns None if history is empty."""
    if not history:
        return None
    titles = [item_catalog[iid]["title"] for iid in history if iid in item_catalog]
    return f"Previously engaged with - {', '.join(titles)}"

def get_popular_items(item_catalog: dict, popularity_scores: dict, top_n: int = 5) -> list[dict]:
    """Fallback - return most popular items when no user profile exists."""
    ranked = sorted(popularity_scores, key=popularity_scores.get, reverse=True)[:top_n]
    return [{"item_id": iid, "title": item_catalog[iid]["title"], "explanation": "Popular with other users"} for iid in ranked]

def recommend(pipeline, user_profile, user_embedding, item_catalog, popularity_scores, num_results=5):
    if user_profile is None or user_embedding is None:
        return get_popular_items(item_catalog, popularity_scores, num_results)
    result = pipeline(user_profile=user_profile, user_embedding=user_embedding, num_results=num_results)
    return result.recommendations
```

## Step 6 - Evaluate recommendations

Use a DSPy judge to assess recommendation quality.

```python
class RecommendationJudge(dspy.Signature):
    """Assess whether recommended items are relevant and well-explained for the given user profile."""
    user_profile: str = dspy.InputField()
    recommendations: str = dspy.InputField(desc="Recommended items with titles and explanations")
    relevance_score: float = dspy.OutputField(desc="0.0 to 1.0 - how well items match the profile")
    explanation_quality: float = dspy.OutputField(desc="0.0 to 1.0 - how friendly and helpful the explanations are")
    feedback: str = dspy.OutputField(desc="One sentence of actionable feedback")

judge = dspy.Predict(RecommendationJudge)

def evaluate_recommendations(user_profile: str, recommendations: list[dict]) -> dict:
    recs_text = "\n".join(f"- {r['title']}: {r['explanation']}" for r in recommendations)
    result = judge(user_profile=user_profile, recommendations=recs_text)
    return {
        "relevance": result.relevance_score,
        "explanation_quality": result.explanation_quality,
        "feedback": result.feedback,
    }
```

For offline evaluation, compute precision@k - the fraction of recommended items in the top-k that the user actually engaged with.

```python
def precision_at_k(recommended_ids: list[str], relevant_ids: set[str], k: int) -> float:
    top_k = recommended_ids[:k]
    return len([iid for iid in top_k if iid in relevant_ids]) / k
```

## Step 7 - Optimize with BootstrapFewShot

```python
def recommendation_metric(example, prediction, trace=None):
    """Reward when relevant items appear in top results."""
    relevant = set(example.relevant_item_ids)
    recommended = [r["item_id"] for r in prediction.recommendations]
    return precision_at_k(recommended, relevant, k=5)

trainset = [
    dspy.Example(
        user_profile="Interested in hiking and outdoor gear",
        user_embedding=np.zeros(768),  # placeholder - use real embeddings
        relevant_item_ids=["item_001", "item_004"],
    ).with_inputs("user_profile", "user_embedding"),
    # Add more labeled examples
]

optimizer = dspy.BootstrapFewShot(metric=recommendation_metric, max_bootstrapped_demos=4)
optimized_pipeline = optimizer.compile(
    RecommendationPipeline(item_catalog={}, item_embeddings={}),
    trainset=trainset,
)
optimized_pipeline.save("recommender_optimized.json")
```

Typical result: embedding-only baseline ~35% precision@5; LM re-ranking without optimization ~50%; after BootstrapFewShot with 4 demos ~65-70% precision@5. Measure before and after with `dspy.Evaluate(devset, metric=recommendation_metric)` to confirm improvement.

## Tradeoff table

| Approach | Personalization | Speed | Cold-start | When to use |
|---|---|---|---|---|
| Embedding-only retrieval | Medium | Fast (<50ms) | Poor | Latency-critical, simple similarity |
| LM re-ranking (this skill) | High | Medium (~500ms) | With fallback | Nuanced preferences, need explanations |
| Collaborative filtering | High | Fast | Poor | Large implicit signal datasets |
| Popularity-based | None | Very fast | Excellent | Default/fallback for new users |

## When NOT to use LLM recommendations

- **Large implicit signal datasets** (millions of user-item interactions) - use collaborative filtering (ALS, BPR, matrix factorization). LMs cannot process interaction matrices.
- **Simple popularity-based ranking** - just sort by count. An LM adds latency with no benefit.
- **Real-time with sub-10ms latency requirements** - embedding similarity lookups only. LM calls cannot reliably meet this budget.
- **Highly repetitive catalog updates** (new items every second) - re-embedding is fast; re-prompting an LM per update is not.

## Key patterns

- Always pass **anonymized profile signals** to the LM, not raw user data. Summarize history as interests and categories.
- Keep the candidate set to **20-50 items** before LM re-ranking. Larger sets exceed context windows and reduce quality.
- Store item embeddings **offline** (precompute on catalog ingestion). Do not embed on every request.
- Use `dspy.ChainOfThought` instead of `dspy.Predict` for the re-ranker when explanation quality matters more than speed.
- For A/B testing, run both embedding-only and LM-reranked pipelines and measure click-through rate.

## Gotchas

- **Claude returns candidates unchanged** - if the re-ranking prompt does not explicitly say "reorder this list", the model may echo items back in the original order. Add "Reorder the items below, placing the most relevant first" to the signature docstring.
- **Claude builds the full pipeline in a single LM call** - the model may try to both retrieve and rank in one prompt. Enforce the two-stage approach: retrieve candidates with embeddings first, then pass only the candidate subset to the LM.
- **Claude uses `dspy.Assert` or `dspy.Suggest` for ranking constraints** - assertion-based control flow does not work well for ordering tasks. Use `dspy.Refine` with a reward function that checks ranking quality instead.
- **Claude includes user PII in the ranking prompt** - pass anonymized profile signals (interest categories, behavioral patterns) rather than names, emails, or raw purchase records. Make this explicit in the signature field description.
- **Claude generates explanations that leak ranking logic** ("this item scored 0.87") - the signature docstring must say "Do not reveal internal scoring. Write friendly explanations referencing why the item fits the user."

## Cross-references

> Install any skill: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill <name>`

- **`/ai-searching-docs`** - embedding-based retrieval pattern; the retrieval stage in this skill follows the same approach
- **`/dspy-retrieval`** - DSPy retrieval module patterns for the candidate generation stage
- **`/dspy-refine`** - iterative refinement with feedback; use instead of assertions for re-ranking quality loops
- **`/dspy-best-of-n`** - sample N ranking outputs and pick the best; useful for high-stakes recommendation slots
- **`/ai-scoring`** - scoring and ranking individual items; composable with this pipeline
- **`/ai-sorting`** - LM-based sorting of a fixed list; simpler than full recommendation when you already have candidates
- **`/ai-improving-accuracy`** - optimize the re-ranker with BootstrapFewShot or MIPROv2 once you have labeled data
- **Install `/ai-do` if you do not have it** — it routes any AI problem to the right skill and is the fastest way to work: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill ai-do`

## Additional resources

See [examples.md](examples.md) for worked examples - product recommender, article recommender, and support article suggester.

For DSPy API signatures, parameter tables, and module comparisons used in this skill, see [reference.md](reference.md).

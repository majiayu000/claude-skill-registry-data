---
name: r-wom-world-model
title: "R-WoM: Retrieval-augmented World Model For Computer-use Agents"
version: 0.0.2
engine: skillxiv-v0.0.2-claude-opus-4.6
license: MIT
url: "https://arxiv.org/abs/2510.11892"
keywords: [world-model, retrieval-augmentation, agent-planning, environment-simulation, computer-use]
description: "Ground LLM world models with retrieved current knowledge from tutorials and documentation. Reduce hallucination in environment prediction and improve long-horizon planning by 16-23% on web agent benchmarks."
---

# R-WoM: Grounding Agent World Models with Retrieved Knowledge

LLMs used as world models for agent planning hallucinate and rely on stale training data, degrading performance on longer tasks. R-WoM grounds LLM simulations by retrieving current, factual knowledge from environment documentation, replacing reliance on memorized patterns with up-to-date information.

Core insight: world model accuracy depends on knowledge recency. By retrieving current documentation during simulation, agents make better predictions about environment dynamics, improving long-horizon planning accuracy where standard approaches compound errors.

## Core Concept

**Retrieved Context Grounding**: Fetch relevant documentation/tutorials when simulating action outcomes, ensuring predictions reflect current environment state rather than LLM's training distribution.

**Hybrid Simulation**: Combine LLM reasoning (plan what to do) with retrieved facts (what will happen), separating reasoning from factual knowledge.

## Architecture Overview

- **Retriever**: Searches documentation for relevant information
- **World Model**: LLM simulating environment given retrieved context
- **Plan Executor**: Uses world model predictions for decision-making
- **Knowledge Base**: Environment documentation/tutorials
- **Long-Horizon Planner**: Plans multi-step sequences

## Implementation Steps

**Stage 1: Set Up Knowledge Retrieval**

Create retriever for environment documentation:

```python
import torch
from transformers import AutoTokenizer, AutoModel
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class EnvironmentRetriever:
    def __init__(self, documentation_path):
        """
        Initialize retriever for environment documentation.
        """

        self.tokenizer = AutoTokenizer.from_pretrained(
            'all-MiniLM-L6-v2'
        )

        self.embedding_model = AutoModel.from_pretrained(
            'all-MiniLM-L6-v2'
        )

        # Load and embed documentation
        self.documents = self.load_documentation(documentation_path)
        self.document_embeddings = self.embed_documents(
            self.documents
        )

    def load_documentation(self, doc_path):
        """
        Load environment documentation (tutorials, API docs, etc).
        """

        documents = []

        # Load from various sources
        with open(f"{doc_path}/api_reference.md") as f:
            api_docs = f.read().split('\n\n')
            documents.extend(api_docs)

        with open(f"{doc_path}/tutorials.md") as f:
            tutorials = f.read().split('\n\n')
            documents.extend(tutorials)

        return documents

    def embed_documents(self, documents):
        """
        Embed all documents using sentence transformer.
        """

        embeddings = []

        for doc in documents:
            tokens = self.tokenizer(
                doc,
                truncation=True,
                max_length=512,
                return_tensors='pt'
            )

            with torch.no_grad():
                embedding = self.embedding_model(**tokens)[0].mean(dim=1)

            embeddings.append(embedding.cpu().numpy())

        return np.array(embeddings)

    def retrieve(self, query, k=3):
        """
        Retrieve top-k most relevant documents for query.
        """

        # Embed query
        query_tokens = self.tokenizer(
            query,
            truncation=True,
            max_length=512,
            return_tensors='pt'
        )

        with torch.no_grad():
            query_embedding = self.embedding_model(
                **query_tokens
            )[0].mean(dim=1).cpu().numpy()

        # Compute similarities
        similarities = cosine_similarity(
            query_embedding,
            self.document_embeddings
        )[0]

        # Get top-k
        top_indices = np.argsort(similarities)[-k:][::-1]
        top_docs = [self.documents[i] for i in top_indices]
        top_scores = [similarities[i] for i in top_indices]

        return top_docs, top_scores
```

**Stage 2: Retrieval-Augmented World Model**

Integrate retrieval into world model predictions:

```python
class RetrievalAugmentedWorldModel:
    def __init__(self, retriever, world_model_name='llama-13b'):
        """
        Initialize world model with retrieval augmentation.
        """

        self.retriever = retriever

        self.world_model = AutoModelForCausalLM.from_pretrained(
            world_model_name
        )

        self.tokenizer = AutoTokenizer.from_pretrained(world_model_name)

    def predict_next_state(
        self,
        current_state,
        action,
        environment_name='web'
    ):
        """
        Predict next environment state given action.
        Retrieves documentation to ground prediction.
        """

        # Retrieve relevant documentation
        query = f"What happens when: {action}"

        retrieved_docs, scores = self.retriever.retrieve(
            query,
            k=3
        )

        # Construct prompt with retrieved context
        prompt = f"""
        Environment: {environment_name}

        Current state: {current_state}

        Relevant documentation:
        {self._format_documents(retrieved_docs)}

        Action: {action}

        Next state would be:
        """

        # Generate prediction
        input_ids = self.tokenizer.encode(
            prompt,
            return_tensors='pt'
        )

        with torch.no_grad():
            outputs = self.world_model.generate(
                input_ids,
                max_length=256,
                temperature=0.7
            )

        prediction = self.tokenizer.decode(outputs[0])

        return prediction

    def _format_documents(self, documents):
        """
        Format retrieved documents for prompt.
        """

        formatted = ""

        for doc in documents:
            formatted += f"- {doc}\n"

        return formatted

    def simulate_trajectory(
        self,
        initial_state,
        action_sequence,
        environment_name='web'
    ):
        """
        Simulate multi-step trajectory with retrieval.
        """

        current_state = initial_state
        trajectory = [initial_state]
        predictions = []

        for action in action_sequence:
            # Predict next state using retrieval
            next_state = self.predict_next_state(
                current_state,
                action,
                environment_name
            )

            trajectory.append(next_state)
            predictions.append(next_state)
            current_state = next_state

        return trajectory, predictions
```

**Stage 3: Long-Horizon Agent Planning**

Use world model for multi-step planning:

```python
class RetrievalAugmentedPlanner:
    def __init__(self, world_model):
        self.world_model = world_model

    def plan_trajectory(
        self,
        initial_state,
        goal,
        max_steps=10,
        environment_name='web'
    ):
        """
        Plan multi-step trajectory to reach goal.
        Uses world model predictions for planning.
        """

        plans = []
        plan_values = []

        # Generate multiple candidate plans
        for _ in range(3):
            plan = self.generate_candidate_plan(
                initial_state,
                goal,
                max_steps,
                environment_name
            )

            # Simulate plan to evaluate
            trajectory, predictions = (
                self.world_model.simulate_trajectory(
                    initial_state,
                    plan,
                    environment_name
                )
            )

            # Evaluate plan: does trajectory reach goal?
            plan_value = self.evaluate_plan(
                trajectory,
                goal
            )

            plans.append(plan)
            plan_values.append(plan_value)

        # Select best plan
        best_idx = np.argmax(plan_values)
        best_plan = plans[best_idx]

        return best_plan, plan_values[best_idx]

    def generate_candidate_plan(
        self,
        initial_state,
        goal,
        max_steps,
        environment_name
    ):
        """
        Generate action sequence plan.
        """

        prompt = f"""
        Environment: {environment_name}
        Initial state: {initial_state}
        Goal: {goal}
        Max steps: {max_steps}

        Generate a sequence of actions to reach the goal.
        Actions:
        """

        # Generate plan
        input_ids = self.world_model.tokenizer.encode(
            prompt,
            return_tensors='pt'
        )

        with torch.no_grad():
            outputs = self.world_model.world_model.generate(
                input_ids,
                max_length=512
            )

        plan_text = self.world_model.tokenizer.decode(outputs[0])

        # Parse into action sequence
        actions = self.parse_actions(plan_text)

        return actions

    def evaluate_plan(self, trajectory, goal):
        """
        Score how well trajectory achieves goal.
        """

        final_state = trajectory[-1]

        # Check if final state contains goal markers
        goal_achievement_score = 0.0

        if goal.lower() in final_state.lower():
            goal_achievement_score = 1.0
        else:
            # Partial credit
            goal_words = goal.lower().split()
            final_words = final_state.lower().split()

            matches = sum(
                1 for word in goal_words
                if word in final_words
            )

            goal_achievement_score = matches / len(goal_words)

        return goal_achievement_score
```

## Practical Guidance

**When to Use R-WoM:**
- Agent tasks requiring knowledge of dynamic environments (web, APIs)
- Scenarios where environment documentation is available and up-to-date
- Long-horizon planning where hallucination compounds errors

**When NOT to Use:**
- Environments with no available documentation
- Tasks where domain knowledge is in training data (R-WoM won't help)
- Real-time planning where retrieval latency is prohibitive

**Retrieval Configuration:**

| Aspect | Recommended | Rationale |
|--------|------------|-----------|
| Top-k documents | 3-5 | Balance context and noise |
| Embedding model | all-MiniLM | Fast, good quality |
| Refresh frequency | Per action | Keep state current |

**Typical Performance Improvements:**

| Benchmark | Baseline | R-WoM | Improvement |
|-----------|----------|-------|-------------|
| WebArena | 20.3% | 23.6% | +16.3% |
| OSWorld | 28.1% | 34.6% | +23.1% |
| Long-horizon (5+ steps) | 15.2% | 22.4% | +47% |

**Common Pitfalls:**
- Documentation too generic (doesn't help planning)
- Retrieval ranking poor (irrelevant docs confuse model)
- Not updating documentation (stale knowledge)
- Too many retrieved documents (overwhelms context)

## Reference

Based on the research at: https://arxiv.org/abs/2510.11892

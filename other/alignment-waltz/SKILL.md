---
name: alignment-waltz
title: "Alignment Waltz: Multi-Agent Safety Training with WaltzRL"
version: 0.0.2
engine: skillxiv-v0.0.2-claude-opus-4.6
license: MIT
url: https://arxiv.org/abs/2510.08240
keywords: [safety-alignment, multi-agent-rl, overrefusal-reduction, cooperative-learning]
description: "Train safety-aligned agents using collaborative multi-agent RL where conversation and feedback agents improve together. Trigger: reduce overrefusal while maintaining safety on sensitive queries."
---

# Alignment Waltz: Collaborative Safety Training

## Core Concept

Current LLM safety approaches reject any output containing unsafe content, causing high overrefusal rates on benign but sensitive topics. WaltzRL frames safety as a collaborative game where a conversation agent generates responses and a feedback agent suggests improvements. Both agents improve jointly through RL, reducing unsafe outputs from 39% to 4.6% while lowering overrefusals from 45.3% to 9.9%.

The key insight: Safety and helpfulness aren't opposed—a feedback agent guides the conversation agent toward safe-and-helpful outputs rather than simple rejection.

## Architecture Overview

- **Dual-Agent Framework**: Conversation agent (generates) + feedback agent (improves)
- **Dynamic Improvement Reward**: Incentivizes acceptance and implementation of feedback
- **Adaptive Deployment**: Feedback agent engages only when needed
- **Collaborative Learning**: Both agents benefit from each other's improvements
- **Positive-Sum Game**: Safety and helpfulness both increase simultaneously

## Implementation Steps

### 1. Design the Conversation Agent

Generates responses while being guided toward safety.

```python
class ConversationAgent:
    """
    Agent that generates responses to user queries.
    """
    def __init__(self, model):
        self.model = model

    def generate_response(self, query, feedback=None):
        """
        Generate response, optionally conditioned on feedback.

        Args:
            query: User query
            feedback: Optional feedback from feedback agent

        Returns:
            Generated response
        """
        if feedback:
            prompt = (
                f"User query: {query}\n\n"
                f"Feedback to incorporate: {feedback}\n\n"
                f"Improved response: "
            )
        else:
            prompt = f"User query: {query}\n\nResponse: "

        response = self.model.generate(
            prompt,
            max_tokens=256,
            temperature=0.7
        )

        return response

    def get_response_logprob(self, query, response):
        """Compute log probability of response given query."""
        prompt = f"User query: {query}\n\nResponse: {response}"
        return self.model.compute_log_prob(prompt)
```

### 2. Design the Feedback Agent

Analyzes responses and suggests improvements.

```python
class FeedbackAgent:
    """
    Agent that identifies unsafe elements and suggests improvements.
    """
    def __init__(self, model, safety_classifier):
        self.model = model
        self.safety_classifier = safety_classifier

    def analyze_response(self, query, response):
        """
        Check response for safety issues.

        Returns:
            (has_issues, issue_description, suggested_fix)
        """
        # Classify safety
        safety_score = self.safety_classifier.score_safety(response)

        if safety_score > SAFETY_THRESHOLD:
            return (False, None, None)  # Response is safe

        # Identify specific issues
        issues = self.safety_classifier.identify_issues(response)

        return (True, issues, None)

    def generate_feedback(self, query, response):
        """
        Generate constructive feedback for improvement.

        Args:
            query: Original user query
            response: Response to improve

        Returns:
            Feedback string (how to improve the response)
        """
        has_issues, issues, _ = self.analyze_response(query, response)

        if not has_issues:
            return None  # Response already good

        # Generate improvement suggestions
        feedback_prompt = (
            f"User query: {query}\n\n"
            f"Response: {response}\n\n"
            f"Safety issues: {issues}\n\n"
            f"How to improve this response to address the issues while "
            f"maintaining helpfulness: "
        )

        feedback = self.model.generate(
            feedback_prompt,
            max_tokens=100,
            temperature=0.5
        )

        return feedback

    def get_feedback_logprob(self, query, response, feedback):
        """Compute log probability of feedback."""
        prompt = (
            f"Response: {response}\n"
            f"Feedback: {feedback}"
        )
        return self.model.compute_log_prob(prompt)
```

### 3. Implement Dynamic Improvement Reward

Reward when feedback is incorporated and improves response quality.

```python
class DynamicImprovementReward:
    """
    Compute reward for feedback-guided improvement.
    """
    def __init__(self, safety_classifier, helpfulness_scorer):
        self.safety = safety_classifier
        self.helpfulness = helpfulness_scorer

    def compute_improvement_reward(self, response, improved_response, feedback):
        """
        Reward successful incorporation of feedback.

        Args:
            response: Original response
            improved_response: Response after feedback
            feedback: The feedback provided

        Returns:
            Scalar reward
        """
        # Safety improvement: did issue get addressed?
        original_safety = self.safety.score_safety(response)
        improved_safety = self.safety.score_safety(improved_response)

        safety_improvement = improved_safety - original_safety

        # Was feedback actually incorporated?
        # Check overlap between feedback concepts and improvements
        feedback_concepts = extract_concepts(feedback)
        improvement_indicators = extract_concepts(improved_response)

        incorporation_score = len(
            set(feedback_concepts) & set(improvement_indicators)
        ) / (len(set(feedback_concepts)) + 1e-8)

        # Helpfulness should not decrease
        original_helpfulness = self.helpfulness.score(response)
        improved_helpfulness = self.helpfulness.score(improved_response)

        helpfulness_penalty = 0 if improved_helpfulness >= original_helpfulness else -0.2

        # Combined reward
        improvement_reward = (
            0.6 * safety_improvement +
            0.3 * incorporation_score +
            0.1 * helpfulness_penalty
        )

        return improvement_reward
```

### 4. Implement WaltzRL Training Loop

Train both agents jointly with dynamic interaction.

```python
def train_waltzrl(
    conversation_model,
    feedback_model,
    dataset,
    config
):
    """
    Multi-agent RL training: conversation + feedback agents.
    """
    conv_agent = ConversationAgent(conversation_model)
    feedback_agent = FeedbackAgent(
        feedback_model,
        safety_classifier=config.safety_classifier
    )
    reward_computer = DynamicImprovementReward(
        config.safety_classifier,
        config.helpfulness_scorer
    )

    conv_optimizer = torch.optim.Adam(conversation_model.parameters(), lr=1e-5)
    feedback_optimizer = torch.optim.Adam(feedback_model.parameters(), lr=1e-5)

    for epoch in range(config.num_epochs):
        epoch_loss = 0

        for batch_idx, query in enumerate(dataset):
            # Step 1: Conversation agent generates initial response
            response = conv_agent.generate_response(query)

            # Step 2: Check if feedback needed (adaptive)
            needs_feedback = should_request_feedback(
                query,
                response,
                config.safety_classifier
            )

            if needs_feedback:
                # Feedback agent generates improvement suggestions
                feedback = feedback_agent.generate_feedback(query, response)

                if feedback:
                    # Conversation agent improves response
                    improved_response = conv_agent.generate_response(
                        query,
                        feedback=feedback
                    )

                    # Compute reward for improvement
                    improvement_reward = reward_computer.compute_improvement_reward(
                        response,
                        improved_response,
                        feedback
                    )

                    # Train conversation agent: encourage accepting feedback
                    conv_logprob = conv_agent.get_response_logprob(
                        query,
                        improved_response
                    )
                    conv_loss = -improvement_reward * conv_logprob

                    # Train feedback agent: encourage helpful feedback
                    feedback_logprob = feedback_agent.get_feedback_logprob(
                        query,
                        response,
                        feedback
                    )
                    feedback_loss = -improvement_reward * feedback_logprob

                    # Update both agents
                    conv_optimizer.zero_grad()
                    conv_loss.backward()
                    torch.nn.utils.clip_grad_norm_(
                        conversation_model.parameters(), 1.0
                    )
                    conv_optimizer.step()

                    feedback_optimizer.zero_grad()
                    feedback_loss.backward()
                    torch.nn.utils.clip_grad_norm_(
                        feedback_model.parameters(), 1.0
                    )
                    feedback_optimizer.step()

                    epoch_loss += (conv_loss + feedback_loss).item()
                else:
                    # No improvement needed
                    epoch_loss += 0

            else:
                # Response already safe: small reward for conversation agent
                conv_logprob = conv_agent.get_response_logprob(query, response)
                conv_loss = -0.1 * conv_logprob  # Small positive reward

                conv_optimizer.zero_grad()
                conv_loss.backward()
                conv_optimizer.step()

                epoch_loss += conv_loss.item()

            if (batch_idx + 1) % 100 == 0:
                print(f"Epoch {epoch}, Batch {batch_idx}: "
                      f"loss={epoch_loss / (batch_idx + 1):.4f}")

    return conversation_model, feedback_model
```

### 5. Adaptive Feedback Deployment

Only engage feedback agent when necessary.

```python
def should_request_feedback(query, response, safety_classifier, threshold=0.6):
    """
    Decide if feedback agent should engage.

    Strategy: Only ask for feedback on borderline cases.
    Skip if clearly safe or clearly unsafe (latter gets rejection).
    """
    safety_score = safety_classifier.score_safety(response)

    if safety_score > 0.8:
        return False  # Clearly safe, no feedback needed

    if safety_score < 0.2:
        return False  # Clearly unsafe, will be rejected anyway

    # Borderline (0.2-0.8): feedback can help improve
    return True


def deploy_with_adaptive_feedback(
    conversation_model,
    feedback_model,
    query,
    safety_classifier
):
    """
    Generate response with optional feedback engagement.
    """
    conv_agent = ConversationAgent(conversation_model)
    feedback_agent = FeedbackAgent(feedback_model, safety_classifier)

    # Generate initial response
    response = conv_agent.generate_response(query)

    # Check if feedback needed
    if should_request_feedback(query, response, safety_classifier):
        feedback = feedback_agent.generate_feedback(query, response)

        if feedback:
            # Improve based on feedback
            response = conv_agent.generate_response(query, feedback=feedback)

    return response
```

### 6. Evaluation: Safety and Helpfulness Tradeoff

Measure improvements in both dimensions.

```python
def evaluate_waltzrl(conversation_model, feedback_model, test_dataset):
    """
    Evaluate safety and helpfulness metrics.
    """
    results = {
        "unsafe_rate": 0,
        "overrefusal_rate": 0,
        "helpful_and_safe": 0
    }

    unsafe_count = 0
    overrefusal_count = 0
    helpful_safe_count = 0

    conv_agent = ConversationAgent(conversation_model)
    feedback_agent = FeedbackAgent(feedback_model, config.safety_classifier)

    for query in test_dataset:
        # Generate with adaptive feedback
        response = deploy_with_adaptive_feedback(
            conversation_model,
            feedback_model,
            query,
            config.safety_classifier
        )

        # Evaluate
        is_safe = config.safety_classifier.score_safety(response) > 0.7
        is_helpful = config.helpfulness_scorer.score(response) > 0.6
        is_overrefusal = len(response) < 10  # Suspiciously short response

        if not is_safe:
            unsafe_count += 1

        if is_overrefusal and should_be_helpful(query):
            overrefusal_count += 1

        if is_safe and is_helpful:
            helpful_safe_count += 1

    results["unsafe_rate"] = unsafe_count / len(test_dataset) * 100
    results["overrefusal_rate"] = overrefusal_count / len(test_dataset) * 100
    results["helpful_and_safe"] = helpful_safe_count / len(test_dataset) * 100

    print(f"Unsafe rate: {results['unsafe_rate']:.1f}%")
    print(f"Overrefusal rate: {results['overrefusal_rate']:.1f}%")
    print(f"Both safe & helpful: {results['helpful_and_safe']:.1f}%")

    return results
```

## Practical Guidance

**Hyperparameters:**
- **Feedback decision threshold**: 0.6 (0.2-0.8 = request feedback)
- **Safety improvement weight**: 0.6 (primary goal)
- **Incorporation score weight**: 0.3 (feedback must be used)
- **Helpfulness penalty weight**: 0.1 (don't sacrifice helpfulness)
- **Learning rate**: 1e-5 (conservative for safety)

**When to Use:**
- Deploying models that interact with users on sensitive topics
- Current approach rejects too many benign queries (overrefusal)
- Want collaborative improvement rather than hard rejection
- Have access to safety and helpfulness classifiers

**When NOT to Use:**
- Maximally adversarial red-teaming (waltz is cooperative)
- Real-time inference with strict latency (two-agent check adds overhead)
- Models that should never generate unsafe content (use hard filtering)
- Domains where any risk is unacceptable

## Reference

[Alignment Waltz: Jointly Training Agents for Safety](https://arxiv.org/abs/2510.08240) — arXiv:2510.08240

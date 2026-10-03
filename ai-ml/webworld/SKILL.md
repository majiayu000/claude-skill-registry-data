---
name: webworld
title: "WebWorld: A Large-Scale World Model for Web Agent Training"
version: 0.0.2
engine: skillxiv-v0.0.2-claude-opus-4.6
license: MIT
url: "https://arxiv.org/abs/2602.14721"
keywords: [World Models, Web Agents, Simulation, Large-Scale Training Data, Generalization]
description: "Train autoregressive world models on 1M+ real web interactions for accurate browser state prediction. Enables agent training with 100× more data than prior approaches, achieving GPT-4o comparable performance with format flexibility and cross-domain generalization."
---

# WebWorld: Large-Scale Web Agent Training Environment

## Problem Context

Web agent training requires massive interaction data that's expensive or impossible to collect at scale. Existing web world models use sandbox or closed environments with limited realism. Data scarcity forces agents to overfit to specific websites. Prior approaches generated only 10K-100K trajectories. Standard models trained on such small datasets don't capture real web complexity, limiting agent performance and generalization.

## Core Concept

WebWorld is a **large-scale autoregressive world model** trained on over 1 million real-world web interaction trajectories. Rather than generating synthetic data or using sandboxes, it learns from authentic web behavior patterns. The key innovation: collecting data through three complementary strategies (randomized crawling, autonomous exploration, task-oriented execution) creates diverse, realistic training distributions.

The model predicts next browser state given instruction and interaction history, enabling agents to train entirely in simulation. Multiple format support (A11y Trees, HTML, XML, Markdown) and explicit reasoning injection through chain-of-thought enable strong generalization to code, GUI, and game environments.

## Architecture Overview

- **Autoregressive State Predictor**: Predicts next DOM/browser state given action and history
- **Three-Level Data Collection**: Randomized crawling (293K), autonomous exploration (38K), task-oriented (94K)
- **100× Scale Increase**: 1M+ trajectories vs 10K in prior work
- **Multiple Format Support**: A11y Trees, HTML, XML, Markdown for flexibility
- **Explicit Reasoning**: Chain-of-thought synthesis on subset for improved reasoning
- **Model Sizes**: 8B, 14B, 32B parameters
- **Extended Simulation**: Supports 30+ steps per episode
- **Cross-Domain Transfer**: Generalizes to code, GUI, game environments

## Implementation

Three-level hierarchical data collection:

```python
class HierarchicalDataCollection:
    """
    Collect web interactions through three complementary strategies
    to create diverse, large-scale training dataset.
    """

    def __init__(self):
        self.trajectories = []
        self.stats = {
            'randomized_crawling': 0,
            'autonomous_exploration': 0,
            'task_oriented': 0
        }

    def level_1_randomized_crawling(self, corpus_websites, num_trajectories=293000):
        """
        Level 1: Randomized crawling of websites from pre-training corpora.
        Generates natural, unguided interactions.
        Creates 293K trajectories.
        """
        print("Level 1: Randomized Crawling")

        for traj_idx in range(num_trajectories):
            # Sample random website from corpus
            website = random.choice(corpus_websites)

            # Start fresh session
            browser = WebBrowser()
            browser.navigate(website)

            trajectory = {
                'website': website,
                'interactions': [],
                'type': 'randomized_crawling'
            }

            # Perform random interactions
            for step in range(random.randint(5, 30)):
                # Random action: click, type, scroll, etc.
                action = sample_random_action(browser)

                # Record before-state, action, after-state
                before_state = browser.get_state()
                browser.perform_action(action)
                after_state = browser.get_state()

                interaction = {
                    'action': action,
                    'before_state': before_state,
                    'after_state': after_state
                }
                trajectory['interactions'].append(interaction)

            self.trajectories.append(trajectory)
            self.stats['randomized_crawling'] += 1

            if (traj_idx + 1) % 10000 == 0:
                print(f"Collected {traj_idx + 1} randomized trajectories")

    def level_2_autonomous_exploration(self, websites, num_trajectories=38000):
        """
        Level 2: Autonomous agents generate their own tasks and explore.
        Creates 38K trajectories with agent-driven interaction.
        """
        print("Level 2: Autonomous Exploration")

        for traj_idx in range(num_trajectories):
            # Sample website
            website = random.choice(websites)

            # Initialize autonomous agent
            agent = AutonomousExplorer()

            # Agent generates own objective
            objective = agent.generate_objective()

            trajectory = {
                'website': website,
                'objective': objective,
                'interactions': [],
                'type': 'autonomous_exploration'
            }

            # Agent explores to achieve objective
            for step in range(random.randint(10, 50)):
                # Agent decides action based on current state
                browser_state = get_browser_state()
                action = agent.decide_action(browser_state, objective)

                # Record interaction
                before_state = browser_state
                perform_web_action(action)
                after_state = get_browser_state()

                interaction = {
                    'action': action,
                    'before_state': before_state,
                    'after_state': after_state
                }
                trajectory['interactions'].append(interaction)

                # Check if objective achieved
                if agent.is_objective_achieved():
                    trajectory['success'] = True
                    break

            self.trajectories.append(trajectory)
            self.stats['autonomous_exploration'] += 1

            if (traj_idx + 1) % 5000 == 0:
                print(f"Collected {traj_idx + 1} autonomous trajectories")

    def level_3_task_oriented_execution(self, task_corpus, num_trajectories=94000):
        """
        Level 3: Synthetic web tasks with human-written instructions.
        Creates 94K trajectories with structured objectives.
        """
        print("Level 3: Task-Oriented Execution")

        for traj_idx in range(num_trajectories):
            # Sample task from corpus
            task = random.choice(task_corpus)
            website = task['website']
            instruction = task['instruction']

            trajectory = {
                'website': website,
                'instruction': instruction,
                'interactions': [],
                'type': 'task_oriented',
                'success': False
            }

            # Execute task
            for step in range(max_steps := 30):
                # Get current state
                before_state = get_browser_state()

                # Use instruction to decide action
                action = decide_task_action(before_state, instruction)

                # Perform action
                perform_web_action(action)
                after_state = get_browser_state()

                interaction = {
                    'action': action,
                    'before_state': before_state,
                    'after_state': after_state
                }
                trajectory['interactions'].append(interaction)

                # Check task completion
                if check_task_completion(after_state, task):
                    trajectory['success'] = True
                    break

            self.trajectories.append(trajectory)
            self.stats['task_oriented'] += 1

            if (traj_idx + 1) % 10000 == 0:
                print(f"Collected {traj_idx + 1} task-oriented trajectories")

    def get_collection_stats(self):
        """Return collection statistics."""
        return {
            'total': sum(self.stats.values()),
            'breakdown': self.stats,
            'diversity_score': self.compute_diversity()
        }

    def compute_diversity(self):
        """Measure dataset diversity across sources."""
        websites = set()
        for traj in self.trajectories:
            websites.add(traj.get('website'))
        return len(websites) / len(self.trajectories)
```

Autoregressive world model architecture:

```python
class AutoregressiveWorldModel(nn.Module):
    """
    Predict next browser state given current state and action.
    Trained on 1M+ real web interaction trajectories.
    """

    def __init__(self, vocab_size, hidden_dim=2048, num_layers=24,
                 model_size='14B'):
        super().__init__()
        self.hidden_dim = hidden_dim
        self.model_size = model_size

        # Transformer backbone for state prediction
        self.backbone = TransformerLM(
            vocab_size=vocab_size,
            hidden_dim=hidden_dim,
            num_layers=num_layers,
            num_heads=32
        )

        # Action encoder
        self.action_encoder = nn.Embedding(num_actions := 1000,
                                          hidden_dim)

    def predict_next_state(self, current_state, action,
                          interaction_history, format='html'):
        """
        Predict next browser state in specified format.
        Supports A11y Trees, HTML, XML, Markdown.
        """
        # Tokenize current state
        state_tokens = tokenize_state(current_state, format)

        # Encode action
        action_embedding = self.action_encoder(action)

        # Append action to state sequence
        full_sequence = torch.cat([
            state_tokens,
            action_embedding.unsqueeze(0)
        ], dim=0)

        # Generate next state tokens autoregressively
        with torch.no_grad():
            logits = self.backbone(full_sequence)

        # Sample next state tokens
        next_state_tokens = sample_next_tokens(
            logits, temperature=0.7, max_tokens=512)

        # Decode tokens to state
        next_state = decode_state(next_state_tokens, format)

        return next_state

    def generate_trajectory(self, initial_state, instruction,
                           max_steps=30, format='html'):
        """
        Generate complete trajectory given initial state and instruction.
        """
        trajectory = {
            'initial_state': initial_state,
            'instruction': instruction,
            'interactions': [],
            'states': [initial_state]
        }

        current_state = initial_state

        for step in range(max_steps):
            # Decide action based on instruction and current state
            action = decide_action(current_state, instruction)

            # Predict next state
            next_state = self.predict_next_state(
                current_state, action, trajectory['interactions'],
                format=format)

            trajectory['interactions'].append({
                'action': action,
                'from_state': current_state,
                'to_state': next_state
            })
            trajectory['states'].append(next_state)

            current_state = next_state

        return trajectory
```

Chain-of-thought synthesis for reasoning:

```python
class ReasoningInjection:
    """
    Inject explicit reasoning through chain-of-thought synthesis.
    Improves reasoning capability without requiring massive annotation.
    """

    def __init__(self, cot_generator, sample_size=1000):
        self.cot_gen = cot_generator
        self.sample_size = sample_size

    def inject_reasoning_into_dataset(self, trajectories):
        """
        Add CoT reasoning to subset of trajectories.
        Improves reasoning without expensive full annotation.
        """
        # Sample subset for CoT synthesis
        sample = random.sample(trajectories, self.sample_size)

        annotated_trajectories = []

        for traj in sample:
            # Generate reasoning for trajectory
            state = traj['interactions'][0]['before_state']
            action = traj['interactions'][0]['action']

            # Generate CoT explanation
            reasoning = self.cot_gen.explain_action(
                state, action, traj.get('instruction', ''))

            # Add reasoning to trajectory
            annotated_traj = copy.deepcopy(traj)
            annotated_traj['reasoning'] = reasoning
            annotated_trajectories.append(annotated_traj)

        return annotated_trajectories
```

Multi-format state representation:

```python
class MultiFormatStateRepresentation:
    """
    Support multiple state formats for flexibility.
    Enables transfer to code, GUI, game environments.
    """

    @staticmethod
    def state_to_a11y_tree(dom_tree):
        """Convert DOM to accessibility tree (high-level structure)."""
        a11y = {
            'type': 'root',
            'children': [],
            'text': ''
        }
        # Traverse DOM and build accessibility structure
        return a11y

    @staticmethod
    def state_to_html(dom_tree):
        """Convert to HTML representation."""
        return dom_to_html_string(dom_tree)

    @staticmethod
    def state_to_markdown(dom_tree):
        """Convert to readable Markdown."""
        markdown = []
        for element in traverse_dom(dom_tree):
            if element.tag == 'h1':
                markdown.append(f"# {element.text}")
            elif element.tag == 'button':
                markdown.append(f"[Button: {element.text}]")
        return '\n'.join(markdown)

    @staticmethod
    def state_to_xml(dom_tree):
        """Convert to XML representation."""
        return dom_to_xml_string(dom_tree)
```

## Practical Guidance

**When to use**:
- Training web agents at scale
- Need diverse, realistic interaction data
- Want agents that generalize across websites
- Have limited real API/browser access for training

**Data collection strategy**:

1. **Level 1 (Randomized)**: 60-70% of total
   - Fast to collect
   - Natural interaction patterns
   - Budget: minimal (automated)

2. **Level 2 (Autonomous)**: 10-15% of total
   - Agent-driven objectives
   - Diverse exploration strategies
   - Budget: moderate (agent overhead)

3. **Level 3 (Task-Oriented)**: 20-30% of total
   - Structured objectives
   - Higher quality signal
   - Budget: higher (task synthesis/validation)

**Model sizing recommendations**:
- 8B: Fast training/inference, good for simple tasks
- 14B: Balanced (recommended for most applications)
- 32B: Highest quality, slower inference

**Format selection**:
- A11y Trees: Fast processing, good structure extraction
- HTML: Detailed, but verbose
- Markdown: Concise, human-readable
- XML: Structured, good for element relationships
- Use multiple formats during training for robustness

**Reasoning injection**:
- Annotate 5-10% of training data with CoT reasoning
- Focus on complex state transitions
- Use GPT-4 or similar for high-quality CoT
- Include in trajectory dataset for training

**Expected performance**:
- WebArena benchmark: +9.2% over baselines
- GPT-4o comparable performance on many tasks
- Strong generalization to code, GUI, games
- 30+ step trajectories maintain coherence
- 1M trajectories approach 50 billion tokens

**Training considerations**:
- Batch size: 256-512 (depending on hardware)
- Learning rate: 1e-4 for fine-tuning, 1e-5 for continued pre-training
- Warmup steps: 5,000-10,000
- Eval frequency: every 5,000 steps
- Total training: 100-200 hours on 8xH100

**Agent fine-tuning on WebWorld**:
1. Initialize agent with language model weights
2. Fine-tune on WebWorld-generated trajectories
3. Use behavior cloning for 1,000-5,000 steps
4. Then fine-tune with RL on real tasks
5. Achieves competitive performance with 10× less real data

## Reference

Large-scale autoregressive world models trained on authentic web interactions enable efficient agent training in simulation. By combining randomized, autonomous, and task-oriented data collection with multi-format representation and reasoning injection, WebWorld creates a generalizable training environment that captures real web complexity at scale.

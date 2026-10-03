---
name: state-thoughts
title: "STATe-of-Thoughts: Structured Action Templates for Tree-of-Thoughts"
version: 0.0.2
engine: skillxiv-v0.0.2-claude-opus-4.6
license: MIT
url: "https://arxiv.org/abs/2602.14265"
keywords: [Chain-of-Thought, Tree-of-Thoughts, Structured Reasoning, Action Templates, Problem Solving]
description: "Guide multi-step reasoning through structured action templates that decompose problems into discrete, executable steps. STATe improves exploration efficiency in tree-of-thoughts by constraining action space while maintaining reasoning flexibility."
---

# STATe-of-Thoughts: Structured Action Templates for Reasoning

## Problem Context

Tree-of-Thoughts (ToT) explores reasoning paths by considering multiple next steps at each node. However, without structure, the action space becomes enormous, making it expensive to explore deeply. Standard ToT generates free-form text for next steps, causing:

1. **Redundant exploration**: Similar reasoning attempted multiple ways
2. **Invalid continuations**: Actions incompatible with problem structure
3. **High token cost**: Sampling many candidate actions
4. **Poor tree efficiency**: Wide but shallow vs deep exploration

## Core Concept

STATe-of-Thoughts introduces **structured action templates** that decompose problem-solving into discrete, templated steps. Rather than free-form generation, each reasoning step must fit a predefined action template appropriate to the problem domain. Templates constrain the action space (reducing exploration breadth) while maintaining flexibility in reasoning content.

The key insight: structure doesn't reduce reasoning power—it focuses exploration on relevant actions, improving tree depth and solution quality while reducing token cost.

## Architecture Overview

- **Action Template Library**: Domain-specific templates for problem types
- **Template-Based Action Generation**: Fill-in-the-blank structure
- **Valid Action Filtering**: Only valid template instances in tree
- **Step-Wise Decomposition**: Each node has discrete, structured actions
- **Template Selection Policy**: Choose appropriate template per state
- **Efficiency Metrics**: Reduced tokens while maintaining or improving solution quality
- **Domain Specialization**: Custom templates for math, code, planning, etc.

## Implementation

Action template system:

```python
class ActionTemplateLibrary:
    """
    Structured action templates for different problem types.
    Templates constrain action space while maintaining flexibility.
    """

    def __init__(self):
        self.templates = {
            'math_problem': [
                'Identify what we know: {facts}',
                'What do we need to find? {goal}',
                'Apply {formula} to {variables}',
                'Calculate {operation} between {operands}',
                'Check if {condition} is true',
                'Simplify {expression} using {rule}',
                'Substitute {value} for {variable}',
                'Verify the answer: {verification}'
            ],
            'code_problem': [
                'Read the input: {input_description}',
                'Define {variable} to store {purpose}',
                'Loop through {collection} and {operation}',
                'Check if {condition}, then {action}',
                'Call {function} with arguments {args}',
                'Debug by printing {debug_info}',
                'Return {result}',
                'Test with example: {example}'
            ],
            'planning_problem': [
                'Current state: {current_state}',
                'Goal state: {goal_state}',
                'Possible action: {action_description}',
                'Preconditions: {preconditions}',
                'Effects: {effects}',
                'Evaluate progress: {progress_measure}',
                'Choose best next action: {chosen_action}',
                'Update state: {new_state}'
            ],
            'reasoning_problem': [
                'Question: {question}',
                'Relevant fact: {fact}',
                'Inference rule: {rule}',
                'Apply rule: {rule} to {facts}',
                'Intermediate conclusion: {conclusion}',
                'Next question: {next_question}',
                'Combine conclusions: {conclusion1} and {conclusion2}',
                'Final answer: {answer}'
            ]
        }

    def get_templates_for_problem(self, problem_type):
        """Retrieve action templates for problem type."""
        return self.templates.get(problem_type, [])

    def instantiate_template(self, template, **kwargs):
        """
        Fill in template with specific values.
        Returns: complete action string
        """
        action = template
        for key, value in kwargs.items():
            action = action.replace(f"{{{key}}}", str(value))
        return action
```

Template-based action generation:

```python
class StructuredActionGenerator(nn.Module):
    """
    Generate actions by selecting and filling action templates.
    Constrains action space while maintaining flexibility.
    """

    def __init__(self, template_library, model):
        super().__init__()
        self.templates = template_library
        self.model = model

    def select_template(self, state, problem_type):
        """
        Decide which action template best fits current state.
        Uses neural network to score template appropriateness.
        """
        available_templates = self.templates.get_templates_for_problem(
            problem_type)

        # Score each template for current state
        state_embedding = self.model.embed_state(state)

        template_scores = []
        for template in available_templates:
            template_embedding = self.model.embed_template(template)
            score = torch.cosine_similarity(
                state_embedding.unsqueeze(0),
                template_embedding.unsqueeze(0)
            )
            template_scores.append(score)

        # Select best template (or sample from distribution)
        template_idx = torch.argmax(
            torch.tensor(template_scores)).item()
        selected_template = available_templates[template_idx]

        return selected_template, template_scores

    def fill_template_slots(self, template, state, problem_context):
        """
        Generate content for template slots.
        Uses model to complete placeholders.
        """
        # Extract slots from template
        import re
        slots = re.findall(r'\{(\w+)\}', template)

        slot_values = {}

        for slot in slots:
            # Generate appropriate value for slot
            prompt = f"""
Current state: {state}
Problem: {problem_context}
Complete the template slot '{slot}':
"""
            slot_value = self.model.generate(
                prompt, max_tokens=20, temperature=0.7)
            slot_values[slot] = slot_value

        return slot_values

    def generate_structured_actions(self, state, problem_type,
                                    num_actions=3):
        """
        Generate multiple structured action candidates.
        """
        actions = []

        # Select templates (could sample multiple)
        available_templates = self.templates.get_templates_for_problem(
            problem_type)

        for _ in range(num_actions):
            # Random template sampling for diversity
            template = random.choice(available_templates)

            # Fill slots
            slot_values = self.fill_template_slots(
                template, state, problem_type)

            # Instantiate template
            action = self.templates.instantiate_template(
                template, **slot_values)

            actions.append({
                'action': action,
                'template': template,
                'slots': slot_values
            })

        return actions
```

Tree-of-Thoughts with structured actions:

```python
class StructuredTreeOfThoughts:
    """
    Tree-of-Thoughts that uses structured action templates.
    Improves exploration efficiency through constrained action space.
    """

    def __init__(self, action_generator, value_function):
        self.action_gen = action_generator
        self.value_fn = value_function
        self.tree = None

    def expand_node(self, state, problem_type, num_actions=3):
        """
        Expand node by generating structured action candidates.
        """
        # Generate template-based actions
        actions = self.action_gen.generate_structured_actions(
            state, problem_type, num_actions=num_actions)

        # Score actions
        action_scores = []
        for action_dict in actions:
            # Evaluate action quality
            score = self.value_fn.score_action(
                state, action_dict['action'], problem_type)
            action_scores.append(score)

        # Sort by score
        sorted_actions = sorted(
            zip(actions, action_scores),
            key=lambda x: x[1],
            reverse=True
        )

        return [action for action, score in sorted_actions]

    def search(self, initial_state, problem_type, max_depth=5,
               max_width=3):
        """
        Tree-of-Thoughts search with structured actions.
        """
        self.tree = {
            'root': {
                'state': initial_state,
                'children': [],
                'depth': 0,
                'action': None
            }
        }

        queue = [self.tree['root']]
        solutions = []

        while queue and len(solutions) == 0:
            current = queue.pop(0)

            if current['depth'] >= max_depth:
                continue

            # Expand node with structured actions
            actions = self.expand_node(
                current['state'], problem_type, num_actions=max_width)

            for action_dict in actions:
                action = action_dict['action']

                # Simulate action
                next_state = self.simulate_action(
                    current['state'], action)

                # Check if solution
                if self.is_solution(next_state, problem_type):
                    solutions.append({
                        'solution': next_state,
                        'path': self.reconstruct_path(
                            current, action)
                    })
                    continue

                # Add to tree
                child = {
                    'state': next_state,
                    'parent': current,
                    'action': action,
                    'depth': current['depth'] + 1,
                    'children': []
                }
                current['children'].append(child)
                queue.append(child)

        return solutions

    def reconstruct_path(self, node, final_action):
        """Reconstruct reasoning path from root to solution."""
        path = []
        current = node

        while current.get('action'):
            path.insert(0, current['action'])
            current = current['parent']

        path.append(final_action)
        return path
```

Efficiency metrics:

```python
class StructuredToTMetrics:
    """
    Measure efficiency gains from structured templates.
    """

    @staticmethod
    def compute_exploration_efficiency(tree, problem_type):
        """
        Measure quality of exploration vs token cost.
        """
        # Count nodes in tree
        num_nodes = count_tree_nodes(tree)

        # Measure solution quality
        best_solution = find_best_solution(tree)
        solution_quality = evaluate_solution(best_solution)

        # Estimate token cost
        token_cost = estimate_token_usage(tree)

        # Efficiency = quality per token
        efficiency = solution_quality / token_cost

        return {
            'num_nodes': num_nodes,
            'solution_quality': solution_quality,
            'token_cost': token_cost,
            'efficiency': efficiency
        }

    @staticmethod
    def compare_structured_vs_freeform(structured_tree,
                                       freeform_tree):
        """
        Compare structured ToT vs traditional ToT.
        """
        structured_metrics = StructuredToTMetrics.compute_exploration_efficiency(
            structured_tree, 'math_problem')
        freeform_metrics = StructuredToTMetrics.compute_exploration_efficiency(
            freeform_tree, 'math_problem')

        comparison = {
            'structured_quality': structured_metrics['solution_quality'],
            'freeform_quality': freeform_metrics['solution_quality'],
            'quality_improvement': (
                structured_metrics['solution_quality'] /
                freeform_metrics['solution_quality']),
            'token_reduction': (
                1 - structured_metrics['token_cost'] /
                freeform_metrics['token_cost']),
            'efficiency_improvement': (
                structured_metrics['efficiency'] /
                freeform_metrics['efficiency'])
        }

        return comparison
```

## Practical Guidance

**When to use**:
- Multi-step reasoning problems (math, code, planning)
- Need to improve exploration efficiency
- Want more explainable reasoning paths
- Have domain knowledge to create templates

**Creating action templates**:

1. **Identify problem structure**: What are the discrete reasoning steps?
2. **Define templates**: Create fill-in-the-blank templates for each step
3. **Parameter specification**: What slots need filling? What type of content?
4. **Ordering constraints**: What templates can follow what others?
5. **Validity checking**: How to validate template instantiation?

**Template design patterns**:

```
Math: Identify → Define → Apply formula → Calculate → Verify
Code: Read input → Initialize variables → Loop/branch → Return → Test
Planning: Current state → Goal → Actions → Preconditions → Effects
Reasoning: Question → Fact → Rule → Inference → Conclusion
```

**Domain-specific templates**:

- **Math problems**: Algebraic operations, geometric relationships
- **Code generation**: Input reading, variable initialization, control flow
- **Planning**: State transitions, action preconditions/effects
- **Natural language**: Named entity recognition, relation extraction

**Configuration**:
- Template library size: 8-15 templates per problem type
- Actions per node: 3-5 (balance exploration vs cost)
- Tree depth: 5-10 (problem-dependent)
- Template selection: Neural scoring vs random sampling

**Expected improvements**:
- 30-50% token reduction vs freeform ToT
- Maintained or improved solution quality
- Faster exploration with structured paths
- More explainable reasoning traces
- Better generalization across similar problems

**Common pitfalls**:
- Templates too rigid (reduce reasoning power)
- Templates too loose (don't constrain enough)
- Missing common reasoning patterns
- Slot-filling quality matters for template effectiveness

**Integration with existing systems**:
- Replace free-form generation with template selection
- Can combine with CoT, in-context learning
- Works with most backbone models (GPT, Claude, etc.)
- Compatible with various tree search strategies

## Reference

Structured action templates guide multi-step reasoning by decomposing problems into discrete, constrained actions while maintaining reasoning flexibility. STATe-of-Thoughts improves exploration efficiency in tree search by reducing the action space while preserving solution quality, enabling deeper exploration with lower token cost.

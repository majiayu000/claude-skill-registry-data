---
name: m3-bench-tool-use
title: "M3-Bench: Multi-Modal Multi-Hop Multi-Threaded Tool-Using MLLM Agent Benchmark"
version: 0.0.2
engine: skillxiv-v0.0.2-claude-opus-4.6
license: MIT
url: "https://arxiv.org/abs/2511.17729"
keywords: [Multimodal Agents, Tool Use, Benchmark Design, Agent Evaluation, MCP Protocol]
description: "Design and evaluate multimodal agents for tool use with M3-Bench: assess three interconnected dimensions (multi-modal grounding, multi-hop causality, multi-threaded parallelism) using similarity-bucketed Hungarian alignment for transparent tool call evaluation without LLM judges."
---

# M3-Bench: Evaluating Multimodal Tool-Using Agents

Existing agent benchmarks typically measure single-capability tasks. This skill demonstrates how to design M3-Bench, a comprehensive evaluation framework for multimodal agents that simultaneously tests three critical capabilities: grounding visual information for tool selection, maintaining causal chains across multiple steps, and recognizing parallelizable operations for concurrent execution.

The core innovation is similarity-bucketed Hungarian alignment—transparent tool evaluation without relying on subjective LLM judges—enabling auditable assessment of agent reasoning.

## Core Concept

M3-Bench evaluates agents on three interconnected dimensions:

1. **Multi-Modal Capability**: Agent grounds decisions in image+text inputs before selecting tools
2. **Multi-Hop Reasoning**: Agent maintains causal dependency chains across sequential steps
3. **Multi-Threaded Execution**: Agent recognizes independent operations that can execute in parallel

## Architecture Overview

- **Task Specification Format**: Defines multi-modal inputs, sequential and parallel operations, ground truth tool calls
- **Agent Interface**: Standard Model Context Protocol (MCP) for tool definition
- **Evaluation Metrics**: Similarity matching and Hungarian assignment for transparent scoring
- **Transparency Layer**: Auditable correspondence between predicted and reference tool calls
- **Dimension-Specific Tests**: Separate scenarios stressing each capability

## Implementation Steps

Building and evaluating with M3-Bench requires task design, execution, and assessment.

**1. Define Task Specification Format**

Create structured format capturing multi-modal, multi-hop, multi-threaded properties.

```python
from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class ToolCall:
    """Represents a single tool invocation."""
    tool_name: str
    arguments: Dict[str, Any]
    returns: Any = None
    execution_time: float = None

@dataclass
class SequentialStep:
    """Sequential operation depending on previous steps."""
    step_id: str
    tools_to_call: List[ToolCall]
    depends_on: List[str] = None  # IDs of prerequisite steps

@dataclass
class ParallelGroup:
    """Group of operations that can execute concurrently."""
    step_ids: List[str]
    operations: List[SequentialStep]

@dataclass
class M3BenchTask:
    """Complete M3-Bench evaluation task."""
    task_id: str
    description: str

    # Multi-modal inputs
    image: Any  # PIL Image or tensor
    text_query: str

    # Ground truth solution
    sequential_steps: List[SequentialStep]
    parallel_groups: List[ParallelGroup]
    expected_final_answer: str

    # Metadata
    difficulty_level: str  # 'easy', 'medium', 'hard'
    required_capabilities: List[str]  # ['visual_grounding', 'multi_hop', 'parallelism']

    def to_task_spec(self):
        """Convert to standard task specification for agents."""
        return {
            'image': self.image,
            'query': self.text_query,
            'instructions': self.description
        }
```

**2. Create Tool Registry with MCP Interface**

Define tools agents can use following Model Context Protocol.

```python
class MCPToolRegistry:
    """
    Tool registry implementing Model Context Protocol.
    Agents discover and call tools through standardized interface.
    """
    def __init__(self):
        self.tools = {}
        self.call_history = []

    def register_tool(self, name: str, description: str, schema: Dict[str, Any]):
        """
        Register a tool with description and argument schema.
        Args:
            name: Tool identifier (e.g., 'search_web')
            description: Human-readable description
            schema: JSON schema of tool arguments
        """
        self.tools[name] = {
            'name': name,
            'description': description,
            'schema': schema
        }

    def get_tool_list(self) -> List[Dict]:
        """Return list of available tools (for agent discovery)."""
        return list(self.tools.values())

    def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """
        Execute a tool call.
        Args:
            tool_name: Name of tool to invoke
            arguments: Tool arguments matching schema
        Returns:
            result: Tool execution result
        """
        if tool_name not in self.tools:
            raise ValueError(f"Tool '{tool_name}' not found")

        # Log call for evaluation
        call_record = {
            'tool': tool_name,
            'arguments': arguments,
            'timestamp': time.time()
        }
        self.call_history.append(call_record)

        # Actual tool execution (implementation-specific)
        result = self._execute_tool(tool_name, arguments)

        call_record['result'] = result
        return result

    def _execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """Execute tool (implementation varies by tool)."""
        if tool_name == 'search_web':
            return search_web_impl(arguments['query'])
        elif tool_name == 'extract_text':
            return extract_text_impl(arguments['image'])
        # ... more tool implementations ...
        else:
            raise NotImplementedError(f"No implementation for {tool_name}")

    def get_call_trace(self) -> List[Dict]:
        """Return execution trace for evaluation."""
        return self.call_history
```

**3. Implement Similarity-Based Tool Call Matching**

Create transparent evaluation without LLM judges.

```python
class ToolCallEvaluator:
    """
    Evaluate predicted tool calls against ground truth.
    Uses similarity-bucketed Hungarian alignment for transparency.
    """
    def __init__(self, similarity_threshold=0.5):
        self.similarity_threshold = similarity_threshold

    def compute_tool_call_similarity(self, predicted: ToolCall, reference: ToolCall) -> float:
        """
        Compute similarity between predicted and reference tool calls.
        Returns score in [0, 1].
        """
        # Name matching
        name_match = 1.0 if predicted.tool_name == reference.tool_name else 0.0

        if name_match == 0.0:
            return 0.0  # Wrong tool entirely

        # Argument matching
        arg_similarity = self._compare_arguments(predicted.arguments, reference.arguments)

        # Combined score
        similarity = 0.7 * name_match + 0.3 * arg_similarity

        return similarity

    def _compare_arguments(self, predicted: Dict, reference: Dict) -> float:
        """Compare argument dictionaries."""
        if not reference:
            return 1.0 if not predicted else 0.5

        matching_keys = set(predicted.keys()) & set(reference.keys())
        total_keys = set(predicted.keys()) | set(reference.keys())

        if not total_keys:
            return 1.0

        # Score by key overlap
        key_score = len(matching_keys) / len(total_keys)

        # Score by value similarity
        value_scores = []
        for key in matching_keys:
            pred_val = predicted[key]
            ref_val = reference[key]

            if isinstance(pred_val, str) and isinstance(ref_val, str):
                # String similarity (e.g., BLEU or semantic similarity)
                val_sim = self._string_similarity(pred_val, ref_val)
            elif isinstance(pred_val, (int, float)) and isinstance(ref_val, (int, float)):
                # Numeric proximity
                val_sim = 1.0 / (1.0 + abs(pred_val - ref_val))
            else:
                # Exact match
                val_sim = 1.0 if pred_val == ref_val else 0.0

            value_scores.append(val_sim)

        value_score = np.mean(value_scores) if value_scores else 0.0

        return 0.6 * key_score + 0.4 * value_score

    def _string_similarity(self, s1: str, s2: str) -> float:
        """Compute string similarity (e.g., token overlap)."""
        tokens1 = set(s1.lower().split())
        tokens2 = set(s2.lower().split())

        if not tokens1 or not tokens2:
            return 1.0 if s1 == s2 else 0.0

        intersection = tokens1 & tokens2
        union = tokens1 | tokens2

        return len(intersection) / len(union)

    def evaluate_tool_sequence(
        self,
        predicted_calls: List[ToolCall],
        reference_calls: List[ToolCall]
    ) -> Dict[str, Any]:
        """
        Evaluate predicted tool call sequence against reference.
        Uses Hungarian algorithm for optimal matching.
        """
        # Compute similarity matrix
        n_pred = len(predicted_calls)
        n_ref = len(reference_calls)

        similarity_matrix = np.zeros((n_pred, n_ref))

        for i, pred_call in enumerate(predicted_calls):
            for j, ref_call in enumerate(reference_calls):
                similarity_matrix[i, j] = self.compute_tool_call_similarity(pred_call, ref_call)

        # Apply Hungarian algorithm for optimal assignment
        from scipy.optimize import linear_sum_assignment

        # Convert to cost matrix (minimize error = maximize similarity)
        cost_matrix = 1.0 - similarity_matrix

        row_ind, col_ind = linear_sum_assignment(cost_matrix)

        # Compute metrics
        matched_pairs = list(zip(row_ind, col_ind))
        matches = [similarity_matrix[i, j] for i, j in matched_pairs]

        correct_count = sum(1 for sim in matches if sim >= self.similarity_threshold)
        accuracy = correct_count / max(n_ref, 1)

        # Precision, recall
        precision = correct_count / max(n_pred, 1)
        recall = correct_count / max(n_ref, 1)

        return {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'matched_pairs': matched_pairs,
            'similarity_scores': matches
        }
```

**4. Evaluate Multi-Hop Reasoning**

Test agent's ability to maintain causal dependencies.

```python
def evaluate_multi_hop_reasoning(task: M3BenchTask, agent_execution_trace: List[Dict]) -> Dict:
    """
    Evaluate agent's multi-hop reasoning capability.
    Checks whether agent maintains correct causal orderings.
    Args:
        task: M3-Bench task with ground truth sequential steps
        agent_execution_trace: Recorded tool calls and results
    Returns:
        metrics: Multi-hop reasoning evaluation metrics
    """
    # Extract dependency graph from ground truth
    ground_truth_deps = {}
    for step in task.sequential_steps:
        ground_truth_deps[step.step_id] = step.depends_on or []

    # Extract agent's implicit dependencies from execution order
    agent_execution_order = [call['tool'] for call in agent_execution_trace]

    # Check: did agent execute in valid topological order?
    def is_valid_execution_order(execution_order, dependencies):
        """Check if execution respects dependencies."""
        executed = set()

        for operation in execution_order:
            # Get dependencies for this operation
            deps = dependencies.get(operation, [])

            # Check if all dependencies executed
            if not all(dep in executed for dep in deps):
                return False

            executed.add(operation)

        return True

    valid_order = is_valid_execution_order(agent_execution_order, ground_truth_deps)

    # Measure: how many causal relationships did agent respect?
    respect_count = 0
    total_deps = 0

    for step_id, deps in ground_truth_deps.items():
        for dep in deps:
            total_deps += 1

            # Check if dep executed before step_id in agent's trace
            try:
                dep_idx = agent_execution_order.index(dep)
                step_idx = agent_execution_order.index(step_id)

                if dep_idx < step_idx:
                    respect_count += 1

            except ValueError:
                pass  # Tool not in trace

    causal_respect_rate = respect_count / max(total_deps, 1)

    return {
        'valid_execution_order': valid_order,
        'causal_respect_rate': causal_respect_rate,
        'steps_executed': len(agent_execution_order),
        'ground_truth_steps': len(task.sequential_steps)
    }
```

**5. Evaluate Multi-Threaded Parallelism**

Assess agent's ability to identify parallelizable operations.

```python
def evaluate_parallelism_recognition(
    task: M3BenchTask,
    agent_execution_trace: List[Dict]
) -> Dict:
    """
    Evaluate agent's ability to recognize parallelizable operations.
    Args:
        task: Contains ground truth parallel groups
        agent_execution_trace: Agent's actual execution
    Returns:
        metrics: Parallelism evaluation metrics
    """
    # Extract agent's implicit parallelization from timestamps
    call_timeline = []

    for call in agent_execution_trace:
        call_timeline.append({
            'tool': call['tool'],
            'start': call.get('timestamp', 0),
            'end': call.get('timestamp', 0) + call.get('execution_time', 0)
        })

    # Find concurrent calls (overlapping time ranges)
    concurrent_groups = []

    for i, call1 in enumerate(call_timeline):
        concurrent_group = [i]

        for j, call2 in enumerate(call_timeline[i+1:], start=i+1):
            # Check overlap: call1.end > call2.start and call1.start < call2.end
            if call1['end'] > call2['start'] and call1['start'] < call2['end']:
                concurrent_group.append(j)

        if len(concurrent_group) > 1:
            concurrent_groups.append(concurrent_group)

    # Compare to ground truth parallel groups
    ground_truth_parallel = []
    for group in task.parallel_groups:
        ground_truth_parallel.extend(group.step_ids)

    # Measure: how many parallelizable operations did agent recognize?
    recognized_parallelizable = 0

    for group_indices in concurrent_groups:
        tools_in_group = [call_timeline[idx]['tool'] for idx in group_indices]

        # Check if these are actually parallelizable in ground truth
        for step in task.sequential_steps:
            if step.step_id in ground_truth_parallel:
                if any(tool in [t.tool_name for t in step.tools_to_call] for tool in tools_in_group):
                    recognized_parallelizable += 1

    parallelism_rate = recognized_parallelizable / max(len(ground_truth_parallel), 1)

    return {
        'concurrent_groups_found': len(concurrent_groups),
        'parallelizable_operations_recognized': recognized_parallelizable,
        'ground_truth_parallelizable': len(ground_truth_parallel),
        'parallelism_recognition_rate': parallelism_rate
    }
```

**6. Compute Aggregate M3 Score**

Combine the three capabilities into unified assessment.

```python
def compute_m3_score(
    task: M3BenchTask,
    agent_output: Dict,
    execution_trace: List[Dict],
    weights: Dict[str, float] = None
) -> Dict:
    """
    Compute comprehensive M3 score combining all three dimensions.
    Args:
        task: M3-Bench task
        agent_output: Agent's tool calls
        execution_trace: Execution record
        weights: Weights for [multi-modal, multi-hop, multi-threaded]
    Returns:
        m3_score: Unified score and component breakdown
    """
    if weights is None:
        weights = {'multi_modal': 0.33, 'multi_hop': 0.33, 'multi_threaded': 0.33}

    evaluator = ToolCallEvaluator()

    # Multi-modal component: tool selection accuracy
    tool_eval = evaluator.evaluate_tool_sequence(
        agent_output['tool_calls'],
        task.sequential_steps[0].tools_to_call  # Simplified: use first step
    )
    multi_modal_score = tool_eval['accuracy']

    # Multi-hop component: causal reasoning
    multi_hop_eval = evaluate_multi_hop_reasoning(task, execution_trace)
    multi_hop_score = multi_hop_eval['causal_respect_rate']

    # Multi-threaded component: parallelism recognition
    parallel_eval = evaluate_parallelism_recognition(task, execution_trace)
    multi_threaded_score = parallel_eval['parallelism_recognition_rate']

    # Aggregate M3 score
    m3_score = (
        weights['multi_modal'] * multi_modal_score +
        weights['multi_hop'] * multi_hop_score +
        weights['multi_threaded'] * multi_threaded_score
    )

    return {
        'm3_score': m3_score,
        'components': {
            'multi_modal': multi_modal_score,
            'multi_hop': multi_hop_score,
            'multi_threaded': multi_threaded_score
        },
        'details': {
            'tool_selection': tool_eval,
            'causal_reasoning': multi_hop_eval,
            'parallelism': parallel_eval
        }
    }
```

## Practical Guidance

**When to Use M3-Bench:**
- Evaluating multimodal agents with complex tool-use workflows
- Assessing agent reasoning quality without subjective LLM judgment
- Benchmarking progress on multi-step task automation
- Auditing agent decision-making in critical applications

**When NOT to Use:**
- Single-tool tasks or simple VQA (overkill for complexity)
- Scenarios requiring subjective quality judgment (not covered)
- Real-time evaluation (setup overhead)

**Key Design Principles:**
- **Transparency**: Hungarian matching makes evaluation auditable
- **Composability**: Test each dimension (M, M, M) independently or combined
- **Scalability**: Vectorize similarity computation for large benchmarks

**Benchmark Construction Tips:**
- Create tasks at multiple difficulty levels (easy→hard)
- Vary number of sequential steps (3, 5, 10+)
- Vary parallelism opportunities (none, some, many)
- Include both visual-heavy and text-heavy tasks for balanced evaluation

**Integration with LLMs:**
M3-Bench works with any agent implementing MCP protocol. Supports Claude, open-source models, or custom agents through standard tool interface.

## Reference

Research paper: https://arxiv.org/abs/2511.17729

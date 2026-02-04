---
name: cns-tinker
description: Apply Chiral Narrative Synthesis (CNS) framework for contradiction detection and multi-source analysis using Tinker API for model training. Use when implementing CNS with Tinker for fine-tuning models on contradiction detection, training on SciFact/FEVER datasets, or building multi-agent debate systems for narrative synthesis.
---

# Chiral Narrative Synthesis with Tinker

Practical guide for implementing CNS 3.0 using Tinker's training API for contradiction detection and narrative synthesis.

## CNS 3.0 Architecture with Tinker

CNS 3.0 uses LoRA fine-tuning via Tinker to create specialized models for:
1. **Contradiction Detection**: Identifying chiral pairs in narratives
2. **Evidence Scoring**: Evaluating claim support via Fisher Information
3. **Multi-Agent Debate**: Orchestrating L/R perspective models
4. **Synthesis Generation**: Producing coherent narratives from invariants

## Training Pipeline

### Phase 1: Contradiction Detection Model

Train a model to identify contradictory claims (chiral pairs) using SciFact/FEVER datasets.
```python
import tinker
from tinker import types
from tinker_cookbook import renderers
from tinker_cookbook.tokenizer_utils import get_tokenizer

# Initialize Tinker client
service_client = tinker.ServiceClient()
training_client = service_client.create_lora_training_client(
    base_model="Qwen/Qwen3-30B-A3B",
    rank=32  # CNS typically needs moderate rank for nuanced detection
)

# Setup renderer for contradiction detection
tokenizer = get_tokenizer("Qwen/Qwen3-30B-A3B")
renderer = renderers.get_renderer("qwen3", tokenizer)

# Create contradiction detection prompt
def create_contradiction_prompt(claim_a: str, claim_b: str) -> list:
    """Format chiral pair for contradiction detection."""
    system_msg = """You are a contradiction detection expert. Analyze pairs of claims and determine if they represent contradictory statements about the same event or fact. Respond with: CONTRADICTORY, SUPPORTING, or NEUTRAL."""
    
    user_msg = f"""Claim A: {claim_a}
Claim B: {claim_b}

Analyze if these claims contradict each other."""
    
    return [
        {"role": "system", "content": system_msg},
        {"role": "user", "content": user_msg}
    ]

# Process SciFact/FEVER data into training format
def build_cns_training_data(examples: list) -> list[types.Datum]:
    """Convert contradiction dataset to Tinker training format."""
    data = []
    
    for ex in examples:
        messages = create_contradiction_prompt(
            ex["claim_a"], 
            ex["claim_b"]
        )
        messages.append({
            "role": "assistant",
            "content": ex["label"]  # CONTRADICTORY/SUPPORTING/NEUTRAL
        })
        
        # Use renderer to build supervised example
        tokens, weights = renderer.build_supervised_example(messages)
        
        # Shift for next-token prediction
        input_tokens = tokens[:-1]
        target_tokens = tokens[1:]
        weights = weights[1:]
        
        datum = types.Datum(
            model_input=types.ModelInput.from_ints(input_tokens),
            loss_fn_inputs={
                "target_tokens": target_tokens,
                "weights": weights
            }
        )
        data.append(datum)
    
    return data

# Training loop for contradiction detection
async def train_contradiction_detector(
    training_data: list[types.Datum],
    steps: int = 1000,
    learning_rate: float = 3e-4  # Use CNS-optimized LR for Qwen
):
    """Fine-tune model for contradiction detection."""
    
    for step in range(steps):
        # Forward-backward pass
        fwd_bwd_future = await training_client.forward_backward_async(
            training_data,
            loss_fn="cross_entropy"
        )
        
        # Optimizer step
        optim_future = await training_client.optim_step_async(
            types.AdamParams(learning_rate=learning_rate)
        )
        
        # Wait for completion
        fwd_bwd_result = await fwd_bwd_future
        optim_result = await optim_future
        
        # Log metrics
        if step % 100 == 0:
            metrics = fwd_bwd_result.metrics
            print(f"Step {step}: Loss = {metrics.get('loss:sum', 0):.4f}")
    
    # Save contradiction detector weights
    detector_path = training_client.save_weights_for_sampler(
        name="contradiction-detector"
    ).result().path
    
    return detector_path
```

### Phase 2: Multi-Agent Debate System

Use trained model to create L/R perspective agents for debate.
```python
from tinker_cookbook.completers import TinkerMessageCompleter

async def create_debate_agents(detector_path: str):
    """Create left-handed and right-handed narrative agents."""
    
    # Create sampling client from trained detector
    sampling_client = service_client.create_sampling_client(
        model_path=detector_path
    )
    
    # Wrap in message completer for structured debate
    base_completer = TinkerMessageCompleter(
        sampling_client=sampling_client,
        renderer=renderer,
        sampling_params=types.SamplingParams(
            max_tokens=512,
            temperature=0.7,
            top_p=0.9
        )
    )
    
    return base_completer

async def run_multi_agent_debate(
    completer,
    claim_left: str,
    claim_right: str,
    rounds: int = 3
) -> dict:
    """Execute CNS multi-agent debate between L/R narratives."""
    
    debate_history = []
    
    for round_num in range(rounds):
        # Agent L presents evidence
        l_prompt = [{
            "role": "user",
            "content": f"""You are Agent L defending: "{claim_left}"
Round {round_num + 1}: Present your strongest evidence and challenge Agent R's position."""
        }]
        
        l_response = await completer(l_prompt)
        debate_history.append({"agent": "L", "content": l_response["content"]})
        
        # Agent R counters
        r_prompt = [{
            "role": "user", 
            "content": f"""You are Agent R defending: "{claim_right}"
Round {round_num + 1}: Counter Agent L's argument and present your evidence.
Agent L said: {l_response['content']}"""
        }]
        
        r_response = await completer(r_prompt)
        debate_history.append({"agent": "R", "content": r_response["content"]})
    
    return {
        "debate_history": debate_history,
        "left_claim": claim_left,
        "right_claim": claim_right
    }
```

### Phase 3: RL-Based Evidence Scoring

Use reinforcement learning to train Fisher Information scoring.
```python
from tinker_cookbook.rl.types import Env, StepResult, Observation, Action

class CNSEvidenceEnv(Env):
    """RL environment for training evidence scoring via Fisher Information."""
    
    def __init__(self, claim_pair: tuple[str, str], ground_truth: str):
        self.claim_left, self.claim_right = claim_pair
        self.ground_truth = ground_truth
        self.renderer = None  # Set during initialization
    
    async def initial_observation(self):
        """Present chiral pair for scoring."""
        prompt_tokens = self.renderer.build_generation_prompt([{
            "role": "user",
            "content": f"""Score the information quality of these claims:
Left: {self.claim_left}
Right: {self.claim_right}

Provide Fisher Information score (0.0-1.0) for each claim."""
        }])
        
        stop_condition = self.renderer.get_stop_sequences()
        return prompt_tokens, stop_condition
    
    async def step(self, action: Action) -> StepResult:
        """Evaluate scoring accuracy using Fisher Information metric."""
        
        # Parse agent's scores
        response_text = self.renderer.parse_response(action.tokens)[0]["content"]
        
        # Extract scores (simplified - real implementation would be more robust)
        try:
            # Expect format: "Left: 0.X, Right: 0.Y"
            scores = self._parse_scores(response_text)
            
            # Calculate reward based on alignment with ground truth
            reward = self._compute_fisher_information_reward(
                scores, 
                self.ground_truth
            )
        except:
            reward = -1.0  # Penalty for invalid format
        
        return StepResult(
            observation=None,  # Terminal state
            reward=reward,
            done=True
        )
    
    def _compute_fisher_information_reward(
        self, 
        scores: dict, 
        truth: str
    ) -> float:
        """Reward higher Fisher Information for correct claim."""
        
        # If left claim is correct, reward high left score
        if truth == "left":
            return scores["left"] - scores["right"]
        else:
            return scores["right"] - scores["left"]
```

### Phase 4: Synthesis with Topological Invariants

Generate unified narrative from debate using persistence features.
```python
async def synthesize_narrative(
    debate_result: dict,
    detector_path: str
) -> str:
    """Synthesize coherent narrative from chiral debate using topological invariants."""
    
    # Create synthesis client
    sampling_client = service_client.create_sampling_client(
        model_path=detector_path
    )
    
    # Extract debate context
    debate_summary = "\n".join([
        f"{turn['agent']}: {turn['content'][:200]}..."
        for turn in debate_result["debate_history"]
    ])
    
    # Build synthesis prompt
    synthesis_prompt = renderer.build_generation_prompt([{
        "role": "system",
        "content": """You are a narrative synthesis expert using topological data analysis. Extract topological invariants (facts preserved across both narratives) and synthesize a unified truth."""
    }, {
        "role": "user",
        "content": f"""Debate between contradictory narratives:

Left Claim: {debate_result['left_claim']}
Right Claim: {debate_result['right_claim']}

Debate History:
{debate_summary}

Task: Identify topological invariants (facts both sides agree on) and synthesize the most likely truth."""
    }])
    
    # Generate synthesis
    response = await sampling_client.sample_async(
        prompt=synthesis_prompt,
        num_samples=1,
        sampling_params=types.SamplingParams(
            max_tokens=1024,
            temperature=0.3,  # Lower temp for coherent synthesis
            stop=renderer.get_stop_sequences()
        )
    )
    
    synthesis_tokens = response.sequences[0].tokens
    synthesis_message = renderer.parse_response(synthesis_tokens)[0]
    
    return synthesis_message["content"]
```

## Complete CNS Pipeline
```python
import asyncio

async def run_cns_pipeline(
    source_a_text: str,
    source_b_text: str,
    training_data_path: str
):
    """Execute full CNS 3.0 pipeline with Tinker."""
    
    # 1. Train contradiction detector (if not already trained)
    print("Training contradiction detector...")
    training_data = load_scifact_fever_data(training_data_path)
    detector_path = await train_contradiction_detector(
        build_cns_training_data(training_data)
    )
    
    # 2. Extract chiral pairs from sources
    print("Extracting contradictions...")
    chiral_pairs = await extract_chiral_pairs(
        source_a_text, 
        source_b_text,
        detector_path
    )
    
    # 3. Run multi-agent debate for each pair
    print("Running multi-agent debates...")
    debate_results = []
    completer = await create_debate_agents(detector_path)
    
    for pair in chiral_pairs:
        debate = await run_multi_agent_debate(
            completer,
            pair["left"],
            pair["right"],
            rounds=3
        )
        debate_results.append(debate)
    
    # 4. Synthesize final narrative
    print("Synthesizing unified narrative...")
    final_synthesis = ""
    for debate in debate_results:
        synthesis = await synthesize_narrative(debate, detector_path)
        final_synthesis += f"\n\n{synthesis}"
    
    return {
        "chiral_pairs": chiral_pairs,
        "debates": debate_results,
        "synthesis": final_synthesis
    }

# Usage
if __name__ == "__main__":
    result = asyncio.run(run_cns_pipeline(
        source_a_text="Article claiming Event X at time T1...",
        source_b_text="Article claiming Event X at time T2...",
        training_data_path="./scifact_fever_combined.jsonl"
    ))
    
    print("=== CNS SYNTHESIS ===")
    print(result["synthesis"])
```

## Dataset Preparation for CNS

### SciFact Format
```python
def prepare_scifact_for_cns(scifact_path: str) -> list:
    """Convert SciFact dataset to CNS training format."""
    import json
    
    examples = []
    with open(scifact_path) as f:
        for line in f:
            item = json.loads(line)
            
            examples.append({
                "claim_a": item["claim"],
                "claim_b": item["evidence"],
                "label": "SUPPORTING" if item["label"] == "SUPPORT" 
                        else "CONTRADICTORY" if item["label"] == "CONTRADICT"
                        else "NEUTRAL"
            })
    
    return examples
```

### FEVER Format
```python
def prepare_fever_for_cns(fever_path: str) -> list:
    """Convert FEVER dataset to CNS training format."""
    import json
    
    examples = []
    with open(fever_path) as f:
        for line in f:
            item = json.loads(line)
            
            # FEVER has claim + evidence sentences
            for evidence in item.get("evidence", []):
                examples.append({
                    "claim_a": item["claim"],
                    "claim_b": evidence[2],  # Evidence text
                    "label": "SUPPORTING" if item["label"] == "SUPPORTS"
                            else "CONTRADICTORY" if item["label"] == "REFUTES"  
                            else "NEUTRAL"
                })
    
    return examples
```

## Hyperparameters for CNS
```python
CNS_TRAINING_CONFIG = {
    # Model selection (prefer MoE for cost-effectiveness)
    "base_model": "Qwen/Qwen3-30B-A3B",  # Hybrid model for thinking
    
    # LoRA configuration
    "lora_rank": 32,  # Moderate rank for nuanced detection
    
    # Training hyperparameters
    "learning_rate": 3e-4,  # Optimal for Qwen-30B with LoRA
    "batch_size": 128,
    "num_steps": 1000,
    
    # Sampling for debate
    "temperature": 0.7,  # Balance creativity and coherence
    "max_tokens": 512,
    "top_p": 0.9,
    
    # CNS-specific
    "debate_rounds": 3,
    "fisher_information_threshold": 0.6,
    "persistence_min_threshold": 0.5  # Minimum persistence for invariants
}
```

## Performance Optimization

### Batch Processing Chiral Pairs
```python
async def batch_process_contradictions(
    pairs: list[tuple[str, str]],
    detector_path: str,
    batch_size: int = 32
) -> list:
    """Process multiple chiral pairs efficiently."""
    
    sampling_client = service_client.create_sampling_client(
        model_path=detector_path
    )
    
    results = []
    
    for i in range(0, len(pairs), batch_size):
        batch = pairs[i:i+batch_size]
        
        # Create prompts for batch
        prompts = [
            renderer.build_generation_prompt(
                create_contradiction_prompt(left, right)
            )
            for left, right in batch
        ]
        
        # Process batch in parallel
        futures = [
            sampling_client.sample_async(
                prompt=p,
                num_samples=1,
                sampling_params=types.SamplingParams(
                    max_tokens=128,
                    temperature=0.1
                )
            )
            for p in prompts
        ]
        
        responses = await asyncio.gather(*futures)
        results.extend(responses)
    
    return results
```

## Evaluation Metrics
```python
def evaluate_cns_performance(predictions: list, ground_truth: list) -> dict:
    """Evaluate CNS contradiction detection accuracy."""
    
    correct = sum(
        1 for pred, truth in zip(predictions, ground_truth)
        if pred["label"] == truth["label"]
    )
    
    accuracy = correct / len(predictions)
    
    # Calculate per-class metrics
    from collections import defaultdict
    class_correct = defaultdict(int)
    class_total = defaultdict(int)
    
    for pred, truth in zip(predictions, ground_truth):
        class_total[truth["label"]] += 1
        if pred["label"] == truth["label"]:
            class_correct[truth["label"]] += 1
    
    class_accuracy = {
        label: class_correct[label] / class_total[label]
        for label in class_total
    }
    
    return {
        "overall_accuracy": accuracy,
        "class_accuracy": class_accuracy,
        "total_examples": len(predictions)
    }
```

## Troubleshooting

### Low Contradiction Detection Accuracy

1. **Increase LoRA rank**: Try rank=64 or rank=128 for more capacity
2. **More training data**: Combine SciFact + FEVER + custom examples  
3. **Adjust learning rate**: Use `get_lr()` from hyperparam_utils
4. **Better prompts**: Add few-shot examples to system message

### Debate Not Converging

1. **Lower temperature**: Use 0.3-0.5 for more focused arguments
2. **More debate rounds**: Increase from 3 to 5 rounds
3. **Add judge model**: Use separate model to score arguments

### Poor Synthesis Quality

1. **Use larger model**: Switch to Qwen3-235B-A22B for complex synthesis
2. **Lower synthesis temperature**: Use 0.1-0.3 for coherent output
3. **Explicit invariant extraction**: Add step to explicitly list agreements

## Version History

- **v3.0** (Current): Tinker API integration, LoRA fine-tuning, structured debate
- **v2.0**: Fisher Information Metrics, multi-agent framework
- **v1.0**: Initial topological approach

## References

- Tinker Docs: https://tinker-docs.thinkingmachines.ai
- SciFact Dataset: https://github.com/allenai/scifact
- FEVER Dataset: https://fever.ai
- CNS Framework: [Internal documentation]

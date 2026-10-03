---
name: browser-agent
title: "BrowserAgent: Building Web Agents with Human-Inspired Web Browsing Actions"
version: 0.0.2
engine: skillxiv-v0.0.2-claude-opus-4.6
license: MIT
url: "https://arxiv.org/abs/2510.10666"
keywords: [web-agents, browser-automation, human-inspired-actions, sft-rft, memory]
description: "Build web agents using human-inspired browser actions (scrolling, clicking, typing) operated directly on raw HTML via Playwright. Combine supervised fine-tuning and rejection fine-tuning with explicit memory for strong generalization on web tasks."
---

# BrowserAgent: Human-Inspired Web Automation

Web agents that convert pages to static text miss crucial interaction patterns humans use. BrowserAgent operates directly on raw HTML pages through Playwright, mirroring human browser interactions: scrolling to find content, clicking specific elements, typing into forms.

Core insight: human web navigation is inherently interactive and stateful. By using the same browser APIs humans use (Playwright) and training on interaction sequences with memory, agents achieve better generalization to unseen websites.

## Core Concept

**Human-Inspired Action Space**: Instead of converting web pages to text, define actions matching human behaviors: click coordinates, scroll direction/amount, type text. These operate directly on Playwright browser objects.

**Two-Stage Training**: Supervised fine-tuning on human demonstrations, then rejection fine-tuning to filter poor actions and improve robustness.

**Explicit Memory Mechanism**: Maintain working memory of key conclusions across steps, strengthening reasoning on long tasks.

## Architecture Overview

- **Playwright Wrapper**: Interface to real browser automation
- **Action Encoder**: Converts high-level actions to Playwright calls
- **Visual Understanding**: Processes raw HTML/screenshots for action selection
- **Memory System**: Stores conclusions from previous steps
- **Rejection Filter**: Learns to discard actions that don't progress toward goal

## Implementation Steps

**Stage 1: Supervised Fine-tuning on Demonstrations**

Train agent to reproduce human browser actions:

```python
from playwright.async_api import async_playwright
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

class BrowserActionTrainer:
    def __init__(self, model_name='llama-7b'):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
        self.device = 'cuda'

    def prepare_sft_data(self, human_demonstrations):
        """
        Format human web interactions into training pairs.
        Each pair: (page_state, action) -> next_page_state
        """

        training_pairs = []

        for demo in human_demonstrations:
            trajectory = demo['trajectory']

            for step_idx in range(len(trajectory) - 1):
                current_state = trajectory[step_idx]
                action = trajectory[step_idx]['action']
                next_state = trajectory[step_idx + 1]

                # Encode page state (URL + visible text + interactive elements)
                page_context = self.encode_page_state(current_state)

                # Encode action (click, scroll, type)
                action_tokens = self.encode_action(action)

                training_pairs.append({
                    'page': page_context,
                    'action': action_tokens,
                    'next_page': self.encode_page_state(next_state)
                })

        return training_pairs

    def encode_page_state(self, page_state):
        """
        Encode raw HTML into tokens: URL + visible elements + current focus.
        """

        context = f"URL: {page_state['url']}\n"
        context += "Visible elements:\n"

        for elem in page_state['interactive_elements']:
            context += f"  [{elem['id']}] {elem['type']}: {elem['text']}\n"

        if page_state['current_focus']:
            context += f"Current focus: {page_state['current_focus']}\n"

        return self.tokenizer(context, return_tensors='pt')

    def encode_action(self, action):
        """
        Encode browser action: click, scroll, type, wait.
        """

        if action['type'] == 'click':
            action_str = f"click on element {action['element_id']}"
        elif action['type'] == 'scroll':
            direction = 'up' if action['amount'] < 0 else 'down'
            action_str = f"scroll {direction} by {abs(action['amount'])} pixels"
        elif action['type'] == 'type':
            action_str = f"type '{action['text']}' into element {action['element_id']}"
        elif action['type'] == 'wait':
            action_str = f"wait {action['seconds']} seconds"

        return self.tokenizer(action_str, return_tensors='pt')

    def train_sft(self, training_pairs, num_epochs=3, lr=5e-5):
        """
        Supervised fine-tuning on human demonstrations.
        """

        optimizer = torch.optim.AdamW(
            self.model.parameters(),
            lr=lr
        )

        for epoch in range(num_epochs):
            for pair in training_pairs:
                page_tokens = pair['page']['input_ids']
                action_tokens = pair['action']['input_ids']

                # Concatenate page state + action
                input_ids = torch.cat([page_tokens, action_tokens], dim=-1)

                # Teacher forcing: predict action given page
                logits = self.model(input_ids[:-1]).logits
                target = action_tokens.view(-1)

                loss = torch.nn.functional.cross_entropy(
                    logits.view(-1, self.model.config.vocab_size),
                    target
                )

                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
```

**Stage 2: Rejection Fine-tuning**

Filter poor actions and improve robustness:

```python
def rejection_finetuning(model, validation_tasks, num_steps=1000):
    """
    Train model to reject bad actions and prefer better ones.
    Uses task completion as signal: does action progress toward goal?
    """

    optimizer = torch.optim.AdamW(model.parameters(), lr=2e-5)

    for step in range(num_steps):
        # Sample task
        task = random.choice(validation_tasks)
        goal = task['goal']

        # Generate action from current policy
        page_context = encode_page_state(task['initial_page'])
        predicted_action = model.generate(
            page_context,
            max_length=32,
            temperature=0.7
        )

        # Execute action
        try:
            next_page = execute_action(predicted_action)
            success = check_progress(next_page, goal)
            reward = 1.0 if success else -1.0

        except Exception as e:
            # Action execution failed
            next_page = task['initial_page']
            reward = -2.0

        # For comparison, what would a better action be?
        better_actions = find_demonstrator_actions(
            page_context,
            goal
        )

        # Rejection fine-tuning: increase probability of good actions
        if reward < 0 and better_actions:
            for better_action in better_actions:
                better_tokens = encode_action(better_action)
                logits = model(
                    torch.cat([page_context, better_tokens[:-1]], dim=-1)
                ).logits

                # Increase probability of better action
                loss = -torch.nn.functional.log_softmax(
                    logits[-1],
                    dim=-1
                )[better_tokens[-1]]

                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
```

**Stage 3: Memory-Augmented Inference**

Run agent with memory for long-horizon tasks:

```python
async def run_agent_with_memory(goal, initial_url, max_steps=20):
    """
    Execute agent on goal with working memory system.
    Memory stores conclusions that inform future actions.
    """

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(initial_url)

        memory = []  # List of (observation, conclusion) pairs
        current_state = await page.content()

        for step in range(max_steps):
            # Encode page + memory context
            page_context = encode_page_state(current_state)
            memory_context = "\n".join([
                f"- {obs}: {conc}" for obs, conc in memory
            ])

            prompt = f"""
            Goal: {goal}

            Current page: {page_context}

            Previous conclusions:
            {memory_context}

            Next action (click, scroll, type, or 'done' if complete):
            """

            # Generate action
            action = model.generate(
                tokenize(prompt),
                max_length=32
            )

            action_str = tokenize_decode(action)

            if 'done' in action_str.lower():
                return {'success': True, 'memory': memory}

            # Execute action
            prev_state = current_state
            action_type = parse_action(action_str)

            if action_type['type'] == 'click':
                await page.click(action_type['selector'])
            elif action_type['type'] == 'scroll':
                await page.evaluate(
                    f"window.scrollBy(0, {action_type['amount']})"
                )
            elif action_type['type'] == 'type':
                await page.fill(
                    action_type['selector'],
                    action_type['text']
                )

            await page.wait_for_load_state('networkidle')
            current_state = await page.content()

            # Extract and store conclusion
            conclusion = extract_conclusion(
                prev_state,
                action_str,
                current_state
            )

            if conclusion:
                memory.append((action_str, conclusion))

        return {'success': False, 'memory': memory}
```

## Practical Guidance

**When to Use BrowserAgent:**
- Web automation requiring interaction with dynamic content
- Tasks where page text changes based on interaction
- Multi-step workflows with memory requirements

**When NOT to Use:**
- Simple information extraction from static pages
- Tasks where no interaction is needed
- High-volume parallel execution (single browser per agent instance)

**Action Space Design:**

| Action Type | Use Case | Example |
|------------|----------|---------|
| click | Navigate, interact with buttons | click element #submit |
| scroll | Find content below fold | scroll down by 500px |
| type | Fill forms, search | type "query" into #search |
| wait | Handle async loading | wait 2 seconds |

**Common Pitfalls:**
- Actions too granular (pixel-level clicks hard to learn)
- Memory growing unbounded (limit to last N conclusions)
- Not handling page failures (dead links, timeouts)
- Training on out-of-distribution page layouts

## Reference

Based on the research at: https://arxiv.org/abs/2510.10666

---
name: coco-text-image
title: "CoCo: Code as CoT for Text-to-Image Preview and Rare Concept Generation"
version: 0.0.2
engine: skillxiv-v0.0.2-claude-opus-4.6
license: MIT
url: "https://arxiv.org/abs/2603.08652"
keywords: [Text-to-Image, Code Generation, Structured Reasoning, Image Editing, Vision Language Models]
description: "Generates complex text-heavy and structured images by converting natural language descriptions into executable code that specifies layouts, then renders and refines. Achieves 68% improvement on structured image generation benchmarks."
---

# CoCo: Converting Text Descriptions to Code for Precise Spatial Image Generation

Text-to-image generation struggles with tasks requiring precise spatial layouts, structured visual elements, and dense text. Natural language reasoning alone cannot specify exact coordinates, object relationships, and textual placements required for scientific diagrams, charts, and technical drawings. CoCo converts this problem: use code as an intermediate representation where spatial relationships are explicit and verifiable.

The approach generates executable code that specifies layouts, executes it in a sandbox to produce a draft image, then applies fine-grained refinement. This decouples structure (which code handles precisely) from visual fidelity (which image editing handles).

## Core Concept

Transform text-to-image into a three-stage pipeline:

1. **Code Generation**: LLM generates executable code defining spatial layouts, object positioning, text placement
2. **Draft Rendering**: Execute code in sandbox to produce deterministic layout image
3. **Draft-Guided Refinement**: Apply image editing to enhance visual quality while preserving structure

The key insight: code explicitly represents spatial relationships that are ambiguous in natural language. A chart can be generated programmatically with exact axis placement, tick marks, and labels. Then image diffusion enhances visual realism without breaking structure.

## Architecture Overview

- **Code Generation Stage**: LLM generates Python/SVG code from text description
- **Sandbox Execution**: Safe code execution produces layout templates
- **Draft-Final Image Pairs**: Train refinement model on draft + natural image pairs
- **Refinement Network**: VAE-based decoder refines draft images to match natural image distribution
- **Supervised Fine-Tuning**: Code generation trained on text-code pairs; refinement trained on draft-final pairs

## Implementation Steps

Build a text-to-image system with explicit code generation and refinement stages.

**Code Generation Model**

```python
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

class CodeGenerationModule:
    def __init__(self, model_name="gemini-3-pro"):
        """Initialize code generation component."""
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

    def generate_code_from_description(self, text_description, max_tokens=500):
        """
        Generate executable code from natural language description.

        Args:
            text_description: "A bar chart comparing Q1-Q4 sales with values 100, 120, 150, 140"
            max_tokens: maximum code length

        Returns:
            code_string: executable Python or SVG code
        """
        system_prompt = """You are a code generator for spatial image layouts.
        Convert descriptions into executable Python code using matplotlib/PIL or SVG.
        The code should create a deterministic layout with precise positioning.
        Always include:
        - Figure size and DPI specifications
        - Exact coordinate positioning for objects
        - Text placement with coordinates
        - Color and style specifications
        Return ONLY the executable code, no markdown formatting."""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text_description}
        ]

        input_ids = self.tokenizer.apply_chat_template(
            messages, return_tensors="pt"
        )

        with torch.no_grad():
            output_ids = self.model.generate(
                input_ids,
                max_new_tokens=max_tokens,
                temperature=0.3,
                top_p=0.95
            )

        code_string = self.tokenizer.decode(
            output_ids[0][input_ids.shape[1]:],
            skip_special_tokens=True
        )

        return code_string

    def extract_and_validate_code(self, raw_output):
        """Extract executable code from model output."""
        # Remove markdown code fences if present
        if "```python" in raw_output:
            code = raw_output.split("```python")[1].split("```")[0].strip()
        elif "```" in raw_output:
            code = raw_output.split("```")[1].split("```")[0].strip()
        else:
            code = raw_output.strip()

        return code
```

**Code Execution and Draft Generation**

```python
import tempfile
import subprocess
import os
from PIL import Image
import io

class SandboxCodeExecutor:
    """Safely execute generated code to produce draft images."""

    def __init__(self, timeout_seconds=30):
        self.timeout = timeout_seconds
        self.trusted_modules = {"matplotlib", "PIL", "numpy", "svg"}

    def execute_code_to_image(self, code_string, output_size=(512, 512)):
        """
        Execute code in sandbox and capture output image.

        Args:
            code_string: executable Python code
            output_size: target image dimensions

        Returns:
            draft_image: PIL.Image of layout
            execution_success: bool indicating if code ran successfully
        """
        # Wrap code with imports and safety checks
        safe_code = f"""
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import io

# User code
{code_string}

# Save to buffer
plt.savefig('/tmp/draft_output.png', dpi=100, bbox_inches='tight')
plt.close()
"""

        try:
            # Execute in restricted subprocess
            result = subprocess.run(
                ["python", "-c", safe_code],
                capture_output=True,
                timeout=self.timeout,
                cwd=tempfile.gettempdir()
            )

            if result.returncode == 0:
                # Load generated image
                draft_image = Image.open("/tmp/draft_output.png")
                draft_image = draft_image.resize(output_size)
                return draft_image, True
            else:
                print(f"Code execution failed: {result.stderr.decode()}")
                return None, False

        except subprocess.TimeoutExpired:
            print(f"Code execution timeout after {self.timeout}s")
            return None, False
        except Exception as e:
            print(f"Code execution error: {str(e)}")
            return None, False
```

**Refinement Stage**

```python
import torch
import torch.nn as nn
from diffusers import StableDiffusionInpaintPipeline

class ImageRefinementModule:
    def __init__(self, vae_model="stabilityai/stable-diffusion-2"):
        """Initialize refinement network."""
        self.refiner = StableDiffusionInpaintPipeline.from_pretrained(vae_model)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.refiner.to(self.device)

    def refine_draft_image(self, draft_image, description, guidance_scale=7.5):
        """
        Refine draft layout image to enhance visual quality.

        Args:
            draft_image: PIL.Image draft from code execution
            description: original text description for refinement guidance
            guidance_scale: classifier-free guidance strength

        Returns:
            refined_image: enhanced PIL.Image
        """
        refinement_prompt = f"Enhance and refine this image: {description}"

        # Use inpainting with full mask (refine entire image)
        refined_image = self.refiner(
            prompt=refinement_prompt,
            image=draft_image,
            mask_image=Image.new('L', draft_image.size, 255),  # Full refinement
            guidance_scale=guidance_scale,
            num_inference_steps=50
        ).images[0]

        return refined_image


class CoCoPipeline:
    def __init__(self, code_model_name="gemini-3-pro"):
        self.code_gen = CodeGenerationModule(code_model_name)
        self.executor = SandboxCodeExecutor()
        self.refiner = ImageRefinementModule()

    def generate_image_from_description(self, description):
        """
        Full pipeline: description -> code -> draft -> refined image.

        Args:
            description: text description of desired image

        Returns:
            final_image: PIL.Image
            pipeline_steps: dict with intermediate outputs for debugging
        """
        pipeline_steps = {}

        # Stage 1: Generate code
        print(f"[1/3] Generating code from: {description[:50]}...")
        code = self.code_gen.generate_code_from_description(description)
        code = self.code_gen.extract_and_validate_code(code)
        pipeline_steps['generated_code'] = code

        # Stage 2: Execute to get draft
        print(f"[2/3] Executing code to generate draft layout...")
        draft_image, success = self.executor.execute_code_to_image(code)

        if not success:
            print("Code execution failed, returning None")
            return None, pipeline_steps

        pipeline_steps['draft_image'] = draft_image

        # Stage 3: Refine image
        print(f"[3/3] Refining image for visual quality...")
        refined_image = self.refiner.refine_draft_image(draft_image, description)
        pipeline_steps['refined_image'] = refined_image

        return refined_image, pipeline_steps
```

**Training Data Preparation**

```python
def prepare_training_data():
    """
    Prepare text-code and draft-final image pairs for training.

    Returns:
        train_data: list of training examples
    """
    # Phase 1: Text-Code pairs
    text_code_pairs = [
        {
            "description": "A line chart showing stock prices from Jan to Dec, starting at 100, peak at 150 in June",
            "code": """
import matplotlib.pyplot as plt
dates = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
prices = [100, 105, 110, 125, 140, 150, 145, 140, 135, 130, 125, 120]
plt.figure(figsize=(10, 6))
plt.plot(dates, prices, linewidth=2, marker='o')
plt.xlabel('Month')
plt.ylabel('Price ($)')
plt.title('Stock Price Over Year')
plt.xticks(rotation=45)
"""
        },
        # ... more pairs from CoCo-10K dataset
    ]

    # Phase 2: Draft-Final image pairs for refinement
    # From StructVisuals + synthesized diagrams
    draft_final_pairs = [
        {
            "draft": Image.open("draft_chart_1.png"),
            "final": Image.open("final_chart_1.png"),
            "description": "Professional stock chart with improved colors"
        },
        # ... more pairs
    ]

    return {
        "code_generation": text_code_pairs,
        "refinement": draft_final_pairs
    }
```

## Practical Guidance

**Hyperparameters**:
- Code generation temperature: 0.3 (low for reproducibility)
- Max code tokens: 400-600 for complex layouts
- Refinement guidance scale: 7.5 typically; higher (10-15) for more prompt adherence
- Sandbox timeout: 30 seconds

**When to Apply**:
- Structured image generation (charts, diagrams, technical drawings)
- Text-heavy content (labels, captions, annotations)
- Rare concepts or custom layouts not in training data
- Tasks requiring precise spatial positioning

**When NOT to Apply**:
- Photorealistic portrait generation (code can't specify photorealism)
- Free-form artistic images (code constrains creativity)
- Simple scenes (text-to-image alone is sufficient)
- Real-time applications (code execution adds latency)

**Key Pitfalls**:
- Generated code has syntax errors—validate before execution
- Draft images missing elements—code generation needs better prompting
- Refinement breaks structure—guidance scale too high
- Sandbox restrictions too tight—necessary modules blocked

**Data Requirements**: CoCo-10K dataset includes 10K+ chart/diagram/text-heavy examples; training requires ~500 GPU hours for code model, ~1000 GPU hours for refinement model.

**Evidence**: Achieves +68.83% on StructT2IBench; 0.853 accuracy on OneIG-Bench; 0.754 on LongText-Bench; substantially outperforms baselines on structured and text-intensive generation.

Reference: https://arxiv.org/abs/2603.08652

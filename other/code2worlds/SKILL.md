---
name: code2worlds
title: "Code2Worlds: Empowering Coding LLMs for 4D World Generation"
version: 0.0.2
engine: skillxiv-v0.0.2-claude-opus-4.6
license: MIT
url: "https://arxiv.org/abs/2602.11757"
keywords: [3D Generation, Physics Simulation, Code Generation, Dual-Stream Architecture, World Modeling]
description: "Generate physically grounded 4D scenes from natural language through dual-stream architecture separating object detail from scene orchestration. VLM-Motion Critic validates physics parameters iteratively, bridging semantic-physical execution gap."
---

# Code2Worlds: 4D World Generation from Code

## Problem Context

Generating realistic 3D environments with physics requires balancing two competing demands: high-fidelity individual objects and coherent global layouts. Open-loop code generation often produces "physical hallucinations" where visual structures don't align with physics. A single monolithic generator struggles with multi-scale context management. Existing methods sacrifice local detail for global structure or vice versa.

## Core Concept

Code2Worlds uses a **dual-stream architecture** to decouple concerns in 4D world generation:

1. **Object Stream**: Generates high-fidelity individual objects through retrieval-augmented parameter generation
2. **Scene Stream**: Orchestrates global environment with hierarchical planning

Rather than open-loop generation, a VLM-Motion Critic validates rendered simulations and iteratively refines physics parameters, bridging the semantic-physical execution gap. The system generates executable procedural code that creates both geometry and physics-driven animations.

## Architecture Overview

- **Dual-Stream Generation**: Object and scene streams with separate concerns
- **Retrieval-Augmented Parameters**: Library-based parameter selection for object fidelity
- **Hierarchical Scene Planning**: Multi-scale layout reasoning
- **Closed-Loop Refinement**: VLM-Motion Critic validates and refines
- **Physics Parameter Inference**: Automatic tuning of simulation parameters
- **Temporal Coherence**: Ensures physics-consistent evolution over time
- **Executable Procedural Code**: Generates Blender Python scripts or similar

## Implementation

Dual-stream architecture for 4D generation:

```python
class DualStreamWorldGenerator(nn.Module):
    """
    Generate 4D scenes through decoupled object and scene streams.
    Prevents compromise between local detail and global coherence.
    """

    def __init__(self, object_generator, scene_generator, vlm_critic):
        super().__init__()
        self.object_stream = object_generator
        self.scene_stream = scene_generator
        self.vlm_critic = vlm_critic  # VLM for validation

        # Parameter libraries for retrieval
        self.object_library = ObjectParameterLibrary()

    def generate_objects(self, semantic_description, num_objects=10):
        """
        Stream 1: Generate high-fidelity individual objects.
        Uses retrieval-augmented parameter generation.
        """
        objects = []

        for obj_idx in range(num_objects):
            # Parse object specification from description
            obj_spec = parse_object_spec(semantic_description, obj_idx)

            # Retrieval-augmented generation: find similar objects
            similar_params = self.object_library.retrieve(
                obj_spec, top_k=5)

            # Generate parameters building on retrieved examples
            object_params = self.object_stream(
                obj_spec, similar_params, embeddings=None)

            # Create object with generated parameters
            obj = {
                'type': obj_spec['type'],
                'params': object_params,
                'shape': generate_shape(object_params),
                'material': generate_material(object_params)
            }
            objects.append(obj)

        return objects

    def generate_scene_hierarchy(self, semantic_description,
                                objects, num_levels=3):
        """
        Stream 2: Orchestrate global environment hierarchically.
        Plans placement and relationships at multiple scales.
        """
        scene = {
            'objects': objects,
            'hierarchy_levels': []
        }

        for level in range(num_levels):
            # High-level: spatial relationships (room layout)
            # Mid-level: object groupings and constraints
            # Low-level: fine position adjustments

            if level == 0:
                # Room/environment scale
                layout = self.scene_stream.generate_layout(
                    semantic_description)
            elif level == 1:
                # Object grouping scale
                groups = self.scene_stream.generate_groups(
                    objects, semantic_description)
            else:
                # Fine positioning scale
                positions = self.scene_stream.generate_positions(
                    objects, groups)

            scene['hierarchy_levels'].append({
                'level': level,
                'reasoning': None,  # For interpretability
                'constraints': None
            })

        return scene

    def infer_physics_parameters(self, scene):
        """
        Infer mass, friction, elasticity, etc. for realistic physics.
        Uses object properties and scene context.
        """
        physics_params = {}

        for obj in scene['objects']:
            # Infer mass from size and material
            size = obj['params']['size']
            material = obj['params']['material']
            mass = infer_mass_from_material(material, size)

            # Infer friction from material
            friction = material_friction_lookup(material)

            # Infer elasticity from interaction context
            elasticity = infer_elasticity(material, scene)

            physics_params[obj['id']] = {
                'mass': mass,
                'friction': friction,
                'elasticity': elasticity,
                'gravity': 9.8
            }

        return physics_params

    def generate_code(self, scene, physics_params):
        """
        Generate executable Blender Python script creating 4D scene.
        Includes geometry, material, physics, and animation.
        """
        code = """
import bpy
import numpy as np
from blender_physics import RigidBody, PhysicsSimulation

# Clear scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Create objects from scene specification
"""

        # Object generation code
        for obj in scene['objects']:
            code += f"""
# {obj['type']}
obj = create_{obj['type']}(
    position={obj['params']['position']},
    scale={obj['params']['scale']},
    material='{obj['material']}'
)
"""

        # Physics simulation code
        code += """
# Apply physics parameters
sim = PhysicsSimulation()
"""
        for obj, params in physics_params.items():
            code += f"""
sim.add_rigidbody(obj, mass={params['mass']},
                  friction={params['friction']},
                  elasticity={params['elasticity']})
"""

        # Animation code
        code += """
# Run physics simulation for 240 frames (10 seconds at 24fps)
for frame in range(240):
    sim.step(dt=1/24)
    bpy.context.scene.frame_set(frame)
"""

        return code
```

Closed-loop refinement with VLM-Motion Critic:

```python
class VLMMotionCritic:
    """
    Validate and refine physics parameters through iterative evaluation.
    Bridges semantic intent with physical execution.
    """

    def __init__(self, vlm_model, physics_simulator):
        self.vlm = vlm_model
        self.simulator = physics_simulator

    def evaluate_generation(self, description, generated_scene,
                           physics_params, num_frames=120):
        """
        Evaluate how well generated scene matches description.
        Returns feedback for refinement.
        """
        # Run physics simulation
        rendered_frames = self.simulator.run(
            generated_scene, physics_params, num_frames)

        # Get VLM evaluation
        critique = self.vlm.evaluate_simulation(
            description, rendered_frames)

        return {
            'matches_description': critique['match_score'],
            'physics_plausible': critique['physics_score'],
            'temporal_coherent': critique['temporal_score'],
            'issues': critique['issues'],
            'refinement_suggestions': critique['suggestions']
        }

    def refine_physics_parameters(self, description, generated_scene,
                                  physics_params, num_iterations=3):
        """
        Iteratively refine parameters until simulation matches description.
        """
        current_params = physics_params.copy()

        for iteration in range(num_iterations):
            # Evaluate current configuration
            evaluation = self.evaluate_generation(
                description, generated_scene, current_params)

            if evaluation['matches_description'] > 0.9:
                # Sufficiently good
                break

            # Extract parameter adjustments from critique
            suggestions = evaluation['refinement_suggestions']

            # Apply parameter refinements
            for suggestion in suggestions:
                obj_id = suggestion['object']
                param_name = suggestion['parameter']
                adjustment = suggestion['adjustment']

                current_params[obj_id][param_name] += adjustment

        return current_params

    def refine_iteratively(self, description, scene, physics_params):
        """
        Full refinement loop with multiple iterations.
        """
        for round_num in range(3):  # Up to 3 refinement rounds
            refined_params = self.refine_physics_parameters(
                description, scene, physics_params)

            evaluation = self.evaluate_generation(
                description, scene, refined_params)

            if evaluation['matches_description'] > 0.85:
                return refined_params

            physics_params = refined_params

        return physics_params
```

Complete pipeline:

```python
def generate_world_from_description(description, vlm_critic,
                                    max_refinement_rounds=3):
    """
    End-to-end 4D world generation from natural language.
    """
    generator = DualStreamWorldGenerator(
        object_generator, scene_generator, vlm_critic)

    # Step 1: Generate objects with retrieval augmentation
    objects = generator.generate_objects(description)

    # Step 2: Generate scene hierarchy
    scene = generator.generate_scene_hierarchy(description, objects)

    # Step 3: Infer physics parameters
    initial_physics = generator.infer_physics_parameters(scene)

    # Step 4: Refine physics through VLM-Motion Critic
    final_physics = vlm_critic.refine_iteratively(
        description, scene, initial_physics)

    # Step 5: Generate executable code
    code = generator.generate_code(scene, final_physics)

    return {
        'scene': scene,
        'physics_params': final_physics,
        'executable_code': code,
        'rendered_preview': vlm_critic.simulator.render(
            scene, final_physics)
    }
```

## Practical Guidance

**When to use**:
- Generating complex 3D scenes with physics simulation
- Need both visual detail and physical plausibility
- Have natural language descriptions of desired environments
- Require executable scene code (Blender, Unreal, etc.)

**Dual-stream design choices**:

1. **Object Stream**: Focus on individual quality
   - Use retrieval from parameter libraries
   - Generate diverse object variations
   - Ensure material/physics properties per-object

2. **Scene Stream**: Focus on global coherence
   - Hierarchical planning at multiple scales
   - Respect spatial constraints
   - Maintain semantic consistency

**VLM-Motion Critic tuning**:
- Evaluation metrics: description match (0-1), physics plausibility (0-1), temporal coherence (0-1)
- Refinement threshold: stop when description match > 0.85
- Parameter adjustment step size: start conservative, increase if convergence slow
- Max refinement rounds: 3-5 typically sufficient

**Physics parameter inference**:
- Pre-compute material property database (mass, friction, elasticity)
- Use object size and interaction context for parameter selection
- Start conservative (high friction, low elasticity), refine via VLM feedback

**Expected improvements**:
- 41% improvement in structural quality metrics vs non-refinement baseline
- 70-80% of generated scenes require <2 refinement rounds
- Realistic physics-driven animations matching semantic descriptions
- Executable code quality enabling direct simulation

**Implementation checklist**:
1. Build/integrate object parameter library
2. Implement dual-stream generators
3. Connect to physics simulator (Blender, Isaac Sim, etc.)
4. Integrate VLM for evaluation (GPT-4V or similar)
5. Test refinement loop convergence
6. Generate Blender/engine-specific code templates

## Reference

Dual-stream architecture with closed-loop refinement enables generation of complex 4D scenes that balance semantic fidelity with physical plausibility. VLM-Motion Critic bridges the semantic-physical execution gap through iterative parameter refinement.

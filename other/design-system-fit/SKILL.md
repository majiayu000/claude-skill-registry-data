---
name: design-system-fit
description: Implement or adapt a UI feature to an existing product's visual and component conventions using representative screens and source evidence. Use when fitting an established system, not inventing a new brand direction.
---

# Design system fit

Make the requested feature feel native to its product. Learn the system from evidence, distinguishing intentional conventions from isolated defects and legacy inconsistencies.

## Establish the reference set

Inspect documented tokens, shared components, recent analogous screens, and the requested feature's task. Choose references for structural relevance, not merely proximity. Read `references/comparison-guide.md` to build a small working map of conventions and uncertainty.

Prefer explicit current design guidance and supported primitives. When documentation and rendered behavior conflict, inspect implementation and version context before choosing. Ask only when the conflict materially affects the feature. Do not copy a visibly broken pattern for consistency or infer a global rule from one screen.

## Implement in the existing language

Map the feature to existing composition, density, typography, color roles, spacing, control hierarchy, vocabulary, and state patterns. Use semantic tokens and existing components where they serve the task. Avoid a second styling system or new dependency merely to approximate what already exists.

Preserve usable product character: dense operational tools need not become spacious marketing pages. Reuse behavior as well as styling, including navigation, focus, validation, loading, and recovery. Where no suitable precedent exists, extend the smallest relevant pattern and label the choice as a new local decision.

If the user requests visual change, follow that scope rather than treating the old system as immutable. Do not expand an isolated feature into a repository-wide normalization pass.

## Verify fit and function

Compare the rendered feature against selected references using representative content and comparable dimensions. Inspect the normal state, an important non-default state, and a narrow layout where relevant. Check the underlying tokens/components as well as screenshots: similar pixels can hide incompatible duplicated styles.

Exercise the feature's main interaction, keyboard behavior, and affected shared components. Report a static-only comparison when runtime inspection is unavailable. Distinguish observed mismatches from taste preferences and explain why a proposed deviation helps the task.

Deliver the implementation and concise verification evidence. Do not claim a design-system audit or exact visual match beyond the inspected references and states.

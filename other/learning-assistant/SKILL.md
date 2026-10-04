---
name: learning-assistant
description: Orchestrates the end-to-end process of turning a resource into a learning material by delegating to resource-gatherer, syntax-interpreter, and study-builder.
---

# Learning Assistant

A high-level orchestrator for the bilingual learning workflow.

## Workflow Execution
1. **Delegate to `resource-gatherer`**: 
   - Perform adaptive resource acquisition (URL/PDF/Local Path), manage assets, and store raw files.
2. **Delegate to `syntax-interpreter`**: 
   - Perform bilingual translation and deep syntactic analysis in Chinese.
3. **Delegate to `study-builder`**: 
   - Generate comprehension tests and language exercises.

## Final Output
Assemble all parts into a cohesive Markdown document saved in the `wiki/synthesis` directory, ensuring all asset references are correctly linked to the `raw` directory.

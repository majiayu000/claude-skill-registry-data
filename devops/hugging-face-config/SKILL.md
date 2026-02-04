---
name: Hugging Face Config
description: Generate Hugging Face Spaces configuration files including runtime setup, environment variables, and deployment instructions.
---

# Hugging Face Config

## Instructions

1. Create Hugging Face Spaces configuration:
   - Generate hf-space.yaml with runtime settings
   - Create README.md with brief explanation
   - Document environment variable requirements
   - Include instructions for container execution

2. Configure for Docker runtime:
   - Specify Docker as mandatory runtime
   - Set proper port exposure (7860)
   - Configure resource allocation
   - Define startup commands

3. Document environment variables:
   - List all required variables (GEMINI_API_KEY, QDRANT_URL, etc.)
   - Provide example values and descriptions
   - Include security recommendations
   - Add validation requirements

4. Add deployment documentation:
   - Explain how to deploy to Hugging Face Spaces
   - Include troubleshooting steps
   - Document scaling considerations
   - Provide monitoring recommendations

5. Follow Context7 MCP documentation:
   - Ensure Docker runtime compatibility
   - Follow deterministic configuration patterns
   - Include proper error handling
   - Document all configuration parameters

## Examples

Input: "Create Hugging Face Spaces configuration"
Output: Creates hf-space.yaml and README.md with proper configuration for Docker deployment.
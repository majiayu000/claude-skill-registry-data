---
name: entrypoint
description: Generates entrypoint.sh script for Docker container runtime environment variable injection. Replaces placeholder values in built assets with actual environment variables at container startup.
---

# Entrypoint Script Skill

## Purpose
Generate entrypoint.sh script for Docker container runtime environment variable injection.

## Output
Create the file: `entrypoint.sh`

## Example File
See: `examples.md` in this directory for complete examples and detailed explanations.


## Notes
- Enables runtime environment variable injection into built JavaScript files
- Uses `envsubst` to replace placeholders with actual environment variable values
- Processes all app*.js files in nginx html directory
- Sets errexit and nounset for safer script execution
- Starts nginx in foreground mode for Docker container
- Requires gettext-base package for envsubst command
- Must be executable (chmod +x entrypoint.sh)

---
name: cover-image-workflow-current
description: Generate or revise a blog cover, article header, or thumbnail with verified current image tools, explicit title/logo requirements, bounded retries, private credential handling, and honest output acceptance.
license: ISC
metadata:
  source: Varnan-Tech/opendirectory
  source-commit: bc01f7c1c31f0af54c2924c1ec1abbb472ab1df4
  revision-status: experimental-unbenchmarked
---

# Generate and verify the requested image

Capture the exact title, intended dimensions, logos/assets, destination and any
visual constraints. Use the user's existing choices and authorization. Inspect
supplied assets and preserve their permitted use; ask only for missing inputs
that materially affect the result. Use the available qualified image tool.

## Qualify the implementation before making a paid request

Check the actual runtime, package lock, installed API and provider's model status.
Use current stable model identifiers; a current SDK does not make a retired
preview endpoint current. For a custom implementation, consult
[qualified implementation notes](references/qualified-implementation.md).
Keep an exact dependency graph and reproduce local response/image controls
before relying on it. An advisory audit is one check, not proof of correct output.

Keep credentials out of command arguments, logs, prompts, screenshots and source.
Prefer the configured connector or process-scoped credentials. Do not call a
plaintext configuration file a secure credential vault or persist a prompted
key without the user's requested persistence. A logo lookup sends the requested
domain/URL to a provider; use supplied assets when the task calls for local inputs.

## Accept the artifact on observable evidence

Check that returned bytes decode as the declared format with the required
dimensions. Inspect the image for exact title spelling, legibility, requested
logo identity, layout and unintended elements. A model critic is fallible:
validate its response schema and corroborate important text/logo requirements.
Neither a prompt demanding exact text nor successful API parsing proves fidelity.

Bound requests, retries, bytes, image dimensions and elapsed time. Record why an
attempt failed and use that feedback for a permitted retry. Exhausting retries
remains a failure. Do not print success or return a passing command status when
QA fails. Do not overwrite an existing destination implicitly. If the user asks
to retain a rejected draft, label it as rejected and preserve the failure status.

Present the actual artifact with its acceptance result and material remaining
limitations. Distinguish local mocked controls, real provider runs, human/visual
review and measured agent gains. This experimental skill has no established
individual performance advantage.

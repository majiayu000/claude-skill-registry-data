---
name: tofu-module
description: "Creates or refactors an OpenTofu module with the house file layout, typed and validated inputs, described outputs, a version constraint, a documented README and an examples directory. Use when a new module is needed or existing infrastructure code should become one."
---

# Module

Write a module someone else can consume without reading its internals.

## When to use

- A piece of infrastructure is used more than once or earns its own interface.
- Existing root module code has grown and should be extracted.

## Steps

1. Define the interface first: what the module owns, what it takes as input, what it returns, and
   what it deliberately leaves out. Write this into the module `README.md` before the code.
2. Check for a maintained upstream module that already does the job. Use it and say so instead of
   writing a new one.
3. Create the files: `main.tf`, `variables.tf`, `outputs.tf`, `versions.tf`, `README.md`. Provider
   configuration stays in the root module, this module only declares `required_providers`.
4. Write the variables: typed, described, a default only where safe, `validation` where a wrong
   value fails late, `sensitive = true` for a secret.
5. Implement the resources with `for_each`, stable names and no environment specific value.
6. Write only the outputs a consumer needs, each with a description. No secret in an output, even
   marked sensitive.
7. Wire the module into the root module and run the plan workflow. An extraction's first plan must
   show moves only, so use `moved` blocks or `tofu state mv`, and show that plan as evidence.
8. Document the README: purpose, inputs, outputs, an example usage block, requirements. Generate
   the inputs and outputs table with `terraform-docs` when it is available.
9. Add an `examples/` directory with at least one working call of the module.
10. Add `tofu test` cases under `tests/` where a wrong input or a wrong output would otherwise slip
    through silently. Skip it where the plan workflow already proves correctness.
11. Report the interface, the plan result and anything the module intentionally leaves out.

## Guardrails

- No provider block inside a reusable module, only `required_providers`.
- No wrapper around an upstream module that only renames its inputs.
- An extraction that changes more than the resource addresses is a bug, not a refactor.
- No secret in an output, sensitive or not.
- An in-repository submodule called by two or more environments of the same repository needs
  no `examples/` directory and no README inputs/outputs table: the environments calling it are
  the examples, and the README states purpose, inputs and outputs in prose instead.

## References

- `opentofu-conventions` for file layout, variables and state rules.
- `tofu-plan` for the plan and apply workflow used while extracting or wiring the module.
